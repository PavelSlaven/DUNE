#pragma once

#include <array>

constexpr int AutomaticWorldScale = 0;
constexpr std::array<int, 4> ManualWorldScales{100, 110, 125, 150};

[[nodiscard]] bool isWorldScaleSupported(int worldScalePercent);
[[nodiscard]] int calculateAutomaticWorldScalePercent(int outputHeight);
[[nodiscard]] int resolveWorldScalePercent(
    int selectedWorldScalePercent,
    int outputHeight
);
[[nodiscard]] int selectHdAssetDensityForDisplay(
    int outputWidth,
    int outputHeight,
    int logicalWidth,
    int logicalHeight,
    int worldScalePercent
);
