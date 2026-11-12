#pragma once

namespace outpost_dish {

inline constexpr int FrameCount = 32;
inline constexpr int CallsPerFrame = 55;

inline void advance(int &frame, int &timer)
{
    ++timer;
    if (timer >= CallsPerFrame) {
        ++frame;
        if (frame >= FrameCount) {
            frame = 0;
        }
        timer = 0;
    }
}

}
