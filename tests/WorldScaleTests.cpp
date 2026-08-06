#include "utils/WorldScale.hpp"

#include <iostream>

namespace {
bool expectEqual(const char *label, int actual, int expected)
{
    if (actual == expected) {
        return true;
    }
    std::cerr << label << ": got " << actual << ", expected " << expected
              << '\n';
    return false;
}
}

int main()
{
    bool passed = true;
    passed &= expectEqual("Auto 600p", calculateAutomaticWorldScalePercent(600), 100);
    passed &= expectEqual("Auto 768p", calculateAutomaticWorldScalePercent(768), 100);
    passed &= expectEqual("Auto 1080p", calculateAutomaticWorldScalePercent(1080), 110);
    passed &= expectEqual("Auto 1440p", calculateAutomaticWorldScalePercent(1440), 125);
    passed &= expectEqual("Auto 2160p", calculateAutomaticWorldScalePercent(2160), 150);
    passed &= expectEqual("Manual 110", resolveWorldScalePercent(110, 2160), 110);
    passed &= expectEqual("Invalid uses Auto", resolveWorldScalePercent(133, 1440), 125);

    passed &= expectEqual(
        "1920x1080 Auto canvas and Auto objects use HD4",
        selectHdAssetDensityForDisplay(1920, 1080, 1067, 600, 0),
        4
    );
    passed &= expectEqual(
        "2560x1440 Auto canvas and Auto objects use HD4",
        selectHdAssetDensityForDisplay(2560, 1440, 1067, 600, 0),
        4
    );
    passed &= expectEqual(
        "4K 100% logical canvas uses HD4",
        selectHdAssetDensityForDisplay(3840, 2160, 3840, 2160, 100),
        4
    );
    passed &= expectEqual(
        "4K Auto canvas uses HD4",
        selectHdAssetDensityForDisplay(3840, 2160, 1067, 600, 0),
        4
    );
    passed &= expectEqual(
        "5120x1440 Auto objects use HD4",
        selectHdAssetDensityForDisplay(5120, 1440, 3413, 960, 0),
        4
    );
    return passed ? 0 : 1;
}
