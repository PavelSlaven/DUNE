# P5G3W — функции интерфейса боя

### cSideBarDrawer::draw — src/drawers/cSideBarDrawer.cpp@dc6e5ff:98-101

Команда: `git show dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/drawers/cSideBarDrawer.cpp | nl -ba | sed -n '98,101p'`

```text
    98	void cSideBarDrawer::draw()
    99	{
   100	    drawHdSidebar();
   101	}
```

### cSideBarDrawer::drawHdSidebar — src/drawers/cSideBarDrawer.cpp@dc6e5ff:109-140

Команда: `git show dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/drawers/cSideBarDrawer.cpp | nl -ba | sed -n '109,140p'`

```text
   109	void cSideBarDrawer::drawHdSidebar()
   110	{
   111	    const HudLayout layout = HudLayout::create(
   112	        m_services->settings->getScreenW(),
   113	        m_services->settings->getScreenH()
   114	    );
   115	    m_sdlDrawer->renderRectFillColor(
   116	        layout.sidebar.getX(),
   117	        layout.sidebar.getY(),
   118	        layout.sidebar.getWidth(),
   119	        layout.sidebar.getHeight(),
   120	        Color{12, 15, 17, 255}
   121	    );
   122	    m_sdlDrawer->renderRectFillColor(
   123	        layout.sidebar.getX(),
   124	        cSideBar::TopBarHeight,
   125	        5,
   126	        m_services->settings->getScreenH() - cSideBar::TopBarHeight,
   127	        Color{32, 36, 38, 255}
   128	    );
   129	    m_sdlDrawer->renderLine(
   130	        layout.sidebar.getX() + 5,
   131	        cSideBar::TopBarHeight,
   132	        layout.sidebar.getX() + 5,
   133	        m_services->settings->getScreenH(),
   134	        Color{166, 124, 44, 255}
   135	    );
   136	
   137	    drawHdRadarPanel();
   138	    drawHdCapacities();
   139	    drawHdBuildingLists();
   140	}
```

### cBuildingListDrawer::getLayout — src/drawers/cBuildingListDrawer.cpp@dc6e5ff:833-842

Команда: `git show dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/drawers/cBuildingListDrawer.cpp | nl -ba | sed -n '833,842p'`

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

### cBuildingListDrawer::getScrollRow — src/drawers/cBuildingListDrawer.cpp@dc6e5ff:844-858

Команда: `git show dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/drawers/cBuildingListDrawer.cpp | nl -ba | sed -n '844,858p'`

```text
   844	int cBuildingListDrawer::getScrollRow(cBuildingList *list) const
   845	{
   846	    if (list == nullptr) {
   847	        return 0;
   848	    }
   849	    const int listId = eListTypeAsInt(list->getType());
   850	    if (listId < 0 || listId >= static_cast<int>(m_scrollRows.size())) {
   851	        return 0;
   852	    }
   853	    return std::clamp(
   854	        m_scrollRows[listId],
   855	        0,
   856	        getLayout(list).maxScrollRow(list->getItemCount())
   857	    );
   858	}
```

### cBuildingListDrawer::setScrollRow — src/drawers/cBuildingListDrawer.cpp@dc6e5ff:860-874

Команда: `git show dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/drawers/cBuildingListDrawer.cpp | nl -ba | sed -n '860,874p'`

```text
   860	void cBuildingListDrawer::setScrollRow(cBuildingList *list, int row)
   861	{
   862	    if (list == nullptr) {
   863	        return;
   864	    }
   865	    const int listId = eListTypeAsInt(list->getType());
   866	    if (listId < 0 || listId >= static_cast<int>(m_scrollRows.size())) {
   867	        return;
   868	    }
   869	    m_scrollRows[listId] = std::clamp(
   870	        row,
   871	        0,
   872	        getLayout(list).maxScrollRow(list->getItemCount())
   873	    );
   874	}
```

### cDrawManager::setMessage — src/managers/cDrawManager.cpp@dc6e5ff:440-443

Команда: `git show dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/managers/cDrawManager.cpp | nl -ba | sed -n '440,443p'`

```text
   440	void cDrawManager::setMessage(std::string msg, bool keepMessage)
   441	{
   442	    m_messageDrawer->setMessage(msg, keepMessage);
   443	}
```

### cDrawManager::thinkFast — src/managers/cDrawManager.cpp@dc6e5ff:430-433

Команда: `git show dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/managers/cDrawManager.cpp | nl -ba | sed -n '430,433p'`

```text
   430	void cDrawManager::thinkFast()
   431	{
   432	    m_messageDrawer->thinkFast();
   433	}
```

### cDrawManager::drawTopBarBackground — src/managers/cDrawManager.cpp@dc6e5ff:298-342

Команда: `git show dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/managers/cDrawManager.cpp | nl -ba | sed -n '298,342p'`

```text
   298	void cDrawManager::drawTopBarBackground()
   299	{
   300	    const Color panel{17, 21, 23, 255};
   301	    const Color border{151, 113, 43, 255};
   302	    const Color text{232, 222, 188, 255};
   303	    m_sdlDrawer->renderRectFillColor(
   304	        0,
   305	        0,
   306	        m_gameSettings->getScreenW(),
   307	        cSideBar::TopBarHeight,
   308	        panel
   309	    );
   310	    m_sdlDrawer->renderLine(
   311	        0,
   312	        cSideBar::TopBarHeight - 2,
   313	        m_gameSettings->getScreenW(),
   314	        cSideBar::TopBarHeight - 2,
   315	        border
   316	    );
   317	
   318	    const cRectangle optionsRect(7, 4, 126, 33);
   319	    m_sdlDrawer->renderRectFillColor(
   320	        optionsRect.getX(),
   321	        optionsRect.getY(),
   322	        optionsRect.getWidth(),
   323	        optionsRect.getHeight(),
   324	        Color{27, 31, 33, 255}
   325	    );
   326	    m_sdlDrawer->renderRectColor(
   327	        optionsRect.getX(),
   328	        optionsRect.getY(),
   329	        optionsRect.getWidth(),
   330	        optionsRect.getHeight(),
   331	        border
   332	    );
   333	    m_textDrawer->drawTextCenteredInBox("OPTIONS", optionsRect, text);
   334	    if (m_mouse->isLeftButtonClicked() &&
   335	        m_mouse->isOverRectangle(
   336	            optionsRect.getX(),
   337	            optionsRect.getY(),
   338	            optionsRect.getWidth(),
   339	            optionsRect.getHeight())) {
   340	        m_stateTransitions->setNextState(GAME_OPTIONS);
   341	    }
   342	}
```

### cMiniMapDrawer::think — src/drawers/cMiniMapDrawer.cpp@dc6e5ff:144-201

Команда: `git show dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/drawers/cMiniMapDrawer.cpp | nl -ba | sed -n '144,201p'`

```text
   144	void cMiniMapDrawer::think()
   145	{
   146	    if (m_player->hasAtleastOneStructure(RADAR)) {
   147	        if (m_status == eMinimapStatus::NOTAVAILABLE) {
   148	            // Route through POWERDOWN instead of jumping straight to POWERUP, so the
   149	            // power check below (which plays SOUND_RADAR) always gets a chance to run,
   150	            // even when power is already sufficient the instant the radar completes.
   151	            m_status = eMinimapStatus::POWERDOWN;
   152	        }
   153	    }
   154	    else {
   155	        m_status = eMinimapStatus::NOTAVAILABLE;
   156	    }
   157	
   158	    if (m_status == eMinimapStatus::NOTAVAILABLE) return;
   159	
   160	    bool hasRadarAndEnoughPower = (m_player->getAmountOfStructuresForType(RADAR) > 0) && m_player->bEnoughPower();
   161	
   162	    // minimap state is enough power
   163	    if (m_status == eMinimapStatus::POWERUP || m_status == eMinimapStatus::RENDERMAP) {
   164	        if (!hasRadarAndEnoughPower) {
   165	            // go to state power down (not enough power)
   166	            m_status = eMinimapStatus::POWERDOWN;
   167	            // "Radar de-activated""
   168	            m_audioContext->playVoice(SOUND_VOICE_04_ATR, m_player->getHouse());
   169	        }
   170	    }
   171	
   172	    // minimap state is not enough power
   173	    if (m_status == eMinimapStatus::POWERDOWN || m_status == eMinimapStatus::LOWPOWER) {
   174	        if (hasRadarAndEnoughPower) {
   175	            // go to state power up (enough power)
   176	            m_status = eMinimapStatus::POWERUP;
   177	            m_audioContext->playSound(SOUND_RADAR);
   178	            // "Radar activated"
   179	            m_audioContext->playVoice(SOUND_VOICE_03_ATR, m_player->getHouse());
   180	        }
   181	    }
   182	
   183	    // think about the animation
   184	
   185	    if (m_status == eMinimapStatus::POWERDOWN) {
   186	        if (m_iStaticFrame < STAT21) {
   187	            m_iStaticFrame++;
   188	        }
   189	        else {
   190	            m_status = eMinimapStatus::LOWPOWER;
   191	        }
   192	    }
   193	    else if (m_status == eMinimapStatus::POWERUP) {
   194	        if (m_iStaticFrame > STAT01) {
   195	            m_iStaticFrame--;
   196	        }
   197	        else {
   198	            m_status = eMinimapStatus::RENDERMAP;
   199	        }
   200	    }
   201	}
```

### cMiniMapDrawer::draw — src/drawers/cMiniMapDrawer.cpp@dc6e5ff:110-134

Команда: `git show dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/drawers/cMiniMapDrawer.cpp | nl -ba | sed -n '110,134p'`

```text
   110	void cMiniMapDrawer::draw()
   111	{
   112	    if (!m_map) {
   113	        return;
   114	    }
   115	
   116	    if (m_status == eMinimapStatus::NOTAVAILABLE) {
   117	        return;
   118	    }
   119	
   120	    m_sdlDrawer->renderRectFillColor(m_RectFullMinimap, Color::Black);
   121	
   122	    if (m_status == eMinimapStatus::POWERUP || m_status == eMinimapStatus::RENDERMAP || m_status == eMinimapStatus::POWERDOWN) {
   123	        drawTerrain();
   124	        drawUnitsAndStructures(false);
   125	    }
   126	
   127	    if (m_status == eMinimapStatus::LOWPOWER) {
   128	        cleanDrawTerrain();
   129	        drawUnitsAndStructures(true);
   130	    }
   131	    m_sdlDrawer->renderStrechFullSprite(m_mipMapTex, m_RectMinimap);
   132	
   133	    drawViewPortRectangle();
   134	}
```

### cOrderDrawer::drawOrderButton — src/drawers/cOrderDrawer.cpp@dc6e5ff:55-72

Команда: `git show dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/drawers/cOrderDrawer.cpp | nl -ba | sed -n '55,72p'`

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

### cStructureDrawer::drawStructureHealthBar — src/drawers/cStructureDrawer.cpp@dc6e5ff:477-510

Команда: `git show dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/drawers/cStructureDrawer.cpp | nl -ba | sed -n '477,510p'`

```text
   477	void cStructureDrawer::drawStructureHealthBar(int iStructure)
   478	{
   479	    if (iStructure < 0 || iStructure >= MAX_STRUCTURES) return;
   480	
   481	    cAbstractStructure *theStructure = m_objects->getStructures()[iStructure];
   482	
   483	    if (!theStructure) {
   484	        return;
   485	    }
   486	
   487	    // Draw structure health
   488	    int draw_x = theStructure->iDrawX() - 1;
   489	    int draw_y = theStructure->iDrawY() - 5;
   490	
   491	    int widthBmp = m_mapCamera->factorZoomLevel(theStructure->getStructureInfo().bmp_width);
   492	    int width_x = widthBmp - 1;
   493	
   494	    int height_y = 4;
   495	
   496	    float healthNormalized = theStructure->getHealthNormalized();
   497	
   498	    int w = healthNormalized * width_x;
   499	    int r = (1.1 - healthNormalized) * 255;
   500	    int g = healthNormalized * 255;
   501	
   502	    if (r > 255) r = 255;
   503	
   504	    // bar itself
   505	    m_sdlDrawer->renderRectFillColor(draw_x, draw_y, width_x+1, height_y+1, 0,0,0,255);
   506	    m_sdlDrawer->renderRectFillColor(draw_x, draw_y, (w-1), height_y, static_cast<Uint8>(r),static_cast<Uint8>(g),32,255);
   507	
   508	    // bar around it
   509	    m_sdlDrawer->renderRectColor(draw_x, draw_y, width_x, height_y, Color{255, 255, 255,255});
   510	}
```

### git grep

Команда: `git grep -n -E 'setTechLevel|addNotification|isMouseOverStructure|setBuildingFase|iGroups|m_cameraEdgeMove|leftButtonClicked|rightButtonClicked' dc6e5ffd74f6275390a9c4a676aafdca058df7dd -- src`

```text
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/controls/cGameControlsContext.h:83:    bool isMouseOverStructure() const {
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/controls/cMouse.cpp:50:    m_leftButtonClickedInPreviousFrame = false;
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/controls/cMouse.cpp:51:    m_rightButtonClickedInPreviousFrame = false;
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/controls/cMouse.cpp:108:                        m_leftButtonClicked = true;
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/controls/cMouse.cpp:118:                    m_rightButtonClicked = true;
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/controls/cMouse.cpp:140:    if (m_leftButtonClickedInPreviousFrame == true)
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/controls/cMouse.cpp:141:        m_leftButtonClicked = false;
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/controls/cMouse.cpp:142:    if (m_rightButtonClickedInPreviousFrame == true)
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/controls/cMouse.cpp:143:        m_rightButtonClicked = false;
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/controls/cMouse.cpp:206:    m_leftButtonClickedInPreviousFrame = m_leftButtonClicked;
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/controls/cMouse.cpp:207:    m_rightButtonClickedInPreviousFrame = m_rightButtonClicked;
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/controls/cMouse.h:58:        return m_leftButtonClicked;
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/controls/cMouse.h:62:        return m_rightButtonClicked;
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/controls/cMouse.h:123:    bool m_leftButtonClicked;
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/controls/cMouse.h:124:    bool m_rightButtonClicked;
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/controls/cMouse.h:127:    bool m_leftButtonClickedInPreviousFrame;
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/controls/cMouse.h:128:    bool m_rightButtonClickedInPreviousFrame;
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/drawers/cMouseDrawer.cpp:81:    if (context->isMouseOverStructure()) {
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/drawers/cMouseDrawer.cpp:92:    if (context->isMouseOverStructure()) {
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/drawers/cMouseDrawer.cpp:136:    if (context->isMouseOverStructure()) {
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/drawers/cMouseDrawer.cpp:171:    if (context->isMouseOverStructure()) {
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/drawers/cStructureDrawer.cpp:132:    if (context->isMouseOverStructure()) {
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/drawers/cUnitDrawer.cpp:108:            if (m_unit.iGroups[i]) {
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/game/cGame.h:190:    bool m_cameraEdgeMove;                  // should move map camera when hitting edges of screen
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/game/cGame_logic.cpp:165:    m_cameraEdgeMove = true;
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/game/cGame_logic.cpp:312:    m_cameraEdgeMove = gs->cameraEdgeMove;
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/game/cGame_logic.cpp:352:    gs.cameraEdgeMove = m_cameraEdgeMove;
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/game/cGame_logic.cpp:862:    m_mapCamera = std::make_unique<cMapCamera>(m_gameObjectsContext->getMap(), m_cameraDragMoveSpeed, m_cameraBorderOrKeyMoveSpeed, m_cameraEdgeMove, m_gameSettings.get(), m_mouse.get());
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/game/cGame_logic.cpp:1411:                m_notificationArea->addNotification(notifEvent->message, notifEvent->type);
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/game/cGame_logic.cpp:1520:        m_notificationArea->addNotification("Screenshot saved.", eNotificationType::NEUTRAL);
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/game/cGame_logic.cpp:1537:        m_notificationArea->addNotification("Music toggle successfully", eNotificationType::NEUTRAL);
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/game/cGame_logic.cpp:1542:        m_notificationArea->addNotification("Music volume down", eNotificationType::NEUTRAL);
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/game/cGame_logic.cpp:1547:        m_notificationArea->addNotification("Music volume up", eNotificationType::NEUTRAL);
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/game/cGame_logic.cpp:1553:        m_notificationArea->addNotification("Game speed up", eNotificationType::NEUTRAL);
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/game/cGame_logic.cpp:1559:        m_notificationArea->addNotification("Game speed down", eNotificationType::NEUTRAL);
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/game/cGame_logic.cpp:1576:        m_notificationArea->addNotification(message, eNotificationType::OTHER);
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/game/cNotificationArea.cpp:35:void cNotificationArea::addNotification(const std::string &msg, eNotificationType type)
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/game/cNotificationArea.h:31:    void addNotification(const std::string &msg, eNotificationType type);
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/gameobjects/map/cMapCamera.cpp:35:    m_cameraEdgeMove(cameraEdgeMove),
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/gameobjects/map/cMapCamera.cpp:288:    if (!m_mouse->isMapScrolling() && m_cameraEdgeMove) {
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/gameobjects/map/cMapCamera.h:228:    bool m_cameraEdgeMove;
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/gameobjects/players/cPlayer.cpp:421:            pUnit.iGroups[groupIndex] = true;
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/gameobjects/players/cPlayer.cpp:426:        if (pUnit.iGroups[groupIndex]) {
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/gameobjects/players/cPlayer.cpp:427:            pUnit.iGroups[groupIndex] = false;
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/gameobjects/players/cPlayer.cpp:444:        if (pUnit->iGroups[groupIndex]) {
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/gameobjects/players/cPlayer.cpp:1654:                // addNotification(msg, eNotificationType::BAD);
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/gameobjects/players/cPlayer.cpp:1671:                // addNotification(msg, eNotificationType::BAD);
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/gameobjects/players/cPlayer.cpp:1690:                    // addNotification(msg, eNotificationType::PRIORITY);
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/gameobjects/players/cPlayer.cpp:1746:                    //addNotification(msg, eNotificationType::PRIORITY);
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/gameobjects/players/cPlayer.cpp:2227:        // addNotification("You've lost a Harvester.", eNotificationType::PRIORITY);
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/gameobjects/players/cPlayer.cpp:2243:            //addNotification("You have one Harvester left.", eNotificationType::NEUTRAL);
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/gameobjects/players/cPlayer.cpp:2265:                // addNotification("No harvesters and refineries left!", eNotificationType::BAD);
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/gameobjects/players/cPlayer.cpp:2295:            //addNotification("No more Harvester left, reinforcing...", BAD);
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/gameobjects/players/cPlayer.h:156:    void setTechLevel(int theTechLevel) {
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/gameobjects/players/cPlayers.cpp:133:        player->setTechLevel(techLevel);
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/gameobjects/projectiles/bullet.cpp:532:                groundUnitTakingDamage->iGroups.fill(false);
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/gameobjects/structures/cAbstractStructure.h:281:    void setBuildingFase(int value) {
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/gameobjects/structures/cStructureFactory.cpp:192:    str->setBuildingFase(1); // prebuild
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/gameobjects/units/cUnit.cpp:84:    iGroups.fill(false);
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/gameobjects/units/cUnit.h:159:    std::array<bool, MAX_UNIT_GROUPS> iGroups; // belongs to groups [0..MAX_UNIT_GROUPS-1]
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/gamestates/cGamePlaying.cpp:668:        // m_controlledPlayer->addNotification(
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/gui/GuiConsole/GuiConsoleMessageParser.cpp:72:        m_notificationArea->addNotification(std::format("Malformed command: {}", text), eNotificationType::BAD);
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/gui/GuiConsole/GuiConsoleMessageParser.cpp:79:    //     m_notificationArea->addNotification(std::format("Unknown command: {}", text), eNotificationType::BAD);
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/gui/GuiConsole/GuiConsoleMessageParser.cpp:84:        m_notificationArea->addNotification("Help mode.", eNotificationType::NEUTRAL);
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/gui/GuiConsole/GuiConsoleMessageParser.cpp:88:    m_notificationArea->addNotification(std::format("> {}", normalizedText), eNotificationType::NEUTRAL);
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/utils/cStructureUtils.cpp:282:bool cStructureUtils::isMouseOverStructure(cAbstractStructure *structure, int screenX, int screenY)
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/utils/cStructureUtils.h:54:    bool isMouseOverStructure(cAbstractStructure *structure, int screenX, int screenY);
```
