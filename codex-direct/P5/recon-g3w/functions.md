### cUnits::unitCreate — src/gameobjects/units/cUnits.cpp@dc6e5ff:145-252

Команда:
```sh
git show dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/gameobjects/units/cUnits.cpp | nl -ba | sed -n '145,252p'
```
Вывод:
```text
   145	int cUnits::unitCreate(cGameObjectContext* objects, cInfoContext* infos, cEventEmitter* eventEmitter, int iCll, int unitType, int iPlayer, bool bOnStart, bool isReinforcement, float hpPercentage, bool canUseCarryAllReserve) {
   146	    if (!objects->getMapGeometry()->isValidCell(iCll)) {
   147	        Logger::warn(COMP_UNITS, "cUnits::unitCreate", "Invalid cell as param");
   148	        return -1;
   149	    }
   150	
   151	    s_UnitInfo &sUnitType = infos->getUnitInfo(unitType);
   152	
   153	    // check if unit already exists on location
   154	    if (!sUnitType.airborn && objects->getMap()->cellGetIdFromLayer(iCll, MAPID_STRUCTURES) > -1) {
   155	        return -1; // cannot place unit, structure exists at location
   156	    }
   157	
   158	    int mapIdIndex = MAPID_UNITS;
   159	    if (sUnitType.airborn) {
   160	        mapIdIndex = MAPID_AIR;
   161	    }
   162	    else if (unitType == SANDWORM) {
   163	        mapIdIndex = MAPID_WORMS;
   164	    }
   165	
   166	    // check if unit already exists on location
   167	    if (objects->getMap()->cellGetIdFromLayer(iCll, mapIdIndex) > -1) {
   168	        return -1; // cannot place unit
   169	    }
   170	
   171	    // check if placed on invalid terrain type
   172	    if (unitType == SANDWORM) {
   173	        if (!objects->getMap()->isCellPassableForWorm(iCll)) {
   174	            return -1;
   175	        }
   176	    }
   177	
   178	    bool validCell = objects->getMap()->canDeployUnitTypeAtCell(iCll, unitType);
   179	    if (!validCell) {
   180	        return -1;
   181	    }
   182	
   183	    int iNewId = unitNewID(objects, canUseCarryAllReserve);
   184	
   185	    if (iNewId < 0) {
   186	        Logger::warn(COMP_UNITS, "cUnits::unitCreate", "Could not find new unit index");
   187	        return -1;
   188	    }
   189	
   190	    cUnit *newUnit = objects->getUnit(iNewId);
   191	    newUnit->init(iNewId);
   192	
   193	    newUnit->setCell(iCll);
   194	    newUnit->rendering.iBodyFacing = randomFacing();
   195	    newUnit->rendering.iHeadFacing = randomFacing();
   196	
   197	    newUnit->rendering.iBodyShouldFace = newUnit->rendering.iBodyFacing;
   198	    newUnit->rendering.iHeadShouldFace = newUnit->rendering.iHeadFacing;
   199	
   200	    newUnit->iType = unitType;
   201	    newUnit->setHp(sUnitType.hp * hpPercentage);
   202	    newUnit->movement.iGoalCell = iCll;
   203	
   204	    newUnit->deselect();
   205	    newUnit->rendering.bHovered = false;
   206	
   207	    // newUnit->TIMER_bored = RNG::rnd(3000);
   208	    newUnit->boredTimer.reset(RNG::rnd(3000));
   209	
   210	    // newUnit->TIMER_guard = 20 + RNG::rnd(70);
   211	    newUnit->guardTimer.reset(20 + RNG::rnd(70));
   212	    newUnit->recreateDimensions();
   213	
   214	    // Sandworm units are always owned by AI_WORM. INI files typically specify "Fremen"
   215	    // as the house (player 5), but sandworms must be owned by AI_WORM (player 6).
   216	    if (unitType == SANDWORM) {
   217	        iPlayer = AI_WORM;
   218	    }
   219	
   220	    newUnit->iPlayer = iPlayer;
   221	
   222	    // AI player immediately moves unit away
   223	    if (iPlayer > 0 && iPlayer < AI_WORM && !sUnitType.airborn && !bOnStart) {
   224	        int iF = cUnit::freeAroundMove(iNewId, objects);
   225	
   226	        if (iF > -1) {
   227	            newUnit->log("Order move #2");
   228	            objects->getUnit(iNewId)->move_to(iF);
   229	        }
   230	    }
   231	
   232	    // Put on map too!:
   233	    objects->getMap()->cellSetIdForLayer(iCll, mapIdIndex, iNewId);
   234	
   235	    newUnit->updateCellXAndY();
   236	
   237	    objects->getMap()->clearShroud(iCll, sUnitType.sight, iPlayer);
   238	
   239	    const s_GameEvent event {
   240	        .eventType = eGameEventType::GAME_EVENT_CREATED,
   241	        .data = CommonEvent {
   242	            .entityType = eBuildType::UNIT,
   243	            .entityID = iNewId,
   244	            .player = newUnit->getPlayer(),
   245	            .entitySpecificType = unitType,
   246	            .isReinforce = isReinforcement
   247	        }
   248	    };
   249	    eventEmitter->emit(event);
   250	
   251	    return iNewId;
   252	}
```

### cGame::missionInit — src/game/cGame_logic.cpp@dc6e5ff:431-461

Команда:
```sh
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

### cGame::setState — src/game/cGame_logic.cpp@dc6e5ff:944-1230

Команда:
```sh
git show dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/game/cGame_logic.cpp | nl -ba | sed -n '944,1230p'
```
Вывод:
```text
   944	void cGame::setState(int newState)
   945	{
   946	    if (newState == m_state) {
   947	        // ignore
   948	        return;
   949	    }
   950	
   951	    if (newState == GAME_BRIEFING && m_state == GAME_TELLHOUSE && m_campaignProgress &&
   952	        CampaignProgress::supportsHouse(m_dataCampaign->housePlayer) &&
   953	        m_campaignProgress->markStarted(m_dataCampaign->housePlayer)) {
   954	        saveCampaignProgress();
   955	    }
   956	
   957	    auto mapToCreatorState = [](int state, eGameState &mapped) -> bool {
   958	        switch (state) {
   959	            case GAME_INITIALIZE: mapped = eGameState::INITIALIZE; return true;
   960	            case GAME_MENU: mapped = eGameState::MENU; return true;
   961	            case GAME_PLAYING: mapped = eGameState::PLAYING; return true;
   962	            case GAME_BRIEFING: mapped = eGameState::BRIEFING; return true;
   963	            case GAME_EDITOR: mapped = eGameState::EDITOR; return true;
   964	            case GAME_OPTIONS: mapped = eGameState::OPTIONS; return true;
   965	            case GAME_REGION: mapped = eGameState::REGION; return true;
   966	            case GAME_SELECT_HOUSE: mapped = eGameState::SELECT_HOUSE; return true;
   967	            case GAME_TELLHOUSE: mapped = eGameState::TELLHOUSE; return true;
   968	            case GAME_WINNING: mapped = eGameState::WINNING; return true;
   969	            case GAME_SCORING: mapped = eGameState::SCORING; return true;
   970	            case GAME_WINBRIEF: mapped = eGameState::WINBRIEF; return true;
   971	            case GAME_LOSEBRIEF: mapped = eGameState::LOSEBRIEF; return true;
   972	            case GAME_LOSING: mapped = eGameState::LOSING; return true;
   973	            case GAME_SETUPSKIRMISH: mapped = eGameState::SETUPSKIRMISH; return true;
   974	            case GAME_CREDITS: mapped = eGameState::CREDITS; return true;
   975	            case GAME_MISSIONSELECT: mapped = eGameState::MISSIONSELECT; return true;
   976	            case GAME_NEW_MAP_EDITOR: mapped = eGameState::NEW_MAP_EDITOR; return true;
   977	            default:
   978	                return false;
   979	        }
   980	    };
   981	
   982	    eGameState oldStateForLog = eGameState::INITIALIZE;
   983	    eGameState newStateForLog = eGameState::INITIALIZE;
   984	    mapToCreatorState(m_state, oldStateForLog);
   985	    mapToCreatorState(newState, newStateForLog);
   986	    Logger::info(COMP_GAME, "cGame::setState", "Setting state from {}(={}) to {}(={})",
   987	                 m_state, gameStateToString(oldStateForLog), newState, gameStateToString(newStateForLog));
   988	
   989	    if (newState > -1) {
   990	        bool deleteOldState = (newState != GAME_REGION &&
   991	                               newState != GAME_PLAYING &&
   992	                               newState != GAME_EDITOR &&
   993	                               newState != GAME_OPTIONS); // don't delete these states, but re-use!
   994	
   995	        if (newState == GAME_PLAYING) {
   996	            // make sure to delete options menu now
   997	            cGameState *optionsState = nullptr;
   998	            if (m_creatorState->hasState(eGameState::OPTIONS)) {
   999	                optionsState = m_creatorState->getState(eGameState::OPTIONS);
  1000	            }
  1001	
  1002	            if (m_currentState == optionsState) {
  1003	                m_currentState = nullptr;
  1004	            }
  1005	            m_creatorState->destroyState(eGameState::OPTIONS);
  1006	        }
  1007	
  1008	        if (newState == GAME_REGION) {
  1009	            // make sure to delete options menu now
  1010	            cGameState *optionsState = nullptr;
  1011	            if (m_creatorState->hasState(eGameState::OPTIONS)) {
  1012	                optionsState = m_creatorState->getState(eGameState::OPTIONS);
  1013	            }
  1014	
  1015	            if (m_currentState == optionsState) {
  1016	                m_currentState = nullptr;
  1017	            }
  1018	            m_creatorState->destroyState(eGameState::OPTIONS);
  1019	        }
  1020	
  1021	        if (newState == GAME_SELECT_HOUSE) {
  1022	            // a new campaign starts, so drop the conquest state of the previous one (it would skip the intro)
  1023	            if (m_creatorState->hasState(eGameState::REGION) &&
  1024	                    m_currentState == m_creatorState->getState(eGameState::REGION)) {
  1025	                m_currentState = nullptr;
  1026	            }
  1027	            m_creatorState->destroyState(eGameState::REGION);
  1028	        }
  1029	
  1030	        if (newState == GAME_MISSIONSELECT) {
  1031	            deleteOldState = true; // delete old missionselect state everytime
  1032	        }
  1033	
  1034	        cPlayer *humanPlayer = m_gameObjectsContext->getPlayer(HUMAN);
  1035	
  1036	        if (newState == GAME_PLAYING && m_state == GAME_OPTIONS) {
  1037	            // Options was opened while a mission was in progress; resume it instead of
  1038	            // re-running the normal mission-start sequence (which would reset mission stats).
  1039	            m_timeManager->restartTimer();
  1040	            takeBackGroundScreen();
  1041	            humanPlayer->getGameControlsContext()->onFocusMouseStateEvent();
  1042	            m_currentState = m_creatorState->getState(eGameState::PLAYING);
  1043	            m_state = newState;
  1044	            return;
  1045	        }
  1046	
  1047	        cGameState *existingStatePtr = nullptr;
  1048	        eGameState targetCreatorState = eGameState::MENU;
  1049	        if (mapToCreatorState(newState, targetCreatorState)) {
  1050	            if (deleteOldState) {
  1051	                m_creatorState->destroyState(targetCreatorState);
  1052	            }
  1053	            if (m_creatorState->hasState(targetCreatorState)) {
  1054	                existingStatePtr = m_creatorState->getState(targetCreatorState);
  1055	            }
  1056	        }
  1057	
  1058	        if (existingStatePtr) {
  1059	            // no need for re-creating state
  1060	            if (newState == GAME_REGION) {
  1061	                playMusicByTypeForStateTransition(eMusicType::CONQUEST);
  1062	
  1063	                // came from a win/lose brief state, so make sure to set up the next state
  1064	                if (m_state == GAME_WINBRIEF || m_state == GAME_LOSEBRIEF) {
  1065	                    // because `GAME_REGION` == if (existingStatePtr->getType() == GAMESTATE_SELECT_YOUR_NEXT_CONQUEST ||
  1066	                    auto *pState = dynamic_cast<cSelectYourNextConquestState *>(existingStatePtr);
  1067	
  1068	                    // always reset: a cached state left in REGSTATE_FADEOUT would never accept clicks (losing mission 2)
  1069	                    pState->conquerRegions();
  1070	
  1071	                    if (m_missionWasWon) {
  1072	                        // we won
  1073	                        pState->regionSetupNextMission(m_dataCampaign->mission, humanPlayer->getHouse());
  1074	                    }
  1075	                    else {
  1076	                        // OR: did not win
  1077	                        pState->regionSetupLostMission();
  1078	                    }
  1079	                }
  1080	            }
  1081	            else if (newState == GAME_OPTIONS) {
  1082	                // This feels awkward. For now, I'll keep it (if it works), but this will change
  1083	                // once we have a proper game playing state and we need to transition properly between states
  1084	                takeBackGroundScreen();
  1085	                auto *pState = dynamic_cast<cOptionsState *>(existingStatePtr);
  1086	                // you cannot 'go back' to mission select
  1087	                if (m_state != GAME_MISSIONSELECT) {
  1088	                    pState->setPrevState(m_state);
  1089	                }
  1090	                else {
  1091	                    pState->refresh(); // rebuilds UI windows, but keeps background
  1092	                }
  1093	            }
  1094	            else if (newState == GAME_PLAYING && m_state == GAME_OPTIONS) {
  1095	                // resuming the mission from the options menu: keep the drawers (radar), mission stats
  1096	                // and sidebar selection as they are (#993)
  1097	                m_timeManager->startTimer();
  1098	            }
  1099	            else if (newState == GAME_PLAYING) {
  1100	                    m_currentState = existingStatePtr;
  1101	
  1102	                    m_drawManager->reset();
  1103	                    m_drawManager->missionInit();
  1104	                    // evaluate all players, so we have initial 'alive' values set properly
  1105	                    m_players->evaluateStillAliveForAI();
  1106	                    m_gameObjectsContext->getParticles().reset();
  1107	                    // in-between solution until we have a proper combat state object
  1108	                    m_drawManager->init();
  1109	
  1110	                    // handle update
  1111	                    s_GameEvent event {
  1112	                        .eventType = eGameEventType::GAME_EVENT_ABOUT_TO_BEGIN,
  1113	                    };
  1114	                    // the game is about to begin!
  1115	                    onNotifyGameEvent(event);
  1116	                    m_timeManager->startTimer();
  1117	            }
  1118	
  1119	            m_currentState = existingStatePtr;
  1120	        }
  1121	        else {
  1122	            cGameState *newStatePtr = nullptr;
  1123	
  1124	            if (newState == GAME_REGION) {
  1125	                auto *pState = dynamic_cast<cSelectYourNextConquestState *>(m_creatorState->getState(eGameState::REGION));
  1126	                pState->calculateOffset();
  1127	                Logger::info(COMP_INIT, "cGame::loadScenario", "Setup:  WORLD");
  1128	                pState->installWorld();
  1129	                if (m_dataCampaign->mission > 1) {
  1130	                    pState->conquerRegions();
  1131	                }
  1132	                // first creation
  1133	                pState->regionSetupNextMission(m_dataCampaign->mission, humanPlayer->getHouse());
  1134	                playMusicByTypeForStateTransition(eMusicType::CONQUEST);
  1135	
  1136	                newStatePtr = pState;
  1137	            }
  1138	            else if (newState == GAME_SETUPSKIRMISH) {
  1139	                m_players->initPlayers(false, m_gameSettings.get(), m_dataCampaign.get(), m_services.get());
  1140	                newStatePtr = m_creatorState->getState(eGameState::SETUPSKIRMISH);
  1141	                playMusicByTypeForStateTransition(eMusicType::MENU);
  1142	            }
  1143	            else if (newState == GAME_CREDITS) {
  1144	                newStatePtr = m_creatorState->getState(eGameState::CREDITS);
  1145	            }
  1146	            else if (newState == GAME_EDITOR) {
  1147	                newStatePtr = m_creatorState->getState(eGameState::EDITOR);
  1148	            }
  1149	            else if (newState == GAME_VIDEO) {
  1150	                newStatePtr = m_creatorState->getState(eGameState::VIDEO);
  1151	            }
  1152	            else if (newState == GAME_MENU) {
  1153	                m_gameSettings->m_cheatMode = false;
  1154	                newStatePtr = m_creatorState->getState(eGameState::MENU);
  1155	                playMusicByTypeForStateTransition(eMusicType::MENU);
  1156	            }
  1157	            else if (newState == GAME_NEW_MAP_EDITOR) {
  1158	                newStatePtr = m_creatorState->getState(eGameState::NEW_MAP_EDITOR);
  1159	            }
  1160	            else if (newState == GAME_SELECT_HOUSE) {
  1161	                newStatePtr = m_creatorState->getState(eGameState::SELECT_HOUSE);
  1162	            }
  1163	            else if (newState == GAME_MISSIONSELECT) {
  1164	                m_mouse->setTile(MOUSE_NORMAL);
  1165	                newStatePtr = m_creatorState->getState(eGameState::MISSIONSELECT);
  1166	            }
  1167	            else if (newState == GAME_OPTIONS) {
  1168	                takeBackGroundScreen();
  1169	                m_mouse->setTile(MOUSE_NORMAL);
  1170	                if (m_state == GAME_PLAYING) {
  1171	                    // so we don't draw mouse cursor
  1172	                    m_drawManager->drawCombatState();
  1173	                    m_timeManager->pauseTimer();
  1174	                }
  1175	                else {
  1176	                    // we fall back what was on screen, (which includes mouse cursor for now)
  1177	                }
  1178	                newStatePtr = m_creatorState->getState(eGameState::OPTIONS);
  1179	            }
  1180	            else if (newState == GAME_PLAYING) {
  1181	                m_dataCampaign->housePlayer = humanPlayer->getHouse();
  1182	                newStatePtr = m_creatorState->getState(eGameState::PLAYING);
  1183	                m_currentState = newStatePtr;
  1184	
  1185	                m_drawManager->reset();
  1186	                // evaluate all players, so we have initial 'alive' values set properly
  1187	                m_players->evaluateStillAliveForAI();
  1188	                m_gameObjectsContext->getParticles().reset();
  1189	                // in-between solution until we have a proper combat state object
  1190	                m_drawManager->init();
  1191	
  1192	                // handle update
  1193	                s_GameEvent event {
  1194	                    .eventType = eGameEventType::GAME_EVENT_ABOUT_TO_BEGIN,
  1195	                };
  1196	                // the game is about to begin!
  1197	                onNotifyGameEvent(event);
  1198	                m_timeManager->startTimer();
  1199	            }
  1200	            else if (newState == GAME_LOSING) {
  1201	                newStatePtr = m_creatorState->getState(eGameState::LOSING);
  1202	            }
  1203	            else if (newState == GAME_WINNING) {
  1204	                newStatePtr = m_creatorState->getState(eGameState::WINNING);
  1205	            }
  1206	            else if (newState == GAME_SCORING) {
  1207	                newStatePtr = m_creatorState->getState(eGameState::SCORING);
  1208	            }
  1209	            else if (newState == GAME_TELLHOUSE) {
  1210	                m_dataCampaign->housePlayer = m_gameObjectsContext->getPlayer(HUMAN)->getHouse();
  1211	                newStatePtr = m_creatorState->getState(eGameState::TELLHOUSE);
  1212	                playMusicByTypeForStateTransition(eMusicType::BRIEFING);
  1213	            }
  1214	            else if (newState == GAME_BRIEFING) {
  1215	                m_gameSettings->m_cheatMode = false;
  1216	                newStatePtr = m_creatorState->getState(eGameState::BRIEFING);
  1217	                playMusicByTypeForStateTransition(eMusicType::BRIEFING);
  1218	            } else if (newState == GAME_WINBRIEF) {
  1219	                newStatePtr = m_creatorState->getState(eGameState::WINBRIEF);
  1220	                playMusicByTypeForStateTransition(eMusicType::BRIEFING);
  1221	            } else if (newState == GAME_LOSEBRIEF) {
  1222	                newStatePtr = m_creatorState->getState(eGameState::LOSEBRIEF);
  1223	                // the defeated human player is reset to GENERALHOUSE, so use the remembered campaign house
  1224	                m_audioContext->playMusicByTypeForStateTransition(eMusicType::BRIEFING, m_dataCampaign->housePlayer);
  1225	            }
  1226	            m_currentState = newStatePtr;
  1227	        }
  1228	    }
  1229	    m_state = newState;
  1230	}
```

### cGame::transitionStateIfRequired — src/game/cGame_logic.cpp@dc6e5ff:1491-1503

Команда:
```sh
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

### cGamePlaying::missionInit — src/gamestates/cGamePlaying.cpp@dc6e5ff:490-495

Команда:
```sh
git show dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/gamestates/cGamePlaying.cpp | nl -ba | sed -n '490,495p'
```
Вывод:
```text
   490	void cGamePlaying::missionInit()
   491	{
   492	    m_objects->getMap()->thinkSlow();
   493	    m_TIMER_evaluatePlayerStatus = 5;
   494	    m_controlledPlayer = m_objects->getPlayer(HUMAN);
   495	}
```

### cGame::takeBackGroundScreen — src/game/cGame_logic.cpp@dc6e5ff:1710-1715

Команда:
```sh
git show dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/game/cGame_logic.cpp | nl -ba | sed -n '1710,1715p'
```
Вывод:
```text
  1710	void cGame::takeBackGroundScreen()
  1711	{
  1712	    m_sdlDrawer->beginDrawingToTexture(screenTexture);
  1713	    SDL_RenderTexture(renderer, actualRenderer->tex.get(), nullptr, nullptr);
  1714	    m_sdlDrawer->endDrawingToTexture();
  1715	}
```

### cMapCamera::setViewportPosition — src/gameobjects/map/cMapCamera.cpp@dc6e5ff:216-220

Команда:
```sh
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

### cMapCamera::centerAndJumpViewPortToCell — src/gameobjects/map/cMapCamera.cpp@dc6e5ff:171-197

Команда:
```sh
git show dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/gameobjects/map/cMapCamera.cpp | nl -ba | sed -n '171,197p'
```
Вывод:
```text
   171	void cMapCamera::centerAndJumpViewPortToCell(int cell)
   172	{
   173	    // fix any boundaries
   174	    if (cell < 0) cell = 0;
   175	    if (cell >= m_pMap->getMaxCells()) cell = (m_pMap->getMaxCells()-1);
   176	
   177	    int mapCellX = m_mapGeometry->getAbsoluteXPositionFromCell(cell);
   178	    int mapCellY = m_mapGeometry->getAbsoluteYPositionFromCell(cell);
   179	
   180	    // determine the half of our screen
   181	    int halfViewportWidth = m_viewportWidth / 2;
   182	    int halfViewportHeight = m_viewportHeight / 2;
   183	
   184	    // determine the new X and Y position, absolute map coordinates
   185	    int newViewPortX = mapCellX - halfViewportWidth;
   186	    int newViewPortY = mapCellY - halfViewportHeight;
   187	
   188	    // for now, snap it to 32x32 grid
   189	    newViewPortX = (newViewPortX / 32) * 32;
   190	    newViewPortY = (newViewPortY / 32) * 32;
   191	
   192	    jumpTo(newViewPortX, newViewPortY);
   193	
   194	    calibrate();
   195	
   196	    keepViewportWithinReasonableBounds();
   197	}
```

### cMapCamera::onNotifyMouseEvent — src/gameobjects/map/cMapCamera.cpp@dc6e5ff:261-283

Команда:
```sh
git show dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/gameobjects/map/cMapCamera.cpp | nl -ba | sed -n '261,283p'
```
Вывод:
```text
   261	void cMapCamera::onNotifyMouseEvent(const s_MouseEvent &event)
   262	{
   263	    // MOUSE WHEEL scrolling causes zooming in/out
   264	    switch (event.eventType) {
   265	        case eMouseEventType::MOUSE_MOVED_TO:
   266	            onMouseMovedTo(event);
   267	            break;
   268	        case eMouseEventType::MOUSE_SCROLLED_DOWN:
   269	            zoomOut();
   270	            break;
   271	        case eMouseEventType::MOUSE_SCROLLED_UP:
   272	            zoomIn();
   273	            break;
   274	        case eMouseEventType::MOUSE_RIGHT_BUTTON_PRESSED:
   275	            onMouseRightButtonPressed(event);
   276	            break;
   277	        case eMouseEventType::MOUSE_RIGHT_BUTTON_CLICKED:
   278	            onMouseRightButtonClicked(event);
   279	            break;
   280	        default:
   281	            break;
   282	    }
   283	}
```

### cMap::setVisibleFor — src/gameobjects/map/cMap.cpp@dc6e5ff:1130-1134

Команда:
```sh
git show dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/gameobjects/map/cMap.cpp | nl -ba | sed -n '1130,1134p'
```
Вывод:
```text
  1130	void cMap::setVisibleFor(int iCell, cPlayer *pPlayer)
  1131	{
  1132	    if (!pPlayer) return;
  1133	    setVisible(iCell, pPlayer->getId(), true);
  1134	}
```

### cMap::canDeployUnitTypeAtCell — src/gameobjects/map/cMap.cpp@dc6e5ff:228-254

Команда:
```sh
git show dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/gameobjects/map/cMap.cpp | nl -ba | sed -n '228,254p'
```
Вывод:
```text
   228	bool cMap::canDeployUnitTypeAtCell(int iCell, int iUnitType)
   229	{
   230	    if (iCell < 0 || iUnitType < 0)
   231	        return false;
   232	
   233	    s_UnitInfo &unitToDeploy = m_infos->getUnitInfo(iUnitType);
   234	
   235	    bool isAirbornUnit = unitToDeploy.airborn;
   236	    bool isInfantryUnit = unitToDeploy.infantry;
   237	    bool isWorm = (iUnitType == SANDWORM);
   238	
   239	    if (isAirbornUnit) return true;
   240	
   241	    if (isWorm) {
   242	        int wormId = getCellIdWormsLayer(iCell);
   243	        return isCellPassableForWorm(iCell) && wormId < 0;
   244	    }
   245	
   246	    if (isInfantryUnit && isCellPassableForFootUnits(iCell)) return true;
   247	
   248	    if (!isCellPassable(iCell)) return false;
   249	
   250	    int strucId = getCellIdStructuresLayer(iCell);
   251	    int unitId = getCellIdUnitLayer(iCell);
   252	
   253	    return unitId < 0 && strucId < 0;
   254	}
```

### cMap::cellChangeType — src/gameobjects/map/cMap.cpp@dc6e5ff:1363-1377

Команда:
```sh
git show dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/gameobjects/map/cMap.cpp | nl -ba | sed -n '1363,1377p'
```
Вывод:
```text
  1363	void cMap::cellChangeType(int cellNr, int type)
  1364	{
  1365	    tCell *pCell = getCell(cellNr);
  1366	    if (pCell) {
  1367	        if (type > TERRAIN_WALL) {
  1368	            pCell->type = type;
  1369	        }
  1370	        else if (type < TERRAIN_BLOOM) {
  1371	            pCell->type = type;
  1372	        }
  1373	        else {
  1374	            pCell->type = type;
  1375	        }
  1376	    }
  1377	}
```

### cAbstractStructure::setRallyPoint — src/gameobjects/structures/cAbstractStructure.cpp@dc6e5ff:459-464

Команда:
```sh
git show dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/gameobjects/structures/cAbstractStructure.cpp | nl -ba | sed -n '459,464p'
```
Вывод:
```text
   459	void cAbstractStructure::setRallyPoint(int cell)
   460	{
   461	    d2tm_assert(cell > -2); // -1 is allowed (means disable);
   462	    d2tm_assert(cell < m_objects->getMap()->getMaxCells());
   463	    iRallyPoint = cell;
   464	}
```

### cMouse::isBoxSelecting — src/controls/cMouse.cpp@dc6e5ff:243-248

Команда:
```sh
git show dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/controls/cMouse.cpp | nl -ba | sed -n '243,248p'
```
Вывод:
```text
   243	bool cMouse::isBoxSelecting()
   244	{
   245	    return m_mouseCoX1 > -1 && m_mouseCoY1 > -1 &&
   246	           m_mouseCoX2 != m_mouseCoX1 && m_mouseCoY2 != m_mouseCoY1 &&
   247	           m_mouseCoX2 > -1 && m_mouseCoY2 > -1;
   248	}
```

### cPlayer::setContextMouseState — src/gameobjects/players/cPlayer.cpp@dc6e5ff:2638-2641

Команда:
```sh
git show dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/gameobjects/players/cPlayer.cpp | nl -ba | sed -n '2638,2641p'
```
Вывод:
```text
  2638	void cPlayer::setContextMouseState(eMouseState newState)
  2639	{
  2640	    gameControlsContext->setMouseState(newState);
  2641	}
```

### cPlayer::bEnoughPower — src/gameobjects/players/cPlayer.cpp@dc6e5ff:360-373

Команда:
```sh
git show dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/gameobjects/players/cPlayer.cpp | nl -ba | sed -n '360,373p'
```
Вывод:
```text
   360	bool cPlayer::bEnoughPower() const
   361	{
   362	    if (!m_settings->isSkirmish()) {
   363	        // AI cheats on power
   364	        if (!m_Human) {
   365	            // Dune 2 non-skirmish AI cheats; else it will be unplayable in some missions.
   366	            // the Dune 2 AI basically has always enough power, to make it somewhat more 'fair' lets check for
   367	            // ConstYard + Windtrap. If both destroyed we are out of power.
   368	            return hasAtleastOneStructure(WINDTRAP) || hasAtleastOneStructure(CONSTYARD);
   369	        }
   370	    }
   371	
   372	    return powerProduce_ >= powerUsage_;
   373	}
```

### cPlayer::update — src/gameobjects/players/cPlayer.cpp@dc6e5ff:898-904

Команда:
```sh
git show dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/gameobjects/players/cPlayer.cpp | nl -ba | sed -n '898,904p'
```
Вывод:
```text
   898	void cPlayer::update()
   899	{
   900	    powerUsage_ = m_structureUtils->getTotalPowerUsageForPlayer(this);
   901	    powerProduce_ = m_structureUtils->getTotalPowerOutForPlayer(this);
   902	    // update spice capacity
   903	    maxCredits_ = m_structureUtils->getTotalSpiceCapacityForPlayer(this);
   904	}
```

### cPlayer::setHouse — src/gameobjects/players/cPlayer.cpp@dc6e5ff:259-327

Команда:
```sh
git show dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/gameobjects/players/cPlayer.cpp | nl -ba | sed -n '259,327p'
```
Вывод:
```text
   259	void cPlayer::setHouse(int iHouse)
   260	{
   261	    int currentHouse = house;
   262	    Logger::info(COMP_PLAYER, "cPlayer::setHouse", "Current house is [{}/{}], setting house to [{}/{}]",
   263	                 currentHouse, getHouseNameForId(currentHouse), iHouse, getHouseNameForId(iHouse));
   264	    house = iHouse; // use rules of this house
   265	
   266	    difficultySettings = cPlayerDifficultySettings::createFromHouse(iHouse);
   267	    if (m_infos) {
   268	        difficultySettings->setInfoContext(m_infos);
   269	    }
   270	    if (currentHouse != iHouse) {
   271	        Logger::info(COMP_PLAYER, "cPlayer::setHouse", "Current house differs from iHouse, preparing palette.");
   272	
   273	        // now set the different colors based upon house
   274	        minimapColor = m_HousesInfo->getMinimapColor(house);
   275	        emblemBackgroundColor = getEmblemBackgroundColorForHouse(house);
   276	
   277	        destroyAllegroBitmaps();
   278	        const Color houseMaskColor = houseMaskTargetColor(house, minimapColor);
   279	        auto createPlayerTexture = [this, &houseMaskColor](SDL_Surface *surface) -> Texture * {
   280	            Texture *houseTexture = m_gfxdata->createHouseTexture(surface, houseMaskColor);
   281	            if (houseTexture != nullptr) return houseTexture;
   282	            return createPlayerTextureFromIndexedSurfaceWithPalette(m_renderer, this, surface, TransparentColorIndex, m_gfxdata->getDensity());
   283	        };
   284	        bmp_flag = createPlayerTexture(m_gfxdata->getSurface(BUILDING_FLAG_LARGE));
   285	        bmp_flag_small = createPlayerTexture(m_gfxdata->getSurface(BUILDING_FLAG_SMALL));
   286	
   287	        // now copy / set all structures for this player, with the correct color
   288	        for (int i = 0; i < MAX_STRUCTURETYPES; i++) {
   289	            s_StructureInfo &structureType = m_infos->getStructureInfo(i);
   290	
   291	            if (!structureType.configured) continue;
   292	
   293	            bmp_structure[i].reset(createPlayerTexture(structureType.bmp));
   294	            if (!bmp_structure[i]) {
   295	                std::cerr << "Could not create bmp structure bitmap!? - Imminent crash.\n";
   296	            }
   297	
   298	            // flash bitmaps are structure type index * 2
   299	            if (structureType.flash) {
   300	                int j = MAX_STRUCTURETYPES + i;
   301	                SDL_Surface *bitmap = SDL_CreateSurface(structureType.bmp->w, structureType.bmp->h, SDL_PIXELFORMAT_RGBA32);
   302	                if (!bitmap) {
   303	                    std::cerr << "Could not create FLASH bmp structure bitmap!? - Imminent crash.\n";
   304	                }
   305	                bmp_structure[j].reset(createPlayerTexture(structureType.flash));
   306	            }
   307	
   308	        }
   309	
   310	
   311	        // same goes for units
   312	        for (int i = 0; i < MAX_UNITTYPES; i++) {
   313	            s_UnitInfo &unitInfo = m_infos->getUnitInfo(i);
   314	
   315	            if (!unitInfo.configured) continue;
   316	
   317	            bmp_unit[i].reset(createPlayerTexture(unitInfo.bmp));
   318	            if (!bmp_unit[i]) {
   319	                std::cerr << "Could not create bmp unit bitmap!? - Imminent crash.\n";
   320	            }
   321	            if (unitInfo.top) {
   322	
   323	                bmp_unit_top[i].reset(createPlayerTexture(unitInfo.top));
   324	            }
   325	        }
   326	    }
   327	}
```

### cUnit::isSelected — src/gameobjects/units/cUnit.cpp@dc6e5ff:3814-3816

Команда:
```sh
git show dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/gameobjects/units/cUnit.cpp | nl -ba | sed -n '3814,3816p'
```
Вывод:
```text
  3814	bool cUnit::isSelected() const {
  3815	    return m_bSelected;
  3816	}
```

### cTimeManager::onWindowFocusLost — src/game/cTimeManager.cpp@dc6e5ff:94-97

Команда:
```sh
git show dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/game/cTimeManager.cpp | nl -ba | sed -n '94,97p'
```
Вывод:
```text
    94	void cTimeManager::onWindowFocusLost()
    95	{
    96	    m_focusLostTime = SDL_GetTicks();
    97	}
```
