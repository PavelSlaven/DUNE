#include <catch2/catch_test_macros.hpp>

#include "utils/WorldObjectScale.hpp"

TEST_CASE("P8A world object scale refinery harvester layout", "[P8A][P8A-scale]")
{
    const WorldObjectLayout scale100 = refineryHarvesterLayout(0, 0, 96, 64);
    CHECK(scale100.x == 32);
    CHECK(scale100.y == 1);
    CHECK(scale100.width == 80);
    CHECK(scale100.height == 52);

    const WorldObjectLayout scale110 = refineryHarvesterLayout(10, 20, 106, 70);
    CHECK(scale110.x == 46);
    CHECK(scale110.y == 21);
    CHECK(scale110.width == 88);
    CHECK(scale110.height == 57);

    const WorldObjectLayout scale125 = refineryHarvesterLayout(0, 0, 120, 80);
    CHECK(scale125.x == 40);
    CHECK(scale125.y == 1);
    CHECK(scale125.width == 100);
    CHECK(scale125.height == 65);

    const WorldObjectLayout scale150 = refineryHarvesterLayout(0, 0, 144, 96);
    CHECK(scale150.x == 49);
    CHECK(scale150.y == 1);
    CHECK(scale150.width == 120);
    CHECK(scale150.height == 78);
}
