#pragma once

#include "include/definitions.h"

#include <array>

struct HdHouseFlag {
    int structureType;
    const char *textureName;
    int frameWidth;
    int frameHeight;
};

[[nodiscard]] inline const HdHouseFlag *findHdHouseFlag(int structureType)
{
    static constexpr std::array<HdHouseFlag, 12> flags{{
        {RADAR, "BUILD_RADAR_FLAG", 64, 64},
        {BARRACKS, "BUILD_BARRACKS_FLAG", 64, 64},
        {WOR, "BUILD_WOR_FLAG", 64, 64},
        {REFINERY, "BUILD_REFINERY_FLAG", 96, 64},
        {WINDTRAP, "BUILD_WINDTRAP_FLAG", 64, 64},
        {SILO, "BUILD_SILO_FLAG", 64, 64},
        {STARPORT, "BUILD_STARPORT_FLAG", 96, 96},
        {PALACE, "BUILD_PALACE_FLAG", 96, 96},
        {IX, "BUILD_IX_FLAG", 64, 64},
        {LIGHTFACTORY, "BUILD_LIGHTFACTORY_FLAG", 64, 64},
        {HIGHTECH, "BUILD_HIGHTECH_FLAG", 96, 64},
        {CONSTYARD, "BUILD_CONSTYARD_FLAG", 64, 64},
    }};
    for (const auto &flag : flags) {
        if (flag.structureType == structureType) {
            return &flag;
        }
    }
    return nullptr;
}
