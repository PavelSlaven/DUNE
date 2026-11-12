#include <catch2/catch_test_macros.hpp>

#include "gameobjects/players/PlacementRule.hpp"

#include <array>

namespace {
placement_rule::CellFacts terrainFacts(bool valid)
{
    placement_rule::CellFacts facts;
    facts.validTerrain = valid;
    return facts;
}
}

TEST_CASE("P8A placement rule terrain decides ordinary buildings and SLAB1", "[P8A][P8A-placement]")
{
    for (const char *terrain : {"sand", "mountain", "spice"}) {
        INFO(terrain);
        CHECK_FALSE(placement_rule::judgeCell(WINDTRAP, terrainFacts(false)).allowed());
    }
    for (const char *terrain : {"rock", "slab"}) {
        INFO(terrain);
        CHECK(placement_rule::judgeCell(WINDTRAP, terrainFacts(true)).allowed());
    }
    CHECK_FALSE(placement_rule::judgeCell(SLAB1, terrainFacts(false)).allowed());
    CHECK(placement_rule::judgeCell(SLAB4, terrainFacts(false)).allowed());
}

TEST_CASE("P8A placement rule matrix of 21 combinations", "[P8A][P8A-placement]")
{
    struct TerrainCase {
        const char *name;
        bool valid;
        std::array<bool, 3> allowed;
    };
    const std::array<int, 3> structureTypes{WINDTRAP, SLAB1, SLAB4};
    const std::array<const char *, 3> structureNames{"ordinary building", "SLAB1", "SLAB4"};
    const std::array<TerrainCase, 5> terrainCases{{
        {"sand", false, {false, false, true}},
        {"rock", true, {true, true, true}},
        {"slab", true, {true, true, true}},
        {"mountain", false, {false, false, true}},
        {"spice", false, {false, false, true}},
    }};

    for (const TerrainCase &terrain : terrainCases) {
        for (std::size_t typeIndex = 0; typeIndex < structureTypes.size(); ++typeIndex) {
            INFO(terrain.name);
            INFO(structureNames[typeIndex]);
            CHECK(placement_rule::judgeCell(structureTypes[typeIndex], terrainFacts(terrain.valid)).allowed() ==
                  terrain.allowed[typeIndex]);
        }
    }

    const std::array<std::array<bool, 3>, 2> occupantRules{{
        {false, false, true},
        {false, false, true},
    }};
    const std::array<const char *, 2> occupantNames{"structure", "living unit"};
    for (std::size_t occupantIndex = 0; occupantIndex < occupantRules.size(); ++occupantIndex) {
        for (std::size_t typeIndex = 0; typeIndex < structureTypes.size(); ++typeIndex) {
            placement_rule::CellFacts facts = terrainFacts(true);
            if (occupantIndex == 0) {
                facts.structurePresent = true;
            }
            else {
                facts.livingUnitPresent = true;
            }
            INFO(occupantNames[occupantIndex]);
            INFO(structureNames[typeIndex]);
            CHECK(placement_rule::judgeCell(structureTypes[typeIndex], facts).allowed() ==
                  occupantRules[occupantIndex][typeIndex]);
        }
    }
}

TEST_CASE("P8A placement rule structures and units block ordinary buildings but not SLAB4", "[P8A][P8A-placement]")
{
    placement_rule::CellFacts occupiedByStructure;
    occupiedByStructure.structurePresent = true;
    const auto ordinaryBuilding = placement_rule::judgeCell(WINDTRAP, occupiedByStructure);
    CHECK(ordinaryBuilding.structureBlocks);
    CHECK_FALSE(ordinaryBuilding.allowed());
    CHECK(placement_rule::judgeCell(SLAB4, occupiedByStructure).allowed());

    placement_rule::CellFacts occupiedByUnit;
    occupiedByUnit.livingUnitPresent = true;
    CHECK(placement_rule::judgeCell(WINDTRAP, occupiedByUnit).unitBlocks);
    CHECK(placement_rule::judgeCell(SLAB1, occupiedByUnit).unitBlocks);
}

TEST_CASE("P8A placement rule out of bounds", "[P8A][P8A-placement]")
{
    for (const int structureType : {WINDTRAP, SLAB1, SLAB4}) {
        placement_rule::CellFacts facts;
        facts.withinBoundaries = false;
        const auto verdict = placement_rule::judgeCell(structureType, facts);
        CHECK((verdict.outOfBounds && !verdict.allowed()));
    }

    placement_rule::CellFacts outOfBoundsAndOccupied;
    outOfBoundsAndOccupied.withinBoundaries = false;
    outOfBoundsAndOccupied.structurePresent = true;
    CHECK_FALSE(placement_rule::judgeCell(WINDTRAP, outOfBoundsAndOccupied).structureBlocks);
}

TEST_CASE("P8A placement rule build anchor", "[P8A][P8A-placement]")
{
    CHECK(placement_rule::isBuildAnchor({.ownStructure = true}));
    CHECK_FALSE(placement_rule::isBuildAnchor({.otherStructure = true, .wallOrSlab = true}));
    CHECK(placement_rule::isBuildAnchor({.wallOrSlab = true}));
    CHECK_FALSE(placement_rule::isBuildAnchor({}));
    CHECK(placement_rule::isBuildAnchor({.ownStructure = true, .wallOrSlab = true}));
}
