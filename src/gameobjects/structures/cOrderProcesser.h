#pragma once

#include "sidebar/cBuildingListItem.h"
#include "StarportOrderQueue.hpp"

class cPlayer;

class cOrderProcesser {
private:
    static constexpr auto kMaxItemsToOrder = 8;

public:
    explicit cOrderProcesser(cPlayer *thePlayer);

    ~cOrderProcesser();

    void think();    // time based (per second)
    void updatePricesForStarport();

    void addOrder(cBuildingListItem *item);

    bool acceptsOrders();    // able to accept orders?
    void removeOrder(cBuildingListItem *item);

    void placeOrder();

    void playTMinusSound(int seconds);

    /**
     * Can place an order (call for Frigate) when anything has been ordered and the order hasn't been placed yet.
     * @return
     */
    bool canPlaceOrder() {
        return hasOrderedAnything() &&
               isOrderPlaced() == false;
    }

    bool isOrderPlaced() {
        return orderPlaced;
    }

    bool isFrigateSent() {
        return frigateSent;
    }

    bool hasOrderedAnything();

    bool hasFreeSlot() {
        return orderedItems.hasFreeSlot();
    }

    std::optional<StarportOrder> takeNextOrderToDeploy();

    void setOrderHasBeenProcessed();

    void sendFrigate();

    void clear();

protected:
    void removeAllItems();

    int getRandomizedSecondsToWait();

private:
    StarportOrderQueue<kMaxItemsToOrder> orderedItems;

    cPlayer *player;

    bool orderPlaced;

    // sent frigate to deliver order
    bool frigateSent;
    int unitIdOfFrigateSent;

    // when above zero, this will be substracted by one (by the think function).
    int secondsUntilArrival;

    // this is randomly set to 60 or more seconds. After the time runs out, new prices
    // will be set in the LIST_STARPORT
    int secondsUntilNewPricesWillBeCalculated;
};
