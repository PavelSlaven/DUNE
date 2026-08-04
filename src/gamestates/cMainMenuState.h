#pragma once

#include "cGameState.h"
#include "controls/cKeyboardEvent.h"
#include "drawers/cTextDrawer.h"
#include "gui/GuiButton.h"
#include "gui/GuiWindow.h"
#include "sMouseEvent.h"

#include <memory>
#include <string_view>

class Texture;
class cGame;
class SaveSlotsDialog;

class cMainMenuState : public cGameState {
public:
    explicit cMainMenuState(cGame &theGame, GameContext* ctx);
    ~cMainMenuState() override;

    void thinkFast() override;
    void draw() const override;

    void onNotifyMouseEvent(const s_MouseEvent &event) override;
    void onNotifyKeyboardEvent(const cKeyboardEvent &event) override;
    void onTextInput(std::string_view text) override;

    eGameStateType getType() override;

private:
    void buildClassicMenu();
    void buildHdMenu();
    void drawHdBackground() const;

    int logoX;
    int logoY;

    int mainMenuFrameX;
    int mainMenuFrameY;
    int mainMenuWidth;
    int mainMenuHeight;

    cTextDrawer* m_textDrawer=nullptr;
    cTextDrawer* m_metaTextDrawer=nullptr;
    cRectangle sdl2power;
    cRectangle m_logoRect;

    GuiWindow *gui_window;
    GuiButton *gui_btn_credits;

    Texture *bmp_D2TM_Title;
    Texture *m_hdMenuBackground = nullptr;
    Texture *m_hdMenuLogo = nullptr;
    Texture *backGroundDebug = nullptr;
    std::unique_ptr<SaveSlotsDialog> m_saveDialog;
    bool m_hdLayout = false;
};
