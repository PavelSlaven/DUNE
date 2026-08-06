#pragma once

#include "utils/cRectangle.h"

#include <algorithm>

struct MusicControlsLayout {
    bool visible = false;
    cRectangle panel;
    cRectangle musicPanel;
    cRectangle previous;
    cRectangle label;
    cRectangle next;
    cRectangle speedPanel;
    cRectangle speedLabel;
    cRectangle speedSlider;

    [[nodiscard]] static MusicControlsLayout create(
        int left,
        int right,
        bool hd)
    {
        constexpr int MinimumWidth = 200;
        constexpr int MaximumWidth = 520;
        const int availableWidth = std::max(0, right - left);
        if (availableWidth < MinimumWidth) {
            return {};
        }

        const int width = std::min(availableWidth, MaximumWidth);
        const int buttonSize = hd ? 33 : 28;
        const int y = hd ? 4 : 1;
        const int gap = 5;
        const int sectionGap = hd ? 8 : 5;
        const int contentWidth = width - sectionGap;
        const int musicWidth = contentWidth / 2;
        const int speedWidth = contentWidth - musicWidth;
        const int labelX = left + buttonSize + gap;
        const int labelWidth = std::max(0, musicWidth - buttonSize * 2 - gap * 2);
        const int speedX = left + musicWidth + sectionGap;
        const int speedLabelWidth = std::min(hd ? 76 : 66, speedWidth / 2);
        const int speedSliderX = speedX + speedLabelWidth + gap;
        const int speedSliderWidth = std::max(0, speedWidth - speedLabelWidth - gap);

        MusicControlsLayout result;
        result.visible = true;
        result.panel = cRectangle(left, y, width, buttonSize);
        result.musicPanel = cRectangle(left, y, musicWidth, buttonSize);
        result.previous = cRectangle(left, y, buttonSize, buttonSize);
        result.label = cRectangle(labelX, y, labelWidth, buttonSize);
        result.next = cRectangle(left + musicWidth - buttonSize, y, buttonSize, buttonSize);
        result.speedPanel = cRectangle(speedX, y, speedWidth, buttonSize);
        result.speedLabel = cRectangle(speedX, y, speedLabelWidth, buttonSize);
        result.speedSlider = cRectangle(speedSliderX, y, speedSliderWidth, buttonSize);
        return result;
    }

    [[nodiscard]] bool showsLabel() const
    {
        return label.getWidth() >= 80;
    }
};
