/**
 * @file GuiTheme.hpp
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

#pragma once

#include "drawers/SDLDrawer.hpp"

struct GuiTheme {
    // Button/Rectangle
    Color fillColor;
    Color borderLight;
    Color borderDark;
    Color background;

    // Text
    Color textColor;
    Color textDarkColor;
    Color textColorHover;
    Color textColorShadow;

    // Disabled properties here (for now, perhaps in the future its own "theme"?)
    Color disabledTextColor;
    Color disabledFillColor;
    Color disabledBorderLight;
    Color disabledBorderDark;

    static GuiTheme Remaster() {
        GuiTheme theme{};
        theme.fillColor = Color{24, 29, 33, 238};
        theme.borderLight = Color{190, 145, 58, 255};
        theme.borderDark = Color{71, 50, 24, 255};
        theme.background = Color{32, 32, 32, 255};
        theme.textColor = Color{236, 229, 202, 255};
        theme.textDarkColor = Color{225, 177, 21, 255};
        theme.textColorHover = Color{255, 202, 83, 255};
        theme.textColorShadow = Color{4, 6, 7, 220};
        theme.disabledTextColor = Color{132, 132, 124, 255};
        theme.disabledFillColor = Color{20, 24, 27, 220};
        theme.disabledBorderLight = Color{91, 84, 66, 255};
        theme.disabledBorderDark = Color{46, 42, 34, 255};
        return theme;
    }

    static GuiTheme RemasterInactive() {
        GuiTheme theme{};
        theme.fillColor = Color{20, 24, 27, 220};
        theme.borderLight = Color{91, 84, 66, 255};
        theme.borderDark = Color{46, 42, 34, 255};
        theme.background = Color{32, 32, 32, 255};
        theme.textColor = Color{132, 132, 124, 255};
        theme.textDarkColor = Color{225, 177, 21, 255};
        theme.textColorHover = Color{154, 146, 124, 255};
        theme.textColorShadow = Color{4, 6, 7, 220};
        theme.disabledTextColor = Color{132, 132, 124, 255};
        theme.disabledFillColor = Color{20, 24, 27, 220};
        theme.disabledBorderLight = Color{91, 84, 66, 255};
        theme.disabledBorderDark = Color{46, 42, 34, 255};
        return theme;
    }
};

class cGuiThemeBuilder {

public:

    cGuiThemeBuilder &dark() {
        m_fillColor = Color{84, 84, 120, 255};
        m_borderLight = Color{40, 40, 40, 255};
        m_borderDark = Color{176, 176, 196, 255};
        m_background = Color{32, 32, 32, 255};
        m_textColor = Color::White;
        m_textDarkColor = Color{225, 177, 21, 255};
        m_textColorHover = Color{255, 0, 0, 255};
        m_textColorShadow = Color::Black;
        m_disabledTextColor = Color{128, 128, 128, 255};
        m_disabledFillColor = Color{64, 64, 100, 255};
        m_disabledBorderLight = {40, 40, 40, 255};
        m_disabledBorderDark = {20, 20, 20, 255};
        return *this;
    }

    cGuiThemeBuilder &inactive() {
        m_fillColor = Color{84, 84, 120, 255};
        m_borderLight = Color{40, 40, 40, 255};
        m_borderDark = Color{176, 176, 196, 255};
        m_background = Color{32, 32, 32, 255};
        m_textColor = Color{192, 192, 192, 255};
        m_textDarkColor = Color{128, 128, 128, 255};
        m_textColorHover = Color::Black;
        m_textColorShadow = Color{128, 128, 128, 255};
        m_disabledTextColor = Color{128, 128, 128, 255};
        m_disabledFillColor = Color{64, 64, 100, 255};
        m_disabledBorderLight = Color{40, 40, 40, 255};
        m_disabledBorderDark = Color{176, 176, 196, 255};
        return *this;
    }

    cGuiThemeBuilder &light() {
        m_fillColor = Color{176, 176, 196, 255};
        m_borderLight = Color{252, 252, 252, 255};
        m_borderDark = Color{84, 84, 120, 255};
        m_background = Color{32, 32, 32, 255};
        m_textColor = Color::White;
        m_textDarkColor = Color{225, 177, 21, 255};
        m_textColorHover = Color{255, 0, 0, 255};
        m_textColorShadow = Color::Black;
        m_disabledTextColor = Color{128, 128, 128, 255};
        m_disabledFillColor = Color{146, 146, 166, 255};
        m_disabledBorderLight = Color{84, 84, 120, 255};
        m_disabledBorderDark = Color{128, 128, 128, 255};
        return *this;
    }

    cGuiThemeBuilder& withTextColor(Color textColor) {
        this->m_textColor = textColor;
        return *this;
    }

    GuiTheme build() const {
        return {
            m_fillColor,
            m_borderLight,
            m_borderDark,
            m_background,
            m_textColor,
            m_textDarkColor,
            m_textColorHover,
            m_textColorShadow,
            m_disabledTextColor,
            m_disabledFillColor,
            m_disabledBorderLight,
            m_disabledBorderDark
        };
    }

private:
    Color m_fillColor;
    Color m_borderLight;
    Color m_borderDark;
    Color m_background;
    Color m_textColor;
    Color m_textDarkColor;
    Color m_textColorHover;
    Color m_textColorShadow;
    Color m_disabledTextColor;
    Color m_disabledFillColor;
    Color m_disabledBorderLight;
    Color m_disabledBorderDark;
};
