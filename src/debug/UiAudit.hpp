#pragma once

#include "debug/UiAuditArguments.hpp"
#include "include/eGameState.h"

#include <string>

class cGame;
class cGameState;
class cSideBarDrawer;
class cCommandBarDrawer;
struct SDL_Renderer;

namespace uiaudit {

enum GameKind {
    Hud,
    Music,
    Structure,
    ListBuild,
    ListInfantry,
    ListVehicles,
    ListStarport,
    ListPalace,
    ListUpgrades,
    RadarNone,
    RadarNoPower,
    PlaceAllowed,
    PlaceForbidden,
    GroupSelect,
    Messages,
    ItemHover,
    ScrollEnd,
    Rally,
    DamagedUnit,
    RepairMode,
    Harvester,
    Mcv,
    RadarDish,
    RefineryHarvester,
    FactoryPad
};

struct Rect {
    int x;
    int y;
    int w;
    int h;
};

void recordText(const std::string &text, int x, int y, int w, int h, const Rect *box = nullptr);
void recordGui(const char *type, int x, int y, int w, int h);
void recordArea(const char *name, int x, int y, int w, int h);
void recordClick(const char *name, int x, int y, int w, int h);
void recordCanvasClick(const char *name);
void dropClicksUnderModal();
void recordLabel(const char *kind, int obj, const char *type, int x, int y, int w, int h, const Rect &owner);
void recordUnitLabel(const char *kind, int obj, int unitType, int x, int y, int w, int h, const Rect &owner);
void beginLabelText();
void endLabelText(const char *kind, int obj, int unitType, const Rect &owner);

class BoxScope {
public:
    BoxScope(int x, int y, int w, int h);
    ~BoxScope();
    BoxScope(const BoxScope &) = delete;
    BoxScope &operator=(const BoxScope &) = delete;
};

void setVerticalClipText(bool enabled);
void recordCreditLine(const std::string &name, const std::string &text);

bool handleEarlyExit(int &exitCode);
void onSetupDone(cGame &game);
void beginFrame(cGame &game);
void onFramePresented(cGame &game);
bool failed();
void setHover(int x, int y);

}

class UiAuditAccess {
public:
    static int state(const cGame &game);
    static const cGameState *currentState(const cGame &game);
    static SDL_Renderer *renderer(cGame &game);
    static int renderScale(const cGame &game);
    static int worldScale(const cGame &game);
    static void setState(cGame &game, eGameState state);
    static void freezeClock(cGame &game);
    static void resumeClock(cGame &game);
    static bool notFadingOut(const cGame &game);
    static void setHouse(cGame &game, int house);
    static bool prepareMentatScene(cGame &game, int house, int kind);
    static bool mentatFreeze(cGame &game, bool awaiting);
    static bool prepareSkirmish(cGame &game, int variant);
    static bool optionsStatus(cGame &game);
    static bool optionsPage(cGame &game, int page);
    static bool resolutionDialog(cGame &game);
    static bool optionsBinding(cGame &game);
    static bool creditsScroll(cGame &game, int frame);
    static void recordCreditLines(cGame &game);
    static void regionOpen(cGame &game, int mission, bool jump);
    static int regionState(const cGame &game);
    static int regionScene(const cGame &game);
    static int regionSceneAlpha(const cGame &game);
    static bool hasMessage(const cGame &game);
    static bool mapViewport(const cGame &game, int &x, int &y, int &w, int &h);
    static void stopCameraEdgeMove(cGame &game);
    static void missionOutcome(cGame &game, bool victory);
    static void recordSidebarClicks(cSideBarDrawer &drawer);
    static void recordCommandBarClicks(cCommandBarDrawer &drawer);
    static bool enterPlaying(cGame &game, int house, int region);
    static bool openEditor(cGame &game, int bar);
    static bool placeLabelUnits(cGame &game, int unitType);
    static bool placeStructure(cGame &game, int edge);
    static bool prepareGameScreen(cGame &game, int house, int kind);
    static void writeSaves(cGame &game);
    static bool openMenuSaveDialog(cGame &game);
    static bool saveDialog(cGame &game, int action);
    static bool startSkirmish(cGame &game);
    static bool saveRoundTrip(cGame &game);
    static bool addFactoryPads(cGame &game);
};
