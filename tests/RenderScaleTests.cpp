#include "utils/RenderScale.hpp"

#include <format>
#include <iostream>
#include <string_view>

namespace {
bool expectCanvas(
    std::string_view name,
    int outputWidth,
    int outputHeight,
    int scalePercent,
    RenderCanvasSize expected)
{
    const RenderCanvasSize actual =
        calculateRenderCanvasSize(outputWidth, outputHeight, scalePercent);
    if (actual == expected) {
        return true;
    }

    std::cerr << std::format(
        "{}: expected {}x{}, got {}x{}\n",
        name,
        expected.width,
        expected.height,
        actual.width,
        actual.height
    );
    return false;
}
}

int main()
{
    bool passed = true;
    passed &= expectCanvas("800x600 Auto", 800, 600, 0, {800, 600});
    passed &= expectCanvas("1024x768 Auto", 1024, 768, 0, {800, 600});
    passed &= expectCanvas("1280x720 Auto", 1280, 720, 0, {1067, 600});
    passed &= expectCanvas("1920x1080 Auto", 1920, 1080, 0, {1067, 600});
    passed &= expectCanvas("1920x1080 100%", 1920, 1080, 100, {1920, 1080});
    passed &= expectCanvas("1920x1080 175%", 1920, 1080, 175, {1097, 617});
    passed &= expectCanvas("2560x1440 Auto", 2560, 1440, 0, {1067, 600});
    passed &= expectCanvas("5120x1440 Auto", 5120, 1440, 0, {2133, 600});

    if (calculateAutomaticRenderScalePercent(1920, 1080) != 180) {
        std::cerr << "1920x1080 Auto must display 180%\n";
        passed = false;
    }
    if (!isManualRenderScaleAvailable(1920, 1080, 175)) {
        std::cerr << "175% must be available at 1920x1080\n";
        passed = false;
    }
    if (isManualRenderScaleAvailable(1920, 1080, 200)) {
        std::cerr << "200% must be unavailable at 1920x1080\n";
        passed = false;
    }

    return passed ? 0 : 1;
}
