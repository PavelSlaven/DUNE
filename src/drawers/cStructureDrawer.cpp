#include "cStructureDrawer.h"

#include "drawers/SDLDrawer.hpp"
#include "controls/cGameControlsContext.h"
#include "data/gfxdata.h"
#include "d2tmc.h"
#include "gameobjects/structures/cGunTurret.h"
#include "gameobjects/structures/cRefinery.h"
#include "gameobjects/structures/cRepairFacility.h"
#include "gameobjects/structures/cRocketTurret.h"
#include "gameobjects/structures/cWindTrap.h"
#include "gameobjects/units/cUnit.h"
#include "map/cMapCamera.h"
#include "player/cPlayer.h"
#include "utils/Graphics.hpp"
#include "utils/WorldObjectScale.hpp"
#include "context/GameContext.hpp"
#include "context/GraphicsContext.hpp"
#include <SDL2/SDL.h>

#include <algorithm>
#include <cmath>

cStructureDrawer::cStructureDrawer(GameContext *ctx) :
    m_gfxdata(ctx->getGraphicsContext()->gfxdata.get()),
    m_gfxinter(ctx->getGraphicsContext()->gfxinter.get())
{
}


void cStructureDrawer::drawStructuresFirstLayer()
{
    drawStructuresForLayer(0);
}

void cStructureDrawer::drawStructuresSecondLayer()
{
    drawStructuresForLayer(2);
}

void cStructureDrawer::drawStructuresHealthBars()
{
    cGameControlsContext *context = players[HUMAN].getGameControlsContext();

    // DRAW HEALTH
    if (context->isMouseOverStructure()) {
        int i = context->getIdOfStructureWhereMouseHovers();
        drawStructureHealthBar(i);
    }
}

void cStructureDrawer::drawRectangleOfStructure(cAbstractStructure *theStructure, Color color)
{
    assert(theStructure);
    int drawX = theStructure->iDrawX();
    int drawY = theStructure->iDrawY();
    int width = sStructureInfo[theStructure->getType()].bmp_width - 1;
    int height = sStructureInfo[theStructure->getType()].bmp_height - 1;

    int width_x = mapCamera->factorZoomLevel(width);
    int height_y = mapCamera->factorZoomLevel(height);

    renderDrawer->renderRectColor(drawX, drawY, width_x, height_y, color.r, color.g, color.b, 96);
}

void cStructureDrawer::drawStructurePrebuildAnimation(cAbstractStructure *structure)
{
    int iDrawPreBuild = determinePreBuildAnimationIndex(structure);
    if (iDrawPreBuild < 0) return; // bail, don't draw invalid tiles

    int pixelWidth = structure->getWidthInPixels();
    int pixelHeight = structure->getHeightInPixels();

    int drawX = structure->iDrawX();
    int drawY = structure->iDrawY();

    int scaledWidth = mapCamera->factorZoomLevel(pixelWidth);
    int scaledHeight = mapCamera->factorZoomLevel(pixelHeight);

    // Draw prebuild
    cRectangle dest= {drawX, drawY, scaledWidth, scaledHeight};
    renderDrawer->renderStrechFullSprite(gfxdata->getTexture(iDrawPreBuild), dest);
}

void cStructureDrawer::drawStructureAnimation(cAbstractStructure *structure)
{
    if (!structure) return;
    structure->draw();
}

int cStructureDrawer::determinePreBuildAnimationIndex(cAbstractStructure *structure)
{
    assert(structure);
    int iBuildFase = structure->getBuildingFase();
    int height = structure->getHeight();
    int width = structure->getWidth();

    // prebuild
    if (iBuildFase == 1 ||
            iBuildFase == 3 ||
            iBuildFase == 5 ||
            iBuildFase == 7 ||
            iBuildFase == 9) {

        // determine what kind of prebuild picture should be used.
        if (width == 1 && height == 1) {
            return BUILD_PRE_1X1;
        }

        if (width == 2 && height == 2) {
            return BUILD_PRE_2X2;
        }

        if (width == 3 && height == 2) {
            return BUILD_PRE_3X2;
        }

        if (width == 3 && height == 3) {
            return BUILD_PRE_3X3;
        }
    }

    return -1;
}

void cStructureDrawer::drawStructureAnimationTurret(cAbstractStructure *structure)
{
    assert(structure);
    assert(structure->getType() == TURRET || structure->getType() == RTURRET);

    int iHeadFacing = -1;
    int facingAngles = 8;
    if (structure->getType() == TURRET) {
        cGunTurret *gunTurret = dynamic_cast<cGunTurret *>(structure);
        iHeadFacing = gunTurret->getHeadFacing();
        facingAngles = gunTurret->getFacingAngles();
    }
    else if (structure->getType() == RTURRET) {
        cRocketTurret *rocketTurret = dynamic_cast<cRocketTurret *>(structure);
        iHeadFacing = rocketTurret->getHeadFacing();
        facingAngles = rocketTurret->getFacingAngles();
    }
    assert(iHeadFacing > -1);

    // for now support these 2 facing angles amounts
    if (facingAngles == 16) {
        structure->setFrame(convertAngleToDrawIndex(iHeadFacing, false, 4, 16));
    }
    else if (facingAngles == 8) {
        structure->setFrame(convertAngleToDrawIndex(iHeadFacing, false, 2, 8));
    }

    // :-/
    if (game.isDebugMode()) {
        cPlayer &humanPlayer = players[HUMAN];
        cAbstractStructure *pStructure = humanPlayer.getSelectedStructure();
        if (pStructure && pStructure == structure) {
            cMouse *pMouse = game.getMouse();
            cGameControlsContext *pContext = humanPlayer.getGameControlsContext();

            int x1 = pMouse->getX();
            int y1 = pMouse->getY();
            int x2 = mapCamera->getWindowXPosition(structure->pos_x() + 16);
            int y2 = mapCamera->getWindowYPosition(structure->pos_y() + 16);

            renderDrawer->renderLine( x1, y1, x2, y2, Color{255, 255, 255,255});

            int mouseCellX = global_map.getCellX(pContext->getMouseCell());
            int mouseCellY = global_map.getCellY(pContext->getMouseCell());

            int cellX = global_map.getCellX(structure->getCell());
            int cellY = global_map.getCellY(structure->getCell());

            float degrees = fDegrees(cellX, cellY, mouseCellX, mouseCellY);

            int facingAngle = faceAngle(degrees, facingAngles);

            pMouse->addDebugLine(std::format("degrees = {}, faceAngle = {}", degrees, facingAngle));

//            int frame = convertAngleToDrawIndex(facingAngle, false, 4, 16);
            // override frame
//            structure->setFrame(frame);

            if (structure->getType() == TURRET) {
                cGunTurret *gunTurret = dynamic_cast<cGunTurret *>(structure);
                gunTurret->setShouldHeadFacing(facingAngle);
            }
            else if (structure->getType() == RTURRET) {
                cRocketTurret *rocketTurret = dynamic_cast<cRocketTurret *>(structure);
                rocketTurret->setShouldHeadFacing(facingAngle);
            }

        }
    }

    drawStructureAnimation(structure);
}

void cStructureDrawer::drawStructureAnimationRefinery(cAbstractStructure *structure)
{
    assert(structure);
    assert(structure->getType() == REFINERY);

    drawStructureAnimation(structure);
    if (game.isHdGraphicsActive() && structure->hasUnitWithin()) {
        drawHarvesterOnRefineryPad(structure);
    }
}

void cStructureDrawer::drawStructureForLayer(cAbstractStructure *structure, int layer)
{
    assert(structure);

    // always select proper palette (of owner)
    // select_palette(players[structure->getOwner()].pal);

    // when layer is <= 1 the building is just being placed. The prebuild
    // animation should be be drawn or, the normal drawing is shown (ie the
    // structure is not in action, like deploying harvester etc).

    // when stage == 2, it means only to draw the repair animation above the structure
    // this is done after all the structures have been drawn with stage 1 or lower. Causing
    // the repair icons to always overlap other structures. This is ugly, the repair icons
    // should be 'particles' (like smoke etc) instead of being hacked here!

    if (layer <= 1) {
        int iDrawPreBuild = determinePreBuildAnimationIndex(structure);

        // if no prebuild picture is selected, than we should draw the building
        // itself. The reason why the above if uses only buildfase 1, 3, 5, 7 and 9 means
        // that it will cause the switching between pre-build/building state as if the
        // building is being 'readied' after placement.
        if (iDrawPreBuild < 0) {
            if (structure->getType() == TURRET || structure->getType() == RTURRET) {
                drawStructureAnimationTurret(structure);
            }
            else if (structure->getType() == REFINERY) {
                drawStructureAnimationRefinery(structure);
            }
            else {
                drawStructureAnimation(structure);
            }
            bool drewHdHouseMarker = false;
            if (game.isHdGraphicsActive()) {
                drewHdHouseMarker = drawHdRefineryFlag(structure);
                if (!drewHdHouseMarker) {
                    drewHdHouseMarker = drawHdSiloFlag(structure);
                }
                if (!drewHdHouseMarker) {
                    drewHdHouseMarker = drawHdWindTrapFlag(structure);
                }
                if (!drewHdHouseMarker) {
                    drewHdHouseMarker = drawHdConstYardFlag(structure);
                }
                if (!drewHdHouseMarker) {
                    drewHdHouseMarker = drawHdBarracksFlag(structure);
                }
                if (!drewHdHouseMarker) {
                    drewHdHouseMarker = drawHdWorFlag(structure);
                }
                if (!drewHdHouseMarker) {
                    drewHdHouseMarker = drawHdRadarFlag(structure);
                }
                if (!drewHdHouseMarker) {
                    drewHdHouseMarker = drawHdStarportFlag(structure);
                }
                if (!drewHdHouseMarker) {
                    drewHdHouseMarker = drawHdPalaceFlag(structure);
                }
                if (!drewHdHouseMarker) {
                    drewHdHouseMarker = drawHdIxFlag(structure);
                }
                if (!drewHdHouseMarker) {
                    drewHdHouseMarker = drawHdLightFactoryFlag(structure);
                }
                if (!drewHdHouseMarker) {
                    drewHdHouseMarker = drawHdHighTechFlag(structure);
                }
            }
            if (!drewHdHouseMarker) {
                structure->drawFlags();
            }
        }
        else {
            drawStructurePrebuildAnimation(structure);
        }
    }
    else if (layer == 2) {
        // TODO: REMOVE THIS CODE AND create particles for this
        // now draw the repair alpha when repairing
        if (structure->getType() == REPAIR && structure->hasUnitWithin()) {
            renderIconOfUnitBeingRepaired(structure);
        }

        if (structure->isRepairing()) {
            renderIconThatStructureIsBeingRepaired(structure);
        }
    }
}

bool cStructureDrawer::drawHdRadarFlag(
    cAbstractStructure *structure) const
{
    if (!structure || structure->getType() != RADAR) {
        return false;
    }
    SDL_Surface *flagSurface =
        m_gfxdata->getSurface("BUILD_RADAR_FLAG");
    if (!flagSurface) {
        return false;
    }

    cPlayer *owner = structure->getPlayer();
    Texture *flag = m_gfxdata->getHouseTexture(
        flagSurface,
        owner->getHouse(),
        -1,
        owner->getMinimapColor(),
        TransparentColorIndex
    );
    if (!flag) {
        return false;
    }

    constexpr int logicalFrameSize = 64;
    constexpr int frameCount = 8;
    const int phase =
        static_cast<int>((SDL_GetTicks() / 125U) % frameCount);
    const cRectangle source = {
        0,
        phase * logicalFrameSize,
        logicalFrameSize,
        logicalFrameSize,
    };
    renderDrawer->renderStrechSprite(
        flag,
        source,
        structure->getVisualRectangle()
    );
    return true;
}

bool cStructureDrawer::drawHdBarracksFlag(
    cAbstractStructure *structure) const
{
    if (!structure || structure->getType() != BARRACKS) {
        return false;
    }
    SDL_Surface *flagSurface =
        m_gfxdata->getSurface("BUILD_BARRACKS_FLAG");
    if (!flagSurface) {
        return false;
    }

    cPlayer *owner = structure->getPlayer();
    Texture *flag = m_gfxdata->getHouseTexture(
        flagSurface,
        owner->getHouse(),
        -1,
        owner->getMinimapColor(),
        TransparentColorIndex
    );
    if (!flag) {
        return false;
    }

    constexpr int logicalFrameSize = 64;
    constexpr int frameCount = 8;
    const int phase =
        static_cast<int>((SDL_GetTicks() / 125U) % frameCount);
    const cRectangle source = {
        0,
        phase * logicalFrameSize,
        logicalFrameSize,
        logicalFrameSize,
    };
    renderDrawer->renderStrechSprite(
        flag,
        source,
        structure->getVisualRectangle()
    );
    return true;
}

bool cStructureDrawer::drawHdWorFlag(
    cAbstractStructure *structure) const
{
    if (!structure || structure->getType() != WOR) {
        return false;
    }
    SDL_Surface *flagSurface =
        m_gfxdata->getSurface("BUILD_WOR_FLAG");
    if (!flagSurface) {
        return false;
    }

    cPlayer *owner = structure->getPlayer();
    Texture *flag = m_gfxdata->getHouseTexture(
        flagSurface,
        owner->getHouse(),
        -1,
        owner->getMinimapColor(),
        TransparentColorIndex
    );
    if (!flag) {
        return false;
    }

    constexpr int logicalFrameSize = 64;
    constexpr int frameCount = 8;
    const int phase =
        static_cast<int>((SDL_GetTicks() / 125U) % frameCount);
    const cRectangle source = {
        0,
        phase * logicalFrameSize,
        logicalFrameSize,
        logicalFrameSize,
    };
    renderDrawer->renderStrechSprite(
        flag,
        source,
        structure->getVisualRectangle()
    );
    return true;
}

bool cStructureDrawer::drawHdRefineryFlag(
    cAbstractStructure *structure) const
{
    if (!structure || structure->getType() != REFINERY) {
        return false;
    }
    SDL_Surface *flagSurface =
        m_gfxdata->getSurface("BUILD_REFINERY_FLAG");
    if (!flagSurface) {
        return false;
    }

    cPlayer *owner = structure->getPlayer();
    Texture *flag = m_gfxdata->getHouseTexture(
        flagSurface,
        owner->getHouse(),
        -1,
        owner->getMinimapColor(),
        TransparentColorIndex
    );
    if (!flag) {
        return false;
    }

    constexpr int logicalFrameWidth = 96;
    constexpr int logicalFrameHeight = 64;
    constexpr int frameCount = 8;
    const int phase =
        static_cast<int>((SDL_GetTicks() / 125U) % frameCount);
    const cRectangle source = {
        0,
        phase * logicalFrameHeight,
        logicalFrameWidth,
        logicalFrameHeight,
    };
    renderDrawer->renderStrechSprite(
        flag,
        source,
        structure->getVisualRectangle()
    );
    return true;
}

bool cStructureDrawer::drawHdWindTrapFlag(
    cAbstractStructure *structure) const
{
    if (!structure || structure->getType() != WINDTRAP) {
        return false;
    }
    SDL_Surface *flagSurface =
        m_gfxdata->getSurface("BUILD_WINDTRAP_FLAG");
    if (!flagSurface) {
        return false;
    }

    cPlayer *owner = structure->getPlayer();
    Texture *flag = m_gfxdata->getHouseTexture(
        flagSurface,
        owner->getHouse(),
        -1,
        owner->getMinimapColor(),
        TransparentColorIndex
    );
    if (!flag) {
        return false;
    }

    constexpr int logicalFrameSize = 64;
    constexpr int frameCount = 8;
    const int phase =
        static_cast<int>((SDL_GetTicks() / 125U) % frameCount);
    const cRectangle source = {
        0,
        phase * logicalFrameSize,
        logicalFrameSize,
        logicalFrameSize,
    };
    renderDrawer->renderStrechSprite(
        flag,
        source,
        structure->getVisualRectangle()
    );
    return true;
}

bool cStructureDrawer::drawHdSiloFlag(
    cAbstractStructure *structure) const
{
    if (!structure || structure->getType() != SILO) {
        return false;
    }
    SDL_Surface *flagSurface =
        m_gfxdata->getSurface("BUILD_SILO_FLAG");
    if (!flagSurface) {
        return false;
    }

    cPlayer *owner = structure->getPlayer();
    Texture *flag = m_gfxdata->getHouseTexture(
        flagSurface,
        owner->getHouse(),
        -1,
        owner->getMinimapColor(),
        TransparentColorIndex
    );
    if (!flag) {
        return false;
    }

    constexpr int logicalFrameSize = 64;
    constexpr int frameCount = 8;
    const int phase =
        static_cast<int>((SDL_GetTicks() / 125U) % frameCount);
    const cRectangle source = {
        0,
        phase * logicalFrameSize,
        logicalFrameSize,
        logicalFrameSize,
    };
    renderDrawer->renderStrechSprite(
        flag,
        source,
        structure->getVisualRectangle()
    );
    return true;
}

bool cStructureDrawer::drawHdStarportFlag(
    cAbstractStructure *structure) const
{
    if (!structure || structure->getType() != STARPORT) {
        return false;
    }
    SDL_Surface *flagSurface =
        m_gfxdata->getSurface("BUILD_STARPORT_FLAG");
    if (!flagSurface) {
        return false;
    }

    cPlayer *owner = structure->getPlayer();
    Texture *flag = m_gfxdata->getHouseTexture(
        flagSurface,
        owner->getHouse(),
        -1,
        owner->getMinimapColor(),
        TransparentColorIndex
    );
    if (!flag) {
        return false;
    }

    constexpr int logicalFrameSize = 96;
    constexpr int frameCount = 8;
    const int phase =
        static_cast<int>((SDL_GetTicks() / 125U) % frameCount);
    const cRectangle source = {
        0,
        phase * logicalFrameSize,
        logicalFrameSize,
        logicalFrameSize,
    };
    renderDrawer->renderStrechSprite(
        flag,
        source,
        structure->getVisualRectangle()
    );
    return true;
}

bool cStructureDrawer::drawHdPalaceFlag(
    cAbstractStructure *structure) const
{
    if (!structure || structure->getType() != PALACE) {
        return false;
    }
    SDL_Surface *flagSurface =
        m_gfxdata->getSurface("BUILD_PALACE_FLAG");
    if (!flagSurface) {
        return false;
    }

    cPlayer *owner = structure->getPlayer();
    Texture *flag = m_gfxdata->getHouseTexture(
        flagSurface,
        owner->getHouse(),
        -1,
        owner->getMinimapColor(),
        TransparentColorIndex
    );
    if (!flag) {
        return false;
    }

    constexpr int logicalFrameSize = 96;
    constexpr int frameCount = 8;
    const int phase =
        static_cast<int>((SDL_GetTicks() / 125U) % frameCount);
    const cRectangle source = {
        0,
        phase * logicalFrameSize,
        logicalFrameSize,
        logicalFrameSize,
    };
    renderDrawer->renderStrechSprite(
        flag,
        source,
        structure->getVisualRectangle()
    );
    return true;
}

bool cStructureDrawer::drawHdIxFlag(
    cAbstractStructure *structure) const
{
    if (!structure || structure->getType() != IX) {
        return false;
    }
    SDL_Surface *flagSurface =
        m_gfxdata->getSurface("BUILD_IX_FLAG");
    if (!flagSurface) {
        return false;
    }

    cPlayer *owner = structure->getPlayer();
    Texture *flag = m_gfxdata->getHouseTexture(
        flagSurface,
        owner->getHouse(),
        -1,
        owner->getMinimapColor(),
        TransparentColorIndex
    );
    if (!flag) {
        return false;
    }

    constexpr int logicalFrameSize = 64;
    constexpr int frameCount = 8;
    const int phase =
        static_cast<int>((SDL_GetTicks() / 125U) % frameCount);
    const cRectangle source = {
        0,
        phase * logicalFrameSize,
        logicalFrameSize,
        logicalFrameSize,
    };
    renderDrawer->renderStrechSprite(
        flag,
        source,
        structure->getVisualRectangle()
    );
    return true;
}

bool cStructureDrawer::drawHdLightFactoryFlag(
    cAbstractStructure *structure) const
{
    if (!structure || structure->getType() != LIGHTFACTORY) {
        return false;
    }
    SDL_Surface *flagSurface =
        m_gfxdata->getSurface("BUILD_LIGHTFACTORY_FLAG");
    if (!flagSurface) {
        return false;
    }

    cPlayer *owner = structure->getPlayer();
    Texture *flag = m_gfxdata->getHouseTexture(
        flagSurface,
        owner->getHouse(),
        -1,
        owner->getMinimapColor(),
        TransparentColorIndex
    );
    if (!flag) {
        return false;
    }

    constexpr int logicalFrameSize = 64;
    constexpr int frameCount = 8;
    const int phase =
        static_cast<int>((SDL_GetTicks() / 125U) % frameCount);
    const cRectangle source = {
        0,
        phase * logicalFrameSize,
        logicalFrameSize,
        logicalFrameSize,
    };
    renderDrawer->renderStrechSprite(
        flag,
        source,
        structure->getVisualRectangle()
    );
    return true;
}

bool cStructureDrawer::drawHdHighTechFlag(
    cAbstractStructure *structure) const
{
    if (!structure || structure->getType() != HIGHTECH) {
        return false;
    }
    SDL_Surface *flagSurface =
        m_gfxdata->getSurface("BUILD_HIGHTECH_FLAG");
    if (!flagSurface) {
        return false;
    }

    cPlayer *owner = structure->getPlayer();
    Texture *flag = m_gfxdata->getHouseTexture(
        flagSurface,
        owner->getHouse(),
        -1,
        owner->getMinimapColor(),
        TransparentColorIndex
    );
    if (!flag) {
        return false;
    }

    constexpr int logicalFrameWidth = 96;
    constexpr int logicalFrameHeight = 64;
    constexpr int frameCount = 8;
    const int phase =
        static_cast<int>((SDL_GetTicks() / 125U) % frameCount);
    const cRectangle source = {
        0,
        phase * logicalFrameHeight,
        logicalFrameWidth,
        logicalFrameHeight,
    };
    renderDrawer->renderStrechSprite(
        flag,
        source,
        structure->getVisualRectangle()
    );
    return true;
}

bool cStructureDrawer::drawHdConstYardFlag(
    cAbstractStructure *structure) const
{
    if (!structure || structure->getType() != CONSTYARD) {
        return false;
    }
    SDL_Surface *flagSurface =
        m_gfxdata->getSurface("BUILD_CONSTYARD_FLAG");
    if (!flagSurface) {
        return false;
    }

    cPlayer *owner = structure->getPlayer();
    Texture *flag = m_gfxdata->getHouseTexture(
        flagSurface,
        owner->getHouse(),
        -1,
        owner->getMinimapColor(),
        TransparentColorIndex
    );
    if (!flag) {
        return false;
    }

    constexpr int logicalFrameSize = 64;
    constexpr int frameCount = 8;
    const int phase =
        static_cast<int>((SDL_GetTicks() / 125U) % frameCount);
    const cRectangle source = {
        0,
        phase * logicalFrameSize,
        logicalFrameSize,
        logicalFrameSize,
    };
    renderDrawer->renderStrechSprite(
        flag,
        source,
        structure->getVisualRectangle()
    );
    return true;
}

void cStructureDrawer::drawHdBuildingFoundation(
    cAbstractStructure *structure) const
{
    Texture *foundation =
        m_gfxdata->findTexture("BUILDING_FOUNDATION_HD");
    if (!foundation) {
        return;
    }

    const cRectangle destination = {
        structure->iDrawX(),
        structure->iDrawY(),
        std::max(
            1,
            static_cast<int>(std::lround(
                mapCamera->factorZoomLevel(
                    structure->getWidthInPixels()
                )
            ))
        ),
        std::max(
            1,
            static_cast<int>(std::lround(
                mapCamera->factorZoomLevel(
                    structure->getHeightInPixels()
                )
            ))
        ),
    };
    renderDrawer->renderStrechFullSprite(
        foundation,
        destination,
        230
    );
}

void cStructureDrawer::drawHarvesterOnRefineryPad(
    cAbstractStructure *structure) const
{
    if (!structure || !structure->hasUnitWithin()) {
        return;
    }
    const int unitId = structure->getUnitIdWithin();
    if (unitId < 0 || unitId >= MAX_UNITS) {
        return;
    }
    cUnit &harvester = unit[unitId];
    if (!harvester.isValid() || harvester.iType != HARVESTER) {
        return;
    }

    Texture *bitmap =
        players[structure->getOwner()].getUnitBitmap(HARVESTER);
    if (!bitmap) {
        return;
    }
    const int frameWidth = harvester.getBmpWidth();
    const int frameHeight = harvester.getBmpHeight();
    // The classic refinery's occupied frame always shows the harvester
    // aligned vertically on the unloading deck.  Do not inherit an arbitrary
    // approach angle after the unit has entered the structure.
    const int bodyFrame = convertAngleToDrawIndex(FACE_DOWN);
    const cRectangle source = {
        bodyFrame * frameWidth,
        0,
        frameWidth,
        frameHeight,
    };

    const cRectangle refineryVisual = structure->getVisualRectangle();
    const WorldObjectLayout harvesterVisual = refineryHarvesterLayout(
        refineryVisual.getX(),
        refineryVisual.getY(),
        refineryVisual.getWidth(),
        refineryVisual.getHeight()
    );
    const cRectangle destination = {
        harvesterVisual.x,
        harvesterVisual.y,
        harvesterVisual.width,
        harvesterVisual.height,
    };
    renderDrawer->renderStrechSprite(
        bitmap,
        source,
        destination
    );
}

void cStructureDrawer::renderIconThatStructureIsBeingRepaired(cAbstractStructure *structure) const
{
    int iconWidth = gfxdata->getLogicalWidth(MOUSE_REPAIR);
    int iconHeight = gfxdata->getLogicalHeight(MOUSE_REPAIR);
    int drawX = structure->iDrawX();
    int drawY = structure->iDrawY();
    int offsetX = (structure->getWidthInPixels() - iconWidth) / 2;
    int offsetY = (structure->getHeightInPixels() - iconHeight) / 2;
    int offsetXScaled = mapCamera->factorZoomLevel(offsetX);
    int offsetYScaled = mapCamera->factorZoomLevel(offsetY);
    int scaledWidth = mapCamera->factorZoomLevel(iconWidth);
    int scaledHeight = mapCamera->factorZoomLevel(iconHeight);
    cRectangle dest = {drawX+offsetXScaled, drawY + offsetYScaled, scaledWidth, scaledHeight};
    renderDrawer->renderStrechFullSprite(gfxdata->getTexture(MOUSE_REPAIR), dest);
}

void cStructureDrawer::renderIconOfUnitBeingRepaired(cAbstractStructure *structure) const
{
    cRepairFacility *repairFacility = dynamic_cast<cRepairFacility *>(structure);
    assert(repairFacility);
    int unitId = repairFacility->getUnitIdWithin();
    cUnit &pUnit = unit[unitId];
    int iconId = pUnit.getUnitInfo().icon;

    int iconWidth = m_gfxinter->getLogicalWidth(iconId);
    int iconHeight = m_gfxinter->getLogicalHeight(iconId);

    // draw health bar of unit on top of icon?
    int draw_x = 3;
    int draw_y = iconHeight - 8;

    int width_x = iconWidth - 6;

    int height_y = 5;

    float healthNormalized = pUnit.getTempHealthNormalized();

    int w = healthNormalized * width_x;
    int r = (1.1 - healthNormalized) * 255;
    int g = healthNormalized * 255;

    if (r > 255) r = 255;

    // bar itself
    renderDrawer->renderRectFillColor(draw_x, draw_y, width_x+1, height_y+1, 0,0,0,255);
    renderDrawer->renderRectFillColor(draw_x, draw_y, (w-1), height_y,r,g,32,255);

    // bar around it
    renderDrawer->renderRectColor(draw_x, draw_y, width_x, height_y, Color{255, 255, 255,255});
    int drawX = structure->iDrawX();
    int drawY = structure->iDrawY();
    int offsetX = (structure->getWidthInPixels() - iconWidth) / 2;
    int offsetY = (structure->getHeightInPixels() - iconHeight) / 2;
    int offsetXScaled = mapCamera->factorZoomLevel(offsetX);
    int offsetYScaled = mapCamera->factorZoomLevel(offsetY);
    int scaledWidth = mapCamera->factorZoomLevel(iconWidth);
    int scaledHeight = mapCamera->factorZoomLevel(iconHeight);
    cRectangle dest = {drawX + offsetXScaled, drawY + offsetYScaled, scaledWidth, scaledHeight};
    renderDrawer->renderStrechFullSprite(m_gfxinter->getTexture(iconId), dest);
}

void cStructureDrawer::drawStructuresForLayer(int layer)
{
    if (layer == 0 && game.isHdGraphicsActive()) {
        // Foundations are a separate pass so a later structure's ground pad
        // can never cover an already drawn neighbouring building.
        for (int i = 0; i < MAX_STRUCTURES; ++i) {
            cAbstractStructure *candidate = structure[i];
            if (candidate &&
                structureUtils.isStructureVisibleOnScreen(candidate)) {
                drawHdBuildingFoundation(candidate);
            }
        }
    }

    for (int i=0; i < MAX_STRUCTURES; i++) {
        cAbstractStructure *theStructure = structure[i];

        if (!theStructure) continue;

        if (structureUtils.isStructureVisibleOnScreen(theStructure)) {
            // draw
            drawStructureForLayer(theStructure, layer);

            cPlayer &player = players[HUMAN]; // TODO: Pass it as variable? (instead of getting it from here)
            const bool skipHdHeavyFactoryOutline =
                game.isHdGraphicsActive() &&
                theStructure->getType() == HEAVYFACTORY;
            if (skipHdHeavyFactoryOutline) {
                continue;
            }
            // regardless if selected, render this so you know from which structure things will come?
            if (player.isPrimaryStructureForStructureType(theStructure->getType(), i)) {
                drawRectangleOfStructure(theStructure, player.getPrimaryBuildingFadingColor());
                continue;
            }

            if (i == player.selected_structure) {
                drawRectangleOfStructure(theStructure, player.getSelectFadingColor());
            }
        }
    }

    renderDrawer->renderRectFillColor((game.m_screenW - cSideBar::SidebarWidth), 0,
                                      cSideBar::SidebarWidth, game.m_screenH, 0, 0, 0,255);
}

void cStructureDrawer::drawStructureHealthBar(int iStructure)
{
    if (iStructure < 0 || iStructure >= MAX_STRUCTURES) return;

    cAbstractStructure *theStructure = structure[iStructure];

    if (!theStructure) {
        return;
    }

    // Draw structure health
    const cRectangle visual = theStructure->getVisualRectangle();
    int draw_x = visual.getX() - 1;
    int draw_y = visual.getY() - 5;
    int width_x = visual.getWidth() - 1;

    int height_y = 4;

    float healthNormalized = theStructure->getHealthNormalized();

    int w = healthNormalized * width_x;
    int r = (1.1 - healthNormalized) * 255;
    int g = healthNormalized * 255;

    if (r > 255) r = 255;

    // bar itself
    renderDrawer->renderRectFillColor(draw_x, draw_y, width_x+1, height_y+1, 0,0,0,255);
    renderDrawer->renderRectFillColor(draw_x, draw_y, (w-1), height_y, (Uint8)r,(Uint8)g,32,255);

    // bar around it
    renderDrawer->renderRectColor(draw_x, draw_y, width_x, height_y, Color{255, 255, 255,255});
}
