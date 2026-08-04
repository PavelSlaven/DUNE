#include "cTextDrawer.h"
#include "drawers/cTextTextureCache.h"

#include "d2tmc.h"
#include "drawers/SDLDrawer.hpp"
#include "utils/Color.hpp"
#include <algorithm>
#include <iostream>
#include <cassert>

cTextDrawer::cTextDrawer(TTF_Font *theFont, int density) :
    m_font(theFont),
    m_density(std::max(1, density)),
    m_textCache(std::make_unique<cTextTextureCache>(theFont, m_density))
{
}

cTextDrawer::~cTextDrawer()
{
    m_font = nullptr;
}

void cTextDrawer::drawText(int x, int y, Color color, const std::string &msg, bool applyShadow) const
{
    if (msg.empty()) return;
    auto cacheEntry = m_textCache->findOrCreate(color, msg);
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
    TTF_SizeUTF8(m_font, msg.c_str(), &w, &h);
    w = (w + m_density - 1) / m_density;
    int half = w / 2;
    int xPos = (game.m_screenW / 2) - half;
    drawText(xPos, y, color, msg);
}

void cTextDrawer::drawTextCenteredInBox(const std::string &msg, int x, int y, int boxWidth, int boxHeight, Color color) const
{
    if (msg.empty()) return;
    int w,h;
    TTF_SizeUTF8(m_font, msg.c_str(), &w, &h);
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
    auto cacheEntry = m_textCache->findOrCreate(color, msg);
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

void cTextDrawer::drawTextCentered(const std::string &msg, int x, int width, int y, Color color) const
{
    if (msg.empty()) return;
    int w,h;
    TTF_SizeUTF8(m_font, msg.c_str(), &w, &h);
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
    TTF_SizeUTF8(m_font, msg.c_str(), &w, &h);
    w = (w + m_density - 1) / m_density;
    int lenghtInPixels = w;
    int x = game.m_screenW - lenghtInPixels-margin;
    int y = game.m_screenH - getFontHeight()-20-margin;
    drawText(x, y, color, msg);
}

int cTextDrawer::getFontHeight() const
{
    return (TTF_FontHeight(m_font) + m_density - 1) / m_density;
}

void cTextDrawer::drawTextBottomLeft(Color color, const std::string &msg, int margin) const
{
    if (msg.empty()) return;
    int w,h;
    TTF_SizeUTF8(m_font, msg.c_str(), &w, &h);
    h = (h + m_density - 1) / m_density;
    int y = game.m_screenH - h-20-margin;
    drawText(margin, y, color, msg);
}

int cTextDrawer::getTextLength(const std::string &msg) const
{
    int w,h;
    TTF_SizeUTF8(m_font, msg.c_str(), &w, &h);
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
}
