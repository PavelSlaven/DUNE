#include "utils/HdPresentation.hpp"

#include <iostream>

namespace {
bool expectEqual(const char *label, bool actual, bool expected)
{
    if (actual == expected) {
        return true;
    }
    std::cerr << label << ": got " << actual << ", expected " << expected
              << '\n';
    return false;
}
}

int main()
{
    bool passed = true;
    passed &= expectEqual(
        "HD menu uses physical presentation",
        shouldUsePhysicalHdPresentation(true, HdPresentationScene::Menu),
        true
    );
    passed &= expectEqual(
        "HD gameplay uses physical presentation",
        shouldUsePhysicalHdPresentation(true, HdPresentationScene::Gameplay),
        true
    );
    passed &= expectEqual(
        "HD post-House Mentat uses physical presentation",
        shouldUsePhysicalHdPresentation(true, HdPresentationScene::Mentat),
        true
    );
    passed &= expectEqual(
        "Classic gameplay keeps logical presentation",
        shouldUsePhysicalHdPresentation(false, HdPresentationScene::Gameplay),
        false
    );
    passed &= expectEqual(
        "Unconverted legacy screens keep their current path",
        shouldUsePhysicalHdPresentation(true, HdPresentationScene::Legacy),
        false
    );
    return passed ? 0 : 1;
}
