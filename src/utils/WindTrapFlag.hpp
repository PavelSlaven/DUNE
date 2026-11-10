#pragma once

#include <cstdint>

inline constexpr int kWindTrapFlagFrames = 8;
inline constexpr int kWindTrapFlagFrameSize = 64;

inline int windTrapFlagFrame(std::uint64_t ticksMs)
{
    return static_cast<int>((ticksMs / 125U) % kWindTrapFlagFrames);
}
