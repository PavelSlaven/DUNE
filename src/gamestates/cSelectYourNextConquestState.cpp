#include "cSelectYourNextConquestState.h"

#include "d2tmc.h"
#include "data/gfxdata.h"
#include "data/gfxinter.h"
#include "data/gfxworld.h"
#include "drawers/SDLDrawer.hpp"
#include "drawers/cMessageDrawer.h"
#include "ini.h"
#include "managers/cDrawManager.h"
#include "player/cPlayer.h"
#include "gui/GuiButton.h"
#include "utils/Localization.hpp"
#include "utils/Graphics.hpp"
#include "utils/HdUiTextureLoader.hpp"
#include "context/GameContext.hpp"
#include "context/TextContext.hpp"
#include "include/Texture.hpp"

#include <SDL2/SDL.h>
#include <algorithm>
#include <cmath>
#include <iostream>
#include <format>

namespace {
Color campaignHouseColor(int house)
{
    switch (house) {
        case HARKONNEN: return Color{194, 48, 42, 255};
        case ATREIDES: return Color{45, 92, 192, 255};
        case ORDOS: return Color{52, 156, 67, 255};
        default: return Color{126, 118, 102, 255};
    }
}

Texture* createTextureFromSurface(SDL_Surface* surface)
{
    if (surface == nullptr) return nullptr;
    SDL_Texture* texture = SDL_CreateTextureFromSurface(
        renderDrawer->getRenderer(),
        surface
    );
    if (texture == nullptr) {
        SDL_Log("Failed to create HD campaign overlay: %s", SDL_GetError());
        return nullptr;
    }
    SDL_SetTextureBlendMode(texture, SDL_BLENDMODE_BLEND);
    SDL_SetTextureScaleMode(texture, SDL_ScaleModeLinear);
    return new Texture(texture, surface->w, surface->h);
}
}

// Return color index from pixel (x, y) in surface
static Uint8 getPixelColorIndexFromSurface(SDL_Surface *surface, int x, int y)
{
    if (surface == nullptr) {
        std::cerr << "Error : nullptr surface" << std::endl;
        return 0;
    }

    if (surface->format->format != SDL_PIXELFORMAT_INDEX8) {
        std::cerr << "Error : no indexed 8 bits surface (format actuel : "
                  << SDL_GetPixelFormatName(surface->format->format) << ")." << std::endl;
        return 0;
    }

    if (x < 0 || x >= surface->w || y < 0 || y >= surface->h) {
        std::cerr << "Error : out of range pixel (" << x << ", " << y << ") in (" << surface->w << ", " << surface->h << ")." << std::endl;
        return 0;
    }
    Uint8 *pixelData = (Uint8 *)surface->pixels;
    Uint8 colorIndex = pixelData[y * (surface->pitch) + x];
    return colorIndex;
}

cSelectYourNextConquestState::cSelectYourNextConquestState(cGame &theGame, GameContext*ctx) :
    cGameState(theGame, ctx),
    m_gfxworld(ctx->getGraphicsContext()->gfxworld.get()),
    m_gfxinter(ctx->getGraphicsContext()->gfxinter.get())
{
    m_hdLayout = m_game.isHdGraphicsActive();
    m_textDrawer = m_hdLayout
        ? ctx->getTextContext()->getMenuTextDrawer()
        : ctx->getTextContext()->getBeneTextDrawer();
    if (m_hdLayout) {
        m_hdCampaignLayout = CampaignMapLayout::create(
            m_game.m_screenW,
            m_game.m_screenH
        );
        m_hdBackground = loadHdUiTexture(
            "main_menu_background.png",
            m_game.getGraphicsDensity(),
            "HD campaign map background"
        );
        m_hdCampaignMap = loadHdUiTexture(
            "campaign_map.png",
            m_game.getGraphicsDensity(),
            "HD campaign map"
        );

        std::string crestFile = "hud_house_atreides.png";
        if (players[0].getHouse() == HARKONNEN) {
            crestFile = "hud_house_harkonnen.png";
        }
        else if (players[0].getHouse() == ORDOS) {
            crestFile = "hud_house_ordos.png";
        }
        m_hdHouseCrest = loadHdUiTexture(
            crestFile,
            m_game.getGraphicsDensity(),
            "HD campaign house crest"
        );
    }
    state = eRegionState::REGSTATE_INIT;
    regionSceneState = eRegionSceneState::SCENE_INIT;

    iRegionSceneAlpha = 0;  // alpha for scene in introduction state

    memset(iRegionConquer, -1, sizeof(iRegionConquer));
    memset(iRegionHouse, -1, sizeof(iRegionHouse));
    memset(cRegionText, 0, sizeof(cRegionText));

    calculateOffset();

    regionClickMapBmp = nullptr;

    regionMouseIsHoveringOver = -1;
    isFinishedConqueringRegions = true;

    const std::string missionSelectLabel = localization::text("MISSION SELECT", "ВЫБОР МИССИИ");
    cRectangle toMissionSelectRect;
    if (m_hdLayout) {
        toMissionSelectRect = m_hdCampaignLayout.missionButton;
    }
    else {
        const int length = m_textDrawer->getTextLength(missionSelectLabel);
        toMissionSelectRect = *m_textDrawer->getAsRectangle(
            m_game.m_screenW - length,
            m_game.m_screenH - m_textDrawer->getFontHeight(),
            missionSelectLabel
        );
    }
    GuiButton *gui_btn_toMissionSelect = GuiButtonBuilder()
            .withRect(toMissionSelectRect)        
            .withLabel(missionSelectLabel)
            .withKind(m_hdLayout
                ? GuiRenderKind::REMASTER_BUTTON
                : GuiRenderKind::TRANSPARENT_WITHOUT_BORDER)
            .withTextDrawer(m_textDrawer)
            .withTheme(m_hdLayout ? GuiTheme::Remaster() : GuiTheme::Light())
            .onClick([this]() {
                m_game.setNextStateToTransitionTo(GAME_MISSIONSELECT);})
            .build();   
    m_guiBtnToMissionSelect = gui_btn_toMissionSelect;
}

void cSelectYourNextConquestState::calculateOffset()
{
    if (m_hdLayout) {
        offsetX = m_hdCampaignLayout.panel.getX();
        offsetY = m_hdCampaignLayout.panel.getY();
        return;
    }
    offsetX = (m_game.m_screenW - 640) / 2;
    offsetY = (m_game.m_screenH - 480) / 2;
}

cSelectYourNextConquestState::~cSelectYourNextConquestState()
{
    delete m_guiBtnToMissionSelect;
    delete m_hdBackground;
    delete m_hdCampaignMap;
    delete m_hdRegionBorders;
    delete m_hdHouseCrest;
    for (auto &region : world) {
        delete region.bmpColor;
        region.bmpColor = nullptr;
    }
}

void cSelectYourNextConquestState::thinkFast()
{

    // First time INIT
    if (state == eRegionState::REGSTATE_INIT) {
        // temp bitmap to read from
        regionClickMapBmp = m_gfxworld->getSurface(WORLD_DUNE_CLICK); // 8 bit bitmap
        if (m_hdLayout && m_hdRegionBorders == nullptr) {
            m_hdRegionBorders = createHdRegionBordersTexture();
        }
        // NOTE: No need to use Offset here, as it is on a tempreg and we pretend our mouse is on that BMP as well
        // we substract the offset from mouse coordinates to compensate
        state = fastForward ? eRegionState::REGSTATE_CONQUER_REGIONS : eRegionState::REGSTATE_INTRODUCTION;
        return;
    }

    if (state == eRegionState::REGSTATE_INTRODUCTION) {
        if (iRegionSceneAlpha < 255) {
            iRegionSceneAlpha += 1;
        }

        if (iRegionSceneAlpha > 255) {
            iRegionSceneAlpha = 255;
        }

        int iHouse = players[0].getHouse();
        int iMission = m_game.m_mission;

        bool hasMessage = drawManager->hasMessage();

        if (regionSceneState == SCENE_INIT) {
            regionSetupNextMission(iMission, iHouse);
            drawManager->setMessage(localization::text("Three Houses came to Dune.", "Три Дома прибыли на Дюну."));
            transitionToNextRegionSceneState(SCENE_THREE_HOUSES_COME_FOR_DUNE);
        }
        else if (regionSceneState == SCENE_THREE_HOUSES_COME_FOR_DUNE) {
            if (!hasMessage && iRegionSceneAlpha >= 255) {
                drawManager->setMessage(localization::text("To take control of the land.", "Чтобы покорить её земли."));
                transitionToNextRegionSceneState(SCENE_TO_TAKE_CONTROL_OF_THE_LAND);
            }
        }
        else if (regionSceneState == SCENE_TO_TAKE_CONTROL_OF_THE_LAND) {
            if (!hasMessage && iRegionSceneAlpha >= 255) {
                drawManager->setMessage(localization::text("It has now become divided.", "Теперь Дюна разделена."));
                transitionToNextRegionSceneState(SCENE_THAT_HAS_BECOME_DIVIDED);
            }
        }
        else if (regionSceneState == SCENE_THAT_HAS_BECOME_DIVIDED) {
            if (iRegionSceneAlpha >= 255) {
                transitionToNextRegionSceneState(SCENE_SELECT_YOUR_NEXT_CONQUEST);
                conquerRegions(); // this will change the message bar and state
            }
        }
    }

    if (state == eRegionState::REGSTATE_CONQUER_REGIONS || state == eRegionState::REGSTATE_INTRODUCTION) {
        for (int i = 0; i < 27; i++) {
            cRegion &regionPiece = world[i];

            if (regionPiece.iHouse < 0) continue; // skip pieces that do not belong to any house

            if (regionPiece.iAlpha < 255) {
                regionPiece.iAlpha += 3;

                // speed up when holding mouse button
                if (m_game.getMouse()->isLeftButtonPressed()) {
                    regionPiece.iAlpha += 3;
                }
            }
        }

        isFinishedConqueringRegions = true;

        for (int i = 0; i < MAX_REGIONS; i++) {
            if (iRegionConquer[i] < 0) continue;
            int houseThatConquersTheRegion = iRegionHouse[i];
            if (houseThatConquersTheRegion < 0) continue;

            int iRegNr = iRegionConquer[i];

            cRegion &region = world[iRegNr];

            // when the region is NOT this house, turn it into this house
            if (region.iHouse != houseThatConquersTheRegion) {
                const char *regionTextString = cRegionText[i];
                bool isRegionTextGiven = regionTextString[0] != '\0';
                bool isRegionTextEmpty = regionTextString[0] == '\0';

                if ((isRegionTextGiven && !drawManager->hasMessage()) || isRegionTextEmpty) {
                    // set this up
                    region.iHouse = houseThatConquersTheRegion;
                    region.iAlpha = 1; // this makes it > 0 and thus it will become opaque over time (see THINK function)

                    if (isRegionTextGiven) {
                        drawManager->setMessage(regionTextString);
                    }
                    isFinishedConqueringRegions = false;
                    break;
                }
                else {
                    isFinishedConqueringRegions = false;
                    break;

                }
            }
            else {
                // house = the same
                if (region.iAlpha >= 255) {
                    // remove this from the 'regionToConquer' index
                    iRegionConquer[i] = -1;
                    houseThatConquersTheRegion = -1; //
                    isFinishedConqueringRegions = false;

                    break;
                }
                else if (region.iAlpha < 255) {
                    isFinishedConqueringRegions = false;
                    break; // not done yet, so wait before we do another region!
                }
            }
        }

        if (isFinishedConqueringRegions) {
            state = REGSTATE_SELECT_NEXT_CONQUEST;
        }
    }

    // select your next conquest... always draw them in the human playing house color
    if (state == REGSTATE_SELECT_NEXT_CONQUEST) {
        if (selectNextConquestAlpha < 255) {
            selectNextConquestAlpha += 1;
        }
        else {
            selectNextConquestAlpha = 1;
        }

        for (int i = 0; i < 27; i++) {
            cRegion &regionPiece = world[i];

            if (!regionPiece.bSelectable) continue; // only animate selectable pieces

            regionPiece.iAlpha = selectNextConquestAlpha;
        }
    }

}

void cSelectYourNextConquestState::draw() const
{
    m_game.getMouse()->setTile(MOUSE_NORMAL); // global state of mouse
    // STEPS:
    // 1. Show current conquered regions
    // 2. Show next progress + story (in message bar)
    // 3. Click next region
    // 4. Set up region and go to GAME_BRIEFING, which will do the rest...-> fade out

    const int iHouse = players[0].getHouse();
    if (m_hdLayout) {
        drawHdBackground();
        drawHdChrome();
        renderDrawer->setClippingFor(
            m_hdCampaignLayout.map.getX(),
            m_hdCampaignLayout.map.getY(),
            m_hdCampaignLayout.map.getEndX(),
            m_hdCampaignLayout.map.getEndY()
        );
    }
    if (state == eRegionState::REGSTATE_INTRODUCTION) {
        drawStateIntroduction();
    }
    else if (state == eRegionState::REGSTATE_CONQUER_REGIONS) {
        drawStateConquerRegions();
    }
    else if (state == eRegionState::REGSTATE_SELECT_NEXT_CONQUEST) {
        drawStateSelectYourNextConquest();
    }
    else if (state == eRegionState::REGSTATE_FADEOUT) {
        drawStateConquerRegions();
    }


    if (m_hdLayout) {
        renderDrawer->resetClippingFor();
        renderDrawer->renderRectColor(
            m_hdCampaignLayout.map,
            Color{190, 145, 58, 255}
        );
        drawHdMessage();
    }
    else {
        // Draw this last
        renderDrawer->renderSprite(
            m_gfxworld->getTexture(BMP_NEXTCONQ),
            offsetX,
            offsetY
        );
        drawLogoInFourCorners(iHouse);
        drawManager->drawMessageBar();
    }

    m_guiBtnToMissionSelect->draw();

    drawManager->drawMouse();
}

void cSelectYourNextConquestState::drawHdBackground() const
{
    renderDrawer->renderClearToColor(Color{7, 9, 11, 255});
    if (m_hdBackground) {
        const double sourceAspect = static_cast<double>(m_hdBackground->w) /
            std::max(1, m_hdBackground->h);
        const double screenAspect = static_cast<double>(m_game.m_screenW) /
            std::max(1, m_game.m_screenH);
        cRectangle destination;
        if (sourceAspect > screenAspect) {
            const int width = static_cast<int>(std::ceil(
                m_game.m_screenH * sourceAspect));
            destination = cRectangle(
                (m_game.m_screenW - width) / 2,
                0,
                width,
                m_game.m_screenH
            );
        }
        else {
            const int height = static_cast<int>(std::ceil(
                m_game.m_screenW / sourceAspect));
            destination = cRectangle(
                0,
                (m_game.m_screenH - height) / 2,
                m_game.m_screenW,
                height
            );
        }
        renderDrawer->renderStrechFullSprite(m_hdBackground, destination);
    }
    renderDrawer->renderRectFillColor(
        0,
        0,
        m_game.m_screenW,
        m_game.m_screenH,
        Color{3, 5, 7, 178}
    );
}

void cSelectYourNextConquestState::drawHdChrome() const
{
    renderDrawer->renderRectFillColor(
        m_hdCampaignLayout.panel,
        Color{14, 18, 21, 246}
    );
    renderDrawer->renderRectColor(
        m_hdCampaignLayout.panel,
        Color{82, 58, 27, 255}
    );
    renderDrawer->renderRectColor(
        m_hdCampaignLayout.panel.getX() + 3,
        m_hdCampaignLayout.panel.getY() + 3,
        m_hdCampaignLayout.panel.getWidth() - 6,
        m_hdCampaignLayout.panel.getHeight() - 6,
        Color{190, 145, 58, 255}
    );

    renderDrawer->renderRectFillColor(
        m_hdCampaignLayout.title,
        Color{20, 25, 29, 245}
    );
    renderDrawer->renderRectColor(
        m_hdCampaignLayout.title,
        Color{112, 82, 36, 255}
    );

    m_textDrawer->drawTextCenteredInBox(
        localization::text("SELECT YOUR NEXT REGION", "ВЫБЕРИТЕ СЛЕДУЮЩИЙ РЕГИОН"),
        m_hdCampaignLayout.title,
        Color{239, 194, 88, 255}
    );

    if (m_hdHouseCrest) {
        const int crestSize = std::max(
            28,
            m_hdCampaignLayout.title.getHeight() - 12
        );
        renderDrawer->renderStrechFullSprite(
            m_hdHouseCrest,
            cRectangle(
                m_hdCampaignLayout.title.getX() + 8,
                m_hdCampaignLayout.title.getY() +
                    (m_hdCampaignLayout.title.getHeight() - crestSize) / 2,
                crestSize,
                crestSize
            )
        );
    }
}

void cSelectYourNextConquestState::drawHdMapBase(Uint8 opacity) const
{
    if (m_hdCampaignMap) {
        renderDrawer->renderStrechFullSprite(
            m_hdCampaignMap,
            m_hdCampaignLayout.map,
            opacity
        );
        return;
    }
    renderDrawer->renderStrechFullSprite(
        m_gfxworld->getTexture(WORLD_DUNE),
        m_hdCampaignLayout.map,
        opacity
    );
}

void cSelectYourNextConquestState::drawHdMapBorders(Uint8 opacity) const
{
    if (m_hdRegionBorders) {
        renderDrawer->renderStrechFullSprite(
            m_hdRegionBorders,
            m_hdCampaignLayout.map,
            opacity
        );
    }
}

Texture* cSelectYourNextConquestState::createHdRegionTintTexture(
    int regionIndex,
    int house) const
{
    if (regionClickMapBmp == nullptr ||
        regionIndex < 0 || regionIndex >= MAX_REGIONS) {
        return nullptr;
    }

    SDL_Surface* surface = SDL_CreateRGBSurfaceWithFormat(
        0,
        regionClickMapBmp->w,
        regionClickMapBmp->h,
        32,
        SDL_PIXELFORMAT_RGBA32
    );
    if (surface == nullptr) return nullptr;

    const Color color = campaignHouseColor(house);
    const Uint32 inside = SDL_MapRGBA(
        surface->format,
        color.r,
        color.g,
        color.b,
        255
    );
    const Uint32 outside = SDL_MapRGBA(
        surface->format,
        color.r,
        color.g,
        color.b,
        0
    );
    if (SDL_MUSTLOCK(surface)) SDL_LockSurface(surface);
    for (int y = 0; y < surface->h; ++y) {
        auto* row = reinterpret_cast<Uint32*>(
            static_cast<Uint8*>(surface->pixels) + y * surface->pitch
        );
        for (int x = 0; x < surface->w; ++x) {
            const int pixelRegion = getPixelColorIndexFromSurface(
                regionClickMapBmp,
                x,
                y
            ) - 1;
            row[x] = pixelRegion == regionIndex ? inside : outside;
        }
    }
    if (SDL_MUSTLOCK(surface)) SDL_UnlockSurface(surface);

    Texture* result = createTextureFromSurface(surface);
    SDL_FreeSurface(surface);
    return result;
}

Texture* cSelectYourNextConquestState::createHdRegionBordersTexture() const
{
    if (regionClickMapBmp == nullptr) return nullptr;

    SDL_Surface* surface = SDL_CreateRGBSurfaceWithFormat(
        0,
        regionClickMapBmp->w,
        regionClickMapBmp->h,
        32,
        SDL_PIXELFORMAT_RGBA32
    );
    if (surface == nullptr) return nullptr;

    const Color borderColor{20, 18, 17, 255};
    const Uint32 border = SDL_MapRGBA(
        surface->format,
        borderColor.r,
        borderColor.g,
        borderColor.b,
        210
    );
    const Uint32 transparent = SDL_MapRGBA(
        surface->format,
        borderColor.r,
        borderColor.g,
        borderColor.b,
        0
    );
    if (SDL_MUSTLOCK(surface)) SDL_LockSurface(surface);
    for (int y = 0; y < surface->h; ++y) {
        auto* row = reinterpret_cast<Uint32*>(
            static_cast<Uint8*>(surface->pixels) + y * surface->pitch
        );
        for (int x = 0; x < surface->w; ++x) {
            const Uint8 current = getPixelColorIndexFromSurface(
                regionClickMapBmp,
                x,
                y
            );
            bool isBorder = false;
            if (current > 0 && x + 1 < surface->w) {
                const Uint8 right = getPixelColorIndexFromSurface(
                    regionClickMapBmp,
                    x + 1,
                    y
                );
                isBorder = right > 0 && right != current;
            }
            if (!isBorder && current > 0 && y + 1 < surface->h) {
                const Uint8 below = getPixelColorIndexFromSurface(
                    regionClickMapBmp,
                    x,
                    y + 1
                );
                isBorder = below > 0 && below != current;
            }
            row[x] = isBorder ? border : transparent;
        }
    }
    if (SDL_MUSTLOCK(surface)) SDL_UnlockSurface(surface);

    Texture* result = createTextureFromSurface(surface);
    SDL_FreeSurface(surface);
    return result;
}

void cSelectYourNextConquestState::drawHdMessage() const
{
    renderDrawer->renderRectFillColor(
        m_hdCampaignLayout.message,
        Color{18, 23, 27, 248}
    );
    renderDrawer->renderRectColor(
        m_hdCampaignLayout.message,
        Color{112, 82, 36, 255}
    );
    const std::string message = drawManager->getMessage();
    if (!message.empty()) {
        m_textDrawer->drawTextScaledCenteredInBox(
            message,
            m_hdCampaignLayout.message,
            1.0F,
            Color{232, 225, 199, 255}
        );
    }
}

void cSelectYourNextConquestState::drawLogoInFourCorners(int iHouse) const
{
    int iLogo = -1;

    // Draw your logo
    if (iHouse == ATREIDES)
        iLogo = BMP_NCATR;

    if (iHouse == ORDOS)
        iLogo = BMP_NCORD;

    if (iHouse == HARKONNEN)
        iLogo = BMP_NCHAR;

    // Draw 4 times the logo (in each corner)
    if (iLogo > -1) {
        renderDrawer->renderSprite(m_gfxworld->getTexture(iLogo), offsetX, offsetY);
        renderDrawer->renderSprite(m_gfxworld->getTexture(iLogo), offsetX + (640) - 64, offsetY);
        renderDrawer->renderSprite(m_gfxworld->getTexture(iLogo), offsetX, offsetY + (480) - 64);
        renderDrawer->renderSprite(m_gfxworld->getTexture(iLogo), offsetX + (640) - 64, offsetY + (480) - 64);
    }
}

void cSelectYourNextConquestState::drawStateIntroduction() const
{
    if (m_hdLayout) {
        if (regionSceneState == SCENE_THREE_HOUSES_COME_FOR_DUNE) {
            drawHdMapBase(static_cast<Uint8>(iRegionSceneAlpha));
        }
        else if (regionSceneState == SCENE_TO_TAKE_CONTROL_OF_THE_LAND ||
                 regionSceneState == SCENE_THAT_HAS_BECOME_DIVIDED) {
            drawHdMapBase();
            drawHdMapBorders(static_cast<Uint8>(iRegionSceneAlpha));
        }
        else if (regionSceneState == SCENE_SELECT_YOUR_NEXT_CONQUEST) {
            drawHdMapBase();
            drawHdMapBorders();
        }
        return;
    }
    if (regionSceneState == SCENE_THREE_HOUSES_COME_FOR_DUNE) {
        // draw dune planet (being faded in)
        renderDrawer->renderSprite(m_gfxinter->getTexture(BMP_GAME_DUNE),offsetX, offsetY + 12,iRegionSceneAlpha);
    }
    else if (regionSceneState == SCENE_TO_TAKE_CONTROL_OF_THE_LAND) {
        renderDrawer->renderSprite(m_gfxinter->getTexture(BMP_GAME_DUNE), offsetX, offsetY + 12); // dune is opaque
        renderDrawer->renderSprite(m_gfxworld->getTexture(WORLD_DUNE), offsetX + 16, offsetY + 73, iRegionSceneAlpha);
    }
    else if (regionSceneState == SCENE_THAT_HAS_BECOME_DIVIDED) {
        // now the world map is opaque
        renderDrawer->renderSprite(m_gfxworld->getTexture(WORLD_DUNE), offsetX + 16, offsetY + 73);
        renderDrawer->renderSprite(m_gfxworld->getTexture(WORLD_DUNE_REGIONS), offsetX + 16, offsetY + 73,iRegionSceneAlpha);
    }
    else if (regionSceneState == SCENE_SELECT_YOUR_NEXT_CONQUEST) {
        renderDrawer->renderSprite(m_gfxworld->getTexture(WORLD_DUNE_REGIONS), offsetX + 16, offsetY + 73);
    }
}

void cSelectYourNextConquestState::drawStateConquerRegions() const   // draw dune first
{
    if (m_hdLayout) {
        drawHdMapBase();
        drawHdMapBorders();
    }
    else {
        renderDrawer->renderSprite(m_gfxworld->getTexture(WORLD_DUNE), offsetX + 16, offsetY + 73);
        renderDrawer->renderSprite(m_gfxworld->getTexture(WORLD_DUNE_REGIONS), offsetX + 16, offsetY + 73);
    }

    // draw here stuff
    for (int i = 0; i < 27; i++) {
        regionDraw(world[i]);
    }

    // Animate here (so add regions that are conquered)
    if (isFinishedConqueringRegions && !drawManager->hasMessage()) {
        drawManager->setMessage(localization::text("Select your next region.", "Выберите следующий регион."), true);
    }
}

void cSelectYourNextConquestState::drawStateSelectYourNextConquest() const
{
    if (m_hdLayout) {
        drawHdMapBase();
        drawHdMapBorders();
    }
    else {
        renderDrawer->renderSprite(m_gfxworld->getTexture(WORLD_DUNE), offsetX + 16, offsetY + 73);
        renderDrawer->renderSprite(m_gfxworld->getTexture(WORLD_DUNE_REGIONS), offsetX + 16, offsetY + 73);
    }

    cRegion *pRegion = getRegionMouseIsOver();
    if (pRegion && pRegion->bSelectable) {
        pRegion->iAlpha = 256;
        m_game.getMouse()->setTile(MOUSE_ATTACK);
    }

    // draw here stuff
    for (int i = 0; i < 27; i++) {
        regionDraw(world[i]);
    }

    // Animate here (so add regions that are conquered)
    if (isFinishedConqueringRegions && !drawManager->hasMessage()) {
        drawManager->setMessage(localization::text("Select your next region.", "Выберите следующий регион."), true);
    }
}

void cSelectYourNextConquestState::loadScenarioAndTransitionToNextState(int iMission)
{
    // Calculate mission from region:
    // region 1 = mission 1
    // region 2, 3, 4 = mission 2
    // region 5, 6, 7 = mission 3
    // region 8, 9, 10 = mission 4
    // region 11,12,13 = mission 5
    // region 14,15,16 = mission 6
    // region 17,18,19 = mission 7
    // region 20,21    = mission 8
    // region 22 = mission 9

    // calculate region stuff, and add it up
    int iNewReg = 0;
    if (iMission == 0) iNewReg = 1;
    if (iMission == 1) iNewReg = 2;
    if (iMission == 2) iNewReg = 5;
    if (iMission == 3) iNewReg = 8;
    if (iMission == 4) iNewReg = 11;
    if (iMission == 5) iNewReg = 14;
    if (iMission == 6) iNewReg = 17;
    if (iMission == 7) iNewReg = 20;
    if (iMission == 8) iNewReg = 22;

    // selected....
    int iReg = 0;
    for (int ir = 0; ir < MAX_REGIONS; ir++) {
        if (world[ir].bSelectable) {
            if (ir != regionMouseIsHoveringOver) {
                iReg++;
            }
            else {
                break;
            }
        }
    }

    iNewReg += iReg;

    m_game.missionInit();
    m_game.setNextStateToTransitionTo(GAME_BRIEFING);
    m_game.m_region = iNewReg;
    m_game.m_mission++;                        // FINALLY ADD MISSION NUMBER...

    // set up drawStateMentat
    m_game.createAndPrepareMentatForHumanPlayer();

    // load map
    m_game.loadScenario();

    m_game.playMusicByType(MUSIC_BRIEFING);

    state = REGSTATE_FADEOUT;
    m_game.initiateFadingOut();
}

cRegion *cSelectYourNextConquestState::getRegionMouseIsOver() const
{
    if (regionMouseIsHoveringOver < 0) {
        return nullptr;
    }
    return &world[regionMouseIsHoveringOver];
}

void cSelectYourNextConquestState::regionSetupLostMission()
{
    drawManager->regionInit(offsetX, offsetY);

    selectNextConquestAlpha = 1;

    // prepare players, so we know house index == player index (for colorizing region pieces)
    for (int i = 1; i < FREMEN; i++) {
        players[i].init(i, nullptr);
        players[i].setHouse(i);
    }

    return;
}

void cSelectYourNextConquestState::regionSetupNextMission(int iMission, int iHouse)
{
    // The first mission, nothing is 'ready', as the pieces gets placed and taken by the houses.
    // Later, after mission 2, the pieces are already taken. That's what this function takes care off
    // making sure everything is 'there' to go on with. Hard-coded stuff.
    drawManager->regionInit(offsetX, offsetY);

    // make world pieces not selectable
    for (int i = 0; i < MAX_REGIONS; i++) {
        world[i].bSelectable = false;
    }

    // clear conquer stuff
    memset(iRegionConquer, -1, sizeof(iRegionConquer));
    memset(iRegionHouse, -1, sizeof(iRegionHouse));
    memset(cRegionText, 0, sizeof(cRegionText));

    // Per mission assign:
    // Every house has a different campaign, so...
    cIni::loadRegionfile(iHouse, iMission, this);

    selectNextConquestAlpha = 1;

    // prepare players, so we know house index == player index (for colorizing region pieces)
    for (int i = 1; i < FREMEN; i++) {
        players[i].init(i, nullptr);
        players[i].setHouse(i);
    }

    return;
}

void cSelectYourNextConquestState::regionDraw(cRegion &regionPiece) const
{
    if (regionPiece.iAlpha <= 0) {
        // no alpha, no use in drawing
        return;
    }

    if (regionPiece.iHouse < 0) return;

    int drawHouse = regionPiece.iHouse;
    if (regionPiece.bSelectable &&
        state == eRegionState::REGSTATE_SELECT_NEXT_CONQUEST) {
        drawHouse = players[HUMAN].getHouse();
    }
    if (drawHouse != regionPiece.oldHouse) {
        delete regionPiece.bmpColor;
        if (m_hdLayout) {
            const int regionIndex = static_cast<int>(&regionPiece - world);
            regionPiece.bmpColor = createHdRegionTintTexture(
                regionIndex,
                drawHouse
            );
        }
        else {
            regionPiece.bmpColor = players[drawHouse]
                .createTextureFromIndexedSurfaceWithPalette(
                    regionPiece.bmp,
                    TransparentColorIndex
                );
        }
        regionPiece.oldHouse = drawHouse;
    }
    drawRegion(regionPiece);

}

void cSelectYourNextConquestState::drawRegion(cRegion &regionPiece) const
{
    if (regionPiece.bmpColor ==nullptr) {
        return;
    }
    if (m_hdLayout) {
        const int maximumAlpha = regionPiece.bSelectable ? 132 : 104;
        const Uint8 alpha = static_cast<Uint8>(std::clamp(
            regionPiece.iAlpha * maximumAlpha / 255,
            0,
            maximumAlpha
        ));
        renderDrawer->renderStrechFullSprite(
            regionPiece.bmpColor,
            m_hdCampaignLayout.map,
            alpha
        );
        return;
    }
    const int regionX = offsetX + regionPiece.x;
    const int regionY = offsetY + regionPiece.y;

    if (regionPiece.iAlpha >= 255) {
        renderDrawer->renderSprite(regionPiece.bmpColor, regionX, regionY);
    }
    else {
        renderDrawer->renderSprite(regionPiece.bmpColor, regionX, regionY,regionPiece.iAlpha);
    }
}
// End of function

int cSelectYourNextConquestState::regionOver(int mouseX, int mouseY)
{
    // when mouse is not even on the map, return -1
    const cRectangle mapRect = m_hdLayout
        ? m_hdCampaignLayout.map
        : cRectangle(offsetX + 16, offsetY + 72, 608, 241);
    if (!mapRect.isPointWithin(mouseX, mouseY)) return -1;

    // from here, we are on a region
    const int wCalc = m_hdLayout
        ? m_hdCampaignLayout.clickMapX(mouseX, regionClickMapBmp->w)
        : std::clamp(
            static_cast<int>(std::floor(
                (mouseX - offsetX - 16) * regionClickMapBmp->w / 608.0)),
            0,
            regionClickMapBmp->w - 1
        );
    const int hCalc = m_hdLayout
        ? m_hdCampaignLayout.clickMapY(mouseY, regionClickMapBmp->h)
        : std::clamp(
            static_cast<int>(std::floor(
                (mouseY - offsetY - 73) * regionClickMapBmp->h / 240.0)),
            0,
            regionClickMapBmp->h - 1
        );
    int c = getPixelColorIndexFromSurface(regionClickMapBmp, wCalc, hCalc);
    //std::cout << "REGION_OVER " << mouseX-offsetX << " " << mouseY-offsetY << " " << c << std::endl;
    drawManager->setMessage(localization::format("Region {}", "Регион {}", c - 1));
    return c - 1;
}

void cSelectYourNextConquestState::regionNew(int x, int y, int iAlpha, int iHouse, int iTile)
{
    int iNew = -1;

    for (int i = 0; i < MAX_REGIONS; i++) {
        if (world[i].x < 0 || world[i].y < 0) {
            iNew = i;
            break;
        }
    }

    // invalid index
    if (iNew < 0)
        return;

    cRegion &region = world[iNew];
    region.x = x;
    region.y = y;
    region.iAlpha = iAlpha;
    region.iHouse = iHouse;
    region.iTile = iTile;
    region.bmp = m_gfxworld->getSurface(iTile);
}

void cSelectYourNextConquestState::installWorld()
{
    // create regions
    for (int i = 0; i < MAX_REGIONS; i++) {
        delete world[i].bmpColor;
        world[i].bmpColor = nullptr;
        world[i].bSelectable = false;
        world[i].iAlpha = 0;
        world[i].iHouse = -1;
        world[i].oldHouse = -2; // all <0 except iHouse = -1 (for cache)
        world[i].iTile = -1;
        world[i].x = -1;
        world[i].y = -1;
        world[i].bmp = nullptr;
    }

    // Now create the regions (x,y wise)

    // FIRST ROW (EASY, SAME Y AXIS)
    regionNew(16, 73, 1, -1, PIECE_DUNE_001);
    regionNew(126, 73, 1, -1, PIECE_DUNE_002);
    regionNew(210, 73, 1, -1, PIECE_DUNE_003);
    regionNew(306, 73, 1, -1, PIECE_DUNE_004);
    regionNew(438, 73, 1, -1, PIECE_DUNE_005);
    regionNew(510, 73, 1, -1, PIECE_DUNE_006);

    // SECOND ROW, HARDER FROM NOW ON (DIFFERENT Y AXIS ALL THE TIME)
    regionNew(16, 91, 1, -1, PIECE_DUNE_007);
    regionNew(158, 149, 1, -1, PIECE_DUNE_008);
    regionNew(282, 135, 1, -1, PIECE_DUNE_009);
    regionNew(362, 105, 1, -1, PIECE_DUNE_010);
    regionNew(456, 117, 1, -1, PIECE_DUNE_011);
    regionNew(544, 105, 1, -1, PIECE_DUNE_012);

    // THIRD ROW
    regionNew(16, 155, 1, -1, PIECE_DUNE_013);
    regionNew(58, 165, 1, -1, PIECE_DUNE_014);
    regionNew(190, 213, 1, -1, PIECE_DUNE_015);
    regionNew(312, 163, 1, -1, PIECE_DUNE_016);
    regionNew(388, 163, 1, -1, PIECE_DUNE_017);
    regionNew(502, 167, 1, -1, PIECE_DUNE_018);
    regionNew(576, 167, 1, -1, PIECE_DUNE_019);

    // FOURTH ROW
    regionNew(16, 237, 1, -1, PIECE_DUNE_020);
    regionNew(62, 255, 1, -1, PIECE_DUNE_021);
    regionNew(134, 245, 1, -1, PIECE_DUNE_022);
    regionNew(282, 257, 1, -1, PIECE_DUNE_023);
    regionNew(360, 253, 1, -1, PIECE_DUNE_024);
    regionNew(406, 213, 1, -1, PIECE_DUNE_025);
    regionNew(448, 269, 1, -1, PIECE_DUNE_026);
    regionNew(514, 227, 1, -1, PIECE_DUNE_027);
}

eGameStateType cSelectYourNextConquestState::getType()
{
    return GAMESTATE_SELECT_YOUR_NEXT_CONQUEST;
}

void cSelectYourNextConquestState::conquerRegions()
{
    fastForward = false;
    state = REGSTATE_CONQUER_REGIONS;
}

void cSelectYourNextConquestState::transitionToNextRegionSceneState(eRegionSceneState newSceneState)
{
    regionSceneState = newSceneState;
    iRegionSceneAlpha = 0;
}

void cSelectYourNextConquestState::onNotifyMouseEvent(const s_MouseEvent &event)
{
    switch (event.eventType) {
        case MOUSE_MOVED_TO:
            onMouseMove(event);
            break;
        case MOUSE_LEFT_BUTTON_CLICKED:
            onMouseLeftButtonClicked(event);
            break;
        default:
            break;
    }
    // WARNING: m_guiBtnToMissionSelect can trigger fast-forward. That will destroy this state object,
    // so it will crash if you do anything beyond here with this object!!
    m_guiBtnToMissionSelect->onNotifyMouseEvent(event);
}

void cSelectYourNextConquestState::onMouseMove(const s_MouseEvent &event)
{
    // no interaction unless we select next conquest
    if (state != eRegionState::REGSTATE_SELECT_NEXT_CONQUEST) return;

    this->regionMouseIsHoveringOver = regionOver(event.coords.x, event.coords.y);

    cRegion *region = getRegionMouseIsOver();
    if (region && region->bSelectable) {
        region->iAlpha = 255;
        m_game.getMouse()->setTile(MOUSE_ATTACK);
    }
}

void cSelectYourNextConquestState::onMouseLeftButtonClicked(const s_MouseEvent &)
{
    // no interaction unless we select next conquest
    if (state != eRegionState::REGSTATE_SELECT_NEXT_CONQUEST) return;

    cRegion *pRegion = getRegionMouseIsOver();
    if (pRegion && pRegion->bSelectable) {
        loadScenarioAndTransitionToNextState(m_game.m_mission);
    }
}

void cSelectYourNextConquestState::onNotifyKeyboardEvent(const cKeyboardEvent &event)
{
    if (event.eventType == eKeyEventType::PRESSED) {
        if (event.hasKey(SDL_SCANCODE_ESCAPE)) {
            m_game.setNextStateToTransitionTo(GAME_OPTIONS);
        }
    }
}

void cSelectYourNextConquestState::fastForwardUntilMission(int missionNr, int house)
{
    fastForward = true;
    for (int m = 1; m < missionNr; m++) {
        regionSetupNextMission(m, house);

        for (int i = 0; i < MAX_REGIONS; i++) {
            if (iRegionConquer[i] < 0) continue;
            int houseThatConquersTheRegion = iRegionHouse[i];
            if (houseThatConquersTheRegion < 0) continue;

            int iRegNr = iRegionConquer[i];

            cRegion &region = world[iRegNr];

            region.iAlpha = 255;
            region.iHouse = houseThatConquersTheRegion;

            iRegionConquer[i] = -1;
        }
    }
}
