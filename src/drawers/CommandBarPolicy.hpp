#pragma once

#include "controls/CommandModePolicy.hpp"
#include "drawers/CommandIcons.hpp"
#include "utils/Utf8.hpp"

#include <string>

[[nodiscard]] constexpr bool isMoveCommandEnabled(bool hasSelectedUnits)
{
    return hasSelectedUnits;
}

[[nodiscard]] constexpr bool isAttackCommandEnabled(bool hasAttackCapableUnit)
{
    return hasAttackCapableUnit;
}

[[nodiscard]] constexpr bool isRepairCommandEnabled()
{
    return true;
}

[[nodiscard]] constexpr bool isUnloadCommandEnabled(bool hasUnloadableHarvester)
{
    return hasUnloadableHarvester;
}

[[nodiscard]] constexpr bool isDeployCommandEnabled(bool hasSelectedMcv)
{
    return hasSelectedMcv;
}

[[nodiscard]] constexpr bool isRallyCommandEnabled(
    bool ownsSelectedStructure,
    bool selectedStructureCanSpawnUnits
) {
    return ownsSelectedStructure && selectedStructureCanSpawnUnits;
}

[[nodiscard]] constexpr bool isReleaseCommandEnabled(
    bool ownsSelectedStructure,
    bool selectedStructureIsRepairFacility
) {
    return ownsSelectedStructure && selectedStructureIsRepairFacility;
}

[[nodiscard]] constexpr bool isCommandButtonActive(CommandIcon command, const CommandTargetingState &state)
{
    switch (command) {
        case CommandIcon::Move:
            return state.move;
        case CommandIcon::Attack:
            return state.attack;
        case CommandIcon::Repair:
            return state.repair;
        case CommandIcon::Rally:
            return state.rally;
        default:
            return false;
    }
}

[[nodiscard]] inline std::string cornerKeyLabel(const std::string &keyLabel)
{
    return utf8CodePointCount(keyLabel) == 1 ? keyLabel : std::string();
}

[[nodiscard]] inline std::string commandTooltip(const std::string &caption, const std::string &keyLabel)
{
    return keyLabel.empty() ? caption : caption + " (" + keyLabel + ")";
}
