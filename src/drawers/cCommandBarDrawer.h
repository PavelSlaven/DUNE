#pragma once

#include "sMouseEvent.h"
#include "utils/Color.hpp"
#include "utils/cRectangle.h"

#include <string>
#include <vector>

class cPlayer;
class cTextDrawer;
class GameContext;
class Texture;

class cCommandBarDrawer {
public:
    explicit cCommandBarDrawer(GameContext *ctx, cPlayer *player);
    ~cCommandBarDrawer();

    void draw();
    void onNotifyMouseEvent(const s_MouseEvent &event);
    void setPlayer(cPlayer *player);

    [[nodiscard]] bool isMouseOver(const cPoint &point) const;
    [[nodiscard]] int getTopY() const;

private:
    enum class Command {
        Move,
        Attack,
        Repair,
        Unload,
        Deploy,
        Rally,
        Release
    };

    struct Button {
        Command command;
        cRectangle rect;
        std::string label;
        std::string hotkey;
        bool enabled;
        bool active;
    };

    void rebuildLayout();
    void drawButton(const Button &button) const;
    void drawIcon(Command command, const cRectangle &rect, Color color) const;
    void execute(Command command);
    void executeUnload();
    void executeDeploy();
    void executeRelease();

    [[nodiscard]] bool hasAttackCapableUnit() const;
    [[nodiscard]] bool hasUnloadableHarvester() const;
    [[nodiscard]] bool hasSelectedMcv() const;

    GameContext *m_ctx;
    cPlayer *m_player;
    cTextDrawer *m_smallTextDrawer;
    cTextDrawer *m_keyTextDrawer;
    Texture *m_commandBarTexture;
    Texture *m_disabledCommandBarTexture;
    cRectangle m_panelRect;
    std::vector<Button> m_buttons;
    int m_hoveredButton;
};
