#pragma once

#include "utils/cRectangle.h"

#include <algorithm>
#include <cmath>

struct TextInkBounds {
    int textureWidth = 1;
    int textureHeight = 1;
    int x = 0;
    int y = 0;
    int width = 1;
    int height = 1;
};

inline cPoint calculateOpticallyCenteredTextOrigin(
    const cRectangle &rect,
    int drawWidth,
    int drawHeight,
    const TextInkBounds &ink)
{
    const double textureWidth = std::max(1, ink.textureWidth);
    const double textureHeight = std::max(1, ink.textureHeight);
    const double inkCenterX =
        (static_cast<double>(ink.x) + static_cast<double>(ink.width) / 2.0) *
        drawWidth / textureWidth;
    const double inkCenterY =
        (static_cast<double>(ink.y) + static_cast<double>(ink.height) / 2.0) *
        drawHeight / textureHeight;

    return cPoint(
        static_cast<int>(std::lround(
            rect.getX() + static_cast<double>(rect.getWidth()) / 2.0 - inkCenterX)),
        static_cast<int>(std::lround(
            rect.getY() + static_cast<double>(rect.getHeight()) / 2.0 - inkCenterY))
    );
}
