#pragma once

#include <algorithm>
#include <cmath>
#include <cstdint>

constexpr float FactionTintReferenceLuminance = 166.0F / 255.0F;

[[nodiscard]] inline std::uint8_t applyFactionTintChannel(
    std::uint8_t target,
    float pixelLuminance,
    float averageLuminance)
{
    const float correction = FactionTintReferenceLuminance /
        std::max(0.01F, averageLuminance);
    return static_cast<std::uint8_t>(std::lround(std::clamp(
        target * pixelLuminance * correction,
        0.0F,
        255.0F
    )));
}
