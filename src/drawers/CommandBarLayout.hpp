#pragma once

#include "utils/cRectangle.h"

#include <algorithm>
#include <array>

struct CommandBarLayout {
    static constexpr int ActionCount = 7;

    cRectangle panel;
    std::array<cRectangle, ActionCount> actions{};

    [[nodiscard]] static CommandBarLayout create(int screenWidth, int screenHeight, int sidebarWidth)
    {
        constexpr int idealPanelWidth = 700;
        constexpr int idealPanelHeight = 86;
        constexpr int bottomScrollClearance = 8;
        constexpr int outerMargin = 8;

        const int battlefieldWidth = std::max(0, screenWidth - sidebarWidth);
        const int availableWidth = std::max(0, battlefieldWidth - outerMargin * 2);
        const int panelWidth = std::min(idealPanelWidth, availableWidth);
        const int panelHeight = std::max(
            1,
            (panelWidth * idealPanelHeight + idealPanelWidth / 2) / idealPanelWidth
        );
        const int panelX = std::min(outerMargin, std::max(0, battlefieldWidth - panelWidth));
        const int panelY = std::max(0, screenHeight - bottomScrollClearance - panelHeight);

        CommandBarLayout result{
            .panel = cRectangle(panelX, panelY, panelWidth, panelHeight)
        };
        constexpr std::array<int, ActionCount + 1> referenceBoundaries{
            0, 448, 858, 1240, 1634, 2035, 2413, 2800
        };
        for (int index = 0; index < ActionCount; ++index) {
            const int x0 = panelX + panelWidth * referenceBoundaries[index] / 2800;
            const int x1 = panelX + panelWidth * referenceBoundaries[index + 1] / 2800;
            result.actions[index] = cRectangle(x0, panelY, x1 - x0, panelHeight);
        }
        return result;
    }
};
