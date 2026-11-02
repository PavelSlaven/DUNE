#pragma once

#include "UnitFrameFixture.hpp"

#include "context/GameContext.hpp"
#include "context/TextContext.hpp"
#include "controls/cGameControlsContext.h"
#include "controls/cMouse.h"
#include "d2tmc.h"
#include "drawers/cTextDrawer.h"
#include "managers/cDrawManager.h"
#include "map/cMapCamera.h"
#include "player/cPlayer.h"
#include "utils/cSoundPlayer.h"
#include "utils/cTimeCounter.h"
#include "utils/cTimeManager.h"

#include <algorithm>
#include <cmath>
#include <format>
#include <memory>
#include <stdexcept>
#include <string>
#include <vector>

namespace zoomtest {

inline constexpr int MapCells = 64;
inline constexpr int CellSize = 32;
inline constexpr int ScreenWidth = 1600;
inline constexpr int ScreenHeight = 900;

inline void require(bool condition, const std::string &message)
{
    if (!condition) throw std::runtime_error(message);
}

inline void requireRect(const cRectangle &actual, const cRectangle &expected, const std::string &label)
{
    require(actual.getX() == expected.getX() && actual.getY() == expected.getY() &&
                actual.getWidth() == expected.getWidth() && actual.getHeight() == expected.getHeight(),
            std::format("{}: expected ({},{},{},{}), got ({},{},{},{})",
                        label, expected.getX(), expected.getY(), expected.getWidth(), expected.getHeight(),
                        actual.getX(), actual.getY(), actual.getWidth(), actual.getHeight()));
}

inline void placeCamera(float zoom, float viewportX, float viewportY)
{
    mapCamera->m_zoomLevel = zoom;
    mapCamera->m_viewportStartX = viewportX;
    mapCamera->m_viewportStartY = viewportY;
    mapCamera->calibrate();
}

inline void useCamera(int screenWidth, int screenHeight, float zoom, float viewportX, float viewportY)
{
    game.m_screenW = screenWidth;
    game.m_screenH = screenHeight;
    delete mapCamera;
    mapCamera = new cMapCamera(&global_map, 0.0F, 0.0F, false);
    placeCamera(zoom, viewportX, viewportY);
}

inline int windowWidth() { return mapCamera->m_windowWidth; }
inline int windowHeight() { return mapCamera->m_windowHeight; }
inline int topBarHeight() { return mapCamera->m_heightOfTopBar; }

inline std::vector<int> columnTable()
{
    std::vector<int> table(windowWidth(), -1);
    for (int column = 0; column < MapCells; ++column) {
        const int first = std::max(0, mapCamera->getWindowXPosition(column * CellSize));
        const int end = std::min(windowWidth(), mapCamera->getWindowXPosition(column * CellSize + CellSize));
        for (int pixel = first; pixel < end; ++pixel) table[pixel] = column;
    }
    return table;
}

inline std::vector<int> rowTable()
{
    std::vector<int> table(windowHeight(), -1);
    for (int row = 0; row < MapCells; ++row) {
        const int first = std::max(topBarHeight(), mapCamera->getWindowYPosition(row * CellSize));
        const int end = std::min(topBarHeight() + windowHeight(),
                                 mapCamera->getWindowYPosition(row * CellSize + CellSize));
        for (int pixel = first; pixel < end; ++pixel) table[pixel - topBarHeight()] = row;
    }
    return table;
}

inline int expectedColumn(int mouseX)
{
    for (int column = 0; column < MapCells; ++column) {
        if (mapCamera->getWindowXPosition(column * CellSize) <= mouseX &&
            mouseX < mapCamera->getWindowXPosition(column * CellSize + CellSize)) {
            return column;
        }
    }
    return -1;
}

inline int expectedRow(int mouseY)
{
    for (int row = 0; row < MapCells; ++row) {
        if (mapCamera->getWindowYPosition(row * CellSize) <= mouseY &&
            mouseY < mapCamera->getWindowYPosition(row * CellSize + CellSize)) {
            return row;
        }
    }
    return -1;
}

inline int expectedCell(int mouseX, int mouseY)
{
    const int column = expectedColumn(mouseX);
    const int row = expectedRow(mouseY);
    if (column < 0 || row < 0) return -1;
    return row * MapCells + column;
}

class InputRig {
public:
    InputRig()
        : m_previousMouse(game.m_mouse)
        , m_previousDrawManager(drawManager)
    {
        std::unique_ptr<cTextDrawer> text1 = std::make_unique<cTextDrawer>(nullptr);
        std::unique_ptr<cTextDrawer> text2 = std::make_unique<cTextDrawer>(nullptr);
        std::unique_ptr<cTextDrawer> text3 = std::make_unique<cTextDrawer>(nullptr);
        std::unique_ptr<cTextDrawer> text4 = std::make_unique<cTextDrawer>(nullptr);
        std::unique_ptr<cTextDrawer> text5 = std::make_unique<cTextDrawer>(nullptr);
        std::unique_ptr<cTextDrawer> text6 = std::make_unique<cTextDrawer>(nullptr);
        m_context.setTextContext(std::make_unique<TextContext>(
            std::move(text1), std::move(text2), std::move(text3),
            std::move(text4), std::move(text5), std::move(text6)));
        m_mouse = std::make_unique<cMouse>(&m_context);
        game.m_mouse = m_mouse.get();
        drawManager = reinterpret_cast<cDrawManager *>(m_drawManagerStorage);
    }

    InputRig(const InputRig &) = delete;
    InputRig &operator=(const InputRig &) = delete;

    ~InputRig()
    {
        if (m_controls) {
            delete players[HUMAN].gameControlsContext;
            players[HUMAN].gameControlsContext = nullptr;
        }
        game.m_mouse = m_previousMouse;
        drawManager = m_previousDrawManager;
    }

    cGameControlsContext &installControls()
    {
        m_controls = new cGameControlsContext(&players[HUMAN], m_mouse.get());
        players[HUMAN].setGameControlsContext(m_controls);
        m_controls->m_prevTickMouseAtBattleField = true;
        return *m_controls;
    }

    cGameControlsContext &controls() { return *m_controls; }

    void setMousePosition(int x, int y)
    {
        m_mouse->coords = cPoint(x, y);
    }

    void placeMouse(int x, int y)
    {
        setMousePosition(x, y);
        s_MouseEvent event;
        event.eventType = eMouseEventType::MOUSE_MOVED_TO;
        event.coords = cPoint(x, y);
        m_controls->onMouseMovedTo(event);
    }

private:
    cMouse *m_previousMouse;
    cDrawManager *m_previousDrawManager;
    GameContext m_context;
    std::unique_ptr<cMouse> m_mouse;
    cGameControlsContext *m_controls = nullptr;
    alignas(cDrawManager) unsigned char m_drawManagerStorage[sizeof(cDrawManager)] = {};
};

}
