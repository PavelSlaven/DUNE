#include "WorldScale.hpp"

#include <algorithm>
#include <ranges>

bool isWorldScaleSupported(int worldScalePercent)
{
    return worldScalePercent == AutomaticWorldScale ||
        std::ranges::find(ManualWorldScales, worldScalePercent) !=
            ManualWorldScales.end();
}

int calculateAutomaticWorldScalePercent(int outputHeight)
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

int resolveWorldScalePercent(
    int selectedWorldScalePercent,
    int outputHeight)
{
    if (selectedWorldScalePercent == AutomaticWorldScale) {
        return calculateAutomaticWorldScalePercent(outputHeight);
    }
    return isWorldScaleSupported(selectedWorldScalePercent)
        ? selectedWorldScalePercent
        : calculateAutomaticWorldScalePercent(outputHeight);
}
