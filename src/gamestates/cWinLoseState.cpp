/**
 * @file cWinLoseState.cpp
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

#include "gamestates/cWinLoseState.h"

#include "data/gfxinter.h"
#include "drawers/SDLDrawer.hpp"
#include "drawers/cTextDrawer.h"
#include "utils/Graphics.hpp"
#include "utils/HdUiTextureLoader.hpp"
#include "utils/OutcomeScreenLayout.hpp"
#include "context/GameContext.hpp"
#include "game/GameStateTransition.hpp"
#include "game/MissionFlow.hpp"
#include "controls/cMouse.h"

#include <SDL3/SDL.h>
#include "include/cAssert.h"
#include "game/cGameSettings.h"
#include "gamestates/cGameState.h"
#include "include/Texture.hpp"
#include "include/sGameServices.h"
#include "context/GraphicsContext.hpp"
#include "include/eGameState.h"
#include "utils/Localization.hpp"

cWinLoseState::cWinLoseState(sGameServices* services, Outcome value) : 
    cGameState(services),
    m_settings(services->settings),
    m_textDrawer(m_ctx->getTextContext()->getBeneTextDrawer()),
    m_statement(value)
{
    d2tm_assert(services != nullptr);
    d2tm_assert(m_settings != nullptr);

    auto ctx = services->ctx;
    m_missionFlow = services->missionFlow;
    m_stateTransitions = services->stateTransitions;
    d2tm_assert(m_missionFlow != nullptr);
    d2tm_assert(m_stateTransitions != nullptr);
    m_mouse = services->mouse;
    d2tm_assert(m_mouse != nullptr);
    auto gfxinter = ctx->getGraphicsContext()->gfxinter;
    d2tm_assert(gfxinter != nullptr);

    const char *outcomeFile = m_statement == Outcome::Lose
        ? localization::text("outcome_defeat_en.png", "outcome_defeat_ru.png")
        : localization::text("outcome_victory_en.png", "outcome_victory_ru.png");
    m_hdOutcomeTexture = loadHdUiTexture(
        m_sdlDrawer->getRenderer(),
        outcomeFile,
        m_statement == Outcome::Lose ? "HD defeat screen" : "HD victory screen"
    );

    m_backgroundTexture = &services->screenTexture;
    
    if (m_statement == Outcome::Lose) {
        m_tex = gfxinter->getTexture(BMP_LOSING);
    } else {
        m_tex = gfxinter->getTexture(BMP_WINNING);
    }
}

cWinLoseState::~cWinLoseState()
{
    delete m_hdOutcomeTexture;
}

void cWinLoseState::thinkFast()
{
}

void cWinLoseState::draw() const
{
    if (m_hdOutcomeTexture) {
        const std::string prompt = localization::text("Click to continue", "Щёлкните, чтобы продолжить");
        const OutcomeScreenLayout layout = calculateOutcomeScreenLayout(
            m_settings->getScreenW(),
            m_settings->getScreenH(),
            m_hdOutcomeTexture->pixelW,
            m_hdOutcomeTexture->pixelH,
            m_textDrawer->getTextLength(prompt)
        );
        m_sdlDrawer->renderStrechFullSprite(m_hdOutcomeTexture, layout.image);
        m_textDrawer->drawTextScaledCenteredInBox(
            prompt,
            layout.prompt,
            layout.promptTextScale,
            Color{255, 224, 164, 255}
        );
    }
    else {
        if (m_backgroundTexture && *m_backgroundTexture) {
            m_sdlDrawer->renderSprite(*m_backgroundTexture, 0, 0);
        }

        const int posW = (m_settings->getScreenW() - m_tex->w) / 2;
        const int posH = (m_settings->getScreenH() - m_tex->h) / 2;
        m_sdlDrawer->renderSprite(m_tex, posW, posH);
    }

    m_mouse->draw();
}

void cWinLoseState::onNotifyMouseEvent(const s_MouseEvent &event)
{
    switch (event.eventType) {
        case MOUSE_LEFT_BUTTON_CLICKED:
            onMouseLeftButtonClicked(event);
            break;
        default:
            break;
    }
}

eGameStateType cWinLoseState::getType()
{
    return GAMESTATE_WINLOSE;
}

void cWinLoseState::onNotifyKeyboardEvent(const cKeyboardEvent &)
{
}

void cWinLoseState::onMouseLeftButtonClicked(const s_MouseEvent &) const
{
    if (m_statement == Outcome::Lose) {
        m_missionFlow->goingToWinLoseBrief(GAME_LOSEBRIEF);
    } else {
        m_stateTransitions->setNextState(GAME_SCORING);
    }
    // FADE OUT
    m_stateTransitions->fadeOut();
}
