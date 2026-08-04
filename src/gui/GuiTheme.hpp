#pragma once

#include "drawers/SDLDrawer.hpp"

struct GuiTheme {
    Color fillColor;
    Color borderLight;
    Color borderDark;
    Color textColor;
    Color textColorHover;
    Color textColorShadow;

    static GuiTheme Light() {
        return {
            Color{176, 176, 196,255},
            Color{252, 252, 252,255},
            Color{84, 84, 120,255},
            Color::white(),
            Color{255, 0, 0,255},
            Color::black()
        };
    }
    static GuiTheme Dark() {
        return {
            Color{84, 84, 120,255},
            Color{40, 40, 40,255},
            Color{176, 176, 196,255},
            Color::white(),
            Color{255, 0, 0,255},
            Color::black()
        };
    }
    static GuiTheme Inactive() {
        return {
            Color{84, 84, 120,255},
            Color{40, 40, 40,255},
            Color{176, 176, 196,255},
            Color{192, 192, 192,255},
            Color{128, 128, 128,255},
            Color::black()
        };
    }

    static GuiTheme Remaster() {
        return {
            Color{24, 29, 33, 238},
            Color{190, 145, 58, 255},
            Color{71, 50, 24, 255},
            Color{236, 229, 202, 255},
            Color{255, 202, 83, 255},
            Color{4, 6, 7, 220}
        };
    }

    static GuiTheme RemasterInactive() {
        return {
            Color{20, 24, 27, 220},
            Color{91, 84, 66, 255},
            Color{46, 42, 34, 255},
            Color{132, 132, 124, 255},
            Color{154, 146, 124, 255},
            Color{4, 6, 7, 220}
        };
    }
};
