#include "HarkonnenMentat.h"
#include "d2tmc.h"
#include "data/gfxmentat.h"
#include "drawers/SDLDrawer.hpp"
#include "utils/Graphics.hpp"
#include "utils/Localization.hpp"
#include "gui/GuiButton.h"
#include "context/GameContext.hpp"
#include <algorithm>

HarkonnenMentat::HarkonnenMentat(GameContext* ctx, bool allowMissionSelect) : AbstractMentat(ctx, allowMissionSelect, true)
{
    iBackgroundFrame = MENTATH;
    if (m_adaptiveHdLayout) {
        leftButton = new cRectangle(baseRect(313, 397, 148, 59));
        rightButton = new cRectangle(baseRect(479, 397, 139, 59));
    }
    else {
        buildLeftButton(gfxmentat->getTexture(BTN_REPEAT), 293, 423);
        buildRightButton(gfxmentat->getTexture(BTN_PROCEED), 466, 423);
    }
    auto leftBuilder = GuiButtonBuilder()
            .withRect(*leftButton)        
            .withLabel(localization::text("Repeat", "Повторить"))
            .withTextDrawer(m_textDrawer)
            .withTextScale(m_adaptiveHdLayout ? HD_BUTTON_TEXT_SCALE : 1.0F)
            .withTheme(m_adaptiveHdLayout ? GuiTheme::Remaster() : GuiTheme::Light())
            .withKind(m_adaptiveHdLayout ? GuiRenderKind::TRANSPARENT_WITHOUT_BORDER : GuiRenderKind::WITH_TEXTURE)
            .onClick([this]() {this->resetSpeak();});
    if (!m_adaptiveHdLayout) leftBuilder.withTexture(gfxmentat->getTexture(BTN_REPEAT));
    leftGuiButton = leftBuilder.build();

    auto rightBuilder = GuiButtonBuilder()
            .withRect(*rightButton)        
            .withLabel(localization::text("Next", "Далее"))
            .withTextDrawer(m_textDrawer)
            .withTextScale(m_adaptiveHdLayout ? HD_BUTTON_TEXT_SCALE : 1.0F)
            .withTheme(m_adaptiveHdLayout ? GuiTheme::Remaster() : GuiTheme::Light())
            .withKind(m_adaptiveHdLayout ? GuiRenderKind::TRANSPARENT_WITHOUT_BORDER : GuiRenderKind::WITH_TEXTURE)
            .onClick([this]() {
                logbook("cYesButtonCommand::execute()");
                game.execute(*this);});
    if (!m_adaptiveHdLayout) rightBuilder.withTexture(gfxmentat->getTexture(BTN_YES));
    rightGuiButton = rightBuilder.build();
    harmonizeHdButtonTextScale();
}

void HarkonnenMentat::think()
{
    // think like base class
    AbstractMentat::think();
}

void HarkonnenMentat::draw()
{
    AbstractMentat::draw();
}

void HarkonnenMentat::draw_other()
{
}

void HarkonnenMentat::draw_eyes()
{
    if (m_adaptiveHdLayout) {
        drawMentatTexture(gfxmentat->getTexture(HAR_EYES01 + iMentatEyes), 96, 180);
    }
    else {
        renderDrawer->renderSprite(gfxmentat->getTexture(HAR_EYES01 + iMentatEyes), offsetX + 64, offsetY + 256);
    }
}

void HarkonnenMentat::draw_mouth()
{
    if (m_adaptiveHdLayout) {
        drawMentatTexture(gfxmentat->getTexture(HAR_MOUTH01 + iMentatMouth), 100, 210);
    }
    else {
        renderDrawer->renderSprite(gfxmentat->getTexture(HAR_MOUTH01 + iMentatMouth), offsetX + 64, offsetY + 288);
    }
}
