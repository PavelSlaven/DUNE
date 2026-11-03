#include "debug/UiAudit.hpp"

#include "cGame.h"
#include "gamestates/cMainMenuState.h"
#include "save/SaveGameManager.hpp"
#include "save/SaveSlotsDialog.hpp"
#include "d2tmc.h"
#include "drawers/cBuildingListDrawer.h"
#include "drawers/cCommandBarDrawer.h"
#include "drawers/cOrderDrawer.h"
#include "drawers/cSideBarDrawer.h"
#include "managers/cDrawManager.h"
#include "sidebar/cSideBar.h"
#include "controls/CommandBindings.hpp"
#include "controls/cMouse.h"
#include "drawers/cTextDrawer.h"
#include "audio/MusicController.h"
#include "gameobjects/structures/cAbstractStructure.h"
#include "gameobjects/structures/cStructureFactory.h"
#include "sidebar/cBuildingList.h"
#include "sidebar/cBuildingListUpdater.h"
#include "sidebar/cBuildingListItem.h"
#include "utils/cStructureUtils.h"
#include "data/gfxdata.h"
#include "gameobjects/units/cUnit.h"
#include "gamestates/cCreditsState.h"
#include "map/cMapCamera.h"
#include "player/cPlayer.h"
#include "gamestates/cOptionsState.h"
#include "gamestates/cSelectYourNextConquestState.h"
#include "gamestates/cSetupSkirmishState.h"
#include "gui/GuiLabel.hpp"
#include "mentat/AbstractMentat.h"
#include "utils/Localization.hpp"

#include <algorithm>
#include <filesystem>
#include <fstream>
#include <cstring>
#include <vector>

int UiAuditAccess::state(const cGame &game)
{
    return game.m_state;
}

const cGameState *UiAuditAccess::currentState(const cGame &game)
{
    return game.m_currentState;
}

const AbstractMentat *UiAuditAccess::mentat(const cGame &game)
{
    return game.m_mentat;
}

SDL_Renderer *UiAuditAccess::renderer(cGame &game)
{
    return game.renderer;
}

void UiAuditAccess::setState(cGame &game, int state)
{
    game.setState(state);
}

void UiAuditAccess::prepareTellHouse(cGame &game, int house)
{
    game.prepareMentatToTellAboutHouse(house);
}

bool UiAuditAccess::mentatFreeze(cGame &game, bool awaiting)
{
    AbstractMentat *mentat = game.m_mentat;
    if (mentat == nullptr) {
        return false;
    }
    if (awaiting) {
        mentat->state = AWAITING_RESPONSE;
        return true;
    }
    int bestPair = 0;
    size_t bestLength = 0;
    for (int pair = 0; pair <= 8; pair += 2) {
        const size_t length = std::strlen(mentat->sentence[pair]) + std::strlen(mentat->sentence[pair + 1]);
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

bool UiAuditAccess::prepareMentatScene(cGame &game, int house, int kind)
{
    players[HUMAN].setHouse(house);
    game.m_region = 1;
    if (kind == 0) {
        game.setNextStateToTransitionTo(GAME_BRIEFING);
        game.transitionStateIfRequired();
    }
    else {
        game.setState(kind == 1 ? GAME_WINBRIEF : GAME_LOSEBRIEF);
        game.createAndPrepareMentatForHumanPlayer(true);
    }
    return game.m_mentat != nullptr;
}

bool UiAuditAccess::prepareSkirmish(cGame &game, int variant)
{
    game.loadSkirmishMaps();
    game.initSkirmish();
    game.setNextStateToTransitionTo(GAME_SETUPSKIRMISH);
    game.transitionStateIfRequired();
    auto *setup = dynamic_cast<cSetupSkirmishState *>(game.m_currentState);
    if (setup == nullptr) {
        return false;
    }
    setup->iSkirmishMap = variant == 0 ? 0 : 1;
    if (variant == 1) {
        setup->startingPoints = 4;
        setup->skirmishPlayer[2].bPlaying = true;
        setup->skirmishPlayer[3].bPlaying = true;
    }
    return true;
}

void UiAuditAccess::missionOutcome(cGame &game, bool victory)
{
    game.m_missionWasWon = victory;
    game.setState(victory ? GAME_WINNING : GAME_LOSING);
    game.takeBackGroundScreen();
}

void UiAuditAccess::writeSaves(cGame &game)
{
    std::string error;
    std::filesystem::create_directories("saves");
    SaveGameManager::saveGame(game, 1, "", error);
    SaveGameManager::saveGame(game, 2, "A very long save name used to check how the slot row fits", error);
    SaveGameManager::saveGame(game, 5, "Before the final attack", error);
    std::ofstream(SaveGameManager::slotPath(3), std::ios::binary) << "not a save file";
    std::filesystem::create_directories(SaveGameManager::slotPath(6));
}

bool UiAuditAccess::openMenuSaveDialog(cGame &game)
{
    auto *menu = dynamic_cast<cMainMenuState *>(game.m_currentState);
    if (menu == nullptr || menu->m_saveDialog == nullptr) {
        return false;
    }
    menu->m_saveDialog->open(false, false);
    return true;
}

bool UiAuditAccess::saveDialog(cGame &game, int action)
{
    auto *options = dynamic_cast<cOptionsState *>(game.m_currentState);
    if (options == nullptr || options->m_saveDialog == nullptr) {
        return false;
    }
    SaveSlotsDialog &dialog = *options->m_saveDialog;
    dialog.open(true, action == 1 || action == 2 || action == 4);
    if (action == 2) {
        dialog.selectSlot(2);
    }
    else if (action == 3) {
        dialog.selectSlot(3);
        dialog.loadSelected();
    }
    else if (action == 4) {
        dialog.selectSlot(6);
        dialog.saveSelected();
    }
    return true;
}

bool UiAuditAccess::optionsPage(cGame &game, int page)
{
    auto *options = dynamic_cast<cOptionsState *>(game.m_currentState);
    if (options == nullptr) {
        return false;
    }
    options->switchOptionsPage(static_cast<cOptionsState::OptionsPage>(page));
    return true;
}

bool UiAuditAccess::optionsBinding(cGame &game)
{
    auto *options = dynamic_cast<cOptionsState *>(game.m_currentState);
    if (options == nullptr) {
        return false;
    }
    options->m_bindingCapture = CommandBindingAction::Attack;
    options->refresh();
    return true;
}

bool UiAuditAccess::optionsStatus(cGame &game)
{
    auto *options = dynamic_cast<cOptionsState *>(game.m_currentState);
    if (options == nullptr || options->m_displayStatusLabel == nullptr) {
        return false;
    }
    options->m_displayStatusLabel->setText(
        localization::text("Saved. Restart the game.", "Сохранено. Перезапустите игру."));
    return true;
}

bool UiAuditAccess::creditsScroll(cGame &game, int frame)
{
    auto *credits = dynamic_cast<cCreditsState *>(game.m_currentState);
    if (credits == nullptr) {
        return false;
    }
    credits->m_moveSpeed = 0;
    if (frame == 0) {
        credits->m_crawlerY = 64;
        return true;
    }
    const int fontHeight = credits->m_textDrawer->getFontHeight();
    const int limit = game.m_screenH - 128;
    std::vector<int> offsets;
    std::vector<bool> visible;
    int offset = credits->m_titleHeight;
    for (const s_CreditLine &line : credits->m_lines) {
        offsets.push_back(offset);
        visible.push_back(!line.name.empty() || !line.txt.empty());
        offset += line.height;
    }
    int group = 0;
    size_t index = 0;
    size_t lastStart = 0;
    while (index < offsets.size()) {
        if (!visible[index]) {
            ++index;
            continue;
        }
        const size_t start = index;
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

void UiAuditAccess::recordCreditLines(cGame &game)
{
    auto *credits = dynamic_cast<cCreditsState *>(game.m_currentState);
    if (credits == nullptr) {
        return;
    }
    for (const s_CreditLine &line : credits->m_lines) {
        if (!line.name.empty() || !line.txt.empty()) {
            uiaudit::recordCreditLine(line.name, line.txt);
        }
    }
}

void UiAuditAccess::regionOpen(cGame &game, int mission, bool jump)
{
    if (jump) {
        game.jumpToSelectYourNextConquestMission(mission);
    }
    else {
        game.m_mission = mission;
    }
    game.setState(GAME_REGION);
}

int UiAuditAccess::regionState(const cGame &game)
{
    auto *region = dynamic_cast<const cSelectYourNextConquestState *>(game.m_currentState);
    return region == nullptr ? -1 : static_cast<int>(region->state);
}

int UiAuditAccess::regionScene(const cGame &game)
{
    auto *region = dynamic_cast<const cSelectYourNextConquestState *>(game.m_currentState);
    return region == nullptr ? -1 : static_cast<int>(region->regionSceneState);
}

int UiAuditAccess::regionSceneAlpha(const cGame &game)
{
    auto *region = dynamic_cast<const cSelectYourNextConquestState *>(game.m_currentState);
    return region == nullptr ? -1 : region->iRegionSceneAlpha;
}

void UiAuditAccess::freezeClock(cGame &game)
{
    game.m_timeManager->onWindowFocusLost();
}

void UiAuditAccess::resumeClock(cGame &game)
{
    game.m_timeManager->onWindowFocusGained();
}

void UiAuditAccess::stopCameraEdgeMove()
{
    if (mapCamera != nullptr) {
        mapCamera->m_cameraEdgeMove = false;
        mapCamera->m_moveX = 0.0f;
        mapCamera->m_moveY = 0.0f;
    }
}

void UiAuditAccess::clearMouseClicks(cGame &game)
{
    game.m_mouse->leftButtonClicked = false;
    game.m_mouse->rightButtonClicked = false;
}

int UiAuditAccess::renderScale(const cGame &game)
{
    return game.m_renderScalePercent;
}

int UiAuditAccess::worldScale(const cGame &game)
{
    return game.m_worldScalePercent;
}

bool UiAuditAccess::mapViewport(const cGame &game, int &x, int &y, int &w, int &h)
{
    if (game.m_mapViewport == nullptr) {
        return false;
    }
    x = game.m_mapViewport->getX();
    y = game.m_mapViewport->getY();
    w = game.m_mapViewport->getWidth();
    h = game.m_mapViewport->getHeight();
    return true;
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

    cBuildingList *selectedList = selected >= 0 && selected < cSideBar::LIST_MAX ? sidebar->getList(selected) : nullptr;
    const bool starportOrdering = selectedList != nullptr && selectedList->isAvailable() &&
                                  selectedList->getType() == eListType::LIST_STARPORT;
    if (starportOrdering && drawManager != nullptr && drawManager->getOrderDrawer() != nullptr) {
        const cRectangle &rect = drawManager->getOrderDrawer()->m_buttonRect;
        uiaudit::recordClick("order-button", rect.getX(), rect.getY(), rect.getWidth(), rect.getHeight());
    }
}

void UiAuditAccess::recordCommandBarClicks(cCommandBarDrawer &drawer)
{
    for (const auto &button : drawer.m_buttons) {
        if (!button.enabled) {
            continue;
        }
        uiaudit::recordClick(("command:" + button.label).c_str(),
                             button.rect.getX(), button.rect.getY(), button.rect.getWidth(), button.rect.getHeight());
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

bool aimCamera(cGame &game, int startColumn, int startRow, MapView &view, bool relaxed)
{
    mapCamera->setViewportPosition(startColumn * kTile, startRow * kTile);
    if (mapCamera->getViewportStartX() != startColumn * kTile || mapCamera->getViewportStartY() != startRow * kTile) {
        return false;
    }
    const int tile = static_cast<int>(mapCamera->factorZoomLevel(kTile));
    if (tile <= 0) {
        return false;
    }
    view.firstColumn = startColumn;
    view.firstRow = startRow;
    view.columns = game.m_mapViewport->getWidth() / tile;
    view.rows = game.m_mapViewport->getHeight() / tile;
    if (relaxed) {
        // On a canvas wider than the map the view cannot stay inside the map, so it is cut to the map.
        view.columns = std::min(view.columns, global_map.getWidth() - view.firstColumn - 3);
        view.rows = std::min(view.rows, global_map.getHeight() - view.firstRow - 3);
    }
    return view.columns >= 8 && view.rows >= 8 &&
           view.firstColumn + view.columns + 2 < global_map.getWidth() &&
           view.firstRow + view.rows + 2 < global_map.getHeight();
}

bool unitFits(int cell, int unitType)
{
    if (!global_map.isValidCell(cell)) {
        return false;
    }
    const bool air = sUnitInfo[unitType].airborn;
    if (!air && global_map.cellGetIdFromLayer(cell, MAPID_STRUCTURES) > -1) {
        return false;
    }
    const int layer = air ? MAPID_AIR : MAPID_UNITS;
    if (global_map.cellGetIdFromLayer(cell, layer) > -1) {
        return false;
    }
    return global_map.canDeployUnitTypeAtCell(cell, unitType);
}

int cellAt(int column, int row)
{
    return row * global_map.getWidth() + column;
}

void revealAround(int column, int row, int radius)
{
    for (int y = row - radius; y <= row + radius; y++) {
        for (int x = column - radius; x <= column + radius; x++) {
            if (x < 0 || y < 0 || x >= global_map.getWidth() || y >= global_map.getHeight()) {
                continue;
            }
            global_map.setVisibleFor(cellAt(x, y), static_cast<int>(HUMAN));
        }
    }
}

int firstFittingColumn(int row, int from, int to, int unitType, int avoid)
{
    for (int column = from; column <= to; column++) {
        if (avoid >= 0 && std::abs(column - avoid) < 3) {
            continue;
        }
        if (unitFits(cellAt(column, row), unitType)) {
            return column;
        }
    }
    return -1;
}

int firstFittingRow(int column, int from, int to, int unitType)
{
    for (int row = from; row <= to; row++) {
        if (unitFits(cellAt(column, row), unitType)) {
            return row;
        }
    }
    return -1;
}

bool structureFits(int column, int row)
{
    for (int dy = 0; dy < 2; dy++) {
        for (int dx = 0; dx < 2; dx++) {
            const int cell = cellAt(column + dx, row + dy);
            if (!global_map.isValidCell(cell) || global_map.getCellIdStructuresLayer(cell) > -1) {
                return false;
            }
        }
    }
    return true;
}

int createLabelUnit(int cell, int unitType)
{
    const int id = UNIT_CREATE(cell, unitType, HUMAN, true, false, 0.3f);
    if (id < 0) {
        return id;
    }
    cUnit &created = unit[id];
    created.bSelected = true;
    created.iGroup = 1;
    created.fExperience = 9;
    if (unitType == HARVESTER) {
        created.iCredits = created.getUnitInfo().credit_capacity;
    }
    return id;
}

}

bool UiAuditAccess::enterPlaying(cGame &game, int house, int region)
{
    players[HUMAN].setHouse(house);
    game.m_region = region;
    game.setNextStateToTransitionTo(GAME_BRIEFING);
    game.transitionStateIfRequired();
    game.setNextStateToTransitionTo(GAME_PLAYING);
    game.transitionStateIfRequired();
    if (drawManager == nullptr || global_map.getWidth() <= 0 || mapCamera == nullptr) {
        return false;
    }
    drawManager->missionInit();
    return game.m_state == GAME_PLAYING;
}

bool UiAuditAccess::placeLabelUnits(cGame &game, int unitType)
{
    MapView view;
    for (const bool relaxed : {false, true}) {
        for (int startRow = kStartMargin; startRow + kStartMargin < global_map.getHeight(); startRow += kStartStep) {
            for (int startColumn = kStartMargin; startColumn + kStartMargin < global_map.getWidth();
                 startColumn += kStartStep) {
                if (!aimCamera(game, startColumn, startRow, view, relaxed)) {
                    continue;
                }
                const int topRow = view.firstRow;
                const int rightColumn = view.firstColumn + view.columns - 1;
                const int bottomRow = view.firstRow + view.rows - 1;

                const int topColumn = firstFittingColumn(topRow, view.firstColumn + 1, rightColumn - 1, unitType, -1);
                const int rightRow = firstFittingRow(rightColumn, view.firstRow + 2, bottomRow - 2, unitType);
                const int bottomColumn = topColumn < 0 ? -1
                    : firstFittingColumn(bottomRow, view.firstColumn + 1, rightColumn - 1, unitType, topColumn);
                if (topColumn < 0 || rightRow < 0 || bottomColumn < 0) {
                    continue;
                }
                const int cells[3] = {cellAt(topColumn, topRow), cellAt(rightColumn, rightRow),
                                      cellAt(bottomColumn, bottomRow)};
                const int columns[3] = {topColumn, rightColumn, bottomColumn};
                const int rows[3] = {topRow, rightRow, bottomRow};
                for (int i = 0; i < 3; i++) {
                    revealAround(columns[i], rows[i], 2);
                }
                for (int i = 0; i < 3; i++) {
                    if (createLabelUnit(cells[i], unitType) < 0) {
                        return false;
                    }
                }
                return true;
            }
        }
    }
    return false;
}

bool UiAuditAccess::placeStructure(cGame &game, int edge)
{
    MapView view;
    for (const bool relaxed : {false, true}) {
        for (int startRow = kStartMargin; startRow + kStartMargin < global_map.getHeight(); startRow += kStartStep) {
            for (int startColumn = kStartMargin; startColumn + kStartMargin < global_map.getWidth();
                 startColumn += kStartStep) {
                if (!aimCamera(game, startColumn, startRow, view, relaxed)) {
                    continue;
                }
                int column = 0;
                int row = 0;
                bool found = false;
                if (edge == 0) {
                    row = view.firstRow;
                    for (column = view.firstColumn + 2; column <= view.firstColumn + view.columns - 4 && !found; column++) {
                        found = structureFits(column, row);
                        if (found) {
                            break;
                        }
                    }
                }
                else {
                    column = view.firstColumn + view.columns - 2;
                    for (row = view.firstRow + 2; row <= view.firstRow + view.rows - 4; row++) {
                        found = structureFits(column, row);
                        if (found) {
                            break;
                        }
                    }
                }
                if (!found) {
                    continue;
                }
                revealAround(column, row, 3);
                revealAround(column + 1, row + 1, 3);
                if (cStructureFactory::getInstance()->createStructure(cellAt(column, row), WINDTRAP, HUMAN, 40) == nullptr) {
                    return false;
                }
                const int cell = cellAt(column, row);
                const int half = static_cast<int>(mapCamera->factorZoomLevel(kTile)) / 2;
                uiaudit::setHover(mapCamera->getWindowXPositionFromCell(cell) + half,
                                  mapCamera->getWindowYPositionFromCell(cell) + half);
                return true;
            }
        }
    }
    return false;
}

namespace {

struct BaseSpot {
    int type;
    int column;
    int row;
};

constexpr BaseSpot kBaseSpots[] = {
    {WINDTRAP, 24, 25}, {WINDTRAP, 26, 25}, {WINDTRAP, 35, 25}, {REFINERY, 32, 25},
    {LIGHTFACTORY, 24, 28}, {RADAR, 30, 28}, {BARRACKS, 28, 25}, {WOR, 32, 28},
    {HEAVYFACTORY, 26, 28}, {HIGHTECH, 32, 22}, {REPAIR, 35, 28}, {STARPORT, 28, 22},
    {IX, 35, 22}, {PALACE, 24, 22},
};

constexpr int kStreetRow = 27;
constexpr int kConstyardColumn = 30;
constexpr int kConstyardRow = 25;

struct BaseResult {
    int factoryId = -1;
    int tankId = -1;
    int harvesterId = -1;
    int mcvId = -1;
};

bool footprintFree(int type, int column, int row)
{
    const int w = structureUtils.getWidthOfStructureTypeInCells(type);
    const int h = structureUtils.getHeightOfStructureTypeInCells(type);
    for (int dy = 0; dy < h; dy++) {
        for (int dx = 0; dx < w; dx++) {
            const int cell = cellAt(column + dx, row + dy);
            if (!global_map.isValidCell(cell) || global_map.getCellIdStructuresLayer(cell) > -1) {
                return false;
            }
        }
    }
    return true;
}

int buildStructure(int type, int column, int row)
{
    if (!footprintFree(type, column, row)) {
        return -1;
    }
    cAbstractStructure *created = cStructureFactory::getInstance()->createStructure(cellAt(column, row), type, HUMAN, 100);
    if (created == nullptr) {
        return -1;
    }
    created->setBuildingFase(10);
    return created->getStructureId();
}

int spawnUnit(int type, int column, int row, float hpFraction)
{
    const int id = UNIT_CREATE(cellAt(column, row), type, HUMAN, true, false, hpFraction);
    if (id >= 0) {
        unit[id].bSelected = false;
    }
    return id;
}

bool buildBase(bool withRadar, float tankHp, BaseResult &result)
{
    players[HUMAN].setTechLevel(9);
    players[HUMAN].getBuildingListUpdater()->onStructureCreated(CONSTYARD);

    revealAround(kConstyardColumn, kConstyardRow, 16);

    for (const BaseSpot &spot : kBaseSpots) {
        if (spot.type == RADAR && !withRadar) {
            continue;
        }
        const int id = buildStructure(spot.type, spot.column, spot.row);
        if (id < 0) {
            return false;
        }
        if (spot.type == LIGHTFACTORY) {
            result.factoryId = id;
        }
    }

    players[HUMAN].update();
    for (int column = 24; column <= 38 && !players[HUMAN].bEnoughPower(); column += 2) {
        if (buildStructure(WINDTRAP, column, 30) < 0) {
            return false;
        }
        players[HUMAN].update();
    }
    if (!players[HUMAN].bEnoughPower()) {
        return false;
    }

    result.tankId = spawnUnit(TANK, 25, kStreetRow, tankHp);
    result.harvesterId = spawnUnit(HARVESTER, 29, kStreetRow, 1.0f);
    result.mcvId = spawnUnit(MCV, 33, kStreetRow, 1.0f);
    const int others[3] = {spawnUnit(SOLDIER, 27, kStreetRow, 1.0f), spawnUnit(TRIKE, 31, kStreetRow, 1.0f),
                           spawnUnit(QUAD, 35, kStreetRow, 1.0f)};
    if (result.tankId < 0 || result.harvesterId < 0 || result.mcvId < 0 ||
        others[0] < 0 || others[1] < 0 || others[2] < 0) {
        return false;
    }
    unit[result.harvesterId].iCredits = unit[result.harvesterId].getUnitInfo().credit_capacity;
    return true;
}

void hoverOnCell(int column, int row)
{
    const int cell = cellAt(column, row);
    const int half = static_cast<int>(mapCamera->factorZoomLevel(kTile)) / 2;
    uiaudit::setHover(mapCamera->getWindowXPositionFromCell(cell) + half,
                      mapCamera->getWindowYPositionFromCell(cell) + half);
}

void selectOnly(int unitId)
{
    for (int i = 0; i < MAX_UNITS; i++) {
        if (unit[i].isValid()) {
            unit[i].bSelected = (i == unitId);
        }
    }
}

eListType listForKind(int kind)
{
    switch (kind) {
        case uiaudit::GameKind::ListBuild: return eListType::LIST_CONSTYARD;
        case uiaudit::GameKind::ListInfantry: return eListType::LIST_FOOT_UNITS;
        case uiaudit::GameKind::ListVehicles: return eListType::LIST_UNITS;
        case uiaudit::GameKind::ListStarport: return eListType::LIST_STARPORT;
        case uiaudit::GameKind::ListPalace: return eListType::LIST_PALACE;
        case uiaudit::GameKind::ListUpgrades: return eListType::LIST_UPGRADES;
        default: return eListType::LIST_NONE;
    }
}

}

bool UiAuditAccess::prepareGameScreen(cGame &game, int house, int kind)
{
    using uiaudit::GameKind;
    if (!enterPlaying(game, house, 22)) {
        return false;
    }
    BaseResult base;
    const bool withRadar = kind != GameKind::RadarNone;
    if (!buildBase(withRadar, kind == GameKind::DamagedUnit ? 0.4f : 1.0f, base)) {
        return false;
    }
    if (kind == GameKind::RadarNoPower) {
        for (int i = 0; i < MAX_STRUCTURES; i++) {
            cAbstractStructure *s = structure[i];
            if (s != nullptr && s->isValid() && s->getOwner() == HUMAN && s->getType() == WINDTRAP) {
                s->setHitPoints(1);
            }
        }
        players[HUMAN].update();
        if (players[HUMAN].bEnoughPower()) {
            return false;
        }
    }
    for (int i = 0; i < 40; i++) {
        drawManager->getMiniMapDrawer()->think();
    }

    const bool lists = listForKind(kind) != eListType::LIST_NONE;
    const int centerColumn = (kind == GameKind::PlaceAllowed || kind == GameKind::PlaceForbidden) ? 28 : 30;
    mapCamera->centerAndJumpViewPortToCell(cellAt(centerColumn, 26));
    cSideBar *sidebar = players[HUMAN].getSideBar();
    if (sidebar == nullptr) {
        return false;
    }
    cBuildingListDrawer *items = drawManager->getBuildingListDrawer();

    if (lists) {
        sidebar->setSelectedListId(listForKind(kind));
        cBuildingList *list = sidebar->getList(sidebar->getSelectedListID());
        return list != nullptr && list->isAvailable() && list->getItemCount() > 0;
    }

    switch (kind) {
        case GameKind::Hud:
        case GameKind::RadarNone:
        case GameKind::RadarNoPower:
            return true;
        case GameKind::Music: {
            MusicController *music = game.m_musicController.get();
            if (music == nullptr) {
                return false;
            }
            MusicTrack track;
            track.externalPath = std::filesystem::path(
                localization::text("Gameplay_theme_with_an_extremely_long_track_title_for_the_layout_audit.ogg",
                                   "Игровая_тема_с_очень_длинным_названием_трека_для_проверки_раскладки.ogg"));
            auto &state = music->m_categories[static_cast<std::size_t>(MusicCategory::Gameplay)];
            state.playlist.setTracks({track});
            state.playlist.next();
            music->m_activeCategory = MusicCategory::Gameplay;
            music->m_hasActiveCategory = true;
            return !music->currentDisplayName().empty();
        }
        case GameKind::DamagedUnit:
            selectOnly(base.tankId);
            return true;
        case GameKind::Harvester:
            selectOnly(base.harvesterId);
            return true;
        case GameKind::Mcv:
            selectOnly(base.mcvId);
            return true;
        case GameKind::Structure:
            players[HUMAN].selected_structure = base.factoryId;
            return true;
        case GameKind::Rally:
            players[HUMAN].selected_structure = base.factoryId;
            structure[base.factoryId]->setRallyPoint(cellAt(28, 32));
            return structure[base.factoryId]->getRallyPoint() >= 0;
        case GameKind::PlaceAllowed:
        case GameKind::PlaceForbidden: {
            cBuildingList *list = sidebar->getList(eListType::LIST_CONSTYARD);
            cBuildingListItem *item = list == nullptr ? nullptr : list->getItemByBuildId(WINDTRAP);
            if (item == nullptr) {
                return false;
            }
            item->setPlaceIt(true);
            players[HUMAN].setContextMouseState(eMouseState::MOUSESTATE_PLACE);
            if (kind == GameKind::PlaceAllowed) {
                for (int dy = 0; dy < 2; dy++) {
                    for (int dx = 0; dx < 2; dx++) {
                        global_map.cellChangeType(cellAt(22 + dx, 25 + dy), TERRAIN_ROCK);
                    }
                }
                hoverOnCell(22, 25);
            }
            else {
                hoverOnCell(29, 24);
            }
            return true;
        }
        case GameKind::GroupSelect: {
            const int cell1 = cellAt(24, 26);
            const int cell2 = cellAt(31, 29);
            cMouse *mouse = game.getMouse();
            mouse->mouse_co_x1 = mapCamera->getWindowXPositionFromCell(cell1);
            mouse->mouse_co_y1 = mapCamera->getWindowYPositionFromCell(cell1);
            mouse->mouse_co_x2 = mapCamera->getWindowXPositionFromCell(cell2);
            mouse->mouse_co_y2 = mapCamera->getWindowYPositionFromCell(cell2);
            uiaudit::setHover(mouse->mouse_co_x2, mouse->mouse_co_y2);
            return mouse->isBoxSelecting();
        }
        case GameKind::Messages: {
            drawManager->setMessage(localization::text("Construction complete: the Windtrap is ready to be placed",
                                                       "Строительство завершено: ветряная электростанция готова к размещению"), true);
            for (int i = 0; i < 90; i++) {
                drawManager->thinkFast();
            }
            players[HUMAN].addNotification(localization::text("Neutral notification", "Обычное уведомление"),
                                           eNotificationType::NEUTRAL);
            players[HUMAN].addNotification(localization::text("Priority notification: Harvester is full",
                                                              "Важное уведомление: комбайн заполнен"),
                                           eNotificationType::PRIORITY);
            players[HUMAN].addNotification(localization::text("Bad news: a structure is under attack",
                                                              "Плохая новость: здание атаковано"),
                                           eNotificationType::BAD);
            return true;
        }
        case GameKind::ItemHover:
        case GameKind::ScrollEnd: {
            sidebar->setSelectedListId(eListType::LIST_CONSTYARD);
            cBuildingList *list = sidebar->getList(eListType::LIST_CONSTYARD);
            if (list == nullptr || list->getItemCount() < 3) {
                return false;
            }
            if (kind == GameKind::ScrollEnd) {
                items->setScrollRow(list, 1000);
                return true;
            }
            const int index = 2;
            const HudLayout layout = items->getLayout(list);
            const cRectangle card = layout.cardRect(index, items->getScrollRow(list));
            const int x = card.getX() + card.getWidth() / 2;
            const int y = card.getY() + card.getHeight() / 2;
            drawManager->setMessage(list->getItem(index)->getInfo(), true);
            for (int i = 0; i < 90; i++) {
                drawManager->thinkFast();
            }
            uiaudit::setHover(x, y);
            return true;
        }
        default:
            return false;
    }
}
