#pragma once

#include "data/gfxdata.h"

#include <array>
#include <cstdint>

inline constexpr int HD_TERRAIN_VARIANT_COUNT = 5;

inline bool supportsHdTerrainVariants(int terrainType)
{
    switch (terrainType) {
        case TERRAIN_HILL:
        case TERRAIN_MOUNTAIN:
        case TERRAIN_ROCK:
        case TERRAIN_SAND:
        case TERRAIN_SPICE:
        case TERRAIN_SPICEHILL:
            return true;
        default:
            return false;
    }
}

inline int hdTerrainVariantIndex(int cellId, int terrainType)
{
    if (cellId < 0 || !supportsHdTerrainVariants(terrainType)) {
        return 0;
    }

    std::uint32_t value =
        static_cast<std::uint32_t>(cellId) ^
        (static_cast<std::uint32_t>(terrainType) * 0x9e3779b9U);
    value ^= value >> 16U;
    value *= 0x7feb352dU;
    value ^= value >> 15U;
    value *= 0x846ca68bU;
    value ^= value >> 16U;
    return static_cast<int>(value % HD_TERRAIN_VARIANT_COUNT);
}

inline const char *hdTerrainVariantName(
    int terrainType,
    int tileIndex,
    int variant)
{
    // Transition frames carry neighbour topology. Substituting independently
    // varied versions of those frames creates rectangular patches and seams.
    if (tileIndex != 0 ||
        variant <= 0 ||
        variant >= HD_TERRAIN_VARIANT_COUNT) {
        return nullptr;
    }

    static constexpr std::array<const char *, 4> hill = {
        "TERRAIN_HILL_VAR_01",
        "TERRAIN_HILL_VAR_02",
        "TERRAIN_HILL_VAR_03",
        "TERRAIN_HILL_VAR_04",
    };
    static constexpr std::array<const char *, 4> mountain = {
        "TERRAIN_MOUNTAIN_VAR_01",
        "TERRAIN_MOUNTAIN_VAR_02",
        "TERRAIN_MOUNTAIN_VAR_03",
        "TERRAIN_MOUNTAIN_VAR_04",
    };
    static constexpr std::array<const char *, 4> rock = {
        "TERRAIN_ROCK_VAR_01",
        "TERRAIN_ROCK_VAR_02",
        "TERRAIN_ROCK_VAR_03",
        "TERRAIN_ROCK_VAR_04",
    };
    static constexpr std::array<const char *, 4> sand = {
        "TERRAIN_SAND_VAR_01",
        "TERRAIN_SAND_VAR_02",
        "TERRAIN_SAND_VAR_03",
        "TERRAIN_SAND_VAR_04",
    };
    static constexpr std::array<const char *, 4> spice = {
        "TERRAIN_SPICE_VAR_01",
        "TERRAIN_SPICE_VAR_02",
        "TERRAIN_SPICE_VAR_03",
        "TERRAIN_SPICE_VAR_04",
    };
    static constexpr std::array<const char *, 4> spiceHill = {
        "TERRAIN_SPICEHILL_VAR_01",
        "TERRAIN_SPICEHILL_VAR_02",
        "TERRAIN_SPICEHILL_VAR_03",
        "TERRAIN_SPICEHILL_VAR_04",
    };

    const std::array<const char *, 4> *names = nullptr;
    switch (terrainType) {
        case TERRAIN_HILL: names = &hill; break;
        case TERRAIN_MOUNTAIN: names = &mountain; break;
        case TERRAIN_ROCK: names = &rock; break;
        case TERRAIN_SAND: names = &sand; break;
        case TERRAIN_SPICE: names = &spice; break;
        case TERRAIN_SPICEHILL: names = &spiceHill; break;
        default: return nullptr;
    }
    return (*names)[variant - 1];
}
