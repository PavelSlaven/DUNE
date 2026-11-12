/**
 * @file cOptionsState.h
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
#include "include/Texture.hpp"

#include <cstddef>
#include <memory>
#include <string>
#include <vector>

struct SDL_Surface;

class GameContext;
class cTextDrawer;
class GuiWindow;
class GuiButton;
class GuiLabel;
class GameStateTransition;
class cMouse;
class cGameSettings;
class SaveSlotsDialog;

class cOptionsState : public cGameState {
    friend class UiAuditAccess;
public:
    explicit cOptionsState(sGameServices* services, int prevState);
    ~cOptionsState() override;

    void thinkFast() override;
    void draw() const override;

    void onNotifyMouseEvent(const s_MouseEvent &event) override;
    void onNotifyKeyboardEvent(const cKeyboardEvent &event) override;

    eGameStateType getType() override;

    void setPrevState(int prevState);
    void refresh();

    bool isKeyboardCapturedByUi() const override;

private:
    cTextDrawer* m_textDrawer = nullptr;
    cGameSettings* m_settings = nullptr;
    GameStateTransition* m_stateTransitions = nullptr;
    cMouse* m_mouse = nullptr;

    int m_prevState;

    std::vector<int> m_renderScaleChoices;
    std::vector<int> m_worldScaleChoices;
    std::size_t m_selectedRenderScaleIndex = 0;
    std::size_t m_selectedWorldScaleIndex = 0;
    std::string m_selectedLanguage = "ru";
    GuiLabel *m_renderScaleValueLabel = nullptr;
    GuiLabel *m_worldScaleValueLabel = nullptr;
    GuiLabel *m_statusLabel = nullptr;
    GuiButton *m_applyButton = nullptr;
    GuiButton *m_languageButton = nullptr;
    GuiButton *m_loadGameButton = nullptr;

    std::unique_ptr<GuiWindow> m_guiWindow;
    std::unique_ptr<SaveSlotsDialog> m_saveDialog;

    void constructWindow(int prevState);
    void selectRenderScale(int step);
    void selectWorldScale(int step);
    void selectLanguage();
    void updateScaleControls();
    void applyScaleSettings();
    Texture *const *m_backgroundTexture = nullptr;
};
