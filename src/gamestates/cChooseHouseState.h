/**
 * @file cChooseHouseState.h
 *
 * Dune 2 - The Maker
 *
 * @author Stefan Hendriks & the D2TM Team
 * @www http://www.dune2themaker.com
 * @copyright Copyright (c) 2002 - 2026 Stefan Hendriks and contributors
 * @license This software is released under the MIT License. See LICENSE.md.
 *
 * Note: Dune 2 is a trademark of Westwood Studios/Electronic Arts.
 *
 * This is a non-commercial educational project.
 */

#pragma once

#include "cGameState.h"
class cKeyboardEvent;
struct s_MouseEvent;
#include "utils/cRectangle.h"

#include <string>

struct SDL_Surface;
class Texture;
class GameContext;
class GameStateTransition;
class MentatFlow;
class cMouse;
class cTextDrawer;
class cGameSettings;
class Graphics;

class cChooseHouseState : public cGameState {
public:
    explicit cChooseHouseState(sGameServices* services);
    ~cChooseHouseState() override;

    void thinkFast() override;
    void draw() const override;

    void onNotifyMouseEvent(const s_MouseEvent &event) override;
    void onNotifyKeyboardEvent(const cKeyboardEvent &event) override;

    eGameStateType getType() override;

private:
    cGameSettings* m_settings = nullptr;
    cTextDrawer* m_textDrawer = nullptr;
    Graphics *m_gfxinter = nullptr;
    GameStateTransition* m_stateTransitions = nullptr;
    MentatFlow* m_mentatFlow = nullptr;
    cMouse* m_mouse = nullptr;
    cRectangle backButtonRect;

    // TODO: abstract away the selectable houses
    Texture *bmp_HouseAtreides;
    Texture *bmp_HouseOrdos;
    Texture *bmp_HouseHarkonnen;
    Texture *bmp_HouseSardaukar;
    Texture *m_hdBackground = nullptr;

    // Click areas of house emblems
    cRectangle houseAtreides;
    cRectangle houseOrdos;
    cRectangle houseHarkonnen;
    cRectangle houseSardaukar;

    // Functions
    bool hoversOverBackButton;

    void onMouseLeftButtonClicked(const s_MouseEvent &event) const;

    void onMouseMoved(const s_MouseEvent &event);
    void drawHdBackground() const;
    void drawHdHouseCard(
        const cRectangle &card,
        Texture *emblem,
        const std::string &name) const;
};
