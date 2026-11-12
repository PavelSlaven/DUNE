#include <catch2/catch_test_macros.hpp>

#include "controls/CommandModePolicy.hpp"
#include "drawers/CommandBarPolicy.hpp"

TEST_CASE("P10A force attack survives pointer movement", "[P10A]")
{
    REQUIRE(pointerMoveCommandPolicy(ActiveCommandMode::ForceAttack) == PointerMoveCommandPolicy::Preserve);
    REQUIRE(pointerMoveCommandPolicy(ActiveCommandMode::Normal) == PointerMoveCommandPolicy::Reevaluate);
}

TEST_CASE("P10A right click cancels force attack", "[P10A]")
{
    REQUIRE(rightClickCommandPolicy(ActiveCommandMode::ForceAttack) == RightClickCommandPolicy::CancelCommand);
    REQUIRE(rightClickCommandPolicy(ActiveCommandMode::Normal) == RightClickCommandPolicy::DefaultAction);
}

TEST_CASE("P10A right click cancels rally mode", "[P10A]")
{
    REQUIRE(rightClickCommandPolicy(ActiveCommandMode::Rally) == RightClickCommandPolicy::CancelCommand);
}

TEST_CASE("P10A right click cancels repair mode", "[P10A]")
{
    REQUIRE(rightClickCommandPolicy(ActiveCommandMode::Repair) == RightClickCommandPolicy::CancelCommand);
}

TEST_CASE("P10A repair command is always available", "[P10A]")
{
    REQUIRE(isRepairCommandEnabled());
}

TEST_CASE("P10A move command follows unit selection", "[P10A]")
{
    REQUIRE_FALSE(isMoveCommandEnabled(false));
    REQUIRE(isMoveCommandEnabled(true));
}

TEST_CASE("P10A attack command follows attack-capable units", "[P10A]")
{
    REQUIRE_FALSE(isAttackCommandEnabled(false));
    REQUIRE(isAttackCommandEnabled(true));
}

TEST_CASE("P10A unload command follows harvester state", "[P10A]")
{
    REQUIRE_FALSE(isUnloadCommandEnabled(false));
    REQUIRE(isUnloadCommandEnabled(true));
}

TEST_CASE("P10A deploy command follows MCV selection", "[P10A]")
{
    REQUIRE_FALSE(isDeployCommandEnabled(false));
    REQUIRE(isDeployCommandEnabled(true));
}

TEST_CASE("P10A rally command needs an owned producer", "[P10A]")
{
    REQUIRE_FALSE(isRallyCommandEnabled(false, true));
    REQUIRE_FALSE(isRallyCommandEnabled(true, false));
    REQUIRE(isRallyCommandEnabled(true, true));
}

TEST_CASE("P10A release command needs an owned repair facility", "[P10A]")
{
    REQUIRE_FALSE(isReleaseCommandEnabled(false, true));
    REQUIRE_FALSE(isReleaseCommandEnabled(true, false));
    REQUIRE(isReleaseCommandEnabled(true, true));
}
