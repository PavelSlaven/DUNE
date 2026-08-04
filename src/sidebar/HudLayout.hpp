#pragma once

#include "utils/cRectangle.h"

#include <algorithm>

/**
 * Immutable geometry for the combat HUD.
 *
 * HD drawing and hit testing must use this object instead of repeating sidebar
 * arithmetic in several drawers.  Classic mode deliberately keeps the original
 * Dune II dimensions.
 */
struct HudLayout {
    static constexpr int TopBarHeight = 42;

    bool hd = false;
    int screenWidth = 0;
    int screenHeight = 0;
    int sidebarWidth = 224;
    int columns = 3;
    int cardGap = 3;
    int cardWidth = 63;
    int cardHeight = 47;

    cRectangle topBar;
    cRectangle battlefield;
    cRectangle sidebar;
    cRectangle credits;
    cRectangle radarPanel;
    cRectangle houseHeader;
    cRectangle radarViewport;
    cRectangle powerMeter;
    cRectangle spiceMeter;
    cRectangle tabs;
    cRectangle catalog;
    cRectangle cards;
    cRectangle scrollbar;

    static HudLayout create(
        bool hdMode,
        int logicalWidth,
        int logicalHeight,
        bool reserveStarportOrderArea = false)
    {
        HudLayout layout;
        layout.hd = hdMode;
        layout.screenWidth = logicalWidth;
        layout.screenHeight = logicalHeight;

        if (!hdMode) {
            layout.sidebarWidth = 224;
            layout.columns = 3;
            layout.cardGap = 3;
            layout.cardWidth = 63;
            layout.cardHeight = 47;

            const int sidebarX = logicalWidth - layout.sidebarWidth;
            layout.topBar = cRectangle(0, 0, logicalWidth, TopBarHeight);
            layout.battlefield = cRectangle(
                0,
                TopBarHeight,
                logicalWidth - layout.sidebarWidth,
                logicalHeight - TopBarHeight
            );
            layout.sidebar = cRectangle(
                sidebarX,
                0,
                layout.sidebarWidth,
                logicalHeight
            );
            layout.credits = cRectangle(logicalWidth - 198, 0, 198, TopBarHeight);
            layout.radarPanel = cRectangle(
                logicalWidth - 200,
                TopBarHeight,
                200,
                208
            );
            layout.radarViewport = layout.radarPanel;
            layout.tabs = cRectangle(logicalWidth - 198, 268, 198, 28);
            layout.catalog = cRectangle(
                logicalWidth - 198,
                302,
                198,
                std::max(0, logicalHeight - 302)
            );
            layout.cards = layout.catalog;
            return layout;
        }

        layout.sidebarWidth = logicalWidth < 960 ? 280 : 360;
        layout.columns = logicalWidth < 960 ? 2 : 3;
        layout.cardGap = 6;

        const int sidebarX = logicalWidth - layout.sidebarWidth;
        const int panelInset = 8;
        const int panelWidth = layout.sidebarWidth - panelInset * 2;
        const int catalogY = 302;
        const int catalogBottom =
            logicalHeight - (reserveStarportOrderArea ? 54 : 6);

        layout.topBar = cRectangle(0, 0, logicalWidth, TopBarHeight);
        layout.battlefield = cRectangle(
            0,
            TopBarHeight,
            logicalWidth - layout.sidebarWidth,
            logicalHeight - TopBarHeight
        );
        layout.sidebar = cRectangle(
            sidebarX,
            0,
            layout.sidebarWidth,
            logicalHeight
        );
        layout.credits = cRectangle(
            sidebarX + panelInset,
            4,
            panelWidth,
            34
        );
        layout.radarPanel = cRectangle(
            sidebarX + panelInset,
            TopBarHeight,
            panelWidth,
            208
        );
        layout.houseHeader = cRectangle(
            layout.radarPanel.getX() + 5,
            layout.radarPanel.getY() + 4,
            layout.radarPanel.getWidth() - 10,
            28
        );
        layout.radarViewport = cRectangle(
            layout.radarPanel.getX() + 5,
            layout.radarPanel.getY() + 34,
            layout.radarPanel.getWidth() - 10,
            138
        );

        const int meterGap = 5;
        const int meterY = layout.radarPanel.getY() + 176;
        const int meterWidth =
            (layout.radarPanel.getWidth() - 10 - meterGap) / 2;
        layout.powerMeter = cRectangle(
            layout.radarPanel.getX() + 5,
            meterY,
            meterWidth,
            27
        );
        layout.spiceMeter = cRectangle(
            layout.powerMeter.getEndX() + meterGap,
            meterY,
            meterWidth,
            27
        );
        layout.tabs = cRectangle(
            sidebarX + panelInset,
            TopBarHeight + 220,
            panelWidth,
            34
        );
        layout.catalog = cRectangle(
            sidebarX + panelInset,
            catalogY,
            panelWidth,
            std::max(0, catalogBottom - catalogY)
        );
        layout.scrollbar = cRectangle(
            layout.catalog.getEndX() - 10,
            layout.catalog.getY(),
            10,
            layout.catalog.getHeight()
        );
        layout.cards = cRectangle(
            layout.catalog.getX(),
            layout.catalog.getY(),
            layout.catalog.getWidth() - 15,
            layout.catalog.getHeight()
        );

        const int gapsWidth = (layout.columns - 1) * layout.cardGap;
        layout.cardWidth =
            (layout.cards.getWidth() - gapsWidth) / layout.columns;
        const int imageHeight =
            std::max(1, (layout.cardWidth - 4) * 3 / 4);
        layout.cardHeight = imageHeight + 32;
        return layout;
    }

    [[nodiscard]] int visibleRows() const
    {
        const int stride = cardHeight + cardGap;
        return stride > 0
            ? std::max(1, (cards.getHeight() + cardGap) / stride)
            : 1;
    }

    [[nodiscard]] int totalRows(int itemCount) const
    {
        return itemCount <= 0 ? 0 : (itemCount + columns - 1) / columns;
    }

    [[nodiscard]] int maxScrollRow(int itemCount) const
    {
        return std::max(0, totalRows(itemCount) - visibleRows());
    }

    [[nodiscard]] cRectangle cardRect(
        int itemIndex,
        int scrollRow) const
    {
        const int row = itemIndex / columns - scrollRow;
        const int column = itemIndex % columns;
        return cRectangle(
            cards.getX() + column * (cardWidth + cardGap),
            cards.getY() + row * (cardHeight + cardGap),
            cardWidth,
            cardHeight
        );
    }

    [[nodiscard]] cRectangle tabRect(int tabIndex, int tabCount = 6) const
    {
        const int width = tabs.getWidth() / tabCount;
        const int x = tabs.getX() + tabIndex * width;
        const int actualWidth =
            tabIndex == tabCount - 1 ? tabs.getEndX() - x : width;
        return cRectangle(x, tabs.getY(), actualWidth, tabs.getHeight());
    }

    [[nodiscard]] cRectangle scrollbarThumb(
        int itemCount,
        int scrollRow) const
    {
        if (maxScrollRow(itemCount) <= 0) {
            return scrollbar;
        }

        const int total = std::max(1, totalRows(itemCount));
        const int thumbHeight = std::max(
            22,
            scrollbar.getHeight() * visibleRows() / total
        );
        const int travel = scrollbar.getHeight() - thumbHeight;
        const int thumbY = scrollbar.getY() +
            travel * std::clamp(scrollRow, 0, maxScrollRow(itemCount)) /
            maxScrollRow(itemCount);
        return cRectangle(
            scrollbar.getX(),
            thumbY,
            scrollbar.getWidth(),
            thumbHeight
        );
    }
};
