#pragma once

#include "cGameState.h"
#include "controls/cKeyboardEvent.h"
#include "drawers/cTextDrawer.h"
#include "gui/GuiWindow.h"
#include "sMouseEvent.h"
#include "utils/GraphicsMode.hpp"
#include "utils/GameSettings.hpp"

#include <cstddef>
#include <memory>
#include <optional>
#include <string>
#include <string_view>
#include <vector>

struct SDL_Surface;
class cGame;
class GameContext;
class GuiButton;
class GuiLabel;
class SaveSlotsDialog;

class cOptionsState : public cGameState {
public:
    explicit cOptionsState(cGame &theGame, GameContext *ctx, int prevState);
    ~cOptionsState() override;

    void thinkFast() override;
    void draw() const override;

    void onNotifyMouseEvent(const s_MouseEvent &event) override;
    void onNotifyKeyboardEvent(const cKeyboardEvent &event) override;
    void onTextInput(std::string_view text) override;

    eGameStateType getType() override;

    void setPrevState(int prevState);
    void refresh();

private:
    struct ResolutionOption {
        int width;
        int height;

        bool operator==(const ResolutionOption &) const = default;
    };

    enum class OptionsPage {
        Main,
        Gameplay,
        Controls,
        Diagnostics
    };

    cTextDrawer* m_textDrawer = nullptr;
    bool m_hdLayout = false;

    int m_prevState;

    GuiWindow *m_guiWindow;
    std::vector<ResolutionOption> m_resolutionOptions;
    std::size_t m_selectedResolutionIndex = 0;
    ResolutionOption m_savedResolution{800, 600};
    std::vector<int> m_renderScaleOptions;
    std::size_t m_selectedRenderScaleIndex = 0;
    int m_savedRenderScalePercent = 0;
    std::vector<int> m_worldScaleOptions;
    std::size_t m_selectedWorldScaleIndex = 0;
    int m_savedWorldScalePercent = 0;
    bool m_selectedFullscreen = false;
    bool m_savedFullscreen = false;
    GraphicsMode m_selectedGraphicsMode = GraphicsMode::Hd;
    GraphicsMode m_savedGraphicsMode = GraphicsMode::Hd;
    GameSettings m_selectedSettings;
    std::string m_savedLanguage = "ru";
    OptionsPage m_optionsPage = OptionsPage::Main;
    std::optional<CommandBindingAction> m_bindingCapture;
    GuiLabel *m_languageValueLabel = nullptr;
    GuiLabel *m_resolutionValueLabel = nullptr;
    GuiLabel *m_renderScaleValueLabel = nullptr;
    GuiLabel *m_worldScaleValueLabel = nullptr;
    GuiLabel *m_graphicsModeValueLabel = nullptr;
    GuiLabel *m_displayStatusLabel = nullptr;
    GuiButton *m_applyDisplayButton = nullptr;
    GuiButton *m_loadGameButton = nullptr;
    std::unique_ptr<SaveSlotsDialog> m_saveDialog;

    void constructWindow(int prevState);
    void constructAdvancedWindow(int prevState);
    void initializeDisplaySettings();
    void rebuildRenderScaleOptions(int preferredScalePercent);
    void selectPreviousResolution();
    void selectNextResolution();
    void selectPreviousRenderScale();
    void selectNextRenderScale();
    void selectPreviousWorldScale();
    void selectNextWorldScale();
    void toggleGraphicsMode();
    void toggleLanguage();
    void switchOptionsPage(OptionsPage page);
    void updateDisplayControls();
    void updateDisplaySettingsDirtyState();
    void saveDisplaySettings();
    [[nodiscard]] std::string selectedResolutionText() const;
    [[nodiscard]] std::string selectedRenderScaleText() const;
    [[nodiscard]] std::string selectedWorldScaleText() const;
    [[nodiscard]] std::string selectedGraphicsModeText() const;
    [[nodiscard]] std::string selectedLanguageText() const;
    Texture *m_backgroundTexture = nullptr;
};
