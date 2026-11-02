#include "ZoomTestSupport.hpp"

#include <iostream>
#include <string>
#include <vector>

using namespace zoomtest;

namespace {
void checkAxis(const char *axis, float zoom, float shift, std::vector<std::string> &failures)
{
    const bool horizontal = axis[0] == 'X';
    for (int tile = 0; tile < MapCells; ++tile) {
        const int absolute = tile * CellSize;
        const int start = horizontal ? mapCamera->getWindowXPosition(absolute) : mapCamera->getWindowYPosition(absolute);
        const int nextStart = horizontal ? mapCamera->getWindowXPosition(absolute + CellSize)
                                         : mapCamera->getWindowYPosition(absolute + CellSize);
        const int size = horizontal ? mapCamera->getTileDrawWidth(absolute) : mapCamera->getTileDrawHeight(absolute);
        if (start + size < nextStart) {
            failures.push_back(std::format("{}: zoom {} shift {} tile {} ends at {} before its neighbour starts at {}",
                                           axis, zoom, shift, tile, start + size, nextStart));
            return;
        }
        if (start + size == nextStart) {
            failures.push_back(std::format("{}: zoom {} shift {} tile {} only touches its neighbour at {}, no overlap",
                                           axis, zoom, shift, tile, nextStart));
            return;
        }
        if (start + size > nextStart + 1) {
            failures.push_back(std::format("{}: zoom {} shift {} tile {} ends at {}, more than 1 pixel past its "
                                           "neighbour start {}",
                                           axis, zoom, shift, tile, start + size, nextStart));
            return;
        }
    }
}

void runChecks(std::vector<std::string> &failures)
{
    UnitFrameFixture fixture(4, 100);
    useCamera(ScreenWidth, ScreenHeight, 1.0F, 0.0F, 0.0F);

    const float zooms[] = {0.5F, 0.8F, 1.0F, 1.1F, 1.25F, 1.3F, 1.5F, 2.0F, 2.5F};
    const float shifts[] = {0.0F, 0.25F, 13.5F, 17.3F};
    for (const float zoom : zooms) {
        for (const float shift : shifts) {
            placeCamera(zoom, shift, shift);
            checkAxis("X", zoom, shift, failures);
            checkAxis("Y", zoom, shift, failures);
        }
    }
}
}

int main()
{
    std::vector<std::string> failures;
    try {
        runChecks(failures);
    }
    catch (const std::exception &error) {
        std::cerr << "terrain_tile_gap: " << error.what() << '\n';
        return 1;
    }
    if (!failures.empty()) {
        for (const std::string &failure : failures) std::cerr << "terrain_tile_gap: " << failure << '\n';
        return 1;
    }
    std::cout << "terrain_tile_gap: all checks passed\n";
    return 0;
}
