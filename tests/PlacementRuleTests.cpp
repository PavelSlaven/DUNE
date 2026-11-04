#include "ZoomTestSupport.hpp"

#include "UnitDrawRecorder.hpp"

#include "controls/mousestates/cMousePlaceState.h"
#include "data/gfxdata.h"
#include "drawers/cPlaceItDrawer.h"
#include "building/cItemBuilder.h"
#include "gameobjects/structures/cWindTrap.h"
#include "player/cPlayer.h"
#include "sidebar/cBuildingList.h"
#include "sidebar/cBuildingListUpdater.h"
#include "sidebar/cSideBar.h"

#include <array>
#include <iostream>
#include <string>

using namespace zoomtest;

namespace {
constexpr int CandidateCell = 20 * MapCells + 20;
constexpr int FakeStructureId = 10;

void requirePlacement(bool condition, const std::string &message)
{
    require(condition, "placement_rule: " + message);
}

void setTerrain(int cell, int terrain)
{
    tCell *mapCell = global_map.getCell(cell);
    requirePlacement(mapCell != nullptr, "test setup cell must exist");
    mapCell->type = terrain;
}

void resetMap()
{
    global_map.init(MapCells, MapCells);
    for (int cell = 0; cell < global_map.getMaxCells(); cell++) {
        setTerrain(cell, TERRAIN_ROCK);
    }
    setTerrain(CandidateCell - MapCells - 1, TERRAIN_SLAB);
}

void configurePlayerPlacement(cPlayer &player)
{
    if (player.getBuildingListUpdater() == nullptr) {
        player.setBuildingListUpdater(new cBuildingListUpdater(&player));
    }
    if (player.getItemBuilder() == nullptr) {
        player.setItemBuilder(new cItemBuilder(&player, player.getBuildingListUpdater()));
    }
    if (player.getSideBar() == nullptr) {
        player.setSideBar(new cSideBar(&player));
    }
    cSideBar *sideBar = player.getSideBar();
    for (int listIndex = 0; listIndex < cSideBar::LIST_MAX; listIndex++) {
        const auto listType = static_cast<eListType>(listIndex);
        if (sideBar->getList(listType) == nullptr) {
            sideBar->setList(listType, new cBuildingList(listType));
        }
        sideBar->getList(listType)->setItemBuilder(player.getItemBuilder());
    }

    sStructureInfo[WINDTRAP].bmp_width = 64;
    sStructureInfo[WINDTRAP].bmp_height = 64;
    sStructureInfo[WINDTRAP].hp = 100;
    sStructureInfo[WINDTRAP].hasConcrete = false;
    sStructureInfo[WINDTRAP].flags.clear();
    sStructureInfo[SLAB1].bmp_width = 32;
    sStructureInfo[SLAB1].bmp_height = 32;
    sStructureInfo[SLAB4].bmp_width = 64;
    sStructureInfo[SLAB4].bmp_height = 64;
}

bool isBadTint(const Color &color)
{
    const Color bad = game.getColorPlaceBad();
    return color.r == bad.r && color.g == bad.g && color.b == bad.b && color.a == bad.a;
}

void assertSharedDecision(InputRig &rig, int structureType, int cell, bool expected, const std::string &label)
{
    cPlayer &player = players[HUMAN];
    cBuildingListItem item(structureType, sStructureInfo[structureType], 0);
    item.setTimesToBuild(2);
    item.setPlaceIt(true);

    const s_PlaceResult placement = player.canPlaceBuildingListItemAt(cell, structureType);
    requirePlacement(placement.success == expected, label + ": shared placement rule returned the wrong result");

    cMousePlaceState placeState(&player, &rig.controls(), game.m_mouse);
    requirePlacement(placeState.mayPlaceIt(&item, cell) == expected,
                     label + ": click check disagrees with the shared placement rule");

    cPlaceItDrawer drawer(&player);
    clearUnitDrawCalls();
    drawer.drawStatusOfStructureAtCell(&item, cell);
    int tintCount = 0;
    for (const UnitDrawCall &call : unitDrawCalls()) {
        if (call.method != "renderRectFillColor") continue;
        tintCount++;
        requirePlacement(isBadTint(call.color) == !expected,
                         label + ": placement tint disagrees with the shared placement rule");
    }
    requirePlacement(tintCount > 0, label + ": no footprint cells were tinted");

    cAbstractStructure *placed = player.placeItem(cell, &item);
    if (expected && structureType == WINDTRAP) {
        requirePlacement(placed != nullptr, label + ": allowed building was not created");
        requirePlacement(item.getTimesToBuild() == 1 && !item.shouldPlaceIt(),
                         label + ": successful building placement did not consume the ready item");
    }
    else if (expected) {
        requirePlacement(placed == nullptr, label + ": concrete placement unexpectedly created a structure object");
        requirePlacement(item.getTimesToBuild() == 1 && !item.shouldPlaceIt(),
                         label + ": successful concrete placement did not consume the ready item");
    }
    else {
        requirePlacement(placed == nullptr, label + ": blocked building was created");
        requirePlacement(item.getTimesToBuild() == 2 && item.shouldPlaceIt(),
                         label + ": refused placement changed the ready item");
    }
}

enum class PlacementOccupant {
    NONE,
    STRUCTURE,
    UNIT
};

void setPlacementFootprintTerrain(int terrain)
{
    for (int offsetY = 0; offsetY < 2; offsetY++) {
        for (int offsetX = 0; offsetX < 2; offsetX++) {
            setTerrain(CandidateCell + offsetX + offsetY * MapCells, terrain);
        }
    }
}

void assertPlacementMatrixCase(UnitFrameFixture &fixture,
                               InputRig &rig,
                               int structureType,
                               int terrain,
                               PlacementOccupant occupant,
                               bool expected,
                               const std::string &label)
{
    resetMap();
    setPlacementFootprintTerrain(terrain);

    if (occupant == PlacementOccupant::STRUCTURE) {
        auto *existingStructure = new cWindTrap();
        existingStructure->setOwner(HUMAN);
        existingStructure->setCell(CandidateCell);
        existingStructure->setStructureId(FakeStructureId);
        structure[FakeStructureId] = existingStructure;
        global_map.cellSetIdForLayer(CandidateCell, MAPID_STRUCTURES, FakeStructureId);
    }
    else if (occupant == PlacementOccupant::UNIT) {
        const int x = global_map.getCellX(CandidateCell) * CellSize;
        const int y = global_map.getCellY(CandidateCell) * CellSize;
        fixture.setUnit(0, TANK, x, y);
    }

    std::array<int, 4> terrainBefore{};
    for (int offsetY = 0; offsetY < 2; offsetY++) {
        for (int offsetX = 0; offsetX < 2; offsetX++) {
            const int index = offsetY * 2 + offsetX;
            terrainBefore[index] = global_map.getCellType(CandidateCell + offsetX + offsetY * MapCells);
        }
    }

    assertSharedDecision(rig, structureType, CandidateCell, expected, label);

    for (int offsetY = 0; offsetY < 2; offsetY++) {
        for (int offsetX = 0; offsetX < 2; offsetX++) {
            const int index = offsetY * 2 + offsetX;
            const int cell = CandidateCell + offsetX + offsetY * MapCells;
            int expectedTerrain = terrainBefore[index];
            if (expected && structureType == SLAB1 && index == 0) {
                expectedTerrain = TERRAIN_SLAB;
            }
            if (expected && structureType == SLAB4 && terrainBefore[index] == TERRAIN_ROCK &&
                    !(occupant == PlacementOccupant::UNIT && index == 0)) {
                expectedTerrain = TERRAIN_SLAB;
            }
            requirePlacement(global_map.getCellType(cell) == expectedTerrain,
                             label + ": placing the item produced an unexpected terrain change");
        }
    }
}

void checkPlacementDecisionMatrix(UnitFrameFixture &fixture, InputRig &rig)
{
    struct TerrainCase {
        const char *name;
        int terrain;
        std::array<bool, 3> allowed;
    };
    const std::array<int, 3> structureTypes{WINDTRAP, SLAB1, SLAB4};
    const std::array<const char *, 3> structureNames{"ordinary building", "SLAB1", "SLAB4"};
    const std::array<TerrainCase, 5> terrainCases{{
        {"sand", TERRAIN_SAND, {false, false, true}},
        {"rock", TERRAIN_ROCK, {true, true, true}},
        {"slab", TERRAIN_SLAB, {true, true, true}},
        {"mountain", TERRAIN_MOUNTAIN, {false, false, true}},
        {"spice", TERRAIN_SPICE, {false, false, true}}
    }};

    for (const TerrainCase &terrainCase : terrainCases) {
        for (std::size_t typeIndex = 0; typeIndex < structureTypes.size(); typeIndex++) {
            const std::string label = std::string(structureNames[typeIndex]) + " on " + terrainCase.name;
            assertPlacementMatrixCase(fixture,
                                      rig,
                                      structureTypes[typeIndex],
                                      terrainCase.terrain,
                                      PlacementOccupant::NONE,
                                      terrainCase.allowed[typeIndex],
                                      label);
        }
    }

    const std::array<std::array<bool, 3>, 2> occupantRules{{
        {false, false, true},
        {false, true, true}
    }};
    const std::array<PlacementOccupant, 2> occupants{PlacementOccupant::STRUCTURE, PlacementOccupant::UNIT};
    const std::array<const char *, 2> occupantNames{"structure", "unit"};
    for (std::size_t occupantIndex = 0; occupantIndex < occupants.size(); occupantIndex++) {
        for (std::size_t typeIndex = 0; typeIndex < structureTypes.size(); typeIndex++) {
            const std::string label = std::string(structureNames[typeIndex]) + " with a " + occupantNames[occupantIndex];
            assertPlacementMatrixCase(fixture,
                                      rig,
                                      structureTypes[typeIndex],
                                      TERRAIN_ROCK,
                                      occupants[occupantIndex],
                                      occupantRules[occupantIndex][typeIndex],
                                      label);
        }
    }
}

void checkTerrainRule(InputRig &rig)
{
    resetMap();
    setTerrain(CandidateCell, TERRAIN_SAND);
    assertSharedDecision(rig, WINDTRAP, CandidateCell, false, "building on sand");

    resetMap();
    assertSharedDecision(rig, WINDTRAP, CandidateCell, true, "building on rock");
}

void checkSlab4OverStructure(InputRig &rig)
{
    resetMap();
    const int occupiedCell = CandidateCell + MapCells + 1;
    auto *existingStructure = new cWindTrap();
    existingStructure->setOwner(HUMAN);
    existingStructure->setCell(occupiedCell);
    existingStructure->setStructureId(FakeStructureId);
    structure[FakeStructureId] = existingStructure;
    global_map.cellSetIdForLayer(occupiedCell, MAPID_STRUCTURES, FakeStructureId);

    assertSharedDecision(rig, SLAB4, CandidateCell, true, "SLAB4 partly over a structure");
}

void checkSlab1OverUnit(UnitFrameFixture &fixture, InputRig &rig)
{
    resetMap();
    fixture.setUnit(0, TANK, 20 * CellSize, 20 * CellSize);
    assertSharedDecision(rig, SLAB1, CandidateCell, true, "SLAB1 over a unit");
}

void checkAiPlacementWithoutBuilderConnection()
{
    resetMap();
    setTerrain(CandidateCell - MapCells - 1, TERRAIN_ROCK);

    cPlayer &human = players[HUMAN];
    cBuildingListItem humanItem(WINDTRAP, sStructureInfo[WINDTRAP], 0);
    humanItem.setTimesToBuild(2);
    humanItem.setPlaceIt(true);
    requirePlacement(!human.canPlaceBuildingListItemAt(CandidateCell, WINDTRAP).success,
                     "human building without a construction link was allowed");
    requirePlacement(human.placeItem(CandidateCell, &humanItem) == nullptr,
                     "human building without a construction link was created");
    requirePlacement(humanItem.getTimesToBuild() == 2 && humanItem.shouldPlaceIt(),
                     "refused human placement changed the ready item");

    cPlayer &ai = players[AI_CPU1];
    ai.id = AI_CPU1;
    ai.house = ATREIDES;
    ai.m_Human = false;
    configurePlayerPlacement(ai);
    cBuildingListItem aiItem(WINDTRAP, sStructureInfo[WINDTRAP], 0);
    aiItem.setTimesToBuild(2);
    aiItem.setPlaceIt(true);
    requirePlacement(ai.placeItem(CandidateCell, &aiItem) != nullptr,
                     "AI building without a construction link was not created");
}

void runPlacementRuleChecks()
{
    UnitFrameFixture fixture(4, 100);
    InputRig rig;
    rig.setMousePosition(400, 300);
    useCamera(ScreenWidth, ScreenHeight, 1.0F, 0.0F, 0.0F);
    rig.installControls();
    configurePlayerPlacement(players[HUMAN]);

    checkTerrainRule(rig);
    checkSlab4OverStructure(rig);
    checkSlab1OverUnit(fixture, rig);
    checkPlacementDecisionMatrix(fixture, rig);
    checkAiPlacementWithoutBuilderConnection();
}
}

int main()
{
    try {
        runPlacementRuleChecks();
        std::cout << "placement_rule: all checks passed\n";
    }
    catch (const std::exception &error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
    return 0;
}
