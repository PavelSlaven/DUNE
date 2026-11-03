#include "UnitDrawRecorder.hpp"
#include "UnitFrameBaseline.hpp"
#include "UnitFrameFixture.hpp"

#include "utils/cSoundPlayer.h"
#include "utils/cTimeCounter.h"
#include "utils/cTimeManager.h"
#include "context/GameContext.hpp"
#include "context/TextContext.hpp"
#include "controls/cGameControlsContext.h"
#include "controls/cMouse.h"
#include "data/gfxdata.h"
#include "d2tmc.h"
#include "drawers/cTextDrawer.h"
#include "map/cMapCamera.h"
#include "player/cPlayer.h"

#include <cmath>
#include <format>
#include <iostream>
#include <stdexcept>

namespace {
void require(bool condition, const std::string &message)
{
    if (!condition) throw std::runtime_error(message);
}

void requireRect(const cRectangle &actual, const cRectangle &expected, const std::string &label)
{
    require(actual.getX() == expected.getX() && actual.getY() == expected.getY() &&
                actual.getWidth() == expected.getWidth() && actual.getHeight() == expected.getHeight(),
            std::format("{}: expected ({},{},{},{}), got ({},{},{},{})",
                        label, expected.getX(), expected.getY(), expected.getWidth(), expected.getHeight(),
                        actual.getX(), actual.getY(), actual.getWidth(), actual.getHeight()));
}

void verifyVisualMatrix(UnitFrameFixture &fixture)
{
    for (const UnitFrameBaseline &baseline : UnitFrameBaselines) {
        for (const int density : {1, 4}) {
            for (const float zoom : UnitFrameZoomLevels) {
                for (const float selectedScale : UnitFrameWorldScales) {
                    fixture.setDisplaySettings(density, static_cast<int>(std::lround(selectedScale * 100.0F)));
                    fixture.setCamera(zoom, 32.0F, 48.0F);
                    fixture.setUnit(0, baseline.type, 256, 288, 0, 0, 0);
                    const cRectangle expected = unitFrameExpectedVisual(
                        256, 288, 32, 48, 40,
                        baseline.width, baseline.height, zoom
                    );
                    requireRect(unit[0].getVisualRectangle(), expected,
                                std::format("{} density={} zoom={} scale={}",
                                            baseline.name, density, zoom, selectedScale));
                }
            }
        }
    }
}

void verifyHealthGroupAndExperience(UnitFrameFixture &fixture)
{
    constexpr int fixtureMaxHp = 100;
    constexpr int fixtureHitPoints = 50;
    constexpr int fixtureCreditCapacity = 100;
    for (const UnitFrameBaseline &baseline : UnitFrameBaselines) {
        sUnitInfo[baseline.type].hp = fixtureMaxHp;
        if (baseline.type == HARVESTER) {
            sUnitInfo[HARVESTER].credit_capacity = fixtureCreditCapacity;
        }
        for (const int density : {1, 4}) {
            for (const float zoom : UnitFrameZoomLevels) {
                for (const float selectedScale : UnitFrameWorldScales) {
                    fixture.setDisplaySettings(
                        density,
                        static_cast<int>(std::lround(selectedScale * 100.0F))
                    );
                    fixture.setCamera(zoom, 32.0F, 48.0F);
                    fixture.setUnit(0, baseline.type, 256, 288, 0, 0, 0);
                    fixture.setUnitFlags(0, true, true);
                    unit[0].iHitPoints = fixtureHitPoints;
                    unit[0].iGroup = 3;
                    unit[0].fExperience = 2.0F;
                    if (baseline.type == HARVESTER) {
                        unit[0].iCredits = fixtureCreditCapacity / 2;
                    }
                    const cRectangle visual = unitFrameExpectedVisual(
                        256, 288, 32, 48, 40,
                        baseline.width, baseline.height, zoom
                    );
                    const int barHeight = std::max(
                        1,
                        static_cast<int>(std::lround(4.0F * zoom))
                    );
                    const float healthRatio = static_cast<float>(fixtureHitPoints) /
                        static_cast<float>(fixtureMaxHp);
                    const int healthWidth = static_cast<int>(healthRatio * visual.getWidth());
                    const int healthRed = static_cast<int>((1.1F - healthRatio) * 255.0F);
                    const int healthGreen = static_cast<int>(healthRatio * 255.0F);

                    clearUnitDrawCalls();
                    unit[0].draw_health();
                    require(unitDrawCalls().size() == (barHeight > 2 ? 3U : 2U),
                            std::format("{} health call count changed", baseline.name));
                    require(unitDrawCalls()[0].method == "renderRectFillColor" &&
                                unitDrawCalls()[0].x == visual.getX() &&
                                unitDrawCalls()[0].y == visual.getY() - (barHeight + 2) &&
                                unitDrawCalls()[0].width == visual.getWidth() &&
                                unitDrawCalls()[0].height == barHeight &&
                                unitDrawCalls()[0].color.r == 0 && unitDrawCalls()[0].color.g == 0 &&
                                unitDrawCalls()[0].opacity == UnitFrameShadowOpacity,
                            std::format("{} health background moved from its visual rectangle", baseline.name));
                    require(unitDrawCalls()[1].method == "renderRectFillColor",
                            std::format("{} health fill method changed", baseline.name));
                    requireRect(unitDrawCalls()[1].destination,
                                {visual.getX(), visual.getY() - (barHeight + 2), healthWidth - 1, barHeight},
                                std::format("{} health fill rectangle", baseline.name));
                    require(unitDrawCalls()[1].color.r == healthRed &&
                                unitDrawCalls()[1].color.g == healthGreen &&
                                unitDrawCalls()[1].color.b == 32 &&
                                unitDrawCalls()[1].opacity == UnitFrameShadowOpacity,
                            std::format("{} health fill changed from its baseline formula", baseline.name));
                    if (barHeight > 2) {
                        require(unitDrawCalls()[2].method == "renderRectColor",
                                std::format("{} health outline method changed", baseline.name));
                        requireRect(unitDrawCalls()[2].destination,
                                    {visual.getX(), visual.getY() - (barHeight + 2),
                                     visual.getWidth(), barHeight},
                                    std::format("{} health outline rectangle", baseline.name));
                        require(unitDrawCalls()[2].color.r == 255 &&
                                    unitDrawCalls()[2].color.g == 255 &&
                                    unitDrawCalls()[2].color.b == 255 &&
                                    unitDrawCalls()[2].opacity == UnitFrameShadowOpacity,
                                std::format("{} health outline color or opacity changed", baseline.name));
                    }

                    cTextDrawer textDrawer(nullptr);
                    clearUnitRecordedText();
                    unit[0].draw_group(&textDrawer);
                    require(unitRecordedText().size() == 2,
                            std::format("{} group number must draw black and white text", baseline.name));
                    const int groupX = visual.getX() + std::max(3, visual.getWidth() - 8);
                    const int groupY = visual.getY() - (barHeight + 2) - 11;
                    require(unitRecordedText()[0].x == groupX && unitRecordedText()[0].y == groupY &&
                                unitRecordedText()[0].text == "3" &&
                                unitRecordedText()[0].color.r == 0 && unitRecordedText()[0].color.g == 0 &&
                                unitRecordedText()[0].color.b == 0 && unitRecordedText()[0].color.a == 255 &&
                                unitRecordedText()[1].x == groupX && unitRecordedText()[1].y == groupY - 1 &&
                                unitRecordedText()[1].text == "3" &&
                                unitRecordedText()[1].color.r == 255 && unitRecordedText()[1].color.g == 255 &&
                                unitRecordedText()[1].color.b == 255 && unitRecordedText()[1].color.a == 255,
                            std::format("{} group text moved from its visual rectangle", baseline.name));

                    clearUnitDrawCalls();
                    unit[0].draw_experience();
                    require(unitDrawCalls().size() == 2,
                            std::format("{} must draw two experience stars", baseline.name));
                    require(unitDrawCalls()[0].texture == gfxdata->getTexture(OBJECT_STAR_01) &&
                                unitDrawCalls()[0].method == "renderSprite" &&
                                unitDrawCalls()[0].opacity == UnitFrameShadowOpacity &&
                                unitDrawCalls()[0].x == visual.getX() + 3 &&
                                unitDrawCalls()[0].y == visual.getY() - 19 &&
                                unitDrawCalls()[1].texture == gfxdata->getTexture(OBJECT_STAR_01) &&
                                unitDrawCalls()[1].method == "renderSprite" &&
                                unitDrawCalls()[1].opacity == UnitFrameShadowOpacity &&
                                unitDrawCalls()[1].x == visual.getX() + 12 &&
                                unitDrawCalls()[1].y == visual.getY() - 19,
                            std::format("{} experience stars moved from their baseline coordinates", baseline.name));

                    if (baseline.type == HARVESTER) {
                        const int spiceWidth = static_cast<int>(
                            (static_cast<float>(fixtureCreditCapacity / 2) /
                             static_cast<float>(fixtureCreditCapacity)) * visual.getWidth()
                        );
                        clearUnitDrawCalls();
                        unit[0].draw_spice();
                        require(unitDrawCalls().size() == (barHeight > 2 ? 3U : 2U),
                                "Harvester spice bar call count changed");
                        const int spiceY = visual.getY() - ((barHeight * 2) + 2);
                        require(unitDrawCalls()[0].method == "renderRectFillColor",
                                "Harvester spice background method changed");
                        requireRect(unitDrawCalls()[0].destination,
                                    {visual.getX(), spiceY, visual.getWidth(), barHeight},
                                    "Harvester spice background rectangle");
                        require(unitDrawCalls()[1].method == "renderRectFillColor",
                                "Harvester spice fill method changed");
                        requireRect(unitDrawCalls()[1].destination,
                                    {visual.getX(), spiceY, spiceWidth, barHeight},
                                    "Harvester spice fill rectangle");
                        require(unitDrawCalls()[1].color.r == 255 &&
                                    unitDrawCalls()[1].color.g == 91 &&
                                    unitDrawCalls()[1].color.b == 1 &&
                                    unitDrawCalls()[1].opacity == UnitFrameShadowOpacity,
                                "Harvester spice bar no longer follows the visual rectangle");
                        if (barHeight > 2) {
                            require(unitDrawCalls()[2].method == "renderRectColor",
                                    "Harvester spice outline method changed");
                            requireRect(unitDrawCalls()[2].destination,
                                        {visual.getX(), spiceY, visual.getWidth(), barHeight},
                                        "Harvester spice outline rectangle");
                            require(unitDrawCalls()[2].color.r == 255 &&
                                        unitDrawCalls()[2].color.g == 255 &&
                                        unitDrawCalls()[2].color.b == 255 &&
                                        unitDrawCalls()[2].opacity == UnitFrameShadowOpacity,
                                    "Harvester spice outline color or opacity changed");
                        }
                    }
                }
            }
        }
    }
}

void verifyClickAndBandSelection(UnitFrameFixture &fixture)
{
    std::unique_ptr<cTextDrawer> text1 = std::make_unique<cTextDrawer>(nullptr);
    std::unique_ptr<cTextDrawer> text2 = std::make_unique<cTextDrawer>(nullptr);
    std::unique_ptr<cTextDrawer> text3 = std::make_unique<cTextDrawer>(nullptr);
    std::unique_ptr<cTextDrawer> text4 = std::make_unique<cTextDrawer>(nullptr);
    std::unique_ptr<cTextDrawer> text5 = std::make_unique<cTextDrawer>(nullptr);
    std::unique_ptr<cTextDrawer> text6 = std::make_unique<cTextDrawer>(nullptr);
    GameContext gameContext;
    gameContext.setTextContext(std::make_unique<TextContext>(
        std::move(text1), std::move(text2), std::move(text3),
        std::move(text4), std::move(text5), std::move(text6)
    ));
    cMouse mouse(&gameContext);
    cGameControlsContext controls(&players[HUMAN], &mouse);
    for (const float zoom : UnitFrameZoomLevels) {
        for (const float selectedScale : UnitFrameWorldScales) {
            fixture.setDisplaySettings(4, static_cast<int>(std::lround(selectedScale * 100.0F)));
            fixture.setCamera(zoom);
            fixture.setUnit(0, SIEGETANK, 256, 256, 0, 0, 0);
            unit[0].thinkFast_position();

            const cRectangle visual = unitFrameExpectedVisual(
                256, 256, 0, 0, 40, 36, 36, zoom
            );
            const int artSize = static_cast<int>(std::lround(44.0F * zoom));
            const cRectangle expectedHdArt(
                visual.getX() - (artSize - visual.getWidth()) / 2,
                visual.getY() - (artSize - visual.getHeight()) / 2,
                artSize,
                artSize
            );
            require(artSize >= visual.getWidth() + 6 && artSize >= visual.getHeight() + 6,
                    "The 44-pixel art must overhang the logical visual rectangle by at least three pixels");
            cRectangle negativeBand(visual.getX() - 3, visual.getY() + 1, 2, 2);
            require(negativeBand.getX() >= expectedHdArt.getX() &&
                        negativeBand.getY() >= expectedHdArt.getY() &&
                        negativeBand.getX() + negativeBand.getWidth() <= expectedHdArt.getX() + expectedHdArt.getWidth() &&
                        negativeBand.getY() + negativeBand.getHeight() <= expectedHdArt.getY() + expectedHdArt.getHeight(),
                    "The negative band must lie inside the expected 44-pixel HD art overhang");
            require(!unit[0].isWithinViewport(&negativeBand),
                    "Viewport clipping must use the logical visual rectangle, not the HD artwork");
            require(players[HUMAN].getAllMyUnitsWithinViewportRect(negativeBand).empty(),
                    "A band touching only the sprite edge must not select the unit");

            const int centerX = static_cast<int>(std::round((256 + 16) * zoom));
            const int centerY = static_cast<int>(std::round((256 + 16) * zoom + 40));
            const cRectangle centerBand(centerX - 1, centerY - 1, 2, 2);
            const std::vector<int> selected = players[HUMAN].getAllMyUnitsWithinViewportRect(centerBand);
            require(selected.size() == 1 && selected[0] == 0,
                    "A band containing the independently calculated unit center must select it");

            controls.m_mouseCell = unit[0].iCell;
            controls.determineHoveringOverUnitId();
            require(controls.getIdOfUnitWhereMouseHovers() == 0,
                    "The actual map-cell hover algorithm must find the unit in its occupied cell");
            const int clickX = static_cast<int>(std::ceil((256 + 32) * zoom)) + 1;
            const int clickY = static_cast<int>(std::round((256 + 16) * zoom + 40));
            require(clickX >= expectedHdArt.getX() && clickX < expectedHdArt.getX() + expectedHdArt.getWidth() &&
                        clickY >= expectedHdArt.getY() && clickY < expectedHdArt.getY() + expectedHdArt.getHeight(),
                    "The adjacent-cell click must lie inside the expected 44-pixel HD art destination");
            const int overhangCell = controls.getMouseCellFromScreen(clickX, clickY);
            require(overhangCell >= 0 && overhangCell != unit[0].iCell,
                    "The computed screen point must map outside the unit's occupied map cell");
            controls.m_mouseCell = overhangCell;
            global_map.setVisibleFor(overhangCell, HUMAN);
            controls.determineHoveringOverUnitId();
            require(controls.getIdOfUnitWhereMouseHovers() == -1,
                    "The adjacent cell must not select the sprite's visual overhang");
            unit[0].iTempHitPoints = 1;
            controls.m_mouseCell = unit[0].iCell;
            controls.determineHoveringOverUnitId();
            require(controls.getIdOfUnitWhereMouseHovers() == -1,
                    "A hidden unit must remain absent from cell hover selection");
        }
    }
}

void verifyDebugPath(UnitFrameFixture &fixture)
{
    for (const int density : {1, 4}) {
        for (const float zoom : UnitFrameZoomLevels) {
            for (const float selectedScale : UnitFrameWorldScales) {
                fixture.setDisplaySettings(density, static_cast<int>(std::lround(selectedScale * 100.0F)));
                fixture.setCamera(zoom, 16.0F, 24.0F);
                fixture.setUnit(0, SIEGETANK, 256, 256);
                unit[0].iCell = 5;
                unit[0].iGoalCell = 11 * 64 + 11;
                unit[0].iPath[0] = 10 * 64 + 10;
                unit[0].iPath[1] = 10 * 64 + 11;
                unit[0].iPath[2] = 11 * 64 + 11;
                unit[0].iPathIndex = 1;
                clearUnitDrawCalls();
                unit[0].draw_path();
                require(unitDrawCalls().size() == 2, "Debug path must draw the two configured segments");

                const auto screenPoint = [zoom](int cellX, int cellY) {
                    return std::pair{
                        static_cast<int>(std::round(zoom * (cellX * 32 + 16 - 16))),
                        static_cast<int>(std::round(zoom * (cellY * 32 + 16 - 24) + 40))
                    };
                };
                const auto [x0, y0] = screenPoint(10, 10);
                const auto [x1, y1] = screenPoint(11, 10);
                const auto [x2, y2] = screenPoint(11, 11);
                require(unitDrawCalls()[0].x == x0 && unitDrawCalls()[0].y == y0 &&
                            unitDrawCalls()[0].width == x1 && unitDrawCalls()[0].height == y1 &&
                            unitDrawCalls()[0].color.r == 255 && unitDrawCalls()[0].color.g == 255,
                        "Debug path's current segment must retain its cell-center coordinates");
                require(unitDrawCalls()[1].x == x1 && unitDrawCalls()[1].y == y1 &&
                            unitDrawCalls()[1].width == x2 && unitDrawCalls()[1].height == y2 &&
                            unitDrawCalls()[1].color.r == 255 && unitDrawCalls()[1].color.g == 0,
                        "Debug path's goal segment must retain its cell-center coordinates");
            }
        }
    }
}

void runInteractions()
{
    UnitFrameFixture fixture(4, 100);
    verifyVisualMatrix(fixture);
    verifyHealthGroupAndExperience(fixture);
    verifyClickAndBandSelection(fixture);
    verifyDebugPath(fixture);
}
}

int main()
{
    try {
        runInteractions();
        std::cout << "unit_frame_interactions: all checks passed\n";
    }
    catch (const std::exception &error) {
        std::cerr << "unit_frame_interactions: " << error.what() << '\n';
        return 1;
    }
    return 0;
}
