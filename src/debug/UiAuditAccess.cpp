#include "debug/UiAudit.hpp"

#include "game/cGame.h"
#include "game/CampaignProgress.hpp"
#include "game/cGameSettings.h"
#include "game/cScreenFader.h"
#include "game/cTimeManager.h"
#include "context/cInfoContext.h"
#include "context/cGameObjectContext.h"
#include "drawers/cBuildingListDrawer.h"
#include "drawers/cSideBarDrawer.h"
#include "drawers/cTextDrawer.h"
#include "gameobjects/map/MapGeometry.hpp"
#include "gameobjects/map/cMap.h"
#include "gameobjects/map/cMapCamera.h"
#include "gameobjects/players/cPlayer.h"
#include "gameobjects/structures/cStructureFactory.h"
#include "gameobjects/units/cUnit.h"
#include "gameobjects/units/cUnitInfos.h"
#include "gameobjects/units/cUnits.h"
#include "gui/GuiLabel.hpp"
#include "gamestates/cCreditsState.h"
#include "gamestates/cGameState.h"
#include "gamestates/cMentatState.h"
#include "gamestates/cOptionsState.h"
#include "gamestates/cSelectYourNextConquestState.h"
#include "gamestates/cSetupSkirmishState.h"
#include "gamestates/cTellHouseState.h"
#include "include/definitions.h"
#include "include/eGameState.h"
#include "include/sDataCampaign.h"
#include "managers/cDrawManager.h"
#include "sidebar/HudLayout.hpp"
#include "sidebar/cBuildingList.h"
#include "sidebar/cSideBar.h"
#include "utils/cRectangle.h"

#include <algorithm>
#include <cstdlib>
#include <string>
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

bool UiAuditAccess::mapViewport(const cGame &currentGame, int &x, int &y, int &w, int &h)
{
    if (!currentGame.m_mapViewport) {
        return false;
    }
    x = currentGame.m_mapViewport->getX();
    y = currentGame.m_mapViewport->getY();
    w = currentGame.m_mapViewport->getWidth();
    h = currentGame.m_mapViewport->getHeight();
    return true;
}

void UiAuditAccess::stopCameraEdgeMove(cGame &currentGame)
{
    if (currentGame.m_mapCamera != nullptr) {
        currentGame.m_mapCamera->m_cameraEdgeMove = false;
        currentGame.m_mapCamera->m_moveX = 0.0f;
        currentGame.m_mapCamera->m_moveY = 0.0f;
    }
}

void UiAuditAccess::missionOutcome(cGame &currentGame, bool victory)
{
    currentGame.m_missionWasWon = victory;
    currentGame.setState(victory ? GAME_WINNING : GAME_LOSING);
    currentGame.takeBackGroundScreen();
}

void UiAuditAccess::recordSidebarClicks(cSideBarDrawer &drawer)
{
    cSideBar *sidebar = drawer.m_sidebar;
    if (sidebar == nullptr) {
        return;
    }
    const int selected = sidebar->getSelectedListID();
    for (int i = eListTypeAsInt(eListType::LIST_CONSTYARD); i < cSideBar::LIST_MAX; i++) {
        if (i == selected) {
            continue;
        }
        cBuildingList *list = sidebar->getList(i);
        if (list == nullptr || !list->isAvailable()) {
            continue;
        }
        uiaudit::recordClick(("list-button:" + std::to_string(i)).c_str(),
                             list->getButtonDrawX(), list->getButtonDrawY(),
                             list->getButtonWidth(), list->getButtonHeight());
    }

    if (selected >= 0 && selected < cSideBar::LIST_MAX) {
        cBuildingList *list = sidebar->getList(selected);
        if (list != nullptr && list->isAvailable()) {
            cBuildingListDrawer &items = drawer.m_buildingListDrawer;
            const HudLayout layout = items.getLayout(list);
            const int scrollRow = items.getScrollRow(list);
            for (int i = 0; i < list->getItemCount(); ++i) {
                if (list->getItem(i) == nullptr) {
                    continue;
                }
                const cRectangle card = layout.cardRect(i, scrollRow);
                if (card.getY() < layout.cards.getY() || card.getEndY() > layout.cards.getEndY()) {
                    continue;
                }
                uiaudit::recordClick(("build-item:" + std::to_string(i)).c_str(),
                                     card.getX(), card.getY(), card.getWidth(), card.getHeight());
            }
            uiaudit::recordClick("build-scrollbar", layout.scrollbar.getX(), layout.scrollbar.getY(),
                                 layout.scrollbar.getWidth(), layout.scrollbar.getHeight());
        }
    }
}

namespace {

constexpr int kTile = 32;
constexpr int kStartStep = 4;
constexpr int kStartMargin = 8;

struct MapView {
    int firstColumn = 0;
    int firstRow = 0;
    int columns = 0;
    int rows = 0;
};

bool aimCamera(cGame &currentGame, int startColumn, int startRow, MapView &view, bool relaxed)
{
    currentGame.m_mapCamera->setViewportPosition(startColumn * kTile, startRow * kTile);
    if (currentGame.m_mapCamera->getViewportStartX() != startColumn * kTile ||
        currentGame.m_mapCamera->getViewportStartY() != startRow * kTile) {
        return false;
    }
    const int tile = static_cast<int>(currentGame.m_mapCamera->factorZoomLevel(kTile));
    if (tile <= 0) {
        return false;
    }
    view.firstColumn = startColumn;
    view.firstRow = startRow;
    view.columns = currentGame.m_mapViewport->getWidth() / tile;
    view.rows = currentGame.m_mapViewport->getHeight() / tile;
    if (relaxed) {
        view.columns = std::min(view.columns,
                                currentGame.m_gameObjectsContext->getMap()->getGeometry()->getWidth() - view.firstColumn - 3);
        view.rows = std::min(view.rows,
                             currentGame.m_gameObjectsContext->getMap()->getGeometry()->getHeight() - view.firstRow - 3);
    }
    return view.columns >= 8 && view.rows >= 8 &&
           view.firstColumn + view.columns + 2 < currentGame.m_gameObjectsContext->getMap()->getGeometry()->getWidth() &&
           view.firstRow + view.rows + 2 < currentGame.m_gameObjectsContext->getMap()->getGeometry()->getHeight();
}

bool unitFits(cGame &currentGame, int cell, int unitType)
{
    if (!currentGame.m_gameObjectsContext->getMap()->getGeometry()->isValidCell(cell)) {
        return false;
    }
    const bool air = currentGame.m_infoContext->getUnitInfo(unitType).airborn;
    if (!air && currentGame.m_gameObjectsContext->getMap()->cellGetIdFromLayer(cell, MAPID_STRUCTURES) > -1) {
        return false;
    }
    const int layer = air ? MAPID_AIR : MAPID_UNITS;
    if (currentGame.m_gameObjectsContext->getMap()->cellGetIdFromLayer(cell, layer) > -1) {
        return false;
    }
    return currentGame.m_gameObjectsContext->getMap()->canDeployUnitTypeAtCell(cell, unitType);
}

int cellAt(cGame &currentGame, int column, int row)
{
    return row * currentGame.m_gameObjectsContext->getMap()->getGeometry()->getWidth() + column;
}

void revealAround(cGame &currentGame, int column, int row, int radius)
{
    for (int y = row - radius; y <= row + radius; y++) {
        for (int x = column - radius; x <= column + radius; x++) {
            if (x < 0 || y < 0 || x >= currentGame.m_gameObjectsContext->getMap()->getGeometry()->getWidth() ||
                y >= currentGame.m_gameObjectsContext->getMap()->getGeometry()->getHeight()) {
                continue;
            }
            currentGame.m_gameObjectsContext->getMap()->setVisibleFor(cellAt(currentGame, x, y), static_cast<int>(HUMAN));
        }
    }
}

int firstFittingColumn(cGame &currentGame, int row, int from, int to, int unitType, int avoid)
{
    for (int column = from; column <= to; column++) {
        if (avoid >= 0 && std::abs(column - avoid) < 3) {
            continue;
        }
        if (unitFits(currentGame, cellAt(currentGame, column, row), unitType)) {
            return column;
        }
    }
    return -1;
}

int firstFittingRow(cGame &currentGame, int column, int from, int to, int unitType)
{
    for (int row = from; row <= to; row++) {
        if (unitFits(currentGame, cellAt(currentGame, column, row), unitType)) {
            return row;
        }
    }
    return -1;
}

bool structureFits(cGame &currentGame, int column, int row)
{
    for (int dy = 0; dy < 2; dy++) {
        for (int dx = 0; dx < 2; dx++) {
            const int cell = cellAt(currentGame, column + dx, row + dy);
            if (!currentGame.m_gameObjectsContext->getMap()->getGeometry()->isValidCell(cell) ||
                currentGame.m_gameObjectsContext->getMap()->getCellIdStructuresLayer(cell) > -1) {
                return false;
            }
        }
    }
    return true;
}

int createLabelUnit(cGame &currentGame, cEventEmitter *events, int cell, int unitType)
{
    const int id = cUnits::unitCreate(currentGame.m_gameObjectsContext.get(), currentGame.m_infoContext.get(), events,
                                      cell, unitType, HUMAN, true, false, 0.3f);
    if (id < 0) {
        return id;
    }
    cUnit *created = currentGame.m_gameObjectsContext->getUnit(id);
    created->select();
    created->iGroups[0] = true;
    created->fExperience = 9;
    if (unitType == HARVESTER) {
        created->iCredits = created->getUnitInfo().credit_capacity;
    }
    return id;
}

}

bool UiAuditAccess::enterPlaying(cGame &currentGame, int house, int region)
{
    setHouse(currentGame, house);
    currentGame.m_dataCampaign->mission = CampaignProgress::FIRST_MISSION;
    currentGame.m_dataCampaign->region = region;
    currentGame.setNextStateToTransitionTo(GAME_BRIEFING);
    currentGame.transitionStateIfRequired();
    currentGame.setNextStateToTransitionTo(GAME_PLAYING);
    currentGame.m_drawManager->missionInit();
    currentGame.transitionStateIfRequired();
    return currentGame.m_gameObjectsContext->getMap()->getGeometry()->getWidth() > 0 &&
           currentGame.m_state == GAME_PLAYING;
}

bool UiAuditAccess::placeLabelUnits(cGame &currentGame, int unitType)
{
    MapView view;
    for (const bool relaxed : {false, true}) {
        for (int startRow = kStartMargin;
             startRow + kStartMargin < currentGame.m_gameObjectsContext->getMap()->getGeometry()->getHeight();
             startRow += kStartStep) {
            for (int startColumn = kStartMargin;
                 startColumn + kStartMargin < currentGame.m_gameObjectsContext->getMap()->getGeometry()->getWidth();
                 startColumn += kStartStep) {
                if (!aimCamera(currentGame, startColumn, startRow, view, relaxed)) {
                    continue;
                }
                const int topRow = view.firstRow;
                const int rightColumn = view.firstColumn + view.columns - 1;
                const int bottomRow = view.firstRow + view.rows - 1;

                const int topColumn = firstFittingColumn(currentGame, topRow, view.firstColumn + 1,
                                                         rightColumn - 1, unitType, -1);
                const int rightRow = firstFittingRow(currentGame, rightColumn, view.firstRow + 2,
                                                     bottomRow - 2, unitType);
                const int bottomColumn = topColumn < 0 ? -1
                    : firstFittingColumn(currentGame, bottomRow, view.firstColumn + 1, rightColumn - 1,
                                         unitType, topColumn);
                if (topColumn < 0 || rightRow < 0 || bottomColumn < 0) {
                    continue;
                }
                const int cells[3] = {cellAt(currentGame, topColumn, topRow),
                                      cellAt(currentGame, rightColumn, rightRow),
                                      cellAt(currentGame, bottomColumn, bottomRow)};
                const int columns[3] = {topColumn, rightColumn, bottomColumn};
                const int rows[3] = {topRow, rightRow, bottomRow};
                for (int i = 0; i < 3; i++) {
                    revealAround(currentGame, columns[i], rows[i], 2);
                }
                for (int i = 0; i < 3; i++) {
                    if (createLabelUnit(currentGame, currentGame.m_eventEmitter.get(), cells[i], unitType) < 0) {
                        return false;
                    }
                }
                return true;
            }
        }
    }
    return false;
}

bool UiAuditAccess::placeStructure(cGame &currentGame, int edge)
{
    MapView view;
    for (const bool relaxed : {false, true}) {
        for (int startRow = kStartMargin;
             startRow + kStartMargin < currentGame.m_gameObjectsContext->getMap()->getGeometry()->getHeight();
             startRow += kStartStep) {
            for (int startColumn = kStartMargin;
                 startColumn + kStartMargin < currentGame.m_gameObjectsContext->getMap()->getGeometry()->getWidth();
                 startColumn += kStartStep) {
                if (!aimCamera(currentGame, startColumn, startRow, view, relaxed)) {
                    continue;
                }
                int column = 0;
                int row = 0;
                bool found = false;
                if (edge == 0) {
                    row = view.firstRow;
                    for (column = view.firstColumn + 2;
                         column <= view.firstColumn + view.columns - 4 && !found; column++) {
                        found = structureFits(currentGame, column, row);
                        if (found) {
                            break;
                        }
                    }
                }
                else {
                    column = view.firstColumn + view.columns - 2;
                    for (row = view.firstRow + 2; row <= view.firstRow + view.rows - 4; row++) {
                        found = structureFits(currentGame, column, row);
                        if (found) {
                            break;
                        }
                    }
                }
                if (!found) {
                    continue;
                }
                revealAround(currentGame, column, row, 3);
                revealAround(currentGame, column + 1, row + 1, 3);
                if (currentGame.m_gameObjectsContext->getStructureFactory()->createStructure(
                        cellAt(currentGame, column, row), WINDTRAP, HUMAN, 40) == nullptr) {
                    return false;
                }
                const int cell = cellAt(currentGame, column, row);
                const int half = static_cast<int>(currentGame.m_mapCamera->factorZoomLevel(kTile)) / 2;
                uiaudit::setHover(currentGame.m_mapCamera->getWindowXPositionFromCell(cell) + half,
                                  currentGame.m_mapCamera->getWindowYPositionFromCell(cell) + half);
                return true;
            }
        }
    }
    return false;
}
