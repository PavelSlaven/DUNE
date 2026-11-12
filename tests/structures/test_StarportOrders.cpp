#include <catch2/catch_test_macros.hpp>

#include <optional>

#include "drawers/OrderButtonPolicy.hpp"
#include "gameobjects/structures/StarportOrderQueue.hpp"

TEST_CASE("Starport order label does not draw a shadow", "[P10B]")
{
    REQUIRE_FALSE(shouldDrawOrderLabelShadow());
}

TEST_CASE("Starport order queue stores values independently of catalog data", "[P10B]")
{
    StarportOrderQueue<8> queue;
    int catalogBuildId = 7;
    REQUIRE(queue.add(catalogBuildId, 400));
    catalogBuildId = 8;
    REQUIRE(catalogBuildId == 8);

    const std::optional<StarportOrder> order = queue.takeNext();
    REQUIRE(order.has_value());
    REQUIRE(order->getBuildId() == 7);
    REQUIRE(order->paidPrice == 400);
}

TEST_CASE("Starport catalog availability follows starport ownership", "[P10B]")
{
    REQUIRE_FALSE(isStarportCatalogAvailable(false));
    REQUIRE(isStarportCatalogAvailable(true));
}

TEST_CASE("Starport order queue peek preserves the next order", "[P10B]")
{
    StarportOrderQueue<8> queue;
    REQUIRE(queue.add(5, 100));
    REQUIRE(queue.add(6, 200));

    const std::optional<StarportOrder> firstPeek = queue.peekNext();
    REQUIRE(firstPeek.has_value());
    REQUIRE(firstPeek->getBuildId() == 5);
    const std::optional<StarportOrder> secondPeek = queue.peekNext();
    REQUIRE(secondPeek.has_value());
    REQUIRE(secondPeek->getBuildId() == 5);

    const std::optional<StarportOrder> firstTaken = queue.takeNext();
    REQUIRE(firstTaken.has_value());
    REQUIRE(firstTaken->getBuildId() == 5);
    const std::optional<StarportOrder> nextPeek = queue.peekNext();
    REQUIRE(nextPeek.has_value());
    REQUIRE(nextPeek->getBuildId() == 6);
    const std::optional<StarportOrder> secondTaken = queue.takeNext();
    REQUIRE(secondTaken.has_value());
    REQUIRE(secondTaken->getBuildId() == 6);

    REQUIRE(queue.empty());
    REQUIRE_FALSE(queue.peekNext().has_value());
    REQUIRE_FALSE(queue.takeNext().has_value());
}

TEST_CASE("Starport order queue enforces capacity and removes the first matching order", "[P10B]")
{
    StarportOrderQueue<8> queue;
    for (int i = 1; i <= 8; ++i) {
        REQUIRE(queue.add(i, 10 * i));
    }

    REQUIRE_FALSE(queue.hasFreeSlot());
    REQUIRE_FALSE(queue.add(9, 90));

    const std::optional<StarportOrder> removed = queue.removeFirst(3);
    REQUIRE(removed.has_value());
    REQUIRE(removed->paidPrice == 30);
    REQUIRE(queue.hasFreeSlot());
    REQUIRE_FALSE(queue.removeFirst(42).has_value());
}
