/**
 * @file cMainMenuState.h
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
#include "controls/cKeyboardEvent.h"
#include "utils/cRectangle.h"
#include "controls/sMouseEvent.h"

#include <memory>

class Texture;
class cTextDrawer;
class MissionFlow;
class VideoFlow;
class GameStateTransition;
class cMouse;
class GuiButton;
class GuiWindow;
class cGameSettings;
class SaveSlotsDialog;

class cMainMenuState : public cGameState {
    friend class UiAuditAccess;
public:
    explicit cMainMenuState(sGameServices* services);
    ~cMainMenuState() override;

    void thinkFast() override;
    void draw() const override;

    void onNotifyMouseEvent(const s_MouseEvent &event) override;
    void onNotifyKeyboardEvent(const cKeyboardEvent &event) override;

    eGameStateType getType() override;

    bool isKeyboardCapturedByUi() const override;

private:
    void buildHdMenu();
    void drawHdBackground() const;

    cGameSettings * m_settings = nullptr;
    cTextDrawer* m_textDrawer = nullptr;
    MissionFlow* m_missionFlow = nullptr;
    VideoFlow* m_videoFlow = nullptr;
    GameStateTransition* m_stateTransitions = nullptr;
    cMouse* m_mouse = nullptr;

    int logoX;
    int logoY;

    int mainMenuFrameX;
    int mainMenuFrameY;
    int mainMenuWidth;
    int mainMenuHeight;
    cRectangle m_logoRect;

    std::unique_ptr<GuiWindow> gui_window;
    std::unique_ptr<GuiButton> gui_btn_credits;

    Texture *bmp_D2TM_Title;
    Texture *m_hdMenuBackground = nullptr;
    Texture *m_hdMenuLogo = nullptr;
    std::unique_ptr<Texture> backGroundDebug;
    std::unique_ptr<SaveSlotsDialog> m_saveDialog;
};
