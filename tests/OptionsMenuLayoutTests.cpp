#include "gamestates/OptionsMenuLayout.hpp"

#include <iostream>

namespace {
bool require(bool condition, const char *message)
{
    if (!condition) {
        std::cerr << message << '\n';
        return false;
    }
    return true;
}

bool verifyNoOverlap(const OptionsMenuLayout &layout, bool playing)
{
    bool valid = true;
    valid &= require(!layout.apply.isOverlapping(layout.advanced), "apply overlaps advanced");
    valid &= require(!layout.apply.isOverlapping(layout.status), "apply overlaps status");
    valid &= require(!layout.advanced.isOverlapping(layout.status), "advanced overlaps status");
    valid &= require(!layout.mainMenu.isOverlapping(layout.quit), "main menu overlaps quit");
    valid &= require(!layout.mainMenu.isOverlapping(layout.back), "main menu overlaps back");
    valid &= require(!layout.quit.isOverlapping(layout.back), "quit overlaps back");

    if (!playing) {
        return valid;
    }
    valid &= require(!layout.apply.isOverlapping(layout.save), "apply overlaps save");
    valid &= require(!layout.apply.isOverlapping(layout.load), "apply overlaps load");
    valid &= require(!layout.advanced.isOverlapping(layout.missionSelect), "advanced overlaps mission");
    valid &= require(!layout.save.isOverlapping(layout.missionSelect), "save overlaps mission");
    valid &= require(!layout.load.isOverlapping(layout.missionSelect), "load overlaps mission");
    valid &= require(!layout.missionSelect.isOverlapping(layout.mainMenu), "mission overlaps main menu");
    return valid;
}
}

int main()
{
    bool valid = verifyNoOverlap(
        OptionsMenuLayout::create(680, 560, 32, 8, 24, 672, true, true),
        true
    );
    valid &= verifyNoOverlap(
        OptionsMenuLayout::create(680, 560, 34, 8, 24, 672, true, true),
        true
    );
    valid &= verifyNoOverlap(
        OptionsMenuLayout::create(680, 560, 32, 8, 24, 672, true, false),
        false
    );
    return valid ? 0 : 1;
}
