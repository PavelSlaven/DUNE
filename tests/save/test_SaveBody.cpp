#include <catch2/catch_test_macros.hpp>

#include "save/SaveBody.hpp"
#include "data/gfxdata.h"

namespace {
save_game_detail::SaveSnapshot sample()
{
    using namespace save_game_detail;

    SaveSnapshot save;
    save.saveName = "Тест \"кавычки\" и \\ слэш";
    save.skirmish = true;
    save.region = 3;
    save.mission = 5;
    save.winFlags = 6;
    save.loseFlags = 1;
    save.cameraCell = 9;
    save.mapWidth = 4;
    save.mapHeight = 4;
    save.autoSpawnBlooms = true;
    save.bloomTimer = 77;
    save.desiredWorms = 2;
    save.wormRespawnTimer = 1234;

    for (int p = 0; p < MAX_PLAYERS; ++p) {
        auto &player = save.players[p];
        player.house = p % 5;
        player.team = p;
        player.techLevel = p + 1;
        player.focusCell = p;
        player.quota = 100 * p;
        player.selectedStructure = p == 0 ? 3 : -1;
        player.credits = 1234.567F + static_cast<float>(p);
        player.maxCredits = 5000.25F;
        player.powerUsage = 10 * p;
        player.powerProduce = 20 * p;
        player.alive = p != 6;
        player.autoSlab = p % 2 == 1;
        for (std::size_t t = 0; t < player.primary.size(); ++t) {
            player.primary[t] = static_cast<int>(t % 3) - 1;
            player.structures[t] = static_cast<int>(t % 4);
            player.upgrades[t] = static_cast<int>(t % 2);
        }
        for (std::size_t u = 0; u < player.appliedUpgrades.size(); ++u) {
            player.appliedUpgrades[u] = u % 3 == 0;
        }
    }

    save.cells.resize(16);
    for (int i = 0; i < 16; ++i) {
        auto &cell = save.cells[i];
        cell.credits = 10 * i;
        cell.type = i % 2 == 0 ? TERRAIN_SAND : TERRAIN_SPICE;
        cell.tile = i;
        cell.smudgeTile = i % 2 == 0 ? 3 : -1;
        cell.smudgeType = i % 4 == 0 ? -1 : i % 3;
        cell.health = 100;
        cell.passable = i % 5 != 0;
        cell.passableFoot = true;
        cell.visibilityMask = i % 2 == 0 ? 1U : 3U;
        cell.seenMask = i % 2 == 1 ? 1U : 0U;
    }

    FogState fog;
    fog.cell = 5;
    fog.hasTerrain = true;
    fog.terrainType = TERRAIN_SAND;
    fog.terrainTile = 7;
    fog.hasStructure = true;
    fog.structureType = 2;
    fog.structureOwner = 1;
    fog.structureFrame = 3;
    fog.structureOffsetX = 1;
    save.fog.push_back(fog);

    StructureState firstStructure;
    firstStructure.oldId = 0;
    firstStructure.type = 1;
    firstStructure.player = 0;
    firstStructure.cell = 0;
    firstStructure.hitPoints = 400;
    firstStructure.rallyPoint = 5;
    firstStructure.frame = 2;
    firstStructure.buildPhase = 1;
    firstStructure.unitHeading = 4;
    firstStructure.concrete = 0.25F;
    firstStructure.animate = true;
    firstStructure.animateOnApproach = true;
    firstStructure.smoke = 2;
    firstStructure.repairTimer = 1;
    firstStructure.flagTimer = 2;
    firstStructure.reduceSmokeTimer = 3;
    firstStructure.decayTimer = 4;
    firstStructure.prebuildTimer = 5;
    save.structures.push_back(firstStructure);

    StructureState secondStructure;
    secondStructure.oldId = 3;
    secondStructure.type = 5;
    secondStructure.player = 1;
    secondStructure.cell = 10;
    secondStructure.hitPoints = 250;
    save.structures.push_back(secondStructure);

    UnitState firstUnit;
    firstUnit.oldId = 0;
    firstUnit.type = 3;
    firstUnit.player = 0;
    firstUnit.cell = 6;
    firstUnit.hitPoints = 100;
    firstUnit.posX = 33.25F;
    firstUnit.posY = 64.5F;
    firstUnit.experience = 0.1F;
    firstUnit.groupMask = 21;
    firstUnit.nextCell = 7;
    firstUnit.goalCell = 9;
    for (std::size_t k = 0; k < firstUnit.path.size(); ++k) {
        firstUnit.path[k] = static_cast<int>(k % 16) - 1;
    }
    firstUnit.pathIndex = 2;
    firstUnit.pathFails = 1;
    firstUnit.calculatePath = true;
    firstUnit.attackStructure = 3;
    firstUnit.structureId = 0;
    firstUnit.credits = 700;
    firstUnit.transferType = 1;
    firstUnit.bodyFacing = 2;
    firstUnit.headFacing = 3;
    firstUnit.bodyShouldFace = 4;
    firstUnit.headShouldFace = 5;
    firstUnit.frame = 1;
    firstUnit.selected = true;
    firstUnit.action = 1;
    firstUnit.mission = 2;
    firstUnit.harvestCellMemory = 11;
    firstUnit.stayAtGoalCell = true;
    for (std::size_t k = 0; k < firstUnit.timers.size(); ++k) {
        firstUnit.timers[k] = static_cast<int>(k) + 1;
    }
    save.units.push_back(firstUnit);

    UnitState secondUnit;
    secondUnit.oldId = UnitSlots - 1;
    secondUnit.type = 10;
    secondUnit.player = 1;
    secondUnit.cell = 15;
    save.units.push_back(secondUnit);

    save.reinforcements.push_back({30, 4, 1, 12, true, false, 60});
    save.buildQueue.push_back({0, 2, 5, 3, 1, 4, 0, 50, 7, 2, 0, 2,
                               false, false, true, 0.3F, 4, 35});
    return save;
}
}

TEST_CASE("P8 save body survives snapshot to body to snapshot to body", "[P8]")
{
    const std::string body1 = save_game_detail::serializeBody(sample());
    save_game_detail::SaveSnapshot restored;
    std::string error;

    REQUIRE(save_game_detail::deserializeBody(body1, restored, error));
    REQUIRE(error.empty());
    REQUIRE(save_game_detail::serializeBody(restored) == body1);
}

TEST_CASE("P8 save body keeps port state exactly", "[P8]")
{
    const auto original = sample();
    const std::string body1 = save_game_detail::serializeBody(original);
    save_game_detail::SaveSnapshot restored;
    std::string error;

    REQUIRE(save_game_detail::deserializeBody(body1, restored, error));
    REQUIRE(restored.saveName == original.saveName);
    REQUIRE(restored.players[1].credits == original.players[1].credits);
    REQUIRE(restored.players[0].appliedUpgrades[3]);
    REQUIRE_FALSE(restored.players[0].appliedUpgrades[1]);
    REQUIRE(restored.cells[1].seenMask == 1U);
    REQUIRE(restored.fog.size() == 1);
    REQUIRE(restored.fog[0].structureFrame == 3);
    REQUIRE_FALSE(restored.fog[0].hasUnit);
    REQUIRE(restored.units[0].posX == 33.25F);
    REQUIRE(restored.units[0].experience == 0.1F);
    REQUIRE(restored.units[0].groupMask == 21);
    REQUIRE(restored.units[0].timers[11] == 12);
    REQUIRE(restored.units[0].harvestCellMemory == 11);
    REQUIRE(restored.units[0].stayAtGoalCell);
    REQUIRE(restored.units[1].oldId == save_game_detail::UnitSlots - 1);
    REQUIRE(restored.buildQueue[0].state == 2);
    REQUIRE(restored.buildQueue[0].waitingForUnitSlot);
    REQUIRE(restored.buildQueue[0].progressFrameTimer == 0.3F);
}

TEST_CASE("P8 save body without END is rejected", "[P8]")
{
    const std::string body1 = save_game_detail::serializeBody(sample());
    REQUIRE(body1.ends_with("END\n"));
    save_game_detail::SaveSnapshot restored;
    std::string error;

    REQUIRE_FALSE(save_game_detail::deserializeBody(
        std::string_view(body1).substr(0, body1.size() - 4), restored, error));
    REQUIRE_FALSE(error.empty());
}

TEST_CASE("P8 save body rejects values out of range", "[P8]")
{
    auto invalidState = sample();
    invalidState.buildQueue[0].state = 6;
    auto invalidGroups = sample();
    invalidGroups.units[0].groupMask = 32;
    auto invalidCell = sample();
    invalidCell.cells[0].type = 0;
    save_game_detail::SaveSnapshot restored;
    std::string error;

    REQUIRE_FALSE(save_game_detail::deserializeBody(
        save_game_detail::serializeBody(invalidState), restored, error));
    REQUIRE_FALSE(save_game_detail::deserializeBody(
        save_game_detail::serializeBody(invalidGroups), restored, error));
    REQUIRE_FALSE(save_game_detail::deserializeBody(
        save_game_detail::serializeBody(invalidCell), restored, error));
}
