#pragma once

#include "utils/cRectangle.h"

#include <algorithm>

struct OptionsMenuLayout {
    cRectangle window;
    cRectangle apply;
    cRectangle advanced;
    cRectangle status;
    cRectangle save;
    cRectangle load;
    cRectangle missionSelect;
    cRectangle mainMenu;
    cRectangle quit;
    cRectangle back;

    [[nodiscard]] static OptionsMenuLayout create(
        int canvasWidth,
        int canvasHeight,
        int buttonHeight,
        bool playing)
    {
        const int margin = 8;
        const int actionGap = std::max(2, margin / 2);
        constexpr int contentGap = 2;
        constexpr int contentX = 24;
        const int applyY = (contentGap + buttonHeight) * 10;
        constexpr int applyWidth = 170;
        constexpr int advancedWidth = 220;
        const int windowWidth = std::min(canvasWidth - 32, 680);
        const int oldHeight = std::min(canvasHeight - 32, 680);
        const int applyBottom = applyY + buttonHeight;
        const int actionRows = playing ? 2 : 1;
        const int requiredHeight = applyBottom + margin + actionRows * buttonHeight
            + (actionRows - 1) * actionGap + margin;
        const int windowHeight = std::min(canvasHeight - 8, std::max(oldHeight, requiredHeight));

        OptionsMenuLayout result;
        result.window = cRectangle(
            (canvasWidth - windowWidth) / 2,
            (canvasHeight - windowHeight) / 2,
            windowWidth,
            windowHeight
        );
        result.apply = cRectangle(
            contentX,
            applyY,
            applyWidth,
            buttonHeight
        );
        result.advanced = cRectangle(
            contentX + applyWidth + margin,
            applyY,
            advancedWidth,
            buttonHeight
        );
        const int statusX = result.advanced.getEndX() + margin;
        result.status = cRectangle(
            statusX,
            applyY,
            std::max(0, windowWidth - margin - statusX),
            buttonHeight
        );
        const int columnWidth = (windowWidth - 4 * margin) / 3;
        const int x0 = margin;
        const int x1 = 2 * margin + columnWidth;
        const int x2 = 3 * margin + 2 * columnWidth;
        const int lastWidth = windowWidth - margin - x2;
        const int bottomY = windowHeight - margin - buttonHeight;
        result.mainMenu = cRectangle(
            x1,
            bottomY,
            columnWidth,
            buttonHeight
        );
        result.quit = cRectangle(
            x0,
            bottomY,
            columnWidth,
            buttonHeight
        );
        result.back = cRectangle(
            x2,
            bottomY,
            lastWidth,
            buttonHeight
        );

        if (playing) {
            const int upperY = bottomY - actionGap - buttonHeight;
            result.save = cRectangle(
                x0,
                upperY,
                columnWidth,
                buttonHeight
            );
            result.load = cRectangle(
                x1,
                upperY,
                columnWidth,
                buttonHeight
            );
            result.missionSelect = cRectangle(
                x2,
                upperY,
                lastWidth,
                buttonHeight
            );
        }

        return result;
    }
};
