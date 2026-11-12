#include <catch2/catch_test_macros.hpp>

#include "gameobjects/structures/OutpostDish.hpp"

#include <vector>

TEST_CASE("P8A outpost dish 32 frames with 55 calls per frame", "[P8A][P8A-dish]")
{
    int frame = 0;
    int timer = 0;
    std::vector<int> frames;
    std::vector<int> callsBetweenChanges;
    int previousFrame = frame;
    int callsSinceChange = 0;
    for (int calls = 0; calls < 4000 && frames.size() < 33; ++calls) {
        outpost_dish::advance(frame, timer);
        ++callsSinceChange;
        if (frame != previousFrame) {
            frames.push_back(frame);
            if (frames.size() > 1) {
                callsBetweenChanges.push_back(callsSinceChange);
            }
            previousFrame = frame;
            callsSinceChange = 0;
        }
    }

    std::vector<int> expectedFrames;
    for (int current = 1; current <= 31; ++current) {
        expectedFrames.push_back(current);
    }
    expectedFrames.push_back(0);
    expectedFrames.push_back(1);
    CHECK(frames == expectedFrames);
    CHECK(callsBetweenChanges.size() == 32);
    for (std::size_t interval = 0; interval < callsBetweenChanges.size(); ++interval) {
        INFO("interval " << interval + 1);
        CHECK(callsBetweenChanges[interval] == 55);
    }
}
