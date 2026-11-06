#include "save/SaveFileCodec.hpp"
#include "save/SaveGameManager.cpp"

#include <iostream>
#include <string>

using namespace save_game_detail;

namespace {
bool passed = true;

void check(bool condition, const std::string &message)
{
    if (!condition) {
        std::cerr << "factory_pad_save: " << message << '\n';
        passed = false;
    }
}

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
    if (ok && result) {
        *result = parsed;
    }
    return ok;
}

void padsSurviveWritingAndReading()
{
    SaveSnapshot save = baseSnapshot();
    save.units.push_back(unitState(9, CARRYALL, 401));
    save.factoryPads.push_back({3, standingPad()});
    save.factoryPads.push_back({5, rollingPad()});
    SaveSnapshot parsed;
    check(parses(save, &parsed), "a valid save with two factory pads must be readable");
    check(parsed.factoryPads.size() == 2, "both factory pads must be read back");
    if (parsed.factoryPads.size() == 2) {
        check(parsed.factoryPads[0].structureId == 3 && samePad(parsed.factoryPads[0].pad, standingPad()),
              "the standing pad of the Light Factory must be read back unchanged");
        check(parsed.factoryPads[1].structureId == 5 && samePad(parsed.factoryPads[1].pad, rollingPad()),
              "the rolling pad of the Heavy Factory must be read back unchanged");
    }
}

void saveWithoutPadsIsReadable()
{
    SaveSnapshot parsed;
    check(parses(baseSnapshot(), &parsed) && parsed.factoryPads.empty(), "a save without pads must be readable");
}

void damagedPadsAreRejected()
{
    SaveSnapshot onBarracks = baseSnapshot();
    onBarracks.factoryPads.push_back({7, standingPad()});
    check(!parses(onBarracks), "a pad on a structure that is not a factory was accepted");

    SaveSnapshot unknownStructure = baseSnapshot();
    unknownStructure.factoryPads.push_back({9, standingPad()});
    check(!parses(unknownStructure), "a pad on a structure missing from the save was accepted");

    SaveSnapshot twice = baseSnapshot();
    twice.factoryPads.push_back({3, standingPad()});
    twice.factoryPads.push_back({3, standingPad()});
    check(!parses(twice), "two pads on one factory were accepted");

    SaveSnapshot emptyPad = baseSnapshot();
    emptyPad.factoryPads.push_back({3, factory_pad::PadState{}});
    check(!parses(emptyPad), "a saved empty pad was accepted");

    SaveSnapshot missingRoller = baseSnapshot();
    factory_pad::PadState rolling = rollingPad();
    rolling.rollUnitId = 12;
    missingRoller.factoryPads.push_back({5, rolling});
    check(!parses(missingRoller), "a rolling unit that is not in the save was accepted");

    SaveSnapshot wrongRollerType = baseSnapshot();
    rolling = rollingPad();
    rolling.unitType = TRIKE;
    wrongRollerType.factoryPads.push_back({5, rolling});
    check(!parses(wrongRollerType), "a rolling unit with a different type was accepted");

    SaveSnapshot wrongRollerOwner = baseSnapshot();
    rolling = rollingPad();
    wrongRollerOwner.units[0].player = 2;
    wrongRollerOwner.factoryPads.push_back({5, rolling});
    check(!parses(wrongRollerOwner), "a rolling unit owned by another player was accepted");

    SaveSnapshot badUnitType = baseSnapshot();
    factory_pad::PadState standing = standingPad();
    standing.unitType = MAX_UNITTYPES;
    badUnitType.factoryPads.push_back({3, standing});
    check(!parses(badUnitType), "an unknown standing unit type was accepted");

    SaveSnapshot badWaitingType = baseSnapshot();
    standing = standingPad();
    standing.waiting = {MAX_UNITTYPES};
    badWaitingType.factoryPads.push_back({3, standing});
    check(!parses(badWaitingType), "an unknown waiting unit type was accepted");

    SaveSnapshot badCarryall = baseSnapshot();
    standing = standingPad();
    standing.carryallId = MAX_UNITS;
    badCarryall.factoryPads.push_back({3, standing});
    check(!parses(badCarryall), "an unknown carry-all number was accepted");

    SaveSnapshot missingCarryall = baseSnapshot();
    missingCarryall.factoryPads.push_back({3, standingPad()});
    check(!parses(missingCarryall), "a carry-all ID missing from the saved units was accepted");

    SaveSnapshot wrongCarryallType = baseSnapshot();
    wrongCarryallType.units.push_back(unitState(9, TANK, 401));
    wrongCarryallType.factoryPads.push_back({3, standingPad()});
    check(!parses(wrongCarryallType), "a carry-all ID referring to a non-carry-all was accepted");

    SaveSnapshot wrongCarryallOwner = baseSnapshot();
    UnitState foreignCarryall = unitState(9, CARRYALL, 401);
    foreignCarryall.player = 2;
    wrongCarryallOwner.units.push_back(foreignCarryall);
    wrongCarryallOwner.factoryPads.push_back({3, standingPad()});
    check(!parses(wrongCarryallOwner), "a carry-all owned by another player was accepted");
}

void truncatedAndOldBodiesAreRejected()
{
    SaveSnapshot save = baseSnapshot();
    save.factoryPads.push_back({3, standingPad()});
    const std::string body = serializeBody(save);

    SaveSnapshot parsed;
    std::string error;
    const std::size_t padsStart = body.find("FACTORYPADS");
    check(padsStart != std::string::npos, "the body must contain the FACTORYPADS section");
    check(!deserializeBody(body.substr(0, padsStart) + "END\n", parsed, error),
          "a body without the FACTORYPADS section was accepted");
    check(!deserializeBody(body.substr(0, body.find("FACTORYPAD ") + 14), parsed, error),
          "a body cut inside a pad record was accepted");

    const std::string versionOne = save_file::encode(body, 1);
    check(!save_file::decode(versionOne, SaveGameManager::FormatVersion, 16 * 1024 * 1024).succeeded(),
          "a save of format version 1 was accepted");
    check(save_file::decode(save_file::encode(body, SaveGameManager::FormatVersion), SaveGameManager::FormatVersion,
                            16 * 1024 * 1024)
              .succeeded(),
          "a save of the current format version must be accepted");
}
}

int main()
{
    padsSurviveWritingAndReading();
    saveWithoutPadsIsReadable();
    damagedPadsAreRejected();
    truncatedAndOldBodiesAreRejected();
    if (passed) {
        std::cout << "factory_pad_save: all checks passed\n";
    }
    return passed ? 0 : 1;
}
