/**
 * @file cSelectYourNextConquestState.cpp
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

#include "cSelectYourNextConquestState.h"

#include <cmath>
#include "controls/eKeyAction.h"
#include "controls/cMouse.h"
#include "data/gfxdata.h"
#include "data/gfxinter.h"
#include "include/gfxworld.h"
#include "drawers/SDLDrawer.hpp"
#include "drawers/cMessageDrawer.h"
#include "utils/ini.h"
#include "utils/texture_utils.h"
#include "include/sDataCampaign.h"
#include "managers/cDrawManager.h"
#include "gameobjects/players/cPlayer.h"
#include "gui/GuiButton.h"
#include "utils/Graphics.hpp"
#include "context/GameContext.hpp"
#include "context/AudioContext.hpp"
#include "context/cGameObjectContext.h"
#include "game/GameStateTransition.hpp"
#include "game/MentatFlow.hpp"
#include "game/MissionFlow.hpp"
#include "game/ScenarioFlow.hpp"
#include "drawers/cTextDrawer.h"

#include <SDL3/SDL.h>
#include <iostream>
#include <format>
#include "include/cAssert.h"
#include "context/GraphicsContext.hpp"
#include "context/TextContext.hpp"
#include "game/cGameSettings.h"
#include "include/sGameServices.h"
#include "include/Texture.hpp"
#include "include/eGameState.h"
#include "controls/cKeyboardEvent.h"
#include "controls/sMouseEvent.h"
#include <algorithm>
#include "utils/HdUiTextureLoader.hpp"
#include "debug/UiAudit.hpp"
#include "utils/Localization.hpp"

// Return color index from pixel (x, y) in surface
static Uint8 getPixelColorIndexFromSurface(SDL_Surface *surface, int x, int y)
{
    if (surface == nullptr) {
        std::cerr << "Error : nullptr surface" << std::endl;
        return 0;
    }

    if (surface->format != SDL_PIXELFORMAT_INDEX8) {
        std::cerr << "Error : no indexed 8 bits surface (format actuel : "
                  << SDL_GetPixelFormatName(surface->format) << ")." << std::endl;
        return 0;
    }

    if (x < 0 || x >= surface->w || y < 0 || y >= surface->h) {
        std::cerr << "Error : out of range pixel (" << x << ", " << y << ") in (" << surface->w << ", " << surface->h << ")." << std::endl;
        return 0;
    }
    Uint8 *pixelData = static_cast<Uint8 *>(surface->pixels);
    Uint8 colorIndex = pixelData[y * (surface->pitch) + x];
    return colorIndex;
}

cSelectYourNextConquestState::cSelectYourNextConquestState(sGameServices* services, cIni* ini, s_DataCampaign* dataCompaign) :
    cGameState(services),
    m_settings(services->settings),
    m_scenarioFlow(services->scenarioFlow),
    m_audioContext(m_ctx->getAudioContext()),
    m_stateTransitions(services->stateTransitions),
    m_mentatFlow(services->mentatFlow),
    m_missionFlow(services->missionFlow),
    m_textDrawer(m_ctx->getTextContext()->getBeneTextDrawer()),
    m_objects(services->objects),
    m_dataCampaign(dataCompaign),
    m_gfxworld(m_ctx->getGraphicsContext()->gfxworld.get()),
    m_gfxinter(m_ctx->getGraphicsContext()->gfxinter.get()),
    m_cIni(ini)
{
    d2tm_assert(m_settings != nullptr);
    d2tm_assert(m_scenarioFlow != nullptr);
    d2tm_assert(m_audioContext != nullptr);
    d2tm_assert(m_stateTransitions != nullptr);
    d2tm_assert(m_mentatFlow != nullptr);
    d2tm_assert(m_missionFlow != nullptr);
    d2tm_assert(m_textDrawer != nullptr);
    d2tm_assert(m_dataCampaign != nullptr);
    d2tm_assert(m_gfxworld != nullptr);
    d2tm_assert(m_gfxinter != nullptr);
    d2tm_assert(m_cIni != nullptr);
    state = eRegionState::REGSTATE_INIT;
    regionSceneState = eRegionSceneState::SCENE_INIT;
    m_mouse = services->mouse;
    d2tm_assert(m_mouse != nullptr);

    m_drawManager = services->drawManager;
	d2tm_assert(m_drawManager != nullptr);
    iRegionSceneAlpha = 0;  // alpha for scene in introduction state

    std::fill(std::begin(iRegionConquer), std::end(iRegionConquer), -1);
    std::fill(std::begin(iRegionHouse), std::end(iRegionHouse), -1);
    for (auto &text : cRegionText) {
        text.clear();
    }

    m_hdCampaignLayout = CampaignMapLayout::create(
        m_settings->getScreenW(),
        m_settings->getScreenH()
    );
    m_hdBackground = loadHdUiTexture(
        m_sdlDrawer->getRenderer(),
        "main_menu_background.png",
        "HD campaign map background"
    );
    m_hdCampaignMap = loadHdUiTexture(
        m_sdlDrawer->getRenderer(),
        "campaign_map.png",
        "HD campaign map"
    );

    std::string houseCrestFile;
    switch (m_objects->getPlayer(0)->getHouse()) {
        case ATREIDES:
            houseCrestFile = "hud_house_atreides.png";
            break;
        case HARKONNEN:
            houseCrestFile = "hud_house_harkonnen.png";
            break;
        case ORDOS:
            houseCrestFile = "hud_house_ordos.png";
            break;
        default:
            break;
    }
    if (!houseCrestFile.empty()) {
        m_hdHouseCrest = loadHdUiTexture(
            m_sdlDrawer->getRenderer(),
            houseCrestFile,
            "HD campaign house crest"
        );
    }

    calculateOffset();

    regionClickMapBmp = nullptr;

    regionMouseIsHoveringOver = -1;
    isFinishedConqueringRegions = true;

    const cRectangle toMissionSelectRect = m_hdCampaignLayout.missionButton;
    m_guiBtnToMissionSelect = GuiButtonBuilder()
            .withRect(toMissionSelectRect)        
            .withLabel(localization::text("Mission select", "Выбор миссии"))
            .withKind(GuiRenderKind::REMASTER_BUTTON)
            .withTextDrawer(m_textDrawer)
            .withRenderer(m_sdlDrawer)
            .withTheme(GuiTheme::Remaster())
            .onClick([this]() {
                m_stateTransitions->setNextState(eGameState::MISSIONSELECT);})
            .build();
}

void cSelectYourNextConquestState::calculateOffset()
{
    offsetX = m_hdCampaignLayout.panel.getX();
    offsetY = m_hdCampaignLayout.panel.getY();
}

cSelectYourNextConquestState::~cSelectYourNextConquestState()
{
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
        if (m_hdRegionBorders == nullptr) {
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

        int iHouse = m_objects->getPlayer(0)->getHouse();
        int iMission = m_dataCampaign->mission;

        bool hasMessage = m_drawManager->hasMessage();

        if (regionSceneState == SCENE_INIT) {
            regionSetupNextMission(iMission, iHouse);
            m_drawManager->setMessage(localization::text("3 Houses have come to Dune.", "Три Дома прибыли на Дюну."));
            transitionToNextRegionSceneState(SCENE_THREE_HOUSES_COME_FOR_DUNE);
        }
        else if (regionSceneState == SCENE_THREE_HOUSES_COME_FOR_DUNE) {
            if (!hasMessage && iRegionSceneAlpha >= 255) {
                m_drawManager->setMessage(localization::text("To take control of the land.", "Чтобы покорить её земли."));
                transitionToNextRegionSceneState(SCENE_TO_TAKE_CONTROL_OF_THE_LAND);
            }
        }
        else if (regionSceneState == SCENE_TO_TAKE_CONTROL_OF_THE_LAND) {
            if (!hasMessage && iRegionSceneAlpha >= 255) {
                m_drawManager->setMessage(localization::text("That has become divided.", "Теперь Дюна разделена."));
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
                if (m_mouse->isLeftButtonPressed()) {
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
                const std::string &regionTextString = cRegionText[i];
                bool isRegionTextGiven = !regionTextString.empty();
                bool isRegionTextEmpty = regionTextString.empty();

                if ((isRegionTextGiven && !m_drawManager->hasMessage()) || isRegionTextEmpty) {
                    // set this up
                    region.iHouse = houseThatConquersTheRegion;
                    region.iAlpha = 1; // this makes it > 0 and thus it will become opaque over time (see THINK function)

                    if (isRegionTextGiven) {
                        m_drawManager->setMessage(regionTextString);
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
    m_mouse->setTile(MOUSE_NORMAL); // global state of mouse
    if (uiaudit::isEnabled() && state == eRegionState::REGSTATE_SELECT_NEXT_CONQUEST) {
        const cRectangle mapRect = m_hdCampaignLayout.map;
        uiaudit::recordClick("campaign-region-map", mapRect.getX(), mapRect.getY(), mapRect.getWidth(), mapRect.getHeight());
    }
    // STEPS:
    // 1. Show current conquered regions
    // 2. Show next progress + story (in message bar)
    // 3. Click next region
    // 4. Set up region and go to eGameState::BRIEFING, which will do the rest...-> fade out

    drawHdBackground();
    drawHdChrome();

    m_sdlDrawer->setClippingFor(
        m_hdCampaignLayout.map.getX(),
        m_hdCampaignLayout.map.getY(),
        m_hdCampaignLayout.map.getEndX(),
        m_hdCampaignLayout.map.getEndY()
    );
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

    m_sdlDrawer->resetClippingFor();
    m_sdlDrawer->renderRectColor(
        m_hdCampaignLayout.map,
        Color{190, 145, 58, 255}
    );
    drawHdMessage();

    m_guiBtnToMissionSelect->draw();

    m_drawManager->drawMouse();
}

void cSelectYourNextConquestState::drawHdBackground() const
{
    const int screenWidth = m_settings->getScreenW();
    const int screenHeight = m_settings->getScreenH();
    m_sdlDrawer->renderClearToColor(Color{7, 9, 11, 255});
    if (m_hdBackground) {
        const double sourceAspect = static_cast<double>(m_hdBackground->w) /
            std::max(1, m_hdBackground->h);
        const double screenAspect = static_cast<double>(screenWidth) /
            std::max(1, screenHeight);
        cRectangle destination;
        if (sourceAspect > screenAspect) {
            const int width = static_cast<int>(std::ceil(
                screenHeight * sourceAspect));
            destination = cRectangle(
                (screenWidth - width) / 2,
                0,
                width,
                screenHeight
            );
        }
        else {
            const int height = static_cast<int>(std::ceil(
                screenWidth / sourceAspect));
            destination = cRectangle(
                0,
                (screenHeight - height) / 2,
                screenWidth,
                height
            );
        }
        m_sdlDrawer->renderStrechFullSprite(m_hdBackground, destination);
    }
    m_sdlDrawer->renderRectFillColor(
        0,
        0,
        screenWidth,
        screenHeight,
        Color{3, 5, 7, 178}
    );
}

void cSelectYourNextConquestState::drawHdChrome() const
{
    m_sdlDrawer->renderRectFillColor(
        m_hdCampaignLayout.panel,
        Color{14, 18, 21, 246}
    );
    m_sdlDrawer->renderRectColor(
        m_hdCampaignLayout.panel,
        Color{82, 58, 27, 255}
    );
    m_sdlDrawer->renderRectColor(
        m_hdCampaignLayout.panel.getX() + 3,
        m_hdCampaignLayout.panel.getY() + 3,
        m_hdCampaignLayout.panel.getWidth() - 6,
        m_hdCampaignLayout.panel.getHeight() - 6,
        Color{190, 145, 58, 255}
    );

    m_sdlDrawer->renderRectFillColor(
        m_hdCampaignLayout.title,
        Color{20, 25, 29, 245}
    );
    m_sdlDrawer->renderRectColor(
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
        m_sdlDrawer->renderStrechFullSprite(
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
        m_sdlDrawer->renderStrechFullSprite(
            m_hdCampaignMap,
            m_hdCampaignLayout.map,
            opacity
        );
        return;
    }
    m_sdlDrawer->renderStrechFullSprite(
        m_gfxworld->getTexture(WORLD_DUNE),
        m_hdCampaignLayout.map,
        opacity
    );
}

void cSelectYourNextConquestState::drawHdMapBorders(Uint8 opacity) const
{
    if (m_hdRegionBorders) {
        m_sdlDrawer->renderStrechFullSprite(
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

    SDL_Surface* surface = SDL_CreateSurface(
        regionClickMapBmp->w,
        regionClickMapBmp->h,
        SDL_PIXELFORMAT_RGBA32
    );
    if (surface == nullptr) return nullptr;

    Color color{126, 118, 102, 255};
    switch (house) {
        case HARKONNEN:
            color = Color{194, 48, 42, 255};
            break;
        case ATREIDES:
            color = Color{45, 92, 192, 255};
            break;
        case ORDOS:
            color = Color{52, 156, 67, 255};
            break;
        default:
            break;
    }

    const auto* format = SDL_GetPixelFormatDetails(surface->format);
    const auto* palette = SDL_GetSurfacePalette(surface);
    const Uint32 inside = SDL_MapRGBA(
        format,
        palette,
        color.r,
        color.g,
        color.b,
        255
    );
    const Uint32 outside = SDL_MapRGBA(
        format,
        palette,
        color.r,
        color.g,
        color.b,
        0
    );
    if (!SDL_LockSurface(surface)) {
        SDL_DestroySurface(surface);
        return nullptr;
    }
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
    SDL_UnlockSurface(surface);

    SDL_Texture* texture = SDL_CreateTextureFromSurface(
        m_sdlDrawer->getRenderer(),
        surface
    );
    SDL_DestroySurface(surface);
    if (texture == nullptr) return nullptr;
    SDL_SetTextureBlendMode(texture, SDL_BLENDMODE_BLEND);
    SDL_SetTextureScaleMode(texture, SDL_SCALEMODE_LINEAR);
    return new Texture(texture, regionClickMapBmp->w, regionClickMapBmp->h, false, m_gfxworld->getDensity());
}

Texture* cSelectYourNextConquestState::createHdRegionBordersTexture() const
{
    if (regionClickMapBmp == nullptr) return nullptr;

    SDL_Surface* surface = SDL_CreateSurface(
        regionClickMapBmp->w,
        regionClickMapBmp->h,
        SDL_PIXELFORMAT_RGBA32
    );
    if (surface == nullptr) return nullptr;

    const Color borderColor{20, 18, 17, 255};
    const auto* format = SDL_GetPixelFormatDetails(surface->format);
    const auto* palette = SDL_GetSurfacePalette(surface);
    const Uint32 border = SDL_MapRGBA(
        format,
        palette,
        borderColor.r,
        borderColor.g,
        borderColor.b,
        210
    );
    const Uint32 transparent = SDL_MapRGBA(
        format,
        palette,
        borderColor.r,
        borderColor.g,
        borderColor.b,
        0
    );
    if (!SDL_LockSurface(surface)) {
        SDL_DestroySurface(surface);
        return nullptr;
    }
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
    SDL_UnlockSurface(surface);

    SDL_Texture* texture = SDL_CreateTextureFromSurface(
        m_sdlDrawer->getRenderer(),
        surface
    );
    SDL_DestroySurface(surface);
    if (texture == nullptr) return nullptr;
    SDL_SetTextureBlendMode(texture, SDL_BLENDMODE_BLEND);
    SDL_SetTextureScaleMode(texture, SDL_SCALEMODE_LINEAR);
    return new Texture(texture, regionClickMapBmp->w, regionClickMapBmp->h, false, m_gfxworld->getDensity());
}

void cSelectYourNextConquestState::drawHdMessage() const
{
    m_sdlDrawer->renderRectFillColor(
        m_hdCampaignLayout.message,
        Color{18, 23, 27, 248}
    );
    m_sdlDrawer->renderRectColor(
        m_hdCampaignLayout.message,
        Color{112, 82, 36, 255}
    );
    const std::string message = m_drawManager->getMessage();
    if (!message.empty()) {
        m_textDrawer->drawTextScaledCenteredInBox(
            message,
            m_hdCampaignLayout.message,
            1.0F,
            Color{232, 225, 199, 255}
        );
    }
}

void cSelectYourNextConquestState::drawStateIntroduction() const
{
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
}

void cSelectYourNextConquestState::drawStateConquerRegions() const   // draw dune first
{
    drawHdMapBase();
    drawHdMapBorders();

    // draw here stuff
    for (int i = 0; i < 27; i++) {
        regionDraw(world[i]);
    }

    // Animate here (so add regions that are conquered)
    if (isFinishedConqueringRegions && !m_drawManager->hasMessage()) {
        m_drawManager->setMessage(localization::text("Select your next region.", "Выберите следующий регион."), true);
    }
}

void cSelectYourNextConquestState::drawStateSelectYourNextConquest() const
{
    drawHdMapBase();
    drawHdMapBorders();

    cRegion *pRegion = getRegionMouseIsOver();
    if (pRegion && pRegion->bSelectable) {
        pRegion->iAlpha = 256;
        m_mouse->setTile(MOUSE_ATTACK);
    }

    // draw here stuff
    for (int i = 0; i < 27; i++) {
        regionDraw(world[i]);
    }

    // Animate here (so add regions that are conquered)
    if (isFinishedConqueringRegions && !m_drawManager->hasMessage()) {
        m_drawManager->setMessage(localization::text("Select your next region.", "Выберите следующий регион."), true);
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

    m_missionFlow->init();
    m_stateTransitions->setNextState(eGameState::BRIEFING);
    m_dataCampaign->region = iNewReg;
    m_dataCampaign->mission++;                        // FINALLY ADD MISSION NUMBER...

    // set up drawStateMentat
    m_mentatFlow->prepareForPlayer();

    // load map
    m_scenarioFlow->loadScenario();

    m_audioContext->playMusicByType(eMusicType::BRIEFING, false, false, m_objects->getPlayer(HUMAN)->getHouse());

    state = REGSTATE_FADEOUT;
    m_stateTransitions->fadeOut();
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
    m_drawManager->regionInit(offsetX, offsetY);

    selectNextConquestAlpha = 1;

    // prepare players, so we know house index == player index (for colorizing region pieces)
    for (int i = 1; i < FREMEN; i++) {
        m_objects->getPlayer(i)->init(i, nullptr);
        m_objects->getPlayer(i)->setHouse(i);
    }

    return;
}

void cSelectYourNextConquestState::regionSetupNextMission(int iMission, int iHouse)
{
    // The first mission, nothing is 'ready', as the pieces gets placed and taken by the houses.
    // Later, after mission 2, the pieces are already taken. That's what this function takes care off
    // making sure everything is 'there' to go on with. Hard-coded stuff.
    m_drawManager->regionInit(offsetX, offsetY);

    // make world pieces not selectable
    for (int i = 0; i < MAX_REGIONS; i++) {
        world[i].bSelectable = false;
    }

    // clear conquer stuff
    std::fill(std::begin(iRegionConquer), std::end(iRegionConquer), -1);
    std::fill(std::begin(iRegionHouse), std::end(iRegionHouse), -1);
    for (auto &text : cRegionText) {
        text.clear();
    }

    // Per mission assign:
    // Every house has a different campaign, so...
    m_cIni->loadRegionfile(world, iHouse, iMission, this);

    selectNextConquestAlpha = 1;

    // prepare players, so we know house index == player index (for colorizing region pieces)
    for (int i = 1; i < FREMEN; i++) {
        m_objects->getPlayer(i)->init(i, nullptr);
        m_objects->getPlayer(i)->setHouse(i);
    }

    return;
}

void cSelectYourNextConquestState::regionDraw(cRegion &regionPiece) const
{
    if (regionPiece.iAlpha <= 0) {
        return;
    }

    if (regionPiece.iHouse < 0) return;

    int drawHouse = regionPiece.iHouse;
    if (regionPiece.bSelectable && state == eRegionState::REGSTATE_SELECT_NEXT_CONQUEST) {
        drawHouse = m_objects->getPlayer(HUMAN)->getHouse();
    }
    if (drawHouse != regionPiece.oldHouse) {
        delete regionPiece.bmpColor;
        const int regionIndex = static_cast<int>(&regionPiece - world.data());
        regionPiece.bmpColor = createHdRegionTintTexture(regionIndex, drawHouse);
        regionPiece.oldHouse = drawHouse;
    }
    drawRegion(regionPiece);

}

void cSelectYourNextConquestState::drawRegion(cRegion &regionPiece) const
{
    if (regionPiece.bmpColor ==nullptr) {
        return;
    }
    const int maximumAlpha = regionPiece.bSelectable ? 132 : 104;
    const Uint8 alpha = static_cast<Uint8>(std::clamp(
        regionPiece.iAlpha * maximumAlpha / 255,
        0,
        maximumAlpha
    ));
    m_sdlDrawer->renderStrechFullSprite(
        regionPiece.bmpColor,
        m_hdCampaignLayout.map,
        alpha
    );
}
// End of function

int cSelectYourNextConquestState::regionOver(int mouseX, int mouseY)
{
    // when mouse is not even on the map, return -1
    const cRectangle mapRect = m_hdCampaignLayout.map;
    if (!mapRect.isPointWithin(mouseX, mouseY)) return -1;

    // from here, we are on a region
    const int wCalc = m_hdCampaignLayout.clickMapX(mouseX, regionClickMapBmp->w);
    const int hCalc = m_hdCampaignLayout.clickMapY(mouseY, regionClickMapBmp->h);
    int c = getPixelColorIndexFromSurface(regionClickMapBmp, wCalc, hCalc);
    //std::cout << "REGION_OVER " << mouseX-offsetX << " " << mouseY-offsetY << " " << c << std::endl;
    m_drawManager->setMessage(localization::format("region {}", "регион {}",c-1));
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
            if (onMouseLeftButtonClicked(event)) {
                return;
            }
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
        m_mouse->setTile(MOUSE_ATTACK);
    }
}

bool cSelectYourNextConquestState::onMouseLeftButtonClicked(const s_MouseEvent &)
{
    // no interaction unless we select next conquest
    if (state != eRegionState::REGSTATE_SELECT_NEXT_CONQUEST) return false;

    cRegion *pRegion = getRegionMouseIsOver();
    if (pRegion && pRegion->bSelectable) {
        loadScenarioAndTransitionToNextState(m_dataCampaign->mission);
        return true;
    }
    return false;
}

void cSelectYourNextConquestState::onNotifyKeyboardEvent(const cKeyboardEvent &event)
{
    if (event.isType(eKeyEventType::PRESSED)) {
        if (event.isAction(eKeyAction::MENU_BACK)) {
            m_stateTransitions->setNextState(eGameState::OPTIONS);
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
