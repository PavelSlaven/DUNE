#include "UnitDrawRecorder.hpp"

#include "drawers/cTextDrawer.h"
#include "drawers/cTextTextureCache.h"

#include <algorithm>
#include <cmath>

namespace {
void recordText(int x, int y, Color color, const std::string &message, bool shadow)
{
    unitRecordedText().push_back({x, y, color, message, shadow});
}
}

std::vector<UnitRecordedText> &unitRecordedText()
{
    static std::vector<UnitRecordedText> calls;
    return calls;
}

void clearUnitRecordedText()
{
    unitRecordedText().clear();
}

cTextDrawer::cTextDrawer(TTF_Font *, int, TTF_Font *) : m_font(nullptr), m_fallbackFont(nullptr), m_density(1)
{
}

cTextDrawer::~cTextDrawer() = default;

void cTextDrawer::drawText(int x, int y, Color color, const std::string &msg, bool applyShadow) const
{
    recordText(x, y, color, msg, applyShadow);
}

void cTextDrawer::drawText(int x, int y, const std::string &msg, bool applyShadow) const
{
    recordText(x, y, Color::white(), msg, applyShadow);
}

void cTextDrawer::drawText(cPoint &coords, Color color, const std::string &msg, bool applyShadow) const
{
    recordText(coords.x, coords.y, color, msg, applyShadow);
}

void cTextDrawer::drawTextCentered(const std::string &msg, int y) const
{
    recordText(0, y, Color::white(), msg, true);
}

void cTextDrawer::drawTextCentered(const std::string &msg, int y, Color color) const
{
    recordText(0, y, color, msg, true);
}

void cTextDrawer::drawTextCentered(const std::string &msg, int x, int, int y, Color color) const
{
    recordText(x, y, color, msg, true);
}

void cTextDrawer::drawTextCenteredInBox(
    const std::string &msg, int x, int y, int boxWidth, int boxHeight, Color color) const
{
    const int textWidth = getTextLength(msg);
    recordText(x + (boxWidth - textWidth) / 2, y + (boxHeight - getFontHeight()) / 2,
               color, msg, true);
}

void cTextDrawer::drawTextCenteredInBox(const std::string &msg, const cRectangle &rect, Color color) const
{
    drawTextCenteredInBox(msg, rect, color, 0, 0);
}

void cTextDrawer::drawTextCenteredInBox(
    const std::string &msg, const cRectangle &rect, Color color, int offsetX, int offsetY) const
{
    recordText(rect.getX() + (rect.getWidth() - getTextLength(msg)) / 2 + offsetX,
               rect.getY() + (rect.getHeight() - getFontHeight()) / 2 + offsetY,
               color, msg, true);
}

void cTextDrawer::drawTextScaledCenteredInBox(
    const std::string &msg, const cRectangle &rect, float scale, Color color, bool applyShadow) const
{
    const int width = static_cast<int>(std::lround(getTextLength(msg) * scale));
    const int height = static_cast<int>(std::lround(getFontHeight() * scale));
    recordText(rect.getX() + (rect.getWidth() - width) / 2,
               rect.getY() + (rect.getHeight() - height) / 2,
               color, msg, applyShadow);
}

void cTextDrawer::drawTextScaledOpticallyCenteredInBox(
    const std::string &msg, const cRectangle &rect, float scale, Color color, bool applyShadow) const
{
    drawTextScaledCenteredInBox(msg, rect, scale, color, applyShadow);
}

void cTextDrawer::drawTextBottomRight(const std::string &msg, int margin) const
{
    recordText(-margin - getTextLength(msg), -margin - getFontHeight(), Color::white(), msg, true);
}

void cTextDrawer::drawTextBottomLeft(const std::string &msg, int margin) const
{
    recordText(margin, -margin - getFontHeight(), Color::white(), msg, true);
}

void cTextDrawer::drawTextBottomRight(Color color, const std::string &msg, int margin) const
{
    recordText(-margin - getTextLength(msg), -margin - getFontHeight(), color, msg, true);
}

void cTextDrawer::drawTextBottomLeft(Color color, const std::string &msg, int margin) const
{
    recordText(margin, -margin - getFontHeight(), color, msg, true);
}

int cTextDrawer::getTextLength(const std::string &msg) const
{
    return static_cast<int>(msg.size()) * 8;
}

int cTextDrawer::getFontHeight() const
{
    return 8;
}

void cTextDrawer::resetCache() const
{
}

cRectangle cTextDrawer::getRect(int x, int y, const std::string &msg) const
{
    return {x, y, getTextLength(msg), getFontHeight()};
}

cRectangle *cTextDrawer::getAsRectangle(int x, int y, const std::string &msg) const
{
    static thread_local cRectangle rect;
    rect = getRect(x, y, msg);
    return &rect;
}

