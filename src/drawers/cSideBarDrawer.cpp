/**
 * @file cSideBarDrawer.cpp
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

#include "cSideBarDrawer.h"
#include "include/sGameServices.h"
#include "data/gfxdata.h"
#include "data/gfxinter.h"
#include "drawers/SDLDrawer.hpp"
#include "drawers/cOrderDrawer.h"
#include "managers/cDrawManager.h"
#include "gameobjects/players/cPlayer.h"
#include "sidebar/cBuildingList.h"
#include "sidebar/cSideBar.h"
#include "sidebar/HudLayout.hpp"
#include "utils/Graphics.hpp"
#include "utils/HdUiTextureLoader.hpp"
#include "context/GameContext.hpp"
#include "context/GraphicsContext.hpp"
#include "context/TextContext.hpp"
#include "controls/cMouse.h"
#include "game/cGameSettings.h"
#include "include/cAssert.h"
#include "include/Texture.hpp"

#include <SDL3/SDL.h>
#include <algorithm>
#include <format>

cSideBarDrawer::cSideBarDrawer(GameContext *ctx, cPlayer *player, sGameServices *services) :
    m_player(player),
    m_gfxinter(ctx->getGraphicsContext()->gfxinter.get()),
    m_sdlDrawer(ctx->getSDLDrawer()),
    m_ctx(ctx),
    m_services(services),
    m_buildingListDrawer(ctx, player),
    m_sidebar(nullptr),
    m_sidebarColor(Color{214, 149, 20,255}),
    m_smallTextDrawer(ctx->getTextContext()->getSmallTextDrawer())
{
    d2tm_assert(player != nullptr);
    d2tm_assert(ctx != nullptr);
    d2tm_assert(services != nullptr);

    m_houseCrests[0] = loadHdUiTexture(
        m_sdlDrawer->getRenderer(),
        "hud_house_atreides.png",
        "HD HUD Atreides crest"
    );
    m_houseCrests[1] = loadHdUiTexture(
        m_sdlDrawer->getRenderer(),
        "hud_house_harkonnen.png",
        "HD HUD Harkonnen crest"
    );
    m_houseCrests[2] = loadHdUiTexture(
        m_sdlDrawer->getRenderer(),
        "hud_house_ordos.png",
        "HD HUD Ordos crest"
    );
}

cSideBarDrawer::~cSideBarDrawer()
{
    for (Texture *&crest : m_houseCrests) {
        delete crest;
        crest = nullptr;
    }
}

void cSideBarDrawer::serviceInit(sGameServices* services)
{
    m_infos = services->info;
    m_mouse = services->mouse;
    m_buildingListDrawer.serviceInit(services);
}

void cSideBarDrawer::onNotifyMouseEvent(const s_MouseEvent &event)
{
    m_buildingListDrawer.onNotifyMouseEvent(event);
}

void cSideBarDrawer::onNotifyKeyboardEvent(const cKeyboardEvent &event)
{
    m_buildingListDrawer.onNotifyKeyboardEvent(event);
}

void cSideBarDrawer::draw()
{
    drawHdSidebar();
}

void cSideBarDrawer::setPlayer(cPlayer *pPlayer)
{
    m_player = pPlayer;
    m_buildingListDrawer.setPlayer(pPlayer);
}

void cSideBarDrawer::drawHdSidebar()
{
    const HudLayout layout = HudLayout::create(
        m_services->settings->getScreenW(),
        m_services->settings->getScreenH()
    );
    m_sdlDrawer->renderRectFillColor(
        layout.sidebar.getX(),
        layout.sidebar.getY(),
        layout.sidebar.getWidth(),
        layout.sidebar.getHeight(),
        Color{12, 15, 17, 255}
    );
    m_sdlDrawer->renderRectFillColor(
        layout.sidebar.getX(),
        cSideBar::TopBarHeight,
        5,
        m_services->settings->getScreenH() - cSideBar::TopBarHeight,
        Color{32, 36, 38, 255}
    );
    m_sdlDrawer->renderLine(
        layout.sidebar.getX() + 5,
        cSideBar::TopBarHeight,
        layout.sidebar.getX() + 5,
        m_services->settings->getScreenH(),
        Color{166, 124, 44, 255}
    );

    drawHdRadarPanel();
    drawHdCapacities();
    drawHdBuildingLists();
}

Texture *cSideBarDrawer::getHouseCrest() const
{
    if (m_player->isHouse(ATREIDES)) {
        return m_houseCrests[0];
    }
    if (m_player->isHouse(HARKONNEN)) {
        return m_houseCrests[1];
    }
    if (m_player->isHouse(ORDOS)) {
        return m_houseCrests[2];
    }
    if (m_player->isHouse(SARDAUKAR)) {
        return m_gfxinter->getTexture(BMP_SELECT_HOUSE_SARDAUKAR);
    }
    return nullptr;
}

std::string cSideBarDrawer::getHouseDisplayName() const
{
    if (m_player->isHouse(ATREIDES)) {
        return "HOUSE ATREIDES";
    }
    if (m_player->isHouse(HARKONNEN)) {
        return "HOUSE HARKONNEN";
    }
    if (m_player->isHouse(ORDOS)) {
        return "HOUSE ORDOS";
    }
    if (m_player->isHouse(SARDAUKAR)) {
        return "SARDAUKAR";
    }
    return "UNKNOWN HOUSE";
}

void cSideBarDrawer::drawHdRadarPanel()
{
    const HudLayout layout = HudLayout::create(
        m_services->settings->getScreenW(),
        m_services->settings->getScreenH()
    );
    const Color panel{16, 20, 22, 255};
    const Color panelInner{7, 10, 11, 255};
    const Color brass{151, 113, 43, 255};
    const Color text{235, 225, 191, 255};
    const Color accent = m_player->getSelectFadingColor();

    m_sdlDrawer->renderRectFillColor(
        layout.radarPanel.getX(),
        layout.radarPanel.getY(),
        layout.radarPanel.getWidth(),
        layout.radarPanel.getHeight(),
        panel
    );
    m_sdlDrawer->renderRectColor(
        layout.radarPanel.getX(),
        layout.radarPanel.getY(),
        layout.radarPanel.getWidth(),
        layout.radarPanel.getHeight(),
        brass
    );
    m_sdlDrawer->renderRectFillColor(
        layout.houseHeader.getX(),
        layout.houseHeader.getY(),
        layout.houseHeader.getWidth(),
        layout.houseHeader.getHeight(),
        Color{25, 29, 30, 255}
    );
    m_sdlDrawer->renderRectFillColor(
        layout.houseHeader.getX(),
        layout.houseHeader.getEndY() - 2,
        layout.houseHeader.getWidth(),
        2,
        accent
    );

    Texture *crest = getHouseCrest();
    const int headerCrestSize = 24;
    if (crest != nullptr) {
        m_sdlDrawer->renderStrechFullSprite(
            crest,
            cRectangle(
                layout.houseHeader.getX() + 3,
                layout.houseHeader.getY() + 2,
                headerCrestSize,
                headerCrestSize
            )
        );
    }
    m_smallTextDrawer->drawText(
        layout.houseHeader.getX() + headerCrestSize + 10,
        layout.houseHeader.getY() + 7,
        text,
        getHouseDisplayName(),
        false
    );

    m_sdlDrawer->renderRectFillColor(
        layout.radarViewport.getX(),
        layout.radarViewport.getY(),
        layout.radarViewport.getWidth(),
        layout.radarViewport.getHeight(),
        panelInner
    );
    m_sdlDrawer->renderRectColor(
        layout.radarViewport.getX(),
        layout.radarViewport.getY(),
        layout.radarViewport.getWidth(),
        layout.radarViewport.getHeight(),
        Color{62, 68, 67, 255}
    );

    if (!m_player->hasRadarAndEnoughPower() && crest != nullptr) {
        const int crestSize = std::min(
            96,
            layout.radarViewport.getHeight() - 18
        );
        m_sdlDrawer->renderStrechFullSprite(
            crest,
            cRectangle(
                layout.radarViewport.getX() +
                    (layout.radarViewport.getWidth() - crestSize) / 2,
                layout.radarViewport.getY() +
                    (layout.radarViewport.getHeight() - crestSize) / 2,
                crestSize,
                crestSize
            ),
            210
        );
    }
}

void cSideBarDrawer::drawHdMeter(
    const cRectangle &rect,
    const std::string &label,
    int value,
    int maximum,
    Color fill,
    bool warning) const
{
    const int safeMaximum = std::max(1, maximum);
    const float ratio = std::clamp(
        static_cast<float>(value) / static_cast<float>(safeMaximum),
        0.0f,
        1.0f
    );
    const Color border{104, 82, 43, 255};
    const Color text{225, 218, 190, 255};
    const Color warningColor = warning
        ? m_player->getErrorFadingColor()
        : fill;

    m_sdlDrawer->renderRectFillColor(
        rect.getX(),
        rect.getY(),
        rect.getWidth(),
        rect.getHeight(),
        Color{10, 13, 15, 255}
    );
    m_sdlDrawer->renderRectColor(
        rect.getX(),
        rect.getY(),
        rect.getWidth(),
        rect.getHeight(),
        border
    );
    m_smallTextDrawer->drawText(
        rect.getX() + 4,
        rect.getY() + 2,
        text,
        label,
        false
    );
    const std::string amount = std::format("{}/{}", value, maximum);
    const int amountWidth = m_smallTextDrawer->getTextLength(amount);
    m_smallTextDrawer->drawText(
        rect.getEndX() - amountWidth - 4,
        rect.getY() + 2,
        text,
        amount,
        false
    );

    const int barX = rect.getX() + 4;
    const int barY = rect.getEndY() - 7;
    const int barWidth = rect.getWidth() - 8;
    m_sdlDrawer->renderRectFillColor(
        barX,
        barY,
        barWidth,
        4,
        Color{31, 35, 36, 255}
    );
    m_sdlDrawer->renderRectFillColor(
        barX,
        barY,
        static_cast<int>(barWidth * ratio),
        4,
        warningColor
    );
}

void cSideBarDrawer::drawHdCapacities()
{
    const HudLayout layout = HudLayout::create(
        m_services->settings->getScreenW(),
        m_services->settings->getScreenH()
    );
    const int produced = std::max(0, m_player->getPowerProduced());
    const int used = std::max(0, m_player->getPowerUsage());
    drawHdMeter(
        layout.powerMeter,
        layout.powerMeter.getWidth() < 140 ? "PWR" : "POWER",
        used,
        produced,
        Color{72, 202, 103, 255},
        !m_player->bEnoughPower()
    );

    drawHdMeter(
        layout.spiceMeter,
        layout.spiceMeter.getWidth() < 140 ? "SPC" : "SPICE",
        std::max(0, m_player->getCredits()),
        std::max(1, static_cast<int>(m_player->getMaxCredits())),
        Color{218, 139, 47, 255},
        !m_player->bEnoughSpiceCapacityToStoreCredits()
    );
}

void cSideBarDrawer::drawHdBuildingLists()
{
    m_sidebar = m_player->getSideBar();
    const int selectedListId = m_sidebar->getSelectedListID();
    cBuildingList *selectedList = nullptr;
    if (selectedListId >= 0 && selectedListId < cSideBar::LIST_MAX) {
        selectedList = m_sidebar->getList(selectedListId);
    }

    const HudLayout layout = HudLayout::create(
        m_services->settings->getScreenW(),
        m_services->settings->getScreenH(),
        selectedList != nullptr &&
            selectedList->getType() == eListType::LIST_STARPORT
    );

    m_sdlDrawer->renderRectFillColor(
        layout.tabs.getX(),
        layout.tabs.getY(),
        layout.tabs.getWidth(),
        layout.tabs.getHeight(),
        Color{13, 16, 18, 255}
    );

    const int startPos = eListTypeAsInt(eListType::LIST_CONSTYARD);
    for (int listId = startPos; listId < cSideBar::LIST_MAX; ++listId) {
        cBuildingList *list = m_sidebar->getList(listId);
        m_buildingListDrawer.drawButton(
            list,
            selectedListId == listId
        );
    }

    m_sdlDrawer->renderRectFillColor(
        layout.catalog.getX(),
        layout.catalog.getY(),
        layout.catalog.getWidth(),
        layout.catalog.getHeight(),
        Color{12, 15, 17, 255}
    );
    m_sdlDrawer->renderRectColor(
        layout.catalog.getX(),
        layout.catalog.getY(),
        layout.catalog.getWidth(),
        layout.catalog.getHeight(),
        Color{93, 75, 40, 255}
    );

    if (selectedList != nullptr) {
        m_buildingListDrawer.drawList(selectedList, selectedListId);
    }

    for (int listId = startPos; listId < cSideBar::LIST_MAX; ++listId) {
        if (listId == selectedListId) {
            continue;
        }
        cBuildingList *list = m_sidebar->getList(listId);
        if (list->isAvailable() &&
            list->isOverButton(m_mouse->getX(), m_mouse->getY())) {
            m_buildingListDrawer.drawButtonHoverRectangle(list);
        }
    }

    if (selectedList != nullptr &&
        selectedList->getType() == eListType::LIST_STARPORT) {
        m_services->drawManager->getOrderDrawer()->drawOrderButton(m_player);
    }
}
