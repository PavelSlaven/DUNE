#include "d2tmc.h"
#include "definitions.h"
#include "gameobjects/structures/cOutPost.h"

#include <iostream>
#include <memory>
#include <sstream>
#include <vector>

int main()
{
    sStructureInfo[RADAR].flags = {s_FlagInfo{false, 25, 3}};
    auto outpost = std::make_unique<cOutPost>();
    outpost->setWidth(2);
    outpost->setHeight(2);
    outpost->setFrame(0);

    std::vector<int> frames;
    std::vector<int> callsBetweenChanges;
    int previousFrame = outpost->getFrame();
    int callsSinceChange = 0;
    for (int calls = 0; calls < 2000 && frames.size() < 17; ++calls) {
        outpost->thinkFast();
        ++callsSinceChange;
        const int frame = outpost->getFrame();
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
    for (int frame = 1; frame <= 15; ++frame) {
        expectedFrames.push_back(frame);
    }
    expectedFrames.push_back(0);
    expectedFrames.push_back(1);
    if (frames != expectedFrames) {
        std::ostringstream message;
        message << "expected frames 1..15,0,1; got";
        for (const int frame : frames) {
            message << ' ' << frame;
        }
        std::cerr << "outpost_frame: " << message.str() << '\n';
        return 1;
    }
    if (callsBetweenChanges.size() != 16) {
        std::cerr << "outpost_frame: expected 16 intervals, got " << callsBetweenChanges.size() << '\n';
        return 1;
    }
    for (size_t interval = 0; interval < callsBetweenChanges.size(); ++interval) {
        if (callsBetweenChanges[interval] != 55) {
            std::cerr << "outpost_frame: interval " << interval + 1 << " used "
                      << callsBetweenChanges[interval] << " thinkFast calls, expected 55\n";
            return 1;
        }
    }
    std::cout << "outpost_frame: 17 frame changes with 55 calls between them: ok\n";
    return 0;
}
