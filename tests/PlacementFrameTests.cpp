#include "ZoomTestSupport.hpp"

#include "UnitDrawRecorder.hpp"

#include "drawers/cPlaceItDrawer.h"
#include "gameobjects/structures/cRefinery.h"
#include "gameobjects/structures/cWindTrap.h"
#include "sidebar/cBuildingListItem.h"

#include <iostream>
#include <memory>
#include <vector>

using namespace zoomtest;

namespace {
constexpr Uint8 PreviewFrameOpacity = 96;

struct BuildingCase {
    int type;
    int widthPixels;
    int heightPixels;
    const char *name;
};

constexpr BuildingCase BuildingCases[] = {
    {WINDTRAP, 64, 64, "windtrap 2x2"},
    {REFINERY, 96, 64, "refinery 3x2"},
};

std::unique_ptr<cAbstractStructure> makeStructure(int type, int cell)
{
    std::unique_ptr<cAbstractStructure> result;
    if (type == WINDTRAP) {
        result.reset(new cWindTrap());
    }
    else {
        result.reset(new cRefinery());
    }
    result->setOwner(HUMAN);
    result->setCell(cell);
    return result;
}

cRectangle recordPreviewFrame(InputRig &rig, const BuildingCase &building, int cell, const std::string &label)
{
    rig.controls().m_mouseCell = cell;
    cBuildingListItem item(building.type, sStructureInfo[building.type], 0);
    cPlaceItDrawer drawer(&players[HUMAN]);
    clearUnitDrawCalls();
    drawer.drawStructureIdAtMousePos(&item);

    std::vector<UnitDrawCall> frames;
    for (const UnitDrawCall &call : unitDrawCalls()) {
        if (call.method == "renderStrechSprite" && call.opacity == PreviewFrameOpacity) {
            frames.push_back(call);
        }
    }
    require(frames.size() == 1,
            std::format("{}: expected one preview frame, recorded {}", label, frames.size()));
    return frames.front().destination;
}

void checkPreviewFrame(InputRig &rig, const BuildingCase &building, int percent, float zoom, float viewportX,
                       float viewportY, int column, int row)
{
    sStructureInfo[building.type].bmp_width = building.widthPixels;
    sStructureInfo[building.type].bmp_height = building.heightPixels;
    useCamera(ScreenWidth, ScreenHeight, zoom, viewportX, viewportY);

    const int cell = row * MapCells + column;
    const std::string label = std::format("{} scale {}% zoom {} viewport ({},{}) cell ({},{})",
                                          building.name, percent, zoom, viewportX, viewportY, column, row);
    const cRectangle frame = recordPreviewFrame(rig, building, cell, label);

    const cRectangle expected = {
        mapCamera->getWindowXPosition(column * CellSize),
        mapCamera->getWindowYPosition(row * CellSize),
        static_cast<int>(std::lround(zoom * building.widthPixels)),
        static_cast<int>(std::lround(zoom * building.heightPixels))
    };
    requireRect(frame, expected, label + " preview frame");

    if (percent == 100) {
        std::unique_ptr<cAbstractStructure> structure = makeStructure(building.type, cell);
        requireRect(frame, structure->getVisualRectangle(), label + " preview frame against building");
    }
}

void runPlacementChecks()
{
    UnitFrameFixture fixture(4, 100);
    InputRig rig;
    rig.setMousePosition(400, 300);
    rig.installControls();

    for (const BuildingCase &building : BuildingCases) {
        for (const int percent : {100, 110, 125, 150}) {
            fixture.setDisplaySettings(4, percent);
            for (const float zoom : {0.8F, 1.0F, 1.1F, 1.25F, 1.3F, 1.5F, 2.0F}) {
                checkPreviewFrame(rig, building, percent, zoom, 0.0F, 0.0F, 10, 12);
                checkPreviewFrame(rig, building, percent, zoom, 13.5F, 17.3F, 10, 12);
                checkPreviewFrame(rig, building, percent, zoom, 31.75F, 0.25F, 21, 33);
            }
        }
    }
}
}

int main()
{
    try {
        runPlacementChecks();
        std::cout << "placement_frame: all checks passed\n";
    }
    catch (const std::exception &error) {
        std::cerr << "placement_frame: " << error.what() << '\n';
        return 1;
    }
    return 0;
}
