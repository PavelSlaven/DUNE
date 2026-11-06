#include "ZoomTestSupport.hpp"

#include "UnitDrawRecorder.hpp"

#include "building/cItemBuilder.h"
#include "data/gfxdata.h"
#include "drawers/cStructureDrawer.h"
#include "gameobjects/structures/cBarracks.h"
#include "gameobjects/structures/cHeavyFactory.h"
#include "gameobjects/structures/cLightFactory.h"
#include "gameobjects/structures/cUnitFactory.h"
#include "gameobjects/units/cUnit.h"
#include "map/cMap.h"
#include "sidebar/cBuildingListItem.h"

#include <functional>
#include <iostream>
#include <string>
#include <vector>

using namespace zoomtest;

namespace {
constexpr int FactoryX = 20;
constexpr int FactoryY = 20;
constexpr int FirstFactoryId = 3;
constexpr int SecondFactoryId = 5;
constexpr int AnimationTicks = 400;

class DrawerAccess : public cStructureDrawer {
public:
    using cStructureDrawer::cStructureDrawer;
    void drawFactoryLayer(cAbstractStructure *structure)
    {
        drawStructureForLayer(structure, 0);
    }
};

int cellAt(int x, int y)
{
    return y * MapCells + x;
}

int absoluteX(int cell)
{
    return global_map.getAbsoluteXPositionFromCell(cell);
}

int absoluteY(int cell)
{
    return global_map.getAbsoluteYPositionFromCell(cell);
}

void defineUnit(int type, int speed, bool airborn, bool infantry)
{
    s_UnitInfo &info = sUnitInfo[type];
    info.hp = 200;
    info.speed = speed;
    info.sight = 4;
    info.airborn = airborn;
    info.infantry = infantry;
}

void defineUnits()
{
    defineUnit(TRIKE, 4, false, false);
    defineUnit(QUAD, 4, false, false);
    defineUnit(TANK, 6, false, false);
    defineUnit(HARVESTER, 8, false, false);
    defineUnit(SOLDIER, 8, false, true);
    defineUnit(CARRYALL, 2, true, false);
}

void resetWorld()
{
    defineUnits();
    for (cPlayer &player : players) {
        if (!player.difficultySettings) {
            player.difficultySettings = new cPlayerDifficultySettings();
        }
    }
    for (cAbstractStructure *&item : structure) {
        delete item;
        item = nullptr;
    }
    for (int index = 0; index < MAX_UNITS; ++index) {
        unit[index].init(index);
    }
    global_map.init(MapCells, MapCells);
    for (int cell = 0; cell < global_map.getMaxCells(); ++cell) {
        global_map.getCell(cell)->type = TERRAIN_ROCK;
    }
    for (cPlayer &player : players) {
        for (int type = 0; type < MAX_STRUCTURETYPES; ++type) {
            player.setPrimaryBuildingForStructureType(type, -1);
        }
    }
    clearUnitDrawCalls();
}

void configureAiPlayer()
{
    cPlayer &ai = players[AI_CPU1];
    ai.id = AI_CPU1;
    ai.house = ATREIDES;
    ai.m_Human = false;
}

cAbstractStructure *placeFactory(int type, int id, int x, int y, int owner)
{
    sStructureInfo[type].bmp_width = type == LIGHTFACTORY ? 64 : 96;
    sStructureInfo[type].bmp_height = 64;
    sStructureInfo[type].hp = 1000;
    sStructureInfo[type].flags.clear();
    sStructureInfo[type].flags.push_back(s_FlagInfo{false, 25, 3});

    cAbstractStructure *created = nullptr;
    if (type == LIGHTFACTORY) {
        created = new cLightFactory();
    }
    else {
        created = new cHeavyFactory();
    }
    created->setOwner(owner);
    created->setCell(cellAt(x, y));
    created->setWidth(type == LIGHTFACTORY ? 2 : 3);
    created->setHeight(2);
    created->setStructureId(id);
    created->setHitPoints(1000);
    created->setFrame(0);
    created->setBuildingFase(0);
    structure[id] = created;
    structureUtils.putStructureOnDimension(MAPID_STRUCTURES, created);
    players[owner].setPrimaryBuildingForStructureType(type, id);
    return created;
}

void finishUnit(int owner, int unitType)
{
    cItemBuilder builder(&players[owner], nullptr);
    cBuildingListItem item(unitType, sUnitInfo[unitType], 0);
    builder.deployUnit(&item, unitType);
}

int countUnits(int type)
{
    int count = 0;
    for (const cUnit &candidate : unit) {
        if (candidate.isValid() && candidate.iType == type) {
            ++count;
        }
    }
    return count;
}

int firstUnitOfType(int type)
{
    for (int index = 0; index < MAX_UNITS; ++index) {
        if (unit[index].isValid() && unit[index].iType == type) {
            return index;
        }
    }
    return -1;
}

int countAllUnits()
{
    int count = 0;
    for (const cUnit &candidate : unit) {
        if (candidate.isValid()) {
            ++count;
        }
    }
    return count;
}

int placeBlocker(int cell)
{
    for (int index = 40; index < MAX_UNITS; ++index) {
        if (!unit[index].isValid()) {
            unit[index].init(index);
            unit[index].iType = TANK;
            unit[index].iPlayer = HUMAN;
            unit[index].setCell(cell);
            unit[index].updateCellXAndY();
            unit[index].iHitPoints = 100;
            unit[index].iTempHitPoints = -1;
            unit[index].iGoalCell = cell;
            global_map.cellSetIdForLayer(cell, MAPID_UNITS, index);
            return index;
        }
    }
    return -1;
}

void removeBlocker(int index)
{
    const int cell = unit[index].iCell;
    global_map.cellResetIdFromLayer(cell, MAPID_UNITS);
    unit[index].init(index);
}

void tickWorld(int ticks = 1)
{
    for (int tick = 0; tick < ticks; ++tick) {
        for (cAbstractStructure *item : structure) {
            if (item && item->isValid()) {
                item->thinkFast();
                item->think_animation();
            }
        }
        for (cUnit &candidate : unit) {
            if (candidate.isValid()) {
                candidate.thinkFast();
            }
        }
    }
}

int ticksUntilAnimationEnds(cAbstractStructure *factory, int limit = 5000)
{
    for (int tick = 1; tick <= limit; ++tick) {
        tickWorld();
        if (!factory->isAnimating()) {
            return tick;
        }
    }
    return -1;
}

std::vector<int> exitCellsOf(int x, int y, int width)
{
    const int pad = x + width - 1;
    return {cellAt(pad, y + 2), cellAt(pad + 1, y + 2), cellAt(pad - 1, y + 2),
            cellAt(pad + 1, y + 1), cellAt(pad + 1, y), cellAt(pad + 1, y - 1),
            cellAt(pad, y - 1), cellAt(pad - 1, y - 1)};
}

std::vector<int> blockAllExits(int x, int y, int width)
{
    std::vector<int> blockers;
    for (const int cell : exitCellsOf(x, y, width)) {
        blockers.push_back(placeBlocker(cell));
    }
    return blockers;
}

void checkPadAppearance(UnitFrameFixture &fixture, int factoryType, int unitType)
{
    const int width = factoryType == LIGHTFACTORY ? 2 : 3;
    for (const int percent : {100, 110, 125, 150}) {
        fixture.setDisplaySettings(4, percent);
        for (const float zoom : {0.8F, 1.0F, 1.25F, 1.5F, 2.0F}) {
            resetWorld();
            cAbstractStructure *factory = placeFactory(factoryType, FirstFactoryId, FactoryX, FactoryY, HUMAN);
            useCamera(ScreenWidth, ScreenHeight, zoom, 0.0F, 0.0F);

            finishUnit(HUMAN, unitType);
            const std::string label = std::string(factoryType == LIGHTFACTORY ? "light" : "heavy") +
                                      " factory, unit type " + std::to_string(unitType) + ", scale " +
                                      std::to_string(percent) + "%, zoom " + std::to_string(zoom);
            require(countAllUnits() == 0, label + ": a real unit exists although the unit must only stand on the pad");

            const int padCenterX = absoluteX(factory->getCell()) + (width == 2 ? 48 : 78);
            const int padCenterY = absoluteY(factory->getCell()) + (width == 2 ? 31 : 30);
            fixture.setUnit(60, unitType, padCenterX - 16, padCenterY - 16, FACE_DOWN, FACE_DOWN);
            unit[60].iHitPoints = 100;
            clearUnitDrawCalls();
            unit[60].draw();
            const std::vector<UnitDrawCall> reference = unitDrawCalls();
            unit[60].init(60);
            global_map.cellResetIdFromLayer(cellAt((padCenterX - 16) / 32, (padCenterY - 16) / 32), MAPID_UNITS);
            require(!reference.empty(), label + ": the reference unit drew nothing");

            GameContext context;
            auto graphics = std::make_unique<GraphicsContext>();
            graphics->gfxdata = gfxdata;
            context.setGraphicsContext(std::move(graphics));
            DrawerAccess drawer(&context);
            clearUnitDrawCalls();
            drawer.drawFactoryLayer(factory);
            std::vector<UnitDrawCall> padCalls;
            size_t firstUnitCall = unitDrawCalls().size();
            size_t lastImageCall = 0;
            for (size_t index = 0; index < unitDrawCalls().size(); ++index) {
                const UnitDrawCall &call = unitDrawCalls()[index];
                if (call.texture != nullptr) {
                    padCalls.push_back(call);
                    firstUnitCall = std::min(firstUnitCall, index);
                }
                else {
                    lastImageCall = index;
                }
            }
            require(padCalls.size() == reference.size(),
                    label + ": the pad drew " + std::to_string(padCalls.size()) + " unit sprites, a unit on the map draws " +
                        std::to_string(reference.size()));
            for (size_t index = 0; index < reference.size(); ++index) {
                require(padCalls[index].method == reference[index].method, label + ": sprite kind differs");
                requireRect(padCalls[index].source, reference[index].source, label + " source");
                requireRect(padCalls[index].destination, reference[index].destination, label + " destination");
                require(std::abs(padCalls[index].floatDestination.x - reference[index].floatDestination.x) < 0.001F &&
                            std::abs(padCalls[index].floatDestination.y - reference[index].floatDestination.y) < 0.001F &&
                            std::abs(padCalls[index].floatDestination.w - reference[index].floatDestination.w) < 0.001F &&
                            std::abs(padCalls[index].floatDestination.h - reference[index].floatDestination.h) < 0.001F,
                        label + ": the fractional destination differs from a real unit");
                require(padCalls[index].opacity == reference[index].opacity, label + ": sprite opacity differs");
            }
            require(lastImageCall < firstUnitCall, label + ": the unit was drawn before the picture of the factory");

            const UnitDrawCall &body = padCalls.back();
            const float centerX = body.method == "renderStrechSpriteF"
                                      ? body.floatDestination.x + body.floatDestination.w / 2.0F
                                      : static_cast<float>(body.destination.getX()) + body.destination.getWidth() / 2.0F;
            const float expectedX = static_cast<float>(mapCamera->getWindowXPosition(padCenterX));
            require(std::abs(centerX - expectedX) <= 2.0F,
                    label + ": the unit is not centered on the pad horizontally");
            const float centerY = body.method == "renderStrechSpriteF"
                                      ? body.floatDestination.y + body.floatDestination.h / 2.0F
                                      : static_cast<float>(body.destination.getY()) + body.destination.getHeight() / 2.0F;
            const float expectedY = static_cast<float>(mapCamera->getWindowYPosition(padCenterY));
            require(std::abs(centerY - expectedY) <= 2.0F,
                    label + ": the unit is not centered on the pad vertically");
        }
    }
}

void itemOnePadAppearance(UnitFrameFixture &fixture)
{
    for (const int unitType : {TRIKE, QUAD}) {
        checkPadAppearance(fixture, LIGHTFACTORY, unitType);
    }
    for (const int unitType : {TANK, HARVESTER}) {
        checkPadAppearance(fixture, HEAVYFACTORY, unitType);
    }
}

struct RollObservation {
    int createdAtTick = -1;
    int firstEndedAnimationTick = -1;
    int rollEndTick = -1;
    int unitId = -1;
    int exitCell = -1;
    float startX = 0.0F;
    float startY = 0.0F;
};

RollObservation observeRoll(cAbstractStructure *factory, int unitType, int limit = 3000)
{
    RollObservation observation;
    for (int tick = 1; tick <= limit; ++tick) {
        tickWorld();
        if (observation.firstEndedAnimationTick < 0 && !factory->isAnimating()) {
            observation.firstEndedAnimationTick = tick;
        }
        if (observation.createdAtTick < 0) {
            const int id = firstUnitOfType(unitType);
            if (id >= 0) {
                observation.createdAtTick = tick;
                observation.unitId = id;
                observation.exitCell = unit[id].iCell;
                observation.startX = unit[id].posX;
                observation.startY = unit[id].posY;
            }
        }
        if (observation.createdAtTick >= 0 && observation.rollEndTick < 0) {
            const cUnit &rolling = unit[observation.unitId];
            if (rolling.posX == static_cast<float>(absoluteX(observation.exitCell)) &&
                    rolling.posY == static_cast<float>(absoluteY(observation.exitCell))) {
                observation.rollEndTick = tick;
                return observation;
            }
        }
    }
    return observation;
}

void itemTwoRoll(int factoryType, int unitType, int owner, int rallyCell, bool blockFirstExit)
{
    const int width = factoryType == LIGHTFACTORY ? 2 : 3;
    resetWorld();
    configureAiPlayer();
    cAbstractStructure *factory = placeFactory(factoryType, FirstFactoryId, FactoryX, FactoryY, owner);
    useCamera(ScreenWidth, ScreenHeight, 1.0F, 0.0F, 0.0F);
    if (rallyCell >= 0) {
        factory->setRallyPoint(rallyCell);
    }
    int blocker = -1;
    const std::vector<int> exits = exitCellsOf(FactoryX, FactoryY, width);
    if (blockFirstExit) {
        blocker = placeBlocker(exits[0]);
    }

    finishUnit(owner, unitType);
    require(countUnits(unitType) == 0, "the unit exists at once; it must stand on the pad until the animation ends");
    const int blockerCountBefore = countAllUnits();

    const RollObservation observed = observeRoll(factory, unitType);
    require(observed.createdAtTick > 0, "the unit never rolled out of the factory");
    require(observed.createdAtTick == observed.firstEndedAnimationTick,
            "the unit must roll out in the tick when the release animation ends: created at " +
                std::to_string(observed.createdAtTick) + ", animation ended at " +
                std::to_string(observed.firstEndedAnimationTick));
    require(observed.firstEndedAnimationTick > 340 && observed.firstEndedAnimationTick < AnimationTicks,
            "the release animation must last five fire switches (about 355 ticks), lasted " +
                std::to_string(observed.firstEndedAnimationTick));
    require(observed.exitCell == exits[blockFirstExit ? 1 : 0], "the unit used the wrong exit cell");
    require(global_map.occupied(observed.exitCell), "the exit cell is not occupied by the rolling unit");
    (void)blockerCountBefore;
    (void)blocker;

    const int padCenterX = absoluteX(factory->getCell()) + (width == 2 ? 48 : 78);
    const int padCenterY = absoluteY(factory->getCell()) + (width == 2 ? 31 : 30);
    require(std::abs(observed.startX - (padCenterX - 16)) <= 1.0F &&
                std::abs(observed.startY - (padCenterY - 16)) <= 1.0F,
            "the rolling unit must start at the center of the pad");
    require(observed.rollEndTick > observed.createdAtTick + 20, "the roll was instantaneous");
}

void itemTwoRollDetails()
{
    resetWorld();
    cAbstractStructure *factory = placeFactory(HEAVYFACTORY, FirstFactoryId, FactoryX, FactoryY, HUMAN);
    useCamera(ScreenWidth, ScreenHeight, 1.0F, 0.0F, 0.0F);
    const int rally = cellAt(30, 30);
    factory->setRallyPoint(rally);
    finishUnit(HUMAN, TANK);
    require(countUnits(TANK) == 0, "the tank exists at once instead of standing on the pad");

    int id = -1;
    for (int tick = 0; tick < 2000 && id < 0; ++tick) {
        tickWorld();
        id = firstUnitOfType(TANK);
    }
    require(id >= 0, "the tank never appeared");
    const int exitCell = unit[id].iCell;
    float previousX = unit[id].posX;
    float previousY = unit[id].posY;
    int ticks = 0;
    int pixelSteps = 0;
    const int speed = static_cast<int>(std::ceil(players[HUMAN].getDifficultySettings()->getMoveSpeed(
        TANK, global_map.getCellSlowDown(exitCell))));
    while (ticks < 5000 &&
           !(unit[id].posX == static_cast<float>(absoluteX(exitCell)) && unit[id].posY == static_cast<float>(absoluteY(exitCell)))) {
        tickWorld();
        ++ticks;
        const cUnit &rolling = unit[id];
        const bool arrived = rolling.posX == static_cast<float>(absoluteX(exitCell)) &&
                             rolling.posY == static_cast<float>(absoluteY(exitCell));
        require(rolling.iCell == exitCell, "the unit cell must stay the exit cell while rolling");
        require(arrived || rolling.iGoalCell == exitCell, "the unit own logic changed the goal while rolling");
        for (const cAbstractStructure *item : structure) {
            if (!item) continue;
            for (const int cell : const_cast<cAbstractStructure *>(item)->getCellsOfStructure()) {
                require(rolling.iCell != cell, "the unit cell became a factory cell");
            }
        }
        const float dx = rolling.posX - previousX;
        const float dy = rolling.posY - previousY;
        require(std::abs(dx) <= 1.0F && std::abs(dy) <= 1.0F, "the drawing jumped while rolling");
        require(dx >= 0.0F && dy >= 0.0F, "the unit moved backwards while rolling");
        if (dx != 0.0F || dy != 0.0F) {
            ++pixelSteps;
        }
        previousX = rolling.posX;
        previousY = rolling.posY;
    }
    const int expectedSteps = 50;
    require(pixelSteps == expectedSteps,
            "a roll from the heavy factory pad to the cell below must take 50 steps, took " + std::to_string(pixelSteps));
    require(ticks >= expectedSteps * speed - speed && ticks <= expectedSteps * speed + speed,
            "the roll speed differs from the walking speed: " + std::to_string(ticks) + " ticks for speed " +
                std::to_string(speed));
    require(unit[id].iBodyFacing == FACE_DOWN, "the body must face the direction of the roll");
    tickWorld();
    require(unit[id].iGoalCell == rally, "after the roll the unit must go to the rally point");

    const int farCell = cellAt(26, 26);
    unit[id].move_to(farCell, -1, -1, INTENT_MOVE);
    require(unit[id].iGoalCell == farCell, "the player order must replace the rally order");
}

void itemTwo()
{
    itemTwoRoll(LIGHTFACTORY, TRIKE, HUMAN, -1, false);
    itemTwoRoll(HEAVYFACTORY, TANK, HUMAN, -1, false);
    itemTwoRoll(LIGHTFACTORY, QUAD, HUMAN, -1, true);
    itemTwoRoll(HEAVYFACTORY, HARVESTER, HUMAN, cellAt(30, 30), false);
    itemTwoRollDetails();
}

void itemTwoAi()
{
    bool everMoved = false;
    for (int attempt = 0; attempt < 12 && !everMoved; ++attempt) {
        resetWorld();
        configureAiPlayer();
        cAbstractStructure *factory = placeFactory(LIGHTFACTORY, FirstFactoryId, FactoryX, FactoryY, AI_CPU1);
        useCamera(ScreenWidth, ScreenHeight, 1.0F, 0.0F, 0.0F);
        finishUnit(AI_CPU1, TRIKE);
        require(countUnits(TRIKE) == 0, "the AI unit exists at once instead of standing on the pad");
        const RollObservation observed = observeRoll(factory, TRIKE);
        require(observed.rollEndTick > 0, "the AI unit never finished rolling");
        tickWorld();
        everMoved = unit[observed.unitId].iGoalCell != unit[observed.unitId].iCell;
    }
    require(everMoved, "an AI unit without a rally point must receive a free-around move after the roll");
}

void itemThree()
{
    resetWorld();
    cAbstractStructure *first = placeFactory(LIGHTFACTORY, FirstFactoryId, 10, 10, HUMAN);
    cAbstractStructure *second = placeFactory(LIGHTFACTORY, SecondFactoryId, 40, 40, HUMAN);
    useCamera(ScreenWidth, ScreenHeight, 1.0F, 0.0F, 0.0F);

    finishUnit(HUMAN, TRIKE);
    finishUnit(HUMAN, TRIKE);
    finishUnit(HUMAN, TRIKE);
    require(countUnits(TRIKE) == 0, "ready units appeared at once instead of standing on the pads");

    int firstRollEnd = -1;
    int thirdCreated = -1;
    int ended = -1;
    for (int tick = 1; tick <= 4000; ++tick) {
        tickWorld();
        if (ended < 0 && !first->isAnimating() && !second->isAnimating()) {
            ended = tick;
        }
        if (ended > 0 && tick == ended) {
            require(countUnits(TRIKE) == 2,
                    "two pads must release two units; the third waits (units on the map: " +
                        std::to_string(countUnits(TRIKE)) + ")");
        }
        if (countUnits(TRIKE) == 2 && firstRollEnd < 0) {
            bool allArrived = true;
            for (const cUnit &candidate : unit) {
                if (candidate.isValid() && candidate.iType == TRIKE &&
                        (std::fmod(candidate.posX, 32.0F) != 0.0F || std::fmod(candidate.posY, 32.0F) != 0.0F)) {
                    allArrived = false;
                }
            }
            if (allArrived) {
                firstRollEnd = tick;
            }
        }
        if (thirdCreated < 0 && countUnits(TRIKE) >= 3) {
            thirdCreated = tick;
            break;
        }
    }
    require(thirdCreated > 0, "the waiting unit never appeared");
    require(firstRollEnd > 0 && thirdCreated >= firstRollEnd + 340,
            "the waiting unit must appear on the pad only after the previous roll ended and then wait out the animation");
}

void itemThreeBarracksUnchanged()
{
    resetWorld();
    auto *barracks = new cBarracks();
    barracks->setOwner(HUMAN);
    barracks->setCell(cellAt(30, 30));
    barracks->setWidth(2);
    barracks->setHeight(2);
    barracks->setStructureId(7);
    sStructureInfo[BARRACKS].bmp_width = 64;
    sStructureInfo[BARRACKS].bmp_height = 64;
    sStructureInfo[BARRACKS].hp = 1000;
    barracks->setHitPoints(1000);
    structure[7] = barracks;
    structureUtils.putStructureOnDimension(MAPID_STRUCTURES, barracks);
    players[HUMAN].setPrimaryBuildingForStructureType(BARRACKS, 7);

    finishUnit(HUMAN, SOLDIER);
    require(countUnits(SOLDIER) == 1, "a Barracks unit must still appear on a free cell at once");
    const int id = firstUnitOfType(SOLDIER);
    require(!global_map.occupied(cellAt(60, 60)) && unit[id].iCell != barracks->getCell(),
            "the Barracks unit was not placed around the building");
}

void itemThreeNoReinforcement()
{
    resetWorld();
    placeFactory(LIGHTFACTORY, FirstFactoryId, FactoryX, FactoryY, HUMAN);
    useCamera(ScreenWidth, ScreenHeight, 1.0F, 0.0F, 0.0F);
    for (const int cell : structure[FirstFactoryId]->getCellsAroundStructure()) {
        placeBlocker(cell);
    }
    const int unitsBefore = countAllUnits();
    finishUnit(HUMAN, TRIKE);
    require(countUnits(CARRYALL) == 0 && countAllUnits() == unitsBefore,
            "a ready factory unit must not be delivered by a reinforcement carry-all");
}

bool isOnMapEdge(int cell)
{
    const int x = global_map.getCellX(cell);
    const int y = global_map.getCellY(cell);
    return x == 0 || y == 0 || x == MapCells - 1 || y == MapCells - 1;
}

int createCarryall(int cell, int owner)
{
    return UNIT_CREATE(cell, CARRYALL, owner, true, false);
}

void itemFourOwnCarryall(bool withRally)
{
    resetWorld();
    cAbstractStructure *factory = placeFactory(LIGHTFACTORY, FirstFactoryId, FactoryX, FactoryY, HUMAN);
    useCamera(ScreenWidth, ScreenHeight, 1.0F, 0.0F, 0.0F);
    const int rally = cellAt(30, 36);
    if (withRally) {
        factory->setRallyPoint(rally);
    }
    const int farCarryall = createCarryall(cellAt(50, 50), HUMAN);
    const int nearCarryall = createCarryall(cellAt(24, 18), HUMAN);
    require(farCarryall >= 0 && nearCarryall >= 0, "the test carry-alls were not created");
    blockAllExits(FactoryX, FactoryY, 2);

    finishUnit(HUMAN, TRIKE);
    const int ended = ticksUntilAnimationEnds(factory);
    require(ended > 0, "the animation never ended");
    tickWorld(597);
    require(unit[nearCarryall].m_transferType == eTransferType::NONE &&
                unit[farCarryall].m_transferType == eTransferType::NONE,
            "a carry-all was called before the exits were blocked for 3 seconds");
    const int padCell = cellAt(FactoryX + 1, FactoryY + 1);
    const bool nearIsNearest = global_map.distance(unit[nearCarryall].iCell, padCell) <
                               global_map.distance(unit[farCarryall].iCell, padCell);
    const int expectedCarryall = nearIsNearest ? nearCarryall : farCarryall;
    const int otherCarryall = nearIsNearest ? farCarryall : nearCarryall;
    tickWorld(20);
    require(unit[expectedCarryall].m_transferType != eTransferType::NONE,
            "the nearest carry-all of the owner must be called after 3 blocked seconds");
    require(unit[otherCarryall].m_transferType == eTransferType::NONE, "only the nearest carry-all may be called");
    require(countUnits(CARRYALL) == 2, "no new carry-all may be created while an own one is free");

    int dropped = -1;
    for (int tick = 0; tick < 60000 && dropped < 0; ++tick) {
        tickWorld();
        for (int index = 0; index < 40; ++index) {
            if (unit[index].isValid() && unit[index].iType == TRIKE && !unit[index].isHidden()) {
                dropped = index;
            }
        }
    }
    require(dropped >= 0, "the carry-all never delivered the unit");
    if (withRally) {
        require(unit[dropped].iCell == rally, "the unit must be dropped at the rally point");
    }
    tickWorld(200);
    require(unit[expectedCarryall].m_transferType == eTransferType::NONE,
            "the own carry-all must end up without an order");
}

void itemFourNewCarryall()
{
    resetWorld();
    cAbstractStructure *factory = placeFactory(LIGHTFACTORY, FirstFactoryId, FactoryX, FactoryY, HUMAN);
    useCamera(ScreenWidth, ScreenHeight, 1.0F, 0.0F, 0.0F);
    blockAllExits(FactoryX, FactoryY, 2);

    finishUnit(HUMAN, TRIKE);
    require(ticksUntilAnimationEnds(factory) > 0, "the animation never ended");
    tickWorld(610);
    require(countUnits(CARRYALL) == 1, "a new carry-all must be created when the owner has none");
    const int carryall = firstUnitOfType(CARRYALL);
    require(isOnMapEdge(unit[carryall].iCell) || unit[carryall].m_transferType != eTransferType::NONE,
            "the new carry-all must start at the map border and carry an order");

    bool dropped = false;
    for (int tick = 0; tick < 80000 && !dropped; ++tick) {
        tickWorld();
        for (int index = 0; index < 40; ++index) {
            if (unit[index].isValid() && unit[index].iType == TRIKE) {
                dropped = true;
            }
        }
    }
    require(dropped, "the new carry-all never delivered the unit");
    tickWorld(50);
    require(unit[carryall].m_transferType == eTransferType::DIE && isOnMapEdge(unit[carryall].iGoalCell),
            "a new carry-all must leave the map after the drop");
}

void itemFourReleased()
{
    resetWorld();
    cAbstractStructure *factory = placeFactory(LIGHTFACTORY, FirstFactoryId, FactoryX, FactoryY, HUMAN);
    useCamera(ScreenWidth, ScreenHeight, 1.0F, 0.0F, 0.0F);
    const int own = createCarryall(cellAt(24, 14), HUMAN);
    const std::vector<int> blockers = blockAllExits(FactoryX, FactoryY, 2);
    finishUnit(HUMAN, TRIKE);
    require(ticksUntilAnimationEnds(factory) > 0, "the animation never ended");
    tickWorld(620);
    require(unit[own].m_transferType != eTransferType::NONE, "the carry-all was not called");

    removeBlocker(blockers[0]);
    tickWorld(2);
    require(unit[own].m_transferType == eTransferType::NONE,
            "the carry-all must be released when an exit cell became free before the pickup");
    require(firstUnitOfType(TRIKE) >= 0, "the unit must roll out when an exit cell became free");
}

void itemFourReleasedCarryallDestinations()
{
    resetWorld();
    cAbstractStructure *factory = placeFactory(LIGHTFACTORY, FirstFactoryId, FactoryX, FactoryY, HUMAN);
    useCamera(ScreenWidth, ScreenHeight, 1.0F, 0.0F, 0.0F);
    const std::vector<int> blockers = blockAllExits(FactoryX, FactoryY, 2);
    finishUnit(HUMAN, TRIKE);
    require(ticksUntilAnimationEnds(factory) > 0, "the animation never ended");
    tickWorld(620);
    const int newCarryall = firstUnitOfType(CARRYALL);
    require(newCarryall >= 0 && unit[newCarryall].m_transferType == eTransferType::PAD_PICKUP_LEAVE,
            "a new carry-all must be called with the leave order");
    removeBlocker(blockers[0]);
    factory->think_animation();
    require(unit[newCarryall].m_transferType == eTransferType::DIE && isOnMapEdge(unit[newCarryall].iGoalCell),
            "a released new carry-all must fly to the map edge and disappear");

    resetWorld();
    factory = placeFactory(LIGHTFACTORY, FirstFactoryId, FactoryX, FactoryY, HUMAN);
    useCamera(ScreenWidth, ScreenHeight, 1.0F, 0.0F, 0.0F);
    const int ownCarryall = createCarryall(cellAt(24, 14), HUMAN);
    const std::vector<int> ownBlockers = blockAllExits(FactoryX, FactoryY, 2);
    finishUnit(HUMAN, TRIKE);
    require(ticksUntilAnimationEnds(factory) > 0, "the animation never ended");
    tickWorld(601);
    require(unit[ownCarryall].m_transferType == eTransferType::PAD_PICKUP_STAY,
            "the own carry-all must be called before the exit is freed");
    const int ownCell = unit[ownCarryall].iCell;
    removeBlocker(ownBlockers[0]);
    factory->think_animation();
    require(unit[ownCarryall].m_transferType == eTransferType::NONE && unit[ownCarryall].iGoalCell == ownCell,
            "a released own carry-all must stay at its current cell without an order");
}

void itemFourForeignCarryall()
{
    resetWorld();
    cUnitFactory *first = static_cast<cUnitFactory *>(
                              placeFactory(LIGHTFACTORY, FirstFactoryId, FactoryX, FactoryY, HUMAN));
    cUnitFactory *second = static_cast<cUnitFactory *>(
                               placeFactory(LIGHTFACTORY, SecondFactoryId, FactoryX + 15, FactoryY, HUMAN));
    const int carryall = createCarryall(cellAt(60, 60), HUMAN);
    require(carryall >= 0, "the test carry-all was not created");

    factory_pad::PadState staleCall;
    staleCall.phase = factory_pad::Phase::Standing;
    staleCall.unitType = TRIKE;
    staleCall.carryallId = carryall;
    first->restorePad(staleCall);

    factory_pad::PadState waitingForCarryall;
    waitingForCarryall.phase = factory_pad::Phase::Standing;
    waitingForCarryall.unitType = TRIKE;
    waitingForCarryall.blockedTicks = factory_pad::BlockedTicksBeforeCarryall - 1;
    second->restorePad(waitingForCarryall);
    blockAllExits(FactoryX + 15, FactoryY, 2);
    second->think_animation();

    const int secondPadCell = cellAt(FactoryX + 15 + 1, FactoryY + 1);
    require(second->getPad().carryallId == carryall &&
                unit[carryall].m_transferType == eTransferType::PAD_PICKUP_STAY &&
                unit[carryall].iBringTarget == secondPadCell,
            "the second factory must call the carry-all to its own pad");
    first->releasePad();

    require(unit[carryall].m_transferType == eTransferType::PAD_PICKUP_STAY &&
                unit[carryall].iBringTarget == secondPadCell,
            "the first factory must not cancel a carry-all called to the second factory");
}

void itemTwoStaleRollerAlias()
{
    resetWorld();
    cUnitFactory *first = static_cast<cUnitFactory *>(
                              placeFactory(LIGHTFACTORY, SecondFactoryId, FactoryX, FactoryY, HUMAN));
    cUnitFactory *second = static_cast<cUnitFactory *>(
                               placeFactory(LIGHTFACTORY, FirstFactoryId, FactoryX + 15, FactoryY, HUMAN));
    const int oldRoller = UNIT_CREATE(cellAt(5, 5), TRIKE, HUMAN, true, false);
    require(oldRoller >= 0, "the first factory's roller was not created");
    factory_pad::PadState firstRoll;
    firstRoll.phase = factory_pad::Phase::Rolling;
    firstRoll.unitType = TRIKE;
    firstRoll.rollUnitId = oldRoller;
    first->restorePad(firstRoll);
    unit[oldRoller].die(false, false);

    second->acceptReadyUnit(TRIKE);
    for (int tick = 0; tick < 5000 && (second->isAnimating() || second->getPad().phase != factory_pad::Phase::Rolling);
            ++tick) {
        second->think_animation();
    }
    require(second->getPad().phase == factory_pad::Phase::Rolling && second->getPad().rollUnitId == oldRoller,
            "the second factory must reuse the dead roller's slot");

    const float beforeX = unit[oldRoller].posX;
    const float beforeY = unit[oldRoller].posY;
    const bool beforeRolling = unit[oldRoller].bRollingOffFactoryPad;
    for (int tick = 0; tick < 50; ++tick) {
        first->think_animation();
    }

    require(unit[oldRoller].posX == beforeX && unit[oldRoller].posY == beforeY &&
                unit[oldRoller].bRollingOffFactoryPad == beforeRolling,
            "the first factory must not move or clear the second factory's roller");
}

struct FrameLog {
    int endTick = -1;
    int toggles = 0;
    bool frameAlwaysZero = true;
};

FrameLog observeCycle(int factoryType)
{
    resetWorld();
    cAbstractStructure *factory = placeFactory(factoryType, FirstFactoryId, FactoryX, FactoryY, HUMAN);
    useCamera(ScreenWidth, ScreenHeight, 1.0F, 0.0F, 0.0F);
    finishUnit(HUMAN, factoryType == LIGHTFACTORY ? TRIKE : TANK);
    FrameLog log;
    bool previousFlash = factoryType == LIGHTFACTORY ? static_cast<cLightFactory *>(factory)->drawFlash
                                                     : static_cast<cHeavyFactory *>(factory)->drawFlash;
    for (int tick = 1; tick <= 1500; ++tick) {
        tickWorld();
        if (factory->getFrame() != 0) {
            log.frameAlwaysZero = false;
        }
        const bool flash = factoryType == LIGHTFACTORY ? static_cast<cLightFactory *>(factory)->drawFlash
                                                       : static_cast<cHeavyFactory *>(factory)->drawFlash;
        if (flash != previousFlash && factory->isAnimating()) {
            ++log.toggles;
        }
        previousFlash = flash;
        if (log.endTick < 0 && !factory->isAnimating()) {
            log.endTick = tick;
        }
    }
    return log;
}

void itemFive()
{
    const FrameLog light = observeCycle(LIGHTFACTORY);
    const FrameLog heavy = observeCycle(HEAVYFACTORY);
    require(heavy.frameAlwaysZero, "the frame of the heavy factory must always be 0");
    require(light.frameAlwaysZero, "the frame of the light factory must stay 0 in this setup");
    require(heavy.endTick == light.endTick,
            "the heavy factory animation must end like the light one: heavy " + std::to_string(heavy.endTick) +
                ", light " + std::to_string(light.endTick));
    require(heavy.toggles == light.toggles && heavy.toggles >= 4,
            "the heavy factory must switch the fire like the light one: heavy " + std::to_string(heavy.toggles) +
                ", light " + std::to_string(light.toggles));
}

constexpr int FlickerTicksPerFrame = 41;

struct BuilderScope {
    int owner;
    cItemBuilder *builder;
    cBuildingListItem item;

    BuilderScope(int ownerId, int unitType) :
        owner(ownerId),
        builder(new cItemBuilder(&players[ownerId], nullptr)),
        item(unitType, sUnitInfo[unitType], 0)
    {
        players[owner].itemBuilder = builder;
        builder->m_items[0] = &item;
        item.setIsBuilding(true);
    }

    ~BuilderScope()
    {
        players[owner].itemBuilder = nullptr;
        delete builder;
    }

    BuilderScope(const BuilderScope &) = delete;
    BuilderScope &operator=(const BuilderScope &) = delete;
};

void itemSevenSingleFactory(int factoryType, int unitType)
{
    resetWorld();
    cAbstractStructure *factory = placeFactory(factoryType, FirstFactoryId, FactoryX, FactoryY, HUMAN);
    useCamera(ScreenWidth, ScreenHeight, 1.0F, 0.0F, 0.0F);
    BuilderScope scope(HUMAN, unitType);
    for (int tick = 1; tick <= FlickerTicksPerFrame * 16; ++tick) {
        tickWorld();
        const int expected = (tick / FlickerTicksPerFrame) % 7;
        require(factory->getFrame() == expected,
                "flicker frame at tick " + std::to_string(tick) + " must be " + std::to_string(expected) +
                    ", is " + std::to_string(factory->getFrame()));
    }
    scope.item.setIsBuilding(false);
    tickWorld();
    require(factory->getFrame() == 0, "the frame must be 0 on the tick after the building stopped");
    tickWorld(FlickerTicksPerFrame * 3);
    require(factory->getFrame() == 0, "the frame must stay 0 without a unit being built");
}

void itemSevenWrongType()
{
    resetWorld();
    cAbstractStructure *heavy = placeFactory(HEAVYFACTORY, FirstFactoryId, FactoryX, FactoryY, HUMAN);
    cAbstractStructure *light = placeFactory(LIGHTFACTORY, SecondFactoryId, 40, 40, HUMAN);
    useCamera(ScreenWidth, ScreenHeight, 1.0F, 0.0F, 0.0F);
    BuilderScope scope(HUMAN, TRIKE);
    for (int tick = 1; tick <= FlickerTicksPerFrame * 3; ++tick) {
        tickWorld();
        require(heavy->getFrame() == 0, "a heavy factory must not flicker while a light factory unit is built");
    }
    require(light->getFrame() == 3, "the light factory must flicker while its unit is built");
}

void itemSevenChosenFactory()
{
    resetWorld();
    cAbstractStructure *first = placeFactory(LIGHTFACTORY, FirstFactoryId, 10, 10, HUMAN);
    cAbstractStructure *second = placeFactory(LIGHTFACTORY, SecondFactoryId, 40, 40, HUMAN);
    useCamera(ScreenWidth, ScreenHeight, 1.0F, 0.0F, 0.0F);
    BuilderScope scope(HUMAN, TRIKE);
    for (int tick = 1; tick <= FlickerTicksPerFrame * 2; ++tick) {
        tickWorld();
        require(first->getFrame() == 0, "only the primary factory may flicker while its pad is free");
    }
    require(second->getFrame() == 2, "the primary factory must flicker");

    finishUnit(HUMAN, TRIKE);
    require(second->isAnimating(), "the finished unit must stand on the primary pad");
    tickWorld(FlickerTicksPerFrame * 2);
    require(second->getFrame() == 0, "the factory with a busy pad must stop flickering");
    require(first->getFrame() == 2, "the other factory with a free pad must flicker");
}

void itemSevenUnderStandingUnit()
{
    resetWorld();
    cAbstractStructure *factory = placeFactory(LIGHTFACTORY, FirstFactoryId, FactoryX, FactoryY, HUMAN);
    useCamera(ScreenWidth, ScreenHeight, 1.0F, 0.0F, 0.0F);
    BuilderScope scope(HUMAN, TRIKE);
    finishUnit(HUMAN, TRIKE);
    require(factory->isAnimating(), "the finished unit must stand on the pad");
    tickWorld(FlickerTicksPerFrame * 3);
    require(factory->getFrame() == 3, "the flicker must go on under a standing unit");
}

void itemSevenDrawsTheFrame()
{
    resetWorld();
    cAbstractStructure *factory = placeFactory(LIGHTFACTORY, FirstFactoryId, FactoryX, FactoryY, HUMAN);
    useCamera(ScreenWidth, ScreenHeight, 1.0F, 0.0F, 0.0F);
    BuilderScope scope(HUMAN, TRIKE);
    tickWorld(FlickerTicksPerFrame * 3);
    require(factory->getFrame() == 3, "the flicker did not reach frame 3");
    factory->setBuildingFase(10);

    GameContext context;
    auto graphics = std::make_unique<GraphicsContext>();
    graphics->gfxdata = gfxdata;
    context.setGraphicsContext(std::move(graphics));
    DrawerAccess drawer(&context);
    clearUnitDrawCalls();
    drawer.drawFactoryLayer(factory);
    bool found = false;
    for (const UnitDrawCall &call : unitDrawCalls()) {
        if (call.texture == nullptr && call.source.getY() == 3 * 64) {
            found = true;
        }
    }
    require(found, "the factory picture must be drawn from the frame of the flicker");
}

void itemSeven()
{
    itemSevenSingleFactory(LIGHTFACTORY, TRIKE);
    itemSevenSingleFactory(HEAVYFACTORY, TANK);
    itemSevenWrongType();
    itemSevenChosenFactory();
    itemSevenUnderStandingUnit();
    itemSevenDrawsTheFrame();
}

using Scenario = std::function<void()>;

bool run(const std::string &name, const Scenario &scenario)
{
    try {
        scenario();
        std::cout << "factory_pad_engine: " << name << ": ok\n";
        return true;
    }
    catch (const std::exception &error) {
        std::cerr << "factory_pad_engine: " << name << ": " << error.what() << '\n';
        return false;
    }
}
}

int main()
{
    bool passed = true;
    try {
        UnitFrameFixture fixture(4, 100);
        passed &= run("item 1, unit stands on the pad", [&] { itemOnePadAppearance(fixture); });
        passed &= run("item 2, unit rolls out", [] { itemTwo(); });
        passed &= run("item 2, AI unit rolls out", [] { itemTwoAi(); });
        passed &= run("item 2, stale rolling unit slot alias", [] { itemTwoStaleRollerAlias(); });
        passed &= run("item 3, queue and factory choice", [] { itemThree(); });
        passed &= run("item 3, Barracks unchanged", [] { itemThreeBarracksUnchanged(); });
        passed &= run("item 3, no reinforcement carry-all", [] { itemThreeNoReinforcement(); });
        passed &= run("item 4, own carry-all", [] { itemFourOwnCarryall(false); });
        passed &= run("item 4, own carry-all with rally point", [] { itemFourOwnCarryall(true); });
        passed &= run("item 4, new carry-all", [] { itemFourNewCarryall(); });
        passed &= run("item 4, carry-all released", [] { itemFourReleased(); });
        passed &= run("item 4, released carry-all destinations", [] { itemFourReleasedCarryallDestinations(); });
        passed &= run("item 4, foreign carry-all slot alias", [] { itemFourForeignCarryall(); });
        passed &= run("item 5, heavy factory animation", [] { itemFive(); });
        passed &= run("item 7, flicker while a unit is built", [] { itemSeven(); });
    }
    catch (const std::exception &error) {
        std::cerr << "factory_pad_engine: " << error.what() << '\n';
        return 1;
    }
    return passed ? 0 : 1;
}
