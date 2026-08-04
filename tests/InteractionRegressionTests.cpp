#include "controls/CommandModePolicy.hpp"
#include "gamestates/AdvancedOptionsHeaderLayout.hpp"

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

bool overlaps(const cRectangle &left, const cRectangle &right)
{
    return left.getX() < right.getEndX() &&
           left.getEndX() > right.getX() &&
           left.getY() < right.getEndY() &&
           left.getEndY() > right.getY();
}
}

int main()
{
    bool valid = true;
    const AdvancedOptionsHeaderLayout header =
        AdvancedOptionsHeaderLayout::create(760, 8, 34, 24);
    for (const cRectangle &tab : header.tabs) {
        valid &= require(!overlaps(header.title, tab),
                         "advanced settings title overlaps a tab");
    }
    valid &= require(
        pointerMoveCommandPolicy(ActiveCommandMode::ForceAttack) ==
            PointerMoveCommandPolicy::Preserve,
        "force attack is reset by pointer movement"
    );
    valid &= require(
        rightClickCommandPolicy(ActiveCommandMode::ForceAttack) ==
            RightClickCommandPolicy::CancelCommand,
        "right click does not cancel force attack"
    );
    valid &= require(
        rightClickCommandPolicy(ActiveCommandMode::Rally) ==
            RightClickCommandPolicy::CancelCommand,
        "right click does not cancel rally mode"
    );
    return valid ? 0 : 1;
}
