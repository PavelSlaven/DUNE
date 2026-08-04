#pragma once

#include "cGameState.h"
#include "controls/cKeyboardEvent.h"
#include "drawers/cTextDrawer.h"
#include "sMouseEvent.h"
#include "utils/cRectangle.h"

struct SDL_Surface;
class Texture;
class cGame;
class GameContext;
class Graphics;

class cChooseHouseState : public cGameState {
public:
    explicit cChooseHouseState(cGame &theGame, GameContext* ctx);
    ~cChooseHouseState() override;

    void thinkFast() override;
    void draw() const override;

    void onNotifyMouseEvent(const s_MouseEvent &event) override;
    void onNotifyKeyboardEvent(const cKeyboardEvent &event) override;

    eGameStateType getType() override;

private:
    cTextDrawer* m_textDrawer = nullptr;
    Graphics *m_gfxinter;
    cRectangle *backButtonRect;

    Texture *bmp_Dune;
    Texture *bmp_SelectYourHouseTitle;

    // TODO: abstract away the selectable houses
    Texture *bmp_HouseAtreides;
    Texture *bmp_HouseOrdos;
    Texture *bmp_HouseHarkonnen;
    Texture *m_hdBackground = nullptr;

    // Click areas of house emblems
    cRectangle houseAtreides;
    cRectangle houseOrdos;
    cRectangle houseHarkonnen;

    int selectYourHouseXCentered;
    cPoint coords_Dune;
    cPoint coords_SelectYourHouseTitle;

    // Functions
    bool hoversOverBackButton;
    bool m_hdLayout = false;
    int m_hoveredHouse = -1;

    void onMouseLeftButtonClicked(const s_MouseEvent &event) const;

    void onMouseMoved(const s_MouseEvent &event);
    void drawHdBackground() const;
    void drawHdHouseCard(
        const cRectangle &card,
        Texture *emblem,
        const std::string &name,
        bool hovered
    ) const;
};
