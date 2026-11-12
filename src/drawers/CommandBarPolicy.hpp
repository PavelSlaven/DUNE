#pragma once

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
