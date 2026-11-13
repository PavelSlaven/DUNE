/**
 * @file SardaukarMentat.cpp
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

#include "SardaukarMentat.h"
#include "include/gfxmentat.h"
#include "drawers/SDLDrawer.hpp"
#include "utils/Graphics.hpp"
#include "utils/common.h"
#include "utils/Log.h"
#include "gui/GuiButton.h"
#include "context/GameContext.hpp"
#include "game/GameStateTransition.hpp"
#include "game/MentatFlow.hpp"
#include "include/cAssert.h"
#include "utils/Localization.hpp"

SardaukarMentat::SardaukarMentat(GameContext* ctx, cGameSettings* settings, GameStateTransition* stateTransitions, MentatFlow* mentatFlow, bool allowMissionSelect) : AbstractMentat(ctx, settings, stateTransitions, mentatFlow, allowMissionSelect)
{
    d2tm_assert(ctx != nullptr);
    d2tm_assert(m_mentatFlow != nullptr);
    iBackgroundFrame = MENTATS;
    buildHdButtons(kHarkonnenMentatHdButtons);
    leftGuiButton = GuiButtonBuilder()
            .withRect(*leftButton)        
            .withLabel(localization::text("Repeat", "Повторить"))
            .withTextDrawer(m_textDrawer)
            .withRenderer(m_sdlDrawer)
            .withKind(GuiRenderKind::TRANSPARENT_WITHOUT_BORDER)
            .onClick([this]() {this->resetSpeak();})
            .build();

    rightGuiButton = GuiButtonBuilder()
            .withRect(*rightButton)        
            .withLabel(localization::text("Next", "Далее"))
            .withTextDrawer(m_textDrawer)
            .withRenderer(m_sdlDrawer)
            .withKind(GuiRenderKind::TRANSPARENT_WITHOUT_BORDER)
            .onClick([this]() {
                Logger::info(COMP_NONE, "cYesButtonCommand::changeStateFromMentat", "called");
                m_mentatFlow->leave();})
            .build();
}

void SardaukarMentat::think()
{
    // think like base class
    AbstractMentat::think();
}

void SardaukarMentat::draw()
{
    AbstractMentat::draw();
}

void SardaukarMentat::draw_other()
{
}

void SardaukarMentat::draw_eyes()
{
    //m_sdlDrawer->renderSprite(gfxmentat->getTexture(ORD_EYES01+ iMentatEyes), offsetX + 32, offsetY + 240);
}

void SardaukarMentat::draw_mouth()
{
    //m_sdlDrawer->renderSprite(gfxmentat->getTexture(ORD_MOUTH01+ iMentatMouth), offsetX + 31, offsetY + 270);
}