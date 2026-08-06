#include "AtreidesMentat.h"

#include "d2tmc.h"
#include "data/gfxmentat.h"
#include "drawers/SDLDrawer.hpp"
#include "utils/Graphics.hpp"
#include "utils/Localization.hpp"
#include "gui/GuiButton.h"
#include <iostream>
#include <algorithm>
#include <array>
#include <cmath>


AtreidesMentat::AtreidesMentat(GameContext* ctx, bool allowMissionSelect)
    : AbstractMentat(ctx, allowMissionSelect, true, 537, 4.0F)
{
    iBackgroundFrame = MENTATA;
    if (m_adaptiveHdLayout) {
        // The movie is deliberately larger than the glass.  A cached alpha
        // foreground keeps the monitor frame and Cyril's shoulder above it.
        m_movieClipX = 276;
        m_movieClipY = 115;
        m_movieClipWidth = 322;
        m_movieClipHeight = 219;
        m_movieWidth = 400;
        m_movieHeight = 243;
        movieTopleftX = baseX(234);
        movieTopleftY = baseY(95);

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

void AtreidesMentat::clearHdMovieOpening(Texture *background)
{
    if (!background) return;

    // The alpha opening follows the monitor glass but stops at Cyril's right
    // shoulder, leaving the portrait inside the single opaque foreground.
    struct EdgePoint {
        int y;
        int rightX;
    };
    static constexpr std::array<EdgePoint, 10> edge = {{
        {270, 273},
        {290, 273},
        {294, 275},
        {296, 285},
        {300, 289},
        {306, 293},
        {314, 297},
        {320, 303},
        {326, 308},
        {334, 314}
    }};

    const int openingRight = m_movieClipX + m_movieClipWidth;
    for (int y = m_movieClipY; y < m_movieClipY + m_movieClipHeight; ++y) {
        int openingLeft = m_movieClipX;
        for (std::size_t segment = 0; segment + 1 < edge.size(); ++segment) {
            const EdgePoint from = edge[segment];
            const EdgePoint to = edge[segment + 1];
            if (y < from.y || y >= to.y) continue;
            const double progress = static_cast<double>(y - from.y) / (to.y - from.y);
            const int portraitRight = static_cast<int>(std::lround(
                from.rightX + (to.rightX - from.rightX) * progress
            ));
            openingLeft = std::max(openingLeft, portraitRight + 1);
            break;
        }
        clearHdForegroundLayerRegion(
            background,
            openingLeft,
            y,
            openingRight - openingLeft,
            1
        );
    }
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
