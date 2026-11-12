#pragma once

#include "utils/cRectangle.h"

#include <array>

struct AdvancedOptionsHeaderLayout {
    cRectangle title;
    std::array<cRectangle, 4> tabs;

    [[nodiscard]] static AdvancedOptionsHeaderLayout create(
        int windowWidth,
        int margin,
        int buttonHeight,
        int fontHeight
    ) {
        const int tabWidth = (windowWidth - margin * 5) / 4;
        const int tabY = fontHeight + margin + 2;
        AdvancedOptionsHeaderLayout result{
            cRectangle(0, 2, windowWidth, fontHeight),
            {}
        };
        for (int index = 0; index < static_cast<int>(result.tabs.size()); ++index) {
            result.tabs[index] = cRectangle(
                margin * (index + 1) + tabWidth * index,
                tabY,
                tabWidth,
                buttonHeight
            );
        }
        return result;
    }
};
