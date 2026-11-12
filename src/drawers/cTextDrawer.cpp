/**
 * @file cTextDrawer.cpp
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

#include "cTextDrawer.h"
#include "debug/UiAudit.hpp"
#include "drawers/cTextTextureCache.h"
#include "game/cGameSettings.h"
#include "drawers/SDLDrawer.hpp"
#include "utils/Color.hpp"
#include "utils/TextAlignment.hpp"
#include <iostream>
#include "include/cAssert.h"

#include <algorithm>
#include <optional>

cTextDrawer::cTextDrawer(TTF_Font *theFont, TTF_Font *fallbackFont, float baseSize, cGameSettings *settings, SDLDrawer *renderer) :
    m_font(theFont),
    m_fallbackFont(fallbackFont),
    m_baseSize(baseSize),
    m_textCache(std::make_unique<cTextTextureCache>(theFont, renderer)),
    m_settings(settings),
    m_renderer(renderer)
{
    d2tm_assert(theFont != nullptr);
    d2tm_assert(settings != nullptr);
    d2tm_assert(renderer != nullptr);
}

cTextDrawer::~cTextDrawer()
{
    m_font = nullptr;
}

void cTextDrawer::drawText(int x, int y, Color color, const std::string &msg, bool applyShadow) const
{
    syncDensity();
    if (msg.empty()) return;
    auto cacheEntry = m_textCache->findOrCreate(color, msg);
    if (!cacheEntry) return;
    cacheEntry->lifeCounter += 1;
    if (uiaudit::isEnabled()) {
        uiaudit::recordText(msg, x, y, cacheEntry->width, cacheEntry->height);
    }
    const float w = cacheEntry->pixelWidth / static_cast<float>(m_density);
    const float h = cacheEntry->pixelHeight / static_cast<float>(m_density);
    if (applyShadow) {
        m_renderer->renderTexture(cacheEntry->shadowsTexture, SDL_FRect{x + 1.0F, y + 1.0F, w, h});
    }
    m_renderer->renderTexture(cacheEntry->texture, SDL_FRect{static_cast<float>(x), static_cast<float>(y), w, h});
}

void cTextDrawer::drawText(cPoint &coords, Color color, const std::string &msg, bool applyShadow) const
{
    drawText(coords.x, coords.y, color, msg, applyShadow);
}

void cTextDrawer::drawText(int x, int y, const std::string &msg, bool applyShadow) const
{
    drawText(x, y, Color::White , msg, applyShadow);
}

void cTextDrawer::drawTextCentered(const std::string &msg, int y) const
{
    drawTextCentered(msg, y, Color::White);
}

void cTextDrawer::drawTextCentered(const std::string &msg, int y, Color color) const
{
    syncDensity();
    if (msg.empty()) return;
    int w,h;
    TTF_GetStringSize(m_font, msg.c_str(), 0, &w, &h);
    w = toLogical(w); h = toLogical(h);
    int half = w / 2;
    int xPos = (m_settings->getScreenW() / 2) - half;
    drawText(xPos, y, color, msg);
}

void cTextDrawer::drawTextCenteredInBox(const std::string &msg, int x, int y, int boxWidth, int boxHeight, Color color) const
{
    syncDensity();
    if (msg.empty()) return;
    int w,h;
    TTF_GetStringSize(m_font, msg.c_str(), 0, &w, &h);
    w = toLogical(w); h = toLogical(h);
    int lenghtInPixels = w;
    int heightInPixels = h;

    int halfLengthInPixels = lenghtInPixels / 2;
    int xPos = x + ((boxWidth / 2) - halfLengthInPixels);
    int halfHeightInPixels = heightInPixels / 2;
    int yPos = y + ((boxHeight / 2) - halfHeightInPixels);
    std::optional<uiaudit::BoxScope> auditBox;
    if (uiaudit::isEnabled()) {
        auditBox.emplace(x, y, boxWidth, boxHeight);
    }
    drawText(xPos, yPos, color, msg);
}

void cTextDrawer::drawTextCenteredInBox(const std::string &msg, const cRectangle &rect, Color color) const
{
    drawTextCenteredInBox(msg, rect.getX(), rect.getY(), rect.getWidth(), rect.getHeight(), color);
}

void cTextDrawer::drawTextCenteredInBox(const std::string &msg, const cRectangle &rect, Color color, int offsetX, int offsetY) const
{
    drawTextCenteredInBox(msg, rect.getX() + offsetX, rect.getY() + offsetY, rect.getWidth(), rect.getHeight(), color);
}

void cTextDrawer::drawTextScaledCenteredInBox(
    const std::string &msg,
    const cRectangle &rect,
    float scale,
    Color color,
    bool applyShadow) const
{
    syncDensity();
    if (msg.empty()) return;
    scale = std::max(0.5F, scale);
    auto cacheEntry = m_textCache->findOrCreate(color, msg);
    cacheEntry->lifeCounter += 1;
    const int width = static_cast<int>(cacheEntry->pixelWidth * scale / m_density + 0.5F);
    const int height = static_cast<int>(cacheEntry->pixelHeight * scale / m_density + 0.5F);
    const int x = rect.getX() + (rect.getWidth() - width) / 2;
    const int y = rect.getY() + (rect.getHeight() - height) / 2;
    if (uiaudit::isEnabled()) {
        const uiaudit::Rect box{rect.getX(), rect.getY(), rect.getWidth(), rect.getHeight()};
        uiaudit::recordText(msg, x, y, width, height, &box);
    }
    if (applyShadow) {
        m_renderer->renderTexture(cacheEntry->shadowsTexture, x + 2, y + 2, width, height);
    }
    m_renderer->renderTexture(cacheEntry->texture, x, y, width, height);
}

void cTextDrawer::drawTextScaledOpticallyCenteredInBox(
    const std::string &msg,
    const cRectangle &rect,
    float scale,
    Color color,
    bool applyShadow) const
{
    syncDensity();
    if (msg.empty()) return;
    scale = std::max(0.5F, scale);
    auto cacheEntry = m_textCache->findOrCreate(color, msg);
    cacheEntry->lifeCounter += 1;
    const int width = static_cast<int>(cacheEntry->pixelWidth * scale / m_density + 0.5F);
    const int height = static_cast<int>(cacheEntry->pixelHeight * scale / m_density + 0.5F);
    const cPoint origin = calculateOpticallyCenteredTextOrigin(
        rect,
        width,
        height,
        cacheEntry->inkBounds
    );
    if (uiaudit::isEnabled()) {
        const uiaudit::Rect box{rect.getX(), rect.getY(), rect.getWidth(), rect.getHeight()};
        uiaudit::recordText(msg, origin.x, origin.y, width, height, &box);
    }
    if (applyShadow) {
        m_renderer->renderTexture(
            cacheEntry->shadowsTexture,
            origin.x + 2,
            origin.y + 2,
            width,
            height
        );
    }
    m_renderer->renderTexture(cacheEntry->texture, origin.x, origin.y, width, height);
}

void cTextDrawer::drawTextCentered(const std::string &msg, int x, int width, int y, Color color) const
{
    syncDensity();
    if (msg.empty()) return;
    int w,h;
    TTF_GetStringSize(m_font, msg.c_str(), 0, &w, &h);
    w = toLogical(w); h = toLogical(h);
    int lenghtInPixels = w;
    int half = lenghtInPixels / 2;
    int xPos = x + ((width / 2) - half);
    std::optional<uiaudit::BoxScope> auditBox;
    if (uiaudit::isEnabled()) {
        auditBox.emplace(x, y, width, getFontHeight());
    }
    drawText(xPos, y, color, msg);
}

void cTextDrawer::drawTextBottomRight(const std::string &msg, int margin) const
{
    drawTextBottomRight(Color::White, msg, margin);
}

void cTextDrawer::drawTextBottomLeft(const std::string &msg, int margin) const
{
    drawTextBottomLeft(Color::White, msg, margin);
}

void cTextDrawer::drawTextBottomRight(Color color, const std::string &msg, int margin) const
{
    syncDensity();
    if (msg.empty()) return;
    int w,h;
    TTF_GetStringSize(m_font, msg.c_str(), 0, &w, &h);
    w = toLogical(w); h = toLogical(h);
    int lenghtInPixels = w;
    int x = m_settings->getScreenW() - lenghtInPixels-margin;
    int y = m_settings->getScreenH() - getFontHeight()-20-margin;
    drawText(x, y, color, msg);
}

int cTextDrawer::getFontHeight() const
{
    syncDensity();
    return toLogical(TTF_GetFontHeight(m_font));
}

void cTextDrawer::drawTextBottomLeft(Color color, const std::string &msg, int margin) const
{
    syncDensity();
    if (msg.empty()) return;
    int w,h;
    TTF_GetStringSize(m_font, msg.c_str(), 0, &w, &h);
    w = toLogical(w); h = toLogical(h);
    int y = m_settings->getScreenH() - h-20-margin;
    drawText(margin, y, color, msg);
}

int cTextDrawer::getTextLength(const std::string &msg) const
{
    syncDensity();
    int w,h;
    TTF_GetStringSize(m_font, msg.c_str(), 0, &w, &h);
    w = toLogical(w); h = toLogical(h);
    return w;
}

cRectangle cTextDrawer::getRect(int x, int y, const std::string &msg) const
{
    return cRectangle(x, y, getTextLength(msg), getFontHeight());
}

cRectangle cTextDrawer::getAsRectangle(int x, int y, const std::string &msg) const
{
    return cRectangle(x, y, getTextLength(msg), getFontHeight());
}

void cTextDrawer::resetCache() const
{
    m_textCache->resetCache();
}

void cTextDrawer::syncDensity() const
{
    const int density = std::max(1, m_renderer->getFrameDensity());
    if (density == m_density) return;
    if (m_fallbackFont != nullptr) {
        TTF_SetFontSize(m_fallbackFont, m_baseSize * density);
    }
    TTF_SetFontSize(m_font, m_baseSize * density);
    m_textCache->setDensity(density);
    m_density = density;
}

int cTextDrawer::toLogical(int pixels) const
{
    return (pixels + m_density - 1) / m_density;
}
