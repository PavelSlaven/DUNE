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

    return passed ? 0 : 1;
}
