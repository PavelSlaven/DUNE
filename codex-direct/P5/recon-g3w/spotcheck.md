# Сверка помощника 4 — P5G3W

## Пункт 1 — headers.md

### src/game/MissionFlow.hpp@dc6e5ff:25-37

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/game/MissionFlow.hpp | nl -ba | sed -n '25,37p'
```

Вывод:

```text
    25	class MissionFlow {
    26	public:
    27	    using Callback = std::function<void()>;
    28	    using IntCallback = std::function<void(int)>;
    29	
    30	    MissionFlow(Callback init, Callback setWon, Callback setLost, Callback checkWinOrFail,
    31	                IntCallback jumpToSelectYourNextConquest, IntCallback goingToWinLoseBrief)
    32	        : m_init(std::move(init)),
    33	          m_setWon(std::move(setWon)),
    34	          m_setLost(std::move(setLost)),
    35	          m_checkWinOrFail(std::move(checkWinOrFail)),
    36	          m_jumpToSelectYourNextConquest(std::move(jumpToSelectYourNextConquest)),
    37	          m_goingToWinLoseBrief(std::move(goingToWinLoseBrief)) {
```

Итог: совпало.

### src/gameobjects/structures/cAbstractStructure.h@dc6e5ff:257-273

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/gameobjects/structures/cAbstractStructure.h | nl -ba | sed -n '257,273p'
```

Вывод:

```text
   257	    bool isValid();
   258	    bool needPowerToWork() const {
   259	        return getStructureInfo().needPowerToWork;
   260	    }
   261	    bool canAttackAirUnits() const {
   262	        return getStructureInfo().canAttackAirUnits;
   263	    }
   264	    bool canAttackGroundUnits() const {
   265	        return getStructureInfo().canAttackGroundUnits;
   266	    }
   267	
   268	    void setHeight(int height);
   269	    void setWidth(int width);
   270	    void setHitPoints(int hp);
   271	    void setCell(int cell);
   272	    void setOwner(int player); // set owner (player id) of structure
   273	    void setRallyPoint(int cell); // set rally point of structure
```

Итог: совпало.

### src/controls/cGameControlsContext.h@dc6e5ff:52-67

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/controls/cGameControlsContext.h | nl -ba | sed -n '52,67p'
```

Вывод:

```text
    52	class cGameControlsContext : public cInputObserver, cScenarioObserver {
    53	public:
    54	    explicit cGameControlsContext(cPlayer *player, cMouse *mouse);
    55	    ~cGameControlsContext() override;
    56	
    57	    void serviceInit(sGameServices *services);
    58	
    59	    cGameObjectContext *getObjects() const { return m_objects; }
    60	    cMapCamera *getMapCamera() const { return m_mapCamera; }
    61	    cGameSettings *getSettings() const { return m_settings; }
    62	    cDrawManager *getDrawManager() const { return m_drawManager; }
    63	    cEventEmitter *getEventEmitter() const { return m_eventEmitter; }
    64	    cStructureUtils *getStructureUtils() const { return m_structureUtils; }
    65	    cInfoContext *getInfos() const { return m_infos; }
    66	    AudioContext *getAudioContext() const { return m_audioContext; }
    67	    cRectangle *getMapViewport() const { return m_mapViewport; }
```

Итог: совпало.

### src/include/sGameServices.h@dc6e5ff:42-66

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/include/sGameServices.h | nl -ba | sed -n '42,66p'
```

Вывод:

```text
    42	struct sGameServices
    43	{
    44	    GameContext *ctx = nullptr;
    45	    cGameObjectContext *objects = nullptr;
    46	    cInfoContext *info = nullptr;
    47	    cGameSettings *settings = nullptr;
    48	    cMapCamera *mapCamera = nullptr;
    49	    cStructureUtils *structureUtils = nullptr;
    50	    cEventEmitter *eventEmitter = nullptr;
    51	    cDrawManager *drawManager = nullptr;
    52	    cRectangle *mapViewport = nullptr;
    53	    cReinforcements *reinforcements = nullptr;
    54	    cMouse *mouse = nullptr;
    55	    cMissionStatsCollector *missionStatsCollector = nullptr;
    56	    cGameConditionChecker *gameConditionChecker = nullptr;
    57	    cScreenShake *screenShake = nullptr;
    58	    cScreenFader *screenFader = nullptr;
    59	    CampaignProgress *campaignProgress = nullptr;
    60	    Texture *screenTexture = nullptr; // set in cGame::run(), before any state transition
    61	    GameStateTransition *stateTransitions = nullptr;
    62	    MentatFlow *mentatFlow = nullptr;
    63	    MissionFlow *missionFlow = nullptr;
    64	    ScenarioFlow *scenarioFlow = nullptr;
    65	    VideoFlow *videoFlow = nullptr;
    66	};
```

Итог: совпало.

## Пункт 2 — functions.md

### cGame::missionInit — src/game/cGame_logic.cpp@dc6e5ff:431-461

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/game/cGame_logic.cpp | nl -ba | sed -n '431,461p'
```

Вывод:

```text
   431	void cGame::missionInit()
   432	{
   433	    m_mapCamera->resetZoom();
   434	    m_mapCamera->resetViewportBookmarks();
   435	
   436	    m_gameConditionChecker->missionInit();
   437	
   438	    m_cScreenFader->inititialize();
   439	
   440	    m_screenShake->reset();
   441	
   442	    m_gameObjectsContext->getMap()->init(64, 64);
   443	    // @mira: while cMap is created beforce all, need to set up terrain before loading scenario, so we can use it in cIni::installGame() when loading map.
   444	    m_gameObjectsContext->getMap()->setTerrainInfo(m_infoContext->getTerrainInfo());
   445	
   446	    for (int i = 0; i < m_gameObjectsContext->getUnits()->size(); i++) {
   447	        m_gameObjectsContext->getUnit(i)->init(i);
   448	    }
   449	
   450	    for (auto& particle : m_gameObjectsContext->getParticles()) {
   451	        particle.init();
   452	    }
   453	
   454	    for (auto& bullet : m_gameObjectsContext->getBullets()) {
   455	        bullet.init();
   456	    }
   457	
   458	    m_players->initPlayers(true, m_gameSettings.get(), m_dataCampaign.get(), m_services.get());
   459	
   460	    m_drawManager->missionInit();
   461	}
```

Итог: совпало.

### cGame::transitionStateIfRequired — src/game/cGame_logic.cpp@dc6e5ff:1491-1503

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/game/cGame_logic.cpp | nl -ba | sed -n '1491,1503p'
```

Вывод:

```text
  1491	void cGame::transitionStateIfRequired()
  1492	{
  1493	    if (m_nextState > -1) {
  1494	        setState(m_nextState);
  1495	
  1496	        if (m_nextState == GAME_BRIEFING) {
  1497	            playMusicByType(eMusicType::BRIEFING);
  1498	            prepareMentatForPlayer();
  1499	        }
  1500	
  1501	        m_nextState = -1;
  1502	    }
  1503	}
```

Итог: совпало.

### cMapCamera::setViewportPosition — src/gameobjects/map/cMapCamera.cpp@dc6e5ff:216-220

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/gameobjects/map/cMapCamera.cpp | nl -ba | sed -n '216,220p'
```

Вывод:

```text
   216	void cMapCamera::setViewportPosition(int x, int y)
   217	{
   218	    jumpTo(x, y);
   219	    keepViewportWithinReasonableBounds();
   220	}
```

Итог: совпало.

### cTimeManager::onWindowFocusLost — src/game/cTimeManager.cpp@dc6e5ff:94-97

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/game/cTimeManager.cpp | nl -ba | sed -n '94,97p'
```

Вывод:

```text
    94	void cTimeManager::onWindowFocusLost()
    95	{
    96	    m_focusLostTime = SDL_GetTicks();
    97	}
```

Итог: совпало.

## Пункт 3 — ui.md

### cSideBarDrawer::draw — src/drawers/cSideBarDrawer.cpp@dc6e5ff:98-101

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/drawers/cSideBarDrawer.cpp | nl -ba | sed -n '98,101p'
```

Вывод:

```text
    98	void cSideBarDrawer::draw()
    99	{
   100	    drawHdSidebar();
   101	}
```

Итог: совпало.

### cBuildingListDrawer::getLayout — src/drawers/cBuildingListDrawer.cpp@dc6e5ff:833-842

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/drawers/cBuildingListDrawer.cpp | nl -ba | sed -n '833,842p'
```

Вывод:

```text
   833	HudLayout cBuildingListDrawer::getLayout(cBuildingList *list) const
   834	{
   835	    const bool reserveOrderArea =
   836	        list != nullptr && list->getType() == eListType::LIST_STARPORT;
   837	    return HudLayout::create(
   838	        m_settings->getScreenW(),
   839	        m_settings->getScreenH(),
   840	        reserveOrderArea
   841	    );
   842	}
```

Итог: совпало.

### cDrawManager::setMessage — src/managers/cDrawManager.cpp@dc6e5ff:440-443

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/managers/cDrawManager.cpp | nl -ba | sed -n '440,443p'
```

Вывод:

```text
   440	void cDrawManager::setMessage(std::string msg, bool keepMessage)
   441	{
   442	    m_messageDrawer->setMessage(msg, keepMessage);
   443	}
```

Итог: совпало.

### cOrderDrawer::drawOrderButton — src/drawers/cOrderDrawer.cpp@dc6e5ff:55-72

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/drawers/cOrderDrawer.cpp | nl -ba | sed -n '55,72p'
```

Вывод:

```text
    55	void cOrderDrawer::drawOrderButton(cPlayer *thePlayer)
    56	{
    57	    d2tm_assert(thePlayer);
    58	
    59	    cOrderProcesser *orderProcesser = thePlayer->getOrderProcesser();
    60	
    61	    d2tm_assert(orderProcesser);
    62	    m_sdlDrawer->renderSprite(m_buttonBitmap.get(), m_buttonRect.getX(), m_buttonRect.getY());
    63	
    64	    bool canOrder = orderProcesser->canPlaceOrder();
    65	    if (!canOrder) {
    66	        m_sdlDrawer->renderRectFillColor(m_buttonRect, Color::Black, 128);
    67	    }
    68	
    69	    if (m_isMouseOverOrderButton && canOrder) {
    70	        drawRectangleOrderButton();
    71	    }
    72	}
```

Итог: совпало.
