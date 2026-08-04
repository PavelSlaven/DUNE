#ifdef _WIN32
#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#endif

#include "save/SaveGameManager.hpp"

#include "building/cItemBuilder.h"
#include "cGame.h"
#include "data/gfxdata.h"
#include "d2tmc.h"
#include "gameobjects/structures/cStructureFactory.h"
#include "gameobjects/particles/cParticle.h"
#include "gameobjects/projectiles/bullet.h"
#include "gameobjects/units/cReinforcements.h"
#include "managers/cDrawManager.h"
#include "map/MapGeometry.hpp"
#include "map/cMapCamera.h"
#include "player/cHousesInfo.h"
#include "player/cPlayer.h"
#include "save/SaveFileCodec.hpp"
#include "save/SaveSlotName.hpp"
#include "sidebar/cBuildingList.h"
#include "sidebar/cSideBar.h"
#include "utils/Localization.hpp"
#include "utils/cLog.h"

#include <algorithm>
#include <array>
#include <cmath>
#include <cstdint>
#include <fstream>
#include <format>
#include <iomanip>
#include <limits>
#include <sstream>
#include <system_error>
#include <vector>

namespace save_game_detail {
constexpr std::size_t MaximumSaveBytes = 16U * 1024U * 1024U;

struct PlayerState {
    int house = GENERALHOUSE;
    int team = -1;
    int techLevel = 0;
    int focusCell = 0;
    int quota = 0;
    int selectedStructure = -1;
    float credits = 0.0F;
    float maxCredits = 1000.0F;
    int powerUsage = 0;
    int powerProduce = 0;
    bool alive = true;
    bool autoSlab = false;
    std::array<int, MAX_STRUCTURETYPES> primary{};
    std::array<int, MAX_STRUCTURETYPES> structures{};
    std::array<int, MAX_STRUCTURETYPES> upgrades{};
};

struct CellState {
    int credits = 0;
    int type = 0;
    int tile = 0;
    int smudgeTile = 0;
    int smudgeType = -1;
    int health = 0;
    bool passable = true;
    bool passableFoot = true;
    std::uint32_t visibilityMask = 0;
};

struct StructureState {
    int oldId = -1;
    int type = -1;
    int player = -1;
    int cell = -1;
    int hitPoints = 0;
    int rallyPoint = -1;
    int frame = 0;
    int buildPhase = 0;
    int unitWithin = -1;
    int unitEntering = -1;
    int unitHeading = -1;
    float concrete = 0.0F;
    bool animate = false;
    bool repair = false;
    bool animateOnApproach = false;
    int smoke = 0;
    int repairTimer = 0;
    int flagTimer = 0;
    int reduceSmokeTimer = 0;
    int decayTimer = 0;
    int prebuildTimer = 0;
};

struct UnitState {
    int oldId = -1;
    int type = -1;
    int player = -1;
    int cell = -1;
    int hitPoints = 0;
    int tempHitPoints = 0;
    float posX = 0.0F;
    float posY = 0.0F;
    float experience = 0.0F;
    int group = 0;
    int nextCell = -1;
    int goalCell = -1;
    std::array<int, MAX_PATH_SIZE> path{};
    int pathIndex = 0;
    int pathFails = 0;
    bool calculatePath = false;
    bool carryMe = false;
    int carryAll = -1;
    int attackUnit = -1;
    int attackStructure = -1;
    int attackCell = -1;
    int unitId = -1;
    int structureId = -1;
    int credits = 0;
    int transferType = 0;
    int bringTarget = -1;
    int newUnitType = -1;
    int lastDroppedOffCell = -1;
    int bodyFacing = 0;
    int headFacing = 0;
    int bodyShouldFace = 0;
    int headShouldFace = 0;
    int frame = 0;
    bool selected = false;
    int action = 0;
    int intent = 0;
    int willBePickedUpBy = -1;
    bool pickedUp = false;
    bool removeMe = false;
    int mission = -1;
    bool reinforcement = false;
    int unitsEaten = 0;
    float turnTimer = 0.0F;
    std::array<int, 11> timers{};
};

struct ReinforcementState {
    int delay = -1;
    int unitType = -1;
    int player = -1;
    int cell = -1;
    bool repeat = false;
    bool remove = false;
    int originalDelay = -1;
};

struct BuildQueueState {
    int player = -1;
    int slot = -1;
    int timer = 0;
    int listType = 0;
    int buildType = 0;
    int buildId = -1;
    int subList = 0;
    int progress = 0;
    int buildFrame = 0;
    int timesToBuild = 0;
    int timesOrdered = 0;
    bool building = false;
    int state = 0;
    bool placeIt = false;
    bool deployIt = false;
    float progressFrameTimer = 0.0F;
    int flashingTimer = 0;
    int timerCap = cBuildingListItem::DefaultTimerCap;
};

struct SaveSnapshot {
    std::string saveName;
    bool skirmish = false;
    int region = 1;
    int mission = 0;
    int winFlags = 0;
    int loseFlags = 0;
    int cameraCell = 0;
    int mapWidth = 64;
    int mapHeight = 64;
    bool autoSpawnBlooms = false;
    bool autoDetonateBlooms = false;
    int bloomTimer = 0;
    int desiredWorms = 0;
    int wormRespawnTimer = 0;
    std::array<PlayerState, MAX_PLAYERS> players{};
    std::vector<CellState> cells;
    std::vector<StructureState> structures;
    std::vector<UnitState> units;
    std::vector<ReinforcementState> reinforcements;
    std::vector<BuildQueueState> buildQueue;
};

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
               << cell.visibilityMask << '\n';
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
               << item.group << ' ' << item.nextCell << ' ' << item.goalCell;
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
               << item.turnTimer;
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
               << item.building << ' ' << item.state << ' ' << item.placeIt << ' '
               << item.deployIt << ' ' << item.progressFrameTimer << ' '
               << item.flashingTimer << ' ' << item.timerCap << '\n';
    }
    output << "END\n";
    return output.str();
}

bool deserializeBody(
    std::string_view body,
    SaveSnapshot &save,
    std::string &error)
{
    std::istringstream input{std::string(body)};
    std::string firstTag;
    if (!readValue(input, firstTag)) {
        error = localization::text("Save header is corrupted", "Повреждён заголовок сохранения");
        return false;
    }
    if (firstTag == "INFO") {
        if (!(input >> std::quoted(save.saveName)) ||
            !expectTag(input, "META")) {
            error = localization::text("Save name is corrupted", "Повреждено название сохранения");
            return false;
        }
    }
    else if (firstTag != "META") {
        error = localization::text("Save header is corrupted", "Повреждён заголовок сохранения");
        return false;
    }
    if (
        !readBool(input, save.skirmish) ||
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
    if (save.mapWidth < 4 || save.mapHeight < 4 ||
        save.mapWidth > 256 || save.mapHeight > 256) {
        error = localization::text("Invalid map size in save", "Некорректный размер карты в сохранении");
        return false;
    }

    std::size_t count = 0;
    if (!expectTag(input, "PLAYERS") ||
        !readValue(input, count) ||
        count != MAX_PLAYERS) {
        error = localization::text("Invalid player list", "Некорректный список игроков");
        return false;
    }
    for (std::size_t index = 0; index < count; ++index) {
        std::size_t storedIndex = 0;
        PlayerState &player = save.players[index];
        if (!expectTag(input, "PLAYER") ||
            !readValue(input, storedIndex) ||
            storedIndex != index ||
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
            !readArray(input, player.upgrades)) {
            error = localization::text("Player data is corrupted", "Повреждены данные игроков");
            return false;
        }
        if (player.house < 0 || player.house >= MAX_HOUSES ||
            !std::isfinite(player.credits) ||
            !std::isfinite(player.maxCredits)) {
            error = localization::text("Invalid player settings", "Некорректные параметры игрока");
            return false;
        }
    }

    const std::size_t expectedCells =
        static_cast<std::size_t>(save.mapWidth) *
        static_cast<std::size_t>(save.mapHeight);
    if (!expectTag(input, "CELLS") ||
        !readValue(input, count) ||
        count != expectedCells) {
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
            !readValue(input, cell.visibilityMask)) {
            error = localization::text("Map cells are corrupted", "Повреждены клетки карты");
            return false;
        }
        if (cell.type < TERRAIN_BLOOM || cell.type > TERRAIN_WALL ||
            cell.smudgeType < -1 ||
            cell.smudgeType >= static_cast<int>(SmudgeType::MAX)) {
            error = localization::text("Invalid terrain type", "Некорректный тип поверхности");
            return false;
        }
    }

    if (!expectTag(input, "STRUCTURES") ||
        !readValue(input, count) ||
        count > MAX_STRUCTURES) {
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
        if (item.oldId < 0 || item.oldId >= MAX_STRUCTURES ||
            usedStructureIds[item.oldId] ||
            item.type < 0 || item.type >= MAX_STRUCTURETYPES ||
            item.player < 0 || item.player >= MAX_PLAYERS ||
            item.cell < 0 || item.cell >= static_cast<int>(expectedCells) ||
            !std::isfinite(item.concrete)) {
            error = localization::text("Invalid reference in structure data", "Некорректная ссылка в данных здания");
            return false;
        }
        usedStructureIds[item.oldId] = true;
    }

    if (!expectTag(input, "UNITS") ||
        !readValue(input, count) ||
        count > MAX_UNITS) {
        error = localization::text("Invalid unit list", "Некорректный список юнитов");
        return false;
    }
    save.units.resize(count);
    std::array<bool, MAX_UNITS> usedUnitIds{};
    for (UnitState &item : save.units) {
        if (!expectTag(input, "UNIT") ||
            !readValue(input, item.oldId) || !readValue(input, item.type) ||
            !readValue(input, item.player) || !readValue(input, item.cell) ||
            !readValue(input, item.hitPoints) || !readValue(input, item.tempHitPoints) ||
            !readValue(input, item.posX) || !readValue(input, item.posY) ||
            !readValue(input, item.experience) || !readValue(input, item.group) ||
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
            !readValue(input, item.turnTimer) ||
            !readArray(input, item.timers)) {
            error = localization::text("Unit data is corrupted", "Повреждены данные юнитов");
            return false;
        }
        if (item.oldId < 0 || item.oldId >= MAX_UNITS ||
            usedUnitIds[item.oldId] ||
            item.type < 0 || item.type >= MAX_UNITTYPES ||
            item.player < 0 || item.player >= MAX_PLAYERS ||
            item.cell < 0 || item.cell >= static_cast<int>(expectedCells) ||
            !std::isfinite(item.posX) || !std::isfinite(item.posY) ||
            !std::isfinite(item.experience) ||
            !std::isfinite(item.turnTimer)) {
            error = localization::text("Invalid reference in unit data", "Некорректная ссылка в данных юнита");
            return false;
        }
        usedUnitIds[item.oldId] = true;
    }

    if (!expectTag(input, "REINFORCEMENTS") ||
        !readValue(input, count) ||
        count > 1024) {
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
        if (item.unitType < 0 || item.unitType >= MAX_UNITTYPES ||
            item.player < 0 || item.player >= MAX_PLAYERS ||
            item.cell < 0 || item.cell >= static_cast<int>(expectedCells)) {
            error = localization::text("Invalid reinforcement data", "Некорректные данные подкрепления");
            return false;
        }
    }

    if (!expectTag(input, "BUILD_QUEUE") ||
        !readValue(input, count) ||
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
            !readValue(input, item.timesOrdered) || !readBool(input, item.building) ||
            !readValue(input, item.state) || !readBool(input, item.placeIt) ||
            !readBool(input, item.deployIt) || !readValue(input, item.progressFrameTimer) ||
            !readValue(input, item.flashingTimer) || !readValue(input, item.timerCap)) {
            error = localization::text("Construction queue is corrupted", "Повреждена очередь строительства");
            return false;
        }
        if (item.player < 0 || item.player >= MAX_PLAYERS ||
            item.slot < 0 || item.slot >= MAX_ITEMS ||
            item.listType < 0 || item.listType >= cSideBar::LIST_MAX ||
            item.buildType < STRUCTURE || item.buildType >= UNKNOWN ||
            item.state < AVAILABLE || item.state > UNAVAILABLE ||
            !std::isfinite(item.progressFrameTimer)) {
            error = localization::text("Invalid construction queue entry", "Некорректная запись очереди строительства");
            return false;
        }
    }
    if (!expectTag(input, "END")) {
        error = localization::text("Save data is incomplete", "Сохранение не завершено");
        return false;
    }
    return true;
}

}

using namespace save_game_detail;

save_game_detail::SaveSnapshot SaveGameManager::captureSnapshot(cGame &game)
{
    SaveSnapshot save;
    save.skirmish = game.m_skirmish;
    save.region = game.m_region;
    save.mission = game.m_mission;
    save.winFlags = game.m_winFlags;
    save.loseFlags = game.m_loseFlags;
    save.mapWidth = global_map.getWidth();
    save.mapHeight = global_map.getHeight();
    save.autoSpawnBlooms = global_map.m_bAutoSpawnSpiceBlooms;
    save.autoDetonateBlooms = global_map.m_bAutoDetonateSpiceBlooms;
    save.bloomTimer = global_map.m_iTIMER_blooms;
    save.desiredWorms = global_map.m_iDesiredAmountOfWorms;
    save.wormRespawnTimer = global_map.m_iTIMER_respawnSandworms;

    const int cameraX =
        mapCamera->getViewportStartX() +
        mapCamera->getViewportWidth() / 2;
    const int cameraY =
        mapCamera->getViewportStartY() +
        mapCamera->getViewportHeight() / 2;
    save.cameraCell = global_map.getGeometry().makeCell(
        std::clamp(cameraX / TILESIZE_WIDTH_PIXELS, 0, save.mapWidth - 1),
        std::clamp(cameraY / TILESIZE_HEIGHT_PIXELS, 0, save.mapHeight - 1)
    );

    for (int index = 0; index < MAX_PLAYERS; ++index) {
        const cPlayer &source = players[index];
        PlayerState &target = save.players[index];
        target.house = source.house;
        target.team = source.iTeam;
        target.techLevel = source.techLevel;
        target.focusCell = source.focusCell_;
        target.quota = source.spiceQuota;
        target.selectedStructure = source.selected_structure;
        target.credits = source.credits;
        target.maxCredits = source.maxCredits_;
        target.powerUsage = source.powerUsage_;
        target.powerProduce = source.powerProduce_;
        target.alive = source.alive;
        target.autoSlab = source.m_autoSlabStructures;
        std::copy_n(source.iPrimaryBuilding, MAX_STRUCTURETYPES, target.primary.begin());
        std::copy_n(source.iStructures, MAX_STRUCTURETYPES, target.structures.begin());
        std::copy_n(source.iStructureUpgradeLevel, MAX_STRUCTURETYPES, target.upgrades.begin());
    }

    save.cells.reserve(global_map.getMaxCells());
    for (int index = 0; index < global_map.getMaxCells(); ++index) {
        const tCell *source = global_map.getCell(index);
        CellState target;
        target.credits = source->credits;
        target.type = source->type;
        target.tile = source->tile;
        target.smudgeTile = source->smudgetile;
        target.smudgeType = source->smudgetype
            ? static_cast<int>(*source->smudgetype)
            : -1;
        target.health = source->health;
        target.passable = source->passable;
        target.passableFoot = source->passableFoot;
        for (int player = 0; player < MAX_PLAYERS; ++player) {
            if (source->iVisible[player]) {
                target.visibilityMask |= (1U << player);
            }
        }
        save.cells.push_back(target);
    }

    for (int index = 0; index < MAX_STRUCTURES; ++index) {
        cAbstractStructure *source = structure[index];
        if (!source || !source->isValid()) {
            continue;
        }
        StructureState target;
        target.oldId = index;
        target.type = source->getType();
        target.player = source->iPlayer;
        target.cell = source->iCell;
        target.hitPoints = source->iHitPoints;
        target.rallyPoint = source->iRallyPoint;
        target.frame = source->iFrame;
        target.buildPhase = source->iBuildFase;
        target.unitWithin = source->iUnitIDWithinStructure;
        target.unitEntering = source->iUnitIDEnteringStructure;
        target.unitHeading = source->iUnitIDHeadingForStructure;
        target.concrete = source->fConcrete;
        target.animate = source->bAnimate;
        target.repair = source->bRepair;
        target.animateOnApproach =
            source->shouldAnimateWhenUnitHeadsTowardsStructure;
        target.smoke = source->m_smokeParticlesCreated;
        target.repairTimer = source->TIMER_repair;
        target.flagTimer = source->TIMER_flag;
        target.reduceSmokeTimer = source->TIMER_reduceSmoke;
        target.decayTimer = source->TIMER_decay;
        target.prebuildTimer = source->TIMER_prebuild;
        save.structures.push_back(target);
    }

    for (int index = 0; index < MAX_UNITS; ++index) {
        const cUnit &source = unit[index];
        if (!source.isValid()) {
            continue;
        }
        UnitState target;
        target.oldId = index;
        target.type = source.iType;
        target.player = source.iPlayer;
        target.cell = source.iCell;
        target.hitPoints = source.iHitPoints;
        target.tempHitPoints = source.iTempHitPoints;
        target.posX = source.posX;
        target.posY = source.posY;
        target.experience = source.fExperience;
        target.group = source.iGroup;
        target.nextCell = source.iNextCell;
        target.goalCell = source.iGoalCell;
        std::copy_n(source.iPath, MAX_PATH_SIZE, target.path.begin());
        target.pathIndex = source.iPathIndex;
        target.pathFails = source.iPathFails;
        target.calculatePath = source.bCalculateNewPath;
        target.carryMe = source.bCarryMe;
        target.carryAll = source.iCarryAll;
        target.attackUnit = source.iAttackUnit;
        target.attackStructure = source.iAttackStructure;
        target.attackCell = source.iAttackCell;
        target.unitId = source.iUnitID;
        target.structureId = source.iStructureID;
        target.credits = source.iCredits;
        target.transferType = static_cast<int>(source.m_transferType);
        target.bringTarget = source.iBringTarget;
        target.newUnitType = source.iNewUnitType;
        target.lastDroppedOffCell = source.lastDroppedOffCell;
        target.bodyFacing = source.iBodyFacing;
        target.headFacing = source.iHeadFacing;
        target.bodyShouldFace = source.iBodyShouldFace;
        target.headShouldFace = source.iHeadShouldFace;
        target.frame = source.iFrame;
        target.selected = source.bSelected;
        target.action = static_cast<int>(source.m_action);
        target.intent = static_cast<int>(source.intent);
        target.willBePickedUpBy = source.willBePickedUpBy;
        target.pickedUp = source.bPickedUp;
        target.removeMe = source.bRemoveMe;
        target.mission = source.mission;
        target.reinforcement = source.isReinforcement;
        target.unitsEaten = source.unitsEaten;
        target.turnTimer = source.TIMER_turn;
        target.timers = {
            source.TIMER_blink,
            source.TIMER_move,
            source.TIMER_movewait,
            source.TIMER_movedelay,
            source.TIMER_thinkwait,
            source.TIMER_frame,
            source.TIMER_harvest,
            source.TIMER_guard,
            source.TIMER_bored,
            source.TIMER_attack,
            source.TIMER_wormtrail
        };
        save.units.push_back(target);
    }

    if (game.m_reinforcements) {
        for (const cReinforcement &source :
             game.m_reinforcements->reinforcements) {
            save.reinforcements.push_back({
                source.m_delayInSeconds,
                source.m_unitType,
                source.m_playerId,
                source.m_cell,
                source.m_repeat,
                source.m_removeMe,
                source.m_originalDelay
            });
        }
    }

    for (int playerIndex = 0; playerIndex < MAX_PLAYERS; ++playerIndex) {
        const cItemBuilder *builder = players[playerIndex].itemBuilder;
        if (!builder) {
            continue;
        }
        for (int slot = 0; slot < MAX_ITEMS; ++slot) {
            cBuildingListItem *item = builder->m_items[slot];
            if (!item || !item->myList) {
                continue;
            }
            BuildQueueState target;
            target.player = playerIndex;
            target.slot = slot;
            target.timer = builder->m_timers[slot];
            target.listType = eListTypeAsInt(item->getListType());
            target.buildType = static_cast<int>(item->type);
            target.buildId = item->buildId;
            target.subList = item->subList;
            target.progress = item->progress;
            target.buildFrame = item->buildFrameToDraw;
            target.timesToBuild = item->timesToBuild;
            target.timesOrdered = item->timesOrdered;
            target.building = item->building;
            target.state = static_cast<int>(item->state);
            target.placeIt = item->placeIt;
            target.deployIt = item->deployIt;
            target.progressFrameTimer = item->TIMER_progressFrame;
            target.flashingTimer = item->TIMER_flashing;
            target.timerCap = item->timerCap;
            save.buildQueue.push_back(target);
        }
    }
    return save;
}

void restoreCellState(const SaveSnapshot &save)
{
    for (int index = 0; index < global_map.getMaxCells(); ++index) {
        tCell *target = global_map.getCell(index);
        const CellState &source = save.cells[static_cast<std::size_t>(index)];
        target->credits = source.credits;
        target->type = source.type;
        target->tile = source.tile;
        target->smudgetile = source.smudgeTile;
        target->smudgetype = source.smudgeType >= 0
            ? std::optional<SmudgeType>(
                static_cast<SmudgeType>(source.smudgeType))
            : std::nullopt;
        target->health = source.health;
        target->passable = source.passable;
        target->passableFoot = source.passableFoot;
        for (int player = 0; player < MAX_PLAYERS; ++player) {
            target->iVisible[player] =
                (source.visibilityMask & (1U << player)) != 0;
        }
    }
}

int translateStructureId(
    int oldId,
    const std::array<int, MAX_STRUCTURES> &mapping)
{
    if (oldId < 0 || oldId >= MAX_STRUCTURES) {
        return -1;
    }
    return mapping[oldId];
}

cBuildingListItem *findBuildItem(const BuildQueueState &saved)
{
    if (saved.player < 0 || saved.player >= MAX_PLAYERS ||
        saved.listType < 0 || saved.listType >= cSideBar::LIST_MAX) {
        return nullptr;
    }
    cSideBar *sidebar = players[saved.player].getSideBar();
    cBuildingList *list = sidebar ? sidebar->getList(saved.listType) : nullptr;
    if (!list) {
        return nullptr;
    }
    for (int index = 0; index < list->getItemCount(); ++index) {
        cBuildingListItem *item = list->getItem(index);
        if (item &&
            static_cast<int>(item->getBuildType()) == saved.buildType &&
            item->getBuildId() == saved.buildId &&
            item->getSubList() == saved.subList) {
            return item;
        }
    }
    return nullptr;
}

bool SaveGameManager::restoreSnapshot(
    cGame &game,
    const save_game_detail::SaveSnapshot &save,
    std::string &error)
{
    game.m_skirmish = save.skirmish;
    game.m_region = save.region;
    game.m_mission = save.mission;
    for (int index = 0; index < MAX_PLAYERS; ++index) {
        players[index].setHouse(save.players[index].house);
    }

    game.missionInit();
    game.setupPlayers();
    global_map.init(save.mapWidth, save.mapHeight);
    restoreCellState(save);
    for (int cell = 0; cell < global_map.getMaxCells(); ++cell) {
        for (int layer = 0; layer < MAPID_MAX; ++layer) {
            global_map.cellResetIdFromLayer(cell, layer);
        }
    }

    for (int index = 0; index < MAX_PLAYERS; ++index) {
        cPlayer &target = players[index];
        const PlayerState &source = save.players[index];
        target.setHouse(source.house);
        target.iTeam = source.team;
        target.techLevel = source.techLevel;
        target.focusCell_ = source.focusCell;
        target.spiceQuota = source.quota;
        target.selected_structure = -1;
        target.credits = source.credits;
        target.maxCredits_ = source.maxCredits;
        target.powerUsage_ = source.powerUsage;
        target.powerProduce_ = source.powerProduce;
        target.alive = source.alive;
        target.m_autoSlabStructures = source.autoSlab;
        std::copy(source.upgrades.begin(), source.upgrades.end(),
                  target.iStructureUpgradeLevel);
    }

    std::array<int, MAX_STRUCTURES> structureMapping{};
    structureMapping.fill(-1);
    for (const StructureState &source : save.structures) {
        if (source.oldId < 0 || source.oldId >= MAX_STRUCTURES ||
            source.player < 0 || source.player >= MAX_PLAYERS ||
            source.cell < 0 || source.cell >= global_map.getMaxCells()) {
            error = localization::text("Invalid structure in save", "Некорректное здание в сохранении");
            return false;
        }
        const int maximumHp = std::max(
            1,
            sStructureInfo[source.type].hp
        );
        const int hpPercent = std::clamp(
            source.hitPoints * 100 / maximumHp,
            1,
            100
        );
        cAbstractStructure *target =
            players[source.player].placeStructure(
                source.cell,
                source.type,
                hpPercent
            );
        if (!target) {
            error = localization::format(
                "Could not restore structure type {} at cell {}",
                "Не удалось восстановить здание типа {} в клетке {}",
                source.type,
                source.cell
            );
            return false;
        }
        structureMapping[source.oldId] = target->getStructureId();
        target->setHitPoints(source.hitPoints);
        target->setRallyPoint(source.rallyPoint);
        target->setFrame(source.frame);
        target->setBuildingFase(source.buildPhase);
        target->fConcrete = source.concrete;
        target->setAnimating(source.animate);
        target->setRepairing(source.repair);
        target->shouldAnimateWhenUnitHeadsTowardsStructure =
            source.animateOnApproach;
        target->m_smokeParticlesCreated = source.smoke;
        target->TIMER_repair = source.repairTimer;
        target->TIMER_flag = source.flagTimer;
        target->TIMER_reduceSmoke = source.reduceSmokeTimer;
        target->TIMER_decay = source.decayTimer;
        target->TIMER_prebuild = source.prebuildTimer;
    }

    for (const UnitState &source : save.units) {
        cUnit &target = unit[source.oldId];
        target.init(source.oldId);
        target.iType = source.type;
        target.iPlayer = source.player;
        target.iCell = source.cell;
        target.iCellX = global_map.getCellX(source.cell);
        target.iCellY = global_map.getCellY(source.cell);
        target.iHitPoints = source.hitPoints;
        target.iTempHitPoints = source.tempHitPoints;
        target.posX = source.posX;
        target.posY = source.posY;
        target.fExperience = source.experience;
        target.iGroup = source.group;
        target.iNextCell = source.nextCell;
        target.iGoalCell = source.goalCell;
        std::copy(source.path.begin(), source.path.end(), target.iPath);
        target.iPathIndex = source.pathIndex;
        target.iPathFails = source.pathFails;
        target.bCalculateNewPath = source.calculatePath;
        target.bCarryMe = source.carryMe;
        target.iCarryAll = source.carryAll;
        target.iAttackUnit = source.attackUnit;
        target.iAttackStructure =
            translateStructureId(source.attackStructure, structureMapping);
        target.iAttackCell = source.attackCell;
        target.iUnitID = source.unitId;
        target.iStructureID =
            translateStructureId(source.structureId, structureMapping);
        target.iCredits = source.credits;
        target.m_transferType =
            static_cast<eTransferType>(source.transferType);
        target.iBringTarget = source.bringTarget;
        target.iNewUnitType = source.newUnitType;
        target.lastDroppedOffCell = source.lastDroppedOffCell;
        target.iBodyFacing = source.bodyFacing;
        target.iHeadFacing = source.headFacing;
        target.iBodyShouldFace = source.bodyShouldFace;
        target.iHeadShouldFace = source.headShouldFace;
        target.iFrame = source.frame;
        target.bSelected = source.selected && source.player == HUMAN;
        target.bHovered = false;
        target.m_action = static_cast<eActionType>(source.action);
        target.intent = static_cast<eUnitActionIntent>(source.intent);
        target.willBePickedUpBy = source.willBePickedUpBy;
        target.bPickedUp = source.pickedUp;
        target.bRemoveMe = source.removeMe;
        target.mission = source.mission;
        target.isReinforcement = source.reinforcement;
        target.unitsEaten = source.unitsEaten;
        target.boundParticleId = -1;
        target.TIMER_blink = source.timers[0];
        target.TIMER_move = source.timers[1];
        target.TIMER_movewait = source.timers[2];
        target.TIMER_movedelay = source.timers[3];
        target.TIMER_thinkwait = source.timers[4];
        target.TIMER_turn = source.turnTimer;
        target.TIMER_frame = source.timers[5];
        target.TIMER_harvest = source.timers[6];
        target.TIMER_guard = source.timers[7];
        target.TIMER_bored = source.timers[8];
        target.TIMER_attack = source.timers[9];
        target.TIMER_wormtrail = source.timers[10];
        target.recreateDimensions();

        if (!target.isHidden()) {
            int layer = MAPID_UNITS;
            if (target.isAirbornUnit()) {
                layer = MAPID_AIR;
            }
            else if (target.isSandworm()) {
                layer = MAPID_WORMS;
            }
            global_map.cellSetIdForLayer(source.cell, layer, source.oldId);
        }
    }

    for (const StructureState &source : save.structures) {
        const int newId = structureMapping[source.oldId];
        cAbstractStructure *target =
            newId >= 0 ? structure[newId] : nullptr;
        if (!target) {
            continue;
        }
        target->setUnitIdWithin(source.unitWithin);
        target->setUnitIdEntering(source.unitEntering);
        target->setUnitIdHeadingTowards(source.unitHeading);
    }

    restoreCellState(save);
    for (const StructureState &source : save.structures) {
        const int newId = structureMapping[source.oldId];
        cAbstractStructure *target =
            newId >= 0 ? structure[newId] : nullptr;
        if (!target) {
            continue;
        }
        for (const int cell : target->getCellsOfStructure()) {
            global_map.cellSetIdForLayer(cell, MAPID_STRUCTURES, newId);
        }
    }
    for (const UnitState &source : save.units) {
        cUnit &target = unit[source.oldId];
        if (target.isHidden()) {
            continue;
        }
        int layer = target.isAirbornUnit()
            ? MAPID_AIR
            : (target.isSandworm() ? MAPID_WORMS : MAPID_UNITS);
        global_map.cellSetIdForLayer(source.cell, layer, source.oldId);
    }

    for (int index = 0; index < MAX_PLAYERS; ++index) {
        cPlayer &target = players[index];
        const PlayerState &source = save.players[index];
        std::copy(source.structures.begin(), source.structures.end(),
                  target.iStructures);
        for (int type = 0; type < MAX_STRUCTURETYPES; ++type) {
            target.iPrimaryBuilding[type] =
                translateStructureId(source.primary[type], structureMapping);
        }
        target.selected_structure =
            translateStructureId(source.selectedStructure, structureMapping);
    }

    if (game.m_reinforcements) {
        game.m_reinforcements->reinforcements.clear();
        for (const ReinforcementState &source : save.reinforcements) {
            cReinforcement item;
            item.m_delayInSeconds = source.delay;
            item.m_unitType = source.unitType;
            item.m_playerId = source.player;
            item.m_cell = source.cell;
            item.m_repeat = source.repeat;
            item.m_removeMe = source.remove;
            item.m_originalDelay = source.originalDelay;
            game.m_reinforcements->reinforcements.push_back(item);
        }
    }

    for (int index = 0; index < MAX_PLAYERS; ++index) {
        cItemBuilder *builder = players[index].itemBuilder;
        if (!builder) {
            continue;
        }
        std::fill_n(builder->m_items, MAX_ITEMS, nullptr);
        std::fill_n(builder->m_timers, MAX_ITEMS, 0);
    }
    for (const BuildQueueState &source : save.buildQueue) {
        if (source.player < 0 || source.player >= MAX_PLAYERS ||
            source.slot < 0 || source.slot >= MAX_ITEMS) {
            continue;
        }
        cItemBuilder *builder = players[source.player].itemBuilder;
        cBuildingListItem *item = findBuildItem(source);
        if (!builder || !item) {
            continue;
        }
        item->progress = source.progress;
        item->buildFrameToDraw = source.buildFrame;
        item->timesToBuild = source.timesToBuild;
        item->timesOrdered = source.timesOrdered;
        item->building = source.building;
        item->state =
            static_cast<eBuildingListItemState>(source.state);
        item->placeIt = source.placeIt;
        item->deployIt = source.deployIt;
        item->TIMER_progressFrame = source.progressFrameTimer;
        item->TIMER_flashing = source.flashingTimer;
        item->timerCap = source.timerCap;
        builder->m_items[source.slot] = item;
        builder->m_timers[source.slot] = source.timer;
    }

    global_map.m_bAutoSpawnSpiceBlooms = save.autoSpawnBlooms;
    global_map.m_bAutoDetonateSpiceBlooms = save.autoDetonateBlooms;
    global_map.m_iTIMER_blooms = save.bloomTimer;
    global_map.m_iDesiredAmountOfWorms = save.desiredWorms;
    global_map.m_iTIMER_respawnSandworms = save.wormRespawnTimer;
    game.m_winFlags = static_cast<std::int8_t>(save.winFlags);
    game.m_loseFlags = static_cast<std::int8_t>(save.loseFlags);
    game.m_TIMER_evaluatePlayerStatus = 5;

    for (cParticle &item : particle) {
        item.init();
    }
    for (cBullet &item : bullet) {
        item.bAlive = false;
    }
    drawManager->setPlayerToDraw(&players[HUMAN]);
    game.setPlayerToInteractFor(&players[HUMAN]);
    mapCamera->centerAndJumpViewPortToCell(
        std::clamp(save.cameraCell, 0, global_map.getMaxCells() - 1)
    );
    game.setNextStateToTransitionTo(GAME_PLAYING);
    return true;
}

bool writeAtomically(
    const std::filesystem::path &destination,
    std::string_view contents,
    std::string &error)
{
    std::error_code directoryError;
    std::filesystem::create_directories(
        destination.parent_path(),
        directoryError
    );
    if (directoryError) {
        error = localization::text("Could not create the saves folder", "Не удалось создать папку saves");
        return false;
    }
    const std::filesystem::path temporary =
        destination.string() + ".tmp";
    {
        std::ofstream output(
            temporary,
            std::ios::binary | std::ios::trunc
        );
        if (!output) {
            error = localization::text("Could not create temporary save file", "Не удалось создать временный файл сохранения");
            return false;
        }
        output.write(
            contents.data(),
            static_cast<std::streamsize>(contents.size())
        );
        output.flush();
        if (!output) {
            error = localization::text("Error writing save file", "Ошибка записи сохранения");
            output.close();
            std::filesystem::remove(temporary, directoryError);
            return false;
        }
    }
#ifdef _WIN32
    if (!MoveFileExW(
            temporary.wstring().c_str(),
            destination.wstring().c_str(),
            MOVEFILE_REPLACE_EXISTING | MOVEFILE_WRITE_THROUGH)) {
        error = localization::format(
            "Could not replace save file (Windows error {})",
            "Не удалось заменить сохранение (ошибка Windows {})",
            GetLastError()
        );
        std::filesystem::remove(temporary, directoryError);
        return false;
    }
#else
    std::filesystem::rename(temporary, destination, directoryError);
    if (directoryError) {
        error = directoryError.message();
        std::filesystem::remove(temporary, directoryError);
        return false;
    }
#endif
    return true;
}
std::filesystem::path SaveGameManager::quickSavePath()
{
    return slotPath(1);
}

bool SaveGameManager::hasQuickSave()
{
    std::error_code error;
    return std::filesystem::is_regular_file(quickSavePath(), error);
}

std::filesystem::path SaveGameManager::slotPath(int slot)
{
    if (!save_slot::isValidSlot(slot)) {
        return {};
    }
    if (slot == 1) {
        return std::filesystem::path("saves") / "quicksave.d2s";
    }
    return std::filesystem::path("saves") /
           std::format("save{:02}.d2s", slot);
}

SaveSlotInfo SaveGameManager::slotInfo(int slot)
{
    SaveSlotInfo info;
    info.slot = slot;
    if (!save_slot::isValidSlot(slot)) {
        return info;
    }

    const std::filesystem::path path = slotPath(slot);
    std::error_code fileError;
    info.exists = std::filesystem::is_regular_file(path, fileError);
    if (!info.exists || fileError) {
        return info;
    }

    std::ifstream input(path, std::ios::binary);
    if (!input) {
        return info;
    }
    const std::string contents{
        std::istreambuf_iterator<char>(input),
        std::istreambuf_iterator<char>()
    };
    const save_file::DecodeResult decoded = save_file::decode(
        contents,
        FormatVersion,
        MaximumSaveBytes
    );
    if (!decoded.succeeded()) {
        return info;
    }

    SaveSnapshot save;
    std::string parseError;
    if (!deserializeBody(decoded.body, save, parseError)) {
        return info;
    }
    info.valid = true;
    info.name = save_slot::sanitizeName(save.saveName);
    if (info.name.empty()) {
        info.name = slot == 1
            ? localization::text("Quick Save", "Быстрое сохранение")
            : save_slot::defaultName(slot);
    }
    return info;
}

std::vector<SaveSlotInfo> SaveGameManager::listSlots()
{
    std::vector<SaveSlotInfo> result;
    result.reserve(MaximumSlots);
    for (int slot = 1; slot <= MaximumSlots; ++slot) {
        result.push_back(slotInfo(slot));
    }
    return result;
}

bool SaveGameManager::hasAnySave()
{
    for (int slot = 1; slot <= MaximumSlots; ++slot) {
        const SaveSlotInfo info = slotInfo(slot);
        if (info.exists && info.valid) {
            return true;
        }
    }
    return false;
}

bool SaveGameManager::saveQuickGame(
    cGame &game,
    std::string &errorMessage)
{
    SaveSlotInfo info = slotInfo(1);
    const std::string name = info.valid
        ? info.name
        : localization::text("Quick Save", "Быстрое сохранение");
    return saveGame(game, 1, name, errorMessage);
}

bool SaveGameManager::saveGame(
    cGame &game,
    int slot,
    const std::string &name,
    std::string &errorMessage)
{
    errorMessage.clear();
    if (!save_slot::isValidSlot(slot)) {
        errorMessage = localization::text("Invalid save slot number", "Некорректный номер слота");
        return false;
    }
    if (!game.isState(GAME_PLAYING) &&
        !game.isState(GAME_OPTIONS) &&
        game.m_nextState != GAME_PLAYING) {
        errorMessage = localization::text("Saving is only available during a mission", "Сохранять можно только во время миссии");
        return false;
    }
    SaveSnapshot save = captureSnapshot(game);
    save.saveName = save_slot::sanitizeName(name);
    if (save.saveName.empty()) {
        save.saveName = save_slot::defaultName(slot);
    }
    const std::string body = serializeBody(save);
    const std::string contents = save_file::encode(body, FormatVersion);
    const std::filesystem::path path = slotPath(slot);
    if (!writeAtomically(path, contents, errorMessage)) {
        return false;
    }
    cLogger::getInstance()->log(
        LOG_INFO,
        COMP_GAMERULES,
        "Save game",
        path.string()
    );
    return true;
}

bool SaveGameManager::loadQuickGame(
    cGame &game,
    std::string &errorMessage)
{
    return loadGame(game, 1, errorMessage);
}

bool SaveGameManager::loadGame(
    cGame &game,
    int slot,
    std::string &errorMessage)
{
    errorMessage.clear();
    if (!save_slot::isValidSlot(slot)) {
        errorMessage = localization::text("Invalid save slot number", "Некорректный номер слота");
        return false;
    }
    const std::filesystem::path path = slotPath(slot);
    std::ifstream input(path, std::ios::binary);
    if (!input) {
        errorMessage = localization::text("Save file was not found", "Сохранение не найдено");
        return false;
    }
    std::string contents{
        std::istreambuf_iterator<char>(input),
        std::istreambuf_iterator<char>()
    };
    save_file::DecodeResult decoded = save_file::decode(
        contents,
        FormatVersion,
        MaximumSaveBytes
    );
    if (!decoded.succeeded()) {
        errorMessage = std::move(decoded.error);
        return false;
    }

    SaveSnapshot save;
    if (!deserializeBody(decoded.body, save, errorMessage)) {
        return false;
    }
    if (!restoreSnapshot(game, save, errorMessage)) {
        return false;
    }
    cLogger::getInstance()->log(
        LOG_INFO,
        COMP_GAMERULES,
        "Load game",
        path.string()
    );
    return true;
}
