#include "debug/UiAudit.hpp"

#include "game/cGame.h"
#include "game/CampaignProgress.hpp"
#include "game/cGameSettings.h"
#include "game/cScreenFader.h"
#include "game/cTimeManager.h"
#include "context/cGameObjectContext.h"
#include "drawers/cTextDrawer.h"
#include "gameobjects/players/cPlayer.h"
#include "gui/GuiLabel.hpp"
#include "gamestates/cCreditsState.h"
#include "gamestates/cGameState.h"
#include "gamestates/cMentatState.h"
#include "gamestates/cOptionsState.h"
#include "gamestates/cSelectYourNextConquestState.h"
#include "gamestates/cSetupSkirmishState.h"
#include "gamestates/cTellHouseState.h"
#include "include/eGameState.h"
#include "include/sDataCampaign.h"
#include "managers/cDrawManager.h"

#include <vector>

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

void UiAuditAccess::setHouse(cGame &currentGame, int house)
{
    currentGame.m_gameObjectsContext->getPlayer(HUMAN)->setHouse(house);
    currentGame.m_dataCampaign->housePlayer = house;
}

bool UiAuditAccess::prepareMentatScene(cGame &currentGame, int house, int kind)
{
    setHouse(currentGame, house);
    currentGame.m_dataCampaign->mission = CampaignProgress::FIRST_MISSION;
    currentGame.m_dataCampaign->region = 1;
    if (kind == 0) {
        currentGame.setNextStateToTransitionTo(GAME_BRIEFING);
        currentGame.transitionStateIfRequired();
    }
    else {
        currentGame.setState(kind == 1 ? GAME_WINBRIEF : GAME_LOSEBRIEF);
    }
    auto *mentatState = dynamic_cast<cMentatState *>(currentGame.m_currentState);
    return mentatState != nullptr && mentatState->m_mentat != nullptr;
}

bool UiAuditAccess::mentatFreeze(cGame &currentGame, bool awaiting)
{
    AbstractMentat *mentat = nullptr;
    if (auto *mentatState = dynamic_cast<cMentatState *>(currentGame.m_currentState)) {
        mentat = mentatState->m_mentat.get();
    }
    else if (auto *tellHouseState = dynamic_cast<cTellHouseState *>(currentGame.m_currentState)) {
        mentat = tellHouseState->m_mentat.get();
    }
    if (mentat == nullptr) {
        return false;
    }
    if (awaiting) {
        mentat->state = AWAITING_RESPONSE;
        return true;
    }
    int bestPair = 0;
    std::size_t bestLength = 0;
    for (int pair = 0; pair <= 8; pair += 2) {
        const std::size_t length = mentat->sentence[pair].size() + mentat->sentence[pair + 1].size();
        if (length > bestLength) {
            bestLength = length;
            bestPair = pair;
        }
    }
    mentat->iMentatSentence = bestPair;
    mentat->TIMER_Speaking = 1 << 20;
    mentat->state = SPEAKING;
    return bestLength > 0;
}

bool UiAuditAccess::prepareSkirmish(cGame &currentGame, int variant)
{
    currentGame.setState(GAME_SETUPSKIRMISH);
    auto *setup = dynamic_cast<cSetupSkirmishState *>(currentGame.m_currentState);
    if (setup == nullptr) {
        return false;
    }
    setup->iSkirmishMap = variant == 0 ? 0 : 1;
    if (variant == 1) {
        setup->iStartingPoints = 4;
        setup->skirmishPlayer[2].bPlaying = true;
        setup->skirmishPlayer[3].bPlaying = true;
    }
    return true;
}

bool UiAuditAccess::optionsStatus(cGame &currentGame)
{
    auto *options = dynamic_cast<cOptionsState *>(currentGame.m_currentState);
    if (options == nullptr || options->m_statusLabel == nullptr) {
        return false;
    }
    options->m_statusLabel->setText("Saved. Restart the game.");
    return true;
}

bool UiAuditAccess::creditsScroll(cGame &currentGame, int frame)
{
    auto *credits = dynamic_cast<cCreditsState *>(currentGame.m_currentState);
    if (credits == nullptr) {
        return false;
    }
    credits->m_moveSpeed = 0;
    if (frame == 0) {
        credits->m_crawlerY = 64;
        return true;
    }
    const int fontHeight = credits->m_textDrawer->getFontHeight();
    const int limit = currentGame.m_gameSettings->getScreenH() - 128;
    std::vector<int> offsets;
    std::vector<bool> visible;
    int offset = credits->m_titleHeight;
    for (const s_CreditLine &line : credits->m_lines) {
        offsets.push_back(offset);
        visible.push_back(!line.name.empty() || !line.txt.empty());
        offset += line.height;
    }
    int group = 0;
    std::size_t index = 0;
    std::size_t lastStart = 0;
    while (index < offsets.size()) {
        if (!visible[index]) {
            ++index;
            continue;
        }
        const std::size_t start = index;
        lastStart = start;
        while (index < offsets.size() &&
               (!visible[index] || offsets[index] + fontHeight - offsets[start] <= limit)) {
            ++index;
        }
        if (++group == frame) {
            credits->m_crawlerY = static_cast<float>(64 - offsets[start]);
            return true;
        }
    }
    if (group == 0) {
        return false;
    }
    // A tall canvas holds fewer groups; the scene must still exist, so it shows the last group.
    credits->m_crawlerY = static_cast<float>(64 - offsets[lastStart]);
    return true;
}

void UiAuditAccess::recordCreditLines(cGame &currentGame)
{
    auto *credits = dynamic_cast<cCreditsState *>(currentGame.m_currentState);
    if (credits == nullptr) {
        return;
    }
    for (const s_CreditLine &line : credits->m_lines) {
        if (!line.name.empty() || !line.txt.empty()) {
            uiaudit::recordCreditLine(line.name, line.txt);
        }
    }
}

void UiAuditAccess::regionOpen(cGame &currentGame, int mission, bool jump)
{
    if (jump) {
        currentGame.jumpToSelectYourNextConquestMission(mission);
    }
    else {
        currentGame.m_dataCampaign->mission = mission;
    }
    currentGame.setState(GAME_REGION);
}

int UiAuditAccess::regionState(const cGame &currentGame)
{
    auto *region = dynamic_cast<const cSelectYourNextConquestState *>(currentGame.m_currentState);
    return region == nullptr ? -1 : static_cast<int>(region->state);
}

int UiAuditAccess::regionScene(const cGame &currentGame)
{
    auto *region = dynamic_cast<const cSelectYourNextConquestState *>(currentGame.m_currentState);
    return region == nullptr ? -1 : static_cast<int>(region->regionSceneState);
}

int UiAuditAccess::regionSceneAlpha(const cGame &currentGame)
{
    auto *region = dynamic_cast<const cSelectYourNextConquestState *>(currentGame.m_currentState);
    return region == nullptr ? -1 : region->iRegionSceneAlpha;
}

bool UiAuditAccess::hasMessage(const cGame &currentGame)
{
    return currentGame.m_drawManager->hasMessage();
}
