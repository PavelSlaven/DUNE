#include <catch2/catch_test_macros.hpp>

#include "data/gfxdata.h"
#include "save/SaveBody.hpp"
#include "save/SaveFileCodec.hpp"
#include "save/SaveGameManager.hpp"

#include <string>
#include <vector>

using namespace save_game_detail;

namespace {
StructureState factoryState(int id, int type, int cell)
{
    StructureState item;
    item.oldId = id;
    item.type = type;
    item.player = 1;
    item.cell = cell;
    item.hitPoints = 100;
    return item;
}

UnitState unitState(int id, int type, int cell)
{
    UnitState item;
    item.oldId = id;
    item.type = type;
    item.player = 1;
    item.cell = cell;
    item.hitPoints = 100;
    return item;
}

SaveSnapshot baseSnapshot()
{
    SaveSnapshot save;
    save.cells.resize(static_cast<std::size_t>(save.mapWidth) * save.mapHeight);
    for (CellState &cell : save.cells) {
        cell.type = TERRAIN_ROCK;
    }
    save.structures.push_back(factoryState(3, LIGHTFACTORY, 100));
    save.structures.push_back(factoryState(5, HEAVYFACTORY, 200));
    save.structures.push_back(factoryState(7, BARRACKS, 300));
    save.units.push_back(unitState(11, TANK, 400));
    return save;
}

factory_pad::PadState standingPad()
{
    factory_pad::PadState pad;
    pad.phase = factory_pad::Phase::Standing;
    pad.unitType = TRIKE;
    pad.blockedTicks = 250;
    pad.carryallId = 9;
    pad.carryallRetry = 40;
    pad.waiting = {QUAD, TRIKE};
    return pad;
}

factory_pad::PadState rollingPad()
{
    factory_pad::PadState pad;
    pad.phase = factory_pad::Phase::Rolling;
    pad.unitType = TANK;
    pad.rollUnitId = 11;
    pad.rollStep = 12;
    pad.rollTick = 2;
    pad.waiting = {HARVESTER};
    return pad;
}

bool samePad(const factory_pad::PadState &left, const factory_pad::PadState &right)
{
    return left.phase == right.phase && left.unitType == right.unitType && left.rollUnitId == right.rollUnitId &&
           left.rollStep == right.rollStep && left.rollTick == right.rollTick &&
           left.blockedTicks == right.blockedTicks && left.carryallId == right.carryallId &&
           left.carryallRetry == right.carryallRetry && left.waiting == right.waiting;
}

bool parses(const SaveSnapshot &save, SaveSnapshot *result = nullptr)
{
    SaveSnapshot parsed;
    std::string error;
    const bool ok = deserializeBody(serializeBody(save), parsed, error);
    if (ok && result != nullptr) {
        *result = parsed;
    }
    return ok;
}

bool roundTripsLongPadQueue()
{
    SaveSnapshot save = baseSnapshot();
    save.units.push_back(unitState(9, CARRYALL, 401));
    factory_pad::PadState pad = standingPad();
    pad.waiting.assign(static_cast<std::size_t>(UnitSlots + 1), TRIKE);
    save.factoryPads.push_back({3, pad});

    SaveSnapshot restored;
    std::string error;
    if (!deserializeBody(serializeBody(save), restored, error) || restored.factoryPads.size() != 1) {
        return false;
    }
    const std::vector<int> &waiting = restored.factoryPads.front().pad.waiting;
    return waiting.size() == static_cast<std::size_t>(UnitSlots + 1) && waiting == pad.waiting;
}
}

TEST_CASE("P8A pads survive writing and reading", "[P8A][P8A-padsave]")
{
    SaveSnapshot save = baseSnapshot();
    save.units.push_back(unitState(9, CARRYALL, 401));
    save.factoryPads.push_back({3, standingPad()});
    save.factoryPads.push_back({5, rollingPad()});
    SaveSnapshot parsed;
    INFO("a valid save with two factory pads must be readable");
    REQUIRE(parses(save, &parsed));
    INFO("both factory pads must be read back");
    CHECK(parsed.factoryPads.size() == 2);
    if (parsed.factoryPads.size() == 2) {
        INFO("the standing pad of the Light Factory must be read back unchanged");
        CHECK((parsed.factoryPads[0].structureId == 3 && samePad(parsed.factoryPads[0].pad, standingPad())));
        INFO("the rolling pad of the Heavy Factory must be read back unchanged");
        CHECK((parsed.factoryPads[1].structureId == 5 && samePad(parsed.factoryPads[1].pad, rollingPad())));
    }
    INFO("standing pad queue of UnitSlots + 1 unit types round trips unchanged");
    CHECK(roundTripsLongPadQueue());
}

TEST_CASE("P8A save without pads is readable", "[P8A][P8A-padsave]")
{
    SaveSnapshot parsed;
    INFO("a save without pads must be readable");
    CHECK((parses(baseSnapshot(), &parsed) && parsed.factoryPads.empty()));
}

TEST_CASE("P8A damaged pads are rejected", "[P8A][P8A-padsave]")
{
    SaveSnapshot onBarracks = baseSnapshot();
    onBarracks.factoryPads.push_back({7, standingPad()});
    INFO("a pad on a structure that is not a factory was accepted");
    CHECK_FALSE(parses(onBarracks));

    SaveSnapshot unknownStructure = baseSnapshot();
    unknownStructure.factoryPads.push_back({9, standingPad()});
    INFO("a pad on a structure missing from the save was accepted");
    CHECK_FALSE(parses(unknownStructure));

    SaveSnapshot twice = baseSnapshot();
    twice.factoryPads.push_back({3, standingPad()});
    twice.factoryPads.push_back({3, standingPad()});
    INFO("two pads on one factory were accepted");
    CHECK_FALSE(parses(twice));

    SaveSnapshot emptyPad = baseSnapshot();
    emptyPad.factoryPads.push_back({3, factory_pad::PadState{}});
    INFO("a saved empty pad was accepted");
    CHECK_FALSE(parses(emptyPad));

    SaveSnapshot missingRoller = baseSnapshot();
    factory_pad::PadState rolling = rollingPad();
    rolling.rollUnitId = 12;
    missingRoller.factoryPads.push_back({5, rolling});
    INFO("a rolling unit that is not in the save was accepted");
    CHECK_FALSE(parses(missingRoller));

    SaveSnapshot wrongRollerType = baseSnapshot();
    rolling = rollingPad();
    rolling.unitType = TRIKE;
    wrongRollerType.factoryPads.push_back({5, rolling});
    INFO("a rolling unit with a different type was accepted");
    CHECK_FALSE(parses(wrongRollerType));

    SaveSnapshot wrongRollerOwner = baseSnapshot();
    rolling = rollingPad();
    wrongRollerOwner.units[0].player = 2;
    wrongRollerOwner.factoryPads.push_back({5, rolling});
    INFO("a rolling unit owned by another player was accepted");
    CHECK_FALSE(parses(wrongRollerOwner));

    SaveSnapshot badUnitType = baseSnapshot();
    factory_pad::PadState standing = standingPad();
    standing.unitType = UnitTypeCount;
    badUnitType.factoryPads.push_back({3, standing});
    INFO("an unknown standing unit type was accepted");
    CHECK_FALSE(parses(badUnitType));

    SaveSnapshot badWaitingType = baseSnapshot();
    standing = standingPad();
    standing.waiting = {UnitTypeCount};
    badWaitingType.factoryPads.push_back({3, standing});
    INFO("an unknown waiting unit type was accepted");
    CHECK_FALSE(parses(badWaitingType));

    SaveSnapshot badCarryall = baseSnapshot();
    standing = standingPad();
    standing.carryallId = UnitSlots;
    badCarryall.factoryPads.push_back({3, standing});
    INFO("an unknown carry-all number was accepted");
    CHECK_FALSE(parses(badCarryall));

    SaveSnapshot missingCarryall = baseSnapshot();
    missingCarryall.factoryPads.push_back({3, standingPad()});
    INFO("a carry-all ID missing from the saved units was accepted");
    CHECK_FALSE(parses(missingCarryall));

    SaveSnapshot wrongCarryallType = baseSnapshot();
    wrongCarryallType.units.push_back(unitState(9, TANK, 401));
    wrongCarryallType.factoryPads.push_back({3, standingPad()});
    INFO("a carry-all ID referring to a non-carry-all was accepted");
    CHECK_FALSE(parses(wrongCarryallType));

    SaveSnapshot wrongCarryallOwner = baseSnapshot();
    UnitState foreignCarryall = unitState(9, CARRYALL, 401);
    foreignCarryall.player = 2;
    wrongCarryallOwner.units.push_back(foreignCarryall);
    wrongCarryallOwner.factoryPads.push_back({3, standingPad()});
    INFO("a carry-all owned by another player was accepted");
    CHECK_FALSE(parses(wrongCarryallOwner));
}

TEST_CASE("P8A truncated and old pad save bodies are rejected", "[P8A][P8A-padsave]")
{
    SaveSnapshot save = baseSnapshot();
    save.units.push_back(unitState(9, CARRYALL, 401));
    save.factoryPads.push_back({3, standingPad()});
    const std::string body = serializeBody(save);

    SaveSnapshot parsed;
    std::string error;
    const std::size_t padsStart = body.find("FACTORYPADS");
    INFO("the body must contain the FACTORYPADS section");
    REQUIRE(padsStart != std::string::npos);
    INFO("a body without the FACTORYPADS section was accepted");
    CHECK_FALSE(deserializeBody(body.substr(0, padsStart) + "END\n", parsed, error));
    INFO("a body cut inside a pad record was accepted");
    CHECK_FALSE(deserializeBody(body.substr(0, body.find("FACTORYPAD ") + 14), parsed, error));

    const std::string versionOne = save_file::encode(body, 1);
    INFO("a save of format version 1 was accepted");
    CHECK_FALSE(save_file::decode(versionOne, SaveGameManager::FormatVersion, MaximumSaveBytes).succeeded());
    INFO("a save of the current format version must be accepted");
    CHECK(save_file::decode(save_file::encode(body, SaveGameManager::FormatVersion), SaveGameManager::FormatVersion,
                             MaximumSaveBytes)
              .succeeded());
}
