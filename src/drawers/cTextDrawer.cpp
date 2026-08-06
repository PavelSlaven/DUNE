#include "cTextDrawer.h"
#include "drawers/cTextTextureCache.h"

#include "d2tmc.h"
#include "drawers/SDLDrawer.hpp"
#include "utils/Color.hpp"
#include "utils/FontSupport.hpp"
#include "utils/TextAlignment.hpp"
#include <algorithm>
#include <iostream>
#include <cassert>

cTextDrawer::cTextDrawer(TTF_Font *theFont, int density, TTF_Font *fallbackFont) :
    m_font(theFont),
    m_fallbackFont(fallbackFont),
    m_density(std::max(1, density)),
    m_textCache(std::make_unique<cTextTextureCache>(theFont, m_density)),
    m_fallbackTextCache(fallbackFont
        ? std::make_unique<cTextTextureCache>(fallbackFont, m_density)
        : nullptr)
{
}

cTextDrawer::~cTextDrawer()
{
    m_font = nullptr;
    m_fallbackFont = nullptr;
}

bool cTextDrawer::shouldUseFallback(const std::string &msg) const
{
    if (!m_fallbackFont) return false;
    const auto found = m_fallbackByText.find(msg);
    if (found != m_fallbackByText.end()) return found->second;

    const bool useFallback = !ttfFontSupportsText(m_font, msg) &&
        ttfFontSupportsText(m_fallbackFont, msg);
    m_fallbackByText.emplace(msg, useFallback);
    return useFallback;
}

TTF_Font *cTextDrawer::fontFor(const std::string &msg) const
{
    return shouldUseFallback(msg) ? m_fallbackFont : m_font;
}

cTextTextureCache *cTextDrawer::cacheFor(const std::string &msg) const
{
    return shouldUseFallback(msg) ? m_fallbackTextCache.get() : m_textCache.get();
}

void cTextDrawer::drawText(int x, int y, Color color, const std::string &msg, bool applyShadow) const
{
    if (msg.empty()) return;
    auto cacheEntry = cacheFor(msg)->findOrCreate(color, msg);
    cacheEntry->lifeCounter += 1;
    if (applyShadow) {
        renderDrawer->renderTexture(cacheEntry->shadowsTexture, x + 1, y + 1,cacheEntry->width, cacheEntry->height);
    }
    renderDrawer->renderTexture(cacheEntry->texture, x, y,cacheEntry->width, cacheEntry->height);
}

void cTextDrawer::drawText(cPoint &coords, Color color, const std::string &msg, bool applyShadow) const
{
    drawText(coords.x, coords.y, color, msg, applyShadow);
}

void cTextDrawer::drawText(int x, int y, const std::string &msg, bool applyShadow) const
{
    drawText(x, y, Color::white() , msg, applyShadow);
}

void cTextDrawer::drawTextCentered(const std::string &msg, int y) const
{
    drawTextCentered(msg, y, Color::white());
}

void cTextDrawer::drawTextCentered(const std::string &msg, int y, Color color) const
{
    if (msg.empty()) return;
    int w,h;
    TTF_SizeUTF8(fontFor(msg), msg.c_str(), &w, &h);
    w = (w + m_density - 1) / m_density;
    int half = w / 2;
    int xPos = (game.m_screenW / 2) - half;
    drawText(xPos, y, color, msg);
}

void cTextDrawer::drawTextCenteredInBox(const std::string &msg, int x, int y, int boxWidth, int boxHeight, Color color) const
{
    if (msg.empty()) return;
    int w,h;
    TTF_SizeUTF8(fontFor(msg), msg.c_str(), &w, &h);
    w = (w + m_density - 1) / m_density;
    h = (h + m_density - 1) / m_density;
    int lenghtInPixels = w;
    int heightInPixels = h;

    int halfLengthInPixels = lenghtInPixels / 2;
    int xPos = x + ((boxWidth / 2) - halfLengthInPixels);
    int halfHeightInPixels = heightInPixels / 2;
    int yPos = y + ((boxHeight / 2) - halfHeightInPixels);
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
    if (msg.empty()) return;
    scale = std::max(0.5F, scale);
    auto cacheEntry = cacheFor(msg)->findOrCreate(color, msg);
    cacheEntry->lifeCounter += 1;
    const int width = static_cast<int>(cacheEntry->width * scale + 0.5F);
    const int height = static_cast<int>(cacheEntry->height * scale + 0.5F);
    const int x = rect.getX() + (rect.getWidth() - width) / 2;
    const int y = rect.getY() + (rect.getHeight() - height) / 2;
    if (applyShadow) {
        renderDrawer->renderTexture(cacheEntry->shadowsTexture, x + 2, y + 2, width, height);
    }
    renderDrawer->renderTexture(cacheEntry->texture, x, y, width, height);
}

void cTextDrawer::drawTextScaledOpticallyCenteredInBox(
    const std::string &msg,
    const cRectangle &rect,
    float scale,
    Color color,
    bool applyShadow) const
{
    if (msg.empty()) return;
    scale = std::max(0.5F, scale);
    auto cacheEntry = cacheFor(msg)->findOrCreate(color, msg);
    cacheEntry->lifeCounter += 1;
    const int width = static_cast<int>(cacheEntry->width * scale + 0.5F);
    const int height = static_cast<int>(cacheEntry->height * scale + 0.5F);
    const cPoint origin = calculateOpticallyCenteredTextOrigin(
        rect,
        width,
        height,
        cacheEntry->inkBounds
    );
    if (applyShadow) {
        renderDrawer->renderTexture(
            cacheEntry->shadowsTexture,
            origin.x + 2,
            origin.y + 2,
            width,
            height
        );
    }
    renderDrawer->renderTexture(cacheEntry->texture, origin.x, origin.y, width, height);
}

void cTextDrawer::drawTextCentered(const std::string &msg, int x, int width, int y, Color color) const
{
    if (msg.empty()) return;
    int w,h;
    TTF_SizeUTF8(fontFor(msg), msg.c_str(), &w, &h);
    w = (w + m_density - 1) / m_density;
    int lenghtInPixels = w;
    int half = lenghtInPixels / 2;
    int xPos = x + ((width / 2) - half);
    drawText(xPos, y, color, msg);
}

void cTextDrawer::drawTextBottomRight(const std::string &msg, int margin) const
{
    drawTextBottomRight(Color::white(), msg, margin);
}

void cTextDrawer::drawTextBottomLeft(const std::string &msg, int margin) const
{
    drawTextBottomLeft(Color::white(), msg, margin);
}

void cTextDrawer::drawTextBottomRight(Color color, const std::string &msg, int margin) const
{
    if (msg.empty()) return;
    int w,h;
    TTF_SizeUTF8(fontFor(msg), msg.c_str(), &w, &h);
    w = (w + m_density - 1) / m_density;
    int lenghtInPixels = w;
    int x = game.m_screenW - lenghtInPixels-margin;
    int y = game.m_screenH - getFontHeight()-20-margin;
    drawText(x, y, color, msg);
}

int cTextDrawer::getFontHeight() const
{
    const int primaryHeight = TTF_FontHeight(m_font);
    const int fallbackHeight = m_fallbackFont ? TTF_FontHeight(m_fallbackFont) : 0;
    return (std::max(primaryHeight, fallbackHeight) + m_density - 1) / m_density;
}

void cTextDrawer::drawTextBottomLeft(Color color, const std::string &msg, int margin) const
{
    if (msg.empty()) return;
    int w,h;
    TTF_SizeUTF8(fontFor(msg), msg.c_str(), &w, &h);
    h = (h + m_density - 1) / m_density;
    int y = game.m_screenH - h-20-margin;
    drawText(margin, y, color, msg);
}

int cTextDrawer::getTextLength(const std::string &msg) const
{
    int w,h;
    TTF_SizeUTF8(fontFor(msg), msg.c_str(), &w, &h);
    return (w + m_density - 1) / m_density;
}

cRectangle cTextDrawer::getRect(int x, int y, const std::string &msg) const
{
    return cRectangle(x, y, getTextLength(msg), getFontHeight());
}

cRectangle *cTextDrawer::getAsRectangle(int x, int y, const std::string &msg) const
{
    return new cRectangle(x, y, getTextLength(msg), getFontHeight());
}

void cTextDrawer::resetCache() const
{
    m_textCache->resetCache();
    if (m_fallbackTextCache) m_fallbackTextCache->resetCache();
    m_fallbackByText.clear();
}
