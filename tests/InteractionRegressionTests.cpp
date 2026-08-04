#include "controls/CommandModePolicy.hpp"
#include "drawers/CommandBarPolicy.hpp"
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
    valid &= require(
        rightClickCommandPolicy(ActiveCommandMode::Repair) ==
            RightClickCommandPolicy::CancelCommand,
        "right click does not cancel repair mode"
    );
    valid &= require(
        isRepairCommandEnabled(),
        "repair command is disabled without a repairable selected unit"
    );
    valid &= require(
        !isMoveCommandEnabled(false) && isMoveCommandEnabled(true),
        "move command availability does not follow unit selection"
    );
    valid &= require(
        !isAttackCommandEnabled(false) && isAttackCommandEnabled(true),
        "attack command availability does not follow attack-capable units"
    );
    valid &= require(
        !isUnloadCommandEnabled(false) && isUnloadCommandEnabled(true),
        "unload command availability does not follow harvester state"
    );
    valid &= require(
        !isDeployCommandEnabled(false) && isDeployCommandEnabled(true),
        "deploy command availability does not follow MCV selection"
    );
    valid &= require(
        !isRallyCommandEnabled(false, true) &&
            !isRallyCommandEnabled(true, false) &&
            isRallyCommandEnabled(true, true),
        "rally command availability does not require an owned producer"
    );
    valid &= require(
        !isReleaseCommandEnabled(false, true) &&
            !isReleaseCommandEnabled(true, false) &&
            isReleaseCommandEnabled(true, true),
        "release command availability does not require an owned repair facility"
    );
    return valid ? 0 : 1;
}
