#pragma once

#include <array>

struct RenderCanvasSize {
    int width;
    int height;

    bool operator==(const RenderCanvasSize &) const = default;
};

constexpr int MinimumRenderWidth = 800;
constexpr int MinimumRenderHeight = 600;
constexpr int AutomaticRenderScale = 0;
constexpr std::array<int, 5> ManualRenderScales{100, 125, 150, 175, 200};

[[nodiscard]] int calculateAutomaticRenderScalePercent(int outputWidth, int outputHeight);
[[nodiscard]] bool isManualRenderScaleAvailable(
    int outputWidth,
    int outputHeight,
    int renderScalePercent
);
[[nodiscard]] RenderCanvasSize calculateRenderCanvasSize(
    int outputWidth,
    int outputHeight,
    int renderScalePercent
);
