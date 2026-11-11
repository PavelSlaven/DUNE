#include "debug/UiAudit.hpp"

#include "game/cGame.h"
#include "game/cGameSettings.h"
#include "game/cScreenFader.h"
#include "game/cTimeManager.h"
#include "gamestates/cGameState.h"

int UiAuditAccess::state(const cGame &currentGame)
{
    return currentGame.m_currentState == nullptr ? -1 : static_cast<int>(currentGame.m_currentState->getType());
}

const cGameState *UiAuditAccess::currentState(const cGame &currentGame)
{
    return currentGame.m_currentState;
}

SDL_Renderer *UiAuditAccess::renderer(cGame &currentGame)
{
    return currentGame.renderer;
}

int UiAuditAccess::renderScale(const cGame &currentGame)
{
    return currentGame.m_gameSettings->m_renderScalePercent;
}

int UiAuditAccess::worldScale(const cGame &currentGame)
{
    return currentGame.m_gameSettings->m_worldScalePercent;
}

void UiAuditAccess::setState(cGame &currentGame, int state)
{
    currentGame.setState(state);
}

void UiAuditAccess::freezeClock(cGame &currentGame)
{
    currentGame.m_timeManager->onWindowFocusLost();
}

void UiAuditAccess::resumeClock(cGame &currentGame)
{
    currentGame.m_timeManager->onWindowFocusGained();
}

// drawState restarts the fade-in every idle frame and the fade-in does not change the picture; only a fade-out does.
bool UiAuditAccess::notFadingOut(const cGame &currentGame)
{
    return currentGame.m_cScreenFader->getAction() != eFadeAction::FadeOut;
}
