/**
 * @file cChooseHouseState.cpp
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

#include "include/definitions.h"
#include "gamestates/cChooseHouseState.h"
#include "game/cGameSettings.h"
#include "controls/eKeyAction.h"
#include "data/gfxinter.h"
#include "drawers/SDLDrawer.hpp"
#include "utils/Graphics.hpp"
#include "include/Texture.hpp"
#include "context/GameContext.hpp"
#include "context/GraphicsContext.hpp"
#include "drawers/cTextDrawer.h"
#include "game/GameStateTransition.hpp"
#include "game/MentatFlow.hpp"
#include "controls/cMouse.h"
#include "include/cAssert.h"
#include "context/TextContext.hpp"
#include "include/sGameServices.h"
#include "include/eGameState.h"

#include "utils/HdUiTextureLoader.hpp"

#include <algorithm>
#include <string>

cChooseHouseState::cChooseHouseState(sGameServices* services) :
    cGameState(services),
    m_settings(services->settings),
    m_textDrawer(m_ctx->getTextContext()->getBeneTextDrawer()),
    m_gfxinter(m_ctx->getGraphicsContext()->gfxinter.get()),
    m_stateTransitions(services->stateTransitions),
    m_mentatFlow(services->mentatFlow),
    m_mouse(services->mouse)
{
    d2tm_assert(m_textDrawer != nullptr);
    d2tm_assert(m_gfxinter != nullptr);
    d2tm_assert(m_stateTransitions != nullptr);
    d2tm_assert(m_mentatFlow != nullptr);
    d2tm_assert(m_mouse != nullptr);
    d2tm_assert(m_settings != nullptr);

    bmp_HouseAtreides = m_gfxinter->getTexture(BMP_SELECT_HOUSE_ATREIDES);
    bmp_HouseOrdos = m_gfxinter->getTexture(BMP_SELECT_HOUSE_ORDOS);
    bmp_HouseHarkonnen = m_gfxinter->getTexture(BMP_SELECT_HOUSE_HARKONNEN);
    bmp_HouseSardaukar = m_gfxinter->getTexture(BMP_SELECT_HOUSE_SARDAUKAR);

    m_hdBackground = loadHdUiTexture(
        m_sdlDrawer->getRenderer(),
        "main_menu_background.png",
        "HD house selection");

    const int gap = std::clamp(m_settings->getScreenW() / 48, 16, 32);
    const int horizontalMargin = std::clamp(m_settings->getScreenW() / 24, 28, 72);
    const int availableCardWidth = (
        m_settings->getScreenW() - horizontalMargin * 2 - gap * 3) / 4;
    const int cardWidth = std::clamp(availableCardWidth, 160, 420);
    const int cardsWidth = cardWidth * 4 + gap * 3;
    const int firstX = (m_settings->getScreenW() - cardsWidth) / 2;
    const int cardsY = std::clamp(m_settings->getScreenH() / 6, 96, 150);
    const int backHeight = 46;
    const int backY = m_settings->getScreenH() - backHeight - 18;
    const int availableCardHeight = backY - cardsY - 26;
    const int preferredCardHeight = std::clamp(
        m_settings->getScreenH() * 3 / 5, 320, 520);
    const int cardHeight = std::max(
        280, std::min(preferredCardHeight, availableCardHeight));

    houseAtreides = cRectangle(firstX, cardsY, cardWidth, cardHeight);
    houseOrdos = cRectangle(firstX + cardWidth + gap, cardsY, cardWidth, cardHeight);
    houseHarkonnen = cRectangle(firstX + (cardWidth + gap) * 2, cardsY, cardWidth, cardHeight);
    houseSardaukar = cRectangle(firstX + (cardWidth + gap) * 3, cardsY, cardWidth, cardHeight);

    const int backWidth = 240;
    backButtonRect = cRectangle(
        (m_settings->getScreenW() - backWidth) / 2,
        backY,
        backWidth,
        backHeight);

    hoversOverBackButton = false;
}

cChooseHouseState::~cChooseHouseState()
{
    delete m_hdBackground;
    m_hdBackground = nullptr;
    bmp_HouseAtreides = nullptr;
    bmp_HouseOrdos = nullptr;
    bmp_HouseHarkonnen = nullptr;
    bmp_HouseSardaukar = nullptr;
}

void cChooseHouseState::thinkFast()
{
}

void cChooseHouseState::draw() const
{
    drawHdBackground();

    const std::string title = "CHOOSE YOUR HOUSE";
    const int titleWidth = m_textDrawer->getTextLength(title);
    m_textDrawer->drawText(
        (m_settings->getScreenW() - titleWidth) / 2,
        48,
        Color{231, 190, 91, 255},
        title);

    drawHdHouseCard(houseAtreides, bmp_HouseAtreides, "ATREIDES");
    drawHdHouseCard(houseOrdos, bmp_HouseOrdos, "ORDOS");
    drawHdHouseCard(houseHarkonnen, bmp_HouseHarkonnen, "HARKONNEN");
    drawHdHouseCard(houseSardaukar, bmp_HouseSardaukar, "SARDAUKAR");

    m_sdlDrawer->renderRectFillColor(
        backButtonRect,
        hoversOverBackButton ? Color{43, 49, 53, 245} : Color{25, 31, 35, 245});
    m_sdlDrawer->renderRectColor(backButtonRect, Color{195, 142, 43, 255});
    const std::string backLabel = "Back";
    const int backLabelWidth = m_textDrawer->getTextLength(backLabel);
    m_textDrawer->drawText(
        backButtonRect.getX() + (backButtonRect.getWidth() - backLabelWidth) / 2,
        backButtonRect.getY() +
            (backButtonRect.getHeight() - m_textDrawer->getFontHeight()) / 2,
        hoversOverBackButton ? Color{255, 224, 139, 255} : Color{238, 229, 204, 255},
        backLabel);

    m_mouse->draw();
}

void cChooseHouseState::drawHdBackground() const
{
    m_sdlDrawer->renderClearToColor(Color{10, 12, 13, 255});
    if (!m_hdBackground) {
        return;
    }

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
        Color{3, 6, 8, 142});
}

void cChooseHouseState::drawHdHouseCard(
    const cRectangle &card,
    Texture *emblem,
    const std::string &name) const
{
    m_sdlDrawer->renderRectFillColor(
        card.getX() + 5,
        card.getY() + 6,
        card.getWidth(),
        card.getHeight(),
        Color{0, 0, 0, 150});
    m_sdlDrawer->renderRectFillColor(card, Color{21, 27, 31, 244});
    m_sdlDrawer->renderRectColor(card, Color{173, 125, 39, 255});
    m_sdlDrawer->renderRectColor(
        card.getX() + 4,
        card.getY() + 4,
        card.getWidth() - 8,
        card.getHeight() - 8,
        Color{102, 78, 35, 255});

    const int imageMaxWidth = card.getWidth() - 24;
    const int imageMaxHeight = card.getHeight() - 72;
    const float sourceAspect = static_cast<float>(emblem->w) /
        std::max(1, emblem->h);
    int imageWidth = imageMaxWidth;
    int imageHeight = std::max(1, static_cast<int>(imageWidth / sourceAspect));
    if (imageHeight > imageMaxHeight) {
        imageHeight = imageMaxHeight;
        imageWidth = std::max(1, static_cast<int>(imageHeight * sourceAspect));
    }
    const cRectangle source(0, 0, emblem->w, emblem->h);
    const cRectangle destination(
        card.getX() + (card.getWidth() - imageWidth) / 2,
        card.getY() + 12,
        imageWidth,
        imageHeight);
    m_sdlDrawer->renderStrechSprite(emblem, source, destination, 232);

    const int nameWidth = m_textDrawer->getTextLength(name);
    m_textDrawer->drawText(
        card.getX() + (card.getWidth() - nameWidth) / 2,
        card.getY() + card.getHeight() - m_textDrawer->getFontHeight() - 22,
        Color{238, 229, 204, 255},
        name);
}

eGameStateType cChooseHouseState::getType()
{
    return GAMESTATE_SELECT_YOUR_NEXT_CONQUEST;
}

void cChooseHouseState::onNotifyMouseEvent(const s_MouseEvent &event)
{
    switch (event.eventType) {
        case MOUSE_LEFT_BUTTON_CLICKED:
            onMouseLeftButtonClicked(event);
            break;
        case MOUSE_MOVED_TO:
            onMouseMoved(event);
            break;
        default:
            break;
    }
}

void cChooseHouseState::onMouseLeftButtonClicked(const s_MouseEvent &event) const
{

    if (event.coords.isWithinRectangle(&houseAtreides)) {
        m_mentatFlow->prepareToTellAboutHouse(ATREIDES);
    }
    else if (event.coords.isWithinRectangle(&houseOrdos)) {
        m_mentatFlow->prepareToTellAboutHouse(ORDOS);
    }
    else if (event.coords.isWithinRectangle(&houseHarkonnen)) {
        m_mentatFlow->prepareToTellAboutHouse(HARKONNEN);
    }
    else if (event.coords.isWithinRectangle(&houseSardaukar)) {
        m_mentatFlow->prepareToTellAboutHouse(SARDAUKAR);
    }
    else if (event.coords.isWithinRectangle(&backButtonRect)) {
        m_stateTransitions->setNextStateWithFade(GAME_MENU);
    }
}

void cChooseHouseState::onMouseMoved(const s_MouseEvent &event)
{
    hoversOverBackButton = event.coords.isWithinRectangle(&backButtonRect);
}

void cChooseHouseState::onNotifyKeyboardEvent(const cKeyboardEvent &event)
{
    if (event.isType(eKeyEventType::PRESSED)) {
        if (event.isAction(eKeyAction::MENU_BACK)) {
            m_stateTransitions->setNextStateWithFade(GAME_MENU);
        }
    }
}
