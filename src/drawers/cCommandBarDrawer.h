#pragma once

#include "controls/eKeyAction.h"
#include "controls/sMouseEvent.h"
#include "utils/Color.hpp"
#include "utils/cPoint.h"
#include "utils/cRectangle.h"

#include <string>
#include <vector>

class cEventEmitter;
class cGameObjectContext;
class cGameSettings;
class cKeyboard;
class cPlayer;
class cTextDrawer;
class GameContext;
class SDLDrawer;
class Texture;
struct sGameServices;

class cCommandBarDrawer {
    friend class UiAuditAccess;
public:
    explicit cCommandBarDrawer(GameContext *ctx, cPlayer *player, sGameServices *services);
    ~cCommandBarDrawer();

    void draw();
    void onNotifyMouseEvent(const s_MouseEvent &event);
    void setPlayer(cPlayer *player);

    [[nodiscard]] bool isMouseOver(const cPoint &point) const;

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
    [[nodiscard]] std::string getKeyLabel(eKeyAction action) const;

    GameContext *m_ctx;
    cPlayer *m_player;
    SDLDrawer *m_sdlDrawer;
    cGameSettings *m_settings;
    cGameObjectContext *m_objects;
    cEventEmitter *m_eventEmitter;
    cKeyboard *m_keyboard;
    cTextDrawer *m_keyTextDrawer;
    Texture *m_commandBarTexture;
    Texture *m_disabledCommandBarTexture;
    cRectangle m_panelRect;
    std::vector<Button> m_buttons;
    int m_hoveredButton;
};
