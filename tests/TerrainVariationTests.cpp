#include "drawers/TerrainVariation.hpp"

#include <array>
#include <cassert>
#include <cstring>

int main()
{
    assert(hdTerrainVariantIndex(-1, TERRAIN_SAND) == 0);
    assert(hdTerrainVariantIndex(42, TERRAIN_WALL) == 0);
    assert(hdTerrainVariantName(TERRAIN_SAND, 0, 0) == nullptr);
    assert(hdTerrainVariantName(TERRAIN_SAND, 0, 5) == nullptr);
    assert(hdTerrainVariantName(TERRAIN_SAND, 1, 3) == nullptr);
    assert(
        std::strcmp(
            hdTerrainVariantName(TERRAIN_SAND, 0, 3),
            "TERRAIN_SAND_VAR_03"
        ) == 0
    );

    std::array<bool, HD_TERRAIN_VARIANT_COUNT> seen = {};
    for (int cell = 0; cell < 4096; ++cell) {
        const int first = hdTerrainVariantIndex(cell, TERRAIN_SAND);
        const int second = hdTerrainVariantIndex(cell, TERRAIN_SAND);
        assert(first == second);
        assert(first >= 0 && first < HD_TERRAIN_VARIANT_COUNT);
        seen[first] = true;
    }
    for (bool present : seen) {
        assert(present);
    }
    return 0;
}
