#pragma once

#include "debug/UiAuditArguments.hpp"

#include <string>

class cGame;
class cGameState;
struct SDL_Renderer;

namespace uiaudit {

struct Rect {
    int x;
    int y;
    int w;
    int h;
};

void recordText(const std::string &text, int x, int y, int w, int h, const Rect *box = nullptr);
void recordGui(const char *type, int x, int y, int w, int h);
void recordClick(const char *name, int x, int y, int w, int h);

class BoxScope {
public:
    BoxScope(int x, int y, int w, int h);
    ~BoxScope();
    BoxScope(const BoxScope &) = delete;
    BoxScope &operator=(const BoxScope &) = delete;
};

bool handleEarlyExit(int &exitCode);
void onSetupDone(cGame &game);
void beginFrame(cGame &game);
void onFramePresented(cGame &game);
bool failed();

}

class UiAuditAccess {
public:
    static int state(const cGame &game);
    static const cGameState *currentState(const cGame &game);
    static SDL_Renderer *renderer(cGame &game);
    static int renderScale(const cGame &game);
    static int worldScale(const cGame &game);
    static void setState(cGame &game, int state);
    static void freezeClock(cGame &game);
    static void resumeClock(cGame &game);
    static bool notFadingOut(const cGame &game);
};
