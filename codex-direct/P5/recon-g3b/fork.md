### src/debug/UiAuditAccess.cpp@9208dcf:641-934

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditAccess.cpp | nl -ba | sed -n '641,934p'
```

Вывод:

```text
   641	namespace {
   642	
   643	struct BaseSpot {
   644	    int type;
   645	    int column;
   646	    int row;
   647	};
   648	
   649	constexpr BaseSpot kBaseSpots[] = {
   650	    {WINDTRAP, 24, 25}, {WINDTRAP, 26, 25}, {WINDTRAP, 35, 25}, {REFINERY, 32, 25},
   651	    {LIGHTFACTORY, 24, 28}, {RADAR, 30, 28}, {BARRACKS, 28, 25}, {WOR, 32, 28},
   652	    {HEAVYFACTORY, 26, 28}, {HIGHTECH, 32, 22}, {REPAIR, 35, 28}, {STARPORT, 28, 22},
   653	    {IX, 35, 22}, {PALACE, 24, 22},
   654	};
   655	
   656	constexpr int kStreetRow = 27;
   657	constexpr int kConstyardColumn = 30;
   658	constexpr int kConstyardRow = 25;
   659	
   660	struct BaseResult {
   661	    int factoryId = -1;
   662	    int tankId = -1;
   663	    int harvesterId = -1;
   664	    int mcvId = -1;
   665	};
   666	
   667	bool footprintFree(int type, int column, int row)
   668	{
   669	    const int w = structureUtils.getWidthOfStructureTypeInCells(type);
   670	    const int h = structureUtils.getHeightOfStructureTypeInCells(type);
   671	    for (int dy = 0; dy < h; dy++) {
   672	        for (int dx = 0; dx < w; dx++) {
   673	            const int cell = cellAt(column + dx, row + dy);
   674	            if (!global_map.isValidCell(cell) || global_map.getCellIdStructuresLayer(cell) > -1) {
   675	                return false;
   676	            }
   677	        }
   678	    }
   679	    return true;
   680	}
   681	
   682	int buildStructure(int type, int column, int row)
   683	{
   684	    if (!footprintFree(type, column, row)) {
   685	        return -1;
   686	    }
   687	    cAbstractStructure *created = cStructureFactory::getInstance()->createStructure(cellAt(column, row), type, HUMAN, 100);
   688	    if (created == nullptr) {
   689	        return -1;
   690	    }
   691	    created->setBuildingFase(10);
   692	    return created->getStructureId();
   693	}
   694	
   695	int spawnUnit(int type, int column, int row, float hpFraction)
   696	{
   697	    const int id = UNIT_CREATE(cellAt(column, row), type, HUMAN, true, false, hpFraction);
   698	    if (id >= 0) {
   699	        unit[id].bSelected = false;
   700	    }
   701	    return id;
   702	}
   703	
   704	bool buildBase(bool withRadar, float tankHp, BaseResult &result)
   705	{
   706	    players[HUMAN].setTechLevel(9);
   707	    players[HUMAN].getBuildingListUpdater()->onStructureCreated(CONSTYARD);
   708	
   709	    revealAround(kConstyardColumn, kConstyardRow, 16);
   710	
   711	    for (const BaseSpot &spot : kBaseSpots) {
   712	        if (spot.type == RADAR && !withRadar) {
   713	            continue;
   714	        }
   715	        const int id = buildStructure(spot.type, spot.column, spot.row);
   716	        if (id < 0) {
   717	            return false;
   718	        }
   719	        if (spot.type == LIGHTFACTORY) {
   720	            result.factoryId = id;
   721	        }
   722	    }
   723	
   724	    players[HUMAN].update();
   725	    for (int column = 24; column <= 38 && !players[HUMAN].bEnoughPower(); column += 2) {
   726	        if (buildStructure(WINDTRAP, column, 30) < 0) {
   727	            return false;
   728	        }
   729	        players[HUMAN].update();
   730	    }
   731	    if (!players[HUMAN].bEnoughPower()) {
   732	        return false;
   733	    }
   734	
   735	    result.tankId = spawnUnit(TANK, 25, kStreetRow, tankHp);
   736	    result.harvesterId = spawnUnit(HARVESTER, 29, kStreetRow, 1.0f);
   737	    result.mcvId = spawnUnit(MCV, 33, kStreetRow, 1.0f);
   738	    const int others[3] = {spawnUnit(SOLDIER, 27, kStreetRow, 1.0f), spawnUnit(TRIKE, 31, kStreetRow, 1.0f),
   739	                           spawnUnit(QUAD, 35, kStreetRow, 1.0f)};
   740	    if (result.tankId < 0 || result.harvesterId < 0 || result.mcvId < 0 ||
   741	        others[0] < 0 || others[1] < 0 || others[2] < 0) {
   742	        return false;
   743	    }
   744	    unit[result.harvesterId].iCredits = unit[result.harvesterId].getUnitInfo().credit_capacity;
   745	    return true;
   746	}
   747	
   748	void hoverOnCell(int column, int row)
   749	{
   750	    const int cell = cellAt(column, row);
   751	    const int half = static_cast<int>(mapCamera->factorZoomLevel(kTile)) / 2;
   752	    uiaudit::setHover(mapCamera->getWindowXPositionFromCell(cell) + half,
   753	                      mapCamera->getWindowYPositionFromCell(cell) + half);
   754	}
   755	
   756	void selectOnly(int unitId)
   757	{
   758	    for (int i = 0; i < MAX_UNITS; i++) {
   759	        if (unit[i].isValid()) {
   760	            unit[i].bSelected = (i == unitId);
   761	        }
   762	    }
   763	}
   764	
   765	eListType listForKind(int kind)
   766	{
   767	    switch (kind) {
   768	        case uiaudit::GameKind::ListBuild: return eListType::LIST_CONSTYARD;
   769	        case uiaudit::GameKind::ListInfantry: return eListType::LIST_FOOT_UNITS;
   770	        case uiaudit::GameKind::ListVehicles: return eListType::LIST_UNITS;
   771	        case uiaudit::GameKind::ListStarport: return eListType::LIST_STARPORT;
   772	        case uiaudit::GameKind::ListPalace: return eListType::LIST_PALACE;
   773	        case uiaudit::GameKind::ListUpgrades: return eListType::LIST_UPGRADES;
   774	        default: return eListType::LIST_NONE;
   775	    }
   776	}
   777	
   778	}
   779	
   780	bool UiAuditAccess::prepareGameScreen(cGame &game, int house, int kind)
   781	{
   782	    using uiaudit::GameKind;
   783	    if (!enterPlaying(game, house, 22)) {
   784	        return false;
   785	    }
   786	    BaseResult base;
   787	    const bool withRadar = kind != GameKind::RadarNone;
   788	    if (!buildBase(withRadar, kind == GameKind::DamagedUnit ? 0.4f : 1.0f, base)) {
   789	        return false;
   790	    }
   791	    if (kind == GameKind::RadarNoPower) {
   792	        for (int i = 0; i < MAX_STRUCTURES; i++) {
   793	            cAbstractStructure *s = structure[i];
   794	            if (s != nullptr && s->isValid() && s->getOwner() == HUMAN && s->getType() == WINDTRAP) {
   795	                s->setHitPoints(1);
   796	            }
   797	        }
   798	        players[HUMAN].update();
   799	        if (players[HUMAN].bEnoughPower()) {
   800	            return false;
   801	        }
   802	    }
   803	    for (int i = 0; i < 40; i++) {
   804	        drawManager->getMiniMapDrawer()->think();
   805	    }
   806	
   807	    const bool lists = listForKind(kind) != eListType::LIST_NONE;
   808	    const int centerColumn = (kind == GameKind::PlaceAllowed || kind == GameKind::PlaceForbidden) ? 28 : 30;
   809	    mapCamera->centerAndJumpViewPortToCell(cellAt(centerColumn, 26));
   810	    cSideBar *sidebar = players[HUMAN].getSideBar();
   811	    if (sidebar == nullptr) {
   812	        return false;
   813	    }
   814	    cBuildingListDrawer *items = drawManager->getBuildingListDrawer();
   815	
   816	    if (lists) {
   817	        sidebar->setSelectedListId(listForKind(kind));
   818	        cBuildingList *list = sidebar->getList(sidebar->getSelectedListID());
   819	        return list != nullptr && list->isAvailable() && list->getItemCount() > 0;
   820	    }
   821	
   822	    switch (kind) {
   823	        case GameKind::Hud:
   824	        case GameKind::RadarNone:
   825	        case GameKind::RadarNoPower:
   826	            return true;
   827	        case GameKind::Music: {
   828	            MusicController *music = game.m_musicController.get();
   829	            if (music == nullptr) {
   830	                return false;
   831	            }
   832	            MusicTrack track;
   833	            track.externalPath = std::filesystem::path(
   834	                localization::text("Gameplay_theme_with_an_extremely_long_track_title_for_the_layout_audit.ogg",
   835	                                   "Игровая_тема_с_очень_длинным_названием_трека_для_проверки_раскладки.ogg"));
   836	            auto &state = music->m_categories[static_cast<std::size_t>(MusicCategory::Gameplay)];
   837	            state.playlist.setTracks({track});
   838	            state.playlist.next();
   839	            music->m_activeCategory = MusicCategory::Gameplay;
   840	            music->m_hasActiveCategory = true;
   841	            return !music->currentDisplayName().empty();
   842	        }
   843	        case GameKind::DamagedUnit:
   844	            selectOnly(base.tankId);
   845	            return true;
   846	        case GameKind::Harvester:
   847	            selectOnly(base.harvesterId);
   848	            return true;
   849	        case GameKind::Mcv:
   850	            selectOnly(base.mcvId);
   851	            return true;
   852	        case GameKind::Structure:
   853	            players[HUMAN].selected_structure = base.factoryId;
   854	            return true;
   855	        case GameKind::Rally:
   856	            players[HUMAN].selected_structure = base.factoryId;
   857	            structure[base.factoryId]->setRallyPoint(cellAt(28, 32));
   858	            return structure[base.factoryId]->getRallyPoint() >= 0;
   859	        case GameKind::PlaceAllowed:
   860	        case GameKind::PlaceForbidden: {
   861	            cBuildingList *list = sidebar->getList(eListType::LIST_CONSTYARD);
   862	            cBuildingListItem *item = list == nullptr ? nullptr : list->getItemByBuildId(WINDTRAP);
   863	            if (item == nullptr) {
   864	                return false;
   865	            }
   866	            item->setPlaceIt(true);
   867	            players[HUMAN].setContextMouseState(eMouseState::MOUSESTATE_PLACE);
   868	            if (kind == GameKind::PlaceAllowed) {
   869	                for (int dy = 0; dy < 2; dy++) {
   870	                    for (int dx = 0; dx < 2; dx++) {
   871	                        global_map.cellChangeType(cellAt(22 + dx, 25 + dy), TERRAIN_ROCK);
   872	                    }
   873	                }
   874	                hoverOnCell(22, 25);
   875	            }
   876	            else {
   877	                hoverOnCell(29, 24);
   878	            }
   879	            return true;
   880	        }
   881	        case GameKind::GroupSelect: {
   882	            const int cell1 = cellAt(24, 26);
   883	            const int cell2 = cellAt(31, 29);
   884	            cMouse *mouse = game.getMouse();
   885	            mouse->mouse_co_x1 = mapCamera->getWindowXPositionFromCell(cell1);
   886	            mouse->mouse_co_y1 = mapCamera->getWindowYPositionFromCell(cell1);
   887	            mouse->mouse_co_x2 = mapCamera->getWindowXPositionFromCell(cell2);
   888	            mouse->mouse_co_y2 = mapCamera->getWindowYPositionFromCell(cell2);
   889	            uiaudit::setHover(mouse->mouse_co_x2, mouse->mouse_co_y2);
   890	            return mouse->isBoxSelecting();
   891	        }
   892	        case GameKind::Messages: {
   893	            drawManager->setMessage(localization::text("Construction complete: the Windtrap is ready to be placed",
   894	                                                       "Строительство завершено: ветряная электростанция готова к размещению"), true);
   895	            for (int i = 0; i < 90; i++) {
   896	                drawManager->thinkFast();
   897	            }
   898	            players[HUMAN].addNotification(localization::text("Neutral notification", "Обычное уведомление"),
   899	                                           eNotificationType::NEUTRAL);
   900	            players[HUMAN].addNotification(localization::text("Priority notification: Harvester is full",
   901	                                                              "Важное уведомление: комбайн заполнен"),
   902	                                           eNotificationType::PRIORITY);
   903	            players[HUMAN].addNotification(localization::text("Bad news: a structure is under attack",
   904	                                                              "Плохая новость: здание атаковано"),
   905	                                           eNotificationType::BAD);
   906	            return true;
   907	        }
   908	        case GameKind::ItemHover:
   909	        case GameKind::ScrollEnd: {
   910	            sidebar->setSelectedListId(eListType::LIST_CONSTYARD);
   911	            cBuildingList *list = sidebar->getList(eListType::LIST_CONSTYARD);
   912	            if (list == nullptr || list->getItemCount() < 3) {
   913	                return false;
   914	            }
   915	            if (kind == GameKind::ScrollEnd) {
   916	                items->setScrollRow(list, 1000);
   917	                return true;
   918	            }
   919	            const int index = 2;
   920	            const HudLayout layout = items->getLayout(list);
   921	            const cRectangle card = layout.cardRect(index, items->getScrollRow(list));
   922	            const int x = card.getX() + card.getWidth() / 2;
   923	            const int y = card.getY() + card.getHeight() / 2;
   924	            drawManager->setMessage(list->getItem(index)->getInfo(), true);
   925	            for (int i = 0; i < 90; i++) {
   926	                drawManager->thinkFast();
   927	            }
   928	            uiaudit::setHover(x, y);
   929	            return true;
   930	        }
   931	        default:
   932	            return false;
   933	    }
   934	}
```

### src/drawers/cCommandBarDrawer.cpp@9208dcf:90-110

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cCommandBarDrawer.cpp | nl -ba | sed -n '90,110p'
```

Вывод:

```text
    90	        {Command::Deploy, layout.actions[4], localization::text("Deploy", "Развернуть"), commandBindingDisplayName(game.m_commandBindings.deploy, localization::isEnglish()), isDeployCommandEnabled(hasSelectedMcv()), false},
    91	        {Command::Rally, layout.actions[5], localization::text("Rally", "Точка сбора"), commandBindingDisplayName(game.m_commandBindings.rally, localization::isEnglish()), isRallyCommandEnabled(ownsSelectedStructure, ownsSelectedStructure && selectedStructure->canSpawnUnits()), false},
    92	        {Command::Release, layout.actions[6], localization::text("Release", "Выпустить"), commandBindingDisplayName(game.m_commandBindings.release, localization::isEnglish()), isReleaseCommandEnabled(ownsSelectedStructure, ownsSelectedStructure && selectedStructure->getType() == REPAIR), false}
    93	    }};
    94	    m_buttons.assign(actions.begin(), actions.end());
    95	}
    96	
    97	void cCommandBarDrawer::draw()
    98	{
    99	    rebuildLayout();
   100	    if (uiaudit::isEnabled()) {
   101	        uiaudit::recordArea("command-bar", m_panelRect.getX(), m_panelRect.getY(), m_panelRect.getWidth(), m_panelRect.getHeight());
   102	        UiAuditAccess::recordCommandBarClicks(*this);
   103	    }
   104	
   105	    if (m_disabledCommandBarTexture) {
   106	        renderDrawer->renderStrechFullSprite(m_disabledCommandBarTexture, m_panelRect);
   107	    }
   108	    else if (m_commandBarTexture) {
   109	        renderDrawer->renderStrechFullSprite(m_commandBarTexture, m_panelRect);
   110	    }
```

### src/managers/cDrawManager.cpp@9208dcf:280-320

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp | nl -ba | sed -n '280,320p'
```

Вывод:

```text
   280	            optionsRect.getX(),
   281	            optionsRect.getY(),
   282	            optionsRect.getWidth(),
   283	            optionsRect.getHeight())) {
   284	        game.setNextStateToTransitionTo(GAME_OPTIONS);
   285	    }
   286	}
   287	
   288	void cDrawManager::drawTopBarMusicControls()
   289	{
   290	    const HudLayout layout = HudLayout::create(game.m_screenW, game.m_screenH);
   291	    const int left = 143;
   292	    const int right = layout.battlefield.getEndX() - 8;
   293	    drawMusicControls(left, right);
   294	}
   295	
   296	void cDrawManager::drawMusicControls(int left, int right)
   297	{
   298	    const std::string message = m_messageDrawer.getMessage();
   299	    const int reservedMessageWidth = message.empty()
   300	        ? 0
   301	        : m_textDrawer->getTextLength(message) + 16;
   302	    const MusicControlsLayout layout = MusicControlsLayout::create(
   303	        left,
   304	        right,
   305	        reservedMessageWidth
   306	    );
   307	    if (!layout.visible) {
   308	        return;
   309	    }
   310	    if (uiaudit::isEnabled()) {
   311	        uiaudit::recordClick("music-previous", layout.previous.getX(), layout.previous.getY(), layout.previous.getWidth(), layout.previous.getHeight());
   312	        uiaudit::recordClick("music-next", layout.next.getX(), layout.next.getY(), layout.next.getWidth(), layout.next.getHeight());
   313	        uiaudit::recordClick("music-speed-slider", layout.speedSlider.getX(), layout.speedSlider.getY(), layout.speedSlider.getWidth(), layout.speedSlider.getHeight());
   314	    }
   315	
   316	    const Color panel{35, 32, 25, 255};
   317	    const Color border{188, 139, 47, 255};
   318	    const Color borderDark{71, 50, 24, 255};
   319	    const Color text{232, 222, 188, 255};
   320	
```

### src/save/SaveSlotsDialog.cpp@9208dcf:262-280

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/save/SaveSlotsDialog.cpp | nl -ba | sed -n '262,280p'
```

Вывод:

```text
   262	
   263	void SaveSlotsDialog::draw() const
   264	{
   265	    if (!m_open) {
   266	        return;
   267	    }
   268	    if (uiaudit::isEnabled()) {
   269	        uiaudit::dropClicksUnderModal();
   270	        for (std::size_t index = 0; index < m_slotRects.size(); ++index) {
   271	            const cRectangle &slot = m_slotRects[index];
   272	            uiaudit::recordClick(("save-slot:" + std::to_string(index + 1)).c_str(), slot.getX(), slot.getY(), slot.getWidth(), slot.getHeight());
   273	        }
   274	        uiaudit::recordClick("save-name", m_nameRect.getX(), m_nameRect.getY(), m_nameRect.getWidth(), m_nameRect.getHeight());
   275	        uiaudit::recordClick("save-save", m_saveRect.getX(), m_saveRect.getY(), m_saveRect.getWidth(), m_saveRect.getHeight());
   276	        uiaudit::recordClick("save-load", m_loadRect.getX(), m_loadRect.getY(), m_loadRect.getWidth(), m_loadRect.getHeight());
   277	        uiaudit::recordClick("save-close", m_closeRect.getX(), m_closeRect.getY(), m_closeRect.getWidth(), m_closeRect.getHeight());
   278	    }
   279	
   280	    const Color overlay{0, 0, 0, 190};
```

### Поиск UiAuditAccess и uiaudit вне src/debug

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git grep -n -E 'uiaudit::|UiAuditAccess::' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src ':!src/debug'
```

Вывод:

```text
9208dcf5a358f40afd95c99480e4e09f781ed566:src/cGame_logic.cpp:771:        if (uiaudit::isEnabled()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/cGame_logic.cpp:772:            uiaudit::beginFrame(*this);
9208dcf5a358f40afd95c99480e4e09f781ed566:src/cGame_logic.cpp:780:        if (uiaudit::isEnabled()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/cGame_logic.cpp:781:            uiaudit::onFramePresented(*this);
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cCommandBarDrawer.cpp:100:    if (uiaudit::isEnabled()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cCommandBarDrawer.cpp:101:        uiaudit::recordArea("command-bar", m_panelRect.getX(), m_panelRect.getY(), m_panelRect.getWidth(), m_panelRect.getHeight());
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cCommandBarDrawer.cpp:102:        UiAuditAccess::recordCommandBarClicks(*this);
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMiniMapDrawer.cpp:73:    if (uiaudit::isEnabled() && m_player->hasAtleastOneStructure(RADAR)) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMiniMapDrawer.cpp:74:        uiaudit::recordClick("minimap", m_RectFullMinimap.getX(), m_RectFullMinimap.getY(), m_RectFullMinimap.getWidth(), m_RectFullMinimap.getHeight());
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMiniMapDrawer.cpp:84:    if (uiaudit::isEnabled()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMiniMapDrawer.cpp:85:        uiaudit::recordArea("minimap", m_RectFullMinimap.getX(), m_RectFullMinimap.getY(), m_RectFullMinimap.getWidth(), m_RectFullMinimap.getHeight());
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp:69:    if (uiaudit::isEnabled()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp:70:        UiAuditAccess::recordSidebarClicks(*this);
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp:81:    if (uiaudit::isEnabled()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp:82:        uiaudit::recordArea("sidebar", layout.sidebar.getX(), cSideBar::TopBarHeight, layout.sidebar.getWidth(), layout.sidebar.getHeight() - cSideBar::TopBarHeight);
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp:366:    if (uiaudit::isEnabled()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp:367:        uiaudit::recordArea("build-list", layout.catalog.getX(), layout.catalog.getY(), layout.catalog.getWidth(), layout.catalog.getHeight());
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cStructureDrawer.cpp:1031:    if (uiaudit::isEnabled()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cStructureDrawer.cpp:1032:        uiaudit::recordLabel("structure-health", iStructure, "STRUCTURE", draw_x, draw_y, width_x + 1, height_y + 1,
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cStructureDrawer.cpp:1033:                             uiaudit::Rect{visual.getX(), visual.getY(), visual.getWidth(), visual.getHeight()});
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cTextDrawer.cpp:59:    if (uiaudit::isEnabled()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cTextDrawer.cpp:60:        uiaudit::recordText(msg, x, y, cacheEntry->width, cacheEntry->height);
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cTextDrawer.cpp:108:    std::optional<uiaudit::BoxScope> auditBox;
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cTextDrawer.cpp:109:    if (uiaudit::isEnabled()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cTextDrawer.cpp:140:    if (uiaudit::isEnabled()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cTextDrawer.cpp:141:        const uiaudit::Rect box{rect.getX(), rect.getY(), rect.getWidth(), rect.getHeight()};
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cTextDrawer.cpp:142:        uiaudit::recordText(msg, x, y, width, height, &box);
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cTextDrawer.cpp:169:    if (uiaudit::isEnabled()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cTextDrawer.cpp:170:        const uiaudit::Rect box{rect.getX(), rect.getY(), rect.getWidth(), rect.getHeight()};
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cTextDrawer.cpp:171:        uiaudit::recordText(msg, origin.x, origin.y, width, height, &box);
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cTextDrawer.cpp:194:    std::optional<uiaudit::BoxScope> auditBox;
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cTextDrawer.cpp:195:    if (uiaudit::isEnabled()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/gameobjects/units/cUnit.cpp:581:    if (uiaudit::isEnabled()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/gameobjects/units/cUnit.cpp:582:        uiaudit::recordUnitLabel("spice", iID, iType, drawx, drawy, static_cast<int>(width_x), height_y, uiaudit::Rect{visual.getX(), visual.getY(), visual.getWidth(), visual.getHeight()});
9208dcf5a358f40afd95c99480e4e09f781ed566:src/gameobjects/units/cUnit.cpp:633:    if (uiaudit::isEnabled()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/gameobjects/units/cUnit.cpp:634:        uiaudit::recordUnitLabel("health", iID, iType, drawx, drawy, static_cast<int>(width_x), height_y, uiaudit::Rect{visual.getX(), visual.getY(), visual.getWidth(), visual.getHeight()});
9208dcf5a358f40afd95c99480e4e09f781ed566:src/gameobjects/units/cUnit.cpp:660:        if (uiaudit::isEnabled()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/gameobjects/units/cUnit.cpp:661:            uiaudit::beginLabelText();
9208dcf5a358f40afd95c99480e4e09f781ed566:src/gameobjects/units/cUnit.cpp:665:        if (uiaudit::isEnabled()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/gameobjects/units/cUnit.cpp:666:            uiaudit::endLabelText("group", iID, iType, uiaudit::Rect{visual.getX(), visual.getY(), visual.getWidth(), visual.getHeight()});
9208dcf5a358f40afd95c99480e4e09f781ed566:src/gameobjects/units/cUnit.cpp:720:    if (uiaudit::isEnabled()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/gameobjects/units/cUnit.cpp:723:            uiaudit::recordUnitLabel("experience", iID, iType, drawx, drawy, (iStars - 1) * 9 + star->w, star->h, uiaudit::Rect{visual.getX(), visual.getY(), visual.getWidth(), visual.getHeight()});
9208dcf5a358f40afd95c99480e4e09f781ed566:src/gamestates/cChooseHouseState.cpp:111:    if (uiaudit::isEnabled()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/gamestates/cChooseHouseState.cpp:112:        uiaudit::recordClick("house-atreides", houseAtreides.getX(), houseAtreides.getY(), houseAtreides.getWidth(), houseAtreides.getHeight());
9208dcf5a358f40afd95c99480e4e09f781ed566:src/gamestates/cChooseHouseState.cpp:113:        uiaudit::recordClick("house-ordos", houseOrdos.getX(), houseOrdos.getY(), houseOrdos.getWidth(), houseOrdos.getHeight());
9208dcf5a358f40afd95c99480e4e09f781ed566:src/gamestates/cChooseHouseState.cpp:114:        uiaudit::recordClick("house-harkonnen", houseHarkonnen.getX(), houseHarkonnen.getY(), houseHarkonnen.getWidth(), houseHarkonnen.getHeight());
9208dcf5a358f40afd95c99480e4e09f781ed566:src/gamestates/cChooseHouseState.cpp:115:        uiaudit::recordClick("house-back", backButtonRect->getX(), backButtonRect->getY(), backButtonRect->getWidth(), backButtonRect->getHeight());
9208dcf5a358f40afd95c99480e4e09f781ed566:src/gamestates/cCreditsState.cpp:405:    if (uiaudit::isEnabled()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/gamestates/cCreditsState.cpp:406:        uiaudit::recordCanvasClick("credits-speed-up");
9208dcf5a358f40afd95c99480e4e09f781ed566:src/gamestates/cSelectYourNextConquestState.cpp:316:    if (uiaudit::isEnabled() && state == eRegionState::REGSTATE_SELECT_NEXT_CONQUEST) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/gamestates/cSelectYourNextConquestState.cpp:318:        uiaudit::recordClick("campaign-region-map", mapRect.getX(), mapRect.getY(), mapRect.getWidth(), mapRect.getHeight());
9208dcf5a358f40afd95c99480e4e09f781ed566:src/gamestates/cSetupSkirmishState.cpp:452:    if (uiaudit::isEnabled()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/gamestates/cSetupSkirmishState.cpp:454:            uiaudit::recordClick(name, r.getX(), r.getY(), r.getWidth(), r.getHeight());
9208dcf5a358f40afd95c99480e4e09f781ed566:src/gui/GuiButton.cpp:31:    if (uiaudit::isEnabled()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/gui/GuiCheckBox.cpp:26:    if (uiaudit::isEnabled()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/gui/GuiLabel.cpp:25:    if (uiaudit::isEnabled()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/gui/GuiObject.cpp:14:    uiaudit::recordGui(type, m_rect.getX(), m_rect.getY(), m_rect.getWidth(), m_rect.getHeight());
9208dcf5a358f40afd95c99480e4e09f781ed566:src/gui/GuiObject.cpp:19:    uiaudit::recordClick(name.c_str(), m_rect.getX(), m_rect.getY(), m_rect.getWidth(), m_rect.getHeight());
9208dcf5a358f40afd95c99480e4e09f781ed566:src/gui/GuiSlider.cpp:20:    if (uiaudit::isEnabled()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/gui/GuiWindow.cpp:25:    if (uiaudit::isEnabled()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/main.cpp:86:    uiaudit::consumeArguments(argc, argv);
9208dcf5a358f40afd95c99480e4e09f781ed566:src/main.cpp:88:    if (uiaudit::isEnabled() && uiaudit::handleEarlyExit(uiAuditExitCode)) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/main.cpp:114:            if (uiaudit::isEnabled()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/main.cpp:115:                uiaudit::onSetupDone(game);
9208dcf5a358f40afd95c99480e4e09f781ed566:src/main.cpp:132:    if (uiaudit::isEnabled() && (uiAuditError || uiaudit::failed())) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp:234:    if (uiaudit::isEnabled()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp:235:        uiaudit::recordArea("top-panel", 0, 0, game.m_screenW, cSideBar::TopBarHeight);
9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp:275:    if (uiaudit::isEnabled()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp:276:        uiaudit::recordClick("top-options", optionsRect.getX(), optionsRect.getY(), optionsRect.getWidth(), optionsRect.getHeight());
9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp:310:    if (uiaudit::isEnabled()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp:311:        uiaudit::recordClick("music-previous", layout.previous.getX(), layout.previous.getY(), layout.previous.getWidth(), layout.previous.getHeight());
9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp:312:        uiaudit::recordClick("music-next", layout.next.getX(), layout.next.getY(), layout.next.getWidth(), layout.next.getHeight());
9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp:313:        uiaudit::recordClick("music-speed-slider", layout.speedSlider.getX(), layout.speedSlider.getY(), layout.speedSlider.getWidth(), layout.speedSlider.getHeight());
9208dcf5a358f40afd95c99480e4e09f781ed566:src/mentat/AbstractMentat.cpp:406:        if (uiaudit::isEnabled()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/mentat/AbstractMentat.cpp:407:            uiaudit::recordCanvasClick("mentat-skip");
9208dcf5a358f40afd95c99480e4e09f781ed566:src/save/SaveSlotsDialog.cpp:268:    if (uiaudit::isEnabled()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/save/SaveSlotsDialog.cpp:269:        uiaudit::dropClicksUnderModal();
9208dcf5a358f40afd95c99480e4e09f781ed566:src/save/SaveSlotsDialog.cpp:272:            uiaudit::recordClick(("save-slot:" + std::to_string(index + 1)).c_str(), slot.getX(), slot.getY(), slot.getWidth(), slot.getHeight());
9208dcf5a358f40afd95c99480e4e09f781ed566:src/save/SaveSlotsDialog.cpp:274:        uiaudit::recordClick("save-name", m_nameRect.getX(), m_nameRect.getY(), m_nameRect.getWidth(), m_nameRect.getHeight());
9208dcf5a358f40afd95c99480e4e09f781ed566:src/save/SaveSlotsDialog.cpp:275:        uiaudit::recordClick("save-save", m_saveRect.getX(), m_saveRect.getY(), m_saveRect.getWidth(), m_saveRect.getHeight());
9208dcf5a358f40afd95c99480e4e09f781ed566:src/save/SaveSlotsDialog.cpp:276:        uiaudit::recordClick("save-load", m_loadRect.getX(), m_loadRect.getY(), m_loadRect.getWidth(), m_loadRect.getHeight());
9208dcf5a358f40afd95c99480e4e09f781ed566:src/save/SaveSlotsDialog.cpp:277:        uiaudit::recordClick("save-close", m_closeRect.getX(), m_closeRect.getY(), m_closeRect.getWidth(), m_closeRect.getHeight());
9208dcf5a358f40afd95c99480e4e09f781ed566:src/utils/cPlatformLayerInit.cpp:18:    const Uint32 initFlags = uiaudit::isEnabled()
9208dcf5a358f40afd95c99480e4e09f781ed566:src/utils/cScreenInit.cpp:127:    if (uiaudit::isEnabled()) {
```

