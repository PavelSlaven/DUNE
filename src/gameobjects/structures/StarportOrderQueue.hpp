#pragma once

#include <array>
#include <optional>

struct StarportOrder {
    int buildId = -1;
    int paidPrice = -1;

    int getBuildId() const {
        return buildId;
    }

    bool isValid() const {
        return buildId >= 0;
    }
};

template <std::size_t Capacity>
class StarportOrderQueue {
public:
    bool add(int buildId, int paidPrice) {
        for (StarportOrder &order : orders) {
            if (!order.isValid()) {
                order = StarportOrder {buildId, paidPrice};
                return true;
            }
        }
        return false;
    }

    bool hasFreeSlot() const {
        for (const StarportOrder &order : orders) {
            if (!order.isValid()) {
                return true;
            }
        }
        return false;
    }

    bool empty() const {
        for (const StarportOrder &order : orders) {
            if (order.isValid()) {
                return false;
            }
        }
        return true;
    }

    std::optional<StarportOrder> takeNext() {
        for (StarportOrder &order : orders) {
            if (order.isValid()) {
                StarportOrder result = order;
                order = {};
                return result;
            }
        }
        return std::nullopt;
    }

    std::optional<StarportOrder> removeFirst(int buildId) {
        for (StarportOrder &order : orders) {
            if (order.getBuildId() == buildId) {
                StarportOrder result = order;
                order = {};
                return result;
            }
        }
        return std::nullopt;
    }

private:
    std::array<StarportOrder, Capacity> orders {};
};

constexpr bool isStarportCatalogAvailable(bool hasStarport) {
    return hasStarport;
}
