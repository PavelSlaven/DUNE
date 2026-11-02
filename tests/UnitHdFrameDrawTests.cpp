#include "UnitDrawRecorder.hpp"
#include "UnitFrameBaseline.hpp"
#include "UnitFrameFixture.hpp"
#include "utils/UnitSpriteLayout.hpp"

#include "d2tmc.h"
#include "data/gfxdata.h"
#include "map/cMapCamera.h"
#include "player/cPlayer.h"

#include <cmath>
#include <format>
#include <iostream>
#include <stdexcept>
#include <vector>

namespace {
struct HdFrameCase {
    int type;
    int logicalWidth;
    int logicalHeight;
    int atlasWidth;
    int atlasHeight;
    int animationFrames;
};

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

void requireFloatRect(const SDL_FRect &actual, const SDL_FRect &expected, const std::string &label)
{
    require(std::abs(actual.x - expected.x) < 0.0001F &&
                std::abs(actual.y - expected.y) < 0.0001F &&
                std::abs(actual.w - expected.w) < 0.0001F &&
                std::abs(actual.h - expected.h) < 0.0001F,
            std::format("{}: expected ({},{},{},{}), got ({},{},{},{})",
                        label, expected.x, expected.y, expected.w, expected.h,
                        actual.x, actual.y, actual.w, actual.h));
}

cRectangle expectedSource(int facing, int frame, int width, int height)
{
    return {facing * width, frame * height, width, height};
}

SDL_FRect expectedDestination(
    const cRectangle &visual,
    int logicalWidth,
    int logicalHeight,
    float zoom,
    float scale)
{
    const float width = static_cast<float>(std::lround(std::lround(logicalWidth * zoom) * scale));
    const float height = static_cast<float>(std::lround(std::lround(logicalHeight * zoom) * scale));
    return {
        visual.getX() + (visual.getWidth() - width) / 2.0F,
        visual.getY() + (visual.getHeight() - height) / 2.0F,
        width,
        height
    };
}

void checkOne(
    UnitFrameFixture &fixture,
    const HdFrameCase &testCase,
    float zoom,
    float selectedScale,
    int bodyAngle,
    int turretAngle,
    int animationFrame)
{
    fixture.setDisplaySettings(4, static_cast<int>(std::lround(selectedScale * 100.0F)));
    fixture.setCamera(zoom);
    fixture.setUnit(0, testCase.type, 256, 288, bodyAngle, turretAngle, animationFrame);
    fixture.setUnitFlags(0, true, true);
    clearUnitDrawCalls();
    unit[0].draw();

    const float effectiveScale = selectedScale;
    const UnitFrameBaseline *baseline = nullptr;
    for (const auto &candidate : UnitFrameBaselines) {
        if (candidate.type == testCase.type) {
            baseline = &candidate;
            break;
        }
    }
    require(baseline != nullptr, "HD draw case is absent from the independent baseline table");
    const cRectangle visual = unitFrameExpectedVisual(
        256, 288, 0, 0, 40,
        baseline->width, baseline->height, zoom, effectiveScale
    );
    const int body = unitFrameFacingIndex(bodyAngle);
    const int turret = unitFrameFacingIndex(turretAngle);
    const int logicalWidth = testCase.atlasWidth / 4;
    const int logicalHeight = testCase.atlasHeight / 4;
    std::vector<UnitDrawCall> expected;

    if (baseline->hasShadow) {
        UnitDrawCall call;
        call.method = "renderStrechSpriteF";
        call.texture = fixture.shadowTexture(testCase.type);
        call.source = expectedSource(body, animationFrame, logicalWidth, logicalHeight);
        call.floatDestination = expectedDestination(visual, logicalWidth, logicalHeight, zoom, effectiveScale);
        call.opacity = UnitFrameShadowOpacity;
        expected.push_back(call);
    }
    UnitDrawCall bodyCall;
    bodyCall.method = "renderStrechSpriteF";
    bodyCall.texture = fixture.bodyTexture(testCase.type);
    bodyCall.source = expectedSource(body, animationFrame, logicalWidth, logicalHeight);
    bodyCall.floatDestination = expectedDestination(visual, logicalWidth, logicalHeight, zoom, effectiveScale);
    expected.push_back(bodyCall);

    if (baseline->hasTurret) {
        UnitDrawCall topCall;
        topCall.method = "renderStrechSpriteF";
        topCall.texture = fixture.turretTexture(testCase.type);
        topCall.source = expectedSource(turret, animationFrame, logicalWidth, logicalHeight);
        topCall.floatDestination = expectedDestination(visual, logicalWidth, logicalHeight, zoom, effectiveScale);
        expected.push_back(topCall);
    }

    UnitDrawCall pickup;
    pickup.method = "renderSprite";
    pickup.texture = gfxdata->getTexture(SYMB_PICKMEUP);
    pickup.x = visual.getX();
    pickup.y = visual.getY() - 7;
    expected.push_back(pickup);
    UnitDrawCall focus;
    focus.method = "renderStrechFullSprite";
    focus.texture = gfxdata->getTexture(FOCUS);
    focus.destination = visual;
    expected.push_back(focus);

    const auto &actual = unitDrawCalls();
    require(actual.size() == expected.size(),
            std::format("{}: expected {} ordered calls, got {}", baseline->name, expected.size(), actual.size()));
    for (std::size_t index = 0; index < expected.size(); ++index) {
        const auto &wanted = expected[index];
        const auto &got = actual[index];
        require(got.method == wanted.method,
                std::format("{} call {}: expected {}, got {}", baseline->name, index, wanted.method, got.method));
        require(got.texture == wanted.texture,
                std::format("{} call {}: wrong texture identity", baseline->name, index));
        if (wanted.method == "renderStrechSpriteF") {
            requireRect(got.source, wanted.source, std::format("{} source {}", baseline->name, index));
            requireFloatRect(got.floatDestination, wanted.floatDestination,
                             std::format("{} fractional destination {}", baseline->name, index));
            require(got.opacity == wanted.opacity && got.blendMode == SDL_BLENDMODE_BLEND,
                    std::format("{} call {} changed opacity or blend mode", baseline->name, index));
        }
        else if (wanted.method == "renderStrechFullSprite") {
            requireRect(got.destination, wanted.destination, std::format("{} visual overlay", baseline->name));
        }
        else {
            require(got.x == wanted.x && got.y == wanted.y,
                    std::format("{} call {} has the wrong overlay position", baseline->name, index));
        }
    }
}

void runHdDrawMatrix()
{
    UnitFrameFixture fixture(4, 100);
    const HdFrameCase cases[] = {
        {SIEGETANK, 44, 44, 176, 176, 0},
        {TANK, 40, 40, 160, 160, 0},
        {HARVESTER, 88, 56, 352, 224, 4},
    };
    for (const HdFrameCase &testCase : cases) {
        sUnitInfo[testCase.type].hd_frame_width = testCase.atlasWidth;
        sUnitInfo[testCase.type].hd_frame_height = testCase.atlasHeight;
        for (const float zoom : UnitFrameZoomLevels) {
            for (const float scale : UnitFrameWorldScales) {
                for (int body = 0; body < 8; ++body) {
                    for (int turret = 0; turret < 8; ++turret) {
                        for (const int frame : unitFrameAnimationRows(testCase.animationFrames)) {
                            checkOne(fixture, testCase, zoom, scale, body, turret, frame);
                        }
                    }
                }
            }
        }
    }
}
}

int main()
{
    try {
        runHdDrawMatrix();
        std::cout << "unit_hd_frame_draw: all checks passed\n";
    }
    catch (const std::exception &error) {
        std::cerr << "unit_hd_frame_draw: " << error.what() << '\n';
        return 1;
    }
    return 0;
}

