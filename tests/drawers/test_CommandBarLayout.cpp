#include <catch2/catch_test_macros.hpp>

#include "drawers/CommandBarLayout.hpp"

namespace {
constexpr int screenWidth = 800;
constexpr int screenHeight = 600;
constexpr int sidebarWidth = 280;
constexpr int battlefieldWidth = screenWidth - sidebarWidth;
const CommandBarLayout layout = CommandBarLayout::create(screenWidth, screenHeight, sidebarWidth);
}

TEST_CASE("P10A command bar is narrower than the battlefield", "[P10A]")
{
    REQUIRE(layout.panel.getWidth() < battlefieldWidth);
}

TEST_CASE("P10A command bar ends above the screen bottom", "[P10A]")
{
    REQUIRE(layout.panel.getEndY() < screenHeight);
}

TEST_CASE("P10A command bar leaves the bottom scroll strip free", "[P10A]")
{
    REQUIRE_FALSE(layout.panel.isPointWithin(260, 599));
}

TEST_CASE("P10A every button has a size", "[P10A]")
{
    for (const cRectangle &button : layout.actions) {
        REQUIRE(button.getWidth() > 0);
        REQUIRE(button.getHeight() > 0);
    }
}

TEST_CASE("P10A every button starts inside the panel", "[P10A]")
{
    for (const cRectangle &button : layout.actions) {
        REQUIRE(layout.panel.isPointWithin(button.getX(), button.getY()));
    }
}

TEST_CASE("P10A every button ends inside the panel", "[P10A]")
{
    for (const cRectangle &button : layout.actions) {
        REQUIRE(layout.panel.isPointWithin(button.getEndX() - 1, button.getEndY() - 1));
    }
}

TEST_CASE("P10A full size panel is 350 by 52", "[P10A]")
{
    const CommandBarLayout fullSize = CommandBarLayout::create(1920, 1080, sidebarWidth);
    REQUIRE(fullSize.panel.getWidth() == 350);
    REQUIRE(fullSize.panel.getHeight() == 52);
}

TEST_CASE("P10A full size buttons are 50 by 52", "[P10A]")
{
    const CommandBarLayout fullSize = CommandBarLayout::create(1920, 1080, sidebarWidth);
    for (const cRectangle &button : fullSize.actions) {
        REQUIRE(button.getWidth() == 50);
        REQUIRE(button.getHeight() == 52);
    }
}
