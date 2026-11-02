#include "ZoomTestSupport.hpp"

#include "controls/mousestates/cMouseNormalState.h"
#include "data/gfxdata.h"

#include <functional>
#include <iostream>
#include <string>
#include <vector>

using namespace zoomtest;

namespace {
constexpr int OwnUnit = 0;
constexpr int EnemyUnit = 1;
constexpr int EnemyPlayer = 1;
constexpr int MouseX = 400;
constexpr int MouseY = 300;

class CountingNormalState : public cMouseNormalState {
public:
    CountingNormalState(cPlayer *player, cGameControlsContext *context, cMouse *mouse)
        : cMouseNormalState(player, context, mouse)
    {
    }

    void onNotifyMouseEvent(const s_MouseEvent &event) override
    {
        if (event.eventType != eMouseEventType::MOUSE_MOVED_TO) return;
        ++count;
        viewportX = mapCamera->m_viewportStartX;
        viewportY = mapCamera->m_viewportStartY;
        zoom = mapCamera->m_zoomLevel;
    }

    int count = 0;
    float viewportX = 0.0F;
    float viewportY = 0.0F;
    float zoom = 0.0F;
};

struct Action {
    std::string name;
    float zoom;
    float shiftX;
    float shiftY;
    std::function<void()> run;
};

void moveByThink(float moveX, float moveY)
{
    mapCamera->m_moveX = moveX;
    mapCamera->m_moveY = moveY;
    mapCamera->thinkFast();
    mapCamera->m_moveX = 0.0F;
    mapCamera->m_moveY = 0.0F;
}

void checkRefreshCounts(InputRig &rig, std::vector<std::string> &failures)
{
    cGameControlsContext &controls = rig.controls();
    cMouseNormalState *original = controls.m_mouseNormalState;
    auto *counter = new CountingNormalState(&players[HUMAN], &controls, game.m_mouse);
    controls.m_mouseNormalState = counter;

    const std::vector<Action> actions = {
        {"jumpTo inside the map", 1.0F, 0.0F, 0.0F, [] { mapCamera->jumpTo(224, 192); }},
        {"jumpTo outside the map", 1.0F, 0.0F, 0.0F, [] { mapCamera->jumpTo(-5000, 90000); }},
        {"setViewportPosition inside the map", 1.0F, 0.0F, 0.0F, [] { mapCamera->setViewportPosition(224, 192); }},
        {"setViewportPosition outside the map", 1.0F, 0.0F, 0.0F,
         [] { mapCamera->setViewportPosition(90000, -5000); }},
        {"centerAndJumpViewPortToCell inside the map", 1.0F, 0.0F, 0.0F,
         [] { mapCamera->centerAndJumpViewPortToCell(40 * MapCells + 40); }},
        {"centerAndJumpViewPortToCell in the corner", 1.0F, 0.0F, 0.0F,
         [] { mapCamera->centerAndJumpViewPortToCell(0); }},
        {"thinkFast inside the map", 1.0F, 32.0F, 32.0F, [] { moveByThink(96.0F, 64.0F); }},
        {"thinkFast outside the map", 1.0F, 32.0F, 32.0F, [] { moveByThink(90000.0F, 90000.0F); }},
        {"zoomIn", 1.0F, 100.0F, 100.0F, [] { mapCamera->zoomIn(); }},
        {"zoomOut", 1.0F, 100.0F, 100.0F, [] { mapCamera->zoomOut(); }},
        {"resetZoom", 2.0F, 100.0F, 100.0F, [] { mapCamera->resetZoom(); }},
    };

    for (const Action &action : actions) {
        placeCamera(action.zoom, action.shiftX, action.shiftY);
        rig.placeMouse(MouseX, MouseY);
        counter->count = 0;
        action.run();
        if (counter->count != 1) {
            failures.push_back(std::format("{}: hover refreshed {} times, expected exactly 1", action.name,
                                           counter->count));
            continue;
        }
        if (counter->viewportX != mapCamera->m_viewportStartX || counter->viewportY != mapCamera->m_viewportStartY ||
            counter->zoom != mapCamera->m_zoomLevel) {
            failures.push_back(std::format(
                "{}: hover refreshed at viewport ({},{}) zoom {}, but the camera ends at ({},{}) zoom {}",
                action.name, counter->viewportX, counter->viewportY, counter->zoom, mapCamera->m_viewportStartX,
                mapCamera->m_viewportStartY, mapCamera->m_zoomLevel));
        }
    }

    controls.m_mouseNormalState = original;
    delete counter;
}

void sendMouseMove(cGameControlsContext &controls)
{
    s_MouseEvent moved;
    moved.eventType = eMouseEventType::MOUSE_MOVED_TO;
    moved.coords = cPoint(MouseX, MouseY);
    controls.onNotifyMouseEvent(moved);
}

void selectOwnUnitsMode(UnitFrameFixture &fixture, cGameControlsContext &controls)
{
    fixture.setUnitFlags(OwnUnit, true, false);
    controls.setMouseState(MOUSESTATE_SELECT);
    controls.setMouseState(MOUSESTATE_UNITS_SELECTED);
}

void checkAttackCursor(UnitFrameFixture &fixture, InputRig &rig, std::vector<std::string> &failures)
{
    cGameControlsContext &controls = rig.controls();

    placeCamera(1.0F, 0.0F, 0.0F);
    rig.setMousePosition(MouseX, MouseY);
    const int cellBefore = expectedCell(MouseX, MouseY);
    mapCamera->jumpTo(224, 192);
    const int cellAfter = expectedCell(MouseX, MouseY);
    const float jumpedX = mapCamera->m_viewportStartX;
    const float jumpedY = mapCamera->m_viewportStartY;
    placeCamera(1.0F, 0.0F, 0.0F);
    require(cellBefore >= 0 && cellAfter >= 0 && cellBefore != cellAfter,
            "setup: the camera jump must move the cell under the mouse");

    const int humanTeam = players[HUMAN].iTeam;
    const int enemyTeam = players[EnemyPlayer].iTeam;
    players[HUMAN].iTeam = 0;
    players[EnemyPlayer].iTeam = 1;

    const int ownCell = cellBefore == 10 * MapCells + 10 ? 12 * MapCells + 12 : 10 * MapCells + 10;
    fixture.setUnit(OwnUnit, TANK, (ownCell % MapCells) * CellSize, (ownCell / MapCells) * CellSize);
    fixture.setUnit(EnemyUnit, TANK, (cellAfter % MapCells) * CellSize, (cellAfter / MapCells) * CellSize);
    unit[EnemyUnit].iPlayer = EnemyPlayer;
    global_map.setVisibleFor(cellAfter, HUMAN);

    placeCamera(1.0F, jumpedX, jumpedY);
    rig.placeMouse(MouseX, MouseY);
    selectOwnUnitsMode(fixture, controls);
    sendMouseMove(controls);
    require(controls.getIdOfUnitWhereMouseHovers() == EnemyUnit && game.m_mouse->isTile(MOUSE_ATTACK),
            std::format("setup: a real mouse move onto the enemy unit must give the attack cursor, "
                        "hovered unit {}, cursor tile {}",
                        controls.getIdOfUnitWhereMouseHovers(), game.m_mouse->mouse_tile));

    placeCamera(1.0F, 0.0F, 0.0F);
    rig.placeMouse(MouseX, MouseY);
    selectOwnUnitsMode(fixture, controls);
    sendMouseMove(controls);
    require(controls.getIdOfUnitWhereMouseHovers() == -1 && game.m_mouse->isTile(MOUSE_MOVE),
            std::format("setup: before the camera jump nothing may be hovered and the cursor must be move, "
                        "hovered unit {}, cursor tile {}",
                        controls.getIdOfUnitWhereMouseHovers(), game.m_mouse->mouse_tile));

    mapCamera->jumpTo(224, 192);

    if (controls.getIdOfUnitWhereMouseHovers() != EnemyUnit) {
        failures.push_back(std::format("attack cursor: hovered unit is {} after the camera jump, expected {}",
                                       controls.getIdOfUnitWhereMouseHovers(), EnemyUnit));
    }
    if (!game.m_mouse->isTile(MOUSE_ATTACK)) {
        failures.push_back(std::format(
            "attack cursor: cursor tile is {} right after the camera jump, expected attack ({})",
            game.m_mouse->mouse_tile, static_cast<int>(MOUSE_ATTACK)));
    }

    controls.setMouseState(MOUSESTATE_SELECT);
    global_map.cellSetIdForLayer(cellAfter, MAPID_UNITS, -1);
    global_map.cellSetIdForLayer(ownCell, MAPID_UNITS, -1);
    unit[OwnUnit].bSelected = false;
    unit[EnemyUnit].bHovered = false;
    players[HUMAN].iTeam = humanTeam;
    players[EnemyPlayer].iTeam = enemyTeam;
}

void runChecks(std::vector<std::string> &failures)
{
    UnitFrameFixture fixture(4, 100);
    InputRig rig;
    rig.setMousePosition(MouseX, MouseY);
    useCamera(ScreenWidth, ScreenHeight, 1.0F, 0.0F, 0.0F);
    rig.installControls();

    checkRefreshCounts(rig, failures);
    checkAttackCursor(fixture, rig, failures);
}
}

int main()
{
    std::vector<std::string> failures;
    try {
        runChecks(failures);
    }
    catch (const std::exception &error) {
        std::cerr << "mouse_hover_state: " << error.what() << '\n';
        return 1;
    }
    if (!failures.empty()) {
        for (const std::string &failure : failures) std::cerr << "mouse_hover_state: " << failure << '\n';
        return 1;
    }
    std::cout << "mouse_hover_state: all checks passed\n";
    return 0;
}
