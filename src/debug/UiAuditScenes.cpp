#include "debug/UiAuditScenes.hpp"

#include "game/cGame.h"
#include "debug/UiAudit.hpp"
#include "include/eGameState.h"

namespace uiaudit {

namespace {

struct GroupScreen {
    const char *group;
    const char *state;
    const char *screen;
};

const GroupScreen kGroupScreens[] = {
    {"main-menu", "GAME_MENU", "cMainMenuState"},
};

Scene scene(const char *id, const char *group, const char *house, const char *readiness,
            bool (*prepare)(cGame &), bool (*ready)(cGame &) = nullptr, int settleFrames = 2)
{
    Scene result{id, group, "", "", house, false, false, false, false, 0, 0, readiness, settleFrames, prepare, ready};
    for (const GroupScreen &entry : kGroupScreens) {
        if (std::string(entry.group) == group) {
            result.state = entry.state;
            result.screen = entry.screen;
        }
    }
    return result;
}

bool prepareMainMenu(cGame &game)
{
    UiAuditAccess::setState(game, GAME_MENU);
    return true;
}

const std::vector<Scene> g_catalog = {
    scene("main-menu", "main-menu", "", "StateSettled", prepareMainMenu),
};

}

const std::vector<Scene> &catalog()
{
    return g_catalog;
}

const Scene *findScene(const std::string &id)
{
    for (const Scene &scene : g_catalog) {
        if (scene.id == id) {
            return &scene;
        }
    }
    return nullptr;
}

}
