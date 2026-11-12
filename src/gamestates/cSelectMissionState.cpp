/**
 * @file cSelectMissionState.cpp
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

#include "cSelectMissionState.h"
#include "context/GameContext.hpp"
//#include "game/cGame.h"
#include "config.h"
#include "drawers/cTextDrawer.h"
#include "gui/GuiTheme.hpp"
#include "gui/GuiButton.h"
#include "gui/GuiWindow.h"
#include "game/GameStateTransition.hpp"
#include "game/MissionFlow.hpp"
#include "game/cGameSettings.h"
#include "game/CampaignProgress.hpp"
#include "controls/cMouse.h"
#include "context/cGameObjectContext.h"
#include "gameobjects/players/cPlayer.h"
#include "include/Texture.hpp"
#include "data/gfxinter.h"
#include "context/GraphicsContext.hpp"
#include "utils/Graphics.hpp"
#include "utils/HdUiTextureLoader.hpp"

#include "include/cAssert.h"
#include "context/TextContext.hpp"
#include "include/sGameServices.h"
#include "include/eGameState.h"
#include "utils/Localization.hpp"

#include <algorithm>
#include <format>

cSelectMissionState::cSelectMissionState(sGameServices* services, int prevState) :
    cGameState(services),
    m_textDrawer(m_ctx->getTextContext()->getBeneTextDrawer()),
    m_settings(services->settings),
    m_missionFlow(services->missionFlow),
    m_stateTransitions(services->stateTransitions),
    m_mouse(services->mouse)
{
    d2tm_assert(services != nullptr);
    d2tm_assert(m_stateTransitions != nullptr);
    cPlayer* humanPlayer = services->objects->getPlayer(HUMAN);
    const int house = humanPlayer->getHouse();
    Graphics* gfxinter = m_ctx->getGraphicsContext()->gfxinter.get();
    if (house == ATREIDES) {
        m_houseFlag = gfxinter->getTexture(BMP_SELECT_HOUSE_ATREIDES);
    } else if (house == HARKONNEN) {
        m_houseFlag = gfxinter->getTexture(BMP_SELECT_HOUSE_HARKONNEN);
    } else if (house == ORDOS) {
        m_houseFlag = gfxinter->getTexture(BMP_SELECT_HOUSE_ORDOS);
    } else if (house == SARDAUKAR) {
        m_houseFlag = gfxinter->getTexture(BMP_SELECT_HOUSE_SARDAUKAR);
    } else {
        m_houseFlag = humanPlayer->getFlagBitmap();
    }
    const int highestUnlockedMission = services->campaignProgress && CampaignProgress::supportsHouse(house)
        ? services->campaignProgress->highestUnlockedMission(house)
        : CampaignProgress::LAST_MISSION;
    const bool campaignCompleted = services->campaignProgress &&
        services->campaignProgress->nextMission(house) == CampaignProgress::COMPLETED;
    m_hdBackground = loadHdUiTexture(
        m_sdlDrawer->getRenderer(),
        "main_menu_background.png",
        "HD mission selection");

    const int mainMenuWidth = std::clamp(m_settings->getScreenW() - 64, 440, 600);
    const int mainMenuHeight = std::min(m_settings->getScreenH() - 64, 500);
    const int mainMenuFrameX = (m_settings->getScreenW() - mainMenuWidth) / 2;
    const int mainMenuFrameY = (m_settings->getScreenH() - mainMenuHeight) / 2;

    const cRectangle window(mainMenuFrameX, mainMenuFrameY, mainMenuWidth, mainMenuHeight);
    gui_window = std::make_unique<GuiWindow>(m_sdlDrawer, window, m_textDrawer);
    gui_window->setTheme(GuiTheme::Remaster());

    gui_window->setTitle(localization::format("{} Campaign", "Кампания: {}", humanPlayer->getHouseName()));

    constexpr int flagMaxWidth = 270;
    constexpr int flagMaxHeight = 220;
    const float flagScale = std::min(
        static_cast<float>(flagMaxWidth) / static_cast<float>(m_houseFlag->w),
        static_cast<float>(flagMaxHeight) / static_cast<float>(m_houseFlag->h));
    m_flagWidth = static_cast<int>(static_cast<float>(m_houseFlag->w) * flagScale);
    m_flagHeight = static_cast<int>(static_cast<float>(m_houseFlag->h) * flagScale);
    m_flagX = mainMenuFrameX + (320 - m_flagWidth) / 2;
    m_flagY = mainMenuFrameY + 65 + (230 - m_flagHeight) / 2;

    const int buttonHeight = std::max(30, m_textDrawer->getFontHeight() + 12);
    const int buttonWidth = 270;
    const int leftButtonX = mainMenuFrameX + 25;
    const int rightButtonX = mainMenuFrameX + mainMenuWidth - 25 - buttonWidth;
    m_headerX = rightButtonX;
    m_headerWidth = buttonWidth;
    m_headerY = mainMenuFrameY + 42;
    const int missionButtonY = mainMenuFrameY + 62;
    const int missionButtonHeight = 34;
    const int missionButtonSpacing = 38;

    auto continueButton = GuiButtonBuilder()
        .withRect(cRectangle(leftButtonX, mainMenuFrameY + 340, buttonWidth, buttonHeight))
        .withLabel(localization::text("CONTINUE", "ПРОДОЛЖИТЬ"))
        .withTextDrawer(m_textDrawer)
        .withRenderer(m_sdlDrawer)
        .withTheme(GuiTheme::Remaster())
        .withKind(GuiRenderKind::REMASTER_BUTTON)
        .onClick([this, campaignCompleted, highestUnlockedMission]() {
            if (campaignCompleted) {
                return;
            }
            m_missionFlow->jumpToSelectYourNextConquest(highestUnlockedMission);
            m_stateTransitions->setNextStateWithFade(
                highestUnlockedMission == CampaignProgress::FIRST_MISSION ? GAME_BRIEFING : GAME_REGION);
        })
        .build();
    gui_window->addGuiObject(std::move(continueButton));

    for (int i = 1; i <= highestUnlockedMission; i++) {
        auto btnMission = GuiButtonBuilder()
            .withRect(cRectangle(
                rightButtonX,
                missionButtonY + (i - 1) * missionButtonSpacing,
                buttonWidth,
                missionButtonHeight))
            .withLabel(localization::format("MISSION {}", "МИССИЯ {}", i))
            .withTextDrawer(m_textDrawer)
            .withRenderer(m_sdlDrawer)
            .withTheme(GuiTheme::Remaster())
            .withKind(GuiRenderKind::REMASTER_BUTTON)
            .onClick([this, i]() {
                m_missionFlow->jumpToSelectYourNextConquest(i);
                m_stateTransitions->setNextStateWithFade(i == CampaignProgress::FIRST_MISSION ? GAME_BRIEFING : GAME_REGION);
            })
            .build();
        gui_window->addGuiObject(std::move(btnMission));
    }

    const int backButtonHeight = std::max(36, m_textDrawer->getFontHeight() + 10);
    const cRectangle backRect = gui_window->getRelativeRect(
        8,
        mainMenuHeight - (backButtonHeight + 8),
        mainMenuWidth - 16 - 8,
        backButtonHeight);
    auto gui_btn_Back = GuiButtonBuilder()
            .withRect(backRect)
            .withLabel(localization::text("Back", "Назад"))
            .withTextDrawer(m_textDrawer)
            .withRenderer(m_sdlDrawer)
            .withTheme(GuiTheme::Remaster())
            .withKind(GuiRenderKind::REMASTER_BUTTON)
            .onClick([this,prevState]() {
                m_stateTransitions->setNextState(prevState);
            })
            .build();
    gui_window->addGuiObject(std::move(gui_btn_Back));
}

cSelectMissionState::~cSelectMissionState()
{
    delete m_hdBackground;
}

void cSelectMissionState::thinkFast()
{

}

void cSelectMissionState::draw() const
{
    m_sdlDrawer->renderClearToColor(Color{10, 12, 14, 255});
    if (m_hdBackground) {
        const float sourceAspect = static_cast<float>(m_hdBackground->w) /
            std::max(1, m_hdBackground->h);
        const float screenAspect = static_cast<float>(m_settings->getScreenW()) /
            std::max(1, m_settings->getScreenH());
        cRectangle destination;
        if (sourceAspect > screenAspect) {
            const int width = static_cast<int>(m_settings->getScreenH() * sourceAspect);
            destination = cRectangle(
                (m_settings->getScreenW() - width) / 2,
                0,
                width,
                m_settings->getScreenH());
        } else {
            const int height = static_cast<int>(m_settings->getScreenW() / sourceAspect);
            destination = cRectangle(
                0,
                (m_settings->getScreenH() - height) / 2,
                m_settings->getScreenW(),
                height);
        }
        m_sdlDrawer->renderStrechFullSprite(m_hdBackground, destination);
        m_sdlDrawer->renderRectFillColor(
            0,
            0,
            m_settings->getScreenW(),
            m_settings->getScreenH(),
            Color{3, 6, 8, 150});
    }

    gui_window->draw();
    m_sdlDrawer->renderTexture(
        m_houseFlag->tex.get(), m_flagX, m_flagY, m_flagWidth, m_flagHeight);
    m_textDrawer->drawTextCentered(
        localization::text("REPLAY MISSION", "ПОВТОРИТЬ МИССИЮ"),
        m_headerX,
        m_headerWidth,
        m_headerY,
        Color::Yellow);

    // MOUSE
    m_mouse->draw();
}

void cSelectMissionState::onNotifyMouseEvent(const s_MouseEvent &event)
{
    gui_window->onNotifyMouseEvent(event);
}

eGameStateType cSelectMissionState::getType()
{
    return GAMESTATE_SELECT_MISSION;
}

void cSelectMissionState::onNotifyKeyboardEvent(const cKeyboardEvent &)
{
}
