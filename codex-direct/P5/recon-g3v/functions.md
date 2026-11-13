### cScoringState::cScoringState — src/gamestates/cScoringState.cpp@91416fb:22-40

Команда поиска:
```text
git grep -n -E '^(.*[ *&])?cScoringState::cScoringState\(' 91416fb0c6aae877242d55e08559c32ec80de3e0 -- src
```

Вывод команды поиска:
```text
91416fb0c6aae877242d55e08559c32ec80de3e0:src/gamestates/cScoringState.cpp:22:cScoringState::cScoringState(sGameServices* services) :
```

Команда функции:
```text
git show 91416fb0c6aae877242d55e08559c32ec80de3e0:src/gamestates/cScoringState.cpp | nl -ba | sed -n '22,40p'
```

Вывод:
```text
    22	cScoringState::cScoringState(sGameServices* services) :
    23	    cGameState(services),
    24	    m_settings(services->settings),
    25	    m_missionFlow(services->missionFlow),
    26	    m_stateTransitions(services->stateTransitions),
    27	    m_textDrawer(m_ctx->getTextContext()->getBeneTextDrawer()),
    28	    m_smallTextDrawer(m_ctx->getTextContext()->getSmallTextDrawer()),
    29	    m_mouse(services->mouse),
    30	    m_screenFader(services->screenFader)
    31	{
    32	    d2tm_assert(m_settings != nullptr);
    33	    d2tm_assert(m_missionFlow != nullptr);
    34	    d2tm_assert(m_stateTransitions != nullptr);
    35	    d2tm_assert(m_textDrawer != nullptr);
    36	    d2tm_assert(m_smallTextDrawer != nullptr);
    37	    d2tm_assert(m_screenFader != nullptr);
    38	
    39	    m_stats = services->missionStatsCollector->snapshot(m_ctx->getTimeManager()->getElapsedSeconds());
    40	}
```

### cScoringState::draw — src/gamestates/cScoringState.cpp@91416fb:56-111

Команда поиска:
```text
git grep -n -E '^(.*[ *&])?cScoringState::draw\(' 91416fb0c6aae877242d55e08559c32ec80de3e0 -- src
```

Вывод команды поиска:
```text
91416fb0c6aae877242d55e08559c32ec80de3e0:src/gamestates/cScoringState.cpp:56:void cScoringState::draw() const
```

Команда функции:
```text
git show 91416fb0c6aae877242d55e08559c32ec80de3e0:src/gamestates/cScoringState.cpp | nl -ba | sed -n '56,111p'
```

Вывод:
```text
    56	void cScoringState::draw() const
    57	{
    58	    m_sdlDrawer->renderClearToColor();
    59	
    60	    int lineHeight = m_textDrawer->getFontHeight() + 4;
    61	    int statLineHeight = m_smallTextDrawer->getFontHeight() + 2;
    62	    int y = 40;
    63	
    64	    m_textDrawer->drawTextCentered("MISSION REPORT", y, Color::Yellow);
    65	    y += lineHeight * 2;
    66	
    67	    uint64_t minutes = m_stats.elapsedSeconds / 60;
    68	    uint64_t seconds = m_stats.elapsedSeconds % 60;
    69	    m_textDrawer->drawTextCentered(std::format("Mission time: {:02}:{:02}", minutes, seconds), y, Color::White);
    70	    y += lineHeight * 2;
    71	
    72	    // AI_CPU5 (Fremen superweapon trigger) and AI_WORM are not real opponents, never shown here.
    73	    for (int playerId = HUMAN; playerId < AI_WORM - 1; playerId++) {
    74	        const PlayerMissionStats &playerStats = m_stats.players[playerId];
    75	        // Read from the mission-start snapshot, not the live player: cGamePlaying resets a
    76	        // defeated player's house to GENERALHOUSE as elimination cleanup, which would otherwise
    77	        // hide anyone the player actually beat during the mission.
    78	        bool isPlaying = playerId == HUMAN || playerStats.house != GENERALHOUSE;
    79	        if (!isPlaying) {
    80	            continue;
    81	        }
    82	
    83	        std::string label = playerId == HUMAN ? "YOU" : "ENEMY";
    84	        std::string playerName = std::format("{} - {}", label, cPlayer::getHouseNameForId(playerStats.house));
    85	        Color nameColor = m_screenFader->getColorFadeSelected(playerStats.minimapColor.r, playerStats.minimapColor.g, playerStats.minimapColor.b);
    86	
    87	        m_textDrawer->drawTextCentered(playerName, y, nameColor);
    88	        y += lineHeight;
    89	        m_smallTextDrawer->drawTextCentered(
    90	            std::format("Units built: {}   lost: {}   destroyed: {}",
    91	                playerStats.unitsBuilt, playerStats.unitsLost, playerStats.unitsDestroyed),
    92	            y, Color::White);
    93	        y += statLineHeight;
    94	        m_smallTextDrawer->drawTextCentered(
    95	            std::format("Structures built: {}   lost: {}   destroyed: {}",
    96	                playerStats.structuresBuilt, playerStats.structuresLost, playerStats.structuresDestroyed),
    97	            y, Color::White);
    98	        y += statLineHeight;
    99	        m_smallTextDrawer->drawTextCentered(
   100	            std::format("Damage dealt: {}   received: {}", playerStats.damageDealt, playerStats.damageReceived),
   101	            y, Color::White);
   102	        y += statLineHeight;
   103	        m_smallTextDrawer->drawTextCentered(
   104	            std::format("Spice harvested: {}", playerStats.spiceHarvested),
   105	            y, Color::White);
   106	        y += lineHeight * 2;
   107	    }
   108	
   109	    m_textDrawer->drawTextCentered("Click to continue", m_settings->getScreenH() - lineHeight - 8, Color::White);
   110	    m_mouse->draw();
   111	}
```

### cScoringState::thinkFast — src/gamestates/cScoringState.cpp@91416fb:52-54

Команда поиска:
```text
git grep -n -E '^(.*[ *&])?cScoringState::thinkFast\(' 91416fb0c6aae877242d55e08559c32ec80de3e0 -- src
```

Вывод команды поиска:
```text
91416fb0c6aae877242d55e08559c32ec80de3e0:src/gamestates/cScoringState.cpp:52:void cScoringState::thinkFast()
```

Команда функции:
```text
git show 91416fb0c6aae877242d55e08559c32ec80de3e0:src/gamestates/cScoringState.cpp | nl -ba | sed -n '52,54p'
```

Вывод:
```text
    52	void cScoringState::thinkFast()
    53	{
    54	}
```

### cScoringState::onNotifyMouseEvent — src/gamestates/cScoringState.cpp@91416fb:113-120

Команда поиска:
```text
git grep -n -E '^(.*[ *&])?cScoringState::onNotifyMouseEvent\(' 91416fb0c6aae877242d55e08559c32ec80de3e0 -- src
```

Вывод команды поиска:
```text
91416fb0c6aae877242d55e08559c32ec80de3e0:src/gamestates/cScoringState.cpp:113:void cScoringState::onNotifyMouseEvent(const s_MouseEvent &event)
```

Команда функции:
```text
git show 91416fb0c6aae877242d55e08559c32ec80de3e0:src/gamestates/cScoringState.cpp | nl -ba | sed -n '113,120p'
```

Вывод:
```text
   113	void cScoringState::onNotifyMouseEvent(const s_MouseEvent &event)
   114	{
   115	    // Any left click continues, matching the WINNING screen's click-anywhere behavior the
   116	    // player just came from.
   117	    if (event.eventType == MOUSE_LEFT_BUTTON_CLICKED) {
   118	        continueToWinBrief();
   119	    }
   120	}
```

### cScoringState::onNotifyKeyboardEvent — src/gamestates/cScoringState.cpp@91416fb:122-124

Команда поиска:
```text
git grep -n -E '^(.*[ *&])?cScoringState::onNotifyKeyboardEvent\(' 91416fb0c6aae877242d55e08559c32ec80de3e0 -- src
```

Вывод команды поиска:
```text
91416fb0c6aae877242d55e08559c32ec80de3e0:src/gamestates/cScoringState.cpp:122:void cScoringState::onNotifyKeyboardEvent(const cKeyboardEvent &)
```

Команда функции:
```text
git show 91416fb0c6aae877242d55e08559c32ec80de3e0:src/gamestates/cScoringState.cpp | nl -ba | sed -n '122,124p'
```

Вывод:
```text
   122	void cScoringState::onNotifyKeyboardEvent(const cKeyboardEvent &)
   123	{
   124	}
```

### cVideoState::cVideoState — src/gamestates/cVideoState.cpp@91416fb:43-65

Команда поиска:
```text
git grep -n -E '^(.*[ *&])?cVideoState::cVideoState\(' 91416fb0c6aae877242d55e08559c32ec80de3e0 -- src
```

Вывод команды поиска:
```text
91416fb0c6aae877242d55e08559c32ec80de3e0:src/gamestates/cVideoState.cpp:43:cVideoState::cVideoState(sGameServices* services, const std::string &filename)
```

Команда функции:
```text
git show 91416fb0c6aae877242d55e08559c32ec80de3e0:src/gamestates/cVideoState.cpp | nl -ba | sed -n '43,65p'
```

Вывод:
```text
    43	cVideoState::cVideoState(sGameServices* services, const std::string &filename)
    44	    : cGameState(services)
    45	{
    46	    d2tm_assert(services != nullptr);
    47	    m_settings = services->settings;
    48	    m_stateTransitions = services->stateTransitions;
    49	    m_mouse = services->mouse;
    50	    d2tm_assert(m_settings != nullptr);
    51	    d2tm_assert(m_stateTransitions != nullptr);
    52	    d2tm_assert(m_mouse != nullptr);
    53	
    54	    m_gfxMovie = std::make_unique<Graphics>(m_sdlDrawer->getRenderer(), filename);
    55	
    56	    // a missing (or invalid) pack has no frames: thinkNormal sends us back to the main menu
    57	    if (m_gfxMovie->getNumberOfFiles() > 0) {
    58	        Logger::info(COMP_INIT, "video", "Successful loaded video [{}]", filename);
    59	        m_currentFrame = m_gfxMovie->getTexture(m_movieFrame);
    60	        m_offsetX = (m_settings->getScreenW() - VIDEO_WIDTH) / 2 - VIDEO_CENTER_SHIFT;
    61	        m_offsetY = (m_settings->getScreenH() - VIDEO_MAX_HEIGHT) / 2 - VIDEO_CENTER_SHIFT;
    62	    } else {
    63	        Logger::error(COMP_INIT, "video", "Failed to load video [{}], returning to main menu", filename);
    64	    }
    65	}
```

### cVideoState::draw — src/gamestates/cVideoState.cpp@91416fb:91-99

Команда поиска:
```text
git grep -n -E '^(.*[ *&])?cVideoState::draw\(' 91416fb0c6aae877242d55e08559c32ec80de3e0 -- src
```

Вывод команды поиска:
```text
91416fb0c6aae877242d55e08559c32ec80de3e0:src/gamestates/cVideoState.cpp:91:void cVideoState::draw() const
```

Команда функции:
```text
git show 91416fb0c6aae877242d55e08559c32ec80de3e0:src/gamestates/cVideoState.cpp | nl -ba | sed -n '91,99p'
```

Вывод:
```text
    91	void cVideoState::draw() const
    92	{
    93	    m_mouse->setTile(MOUSE_NORMAL);
    94	    if (m_currentFrame != nullptr) {
    95	        cRectangle dest = {m_offsetX, m_offsetY, VIDEO_WIDTH + VIDEO_DRAW_EXTRA, VIDEO_MAX_HEIGHT + VIDEO_DRAW_EXTRA};
    96	        m_sdlDrawer->renderStrechFullSprite(m_currentFrame, dest);
    97	    }
    98	    m_mouse->draw();
    99	}
```

### cVideoState::thinkFast — src/gamestates/cVideoState.cpp@91416fb:76-78

Команда поиска:
```text
git grep -n -E '^(.*[ *&])?cVideoState::thinkFast\(' 91416fb0c6aae877242d55e08559c32ec80de3e0 -- src
```

Вывод команды поиска:
```text
91416fb0c6aae877242d55e08559c32ec80de3e0:src/gamestates/cVideoState.cpp:76:void cVideoState::thinkFast()
```

Команда функции:
```text
git show 91416fb0c6aae877242d55e08559c32ec80de3e0:src/gamestates/cVideoState.cpp | nl -ba | sed -n '76,78p'
```

Вывод:
```text
    76	void cVideoState::thinkFast()
    77	{
    78	}
```

### cVideoState::onNotifyMouseEvent — src/gamestates/cVideoState.cpp@91416fb:101-106

Команда поиска:
```text
git grep -n -E '^(.*[ *&])?cVideoState::onNotifyMouseEvent\(' 91416fb0c6aae877242d55e08559c32ec80de3e0 -- src
```

Вывод команды поиска:
```text
91416fb0c6aae877242d55e08559c32ec80de3e0:src/gamestates/cVideoState.cpp:101:void cVideoState::onNotifyMouseEvent(const s_MouseEvent &event)
```

Команда функции:
```text
git show 91416fb0c6aae877242d55e08559c32ec80de3e0:src/gamestates/cVideoState.cpp | nl -ba | sed -n '101,106p'
```

Вывод:
```text
   101	void cVideoState::onNotifyMouseEvent(const s_MouseEvent &event)
   102	{
   103	    if (event.eventType == eMouseEventType::MOUSE_LEFT_BUTTON_PRESSED) {
   104	        m_stateTransitions->setNextStateWithFade(GAME_MENU);
   105	    }
   106	}
```

### cVideoState::onNotifyKeyboardEvent — src/gamestates/cVideoState.cpp@91416fb:108-113

Команда поиска:
```text
git grep -n -E '^(.*[ *&])?cVideoState::onNotifyKeyboardEvent\(' 91416fb0c6aae877242d55e08559c32ec80de3e0 -- src
```

Вывод команды поиска:
```text
91416fb0c6aae877242d55e08559c32ec80de3e0:src/gamestates/cVideoState.cpp:108:void cVideoState::onNotifyKeyboardEvent(const cKeyboardEvent &event)
```

Команда функции:
```text
git show 91416fb0c6aae877242d55e08559c32ec80de3e0:src/gamestates/cVideoState.cpp | nl -ba | sed -n '108,113p'
```

Вывод:
```text
   108	void cVideoState::onNotifyKeyboardEvent(const cKeyboardEvent &event)
   109	{
   110	    if (event.isType(eKeyEventType::PRESSED)) {
   111	        m_stateTransitions->setNextStateWithFade(GAME_MENU);
   112	    }
   113	}
```

### cEditorState::cEditorState — src/gamestates/cEditorState.cpp@91416fb:60-105

Команда поиска:
```text
git grep -n -E '^(.*[ *&])?cEditorState::cEditorState\(' 91416fb0c6aae877242d55e08559c32ec80de3e0 -- src
```

Вывод команды поиска:
```text
91416fb0c6aae877242d55e08559c32ec80de3e0:src/gamestates/cEditorState.cpp:60:cEditorState::cEditorState(sGameServices* services)
```

Команда функции:
```text
git show 91416fb0c6aae877242d55e08559c32ec80de3e0:src/gamestates/cEditorState.cpp | nl -ba | sed -n '60,105p'
```

Вывод:
```text
    60	cEditorState::cEditorState(sGameServices* services) 
    61	    : cGameState(services),
    62	    m_gfxdata(m_ctx->getGraphicsContext()->gfxdata.get()),
    63	    m_gfxeditor(m_ctx->getGraphicsContext()->gfxeditor.get()),
    64	    m_settings(services->settings),
    65	    m_eventEmitter(services->eventEmitter),
    66	    m_stateTransitions(services->stateTransitions),
    67	    m_mouse(services->mouse),
    68	    m_textDrawer(m_ctx->getTextContext()->getBeneTextDrawer()),
    69	    m_previewMaps(services->objects->getPreviewMaps())
    70	{
    71	    d2tm_assert(m_gfxdata != nullptr);
    72	    d2tm_assert(m_gfxeditor != nullptr);
    73	    d2tm_assert(m_settings != nullptr);
    74	    d2tm_assert(m_eventEmitter != nullptr);
    75	    d2tm_assert(m_stateTransitions != nullptr);
    76	    d2tm_assert(m_mouse != nullptr);
    77	    d2tm_assert(m_textDrawer != nullptr);
    78	
    79	    m_undoRedo = std::make_unique<cEditorUndoRedoHistory>();
    80	
    81	    const cRectangle &selectRect = cRectangle(0, 0, m_settings->getScreenW(), heightBarSize);
    82	    const cRectangle &modifRect = cRectangle(m_settings->getScreenW()-heightBarSize, heightBarSize, heightBarSize, m_settings->getScreenH()-heightBarSize);
    83	    mapSizeArea = cRectangle(0,heightBarSize,m_settings->getScreenW()-heightBarSize,m_settings->getScreenH()-heightBarSize);
    84	    m_editorCam = std::make_unique<cEditorCam>(mapSizeArea);
    85	    m_selectBar = std::make_unique<GuiBar>(m_sdlDrawer, selectRect,GuiBarPlacement::HORIZONTAL,heightButtonSize);
    86	    m_topologyBar = std::make_unique<GuiBar>(m_sdlDrawer, modifRect,GuiBarPlacement::VERTICAL, heightButtonSize);
    87	    m_startCellBar = std::make_unique<GuiBar>(m_sdlDrawer, modifRect,GuiBarPlacement::VERTICAL, heightButtonSize);
    88	    m_symmetricBar = std::make_unique<GuiBar>(m_sdlDrawer, modifRect,GuiBarPlacement::VERTICAL, heightButtonSize);
    89	
    90	    m_selectBar->setTheme(cGuiThemeBuilder().light().build());
    91	    m_selectBar->beginPlacement(heightBarSize);
    92	    m_topologyBar->setTheme(cGuiThemeBuilder().light().build());
    93	    m_topologyBar->beginPlacement(heightBarSize);
    94	    m_startCellBar->setTheme(cGuiThemeBuilder().light().build());
    95	    m_startCellBar->beginPlacement(heightBarSize);
    96	    m_symmetricBar->setTheme(cGuiThemeBuilder().light().build());
    97	    m_symmetricBar->beginPlacement(heightBarSize);
    98	
    99	    populateSelectBar();
   100	    populateTopologyBar();
   101	    populateStartCellBar();
   102	    populateSymmetricBar();
   103	    setCurrentBar(m_topologyBar.get());
   104	    startCells.fill({-1, -1});
   105	}
```

### cEditorState::draw — src/gamestates/cEditorState.cpp@91416fb:415-431

Команда поиска:
```text
git grep -n -E '^(.*[ *&])?cEditorState::draw\(' 91416fb0c6aae877242d55e08559c32ec80de3e0 -- src
```

Вывод команды поиска:
```text
91416fb0c6aae877242d55e08559c32ec80de3e0:src/gamestates/cEditorState.cpp:415:void cEditorState::draw() const
```

Команда функции:
```text
git show 91416fb0c6aae877242d55e08559c32ec80de3e0:src/gamestates/cEditorState.cpp | nl -ba | sed -n '415,431p'
```

Вывод:
```text
   415	void cEditorState::draw() const
   416	{
   417	    drawMap();
   418	    drawHoveredCellHighlight();
   419	    drawSelectionRectangle();
   420	    if (m_displayPastPreview)
   421	        drawPastePreviewGhost();
   422	    if (m_displayGrid)
   423	        drawGrid();
   424	    if (m_displayAxes)
   425	        drawAxes();
   426	    if (m_currentBar == m_startCellBar.get())
   427	        drawStartCells();
   428	    m_selectBar->draw();
   429	    m_currentBar->draw();
   430	    m_mouse->draw();
   431	}
```

### cEditorState::thinkFast — src/gamestates/cEditorState.cpp@91416fb:411-413

Команда поиска:
```text
git grep -n -E '^(.*[ *&])?cEditorState::thinkFast\(' 91416fb0c6aae877242d55e08559c32ec80de3e0 -- src
```

Вывод команды поиска:
```text
91416fb0c6aae877242d55e08559c32ec80de3e0:src/gamestates/cEditorState.cpp:411:void cEditorState::thinkFast()
```

Команда функции:
```text
git show 91416fb0c6aae877242d55e08559c32ec80de3e0:src/gamestates/cEditorState.cpp | nl -ba | sed -n '411,413p'
```

Вывод:
```text
   411	void cEditorState::thinkFast()
   412	{
   413	}
```

### cEditorState::onNotifyMouseEvent — src/gamestates/cEditorState.cpp@91416fb:433-491

Команда поиска:
```text
git grep -n -E '^(.*[ *&])?cEditorState::onNotifyMouseEvent\(' 91416fb0c6aae877242d55e08559c32ec80de3e0 -- src
```

Вывод команды поиска:
```text
91416fb0c6aae877242d55e08559c32ec80de3e0:src/gamestates/cEditorState.cpp:433:void cEditorState::onNotifyMouseEvent(const s_MouseEvent &event)
```

Команда функции:
```text
git show 91416fb0c6aae877242d55e08559c32ec80de3e0:src/gamestates/cEditorState.cpp | nl -ba | sed -n '433,491p'
```

Вывод:
```text
   433	void cEditorState::onNotifyMouseEvent(const s_MouseEvent &event)
   434	{
   435	    if (m_mapData == nullptr) {
   436	        return;
   437	    }
   438	
   439	    if (event.eventType == MOUSE_RIGHT_BUTTON_CLICKED) {
   440	        if (m_hasSelection) {
   441	            const int selectionWidth = m_selectionEndTileX - m_selectionStartTileX + 1;
   442	            const int selectionHeight = m_selectionEndTileY - m_selectionStartTileY + 1;
   443	            if (selectionWidth * selectionHeight < 2) {
   444	                m_hasSelection = false;
   445	            }
   446	        }
   447	        m_isDraggingSelection = false;
   448	    }
   449	
   450	    if (event.coords.isWithinRectangle(&mapSizeArea)) {
   451	        // Zoom centered on the cursor
   452	        int mouseX = event.coords.x;
   453	        int mouseY = event.coords.y - mapSizeArea.getY(); // offset barre
   454	        if (event.eventType == MOUSE_SCROLLED_DOWN) {
   455	            m_editorCam->zoomAtMapPosition(mouseX, mouseY, cEditorCam::ZoomDirection::zoomOut, *m_mapData);
   456	            m_editorCam->updateVisibleTiles(*m_mapData);
   457	        } else if (event.eventType == MOUSE_SCROLLED_UP) {
   458	            m_editorCam->zoomAtMapPosition(mouseX, mouseY, cEditorCam::ZoomDirection::zoomIn, *m_mapData);
   459	            m_editorCam->updateVisibleTiles(*m_mapData);
   460	        } else if (event.eventType == MOUSE_RIGHT_BUTTON_PRESSED) {
   461	            int tileX = 0;
   462	            int tileY = 0;
   463	            if (tryGetTileFromMouseCoords(event.coords, tileX, tileY) && isEditableTile(tileX, tileY)) {
   464	                if (!m_isDraggingSelection) {
   465	                    m_selectionAnchorTileX = tileX;
   466	                    m_selectionAnchorTileY = tileY;
   467	                    m_isDraggingSelection = true;
   468	                    m_hasSelection = true;
   469	                }
   470	                updateSelectionFromTiles(m_selectionAnchorTileX, m_selectionAnchorTileY, tileX, tileY);
   471	            }
   472	        } else if (event.eventType == MOUSE_MOVED_TO && m_isDraggingSelection) {
   473	            int tileX = 0;
   474	            int tileY = 0;
   475	            if (tryGetTileFromMouseCoords(event.coords, tileX, tileY)) {
   476	                updateSelectionFromTiles(m_selectionAnchorTileX, m_selectionAnchorTileY, tileX, tileY);
   477	            }
   478	        } else if (event.eventType == MOUSE_LEFT_BUTTON_PRESSED && m_currentBar == m_topologyBar.get()) {
   479	            modifyTile(mouseX, mouseY, idTerrainToMapModif);
   480	        }else if (event.eventType == MOUSE_LEFT_BUTTON_PRESSED && m_currentBar == m_startCellBar.get()) {
   481	            modifyStartCell(mouseX, mouseY, idStartCellPlayer);
   482	        }        
   483	        else {
   484	            return;
   485	        }
   486		// to test : updateVisibleTiles();
   487	    } else {
   488	        m_selectBar->onNotifyMouseEvent(event);
   489	        m_currentBar->onNotifyMouseEvent(event);
   490	    }
   491	}
```

### cEditorState::onNotifyKeyboardEvent — src/gamestates/cEditorState.cpp@91416fb:498-603

Команда поиска:
```text
git grep -n -E '^(.*[ *&])?cEditorState::onNotifyKeyboardEvent\(' 91416fb0c6aae877242d55e08559c32ec80de3e0 -- src
```

Вывод команды поиска:
```text
91416fb0c6aae877242d55e08559c32ec80de3e0:src/gamestates/cEditorState.cpp:498:void cEditorState::onNotifyKeyboardEvent(const cKeyboardEvent &event)
```

Команда функции:
```text
git show 91416fb0c6aae877242d55e08559c32ec80de3e0:src/gamestates/cEditorState.cpp | nl -ba | sed -n '498,603p'
```

Вывод:
```text
   498	void cEditorState::onNotifyKeyboardEvent(const cKeyboardEvent &event)
   499	{
   500	    if (m_mapData == nullptr) {
   501	        if (event.isType(eKeyEventType::PRESSED) && event.isAction(eKeyAction::MENU_BACK)) {
   502	            m_stateTransitions->setNextStateWithFade(GAME_MENU);
   503	        }
   504	        return;
   505	    }
   506	    if (event.isType(eKeyEventType::PRESSED)) {
   507	        if (event.isAction(eKeyAction::MENU_BACK)) {
   508	            if (m_hasChanged) {
   509	                // saveMap() notifies the user when it fails, still leave the editor
   510	                saveMap(true);
   511	                m_hasChanged = false;
   512	            }
   513	            m_stateTransitions->setNextState(GAME_OPTIONS);
   514	        }
   515	        if (event.isAction(eKeyAction::EDITOR_SAVE)) {
   516	            //std::cout << "Save" << std::endl;
   517	            if (saveMap()) {
   518	                m_hasChanged = false;
   519	            }
   520	        }
   521	        if (event.isAction(eKeyAction::EDITOR_ZOOM_IN)) {
   522	            m_editorCam->zoomAtMapPosition(mapSizeArea.getWidth()/2, mapSizeArea.getHeight()/2, cEditorCam::ZoomDirection::zoomIn, *m_mapData);
   523	            m_editorCam->updateVisibleTiles(*m_mapData);
   524	        }
   525	        if (event.isAction(eKeyAction::EDITOR_ZOOM_OUT)) {
   526	            m_editorCam->zoomAtMapPosition(mapSizeArea.getWidth()/2, mapSizeArea.getHeight()/2, cEditorCam::ZoomDirection::zoomOut, *m_mapData);
   527	            m_editorCam->updateVisibleTiles(*m_mapData);
   528	        }
   529	        // to test : updateVisibleTiles();
   530	        //m_selectBar->onNotifyKeyboardEvent(event);
   531	        m_currentBar->onNotifyKeyboardEvent(event);
   532	
   533	        if (event.isAction(eKeyAction::EDITOR_DISPLAY_GRID)) {
   534	            // toggle grid display
   535	            //std::cout << "Toggle grid display" << std::endl;
   536	            m_displayGrid = !m_displayGrid;
   537	
   538	        }
   539	        if (event.isAction(eKeyAction::EDITOR_DISPLAY_AXES)) {
   540	            // toggle axes display
   541	            //std::cout << "Toggle axes display" << std::endl;
   542	            m_displayAxes = !m_displayAxes;
   543	        }
   544	        if (event.isAction(eKeyAction::EDITOR_UNDO)) {
   545	            if (m_undoRedo->applyUndo(*m_mapData, startCells)) {
   546	                m_hasChanged = true;
   547	            }
   548	        }
   549	        if (event.isAction(eKeyAction::EDITOR_REDO)) {
   550	            if (m_undoRedo->applyRedo(*m_mapData, startCells)) {
   551	                m_hasChanged = true;
   552	            }
   553	        }
   554	        if (event.isAction(eKeyAction::EDITOR_COPY)) {
   555	            //std::cout << "Action : Copy selection to clipboard" << std::endl;
   556	            copySelectionToClipboard();
   557	        }
   558	        if (event.isAction(eKeyAction::EDITOR_PASTE)) {
   559	            //std::cout << "Action : Paste selection to clipboard" << std::endl;
   560	            pasteClipboardAtMouseCursor();
   561	        }
   562	        if (event.isAction(eKeyAction::EDITOR_CUT)) {
   563	            cutSelectionToClipboard();
   564	        }
   565	
   566	        if (!event.isCtrlPressed()) {
   567	            m_displayPastPreview = false;
   568	        }
   569	    }
   570	
   571	    if (event.isType(eKeyEventType::HOLD)) {
   572	        if (event.isAction(eKeyAction::SCROLL_LEFT)) {
   573	            m_editorCam->scrollByTiles(-1, 0, *m_mapData);
   574	            m_editorCam->updateVisibleTiles(*m_mapData);
   575	        }
   576	        if (event.isAction(eKeyAction::SCROLL_RIGHT)) {
   577	            m_editorCam->scrollByTiles(1, 0, *m_mapData);
   578	            m_editorCam->updateVisibleTiles(*m_mapData);
   579	        }
   580	        if (event.isAction(eKeyAction::SCROLL_UP)) {
   581	            m_editorCam->scrollByTiles(0, -1, *m_mapData);
   582	            m_editorCam->updateVisibleTiles(*m_mapData);
   583	        }
   584	        if (event.isAction(eKeyAction::SCROLL_DOWN)) {
   585	            m_editorCam->scrollByTiles(0, 1, *m_mapData);
   586	            m_editorCam->updateVisibleTiles(*m_mapData);
   587	        }
   588	        if (event.isShiftPressed() && event.isAction(eKeyAction::SCROLL_UP)) {
   589	            m_editorCam->zoomAtMapPosition(mapSizeArea.getWidth()/2, mapSizeArea.getHeight()/2, cEditorCam::ZoomDirection::zoomIn, *m_mapData);
   590	            m_editorCam->updateVisibleTiles(*m_mapData);
   591	            return;
   592	        }
   593	        if (event.isShiftPressed() && event.isAction(eKeyAction::SCROLL_DOWN)) {
   594	            m_editorCam->zoomAtMapPosition(mapSizeArea.getWidth()/2, mapSizeArea.getHeight()/2, cEditorCam::ZoomDirection::zoomOut, *m_mapData);
   595	            m_editorCam->updateVisibleTiles(*m_mapData);
   596	            return;
   597	        }
   598	        if (event.isCtrlPressed()) {
   599	            m_displayPastPreview = true;
   600	        }
   601	        //to test : updateVisibleTiles();
   602	    }
   603	}
```

### cNewMapEditorState::cNewMapEditorState — src/gamestates/cNewmapEditorState.cpp@91416fb:48-66

Команда поиска:
```text
git grep -n -E '^(.*[ *&])?cNewMapEditorState::cNewMapEditorState\(' 91416fb0c6aae877242d55e08559c32ec80de3e0 -- src
```

Вывод команды поиска:
```text
91416fb0c6aae877242d55e08559c32ec80de3e0:src/gamestates/cNewmapEditorState.cpp:48:cNewMapEditorState::cNewMapEditorState(sGameServices* services, cIni* ini)
```

Команда функции:
```text
git show 91416fb0c6aae877242d55e08559c32ec80de3e0:src/gamestates/cNewmapEditorState.cpp | nl -ba | sed -n '48,66p'
```

Вывод:
```text
    48	cNewMapEditorState::cNewMapEditorState(sGameServices* services, cIni* ini)
    49	    : cGameState(services),
    50	    m_textDrawer(m_ctx->getTextContext()->getBeneTextDrawer()),
    51	    m_settings(services->settings),
    52	    m_scenarioFlow(services->scenarioFlow),
    53	    m_stateTransitions(services->stateTransitions),
    54	    m_mouse(services->mouse),
    55	    m_guiWindow(nullptr),
    56	    m_objects(services->objects),
    57	    m_previewMap(services->objects->getPreviewMaps()),
    58	    m_cIni(ini)
    59	{
    60	    d2tm_assert(m_textDrawer != nullptr);
    61	    d2tm_assert(m_settings != nullptr);
    62	    d2tm_assert(m_scenarioFlow != nullptr);
    63	    d2tm_assert(m_stateTransitions != nullptr);
    64	    d2tm_assert(m_cIni != nullptr);
    65	    constructWindow();
    66	}
```

### cNewMapEditorState::draw — src/gamestates/cNewmapEditorState.cpp@91416fb:291-295

Команда поиска:
```text
git grep -n -E '^(.*[ *&])?cNewMapEditorState::draw\(' 91416fb0c6aae877242d55e08559c32ec80de3e0 -- src
```

Вывод команды поиска:
```text
91416fb0c6aae877242d55e08559c32ec80de3e0:src/gamestates/cNewmapEditorState.cpp:291:void cNewMapEditorState::draw() const
```

Команда функции:
```text
git show 91416fb0c6aae877242d55e08559c32ec80de3e0:src/gamestates/cNewmapEditorState.cpp | nl -ba | sed -n '291,295p'
```

Вывод:
```text
   291	void cNewMapEditorState::draw() const
   292	{
   293	    m_guiWindow->draw();
   294	    m_mouse->draw();
   295	}
```

### cNewMapEditorState::thinkFast — src/gamestates/cNewmapEditorState.cpp@91416fb:286-289

Команда поиска:
```text
git grep -n -E '^(.*[ *&])?cNewMapEditorState::thinkFast\(' 91416fb0c6aae877242d55e08559c32ec80de3e0 -- src
```

Вывод команды поиска:
```text
91416fb0c6aae877242d55e08559c32ec80de3e0:src/gamestates/cNewmapEditorState.cpp:286:void cNewMapEditorState::thinkFast()
```

Команда функции:
```text
git show 91416fb0c6aae877242d55e08559c32ec80de3e0:src/gamestates/cNewmapEditorState.cpp | nl -ba | sed -n '286,289p'
```

Вывод:
```text
   286	void cNewMapEditorState::thinkFast()
   287	{
   288	
   289	}
```

### cNewMapEditorState::onNotifyMouseEvent — src/gamestates/cNewmapEditorState.cpp@91416fb:297-300

Команда поиска:
```text
git grep -n -E '^(.*[ *&])?cNewMapEditorState::onNotifyMouseEvent\(' 91416fb0c6aae877242d55e08559c32ec80de3e0 -- src
```

Вывод команды поиска:
```text
91416fb0c6aae877242d55e08559c32ec80de3e0:src/gamestates/cNewmapEditorState.cpp:297:void cNewMapEditorState::onNotifyMouseEvent(const s_MouseEvent &event)
```

Команда функции:
```text
git show 91416fb0c6aae877242d55e08559c32ec80de3e0:src/gamestates/cNewmapEditorState.cpp | nl -ba | sed -n '297,300p'
```

Вывод:
```text
   297	void cNewMapEditorState::onNotifyMouseEvent(const s_MouseEvent &event)
   298	{
   299	    m_guiWindow->onNotifyMouseEvent(event);
   300	}
```

### cNewMapEditorState::onNotifyKeyboardEvent — src/gamestates/cNewmapEditorState.cpp@91416fb:307-310

Команда поиска:
```text
git grep -n -E '^(.*[ *&])?cNewMapEditorState::onNotifyKeyboardEvent\(' 91416fb0c6aae877242d55e08559c32ec80de3e0 -- src
```

Вывод команды поиска:
```text
91416fb0c6aae877242d55e08559c32ec80de3e0:src/gamestates/cNewmapEditorState.cpp:307:void cNewMapEditorState::onNotifyKeyboardEvent(const cKeyboardEvent &event)
```

Команда функции:
```text
git show 91416fb0c6aae877242d55e08559c32ec80de3e0:src/gamestates/cNewmapEditorState.cpp | nl -ba | sed -n '307,310p'
```

Вывод:
```text
   307	void cNewMapEditorState::onNotifyKeyboardEvent(const cKeyboardEvent &event)
   308	{
   309	    m_guiWindow->onNotifyKeyboardEvent(event);
   310	}
```
