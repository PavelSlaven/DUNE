# Сверка помощника 4

Для каждой сверки ниже указаны таблица и номер строки в ней; строка таблицы приведена дословно. Каждую команду Git выполнил отдельно с заданной ревизией и экспортированным PATH.

## Таблицы помощника 1

### 1. Объявление **m_currentState**

**Таблица и строка:** **access.tsv**, строка 3.

~~~text
currentState	src/debug/UiAuditAccess.cpp@9208dcf:47-50	m_currentState	src/debug/UiAuditAccess.cpp@9208dcf:49	src/cGame.h@9208dcf:382: cGameState *m_currentState;	src/game/cGame.h@4aa980e:228: cGameState *m_currentState;; src/game/cGame_logic.cpp@4aa980e:136: return m_currentState && m_currentState->isKeyboardCapturedByUi();; src/game/cGame_logic.cpp@4aa980e:152: m_currentState = nullptr;; src/game/cGame_logic.cpp@4aa980e:387: m_currentState = nullptr;; src/game/cGame_logic.cpp@4aa980e:562: m_currentState->draw();
~~~

Проверяемый факт: строка 382 файла **src/cGame.h** в FORK1 объявляет **m_currentState** как указатель на **cGameState**.

Команда:

~~~sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/cGame.h | sed -n '382p'
~~~

Дословный stdout:

~~~text
    cGameState *m_currentState;
~~~

Результат: совпало.

### 2. Объявление **prepareMentatToTellAboutHouse**

**Таблица и строка:** **access.tsv**, строка 7.

~~~text
prepareTellHouse	src/debug/UiAuditAccess.cpp@9208dcf:67-70	prepareMentatToTellAboutHouse	src/debug/UiAuditAccess.cpp@9208dcf:69	src/cGame.h@9208dcf:257: void prepareMentatToTellAboutHouse(int house);	src/game/cGame.h@4aa980e:163: void prepareMentatToTellAboutHouse(int house);; src/game/cGame_logic.cpp@4aa980e:225: prepareMentatToTellAboutHouse(house);; src/game/cGame_logic.cpp@4aa980e:1250: void cGame::prepareMentatToTellAboutHouse(int house)
~~~

Проверяемый факт: строка 257 файла **src/cGame.h** в FORK1 объявляет метод **prepareMentatToTellAboutHouse(int house)**.

Команда:

~~~sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/cGame.h | sed -n '257p'
~~~

Дословный stdout:

~~~text
    void prepareMentatToTellAboutHouse(int house);
~~~

Результат: совпало.

### 3. Вызов **setViewportPosition** в **aimCamera**

**Таблица и строка:** **access-helpers.tsv**, строка 3.

~~~text
aimCamera	src/debug/UiAuditAccess.cpp@9208dcf:425-447	setViewportPosition	src/debug/UiAuditAccess.cpp@9208dcf:427	src/map/cMapCamera.cpp@9208dcf:199: void cMapCamera::setViewportPosition(int x, int y)	src/gameobjects/map/cMapCamera.cpp@4aa980e:216: void cMapCamera::setViewportPosition(int x, int y); src/gameobjects/map/cMapCamera.cpp@4aa980e:241: setViewportPosition(static_cast<int>(bookmark.x), static_cast<int>(bookmark.y));; src/gameobjects/map/cMapCamera.h@4aa980e:214: void setViewportPosition(int x, int y);
~~~

Проверяемый факт: в диапазоне **aimCamera** строка 427 вызывает **mapCamera->setViewportPosition** с координатами, умноженными на **kTile**.

Команда:

~~~sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditAccess.cpp | sed -n '425,447p'
~~~

Дословный stdout:

~~~text
bool aimCamera(cGame &game, int startColumn, int startRow, MapView &view, bool relaxed)
{
    mapCamera->setViewportPosition(startColumn * kTile, startRow * kTile);
    if (mapCamera->getViewportStartX() != startColumn * kTile || mapCamera->getViewportStartY() != startRow * kTile) {
        return false;
    }
    const int tile = static_cast<int>(mapCamera->factorZoomLevel(kTile));
    if (tile <= 0) {
        return false;
    }
    view.firstColumn = startColumn;
    view.firstRow = startRow;
    view.columns = game.m_mapViewport->getWidth() / tile;
    view.rows = game.m_mapViewport->getHeight() / tile;
    if (relaxed) {
        // On a canvas wider than the map the view cannot stay inside the map, so it is cut to the map.
        view.columns = std::min(view.columns, global_map.getWidth() - view.firstColumn - 3);
        view.rows = std::min(view.rows, global_map.getHeight() - view.firstRow - 3);
    }
    return view.columns >= 8 && view.rows >= 8 &&
           view.firstColumn + view.columns + 2 < global_map.getWidth() &&
           view.firstRow + view.rows + 2 < global_map.getHeight();
}
~~~

Результат: совпало.

### 4. Сопоставление **ListBuild** в **listForKind**

**Таблица и строка:** **access-helpers.tsv**, строка 117.

~~~text
listForKind	src/debug/UiAuditAccess.cpp@9208dcf:765-776	LIST_CONSTYARD	src/debug/UiAuditAccess.cpp@9208dcf:768	src/include/enums.h@9208dcf:195: LIST_CONSTYARD,	src/context/cInfoContextCreator.cpp@4aa980e:1169: upgradeInfos[UPGRADE_TYPE_CONSTYARD_SLAB4].providesTypeList = eListType::LIST_CONSTYARD;; src/context/cInfoContextCreator.cpp@4aa980e:1185: upgradeInfos[UPGRADE_TYPE_CONSTYARD_RTURRET].providesTypeList = eListType::LIST_CONSTYARD;; src/controls/mousestates/cMousePlaceState.cpp@4aa980e:81: cBuildingListItem *itemToPlace = m_player->getSideBar()->getList(eListType::LIST_CONSTYARD)->getItemToPlace();; src/drawers/cBuildingListDrawer.cpp@4aa980e:110: if (listIDToDraw == eListTypeAsInt(eListType::LIST_CONSTYARD)) {; src/drawers/cBuildingListDrawer.cpp@4aa980e:250: list->isType(eListType::LIST_CONSTYARD) &&
~~~

Проверяемый факт: **listForKind** возвращает **eListType::LIST_CONSTYARD** для **uiaudit::GameKind::ListBuild**.

Команда:

~~~sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditAccess.cpp | sed -n '765,776p'
~~~

Дословный stdout:

~~~text
eListType listForKind(int kind)
{
    switch (kind) {
        case uiaudit::GameKind::ListBuild: return eListType::LIST_CONSTYARD;
        case uiaudit::GameKind::ListInfantry: return eListType::LIST_FOOT_UNITS;
        case uiaudit::GameKind::ListVehicles: return eListType::LIST_UNITS;
        case uiaudit::GameKind::ListStarport: return eListType::LIST_STARPORT;
        case uiaudit::GameKind::ListPalace: return eListType::LIST_PALACE;
        case uiaudit::GameKind::ListUpgrades: return eListType::LIST_UPGRADES;
        default: return eListType::LIST_NONE;
    }
}
~~~

Результат: совпало.

## Таблицы помощника 2

### 5. Объявление дружбы в **MusicController.h**

**Таблица и строка:** **friends.tsv**, строка 2.

~~~text
src/audio/MusicController.h@9208dcf:25	MusicController	нет
~~~

Проверяемый факт: строка 25 файла **src/audio/MusicController.h** в FORK1 содержит объявление **friend class UiAuditAccess**.

Команда:

~~~sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/audio/MusicController.h | sed -n '25p'
~~~

Дословный stdout:

~~~text
    friend class UiAuditAccess;
~~~

Результат: совпало.

### 6. Объявление дружбы в **cCommandBarDrawer.h**

**Таблица и строка:** **friends.tsv**, строка 6.

~~~text
src/drawers/cCommandBarDrawer.h@9208dcf:16	cCommandBarDrawer	нет
~~~

Проверяемый факт: строка 16 файла **src/drawers/cCommandBarDrawer.h** в FORK1 содержит объявление **friend class UiAuditAccess**.

Команда:

~~~sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cCommandBarDrawer.h | sed -n '16p'
~~~

Дословный stdout:

~~~text
    friend class UiAuditAccess;
~~~

Результат: совпало.

### 7. Проверка включения аудита в **cCommandBarDrawer::draw**

**Таблица и строка:** **missing-hooks.tsv**, строка 2.

~~~text
src/drawers/cCommandBarDrawer.cpp@9208dcf:100	cCommandBarDrawer::draw	src/drawers/cCommandBarDrawer.cpp@9208dcf:97-124	{ ⏎     rebuildLayout(); ⏎     if (uiaudit::isEnabled()) { ⏎         uiaudit::recordArea("command-bar", m_panelRect.getX(), m_panelRect.getY(), m_panelRect.getWidth(), m_panelRect.getHeight()); ⏎         UiAuditAccess::recordCommandBarClicks(*this);	4aa980e36ee7a8ff0e651ce10c4f55869d86f08d:src/controls/cMouse.cpp:269:        // when mouse is deviating from this coordinate, draw a line; 4aa980e36ee7a8ff0e651ce10c4f55869d86f08d:src/controls/cMouse.cpp:355:void cMouse::draw(); 4aa980e36ee7a8ff0e651ce10c4f55869d86f08d:src/controls/cMouse.h:97:    void draw();; 4aa980e36ee7a8ff0e651ce10c4f55869d86f08d:src/drawers/CreditsDrawer.cpp:194:        // always 'add' here, the draw routine knows how to handle this for up/down movement.; 4aa980e36ee7a8ff0e651ce10c4f55869d86f08d:src/drawers/CreditsDrawer.cpp:213: * Create bitmap to draw credits	m_panelRect: нет | getX: 4aa980e36ee7a8ff0e651ce10c4f55869d86f08d:src/controls/cMouse.cpp:225:    return cRectangle::isWithin(getX(), getY(), x, y, width, height);; 4aa980e36ee7a8ff0e651ce10c4f55869d86f08d:src/controls/cMouse.cpp:231:    return rectangle->isPointWithin(getX(), getY());; 4aa980e36ee7a8ff0e651ce10c4f55869d86f08d:src/controls/cMouse.cpp:414:    return cPoint(getX(), getY());; 4aa980e36ee7a8ff0e651ce10c4f55869d86f08d:src/controls/cMouse.h:65:    int getX() {; 4aa980e36ee7a8ff0e651ce10c4f55869d86f08d:src/controls/cMouse.h:69:    int getY() {; 4aa980e36ee7a8ff0e651ce10c4f55869d86f08d:src/controls/mousestates/cMouseUnitsSelectedState.cpp:640:        int absoluteXCoordinate = m_context->getMapCamera()->getAbsMapMouseX(m_mouse->getX());; 4aa980e36ee7a8ff0e651ce10c4f55869d86f08d:src/controls/mousestates/cMouseUnitsSelectedState.cpp:641:        int absoluteYCoordinate = m_context->getMapCamera()->getAbsMapMouseY(m_mouse->getY()); | getWidth: 4aa980e36ee7a8ff0e651ce10c4f55869d86f08d:src/drawers/CreditsDrawer.cpp:230:        rect.getWidth(),; 4aa980e36ee7a8ff0e651ce10c4f55869d86f08d:src/drawers/CreditsDrawer.cpp:237:        rect.getWidth(),; 4aa980e36ee7a8ff0e651ce10c4f55869d86f08d:src/drawers/SDLDrawer.cpp:87:                         static_cast<float>(src_pos.getWidth()) * density,; 4aa980e36ee7a8ff0e651ce10c4f55869d86f08d:src/drawers/SDLDrawer.cpp:125:    renderRectFillColor(rect.getX(),rect.getY(), rect.getWidth(), rect.getHeight(),; 4aa980e36ee7a8ff0e651ce10c4f55869d86f08d:src/drawers/SDLDrawer.cpp:131:    renderRectColor(rect.getX(),rect.getY(), rect.getWidth(), rect.getHeight(),r,g,b,opacity); | recordCommandBarClicks: нет
~~~

Проверяемый факт: строка 100 **cCommandBarDrawer.cpp** проверяет **uiaudit::isEnabled()**.

Команда:

~~~sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cCommandBarDrawer.cpp | sed -n '100p'
~~~

Дословный stdout:

~~~text
    if (uiaudit::isEnabled()) {
~~~

Результат: совпало.

### 8. Проверка включения аудита в **cUnit::draw_spice**

**Таблица и строка:** **missing-hooks.tsv**, строка 9.

~~~text
src/gameobjects/units/cUnit.cpp@9208dcf:581	cUnit::draw_spice	src/gameobjects/units/cUnit.cpp@9208dcf:570-593	    int w = healthBar(width_x, iCredits, max); ⏎  ⏎     if (uiaudit::isEnabled()) { ⏎         uiaudit::recordUnitLabel("spice", iID, iType, drawx, drawy, static_cast<int>(width_x), height_y, uiaudit::Rect{visual.getX(), visual.getY(), visual.getWidth(), visual.getHeight()}); ⏎     }	4aa980e36ee7a8ff0e651ce10c4f55869d86f08d:src/drawers/cUnitDrawer.cpp:48:void cUnitDrawer::draw_spice(); 4aa980e36ee7a8ff0e651ce10c4f55869d86f08d:src/drawers/cUnitDrawer.h:31:    void draw_spice();; 4aa980e36ee7a8ff0e651ce10c4f55869d86f08d:src/gameobjects/map/cMap.cpp:904:            unitDrawer.draw_spice();	iID: 4aa980e36ee7a8ff0e651ce10c4f55869d86f08d:src/controls/mousestates/cMousePlaceState.cpp:137:                    int iID = idOfStructureAtCell;; 4aa980e36ee7a8ff0e651ce10c4f55869d86f08d:src/controls/mousestates/cMousePlaceState.cpp:139:                    if (m_context->getObjects()->getStructures()[iID]->getOwner() == m_player->getId()) {; 4aa980e36ee7a8ff0e651ce10c4f55869d86f08d:src/drawers/cPlaceItDrawer.cpp:107:                    int iID = idOfStructureAtCell;; 4aa980e36ee7a8ff0e651ce10c4f55869d86f08d:src/drawers/cPlaceItDrawer.cpp:109:                    if (m_objects->getStructures()[iID]->getOwner() == m_player->getId()) {; 4aa980e36ee7a8ff0e651ce10c4f55869d86f08d:src/drawers/cUnitDrawer.cpp:328:        textDrawer->drawText(m_unit.draw_x(), m_unit.draw_y(), Color{255, 255, 255,ShadowTrans}, std::format("{}", m_unit.iID)); | iType: 4aa980e36ee7a8ff0e651ce10c4f55869d86f08d:src/context/AudioContext.cpp:84:void AudioContext::playMusicByTypeForStateTransition(eMusicType iType, int humanHouse); 4aa980e36ee7a8ff0e651ce10c4f55869d86f08d:src/context/AudioContext.cpp:86:    if (m_settings->getMusicType() != iType) {; 4aa980e36ee7a8ff0e651ce10c4f55869d86f08d:src/context/AudioContext.cpp:88:        playMusicByType(iType, false, false, humanHouse);; 4aa980e36ee7a8ff0e651ce10c4f55869d86f08d:src/context/AudioContext.cpp:92:bool AudioContext::playMusicByType(eMusicType iType, bool triggerWithVoice, bool isCurrentlyPlayingMission, int humanHouse);; 4aa980e36ee7a8ff0e651ce10c4f55869d86f08d:src/context/AudioContext.cpp:94:    Logger::info(COMP_SOUND, "AudioContext::playMusicByType", "iType = {}. triggerWithVoice = {}", musicTypeName(iType), triggerWithVoice);; 4aa980e36ee7a8ff0e651ce10c4f55869d86f08d:src/gameobjects/units/cUnit.cpp:580:    int iType = 0;;
~~~

Проверяемый факт: строка 581 **cUnit.cpp** проверяет **uiaudit::isEnabled()** перед записью метки для специи.

Команда:

~~~sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/gameobjects/units/cUnit.cpp | sed -n '581p'
~~~

Дословный stdout:

~~~text
    if (uiaudit::isEnabled()) {
~~~

Результат: совпало.

## Таблицы помощника 3

### 9. Условие завершения **pause**

**Таблица и строка:** **scene-functions.tsv**, строка 3.

~~~text
pause(int frames)	src/debug/UiAuditScenes.cpp@9208dcf:25-32	—	—	—	—	—
~~~

Проверяемый факт: **pause** увеличивает **g_wait**; когда значение становится больше **frames**, функция сбрасывает его и возвращает **true**.

Команда:

~~~sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '25,32p'
~~~

Дословный stdout:

~~~text
bool pause(int frames)
{
    if (++g_wait > frames) {
        g_wait = 0;
        return true;
    }
    return false;
}
~~~

Результат: совпало.

### 10. Значение **REGSTATE_SELECT_NEXT_CONQUEST**

**Таблица и строка:** **scene-functions.tsv**, строка 40.

~~~text
readyRegionSelect()	src/debug/UiAuditScenes.cpp@9208dcf:346-352	regionState	REGSTATE_SELECT_NEXT_CONQUEST	src/debug/UiAuditScenes.cpp@9208dcf:348	src/gamestates/cSelectYourNextConquestState.h@9208dcf:22: REGSTATE_SELECT_NEXT_CONQUEST,	4aa980e36ee7a8ff0e651ce10c4f55869d86f08d:src/gamestates/cSelectYourNextConquestState.cpp:317:            state = REGSTATE_SELECT_NEXT_CONQUEST;; 4aa980e36ee7a8ff0e651ce10c4f55869d86f08d:src/gamestates/cSelectYourNextConquestState.cpp:322:    if (state == REGSTATE_SELECT_NEXT_CONQUEST) {; 4aa980e36ee7a8ff0e651ce10c4f55869d86f08d:src/gamestates/cSelectYourNextConquestState.cpp:359:    else if (state == eRegionState::REGSTATE_SELECT_NEXT_CONQUEST) {; 4aa980e36ee7a8ff0e651ce10c4f55869d86f08d:src/gamestates/cSelectYourNextConquestState.cpp:852:    if (regionPiece.bSelectable && state == eRegionState::REGSTATE_SELECT_NEXT_CONQUEST) {; 4aa980e36ee7a8ff0e651ce10c4f55869d86f08d:src/gamestates/cSelectYourNextConquestState.cpp:1016:    if (state != eRegionState::REGSTATE_SELECT_NEXT_CONQUEST) return;
~~~

Проверяемый факт: строка 22 **src/gamestates/cSelectYourNextConquestState.h** объявляет **REGSTATE_SELECT_NEXT_CONQUEST**.

Команда:

~~~sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/gamestates/cSelectYourNextConquestState.h | sed -n '22p'
~~~

Дословный stdout:

~~~text
    REGSTATE_SELECT_NEXT_CONQUEST,   // here the user may select the next area to attack
~~~

Результат: совпало.

### 11. Разбор аргументов в **main.cpp**

**Таблица и строка:** **runtime.tsv**, строка 8.

~~~text
Вызов из main.cpp	src/main.cpp@4aa980e:94	int parseResult = handleArg.handleArguments(argc, argv, settings.get());
~~~

Проверяемый факт: в строке 94 **main.cpp** результат **handleArg.handleArguments(argc, argv, settings.get())** присваивается переменной **parseResult**.

Команда:

~~~sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show 4aa980e36ee7a8ff0e651ce10c4f55869d86f08d:src/main.cpp | sed -n '94p'
~~~

Дословный stdout:

~~~text
        int parseResult = handleArg.handleArguments(argc, argv, settings.get());
~~~

Результат: совпало.

### 12. Вызов SDL для пути пользовательских настроек

**Таблица и строка:** **runtime.tsv**, строка 14.

~~~text
PreferencesPath::directory()	src/game/PreferencesPath.cpp@4aa980e:28-40	    28	std::optional<std::filesystem::path> directory() |     29	{ |     30	    char *preferencePath = SDL_GetPrefPath("D2TM", "Dune II - The Maker"); |     31	    if (preferencePath == nullptr) { |     32	        Logger::warn(COMP_INIT, "PreferencesPath", "Could not get the user data directory: {}", SDL_GetError()); |     33	        return std::nullopt; |     34	    } |     35	    // SDL_GetPrefPath returns UTF-8, a plain char* path would be read in the ANSI code page on Windows |     36	    const std::string_view utf8(preferencePath); |     37	    std::filesystem::path result(std::u8string(utf8.begin(), utf8.end())); |     38	    SDL_free(preferencePath); |     39	    return result; |     40	}
~~~

Проверяемый факт: строка 30 **PreferencesPath.cpp** вызывает **SDL_GetPrefPath** с идентификаторами **"D2TM"** и **"Dune II - The Maker"**.

Команда:

~~~sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show 4aa980e36ee7a8ff0e651ce10c4f55869d86f08d:src/game/PreferencesPath.cpp | sed -n '30p'
~~~

Дословный stdout:

~~~text
    char *preferencePath = SDL_GetPrefPath("D2TM", "Dune II - The Maker");
~~~

Результат: совпало.

