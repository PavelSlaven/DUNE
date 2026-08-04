#include "cSideBarDrawer.h"

#include "d2tmc.h"
#include "data/gfxinter.h"
#include "drawers/SDLDrawer.hpp"
#include "drawers/cOrderDrawer.h"
#include "managers/cDrawManager.h"
#include "player/cPlayer.h"
#include "utils/Graphics.hpp"
#include "utils/Localization.hpp"
#include <SDL2/SDL.h>
#include "context/GameContext.hpp"
#include "context/GraphicsContext.hpp"
#include "context/TextContext.hpp"
#include "sidebar/HudLayout.hpp"
#include "utils/HdUiTextureLoader.hpp"
#include <algorithm>
#include <format>

cSideBarDrawer::cSideBarDrawer(GameContext *ctx, cPlayer *player) :
    m_player(player),
    m_gfxinter(ctx->getGraphicsContext()->gfxinter.get()),
    m_buildingListDrawer(ctx, player),
    m_sidebar(nullptr),
    m_sidebarColor(Color{214, 149, 20,255}),
    m_smallTextDrawer(ctx->getTextContext()->getSmallTextDrawer())
{
    assert(player);

    candyBarBall = m_player->createTextureFromIndexedSurfaceWithPalette(
        m_gfxinter->getSurface(BMP_GERALD_CANDYBAR_BALL), TransparentColorIndex);
    candyBarPiece = m_player->createTextureFromIndexedSurfaceWithPalette(
        m_gfxinter->getSurface(BMP_GERALD_CANDYBAR_PIECE), TransparentColorIndex);
    candyHorizonBar = m_player->createTextureFromIndexedSurfaceWithPalette(
        m_gfxinter->getSurface(HORIZONTAL_CANDYBAR), TransparentColorIndex);

    candiBarRenderer = renderDrawer->createRenderTargetTexture(cSideBar::SidebarWidth, game.m_screenH-40);
    renderDrawer->beginDrawingToTexture(candiBarRenderer);
    createCandyBar();
    renderDrawer->endDrawingToTexture();

    if (game.isHdGraphicsActive()) {
        const int density = game.getGraphicsDensity();
        m_houseCrests[0] = loadHdUiTexture(
            "hud_house_atreides.png",
            density,
            "HD HUD Atreides crest"
        );
        m_houseCrests[1] = loadHdUiTexture(
            "hud_house_harkonnen.png",
            density,
            "HD HUD Harkonnen crest"
        );
        m_houseCrests[2] = loadHdUiTexture(
            "hud_house_ordos.png",
            density,
            "HD HUD Ordos crest"
        );
    }
}

cSideBarDrawer::~cSideBarDrawer()
{
    if (candyBarBall)
        delete candyBarBall;
    if (candyBarPiece)
        delete candyBarPiece;
    if (candyHorizonBar)
        delete candyHorizonBar;

    if (candiBarRenderer)
        delete candiBarRenderer;

    for (Texture *&crest : m_houseCrests) {
        delete crest;
        crest = nullptr;
    }
}

void cSideBarDrawer::onNotifyMouseEvent(const s_MouseEvent &event)
{
    m_buildingListDrawer.onNotifyMouseEvent(event);
}

void cSideBarDrawer::onNotifyKeyboardEvent(const cKeyboardEvent &event)
{
    m_buildingListDrawer.onNotifyKeyboardEvent(event);
}

// draws the sidebar on screen
void cSideBarDrawer::draw()
{
    if (game.isHdGraphicsActive()) {
        drawHdSidebar();
        return;
    }

    // black out sidebar
    renderDrawer->renderRectFillColor((game.m_screenW - cSideBar::SidebarWidth), 0, cSideBar::SidebarWidth, game.m_screenH, Color{0, 0, 0,255});

    drawCandybar();

    drawMinimap();
    drawCapacities();
    drawBuildingLists();
}

void cSideBarDrawer::drawHdSidebar()
{
    const HudLayout layout = HudLayout::create(
        true,
        game.m_screenW,
        game.m_screenH
    );
    renderDrawer->renderRectFillColor(
        layout.sidebar.getX(),
        layout.sidebar.getY(),
        layout.sidebar.getWidth(),
        layout.sidebar.getHeight(),
        Color{12, 15, 17, 255}
    );
    renderDrawer->renderRectFillColor(
        layout.sidebar.getX(),
        cSideBar::TopBarHeight,
        5,
        game.m_screenH - cSideBar::TopBarHeight,
        Color{32, 36, 38, 255}
    );
    renderDrawer->renderLine(
        layout.sidebar.getX() + 5,
        cSideBar::TopBarHeight,
        layout.sidebar.getX() + 5,
        game.m_screenH,
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
    return nullptr;
}

std::string cSideBarDrawer::getHouseDisplayName() const
{
    if (m_player->isHouse(ATREIDES)) {
        return localization::text("HOUSE ATREIDES", "ДОМ АТРЕЙДЕС");
    }
    if (m_player->isHouse(HARKONNEN)) {
        return localization::text("HOUSE HARKONNEN", "ДОМ ХАРКОННЕН");
    }
    if (m_player->isHouse(ORDOS)) {
        return localization::text("HOUSE ORDOS", "ДОМ ОРДОС");
    }
    return localization::text("UNKNOWN HOUSE", "НЕИЗВЕСТНЫЙ ДОМ");
}

void cSideBarDrawer::drawHdRadarPanel()
{
    const HudLayout layout = HudLayout::create(
        true,
        game.m_screenW,
        game.m_screenH
    );
    const Color panel{16, 20, 22, 255};
    const Color panelInner{7, 10, 11, 255};
    const Color brass{151, 113, 43, 255};
    const Color text{235, 225, 191, 255};
    const Color accent = m_player->getSelectFadingColor();

    renderDrawer->renderRectFillColor(
        layout.radarPanel.getX(),
        layout.radarPanel.getY(),
        layout.radarPanel.getWidth(),
        layout.radarPanel.getHeight(),
        panel
    );
    renderDrawer->renderRectColor(
        layout.radarPanel.getX(),
        layout.radarPanel.getY(),
        layout.radarPanel.getWidth(),
        layout.radarPanel.getHeight(),
        brass
    );
    renderDrawer->renderRectFillColor(
        layout.houseHeader.getX(),
        layout.houseHeader.getY(),
        layout.houseHeader.getWidth(),
        layout.houseHeader.getHeight(),
        Color{25, 29, 30, 255}
    );
    renderDrawer->renderRectFillColor(
        layout.houseHeader.getX(),
        layout.houseHeader.getEndY() - 2,
        layout.houseHeader.getWidth(),
        2,
        accent
    );

    Texture *crest = getHouseCrest();
    const int headerCrestSize = 24;
    if (crest != nullptr) {
        renderDrawer->renderStrechFullSprite(
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

    renderDrawer->renderRectFillColor(
        layout.radarViewport.getX(),
        layout.radarViewport.getY(),
        layout.radarViewport.getWidth(),
        layout.radarViewport.getHeight(),
        panelInner
    );
    renderDrawer->renderRectColor(
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
        renderDrawer->renderStrechFullSprite(
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

    renderDrawer->renderRectFillColor(
        rect.getX(),
        rect.getY(),
        rect.getWidth(),
        rect.getHeight(),
        Color{10, 13, 15, 255}
    );
    renderDrawer->renderRectColor(
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
    renderDrawer->renderRectFillColor(
        barX,
        barY,
        barWidth,
        4,
        Color{31, 35, 36, 255}
    );
    renderDrawer->renderRectFillColor(
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
        true,
        game.m_screenW,
        game.m_screenH
    );
    const int produced = std::max(0, m_player->getPowerProduced());
    const int used = std::max(0, m_player->getPowerUsage());
    drawHdMeter(
        layout.powerMeter,
        layout.powerMeter.getWidth() < 140 ? localization::text("PWR", "ЭНЕРГ.") : localization::text("POWER", "ЭНЕРГИЯ"),
        used,
        produced,
        Color{72, 202, 103, 255},
        !m_player->bEnoughPower()
    );

    drawHdMeter(
        layout.spiceMeter,
        layout.spiceMeter.getWidth() < 140 ? localization::text("SPC", "ПРЯН.") : localization::text("SPICE", "ПРЯНОСТЬ"),
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
        true,
        game.m_screenW,
        game.m_screenH,
        selectedList != nullptr &&
            selectedList->getType() == eListType::LIST_STARPORT
    );

    renderDrawer->renderRectFillColor(
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

    renderDrawer->renderRectFillColor(
        layout.catalog.getX(),
        layout.catalog.getY(),
        layout.catalog.getWidth(),
        layout.catalog.getHeight(),
        Color{12, 15, 17, 255}
    );
    renderDrawer->renderRectColor(
        layout.catalog.getX(),
        layout.catalog.getY(),
        layout.catalog.getWidth(),
        layout.catalog.getHeight(),
        Color{93, 75, 40, 255}
    );

    if (selectedList != nullptr) {
        m_buildingListDrawer.drawList(selectedList, selectedListId);
    }

    auto mouse = game.getMouse();
    for (int listId = startPos; listId < cSideBar::LIST_MAX; ++listId) {
        if (listId == selectedListId) {
            continue;
        }
        cBuildingList *list = m_sidebar->getList(listId);
        if (list->isAvailable() &&
            list->isOverButton(mouse->getX(), mouse->getY())) {
            m_buildingListDrawer.drawButtonHoverRectangle(list);
        }
    }

    if (selectedList != nullptr &&
        selectedList->getType() == eListType::LIST_STARPORT) {
        drawManager->getOrderDrawer()->drawOrderButton(m_player);
    }
}

void cSideBarDrawer::setPlayer(cPlayer *pPlayer)
{
    m_player = pPlayer;
    m_buildingListDrawer.setPlayer(pPlayer);
}

void cSideBarDrawer::drawBuildingLists()
{
    // draw the sidebar itself (the backgrounds, borders, etc)

    // !??! sidebar is not set earlier...but can be re-set, so keep doing this :(
    // This basically means the allocation goes wrong somewhere! :(
    m_sidebar = m_player->getSideBar();

    // draw the buildlist icons
    int selectedListId = m_sidebar->getSelectedListID();

    int startPos = eListTypeAsInt(eListType::LIST_CONSTYARD);
    for (int listId = startPos; listId < cSideBar::LIST_MAX; listId++) {
        cBuildingList *list = m_sidebar->getList(listId);
        bool isListIdSelectedList = (selectedListId == listId);
        m_buildingListDrawer.drawButton(list, isListIdSelectedList);
    }

    // draw background of buildlist
    Texture *backgroundSprite = m_gfxinter->getTexture(BMP_GERALD_ICONLIST_BACKGROUND);

    int drawX = game.m_screenW - cSideBar::SidebarWidthWithoutCandyBar + 1;

    int startY = cSideBar::TopBarHeight + cSideBar::HeightOfMinimap + cSideBar::HorizontalCandyBarHeight +
                 cSideBar::HeightOfListButton;

    for (; drawX < game.m_screenW; drawX += backgroundSprite->w) {
        for (int drawY=startY; drawY < game.m_screenH; drawY += backgroundSprite->h) {
            renderDrawer->renderSprite(backgroundSprite, drawX, drawY);
        }
    }

    // draw the 'lines' between the icons    // draw the buildlist itself (take scrolling into account)
    cBuildingList *selectedList = nullptr;

    int iDrawX = m_buildingListDrawer.getDrawX();
    int iDrawY = m_buildingListDrawer.getDrawY();

    Texture *horBar = m_gfxinter->getTexture(BMP_GERALD_SIDEBAR_PIECE);
    if (game.isHdGraphicsActive()) {
        const int separatorWidth =
            game.m_screenW - (iDrawX - 1);
        renderDrawer->renderStrechFullSprite(
            horBar,
            cRectangle(iDrawX - 1, iDrawY - 38, separatorWidth, horBar->h)
        );
        renderDrawer->renderStrechFullSprite(
            horBar,
            cRectangle(iDrawX - 1, iDrawY - 5, separatorWidth, horBar->h)
        );
    }
    else {
        renderDrawer->renderSprite(horBar, iDrawX-1, iDrawY-38);
        renderDrawer->renderSprite(horBar, iDrawX-1, iDrawY-5);
    }

    if (selectedListId > -1) {
        selectedList = m_sidebar->getList(selectedListId);
    }

    int endY = game.m_screenH;
    int rows = 6;
    if (selectedList && selectedList->getType() == eListType::LIST_STARPORT) {
        rows = 5;
        endY = game.m_screenH - 50;
    }

    if (!game.isHdGraphicsActive()) {
        for (int i = 1; i < 3; i++) {
            int barX = (iDrawX - 1) + (i * 66);
            Color darker = Color{89, 56, 0,255};
            Color veryDark = Color{48, 28, 0,255};
            renderDrawer->renderLine( barX - 1, iDrawY, barX - 1, endY, darker);
            renderDrawer->renderLine( barX, iDrawY, barX, endY, veryDark);

            for (int j = 1; j < rows; j++) {
                int barY = iDrawY - 1 + (j * 50);
                renderDrawer->renderLine( iDrawX, barY-1, game.m_screenW, barY - 1, darker);
                renderDrawer->renderLine( iDrawX, barY, game.m_screenW, barY, veryDark);
            }
        }
    }

    if (selectedList && selectedList->getType() == eListType::LIST_STARPORT) {
        renderDrawer->renderRectFillColor(iDrawX, endY, game.m_screenW-iDrawX, game.m_screenH-endY, m_sidebarColor);
        if (game.isHdGraphicsActive()) {
            renderDrawer->renderStrechFullSprite(
                horBar,
                cRectangle(
                    iDrawX - 1,
                    endY,
                    game.m_screenW - (iDrawX - 1),
                    horBar->h
                )
            );
        }
        else {
            renderDrawer->renderSprite(horBar, iDrawX-1, endY);
        }
    }

    // vertical lines at the side
    renderDrawer->renderLine( iDrawX - 1, iDrawY-38, iDrawX-1, game.m_screenH, Color{255, 211, 125,255}); // left
    renderDrawer->renderLine( game.m_screenW - 1, iDrawY - 38, game.m_screenW - 1, endY, Color{209, 150, 28,255}); // right

    // END drawing icons grid

    if (selectedList) {
        m_buildingListDrawer.drawList(selectedList, selectedListId);
    }

    // button interaction
    for (int i = startPos; i < cSideBar::LIST_MAX; i++) {
        if (i == selectedListId) continue; // skip selected list for button interaction
        cBuildingList *list = m_sidebar->getList(i);

        if (list->isAvailable() == false) continue; // not available, so no interaction possible

        // render hover over border
        auto m_mouse = game.getMouse();
        if (list->isOverButton(m_mouse->getX(), m_mouse->getX())) {
            m_buildingListDrawer.drawButtonHoverRectangle(list);
        }
    }

    cOrderDrawer *orderDrawer = drawManager->getOrderDrawer();

    // allow clicking on the order button
    if (selectedList && selectedList->getType() == eListType::LIST_STARPORT) {
        orderDrawer->drawOrderButton(m_player);
    }
}

void cSideBarDrawer::drawCapacities()
{
    drawPowerUsage();
    drawCreditsUsage();
}

void cSideBarDrawer::drawCandybar()
{
    renderDrawer->renderSprite(candiBarRenderer,game.m_screenW - cSideBar::SidebarWidth,40);
}

void cSideBarDrawer::drawMinimap()
{
    Texture *sprite = candyHorizonBar;
    int drawX = (game.m_screenW - sprite->w) + 1;
    // 128 pixels (each pixel is a cell) + 8 margin
    int heightMinimap = cSideBar::HeightOfMinimap;
    int drawY = cSideBar::TopBarHeight + heightMinimap;
    renderDrawer->renderSprite(sprite, drawX, drawY);

    // 11, 10
    // 78, 60
    // ------
    // 67, 50 (width/height)

    bool hasRadarAndEnoughPower = m_player->hasRadarAndEnoughPower();

    if (hasRadarAndEnoughPower) {
        return; // bail, because we render the minimap
    }

    // else, we render the house emblem
    renderDrawer->renderRectFillColor(drawX + 1, cSideBar::TopBarHeight + 1,game.m_screenW-(drawX + 1), drawY-(cSideBar::TopBarHeight + 1),
                                      m_player->getEmblemBackgroundColor());

    if (m_player->isHouse(ATREIDES) || m_player->isHouse(HARKONNEN) || m_player->isHouse(ORDOS)) {
        int bitmapId = BMP_SELECT_HOUSE_ATREIDES;

        int srcX = 11;
        int srcY = 10;

        // draw house emblem, which is the same as the 'select house x' picture, but partially
        int emblemWidth = 68;
        int emblemHeight = 50;

        if (m_player->isHouse(HARKONNEN)) {
            bitmapId = BMP_SELECT_HOUSE_HARKONNEN;
        }

        if (m_player->isHouse(ORDOS)) {
            bitmapId = BMP_SELECT_HOUSE_ORDOS;
            emblemHeight = 49;
            srcY = 11;
        }

        int emblemDesiredWidth = (emblemWidth * 2);
        int emblemDesiredHeight = (emblemHeight * 2);

        drawX += (sprite->w / 2) - (emblemDesiredWidth / 2);
        drawY = cSideBar::TopBarHeight + ((heightMinimap / 2) - (emblemDesiredHeight / 2));

        cRectangle src = {srcX, srcY, emblemWidth,emblemHeight};
        cRectangle dest = {drawX, drawY, emblemDesiredWidth, emblemDesiredHeight};
        renderDrawer->renderStrechSprite(m_gfxinter->getTexture(bitmapId), src, dest);
    }
}

void cSideBarDrawer::createCandyBar()
{
    int heightInPixels = (game.m_screenH - cSideBar::TopBarHeight);
    // ball first
    renderDrawer->renderSprite(candyBarBall, 0,0); // height of ball = 25
    renderDrawer->renderSprite(m_gfxinter->getTexture(BMP_GERALD_CANDYBAR_TOP), 0, 26); // height of top = 10
    // now draw pieces untill the end (height of piece is 23 pixels)
    int startY = 26 + 10; // end of ball (26) + height of top m_candybar (=10) , makes 36
    int heightMinimap = cSideBar::HeightOfMinimap;
    // auto tmp = cRectangle{0,0,24, heightMinimap - (6 + 1)};  // (add 1 pixel for room between ball and bar)
    for (int y = startY; y < (heightMinimap); y += 24) {
        renderDrawer->renderSprite(candyBarPiece, 0, y);
    }
    // note: no need to take top bar into account because 'm_candybar' is a separate bitmap so coords start at 0,0
    // ball is 6 pixels higher than horizontal m_candybar
    int ballY = (heightMinimap) - 6;

    // draw bottom m_candybar
    renderDrawer->renderSprite(m_gfxinter->getTexture(BMP_GERALD_CANDYBAR_BOTTOM), 0, ballY - 10); // height of bottom = 9

    // draw ball
    renderDrawer->renderSprite(candyBarBall, 0, ballY); // height of ball = 25

    // draw top m_candybar again
    renderDrawer->renderSprite(m_gfxinter->getTexture(BMP_GERALD_CANDYBAR_TOP), 0, ballY + 26); // height of top = 10

    startY = ballY + 26 + 10;
    for (int y = startY; y < (heightInPixels + 23); y += 24) {
        renderDrawer->renderSprite(candyBarPiece, 0, y);
    }
    // draw bottom
    renderDrawer->renderSprite(m_gfxinter->getTexture(BMP_GERALD_CANDYBAR_BOTTOM), 0, heightInPixels - 10); // height of top = 10
}

void cSideBarDrawer::drawPowerUsage() const
{
    int arbitraryMargin = 6;
    int barTotalHeight = game.m_screenH - (cSideBar::TotalHeightBeforePowerBarStarts + cSideBar::PowerBarMarginHeight);
    int barX = (game.m_screenW - cSideBar::SidebarWidth) + (cSideBar::VerticalCandyBarWidth / 3);
    int barY = cSideBar::TotalHeightBeforePowerBarStarts + arbitraryMargin;
    int barWidth = (cSideBar::VerticalCandyBarWidth / 3) - 1;
    //cRectangle powerBarRect(barX, barY, barWidth, barTotalHeight);
    renderDrawer->renderRectFillColor(barX, barY, barWidth, barTotalHeight, Color::black()); //renderDrawer->getColor_BLACK());

    // the maximum power (ie a full bar) is 1 + amount windtraps * power_give (100)
    int maxPowerOutageOfWindtrap = sStructureInfo[WINDTRAP].power_give;
    float totalPowerOutput = (1 + (m_player->getAmountOfStructuresForType(WINDTRAP))) * maxPowerOutageOfWindtrap;
    float powerIn = (float)m_player->getPowerProduced() / totalPowerOutput;
    float powerUse = (float)m_player->getPowerUsage() / totalPowerOutput;

    float barHeightToDraw = barTotalHeight * powerIn;
    if (barHeightToDraw > barTotalHeight) barHeightToDraw = barTotalHeight;
    int powerInY = barY + (barTotalHeight - barHeightToDraw);

    renderDrawer->renderRectFillColor(barX, powerInY, barWidth, barY+barTotalHeight-powerInY, Color{0, 232, 0,255});

    barHeightToDraw = barTotalHeight * powerUse;
    if (barHeightToDraw > barTotalHeight) barHeightToDraw = barTotalHeight;
    int powerOutY = barY + (barTotalHeight - barHeightToDraw);

    float powerUsageRatio = ((float)m_player->getPowerUsage() + 1) / ((float)m_player->getPowerProduced() + 1);
    int r = powerUsageRatio * 255;
    int g = (1.1 - powerUsageRatio) * 255;

    if (r > 255) r = 255;
    if (g > 255) g = 255;

    if (m_player->bEnoughPower()) {
        renderDrawer->renderRectFillColor(barX, powerOutY, barWidth, barY + barTotalHeight-powerOutY, Color{(Uint8)r, (Uint8)g, 32,255});
    }
    else {
        renderDrawer->renderRectFillColor(barX, powerOutY, barWidth, barY + barTotalHeight-powerOutY, m_player->getErrorFadingColor());
    }

    renderDrawer->renderLine(barX, powerOutY, barX+barWidth, powerOutY, Color{255, 255, 255,255});

    renderDrawer->renderRectColor(barX, barY, barWidth, barTotalHeight, m_sidebarColor);

    // draw darker 'sides' at the left and top
    Color darker = Color{89, 56, 0,255};
    renderDrawer->renderLine(barX, barY, barX, barY + barTotalHeight, darker); // left side |
    renderDrawer->renderLine(barX, barY, barX+barWidth, barY, darker); // top side _
    if (m_player->bEnoughPower()) {
        renderDrawer->renderSprite(m_gfxinter->getTexture(ICON_POWER_HIGH),barX-3, barY - 21);
    }
    else {
        renderDrawer->renderSprite(m_gfxinter->getTexture(ICON_POWER),barX-3, barY - 21);
    }
}

void cSideBarDrawer::drawCreditsUsage()
{
    int barTotalHeight = (cSideBar::HeightOfMinimap - 76);
    int barX = (game.m_screenW - cSideBar::SidebarWidth) + (cSideBar::VerticalCandyBarWidth / 3);
    int barY = cSideBar::TopBarHeight + 48;
    int barWidth = (cSideBar::VerticalCandyBarWidth / 3) - 1;
    // cRectangle powerBarRect(barX, barY, barWidth, barTotalHeight);
    renderDrawer->renderRectFillColor(barX, barY, barWidth, barTotalHeight, 0,0,0,255);

    // STEFAN: 01/05/2021 -> looks like a lot of this code can be moved to the player class to retrieve max spice capacity
    // and so forth.

    // the maximum power (ie a full bar) is 1 + amount windtraps * power_give (100)
    int maxSpiceCapacity = 1000; // this is still hard coded, need to move to INI file
    int structuresWithSpice = m_player->getAmountOfStructuresForType(REFINERY) + m_player->getAmountOfStructuresForType(SILO);
    float totalSpiceCapacity = (1 + structuresWithSpice) * maxSpiceCapacity;
    float maxSpice = m_player->getMaxCredits() / totalSpiceCapacity;
    float spiceStored = static_cast<float>(m_player->getCredits()) / totalSpiceCapacity;

    float barHeightToDraw = barTotalHeight * maxSpice;
    if (barHeightToDraw > barTotalHeight) barHeightToDraw = barTotalHeight;
    int powerInY = barY + (barTotalHeight - barHeightToDraw);

    renderDrawer->renderRectFillColor(barX, powerInY, barWidth, barY + barTotalHeight - powerInY, Color{0, 232, 0,255});

    barHeightToDraw = barTotalHeight * spiceStored;
    if (barHeightToDraw > barTotalHeight) barHeightToDraw = barTotalHeight;
    int powerOutY = barY + (barTotalHeight - barHeightToDraw);

    auto spiceCapacityRatio = static_cast<float>(m_player->getCredits() + 1) / (m_player->getMaxCredits() + 1);
    spiceCapacityRatio = std::clamp(spiceCapacityRatio, 0.0f, 1.0f);
    int r = spiceCapacityRatio * 255;
    int g = (1.1 - spiceCapacityRatio) * 255;

    if (r > 255) r = 255;
    if (g > 255) g = 255;

    if (m_player->bEnoughSpiceCapacityToStoreCredits()) {
        renderDrawer->renderRectFillColor(barX, powerOutY, barWidth, barY + barTotalHeight - powerOutY, (Uint8)r,(Uint8)g, 32,255);
    }
    else {
        renderDrawer->renderRectFillColor(barX, powerOutY, barWidth, barY + barTotalHeight - powerOutY, m_player->getErrorFadingColor());
    }

    renderDrawer->renderLine( barX, powerOutY, barX+barWidth, powerOutY, Color{255, 255, 255,255});

    // draw darker 'sides' at the left and top
    Color darker = Color{89, 56, 0,255};
    renderDrawer->renderLine( barX, barY, barX, barY + barTotalHeight, darker); // left side |
    renderDrawer->renderLine( barX, barY, barX+barWidth, barY, darker); // top side _

    if (spiceCapacityRatio>0.95) {
        renderDrawer->renderSprite(m_gfxinter->getTexture(ICON_SOLARIS_FULL), barX-5, barY-20);
    } else  if (spiceCapacityRatio<0.05) {
        renderDrawer->renderSprite(m_gfxinter->getTexture(ICON_SOLARIS_LOW), barX-5, barY-20);
    } else {
        renderDrawer->renderSprite(m_gfxinter->getTexture(ICON_SOLARIS), barX-5, barY-20);
    }
}
