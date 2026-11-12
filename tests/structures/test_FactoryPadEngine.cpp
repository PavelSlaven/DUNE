#include <catch2/catch_test_macros.hpp>

#include "gameobjects/structures/FactoryPad.hpp"

#include <cstdlib>
#include <vector>

using namespace factory_pad;

TEST_CASE("P8A pad engine unit center sits on the pad center", "[P8A][P8A-padengine]")
{
    const Point light = padOrigin(480, 320, 2, 2, 32, 32);
    CHECK(light.x == 512);
    CHECK(light.y == 335);
    const Point heavy = padOrigin(480, 320, 3, 2, 32, 32);
    CHECK(heavy.x == 542);
    CHECK(heavy.y == 334);
}

TEST_CASE("P8A pad engine exit cell is the first free cell and moves on when blocked", "[P8A][P8A-padengine]")
{
    const auto resolve = [](int x, int y) {
        return y * 64 + x;
    };
    int blockedCell = -1;
    const auto isFree = [&blockedCell](int cell) {
        return cell != blockedCell;
    };
    const std::vector<CellCoord> candidates = exitCandidates(20, 20, 2, 2);
    CHECK(chooseExitCell(20, 20, 2, 2, resolve, isFree) == resolve(candidates[0].x, candidates[0].y));
    blockedCell = resolve(candidates[0].x, candidates[0].y);
    CHECK(chooseExitCell(20, 20, 2, 2, resolve, isFree) == resolve(candidates[1].x, candidates[1].y));
}

TEST_CASE("P8A pad engine roll starts at the pad center and takes more than 20 ticks", "[P8A][P8A-padengine]")
{
    const Point from = padOrigin(480, 320, 2, 2, 32, 32);
    const Point to{21 * 32, 22 * 32};
    const Point start = rollPosition(from, to, 0);
    CHECK((start.x == from.x && start.y == from.y));
    CHECK(rollSteps(from, to) * 4 > 20);
}

TEST_CASE("P8A pad engine roll duration follows the movement speed", "[P8A][P8A-padengine]")
{
    const Point from = padOrigin(480, 320, 2, 2, 32, 32);
    const Point to{21 * 32, 22 * 32};
    const int steps = rollSteps(from, to);
    PadState pad;
    offer(pad, 7);
    startRoll(pad, 3);
    int advanced = 0;
    int calls = 0;
    bool done = false;
    while (!done) {
        const RollTick tick = tickRoll(pad, 4, steps);
        ++calls;
        advanced += tick.advanced ? 1 : 0;
        done = tick.done;
    }
    CHECK(advanced == steps);
    CHECK((calls >= steps * 4 - 4 && calls <= steps * 4 + 4));
}

TEST_CASE("P8A pad engine roll position never jumps", "[P8A][P8A-padengine]")
{
    const Point from = padOrigin(480, 320, 2, 2, 32, 32);
    const Point to{21 * 32, 22 * 32};
    const int steps = rollSteps(from, to);
    Point previous = rollPosition(from, to, 0);
    for (int step = 1; step <= steps; ++step) {
        const Point current = rollPosition(from, to, step);
        INFO("step " << step);
        CHECK((std::abs(current.x - previous.x) <= 1 && std::abs(current.y - previous.y) <= 1));
        CHECK((current.x >= previous.x && current.y >= previous.y));
        previous = current;
    }
}

TEST_CASE("P8A pad engine flicker steps through frames 0 to 6 once per 41 calls", "[P8A][P8A-padengine]")
{
    int frame = 0;
    int timer = 0;
    for (int tick = 1; tick <= 656; ++tick) {
        advanceFlicker(frame, timer, true);
        INFO("tick " << tick);
        CHECK(frame == (tick / FlickerTicksPerFrame) % FlickerFrames);
    }
    advanceFlicker(frame, timer, false);
    CHECK(frame == 0);
    CHECK(timer == 0);
}

TEST_CASE("P8A pad engine flicker goes only to the chosen factory and only for the building type", "[P8A][P8A-padengine]")
{
    const int chosen = chooseFactory({{3, true}, {5, true}}, 5);
    CHECK(chosen == 5);

    int firstFrame = 0;
    int firstTimer = 0;
    int secondFrame = 0;
    int secondTimer = 0;
    for (int tick = 0; tick < FlickerTicksPerFrame * 2; ++tick) {
        advanceFlicker(firstFrame, firstTimer, chosen == 3);
        advanceFlicker(secondFrame, secondTimer, chosen == 5);
    }
    CHECK(firstFrame == 0);
    CHECK(secondFrame == 2);

    for (int tick = 0; tick < FlickerTicksPerFrame * 2; ++tick) {
        advanceFlicker(firstFrame, firstTimer, false);
        advanceFlicker(secondFrame, secondTimer, false);
    }
    CHECK(firstFrame == 0);
    CHECK(secondFrame == 0);
}

TEST_CASE("P8A pad engine flicker follows the free pad and goes on under a standing unit", "[P8A][P8A-padengine]")
{
    PadState busyPad;
    offer(busyPad, 7);
    const int chosen = chooseFactory({{3, true}, {5, false}}, 5);
    CHECK(chosen == 3);

    int busyFrame = 0;
    int busyTimer = 0;
    int freeFrame = 0;
    int freeTimer = 0;
    for (int tick = 0; tick < FlickerTicksPerFrame * 2; ++tick) {
        advanceFlicker(busyFrame, busyTimer, false);
        advanceFlicker(freeFrame, freeTimer, chosen == 3);
    }
    CHECK(busyFrame == 0);
    CHECK(freeFrame == 2);

    int activeFrame = 0;
    int activeTimer = 0;
    for (int tick = 0; tick < FlickerTicksPerFrame * 3; ++tick) {
        advanceFlicker(activeFrame, activeTimer, true);
    }
    CHECK(activeFrame == 3);
}
