#pragma once

#include "utils/cRectangle.h"

#include <algorithm>
#include <cstdint>

struct OutcomeScreenLayout {
    cRectangle image;
    cRectangle prompt;
};

[[nodiscard]] inline OutcomeScreenLayout calculateOutcomeScreenLayout(
    int screenWidth,
    int screenHeight,
    int imageWidth,
    int imageHeight)
{
    screenWidth = std::max(1, screenWidth);
    screenHeight = std::max(1, screenHeight);
    imageWidth = std::max(1, imageWidth);
    imageHeight = std::max(1, imageHeight);

    const int margin = std::max(
        12,
        std::min(screenWidth, screenHeight) / 32
    );
    const int availableWidth = std::max(1, screenWidth - margin * 2);
    const int availableHeight = std::max(1, screenHeight - margin * 2);

    int drawWidth = availableWidth;
    int drawHeight = static_cast<int>(
        static_cast<std::int64_t>(availableWidth) * imageHeight / imageWidth
    );
    if (drawHeight > availableHeight) {
        drawHeight = availableHeight;
        drawWidth = static_cast<int>(
            static_cast<std::int64_t>(availableHeight) * imageWidth / imageHeight
        );
    }
    drawWidth = std::max(1, drawWidth);
    drawHeight = std::max(1, drawHeight);

    const cRectangle image{
        (screenWidth - drawWidth) / 2,
        (screenHeight - drawHeight) / 2,
        drawWidth,
        drawHeight
    };

    const int promptWidth = std::max(1, drawWidth * 48 / 100);
    const int promptHeight = std::max(1, drawHeight * 5 / 100);
    const int rightInset = std::max(1, drawWidth * 6 / 100);
    const int bottomInset = std::max(1, drawHeight * 7 / 100);
    const cRectangle prompt{
        image.getEndX() - rightInset - promptWidth,
        image.getEndY() - bottomInset - promptHeight,
        promptWidth,
        promptHeight
    };

    return {image, prompt};
}
