#pragma once

#include "cBuildingListDrawer.h"
#include "cTextDrawer.h"
#include "controls/cKeyboardEvent.h"
#include "observers/cInputObserver.h"
#include "sMouseEvent.h"

#include <array>

class Texture;
class cPlayer;
class GameContext;
class Graphics;

class cSideBarDrawer : cInputObserver {
public:
    explicit cSideBarDrawer(GameContext *ctx, cPlayer *player);
    ~cSideBarDrawer() override;

    void onNotifyMouseEvent(const s_MouseEvent &event) override;
    void onNotifyKeyboardEvent(const cKeyboardEvent &event) override;

    void draw();

    cBuildingListDrawer *getBuildingListDrawer() {
        return &m_buildingListDrawer;
    }

    void setPlayer(cPlayer *pPlayer);

protected:
    void drawBuildingLists();
    void drawCapacities();

    void drawCandybar();

    void drawMinimap();

private:
    cPlayer *m_player;
    Graphics *m_gfxinter;
    cBuildingListDrawer m_buildingListDrawer;
    cSideBar *m_sidebar;
    Color m_sidebarColor;
    cTextDrawer *m_smallTextDrawer;
    std::array<Texture *, 3> m_houseCrests{};

    void createCandyBar();
    void drawHdSidebar();
    void drawHdBuildingLists();
    void drawHdRadarPanel();
    void drawHdCapacities();
    void drawHdMeter(
        const cRectangle &rect,
        const std::string &label,
        int value,
        int maximum,
        Color fill,
        bool warning) const;
    [[nodiscard]] Texture *getHouseCrest() const;
    [[nodiscard]] std::string getHouseDisplayName() const;

    void drawPowerUsage() const;
    void drawCreditsUsage();
    Texture *candyBarBall=nullptr;
    Texture *candyBarPiece=nullptr;
    Texture *candyHorizonBar=nullptr;
    Texture *candiBarRenderer= nullptr;
};
