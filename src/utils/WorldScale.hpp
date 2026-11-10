#pragma once

#include <algorithm>
#include <array>

inline constexpr int AutomaticWorldScale = 0;
inline constexpr std::array<int, 4> ManualWorldScales{100, 110, 125, 150};

inline bool isWorldScaleSupported(int worldScalePercent)
{
    return worldScalePercent == AutomaticWorldScale
        || std::find(ManualWorldScales.begin(), ManualWorldScales.end(), worldScalePercent) != ManualWorldScales.end();
}

inline int calculateAutomaticWorldScalePercent(int outputHeight)
{
    if (outputHeight <= 768) {
        return 100;
    }
    if (outputHeight <= 1080) {
        return 110;
    }
    if (outputHeight <= 1600) {
        return 125;
    }
    return 150;
}

inline int resolveWorldScalePercent(int selectedWorldScalePercent, int outputHeight)
{
    if (selectedWorldScalePercent == AutomaticWorldScale || !isWorldScaleSupported(selectedWorldScalePercent)) {
        return calculateAutomaticWorldScalePercent(outputHeight);
    }
    return selectedWorldScalePercent;
}

inline float worldScaleZoom(int selectedWorldScalePercent, int outputHeight)
{
    return static_cast<float>(resolveWorldScalePercent(selectedWorldScalePercent, outputHeight)) / 100.0f;
}
