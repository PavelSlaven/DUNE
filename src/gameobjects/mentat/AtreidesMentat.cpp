/**
 * @file AtreidesMentat.cpp
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

#include "AtreidesMentat.h"
#include "include/gfxmentat.h"
#include "drawers/SDLDrawer.hpp"
#include "utils/Graphics.hpp"
#include "utils/Log.h"
#include "gui/GuiButton.h"
#include <iostream>
#include "game/GameStateTransition.hpp"
#include "game/MentatFlow.hpp"
#include "include/cAssert.h"
#include "utils/Localization.hpp"

AtreidesMentat::AtreidesMentat(GameContext* ctx, cGameSettings* settings, GameStateTransition* stateTransitions, MentatFlow* mentatFlow, bool allowMissionSelect) : AbstractMentat(ctx, settings, stateTransitions, mentatFlow, allowMissionSelect)
{
    d2tm_assert(ctx != nullptr);
    d2tm_assert(m_mentatFlow != nullptr);
    iBackgroundFrame = MENTATA;
    m_hdLayout = &kAtreidesMentatHdLayout;
    buildLeftButton(gfxmentat->getTexture(BTN_REPEAT), 293, 423);
    buildRightButton(gfxmentat->getTexture(BTN_PROCEED), 466, 423);


    leftGuiButton = GuiButtonBuilder()
            .withRect(*leftButton)        
            .withLabel(localization::text("Repeat", "Повторить"))
            .withTexture(gfxmentat->getTexture(BTN_REPEAT))
            .withRenderer(m_sdlDrawer)
            .withKind(GuiRenderKind::WITH_TEXTURE)
            .onClick([this]() {this->resetSpeak();})
            .build();

    rightGuiButton = GuiButtonBuilder()
            .withRect(*rightButton)        
            .withLabel(localization::text("Yes", "Да"))
            .withTexture(gfxmentat->getTexture(BTN_YES))
            .withRenderer(m_sdlDrawer)
            .withKind(GuiRenderKind::WITH_TEXTURE)
            .onClick([this]() {
                Logger::info(COMP_GAME, "AtreidesMentat", "changing state from mentat");
                m_mentatFlow->leave();})
            .build();
}

void AtreidesMentat::think()
{
    // think like base class
    AbstractMentat::think();
}

void AtreidesMentat::draw()
{
    AbstractMentat::draw();
}

void AtreidesMentat::draw_other()
{

}

void AtreidesMentat::draw_eyes()
{
    drawMentatTexture(gfxmentat->getTexture(ATR_EYES01 + iMentatEyes), kAtreidesMentatHdLayout.eyes);
}

void AtreidesMentat::draw_mouth()
{
    drawMentatTexture(gfxmentat->getTexture(ATR_MOUTH01 + iMentatMouth), kAtreidesMentatHdLayout.mouth);
}
