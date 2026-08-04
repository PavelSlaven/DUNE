#include "OrdosMentat.h"
#include "d2tmc.h"
#include "data/gfxmentat.h"
#include "drawers/SDLDrawer.hpp"
#include "utils/Graphics.hpp"
#include "utils/Localization.hpp"
#include "gui/GuiButton.h"
#include "context/GameContext.hpp"
#include <algorithm>

OrdosMentat::OrdosMentat(GameContext* ctx, bool allowMissionSelect) : AbstractMentat(ctx, allowMissionSelect, true)
{
    iBackgroundFrame = MENTATO;
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

void OrdosMentat::think()
{
    // think like base class
    AbstractMentat::think();
}

void OrdosMentat::draw()
{
    AbstractMentat::draw();
}

void OrdosMentat::draw_other()
{
}

void OrdosMentat::draw_eyes()
{
    if (m_adaptiveHdLayout) {
        drawMentatTexture(gfxmentat->getTexture(ORD_EYES01 + iMentatEyes), 48, 174);
    }
    else {
        renderDrawer->renderSprite(gfxmentat->getTexture(ORD_EYES01 + iMentatEyes), offsetX + 32, offsetY + 240);
    }
}

void OrdosMentat::draw_mouth()
{
    if (m_adaptiveHdLayout) {
        drawMentatTexture(gfxmentat->getTexture(ORD_MOUTH01 + iMentatMouth), 52, 207);
    }
    else {
        renderDrawer->renderSprite(gfxmentat->getTexture(ORD_MOUTH01 + iMentatMouth), offsetX + 31, offsetY + 270);
    }
}
