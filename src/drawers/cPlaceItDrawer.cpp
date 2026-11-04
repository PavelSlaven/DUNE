#include "cPlaceItDrawer.h"

#include "d2tmc.h"
#include "data/gfxdata.h"
#include "drawers/SDLDrawer.hpp"
#include "map/cMapCamera.h"
#include "map/MapGeometry.hpp"
#include "player/cPlayer.h"
#include "utils/Graphics.hpp"
#include <SDL2/SDL.h>

#include <cassert>

cPlaceItDrawer::cPlaceItDrawer(cPlayer *thePlayer) : player(thePlayer)
{
}

cPlaceItDrawer::~cPlaceItDrawer()
{
    player = nullptr;
}

void cPlaceItDrawer::draw(cBuildingListItem *itemToPlace, int mouseCell)
{
    if (itemToPlace == nullptr) {
        return;
    }

    if (mouseCell < 0) {
        return;
    }

    drawStructureIdAtMousePos(itemToPlace);
    drawStatusOfStructureAtCell(itemToPlace, mouseCell);
}

void cPlaceItDrawer::drawStatusOfStructureAtCell(cBuildingListItem *itemToPlace, int mouseCell)
{
    assert(itemToPlace);
    if (mouseCell < 0) return;
    Color itemToPlaceColor;

    int structureId = itemToPlace->getBuildId();
    assert(structureId > -1);
    const s_PlaceResult placement = player->canPlaceBuildingListItemAt(mouseCell, structureId);
    int cellWidth = structureUtils.getWidthOfStructureTypeInCells(structureId);
    int cellHeight = structureUtils.getHeightOfStructureTypeInCells(structureId);

    int iCellX = global_map.getCellX(mouseCell);
    int iCellY = global_map.getCellY(mouseCell);

    int iDrawX = global_map.mouse_draw_x();
    int iDrawY = global_map.mouse_draw_y();

    for (int iX = 0; iX < cellWidth; iX++) {
        for (int iY = 0; iY < cellHeight; iY++) {
            const int cellX = iCellX + iX;
            const int cellY = iCellY + iY;
            if (!global_map.isWithinBoundaries(cellX, cellY)) {
                continue;
            }

            const int cell = global_map.getGeometry().makeCell(cellX, cellY);
            itemToPlaceColor = placement.success
                ? global_map.getCellType(cell) == TERRAIN_SLAB
                    ? game.getColorPlaceGood()
                    : game.getColorPlaceNeutral()
                : game.getColorPlaceBad();

            const float desiredWidth = mapCamera->getZoomedTileWidth();
            const float desiredHeight = mapCamera->getZoomedTileHeight();
            const float posX = iX * desiredWidth;
            const float posY = iY * desiredHeight;
            renderDrawer->renderRectFillColor(iDrawX + posX, iDrawY + posY, desiredWidth, desiredHeight,
                                              itemToPlaceColor);
        }
    }
}

void cPlaceItDrawer::drawStructureIdAtMousePos(cBuildingListItem *itemToPlace)
{
    assert(itemToPlace);

    int structureId = itemToPlace->getBuildId();

    int iDrawX = global_map.mouse_draw_x();
    int iDrawY = global_map.mouse_draw_y();

    int width = sStructureInfo[structureId].bmp_width;
    int height = sStructureInfo[structureId].bmp_height;

    int scaledWidth = std::lround(mapCamera->factorZoomLevel(width));
    int scaledHeight = std::lround(mapCamera->factorZoomLevel(height));

    Texture *bmp = nullptr;
    if (structureId == SLAB1) {
        bmp = gfxdata->getTexture(PLACE_SLAB1);
    }
    else if (structureId == SLAB4) {
        bmp = gfxdata->getTexture(PLACE_SLAB4);
    }
    else if (structureId == WALL) {
        bmp = gfxdata->getTexture(PLACE_WALL);
    }
    else {
        bmp = player->getStructureBitmap(structureId);
    }
    // We need to take a source rectangle, as the structure BMP contains multiple frames of the structure
    // therefore we cannot use renderStrechFullSprite (as that assumes the source texture can be used as a whole
    // which cannot be used in this case)
    cRectangle src = { 0, 0, width, height}; // takes first frame
    cRectangle dest= {iDrawX, iDrawY, scaledWidth, scaledHeight};
    renderDrawer->renderStrechSprite(bmp, src, dest,96);
}
