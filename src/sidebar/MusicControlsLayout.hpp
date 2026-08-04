#pragma once

#include "utils/cRectangle.h"

#include <algorithm>

struct MusicControlsLayout {
    bool visible = false;
    cRectangle panel;
    cRectangle previous;
    cRectangle label;
    cRectangle next;

    [[nodiscard]] static MusicControlsLayout create(
        int left,
        int right,
        bool hd)
    {
        constexpr int MinimumWidth = 70;
        constexpr int MaximumWidth = 520;
        const int availableWidth = std::max(0, right - left);
        if (availableWidth < MinimumWidth) {
            return {};
        }

        const int width = std::min(availableWidth, MaximumWidth);
        const int buttonSize = hd ? 33 : 28;
        const int y = hd ? 4 : 1;
        const int gap = 5;
        const int labelX = left + buttonSize + gap;
        const int labelWidth = std::max(0, width - buttonSize * 2 - gap * 2);

        MusicControlsLayout result;
        result.visible = true;
        result.panel = cRectangle(left, y, width, buttonSize);
        result.previous = cRectangle(left, y, buttonSize, buttonSize);
        result.label = cRectangle(labelX, y, labelWidth, buttonSize);
        result.next = cRectangle(left + width - buttonSize, y, buttonSize, buttonSize);
        return result;
    }

    [[nodiscard]] bool showsLabel() const
    {
        return label.getWidth() >= 80;
    }
};
