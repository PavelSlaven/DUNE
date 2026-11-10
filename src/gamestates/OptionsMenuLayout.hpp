#pragma once

#include "utils/cRectangle.h"

#include <algorithm>

struct OptionsMenuLayout {
    cRectangle window;
    cRectangle speedLabel;
    cRectangle apply;
    cRectangle advanced;
    cRectangle status;
    cRectangle save;
    cRectangle load;
    cRectangle missionSelect;
    cRectangle mainMenu;
    cRectangle quit;
    cRectangle back;
    int contentTop = 0;
    int contentGap = 0;

    [[nodiscard]] static OptionsMenuLayout create(
        int canvasWidth,
        int canvasHeight,
        int buttonHeight,
        bool playing,
        int titleFontHeight = -1)
    {
        const int margin = 8;
        const int actionGap = std::max(2, margin / 2);
        const int contentGap = 2;
        const int contentX = 24;
        const int applyWidth = 170;
        const int advancedWidth = 220;
        const int windowWidth = std::min(canvasWidth - 32, 680);
        const int oldHeight = std::min(canvasHeight - 32, 680);
        const int actionRows = playing ? 2 : 1;
        const int availableHeight = canvasHeight - 8;
        const int preferredContentTop = buttonHeight + contentGap;
        const int measuredTitleFontHeight = titleFontHeight >= 0
            ? titleFontHeight
            : std::max(0, buttonHeight - 10);
        const int preferredApplyY = (contentGap + buttonHeight) * 10;
        const int preferredHeight = preferredApplyY + buttonHeight + margin
            + actionRows * buttonHeight + (actionRows - 1) * actionGap + margin;
        const bool compact = preferredHeight > availableHeight;
        const int minimumContentTop = 2 + measuredTitleFontHeight + 2;
        const int contentTop = compact
            ? std::max(28, minimumContentTop)
            : preferredContentTop;
        const int compactActionGap = compact ? 2 : actionGap;
        const int applyGap = compact ? 2 : margin;
        const int bottomMargin = compact ? 4 : margin;
        const int applyY = compact
            ? contentTop + 9 * (buttonHeight + contentGap)
            : preferredApplyY;
        const int requiredHeight = applyY + buttonHeight + applyGap
            + actionRows * buttonHeight + (actionRows - 1) * compactActionGap + bottomMargin;
        const int windowHeight = std::min(canvasHeight - 8, std::max(oldHeight, requiredHeight));

        OptionsMenuLayout result;
        result.window = cRectangle(
            (canvasWidth - windowWidth) / 2,
            (canvasHeight - windowHeight) / 2,
            windowWidth,
            windowHeight
        );
        result.contentTop = contentTop;
        result.contentGap = contentGap;
        result.speedLabel = cRectangle(
            16,
            contentTop + 2 * (buttonHeight + contentGap),
            122,
            buttonHeight
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
        const int bottomY = windowHeight - bottomMargin - buttonHeight;
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
            const int upperY = bottomY - compactActionGap - buttonHeight;
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
