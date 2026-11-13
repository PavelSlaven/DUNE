#pragma once

#include "utils/cRectangle.h"

#include <algorithm>
#include <array>

struct NewMapDialogLayout {
    static constexpr int RowCount = 7;

    cRectangle panel;
    cRectangle title;
    std::array<cRectangle, RowCount> labels{};
    std::array<cRectangle, RowCount> fields{};
    cRectangle returnButton;
    cRectangle createButton;

    [[nodiscard]] static NewMapDialogLayout create(int screenWidth, int screenHeight)
    {
        constexpr int panelWidth = 520;
        constexpr int innerMargin = 24;
        constexpr int titleHeight = 40;
        constexpr int rowHeight = 32;
        constexpr int rowStride = 44;
        constexpr int buttonHeight = 40;
        constexpr int labelWidth = 200;
        constexpr int columnGap = 16;
        constexpr int buttonGap = 16;
        constexpr int gapAfterTitle = 12;
        constexpr int gapBeforeButtons = 8;

        constexpr int contentWidth = panelWidth - innerMargin * 2;
        constexpr int panelHeight = innerMargin + titleHeight + gapAfterTitle + RowCount * rowStride +
                                    gapBeforeButtons + buttonHeight + innerMargin;
        const int panelX = std::max(0, (screenWidth - panelWidth) / 2);
        const int panelY = std::max(0, (screenHeight - panelHeight) / 2);
        const int contentX = panelX + innerMargin;

        NewMapDialogLayout result;
        result.panel = cRectangle(panelX, panelY, panelWidth, panelHeight);
        result.title = cRectangle(contentX, panelY + innerMargin, contentWidth, titleHeight);
        const int firstRowY = result.title.getEndY() + gapAfterTitle;
        for (int row = 0; row < RowCount; ++row) {
            const int y = firstRowY + row * rowStride;
            result.labels[row] = cRectangle(contentX, y, labelWidth, rowHeight);
            result.fields[row] = cRectangle(
                contentX + labelWidth + columnGap, y, contentWidth - labelWidth - columnGap, rowHeight);
        }
        const int buttonsY = firstRowY + RowCount * rowStride + gapBeforeButtons;
        const int buttonWidth = (contentWidth - buttonGap) / 2;
        result.returnButton = cRectangle(contentX, buttonsY, buttonWidth, buttonHeight);
        result.createButton = cRectangle(contentX + buttonWidth + buttonGap, buttonsY, buttonWidth, buttonHeight);
        return result;
    }
};
