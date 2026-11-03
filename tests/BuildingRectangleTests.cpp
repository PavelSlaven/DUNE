#include "ZoomTestSupport.hpp"

#include "gameobjects/structures/cRefinery.h"
#include "gameobjects/structures/cWindTrap.h"

#include <iostream>
#include <memory>

using namespace zoomtest;

namespace {
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

void checkBuilding(const BuildingCase &building, int percent, float zoom, float viewportX, float viewportY)
{
    sStructureInfo[building.type].bmp_width = building.widthPixels;
    sStructureInfo[building.type].bmp_height = building.heightPixels;

    useCamera(ScreenWidth, ScreenHeight, zoom, viewportX, viewportY);
    const int cell = 12 * MapCells + 10;
    std::unique_ptr<cAbstractStructure> structure = makeStructure(building.type, cell);

    const int absoluteX = global_map.getAbsoluteXPositionFromCell(cell);
    const int absoluteY = global_map.getAbsoluteYPositionFromCell(cell);
    const cRectangle expected = {
        mapCamera->getWindowXPosition(absoluteX),
        mapCamera->getWindowYPosition(absoluteY),
        static_cast<int>(std::lround(zoom * building.widthPixels)),
        static_cast<int>(std::lround(zoom * building.heightPixels))
    };
    requireRect(structure->getVisualRectangle(), expected,
                std::format("{} scale {}% zoom {} viewport ({},{})",
                            building.name, percent, zoom, viewportX, viewportY));
}

void runBuildingChecks()
{
    UnitFrameFixture fixture(4, 100);
    for (const BuildingCase &building : BuildingCases) {
        for (const int percent : {100, 110, 125, 150}) {
            fixture.setDisplaySettings(4, percent);
            for (const float zoom : {0.8F, 1.0F, 1.1F, 1.25F, 1.5F, 2.0F}) {
                checkBuilding(building, percent, zoom, 0.0F, 0.0F);
                checkBuilding(building, percent, zoom, 13.5F, 17.3F);
            }
        }
    }
}
}

int main()
{
    try {
        runBuildingChecks();
        std::cout << "building_visual_rectangle: all checks passed\n";
    }
    catch (const std::exception &error) {
        std::cerr << "building_visual_rectangle: " << error.what() << '\n';
        return 1;
    }
    return 0;
}
