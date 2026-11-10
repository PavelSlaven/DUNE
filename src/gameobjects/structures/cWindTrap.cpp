/**
 * @file cWindTrap.cpp
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

#include "cWindTrap.h"

#include "utils/Log.h"
#include "definitions.h"
#include "gameobjects/players/cPlayer.h"
#include "context/cInfoContext.h"
#include <format>

// Constructor
cWindTrap::cWindTrap()
{
    Logger::debug(COMP_STRUCTURES, "cWindTrap", "(cWindTrap)(ID {}) Constructor", this->id);

    iFrame = 0;
}

int cWindTrap::getType() const
{
    return WINDTRAP;
}

cWindTrap::~cWindTrap()
{
    Logger::debug(COMP_STRUCTURES, "cWindTrap", "(cWindTrap)(ID {}) Destructor", this->id);
}

void cWindTrap::thinkFast()
{
    cAbstractStructure::thinkFast();
}

void cWindTrap::think_animation()
{
    cAbstractStructure::think_animation();
    cAbstractStructure::think_flag_new();
}

void cWindTrap::think_guard()
{

}

/*  STRUCTURE SPECIFIC FUNCTIONS  */
int cWindTrap::getPowerOut() const
{
    float percentage = (static_cast<float>(getHitPoints()) / static_cast<float>(m_info->getStructureInfo(getType()).hp));
    return getMaxPowerOut() * percentage;
}

int cWindTrap::getMaxPowerOut() const
{
    return getStructureInfo().power_give;
}

std::string cWindTrap::getStatusForMessageBar() const
{
    int powerProduction = (static_cast<float>(getPowerOut()) / static_cast<float>(getMaxPowerOut())) * static_cast<float>(100);
    return std::format("{} and producing at {} percent capacity", cAbstractStructure::getDefaultStatusMessageBar(), powerProduction);
}
