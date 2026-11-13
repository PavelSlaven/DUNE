# Сверка выборки

### Факт из 1.md: перечисление `eListType` содержит семь вариантов

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show af6a2e1e4f2baba4ff52e4812c7dc798cfd46aaf:src/include/enums/ListEnums.h | nl -ba | sed -n '3,11p'
```

```text
     3	enum class eListType {
     4	    LIST_NONE,  // no list (empty list)
     5	    LIST_CONSTYARD,
     6	    LIST_FOOT_UNITS, // infantry, soldier, trooper, troopers, etc.
     7	    LIST_UNITS, // quad, trike, tanks, air units
     8	    LIST_STARPORT, // special list to order stuff
     9	    LIST_PALACE, // REMOVE? (ie super weapon icon should always show top left/right?)
    10	    LIST_UPGRADES, // possible sUpgradeInfo
    11	};
```
Код выхода: 0
Итог: совпало.

### Факт из 1.md: `eListTypeAsInt` сопоставляет `LIST_UPGRADES` числу 6

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show af6a2e1e4f2baba4ff52e4812c7dc798cfd46aaf:src/include/enums/ListEnums.h | nl -ba | sed -n '44,63p'
```

```text
    44	inline int eListTypeAsInt(eListType value)
    45	{
    46	    switch (value) {
    47	        case eListType::LIST_NONE:
    48	            return 0;
    49	        case eListType::LIST_CONSTYARD:
    50	            return 1;
    51	        case eListType::LIST_FOOT_UNITS:
    52	            return 2;
    53	        case eListType::LIST_UNITS:
    54	            return 3;
    55	        case eListType::LIST_STARPORT:
    56	            return 4;
    57	        case eListType::LIST_PALACE:
    58	            return 5;
    59	        case eListType::LIST_UPGRADES:
    60	            return 6;
    61	    }
    62	    return 0;
    63	}
```
Код выхода: 0
Итог: совпало.

### Факт из 2.md: полоса здоровья строения рисуется при наведении мыши на строение

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show af6a2e1e4f2baba4ff52e4812c7dc798cfd46aaf:src/drawers/cStructureDrawer.cpp | nl -ba | sed -n '128,137p'
```

```text
   128	void cStructureDrawer::drawStructuresHealthBars()
   129	{
   130	    cGameControlsContext *context = m_objects->getPlayer(HUMAN)->getGameControlsContext();
   131	
   132	    // DRAW HEALTH
   133	    if (context->isMouseOverStructure()) {
   134	        int i = context->getIdOfStructureWhereMouseHovers();
   135	        drawStructureHealthBar(i);
   136	    }
   137	}
```
Код выхода: 0
Итог: совпало.
Проверка функции `cStructureDrawer::drawStructuresHealthBars`: последняя строка тела, 137, целиком равна `}`; между заголовком и ней нет строки, целиком равной `}`.

### Факт из 3.md: `cPlaceItDrawer::setPlayer` присваивает указатель `m_player`

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show af6a2e1e4f2baba4ff52e4812c7dc798cfd46aaf:src/drawers/cPlaceItDrawer.h | nl -ba | sed -n '30,55p'
```

```text
    30	class cPlaceItDrawer {
    31	public:
    32	    explicit cPlaceItDrawer(GameContext *ctx, cPlayer *thePlayer, cStructureUtils *structureUtils);
    33	
    34	    ~cPlaceItDrawer();
    35	
    36	    void setPlayer(cPlayer *pPlayer) { m_player = pPlayer; }
    37	    void serviceInit(sGameServices* services);
    38	
    39	    void draw(cBuildingListItem *itemToPlace, int mouseCell);
    40	
    41	protected:
    42	    void drawStructureIdAtMousePos(cBuildingListItem *itemToPlace, int mouseCell);
    43	
    44	    void drawStatusOfStructureAtCell(cBuildingListItem *itemToPlace, int mouseCell);
    45	
    46	private:
    47	    cStructureUtils* m_structureUtils = nullptr;
    48	    cPlayer *m_player;
    49	    GameContext *m_ctx;
    50	    SDLDrawer *m_sdlDrawer;
    51	    Graphics *m_gfxdata;
    52	    cGameObjectContext* m_objects = nullptr;
    53	    cInfoContext* m_infos = nullptr;
    54	    cMapCamera* m_mapCamera = nullptr;
    55	};
```
Код выхода: 0
Итог: совпало.

### Факт из 3.md: рисование размещения прекращается вне состояния `MOUSESTATE_PLACE`

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show af6a2e1e4f2baba4ff52e4812c7dc798cfd46aaf:src/managers/cDrawManager.cpp | nl -ba | sed -n '265,275p'
```

```text
   265	void cDrawManager::drawStructurePlacing()
   266	{
   267	    // TODO: move drawing this into mouse state draw function ??
   268	    if (m_player->isContextMouseState(eMouseState::MOUSESTATE_DEPLOY)) return;
   269	    if (!m_player->isContextMouseState(eMouseState::MOUSESTATE_PLACE)) return;
   270	
   271	    cBuildingListItem *itemToPlace = m_player->getSideBar()->getList(eListType::LIST_CONSTYARD)->getItemToPlace();
   272	    if (itemToPlace == nullptr) return;
   273	
   274	    m_placeitDrawer->draw(itemToPlace, m_player->getGameControlsContext()->getMouseCell());
   275	}
```
Код выхода: 0
Итог: совпало.

### Факт из 4.md: координаты рамки обновляются, если сдвиг по обеим осям больше четырёх пикселей

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show af6a2e1e4f2baba4ff52e4812c7dc798cfd46aaf:src/controls/cMouse.cpp | nl -ba | sed -n '279,306p'
```

```text
   279	void cMouse::boxSelectLogic(int mouseCell)
   280	{
   281	// When the mouse is pressed, we will check if the first coordinates are filled in
   282	    // if so, we will update the second coordinates. If the player holds his mouse we
   283	    // keep updating the second coordinates and create a rectangle to select units with.
   284	    if (m_mouseCoX1 > -1 && m_mouseCoY1 > -1) {
   285	        if (abs(m_coords.x - m_mouseCoX1) > 4 && abs(m_coords.y - m_mouseCoY1) > 4) {
   286	            // assign 2nd coordinates
   287	            m_mouseCoX2 = m_coords.x;
   288	            if (m_coords.x > m_settings->getScreenW() - cSideBar::SidebarWidth) {
   289	                m_mouseCoX2 = m_settings->getScreenW() - cSideBar::SidebarWidth - 1;
   290	            }
   291	
   292	            m_mouseCoY2 = m_coords.y;
   293	            if (m_mouseCoY2 < cSideBar::TopBarHeight) {
   294	                m_mouseCoY2 = cSideBar::TopBarHeight;
   295	            }
   296	        }
   297	
   298	        // Note that we have to fix up the coordinates when checking 'within border'
   299	        // for units (when X2 < X1 for example!)
   300	    }
   301	    else if (mouseCell > -1) {
   302	        // no first coordinates set, so do that here.
   303	        m_mouseCoX1 = m_coords.x;
   304	        m_mouseCoY1 = m_coords.y;
   305	    }
   306	}
```
Код выхода: 0
Итог: совпало.
Проверка функции `cMouse::boxSelectLogic`: последняя строка тела, 306, целиком равна `}`; между заголовком и ней нет строки, целиком равной `}`.

### Факт из 5.md: конструктор `cGame` создаёт `cNotificationArea`

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show af6a2e1e4f2baba4ff52e4812c7dc798cfd46aaf:src/game/cGame_logic.cpp | nl -ba | sed -n '149,168p'
```

```text
   149	cGame::cGame()
   150	{
   151	    m_state = -1;
   152	    m_nextState = -1;
   153	    m_currentState = nullptr;
   154	
   155	    m_windowed = false;
   156	    context = nullptr;
   157	    ctx = nullptr;
   158	    m_pauseWhenLosingFocus = false;
   159	
   160	    m_mapCamera = nullptr;
   161	    m_drawManager = nullptr;
   162	
   163	    m_cameraDragMoveSpeed=0.5f;
   164	    m_cameraBorderOrKeyMoveSpeed=0.5;
   165	    m_cameraEdgeMove = true;
   166	
   167	    m_notificationArea = std::make_unique<cNotificationArea>();
   168	
```
Код выхода: 0
Итог: совпало.

### Факт из 5.md: `cGame::init` очищает область уведомлений

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show af6a2e1e4f2baba4ff52e4812c7dc798cfd46aaf:src/game/cGame_logic.cpp | nl -ba | sed -n '378,393p'
```

```text
   378	void cGame::init()
   379	{
   380	    m_infoContext->initializeDefaultInfos();
   381	
   382	    auto map = m_gameObjectsContext->getMap();
   383	    map->setTerrainInfo(m_infoContext->getTerrainInfo());
   384	
   385	    m_gameSettings->m_drawFps = false;
   386	    m_nextState = -1;
   387	    m_missionWasWon = false;
   388	    m_currentState = nullptr;
   389	    m_gameSettings->m_playing = true;
   390	    m_gameSettings->m_skirmish = false;
   391	    m_notificationArea->clear();
   392	
   393	    setState(GAME_INITIALIZE);
```
Код выхода: 0
Итог: совпало.

### Факт из 6.md: описание строения включает разницу между выдаваемой и потребляемой мощностью

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show af6a2e1e4f2baba4ff52e4812c7dc798cfd46aaf:src/sidebar/cBuildingListItem.cpp | nl -ba | sed -n '397,431p'
```

```text
   397	std::string cBuildingListItem::getInfo()
   398	{
   399	    std::string msg;
   400	    int seconds = getTotalBuildTimeInMs() / 1000;
   401	    if (isBuilding()) {
   402	        int secondsInProgress = getProgressBuildTimeInMs() / 1000;
   403	        seconds -= secondsInProgress;
   404	    }
   405	
   406	    if (isTypeStructure()) {
   407	        s_StructureInfo structureType = getStructureInfo();
   408	        msg = std::format("${} | {} | {} Power | {} Secs", getBuildCost(), structureType.name, (structureType.power_give - structureType.power_drain), seconds);
   409	    }
   410	    else if (isTypeUnit()) {
   411	        s_UnitInfo unitType = getUnitInfo();
   412	        if (getBuildCost() > 0) {
   413	            msg = std::format("${} | {} | {} Secs", getBuildCost(), unitType.name, seconds);
   414	        }
   415	        else {
   416	            msg = std::format("{} | {} Secs", m_info->getUnitInfo(getBuildId()).name, seconds);
   417	        }
   418	    }
   419	    else if (isTypeUpgrade()) {
   420	        s_UpgradeInfo upgrade = getUpgradeInfo();
   421	        msg = std::format("UPGRADE: ${} | {} | {} Secs", getBuildCost(), upgrade.description, seconds);
   422	    }
   423	    else if (isTypeSpecial()) {
   424	        s_SpecialInfo special = getSpecialInfo();
   425	        msg = std::format("${} | {} | {} Secs", getBuildCost(), special.description, seconds);
   426	    }
   427	    else {
   428	        msg = "ERROR: UNKNOWN BUILD TYPE";
   429	    }
   430	    return msg;
   431	}
```
Код выхода: 0
Итог: совпало.
Проверка функции `cBuildingListItem::getInfo`: последняя строка тела, 431, целиком равна `}`; между заголовком и ней нет строки, целиком равной `}`.

### Факт из 7.md: `drawRallyPoint` прекращает работу при отсутствии выбранного строения, объекта или точки сбора

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show af6a2e1e4f2baba4ff52e4812c7dc798cfd46aaf:src/managers/cDrawManager.cpp | nl -ba | sed -n '223,252p'
```

```text
   223	void cDrawManager::drawRallyPoint()
   224	{
   225	    if (m_player->selected_structure < 0) return;
   226	    cAbstractStructure *theStructure = m_objects->getStructures()[m_player->selected_structure];
   227	    if (!theStructure) return;
   228	    int rallyPointCell = theStructure->getRallyPoint();
   229	    if (rallyPointCell < 0) return;
   230	
   231	    int drawX = m_mapCamera->getWindowXPositionFromCell(rallyPointCell);
   232	    int drawY = m_mapCamera->getWindowYPositionFromCell(rallyPointCell);
   233	
   234	    Texture *mouseMoveBitmap = m_gfxdata->getTexture(MOUSE_MOVE);
   235	
   236	    int rallyPointWidthScaled = m_mapCamera->factorZoomLevel(mouseMoveBitmap->w);
   237	    int rallyPointHeightScaled = m_mapCamera->factorZoomLevel(mouseMoveBitmap->h);
   238	    cRectangle dest = {drawX, drawY, rallyPointWidthScaled, rallyPointHeightScaled};
   239	    m_sdlDrawer->renderStrechFullSprite(m_gfxdata->getTexture(MOUSE_MOVE), dest);
   240	
   241	    int startX = theStructure->iDrawX() + m_mapCamera->factorZoomLevel(theStructure->getWidthInPixels() / 2);
   242	    int startY = theStructure->iDrawY() + m_mapCamera->factorZoomLevel(theStructure->getHeightInPixels() / 2);
   243	
   244	    int offset = (mouseMoveBitmap->w/2);
   245	    drawX = m_mapCamera->getWindowXPositionFromCellWithOffset(rallyPointCell, offset);
   246	    drawY = m_mapCamera->getWindowYPositionFromCellWithOffset(rallyPointCell, offset);
   247	
   248	    int endX = drawX;
   249	    int endY = drawY;
   250	
   251	    m_sdlDrawer->renderLine( startX, startY, endX, endY, m_player->getMinimapColor());
   252	}
```
Код выхода: 0
Итог: совпало.
Проверка функции `cDrawManager::drawRallyPoint`: последняя строка тела, 252, целиком равна `}`; между заголовком и ней нет строки, целиком равной `}`.

### Факт из 7.md: порядок рисования включает туман, открытые во тьме юниты, точку сбора, интерфейс и сообщение

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show af6a2e1e4f2baba4ff52e4812c7dc798cfd46aaf:src/managers/cDrawManager.cpp | nl -ba | sed -n '147,169p'
```

```text
   147	    m_structureDrawer->drawStructuresHealthBars();
   148	
   149	    m_mapDrawer->drawShroud();
   150	
   151	    // after the shroud: an attacker on a never explored cell would otherwise be painted over in black
   152	    m_objects->getMap()->drawRevealedUnitsInFog();
   153	
   154	    drawRallyPoint();
   155	
   156	    m_sdlDrawer->resetClippingFor();
   157	
   158	    // GUI
   159	    drawSidebar();
   160	
   161	    m_sdlDrawer->setClippingFor(0, cSideBar::TopBarHeight, m_mapCamera->getWindowWidth(), m_mapCamera->getWindowHeight() + cSideBar::TopBarHeight);
   162	    drawStructurePlacing();
   163	    m_sdlDrawer->resetClippingFor();
   164	
   165	    drawTopBarBackground();
   166	    drawCredits();
   167	
   168	    // THE MESSAGE
   169	    drawMessage();
```
Код выхода: 0
Итог: совпало.

### Факт из 8.md: `cGame::loadScenario` создаёт состояние брифинга вместо повторной загрузки сценария

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show af6a2e1e4f2baba4ff52e4812c7dc798cfd46aaf:src/game/cGame_logic.cpp | nl -ba | sed -n '1289,1300p'
```

```text
  1289	void cGame::loadScenario()
  1290	{
  1291	    if (!m_creatorState->hasState(eGameState::BRIEFING)) {
  1292	        // creating the state loads the scenario (see cMentatState constructor), loading again would duplicate it
  1293	        m_creatorState->getState(eGameState::BRIEFING);
  1294	        return;
  1295	    }
  1296	
  1297	    auto *pState = dynamic_cast<cMentatState *>(m_creatorState->getState(eGameState::BRIEFING));
  1298	    if (!pState) return; // state not yet created; prepareMentat() in the constructor will load the scenario
  1299	    pState->loadScenario(m_reinforcements.get());
  1300	}
```
Код выхода: 0
Итог: совпало.
