#include "drawers/CommandBarLayout.hpp"

int main()
{
    constexpr int screenWidth = 800;
    constexpr int screenHeight = 600;
    constexpr int sidebarWidth = 280;
    constexpr int battlefieldWidth = screenWidth - sidebarWidth;

    const CommandBarLayout layout = CommandBarLayout::create(screenWidth, screenHeight, sidebarWidth);

    if (layout.panel.getWidth() >= battlefieldWidth) return 1;
    if (layout.panel.getEndY() >= screenHeight) return 2;
    if (layout.panel.isPointWithin(battlefieldWidth / 2, screenHeight - 1)) return 3;

    for (const cRectangle &button : layout.actions) {
        if (button.getWidth() <= 0 || button.getHeight() <= 0) return 4;
        if (!layout.panel.isPointWithin(button.getX(), button.getY())) return 5;
        if (!layout.panel.isPointWithin(button.getEndX() - 1, button.getEndY() - 1)) return 6;
    }

    const CommandBarLayout fullSizeLayout = CommandBarLayout::create(1920, 1080, sidebarWidth);
    if (fullSizeLayout.panel.getWidth() != 350 || fullSizeLayout.panel.getHeight() != 52) return 7;
    for (const cRectangle &button : fullSizeLayout.actions) {
        if (button.getWidth() != 50 || button.getHeight() != 52) return 8;
    }
    return 0;
}
