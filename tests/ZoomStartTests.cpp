#include "ZoomTestSupport.hpp"

#include <iostream>

using namespace zoomtest;

namespace {
constexpr float ZoomTolerance = 1e-4F;
constexpr float ZoomStep = 0.1F;

void requireZoom(float actual, float expected, const std::string &label)
{
    require(std::fabs(actual - expected) < ZoomTolerance,
            std::format("{}: expected zoom {}, got {}", label, expected, actual));
}

void replaceCamera()
{
    delete mapCamera;
    mapCamera = new cMapCamera(&global_map, 0.0F, 0.0F, false);
}

void checkStartZoom(UnitFrameFixture &fixture, int density, int percent, float expectedZoom)
{
    fixture.setDisplaySettings(density, percent);
    const std::string label = std::format("density {} scale {}%", density, percent);

    replaceCamera();
    requireZoom(mapCamera->getZoomLevel(), expectedZoom, label + " new camera");

    mapCamera->m_zoomLevel = 2.3F;
    mapCamera->resetZoom();
    requireZoom(mapCamera->getZoomLevel(), expectedZoom, label + " after resetZoom");
}

void checkZoomSteps(UnitFrameFixture &fixture, int percent)
{
    fixture.setDisplaySettings(4, percent);
    const float start = percent / 100.0F;
    const std::string label = std::format("scale {}%", percent);

    replaceCamera();
    mapCamera->m_zoomLevel = start;
    mapCamera->zoomIn();
    requireZoom(mapCamera->getZoomLevel(), start + ZoomStep, label + " zoomIn");

    mapCamera->m_zoomLevel = start;
    mapCamera->zoomOut();
    requireZoom(mapCamera->getZoomLevel(), start - ZoomStep, label + " zoomOut");
}

void checkZoomLimits(UnitFrameFixture &fixture)
{
    fixture.setDisplaySettings(4, 100);
    replaceCamera();

    mapCamera->m_zoomLevel = 4.0F;
    mapCamera->zoomIn();
    requireZoom(mapCamera->getZoomLevel(), 4.0F, "zoomIn at the upper limit");

    mapCamera->m_zoomLevel = 0.25F;
    mapCamera->zoomOut();
    requireZoom(mapCamera->getZoomLevel(), 0.25F, "zoomOut at the lower limit");
}

void runZoomStartChecks()
{
    UnitFrameFixture fixture(4, 100);
    InputRig rig;
    rig.setMousePosition(400, 300);

    for (const int percent : {100, 110, 125, 150}) {
        checkStartZoom(fixture, 4, percent, percent / 100.0F);
    }

    for (const int percent : {100, 110, 125, 150}) {
        checkZoomSteps(fixture, percent);
    }
    checkZoomLimits(fixture);
}
}

int main()
{
    try {
        runZoomStartChecks();
        std::cout << "zoom_start: all checks passed\n";
    }
    catch (const std::exception &error) {
        std::cerr << "zoom_start: " << error.what() << '\n';
        return 1;
    }
    return 0;
}
