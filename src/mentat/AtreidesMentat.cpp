#include "AtreidesMentat.h"

#include "d2tmc.h"
#include "data/gfxmentat.h"
#include "drawers/SDLDrawer.hpp"
#include "utils/Graphics.hpp"
#include "utils/Localization.hpp"
#include "gui/GuiButton.h"
#include <iostream>
#include <algorithm>


AtreidesMentat::AtreidesMentat(GameContext* ctx, bool allowMissionSelect) : AbstractMentat(ctx, allowMissionSelect, true)
{
    iBackgroundFrame = MENTATA;
    if (m_adaptiveHdLayout) {
        // The remastered Atreides artwork has a narrower monitor than the
        // original mentat frame.  These coordinates keep every scene inside
        // the actual glass area and away from Cyril's portrait.
        m_movieWidth = 337;
        m_movieHeight = 205;
        movieTopleftX = baseX(265);
        movieTopleftY = baseY(114);

        // Match the two painted recesses in the remastered console.
        leftButton = new cRectangle(baseRect(342, 393, 124, 52));
        rightButton = new cRectangle(baseRect(482, 393, 110, 52));
    }
    else {
        buildLeftButton(gfxmentat->getTexture(BTN_REPEAT), 293, 423);
        buildRightButton(gfxmentat->getTexture(BTN_PROCEED), 466, 423);
    }

    auto leftBuilder = GuiButtonBuilder()
            .withRect(*leftButton)        
            .withLabel(localization::text("Repeat", "Повторить"))
            .withTextDrawer(m_textDrawer)
            .withTextScale(m_adaptiveHdLayout ? 0.85F : 1.0F)
            .withTheme(m_adaptiveHdLayout ? GuiTheme::Remaster() : GuiTheme::Light())
            .withKind(m_adaptiveHdLayout ? GuiRenderKind::TRANSPARENT_WITHOUT_BORDER : GuiRenderKind::WITH_TEXTURE)
            .onClick([this]() {this->resetSpeak();});
    if (!m_adaptiveHdLayout) leftBuilder.withTexture(gfxmentat->getTexture(BTN_REPEAT));
    leftGuiButton = leftBuilder.build();

    auto rightBuilder = GuiButtonBuilder()
            .withRect(*rightButton)        
            .withLabel(localization::text("Next", "Далее"))
            .withTextDrawer(m_textDrawer)
            .withTextScale(m_adaptiveHdLayout ? 0.85F : 1.0F)
            .withTheme(m_adaptiveHdLayout ? GuiTheme::Remaster() : GuiTheme::Light())
            .withKind(m_adaptiveHdLayout ? GuiRenderKind::TRANSPARENT_WITHOUT_BORDER : GuiRenderKind::WITH_TEXTURE)
            .onClick([this]() {
                logbook("cYesButtonCommand::execute()");
                game.execute(*this);});
    if (!m_adaptiveHdLayout) rightBuilder.withTexture(gfxmentat->getTexture(BTN_YES));
    rightGuiButton = rightBuilder.build();
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
    if (m_adaptiveHdLayout) {
        drawMentatTexture(gfxmentat->getTexture(ATR_EYES01 + iMentatEyes), 96, 180);
    }
    else {
        renderDrawer->renderSprite(gfxmentat->getTexture(ATR_EYES01 + iMentatEyes), offsetX + 80, offsetY + 241);
    }
}

void AtreidesMentat::draw_mouth()
{
    if (m_adaptiveHdLayout) {
        drawMentatTexture(gfxmentat->getTexture(ATR_MOUTH01 + iMentatMouth), 100, 210);
    }
    else {
        renderDrawer->renderSprite(gfxmentat->getTexture(ATR_MOUTH01 + iMentatMouth), offsetX + 80, offsetY + 273);
    }
}
