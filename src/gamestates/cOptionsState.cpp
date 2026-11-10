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

#include <algorithm>

cOptionsState::cOptionsState(sGameServices* services, int prevState)
    : cGameState(services),
    m_textDrawer(m_ctx->getTextContext()->getBeneTextDrawer()),
    m_settings(services->settings),
    m_stateTransitions(services->stateTransitions),
    m_mouse(services->mouse),
    m_prevState(prevState),
    m_guiWindow(nullptr)
{
    d2tm_assert(m_textDrawer != nullptr);
    d2tm_assert(m_settings != nullptr);
    d2tm_assert(m_stateTransitions != nullptr);
    d2tm_assert(m_mouse != nullptr);

    m_renderScaleChoices = renderScaleChoices(m_settings->getOutputW(), m_settings->getOutputH());
    m_worldScaleChoices = worldScaleChoices();
    m_selectedRenderScaleIndex = scaleChoiceIndex(m_renderScaleChoices, m_settings->getSavedRenderScalePercent());
    m_selectedWorldScaleIndex = scaleChoiceIndex(m_worldScaleChoices, m_settings->getSavedWorldScalePercent());
    refresh();
    m_backgroundTexture = &services->screenTexture;
}

void cOptionsState::constructWindow(int prevState)
{
    const int margin = 8;
    const int buttonHeight = std::max(32, m_textDrawer->getFontHeight() + 10);
    const OptionsMenuLayout menuLayout = OptionsMenuLayout::create(
        m_settings->getScreenW(),
        m_settings->getScreenH(),
        buttonHeight,
        m_prevState == GAME_PLAYING,
        m_textDrawer->getFontHeight()
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

    m_guiWindow->setTitle("Dune II - The Maker - version " + D2TM_VERSION);

    const cRectangle &toMainMenuRect = relativeRect(menuLayout.mainMenu);
    auto gui_btn_toMenu = GuiButtonBuilder()
            .withRect(toMainMenuRect)
            .withLabel("Main menu")
            .withTextDrawer(m_textDrawer)
            .withRenderer(m_sdlDrawer)
            .withTheme(controlTheme)
            .withKind(buttonKind)
            .onClick([this]() {
                m_stateTransitions->setNextStateWithFade(GAME_MENU);
            })
            .build();
    m_guiWindow->addGuiObject(std::move(gui_btn_toMenu));

    const cRectangle &quitRect = relativeRect(menuLayout.quit);
    auto gui_btn_Quit = GuiButtonBuilder()
            .withRect(quitRect)
            .withLabel("Quit game")
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
            .withLabel("Back")
            .withTextDrawer(m_textDrawer)
            .withRenderer(m_sdlDrawer)
            .withTheme(controlTheme)
            .withKind(buttonKind)
            .onClick([this,prevState](){
                m_stateTransitions->setNextState(prevState);
            })
            .build();
    m_guiWindow->addGuiObject(std::move(gui_btn_Back));

    if (m_prevState == GAME_PLAYING) {
        const cRectangle &saveRect = relativeRect(menuLayout.save);
        auto saveButton = GuiButtonBuilder()
                .withRect(saveRect)
                .withLabel("Save game")
                .withTextDrawer(m_textDrawer)
                .withRenderer(m_sdlDrawer)
                .withTheme(GuiTheme::RemasterInactive())
                .withKind(buttonKind)
                .withEnabled(false)
                .build();
        m_guiWindow->addGuiObject(std::move(saveButton));

        const cRectangle &loadRect = relativeRect(menuLayout.load);
        auto loadButton = GuiButtonBuilder()
                .withRect(loadRect)
                .withLabel("Load game")
                .withTextDrawer(m_textDrawer)
                .withRenderer(m_sdlDrawer)
                .withTheme(GuiTheme::RemasterInactive())
                .withKind(buttonKind)
                .withEnabled(false)
                .build();
        m_guiWindow->addGuiObject(std::move(loadButton));
    }

    if (m_prevState == GAME_PLAYING && !m_settings->isSkirmish()) {
        const cRectangle &toMissionSelectRect = relativeRect(menuLayout.missionSelect);
        auto gui_btn_toMissionSelect = GuiButtonBuilder()
                .withRect(toMissionSelectRect)
                .withLabel("Mission select")
                .withTextDrawer(m_textDrawer)
                .withRenderer(m_sdlDrawer)
                .withTheme(controlTheme)
                .withKind(buttonKind)
                .onClick([this]() {
                    m_stateTransitions->setNextState(GAME_MISSIONSELECT);
                })
                .build();
        m_guiWindow->addGuiObject(std::move(gui_btn_toMissionSelect));
    }

    if (m_settings->isCheatMode()) {
        const cRectangle &cheatRect = rect(contentX, contentRowY(9), checkLabelWidth, buttonHeight);
        auto gui_cheatLabel = GuiLabelBuilder()
                .withLabel("Cheat mode enabled")
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
            .withLabel("Music")
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
            .withLabel("Volume")
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
            .withLabel("Sound")
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
            .withLabel("Volume")
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
            .withLabel("Game speed")
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
            .withLabel("FOW")
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
            .withLabel("Game scale")
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
            .withLabel("<")
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
            .withLabel(">")
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
            .withLabel("Object size")
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
            .withLabel("<")
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
            .withLabel(">")
            .withTextDrawer(m_textDrawer)
            .withRenderer(m_sdlDrawer)
            .withTheme(controlTheme)
            .withKind(buttonKind)
            .onClick([this]() { selectWorldScale(1); })
            .build();
    m_guiWindow->addGuiObject(std::move(nextWorldScaleButton));

    const cRectangle &lowPowerIconRect = rect(contentX, contentRowY(7), checkLabelWidth, buttonHeight);
    auto gui_LowPowerIconLabel = GuiLabelBuilder()
            .withLabel("Low power icon")
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

    const cRectangle &applyRect = relativeRect(menuLayout.apply);
    auto applyButton = GuiButtonBuilder()
            .withRect(applyRect)
            .withLabel("Apply")
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
            .withLabel("More settings")
            .withTextDrawer(m_textDrawer)
            .withRenderer(m_sdlDrawer)
            .withTheme(GuiTheme::RemasterInactive())
            .withKind(buttonKind)
            .withEnabled(false)
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

void cOptionsState::updateScaleControls()
{
    const int outputW = m_settings->getOutputW();
    const int outputH = m_settings->getOutputH();
    const int renderScale = m_renderScaleChoices[m_selectedRenderScaleIndex];
    const int worldScale = m_worldScaleChoices[m_selectedWorldScaleIndex];
    m_renderScaleValueLabel->setText(scaleChoiceText(renderScale, calculateAutomaticRenderScalePercent(outputW, outputH)));
    m_worldScaleValueLabel->setText(scaleChoiceText(worldScale, calculateAutomaticWorldScalePercent(outputH)));
    m_applyButton->setEnabled(
        renderScale != m_settings->getSavedRenderScalePercent() ||
        worldScale != m_settings->getSavedWorldScalePercent()
    );
}

void cOptionsState::applyScaleSettings()
{
    const int renderScale = m_renderScaleChoices[m_selectedRenderScaleIndex];
    const int worldScale = m_worldScaleChoices[m_selectedWorldScaleIndex];
    std::string error = "Could not get the user data directory";
    const auto prefsFile = PreferencesPath::file(Preferences::FILE_NAME);
    if (prefsFile && Preferences::saveScales(*prefsFile, renderScale, worldScale, error)) {
        m_settings->setSavedScalePercents(renderScale, worldScale);
        m_statusLabel->setText("Saved. Restart the game.");
    } else {
        Logger::warn(COMP_GAMERULES, "Preferences", "Could not save the scales: {}", error);
        m_statusLabel->setText("Could not save preferences.ini");
    }
    updateScaleControls();
}

cOptionsState::~cOptionsState()
{
    // Smart pointers handle cleanup
}

void cOptionsState::thinkFast()
{
}

void cOptionsState::draw() const
{
    if (m_backgroundTexture && *m_backgroundTexture) {
        m_sdlDrawer->renderSprite(*m_backgroundTexture,0,0);
    }
    m_guiWindow->draw();

    // MOUSE
    m_mouse->draw();
}

void cOptionsState::onNotifyMouseEvent(const s_MouseEvent &event)
{
    m_guiWindow->onNotifyMouseEvent(event);
}

eGameStateType cOptionsState::getType()
{
    return GAMESTATE_OPTIONS;
}

void cOptionsState::onNotifyKeyboardEvent(const cKeyboardEvent &)
{
}

/**
 * Reconstructs window so that it knows to which previous state it should go 'back to'
 * @param prevState
 */
void cOptionsState::setPrevState(int prevState)
{
    m_prevState = prevState;
    refresh();
}

void cOptionsState::refresh()
{
    m_guiWindow.reset();
    m_renderScaleValueLabel = nullptr;
    m_worldScaleValueLabel = nullptr;
    m_statusLabel = nullptr;
    m_applyButton = nullptr;
    constructWindow(m_prevState);
    m_backgroundTexture = nullptr;
}
