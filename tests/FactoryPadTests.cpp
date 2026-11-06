#include "gameobjects/structures/FactoryPad.hpp"

#include <cstdlib>
#include <iostream>
#include <set>
#include <sstream>
#include <string>

using namespace factory_pad;

namespace {
bool passed = true;

void check(bool condition, const std::string &message)
{
    if (!condition) {
        std::cerr << "factory_pad: " << message << '\n';
        passed = false;
    }
}

std::string describe(const std::vector<CellCoord> &cells)
{
    std::ostringstream text;
    for (const CellCoord &cell : cells) {
        text << '(' << cell.x << ',' << cell.y << ')';
    }
    return text.str();
}

void padCenterIsOnTheRightColumn()
{
    const Point light = padCenter(2, 2);
    check(light.x == 48 && light.y == 31, "light factory pad center must be (48, 31)");
    const Point heavy = padCenter(3, 2);
    check(heavy.x == 78 && heavy.y == 30, "heavy factory pad center must be (78, 30)");
}

void exitCellsFollowTheDocumentedOrder()
{
    const std::vector<CellCoord> light = exitCandidates(10, 10, 2, 2);
    check(describe(light) == "(11,12)(12,12)(10,12)(12,11)(12,10)(12,9)(11,9)(10,9)",
          "light factory exit order is wrong: " + describe(light));
    const std::vector<CellCoord> heavy = exitCandidates(5, 5, 3, 2);
    check(describe(heavy) == "(7,7)(8,7)(6,7)(8,6)(8,5)(8,4)(7,4)(6,4)",
          "heavy factory exit order is wrong: " + describe(heavy));
}

void exitSelectionSkipsOutsideAndOccupiedCells()
{
    const auto resolve = [](int x, int y) {
        if (x < 1 || y < 1 || x > 62 || y > 62) {
            return -1;
        }
        return y * 64 + x;
    };
    std::set<int> occupied;
    const auto isFree = [&occupied](int cell) {
        return occupied.count(cell) == 0;
    };

    check(chooseExitCell(10, 10, 2, 2, resolve, isFree) == 12 * 64 + 11,
          "the first exit cell under the pad must be chosen when free");

    occupied.insert(12 * 64 + 11);
    check(chooseExitCell(10, 10, 2, 2, resolve, isFree) == 12 * 64 + 12,
          "the lower right cell must follow the lower cell");
    occupied.insert(12 * 64 + 12);
    occupied.insert(12 * 64 + 10);
    check(chooseExitCell(10, 10, 2, 2, resolve, isFree) == 11 * 64 + 12,
          "the right side must be searched from the bottom up");

    check(chooseExitCell(61, 10, 2, 2, resolve, isFree) == 12 * 64 + 62,
          "a free cell under the pad must still be chosen at the map edge");
    occupied.insert(12 * 64 + 62);
    check(chooseExitCell(61, 10, 2, 2, resolve, isFree) == 12 * 64 + 61,
          "cells outside the map must be skipped");

    for (const CellCoord &cell : exitCandidates(10, 10, 2, 2)) {
        occupied.insert(resolve(cell.x, cell.y));
    }
    check(chooseExitCell(10, 10, 2, 2, resolve, isFree) == -1,
          "no exit cell must be reported when all are occupied");
}

void rollMovesInAStraightLineWithoutJumps()
{
    const Point from{352, 336};
    const Point to{384, 384};
    check(rollSteps(from, to) == 48, "the number of steps must be the larger axis distance");
    const Point first = rollPosition(from, to, 0);
    check(first.x == from.x && first.y == from.y, "step 0 must be the pad center");
    const Point last = rollPosition(from, to, 48);
    check(last.x == to.x && last.y == to.y, "the last step must be the exit cell");
    Point previous = first;
    for (int step = 1; step <= 48; ++step) {
        const Point now = rollPosition(from, to, step);
        check(std::abs(now.x - previous.x) <= 1 && std::abs(now.y - previous.y) <= 1,
              "the drawing jumped more than one pixel at step " + std::to_string(step));
        check(now.x >= previous.x && now.y >= previous.y, "the roll must not move backwards");
        previous = now;
    }
    check(rollSteps(from, from) == 0, "a roll onto the same point has no steps");
}

void padIsBusyUntilTheRollEnds()
{
    PadState pad;
    check(offer(pad, 7) == Offer::Appeared && pad.phase == Phase::Standing && pad.unitType == 7,
          "an empty pad must accept the unit");
    check(offer(pad, 8) == Offer::Queued && offer(pad, 9) == Offer::Queued,
          "a busy pad must queue units");
    check(pad.waiting.size() == 2, "two units must wait");

    startRoll(pad, 41);
    check(pad.phase == Phase::Rolling && pad.rollUnitId == 41, "the roll must be recorded");
    check(offer(pad, 10) == Offer::Queued, "the pad must stay busy while the unit rolls");

    check(finishPad(pad) == 8, "the first waiting unit must appear when the roll ends");
    check(pad.phase == Phase::Standing && pad.unitType == 8 && pad.rollUnitId == -1,
          "the next unit must stand on the pad");
    check(finishPad(pad) == 9, "the waiting units must appear in the order of readiness");
    check(finishPad(pad) == 10, "the last queued unit must appear");
    check(finishPad(pad) == -1 && pad.phase == Phase::Empty, "an empty queue must free the pad");
}

void factoryChoiceFollowsThePrimaryRule()
{
    std::vector<FactoryCandidate> factories{{3, true}, {5, true}, {9, true}};
    check(chooseFactory(factories, 5) == 5, "a free primary factory must be chosen");
    factories[1].padFree = false;
    check(chooseFactory(factories, 5) == 3, "the first other factory with a free pad must be chosen");
    factories[0].padFree = false;
    check(chooseFactory(factories, 5) == 9, "any free pad must be used before waiting");
    factories[2].padFree = false;
    check(chooseFactory(factories, 5) == 5, "with all pads busy the unit waits at the primary factory");
    check(chooseFactory(factories, -1) == 3, "without a primary factory the first factory is used");
    check(chooseFactory({}, -1) == -1, "no factories means no choice");
}

void blockedExitCallsACarryallAfterThreeSeconds()
{
    PadState pad;
    offer(pad, 7);
    check(tickStanding(pad, false, false) == StandingAction::None && pad.blockedTicks == 0,
          "the counter must not run during the release animation");

    for (int tick = 1; tick < BlockedTicksBeforeCarryall; ++tick) {
        check(tickStanding(pad, true, false) == StandingAction::None,
              "the carryall was requested early at tick " + std::to_string(tick));
    }
    check(tickStanding(pad, true, false) == StandingAction::RequestCarryall,
          "the carryall must be requested on the 600th blocked tick");
    pad.carryallId = 12;
    for (int tick = 0; tick < 1000; ++tick) {
        check(tickStanding(pad, true, false) == StandingAction::None,
              "the carryall must be requested only once");
    }

    pad.carryallId = -1;
    int requests = 0;
    for (int tick = 0; tick < 3 * CarryallRetryTicks; ++tick) {
        if (tickStanding(pad, true, false) == StandingAction::RequestCarryall) {
            ++requests;
        }
    }
    check(requests == 3, "a lost carryall must be requested again once per 200 ticks, got "
                             + std::to_string(requests));
}

void aFreeExitStartsTheRollAndResetsTheCounter()
{
    PadState pad;
    offer(pad, 7);
    for (int tick = 0; tick < 300; ++tick) {
        tickStanding(pad, true, false);
    }
    check(tickStanding(pad, true, true) == StandingAction::StartRoll,
          "a free exit must start the roll even while a carryall is called");
    startRoll(pad, 3);
    check(pad.blockedTicks == 0, "the counter must be cleared when the roll starts");

    PadState again;
    offer(again, 7);
    for (int tick = 0; tick < 300; ++tick) {
        tickStanding(again, true, false);
    }
    tickStanding(again, true, true);
    check(again.blockedTicks == 0, "an exit that became free must reset the 3 second counter");
}

void rollAdvancesByTheMovementSpeed()
{
    PadState pad;
    offer(pad, 7);
    startRoll(pad, 3);
    int advances = 0;
    bool done = false;
    int ticks = 0;
    while (!done && ticks < 1000) {
        const RollTick result = tickRoll(pad, 4, 5);
        ++ticks;
        if (result.advanced) {
            ++advances;
        }
        done = result.done;
    }
    check(done && advances == 5 && ticks == 20,
          "a 5 step roll at 4 ticks per pixel must take 20 ticks, took " + std::to_string(ticks));
}

void stateSurvivesWritingAndReading()
{
    PadState original;
    offer(original, 7);
    offer(original, 8);
    offer(original, 9);
    original.blockedTicks = 123;
    original.carryallId = 17;
    original.carryallRetry = 55;

    std::stringstream stream;
    write(stream, original);
    PadState restored;
    check(read(stream, restored), "a written state must be readable");
    check(restored.phase == Phase::Standing && restored.unitType == 7 &&
              restored.blockedTicks == 123 && restored.carryallId == 17 &&
              restored.carryallRetry == 55 && restored.waiting == std::vector<int>({8, 9}),
          "the restored state differs from the written state");

    PadState rolling;
    offer(rolling, 4);
    startRoll(rolling, 30);
    rolling.rollStep = 11;
    rolling.rollTick = 2;
    std::stringstream rollingStream;
    write(rollingStream, rolling);
    PadState rollingBack;
    check(read(rollingStream, rollingBack) && rollingBack.phase == Phase::Rolling &&
              rollingBack.rollUnitId == 30 && rollingBack.rollStep == 11 && rollingBack.rollTick == 2,
          "a rolling state must survive writing and reading");

    PadState empty;
    std::stringstream emptyStream;
    write(emptyStream, empty);
    PadState emptyBack;
    emptyBack.phase = Phase::Standing;
    check(read(emptyStream, emptyBack) && emptyBack.phase == Phase::Empty && emptyBack.waiting.empty(),
          "an empty state must survive writing and reading");
}

void damagedStateIsRejected()
{
    const char *broken[] = {
        "5 7 -1 0 0 0 -1 0 0",
        "1 -1 -1 0 0 0 -1 0 0",
        "2 7 -1 0 0 0 -1 0 0",
        "1 7 -1 0 0 0 -1 0 1000000 1",
        "1 7 -1 0 0 0 -1 0 2 5",
        "1 7 -1 0 0 -4 -1 0 0",
        "0 -1 -1 0 0 0 -1 0 1 7",
        "garbage",
        "",
    };
    for (const char *text : broken) {
        std::stringstream stream{std::string(text)};
        PadState state;
        check(!read(stream, state), std::string("a damaged state was accepted: '") + text + "'");
    }
}
}

int main()
{
    padCenterIsOnTheRightColumn();
    exitCellsFollowTheDocumentedOrder();
    exitSelectionSkipsOutsideAndOccupiedCells();
    rollMovesInAStraightLineWithoutJumps();
    padIsBusyUntilTheRollEnds();
    factoryChoiceFollowsThePrimaryRule();
    blockedExitCallsACarryallAfterThreeSeconds();
    aFreeExitStartsTheRollAndResetsTheCounter();
    rollAdvancesByTheMovementSpeed();
    stateSurvivesWritingAndReading();
    damagedStateIsRejected();
    if (passed) {
        std::cout << "factory_pad: all checks passed\n";
    }
    return passed ? 0 : 1;
}
