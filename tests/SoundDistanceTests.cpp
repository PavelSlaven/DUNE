#include "utils/SoundDistance.hpp"

#include <cmath>
#include <iostream>

namespace {
bool expectNear(const char *label, float actual, float expected)
{
    if (std::fabs(actual - expected) <= 1e-3f * std::fabs(expected)) {
        return true;
    }
    std::cerr << label << ": got " << actual << ", expected " << expected << "\n";
    return false;
}
}

int main()
{
    constexpr int mapDistance = 4000;
    const float scales[] = {1.0f, 1.1f, 1.25f, 1.5f};
    const float baseDistance = soundMaxDistance(mapDistance, 1.0f, 1.0f);
    const float baseFactor = soundVolumeFactor(1.0f, 1.0f);
    const float zoomedDistance = soundMaxDistance(mapDistance, 1.2f, 1.0f);
    const float zoomedFactor = soundVolumeFactor(1.2f, 1.0f);

    bool passed = true;
    for (const float scale : scales) {
        passed &= expectNear("distance at Z = S", soundMaxDistance(mapDistance, scale, scale), baseDistance);
        passed &= expectNear("factor at Z = S", soundVolumeFactor(scale, scale), baseFactor);
        passed &= expectNear("distance at Z = 1.2 S", soundMaxDistance(mapDistance, 1.2f * scale, scale), zoomedDistance);
        passed &= expectNear("factor at Z = 1.2 S", soundVolumeFactor(1.2f * scale, scale), zoomedFactor);
    }
    return passed ? 0 : 1;
}
