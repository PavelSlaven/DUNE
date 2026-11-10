#include <catch2/catch_test_macros.hpp>

#include "sidebar/HudLayout.hpp"

#include <algorithm>

namespace {
void verifyHdLayout(int width, int height, int expectedSidebar, int expectedColumns)
{
    const HudLayout layout = HudLayout::create(width, height);
    CHECK(layout.sidebarWidth == expectedSidebar);
    CHECK(layout.columns == expectedColumns);
    CHECK(layout.sidebar.getX() == width - expectedSidebar);
    CHECK(layout.credits.getEndX() <= width);
    CHECK(layout.catalog.getEndY() <= height);
    CHECK(layout.cardWidth >= 99);
    CHECK(layout.cardHeight > 100);

    for (int i = 0; i < expectedColumns; ++i) {
        const cRectangle card = layout.cardRect(i, 0);
        CHECK(card.getX() >= layout.cards.getX());
        CHECK(card.getEndX() <= layout.cards.getEndX());
        CHECK(card.getY() >= layout.cards.getY());
    }

    const int maxScroll = layout.maxScrollRow(18);
    CHECK(maxScroll >= 0);
    const cRectangle lastVisible =
        layout.cardRect(17, maxScroll);
    CHECK(lastVisible.getEndY() <= layout.cards.getEndY());

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
    CHECK(!price.isOverlapping(footprint));
}


bool inside(const cRectangle &inner, const cRectangle &outer)
{
    return inner.getX() >= outer.getX() && inner.getEndX() <= outer.getEndX() &&
           inner.getY() >= outer.getY() && inner.getEndY() <= outer.getEndY();
}

bool sameRect(const cRectangle &rect, int x, int y, int width, int height)
{
    return rect.getX() == x && rect.getY() == y && rect.getWidth() == width && rect.getHeight() == height;
}
}

TEST_CASE("P5C hud layout keeps the fork examples", "[P5C]")
{
    verifyHdLayout(800, 600, 280, 2);
    verifyHdLayout(1067, 600, 360, 3);
    verifyHdLayout(1280, 720, 360, 3);
    verifyHdLayout(1920, 1080, 360, 3);
}

TEST_CASE("P5C hud layout fits every canvas", "[P5C]")
{
    int cases = 0;
    int sidebarFailures = 0;
    int topFailures = 0;
    int panelFailures = 0;
    int orderFailures = 0;
    int radarFailures = 0;
    int catalogFailures = 0;
    int cardSizeFailures = 0;
    for (int width = 800; width <= 3840; ++width) {
        for (int height = 600; height <= 2160; ++height) {
            ++cases;
            const HudLayout layout = HudLayout::create(width, height);
            const int expectedSidebar = width < 960 ? 280 : 360;
            const int expectedColumns = width < 960 ? 2 : 3;
            if (layout.sidebarWidth != expectedSidebar || layout.columns != expectedColumns ||
                !sameRect(layout.sidebar, width - expectedSidebar, 0, expectedSidebar, height)) {
                ++sidebarFailures;
            }
            if (!sameRect(layout.topBar, 0, 0, width, HudLayout::TopBarHeight) ||
                !sameRect(layout.battlefield, 0, HudLayout::TopBarHeight, width - expectedSidebar,
                          height - HudLayout::TopBarHeight)) {
                ++topFailures;
            }
            if (!inside(layout.credits, layout.sidebar) || !inside(layout.radarPanel, layout.sidebar) ||
                !inside(layout.tabs, layout.sidebar) || !inside(layout.catalog, layout.sidebar)) {
                ++panelFailures;
            }
            if (layout.credits.getEndY() > layout.radarPanel.getY() ||
                layout.radarPanel.getEndY() > layout.tabs.getY() ||
                layout.tabs.getEndY() > layout.catalog.getY()) {
                ++orderFailures;
            }
            if (!inside(layout.houseHeader, layout.radarPanel) || !inside(layout.radarViewport, layout.radarPanel) ||
                !inside(layout.powerMeter, layout.radarPanel) || !inside(layout.spiceMeter, layout.radarPanel) ||
                layout.houseHeader.getEndY() > layout.radarViewport.getY() ||
                layout.radarViewport.getEndY() > layout.powerMeter.getY() ||
                layout.powerMeter.getY() != layout.spiceMeter.getY() ||
                layout.powerMeter.getEndX() > layout.spiceMeter.getX()) {
                ++radarFailures;
            }
            if (!inside(layout.cards, layout.catalog) || !inside(layout.scrollbar, layout.catalog) ||
                layout.cards.getEndX() > layout.scrollbar.getX()) {
                ++catalogFailures;
            }
            if (layout.cardWidth < 99 || layout.cardHeight <= 100) {
                ++cardSizeFailures;
            }
        }
    }
    CHECK(cases == 4747001);
    CHECK(sidebarFailures == 0);
    CHECK(topFailures == 0);
    CHECK(panelFailures == 0);
    CHECK(orderFailures == 0);
    CHECK(radarFailures == 0);
    CHECK(catalogFailures == 0);
    CHECK(cardSizeFailures == 0);
}

TEST_CASE("P5C hud layout keeps visible cards and the scrollbar thumb inside the catalog", "[P5C]")
{
    int cases = 0;
    int cardFailures = 0;
    int columnOrderFailures = 0;
    int rowOrderFailures = 0;
    int thumbFailures = 0;
    int thumbEndFailures = 0;
    for (const int width : {800, 959, 960, 3840}) {
        for (int height = 600; height <= 2160; ++height) {
            const HudLayout layout = HudLayout::create(width, height);
            for (int itemCount = 0; itemCount <= 40; ++itemCount) {
                const int maxScroll = layout.maxScrollRow(itemCount);
                for (int scrollRow = 0; scrollRow <= maxScroll; ++scrollRow) {
                    ++cases;
                    const int first = scrollRow * layout.columns;
                    const int last = std::min(itemCount, (scrollRow + layout.visibleRows()) * layout.columns);
                    for (int item = first; item < last; ++item) {
                        const cRectangle card = layout.cardRect(item, scrollRow);
                        if (!inside(card, layout.cards)) {
                            ++cardFailures;
                        }
                        if (item + 1 < last && (item + 1) % layout.columns != 0 &&
                            card.getEndX() > layout.cardRect(item + 1, scrollRow).getX()) {
                            ++columnOrderFailures;
                        }
                        if (item + layout.columns < last &&
                            card.getEndY() > layout.cardRect(item + layout.columns, scrollRow).getY()) {
                            ++rowOrderFailures;
                        }
                    }
                    const cRectangle thumb = layout.scrollbarThumb(itemCount, scrollRow);
                    if (thumb.getX() != layout.scrollbar.getX() || thumb.getWidth() != layout.scrollbar.getWidth() ||
                        thumb.getY() < layout.scrollbar.getY() || thumb.getEndY() > layout.scrollbar.getEndY()) {
                        ++thumbFailures;
                    }
                    if (maxScroll == 0) {
                        if (!sameRect(thumb, layout.scrollbar.getX(), layout.scrollbar.getY(),
                                      layout.scrollbar.getWidth(), layout.scrollbar.getHeight())) {
                            ++thumbEndFailures;
                        }
                    } else if (thumb.getHeight() < 22 ||
                               (scrollRow == 0 && thumb.getY() != layout.scrollbar.getY()) ||
                               (scrollRow == maxScroll && thumb.getEndY() != layout.scrollbar.getEndY())) {
                        ++thumbEndFailures;
                    }
                }
            }
        }
    }
    CHECK(cases == 955624);
    CHECK(cardFailures == 0);
    CHECK(columnOrderFailures == 0);
    CHECK(rowOrderFailures == 0);
    CHECK(thumbFailures == 0);
    CHECK(thumbEndFailures == 0);
}

TEST_CASE("P5C hud layout splits the tab strip into six tabs", "[P5C]")
{
    for (const int width : {800, 960, 1920}) {
        const HudLayout layout = HudLayout::create(width, 720);
        CHECK(layout.tabRect(0).getX() == layout.tabs.getX());
        CHECK(layout.tabRect(5).getEndX() == layout.tabs.getEndX());
        for (int tab = 0; tab < 6; ++tab) {
            const cRectangle rect = layout.tabRect(tab);
            CHECK(rect.getY() == layout.tabs.getY());
            CHECK(rect.getHeight() == layout.tabs.getHeight());
            CHECK(rect.getWidth() > 0);
            if (tab < 5) {
                CHECK(rect.getEndX() == layout.tabRect(tab + 1).getX());
            }
        }
    }
}

TEST_CASE("P5C hud layout reserves the starport order area", "[P5C]")
{
    int cases = 0;
    int failures = 0;
    for (const int width : {800, 960}) {
        for (int height = 600; height <= 2160; ++height) {
            ++cases;
            if (HudLayout::create(width, height, true).catalog.getEndY() != height - 54 ||
                HudLayout::create(width, height, false).catalog.getEndY() != height - 6) {
                ++failures;
            }
        }
    }
    CHECK(cases == 3122);
    CHECK(failures == 0);
}
