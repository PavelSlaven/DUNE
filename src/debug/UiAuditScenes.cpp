#include "debug/UiAuditScenes.hpp"

#include "game/cGame.h"
#include "debug/UiAudit.hpp"
#include "include/definitions.h"
#include "include/eGameState.h"
#include "gamestates/cSelectYourNextConquestState.h"

namespace uiaudit {

namespace {

int g_step = 0;
int g_wait = 0;

void resetSteps()
{
    g_step = 0;
    g_wait = 0;
}

bool pause(int frames)
{
    if (++g_wait > frames) {
        g_wait = 0;
        return true;
    }
    return false;
}

const char *const kFixedGameFrames = "FixedFrames(5, no readiness flag)";

Scene onGameScreen(Scene value, bool hovering)
{
    value.gameScreen = true;
    value.hover = hovering;
    return value;
}

struct GroupScreen {
    const char *group;
    const char *state;
    const char *screen;
};

const GroupScreen kGroupScreens[] = {
    {"main-menu", "GAME_MENU", "cMainMenuState"},
    {"region", "GAME_REGION", "cSelectYourNextConquestState"},
    {"choose-house", "GAME_SELECT_HOUSE", "cChooseHouseState"},
    {"select-mission", "GAME_MISSIONSELECT", "cSelectMissionState"},
    {"tellhouse", "GAME_TELLHOUSE", "BeneMentat"},
    {"options-menu", "GAME_OPTIONS", "cOptionsState"},
    {"credits", "GAME_CREDITS", "cCreditsState"},
    {"skirmish-setup", "GAME_SETUPSKIRMISH", "cSetupSkirmishState"},
    {"game-playing", "GAME_PLAYING", "cGamePlaying"},
    {"options-game", "GAME_OPTIONS", "cOptionsState"},
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

Scene withScreen(Scene value, const char *state, const char *screen)
{
    value.state = state;
    value.screen = screen;
    return value;
}

Scene hdOnly(Scene value)
{
    value.hdOnly = true;
    return value;
}

template <int House, int Kind>
bool prepareMentat(cGame &game)
{
    resetSteps();
    return UiAuditAccess::prepareMentatScene(game, House, Kind);
}

template <int Variant>
bool prepareSkirmishSetup(cGame &game)
{
    resetSteps();
    return UiAuditAccess::prepareSkirmish(game, Variant);
}

template <bool Victory>
bool prepareOutcome(cGame &game)
{
    resetSteps();
    return UiAuditAccess::enterPlaying(game, ATREIDES, 1);
}

template <bool Victory>
bool readyOutcome(cGame &game)
{
    if (g_step == 0) {
        if (!pause(3)) {
            return false;
        }
        UiAuditAccess::missionOutcome(game, Victory);
        g_step = 1;
        return false;
    }
    return pause(3);
}

bool prepareMainMenu(cGame &game)
{
    UiAuditAccess::setState(game, GAME_MENU);
    return true;
}

bool prepareChooseHouse(cGame &game)
{
    UiAuditAccess::setState(game, GAME_SELECT_HOUSE);
    return true;
}

template <int House>
bool prepareSelectMission(cGame &game)
{
    UiAuditAccess::setHouse(game, House);
    UiAuditAccess::setState(game, GAME_MISSIONSELECT);
    return true;
}

template <int House, bool Awaiting>
bool prepareTellHouse(cGame &game)
{
    resetSteps();
    UiAuditAccess::setHouse(game, House);
    UiAuditAccess::setState(game, GAME_TELLHOUSE);
    return true;
}

template <bool Awaiting>
bool readyMentatFrozen(cGame &game)
{
    if (g_step == 0) {
        if (!UiAuditAccess::mentatFreeze(game, Awaiting)) {
            return false;
        }
        g_step = 1;
        g_wait = 0;
        return false;
    }
    return pause(3);
}

template <int Variant>
bool prepareOptionsMenu(cGame &game)
{
    resetSteps();
    UiAuditAccess::setState(game, GAME_MENU);
    return true;
}

template <int Variant>
bool readyOptionsMenu(cGame &game)
{
    switch (g_step) {
        case 0:
            UiAuditAccess::setState(game, GAME_OPTIONS);
            g_step = 1;
            g_wait = 0;
            return false;
        case 1:
            if (!pause(4)) {
                return false;
            }
            if (Variant == 1) { UiAuditAccess::optionsStatus(game); }
            g_step = 2;
            return false;
        default:
            return pause(4);
    }
}

bool prepareCredits(cGame &game)
{
    resetSteps();
    UiAuditAccess::setState(game, GAME_CREDITS);
    setVerticalClipText(true);
    return true;
}

template <int Frame>
bool readyCredits(cGame &game)
{
    if (g_step == 0) {
        if (!UiAuditAccess::creditsScroll(game, Frame)) {
            return false;
        }
        g_step = 1;
        g_wait = 0;
        return false;
    }
    return pause(3);
}

template <int House, int Mission, bool Jump>
bool prepareRegion(cGame &game)
{
    resetSteps();
    UiAuditAccess::setHouse(game, House);
    UiAuditAccess::regionOpen(game, Mission, Jump);
    return true;
}

template <int SceneIndex>
bool readyRegionIntro(cGame &game)
{
    if (UiAuditAccess::regionScene(game) != SceneIndex || UiAuditAccess::regionSceneAlpha(game) < 128) {
        return false;
    }
    // On a large canvas a frame advances the fade by tens of steps, so the last scene would pass before the pause ends.
    return pause(3) || UiAuditAccess::regionSceneAlpha(game) >= 160;
}

bool readyRegionSelect(cGame &game)
{
    if (UiAuditAccess::regionState(game) != REGSTATE_SELECT_NEXT_CONQUEST) {
        return false;
    }
    return pause(3);
}

bool readyRegionConquer(cGame &game)
{
    if (UiAuditAccess::regionState(game) != REGSTATE_CONQUER_REGIONS || !UiAuditAccess::hasMessage(game)) {
        return false;
    }
    return true;
}

bool prepareGameOptions(cGame &game)
{
    resetSteps();
    return UiAuditAccess::enterPlaying(game, ATREIDES, 1);
}

template <int Type>
bool prepareUnitLabels(cGame &game)
{
    resetSteps();
    return UiAuditAccess::enterPlaying(game, ATREIDES, 1) && UiAuditAccess::placeLabelUnits(game, Type);
}

template <int Edge>
bool prepareStructureLabel(cGame &game)
{
    resetSteps();
    return UiAuditAccess::enterPlaying(game, ATREIDES, 1) && UiAuditAccess::placeStructure(game, Edge);
}

const std::vector<Scene> g_catalog = {
    scene("main-menu", "main-menu", "", "StateSettled", prepareMainMenu),
    scene("region-atreides-intro-1", "region", "atreides", "RegionIntroScene", prepareRegion<ATREIDES, 1, false>, readyRegionIntro<1>),
    scene("region-atreides-intro-2", "region", "atreides", "RegionIntroScene", prepareRegion<ATREIDES, 1, false>, readyRegionIntro<2>),
    scene("region-atreides-intro-3", "region", "atreides", "RegionIntroScene", prepareRegion<ATREIDES, 1, false>, readyRegionIntro<3>),
    scene("region-atreides-conquer-3", "region", "atreides", "RegionConquerMessage", prepareRegion<ATREIDES, 3, true>, readyRegionConquer, 1),
    scene("region-atreides-conquer-5", "region", "atreides", "RegionConquerMessage", prepareRegion<ATREIDES, 5, true>, readyRegionConquer, 1),
    scene("region-atreides-conquer-7", "region", "atreides", "RegionConquerMessage", prepareRegion<ATREIDES, 7, true>, readyRegionConquer, 1),
    scene("region-atreides-conquer-9", "region", "atreides", "RegionConquerMessage", prepareRegion<ATREIDES, 9, true>, readyRegionConquer, 1),
    scene("region-atreides-select-2", "region", "atreides", "RegionStateSelect", prepareRegion<ATREIDES, 2, true>, readyRegionSelect),
    scene("region-atreides-select-3", "region", "atreides", "RegionStateSelect", prepareRegion<ATREIDES, 3, true>, readyRegionSelect),
    scene("region-atreides-select-4", "region", "atreides", "RegionStateSelect", prepareRegion<ATREIDES, 4, true>, readyRegionSelect),
    scene("region-atreides-select-5", "region", "atreides", "RegionStateSelect", prepareRegion<ATREIDES, 5, true>, readyRegionSelect),
    scene("region-atreides-select-6", "region", "atreides", "RegionStateSelect", prepareRegion<ATREIDES, 6, true>, readyRegionSelect),
    scene("region-atreides-select-7", "region", "atreides", "RegionStateSelect", prepareRegion<ATREIDES, 7, true>, readyRegionSelect),
    scene("region-atreides-select-8", "region", "atreides", "RegionStateSelect", prepareRegion<ATREIDES, 8, true>, readyRegionSelect),
    scene("region-atreides-select-9", "region", "atreides", "RegionStateSelect", prepareRegion<ATREIDES, 9, true>, readyRegionSelect),
    scene("region-harkonnen-intro-1", "region", "harkonnen", "RegionIntroScene", prepareRegion<HARKONNEN, 1, false>, readyRegionIntro<1>),
    scene("region-harkonnen-intro-2", "region", "harkonnen", "RegionIntroScene", prepareRegion<HARKONNEN, 1, false>, readyRegionIntro<2>),
    scene("region-harkonnen-intro-3", "region", "harkonnen", "RegionIntroScene", prepareRegion<HARKONNEN, 1, false>, readyRegionIntro<3>),
    scene("region-harkonnen-conquer-3", "region", "harkonnen", "RegionConquerMessage", prepareRegion<HARKONNEN, 3, true>, readyRegionConquer, 1),
    scene("region-harkonnen-conquer-5", "region", "harkonnen", "RegionConquerMessage", prepareRegion<HARKONNEN, 5, true>, readyRegionConquer, 1),
    scene("region-harkonnen-conquer-7", "region", "harkonnen", "RegionConquerMessage", prepareRegion<HARKONNEN, 7, true>, readyRegionConquer, 1),
    scene("region-harkonnen-conquer-9", "region", "harkonnen", "RegionConquerMessage", prepareRegion<HARKONNEN, 9, true>, readyRegionConquer, 1),
    scene("region-harkonnen-select-2", "region", "harkonnen", "RegionStateSelect", prepareRegion<HARKONNEN, 2, true>, readyRegionSelect),
    scene("region-harkonnen-select-3", "region", "harkonnen", "RegionStateSelect", prepareRegion<HARKONNEN, 3, true>, readyRegionSelect),
    scene("region-harkonnen-select-4", "region", "harkonnen", "RegionStateSelect", prepareRegion<HARKONNEN, 4, true>, readyRegionSelect),
    scene("region-harkonnen-select-5", "region", "harkonnen", "RegionStateSelect", prepareRegion<HARKONNEN, 5, true>, readyRegionSelect),
    scene("region-harkonnen-select-6", "region", "harkonnen", "RegionStateSelect", prepareRegion<HARKONNEN, 6, true>, readyRegionSelect),
    scene("region-harkonnen-select-7", "region", "harkonnen", "RegionStateSelect", prepareRegion<HARKONNEN, 7, true>, readyRegionSelect),
    scene("region-harkonnen-select-8", "region", "harkonnen", "RegionStateSelect", prepareRegion<HARKONNEN, 8, true>, readyRegionSelect),
    scene("region-harkonnen-select-9", "region", "harkonnen", "RegionStateSelect", prepareRegion<HARKONNEN, 9, true>, readyRegionSelect),
    scene("region-ordos-intro-1", "region", "ordos", "RegionIntroScene", prepareRegion<ORDOS, 1, false>, readyRegionIntro<1>),
    scene("region-ordos-intro-2", "region", "ordos", "RegionIntroScene", prepareRegion<ORDOS, 1, false>, readyRegionIntro<2>),
    scene("region-ordos-intro-3", "region", "ordos", "RegionIntroScene", prepareRegion<ORDOS, 1, false>, readyRegionIntro<3>),
    scene("region-ordos-conquer-3", "region", "ordos", "RegionConquerMessage", prepareRegion<ORDOS, 3, true>, readyRegionConquer, 1),
    scene("region-ordos-conquer-5", "region", "ordos", "RegionConquerMessage", prepareRegion<ORDOS, 5, true>, readyRegionConquer, 1),
    scene("region-ordos-conquer-7", "region", "ordos", "RegionConquerMessage", prepareRegion<ORDOS, 7, true>, readyRegionConquer, 1),
    scene("region-ordos-conquer-9", "region", "ordos", "RegionConquerMessage", prepareRegion<ORDOS, 9, true>, readyRegionConquer, 1),
    scene("region-ordos-select-2", "region", "ordos", "RegionStateSelect", prepareRegion<ORDOS, 2, true>, readyRegionSelect),
    scene("region-ordos-select-3", "region", "ordos", "RegionStateSelect", prepareRegion<ORDOS, 3, true>, readyRegionSelect),
    scene("region-ordos-select-4", "region", "ordos", "RegionStateSelect", prepareRegion<ORDOS, 4, true>, readyRegionSelect),
    scene("region-ordos-select-5", "region", "ordos", "RegionStateSelect", prepareRegion<ORDOS, 5, true>, readyRegionSelect),
    scene("region-ordos-select-6", "region", "ordos", "RegionStateSelect", prepareRegion<ORDOS, 6, true>, readyRegionSelect),
    scene("region-ordos-select-7", "region", "ordos", "RegionStateSelect", prepareRegion<ORDOS, 7, true>, readyRegionSelect),
    scene("region-ordos-select-8", "region", "ordos", "RegionStateSelect", prepareRegion<ORDOS, 8, true>, readyRegionSelect),
    scene("region-ordos-select-9", "region", "ordos", "RegionStateSelect", prepareRegion<ORDOS, 9, true>, readyRegionSelect),
    scene("region-sardaukar-intro-1", "region", "sardaukar", "RegionIntroScene", prepareRegion<SARDAUKAR, 1, false>, readyRegionIntro<1>),
    scene("region-sardaukar-intro-2", "region", "sardaukar", "RegionIntroScene", prepareRegion<SARDAUKAR, 1, false>, readyRegionIntro<2>),
    scene("region-sardaukar-intro-3", "region", "sardaukar", "RegionIntroScene", prepareRegion<SARDAUKAR, 1, false>, readyRegionIntro<3>),
    scene("region-sardaukar-conquer-3", "region", "sardaukar", "RegionConquerMessage", prepareRegion<SARDAUKAR, 3, true>, readyRegionConquer, 1),
    scene("region-sardaukar-conquer-5", "region", "sardaukar", "RegionConquerMessage", prepareRegion<SARDAUKAR, 5, true>, readyRegionConquer, 1),
    scene("region-sardaukar-conquer-7", "region", "sardaukar", "RegionConquerMessage", prepareRegion<SARDAUKAR, 7, true>, readyRegionConquer, 1),
    scene("region-sardaukar-conquer-9", "region", "sardaukar", "RegionConquerMessage", prepareRegion<SARDAUKAR, 9, true>, readyRegionConquer, 1),
    scene("region-sardaukar-select-2", "region", "sardaukar", "RegionStateSelect", prepareRegion<SARDAUKAR, 2, true>, readyRegionSelect),
    scene("region-sardaukar-select-3", "region", "sardaukar", "RegionStateSelect", prepareRegion<SARDAUKAR, 3, true>, readyRegionSelect),
    scene("region-sardaukar-select-4", "region", "sardaukar", "RegionStateSelect", prepareRegion<SARDAUKAR, 4, true>, readyRegionSelect),
    scene("region-sardaukar-select-5", "region", "sardaukar", "RegionStateSelect", prepareRegion<SARDAUKAR, 5, true>, readyRegionSelect),
    scene("region-sardaukar-select-6", "region", "sardaukar", "RegionStateSelect", prepareRegion<SARDAUKAR, 6, true>, readyRegionSelect),
    scene("region-sardaukar-select-7", "region", "sardaukar", "RegionStateSelect", prepareRegion<SARDAUKAR, 7, true>, readyRegionSelect),
    scene("region-sardaukar-select-8", "region", "sardaukar", "RegionStateSelect", prepareRegion<SARDAUKAR, 8, true>, readyRegionSelect),
    scene("region-sardaukar-select-9", "region", "sardaukar", "RegionStateSelect", prepareRegion<SARDAUKAR, 9, true>, readyRegionSelect),
    scene("choose-house", "choose-house", "", "StateSettled", prepareChooseHouse),
    scene("select-mission-atreides", "select-mission", "atreides", "StateSettled", prepareSelectMission<ATREIDES>),
    scene("select-mission-harkonnen", "select-mission", "harkonnen", "StateSettled", prepareSelectMission<HARKONNEN>),
    scene("select-mission-ordos", "select-mission", "ordos", "StateSettled", prepareSelectMission<ORDOS>),
    scene("select-mission-sardaukar", "select-mission", "sardaukar", "StateSettled", prepareSelectMission<SARDAUKAR>),
    scene("tellhouse-atreides-speak", "tellhouse", "atreides", "MentatFrozen", prepareTellHouse<ATREIDES, false>, readyMentatFrozen<false>),
    scene("tellhouse-atreides-await", "tellhouse", "atreides", "MentatFrozen", prepareTellHouse<ATREIDES, true>, readyMentatFrozen<true>),
    scene("tellhouse-harkonnen-speak", "tellhouse", "harkonnen", "MentatFrozen", prepareTellHouse<HARKONNEN, false>, readyMentatFrozen<false>),
    scene("tellhouse-harkonnen-await", "tellhouse", "harkonnen", "MentatFrozen", prepareTellHouse<HARKONNEN, true>, readyMentatFrozen<true>),
    scene("tellhouse-ordos-speak", "tellhouse", "ordos", "MentatFrozen", prepareTellHouse<ORDOS, false>, readyMentatFrozen<false>),
    scene("tellhouse-ordos-await", "tellhouse", "ordos", "MentatFrozen", prepareTellHouse<ORDOS, true>, readyMentatFrozen<true>),
    scene("tellhouse-sardaukar-speak", "tellhouse", "sardaukar", "MentatFrozen", prepareTellHouse<SARDAUKAR, false>, readyMentatFrozen<false>),
    scene("tellhouse-sardaukar-await", "tellhouse", "sardaukar", "MentatFrozen", prepareTellHouse<SARDAUKAR, true>, readyMentatFrozen<true>),
    withScreen(scene("mentat-briefing-atreides-speak", "mentat", "atreides", "MentatFrozen", prepareMentat<ATREIDES, 0>, readyMentatFrozen<false>), "GAME_BRIEFING", "AtreidesMentat"),
    withScreen(scene("mentat-briefing-atreides-await", "mentat", "atreides", "MentatFrozen", prepareMentat<ATREIDES, 0>, readyMentatFrozen<true>), "GAME_BRIEFING", "AtreidesMentat"),
    withScreen(scene("mentat-win-atreides-speak", "mentat", "atreides", "MentatFrozen", prepareMentat<ATREIDES, 1>, readyMentatFrozen<false>), "GAME_WINBRIEF", "AtreidesMentat"),
    withScreen(scene("mentat-win-atreides-await", "mentat", "atreides", "MentatFrozen", prepareMentat<ATREIDES, 1>, readyMentatFrozen<true>), "GAME_WINBRIEF", "AtreidesMentat"),
    withScreen(scene("mentat-lose-atreides-speak", "mentat", "atreides", "MentatFrozen", prepareMentat<ATREIDES, 2>, readyMentatFrozen<false>), "GAME_LOSEBRIEF", "AtreidesMentat"),
    withScreen(scene("mentat-lose-atreides-await", "mentat", "atreides", "MentatFrozen", prepareMentat<ATREIDES, 2>, readyMentatFrozen<true>), "GAME_LOSEBRIEF", "AtreidesMentat"),
    withScreen(scene("mentat-briefing-harkonnen-speak", "mentat", "harkonnen", "MentatFrozen", prepareMentat<HARKONNEN, 0>, readyMentatFrozen<false>), "GAME_BRIEFING", "HarkonnenMentat"),
    withScreen(scene("mentat-briefing-harkonnen-await", "mentat", "harkonnen", "MentatFrozen", prepareMentat<HARKONNEN, 0>, readyMentatFrozen<true>), "GAME_BRIEFING", "HarkonnenMentat"),
    withScreen(scene("mentat-win-harkonnen-speak", "mentat", "harkonnen", "MentatFrozen", prepareMentat<HARKONNEN, 1>, readyMentatFrozen<false>), "GAME_WINBRIEF", "HarkonnenMentat"),
    withScreen(scene("mentat-win-harkonnen-await", "mentat", "harkonnen", "MentatFrozen", prepareMentat<HARKONNEN, 1>, readyMentatFrozen<true>), "GAME_WINBRIEF", "HarkonnenMentat"),
    withScreen(scene("mentat-lose-harkonnen-speak", "mentat", "harkonnen", "MentatFrozen", prepareMentat<HARKONNEN, 2>, readyMentatFrozen<false>), "GAME_LOSEBRIEF", "HarkonnenMentat"),
    withScreen(scene("mentat-lose-harkonnen-await", "mentat", "harkonnen", "MentatFrozen", prepareMentat<HARKONNEN, 2>, readyMentatFrozen<true>), "GAME_LOSEBRIEF", "HarkonnenMentat"),
    withScreen(scene("mentat-briefing-ordos-speak", "mentat", "ordos", "MentatFrozen", prepareMentat<ORDOS, 0>, readyMentatFrozen<false>), "GAME_BRIEFING", "OrdosMentat"),
    withScreen(scene("mentat-briefing-ordos-await", "mentat", "ordos", "MentatFrozen", prepareMentat<ORDOS, 0>, readyMentatFrozen<true>), "GAME_BRIEFING", "OrdosMentat"),
    withScreen(scene("mentat-win-ordos-speak", "mentat", "ordos", "MentatFrozen", prepareMentat<ORDOS, 1>, readyMentatFrozen<false>), "GAME_WINBRIEF", "OrdosMentat"),
    withScreen(scene("mentat-win-ordos-await", "mentat", "ordos", "MentatFrozen", prepareMentat<ORDOS, 1>, readyMentatFrozen<true>), "GAME_WINBRIEF", "OrdosMentat"),
    withScreen(scene("mentat-lose-ordos-speak", "mentat", "ordos", "MentatFrozen", prepareMentat<ORDOS, 2>, readyMentatFrozen<false>), "GAME_LOSEBRIEF", "OrdosMentat"),
    withScreen(scene("mentat-lose-ordos-await", "mentat", "ordos", "MentatFrozen", prepareMentat<ORDOS, 2>, readyMentatFrozen<true>), "GAME_LOSEBRIEF", "OrdosMentat"),
    withScreen(scene("mentat-briefing-sardaukar-speak", "mentat", "sardaukar", "MentatFrozen", prepareMentat<SARDAUKAR, 0>, readyMentatFrozen<false>), "GAME_BRIEFING", "SardaukarMentat"),
    withScreen(scene("mentat-briefing-sardaukar-await", "mentat", "sardaukar", "MentatFrozen", prepareMentat<SARDAUKAR, 0>, readyMentatFrozen<true>), "GAME_BRIEFING", "SardaukarMentat"),
    withScreen(scene("mentat-win-sardaukar-speak", "mentat", "sardaukar", "MentatFrozen", prepareMentat<SARDAUKAR, 1>, readyMentatFrozen<false>), "GAME_WINBRIEF", "SardaukarMentat"),
    withScreen(scene("mentat-win-sardaukar-await", "mentat", "sardaukar", "MentatFrozen", prepareMentat<SARDAUKAR, 1>, readyMentatFrozen<true>), "GAME_WINBRIEF", "SardaukarMentat"),
    withScreen(scene("mentat-lose-sardaukar-speak", "mentat", "sardaukar", "MentatFrozen", prepareMentat<SARDAUKAR, 2>, readyMentatFrozen<false>), "GAME_LOSEBRIEF", "SardaukarMentat"),
    withScreen(scene("mentat-lose-sardaukar-await", "mentat", "sardaukar", "MentatFrozen", prepareMentat<SARDAUKAR, 2>, readyMentatFrozen<true>), "GAME_LOSEBRIEF", "SardaukarMentat"),
    scene("skirmish-setup-random", "skirmish-setup", "", "FixedFrames(2, no readiness flag)", prepareSkirmishSetup<0>),
    scene("skirmish-setup-ready-map", "skirmish-setup", "", "FixedFrames(2, no readiness flag)", prepareSkirmishSetup<1>),
    scene("options-menu-main", "options-menu", "", "FixedFrames(14, no readiness flag)", prepareOptionsMenu<0>, readyOptionsMenu<0>),
    scene("options-menu-applied", "options-menu", "", "FixedFrames(14, no readiness flag)", prepareOptionsMenu<1>, readyOptionsMenu<1>),
    scene("credits-title", "credits", "", "CreditsScrollPosition", prepareCredits, readyCredits<0>),
    scene("credits-1", "credits", "", "CreditsScrollPosition", prepareCredits, readyCredits<1>),
    scene("credits-2", "credits", "", "CreditsScrollPosition", prepareCredits, readyCredits<2>),
    scene("credits-3", "credits", "", "CreditsScrollPosition", prepareCredits, readyCredits<3>),
    hdOnly(scene("credits-4", "credits", "", "CreditsScrollPosition", prepareCredits, readyCredits<4>)),
    hdOnly(scene("credits-5", "credits", "", "CreditsScrollPosition", prepareCredits, readyCredits<5>)),
    withScreen(scene("outcome-win", "outcome", "atreides", "FixedFrames(8, no readiness flag)", prepareOutcome<true>,
                     readyOutcome<true>), "GAME_WINNING", "cWinLoseState"),
    withScreen(scene("outcome-lose", "outcome", "atreides", "FixedFrames(8, no readiness flag)", prepareOutcome<false>,
                     readyOutcome<false>), "GAME_LOSING", "cWinLoseState"),
    scene("options-game-main-nosaves", "options-game", "", "FixedFrames(14, no readiness flag)", prepareGameOptions, readyOptionsMenu<0>),
    scene("options-game-applied", "options-game", "", "FixedFrames(14, no readiness flag)", prepareGameOptions, readyOptionsMenu<1>),
    onGameScreen(scene("structure-label-top", "game-playing", "atreides", kFixedGameFrames, prepareStructureLabel<0>,
                       nullptr, 5), true),
    onGameScreen(scene("structure-label-right", "game-playing", "atreides", kFixedGameFrames, prepareStructureLabel<1>,
                       nullptr, 5), true),
    onGameScreen(scene("units-label-trike", "game-playing", "atreides", kFixedGameFrames, prepareUnitLabels<TRIKE>), false),
    onGameScreen(scene("units-label-raider", "game-playing", "atreides", kFixedGameFrames, prepareUnitLabels<RAIDER>), false),
    onGameScreen(scene("units-label-quad", "game-playing", "atreides", kFixedGameFrames, prepareUnitLabels<QUAD>), false),
    onGameScreen(scene("units-label-tank", "game-playing", "atreides", kFixedGameFrames, prepareUnitLabels<TANK>), false),
    onGameScreen(scene("units-label-siegetank", "game-playing", "atreides", kFixedGameFrames, prepareUnitLabels<SIEGETANK>), false),
    onGameScreen(scene("units-label-launcher", "game-playing", "atreides", kFixedGameFrames, prepareUnitLabels<LAUNCHER>), false),
    onGameScreen(scene("units-label-deviator", "game-playing", "atreides", kFixedGameFrames, prepareUnitLabels<DEVIATOR>), false),
    onGameScreen(scene("units-label-sonictank", "game-playing", "atreides", kFixedGameFrames, prepareUnitLabels<SONICTANK>), false),
    onGameScreen(scene("units-label-devastator", "game-playing", "atreides", kFixedGameFrames, prepareUnitLabels<DEVASTATOR>), false),
    onGameScreen(scene("units-label-harvester", "game-playing", "atreides", kFixedGameFrames, prepareUnitLabels<HARVESTER>), false),
    onGameScreen(scene("units-label-mcv", "game-playing", "atreides", kFixedGameFrames, prepareUnitLabels<MCV>), false),
    onGameScreen(scene("units-label-soldier", "game-playing", "atreides", kFixedGameFrames, prepareUnitLabels<SOLDIER>), false),
    onGameScreen(scene("units-label-infantry", "game-playing", "atreides", kFixedGameFrames, prepareUnitLabels<INFANTRY>), false),
    onGameScreen(scene("units-label-trooper", "game-playing", "atreides", kFixedGameFrames, prepareUnitLabels<TROOPER>), false),
    onGameScreen(scene("units-label-troopers", "game-playing", "atreides", kFixedGameFrames, prepareUnitLabels<TROOPERS>), false),
    onGameScreen(scene("units-label-unit-fremen-one", "game-playing", "atreides", kFixedGameFrames, prepareUnitLabels<UNIT_FREMEN_ONE>), false),
    onGameScreen(scene("units-label-unit-fremen-three", "game-playing", "atreides", kFixedGameFrames, prepareUnitLabels<UNIT_FREMEN_THREE>), false),
    onGameScreen(scene("units-label-saboteur", "game-playing", "atreides", kFixedGameFrames, prepareUnitLabels<SABOTEUR>), false),
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
