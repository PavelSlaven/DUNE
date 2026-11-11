/**
 * @file cBuildingListFactory.cpp
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

#include "cBuildingListFactory.h"
#include "game/cGameSettings.h"
#include "data/gfxinter.h"
#include "sidebar/HudLayout.hpp"

cBuildingListFactory::cBuildingListFactory(cGameSettings* settings) : m_settings(settings)
{}

int cBuildingListFactory::getButtonDrawY()
{
    return HudLayout::create(
        m_settings->getScreenW(),
        m_settings->getScreenH()
    ).tabs.getY();
}

int cBuildingListFactory::getButtonDrawXStart()
{
    return HudLayout::create(
        m_settings->getScreenW(),
        m_settings->getScreenH()
    ).tabs.getX();
}


void cBuildingListFactory::initializeList(cBuildingList *list, eListType listType)
{
    d2tm_assert(list != nullptr);

    // first clear the list
    list->removeAllItems();

    // Y is the same for all list buttons
    list->setButtonDrawY(getButtonDrawY());

    const HudLayout layout = HudLayout::create(
        m_settings->getScreenW(),
        m_settings->getScreenH()
    );
    const int widthOfButtonIncludingMargin = layout.tabs.getWidth() / 6;
    const int buttonHeight = layout.tabs.getHeight();
    list->setButtonWidth(widthOfButtonIncludingMargin);
    list->setButtonHeight(buttonHeight);

    int startX = getButtonDrawXStart();

    // now set it up
    if (listType == eListType::LIST_CONSTYARD) {
        list->setButtonDrawX(startX);
        list->setButtonIconIdPressed(LIST_BTN_CONSTYARD);
        list->setButtonIconIdUnpressed(LIST_BTN_CONSTYARD);
    }


    startX += widthOfButtonIncludingMargin;

    // other lists, have 40 pixels more Y , but the X remains the same
    // now set it up
    if (listType == eListType::LIST_FOOT_UNITS) {
        list->setButtonDrawX(startX);
        list->setButtonIconIdPressed(LIST_BTN_INFANTRY);
        list->setButtonIconIdUnpressed(LIST_BTN_INFANTRY);
    }

    startX += widthOfButtonIncludingMargin;

    if (listType == eListType::LIST_UNITS) {
        list->setButtonDrawX(startX);
        list->setButtonIconIdPressed(LIST_BTN_FACTORY);
        list->setButtonIconIdUnpressed(LIST_BTN_FACTORY);
    }

    startX += widthOfButtonIncludingMargin;

    if (listType == eListType::LIST_STARPORT) {
        list->setButtonDrawX(startX);
        list->setButtonIconIdPressed(LIST_BTN_STARPORT);
        list->setButtonIconIdUnpressed(LIST_BTN_STARPORT);
    }

    startX += widthOfButtonIncludingMargin;

    if (listType == eListType::LIST_PALACE) {
        list->setButtonDrawX(startX);
        list->setButtonIconIdPressed(LIST_BTN_PALACE);
        list->setButtonIconIdUnpressed(LIST_BTN_PALACE);
    }

    startX += widthOfButtonIncludingMargin;

    if (listType == eListType::LIST_UPGRADES) {
        list->setButtonDrawX(startX);
        // temp, use CONST YARD
        list->setButtonIconIdPressed(LIST_BTN_UPGRADE);
        list->setButtonIconIdUnpressed(LIST_BTN_UPGRADE);

        // the contents of the list is determined elsewhere
    }

}

/**
 * Create new instance of list, initialize and return it.
 *
 * @param listType
 * @param techlevel
 * @return
 */
cBuildingList *cBuildingListFactory::createList(eListType listType)
{
    cBuildingList *list = new cBuildingList(listType);
    initializeList(list, listType);
    return list;
}
