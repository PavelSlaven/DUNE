#include "RenderScale.hpp"

#include <algorithm>
#include <cmath>

namespace {
int normalizedOutputWidth(int outputWidth)
{
    return std::max(outputWidth, MinimumRenderWidth);
}

int normalizedOutputHeight(int outputHeight)
{
    return std::max(outputHeight, MinimumRenderHeight);
}

double automaticRenderScale(int outputWidth, int outputHeight)
{
    const double horizontalScale =
        static_cast<double>(normalizedOutputWidth(outputWidth)) / MinimumRenderWidth;
    const double verticalScale =
        static_cast<double>(normalizedOutputHeight(outputHeight)) / MinimumRenderHeight;
    return std::min(horizontalScale, verticalScale);
}
}

int calculateAutomaticRenderScalePercent(int outputWidth, int outputHeight)
{
    return static_cast<int>(std::lround(automaticRenderScale(outputWidth, outputHeight) * 100.0));
}

bool isManualRenderScaleAvailable(
    int outputWidth,
    int outputHeight,
    int renderScalePercent)
{
    if (std::ranges::find(ManualRenderScales, renderScalePercent) ==
        ManualRenderScales.end()) {
        return false;
    }

    const int width = normalizedOutputWidth(outputWidth);
    const int height = normalizedOutputHeight(outputHeight);
    return
        static_cast<long long>(width) * 100 >=
            static_cast<long long>(MinimumRenderWidth) * renderScalePercent &&
        static_cast<long long>(height) * 100 >=
            static_cast<long long>(MinimumRenderHeight) * renderScalePercent;
}

RenderCanvasSize calculateRenderCanvasSize(
    int outputWidth,
    int outputHeight,
    int renderScalePercent)
{
    const int width = normalizedOutputWidth(outputWidth);
    const int height = normalizedOutputHeight(outputHeight);
    const double scale =
        isManualRenderScaleAvailable(width, height, renderScalePercent)
            ? static_cast<double>(renderScalePercent) / 100.0
            : automaticRenderScale(width, height);

    return {
        std::max(
            MinimumRenderWidth,
            static_cast<int>(std::lround(static_cast<double>(width) / scale))
        ),
        std::max(
            MinimumRenderHeight,
            static_cast<int>(std::lround(static_cast<double>(height) / scale))
        )
    };
}
