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
 * Keep the harvester on the refinery pad at exactly the same visual scale
 * as the unit uses on the map.  The transparent 80x52 unit frame extends
 * beyond the pad, while its visible south-facing body is centred on the deck.
 */
inline WorldObjectLayout refineryHarvesterLayout(
    int refineryX,
    int refineryY,
    int refineryWidth,
    int refineryHeight)
{
    constexpr float logicalRefineryWidth = 96.0F;
    constexpr float logicalRefineryHeight = 64.0F;
    constexpr float logicalOffsetX = 26.75F;
    constexpr float logicalOffsetY = 17.375F;
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
