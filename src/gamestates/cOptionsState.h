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
#include "controls/cKeyBindings.h"
#include "gamestates/OptionsPageData.hpp"
#include "utils/InitialGameSettings.hpp"

#include <cstddef>
#include <memory>
#include <optional>
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
class cKeyboard;
class SaveSlotsDialog;

class cOptionsState : public cGameState {
    friend class UiAuditAccess;
public:
    enum class OptionsPage { Main, Gameplay, Controls, Diagnostics };

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
    cKeyboard* m_keyboard = nullptr;

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
    GuiLabel *m_resolutionValueLabel = nullptr;
    OptionsPage m_optionsPage = OptionsPage::Main;
    std::optional<OptionsPage> m_pendingOptionsPage;
    bool m_refreshRequested = false;
    InitialGameSettings m_selected;
    cKeyBindings m_selectedBindings;
    std::optional<eKeyAction> m_bindingCapture;
    bool m_bindingCaptureFinished = false;
    std::string m_bindingMessage;
    int m_controlsScrollRow = 0;
    std::vector<ResolutionOption> m_resolutionChoices;
    std::size_t m_selectedResolutionIndex = 0;
    ResolutionOption m_savedResolution;
    bool m_selectedFullscreen = false;
    bool m_savedFullscreen = false;

    std::unique_ptr<GuiWindow> m_guiWindow;
    std::unique_ptr<SaveSlotsDialog> m_saveDialog;

    void constructWindow(int prevState);
    void selectRenderScale(int step);
    void selectWorldScale(int step);
    void selectLanguage();
    void updateScaleControls();
    void applyScaleSettings();
    void selectResolution(int step);
    void loadSelectedOptions();
    void switchOptionsPage(OptionsPage page);
    void requestOptionsPage(OptionsPage page);
    void constructAdvancedWindow(int prevState);
    void applyAdvancedPage();
    Texture *const *m_backgroundTexture = nullptr;
};
