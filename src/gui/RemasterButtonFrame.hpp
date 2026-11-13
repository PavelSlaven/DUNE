#pragma once

#include "drawers/SDLDrawer.hpp"
#include "gui/GuiTheme.hpp"
#include "utils/cRectangle.h"

#include <algorithm>

inline void drawRemasterButtonFrame(SDLDrawer &drawer, const cRectangle &rect, const GuiTheme &theme, bool focused, bool pressed)
{
    Color fillColor = theme.fillColor;
    Color outerBorder = theme.borderDark;
    Color innerBorder = theme.borderLight;

    if (focused) {
        fillColor = Color{
            static_cast<Uint8>(std::min(255, fillColor.r + 18)),
            static_cast<Uint8>(std::min(255, fillColor.g + 18)),
            static_cast<Uint8>(std::min(255, fillColor.b + 18)),
            fillColor.a
        };
    }
    if (pressed) {
        fillColor = Color{
            static_cast<Uint8>(fillColor.r * 3 / 4),
            static_cast<Uint8>(fillColor.g * 3 / 4),
            static_cast<Uint8>(fillColor.b * 3 / 4),
            fillColor.a
        };
        std::swap(outerBorder, innerBorder);
    }

    drawer.renderRectFillColor(
        rect.getX() + 3,
        rect.getY() + 3,
        rect.getWidth(),
        rect.getHeight(),
        theme.textColorShadow
    );
    drawer.renderRectFillColor(rect, fillColor);
    drawer.renderRectColor(rect, outerBorder);
    drawer.renderRectColor(
        rect.getX() + 1,
        rect.getY() + 1,
        rect.getWidth() - 2,
        rect.getHeight() - 2,
        innerBorder
    );
    drawer.renderLine(
        rect.getX() + 4,
        rect.getY() + 3,
        rect.getX() + rect.getWidth() - 5,
        rect.getY() + 3,
        focused ? theme.textColorHover : theme.borderLight
    );
}
