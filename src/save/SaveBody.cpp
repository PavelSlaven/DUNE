#include "save/SaveBody.hpp"

#include "data/gfxdata.h"
#include "include/enums/BuildEnums.h"
#include "include/enums/ListEnums.h"
#include "include/enums/MapEnums.h"
#include "utils/Localization.hpp"

#include <array>
#include <cmath>
#include <iomanip>
#include <istream>
#include <limits>
#include <ostream>
#include <sstream>
#include <string>
#include <string_view>

namespace save_game_detail {

template<typename T>
void writeArray(std::ostream &output, const T &values)
{
    for (const auto &value : values) {
        output << ' ' << value;
    }
}

template<typename T>
bool readValue(std::istream &input, T &value)
{
    input >> value;
    return static_cast<bool>(input);
}

bool readBool(std::istream &input, bool &value)
{
    int raw = 0;
    if (!readValue(input, raw) || (raw != 0 && raw != 1)) {
        return false;
    }
    value = raw != 0;
    return true;
}

template<typename T>
bool readArray(std::istream &input, T &values)
{
    for (auto &value : values) {
        if (!readValue(input, value)) {
            return false;
        }
    }
    return true;
}

bool expectTag(std::istream &input, std::string_view expected)
{
    std::string tag;
    return readValue(input, tag) && tag == expected;
}

std::string serializeBody(const SaveSnapshot &save)
{
    std::ostringstream output;
    output << std::setprecision(std::numeric_limits<float>::max_digits10);
    output << "INFO " << std::quoted(save.saveName) << '\n';
    output << "META "
           << save.skirmish << ' '
           << save.region << ' '
           << save.mission << ' '
           << save.winFlags << ' '
           << save.loseFlags << ' '
           << save.cameraCell << '\n';
    output << "MAP "
           << save.mapWidth << ' '
           << save.mapHeight << ' '
           << save.autoSpawnBlooms << ' '
           << save.autoDetonateBlooms << ' '
           << save.bloomTimer << ' '
           << save.desiredWorms << ' '
           << save.wormRespawnTimer << '\n';
    output << "PLAYERS " << save.players.size() << '\n';
    for (std::size_t index = 0; index < save.players.size(); ++index) {
        const PlayerState &player = save.players[index];
        output << "PLAYER " << index << ' '
               << player.house << ' '
               << player.team << ' '
               << player.techLevel << ' '
               << player.focusCell << ' '
               << player.quota << ' '
               << player.selectedStructure << ' '
               << player.credits << ' '
               << player.maxCredits << ' '
               << player.powerUsage << ' '
               << player.powerProduce << ' '
               << player.alive << ' '
               << player.autoSlab;
        writeArray(output, player.primary);
        writeArray(output, player.structures);
        writeArray(output, player.upgrades);
        writeArray(output, player.appliedUpgrades);
        output << '\n';
    }
    output << "CELLS " << save.cells.size() << '\n';
    for (const CellState &cell : save.cells) {
        output << "CELL "
               << cell.credits << ' '
               << cell.type << ' '
               << cell.tile << ' '
               << cell.smudgeTile << ' '
               << cell.smudgeType << ' '
               << cell.health << ' '
               << cell.passable << ' '
               << cell.passableFoot << ' '
               << cell.visibilityMask << ' '
               << cell.seenMask << '\n';
    }
    output << "FOGMEMORY " << save.fog.size() << '\n';
    for (const FogState &item : save.fog) {
        output << "FOG "
               << item.cell << ' '
               << item.hasTerrain << ' '
               << item.terrainType << ' '
               << item.terrainTile << ' '
               << item.terrainSmudgeTile << ' '
               << item.terrainSmudgeType << ' '
               << item.hasStructure << ' '
               << item.structureType << ' '
               << item.structureOwner << ' '
               << item.structureFrame << ' '
               << item.structureOffsetX << ' '
               << item.structureOffsetY << ' '
               << item.hasUnit << ' '
               << item.unitType << ' '
               << item.unitOwner << ' '
               << item.unitBodyIndex << ' '
               << item.unitHeadIndex << ' '
               << item.unitFrame << '\n';
    }
    output << "STRUCTURES " << save.structures.size() << '\n';
    for (const StructureState &item : save.structures) {
        output << "STRUCTURE "
               << item.oldId << ' ' << item.type << ' ' << item.player << ' '
               << item.cell << ' ' << item.hitPoints << ' ' << item.rallyPoint << ' '
               << item.frame << ' ' << item.buildPhase << ' '
               << item.unitWithin << ' ' << item.unitEntering << ' '
               << item.unitHeading << ' ' << item.concrete << ' '
               << item.animate << ' ' << item.repair << ' '
               << item.animateOnApproach << ' ' << item.smoke << ' '
               << item.repairTimer << ' ' << item.flagTimer << ' '
               << item.reduceSmokeTimer << ' ' << item.decayTimer << ' '
               << item.prebuildTimer << '\n';
    }
    output << "UNITS " << save.units.size() << '\n';
    for (const UnitState &item : save.units) {
        output << "UNIT "
               << item.oldId << ' ' << item.type << ' ' << item.player << ' '
               << item.cell << ' ' << item.hitPoints << ' ' << item.tempHitPoints << ' '
               << item.posX << ' ' << item.posY << ' ' << item.experience << ' '
               << item.groupMask << ' ' << item.nextCell << ' ' << item.goalCell;
        writeArray(output, item.path);
        output << ' ' << item.pathIndex << ' ' << item.pathFails << ' '
               << item.calculatePath << ' ' << item.carryMe << ' ' << item.carryAll << ' '
               << item.attackUnit << ' ' << item.attackStructure << ' '
               << item.attackCell << ' ' << item.unitId << ' ' << item.structureId << ' '
               << item.credits << ' ' << item.transferType << ' ' << item.bringTarget << ' '
               << item.newUnitType << ' ' << item.lastDroppedOffCell << ' '
               << item.bodyFacing << ' ' << item.headFacing << ' '
               << item.bodyShouldFace << ' ' << item.headShouldFace << ' '
               << item.frame << ' ' << item.selected << ' ' << item.action << ' '
               << item.intent << ' ' << item.willBePickedUpBy << ' '
               << item.pickedUp << ' ' << item.removeMe << ' ' << item.mission << ' '
               << item.reinforcement << ' ' << item.unitsEaten << ' '
               << item.harvestCellMemory << ' ' << item.stayAtGoalCell;
        writeArray(output, item.timers);
        output << '\n';
    }
    output << "REINFORCEMENTS " << save.reinforcements.size() << '\n';
    for (const ReinforcementState &item : save.reinforcements) {
        output << "REINFORCEMENT "
               << item.delay << ' ' << item.unitType << ' ' << item.player << ' '
               << item.cell << ' ' << item.repeat << ' ' << item.remove << ' '
               << item.originalDelay << '\n';
    }
    output << "BUILD_QUEUE " << save.buildQueue.size() << '\n';
    for (const BuildQueueState &item : save.buildQueue) {
        output << "BUILD "
               << item.player << ' ' << item.slot << ' ' << item.timer << ' '
               << item.listType << ' ' << item.buildType << ' ' << item.buildId << ' '
               << item.subList << ' ' << item.progress << ' ' << item.buildFrame << ' '
               << item.timesToBuild << ' ' << item.timesOrdered << ' '
               << item.state << ' ' << item.placeIt << ' '
               << item.deployIt << ' ' << item.waitingForUnitSlot << ' '
               << item.progressFrameTimer << ' ' << item.flashingTimer << ' '
               << item.timerCap << '\n';
    }
    output << "FACTORYPADS " << save.factoryPads.size() << '\n';
    for (const FactoryPadSave &item : save.factoryPads) {
        output << "FACTORYPAD " << item.structureId << ' ';
        factory_pad::write(output, item.pad);
        output << '\n';
    }
    output << "END\n";
    return output.str();
}

bool deserializeBody(std::string_view body, SaveSnapshot &save, std::string &error)
{
    std::istringstream input{std::string(body)};
    std::string firstTag;
    if (!readValue(input, firstTag)) {
        error = localization::text("Save header is corrupted", "Повреждён заголовок сохранения");
        return false;
    }
    if (firstTag == "INFO") {
        if (!(input >> std::quoted(save.saveName)) || !expectTag(input, "META")) {
            error = localization::text("Save name is corrupted", "Имя сохранения повреждено");
            return false;
        }
    }
    else if (firstTag != "META") {
        error = localization::text("Save header is corrupted", "Повреждён заголовок сохранения");
        return false;
    }
    if (!readBool(input, save.skirmish) ||
        !readValue(input, save.region) ||
        !readValue(input, save.mission) ||
        !readValue(input, save.winFlags) ||
        !readValue(input, save.loseFlags) ||
        !readValue(input, save.cameraCell) ||
        !expectTag(input, "MAP") ||
        !readValue(input, save.mapWidth) ||
        !readValue(input, save.mapHeight) ||
        !readBool(input, save.autoSpawnBlooms) ||
        !readBool(input, save.autoDetonateBlooms) ||
        !readValue(input, save.bloomTimer) ||
        !readValue(input, save.desiredWorms) ||
        !readValue(input, save.wormRespawnTimer)) {
        error = localization::text("Save header is corrupted", "Повреждён заголовок сохранения");
        return false;
    }
    if (save.mapWidth < 4 || save.mapHeight < 4 || save.mapWidth > 256 || save.mapHeight > 256) {
        error = localization::text("Invalid map size in save", "Некорректный размер карты в сохранении");
        return false;
    }

    std::size_t count = 0;
    if (!expectTag(input, "PLAYERS") || !readValue(input, count) || count != MAX_PLAYERS) {
        error = localization::text("Invalid player list", "Некорректный список игроков");
        return false;
    }
    for (std::size_t index = 0; index < count; ++index) {
        std::size_t storedIndex = 0;
        PlayerState &player = save.players[index];
        if (!expectTag(input, "PLAYER") ||
            !readValue(input, storedIndex) || storedIndex != index ||
            !readValue(input, player.house) ||
            !readValue(input, player.team) ||
            !readValue(input, player.techLevel) ||
            !readValue(input, player.focusCell) ||
            !readValue(input, player.quota) ||
            !readValue(input, player.selectedStructure) ||
            !readValue(input, player.credits) ||
            !readValue(input, player.maxCredits) ||
            !readValue(input, player.powerUsage) ||
            !readValue(input, player.powerProduce) ||
            !readBool(input, player.alive) ||
            !readBool(input, player.autoSlab) ||
            !readArray(input, player.primary) ||
            !readArray(input, player.structures) ||
            !readArray(input, player.upgrades) ||
            !readArray(input, player.appliedUpgrades)) {
            error = localization::text("Player data is corrupted", "Повреждены данные игроков");
            return false;
        }
        if (player.house < 0 || player.house >= HouseCount ||
            !std::isfinite(player.credits) || !std::isfinite(player.maxCredits)) {
            error = localization::text("Invalid player settings", "Некорректные параметры игрока");
            return false;
        }
    }

    const std::size_t expectedCells = static_cast<std::size_t>(save.mapWidth) *
                                      static_cast<std::size_t>(save.mapHeight);
    if (!expectTag(input, "CELLS") || !readValue(input, count) || count != expectedCells) {
        error = localization::text("Invalid map data", "Некорректные данные карты");
        return false;
    }
    save.cells.resize(count);
    for (CellState &cell : save.cells) {
        if (!expectTag(input, "CELL") ||
            !readValue(input, cell.credits) ||
            !readValue(input, cell.type) ||
            !readValue(input, cell.tile) ||
            !readValue(input, cell.smudgeTile) ||
            !readValue(input, cell.smudgeType) ||
            !readValue(input, cell.health) ||
            !readBool(input, cell.passable) ||
            !readBool(input, cell.passableFoot) ||
            !readValue(input, cell.visibilityMask) ||
            !readValue(input, cell.seenMask)) {
            error = localization::text("Map cells are corrupted", "Ячейки карты повреждены");
            return false;
        }
        if (cell.type < TERRAIN_BLOOM || cell.type > TERRAIN_WALL ||
            cell.smudgeType < -1 || cell.smudgeType >= static_cast<int>(SmudgeType::COUNT)) {
            error = localization::text("Invalid terrain type", "Некорректный тип местности");
            return false;
        }
    }

    if (!expectTag(input, "FOGMEMORY") || !readValue(input, count) || count > expectedCells) {
        error = localization::text("Invalid fog memory list", "Некорректный список памяти тумана");
        return false;
    }
    save.fog.resize(count);
    int previousFogCell = -1;
    for (FogState &item : save.fog) {
        if (!expectTag(input, "FOG") ||
            !readValue(input, item.cell) ||
            !readBool(input, item.hasTerrain) ||
            !readValue(input, item.terrainType) ||
            !readValue(input, item.terrainTile) ||
            !readValue(input, item.terrainSmudgeTile) ||
            !readValue(input, item.terrainSmudgeType) ||
            !readBool(input, item.hasStructure) ||
            !readValue(input, item.structureType) ||
            !readValue(input, item.structureOwner) ||
            !readValue(input, item.structureFrame) ||
            !readValue(input, item.structureOffsetX) ||
            !readValue(input, item.structureOffsetY) ||
            !readBool(input, item.hasUnit) ||
            !readValue(input, item.unitType) ||
            !readValue(input, item.unitOwner) ||
            !readValue(input, item.unitBodyIndex) ||
            !readValue(input, item.unitHeadIndex) ||
            !readValue(input, item.unitFrame)) {
            error = localization::text("Fog memory is corrupted", "Повреждена память тумана");
            return false;
        }
        if (item.cell < 0 || item.cell >= static_cast<int>(expectedCells) ||
            item.cell <= previousFogCell || item.terrainSmudgeType < -1 ||
            item.terrainSmudgeType >= static_cast<int>(SmudgeType::COUNT)) {
            error = localization::text("Invalid fog memory data", "Некорректные данные памяти тумана");
            return false;
        }
        previousFogCell = item.cell;
    }

    if (!expectTag(input, "STRUCTURES") || !readValue(input, count) || count > MAX_STRUCTURES) {
        error = localization::text("Invalid structure list", "Некорректный список зданий");
        return false;
    }
    save.structures.resize(count);
    std::array<bool, MAX_STRUCTURES> usedStructureIds{};
    for (StructureState &item : save.structures) {
        if (!expectTag(input, "STRUCTURE") ||
            !readValue(input, item.oldId) || !readValue(input, item.type) ||
            !readValue(input, item.player) || !readValue(input, item.cell) ||
            !readValue(input, item.hitPoints) || !readValue(input, item.rallyPoint) ||
            !readValue(input, item.frame) || !readValue(input, item.buildPhase) ||
            !readValue(input, item.unitWithin) || !readValue(input, item.unitEntering) ||
            !readValue(input, item.unitHeading) || !readValue(input, item.concrete) ||
            !readBool(input, item.animate) || !readBool(input, item.repair) ||
            !readBool(input, item.animateOnApproach) || !readValue(input, item.smoke) ||
            !readValue(input, item.repairTimer) || !readValue(input, item.flagTimer) ||
            !readValue(input, item.reduceSmokeTimer) || !readValue(input, item.decayTimer) ||
            !readValue(input, item.prebuildTimer)) {
            error = localization::text("Structure data is corrupted", "Повреждены данные зданий");
            return false;
        }
        if (item.oldId < 0 || item.oldId >= MAX_STRUCTURES || usedStructureIds[item.oldId] ||
            item.type < 0 || item.type >= MAX_STRUCTURETYPES ||
            item.player < 0 || item.player >= MAX_PLAYERS ||
            item.cell < 0 || item.cell >= static_cast<int>(expectedCells) ||
            !std::isfinite(item.concrete)) {
            error = localization::text("Invalid reference in structure data", "Некорректная ссылка в данных здания");
            return false;
        }
        usedStructureIds[item.oldId] = true;
    }

    if (!expectTag(input, "UNITS") || !readValue(input, count) || count > UnitSlots) {
        error = localization::text("Invalid unit list", "Некорректный список юнитов");
        return false;
    }
    save.units.resize(count);
    std::array<bool, UnitSlots> usedUnitIds{};
    for (UnitState &item : save.units) {
        if (!expectTag(input, "UNIT") ||
            !readValue(input, item.oldId) || !readValue(input, item.type) ||
            !readValue(input, item.player) || !readValue(input, item.cell) ||
            !readValue(input, item.hitPoints) || !readValue(input, item.tempHitPoints) ||
            !readValue(input, item.posX) || !readValue(input, item.posY) ||
            !readValue(input, item.experience) || !readValue(input, item.groupMask) ||
            !readValue(input, item.nextCell) || !readValue(input, item.goalCell) ||
            !readArray(input, item.path) ||
            !readValue(input, item.pathIndex) || !readValue(input, item.pathFails) ||
            !readBool(input, item.calculatePath) || !readBool(input, item.carryMe) ||
            !readValue(input, item.carryAll) || !readValue(input, item.attackUnit) ||
            !readValue(input, item.attackStructure) || !readValue(input, item.attackCell) ||
            !readValue(input, item.unitId) || !readValue(input, item.structureId) ||
            !readValue(input, item.credits) || !readValue(input, item.transferType) ||
            !readValue(input, item.bringTarget) || !readValue(input, item.newUnitType) ||
            !readValue(input, item.lastDroppedOffCell) || !readValue(input, item.bodyFacing) ||
            !readValue(input, item.headFacing) || !readValue(input, item.bodyShouldFace) ||
            !readValue(input, item.headShouldFace) || !readValue(input, item.frame) ||
            !readBool(input, item.selected) || !readValue(input, item.action) ||
            !readValue(input, item.intent) || !readValue(input, item.willBePickedUpBy) ||
            !readBool(input, item.pickedUp) || !readBool(input, item.removeMe) ||
            !readValue(input, item.mission) || !readBool(input, item.reinforcement) ||
            !readValue(input, item.unitsEaten) ||
            !readValue(input, item.harvestCellMemory) || !readBool(input, item.stayAtGoalCell) ||
            !readArray(input, item.timers)) {
            error = localization::text("Unit data is corrupted", "Повреждены данные юнитов");
            return false;
        }
        if (item.oldId < 0 || item.oldId >= UnitSlots || usedUnitIds[item.oldId] ||
            item.type < 0 || item.type >= UnitTypeCount ||
            item.player < 0 || item.player >= MAX_PLAYERS ||
            item.cell < 0 || item.cell >= static_cast<int>(expectedCells) ||
            !std::isfinite(item.posX) || !std::isfinite(item.posY) ||
            !std::isfinite(item.experience) ||
            item.groupMask < 0 || item.groupMask >= (1 << MAX_UNIT_GROUPS)) {
            error = localization::text("Invalid reference in unit data", "Некорректная ссылка в данных юнита");
            return false;
        }
        usedUnitIds[item.oldId] = true;
    }

    if (!expectTag(input, "REINFORCEMENTS") || !readValue(input, count) || count > 1024) {
        error = localization::text("Invalid reinforcement list", "Некорректный список подкреплений");
        return false;
    }
    save.reinforcements.resize(count);
    for (ReinforcementState &item : save.reinforcements) {
        if (!expectTag(input, "REINFORCEMENT") ||
            !readValue(input, item.delay) || !readValue(input, item.unitType) ||
            !readValue(input, item.player) || !readValue(input, item.cell) ||
            !readBool(input, item.repeat) || !readBool(input, item.remove) ||
            !readValue(input, item.originalDelay)) {
            error = localization::text("Reinforcement data is corrupted", "Повреждены данные подкреплений");
            return false;
        }
        if (item.unitType < 0 || item.unitType >= UnitTypeCount ||
            item.player < 0 || item.player >= MAX_PLAYERS ||
            item.cell < 0 || item.cell >= static_cast<int>(expectedCells)) {
            error = localization::text("Invalid reinforcement data", "Некорректные данные подкрепления");
            return false;
        }
    }

    if (!expectTag(input, "BUILD_QUEUE") || !readValue(input, count) ||
        count > MAX_PLAYERS * MAX_ITEMS) {
        error = localization::text("Invalid construction queue", "Некорректная очередь строительства");
        return false;
    }
    save.buildQueue.resize(count);
    for (BuildQueueState &item : save.buildQueue) {
        if (!expectTag(input, "BUILD") ||
            !readValue(input, item.player) || !readValue(input, item.slot) ||
            !readValue(input, item.timer) || !readValue(input, item.listType) ||
            !readValue(input, item.buildType) || !readValue(input, item.buildId) ||
            !readValue(input, item.subList) || !readValue(input, item.progress) ||
            !readValue(input, item.buildFrame) || !readValue(input, item.timesToBuild) ||
            !readValue(input, item.timesOrdered) || !readValue(input, item.state) ||
            !readBool(input, item.placeIt) || !readBool(input, item.deployIt) ||
            !readBool(input, item.waitingForUnitSlot) ||
            !readValue(input, item.progressFrameTimer) ||
            !readValue(input, item.flashingTimer) || !readValue(input, item.timerCap)) {
            error = localization::text("Construction queue is corrupted", "Повреждена очередь строительства");
            return false;
        }
        if (item.player < 0 || item.player >= MAX_PLAYERS ||
            item.slot < 0 || item.slot >= MAX_ITEMS ||
            item.listType < 0 || item.listType > eListTypeAsInt(eListType::LIST_UPGRADES) ||
            item.buildType < STRUCTURE || item.buildType >= UNKNOWN ||
            item.state < AVAILABLE || item.state > UNAVAILABLE ||
            !std::isfinite(item.progressFrameTimer)) {
            error = localization::text("Invalid construction queue entry", "Некорректная запись очереди строительства");
            return false;
        }
    }
    if (!expectTag(input, "FACTORYPADS") || !readValue(input, count) || count > MAX_STRUCTURES) {
        error = localization::text("Invalid factory pad list", "Некорректный список площадок заводов");
        return false;
    }
    std::array<bool, MAX_STRUCTURES> padStructureSeen{};
    save.factoryPads.resize(count);
    for (FactoryPadSave &item : save.factoryPads) {
        if (!expectTag(input, "FACTORYPAD") ||
            !readValue(input, item.structureId) ||
            !factory_pad::read(input, item.pad, MaximumSaveBytes)) {
            error = localization::text("Factory pad data is corrupted", "Повреждены данные площадок заводов");
            return false;
        }
        bool isFactory = false;
        int factoryOwner = -1;
        for (const StructureState &structureItem : save.structures) {
            if (structureItem.oldId == item.structureId) {
                isFactory = structureItem.type == LIGHTFACTORY || structureItem.type == HEAVYFACTORY;
                if (isFactory) {
                    factoryOwner = structureItem.player;
                }
            }
        }
        bool referencesAreValid = item.structureId >= 0 && item.structureId < MAX_STRUCTURES &&
                                  isFactory && !padStructureSeen[item.structureId] &&
                                  item.pad.phase != factory_pad::Phase::Empty &&
                                  item.pad.unitType >= 0 && item.pad.unitType < UnitTypeCount &&
                                  item.pad.carryallId >= -1 && item.pad.carryallId < UnitSlots;
        if (referencesAreValid && item.pad.carryallId >= 0) {
            referencesAreValid = usedUnitIds[item.pad.carryallId];
            for (const UnitState &unitItem : save.units) {
                if (unitItem.oldId == item.pad.carryallId) {
                    referencesAreValid = referencesAreValid && unitItem.type == CARRYALL &&
                                         unitItem.player == factoryOwner;
                    break;
                }
            }
        }
        for (const int waitingType : item.pad.waiting) {
            referencesAreValid = referencesAreValid && waitingType >= 0 && waitingType < UnitTypeCount;
        }
        if (referencesAreValid && item.pad.phase == factory_pad::Phase::Rolling) {
            referencesAreValid = item.pad.rollUnitId >= 0 && item.pad.rollUnitId < UnitSlots && usedUnitIds[item.pad.rollUnitId];
            bool foundMatchingRoller = false;
            for (const UnitState &unitItem : save.units) {
                if (unitItem.oldId == item.pad.rollUnitId) {
                    foundMatchingRoller = unitItem.type == item.pad.unitType && unitItem.player == factoryOwner;
                    break;
                }
            }
            referencesAreValid = referencesAreValid && foundMatchingRoller;
        }
        if (!referencesAreValid) {
            error = localization::text("Invalid factory pad data", "Некорректные данные площадки завода");
            return false;
        }
        padStructureSeen[item.structureId] = true;
    }
    if (!expectTag(input, "END")) {
        error = localization::text("Save data is incomplete", "Данные сохранения неполны");
        return false;
    }
    return true;
}

}
