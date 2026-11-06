#include "utils/WorldObjectScale.hpp"

#include <iostream>

namespace {
bool expectEqual(const char *name, int actual, int expected)
{
    if (actual == expected) {
        return true;
    }
    std::cerr << name << ": expected " << expected
              << ", got " << actual << '\n';
    return false;
}
}

int main()
{
    bool passed = true;
    const WorldObjectLayout scale100 =
        refineryHarvesterLayout(0, 0, 96, 64);
    passed &= expectEqual("100% x", scale100.x, 32);
    passed &= expectEqual("100% y", scale100.y, 1);
    passed &= expectEqual("100% width", scale100.width, 80);
    passed &= expectEqual("100% height", scale100.height, 52);

    const WorldObjectLayout scale110 =
        refineryHarvesterLayout(10, 20, 106, 70);
    passed &= expectEqual("110% x", scale110.x, 46);
    passed &= expectEqual("110% y", scale110.y, 21);
    passed &= expectEqual("110% width", scale110.width, 88);
    passed &= expectEqual("110% height", scale110.height, 57);

    const WorldObjectLayout scale125 =
        refineryHarvesterLayout(0, 0, 120, 80);
    passed &= expectEqual("125% x", scale125.x, 40);
    passed &= expectEqual("125% y", scale125.y, 1);
    passed &= expectEqual("125% width", scale125.width, 100);
    passed &= expectEqual("125% height", scale125.height, 65);

    const WorldObjectLayout scale150 =
        refineryHarvesterLayout(0, 0, 144, 96);
    passed &= expectEqual("150% x", scale150.x, 49);
    passed &= expectEqual("150% y", scale150.y, 1);
    passed &= expectEqual("150% width", scale150.width, 120);
    passed &= expectEqual("150% height", scale150.height, 78);
    return passed ? 0 : 1;
}
