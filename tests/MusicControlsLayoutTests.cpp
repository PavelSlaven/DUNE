#include "sidebar/HudLayout.hpp"
#include "sidebar/MusicControlsLayout.hpp"

#include <iostream>

namespace {
bool verify(int width, int height)
{
    const HudLayout hud = HudLayout::create(true, width, height);
    const MusicControlsLayout music = MusicControlsLayout::create(
        143,
        hud.battlefield.getEndX() - 8,
        true
    );
    if (!music.visible || music.panel.getWidth() > 520 ||
        music.previous.isOverlapping(music.next) ||
        music.panel.getEndX() > hud.battlefield.getEndX() ||
        music.panel.getEndY() > HudLayout::TopBarHeight) {
        std::cerr << "invalid music controls at " << width << 'x' << height << '\n';
        return false;
    }
    const cRectangle message(
        music.panel.getEndX() + 8,
        4,
        std::max(0, hud.battlefield.getEndX() - 8 - music.panel.getEndX() - 8),
        33
    );
    if (message.getWidth() > 0 && message.isOverlapping(music.panel)) {
        std::cerr << "message overlaps music controls\n";
        return false;
    }
    if (music.showsLabel() &&
        (music.label.isOverlapping(music.previous) || music.label.isOverlapping(music.next))) {
        std::cerr << "music label overlaps buttons\n";
        return false;
    }
    if (music.musicPanel.isOverlapping(music.speedPanel) ||
        music.speedLabel.isOverlapping(music.speedSlider) ||
        music.speedSlider.getWidth() < 50 ||
        std::abs(music.musicPanel.getWidth() - music.speedPanel.getWidth()) > 1) {
        std::cerr << "invalid speed controls geometry\n";
        return false;
    }
    return true;
}
}

int main()
{
    return verify(800, 600) &&
           verify(1920, 1080) &&
           verify(3440, 1440)
        ? 0
        : 1;
}
