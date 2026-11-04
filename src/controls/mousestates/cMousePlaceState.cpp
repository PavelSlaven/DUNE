#include "cMousePlaceState.h"

#include "d2tmc.h"
#include "data/gfxdata.h"
#include "controls/cGameControlsContext.h"
#include "player/cPlayer.h"
#include "utils/Localization.hpp"
#include "utils/cSoundPlayer.h"

#include "data/gfxaudio.h"

cMousePlaceState::cMousePlaceState(cPlayer *player, cGameControlsContext *context, cMouse *mouse) :
    cMouseState(player, context, mouse)
{

}

void cMousePlaceState::onNotifyMouseEvent(const s_MouseEvent &event)
{
    // these methods can have a side-effect which changes mouseTile...
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
        m_mouse->setTile(mouseTile);
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

    const auto notifyPlacementFailure = [this](const s_PlaceResult &result) {
        const char *message = localization::text(
            "Cannot build here.",
            "Здесь нельзя строить.");
        if (result.success) {
            message = localization::text(
                "Cannot place another structure: no structure slot is available.",
                "Нельзя поставить постройку: не осталось свободного места.");
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
        m_player->addNotification(message, eNotificationType::BAD);
    };

    s_PlaceResult result;
    if (!mayPlaceIt(itemToPlace, mouseCell, &result)) {
        notifyPlacementFailure(result);
        return;
    }

    const int structureType = itemToPlace->getBuildId();
    cAbstractStructure *placed = m_player->placeItem(mouseCell, itemToPlace);
    const bool terrainPlacement = structureType == SLAB1 || structureType == SLAB4 || structureType == WALL;
    if (placed == nullptr && !terrainPlacement) {
        result = m_player->canPlaceBuildingListItemAt(mouseCell, structureType);
        notifyPlacementFailure(result);
        return;
    }

    game.playSound(SOUND_PLACE);
    m_context->toPreviousState();
}

bool cMousePlaceState::mayPlaceIt(cBuildingListItem *itemToPlace, int mouseCell, s_PlaceResult *result)
{
    if (itemToPlace == nullptr) {
        return false;
    }

    const s_PlaceResult placement = m_player->canPlaceBuildingListItemAt(mouseCell, itemToPlace->getBuildId());
    if (result != nullptr) {
        *result = placement;
    }
    return placement.success;
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
    mouseTile = MOUSE_NORMAL;
    m_mouse->setTile(mouseTile);
}


void cMousePlaceState::onNotifyKeyboardEvent(const cKeyboardEvent &)
{
}

void cMousePlaceState::onFocus()
{
    m_mouse->setTile(mouseTile);
}

void cMousePlaceState::onBlur()
{
    m_mouse->resetBoxSelect();
    m_mouse->resetDragViewportInteraction();
}
