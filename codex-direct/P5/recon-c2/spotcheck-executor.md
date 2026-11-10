# Выборочная сверка

## Помощник 1 — `fork-hunks-1.tsv`

### 1. `src/drawers/CreditsDrawer.cpp@9208dcf:37-43`
Факт из таблицы: ширина полосы вычисляется по логическому размеру текстуры для HD-плотности.

Команда:
```sh
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/CreditsDrawer.cpp | sed -n '37,43p'
```

Вывод:
```text
    previousCredits = 0;

    // center credits bar within sidebar
    int widthCreditsBar = m_gfxinter->getLogicalWidth(CREDITS_BAR);
    drawX = game.m_screenW - (cSideBar::SidebarWidthWithoutCandyBar / 2) - (widthCreditsBar / 2);
    drawY = 0;
}
```

Вердикт: совпало

### 2. `src/drawers/cBuildingListDrawer.cpp@9208dcf:97-104`
Факт из таблицы: размер рамки наведения берётся из геометрии кнопки списка.

Команда:
```sh
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp | sed -n '97,104p'
```

Вывод:
```text
    int y = list->getButtonDrawY();
    int id = list->getButtonIconIdUnpressed();

    int width = list->getButtonWidth();
    int height = list->getButtonHeight();

    Color color = m_player->getSelectFadingColor();
```

Вердикт: совпало

### 3. `src/drawers/cBuildingListDrawer.cpp@9208dcf:220-237`
Факт из таблицы: рисование списка ограничено областью карточек, размеры и вертикальная раскладка взяты из HudLayout.

Команда:
```sh
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp | sed -n '220,237p'
```

Вывод:
```text
    std::array<int, 6> isBuildingItemInList = list->isBuildingItem();

    // Start drawing the 'icons grid'
    int withOfIcon = getCardWidth();
    int heightOfIcon = getCardHeight();

    renderDrawer->setClippingFor(
        layout.cards.getX(),
        layout.cards.getY(),
        layout.cards.getEndX(),
        layout.cards.getEndY()
    );

    // Draw the visible icon rows. HD positions come from HudLayout so drawing
    // and hit testing cannot drift apart.
    for (int i = 0; i < end; i++) {
        cBuildingListItem *item = list->getItem(i);
```

Вердикт: совпало

### 4. `src/drawers/cBuildingListDrawer.cpp@9208dcf:354-360`
Факт из таблицы: надпись о занятом строительстве локализована.

Команда:
```sh
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp | sed -n '354,360p'
```

Вывод:
```text
                    renderDrawer->renderLine( iDrawX, iDrawY + heightOfIcon, iDrawX + withOfIcon, iDrawY, errorFadingColor);

                    Color red = Color{255, 0, 0,255};
                    m_smallTextDrawer->drawTextCenteredInBox(localization::text("Upgrade", "Улучшение"), iDrawX, iDrawY, withOfIcon, heightOfIcon, red);
                }

                // Pending building (ie: a build is progressing, blocking the upgrade)
```

Вердикт: не совпало

## Помощник 2 — `fork-hunks-2.tsv`

### 1. `src/managers/cDrawManager.cpp@9208dcf:2-8`
Факт из таблицы: подключены средства аудита интерфейса.

Команда:
```sh
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp | sed -n '2,8p'
```

Вывод:
```text

#include "controls/cGameControlsContext.h"
#include "d2tmc.h"
#include "debug/UiAudit.hpp"
#include "data/gfxdata.h"
#include "data/gfxinter.h"
#include "drawers/SDLDrawer.hpp"
```

Вердикт: совпало

### 2. `src/managers/cDrawManager.cpp@9208dcf:77-82`
Факт из таблицы: вызов старой панели параметров удалён из отрисовки боевого состояния.

Команда:
```sh
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp | sed -n '77,82p'
```

Вывод:
```text
    // GUI
    drawSidebar();

    renderDrawer->setClippingFor(0, cSideBar::TopBarHeight, mapCamera->getWindowWidth(), mapCamera->getWindowHeight() + cSideBar::TopBarHeight);
    drawStructurePlacing();
    renderDrawer->resetClippingFor();
```

Вердикт: не совпало

### 3. `src/managers/cDrawManager.cpp@9208dcf:86-97`
Факт из таблицы: добавлены музыкальные элементы верхней строки и командная строка, удалена старая отрисовка полосы параметров.

Команда:
```sh
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp | sed -n '86,97p'
```

Вывод:
```text

    // THE MESSAGE
    drawMessage();
    drawTopBarMusicControls();

    drawNotifications();

    m_commandBarDrawer.draw();

    renderDrawer->resetClippingFor();

    if (game.m_drawUsages) {
```

Вердикт: совпало

### 4. `src/managers/cDrawManager.cpp@9208dcf:456-462`
Факт из таблицы: события мыши передаются командной строке.

Команда:
```sh
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp | sed -n '456,462p'
```

Вывод:
```text
void cDrawManager::onNotifyMouseEvent(const s_MouseEvent &event)
{
    m_sidebarDrawer.onNotifyMouseEvent(event);
    m_commandBarDrawer.onNotifyMouseEvent(event);
}

void cDrawManager::onNotifyKeyboardEvent(const cKeyboardEvent &event)
```

Вердикт: совпало

## Помощник 3 — `hud-images.tsv` и `camera-mouse.tsv`

### 1. `src/cGame_logic.cpp@9208dcf:2542` (`hud-images.tsv`)
Факт из таблицы: в `getHdOutcomeTexture` используется имя `outcome_victory_en.png`.

Команда:
```sh
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/cGame_logic.cpp | sed -n '2542p'
```

Вывод:
```text
                "outcome_victory_en.png",
```

Вердикт: совпало

### 2. `src/cGame_logic.cpp@9208dcf:2543` (`hud-images.tsv`)
Факт из таблицы: в `getHdOutcomeTexture` используется имя `outcome_victory_ru.png`.

Команда:
```sh
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/cGame_logic.cpp | sed -n '2543p'
```

Вывод:
```text
                "outcome_victory_ru.png"
```

Вердикт: совпало

### 3. `src/map/cMapCamera.cpp@9208dcf:37-64` (`camera-mouse.tsv`)
Факт из таблицы: окно камеры получает размеры экрана за вычетом боковой и верхней панелей; viewport получает размеры окна, после чего вызывается калибровка масштаба.

Команда:
```sh
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/map/cMapCamera.cpp | sed -n '37,64p'
```

Вывод:
```text
cMapCamera::cMapCamera(cMap *theMap, float moveSpeedDrag, float moveSpeedBorderOrKeys, bool cameraEdgeMove) :
    m_moveSpeedDrag(moveSpeedDrag),
    m_moveSpeedBorderOrKeys(moveSpeedBorderOrKeys),
    m_cameraEdgeMove(cameraEdgeMove),
    m_pMap(theMap)
{
    m_viewportStartX = m_viewportStartY = 32;
    m_zoomLevel = game.getWorldScaleFactor();

    int widthOfSidebar = cSideBar::SidebarWidth;
    m_heightOfTopBar = cSideBar::TopBarHeight;

    m_windowWidth= game.m_screenW - widthOfSidebar;
    m_windowHeight= game.m_screenH - m_heightOfTopBar;

    m_viewportWidth=m_windowWidth;
    m_viewportHeight=m_windowHeight;

    m_moveX = 0.0f;
    m_moveY = 0.0f;

    m_keyPressedDown = false;
    m_keyPressedUp = false;
    m_keyPressedLeft = false;
    m_keyPressedRight = false;

    calibrate();
}
```

Вердикт: совпало

### 4. `src/controls/cGameControlsContext.cpp@9208dcf:46-73` (`camera-mouse.tsv`)
Факт из таблицы: координаты мыши классифицируются как верхняя панель, командная строка, миникарта или боковая панель; иначе выбирается клетка поля боя.

Команда:
```sh
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/controls/cGameControlsContext.cpp | sed -n '46,73p'
```

Вывод:
```text
void cGameControlsContext::updateMouseCell(const cPoint &coords)
{
    if (coords.y < cSideBar::TopBarHeight) {
        m_mouseCell = MOUSECELL_TOPBAR; // at the top bar or higher, so no mouse cell id.
        m_mouseOnBattleField = false;
        return;
    }

    if (drawManager->getCommandBarDrawer()->isMouseOver(coords)) {
        m_mouseCell = MOUSECELL_COMMAND_BAR;
        m_mouseOnBattleField = false;
        return;
    }

    if (drawManager->getMiniMapDrawer()->isMouseOver()) {
        m_mouseCell = MOUSECELL_MINIMAP; // on minimap
        m_mouseOnBattleField = false;
        return;
    }

    if (coords.x > (game.m_screenW - cSideBar::SidebarWidth)) {
        m_mouseCell = MOUSECELL_SIDEBAR;
        m_mouseOnBattleField = false;
        return;
    }
    m_mouseOnBattleField = true;
    m_mouseCell = getMouseCellFromScreen(coords.x, coords.y);
}
```

Вердикт: совпало
