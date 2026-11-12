/**
 * @file cTextTextureCache.cpp
 *
 * Dune 2 - The Maker
 *
 * @author Stefan Hendriks & the D2TM Team
 * @www http://www.dune2themaker.com
 * @copyright Copyright (c) 2002 - 2026 Stefan Hendriks and contributors
 * @license This software is released under the MIT License. See LICENSE.md.
 *
 * Note: Dune 2 is a trademark of Westwood Studios/Electronic Arts.
 *
 * This is a non-commercial educational project.
 */

#include "drawers/cTextTextureCache.h"
#include "drawers/SDLDrawer.hpp"

#include "include/cAssert.h"
#include "utils/Log.h"

#include <algorithm>

namespace {
TextInkBounds findInkBounds(SDL_Surface *surface)
{
    TextInkBounds result;
    if (!surface || surface->w <= 0 || surface->h <= 0) return result;

    result.textureWidth = surface->w;
    result.textureHeight = surface->h;
    result.width = surface->w;
    result.height = surface->h;

    SDL_Surface *rgba = SDL_ConvertSurface(surface, SDL_PIXELFORMAT_RGBA32);
    if (!rgba) return result;

    if (!SDL_LockSurface(rgba)) {
        SDL_DestroySurface(rgba);
        return result;
    }

    int minX = rgba->w;
    int minY = rgba->h;
    int maxX = -1;
    int maxY = -1;
    const auto *pixels = static_cast<const Uint8 *>(rgba->pixels);
    for (int y = 0; y < rgba->h; ++y) {
        const Uint8 *row = pixels + y * rgba->pitch;
        for (int x = 0; x < rgba->w; ++x) {
            if (row[x * 4 + 3] == 0) continue;
            minX = std::min(minX, x);
            minY = std::min(minY, y);
            maxX = std::max(maxX, x);
            maxY = std::max(maxY, y);
        }
    }

    SDL_UnlockSurface(rgba);
    SDL_DestroySurface(rgba);

    if (maxX >= minX && maxY >= minY) {
        result.x = minX;
        result.y = minY;
        result.width = maxX - minX + 1;
        result.height = maxY - minY + 1;
    }
    return result;
}
}

cTextTextureCache::cTextTextureCache(TTF_Font *font, SDLDrawer *renderer)
    : m_font(font), m_renderer(renderer)
{
    d2tm_assert(font != nullptr);
    d2tm_assert(renderer != nullptr);
}

cTextTextureCache::~cTextTextureCache()
{
    for (auto &pair : m_textCache) {
        auto &cacheEntry = pair.second;
        if (cacheEntry->texture) {
            SDL_DestroyTexture(cacheEntry->texture);
        }
        if (cacheEntry->shadowsTexture) {
            SDL_DestroyTexture(cacheEntry->shadowsTexture);
        }
    }
}

void cTextTextureCache::setDensity(int density) const
{
    const int normalizedDensity = std::max(1, density);
    if (normalizedDensity == m_density) return;

    for (auto &pair : m_textCache) {
        auto &cacheEntry = pair.second;
        if (cacheEntry->texture) {
            SDL_DestroyTexture(cacheEntry->texture);
        }
        if (cacheEntry->shadowsTexture) {
            SDL_DestroyTexture(cacheEntry->shadowsTexture);
        }
    }
    m_textCache.clear();
    m_density = normalizedDensity;
}

std::unique_ptr<textCacheEntry> cTextTextureCache::createCacheEntry(Color color, const std::string &msg) const
{
    auto newCacheEntry = std::make_unique<textCacheEntry>();
    SDL_Surface *textSurface = TTF_RenderText_Blended(m_font, msg.c_str(), 0, Color::Black.toSDL());
    if (!textSurface) {
        Logger::error(COMP_TEXT, "cTextTextureCache", "Failed to create shadow surface for text '{}': {}", msg, SDL_GetError());
        return nullptr;
    }
    newCacheEntry->shadowsTexture = SDL_CreateTextureFromSurface(m_renderer->getRenderer(), textSurface);
    SDL_SetTextureScaleMode(newCacheEntry->shadowsTexture, SDL_SCALEMODE_LINEAR);
    SDL_DestroySurface(textSurface);

    textSurface = TTF_RenderText_Blended(m_font, msg.c_str(), 0, color.toSDL());
    if (!textSurface) {
        Logger::error(COMP_TEXT, "cTextTextureCache", "Failed to create surface for text '{}': {}", msg, SDL_GetError());
        return nullptr;
    }
    newCacheEntry->texture = SDL_CreateTextureFromSurface(m_renderer->getRenderer(), textSurface);
    SDL_SetTextureScaleMode(newCacheEntry->texture, SDL_SCALEMODE_LINEAR);
    newCacheEntry->pixelWidth = textSurface->w;
    newCacheEntry->pixelHeight = textSurface->h;
    newCacheEntry->width = (newCacheEntry->pixelWidth + m_density - 1) / m_density;
    newCacheEntry->height = (newCacheEntry->pixelHeight + m_density - 1) / m_density;
    newCacheEntry->inkBounds = findInkBounds(textSurface);
    newCacheEntry->lifeCounter = 10;
    SDL_DestroySurface(textSurface);

    return newCacheEntry;
}

textCacheEntry* cTextTextureCache::findOrCreate(const Color color, const std::string &msg) const
{
    textKey key{msg, color};
    const auto it = m_textCache.find(key);
    if (it == m_textCache.end()) {
        auto newCacheEntry = createCacheEntry(color, msg);
        if (!newCacheEntry) {
            return nullptr;
        }
        auto result = m_textCache.emplace(key, std::move(newCacheEntry));
        return result.first->second.get();
    }
    return it->second.get();
}

void cTextTextureCache::resetCache() const
{
    auto it = m_textCache.begin();
    while (it != m_textCache.end()) {
        auto &cacheEntry = it->second;
        if (cacheEntry->lifeCounter == 0) {
            if (cacheEntry->texture) SDL_DestroyTexture(cacheEntry->texture);
            if (cacheEntry->shadowsTexture) SDL_DestroyTexture(cacheEntry->shadowsTexture);
            it = m_textCache.erase(it);
        } else {
            cacheEntry->lifeCounter = 0;
            ++it;
        }
    }
}
