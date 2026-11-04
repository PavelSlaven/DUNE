#include "OrdosMentat.h"
#include "d2tmc.h"
#include "data/gfxmentat.h"
#include "drawers/SDLDrawer.hpp"
#include "utils/Graphics.hpp"
#include "utils/Localization.hpp"
#include "gui/GuiButton.h"
#include "context/GameContext.hpp"
#include <algorithm>
#include <array>
#include <cmath>

OrdosMentat::OrdosMentat(GameContext* ctx, bool allowMissionSelect) : AbstractMentat(ctx, allowMissionSelect)
{
    iBackgroundFrame = MENTATO;
    leftButton = new cRectangle(baseRect(313, 397, 148, 59));
    rightButton = new cRectangle(baseRect(479, 397, 139, 59));
    auto leftBuilder = GuiButtonBuilder()
            .withRect(*leftButton)        
            .withLabel(localization::text("Repeat", "Повторить"))
            .withTextDrawer(m_textDrawer)
            .withTextScale(HD_BUTTON_TEXT_SCALE)
            .withTheme(GuiTheme::Remaster())
            .withKind(GuiRenderKind::TRANSPARENT_WITHOUT_BORDER)
            .onClick([this]() {this->resetSpeak();});
    leftGuiButton = leftBuilder.build();

    auto rightBuilder = GuiButtonBuilder()
            .withRect(*rightButton)        
            .withLabel(localization::text("Next", "Далее"))
            .withTextDrawer(m_textDrawer)
            .withTextScale(HD_BUTTON_TEXT_SCALE)
            .withTheme(GuiTheme::Remaster())
            .withKind(GuiRenderKind::TRANSPARENT_WITHOUT_BORDER)
            .onClick([this]() {
                logbook("cYesButtonCommand::execute()");
                game.execute(*this);});
    rightGuiButton = rightBuilder.build();
    harmonizeHdButtonTextScale();
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

void OrdosMentat::clearHdMovieOpening(Texture *background)
{
    if (!background) return;

    // The restored Ordos shoulder passes in front of the monitor.  Follow its
    // painted edge so the movie stays behind the garment without leaving a
    // vertical cut or preserving a rectangle of the static monitor image.
    struct EdgePoint {
        int y;
        int rightX;
    };
    static constexpr std::array<EdgePoint, 11> shoulderEdge = {{
        {273, 213},
        {276, 218},
        {280, 225},
        {285, 232},
        {290, 239},
        {295, 243},
        {300, 247},
        {305, 250},
        {310, 254},
        {315, 257},
        {319, 261}
    }};

    constexpr int cornerHeight = 14;
    const int bottom = m_movieClipY + m_movieClipHeight;

    for (int y = m_movieClipY; y < bottom; ++y) {
        int inset = 0;
        if (y < m_movieClipY + cornerHeight) {
            inset = m_movieClipY + cornerHeight - y;
        }
        else if (y >= bottom - cornerHeight) {
            inset = y - (bottom - cornerHeight) + 1;
        }

        int openingLeft = m_movieClipX + inset;
        const int openingRight = m_movieClipX + m_movieClipWidth - inset;
        int portraitRight = -1;
        for (std::size_t segment = 0; segment + 1 < shoulderEdge.size(); ++segment) {
            const EdgePoint from = shoulderEdge[segment];
            const EdgePoint to = shoulderEdge[segment + 1];
            if (y < from.y || y >= to.y) continue;
            const double progress = static_cast<double>(y - from.y) / (to.y - from.y);
            portraitRight = static_cast<int>(std::lround(
                from.rightX + (to.rightX - from.rightX) * progress
            ));
            break;
        }
        openingLeft = std::max(openingLeft, portraitRight + 1);

        clearHdForegroundLayerRegion(
            background,
            openingLeft,
            y,
            openingRight - openingLeft,
            1
        );
    }
}

void OrdosMentat::draw_eyes()
{
    drawMentatTexture(gfxmentat->getTexture(ORD_EYES01 + iMentatEyes), 48, 174);
}

void OrdosMentat::draw_mouth()
{
    drawMentatTexture(gfxmentat->getTexture(ORD_MOUTH01 + iMentatMouth), 52, 207);
}
