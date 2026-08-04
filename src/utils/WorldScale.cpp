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

int selectHdAssetDensityForDisplay(
    int outputWidth,
    int outputHeight,
    int logicalWidth,
    int logicalHeight,
    int worldScalePercent)
{
    // A 4K-class physical output has enough pixels to expose the HD2 source
    // texels even when the logical canvas is deliberately large.  Prefer the
    // true HD4 masters there; camera zoom can enlarge world sprites further.
    if (outputWidth >= 3840 || outputHeight >= 2160) {
        return 4;
    }
    const double canvasScale = std::min(
        static_cast<double>(std::max(1, outputWidth)) /
            std::max(1, logicalWidth),
        static_cast<double>(std::max(1, outputHeight)) /
            std::max(1, logicalHeight)
    );
    const double objectScale =
        canvasScale * resolveWorldScalePercent(
            worldScalePercent,
            outputHeight
        ) / 100.0;
    return objectScale > 2.0 ? 4 : 2;
}
