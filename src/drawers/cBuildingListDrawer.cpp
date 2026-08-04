#include "cBuildingListDrawer.h"

#include "drawers/SDLDrawer.hpp"
#include "d2tmc.h"
#include "data/gfxinter.h"
#include "player/cPlayer.h"
#include "utils/Graphics.hpp"
#include "utils/Localization.hpp"
#include "utils/common.h"
#include "context/GameContext.hpp"
#include "context/GraphicsContext.hpp"

#include <SDL2/SDL.h>
#include <algorithm>
#include <format>
#include <sstream>
#include <vector>

namespace {
void removeLastUtf8CodePoint(std::string &text)
{
    if (text.empty()) {
        return;
    }
    std::size_t position = text.size() - 1;
    while (position > 0 &&
           (static_cast<unsigned char>(text[position]) & 0xC0U) == 0x80U) {
        --position;
    }
    text.erase(position);
}

std::string fitWithEllipsis(
    const cTextDrawer *drawer,
    std::string text,
    int maximumWidth)
{
    if (drawer->getTextLength(text) <= maximumWidth) {
        return text;
    }
    constexpr const char *ellipsis = "…";
    while (!text.empty() &&
           drawer->getTextLength(text + ellipsis) > maximumWidth) {
        removeLastUtf8CodePoint(text);
    }
    return text + ellipsis;
}

std::string compactCardName(const std::string &name)
{
    // Keep canonical names in status messages and save-independent game data,
    // but use familiar short forms in the narrow construction cards.
    if (name == localization::text("Hi-Tech", "Высокотехнологичный завод")) return localization::text("Hi-Tech", "Высокотех. завод");
    if (name == localization::text("Spice Refinery", "Перерабатывающий завод")) return localization::text("Refinery", "Переработчик");
    if (name == localization::text("MCV", "Мобильный стройкомплекс")) return localization::text("MCV", "Стройкомплекс");
    if (name == localization::text("Light Infantry", "Отряд автоматчиков")) return localization::text("Infantry", "Автоматчики");
    if (name == localization::text("Troopers", "Отряд гранатомётчиков")) return localization::text("Troopers", "Гранатомётчики");
    return name;
}
}

cBuildingListDrawer::cBuildingListDrawer(const GameContext *ctx, cPlayer *player) :
    m_gameTextDrawer(ctx->getTextContext()->getGameTextDrawer()),
    m_smallTextDrawer(ctx->getTextContext()->getSmallTextDrawer()),
    m_gfxinter(ctx->getGraphicsContext()->gfxinter.get()),
    m_player(player),
    m_renderListIds(false),
    m_readyLabel(localization::text("READY", "ГОТОВО"))
{
}

void cBuildingListDrawer::drawList(cBuildingList *list, int listIDToDraw)
{
    if (listIDToDraw == eListTypeAsInt(eListType::LIST_CONSTYARD)) {
        drawListWithStructures(list);
    }
    else {
        drawListWithUnitsOrAbilities(list);
    }
}

void cBuildingListDrawer::drawListWithStructures(cBuildingList *list)
{
    drawList(list, true);
}

void cBuildingListDrawer::drawListWithUnitsOrAbilities(cBuildingList *list)
{
    drawList(list, false);
}

void cBuildingListDrawer::drawButtonHoverRectangle(cBuildingList *list)
{
    assert(list != nullptr);

    int x = list->getButtonDrawX();
    int y = list->getButtonDrawY();
    int id = list->getButtonIconIdUnpressed();

    int width = game.isHdGraphicsActive() ? list->getButtonWidth() : 33;
    int height = game.isHdGraphicsActive()
        ? list->getButtonHeight()
        : m_gfxinter->getLogicalHeight(id);

    Color color = m_player->getSelectFadingColor();

    renderDrawer->renderRectColor(x, y, width, height, color);
    renderDrawer->renderRectColor(x + 1, y + 1, width-2, height-2, color);
}

void cBuildingListDrawer::drawButton(cBuildingList *list, bool pressed)
{
    assert(list != nullptr);

    int x = list->getButtonDrawX();
    int y = list->getButtonDrawY();
    int id = list->getButtonIconIdUnpressed();

    if (pressed) {
        id = list->getButtonIconIdPressed();
    }

    if (id < 0) {
        // this is not good
        logbook("ERROR UNABLE TO DRAW LIST BECAUSE ID IS NOT VALID!?");
        return;
    }

//	int width = (gfxinter->getSurface(id))->w;
    int width = game.isHdGraphicsActive() ? list->getButtonWidth() : 33;
    int height = game.isHdGraphicsActive()
        ? list->getButtonHeight()
        : m_gfxinter->getLogicalHeight(id);

    if (game.isHdGraphicsActive()) {
        const Color panel{18, 22, 25, 255};
        const Color border{93, 78, 49, 255};
        const Color active{217, 164, 54, 255};
        renderDrawer->renderRectFillColor(x, y, width, height, panel);

        Texture *icon = m_gfxinter->getTexture(id);
        const int availableWidth = std::max(1, width - 8);
        const int availableHeight = std::max(1, height - 6);
        const float scale = std::min(
            static_cast<float>(availableWidth) / icon->w,
            static_cast<float>(availableHeight) / icon->h
        );
        const int iconWidth = std::max(1, static_cast<int>(icon->w * scale));
        const int iconHeight = std::max(1, static_cast<int>(icon->h * scale));
        const cRectangle iconRect(
            x + (width - iconWidth) / 2,
            y + (height - iconHeight) / 2,
            iconWidth,
            iconHeight
        );
        renderDrawer->renderStrechFullSprite(
            icon,
            iconRect,
            list->isAvailable() ? 255 : 96
        );
        if (!list->isAvailable()) {
            renderDrawer->renderRectFillColor(
                iconRect,
                Color{20, 22, 23, 255},
                138
            );
        }
        renderDrawer->renderRectColor(
            x,
            y,
            width,
            height,
            pressed ? active : border
        );
        if (pressed) {
            renderDrawer->renderRectFillColor(
                x + 2,
                y + height - 3,
                width - 4,
                2,
                active
            );
            list->stopFlashing();
        }
        else if (list->isFlashing()) {
            renderDrawer->renderRectColor(
                x + 1,
                y + 1,
                width - 2,
                height - 2,
                list->getFlashingColor()
            );
        }
        return;
    }

    // clear
    renderDrawer->renderSprite(m_gfxinter->getTexture(list->getButtonIconIdUnpressed()), x, y);		// draw pressed button version (unpressed == default in gui)

    // set blender
    renderDrawer->renderSprite(m_gfxinter->getTexture(id), x, y,128);

    if (!list->isAvailable()) {
        renderDrawer->renderRectFillColor(x, y, width, height, 0,0,0,96);
    }

    if (pressed) {
        list->stopFlashing();

        Color color = m_player->getHouseFadingColor();

        renderDrawer->renderRectColor(x, y, width, height, color);
        renderDrawer->renderRectColor(x + 1, y + 1, width - 2, height - 2, color);
    }
    else {
        if (list->isFlashing()) {
            Color color = list->getFlashingColor();

            renderDrawer->renderRectColor(x, y, width, height, color);
            renderDrawer->renderRectColor(x + 1, y + 1, width - 2, height - 2, color);
            renderDrawer->renderRectColor(x + 2, y + 2, width - 3, height - 3, color);
        }
    }
}


int cBuildingListDrawer::getDrawX()
{
    if (game.isHdGraphicsActive()) {
        return getLayout().cards.getX();
    }
    return (game.m_screenW - cSideBar::SidebarWidthWithoutCandyBar) + 2;
}

int cBuildingListDrawer::getDrawY()
{
    if (game.isHdGraphicsActive()) {
        return getLayout().cards.getY();
    }
    return cSideBar::TopBarHeight + 230 + 30;
}

/**
 * Draw the list, start from startId, until the max icons in the list to be drawn.
 *
 * @param startId
 */
void cBuildingListDrawer::drawList(cBuildingList *list, bool shouldDrawStructureSize)
{
    const bool hdMode = game.isHdGraphicsActive();
    const HudLayout layout = getLayout(list);
    const int scrollRow = getScrollRow(list);

    // starting draw coordinates
    int iDrawX=getDrawX();
    int iDrawY=getDrawY();

    Color selectFadingColor = m_player->getSelectFadingColor();

    int end = MAX_ITEMS;

    // is building an item in the list?
    std::array<int, 6> isBuildingItemInList = list->isBuildingItem();

    // Start drawing the 'icons grid'
    int withOfIcon = getCardWidth();
    int heightOfIcon = getCardHeight();
    const int columns = getColumnCount();
    const int cardGap = getCardGap();

    if (hdMode) {
        renderDrawer->setClippingFor(
            layout.cards.getX(),
            layout.cards.getY(),
            layout.cards.getEndX(),
            layout.cards.getEndY()
        );
    }

    // Draw the visible icon rows. HD positions come from HudLayout so drawing
    // and hit testing cannot drift apart.
    int rowNr = 0;
    for (int i = 0; i < end; i++) {
        cBuildingListItem *item = list->getItem(i);

        if (item == nullptr) {
            continue; // allow gaps in the list data structure (just not with rendering)
        }

        if (hdMode) {
            const cRectangle card = layout.cardRect(i, scrollRow);
            if (card.getEndY() <= layout.cards.getY() ||
                card.getY() >= layout.cards.getEndY()) {
                continue;
            }
            iDrawX = card.getX();
            iDrawY = card.getY();
        }

        int iDrawXEnd = iDrawX + withOfIcon;
        int iDrawYEnd = iDrawY + heightOfIcon;

        // asumes drawing for human player
        bool cannotPayIt = !m_player->hasEnoughCreditsFor(item->getBuildCost());

        // icon id must be set , assert it.
        assert(item->getIconId() > -1);

        if (hdMode) {
            drawHdCard(item, iDrawX, iDrawY);
        }
        else {
            renderDrawer->renderSprite(
                m_gfxinter->getTexture(item->getIconId()),
                iDrawX,
                iDrawY
            );
        }

        if (shouldDrawStructureSize) {
            drawStructureSize(item->getBuildId(), iDrawX, iDrawY);
        }

        // when this item is being built.
        if (item->isBuilding()) {
            int iFrame = item->getBuildProgressFrame();

            if (hdMode && (!item->isDoneBuilding() || iFrame < 31)) {
                const int progressWidth = std::clamp(
                    (withOfIcon - 4) * iFrame / 31,
                    0,
                    withOfIcon - 4
                );
                const int progressY = iDrawY + heightOfIcon - 36;
                renderDrawer->renderRectFillColor(
                    iDrawX + 2,
                    progressY,
                    withOfIcon - 4,
                    4,
                    15,
                    18,
                    20,
                    230
                );
                renderDrawer->renderRectFillColor(
                    iDrawX + 2,
                    progressY,
                    progressWidth,
                    4,
                    selectFadingColor
                );
            }
            else if (!item->isDoneBuilding() || iFrame < 31) {
                // draw the other progress stuff
                renderDrawer->renderSprite(m_gfxinter->getTexture(PROGRESSFIX), iDrawX+2, iDrawY+2,128);
                renderDrawer->renderSprite(m_gfxinter->getTexture(PROGRESS001+iFrame), iDrawX+2, iDrawY+2,128);
            }
            else {
                if (item->shouldPlaceIt()) {
                    const Color readyColor = m_player->isContextMouseState(
                        eMouseState::MOUSESTATE_PLACE
                    ) ? Color{225, 48, 42, 255} : Color::white();
                    m_smallTextDrawer->drawTextScaledCenteredInBox(
                        m_readyLabel,
                        cRectangle(iDrawX + 2, iDrawY + 2, withOfIcon - 4, heightOfIcon - 32),
                        hdMode ? 1.0F : 0.85F,
                        readyColor
                    );
                }
                else if (item->shouldDeployIt()) {
                    const Color readyColor = m_player->isContextMouseState(
                        eMouseState::MOUSESTATE_DEPLOY
                    ) ? Color{225, 48, 42, 255} : Color::white();
                    m_smallTextDrawer->drawTextScaledCenteredInBox(
                        m_readyLabel,
                        cRectangle(iDrawX + 2, iDrawY + 2, withOfIcon - 4, heightOfIcon - 32),
                        hdMode ? 1.0F : 0.85F,
                        readyColor
                    );
                }
            }
        }
        else {   // not building
            // this item is not being built. So we do not draw a progress indicator.
            // however, it could be that an other item is being built.

            // draw the item 'unavailable' when:
            // - is not available (doh)
            // - we cant pay it
            // - some other item is being built
            // - list is being upgraded, so you cannot build items
            bool isBuildingSameSubListItem = false;
            for (int i2 = 0; i2 < 5; i2++) {
                if (isBuildingItemInList[i2] < 0) continue;
                if (i2 == item->getSubList()) {
                    isBuildingSameSubListItem = true;
                    break;
                }
            }

            if (!item->isAvailable() || isBuildingSameSubListItem) {
                if (hdMode) {
                    renderDrawer->renderRectFillColor(
                        iDrawX,
                        iDrawY,
                        withOfIcon,
                        heightOfIcon - 32,
                        0,
                        0,
                        0,
                        128
                    );
                }
                else {
                    renderDrawer->renderSprite(
                        m_gfxinter->getTexture(PROGRESSNA),
                        iDrawX,
                        iDrawY,
                        64
                    );
                }

                // Pending upgrading (ie: an upgrade is progressing, blocking the construction of these items)
                if (item->isPendingUpgrading()) {
                    Color errorFadingColor = m_player->getErrorFadingColor();
                    renderDrawer->renderRectColor(iDrawX, iDrawY, iDrawXEnd-iDrawX, iDrawYEnd-iDrawY, errorFadingColor);
                    renderDrawer->renderLine( iDrawX, iDrawY, iDrawXEnd, iDrawYEnd, errorFadingColor);
                    renderDrawer->renderLine( iDrawX, iDrawY + heightOfIcon, iDrawX + withOfIcon, iDrawY, errorFadingColor);

                    Color red = Color{255, 0, 0,255};
                    m_smallTextDrawer->drawTextCenteredInBox(localization::text("Upgrade", "Улучшение"), iDrawX, iDrawY, withOfIcon, heightOfIcon, red);
                }

                // Pending building (ie: a build is progressing, blocking the upgrade)
                if (item->isPendingBuilding()) {
                    Color errorFadingColor = m_player->getErrorFadingColor();
                    renderDrawer->renderRectColor(iDrawX, iDrawY, iDrawXEnd-iDrawX, iDrawYEnd-iDrawY, errorFadingColor);
                    renderDrawer->renderLine( iDrawX, iDrawY, iDrawXEnd, iDrawYEnd, errorFadingColor);
                    renderDrawer->renderLine( iDrawX, iDrawY + heightOfIcon, iDrawX + withOfIcon, iDrawY, errorFadingColor);

                    Color red = Color{255, 0, 0, 255};
                    m_smallTextDrawer->drawTextCenteredInBox(
                        localization::text("OCCUPIED", "ЗАНЯТО"),
                        iDrawX,
                        iDrawY,
                        withOfIcon,
                        heightOfIcon,
                        red
                    );
                }
            }

            if (list->getType() == eListType::LIST_STARPORT) {
                // only for starport show you can't pay it, as we allow building units when you cannot pay it (ie partial
                // payment/progress)
                if (cannotPayIt) {
                    if (hdMode) {
                        renderDrawer->renderRectFillColor(
                            iDrawX,
                            iDrawY,
                            withOfIcon,
                            heightOfIcon - 32,
                            0,
                            0,
                            0,
                            128
                        );
                    }
                    else {
                        renderDrawer->renderSprite(
                            m_gfxinter->getTexture(PROGRESSNA),
                            iDrawX,
                            iDrawY,
                            64
                        );
                    }
                    Color errorFadingColor = m_player->getErrorFadingColor();
                    renderDrawer->renderRectColor(iDrawX, iDrawY, iDrawXEnd-iDrawX, iDrawYEnd-iDrawY, errorFadingColor);
                    renderDrawer->renderLine( iDrawX, iDrawY, iDrawXEnd, iDrawYEnd, errorFadingColor);
                    renderDrawer->renderLine( iDrawX, iDrawY + heightOfIcon, iDrawX + withOfIcon, iDrawY, errorFadingColor);
                }
            }

            // last built id
            if (list->getLastClickedId() == i) {
                renderDrawer->renderRectColor((iDrawX + 1), (iDrawY + 1), (iDrawXEnd - 1)-(iDrawX + 1), (iDrawYEnd - 1)-(iDrawY + 1), selectFadingColor);
                renderDrawer->renderRectColor(iDrawX, iDrawY, iDrawXEnd-iDrawX, iDrawYEnd-iDrawY, selectFadingColor);
            }
        }

        // if item is queuable, then it will show the amount of
        // items being built. Meaning, with 1 item to build, it will show a 1.
        int amountToShow = item->getTimesToBuild();
        bool showAmount = item->isQueuable() && amountToShow > 0;

        bool listIsStarport = item->getList()->getType() == eListType::LIST_STARPORT;
        if (listIsStarport) {
            amountToShow = item->getTimesOrdered();
            showAmount = true; // starport shows always all amounts
        }

        if (showAmount) {
            // draw number of times to build this thing (queueing)
            int textX = hdMode
                ? iDrawX + withOfIcon - 20
                : iDrawX + 41;
            int textY = hdMode
                ? iDrawY + heightOfIcon - 51
                : iDrawY + 16;

            if (amountToShow < 10) {
                textX += hdMode ? 6 : 10;
            }

            if (hdMode) {
                renderDrawer->renderRectFillColor(
                    textX - 3,
                    textY - 1,
                    withOfIcon - (textX - iDrawX) - 1,
                    16,
                    8,
                    10,
                    12,
                    220
                );
            }

            // draw
            m_gameTextDrawer->drawText(textX, textY, std::format("{}",amountToShow));
        }

        if (game.isDebugMode()) {
            if (m_renderListIds) {
                int textX = iDrawX + 41;
                int textY = iDrawY + 40;

                m_gameTextDrawer->drawText(textX, textY, std::format("{}",item->getSubList()));
            }
        }

        // draw rectangle when mouse hovers over icon
        auto m_mouse = game.getMouse();
        if (isOverItemCoordinates_Boolean(m_mouse->getX(), m_mouse->getY(), iDrawX, iDrawY)) {
            renderDrawer->renderRectColor((iDrawX + 1), (iDrawY + 1), (iDrawXEnd - 1)-(iDrawX + 1), (iDrawYEnd - 1)-(iDrawY + 1), selectFadingColor);
            renderDrawer->renderRectColor(iDrawX, iDrawY, iDrawXEnd-iDrawX, iDrawYEnd-iDrawY, selectFadingColor);
        }
        else {
            Color color = list->getFlashingColor();
            if (item->isFlashing()) {
                renderDrawer->renderRectColor((iDrawX + 1), (iDrawY + 1), (iDrawXEnd - 1)-(iDrawX + 1), (iDrawYEnd - 1)-(iDrawY + 1), color);
                renderDrawer->renderRectColor(iDrawX, iDrawY, iDrawXEnd-iDrawX, iDrawYEnd-iDrawY, color);
            }
        }

        // update coordinates
        if (!hdMode && rowNr < columns - 1) {
            iDrawX += withOfIcon + cardGap;
            rowNr++;
        }
        else if (!hdMode) {
            rowNr = 0;
            iDrawX=getDrawX();
            iDrawY += heightOfIcon + cardGap;
        }
    }

    if (hdMode) {
        renderDrawer->resetClippingFor();
        drawHdScrollbar(list, layout);
    }
}

/**
 * Draw the amount of squares a structure would take. The X and Y coordinates are the top
 * left coordinates of an icon.
 *
 * @param structureId
 * @param x
 * @param y
 */
void cBuildingListDrawer::drawStructureSize(int structureId, int x, int y)
{
    // figure out size
    int iW= sStructureInfo[structureId].bmp_width / 32;
    int iH= sStructureInfo[structureId].bmp_height / 32;
    int iTile = GRID_1X1;

    if (iW == 2 && iH == 2) {
        iTile = GRID_2X2;
    }

    if (iW == 3 && iH == 2) {
        iTile = GRID_3X2;
    }

    if (iW == 3 && iH == 3) {
        iTile = GRID_3X3;
    }

    const int gridX = game.isHdGraphicsActive()
        ? x + getCardWidth() - 22
        : x + 43;
    const int gridY = game.isHdGraphicsActive() ? y + 3 : y + 20;
    renderDrawer->renderRectFillColor(gridX, gridY,19,19,8,10,12,220);
    renderDrawer->renderSprite(m_gfxinter->getTexture(GRID_0X0), gridX, gridY);
    renderDrawer->renderSprite(m_gfxinter->getTexture(iTile), gridX, gridY);
}

bool cBuildingListDrawer::isOverItemCoordinates_Boolean(int x, int y, int drawX, int drawY)
{
    if (x >= drawX &&
        x <= drawX + getCardWidth() &&
        y >= drawY &&
        y < drawY + getCardHeight()) {
        return true;
    }
    return false;
}

cBuildingListItem *cBuildingListDrawer::isOverItemCoordinates(cBuildingList *list, int x, int y)
{
    assert(list != nullptr);

    if (game.isHdGraphicsActive()) {
        const HudLayout layout = getLayout(list);
        if (!layout.cards.isPointWithin(x, y)) {
            return nullptr;
        }
        const int scrollRow = getScrollRow(list);
        for (int i = 0; i < list->getItemCount(); ++i) {
            cBuildingListItem *item = list->getItem(i);
            if (item == nullptr) {
                continue;
            }
            const cRectangle card = layout.cardRect(i, scrollRow);
            if (card.getY() < layout.cards.getY() ||
                card.getEndY() > layout.cards.getEndY()) {
                continue;
            }
            if (card.isPointWithin(x, y)) {
                return item;
            }
        }
        return nullptr;
    }

    // starting draw coordinates
    int iDrawX=getDrawX();
    int iDrawY=getDrawY();

    int end = MAX_ITEMS;

    int rowNr = 0;
    for (int i = 0; i < end; i++) {
        cBuildingListItem *item = list->getItem(i);
        if (item == nullptr) break;

        if (isOverItemCoordinates_Boolean(x, y, iDrawX, iDrawY)) {
            return item;
        }

        if (rowNr < getColumnCount() - 1) {
            rowNr++;
            iDrawX += getCardWidth() + getCardGap();
        }
        else {
            iDrawY += getCardHeight() + getCardGap();
            iDrawX=getDrawX();
            rowNr = 0;
        }
    }

    return nullptr;
}

int cBuildingListDrawer::getColumnCount() const
{
    if (!game.isHdGraphicsActive()) {
        return 3;
    }
    return getLayout().columns;
}

int cBuildingListDrawer::getCardWidth() const
{
    if (!game.isHdGraphicsActive()) {
        return 63;
    }
    return getLayout().cardWidth;
}

int cBuildingListDrawer::getCardHeight() const
{
    return game.isHdGraphicsActive() ? getLayout().cardHeight : 47;
}

int cBuildingListDrawer::getCardGap() const
{
    return game.isHdGraphicsActive() ? getLayout().cardGap : 3;
}

void cBuildingListDrawer::drawHdCard(
    cBuildingListItem *item,
    int x,
    int y)
{
    const int cardWidth = getCardWidth();
    const int cardHeight = getCardHeight();
    const int labelHeight = 32;
    const int imageHeight = cardHeight - labelHeight;
    const Color panelColor{18, 22, 25, 255};
    const Color borderColor{142, 111, 51, 255};
    const Color innerBorder{56, 61, 62, 255};
    const Color labelColor{232, 225, 196, 255};
    const Color priceColor{255, 205, 73, 255};

    renderDrawer->renderRectFillColor(
        x,
        y,
        cardWidth,
        cardHeight,
        panelColor
    );

    Texture *icon = m_gfxinter->getTexture(item->getIconId());
    // Classic icons have a baked 10 px title strip. HD masters contain only
    // clean artwork; the localized title is rendered in the separate label
    // block below the image.
    const int sourceHeight = game.isHdGraphicsActive()
        ? icon->h
        : std::max(1, icon->h - 10);
    renderDrawer->renderStrechSprite(
        icon,
        cRectangle(0, 0, icon->w, sourceHeight),
        cRectangle(x + 3, y + 3, cardWidth - 6, imageHeight - 5)
    );

    renderDrawer->renderRectFillColor(
        x + 1,
        y + imageHeight,
        cardWidth - 2,
        labelHeight - 1,
        panelColor
    );
    renderDrawer->renderRectColor(
        x,
        y,
        cardWidth,
        cardHeight,
        borderColor
    );
    renderDrawer->renderRectColor(
        x + 1,
        y + 1,
        cardWidth - 2,
        cardHeight - 2,
        innerBorder
    );
    renderDrawer->renderLine(
        x + 2,
        y + imageHeight,
        x + cardWidth - 3,
        y + imageHeight,
        borderColor
    );

    const std::string name = compactCardName(item->getNameString());
    const int textWidth = cardWidth - 6;
    if (m_smallTextDrawer->getTextLength(name) <= textWidth) {
        m_smallTextDrawer->drawTextCenteredInBox(
            name,
            x + 3,
            y + imageHeight,
            textWidth,
            labelHeight,
            labelColor
        );
    }
    else {
        std::istringstream stream(name);
        std::vector<std::string> words;
        std::string word;
        while (stream >> word) {
            words.push_back(word);
        }

        std::string firstLine;
        std::string secondLine;
        for (const auto &candidateWord : words) {
            const std::string candidate = firstLine.empty()
                ? candidateWord
                : firstLine + " " + candidateWord;
            if (secondLine.empty() &&
                m_smallTextDrawer->getTextLength(candidate) <= textWidth) {
                firstLine = candidate;
            }
            else {
                secondLine += secondLine.empty()
                    ? candidateWord
                    : " " + candidateWord;
            }
        }

        firstLine = fitWithEllipsis(
            m_smallTextDrawer,
            firstLine.empty() ? name : firstLine,
            textWidth
        );
        secondLine = fitWithEllipsis(
            m_smallTextDrawer,
            secondLine,
            textWidth
        );

        if (secondLine.empty()) {
            m_smallTextDrawer->drawTextCenteredInBox(
                firstLine,
                x + 3,
                y + imageHeight,
                textWidth,
                labelHeight,
                labelColor
            );
        }
        else {
            m_smallTextDrawer->drawTextCentered(
                firstLine,
                x + 3,
                textWidth,
                y + imageHeight + 2,
                labelColor
            );
            m_smallTextDrawer->drawTextCentered(
                secondLine,
                x + 3,
                textWidth,
                y + imageHeight + 15,
                labelColor
            );
        }
    }

    if (item->getBuildCost() > 0) {
        const std::string price = std::format("${}", item->getBuildCost());
        const int priceWidth = m_smallTextDrawer->getTextLength(price);
        const int priceX = x + 6;
        renderDrawer->renderRectFillColor(
            priceX - 3,
            y + 3,
            priceWidth + 4,
            17,
            8,
            10,
            12,
            220
        );
        renderDrawer->renderRectColor(
            priceX - 3,
            y + 3,
            priceWidth + 4,
            17,
            Color{126, 94, 35, 255}
        );
        m_smallTextDrawer->drawText(
            priceX,
            y + 4,
            priceColor,
            price,
            false
        );
    }
}

void cBuildingListDrawer::setPlayer(cPlayer *player)
{
    this->m_player = player;
}

HudLayout cBuildingListDrawer::getLayout(cBuildingList *list) const
{
    const bool reserveOrderArea =
        list != nullptr &&
        list->getType() == eListType::LIST_STARPORT;
    return HudLayout::create(
        game.isHdGraphicsActive(),
        game.m_screenW,
        game.m_screenH,
        reserveOrderArea
    );
}

int cBuildingListDrawer::getScrollRow(cBuildingList *list) const
{
    if (list == nullptr) {
        return 0;
    }
    const int listId = eListTypeAsInt(list->getType());
    if (listId < 0 || listId >= static_cast<int>(m_scrollRows.size())) {
        return 0;
    }
    return std::clamp(
        m_scrollRows[listId],
        0,
        getLayout(list).maxScrollRow(list->getItemCount())
    );
}

void cBuildingListDrawer::setScrollRow(cBuildingList *list, int row)
{
    if (list == nullptr) {
        return;
    }
    const int listId = eListTypeAsInt(list->getType());
    if (listId < 0 || listId >= static_cast<int>(m_scrollRows.size())) {
        return;
    }
    m_scrollRows[listId] = std::clamp(
        row,
        0,
        getLayout(list).maxScrollRow(list->getItemCount())
    );
}

void cBuildingListDrawer::scrollSelectedList(int rowDelta)
{
    if (m_player == nullptr || m_player->getSideBar() == nullptr) {
        return;
    }
    cSideBar *sidebar = m_player->getSideBar();
    const int selectedId = sidebar->getSelectedListID();
    if (selectedId < 0 || selectedId >= cSideBar::LIST_MAX) {
        return;
    }
    cBuildingList *list = sidebar->getList(selectedId);
    setScrollRow(list, getScrollRow(list) + rowDelta);
}

void cBuildingListDrawer::drawHdScrollbar(
    cBuildingList *list,
    const HudLayout &layout)
{
    const Color track{10, 13, 15, 245};
    const Color border{83, 69, 43, 255};
    const Color thumb{181, 135, 44, 255};
    renderDrawer->renderRectFillColor(
        layout.scrollbar.getX(),
        layout.scrollbar.getY(),
        layout.scrollbar.getWidth(),
        layout.scrollbar.getHeight(),
        track
    );
    renderDrawer->renderRectColor(
        layout.scrollbar.getX(),
        layout.scrollbar.getY(),
        layout.scrollbar.getWidth(),
        layout.scrollbar.getHeight(),
        border
    );

    if (layout.maxScrollRow(list->getItemCount()) <= 0) {
        return;
    }
    const cRectangle thumbRect = layout.scrollbarThumb(
        list->getItemCount(),
        getScrollRow(list)
    );
    renderDrawer->renderRectFillColor(
        thumbRect.getX() + 2,
        thumbRect.getY() + 2,
        thumbRect.getWidth() - 4,
        thumbRect.getHeight() - 4,
        thumb
    );
}

void cBuildingListDrawer::onNotifyMouseEvent(const s_MouseEvent &event)
{
    if (!game.isHdGraphicsActive() ||
        m_player == nullptr ||
        m_player->getSideBar() == nullptr) {
        return;
    }

    cSideBar *sidebar = m_player->getSideBar();
    const int selectedId = sidebar->getSelectedListID();
    if (selectedId < 0 || selectedId >= cSideBar::LIST_MAX) {
        return;
    }
    cBuildingList *list = sidebar->getList(selectedId);
    if (list == nullptr) {
        return;
    }

    const HudLayout layout = getLayout(list);
    if (!layout.catalog.isPointWithin(event.coords.x, event.coords.y)) {
        return;
    }

    if (event.eventType == eMouseEventType::MOUSE_SCROLLED_UP) {
        scrollSelectedList(-1);
        return;
    }
    if (event.eventType == eMouseEventType::MOUSE_SCROLLED_DOWN) {
        scrollSelectedList(1);
        return;
    }
    if (event.eventType != eMouseEventType::MOUSE_LEFT_BUTTON_CLICKED ||
        !layout.scrollbar.isPointWithin(event.coords.x, event.coords.y)) {
        return;
    }

    const cRectangle thumb = layout.scrollbarThumb(
        list->getItemCount(),
        getScrollRow(list)
    );
    if (event.coords.y < thumb.getY()) {
        scrollSelectedList(-layout.visibleRows());
    }
    else if (event.coords.y > thumb.getEndY()) {
        scrollSelectedList(layout.visibleRows());
    }
}

void cBuildingListDrawer::onNotifyKeyboardEvent(const cKeyboardEvent &event)
{
    switch (event.eventType) {
        case eKeyEventType::HOLD:
            onKeyHold(event);
            break;
        case eKeyEventType::PRESSED:
            onKeyPressed(event);
            break;
        default:
            break;
    }
}

void cBuildingListDrawer::onKeyHold(const cKeyboardEvent &event)
{
    if (event.hasKeys(SDL_SCANCODE_TAB, SDL_SCANCODE_D)) {
        m_renderListIds = true;
    }
}

void cBuildingListDrawer::onKeyPressed(const cKeyboardEvent &event)
{
    if (event.hasEitherKey(SDL_SCANCODE_TAB, SDL_SCANCODE_D)) {
        m_renderListIds = false;
    }
}
