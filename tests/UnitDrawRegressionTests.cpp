#include "UnitDrawRecorder.hpp"
#include "UnitFrameBaseline.hpp"
#include "UnitFrameFixture.hpp"

#include "d2tmc.h"
#include "data/gfxdata.h"
#include "map/cMapCamera.h"
#include "player/cPlayer.h"

#include <format>
#include <iostream>
#include <stdexcept>
#include <vector>

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

void appendSprite(
    std::vector<UnitDrawCall> &expected,
    std::string method,
    Texture *texture,
    cRectangle source,
    cRectangle destination,
    Uint8 opacity = 255)
{
    UnitDrawCall call;
    call.method = std::move(method);
    call.texture = texture;
    call.source = source;
    call.destination = destination;
    call.x = destination.getX();
    call.y = destination.getY();
    call.width = destination.getWidth();
    call.height = destination.getHeight();
    call.opacity = opacity;
    expected.push_back(call);
}

void appendIcon(
    std::vector<UnitDrawCall> &expected,
    const std::string &method,
    Texture *texture,
    int x,
    int y,
    const cRectangle *destination = nullptr)
{
    UnitDrawCall call;
    call.method = method;
    call.texture = texture;
    call.x = x;
    call.y = y;
    if (destination) {
        call.destination = *destination;
        call.width = destination->getWidth();
        call.height = destination->getHeight();
    }
    expected.push_back(call);
}

void verifyCalls(const std::vector<UnitDrawCall> &expected, const std::string &label)
{
    const auto &actual = unitDrawCalls();
    require(actual.size() == expected.size(),
            std::format("{}: expected {} ordered calls, got {}", label, expected.size(), actual.size()));
    for (std::size_t index = 0; index < expected.size(); ++index) {
        const UnitDrawCall &wanted = expected[index];
        const UnitDrawCall &got = actual[index];
        require(got.method == wanted.method,
                std::format("{} call {}: expected {}, got {}", label, index, wanted.method, got.method));
        require(got.texture == wanted.texture,
                std::format("{} call {} has a different texture pointer", label, index));
        require(got.opacity == wanted.opacity && got.blendMode == wanted.blendMode,
                std::format("{} call {} changed opacity or blend mode", label, index));
        if (wanted.method == "renderStrechSprite") {
            requireRect(got.source, wanted.source, std::format("{} source {}", label, index));
            requireRect(got.destination, wanted.destination, std::format("{} destination {}", label, index));
            require(got.opacity == wanted.opacity && got.blendMode == SDL_BLENDMODE_BLEND,
                    std::format("{} call {} changed opacity or blend mode", label, index));
        }
        else if (wanted.method == "renderStrechFullSprite") {
            requireRect(got.destination, wanted.destination, std::format("{} overlay {}", label, index));
        }
        else {
            require(got.x == wanted.x && got.y == wanted.y,
                    std::format("{} call {} has a different icon position", label, index));
        }
    }
}

void checkBaselineCase(
    UnitFrameFixture &fixture,
    const UnitFrameBaseline &baseline,
    int density,
    float zoom,
    float selectedScale,
    int bodyAngle,
    int turretAngle,
    int animationFrame)
{
    fixture.setDisplaySettings(density, static_cast<int>(std::lround(selectedScale * 100.0F)));
    fixture.setCamera(zoom);
    fixture.setUnit(0, baseline.type, 256, 288, bodyAngle, turretAngle, animationFrame);
    fixture.setUnitFlags(0, true, true);
    clearUnitDrawCalls();
    unit[0].draw();

    if (baseline.type == SANDWORM) {
        verifyCalls({}, "SANDWORM emits no draw calls");
        return;
    }

    const cRectangle visual = unitFrameExpectedVisual(
        256, 288, 0, 0, 40, baseline.width, baseline.height, zoom
    );
    const int bodyFacing = unitFrameFacingIndex(bodyAngle);
    const int turretFacing = unitFrameFacingIndex(turretAngle);
    const cRectangle sourceBody = {
        bodyFacing * baseline.width,
        animationFrame * baseline.height,
        baseline.width,
        baseline.height
    };
    std::vector<UnitDrawCall> expected;
    if (baseline.hasShadow) {
        cRectangle shadowDestination = visual;
        if (baseline.type == CARRYALL) {
            shadowDestination = {visual.getX(), visual.getY() + 24, visual.getWidth(), visual.getHeight()};
        }
        appendSprite(expected, "renderStrechSprite", fixture.shadowTexture(baseline.type),
                     sourceBody, shadowDestination, UnitFrameShadowOpacity);
    }
    if (baseline.hasBody) {
        appendSprite(expected, "renderStrechSprite", fixture.bodyTexture(baseline.type),
                     sourceBody, visual);
    }
    if (baseline.hasTurret) {
        const cRectangle sourceTurret = {
            turretFacing * baseline.width,
            animationFrame * baseline.height,
            baseline.width,
            baseline.height
        };
        appendSprite(expected, "renderStrechSprite", fixture.turretTexture(baseline.type),
                     sourceTurret, visual);
    }
    appendIcon(expected, "renderSprite", gfxdata->getTexture(SYMB_PICKMEUP),
               visual.getX(), visual.getY() - 7);
    appendIcon(expected, "renderStrechFullSprite", gfxdata->getTexture(FOCUS),
               visual.getX(), visual.getY(), &visual);
    verifyCalls(expected, std::format("{} density={} zoom={} scale={} body={} turret={} frame={}",
                                      baseline.name, density, zoom, selectedScale,
                                      bodyAngle, turretAngle, animationFrame));
}

void checkVisibilityAndMissingLayers(UnitFrameFixture &fixture)
{
    fixture.setDisplaySettings(1, 100);
    fixture.setCamera(1.0F);
    fixture.setUnit(0, TANK, 256, 288, 1, 6, 0);
    fixture.setUnitFlags(0, false, false);
    unit[0].iHitPoints = -1;
    clearUnitDrawCalls();
    unit[0].draw();
    require(unitDrawCalls().size() == 2, "A tank without hit points must omit only its turret");
    require(unitDrawCalls()[0].method == "renderStrechSprite" &&
                unitDrawCalls()[1].method == "renderStrechSprite",
            "The shadow and body must remain ordered when hit points are negative");

    fixture.setUnit(0, SIEGETANK, 256, 288);
    fixture.setUnitFlags(0, false, false);
    Texture *savedBody = players[HUMAN].bmp_unit[SIEGETANK];
    players[HUMAN].bmp_unit[SIEGETANK] = nullptr;
    clearUnitDrawCalls();
    unit[0].draw();
    require(unitDrawCalls().size() == 2,
            "A missing body bitmap must not add a body call or suppress shadow and turret");
    players[HUMAN].bmp_unit[SIEGETANK] = savedBody;

    unit[0].iTempHitPoints = 1;
    clearUnitDrawCalls();
    unit[0].draw();
    require(unitDrawCalls().empty(), "A hidden unit must produce no drawing calls");

    fixture.setUnit(0, SANDWORM, 256, 288);
    clearUnitDrawCalls();
    unit[0].draw();
    require(unitDrawCalls().empty(), "A sandworm must produce no drawing calls");
}

void runRegressionMatrix()
{
    UnitFrameFixture fixture(4, 100);
    for (const UnitFrameBaseline &baseline : UnitFrameBaselines) {
        for (const int density : {1, 4}) {
            if (baseline.type == SIEGETANK && density == 4) continue;
            for (const float zoom : UnitFrameZoomLevels) {
                for (const float selectedScale : UnitFrameWorldScales) {
                    for (int bodyAngle = 0; bodyAngle < 8; ++bodyAngle) {
                        for (int turretAngle = 0; turretAngle < 8; ++turretAngle) {
                            for (const int animationFrame : unitFrameAnimationRows(baseline.animationFrames)) {
                                checkBaselineCase(
                                    fixture,
                                    baseline,
                                    density,
                                    zoom,
                                    selectedScale,
                                    bodyAngle,
                                    turretAngle,
                                    animationFrame
                                );
                            }
                        }
                    }
                }
            }
        }
    }
    checkVisibilityAndMissingLayers(fixture);
}
}

int main()
{
    try {
        runRegressionMatrix();
        std::cout << "unit_draw_regression: all checks passed\n";
    }
    catch (const std::exception &error) {
        std::cerr << "unit_draw_regression: " << error.what() << '\n';
        return 1;
    }
    return 0;
}
