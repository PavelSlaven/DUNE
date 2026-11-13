# Сверка второй разведки П5в (Haiku)

Ревизии: FORK1 = 9208dcf5a358f40afd95c99480e4e09f781ed566, PORT = 832c953a94a632d57872349013f7ed1a37434715. Источник: четыре таблицы папки recon-c2; RECON.md не открывался. Для строк fork-hunks проверены два утверждения: функция в FORK1 (столбец 3) и место в PORT (столбец 7). Номер строки таблицы — номер строки в файле (строка 1 — заголовок). Для функции, начинающейся до участка, печатается отрезок от её первой строки.

## 1. fork-hunks-1.tsv, строка 3
- Утверждение: FORK1 `CreditsDrawer::CreditsDrawer`, участок 37-43 (ширина полосы по логическому размеру текстуры); PORT `src/drawers/CreditsDrawer.cpp@832c953:50-76`, `CreditsDrawer::CreditsDrawer`.
- Команда FORK1: `git -C C:/Users/Slaven/Projects/DUNE show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/CreditsDrawer.cpp | sed -n '21,43p'`
- Вывод FORK1 (выдержка): `21: CreditsDrawer::CreditsDrawer(GameContext* ctx, cPlayer *player) :`; `40:     int widthCreditsBar = m_gfxinter->getLogicalWidth(CREDITS_BAR);`
- Команда PORT: `git -C C:/Users/Slaven/Projects/DUNE show 832c953a94a632d57872349013f7ed1a37434715:src/drawers/CreditsDrawer.cpp | sed -n '50,76p'`
- Вывод PORT (выдержка): `50: CreditsDrawer::CreditsDrawer(GameContext* ctx, cGameSettings *settings, cPlayer *player) :`
- Итог: совпало

## 2. fork-hunks-1.tsv, строка 12
- Утверждение: FORK1 `cBuildingListDrawer::drawList`, участок 220-237; PORT `src/drawers/cBuildingListDrawer.cpp@832c953:165-377`, `cBuildingListDrawer::drawList`.
- Команда FORK1: `git -C C:/Users/Slaven/Projects/DUNE show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp | sed -n '206,237p'`
- Вывод FORK1 (выдержка): `206: void cBuildingListDrawer::drawList(cBuildingList *list, bool shouldDrawStructureSize)`
- Команда PORT: `git -C C:/Users/Slaven/Projects/DUNE show 832c953a94a632d57872349013f7ed1a37434715:src/drawers/cBuildingListDrawer.cpp | sed -n '165,377p' | grep -n "drawList"`
- Вывод PORT: `1:void cBuildingListDrawer::drawList(cBuildingList *list, const bool shouldDrawStructureSize)` (файловая строка 165)
- Итог: совпало

## 3. fork-hunks-1.tsv, строка 22
- Утверждение: FORK1 `cBuildingListDrawer::drawStructureSize` и `cBuildingListDrawer::isOverItemCoordinates_Boolean`, участок 494-512; PORT `drawStructureSize` 403-425 и `isOverItemCoordinates_Boolean` 427-433.
- Команда FORK1: `git -C C:/Users/Slaven/Projects/DUNE show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp | sed -n '478,512p'`
- Вывод FORK1 (выдержка): `478: void cBuildingListDrawer::drawStructureSize(int structureId, int x, int y)`; `504: bool cBuildingListDrawer::isOverItemCoordinates_Boolean(int x, int y, int drawX, int drawY)`
- Команда PORT: `git -C C:/Users/Slaven/Projects/DUNE show 832c953a94a632d57872349013f7ed1a37434715:src/drawers/cBuildingListDrawer.cpp | sed -n '403,433p'`
- Вывод PORT (выдержка): `403: void cBuildingListDrawer::drawStructureSize(int structureId, int x, int y)`; `427: bool cBuildingListDrawer::isOverItemCoordinates_Boolean(int x, int y, int drawX, int drawY)`
- Итог: совпало

## 4. fork-hunks-1.tsv, строка 30
- Утверждение: FORK1 `cMessageDrawer::createMessageBarBmp`, участок 233-266; PORT `src/drawers/cMessageDrawer.cpp@832c953:173-195`, `cMessageDrawer::createMessageBarBmp`.
- Команда FORK1: `git -C C:/Users/Slaven/Projects/DUNE show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMessageDrawer.cpp | sed -n '230,266p'`
- Вывод FORK1 (выдержка): `230: void cMessageDrawer::createMessageBarBmp(int desiredWidth)`
- Команда PORT: `git -C C:/Users/Slaven/Projects/DUNE show 832c953a94a632d57872349013f7ed1a37434715:src/drawers/cMessageDrawer.cpp | sed -n '173,195p'`
- Вывод PORT (выдержка): `173: void cMessageDrawer::createMessageBarBmp(int desiredWidth)`
- Итог: совпало

## 5. fork-hunks-1.tsv, строка 40
- Утверждение: FORK1 `cSideBarDrawer::cSideBarDrawer` и `cSideBarDrawer::~cSideBarDrawer`, участок 1-56; PORT `src/drawers/cSideBarDrawer.cpp@832c953:36-44` (конструктор) и `54-61` (деструктор).
- Команда FORK1: `git -C C:/Users/Slaven/Projects/DUNE show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp | sed -n '1,56p'`
- Вывод FORK1 (выдержка): `21: cSideBarDrawer::cSideBarDrawer(GameContext *ctx, cPlayer *player) :`; `48: cSideBarDrawer::~cSideBarDrawer()`
- Команда PORT: `git -C C:/Users/Slaven/Projects/DUNE show 832c953a94a632d57872349013f7ed1a37434715:src/drawers/cSideBarDrawer.cpp | sed -n '36,44p;54,61p'`
- Вывод PORT (выдержка): `36: cSideBarDrawer::cSideBarDrawer(GameContext *ctx, cPlayer *player, sGameServices *services) :`; `54: cSideBarDrawer::~cSideBarDrawer()`
- Итог: совпало

## 6. fork-hunks-2.tsv, строка 3
- Утверждение: FORK1 `cDrawManager::cDrawManager`, участок 10-28; PORT `src/managers/cDrawManager.cpp@832c953:59-87`, `cDrawManager`.
- Команда FORK1: `git -C C:/Users/Slaven/Projects/DUNE show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp | sed -n '10,28p'`
- Вывод FORK1 (выдержка): `23: cDrawManager::cDrawManager(GameContext *ctx, cPlayer *thePlayer) :`
- Команда PORT: `git -C C:/Users/Slaven/Projects/DUNE show 832c953a94a632d57872349013f7ed1a37434715:src/managers/cDrawManager.cpp | sed -n '59,87p'`
- Вывод PORT (выдержка): `59: cDrawManager::cDrawManager(GameContext *ctx, cPlayer *thePlayer, sGameServices *services) :`
- Итог: совпало

## 7. fork-hunks-2.tsv, строка 11
- Утверждение: FORK1 `cDrawManager::getMessage`, участок 527-537; PORT `src/managers/cDrawManager.cpp@832c953:433-436`, `cDrawManager::getMessage`.
- Команда FORK1: `git -C C:/Users/Slaven/Projects/DUNE show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp | sed -n '527,537p'`
- Вывод FORK1 (выдержка): `530: std::string cDrawManager::getMessage() const`
- Команда PORT: `git -C C:/Users/Slaven/Projects/DUNE show 832c953a94a632d57872349013f7ed1a37434715:src/managers/cDrawManager.cpp | sed -n '433,436p'`
- Вывод PORT (выдержка): `433: std::string cDrawManager::getMessage() const`
- Итог: совпало

## 8. fork-hunks-2.tsv, строка 20
- Утверждение: FORK1 `cMapCamera::cMapCamera`, участок 41-47 (`src/map/cMapCamera.cpp`); PORT `src/gameobjects/map/cMapCamera.cpp@832c953:32-65`, `cMapCamera::cMapCamera`.
- Команда FORK1: `git -C C:/Users/Slaven/Projects/DUNE show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/map/cMapCamera.cpp | sed -n '37,47p'`
- Вывод FORK1 (выдержка): `37: cMapCamera::cMapCamera(cMap *theMap, float moveSpeedDrag, float moveSpeedBorderOrKeys, bool cameraEdgeMove) :`
- Команда PORT: `git -C C:/Users/Slaven/Projects/DUNE show 832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/map/cMapCamera.cpp | sed -n '32,65p'`
- Вывод PORT (выдержка): `32: cMapCamera::cMapCamera(cMap *theMap, float moveSpeedDrag, float moveSpeedBorderOrKeys, bool cameraEdgeMove, cGameSettings* gameSettings, cMouse* mouse) :`
- Итог: совпало

## 9. fork-hunks-2.tsv, строка 36
- Утверждение: FORK1 `cBuildingListFactory::initializeList`, участок 46-59; PORT `src/sidebar/cBuildingListFactory.cpp@832c953:36-105`, `cBuildingListFactory::initializeList`.
- Команда FORK1: `git -C C:/Users/Slaven/Projects/DUNE show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/sidebar/cBuildingListFactory.cpp | sed -n '39,59p'`
- Вывод FORK1 (выдержка): `39: void cBuildingListFactory::initializeList(cBuildingList *list, eListType listType)`
- Команда PORT: `git -C C:/Users/Slaven/Projects/DUNE show 832c953a94a632d57872349013f7ed1a37434715:src/sidebar/cBuildingListFactory.cpp | sed -n '36,105p'`
- Вывод PORT (выдержка): `36: void cBuildingListFactory::initializeList(cBuildingList *list, eListType listType)`
- Итог: совпало

## 10. fork-hunks-2.tsv, строка 43
- Утверждение: FORK1 `cBuildingListUpdater::onStructureDestroyed`, участок 436-450; PORT `src/sidebar/cBuildingListUpdater.cpp@832c953:494-543`, `cBuildingListUpdater::onStructureDestroyed`.
- Команда FORK1: `git -C C:/Users/Slaven/Projects/DUNE show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/sidebar/cBuildingListUpdater.cpp | sed -n '429,450p'`
- Вывод FORK1 (выдержка): `429: void cBuildingListUpdater::onStructureDestroyed(int structureType)`
- Команда PORT: `git -C C:/Users/Slaven/Projects/DUNE show 832c953a94a632d57872349013f7ed1a37434715:src/sidebar/cBuildingListUpdater.cpp | sed -n '494,543p'`
- Вывод PORT (выдержка): `494: void cBuildingListUpdater::onStructureDestroyed(int structureType)`
- Итог: совпало

## 11. hud-images.tsv, строка 2
- Утверждение: литерал `outcome_victory_en.png` в `src/cGame_logic.cpp@9208dcf:2542` внутри `cGame::getHdOutcomeTexture(bool victory)`; вызов в `src/cGame_logic.cpp@9208dcf:2549`.
- Команда: `git -C C:/Users/Slaven/Projects/DUNE show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/cGame_logic.cpp | sed -n '2542p'`
- Вывод: `"outcome_victory_en.png",`
- Команда: `git -C C:/Users/Slaven/Projects/DUNE show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/cGame_logic.cpp | sed -n '2549p'`
- Вывод: `texture = loadHdUiTexture(` (в таблице вызов указан без имени функции)
- Команда: `git -C C:/Users/Slaven/Projects/DUNE show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/cGame_logic.cpp | grep -n "getHdOutcomeTexture"`
- Вывод: `2533:Texture *cGame::getHdOutcomeTexture(bool victory)`; `2560:    Texture *texture = getHdOutcomeTexture(victory);`
- Итог: совпало

## 12. hud-images.tsv, строка 10
- Утверждение: литерал `screenshot{}.bmp` в `src/cGame_logic.cpp@9208dcf:1956`, функция `cGame::saveBmpScreenToDisk()`.
- Команда: `git -C C:/Users/Slaven/Projects/DUNE show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/cGame_logic.cpp | sed -n '1956p'`
- Вывод: `    std::string name = std::format("screenshot{}.bmp",m_screenshot);`
- Команда: `git -C C:/Users/Slaven/Projects/DUNE show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/cGame_logic.cpp | grep -n "saveBmpScreenToDisk"`
- Вывод: `1942:void cGame::saveBmpScreenToDisk()`
- Итог: совпало

## 13. camera-mouse.tsv, строка 2
- Утверждение: FORK1 `cMapCamera::cMapCamera(...)`, `src/map/cMapCamera.cpp@9208dcf:37-64`; формула окна: ширина = screenW − SidebarWidth, высота = screenH − TopBarHeight (строки 49-53); `calibrate` делит на zoom level (строки 122-123).
- Команда: `git -C C:/Users/Slaven/Projects/DUNE show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/map/cMapCamera.cpp | sed -n '37p'`
- Вывод: `37: cMapCamera::cMapCamera(cMap *theMap, float moveSpeedDrag, float moveSpeedBorderOrKeys, bool cameraEdgeMove) :`
- Команда: `git -C C:/Users/Slaven/Projects/DUNE show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/map/cMapCamera.cpp | sed -n '49,53p'`
- Вывод: `49:     m_windowWidth= game.m_screenW - widthOfSidebar;`; `50:     m_windowHeight= game.m_screenH - m_heightOfTopBar;`; `52:     m_viewportWidth=m_windowWidth;`; `53:     m_viewportHeight=m_windowHeight;`
- Команда: `git -C C:/Users/Slaven/Projects/DUNE show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/map/cMapCamera.cpp | sed -n '117p;122,123p'`
- Вывод: `117: void cMapCamera::calibrate()`; `122:     m_viewportWidth = divideByZoomLevel(m_windowWidth);`; `123:     m_viewportHeight = divideByZoomLevel(m_windowHeight);`
- Итог: совпало (`widthOfSidebar` в строке 46 инициализирован как `cSideBar::SidebarWidth`, по выводе 37-47)

## 14. camera-mouse.tsv, строка 5
- Утверждение: FORK1 `cGameControlsContext::updateMouseCell(...)`, `src/controls/cGameControlsContext.cpp@9208dcf:48-72`: вызов `cellFromScreen(x,y)` при попадании в поле боя.
- Команда: `git -C C:/Users/Slaven/Projects/DUNE show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/controls/cGameControlsContext.cpp | sed -n '46,73p'`
- Вывод (выдержка): `46: void cGameControlsContext::updateMouseCell(const cPoint &coords)`; `48:     if (coords.y < cSideBar::TopBarHeight) {`; `54:     if (drawManager->getCommandBarDrawer()->isMouseOver(coords)) {`; `60:     if (drawManager->getMiniMapDrawer()->isMouseOver()) {`; `66:     if (coords.x > (game.m_screenW - cSideBar::SidebarWidth)) {`; `72:         m_mouseCell = getMouseCellFromScreen(coords.x, coords.y);`
- Итог: не совпало. Таблица утверждает вызов `cellFromScreen(x,y)`; в выводе (строка 72) вызов `getMouseCellFromScreen(coords.x, coords.y)`. Совпадают функция, проверки TopBarHeight, command bar, minimap и sidebar; расходится имя вызова в последней ветке.

## 15. camera-mouse.tsv, строка 11
- Утверждение: PORT `cMouse::boxSelectLogic(...)`, `src/controls/cMouse.cpp@832c953:279-306`; конец выделения по x ограничен `screenW − SidebarWidth − 1`, по y — `TopBarHeight` (строки 288-294).
- Команда: `git -C C:/Users/Slaven/Projects/DUNE show 832c953a94a632d57872349013f7ed1a37434715:src/controls/cMouse.cpp | sed -n '279,306p'`
- Вывод (выдержка): `279: void cMouse::boxSelectLogic(int mouseCell)`; `288:             if (m_coords.x > m_settings->getScreenW() - cSideBar::SidebarWidth) {`; `289:                 m_mouseCoX2 = m_settings->getScreenW() - cSideBar::SidebarWidth - 1;`; `293:             if (m_mouseCoY2 < cSideBar::TopBarHeight) {`; `294:                 m_mouseCoY2 = cSideBar::TopBarHeight;`
- Итог: совпало

Итог: совпало 14 из 15. Не совпало: № 14 (camera-mouse.tsv, строка 5), различие в имени вызова `cellFromScreen` и `getMouseCellFromScreen`.
