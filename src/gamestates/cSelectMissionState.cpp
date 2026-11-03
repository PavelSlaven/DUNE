#include "cSelectMissionState.h"
#include "context/GameContext.hpp"
#include "d2tmc.h"
#include "config.h"
#include "drawers/SDLDrawer.hpp"
#include "gui/GuiButton.h"
#include "gui/GuiWindow.h"
#include "drawers/SDLDrawer.hpp"
#include "include/Texture.hpp"
#include "utils/HdUiTextureLoader.hpp"
#include "utils/Localization.hpp"

#include <algorithm>


cSelectMissionState::cSelectMissionState(cGame &theGame, GameContext* ctx, int prevState) :
    cGameState(theGame, ctx),
    m_textDrawer(ctx->getTextContext()->getMenuTextDrawer())
{
    m_hdBackground = loadHdUiTexture(
        "main_menu_background.png",
        m_game.getGraphicsDensity(),
        "HD mission selection"
    );

    const int mainMenuWidth = std::clamp(
        m_game.m_screenW - 64,
        440,
        600
    );
    const int mainMenuHeight = std::min(
        m_game.m_screenH - 64,
        500
    );
    const int mainMenuFrameX = (m_game.m_screenW - mainMenuWidth) / 2;
    const int mainMenuFrameY = (m_game.m_screenH - mainMenuHeight) / 2;

    const int margin = 8;
    const int buttonHeight = std::max(36, m_textDrawer->getFontHeight() + 10);
    const int buttonWidth = mainMenuWidth - margin * 2;
    const GuiTheme theme = GuiTheme::Remaster();
    const GuiRenderKind kind = GuiRenderKind::REMASTER_BUTTON;

    const cRectangle &window = cRectangle(mainMenuFrameX, mainMenuFrameY, mainMenuWidth, mainMenuHeight);
    gui_window = new GuiWindow(window, m_textDrawer);
    gui_window->setTheme(theme);

    // Title
    gui_window->setTitle("Dune II - The Maker - version " + D2TM_VERSION);


    // QUIT game
    int width = buttonWidth;

    int y = 42;
    for (int i = 2; i <= 9; i++) {
        const cRectangle &rect = gui_window->getRelativeRect(margin, y, width, buttonHeight);
        GuiButton *btnMission = GuiButtonBuilder()
            .withRect(rect)        
            .withLabel(localization::format(
                "Mission {}", "Миссия {}", i))
            .withTextDrawer(m_textDrawer)    
            .withTheme(theme)
            .withKind(kind)
            .onClick([this,i]() {
                m_game.jumpToSelectYourNextConquestMission(i);
                m_game.setNextStateToTransitionTo(GAME_REGION);
                m_game.initiateFadingOut();})
            .build();   
        gui_window->addGuiObject(btnMission);

        y += buttonHeight + margin;
    }

    // BACK to where we came from
    int back = mainMenuHeight - (buttonHeight + margin);
    width = buttonWidth;
    const cRectangle &backRect = gui_window->getRelativeRect(margin, back, (width - margin), buttonHeight);
    GuiButton *gui_btn_Back = GuiButtonBuilder()
            .withRect(backRect)        
            .withLabel(localization::text("Back", "Назад"))
            .withTextDrawer(m_textDrawer)    
            .withTheme(theme)
            .withKind(kind)
            .onClick([this,prevState]() {
                m_game.setNextStateToTransitionTo(prevState);
            })
            .build();  
    gui_window->addGuiObject(gui_btn_Back);
}

cSelectMissionState::~cSelectMissionState()
{
    delete gui_window;
    delete m_hdBackground;
}

void cSelectMissionState::thinkFast()
{

}

void cSelectMissionState::draw() const
{
    renderDrawer->renderClearToColor(Color{10, 12, 14, 255});
    if (m_hdBackground) {
        const float sourceAspect =
            static_cast<float>(m_hdBackground->w) /
            std::max(1, m_hdBackground->h);
        const float screenAspect =
            static_cast<float>(m_game.m_screenW) /
            std::max(1, m_game.m_screenH);
        cRectangle destination;
        if (sourceAspect > screenAspect) {
            const int width = static_cast<int>(
                m_game.m_screenH * sourceAspect
            );
            destination = cRectangle(
                (m_game.m_screenW - width) / 2,
                0,
                width,
                m_game.m_screenH
            );
        }
        else {
            const int height = static_cast<int>(
                m_game.m_screenW / sourceAspect
            );
            destination = cRectangle(
                0,
                (m_game.m_screenH - height) / 2,
                m_game.m_screenW,
                height
            );
        }
        renderDrawer->renderStrechFullSprite(
            m_hdBackground,
            destination
        );
        renderDrawer->renderRectFillColor(
            0,
            0,
            m_game.m_screenW,
            m_game.m_screenH,
            Color{3, 6, 8, 150}
        );
    }

    gui_window->draw();

    // MOUSE
    m_game.getMouse()->draw();
}

void cSelectMissionState::onNotifyMouseEvent(const s_MouseEvent &event)
{
    gui_window->onNotifyMouseEvent(event);
}

eGameStateType cSelectMissionState::getType()
{
    return GAMESTATE_SELECT_MISSION;
}

void cSelectMissionState::onNotifyKeyboardEvent(const cKeyboardEvent &)
{
}
