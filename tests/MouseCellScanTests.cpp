#include "ZoomTestSupport.hpp"

#include <cmath>
#include <iostream>
#include <vector>

using namespace zoomtest;

namespace {
constexpr float ZoomLevels[] = {0.5F, 0.8F, 1.0F, 1.1F, 1.25F, 1.3F, 1.5F, 2.0F, 2.5F};
constexpr float ShiftValues[] = {0.0F, 0.25F, 0.5F, 13.0F, 13.5F, 17.3F, 31.75F};
constexpr double BoundaryMargin = 1e-3;

int firstValid(const std::vector<int> &table)
{
    for (std::size_t index = 0; index < table.size(); ++index) {
        if (table[index] >= 0) return static_cast<int>(index);
    }
    return -1;
}

bool containsInvalid(const std::vector<int> &table)
{
    for (const int value : table) {
        if (value < 0) return true;
    }
    return false;
}

bool nearCellBoundary(double samplePosition)
{
    const double remainder = std::fmod(samplePosition, static_cast<double>(CellSize));
    return remainder < BoundaryMargin || CellSize - remainder < BoundaryMargin;
}

bool boundaryAmbiguousX(int mouseX)
{
    return nearCellBoundary((mouseX + 0.5) / static_cast<double>(mapCamera->m_zoomLevel) +
                            static_cast<double>(mapCamera->m_viewportStartX));
}

bool boundaryAmbiguousY(int mouseY)
{
    return nearCellBoundary((mouseY - topBarHeight() + 0.5) / static_cast<double>(mapCamera->m_zoomLevel) +
                            static_cast<double>(mapCamera->m_viewportStartY));
}

int firstUnambiguousRow(const std::vector<int> &rows)
{
    for (int index = 0; index < static_cast<int>(rows.size()); ++index) {
        if (rows[index] >= 0 && !boundaryAmbiguousY(topBarHeight() + index)) return index;
    }
    return -1;
}

int firstUnambiguousColumn(const std::vector<int> &columns)
{
    for (int index = 0; index < static_cast<int>(columns.size()); ++index) {
        if (columns[index] >= 0 && !boundaryAmbiguousX(index)) return index;
    }
    return -1;
}

std::string describe(float zoom, float shiftX, float shiftY, const char *kind)
{
    return std::format("zoom {} viewport ({},{}) {}", zoom, shiftX, shiftY, kind);
}

void checkCell(const cGameControlsContext &controls, int mouseX, int mouseY, int expected,
               const std::string &label)
{
    const int actual = controls.getMouseCellFromScreen(mouseX, mouseY);
    if (actual != expected) {
        throw std::runtime_error(
            std::format("{} pixel ({},{}): expected cell {}, getMouseCellFromScreen returned {}",
                        label, mouseX, mouseY, expected, actual));
    }
}

void checkAbsolute(int mouseX, int mouseY, int expected, const std::string &label)
{
    if (boundaryAmbiguousX(mouseX) || boundaryAmbiguousY(mouseY)) return;
    const int absoluteX = mapCamera->getAbsMapMouseX(mouseX);
    const int absoluteY = mapCamera->getAbsMapMouseY(mouseY);
    const int cell = mapCamera->getCellFromAbsolutePosition(absoluteX, absoluteY);
    if (cell != expected) {
        throw std::runtime_error(
            std::format("{} pixel ({},{}): expected cell {}, absolute map pixel ({},{}) lies in cell {}",
                        label, mouseX, mouseY, expected, absoluteX, absoluteY, cell));
    }
}

void scanColumns(const cGameControlsContext &controls, float zoom, float shiftX, float shiftY = 0.0F)
{
    placeCamera(zoom, shiftX, shiftY);
    const std::vector<int> columns = columnTable();
    const std::vector<int> rows = rowTable();
    const int referenceRow = firstUnambiguousRow(rows);
    require(firstValid(columns) >= 0 && referenceRow >= 0,
            describe(zoom, shiftX, shiftY, "column scan") + ": the window shows no map cell");
    const int mouseY = topBarHeight() + referenceRow;

    const std::string cellLabel = describe(zoom, shiftX, shiftY, "cell, column scan");
    for (int mouseX = 0; mouseX < windowWidth(); ++mouseX) {
        const int expected = columns[mouseX] < 0 ? -1 : rows[referenceRow] * MapCells + columns[mouseX];
        checkCell(controls, mouseX, mouseY, expected, cellLabel);
    }
    const std::string absoluteLabel = describe(zoom, shiftX, shiftY, "absolute pixel, column scan");
    for (int mouseX = 0; mouseX < windowWidth(); ++mouseX) {
        const int expected = columns[mouseX] < 0 ? -1 : rows[referenceRow] * MapCells + columns[mouseX];
        checkAbsolute(mouseX, mouseY, expected, absoluteLabel);
    }
}

void scanRows(const cGameControlsContext &controls, float zoom, float shiftY, float shiftX = 0.0F)
{
    placeCamera(zoom, shiftX, shiftY);
    const std::vector<int> columns = columnTable();
    const std::vector<int> rows = rowTable();
    const int referenceColumn = firstUnambiguousColumn(columns);
    require(referenceColumn >= 0 && firstValid(rows) >= 0,
            describe(zoom, shiftX, shiftY, "row scan") + ": the window shows no map cell");

    const std::string cellLabel = describe(zoom, shiftX, shiftY, "cell, row scan");
    for (int index = 0; index < windowHeight(); ++index) {
        const int expected = rows[index] < 0 ? -1 : rows[index] * MapCells + columns[referenceColumn];
        checkCell(controls, referenceColumn, topBarHeight() + index, expected, cellLabel);
    }
    const std::string absoluteLabel = describe(zoom, shiftX, shiftY, "absolute pixel, row scan");
    for (int index = 0; index < windowHeight(); ++index) {
        const int expected = rows[index] < 0 ? -1 : rows[index] * MapCells + columns[referenceColumn];
        checkAbsolute(referenceColumn, topBarHeight() + index, expected, absoluteLabel);
    }
}

void scanPlane(const cGameControlsContext &controls, float zoom, float shiftX, float shiftY)
{
    placeCamera(zoom, shiftX, shiftY);
    const std::vector<int> columns = columnTable();
    const std::vector<int> rows = rowTable();
    const std::string label = describe(zoom, shiftX, shiftY, "cell, plane scan");
    for (int index = 5; index < windowHeight(); index += 13) {
        for (int mouseX = 3; mouseX < windowWidth(); mouseX += 11) {
            const int expected =
                (columns[mouseX] < 0 || rows[index] < 0) ? -1 : rows[index] * MapCells + columns[mouseX];
            checkCell(controls, mouseX, topBarHeight() + index, expected, label);
        }
    }
}

void checkWindowAndTables(float zoom)
{
    placeCamera(zoom, 0.0F, 0.0F);
    require(windowWidth() > 1000 && windowHeight() > 700,
            std::format("the map window must be large, got {}x{}", windowWidth(), windowHeight()));
    require(topBarHeight() > 0, "the top bar must have a height");
    const std::vector<int> columns = columnTable();
    const std::vector<int> rows = rowTable();
    require(static_cast<int>(columns.size()) == windowWidth() && static_cast<int>(rows.size()) == windowHeight(),
            "the pixel tables must cover the whole map window");
    if (zoom <= 0.5F) {
        require(containsInvalid(columns), "at the smallest zoom the window must show columns outside the map");
    }
}

struct EdgeView {
    float zoom;
    float shiftX;
    float shiftY;
};

constexpr EdgeView EdgeViews[] = {
    {0.5F, 900.5F, 1100.25F},
    {1.0F, 700.5F, 1500.25F},
    {1.5F, 1300.5F, 1700.25F},
};

void scanBeyondMapEdge(const cGameControlsContext &controls, const EdgeView &view)
{
    placeCamera(view.zoom, view.shiftX, view.shiftY);
    require(containsInvalid(columnTable()) && containsInvalid(rowTable()),
            describe(view.zoom, view.shiftX, view.shiftY, "edge view") +
                ": the window must show pixels beyond the right and bottom map edges");
    scanColumns(controls, view.zoom, view.shiftX, view.shiftY);
    scanRows(controls, view.zoom, view.shiftY, view.shiftX);
    scanPlane(controls, view.zoom, view.shiftX, view.shiftY);
}

void runScan()
{
    UnitFrameFixture fixture(4, 100);
    InputRig rig;
    rig.setMousePosition(400, 300);
    const cGameControlsContext &controls = rig.installControls();

    useCamera(ScreenWidth, ScreenHeight, 1.0F, 0.0F, 0.0F);
    for (const float zoom : ZoomLevels) checkWindowAndTables(zoom);

    for (const float zoom : ZoomLevels) {
        for (const float shift : ShiftValues) scanColumns(controls, zoom, shift);
    }
    for (const float zoom : ZoomLevels) {
        for (const float shift : ShiftValues) scanRows(controls, zoom, shift);
    }
    for (const float zoom : ZoomLevels) {
        for (const float shiftX : ShiftValues) {
            for (const float shiftY : ShiftValues) scanPlane(controls, zoom, shiftX, shiftY);
        }
    }
    for (const EdgeView &view : EdgeViews) scanBeyondMapEdge(controls, view);
}
}

int main()
{
    try {
        runScan();
        std::cout << "mouse_cell_scan: all checks passed\n";
    }
    catch (const std::exception &error) {
        std::cerr << "mouse_cell_scan: " << error.what() << '\n';
        return 1;
    }
    return 0;
}
