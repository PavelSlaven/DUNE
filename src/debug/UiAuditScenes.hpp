#pragma once

#include <string>
#include <vector>

class cGame;

namespace uiaudit {

struct Scene {
    const char *id;
    const char *group;
    const char *state;
    const char *screen;
    const char *house;
    bool hud;
    bool gameScreen;
    bool hdOnly;
    bool hover;
    int hoverX;
    int hoverY;
    const char *readiness;
    int settleFrames;
    bool (*prepare)(cGame &game);
    bool (*ready)(cGame &game);
};

const std::vector<Scene> &catalog();
const Scene *findScene(const std::string &id);

}
