#pragma once

#include "utils/cRectangle.h"

#include <algorithm>
#include <cmath>

struct CampaignMapLayout {
    static constexpr int SourceMapX = 16;
    static constexpr int SourceMapY = 73;
    static constexpr int SourceMapWidth = 608;
    static constexpr int SourceMapHeight = 240;

    cRectangle panel;
    cRectangle title;
    cRectangle map;
    cRectangle message;
    cRectangle missionButton;

    [[nodiscard]] static CampaignMapLayout create(
        int screenWidth,
        int screenHeight)
    {
        const int margin = std::clamp(screenWidth / 48, 14, 40);
        const int titleHeight = std::clamp(screenHeight / 14, 44, 64);
        const int messageHeight = std::clamp(screenHeight / 12, 46, 64);
        const int buttonHeight = std::clamp(screenHeight / 15, 42, 54);
        const int gap = std::clamp(screenHeight / 80, 8, 14);
        const int panelPadding = std::clamp(screenWidth / 100, 14, 24);

        const int availableMapHeight = std::max(
            180,
            screenHeight - margin * 2 - titleHeight - messageHeight -
                buttonHeight - gap * 4 - panelPadding * 2
        );
        const int availableMapWidth = std::max(
            320,
            screenWidth - margin * 2 - panelPadding * 2
        );
        const double aspect = static_cast<double>(SourceMapWidth) /
            SourceMapHeight;
        const int mapWidth = std::max(
            320,
            std::min(
                availableMapWidth,
                static_cast<int>(std::lround(availableMapHeight * aspect))
            )
        );
        const int mapHeight = std::max(
            126,
            static_cast<int>(std::lround(mapWidth / aspect))
        );

        const int panelWidth = mapWidth + panelPadding * 2;
        const int panelHeight = panelPadding * 2 + titleHeight + mapHeight +
            messageHeight + buttonHeight + gap * 4;
        const int panelX = (screenWidth - panelWidth) / 2;
        const int panelY = std::max(margin, (screenHeight - panelHeight) / 2);
        const int contentX = panelX + panelPadding;
        int contentY = panelY + panelPadding;

        CampaignMapLayout result;
        result.panel = cRectangle(panelX, panelY, panelWidth, panelHeight);
        result.title = cRectangle(contentX, contentY, mapWidth, titleHeight);
        contentY += titleHeight + gap;
        result.map = cRectangle(contentX, contentY, mapWidth, mapHeight);
        contentY += mapHeight + gap;
        result.message = cRectangle(
            contentX,
            contentY,
            mapWidth,
            messageHeight
        );
        contentY += messageHeight + gap;

        const int buttonWidth = std::clamp(mapWidth / 4, 190, 300);
        result.missionButton = cRectangle(
            contentX + mapWidth - buttonWidth,
            contentY,
            buttonWidth,
            buttonHeight
        );
        return result;
    }

    [[nodiscard]] cRectangle regionDestination(
        int sourceX,
        int sourceY,
        int sourceWidth,
        int sourceHeight) const
    {
        const double scaleX = static_cast<double>(map.getWidth()) /
            SourceMapWidth;
        const double scaleY = static_cast<double>(map.getHeight()) /
            SourceMapHeight;
        return cRectangle(
            map.getX() + static_cast<int>(std::lround(
                (sourceX - SourceMapX) * scaleX)),
            map.getY() + static_cast<int>(std::lround(
                (sourceY - SourceMapY) * scaleY)),
            std::max(1, static_cast<int>(std::lround(sourceWidth * scaleX))),
            std::max(1, static_cast<int>(std::lround(sourceHeight * scaleY)))
        );
    }

    [[nodiscard]] int clickMapX(int screenX, int clickMapWidth) const
    {
        const double normalized = static_cast<double>(screenX - map.getX()) /
            std::max(1, map.getWidth());
        return std::clamp(
            static_cast<int>(normalized * clickMapWidth),
            0,
            std::max(0, clickMapWidth - 1)
        );
    }

    [[nodiscard]] int clickMapY(int screenY, int clickMapHeight) const
    {
        const double normalized = static_cast<double>(screenY - map.getY()) /
            std::max(1, map.getHeight());
        return std::clamp(
            static_cast<int>(normalized * clickMapHeight),
            0,
            std::max(0, clickMapHeight - 1)
        );
    }
};
