#include "utils/GraphicsMode.hpp"

#include <iostream>

int main()
{
    if (graphicsModeFromString("Classic") != GraphicsMode::Classic) {
        std::cerr << "Classic mode was not parsed\n";
        return 1;
    }
    if (graphicsModeFromString("hd") != GraphicsMode::Hd) {
        std::cerr << "HD mode was not parsed case-insensitively\n";
        return 1;
    }
    if (graphicsModeFromString("unexpected") != GraphicsMode::Hd) {
        std::cerr << "Unknown values must safely default to HD\n";
        return 1;
    }
    if (selectHdAssetDensity(2560, 1440) != 4) {
        std::cerr << "1440p HD mode must select HD4\n";
        return 1;
    }
    if (selectHdAssetDensity(3840, 1080) != 4) {
        std::cerr << "3840-wide output must select HD4\n";
        return 1;
    }
    if (selectHdAssetDensity(1920, 2160) != 4) {
        std::cerr << "2160-high output must select HD4\n";
        return 1;
    }
    if (hdDataFileSection(2) != "HD4_DATAFILE" ||
        hdDataFileSection(4) != "HD4_DATAFILE") {
        std::cerr << "HD mode must always use the HD4 section\n";
        return 1;
    }
    return 0;
}
