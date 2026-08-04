#pragma once

#include <algorithm>
#include <cmath>

struct WorldObjectLayout {
    int x;
    int y;
    int width;
    int height;
};

/**
 * WorldScale is visual only. Buildings stay anchored to the bottom of their
 * logical footprint, so allowing the full configured range does not move
 * their gameplay cells or collision geometry.
 */
inline float structureWorldScaleFactor(float worldScaleFactor)
{
    return std::clamp(worldScaleFactor, 0.5F, 1.5F);
}

/** Keep every unit at the configured world scale, regardless of HD artwork. */
inline float unitWorldScaleFactor(
    float worldScaleFactor,
    bool /*hdGraphics*/,
    bool /*enlargedHdTank*/)
{
    return worldScaleFactor;
}

/**
 * Keep the harvester on the refinery pad at exactly the same visual scale
 * as the unit uses on the map.  The transparent 80x52 unit frame extends
 * beyond the pad, while its visible south-facing body stays on the deck.
 */
inline WorldObjectLayout refineryHarvesterLayout(
    int refineryX,
    int refineryY,
    int refineryWidth,
    int refineryHeight)
{
    constexpr float logicalRefineryWidth = 96.0F;
    constexpr float logicalRefineryHeight = 64.0F;
    constexpr float logicalOffsetX = 30.0F;
    constexpr float logicalOffsetY = 15.0F;
    constexpr float logicalHarvesterWidth = 80.0F;
    constexpr float logicalHarvesterHeight = 52.0F;
    return {
        refineryX + static_cast<int>(std::lround(
            refineryWidth * logicalOffsetX / logicalRefineryWidth
        )),
        refineryY + static_cast<int>(std::lround(
            refineryHeight * logicalOffsetY / logicalRefineryHeight
        )),
        std::max(1, static_cast<int>(std::lround(
            refineryWidth * logicalHarvesterWidth /
                logicalRefineryWidth
        ))),
        std::max(1, static_cast<int>(std::lround(
            refineryHeight * logicalHarvesterHeight /
                logicalRefineryHeight
        )))
    };
}
