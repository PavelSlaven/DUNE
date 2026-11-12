/**
 * @file cMouseDrawer.cpp
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

#include "cMouseDrawer.h"
#include "include/sGameServices.h"
#include "controls/cGameControlsContext.h"
#include "controls/cMouse.h"
#include "context/GameContext.hpp"
#include "drawers/SDLDrawer.hpp"
#include "gameobjects/structures/cRefinery.h"
#include "gameobjects/structures/cSpiceSilo.h"
#include "gameobjects/structures/cWindTrap.h"
#include "gui/cTextWriter.h"
#include "gameobjects/players/cPlayer.h"

#include <SDL3/SDL.h>
#include <algorithm>
#include "include/cAssert.h"
#include "game/cGameSettings.h"
#include "utils/Localization.hpp"

void cMouseDrawer::serviceInit(sGameServices* services)
{
    m_renderer = services->ctx->getSDLDrawer();
    m_settings = services->settings;
    m_mouse = services->mouse;
}

cMouseDrawer::cMouseDrawer(cPlayer *thePlayer, cTextDrawer *textDrawer) : m_player(thePlayer)
{
    d2tm_assert(thePlayer != nullptr);
    d2tm_assert(textDrawer != nullptr);
    m_mouseX = m_mouseY = 0;
    m_textWriter = std::make_unique<cTextWriter>(textDrawer,12);
}

void cMouseDrawer::draw()
{
    m_mouse->draw();
}

int cMouseDrawer::getDrawXToolTip(int width)
{
    int x = m_mouseX + 32;

    // correct drawing position so it does not fall off screen.
    int diffX = (x + width) - m_settings->getScreenW();
    if (diffX > 0) {
        x-= diffX;
    }
    return x;
}

int cMouseDrawer::getDrawYToolTip(int height)
{
    int y = m_mouseY + 32;

    // correct drawing position so it does not fall off screen.
    int diffY = (y + height) - m_settings->getScreenH();
    if (diffY > 0) {
        y -= diffY;
    }
    return y;
}

int cMouseDrawer::getWidthToolTip()
{
    cGameControlsContext *context = m_player->getGameControlsContext();

    if (context->isMouseOverStructure()) {
        return 250;
    }

    return 0;
}

int cMouseDrawer::getHeightToolTip()
{
    cGameControlsContext *context = m_player->getGameControlsContext();

    if (context->isMouseOverStructure()) {
        cAbstractStructure *theStructure = context->getStructurePointerWhereMouseHovers();

        int height = 50;
        switch (theStructure->getType()) {
            case WINDTRAP:
                height = 78;
                break;
            case REFINERY:
                height = 78;
                break;
            case SILO:
                height = 78;
                break;
            case TURRET:
                height = 78;
                break;
            case RTURRET:
                height = 78;
                break;
            default:
                height = 50;
                break;
        }
        return height;
    }

    return 0;
}

void cMouseDrawer::drawToolTip()
{
    int height = getHeightToolTip();
    int width = getWidthToolTip();

    if (height <= 0|| width <= 0) {
        return;
    }

    int x = getDrawXToolTip(width);
    int y = getDrawYToolTip(height);

    cGameControlsContext *context = m_player->getGameControlsContext();

    if (context->isMouseOverStructure()) {
        m_textWriter->moveTo(x + 2, y + 2);
        cAbstractStructure *theStructure = context->getStructurePointerWhereMouseHovers();

        drawToolTipBackground();
        drawToolTipGeneralInformation(theStructure);

//		// depending on structure type give more info
        int structureType = theStructure->getType();
        if (structureType == WINDTRAP) {
            cWindTrap *windTrap = dynamic_cast<cWindTrap *>(theStructure);
            d2tm_assert(windTrap);
            drawToolTipWindTrapInformation(windTrap);
        }
        else if (structureType == SILO || structureType == REFINERY) {
            drawToolTipSiloInformation(theStructure);
        }
        else if (structureType == TURRET || structureType == RTURRET) {
            drawToolTipTurretInformation(theStructure);
        }
    }
}

void cMouseDrawer::drawToolTipBackground()
{
    cGameControlsContext *context = m_player->getGameControlsContext();

    int width = getWidthToolTip();
    int height = getHeightToolTip();

    int x = getDrawXToolTip(width);
    int y = getDrawYToolTip(height);

    Color color = m_player->getMinimapColor();

    if (context->isMouseOverStructure()) {
        cAbstractStructure *theStructure = context->getStructurePointerWhereMouseHovers();
        color = theStructure->getPlayer()->getMinimapColor();
    }

    unsigned char red = color.r;
    unsigned char green = color.g;
    unsigned char blue = color.b;

    // tone down a bit
    red = std::max(red - 64, 0);
    green = std::max(green - 64, 0);
    blue = std::max(blue - 64, 0);

    color = Color{red, green, blue,128};
    auto black = Color::Black;
    black.a = 128;
    m_renderer->renderRectFillColor(x, y, width, height, color);
    int shadowX = x + width;
    int shadowY = y + height;
    m_renderer->renderRectFillColor(x + 4, shadowY, (width - 4), 4, black);
    m_renderer->renderRectFillColor(shadowX, y + 4, 4, height, black);
}

void cMouseDrawer::drawToolTipTurretInformation(cAbstractStructure *theStructure)
{
    d2tm_assert(theStructure);
    if (theStructure->belongsTo(m_player)) {
        m_textWriter->write(localization::format("Sight : {}", "Обзор: {}", theStructure->getSight()));
        m_textWriter->write(localization::format("Range : {}", "Дальность: {}", theStructure->getRange()));
    }
    else {
        m_textWriter->write(localization::text("Sight : Unknown", "Обзор: неизвестно"));
        m_textWriter->write(localization::text("Range : Unknown", "Дальность: неизвестно"));
    }
}

void cMouseDrawer::drawToolTipGeneralInformation(cAbstractStructure *theStructure)
{
    d2tm_assert(theStructure);
    const s_StructureInfo &structureType = theStructure->getStructureInfo();

    std::string description;
    if (theStructure->isPrimary()) {
        description=localization::format("{} (PRIMARY)", "{} (основное)", structureType.name);
    }
    else {
        description=std::format("{}", structureType.name);
    }
    m_textWriter->write(description.c_str(), Color{255, 255, 0,255});
    m_textWriter->write(localization::format("Hitpoints : {}/{}", "Прочность: {}/{}", theStructure->getHitPoints(), theStructure->getMaxHP()));
    m_textWriter->write(localization::format("Armor : {}", "Броня: {}", theStructure->getArmor()));
    m_textWriter->write(localization::format("Protected : {}%%", "Защита: {} %", (100-theStructure->getPercentageNotPaved())));
}

void cMouseDrawer::drawToolTipWindTrapInformation(cWindTrap *theWindTrap)
{
    d2tm_assert(theWindTrap);
    if (theWindTrap->getOwner() == HUMAN) {
        int powerOut = theWindTrap->getPlayer()->getPowerProduced();
        int powerUse = theWindTrap->getPlayer()->getPowerUsage();

        if (powerUse <= powerOut) {
            m_textWriter->write(localization::format("Total usage : {}/{} (OK)", "Расход: {}/{} (норма)", powerUse, powerOut));
        }
        else {
            m_textWriter->write(localization::format("Total usage : {}/{} (LOW)", "Расход: {}/{} (мало)", powerUse, powerOut));
        }
        m_textWriter->write(localization::format("Windtrap outage : {}/{}", "Выработка: {}/{}", theWindTrap->getPowerOut(), theWindTrap->getMaxPowerOut()));
    }
    else {
        m_textWriter->write(localization::text("Total usage : Unknown", "Расход: неизвестно"));
        m_textWriter->write(localization::text("Windtrap outage : Unknown", "Выработка: неизвестно"));
    }
}

void cMouseDrawer::drawToolTipSiloInformation(cAbstractStructure *theStructure)
{
    d2tm_assert(theStructure);

    // TODO / IDEA --> Perhaps some 'spy on enemy intel' upgrade should be available for
    // house Ordos, so you can actually check on the enemy spice etc.
    if (theStructure->getOwner() == HUMAN) {
        int spiceCapacityOfStructure = 0;
        if (theStructure->getType() == REFINERY) {
            cRefinery *refinery = dynamic_cast<cRefinery *>(theStructure);
            d2tm_assert(refinery);
            spiceCapacityOfStructure = refinery->getSpiceSiloCapacity();
        }
        else if (theStructure->getType() == SILO) {
            cSpiceSilo *spiceSilo = dynamic_cast<cSpiceSilo *>(theStructure);
            d2tm_assert(spiceSilo);
            spiceCapacityOfStructure = spiceSilo->getSpiceSiloCapacity();
        }

        cPlayer *thePlayer = theStructure->getPlayer();
        int maxSpice = thePlayer->getMaxCredits();
        int currentSpice =  thePlayer->getCredits();
        if (currentSpice <= maxSpice) {
            m_textWriter->write(localization::format("Total usage : {}/{} (OK)", "Запас: {}/{} (норма)", currentSpice, maxSpice));
        }
        else {
            m_textWriter->write(localization::format("Total usage : {}/{} (NOK)", "Запас: {}/{} (не норма)", currentSpice, maxSpice));
        }
        m_textWriter->write(localization::format("Silo capacity : {}/{}", "Ёмкость хранилища: {}/{}", spiceCapacityOfStructure, 1000));
    }
    else {
        m_textWriter->write(localization::text("Spice usage : Unknown", "Пряность: неизвестно"));
    }
}

void cMouseDrawer::onMouseAt(const s_MouseEvent &event)
{
    this->m_mouseX = event.coords.x;
    this->m_mouseY = event.coords.y;
}

void cMouseDrawer::onNotify(const s_MouseEvent &event)
{
    if (event.eventType == eMouseEventType::MOUSE_MOVED_TO) {
        onMouseAt(event);
    }
}
