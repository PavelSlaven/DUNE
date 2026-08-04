#pragma once

#include "cTextDrawer.h"
#include "observers/cInputObserver.h"
#include "sidebar/cBuildingList.h"
#include "sidebar/HudLayout.hpp"

#include <array>
#include <string>

class cPlayer;
class GameContext;
class Graphics;

class cBuildingListDrawer : cInputObserver {

public:
    explicit cBuildingListDrawer(const GameContext *ctx, cPlayer *player);

    void onNotifyMouseEvent(const s_MouseEvent &event) override;
    void onNotifyKeyboardEvent(const cKeyboardEvent &event) override;

    void drawList(cBuildingList *list, int listIDToDraw);
    void drawButtonHoverRectangle(cBuildingList *list);
    void drawButton(cBuildingList *list, bool pressed);

    cBuildingListItem *isOverItemCoordinates(cBuildingList *list, int x, int y);

    int getDrawX();
    int getDrawY();

    void setPlayer(cPlayer *player);

protected:

private:
    // the list to draw
    cTextDrawer* m_gameTextDrawer;
    cTextDrawer* m_smallTextDrawer;
    Graphics* m_gfxinter;

    cPlayer *m_player;

    bool m_renderListIds;
    std::array<int, cSideBar::LIST_MAX> m_scrollRows{};
    std::string m_readyLabel;

    void drawStructureSize(int structureId, int x, int y);
    void drawList(cBuildingList *list, bool shouldDrawStructureSize);
    void drawListWithStructures(cBuildingList *list);		// used for const yard
    void drawListWithUnitsOrAbilities(cBuildingList *list); // used for units or palace / starport

    bool isOverItemCoordinates_Boolean(int x, int y, int drawX, int drawY);
    [[nodiscard]] int getColumnCount() const;
    [[nodiscard]] int getCardWidth() const;
    [[nodiscard]] int getCardHeight() const;
    [[nodiscard]] int getCardGap() const;
    void drawHdCard(cBuildingListItem *item, int x, int y);
    void drawHdScrollbar(cBuildingList *list, const HudLayout &layout);
    [[nodiscard]] HudLayout getLayout(cBuildingList *list = nullptr) const;
    [[nodiscard]] int getScrollRow(cBuildingList *list) const;
    void setScrollRow(cBuildingList *list, int row);
    void scrollSelectedList(int rowDelta);

    void onKeyHold(const cKeyboardEvent &event);

    void onKeyPressed(const cKeyboardEvent &event);
};
