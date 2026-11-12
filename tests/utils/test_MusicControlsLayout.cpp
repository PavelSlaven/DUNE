#include "sidebar/HudLayout.hpp"
#include "sidebar/MusicControlsLayout.hpp"

#include <catch2/catch_test_macros.hpp>
#include <algorithm>
#include <array>
#include <cstdlib>

namespace {
void checkMusicControls(int width, int height)
{
    const HudLayout hud = HudLayout::create(width, height);
    const MusicControlsLayout music = MusicControlsLayout::create(143, hud.battlefield.getEndX() - 8);
    REQUIRE(music.visible);
    REQUIRE(music.panel.getWidth() <= 520);
    REQUIRE_FALSE(music.previous.isOverlapping(music.next));
    REQUIRE(music.panel.getEndX() <= hud.battlefield.getEndX());
    REQUIRE(music.panel.getEndY() <= HudLayout::TopBarHeight);

    const cRectangle message(
        music.panel.getEndX() + 8,
        4,
        std::max(0, hud.battlefield.getEndX() - 8 - music.panel.getEndX() - 8),
        33
    );
    if (message.getWidth() > 0) {
        REQUIRE_FALSE(message.isOverlapping(music.panel));
    }
    if (music.showsLabel()) {
        REQUIRE_FALSE(music.label.isOverlapping(music.previous));
        REQUIRE_FALSE(music.label.isOverlapping(music.next));
    }
    REQUIRE_FALSE(music.musicPanel.isOverlapping(music.speedPanel));
    REQUIRE_FALSE(music.speedLabel.isOverlapping(music.speedSlider));
    REQUIRE(music.speedSlider.getWidth() >= 50);
    REQUIRE(std::abs(music.musicPanel.getWidth() - music.speedPanel.getWidth()) <= 1);
}
}

TEST_CASE("P9 music controls fit the top bar on three canvases", "[P9]")
{
    for (const auto &canvas : std::array<std::array<int, 2>, 3>{{{800, 600}, {1920, 1080}, {3440, 1440}}}) {
        INFO("canvas " << canvas[0] << "x" << canvas[1]);
        checkMusicControls(canvas[0], canvas[1]);
    }
}
