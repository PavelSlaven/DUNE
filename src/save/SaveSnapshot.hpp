#pragma once

#include "include/definitions.h"

#include <array>
#include <cstddef>
#include <cstdint>
#include <string>
#include <vector>

namespace save_game_detail {

inline constexpr std::size_t MaximumSaveBytes = 16U * 1024U * 1024U;
inline constexpr int PathSize = 512;
inline constexpr int UnitSlots = 315;
inline constexpr int HouseCount = 12;
inline constexpr int UnitTypeCount = 50;
inline constexpr int UpgradeTypeCount = 50;
inline constexpr int UnitTimerCount = 12;
inline constexpr int DefaultTimerCap = 35;

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
    std::array<bool, UpgradeTypeCount> appliedUpgrades{};
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
    std::uint32_t seenMask = 0;
};

struct FogState {
    int cell = -1;
    bool hasTerrain = false;
    int terrainType = 0;
    int terrainTile = 0;
    int terrainSmudgeTile = -1;
    int terrainSmudgeType = -1;
    bool hasStructure = false;
    int structureType = 0;
    int structureOwner = 0;
    int structureFrame = 0;
    int structureOffsetX = 0;
    int structureOffsetY = 0;
    bool hasUnit = false;
    int unitType = 0;
    int unitOwner = 0;
    int unitBodyIndex = 0;
    int unitHeadIndex = 0;
    int unitFrame = 0;
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
    int groupMask = 0;
    int nextCell = -1;
    int goalCell = -1;
    std::array<int, PathSize> path{};
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
    int harvestCellMemory = -1;
    bool stayAtGoalCell = false;
    std::array<int, UnitTimerCount> timers{};
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
    int state = 0;
    bool placeIt = false;
    bool deployIt = false;
    bool waitingForUnitSlot = false;
    float progressFrameTimer = 0.0F;
    int flashingTimer = 0;
    int timerCap = DefaultTimerCap;
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
    std::vector<FogState> fog;
    std::vector<StructureState> structures;
    std::vector<UnitState> units;
    std::vector<ReinforcementState> reinforcements;
    std::vector<BuildQueueState> buildQueue;
};

}
