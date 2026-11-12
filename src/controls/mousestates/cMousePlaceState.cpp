/**
 * @file cMousePlaceState.cpp
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

#include "cMousePlaceState.h"

#include "gameobjects/map/cMap.h"
#include "context/AudioContext.hpp"
#include "data/gfxdata.h"
#include "controls/cGameControlsContext.h"
#include "gameobjects/structures/cStructures.h"
#include "gameobjects/units/cUnits.h"
#include "utils/cStructureUtils.h"
#include "gameobjects/players/cPlayer.h"
#include "sidebar/cSideBar.h"
#include "utils/cSoundPlayer.h"
#include "gameobjects/map/MapGeometry.hpp"
#include "context/cInfoContext.h"
#include "context/cGameObjectContext.h"
#include "managers/cDrawManager.h"
#include <algorithm>
#include "include/cAssert.h"

#include "data/gfxaudio.h"
#include "gameobjects/structures/cStructureFactory.h"
#include "utils/Localization.hpp"
#include "game/cEventEmitter.h"
#include "include/sGameEvent.h"

cMousePlaceState::cMousePlaceState(cPlayer *player, cGameControlsContext *context, cMouse *mouse) :
    cMouseState(player, context, mouse)
{
    d2tm_assert(player!=nullptr);
    d2tm_assert(context!=nullptr);
    d2tm_assert(mouse!=nullptr);
}

void cMousePlaceState::onNotifyMouseEvent(const s_MouseEvent &event)
{
    // these methods can have a side-effect which changes m_mouseTile...
    switch (event.eventType) {
        case MOUSE_LEFT_BUTTON_CLICKED:
            onMouseLeftButtonClicked();
            break;
        case MOUSE_RIGHT_BUTTON_PRESSED:
            onMouseRightButtonPressed();
            break;
        case MOUSE_RIGHT_BUTTON_CLICKED:
            onMouseRightButtonClicked();
            break;
        case MOUSE_MOVED_TO:
            onMouseMovedTo();
            break;
        default:
            break;
    }

    // ... so set it here
    if (m_context->isState(MOUSESTATE_PLACE)) { // if , required in case we switched state
        m_mouse->setTile(m_mouseTile);
    }
}

void cMousePlaceState::onMouseLeftButtonClicked()
{
    // this assumes the m_context has been updated beforehand...
    int mouseCell = m_context->getMouseCell();

    if (mouseCell < 0) {
        return;
    }

    cBuildingListItem *itemToPlace = m_player->getSideBar()->getList(eListType::LIST_CONSTYARD)->getItemToPlace();
    if (itemToPlace == nullptr) {
        return;
    }

    s_PlaceResult result;
    if (!mayPlaceIt(itemToPlace, mouseCell, &result)) {
        notifyPlacementFailure(result);
        return;
    }

    const int structureType = itemToPlace->getBuildId();
    if (m_context->getObjects()->getStructureFactory()->isStructureLimitReached() && !cStructureFactory::isModifyingTerrain(structureType)) {
        m_context->getDrawManager()->setMessage(localization::text("Unable to create more.", "Больше построить нельзя."));
        return;
    }

    cAbstractStructure *placed = m_player->placeItem(mouseCell, itemToPlace);
    if (placed == nullptr && !cStructureFactory::isModifyingTerrain(structureType)) {
        notifyPlacementFailure(m_player->canPlaceBuildingListItemAt(mouseCell, structureType));
        return;
    }

    m_context->getAudioContext()->playSound(SOUND_PLACE);
    m_context->toPreviousState();
}

bool cMousePlaceState::mayPlaceIt(cBuildingListItem *itemToPlace, int mouseCell, s_PlaceResult *result)
{
    if (itemToPlace == nullptr || mouseCell < 0) {
        return false;
    }

    d2tm_assert(itemToPlace->getBuildId() > -1);
    const s_PlaceResult placement = m_player->canPlaceBuildingListItemAt(mouseCell, itemToPlace->getBuildId());
    if (result != nullptr) {
        *result = placement;
    }
    return placement.success;
}

void cMousePlaceState::notifyPlacementFailure(const s_PlaceResult &result)
{
    const char *message = localization::text(
        "Cannot build here.",
        "Здесь нельзя строить.");
    if (result.success) {
        message = localization::text(
            "Unable to create more.",
            "Больше построить нельзя.");
    }
    else if (result.outOfBounds) {
        message = localization::text(
            "Cannot build here: the structure would be outside the map.",
            "Здесь нельзя строить: постройка выходит за пределы карты.");
    }
    else if (result.badTerrain) {
        message = localization::text(
            "Cannot build here: this terrain does not support structures.",
            "Здесь нельзя строить: неподходящий рельеф.");
    }
    else if (!result.unitIds.empty()) {
        message = localization::text(
            "Cannot build here: a unit occupies the site.",
            "Здесь нельзя строить: клетку занимает юнит.");
    }
    else if (!result.structureIds.empty()) {
        message = localization::text(
            "Cannot build here: a structure occupies the site.",
            "Здесь нельзя строить: клетку занимает постройка.");
    }
    else if (result.outOfBuildDistance) {
        message = localization::text(
            "Cannot build here: the site is too far from your base.",
            "Здесь нельзя строить: место слишком далеко от вашей базы.");
    }
    m_context->getEventEmitter()->emit(s_GameEvent{
        .eventType = eGameEventType::GAME_EVENT_NOTIFICATION,
        .data = NotificationEvent{
            .message = message,
            .type = eNotificationType::BAD,
        }
    });
}

void cMousePlaceState::onMouseRightButtonPressed()
{
    m_mouse->dragViewportInteraction();
}

void cMousePlaceState::onMouseRightButtonClicked()
{
    if (m_mouse->isMapScrolling()) {
        m_mouse->resetDragViewportInteraction();
    }
    else {
        m_context->toPreviousState();
    }
}

void cMousePlaceState::onMouseMovedTo()
{
    // TODO: update state for determining place result so that renderer does not need to do
    // that logic every frame (see cPlaceItDrawer)
}

void cMousePlaceState::onStateSet()
{
    m_mouseTile = MOUSE_NORMAL;
    m_mouse->setTile(m_mouseTile);
}


void cMousePlaceState::onNotifyKeyboardEvent(const cKeyboardEvent &)
{
}

void cMousePlaceState::onFocus()
{
    m_mouse->setTile(m_mouseTile);
}

void cMousePlaceState::onBlur()
{
    m_mouse->resetBoxSelect();
    m_mouse->resetDragViewportInteraction();
}
