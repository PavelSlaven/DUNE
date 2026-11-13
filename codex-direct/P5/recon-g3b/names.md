Ревизия: `dc6e5ffd74f6275390a9c4a676aafdca058df7dd`.

### setPlaceIt

```console
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git grep -n -w 'setPlaceIt' dc6e5ffd74f6275390a9c4a676aafdca058df7dd -- src
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/building/cItemBuilder.cpp:257:            item->setPlaceIt(true);
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/gameobjects/players/cPlayer.cpp:1634:    itemToPlace->setPlaceIt(false);
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/sidebar/cBuildingListItem.h:214:    void setPlaceIt(bool value) {
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/sidebar/cSideBar.cpp:312:        item->setPlaceIt(false);
```


### setSelectedListId

```console
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git grep -n -w 'setSelectedListId' dc6e5ffd74f6275390a9c4a676aafdca058df7dd -- src
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/controls/mousestates/cMouseNormalState.cpp:135:                        m_player->getSideBar()->setSelectedListId(listId);
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/controls/mousestates/cMouseUnitsSelectedState.cpp:154:                    m_player->getSideBar()->setSelectedListId(pStructure->getAssociatedListID());
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/gameobjects/players/cPlayer.cpp:1734:                        getSideBar()->setSelectedListId(eListType::LIST_CONSTYARD);
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/sidebar/cSideBar.cpp:213:            setSelectedListId(eListTypeFromInt(i));
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/sidebar/cSideBar.cpp:228:        m_player->getSideBar()->setSelectedListId(eListType::LIST_NONE);
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/sidebar/cSideBar.cpp:439:            setSelectedListId(eListTypeFromInt(i));
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/sidebar/cSideBar.cpp:446:void cSideBar::setSelectedListId(eListType value)
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/sidebar/cSideBar.cpp:448:    Logger::info(COMP_SIDEBAR, "cSideBar::setSelectedListId", "m_PlayerId = [{}] - old value [{}], new [{}]",
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/sidebar/cSideBar.h:98:    void setSelectedListId(eListType value);
```


```console
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git grep -n -E '^(.*[ *&])?cSideBar::setSelectedListId\(' dc6e5ffd74f6275390a9c4a676aafdca058df7dd -- src
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/sidebar/cSideBar.cpp:446:void cSideBar::setSelectedListId(eListType value)
```


```console
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git show dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/sidebar/cSideBar.cpp | nl -ba | sed -n '446,460p'
   446	void cSideBar::setSelectedListId(eListType value)
   447	{
   448	    Logger::info(COMP_SIDEBAR, "cSideBar::setSelectedListId", "m_PlayerId = [{}] - old value [{}], new [{}]",
   449	                 m_player->getId(), m_selectedListID, eListTypeAsInt(value));
   450	
   451	    int oldListId = m_selectedListID;
   452	    m_selectedListID = eListTypeAsInt(value);
   453	    if (oldListId > -1 && oldListId < LIST_MAX) {
   454	        m_lists[oldListId]->setSelected(false);
   455	    }
   456	
   457	    if (m_selectedListID > -1 && m_selectedListID < LIST_MAX) {
   458	        m_lists[m_selectedListID]->setSelected(true);
   459	    }
   460	}
```


### onStructureCreated

```console
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git grep -n -w 'onStructureCreated' dc6e5ffd74f6275390a9c4a676aafdca058df7dd -- src
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/gameobjects/players/cPlayer.cpp:1731:                    buildingListUpdater->onStructureCreated(commonEvent->entitySpecificType);
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/sidebar/cBuildingListUpdater.cpp:42:void cBuildingListUpdater::onStructureCreated(int structureType)
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/sidebar/cBuildingListUpdater.cpp:44:    m_player->log("onStructureCreated - begin");
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/sidebar/cBuildingListUpdater.cpp:67:    m_player->log("onStructureCreated - end");
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/sidebar/cBuildingListUpdater.cpp:258:        m_player->log("onStructureCreated - added SLAB1 to list");
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/sidebar/cBuildingListUpdater.cpp:263:                m_player->log("onStructureCreated - added BARRACKS to list");
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/sidebar/cBuildingListUpdater.cpp:267:                m_player->log("onStructureCreated - added WOR to list");
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/sidebar/cBuildingListUpdater.cpp:274:            m_player->log("onStructureCreated - added WALL to list");
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/sidebar/cBuildingListUpdater.cpp:278:        m_player->log("onStructureCreated - added WINDTRAP to list");
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/sidebar/cBuildingListUpdater.cpp:292:				m_player->log("onStructureCreated - added WOR to list");
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/sidebar/cBuildingListUpdater.h:34:    void onStructureCreated(int structureType);
```


```console
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git grep -n -E '^(.*[ *&])?cBuildingListUpdater::onStructureCreated\(' dc6e5ffd74f6275390a9c4a676aafdca058df7dd -- src
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/sidebar/cBuildingListUpdater.cpp:42:void cBuildingListUpdater::onStructureCreated(int structureType)
```


```console
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git show dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/sidebar/cBuildingListUpdater.cpp | nl -ba | sed -n '42,68p'
    42	void cBuildingListUpdater::onStructureCreated(int structureType)
    43	{
    44	    m_player->log("onStructureCreated - begin");
    45	
    46	    if (m_player->isHuman()) {
    47	        // always strict (skirmish) mode. Which means, do not cheat...
    48	        onStructureCreatedSkirmishMode(structureType);
    49	        evaluateUpgrades();
    50	    }
    51	    else {
    52	        // AI m_players...
    53	
    54	        if (m_settings->isSkirmish()) {
    55	            // on skirmish mode use the 'strict' / no cheating mode (same as human m_players)
    56	            onStructureCreatedSkirmishMode(structureType);
    57	            evaluateUpgrades();
    58	        }
    59	        else {
    60	            // but on campaign missions, the AI has to cheat in order to be more fun...
    61	            onStructureCreatedCampaignMode(structureType);
    62	            // AI does use upgrades at all...
    63	        }
    64	    }
    65	
    66	    m_player->logStructures();
    67	    m_player->log("onStructureCreated - end");
    68	}
```


### setTechLevel

```console
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git grep -n -w 'setTechLevel' dc6e5ffd74f6275390a9c4a676aafdca058df7dd -- src
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/gameobjects/players/cPlayer.h:156:    void setTechLevel(int theTechLevel) {
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/gameobjects/players/cPlayers.cpp:133:        player->setTechLevel(techLevel);
```


### setBuildingFase

```console
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git grep -n -w 'setBuildingFase' dc6e5ffd74f6275390a9c4a676aafdca058df7dd -- src
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/gameobjects/structures/cAbstractStructure.h:281:    void setBuildingFase(int value) {
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/gameobjects/structures/cStructureFactory.cpp:192:    str->setBuildingFase(1); // prebuild
```


### getItemByBuildId

```console
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git grep -n -w 'getItemByBuildId' dc6e5ffd74f6275390a9c4a676aafdca058df7dd -- src
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/sidebar/cBuildingList.cpp:87:    return getItemByBuildId(item->getBuildId()) != nullptr;
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/sidebar/cBuildingList.cpp:90:cBuildingListItem *cBuildingList::getItemByBuildId(int buildId)
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/sidebar/cBuildingList.cpp:205:    cBuildingListItem *item = getItemByBuildId(buildId);
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/sidebar/cBuildingList.h:120:    cBuildingListItem *getItemByBuildId(int buildId);
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/sidebar/cBuildingListUpdater.cpp:626:            cBuildingListItem *item = listUpgrades->getItemByBuildId(i);
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/sidebar/cSideBar.cpp:166:    return pList->getItemByBuildId(buildId);
```


```console
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git grep -n -E '^(.*[ *&])?cBuildingList::getItemByBuildId\(' dc6e5ffd74f6275390a9c4a676aafdca058df7dd -- src
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/sidebar/cBuildingList.cpp:90:cBuildingListItem *cBuildingList::getItemByBuildId(int buildId)
```


```console
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git show dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/sidebar/cBuildingList.cpp | nl -ba | sed -n '90,102p'
    90	cBuildingListItem *cBuildingList::getItemByBuildId(int buildId)
    91	{
    92	    for (int i =0; i < MAX_ICONS; i++) {
    93	        cBuildingListItem *itemInList = getItem(i);
    94	        if (itemInList == nullptr) continue;
    95	
    96	        // item already in list (same build id)
    97	        if (buildId == itemInList->getBuildId()) {
    98	            return itemInList;
    99	        }
   100	    }
   101	    return nullptr;
   102	}
```


### getRallyPoint

```console
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git grep -n -w 'getRallyPoint' dc6e5ffd74f6275390a9c4a676aafdca058df7dd -- src
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/building/cItemBuilder.cpp:291:                        int rallyPoint = pStructureToDeploy->getRallyPoint();
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/building/cItemBuilder.cpp:451:                int rallyPoint = pStructureToDeploy->getRallyPoint();
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/building/cItemBuilder.cpp:480:            if (pStructureToDeploy->getRallyPoint() > -1) {
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/building/cItemBuilder.cpp:481:                cellToDeploy = pStructureToDeploy->getRallyPoint();
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/gameobjects/structures/cAbstractStructure.cpp:835:    if (getRallyPoint() > -1) {
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/gameobjects/structures/cAbstractStructure.cpp:836:        unitToLeave->move_to(getRallyPoint(), -1, -1);
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/gameobjects/structures/cAbstractStructure.h:200:    int getRallyPoint() {
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/gameobjects/structures/cStarPort.cpp:106:                int rallyPoint = getRallyPoint();
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/managers/cDrawManager.cpp:227:    int rallyPointCell = theStructure->getRallyPoint();
```


### setHitPoints

```console
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git grep -n -w 'setHitPoints' dc6e5ffd74f6275390a9c4a676aafdca058df7dd -- src
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/gameobjects/structures/cAbstractStructure.cpp:565:void cAbstractStructure::setHitPoints(int hp)
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/gameobjects/structures/cAbstractStructure.h:270:    void setHitPoints(int hp);
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/gameobjects/structures/cStructureFactory.cpp:196:    str->setHitPoints(static_cast<int>(fHealth));
```


```console
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git grep -n -E '^(.*[ *&])?cAbstractStructure::setHitPoints\(' dc6e5ffd74f6275390a9c4a676aafdca058df7dd -- src
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/gameobjects/structures/cAbstractStructure.cpp:565:void cAbstractStructure::setHitPoints(int hp)
```


```console
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git show dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/gameobjects/structures/cAbstractStructure.cpp | nl -ba | sed -n '565,579p'
   565	void cAbstractStructure::setHitPoints(int hp)
   566	{
   567	    iHitPoints = hp;
   568	    int maxHp = m_info->getStructureInfo(getType()).hp;
   569	
   570	    if (iHitPoints > maxHp) {
   571	        Logger::warn(COMP_STRUCTURES, "cAbstractStructure::setHitpoints", "setHitpoints({}) while max is {}; capped at max.", hp, maxHp);
   572	
   573	        // will fail (uncomment to let it be capped)
   574	        d2tm_assert(iHitPoints <= maxHp); // may never be more than the maximum of that structure
   575	
   576	        iHitPoints = maxHp;
   577	    }
   578	
   579	}
```


### getBuildingListUpdater

```console
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git grep -n -w 'getBuildingListUpdater' dc6e5ffd74f6275390a9c4a676aafdca058df7dd -- src
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/gameobjects/players/cPlayer.h:165:    cBuildingListUpdater *getBuildingListUpdater() const {
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/sidebar/cSideBar.cpp:321:                m_player->getBuildingListUpdater()->onBuildItemCancelled(item);
```


### getMiniMapDrawer

```console
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git grep -n -w 'getMiniMapDrawer' dc6e5ffd74f6275390a9c4a676aafdca058df7dd -- src
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/controls/cGameControlsContext.cpp:94:    if (m_drawManager->getMiniMapDrawer()->isMouseOver()) {
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/gamestates/cGamePlaying.cpp:328:    m_drawManager->getMiniMapDrawer()->onNotifyMouseEvent(event);
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/managers/cDrawManager.h:68:    cMiniMapDrawer *getMiniMapDrawer() {
```


### getBuildingListDrawer

```console
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git grep -n -w 'getBuildingListDrawer' dc6e5ffd74f6275390a9c4a676aafdca058df7dd -- src
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/drawers/cSideBarDrawer.h:48:    cBuildingListDrawer *getBuildingListDrawer() {
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/managers/cDrawManager.cpp:465:cBuildingListDrawer *cDrawManager::getBuildingListDrawer() {
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/managers/cDrawManager.cpp:466:    return m_sidebarDrawer->getBuildingListDrawer();
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/managers/cDrawManager.h:84:    cBuildingListDrawer *getBuildingListDrawer();
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/sidebar/cSideBar.cpp:190:    cBuildingListDrawer *buildingListDrawer = m_drawManager->getBuildingListDrawer();
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/sidebar/cSideBar.cpp:239:    cBuildingListDrawer *buildingListDrawer = m_drawManager->getBuildingListDrawer();
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/sidebar/cSideBar.cpp:282:    cBuildingListDrawer *buildingListDrawer = m_drawManager->getBuildingListDrawer();
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/sidebar/cSideBar.cpp:356:    m_drawManager->getBuildingListDrawer()->onNotifyMouseEvent(event);
```


```console
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git grep -n -E '^(.*[ *&])?cDrawManager::getBuildingListDrawer\(' dc6e5ffd74f6275390a9c4a676aafdca058df7dd -- src
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/managers/cDrawManager.cpp:465:cBuildingListDrawer *cDrawManager::getBuildingListDrawer() {
```


```console
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git show dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/managers/cDrawManager.cpp | nl -ba | sed -n '465,467p'
   465	cBuildingListDrawer *cDrawManager::getBuildingListDrawer() {
   466	    return m_sidebarDrawer->getBuildingListDrawer();
   467	}
```


### addNotification

```console
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git grep -n -w 'addNotification' dc6e5ffd74f6275390a9c4a676aafdca058df7dd -- src
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
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/gameobjects/players/cPlayer.cpp:1654:                // addNotification(msg, eNotificationType::BAD);
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/gameobjects/players/cPlayer.cpp:1671:                // addNotification(msg, eNotificationType::BAD);
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/gameobjects/players/cPlayer.cpp:1690:                    // addNotification(msg, eNotificationType::PRIORITY);
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/gameobjects/players/cPlayer.cpp:1746:                    //addNotification(msg, eNotificationType::PRIORITY);
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/gameobjects/players/cPlayer.cpp:2227:        // addNotification("You've lost a Harvester.", eNotificationType::PRIORITY);
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/gameobjects/players/cPlayer.cpp:2243:            //addNotification("You have one Harvester left.", eNotificationType::NEUTRAL);
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/gameobjects/players/cPlayer.cpp:2265:                // addNotification("No harvesters and refineries left!", eNotificationType::BAD);
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/gameobjects/players/cPlayer.cpp:2295:            //addNotification("No more Harvester left, reinforcing...", BAD);
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/gamestates/cGamePlaying.cpp:668:        // m_controlledPlayer->addNotification(
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/gui/GuiConsole/GuiConsoleMessageParser.cpp:72:        m_notificationArea->addNotification(std::format("Malformed command: {}", text), eNotificationType::BAD);
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/gui/GuiConsole/GuiConsoleMessageParser.cpp:79:    //     m_notificationArea->addNotification(std::format("Unknown command: {}", text), eNotificationType::BAD);
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/gui/GuiConsole/GuiConsoleMessageParser.cpp:84:        m_notificationArea->addNotification("Help mode.", eNotificationType::NEUTRAL);
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/gui/GuiConsole/GuiConsoleMessageParser.cpp:88:    m_notificationArea->addNotification(std::format("> {}", normalizedText), eNotificationType::NEUTRAL);
```


```console
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git grep -n -E '^(.*[ *&])?cNotificationArea::addNotification\(' dc6e5ffd74f6275390a9c4a676aafdca058df7dd -- src
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/game/cNotificationArea.cpp:35:void cNotificationArea::addNotification(const std::string &msg, eNotificationType type)
```


```console
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git show dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/game/cNotificationArea.cpp | nl -ba | sed -n '35,41p'
    35	void cNotificationArea::addNotification(const std::string &msg, eNotificationType type)
    36	{
    37	    m_notifications.push_back(cPlayerNotification(msg, type));
    38	    std::sort(m_notifications.begin(), m_notifications.end(), [](const cPlayerNotification &lhs, const cPlayerNotification &rhs) {
    39	        return lhs.getTimer() > rhs.getTimer();
    40	    });
    41	}
```


### getWidthOfStructureTypeInCells

```console
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git grep -n -w 'getWidthOfStructureTypeInCells' dc6e5ffd74f6275390a9c4a676aafdca058df7dd -- src
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/controls/mousestates/cMousePlaceState.cpp:110:    int cellWidth = m_context->getStructureUtils()->getWidthOfStructureTypeInCells(structureIdToPlace);
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/drawers/cPlaceItDrawer.cpp:80:    int cellWidth = m_structureUtils->getWidthOfStructureTypeInCells(structureId);
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/utils/cStructureUtils.cpp:59:int cStructureUtils::getWidthOfStructureTypeInCells(int structureType)
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/utils/cStructureUtils.h:48:    int getWidthOfStructureTypeInCells(int structureType);
```


```console
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git grep -n -E '^(.*[ *&])?cStructureUtils::getWidthOfStructureTypeInCells\(' dc6e5ffd74f6275390a9c4a676aafdca058df7dd -- src
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/utils/cStructureUtils.cpp:59:int cStructureUtils::getWidthOfStructureTypeInCells(int structureType)
```


```console
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git show dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/utils/cStructureUtils.cpp | nl -ba | sed -n '59,64p'
    59	int cStructureUtils::getWidthOfStructureTypeInCells(int structureType)
    60	{
    61	    d2tm_assert(structureType >= 0);
    62	    d2tm_assert(structureType < MAX_STRUCTURETYPES);
    63	    return m_infos->getStructureInfo(structureType).bmp_width / TILESIZE_WIDTH_PIXELS;
    64	}
```


### getHeightOfStructureTypeInCells

```console
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git grep -n -w 'getHeightOfStructureTypeInCells' dc6e5ffd74f6275390a9c4a676aafdca058df7dd -- src
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/controls/mousestates/cMousePlaceState.cpp:111:    int cellHeight = m_context->getStructureUtils()->getHeightOfStructureTypeInCells(structureIdToPlace);
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/drawers/cPlaceItDrawer.cpp:81:    int cellHeight = m_structureUtils->getHeightOfStructureTypeInCells(structureId);
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/utils/cStructureUtils.cpp:52:int cStructureUtils::getHeightOfStructureTypeInCells(int structureType)
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/utils/cStructureUtils.h:46:    int getHeightOfStructureTypeInCells(int structureType);
```


```console
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git grep -n -E '^(.*[ *&])?cStructureUtils::getHeightOfStructureTypeInCells\(' dc6e5ffd74f6275390a9c4a676aafdca058df7dd -- src
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/utils/cStructureUtils.cpp:52:int cStructureUtils::getHeightOfStructureTypeInCells(int structureType)
```


```console
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git show dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/utils/cStructureUtils.cpp | nl -ba | sed -n '52,57p'
    52	int cStructureUtils::getHeightOfStructureTypeInCells(int structureType)
    53	{
    54	    d2tm_assert(structureType >= 0);
    55	    d2tm_assert(structureType < MAX_STRUCTURETYPES);
    56	    return m_infos->getStructureInfo(structureType).bmp_height / TILESIZE_HEIGHT_PIXELS;
    57	}
```


### isMouseOverStructure

```console
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git grep -n -w 'isMouseOverStructure' dc6e5ffd74f6275390a9c4a676aafdca058df7dd -- src
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/controls/cGameControlsContext.h:83:    bool isMouseOverStructure() const {
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/drawers/cMouseDrawer.cpp:81:    if (context->isMouseOverStructure()) {
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/drawers/cMouseDrawer.cpp:92:    if (context->isMouseOverStructure()) {
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/drawers/cMouseDrawer.cpp:136:    if (context->isMouseOverStructure()) {
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/drawers/cMouseDrawer.cpp:171:    if (context->isMouseOverStructure()) {
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/drawers/cStructureDrawer.cpp:132:    if (context->isMouseOverStructure()) {
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/utils/cStructureUtils.cpp:282:bool cStructureUtils::isMouseOverStructure(cAbstractStructure *structure, int screenX, int screenY)
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/utils/cStructureUtils.h:54:    bool isMouseOverStructure(cAbstractStructure *structure, int screenX, int screenY);
```


```console
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git grep -n -E '^(.*[ *&])?cStructureUtils::isMouseOverStructure\(' dc6e5ffd74f6275390a9c4a676aafdca058df7dd -- src
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/utils/cStructureUtils.cpp:282:bool cStructureUtils::isMouseOverStructure(cAbstractStructure *structure, int screenX, int screenY)
```


```console
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git show dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/utils/cStructureUtils.cpp | nl -ba | sed -n '282,293p'
   282	bool cStructureUtils::isMouseOverStructure(cAbstractStructure *structure, int screenX, int screenY)
   283	{
   284	    if (!structure) return false;
   285	
   286	    // translate the structure coordinates to screen coordinates
   287	    int drawX = structure->iDrawX();
   288	    int drawY = structure->iDrawY();
   289	    int width = m_mapCamera->factorZoomLevel(structure->getWidthInPixels());
   290	    int height = m_mapCamera->factorZoomLevel(structure->getHeightInPixels());
   291	
   292	    return cRectangle::isWithin(screenX, screenY, drawX, drawY, width, height);
   293	}
```


### getIdOfStructureWhereMouseHovers

```console
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git grep -n -w 'getIdOfStructureWhereMouseHovers' dc6e5ffd74f6275390a9c4a676aafdca058df7dd -- src
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/controls/cGameControlsContext.h:69:    int getIdOfStructureWhereMouseHovers() const {
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/controls/mousestates/cMouseNormalState.cpp:128:            int hoverStructureId = m_context->getIdOfStructureWhereMouseHovers();
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/controls/mousestates/cMouseUnitsSelectedState.cpp:149:            int hoverStructureId = m_context->getIdOfStructureWhereMouseHovers();
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/drawers/cStructureDrawer.cpp:133:        int i = context->getIdOfStructureWhereMouseHovers();
```

