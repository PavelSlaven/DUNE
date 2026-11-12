#include <catch2/catch_test_macros.hpp>

#include "gameobjects/structures/FactoryPad.hpp"

#include <cstdlib>
#include <set>
#include <sstream>
#include <string>
#include <vector>

using namespace factory_pad;

namespace {
std::string describe(const std::vector<CellCoord> &cells)
{
    std::ostringstream text;
    for (const CellCoord &cell : cells) {
        text << '(' << cell.x << ',' << cell.y << ')';
    }
    return text.str();
}
}

TEST_CASE("P8A pad center is on the right column", "[P8A][P8A-pad]")
{
    const Point light = padCenter(2, 2);
    INFO("light factory pad center must be (48, 31)");
    CHECK((light.x == 48 && light.y == 31));
    const Point heavy = padCenter(3, 2);
    INFO("heavy factory pad center must be (78, 30)");
    CHECK((heavy.x == 78 && heavy.y == 30));
}

TEST_CASE("P8A pad exit cells follow the documented order", "[P8A][P8A-pad]")
{
    const std::vector<CellCoord> light = exitCandidates(10, 10, 2, 2);
    INFO("light factory exit order is wrong: " + describe(light));
    CHECK(describe(light) == "(11,12)(12,12)(10,12)(12,11)(12,10)(12,9)(11,9)(10,9)");
    const std::vector<CellCoord> heavy = exitCandidates(5, 5, 3, 2);
    INFO("heavy factory exit order is wrong: " + describe(heavy));
    CHECK(describe(heavy) == "(7,7)(8,7)(6,7)(8,6)(8,5)(8,4)(7,4)(6,4)");
}

TEST_CASE("P8A pad exit selection skips outside and occupied cells", "[P8A][P8A-pad]")
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

    INFO("the first exit cell under the pad must be chosen when free");
    CHECK(chooseExitCell(10, 10, 2, 2, resolve, isFree) == 12 * 64 + 11);
    occupied.insert(12 * 64 + 11);
    INFO("the lower right cell must follow the lower cell");
    CHECK(chooseExitCell(10, 10, 2, 2, resolve, isFree) == 12 * 64 + 12);
    occupied.insert(12 * 64 + 12);
    occupied.insert(12 * 64 + 10);
    INFO("the right side must be searched from the bottom up");
    CHECK(chooseExitCell(10, 10, 2, 2, resolve, isFree) == 11 * 64 + 12);

    INFO("a free cell under the pad must still be chosen at the map edge");
    CHECK(chooseExitCell(61, 10, 2, 2, resolve, isFree) == 12 * 64 + 62);
    occupied.insert(12 * 64 + 62);
    INFO("cells outside the map must be skipped");
    CHECK(chooseExitCell(61, 10, 2, 2, resolve, isFree) == 12 * 64 + 61);
    for (const CellCoord &cell : exitCandidates(10, 10, 2, 2)) {
        occupied.insert(resolve(cell.x, cell.y));
    }
    INFO("no exit cell must be reported when all are occupied");
    CHECK(chooseExitCell(10, 10, 2, 2, resolve, isFree) == -1);
}

TEST_CASE("P8A pad roll moves in a straight line without jumps", "[P8A][P8A-pad]")
{
    const Point from{352, 336};
    const Point to{384, 384};
    INFO("the number of steps must be the larger axis distance");
    CHECK(rollSteps(from, to) == 48);
    const Point first = rollPosition(from, to, 0);
    INFO("step 0 must be the pad center");
    CHECK((first.x == from.x && first.y == from.y));
    const Point last = rollPosition(from, to, 48);
    INFO("the last step must be the exit cell");
    CHECK((last.x == to.x && last.y == to.y));
    Point previous = first;
    for (int step = 1; step <= 48; ++step) {
        const Point now = rollPosition(from, to, step);
        INFO("the drawing jumped more than one pixel at step " + std::to_string(step));
        CHECK((std::abs(now.x - previous.x) <= 1 && std::abs(now.y - previous.y) <= 1));
        INFO("the roll must not move backwards");
        CHECK((now.x >= previous.x && now.y >= previous.y));
        previous = now;
    }
    INFO("a roll onto the same point has no steps");
    CHECK(rollSteps(from, from) == 0);
}

TEST_CASE("P8A pad stays busy until the roll ends", "[P8A][P8A-pad]")
{
    PadState pad;
    INFO("an empty pad must accept the unit");
    CHECK((offer(pad, 7) == Offer::Appeared && pad.phase == Phase::Standing && pad.unitType == 7));
    INFO("a busy pad must queue units");
    CHECK((offer(pad, 8) == Offer::Queued && offer(pad, 9) == Offer::Queued));
    INFO("two units must wait");
    CHECK(pad.waiting.size() == 2);

    startRoll(pad, 41);
    INFO("the roll must be recorded");
    CHECK((pad.phase == Phase::Rolling && pad.rollUnitId == 41));
    INFO("the pad must stay busy while the unit rolls");
    CHECK(offer(pad, 10) == Offer::Queued);

    INFO("the first waiting unit must appear when the roll ends");
    CHECK(finishPad(pad) == 8);
    INFO("the next unit must stand on the pad");
    CHECK((pad.phase == Phase::Standing && pad.unitType == 8 && pad.rollUnitId == -1));
    INFO("the waiting units must appear in the order of readiness");
    CHECK(finishPad(pad) == 9);
    INFO("the waiting units must appear in the order of readiness");
    CHECK(finishPad(pad) == 10);
    INFO("an empty queue must free the pad");
    CHECK((finishPad(pad) == -1 && pad.phase == Phase::Empty));
}

TEST_CASE("P8A pad queue keeps every ready unit", "[P8A][P8A-pad]")
{
    PadState pad;
    offer(pad, 7);
    std::vector<int> expected;
    for (int unitType = 0; unitType < 300; ++unitType) {
        offer(pad, unitType);
        expected.push_back(unitType);
    }
    INFO("all 300 waiting unit types must remain in order");
    CHECK(pad.waiting == expected);
}

TEST_CASE("P8A pad factory choice follows the primary rule", "[P8A][P8A-pad]")
{
    std::vector<FactoryCandidate> factories{{3, true}, {5, true}, {9, true}};
    INFO("a free primary factory must be chosen");
    CHECK(chooseFactory(factories, 5) == 5);
    factories[1].padFree = false;
    INFO("the first other factory with a free pad must be chosen");
    CHECK(chooseFactory(factories, 5) == 3);
    factories[0].padFree = false;
    INFO("any free pad must be used before waiting");
    CHECK(chooseFactory(factories, 5) == 9);
    factories[2].padFree = false;
    INFO("with all pads busy the unit waits at the primary factory");
    CHECK(chooseFactory(factories, 5) == 5);
    INFO("without a primary factory the first factory is used");
    CHECK(chooseFactory(factories, -1) == 3);
    INFO("no factories means no choice");
    CHECK(chooseFactory({}, -1) == -1);
}

TEST_CASE("P8A pad blocked exit calls a carryall after three seconds", "[P8A][P8A-pad]")
{
    PadState pad;
    offer(pad, 7);
    INFO("the counter must not run during the release animation");
    CHECK((tickStanding(pad, false, false) == StandingAction::None && pad.blockedTicks == 0));

    for (int tick = 1; tick < BlockedTicksBeforeCarryall; ++tick) {
        INFO("the carryall was requested early at tick " + std::to_string(tick));
        CHECK(tickStanding(pad, true, false) == StandingAction::None);
    }
    INFO("the carryall must be requested on the 600th blocked tick");
    CHECK(tickStanding(pad, true, false) == StandingAction::RequestCarryall);
    pad.carryallId = 12;
    for (int tick = 0; tick < 1000; ++tick) {
        INFO("the carryall must be requested only once");
        CHECK(tickStanding(pad, true, false) == StandingAction::None);
    }

    pad.carryallId = -1;
    int requests = 0;
    for (int tick = 0; tick < 3 * CarryallRetryTicks; ++tick) {
        if (tickStanding(pad, true, false) == StandingAction::RequestCarryall) {
            ++requests;
        }
    }
    INFO("a lost carryall must be requested again once per 200 ticks, got " + std::to_string(requests));
    CHECK(requests == 3);
}

TEST_CASE("P8A pad free exit starts the roll and resets the counter", "[P8A][P8A-pad]")
{
    PadState pad;
    offer(pad, 7);
    for (int tick = 0; tick < 300; ++tick) {
        tickStanding(pad, true, false);
    }
    INFO("a free exit must start the roll even while a carryall is called");
    CHECK(tickStanding(pad, true, true) == StandingAction::StartRoll);
    startRoll(pad, 3);
    INFO("the counter must be cleared when the roll starts");
    CHECK(pad.blockedTicks == 0);

    PadState again;
    offer(again, 7);
    for (int tick = 0; tick < 300; ++tick) {
        tickStanding(again, true, false);
    }
    tickStanding(again, true, true);
    INFO("an exit that became free must reset the 3 second counter");
    CHECK(again.blockedTicks == 0);
}

TEST_CASE("P8A pad roll advances by the movement speed", "[P8A][P8A-pad]")
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
    INFO("a 5 step roll at 4 ticks per pixel must take 20 ticks, took " + std::to_string(ticks));
    CHECK((done && advances == 5 && ticks == 20));
}

TEST_CASE("P8A pad state survives writing and reading", "[P8A][P8A-pad]")
{
    constexpr std::size_t TestQueueLimit = 300;
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
    INFO("a written state must be readable");
    REQUIRE(read(stream, restored, TestQueueLimit));
    INFO("the restored state differs from the written state");
    CHECK((restored.phase == Phase::Standing && restored.unitType == 7 && restored.blockedTicks == 123 &&
           restored.carryallId == 17 && restored.carryallRetry == 55 &&
           restored.waiting == std::vector<int>({8, 9})));

    PadState rolling;
    offer(rolling, 4);
    startRoll(rolling, 30);
    rolling.rollStep = 11;
    rolling.rollTick = 2;
    std::stringstream rollingStream;
    write(rollingStream, rolling);
    PadState rollingBack;
    INFO("a rolling state must survive writing and reading");
    CHECK((read(rollingStream, rollingBack, TestQueueLimit) && rollingBack.phase == Phase::Rolling &&
           rollingBack.rollUnitId == 30 && rollingBack.rollStep == 11 && rollingBack.rollTick == 2));

    PadState empty;
    std::stringstream emptyStream;
    write(emptyStream, empty);
    PadState emptyBack;
    emptyBack.phase = Phase::Standing;
    INFO("an empty state must survive writing and reading");
    CHECK((read(emptyStream, emptyBack, TestQueueLimit) && emptyBack.phase == Phase::Empty &&
           emptyBack.waiting.empty()));
}

TEST_CASE("P8A pad damaged state is rejected", "[P8A][P8A-pad]")
{
    constexpr std::size_t TestQueueLimit = 300;
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
        INFO("a damaged state was accepted: '" + std::string(text) + "'");
        CHECK_FALSE(read(stream, state, TestQueueLimit));
    }
}
