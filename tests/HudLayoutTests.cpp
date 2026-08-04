#include "sidebar/HudLayout.hpp"

#include <array>
#include <cassert>

namespace {
void verifyHdLayout(int width, int height, int expectedSidebar, int expectedColumns)
{
    const HudLayout layout = HudLayout::create(true, width, height);
    assert(layout.sidebarWidth == expectedSidebar);
    assert(layout.columns == expectedColumns);
    assert(layout.sidebar.getX() == width - expectedSidebar);
    assert(layout.credits.getEndX() <= width);
    assert(layout.catalog.getEndY() <= height);
    assert(layout.cardWidth >= 99);
    assert(layout.cardHeight > 100);

    for (int i = 0; i < expectedColumns; ++i) {
        const cRectangle card = layout.cardRect(i, 0);
        assert(card.getX() >= layout.cards.getX());
        assert(card.getEndX() <= layout.cards.getEndX());
        assert(card.getY() >= layout.cards.getY());
    }

    const int maxScroll = layout.maxScrollRow(18);
    assert(maxScroll >= 0);
    const cRectangle lastVisible =
        layout.cardRect(17, maxScroll);
    assert(lastVisible.getEndY() <= layout.cards.getEndY());

    const cRectangle price(
        layout.cardRect(0, 0).getX() + 3,
        layout.cardRect(0, 0).getY() + 3,
        45,
        16
    );
    const cRectangle footprint(
        layout.cardRect(0, 0).getEndX() - 22,
        layout.cardRect(0, 0).getY() + 3,
        19,
        19
    );
    assert(!price.isOverlapping(footprint));
}
}

int main()
{
    verifyHdLayout(800, 600, 280, 2);
    verifyHdLayout(1067, 600, 360, 3);
    verifyHdLayout(1280, 720, 360, 3);
    verifyHdLayout(1920, 1080, 360, 3);

    const HudLayout classic = HudLayout::create(false, 800, 600);
    assert(classic.sidebarWidth == 224);
    assert(classic.cardWidth == 63);
    assert(classic.cardHeight == 47);
    return 0;
}
