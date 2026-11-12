/**
 * @file cBuildingListDrawer.cpp
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

#include "cBuildingListDrawer.h"
#include "debug/UiAudit.hpp"
#include "include/sGameServices.h"
#include "drawers/SDLDrawer.hpp"
#include "data/gfxinter.h"
#include "gameobjects/structures/cOrderProcesser.h"
#include "gameobjects/players/cPlayer.h"
#include "utils/Graphics.hpp"
#include "context/GameContext.hpp"
#include "context/GraphicsContext.hpp"
#include "context/cInfoContext.h"
#include "context/cGameObjectContext.h"
#include "controls/cMouse.h"
#include "utils/common.h"
#include "utils/Log.h"

#include <SDL3/SDL.h>
#include <algorithm>
#include <format>
#include <sstream>
#include <vector>

#include "gameobjects/structures/cStructureFactory.h"
#include "gameobjects/units/cUnits.h"
#include "include/cAssert.h"
#include "include/Texture.hpp"
#include "context/TextContext.hpp"
#include "drawers/cTextDrawer.h"
#include "game/cGameSettings.h"
#include "gameobjects/structures/cStructureInfo.h"
#include "utils/Localization.hpp"
#include "utils/Utf8.hpp"

namespace {
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
    if (name == "Hi-Tech") return "Hi-Tech";
    if (name == localization::text("Spice Refinery", "Переработчик пряности")) return localization::text("Refinery", "Переработчик");
    if (name == "MCV") return "MCV";
    if (name == localization::text("Light Infantry", "Отряд пехоты")) return localization::text("Infantry", "Пехота");
    if (name == localization::text("Troopers", "Отряд ракетчиков")) return localization::text("Troopers", "Ракетчики");
    return name;
}
}
#include "controls/cKeyboardEvent.h"

cBuildingListDrawer::cBuildingListDrawer(const GameContext *ctx, cPlayer *player) :
    m_gameTextDrawer(ctx->getTextContext()->getGameTextDrawer()),
    m_smallTextDrawer(ctx->getTextContext()->getSmallTextDrawer()),
    m_gfxinter(ctx->getGraphicsContext()->gfxinter.get()),
    m_sdlDrawer(ctx->getSDLDrawer()),
    m_player(player),
    m_renderListIds(false),
    m_readyLabel(localization::text("READY", "ГОТОВО"))
{
    d2tm_assert(player != nullptr);
    d2tm_assert(ctx != nullptr);
}

void cBuildingListDrawer::serviceInit(sGameServices* services)
{
    m_infos = services->info;
    m_settings = services->settings;
    m_mouse = services->mouse;
    m_objects = services->objects;
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
    d2tm_assert(list != nullptr);

    int x = list->getButtonDrawX();
    int y = list->getButtonDrawY();

    int width = list->getButtonWidth();
    int height = list->getButtonHeight();

    Color color = m_player->getSelectFadingColor();

    m_sdlDrawer->renderRectColor(x, y, width, height, color);
    m_sdlDrawer->renderRectColor(x + 1, y + 1, width-2, height-2, color);
}

void cBuildingListDrawer::drawButton(cBuildingList *list, bool pressed)
{
    d2tm_assert(list != nullptr);

    int x = list->getButtonDrawX();
    int y = list->getButtonDrawY();
    int id = list->getButtonIconIdUnpressed();

    if (pressed) {
        id = list->getButtonIconIdPressed();
    }

    if (id < 0) {
        // this is not good
        Logger::error(COMP_GAME, "cBuildingListDrawer::drawButton","unable to draw list because id is not valid!? id={}", id);
        return;
    }

    int width = list->getButtonWidth();
    int height = list->getButtonHeight();
    const Color panel{18, 22, 25, 255};
    const Color border{93, 78, 49, 255};
    const Color active{217, 164, 54, 255};
    m_sdlDrawer->renderRectFillColor(x, y, width, height, panel);

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
    m_sdlDrawer->renderStrechFullSprite(
        icon,
        iconRect,
        list->isAvailable() ? 255 : 96
    );
    if (!list->isAvailable()) {
        m_sdlDrawer->renderRectFillColor(
            iconRect,
            Color{20, 22, 23, 255},
            138
        );
    }
    m_sdlDrawer->renderRectColor(
        x,
        y,
        width,
        height,
        pressed ? active : border
    );
    if (pressed) {
        m_sdlDrawer->renderRectFillColor(
            x + 2,
            y + height - 3,
            width - 4,
            2,
            active
        );
        list->stopFlashing();
    }
    else if (list->isFlashing()) {
        m_sdlDrawer->renderRectColor(
            x + 1,
            y + 1,
            width - 2,
            height - 2,
            list->getFlashingColor()
        );
    }
}


int cBuildingListDrawer::getDrawX()
{
    return getLayout().cards.getX();
}

int cBuildingListDrawer::getDrawY()
{
    return getLayout().cards.getY();
}

/**
 * Draw the list, start from startId, until the max icons in the list to be drawn.
 */
void cBuildingListDrawer::drawList(cBuildingList *list, const bool shouldDrawStructureSize)
{
    const HudLayout layout = getLayout(list);
    const int scrollRow = getScrollRow(list);
    int iDrawX = getDrawX();
    int iDrawY = getDrawY();
    const Color selectFadingColor = m_player->getSelectFadingColor();
    constexpr int end = MAX_ITEMS;
    const std::array<int, 6> isBuildingItemInList = list->isBuildingItem();
    const int withOfIcon = getCardWidth();
    const int heightOfIcon = getCardHeight();
    const bool structureLimitReached =
        list->isType(eListType::LIST_CONSTYARD) &&
        m_objects->getStructureFactory()->isStructureLimitReached();
    const bool unitLimitReached =
        (list->isType(eListType::LIST_FOOT_UNITS) ||
         list->isType(eListType::LIST_UNITS)) &&
        m_objects->getUnits()->isUnitLimitReached();

    m_sdlDrawer->setClippingFor(
        layout.cards.getX(),
        layout.cards.getY(),
        layout.cards.getEndX(),
        layout.cards.getEndY()
    );

    for (int i = 0; i < end; i++) {
        cBuildingListItem *item = list->getItem(i);
        if (item == nullptr) {
            continue;
        }

        const cRectangle card = layout.cardRect(i, scrollRow);
        if (card.getEndY() <= layout.cards.getY() ||
            card.getY() >= layout.cards.getEndY()) {
            continue;
        }
        iDrawX = card.getX();
        iDrawY = card.getY();
        const int iDrawXEnd = iDrawX + withOfIcon;
        const int iDrawYEnd = iDrawY + heightOfIcon;
        const bool cannotPayIt = !m_player->hasEnoughCreditsFor(item->getBuildCost());

        d2tm_assert(item->getIconId() > -1);
        drawHdCard(item, iDrawX, iDrawY);
        if (shouldDrawStructureSize) {
            drawStructureSize(item->getBuildId(), iDrawX, iDrawY);
        }

        if (item->isBuilding()) {
            const int iFrame = item->getBuildProgressFrame();
            if (!item->isDoneBuilding() || iFrame < 31) {
                const int progressWidth = std::clamp(
                    (withOfIcon - 4) * iFrame / 31,
                    0,
                    withOfIcon - 4
                );
                const int progressY = iDrawY + heightOfIcon - 36;
                m_sdlDrawer->renderRectFillColor(
                    iDrawX + 2,
                    progressY,
                    withOfIcon - 4,
                    4,
                    15,
                    18,
                    20,
                    230
                );
                m_sdlDrawer->renderRectFillColor(
                    iDrawX + 2,
                    progressY,
                    progressWidth,
                    4,
                    selectFadingColor
                );
                if (item->isPaused()) {
                    m_smallTextDrawer->drawTextCenteredInBox(
                        localization::text("Paused", "Пауза"),
                        iDrawX + 2,
                        iDrawY + 2,
                        withOfIcon - 4,
                        heightOfIcon - 32,
                        Color::Yellow
                    );
                }
            }
            else {
                if (item->shouldPlaceIt()) {
                    const Color readyColor = m_player->isContextMouseState(
                        eMouseState::MOUSESTATE_PLACE
                    ) ? Color{225, 48, 42, 255} : Color::White;
                    m_smallTextDrawer->drawTextScaledCenteredInBox(
                        m_readyLabel,
                        cRectangle(iDrawX + 2, iDrawY + 2, withOfIcon - 4, heightOfIcon - 32),
                        1.0F,
                        readyColor
                    );
                }
                else if (item->shouldDeployIt()) {
                    const Color readyColor = m_player->isContextMouseState(
                        eMouseState::MOUSESTATE_DEPLOY
                    ) ? Color{225, 48, 42, 255} : Color::White;
                    m_smallTextDrawer->drawTextScaledCenteredInBox(
                        m_readyLabel,
                        cRectangle(iDrawX + 2, iDrawY + 2, withOfIcon - 4, heightOfIcon - 32),
                        1.0F,
                        readyColor
                    );
                }
            }
            if (unitLimitReached && item->isTypeUnit()) {
                drawMaxBuilt(
                    iDrawX + 2,
                    iDrawY + 2,
                    withOfIcon - 4,
                    heightOfIcon - 32
                );
            }
        }
        else {
            bool isBuildingSameSubListItem = false;
            for (int i2 = 0; i2 < 5; i2++) {
                if (isBuildingItemInList[i2] < 0) continue;
                if (i2 == item->getSubList()) {
                    isBuildingSameSubListItem = true;
                    break;
                }
            }

            const bool cannotBuildDueStructureLimit =
                structureLimitReached &&
                !cStructureFactory::isModifyingTerrain(item->getBuildId());
            const bool cannotBuildDueUnitLimit =
                unitLimitReached && item->isTypeUnit();
            const bool cannotBuildDueLimit =
                cannotBuildDueStructureLimit || cannotBuildDueUnitLimit;

            if (!item->isAvailable() || isBuildingSameSubListItem || cannotBuildDueLimit) {
                if (!cannotBuildDueLimit) {
                    m_sdlDrawer->renderRectFillColor(
                        iDrawX,
                        iDrawY,
                        withOfIcon,
                        heightOfIcon - 32,
                        0,
                        0,
                        0,
                        128
                    );
                    if (item->isPendingUpgrading()) {
                        const Color errorFadingColor = m_player->getErrorFadingColor();
                        m_sdlDrawer->renderRectColor(
                            iDrawX,
                            iDrawY,
                            iDrawXEnd - iDrawX,
                            iDrawYEnd - iDrawY,
                            errorFadingColor
                        );
                        m_sdlDrawer->renderLine(
                            iDrawX,
                            iDrawY,
                            iDrawXEnd,
                            iDrawYEnd,
                            errorFadingColor
                        );
                        m_sdlDrawer->renderLine(
                            iDrawX,
                            iDrawY + heightOfIcon,
                            iDrawX + withOfIcon,
                            iDrawY,
                            errorFadingColor
                        );
                        m_smallTextDrawer->drawTextCenteredInBox(
                            localization::text("Upgrade", "Улучшение"),
                            iDrawX,
                            iDrawY,
                            withOfIcon,
                            heightOfIcon,
                            Color{255, 0, 0, 255}
                        );
                    }
                    if (item->isPendingBuilding()) {
                        const Color errorFadingColor = m_player->getErrorFadingColor();
                        m_sdlDrawer->renderRectColor(
                            iDrawX,
                            iDrawY,
                            iDrawXEnd - iDrawX,
                            iDrawYEnd - iDrawY,
                            errorFadingColor
                        );
                        m_sdlDrawer->renderLine(
                            iDrawX,
                            iDrawY,
                            iDrawXEnd,
                            iDrawYEnd,
                            errorFadingColor
                        );
                        m_sdlDrawer->renderLine(
                            iDrawX,
                            iDrawY + heightOfIcon,
                            iDrawX + withOfIcon,
                            iDrawY,
                            errorFadingColor
                        );
                        m_smallTextDrawer->drawTextCenteredInBox(
                            localization::text("OCCUPIED", "ЗАНЯТО"),
                            iDrawX,
                            iDrawY,
                            withOfIcon,
                            heightOfIcon,
                            Color{255, 0, 0, 255}
                        );
                    }
                }
                else {
                    drawMaxBuilt(
                        iDrawX + 2,
                        iDrawY + 2,
                        withOfIcon - 4,
                        heightOfIcon - 32
                    );
                }
            }

            if (list->getType() == eListType::LIST_STARPORT) {
                cOrderProcesser *orderProcesser = m_player->getOrderProcesser();
                const bool orderIsAwaitingFrigate =
                    orderProcesser->isOrderPlaced() || orderProcesser->isFrigateSent();
                if (cannotPayIt || orderIsAwaitingFrigate) {
                    m_sdlDrawer->renderRectFillColor(
                        iDrawX,
                        iDrawY,
                        withOfIcon,
                        heightOfIcon - 32,
                        0,
                        0,
                        0,
                        128
                    );
                    const Color errorFadingColor = m_player->getErrorFadingColor();
                    m_sdlDrawer->renderRectColor(
                        iDrawX,
                        iDrawY,
                        iDrawXEnd - iDrawX,
                        iDrawYEnd - iDrawY,
                        errorFadingColor
                    );
                    m_sdlDrawer->renderLine(
                        iDrawX,
                        iDrawY,
                        iDrawXEnd,
                        iDrawYEnd,
                        errorFadingColor
                    );
                    m_sdlDrawer->renderLine(
                        iDrawX,
                        iDrawY + heightOfIcon,
                        iDrawX + withOfIcon,
                        iDrawY,
                        errorFadingColor
                    );
                }
            }

            if (list->getLastClickedId() == i) {
                m_sdlDrawer->renderRectColor(
                    iDrawX + 1,
                    iDrawY + 1,
                    iDrawXEnd - iDrawX - 2,
                    iDrawYEnd - iDrawY - 2,
                    selectFadingColor
                );
                m_sdlDrawer->renderRectColor(
                    iDrawX,
                    iDrawY,
                    iDrawXEnd - iDrawX,
                    iDrawYEnd - iDrawY,
                    selectFadingColor
                );
            }
        }

        int amountToShow = item->getTimesToBuild();
        bool showAmount = item->isQueuable() && amountToShow > 0;
        const bool listIsStarport = item->getList()->getType() == eListType::LIST_STARPORT;
        if (listIsStarport) {
            amountToShow = item->getTimesOrdered();
            showAmount = true;
        }

        if (showAmount) {
            int textX = iDrawX + withOfIcon - 20;
            const int textY = iDrawY + heightOfIcon - 51;
            if (amountToShow < 10) {
                textX += 6;
            }
            m_sdlDrawer->renderRectFillColor(
                textX - 3,
                textY - 1,
                withOfIcon - (textX - iDrawX) - 1,
                16,
                8,
                10,
                12,
                220
            );
            m_gameTextDrawer->drawText(textX, textY, std::format("{}", amountToShow));
        }

        if (m_settings->isDebugMode() && m_renderListIds) {
            const int textX = iDrawX + 41;
            const int textY = iDrawY + 40;
            m_gameTextDrawer->drawText(textX, textY, std::format("{}", item->getSubList()));
        }

        if (isOverItemCoordinates_Boolean(m_mouse->getX(), m_mouse->getY(), iDrawX, iDrawY)) {
            if (uiaudit::isEnabled()) { uiaudit::recordLabel("card-hover", i, "ITEM", iDrawX, iDrawY, iDrawXEnd - iDrawX, iDrawYEnd - iDrawY, uiaudit::Rect{card.getX(), card.getY(), card.getWidth(), card.getHeight()}); }
            m_sdlDrawer->renderRectColor(
                iDrawX + 1,
                iDrawY + 1,
                iDrawXEnd - iDrawX - 2,
                iDrawYEnd - iDrawY - 2,
                selectFadingColor
            );
            m_sdlDrawer->renderRectColor(
                iDrawX,
                iDrawY,
                iDrawXEnd - iDrawX,
                iDrawYEnd - iDrawY,
                selectFadingColor
            );
        }
        else {
            const Color color = list->getFlashingColor();
            if (item->isFlashing()) {
                m_sdlDrawer->renderRectColor(
                    iDrawX + 1,
                    iDrawY + 1,
                    iDrawXEnd - iDrawX - 2,
                    iDrawYEnd - iDrawY - 2,
                    color
                );
                m_sdlDrawer->renderRectColor(
                    iDrawX,
                    iDrawY,
                    iDrawXEnd - iDrawX,
                    iDrawYEnd - iDrawY,
                    color
                );
            }
        }
    }

    m_sdlDrawer->resetClippingFor();
    drawHdScrollbar(list, layout);
}
/**
 * Draws the red cross with "Max built" over an icon, when its item can not be built because a limit is reached.
 */
void cBuildingListDrawer::drawMaxBuilt(int x, int y, int width, int height)
{
    m_sdlDrawer->renderSprite(m_gfxinter->getTexture(PROGRESSNA), x, y, 64);
    Color errorFadingColor = m_player->getErrorFadingColor();
    m_sdlDrawer->renderRectColor(x, y, width, height, errorFadingColor);
    m_sdlDrawer->renderLine(x, y, x + width, y + height, errorFadingColor);
    m_sdlDrawer->renderLine(x, y + height, x + width, y, errorFadingColor);

    int halfHeight = height / 2;
    m_smallTextDrawer->drawTextCenteredInBox(localization::text("Max", "Больше"), x, y, width, halfHeight, Color::Red);
    m_smallTextDrawer->drawTextCenteredInBox(localization::text("built", "нельзя"), x, y + halfHeight, width, halfHeight, Color::Red);
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
    int iW= m_infos->getStructureInfo(structureId).bmp_width / 32;
    int iH= m_infos->getStructureInfo(structureId).bmp_height / 32;
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

    const int gridX = x + getCardWidth() - 22;
    const int gridY = y + 3;
    m_sdlDrawer->renderRectFillColor(gridX, gridY, 19, 19, 8, 10, 12, 220);
    m_sdlDrawer->renderSprite(m_gfxinter->getTexture(GRID_0X0), gridX, gridY);
    m_sdlDrawer->renderSprite(m_gfxinter->getTexture(iTile), gridX, gridY);
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
    d2tm_assert(list != nullptr);
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

int cBuildingListDrawer::getCardWidth() const
{
    return getLayout().cardWidth;
}

int cBuildingListDrawer::getCardHeight() const
{
    return getLayout().cardHeight;
}

void cBuildingListDrawer::drawHdCard(cBuildingListItem *item, int x, int y)
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

    m_sdlDrawer->renderRectFillColor(x, y, cardWidth, cardHeight, panelColor);
    Texture *icon = m_gfxinter->getTexture(item->getIconId());
    m_sdlDrawer->renderStrechSprite(
        icon,
        cRectangle(0, 0, icon->w, icon->h),
        cRectangle(x + 3, y + 3, cardWidth - 6, imageHeight - 5)
    );
    m_sdlDrawer->renderRectFillColor(
        x + 1,
        y + imageHeight,
        cardWidth - 2,
        labelHeight - 1,
        panelColor
    );
    m_sdlDrawer->renderRectColor(x, y, cardWidth, cardHeight, borderColor);
    m_sdlDrawer->renderRectColor(
        x + 1,
        y + 1,
        cardWidth - 2,
        cardHeight - 2,
        innerBorder
    );
    m_sdlDrawer->renderLine(
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
        secondLine = fitWithEllipsis(m_smallTextDrawer, secondLine, textWidth);
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
            const int firstLineY = y + imageHeight + 2;
            m_smallTextDrawer->drawTextCentered(
                firstLine,
                x + 3,
                textWidth,
                firstLineY,
                labelColor
            );
            m_smallTextDrawer->drawTextCentered(
                secondLine,
                x + 3,
                textWidth,
                firstLineY + m_smallTextDrawer->getFontHeight(),
                labelColor
            );
        }
    }

    if (item->getBuildCost() > 0) {
        const std::string price = std::format("${}", item->getBuildCost());
        const int priceWidth = m_smallTextDrawer->getTextLength(price);
        const int priceX = x + 6;
        m_sdlDrawer->renderRectFillColor(
            priceX - 3,
            y + 3,
            priceWidth + 4,
            17,
            8,
            10,
            12,
            220
        );
        m_sdlDrawer->renderRectColor(
            priceX - 3,
            y + 3,
            priceWidth + 4,
            17,
            Color{126, 94, 35, 255}
        );
        m_smallTextDrawer->drawText(priceX, y + 4, priceColor, price, false);
    }
}

void cBuildingListDrawer::setPlayer(cPlayer *player)
{
    this->m_player = player;
}

HudLayout cBuildingListDrawer::getLayout(cBuildingList *list) const
{
    const bool reserveOrderArea =
        list != nullptr && list->getType() == eListType::LIST_STARPORT;
    return HudLayout::create(
        m_settings->getScreenW(),
        m_settings->getScreenH(),
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
    m_sdlDrawer->renderRectFillColor(
        layout.scrollbar.getX(),
        layout.scrollbar.getY(),
        layout.scrollbar.getWidth(),
        layout.scrollbar.getHeight(),
        track
    );
    m_sdlDrawer->renderRectColor(
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
    m_sdlDrawer->renderRectFillColor(
        thumbRect.getX() + 2,
        thumbRect.getY() + 2,
        thumbRect.getWidth() - 4,
        thumbRect.getHeight() - 4,
        thumb
    );
}

void cBuildingListDrawer::onNotifyMouseEvent(const s_MouseEvent &event)
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
    switch (event.getType()) {
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
