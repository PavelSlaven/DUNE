/**
 * @file cPlaceItDrawer.cpp
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

#include "cPlaceItDrawer.h"
#include "debug/UiAudit.hpp"
#include "utils/cStructureUtils.h"

#include "include/sGameServices.h"
#include "context/GameContext.hpp"
#include "data/gfxdata.h"
#include "drawers/SDLDrawer.hpp"
#include "gameobjects/map/cMapCamera.h"
#include "gameobjects/map/MapGeometry.hpp"
#include "gameobjects/players/cPlayer.h"
#include "utils/Graphics.hpp"
#include "gameobjects/map/cMap.h"
#include "gameobjects/structures/cStructures.h"
#include "gameobjects/units/cUnits.h"
#include "context/cInfoContext.h"
#include "context/cGameObjectContext.h"
#include <SDL3/SDL.h>

#include "include/cAssert.h"
#include "context/GraphicsContext.hpp"

cPlaceItDrawer::cPlaceItDrawer(GameContext *ctx, cPlayer *thePlayer, cStructureUtils *structureUtils) : m_structureUtils(structureUtils), m_player(thePlayer), m_ctx(ctx), m_sdlDrawer(ctx->getSDLDrawer())
{
    d2tm_assert(thePlayer != nullptr);
    d2tm_assert(ctx != nullptr);
    m_gfxdata = m_ctx->getGraphicsContext()->gfxdata.get();
}

cPlaceItDrawer::~cPlaceItDrawer()
{
    m_player = nullptr;
}

void cPlaceItDrawer::serviceInit(sGameServices* services)
{
    m_objects = services->objects;
    m_infos = services->info;
    m_mapCamera = services->mapCamera;
}

void cPlaceItDrawer::draw(cBuildingListItem *itemToPlace, int mouseCell)
{
    if (itemToPlace == nullptr) {
        return;
    }

    if (mouseCell < 0) {
        return;
    }

    drawStructureIdAtMousePos(itemToPlace, mouseCell);
    drawStatusOfStructureAtCell(itemToPlace, mouseCell);
}

void cPlaceItDrawer::drawStatusOfStructureAtCell(cBuildingListItem *itemToPlace, int mouseCell)
{
    d2tm_assert(itemToPlace);
    if (mouseCell < 0) return;

    const int structureId = itemToPlace->getBuildId();
    d2tm_assert(structureId > -1);

    const s_PlaceResult placement = m_player->canPlaceBuildingListItemAt(mouseCell, structureId);
    const int cellWidth = m_structureUtils->getWidthOfStructureTypeInCells(structureId);
    const int cellHeight = m_structureUtils->getHeightOfStructureTypeInCells(structureId);

    const int iCellX = m_objects->getMapGeometry()->getCellX(mouseCell);
    const int iCellY = m_objects->getMapGeometry()->getCellY(mouseCell);

    const int iDrawX = m_objects->getMap()->mouse_draw_x(mouseCell);
    const int iDrawY = m_objects->getMap()->mouse_draw_y(mouseCell);

    for (int iX = 0; iX < cellWidth; iX++) {
        for (int iY = 0; iY < cellHeight; iY++) {
            const int cellX = iCellX + iX;
            const int cellY = iCellY + iY;
            if (!m_objects->getMapGeometry()->isWithinBoundaries(cellX, cellY)) {
                continue;
            }

            const int cell = m_objects->getMapGeometry()->makeCell(cellX, cellY);
            Color itemToPlaceColor = Color::PlaceBad;
            const char *auditType = "BAD";
            if (placement.success) {
                if (m_objects->getMap()->getCellType(cell) == TERRAIN_SLAB) {
                    itemToPlaceColor = Color::PlaceGood;
                    auditType = "GOOD";
                }
                else {
                    itemToPlaceColor = Color::PlaceNeutral;
                    auditType = "NEUTRAL";
                }
            }

            const float desiredWidth = m_mapCamera->getZoomedTileWidth();
            const float desiredHeight = m_mapCamera->getZoomedTileHeight();
            const float posX = iX * desiredWidth;
            const float posY = iY * desiredHeight;
            if (uiaudit::isEnabled()) { uiaudit::recordLabel("place-cell", structureId, auditType, static_cast<int>(iDrawX + posX), static_cast<int>(iDrawY + posY), static_cast<int>(desiredWidth), static_cast<int>(desiredHeight), uiaudit::Rect{iDrawX, iDrawY, static_cast<int>(cellWidth * desiredWidth), static_cast<int>(cellHeight * desiredHeight)}); }
            m_sdlDrawer->renderRectFillColor(iDrawX + posX, iDrawY + posY, desiredWidth, desiredHeight, itemToPlaceColor);
        }
    }
}

void cPlaceItDrawer::drawStructureIdAtMousePos(cBuildingListItem *itemToPlace, int mouseCell)
{
    d2tm_assert(itemToPlace);

    int structureId = itemToPlace->getBuildId();

    int iDrawX = m_objects->getMap()->mouse_draw_x(mouseCell);
    int iDrawY = m_objects->getMap()->mouse_draw_y(mouseCell);

    int width = m_infos->getStructureInfo(structureId).bmp_width;
    int height = m_infos->getStructureInfo(structureId).bmp_height;

    int scaledWidth = m_mapCamera->factorZoomLevel(width);
    int scaledHeight = m_mapCamera->factorZoomLevel(height);

    Texture *bmp = nullptr;
    if (structureId == SLAB1) {
        bmp = m_gfxdata->getTexture(PLACE_SLAB1);
    }
    else if (structureId == SLAB4) {
        bmp = m_gfxdata->getTexture(PLACE_SLAB4);
    }
    else if (structureId == WALL) {
        bmp = m_gfxdata->getTexture(PLACE_WALL);
    }
    else {
        bmp = m_player->getStructureBitmap(structureId);
    }
    // We need to take a source rectangle, as the structure BMP contains multiple frames of the structure
    // therefore we cannot use renderStrechFullSprite (as that assumes the source texture can be used as a whole
    // which cannot be used in this case)
    cRectangle src = { 0, 0, width, height}; // takes first frame
    cRectangle dest= {iDrawX, iDrawY, scaledWidth, scaledHeight};
    m_sdlDrawer->renderStrechSprite(bmp, src, dest,96);
}
