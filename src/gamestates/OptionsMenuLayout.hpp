#pragma once

#include "utils/cRectangle.h"

#include <algorithm>

struct OptionsMenuLayout {
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
        int windowWidth,
        int windowHeight,
        int buttonHeight,
        int margin,
        int contentX,
        int buttonWidth,
        bool hdLayout,
        bool playing)
    {
        const int contentGap = hdLayout ? 2 : 5;
        const int applyY = (contentGap + buttonHeight) * 10;
        const int applyWidth = hdLayout ? 170 : 115;
        const int halfWidth = buttonWidth / 2;
        const int advancedWidth = hdLayout ? 220 : 160;
        const int actionGap = std::max(2, margin / 2);

        OptionsMenuLayout result;
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
        const int quitY = windowHeight - margin - buttonHeight;
        const int mainMenuY = quitY - actionGap - buttonHeight;
        result.mainMenu = cRectangle(
            margin,
            mainMenuY,
            buttonWidth,
            buttonHeight
        );
        result.quit = cRectangle(
            margin,
            quitY,
            halfWidth,
            buttonHeight
        );
        result.back = cRectangle(
            margin + halfWidth + margin,
            result.quit.getY(),
            halfWidth - margin,
            buttonHeight
        );

        if (playing) {
            const int missionY = mainMenuY - actionGap - buttonHeight;
            const int saveY = missionY - actionGap - buttonHeight;
            const int saveWidth = (buttonWidth - margin) / 2;
            result.save = cRectangle(
                margin,
                saveY,
                saveWidth,
                buttonHeight
            );
            result.load = cRectangle(
                margin + saveWidth + margin,
                saveY,
                buttonWidth - saveWidth - margin,
                buttonHeight
            );
            result.missionSelect = cRectangle(
                margin,
                missionY,
                buttonWidth,
                buttonHeight
            );
        }

        return result;
    }
};
