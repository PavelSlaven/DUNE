/**
 * @file cMainMenuState.cpp
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

#include "cMainMenuState.h"
#include "controls/cMouse.h"

#include "gui/GuiButton.h"
#include "gui/GuiWindow.h"
#include "controls/eKeyAction.h"
#include "config.h"
#include "data/gfxinter.h"
#include "drawers/SDLDrawer.hpp"
#include "drawers/cTextDrawer.h"
#include "utils/Graphics.hpp"
#include "utils/HdUiTextureLoader.hpp"
#include "context/AudioContext.hpp"
#include "context/GameContext.hpp"
#include "utils/cSoundPlayer.h"
#include "game/GameStateTransition.hpp"
#include "game/MissionFlow.hpp"
#include "game/VideoFlow.hpp"

#include <SDL3/SDL.h>
#include <algorithm>
#include <filesystem>
#include <format>
#include <functional>
#include <string>
#include <utility>
#include "include/cAssert.h"
#include "context/GraphicsContext.hpp"
#include "context/TextContext.hpp"
#include "game/cGameSettings.h"
#include "gamestates/cGameState.h"
#include "include/Texture.hpp"
#include "include/sGameServices.h"
#include "include/eGameState.h"

cMainMenuState::cMainMenuState(sGameServices* services) :
    cGameState(services),
    m_settings(services->settings),
    m_textDrawer(m_ctx->getTextContext()->getBeneTextDrawer()),
    m_missionFlow(services->missionFlow),
    m_videoFlow(services->videoFlow),
    m_stateTransitions(services->stateTransitions),
    m_mouse(services->mouse)
{
    d2tm_assert(m_settings != nullptr);
    d2tm_assert(m_textDrawer != nullptr);
    d2tm_assert(m_missionFlow != nullptr);
    d2tm_assert(m_videoFlow != nullptr);
    d2tm_assert(m_stateTransitions != nullptr);
    d2tm_assert(m_mouse != nullptr);
    auto *gfxinter = m_ctx->getGraphicsContext()->gfxinter.get();
    bmp_D2TM_Title = gfxinter->getTexture(BMP_D2TM);
    buildHdMenu();

    // prepare to drawing in cache texture
    if (m_settings->isDebugMode()) {
        backGroundDebug.reset(m_sdlDrawer->createRenderTargetTexture(m_settings->getScreenW(), m_settings->getScreenH()));
        m_sdlDrawer->beginDrawingToTexture(backGroundDebug.get());
        for (int x = 0; x < m_settings->getScreenW(); x += 60) {
            for (int y = 0; y < m_settings->getScreenH(); y += 20) {
                m_textDrawer->drawText(x, y, Color{48, 48, 48,255}, "DEBUG");
            }
        }
        m_sdlDrawer->endDrawingToTexture();
    }
}

cMainMenuState::~cMainMenuState()
{
    delete m_hdMenuBackground;
    delete m_hdMenuLogo;
}

void cMainMenuState::buildHdMenu()
{
    m_hdMenuBackground = loadHdUiTexture(
        m_sdlDrawer->getRenderer(),
        "main_menu_background.png",
        "HD main menu"
    );
    m_hdMenuLogo = loadHdUiTexture(
        m_sdlDrawer->getRenderer(),
        "main_menu_logo.png",
        "HD main menu"
    );

    const int buttonCount = 8;
    const int buttonWidth = std::clamp(m_settings->getScreenW() / 4, 280, 360);
    const int buttonHeight = std::clamp(m_settings->getScreenH() / 15, 40, 48);
    const int buttonGap = std::clamp(m_settings->getScreenH() / 90, 6, 10);
    const int panelPadding = 16;
    const int panelWidth = buttonWidth + panelPadding * 2;
    const int panelHeight = buttonCount * buttonHeight +
        (buttonCount - 1) * buttonGap + panelPadding * 2;
    const int panelX = (m_settings->getScreenW() - panelWidth) / 2;
    const int panelY = std::clamp(
        (m_settings->getScreenH() - panelHeight) / 2 + 28,
        132,
        std::max(132, m_settings->getScreenH() - panelHeight - 46));

    mainMenuFrameX = panelX;
    mainMenuFrameY = panelY;
    mainMenuWidth = panelWidth;
    mainMenuHeight = panelHeight;

    const int sourceLogoWidth = m_hdMenuLogo ? m_hdMenuLogo->w : bmp_D2TM_Title->w;
    const int sourceLogoHeight = m_hdMenuLogo ? m_hdMenuLogo->h : bmp_D2TM_Title->h;
    const int logoWidth = std::clamp(m_settings->getScreenW() * 2 / 5, 310, 430);
    const int logoHeight = std::max(1, logoWidth * sourceLogoHeight / std::max(1, sourceLogoWidth));
    logoX = (m_settings->getScreenW() - logoWidth) / 2;
    logoY = std::max(24, panelY - logoHeight - 24);
    m_logoRect = cRectangle(logoX, logoY, logoWidth, logoHeight);

    gui_window = std::make_unique<GuiWindow>(
        m_sdlDrawer,
        cRectangle(panelX, panelY, panelWidth, panelHeight),
        m_textDrawer);
    gui_window->setTheme(GuiTheme::Remaster());

    const int buttonX = panelX + panelPadding;
    int buttonY = panelY + panelPadding;
    const auto addButton = [this, buttonX, buttonWidth, buttonHeight, buttonGap, &buttonY](
        const std::string &label,
        bool enabled,
        std::function<void()> onClick) {
        auto button = GuiButtonBuilder()
            .withRect(cRectangle(buttonX, buttonY, buttonWidth, buttonHeight))
            .withLabel(label)
            .withTextDrawer(m_textDrawer)
            .withRenderer(m_sdlDrawer)
            .withTheme(enabled ? GuiTheme::Remaster() : GuiTheme::RemasterInactive())
            .withKind(GuiRenderKind::REMASTER_BUTTON)
            .withEnabled(enabled)
            .onClick(std::move(onClick))
            .build();
        gui_window->addGuiObject(std::move(button));
        buttonY += buttonHeight + buttonGap;
    };

    addButton("Campaign", true, [this]() {
        m_stateTransitions->setNextStateWithFade(GAME_SELECT_HOUSE);
    });
    addButton("Skirmish", true, [this]() {
        m_missionFlow->init();
        m_stateTransitions->setNextStateWithFade(GAME_SETUPSKIRMISH);
    });
    addButton("Load", true, [this]() { m_stateTransitions->fadeOut(); });
    addButton("Map Editor", true, [this]() {
        m_stateTransitions->setNextStateWithFade(GAME_NEW_MAP_EDITOR);
    });
    addButton("Options", true, [this]() {
        m_stateTransitions->setNextState(GAME_OPTIONS);
    });
    addButton("Hall of Fame", true, [this]() { m_stateTransitions->fadeOut(); });

    const std::string introMoviePack = "intro.pak";
    const bool hasIntroMoviePack = std::filesystem::exists(introMoviePack);
    addButton("Introduction", hasIntroMoviePack, [this, introMoviePack]() {
        m_videoFlow->play(introMoviePack);
    });
    addButton("Exit", true, [this]() {
        m_settings->setPlaying(false);
        m_stateTransitions->fadeOut();
    });

    gui_btn_credits = GuiButtonBuilder()
        .withRect(cRectangle(m_settings->getScreenW() - 132 - 18, 16, 132, 34))
        .withLabel("CREDITS")
        .withTextDrawer(m_textDrawer)
        .withRenderer(m_sdlDrawer)
        .withTheme(GuiTheme::Remaster())
        .withKind(GuiRenderKind::REMASTER_BUTTON)
        .onClick([this]() {
            m_stateTransitions->setNextStateWithFade(GAME_CREDITS);
        })
        .build();
}

void cMainMenuState::drawHdBackground() const
{
    m_sdlDrawer->renderClearToColor(Color{10, 12, 14, 255});
    if (!m_hdMenuBackground) {
        return;
    }

    m_sdlDrawer->renderStrechFullSprite(
        m_hdMenuBackground,
        cRectangle(0, 0, m_settings->getScreenW(), m_settings->getScreenH()),
        90);

    const float backgroundAspect = static_cast<float>(m_hdMenuBackground->w) /
        std::max(1, m_hdMenuBackground->h);
    const float screenAspect = static_cast<float>(m_settings->getScreenW()) /
        std::max(1, m_settings->getScreenH());

    int drawWidth = m_settings->getScreenW();
    int drawHeight = m_settings->getScreenH();
    if (screenAspect > 2.2f) {
        drawHeight = m_settings->getScreenH();
        drawWidth = static_cast<int>(drawHeight * backgroundAspect);
    } else if (screenAspect > backgroundAspect) {
        drawWidth = m_settings->getScreenW();
        drawHeight = static_cast<int>(drawWidth / backgroundAspect);
    } else {
        drawHeight = m_settings->getScreenH();
        drawWidth = static_cast<int>(drawHeight * backgroundAspect);
    }

    m_sdlDrawer->renderStrechFullSprite(
        m_hdMenuBackground,
        cRectangle((m_settings->getScreenW() - drawWidth) / 2,
                   (m_settings->getScreenH() - drawHeight) / 2,
                   drawWidth,
                   drawHeight));
}

void cMainMenuState::thinkFast()
{
}

void cMainMenuState::draw() const
{
    drawHdBackground();

    if (m_settings->isDebugMode()) {
        m_sdlDrawer->renderSprite(backGroundDebug.get(),0,0);
    }

    m_sdlDrawer->renderStrechFullSprite(
        m_hdMenuLogo ? m_hdMenuLogo : bmp_D2TM_Title,
        m_logoRect);

    gui_window->draw();
    gui_btn_credits->draw();

    m_textDrawer->drawTextBottomRight(
        Color{220, 213, 188, 230},
        D2TM_VERSION,
        18);
    m_textDrawer->drawText(
        18,
        m_settings->getScreenH() - m_textDrawer->getFontHeight() - 22,
        D2TM_BUILD_DATETIME);

    if (m_settings->isDebugMode()) {
        m_textDrawer->drawText(0, 0, std::format("{}, {}", m_mouse->getX(), m_mouse->getY()).c_str());
    }

    // MOUSE
    m_mouse->draw();

}

void cMainMenuState::onNotifyMouseEvent(const s_MouseEvent &event)
{
    gui_window->onNotifyMouseEvent(event);
    gui_btn_credits->onNotifyMouseEvent(event);
}

eGameStateType cMainMenuState::getType()
{
    return GAMESTATE_MAIN_MENU;
}

void cMainMenuState::onNotifyKeyboardEvent(const cKeyboardEvent &event)
{
    if (event.isType(eKeyEventType::PRESSED)) {
        if (event.isAction(eKeyAction::MENU_BACK)) {
            m_settings->setPlaying(false);
        }

        if (event.isAction(eKeyAction::TOGGLE_MUSIC) || event.hasKey(SDL_SCANCODE_MUTE)) {
            auto m_soundPlayer = m_ctx->getAudioContext()->getSoundPlayer();
            m_settings->setPlayMusic(!m_settings->isPlayMusic());
            if (!m_settings->isPlayMusic()) {
                m_soundPlayer->stopMusic();
            }
        }
    }
}
