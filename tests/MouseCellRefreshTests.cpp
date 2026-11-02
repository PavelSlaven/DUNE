#include "ZoomTestSupport.hpp"

#include <functional>
#include <iostream>
#include <string>
#include <vector>

using namespace zoomtest;

namespace {
constexpr int UnitInFirstCell = 0;
constexpr int UnitInSecondCell = 1;
constexpr int StructureInFirstCell = 10;
constexpr int StructureInSecondCell = 11;

struct Start {
    float zoom;
    float shiftX;
    float shiftY;
    int mouseX;
    int mouseY;
};

struct Scenario {
    std::string name;
    Start start;
    std::function<void()> operation;
};

void operationJumpTo() { mapCamera->jumpTo(224, 192); }

void operationSetViewportPosition() { mapCamera->setViewportPosition(224, 192); }

void operationCenterOnCell() { mapCamera->centerAndJumpViewPortToCell(40 * MapCells + 40); }

void operationMoveByThink()
{
    mapCamera->m_moveX = 96.0F;
    mapCamera->m_moveY = 64.0F;
    mapCamera->thinkFast();
    mapCamera->m_moveX = 0.0F;
    mapCamera->m_moveY = 0.0F;
}

void operationZoomIn() { mapCamera->zoomIn(); }

void operationZoomOut() { mapCamera->zoomOut(); }

bool operationMovesCellUnderMouse(InputRig &rig, const Start &start, const std::function<void()> &operation,
                                  int &cellBefore, int &cellAfter)
{
    placeCamera(start.zoom, start.shiftX, start.shiftY);
    rig.setMousePosition(start.mouseX, start.mouseY);
    cellBefore = expectedCell(start.mouseX, start.mouseY);
    operation();
    cellAfter = expectedCell(start.mouseX, start.mouseY);
    placeCamera(start.zoom, start.shiftX, start.shiftY);
    return cellBefore >= 0 && cellAfter >= 0 && cellBefore != cellAfter;
}

Start findZoomStart(InputRig &rig, const std::function<void()> &operation, const std::string &name)
{
    for (int shiftX = 0; shiftX < 200; ++shiftX) {
        for (const int mouseX : {400, 700, 1000, 1300}) {
            for (const int mouseY : {300, 500, 700}) {
                const Start start = {1.0F, static_cast<float>(shiftX), 96.0F, mouseX, mouseY};
                int before = -1;
                int after = -1;
                if (operationMovesCellUnderMouse(rig, start, operation, before, after)) return start;
            }
        }
    }
    throw std::runtime_error("setup: no start position makes " + name + " change the cell under the mouse");
}

void placeObjects(UnitFrameFixture &fixture, int firstCell, int secondCell)
{
    fixture.setUnit(UnitInFirstCell, TANK, (firstCell % MapCells) * CellSize, (firstCell / MapCells) * CellSize);
    fixture.setUnit(UnitInSecondCell, TANK, (secondCell % MapCells) * CellSize, (secondCell / MapCells) * CellSize);
    global_map.cellSetIdForLayer(firstCell, MAPID_STRUCTURES, StructureInFirstCell);
    global_map.cellSetIdForLayer(secondCell, MAPID_STRUCTURES, StructureInSecondCell);
    global_map.setVisibleFor(firstCell, HUMAN);
    global_map.setVisibleFor(secondCell, HUMAN);
}

void removeObjects(int firstCell, int secondCell)
{
    for (const int cell : {firstCell, secondCell}) {
        global_map.cellSetIdForLayer(cell, MAPID_UNITS, -1);
        global_map.cellSetIdForLayer(cell, MAPID_STRUCTURES, -1);
    }
    unit[UnitInFirstCell].bHovered = false;
    unit[UnitInSecondCell].bHovered = false;
}

void runScenario(UnitFrameFixture &fixture, InputRig &rig, const Scenario &scenario,
                 std::vector<std::string> &failures)
{
    const Start &start = scenario.start;
    int firstCell = -1;
    int secondCell = -1;
    if (!operationMovesCellUnderMouse(rig, start, scenario.operation, firstCell, secondCell)) {
        throw std::runtime_error(std::format(
            "setup {}: the operation must move the cell under the mouse, got {} then {}",
            scenario.name, firstCell, secondCell));
    }

    cGameControlsContext &controls = rig.controls();
    placeObjects(fixture, firstCell, secondCell);
    rig.placeMouse(start.mouseX, start.mouseY);
    require(controls.getMouseCell() == firstCell,
            std::format("setup {}: before the operation the mouse cell must be {}, got {}",
                        scenario.name, firstCell, controls.getMouseCell()));
    require(controls.getIdOfUnitWhereMouseHovers() == UnitInFirstCell && unit[UnitInFirstCell].bHovered,
            "setup " + scenario.name + ": before the operation the unit in the first cell must be hovered");
    require(controls.getIdOfStructureWhereMouseHovers() == StructureInFirstCell,
            "setup " + scenario.name + ": before the operation the structure in the first cell must be hovered");

    scenario.operation();

    const int expected = expectedCell(start.mouseX, start.mouseY);
    if (controls.getMouseCell() != expected) {
        failures.push_back(std::format("{}: mouse cell is {} after the operation, expected {}",
                                       scenario.name, controls.getMouseCell(), expected));
    }
    if (controls.getIdOfUnitWhereMouseHovers() != UnitInSecondCell || !unit[UnitInSecondCell].bHovered ||
        unit[UnitInFirstCell].bHovered) {
        failures.push_back(std::format(
            "{}: unit hover is id {} (flags first {}, second {}) after the operation, expected id {} hovered and id {} released",
            scenario.name, controls.getIdOfUnitWhereMouseHovers(), unit[UnitInFirstCell].bHovered,
            unit[UnitInSecondCell].bHovered, UnitInSecondCell, UnitInFirstCell));
    }
    if (controls.getIdOfStructureWhereMouseHovers() != StructureInSecondCell) {
        failures.push_back(std::format("{}: structure hover is id {} after the operation, expected {}",
                                       scenario.name, controls.getIdOfStructureWhereMouseHovers(),
                                       StructureInSecondCell));
    }

    removeObjects(firstCell, secondCell);
}

void runRefreshChecks(std::vector<std::string> &failures)
{
    UnitFrameFixture fixture(4, 100);
    InputRig rig;
    rig.setMousePosition(400, 300);
    // The camera is created before the controls and is never replaced, so a fix that
    // subscribes the controls to the camera stays subscribed through every scenario.
    useCamera(ScreenWidth, ScreenHeight, 1.0F, 0.0F, 0.0F);
    rig.installControls();

    const Start zoomInStart = findZoomStart(rig, operationZoomIn, "zoomIn");
    const Start zoomOutStart = findZoomStart(rig, operationZoomOut, "zoomOut");

    const std::vector<Scenario> scenarios = {
        {"jumpTo at zoom 1.0", {1.0F, 0.0F, 0.0F, 400, 300}, operationJumpTo},
        {"setViewportPosition at zoom 2.0", {2.0F, 32.0F, 64.0F, 400, 300}, operationSetViewportPosition},
        {"centerAndJumpViewPortToCell at zoom 1.0", {1.0F, 0.0F, 0.0F, 400, 300}, operationCenterOnCell},
        {"thinkFast with camera speed at zoom 1.0", {1.0F, 32.0F, 32.0F, 400, 300}, operationMoveByThink},
        {"zoomIn", zoomInStart, operationZoomIn},
        {"zoomOut", zoomOutStart, operationZoomOut},
    };
    for (const Scenario &scenario : scenarios) runScenario(fixture, rig, scenario, failures);
}
}

int main()
{
    std::vector<std::string> failures;
    try {
        runRefreshChecks(failures);
    }
    catch (const std::exception &error) {
        std::cerr << "mouse_cell_refresh: " << error.what() << '\n';
        return 1;
    }
    if (!failures.empty()) {
        for (const std::string &failure : failures) std::cerr << "mouse_cell_refresh: " << failure << '\n';
        return 1;
    }
    std::cout << "mouse_cell_refresh: all checks passed\n";
    return 0;
}
