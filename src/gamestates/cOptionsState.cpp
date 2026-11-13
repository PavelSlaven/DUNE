/**
 * @file cOptionsState.cpp
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

#include "cOptionsState.h"
#include "config.h"

#include "gui/GuiButton.h"
#include "gui/GuiWindow.h"
#include "gui/GuiLabel.hpp"
#include "gui/GuiCheckBox.hpp"
#include "gui/GuiSlider.hpp"
#include "game/cTimeManager.h"
#include "context/AudioContext.hpp"
#include "context/GameContext.hpp"
#include "utils/cSoundPlayer.h"
#include "drawers/cTextDrawer.h"
#include "game/GameStateTransition.hpp"
#include "controls/cMouse.h"
#include "game/cGameSettings.h"

#include "include/cAssert.h"
#include "context/TextContext.hpp"
#include "gamestates/cGameState.h"
#include "include/sGameServices.h"
#include "include/eGameState.h"
#include "gamestates/OptionsMenuLayout.hpp"
#include "gui/GuiTheme.hpp"
#include "game/Preferences.hpp"
#include "game/PreferencesPath.hpp"
#include "utils/Log.h"
#include "utils/RenderScale.hpp"
#include "utils/WorldScale.hpp"
#include "utils/ScaleChoices.hpp"
#include "utils/Localization.hpp"
#include "save/SaveGameManager.hpp"
#include "save/SaveSlotsDialog.hpp"
#include "gamestates/ResolutionDialog.hpp"
#include "controls/cKeyboard.h"
#include "controls/cKeyboardEvent.h"
#include "controls/sMouseEvent.h"
#include "gamestates/OptionsKeyLabels.hpp"

#include <algorithm>
#include <SDL3/SDL.h>
#include <format>

namespace {

std::string normalizeLanguage(const std::string &language)
{
    return language == "en" || language == "EN" ? "en" : "ru";
}

std::string resolutionChoiceText(
    const ResolutionOption &resolution,
    const ResolutionOption &native)
{
    const std::string label = std::format("{}×{}", resolution.width, resolution.height);
    if (resolution == native) {
        return std::format("{} ({})", label, localization::text("native", "родное"));
    }
    return label;
}

}

cOptionsState::cOptionsState(sGameServices* services, eGameState prevState)
    : cGameState(services),
    m_textDrawer(m_ctx->getTextContext()->getBeneTextDrawer()),
    m_settings(services->settings),
    m_stateTransitions(services->stateTransitions),
    m_mouse(services->mouse),
    m_keyboard(services->keyboard),
    m_prevState(prevState),
    m_guiWindow(nullptr)
{
    d2tm_assert(m_textDrawer != nullptr);
    d2tm_assert(m_settings != nullptr);
    d2tm_assert(m_stateTransitions != nullptr);
    d2tm_assert(m_mouse != nullptr);
    d2tm_assert(m_keyboard != nullptr);
    d2tm_assert(m_keyboard->getKeyBindings() != nullptr);

    m_renderScaleChoices = renderScaleChoices(m_settings->getOutputW(), m_settings->getOutputH());
    m_worldScaleChoices = worldScaleChoices();
    m_selectedRenderScaleIndex = scaleChoiceIndex(m_renderScaleChoices, m_settings->getSavedRenderScalePercent());
    m_selectedWorldScaleIndex = scaleChoiceIndex(m_worldScaleChoices, m_settings->getSavedWorldScalePercent());
    m_selectedLanguage = normalizeLanguage(m_settings->getSavedLanguage());
    m_saveDialog = std::make_unique<SaveSlotsDialog>(
        services->saveGameFlow,
        m_sdlDrawer,
        m_textDrawer,
        m_settings,
        [this]() {
            m_stateTransitions->fadeOut();
        },
        [this]() {
            if (m_loadGameButton == nullptr) {
                return;
            }
            m_loadGameButton->setEnabled(true);
            m_loadGameButton->setTheme(GuiTheme::Remaster());
        });
    m_resolutionDialog = std::make_unique<ResolutionDialog>(
        m_sdlDrawer,
        m_textDrawer,
        m_settings,
        [this](std::size_t index) {
            m_selectedResolutionIndex = index;
            m_statusLabel->setText("");
            updateScaleControls();
        });
    loadSelectedOptions();
    refresh();
    m_backgroundTexture = &services->screenTexture;
}

void cOptionsState::constructWindow(eGameState prevState)
{
    if (m_optionsPage != OptionsPage::Main) {
        constructAdvancedWindow(prevState);
        return;
    }
    const int margin = 8;
    const int buttonHeight = std::max(32, m_textDrawer->getFontHeight() + 10);
    const OptionsMenuLayout menuLayout = OptionsMenuLayout::create(
        m_settings->getScreenW(),
        m_settings->getScreenH(),
        buttonHeight,
        m_prevState == eGameState::PLAYING,
        m_textDrawer->getFontHeight(),
        2
    );
    const GuiTheme controlTheme = GuiTheme::Remaster();
    const GuiRenderKind buttonKind = GuiRenderKind::REMASTER_BUTTON;
    const int contentX = 24;
    const int audioLabelWidth = 110;
    const int audioCheckX = 138;
    const int volumeLabelX = 218;
    const int volumeLabelWidth = 110;
    const int audioSliderX = 350;
    const int audioSliderWidth = 250;
    const int checkLabelWidth = 220;
    const int checkX = 252;
    const int displayLabelWidth = 160;
    const int arrowWidth = 46;
    const int selectorX = 198;
    const int scaleValueWidth = 200;
    const int contentRowStride = buttonHeight + menuLayout.contentGap;
    const auto contentRowY = [menuLayout, contentRowStride](int row) {
        return menuLayout.contentTop + (row - 1) * contentRowStride;
    };
    const auto relativeRect = [this](const cRectangle &rect) {
        return m_guiWindow->getRelativeRect(
            rect.getX(),
            rect.getY(),
            rect.getWidth(),
            rect.getHeight()
        );
    };
    const auto rect = [this](int x, int y, int w, int h) {
        return m_guiWindow->getRelativeRect(x, y, w, h);
    };

    m_guiWindow = std::make_unique<GuiWindow>(m_sdlDrawer, menuLayout.window, m_textDrawer);
    m_guiWindow->setTheme(controlTheme);
    AudioContext* audioContext = m_ctx->getAudioContext();
    cSoundPlayer* soundPlayer = audioContext->getSoundPlayer();

    m_guiWindow->setTitle(localization::text("Dune II - The Maker - version ", "Dune II - The Maker - версия ") + D2TM_VERSION);

    const cRectangle &toMainMenuRect = relativeRect(menuLayout.mainMenu);
    auto gui_btn_toMenu = GuiButtonBuilder()
            .withRect(toMainMenuRect)
            .withLabel(localization::text("Main menu", "В главное меню"))
            .withTextDrawer(m_textDrawer)
            .withRenderer(m_sdlDrawer)
            .withTheme(controlTheme)
            .withKind(buttonKind)
            .onClick([this]() {
                m_stateTransitions->setNextStateWithFade(eGameState::MENU);
            })
            .build();
    m_guiWindow->addGuiObject(std::move(gui_btn_toMenu));

    const cRectangle &quitRect = relativeRect(menuLayout.quit);
    auto gui_btn_Quit = GuiButtonBuilder()
            .withRect(quitRect)
            .withLabel(localization::text("Quit game", "Выйти из игры"))
            .withTextDrawer(m_textDrawer)
            .withRenderer(m_sdlDrawer)
            .withTheme(controlTheme)
            .withKind(buttonKind)
            .onClick([this]() {
                m_settings->setPlaying(false);
                m_stateTransitions->fadeOut();
            })
            .build();
    m_guiWindow->addGuiObject(std::move(gui_btn_Quit));

    const cRectangle &backRect = relativeRect(menuLayout.back);
    auto gui_btn_Back = GuiButtonBuilder()
            .withRect(backRect)
            .withLabel(localization::text("Back", "Назад"))
            .withTextDrawer(m_textDrawer)
            .withRenderer(m_sdlDrawer)
            .withTheme(controlTheme)
            .withKind(buttonKind)
            .onClick([this,prevState](){
                m_stateTransitions->setNextState(prevState);
            })
            .build();
    m_guiWindow->addGuiObject(std::move(gui_btn_Back));

    if (m_prevState == eGameState::PLAYING) {
        const bool hasSaves = SaveGameManager::hasAnySave();
        const cRectangle &saveRect = relativeRect(menuLayout.save);
        auto saveButton = GuiButtonBuilder()
                .withRect(saveRect)
                .withLabel(localization::text("Save game", "Сохранить игру"))
                .withTextDrawer(m_textDrawer)
                .withRenderer(m_sdlDrawer)
                .withTheme(controlTheme)
                .withKind(buttonKind)
                .onClick([this]() {
                    m_saveDialog->open(true, true);
                })
                .build();
        m_guiWindow->addGuiObject(std::move(saveButton));

        const cRectangle &loadRect = relativeRect(menuLayout.load);
        auto loadButton = GuiButtonBuilder()
                .withRect(loadRect)
                .withLabel(localization::text("Load game", "Загрузить игру"))
                .withTextDrawer(m_textDrawer)
                .withRenderer(m_sdlDrawer)
                .withTheme(hasSaves ? controlTheme : GuiTheme::RemasterInactive())
                .withKind(buttonKind)
                .withEnabled(hasSaves)
                .onClick([this]() {
                    m_saveDialog->open(true, false);
                })
                .build();
        m_loadGameButton = loadButton.get();
        m_guiWindow->addGuiObject(std::move(loadButton));
    }

    if (m_prevState == eGameState::PLAYING && !m_settings->isSkirmish()) {
        const cRectangle &toMissionSelectRect = relativeRect(menuLayout.missionSelect);
        auto gui_btn_toMissionSelect = GuiButtonBuilder()
                .withRect(toMissionSelectRect)
                .withLabel(localization::text("Mission select", "Выбор миссии"))
                .withTextDrawer(m_textDrawer)
                .withRenderer(m_sdlDrawer)
                .withTheme(controlTheme)
                .withKind(buttonKind)
                .onClick([this]() {
                    m_stateTransitions->setNextState(eGameState::MISSIONSELECT);
                })
                .build();
        m_guiWindow->addGuiObject(std::move(gui_btn_toMissionSelect));
    }

    if (m_settings->isCheatMode()) {
        const cRectangle &cheatRect = rect(contentX, contentRowY(11), checkLabelWidth, buttonHeight);
        auto gui_cheatLabel = GuiLabelBuilder()
                .withLabel(localization::text("Cheat mode enabled", "Режим читов включён"))
                .withTextDrawer(m_textDrawer)
                .withRenderer(m_sdlDrawer)
                .withKind(GuiRenderKind::TRANSPARENT_WITHOUT_BORDER)
                .withTheme(cGuiThemeBuilder().light().withTextColor(Color::Yellow).build())
                .withTextAlign(GuiTextAlignHorizontal::LEFT)
                .withRect(cheatRect)
                .build();
        m_guiWindow->addGuiObject(std::move(gui_cheatLabel));
    }

    const cRectangle &musicRect = rect(contentX, contentRowY(1), audioLabelWidth, buttonHeight);
    auto gui_MusicLabel = GuiLabelBuilder()
            .withLabel(localization::text("Music", "Музыка"))
            .withTextDrawer(m_textDrawer)
            .withRenderer(m_sdlDrawer)
            .withKind(GuiRenderKind::TRANSPARENT_WITHOUT_BORDER)
            .withTheme(controlTheme)
            .withRect(musicRect)
            .build();
    m_guiWindow->addGuiObject(std::move(gui_MusicLabel));

    const cRectangle &musicCheckRect = rect(audioCheckX, contentRowY(1), buttonHeight, buttonHeight);
    auto gui_MusicCheckLabel = GuiCheckBoxBuilder()
            .withRect(musicCheckRect)
            .withRenderer(m_sdlDrawer)
            .withTheme(controlTheme)
            .onCheck([audioContext]() {
                audioContext->setMusicEnabled(true);
            })
            .onUnCheck([audioContext]() {
                audioContext->setMusicEnabled(false);
            })
            .build();
    gui_MusicCheckLabel->setChecked(soundPlayer->getMusicEnabled());
    m_guiWindow->addGuiObject(std::move(gui_MusicCheckLabel));

    const cRectangle &musicVolumeRect = rect(volumeLabelX, contentRowY(1), volumeLabelWidth, buttonHeight);
    auto gui_MusicVolumeLabel = GuiLabelBuilder()
            .withLabel(localization::text("Volume", "Громкость"))
            .withTextDrawer(m_textDrawer)
            .withRenderer(m_sdlDrawer)
            .withKind(GuiRenderKind::TRANSPARENT_WITHOUT_BORDER)
            .withTheme(controlTheme)
            .withRect(musicVolumeRect)
            .build();
    m_guiWindow->addGuiObject(std::move(gui_MusicVolumeLabel));

    const cRectangle &btn_musicVolumeRect = rect(audioSliderX, contentRowY(1), audioSliderWidth, buttonHeight);
    auto gui_sld_musicVolumeRect = GuiSliderBuilder()
            .withRect(btn_musicVolumeRect)
            .withRenderer(m_sdlDrawer)
            .withTheme(controlTheme)
            .withMinValue(0)
            .withMaxValue(10)
            .withInitialValue(soundPlayer->getMusicVolume())
            .onValueChanged([soundPlayer](int newValue) {
                soundPlayer->setMusicVolume(newValue);
            })
            .build();
    m_guiWindow->addGuiObject(std::move(gui_sld_musicVolumeRect));

    const cRectangle &soundRect = rect(contentX, contentRowY(2), audioLabelWidth, buttonHeight);
    auto gui_SoundLabel = GuiLabelBuilder()
            .withLabel(localization::text("Sound", "Звук"))
            .withTextDrawer(m_textDrawer)
            .withRenderer(m_sdlDrawer)
            .withKind(GuiRenderKind::TRANSPARENT_WITHOUT_BORDER)
            .withTheme(controlTheme)
            .withRect(soundRect)
            .build();
    m_guiWindow->addGuiObject(std::move(gui_SoundLabel));

    const cRectangle &soundCheckRect = rect(audioCheckX, contentRowY(2), buttonHeight, buttonHeight);
    auto gui_SoundCheckLabel = GuiCheckBoxBuilder()
            .withRect(soundCheckRect)
            .withRenderer(m_sdlDrawer)
            .withTheme(controlTheme)
            .onCheck([soundPlayer]() {
                soundPlayer->setSoundEnabled(true);
            })
            .onUnCheck([soundPlayer]() {
                soundPlayer->setSoundEnabled(false);
            })
            .build();
    gui_SoundCheckLabel->setChecked(soundPlayer->getSoundEnabled());
    m_guiWindow->addGuiObject(std::move(gui_SoundCheckLabel));

    const cRectangle &soundVolumeRect = rect(volumeLabelX, contentRowY(2), volumeLabelWidth, buttonHeight);
    auto gui_SoundVolumeLabel = GuiLabelBuilder()
            .withLabel(localization::text("Volume", "Громкость"))
            .withTextDrawer(m_textDrawer)
            .withRenderer(m_sdlDrawer)
            .withKind(GuiRenderKind::TRANSPARENT_WITHOUT_BORDER)
            .withTheme(controlTheme)
            .withRect(soundVolumeRect)
            .build();
    m_guiWindow->addGuiObject(std::move(gui_SoundVolumeLabel));

    const cRectangle &btn_soundVolumeRect = rect(audioSliderX, contentRowY(2), audioSliderWidth, buttonHeight);
    auto gui_sld_soundVolumeRect = GuiSliderBuilder()
            .withRect(btn_soundVolumeRect)
            .withRenderer(m_sdlDrawer)
            .withTheme(controlTheme)
            .withMinValue(0)
            .withMaxValue(10)
            .withInitialValue(soundPlayer->getSoundVolume())
            .onValueChanged([soundPlayer](int newValue) {
                soundPlayer->setSoundVolume(newValue);
            })
            .build();
    m_guiWindow->addGuiObject(std::move(gui_sld_soundVolumeRect));

    const cRectangle &speedRect = relativeRect(menuLayout.speedLabel);
    auto gui_DifficultyLabel = GuiLabelBuilder()
            .withLabel(localization::text("Game speed", "Скорость игры"))
            .withTextDrawer(m_textDrawer)
            .withRenderer(m_sdlDrawer)
            .withKind(GuiRenderKind::TRANSPARENT_WITHOUT_BORDER)
            .withTheme(controlTheme)
            .withRect(speedRect)
            .build();
    m_guiWindow->addGuiObject(std::move(gui_DifficultyLabel));

    cTimeManager* timeManager = m_ctx->getTimeManager();
    const cRectangle &sld_speedRect = rect(audioCheckX, contentRowY(3), 220, buttonHeight);
    int convertedForSlider = 2 - timeManager->getGlobalSpeed() + 10;
    auto gui_sld_speedRect = GuiSliderBuilder()
            .withRect(sld_speedRect)
            .withRenderer(m_sdlDrawer)
            .withTheme(controlTheme)
            .withMinValue(2)
            .withMaxValue(10)
            .withInitialValue(convertedForSlider)
            .onValueChanged([timeManager](int newValue) {
                int globalSpeed = 10 - newValue + 2;
                // higher means slower, so convert into opposite
                timeManager->setGlobalSpeed(globalSpeed);
            })
            .build();
    m_guiWindow->addGuiObject(std::move(gui_sld_speedRect));

    const cRectangle &fogOfWarRect = rect(contentX, contentRowY(4), checkLabelWidth, buttonHeight);
    auto gui_FogOfWarLabel = GuiLabelBuilder()
            .withLabel(localization::text("FOW", "Туман войны"))
            .withTextDrawer(m_textDrawer)
            .withRenderer(m_sdlDrawer)
            .withKind(GuiRenderKind::TRANSPARENT_WITHOUT_BORDER)
            .withTextAlign(GuiTextAlignHorizontal::LEFT)
            .withTheme(controlTheme)
            .withRect(fogOfWarRect)
            .build();
    m_guiWindow->addGuiObject(std::move(gui_FogOfWarLabel));

    const cRectangle &fogOfWarCheckRect = rect(checkX, contentRowY(4), buttonHeight, buttonHeight);
    auto gui_FogOfWarCheckLabel = GuiCheckBoxBuilder()
            .withRect(fogOfWarCheckRect)
            .withRenderer(m_sdlDrawer)
            .withTheme(controlTheme)
            .onCheck([this]() {
                m_settings->setFogOfWarEnabled(true);
            })
            .onUnCheck([this]() {
                m_settings->setFogOfWarEnabled(false);
            })
            .build();
    gui_FogOfWarCheckLabel->setChecked(m_settings->isFogOfWarEnabled());
    m_guiWindow->addGuiObject(std::move(gui_FogOfWarCheckLabel));

    const cRectangle &renderScaleRect = rect(contentX, contentRowY(5), displayLabelWidth, buttonHeight);
    auto renderScaleLabel = GuiLabelBuilder()
            .withRect(renderScaleRect)
            .withLabel(localization::text("Game scale", "Масштаб игры"))
            .withTextDrawer(m_textDrawer)
            .withRenderer(m_sdlDrawer)
            .withTheme(controlTheme)
            .withKind(GuiRenderKind::TRANSPARENT_WITHOUT_BORDER)
            .withTextAlign(GuiTextAlignHorizontal::LEFT)
            .build();
    m_guiWindow->addGuiObject(std::move(renderScaleLabel));

    const cRectangle &previousRenderScaleRect = rect(selectorX, contentRowY(5), arrowWidth, buttonHeight);
    auto previousRenderScaleButton = GuiButtonBuilder()
            .withRect(previousRenderScaleRect)
            .withLabel("◄")
            .withTextDrawer(m_textDrawer)
            .withRenderer(m_sdlDrawer)
            .withTheme(controlTheme)
            .withKind(buttonKind)
            .onClick([this]() { selectRenderScale(-1); })
            .build();
    m_guiWindow->addGuiObject(std::move(previousRenderScaleButton));

    const cRectangle &renderScaleValueRect = rect(selectorX + arrowWidth + margin, contentRowY(5), scaleValueWidth, buttonHeight);
    auto renderScaleValueLabel = GuiLabelBuilder()
            .withRect(renderScaleValueRect)
            .withLabel("")
            .withTextDrawer(m_textDrawer)
            .withRenderer(m_sdlDrawer)
            .withTheme(controlTheme)
            .withKind(GuiRenderKind::OPAQUE_WITH_BORDER)
            .build();
    m_renderScaleValueLabel = renderScaleValueLabel.get();
    m_guiWindow->addGuiObject(std::move(renderScaleValueLabel));

    const cRectangle &nextRenderScaleRect = rect(selectorX + arrowWidth + margin + scaleValueWidth + margin, contentRowY(5), arrowWidth, buttonHeight);
    auto nextRenderScaleButton = GuiButtonBuilder()
            .withRect(nextRenderScaleRect)
            .withLabel("►")
            .withTextDrawer(m_textDrawer)
            .withRenderer(m_sdlDrawer)
            .withTheme(controlTheme)
            .withKind(buttonKind)
            .onClick([this]() { selectRenderScale(1); })
            .build();
    m_guiWindow->addGuiObject(std::move(nextRenderScaleButton));

    const cRectangle &worldScaleRect = rect(contentX, contentRowY(6), displayLabelWidth, buttonHeight);
    auto worldScaleLabel = GuiLabelBuilder()
            .withRect(worldScaleRect)
            .withLabel(localization::text("Object size", "Размер объектов"))
            .withTextDrawer(m_textDrawer)
            .withRenderer(m_sdlDrawer)
            .withTheme(controlTheme)
            .withKind(GuiRenderKind::TRANSPARENT_WITHOUT_BORDER)
            .withTextAlign(GuiTextAlignHorizontal::LEFT)
            .build();
    m_guiWindow->addGuiObject(std::move(worldScaleLabel));

    const cRectangle &previousWorldScaleRect = rect(selectorX, contentRowY(6), arrowWidth, buttonHeight);
    auto previousWorldScaleButton = GuiButtonBuilder()
            .withRect(previousWorldScaleRect)
            .withLabel("◄")
            .withTextDrawer(m_textDrawer)
            .withRenderer(m_sdlDrawer)
            .withTheme(controlTheme)
            .withKind(buttonKind)
            .onClick([this]() { selectWorldScale(-1); })
            .build();
    m_guiWindow->addGuiObject(std::move(previousWorldScaleButton));

    const cRectangle &worldScaleValueRect = rect(selectorX + arrowWidth + margin, contentRowY(6), scaleValueWidth, buttonHeight);
    auto worldScaleValueLabel = GuiLabelBuilder()
            .withRect(worldScaleValueRect)
            .withLabel("")
            .withTextDrawer(m_textDrawer)
            .withRenderer(m_sdlDrawer)
            .withTheme(controlTheme)
            .withKind(GuiRenderKind::OPAQUE_WITH_BORDER)
            .build();
    m_worldScaleValueLabel = worldScaleValueLabel.get();
    m_guiWindow->addGuiObject(std::move(worldScaleValueLabel));

    const cRectangle &nextWorldScaleRect = rect(selectorX + arrowWidth + margin + scaleValueWidth + margin, contentRowY(6), arrowWidth, buttonHeight);
    auto nextWorldScaleButton = GuiButtonBuilder()
            .withRect(nextWorldScaleRect)
            .withLabel("►")
            .withTextDrawer(m_textDrawer)
            .withRenderer(m_sdlDrawer)
            .withTheme(controlTheme)
            .withKind(buttonKind)
            .onClick([this]() { selectWorldScale(1); })
            .build();
    m_guiWindow->addGuiObject(std::move(nextWorldScaleButton));

    const cRectangle &lowPowerIconRect = rect(contentX, contentRowY(7), checkLabelWidth, buttonHeight);
    auto gui_LowPowerIconLabel = GuiLabelBuilder()
            .withLabel(localization::text("Low power icon", "Значок энергии"))
            .withTextDrawer(m_textDrawer)
            .withRenderer(m_sdlDrawer)
            .withKind(GuiRenderKind::TRANSPARENT_WITHOUT_BORDER)
            .withTextAlign(GuiTextAlignHorizontal::LEFT)
            .withTheme(controlTheme)
            .withRect(lowPowerIconRect)
            .build();
    m_guiWindow->addGuiObject(std::move(gui_LowPowerIconLabel));

    const cRectangle &lowPowerIconCheckRect = rect(checkX, contentRowY(7), buttonHeight, buttonHeight);
    auto gui_LowPowerIconCheck = GuiCheckBoxBuilder()
            .withRect(lowPowerIconCheckRect)
            .withRenderer(m_sdlDrawer)
            .withTheme(controlTheme)
            .onCheck([this]() {
                m_settings->setShowLowPowerIcon(true);
            })
            .onUnCheck([this]() {
                m_settings->setShowLowPowerIcon(false);
            })
            .build();
    gui_LowPowerIconCheck->setChecked(m_settings->isShowLowPowerIcon());
    m_guiWindow->addGuiObject(std::move(gui_LowPowerIconCheck));

    const cRectangle &languageRect = rect(contentX, contentRowY(8), displayLabelWidth, buttonHeight);
    auto languageLabel = GuiLabelBuilder()
            .withRect(languageRect)
            .withLabel(localization::text("Language", "Язык"))
            .withTextDrawer(m_textDrawer)
            .withRenderer(m_sdlDrawer)
            .withTheme(controlTheme)
            .withKind(GuiRenderKind::TRANSPARENT_WITHOUT_BORDER)
            .withTextAlign(GuiTextAlignHorizontal::LEFT)
            .build();
    m_guiWindow->addGuiObject(std::move(languageLabel));

    const int languageButtonWidth = arrowWidth + margin + scaleValueWidth + margin + arrowWidth;
    const cRectangle &languageButtonRect = rect(selectorX, contentRowY(8), languageButtonWidth, buttonHeight);
    auto languageButton = GuiButtonBuilder()
            .withRect(languageButtonRect)
            .withLabel(m_selectedLanguage == "en" ? "English" : "Русский")
            .withTextDrawer(m_textDrawer)
            .withRenderer(m_sdlDrawer)
            .withTheme(controlTheme)
            .withKind(buttonKind)
            .onClick([this]() { selectLanguage(); })
            .build();
    m_languageButton = languageButton.get();
    m_guiWindow->addGuiObject(std::move(languageButton));

    const cRectangle &resolutionRect = rect(contentX, contentRowY(9), displayLabelWidth, buttonHeight);
    auto resolutionLabel = GuiLabelBuilder()
            .withRect(resolutionRect)
            .withLabel(localization::text("Resolution", "Разрешение"))
            .withTextDrawer(m_textDrawer)
            .withRenderer(m_sdlDrawer)
            .withTheme(controlTheme)
            .withKind(GuiRenderKind::TRANSPARENT_WITHOUT_BORDER)
            .withTextAlign(GuiTextAlignHorizontal::LEFT)
            .build();
    m_guiWindow->addGuiObject(std::move(resolutionLabel));

    const int resolutionButtonWidth = arrowWidth * 2 + margin * 2 + scaleValueWidth;
    const cRectangle &resolutionButtonRect = rect(selectorX, contentRowY(9), resolutionButtonWidth, buttonHeight);
    auto resolutionButton = GuiButtonBuilder()
            .withRect(resolutionButtonRect)
            .withLabel("")
            .withTextDrawer(m_textDrawer)
            .withRenderer(m_sdlDrawer)
            .withTheme(controlTheme)
            .withKind(buttonKind)
            .onClick([this]() { openResolutionDialog(); })
            .build();
    m_resolutionButton = resolutionButton.get();
    m_guiWindow->addGuiObject(std::move(resolutionButton));

    const cRectangle &fullscreenRect = rect(contentX, contentRowY(10), checkLabelWidth, buttonHeight);
    auto fullscreenLabel = GuiLabelBuilder()
            .withRect(fullscreenRect)
            .withLabel(localization::text("Fullscreen", "Полноэкранный режим"))
            .withTextDrawer(m_textDrawer)
            .withRenderer(m_sdlDrawer)
            .withKind(GuiRenderKind::TRANSPARENT_WITHOUT_BORDER)
            .withTextAlign(GuiTextAlignHorizontal::LEFT)
            .withTheme(controlTheme)
            .build();
    m_guiWindow->addGuiObject(std::move(fullscreenLabel));

    const cRectangle &fullscreenCheckRect = rect(checkX, contentRowY(10), buttonHeight, buttonHeight);
    auto fullscreenCheck = GuiCheckBoxBuilder()
            .withRect(fullscreenCheckRect)
            .withRenderer(m_sdlDrawer)
            .withTheme(controlTheme)
            .onCheck([this]() {
                m_selectedFullscreen = true;
                m_statusLabel->setText("");
                updateScaleControls();
            })
            .onUnCheck([this]() {
                m_selectedFullscreen = false;
                m_statusLabel->setText("");
                updateScaleControls();
            })
            .build();
    fullscreenCheck->setChecked(m_selectedFullscreen);
    m_guiWindow->addGuiObject(std::move(fullscreenCheck));

    const cRectangle &applyRect = relativeRect(menuLayout.apply);
    auto applyButton = GuiButtonBuilder()
            .withRect(applyRect)
            .withLabel(localization::text("Apply", "Применить"))
            .withTextDrawer(m_textDrawer)
            .withRenderer(m_sdlDrawer)
            .withTheme(controlTheme)
            .withKind(buttonKind)
            .onClick([this]() { applyScaleSettings(); })
            .build();
    m_applyButton = applyButton.get();
    m_guiWindow->addGuiObject(std::move(applyButton));

    const cRectangle &statusRect = relativeRect(menuLayout.status);
    auto statusLabel = GuiLabelBuilder()
            .withRect(statusRect)
            .withLabel("")
            .withTextDrawer(m_textDrawer)
            .withRenderer(m_sdlDrawer)
            .withTheme(controlTheme)
            .withKind(GuiRenderKind::TRANSPARENT_WITHOUT_BORDER)
            .withTextAlign(GuiTextAlignHorizontal::LEFT)
            .build();
    m_statusLabel = statusLabel.get();
    m_guiWindow->addGuiObject(std::move(statusLabel));

    const cRectangle &advancedRect = relativeRect(menuLayout.advanced);
    auto advancedButton = GuiButtonBuilder()
            .withRect(advancedRect)
            .withLabel(localization::text("More settings", "Ещё настройки"))
            .withTextDrawer(m_textDrawer)
            .withRenderer(m_sdlDrawer)
            .withTheme(controlTheme)
            .withKind(buttonKind)
            .onClick([this]() { requestOptionsPage(OptionsPage::Gameplay); })
            .build();
    m_guiWindow->addGuiObject(std::move(advancedButton));

    updateScaleControls();
}

void cOptionsState::selectRenderScale(int step)
{
    const int count = static_cast<int>(m_renderScaleChoices.size());
    m_selectedRenderScaleIndex = static_cast<std::size_t>((static_cast<int>(m_selectedRenderScaleIndex) + step + count) % count);
    m_statusLabel->setText("");
    updateScaleControls();
}

void cOptionsState::selectWorldScale(int step)
{
    const int count = static_cast<int>(m_worldScaleChoices.size());
    m_selectedWorldScaleIndex = static_cast<std::size_t>((static_cast<int>(m_selectedWorldScaleIndex) + step + count) % count);
    m_statusLabel->setText("");
    updateScaleControls();
}

void cOptionsState::selectLanguage()
{
    m_selectedLanguage = m_selectedLanguage == "en" ? "ru" : "en";
    m_statusLabel->setText("");
    updateScaleControls();
}

void cOptionsState::openResolutionDialog()
{
    std::vector<std::string> labels;
    labels.reserve(m_resolutionChoices.size());
    for (const ResolutionOption &resolution : m_resolutionChoices) {
        labels.push_back(resolutionChoiceText(resolution, m_nativeResolution));
    }
    m_resolutionDialog->open(labels, m_selectedResolutionIndex);
}

void cOptionsState::updateScaleControls()
{
    const int outputW = m_settings->getOutputW();
    const int outputH = m_settings->getOutputH();
    const int renderScale = m_renderScaleChoices[m_selectedRenderScaleIndex];
    const int worldScale = m_worldScaleChoices[m_selectedWorldScaleIndex];
    m_renderScaleValueLabel->setText(scaleChoiceText(renderScale, calculateAutomaticRenderScalePercent(outputW, outputH)));
    m_worldScaleValueLabel->setText(scaleChoiceText(worldScale, calculateAutomaticWorldScalePercent(outputH)));
    const ResolutionOption &resolution = m_resolutionChoices[m_selectedResolutionIndex];
    m_resolutionButton->setText(resolutionChoiceText(resolution, m_nativeResolution));
    m_languageButton->setText(m_selectedLanguage == "en" ? "English" : "Русский");
    const std::string savedLanguage = normalizeLanguage(m_settings->getSavedLanguage());
    m_applyButton->setEnabled(
        renderScale != m_settings->getSavedRenderScalePercent() ||
        worldScale != m_settings->getSavedWorldScalePercent() ||
        m_selectedLanguage != savedLanguage ||
        resolution != m_savedResolution || m_selectedFullscreen != m_savedFullscreen
    );
}

void cOptionsState::applyScaleSettings()
{
    const int renderScale = m_renderScaleChoices[m_selectedRenderScaleIndex];
    const int worldScale = m_worldScaleChoices[m_selectedWorldScaleIndex];
    const ResolutionOption resolution = m_resolutionChoices[m_selectedResolutionIndex];
    m_selected.renderScalePercent = renderScale;
    m_selected.worldScalePercent = worldScale;
    m_selected.language = m_selectedLanguage;
    m_selected.screenW = resolution.width;
    m_selected.screenH = resolution.height;
    m_selected.windowed = !m_selectedFullscreen;
    std::string error = "Could not get the user data directory";
    const auto prefsFile = PreferencesPath::file(Preferences::FILE_NAME);
    const bool saved = prefsFile && Preferences::saveValues(*prefsFile, Preferences::valuesOf(m_selected, MAIN_PAGE_KEYS), error);
    if (saved) {
        m_settings->setSavedScalePercents(renderScale, worldScale);
        m_settings->setSavedLanguage(m_selectedLanguage);
        m_savedResolution = resolution;
        m_savedFullscreen = m_selectedFullscreen;
        m_statusLabel->setText(localization::text("Saved. Restart the game.", "Сохранено. Перезапустите игру."));
    } else {
        Logger::warn(COMP_GAMERULES, "Preferences", "Could not save preferences: {}", error);
        m_statusLabel->setText(localization::text("Could not save preferences.ini", "Не удалось сохранить preferences.ini"));
    }
    updateScaleControls();
}

void cOptionsState::loadSelectedOptions()
{
    InitialGameSettings selected;
    selected.screenW = m_settings->getRequestedScreenW();
    selected.screenH = m_settings->getRequestedScreenH();
    selected.windowed = m_settings->isWindowed();
    selected.renderScalePercent = m_settings->getSavedRenderScalePercent();
    selected.worldScalePercent = m_settings->getSavedWorldScalePercent();
    selected.language = normalizeLanguage(m_settings->getSavedLanguage());
    selected.cameraEdgeMove = m_settings->isCameraEdgeMove();
    selected.cameraDragMoveSpeed = m_settings->getCameraDragMoveSpeed();
    selected.cameraBorderOrKeyMoveSpeed = m_settings->getCameraBorderOrKeyMoveSpeed();
    selected.pauseWhenLosingFocus = m_settings->isPauseWhenLosingFocus();
    selected.allowRepeatingReinforcements = m_settings->isAllowRepeatingReinforcements();
    selected.turretsDownOnLowPower = m_settings->isTurretsDownOnLowPower();
    selected.rocketTurretsDownOnLowPower = m_settings->isRocketTurretsDownOnLowPower();
    selected.debugMode = m_settings->isDebugMode();
    selected.disableAI = m_settings->isDisableAI();
    selected.oneAi = m_settings->isOneAi();
    selected.disableWormAi = m_settings->isDisableWormAi();
    selected.disableReinforcements = m_settings->isDisableReinforcements();
    selected.noAiRest = m_settings->isNoAiRest();
    selected.drawUnitDebug = m_settings->isDrawUnitDebug();
    selected.drawUsages = m_settings->isDrawUsages();
    if (const auto prefsFile = PreferencesPath::file(Preferences::FILE_NAME)) {
        std::string error;
        Preferences::loadChosenOptions(*prefsFile, selected, error);
    }
    m_selected = selected;
    m_selectedBindings = *m_keyboard->getKeyBindings();
    m_bindingCapture.reset();
    m_bindingCaptureFinished = false;
    m_bindingMessage.clear();
    m_controlsScrollRow = 0;

    int desktopWidth = m_settings->getScreenW();
    int desktopHeight = m_settings->getScreenH();
    SDL_Rect bounds{};
    if (SDL_GetDisplayBounds(SDL_GetPrimaryDisplay(), &bounds)) {
        desktopWidth = bounds.w;
        desktopHeight = bounds.h;
    }
    m_nativeResolution = {desktopWidth, desktopHeight};
    m_savedResolution = selected.screenW <= 0 || selected.screenH <= 0
        ? m_nativeResolution
        : ResolutionOption{selected.screenW, selected.screenH};
    m_resolutionChoices = resolutionChoices(m_nativeResolution, m_savedResolution);
    m_selectedResolutionIndex = resolutionChoiceIndex(m_resolutionChoices, m_savedResolution);
    m_savedFullscreen = !selected.windowed;
    m_selectedFullscreen = m_savedFullscreen;
}

void cOptionsState::switchOptionsPage(OptionsPage page)
{
    m_bindingCapture.reset();
    m_bindingCaptureFinished = false;
    m_bindingMessage.clear();
    m_controlsScrollRow = 0;
    m_optionsPage = page;
    refresh();
}

void cOptionsState::requestOptionsPage(OptionsPage page)
{
    m_pendingOptionsPage = page;
}

cOptionsState::~cOptionsState()
{
    // Smart pointers handle cleanup
}

void cOptionsState::thinkFast()
{
    if (m_pendingOptionsPage) {
        const OptionsPage page = *m_pendingOptionsPage;
        m_pendingOptionsPage.reset();
        switchOptionsPage(page);
        return;
    }
    if (m_bindingCaptureFinished) {
        m_bindingCaptureFinished = false;
        m_bindingCapture.reset();
        m_refreshRequested = false;
        refresh();
        return;
    }
    if (m_refreshRequested) {
        m_refreshRequested = false;
        refresh();
    }
}

void cOptionsState::draw() const
{
    if (m_backgroundTexture && *m_backgroundTexture) {
        m_sdlDrawer->renderSprite(*m_backgroundTexture,0,0);
    }
    m_guiWindow->draw();
    if (m_saveDialog->isOpen()) {
        m_saveDialog->draw();
    }
    if (m_resolutionDialog->isOpen()) {
        m_resolutionDialog->draw();
    }

    // MOUSE
    m_mouse->draw();
}

void cOptionsState::onNotifyMouseEvent(const s_MouseEvent &event)
{
    if (m_resolutionDialog->isOpen()) {
        m_resolutionDialog->onMouseEvent(event);
        return;
    }
    if (m_saveDialog->isOpen()) {
        m_saveDialog->onMouseEvent(event);
        return;
    }
    const bool isWheelEvent = event.eventType == eMouseEventType::MOUSE_SCROLLED_UP ||
                              event.eventType == eMouseEventType::MOUSE_SCROLLED_DOWN;
    if (isWheelEvent && m_optionsPage == OptionsPage::Controls && !m_bindingCapture) {
        m_controlsScrollRow += event.eventType == eMouseEventType::MOUSE_SCROLLED_UP ? -3 : 3;
        refresh();
        return;
    }
    m_guiWindow->onNotifyMouseEvent(event);
}

eGameStateType cOptionsState::getType()
{
    return GAMESTATE_OPTIONS;
}

void cOptionsState::onNotifyKeyboardEvent(const cKeyboardEvent &event)
{
    if (m_resolutionDialog->isOpen()) {
        m_resolutionDialog->onKeyboardEvent(event);
        return;
    }
    if (m_saveDialog->isOpen()) {
        m_saveDialog->onKeyboardEvent(event);
        return;
    }
    if (m_optionsPage != OptionsPage::Controls || !m_bindingCapture || m_bindingCaptureFinished ||
        !event.isType(eKeyEventType::PRESSED) || event.hasTextInput()) {
        return;
    }
    const SDL_Scancode key = event.getFirstKey();
    if (key == SDL_SCANCODE_UNKNOWN) {
        return;
    }
    // The capture ends in thinkFast, so that the game's global key actions do not receive the key just chosen.
    m_bindingCaptureFinished = true;
    m_bindingMessage.clear();
    if (key == SDL_SCANCODE_ESCAPE) {
        return;
    }
    if (!cKeyBindings::canStoreKey(key)) {
        m_bindingMessage = localization::text("This key cannot be assigned.", "Эту клавишу нельзя назначить.");
        return;
    }
    const s_KeyBinding binding = cKeyBindings::makeCapturedBinding(key, event.getCombo());
    const std::optional<eKeyAction> conflict = m_selectedBindings.trySetBinding(*m_bindingCapture, binding);
    if (conflict) {
        m_bindingMessage = localization::format(
            "Key {} is already assigned to {}.",
            "Клавиша {} уже назначена команде «{}».",
            cKeyBindings::describeBinding(binding),
            keyActionLabelText(*conflict));
    }
}

/**
 * Reconstructs window so that it knows to which previous state it should go 'back to'
 * @param prevState
 */
void cOptionsState::setPrevState(eGameState prevState)
{
    m_prevState = prevState;
    m_optionsPage = OptionsPage::Main;
    m_pendingOptionsPage.reset();
    loadSelectedOptions();
    refresh();
}

void cOptionsState::refresh()
{
    if (m_saveDialog) {
        m_saveDialog->close();
    }
    if (m_resolutionDialog) {
        m_resolutionDialog->close();
    }
    m_guiWindow.reset();
    m_renderScaleValueLabel = nullptr;
    m_worldScaleValueLabel = nullptr;
    m_statusLabel = nullptr;
    m_applyButton = nullptr;
    m_languageButton = nullptr;
    m_loadGameButton = nullptr;
    m_resolutionButton = nullptr;
    constructWindow(m_prevState);
    m_backgroundTexture = nullptr;
}

bool cOptionsState::isKeyboardCapturedByUi() const
{
    return m_bindingCapture.has_value() || m_saveDialog->isCapturingText() || m_resolutionDialog->isOpen();
}
