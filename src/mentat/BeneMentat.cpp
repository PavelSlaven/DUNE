#include "BeneMentat.h"

#include "data/gfxmentat.h"
#include "d2tmc.h"
#include "player/cPlayer.h"
#include "drawers/SDLDrawer.hpp"
#include "utils/Graphics.hpp"
#include "utils/Localization.hpp"
#include "drawers/cTextDrawer.h"
#include <SDL2/SDL_ttf.h>
#include "gui/GuiButton.h"
#include "context/GameContext.hpp"
#include <algorithm>
#include <cmath>
#include <iostream>

BeneMentat::BeneMentat(GameContext* ctx) : AbstractMentat(ctx, false, true)
{
    iBackgroundFrame = MENTATM;
    if (m_adaptiveHdLayout) {
        // Match the two inset recesses painted into the HD background.  The
        // classic 154x46 button bitmaps are wider and start too low here.
        leftButton = new cRectangle(baseRect(336, 405, 112, 49));
        rightButton = new cRectangle(baseRect(492, 405, 112, 49));
    }
    else {
        buildLeftButton(gfxmentat->getTexture(BTN_NO), 293, 423);
        buildRightButton(gfxmentat->getTexture(BTN_YES), 466, 423);
    }

    auto leftBuilder = GuiButtonBuilder()
            .withRect(*leftButton)        
            .withLabel(localization::text("No", "Нет"))
            .withTextDrawer(m_textDrawer)
            .withTextScale(m_adaptiveHdLayout ? HD_BUTTON_TEXT_SCALE : 1.0F)
            .withTheme(m_adaptiveHdLayout ? GuiTheme::Remaster() : GuiTheme::Light())
            .withKind(m_adaptiveHdLayout ? GuiRenderKind::TRANSPARENT_WITHOUT_BORDER : GuiRenderKind::WITH_TEXTURE)
            .onClick([]() {
                logbook("cNoButtonCommand::execute()");
                // head back to choose house
                players[HUMAN].setHouse(GENERALHOUSE);
                game.setNextStateToTransitionTo(GAME_SELECT_HOUSE);
                game.initiateFadingOut();
            });
    if (!m_adaptiveHdLayout) {
        leftBuilder.withTexture(gfxmentat->getTexture(BTN_NO));
    }
    leftGuiButton = leftBuilder.build();

    auto rightBuilder = GuiButtonBuilder()
            .withRect(*rightButton)        
            .withLabel(localization::text("Yes", "Да"))
            .withTextDrawer(m_textDrawer)
            .withTextScale(m_adaptiveHdLayout ? HD_BUTTON_TEXT_SCALE : 1.0F)
            .withTheme(m_adaptiveHdLayout ? GuiTheme::Remaster() : GuiTheme::Light())
            .withKind(m_adaptiveHdLayout ? GuiRenderKind::TRANSPARENT_WITHOUT_BORDER : GuiRenderKind::WITH_TEXTURE)
            .onClick([this]() {
                logbook("cYesButtonCommand::execute()");
                game.setNextStateToTransitionTo(GAME_BRIEFING);
                game.m_mission = 1; // first mission
                game.m_region  = 1; // and the first "region" so to speak
                game.missionInit();
                players[HUMAN].setHouse(this->getHouse());
               game.initiateFadingOut();});
    if (!m_adaptiveHdLayout) {
        rightBuilder.withTexture(gfxmentat->getTexture(BTN_YES));
    }
    rightGuiButton = rightBuilder.build();
}

void BeneMentat::think()
{
    // think like base class
    AbstractMentat::think();
}

void BeneMentat::draw()
{
    AbstractMentat::draw();

    // when not speaking, draw 'do you wish to join house x'
    if (state == AWAITING_RESPONSE) {
        std::string houseName;
        switch (house) {
            case ATREIDES: houseName = localization::text("Atreides", "Атрейдес"); break;
            case HARKONNEN: houseName = localization::text("Harkonnen", "Харконнен"); break;
            case ORDOS: houseName = localization::text("Ordos", "Ордос"); break;
            default: houseName = cPlayer::getHouseNameForId(house); break;
        }
        std::string msg = localization::format(
            "Do you wish to join House {}?",
            "Желаете вступить в Дом {}?",
            houseName);
        if (m_adaptiveHdLayout) {
            const float textScale = std::clamp(m_uiScale, 1.35F, 1.90F);
            const int horizontalMargin = static_cast<int>(std::lround(18.0F * m_uiScale));
            m_textDrawer->drawTextScaledCenteredInBox(
                msg,
                cRectangle(
                    offsetX + horizontalMargin,
                    baseY(3),
                    m_panelWidth - horizontalMargin * 2,
                    static_cast<int>(std::lround(49.0F * m_uiScale))
                ),
                textScale,
                Color{255, 226, 165,255}
            );
        }
        else {
            m_textDrawer->drawText(baseX(18), baseY(17) + 1, Color{0, 0, 0,255}, msg);
            m_textDrawer->drawText(baseX(17), baseY(17), Color{255, 214, 137,255}, msg);
        }
    }
}

void BeneMentat::draw_other()
{
}

void BeneMentat::draw_eyes()
{
    drawMentatTexture(
        gfxmentat->getTexture(BEN_EYES01+ iMentatEyes),
        m_adaptiveHdLayout ? 96 : 128,
        m_adaptiveHdLayout ? 180 : 240
    );
}

void BeneMentat::draw_mouth()
{
    drawMentatTexture(
        gfxmentat->getTexture(BEN_MOUTH01+ iMentatMouth),
        m_adaptiveHdLayout ? 100 : 112,
        m_adaptiveHdLayout ? 210 : 272
    );
}
