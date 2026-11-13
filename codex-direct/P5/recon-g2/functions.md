# Функции

## Заголовки из второго поиска

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ PORT=acddd297b21ec200c7090dd2f1b73e014e2b74c0
$ git grep -n -E '^[A-Za-z_].*::[A-Za-z_]*([Mm]entat|[Ss]kirmish|[Mm]ission|[Rr]egion)[A-Za-z_]*\(' $PORT -- src/game | grep -v ';$'
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/CampaignProgress.cpp:155:int CampaignProgress::nextMission(int house) const
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/CampaignProgress.cpp:160:int CampaignProgress::highestUnlockedMission(int house) const
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/CampaignProgress.cpp:182:bool CampaignProgress::recordMissionVictory(int house, int mission)
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGameConditionChecker.cpp:35:void cGameConditionChecker::missionInit()
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGameConditionChecker.cpp:53:bool cGameConditionChecker::isMissionWon() const
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGameConditionChecker.cpp:85:bool cGameConditionChecker::isMissionFailed() const
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGame_logic.cpp:431:void cGame::missionInit()
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGame_logic.cpp:472:void cGame::setMissionWon()
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGame_logic.cpp:500:void cGame::setMissionLost()
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGame_logic.cpp:913:void cGame::jumpToSelectYourNextConquestMission(int missionNr)
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGame_logic.cpp:1239:void cGame::prepareMentatForPlayer()
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGame_logic.cpp:1257:void cGame::prepareMentatToTellAboutHouse(int house)
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGame_logic.cpp:1307:void cGame::changeStateFromMentat()
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGame_logic.cpp:1720:void cGame::checkMissionWinOrFail()
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cMissionStatsCollector.cpp:25:cMissionStatsCollector::cMissionStatsCollector(cGameObjectContext *objects) : m_objects(objects)
```

## Определения

### cGame::setState — src/game/cGame_logic.cpp@acddd29:942-1228

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ PORT=acddd297b21ec200c7090dd2f1b73e014e2b74c0
$ git grep -n -E '^(.*[ *&])?cGame::setState\(' $PORT -- src | grep -v ';$'
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGame_logic.cpp:942:void cGame::setState(int newState)
$ git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGame_logic.cpp | nl -ba | sed -n '942,1228p'
   942	void cGame::setState(int newState)
   943	{
   944	    if (newState == m_state) {
   945	        // ignore
   946	        return;
   947	    }
   948	
   949	    if (newState == GAME_BRIEFING && m_state == GAME_TELLHOUSE && m_campaignProgress &&
   950	        CampaignProgress::supportsHouse(m_dataCampaign->housePlayer) &&
   951	        m_campaignProgress->markStarted(m_dataCampaign->housePlayer)) {
   952	        saveCampaignProgress();
   953	    }
   954	
   955	    auto mapToCreatorState = [](int state, eGameState &mapped) -> bool {
   956	        switch (state) {
   957	            case GAME_INITIALIZE: mapped = eGameState::INITIALIZE; return true;
   958	            case GAME_MENU: mapped = eGameState::MENU; return true;
   959	            case GAME_PLAYING: mapped = eGameState::PLAYING; return true;
   960	            case GAME_BRIEFING: mapped = eGameState::BRIEFING; return true;
   961	            case GAME_EDITOR: mapped = eGameState::EDITOR; return true;
   962	            case GAME_OPTIONS: mapped = eGameState::OPTIONS; return true;
   963	            case GAME_REGION: mapped = eGameState::REGION; return true;
   964	            case GAME_SELECT_HOUSE: mapped = eGameState::SELECT_HOUSE; return true;
   965	            case GAME_TELLHOUSE: mapped = eGameState::TELLHOUSE; return true;
   966	            case GAME_WINNING: mapped = eGameState::WINNING; return true;
   967	            case GAME_SCORING: mapped = eGameState::SCORING; return true;
   968	            case GAME_WINBRIEF: mapped = eGameState::WINBRIEF; return true;
   969	            case GAME_LOSEBRIEF: mapped = eGameState::LOSEBRIEF; return true;
   970	            case GAME_LOSING: mapped = eGameState::LOSING; return true;
   971	            case GAME_SETUPSKIRMISH: mapped = eGameState::SETUPSKIRMISH; return true;
   972	            case GAME_CREDITS: mapped = eGameState::CREDITS; return true;
   973	            case GAME_MISSIONSELECT: mapped = eGameState::MISSIONSELECT; return true;
   974	            case GAME_NEW_MAP_EDITOR: mapped = eGameState::NEW_MAP_EDITOR; return true;
   975	            default:
   976	                return false;
   977	        }
   978	    };
   979	
   980	    eGameState oldStateForLog = eGameState::INITIALIZE;
   981	    eGameState newStateForLog = eGameState::INITIALIZE;
   982	    mapToCreatorState(m_state, oldStateForLog);
   983	    mapToCreatorState(newState, newStateForLog);
   984	    Logger::info(COMP_GAME, "cGame::setState", "Setting state from {}(={}) to {}(={})",
   985	                 m_state, gameStateToString(oldStateForLog), newState, gameStateToString(newStateForLog));
   986	
   987	    if (newState > -1) {
   988	        bool deleteOldState = (newState != GAME_REGION &&
   989	                               newState != GAME_PLAYING &&
   990	                               newState != GAME_EDITOR &&
   991	                               newState != GAME_OPTIONS); // don't delete these states, but re-use!
   992	
   993	        if (newState == GAME_PLAYING) {
   994	            // make sure to delete options menu now
   995	            cGameState *optionsState = nullptr;
   996	            if (m_creatorState->hasState(eGameState::OPTIONS)) {
   997	                optionsState = m_creatorState->getState(eGameState::OPTIONS);
   998	            }
   999	
  1000	            if (m_currentState == optionsState) {
  1001	                m_currentState = nullptr;
  1002	            }
  1003	            m_creatorState->destroyState(eGameState::OPTIONS);
  1004	        }
  1005	
  1006	        if (newState == GAME_REGION) {
  1007	            // make sure to delete options menu now
  1008	            cGameState *optionsState = nullptr;
  1009	            if (m_creatorState->hasState(eGameState::OPTIONS)) {
  1010	                optionsState = m_creatorState->getState(eGameState::OPTIONS);
  1011	            }
  1012	
  1013	            if (m_currentState == optionsState) {
  1014	                m_currentState = nullptr;
  1015	            }
  1016	            m_creatorState->destroyState(eGameState::OPTIONS);
  1017	        }
  1018	
  1019	        if (newState == GAME_SELECT_HOUSE) {
  1020	            // a new campaign starts, so drop the conquest state of the previous one (it would skip the intro)
  1021	            if (m_creatorState->hasState(eGameState::REGION) &&
  1022	                    m_currentState == m_creatorState->getState(eGameState::REGION)) {
  1023	                m_currentState = nullptr;
  1024	            }
  1025	            m_creatorState->destroyState(eGameState::REGION);
  1026	        }
  1027	
  1028	        if (newState == GAME_MISSIONSELECT) {
  1029	            deleteOldState = true; // delete old missionselect state everytime
  1030	        }
  1031	
  1032	        cPlayer *humanPlayer = m_gameObjectsContext->getPlayer(HUMAN);
  1033	
  1034	        if (newState == GAME_PLAYING && m_state == GAME_OPTIONS) {
  1035	            // Options was opened while a mission was in progress; resume it instead of
  1036	            // re-running the normal mission-start sequence (which would reset mission stats).
  1037	            m_timeManager->restartTimer();
  1038	            takeBackGroundScreen();
  1039	            humanPlayer->getGameControlsContext()->onFocusMouseStateEvent();
  1040	            m_currentState = m_creatorState->getState(eGameState::PLAYING);
  1041	            m_state = newState;
  1042	            return;
  1043	        }
  1044	
  1045	        cGameState *existingStatePtr = nullptr;
  1046	        eGameState targetCreatorState = eGameState::MENU;
  1047	        if (mapToCreatorState(newState, targetCreatorState)) {
  1048	            if (deleteOldState) {
  1049	                m_creatorState->destroyState(targetCreatorState);
  1050	            }
  1051	            if (m_creatorState->hasState(targetCreatorState)) {
  1052	                existingStatePtr = m_creatorState->getState(targetCreatorState);
  1053	            }
  1054	        }
  1055	
  1056	        if (existingStatePtr) {
  1057	            // no need for re-creating state
  1058	            if (newState == GAME_REGION) {
  1059	                playMusicByTypeForStateTransition(eMusicType::CONQUEST);
  1060	
  1061	                // came from a win/lose brief state, so make sure to set up the next state
  1062	                if (m_state == GAME_WINBRIEF || m_state == GAME_LOSEBRIEF) {
  1063	                    // because `GAME_REGION` == if (existingStatePtr->getType() == GAMESTATE_SELECT_YOUR_NEXT_CONQUEST ||
  1064	                    auto *pState = dynamic_cast<cSelectYourNextConquestState *>(existingStatePtr);
  1065	
  1066	                    // always reset: a cached state left in REGSTATE_FADEOUT would never accept clicks (losing mission 2)
  1067	                    pState->conquerRegions();
  1068	
  1069	                    if (m_missionWasWon) {
  1070	                        // we won
  1071	                        pState->regionSetupNextMission(m_dataCampaign->mission, humanPlayer->getHouse());
  1072	                    }
  1073	                    else {
  1074	                        // OR: did not win
  1075	                        pState->regionSetupLostMission();
  1076	                    }
  1077	                }
  1078	            }
  1079	            else if (newState == GAME_OPTIONS) {
  1080	                // This feels awkward. For now, I'll keep it (if it works), but this will change
  1081	                // once we have a proper game playing state and we need to transition properly between states
  1082	                takeBackGroundScreen();
  1083	                auto *pState = dynamic_cast<cOptionsState *>(existingStatePtr);
  1084	                // you cannot 'go back' to mission select
  1085	                if (m_state != GAME_MISSIONSELECT) {
  1086	                    pState->setPrevState(m_state);
  1087	                }
  1088	                else {
  1089	                    pState->refresh(); // rebuilds UI windows, but keeps background
  1090	                }
  1091	            }
  1092	            else if (newState == GAME_PLAYING && m_state == GAME_OPTIONS) {
  1093	                // resuming the mission from the options menu: keep the drawers (radar), mission stats
  1094	                // and sidebar selection as they are (#993)
  1095	                m_timeManager->startTimer();
  1096	            }
  1097	            else if (newState == GAME_PLAYING) {
  1098	                    m_currentState = existingStatePtr;
  1099	
  1100	                    m_drawManager->reset();
  1101	                    m_drawManager->missionInit();
  1102	                    // evaluate all players, so we have initial 'alive' values set properly
  1103	                    m_players->evaluateStillAliveForAI();
  1104	                    m_gameObjectsContext->getParticles().reset();
  1105	                    // in-between solution until we have a proper combat state object
  1106	                    m_drawManager->init();
  1107	
  1108	                    // handle update
  1109	                    s_GameEvent event {
  1110	                        .eventType = eGameEventType::GAME_EVENT_ABOUT_TO_BEGIN,
  1111	                    };
  1112	                    // the game is about to begin!
  1113	                    onNotifyGameEvent(event);
  1114	                    m_timeManager->startTimer();
  1115	            }
  1116	
  1117	            m_currentState = existingStatePtr;
  1118	        }
  1119	        else {
  1120	            cGameState *newStatePtr = nullptr;
  1121	
  1122	            if (newState == GAME_REGION) {
  1123	                auto *pState = dynamic_cast<cSelectYourNextConquestState *>(m_creatorState->getState(eGameState::REGION));
  1124	                pState->calculateOffset();
  1125	                Logger::info(COMP_INIT, "cGame::loadScenario", "Setup:  WORLD");
  1126	                pState->installWorld();
  1127	                if (m_dataCampaign->mission > 1) {
  1128	                    pState->conquerRegions();
  1129	                }
  1130	                // first creation
  1131	                pState->regionSetupNextMission(m_dataCampaign->mission, humanPlayer->getHouse());
  1132	                playMusicByTypeForStateTransition(eMusicType::CONQUEST);
  1133	
  1134	                newStatePtr = pState;
  1135	            }
  1136	            else if (newState == GAME_SETUPSKIRMISH) {
  1137	                m_players->initPlayers(false, m_gameSettings.get(), m_dataCampaign.get(), m_services.get());
  1138	                newStatePtr = m_creatorState->getState(eGameState::SETUPSKIRMISH);
  1139	                playMusicByTypeForStateTransition(eMusicType::MENU);
  1140	            }
  1141	            else if (newState == GAME_CREDITS) {
  1142	                newStatePtr = m_creatorState->getState(eGameState::CREDITS);
  1143	            }
  1144	            else if (newState == GAME_EDITOR) {
  1145	                newStatePtr = m_creatorState->getState(eGameState::EDITOR);
  1146	            }
  1147	            else if (newState == GAME_VIDEO) {
  1148	                newStatePtr = m_creatorState->getState(eGameState::VIDEO);
  1149	            }
  1150	            else if (newState == GAME_MENU) {
  1151	                m_gameSettings->m_cheatMode = false;
  1152	                newStatePtr = m_creatorState->getState(eGameState::MENU);
  1153	                playMusicByTypeForStateTransition(eMusicType::MENU);
  1154	            }
  1155	            else if (newState == GAME_NEW_MAP_EDITOR) {
  1156	                newStatePtr = m_creatorState->getState(eGameState::NEW_MAP_EDITOR);
  1157	            }
  1158	            else if (newState == GAME_SELECT_HOUSE) {
  1159	                newStatePtr = m_creatorState->getState(eGameState::SELECT_HOUSE);
  1160	            }
  1161	            else if (newState == GAME_MISSIONSELECT) {
  1162	                m_mouse->setTile(MOUSE_NORMAL);
  1163	                newStatePtr = m_creatorState->getState(eGameState::MISSIONSELECT);
  1164	            }
  1165	            else if (newState == GAME_OPTIONS) {
  1166	                takeBackGroundScreen();
  1167	                m_mouse->setTile(MOUSE_NORMAL);
  1168	                if (m_state == GAME_PLAYING) {
  1169	                    // so we don't draw mouse cursor
  1170	                    m_drawManager->drawCombatState();
  1171	                    m_timeManager->pauseTimer();
  1172	                }
  1173	                else {
  1174	                    // we fall back what was on screen, (which includes mouse cursor for now)
  1175	                }
  1176	                newStatePtr = m_creatorState->getState(eGameState::OPTIONS);
  1177	            }
  1178	            else if (newState == GAME_PLAYING) {
  1179	                m_dataCampaign->housePlayer = humanPlayer->getHouse();
  1180	                newStatePtr = m_creatorState->getState(eGameState::PLAYING);
  1181	                m_currentState = newStatePtr;
  1182	
  1183	                m_drawManager->reset();
  1184	                // evaluate all players, so we have initial 'alive' values set properly
  1185	                m_players->evaluateStillAliveForAI();
  1186	                m_gameObjectsContext->getParticles().reset();
  1187	                // in-between solution until we have a proper combat state object
  1188	                m_drawManager->init();
  1189	
  1190	                // handle update
  1191	                s_GameEvent event {
  1192	                    .eventType = eGameEventType::GAME_EVENT_ABOUT_TO_BEGIN,
  1193	                };
  1194	                // the game is about to begin!
  1195	                onNotifyGameEvent(event);
  1196	                m_timeManager->startTimer();
  1197	            }
  1198	            else if (newState == GAME_LOSING) {
  1199	                newStatePtr = m_creatorState->getState(eGameState::LOSING);
  1200	            }
  1201	            else if (newState == GAME_WINNING) {
  1202	                newStatePtr = m_creatorState->getState(eGameState::WINNING);
  1203	            }
  1204	            else if (newState == GAME_SCORING) {
  1205	                newStatePtr = m_creatorState->getState(eGameState::SCORING);
  1206	            }
  1207	            else if (newState == GAME_TELLHOUSE) {
  1208	                m_dataCampaign->housePlayer = m_gameObjectsContext->getPlayer(HUMAN)->getHouse();
  1209	                newStatePtr = m_creatorState->getState(eGameState::TELLHOUSE);
  1210	                playMusicByTypeForStateTransition(eMusicType::BRIEFING);
  1211	            }
  1212	            else if (newState == GAME_BRIEFING) {
  1213	                m_gameSettings->m_cheatMode = false;
  1214	                newStatePtr = m_creatorState->getState(eGameState::BRIEFING);
  1215	                playMusicByTypeForStateTransition(eMusicType::BRIEFING);
  1216	            } else if (newState == GAME_WINBRIEF) {
  1217	                newStatePtr = m_creatorState->getState(eGameState::WINBRIEF);
  1218	                playMusicByTypeForStateTransition(eMusicType::BRIEFING);
  1219	            } else if (newState == GAME_LOSEBRIEF) {
  1220	                newStatePtr = m_creatorState->getState(eGameState::LOSEBRIEF);
  1221	                // the defeated human player is reset to GENERALHOUSE, so use the remembered campaign house
  1222	                m_audioContext->playMusicByTypeForStateTransition(eMusicType::BRIEFING, m_dataCampaign->housePlayer);
  1223	            }
  1224	            m_currentState = newStatePtr;
  1225	        }
  1226	    }
  1227	    m_state = newState;
  1228	}
```

### cGame::transitionStateIfRequired — src/game/cGame_logic.cpp@acddd29:1489-1501

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ PORT=acddd297b21ec200c7090dd2f1b73e014e2b74c0
$ git grep -n -E '^(.*[ *&])?cGame::transitionStateIfRequired\(' $PORT -- src | grep -v ';$'
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGame_logic.cpp:1489:void cGame::transitionStateIfRequired()
$ git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGame_logic.cpp | nl -ba | sed -n '1489,1501p'
  1489	void cGame::transitionStateIfRequired()
  1490	{
  1491	    if (m_nextState > -1) {
  1492	        setState(m_nextState);
  1493	
  1494	        if (m_nextState == GAME_BRIEFING) {
  1495	            playMusicByType(eMusicType::BRIEFING);
  1496	            prepareMentatForPlayer();
  1497	        }
  1498	
  1499	        m_nextState = -1;
  1500	    }
  1501	}
```

### cGame::setNextStateToTransitionTo — src/game/cGame_logic.cpp@acddd29:1503-1506

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ PORT=acddd297b21ec200c7090dd2f1b73e014e2b74c0
$ git grep -n -E '^(.*[ *&])?cGame::setNextStateToTransitionTo\(' $PORT -- src | grep -v ';$'
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGame_logic.cpp:1503:void cGame::setNextStateToTransitionTo(int newState)
$ git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGame_logic.cpp | nl -ba | sed -n '1503,1506p'
  1503	void cGame::setNextStateToTransitionTo(int newState)
  1504	{
  1505	    m_nextState = newState;
  1506	}
```

### cGame::jumpToSelectYourNextConquestMission — src/game/cGame_logic.cpp@acddd29:913-940

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ PORT=acddd297b21ec200c7090dd2f1b73e014e2b74c0
$ git grep -n -E '^(.*[ *&])?cGame::jumpToSelectYourNextConquestMission\(' $PORT -- src | grep -v ';$'
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGame_logic.cpp:913:void cGame::jumpToSelectYourNextConquestMission(int missionNr)
$ git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGame_logic.cpp | nl -ba | sed -n '913,940p'
   913	void cGame::jumpToSelectYourNextConquestMission(int missionNr)
   914	{
   915	    if (missionNr == CampaignProgress::FIRST_MISSION) {
   916	        m_dataCampaign->mission = CampaignProgress::FIRST_MISSION;
   917	        m_dataCampaign->region = 1;
   918	        return;
   919	    }
   920	
   921	    cGameState *state = m_creatorState->getOrCreateState(eGameState::REGION, true);
   922	    auto *pState = dynamic_cast<cSelectYourNextConquestState *>(state);
   923	    if (!pState) {
   924	        Logger::error(COMP_GAME, "cGame::jumpToSelectYourNextConquestMission", "Failed to create cSelectYourNextConquestState for mission {}. Aborting.", missionNr);
   925	        return;
   926	    }
   927	
   928	    pState->calculateOffset();
   929	    pState->installWorld();
   930	
   931	    cPlayer *humanPlayer = m_gameObjectsContext->getPlayer(HUMAN);
   932	    int missionZeroBased = missionNr - 1;
   933	    m_dataCampaign->mission = missionZeroBased;
   934	
   935	    // a 'missionX.ini' file is from 1 til (including) 8
   936	    // to play mission 2 (passed as missionNr param), we have to load up mission1.ini
   937	    // meaning we have to use the 'zero based' value here
   938	    pState->fastForwardUntilMission(missionZeroBased, humanPlayer->getHouse());
   939	    pState->regionSetupNextMission(missionZeroBased, humanPlayer->getHouse());
   940	}
```

### cChooseHouseState::draw — src/gamestates/cChooseHouseState.cpp@acddd29:111-142

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ PORT=acddd297b21ec200c7090dd2f1b73e014e2b74c0
$ git grep -n -E '^(.*[ *&])?cChooseHouseState::draw\(' $PORT -- src | grep -v ';$'
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cChooseHouseState.cpp:111:void cChooseHouseState::draw() const
$ git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cChooseHouseState.cpp | nl -ba | sed -n '111,142p'
   111	void cChooseHouseState::draw() const
   112	{
   113	    drawHdBackground();
   114	
   115	    const std::string title = "CHOOSE YOUR HOUSE";
   116	    const int titleWidth = m_textDrawer->getTextLength(title);
   117	    m_textDrawer->drawText(
   118	        (m_settings->getScreenW() - titleWidth) / 2,
   119	        48,
   120	        Color{231, 190, 91, 255},
   121	        title);
   122	
   123	    drawHdHouseCard(houseAtreides, bmp_HouseAtreides, "ATREIDES");
   124	    drawHdHouseCard(houseOrdos, bmp_HouseOrdos, "ORDOS");
   125	    drawHdHouseCard(houseHarkonnen, bmp_HouseHarkonnen, "HARKONNEN");
   126	    drawHdHouseCard(houseSardaukar, bmp_HouseSardaukar, "SARDAUKAR");
   127	
   128	    m_sdlDrawer->renderRectFillColor(
   129	        backButtonRect,
   130	        hoversOverBackButton ? Color{43, 49, 53, 245} : Color{25, 31, 35, 245});
   131	    m_sdlDrawer->renderRectColor(backButtonRect, Color{195, 142, 43, 255});
   132	    const std::string backLabel = "Back";
   133	    const int backLabelWidth = m_textDrawer->getTextLength(backLabel);
   134	    m_textDrawer->drawText(
   135	        backButtonRect.getX() + (backButtonRect.getWidth() - backLabelWidth) / 2,
   136	        backButtonRect.getY() +
   137	            (backButtonRect.getHeight() - m_textDrawer->getFontHeight()) / 2,
   138	        hoversOverBackButton ? Color{255, 224, 139, 255} : Color{238, 229, 204, 255},
   139	        backLabel);
   140	
   141	    m_mouse->draw();
   142	}
```

### cSelectMissionState::draw — src/gamestates/cSelectMissionState.cpp@acddd29:179-224

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ PORT=acddd297b21ec200c7090dd2f1b73e014e2b74c0
$ git grep -n -E '^(.*[ *&])?cSelectMissionState::draw\(' $PORT -- src | grep -v ';$'
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSelectMissionState.cpp:179:void cSelectMissionState::draw() const
$ git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSelectMissionState.cpp | nl -ba | sed -n '179,224p'
   179	void cSelectMissionState::draw() const
   180	{
   181	    m_sdlDrawer->renderClearToColor(Color{10, 12, 14, 255});
   182	    if (m_hdBackground) {
   183	        const float sourceAspect = static_cast<float>(m_hdBackground->w) /
   184	            std::max(1, m_hdBackground->h);
   185	        const float screenAspect = static_cast<float>(m_settings->getScreenW()) /
   186	            std::max(1, m_settings->getScreenH());
   187	        cRectangle destination;
   188	        if (sourceAspect > screenAspect) {
   189	            const int width = static_cast<int>(m_settings->getScreenH() * sourceAspect);
   190	            destination = cRectangle(
   191	                (m_settings->getScreenW() - width) / 2,
   192	                0,
   193	                width,
   194	                m_settings->getScreenH());
   195	        } else {
   196	            const int height = static_cast<int>(m_settings->getScreenW() / sourceAspect);
   197	            destination = cRectangle(
   198	                0,
   199	                (m_settings->getScreenH() - height) / 2,
   200	                m_settings->getScreenW(),
   201	                height);
   202	        }
   203	        m_sdlDrawer->renderStrechFullSprite(m_hdBackground, destination);
   204	        m_sdlDrawer->renderRectFillColor(
   205	            0,
   206	            0,
   207	            m_settings->getScreenW(),
   208	            m_settings->getScreenH(),
   209	            Color{3, 6, 8, 150});
   210	    }
   211	
   212	    gui_window->draw();
   213	    m_sdlDrawer->renderTexture(
   214	        m_houseFlag->tex.get(), m_flagX, m_flagY, m_flagWidth, m_flagHeight);
   215	    m_textDrawer->drawTextCentered(
   216	        "REPLAY MISSION",
   217	        m_headerX,
   218	        m_headerWidth,
   219	        m_headerY,
   220	        Color::Yellow);
   221	
   222	    // MOUSE
   223	    m_mouse->draw();
   224	}
```

### cSetupSkirmishState::cSetupSkirmishState — src/gamestates/cSetupSkirmishState.cpp@acddd29:93-402

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ PORT=acddd297b21ec200c7090dd2f1b73e014e2b74c0
$ git grep -n -E '^(.*[ *&])?cSetupSkirmishState::cSetupSkirmishState\(' $PORT -- src | grep -v ';$'
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSetupSkirmishState.cpp:93:cSetupSkirmishState::cSetupSkirmishState(sGameServices* services, cPreviewMaps* previewMaps,s_DataCampaign* dataCompaign) :
$ git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSetupSkirmishState.cpp | nl -ba | sed -n '93,402p'
    93	cSetupSkirmishState::cSetupSkirmishState(sGameServices* services, cPreviewMaps* previewMaps,s_DataCampaign* dataCompaign) :
    94	    cGameState(services),
    95	    m_textDrawer(m_ctx->getTextContext()->getBeneTextDrawer()),
    96	    m_settings(services->settings),
    97	    m_scenarioFlow(services->scenarioFlow),
    98	    m_eventEmitter(services->eventEmitter),
    99	    m_audioContext(m_ctx->getAudioContext()),
   100	    m_stateTransitions(services->stateTransitions),
   101	    m_mapCamera(services->mapCamera),
   102	    m_gameConditionChecker(services->gameConditionChecker),
   103	    m_screenFader(services->screenFader),
   104	    m_objects(services->objects),
   105	    m_services(services),
   106	    m_dataCampaign(dataCompaign),
   107	    m_previewMaps(previewMaps),
   108	    m_gfxinter(m_ctx->getGraphicsContext()->gfxinter.get())
   109	{
   110	    d2tm_assert(m_textDrawer != nullptr);
   111	    d2tm_assert(m_settings != nullptr);
   112	    d2tm_assert(m_scenarioFlow != nullptr);
   113	    d2tm_assert(m_eventEmitter != nullptr);
   114	    d2tm_assert(m_audioContext != nullptr);
   115	    d2tm_assert(m_stateTransitions != nullptr);
   116	    d2tm_assert(m_screenFader != nullptr);
   117	    d2tm_assert(m_objects != nullptr);
   118	    d2tm_assert(m_dataCampaign != nullptr);
   119	    d2tm_assert(m_gfxinter != nullptr);
   120	    for (int i = 0; i < MAX_PLAYERS; i++) {
   121	        s_SkirmishPlayer &sSkirmishPlayer = skirmishPlayer[i];
   122	        // index 0 == human player, but to keep our lives sane we don't change the index.
   123	
   124	        // player 0 (HUMAN) is always playing,
   125	        sSkirmishPlayer.bHuman = i == HUMAN;
   126	
   127	        // and 1 additional AI is minimally required to play
   128	        sSkirmishPlayer.bPlaying = (i <= 1);
   129	
   130	        // just some defaults
   131	        sSkirmishPlayer.startingUnits = 3;
   132	        sSkirmishPlayer.iCredits = 2500;
   133	        sSkirmishPlayer.iHouse = 0; // random house
   134	        sSkirmishPlayer.team = (i + 1); // all different team
   135	    }
   136	
   137	    iStartingPoints = 2;
   138	    iSkirmishMap = -1;
   139	    mapStartingIndexToDisplay = 0;
   140	
   141	    randomMapGenerator = std::make_unique<cRandomMapGenerator>();
   142	    generateRandomMap();
   143	
   144	    m_mouse = services->mouse;
   145	    d2tm_assert(m_mouse != nullptr);
   146	    d2tm_assert(m_mapCamera != nullptr);
   147	    d2tm_assert(m_gameConditionChecker != nullptr);
   148	
   149	    spawnWorms = 2;
   150	    techLevel = 9;
   151	    spawnBlooms = true;
   152	    detonateBlooms = true;
   153	
   154	    // Colors
   155	    colorDarkishBorder = Color{173, 125, 39, 255};
   156	    colorDarkerYellow = Color{255, 224, 139, 255};
   157	    colorDisabled = Color{92, 96, 98, 255};
   158	    colorLightBackground = Color{21, 27, 31, 255};
   159	    colorOtherBorder = Color{102, 78, 35, 255};
   160	
   161	    // Basic coordinates
   162	    topBarHeight = 28;
   163	    previewMapHeight = 129;
   164	    previewMapWidth = 129;
   165	    widthOfRightColumn = 300;
   166	    mapItemButtonHeight = 150;
   167	    mapItemButtonWidth = 145;
   168	    m_playerRowHeight = 26;
   169	
   170	    // Screen
   171	    screen_x = m_settings->getScreenW();
   172	    screen_y = m_settings->getScreenH();
   173	
   174	    // Rectangles for GUI interaction
   175	    int topBarWidth = screen_x + 4;
   176	
   177	    // title box
   178	    topBar = cRectangle(-1, -1, topBarWidth, topBarHeight);
   179	
   180	    // Players title bar
   181	    int widthOfSidebar = widthOfRightColumn + 2;
   182	    int playerTitleBarWidth = screen_x - widthOfSidebar;
   183	    int playerTitleBarHeight = topBarHeight;
   184	    int playerTitleBarX = 0;
   185	    int playerTitleBarY = topBarHeight-1;
   186	    playerTitleBar = cRectangle(playerTitleBarX, playerTitleBarY, playerTitleBarWidth, playerTitleBarHeight);
   187	
   188	    // this is the box at the right from the Player list
   189	    int topRightBoxWidth = widthOfSidebar;
   190	    int topRightBoxHeight = playerTitleBarHeight + previewMapHeight+playerTitleBarHeight;
   191	    int topRightBoxX = screen_x - topRightBoxWidth;
   192	    int topRightBoxY = topBarHeight-1;
   193	    topRightBox = cRectangle(topRightBoxX, topRightBoxY, topRightBoxWidth, topRightBoxHeight);
   194	
   195	    // player list
   196	    int playerListBarWidth = playerTitleBarWidth;
   197	    int playerListBarHeight = playerTitleBarHeight + previewMapHeight;
   198	    int playerListBarX = 0;
   199	    int playerListBarY = playerTitleBarY + topBarHeight;
   200	    playerList = cRectangle(playerListBarX, playerListBarY, playerListBarWidth, playerListBarHeight);
   201	
   202	    // map list
   203	
   204	    // title bar
   205	    int mapListFrameX = 0;
   206	    int mapListFrameY = playerListBarY + playerListBarHeight;
   207	    int mapListFrameHeight = topBarHeight;
   208	
   209	    // rectangle for map list
   210	    mapListTitle = cRectangle(mapListFrameX, mapListFrameY, playerTitleBarWidth, mapListFrameHeight);
   211	    cRectangle previousMaps(mapListFrameX + 4, mapListFrameY, 60, mapListFrameHeight);
   212	    cRectangle nextMaps(mapListFrameX + playerTitleBarWidth - 48, mapListFrameY, 50, mapListFrameHeight);
   213	
   214	    // preview map
   215	    int previewMapFrameX = screen_x - widthOfSidebar;
   216	    int previewMapFrameY = playerListBarY + playerListBarHeight;
   217	    int previewMapFrameWidth = widthOfSidebar;
   218	    int previewMapFrameHeight = topBarHeight;
   219	    previewMapTitle = cRectangle(previewMapFrameX, previewMapFrameY,previewMapFrameWidth, previewMapFrameHeight);
   220	
   221	    // actual list of maps
   222	    int mapListTopY = mapListTitle.getY() + mapListTitle.getHeight();
   223	
   224	    int previewMapY = playerListBarY + playerListBarHeight + previewMapFrameHeight;
   225	    int previewMapX = (screen_x - widthOfSidebar);
   226	    const int previewAreaHeight = screen_y - topBarHeight - previewMapY;
   227	    previewMap = cRectangle(previewMapX, previewMapY, widthOfRightColumn, previewAreaHeight);
   228	    const int previewSize = std::min(widthOfRightColumn - 50, previewAreaHeight - 92);
   229	    previewMapRect = cRectangle(
   230	        previewMapX + (widthOfRightColumn - previewSize) / 2,
   231	        previewMapY + 18,
   232	        previewSize,
   233	        previewSize
   234	    );
   235	
   236	    selectArea = cRectangle(0, mapListTopY, screen_x -widthOfRightColumn-2, screen_y-topBarHeight-mapListTopY);
   237	
   238	    int margin = 10;
   239	
   240	    maxMapsInSelectAreaHorizontally = selectArea.getWidth() / (mapItemButtonWidth+margin);
   241	    maxMapsInSelectAreaVertically = selectArea.getHeight() / (mapItemButtonHeight + 15);
   242	    maxMapsInSelectArea = maxMapsInSelectAreaHorizontally * maxMapsInSelectAreaVertically;
   243	
   244	    nextFunction = [this]() {
   245	        // Go to the next map
   246	        int intendedNextStartIndex = mapStartingIndexToDisplay + maxMapsInSelectArea;
   247	        if (intendedNextStartIndex <= m_previewMaps->getMapCount()) {
   248	            mapStartingIndexToDisplay = intendedNextStartIndex;
   249	        }
   250	    };
   251	    previousFunction = [this]() {
   252	        // Go back to the previous map
   253	        if (mapStartingIndexToDisplay > 0) {
   254	            mapStartingIndexToDisplay -= maxMapsInSelectArea;
   255	        }
   256	    };
   257	
   258	    nextMapButton = GuiButtonBuilder()
   259	        .withRect(nextMaps)
   260	        .withLabel("Next")
   261	        .withTextDrawer(m_textDrawer)
   262	        .withRenderer(m_sdlDrawer)
   263	        .withTheme(GuiTheme::Remaster())
   264	        .withKind(GuiRenderKind::REMASTER_BUTTON)
   265	        .onClick(nextFunction)
   266	        .build();
   267	
   268	    previousMapButton = GuiButtonBuilder()
   269	            .withRect(previousMaps)
   270	            .withLabel("Previous")
   271	            .withTextDrawer(m_textDrawer)
   272	            .withRenderer(m_sdlDrawer)
   273	            .withTheme(GuiTheme::Remaster())
   274	            .withKind(GuiRenderKind::REMASTER_BUTTON)
   275	            .onClick(previousFunction)
   276	            .build();
   277	
   278	    // Top right skirmish game properties:
   279	
   280	    // Starting positions
   281	    int startPointsX = screen_x - widthOfRightColumn;
   282	    int startPointsY = topBarHeight + 6;
   283	    int startPointHitBoxWidth = 260;
   284	    int startPointHitBoxHeight = m_textDrawer->getFontHeight() + 4;
   285	    startPointsRect = cRectangle(startPointsX, startPointsY, startPointHitBoxWidth, startPointHitBoxHeight);
   286	
   287	    // Worms
   288	    int wormsX = screen_x - widthOfRightColumn;
   289	    int wormsY = startPointsY + 32;
   290	    int wormsHitBoxWidth = startPointHitBoxWidth;
   291	    int wormsHitBoxHeight = startPointHitBoxHeight;
   292	    wormsRect = cRectangle(wormsX, wormsY, wormsHitBoxWidth, wormsHitBoxHeight);
   293	
   294	    // Spice Blooms
   295	    int bloomsX = screen_x - widthOfRightColumn;
   296	    int bloomsY = wormsY + 32;
   297	    int bloomsHitBoxWidth = startPointHitBoxWidth;
   298	    int bloomsHitBoxHeight = startPointHitBoxHeight;
   299	    bloomsRect = cRectangle(bloomsX, bloomsY, bloomsHitBoxWidth, bloomsHitBoxHeight);
   300	
   301	    int detonateX = screen_x - widthOfRightColumn;
   302	    int detonateY = bloomsY + 32;
   303	    int detonateHitBoxWidth = startPointHitBoxWidth;
   304	    int detonateHitBoxHeight = startPointHitBoxHeight;
   305	    detonateBloomsRect = cRectangle(detonateX, detonateY, detonateHitBoxWidth, detonateHitBoxHeight);
   306	
   307	    int techLevelX = screen_x - widthOfRightColumn;
   308	    int techLevelY = detonateY + 32;
   309	    int techLevelHitBoxWidth = startPointHitBoxWidth;
   310	    int techLevelHitBoxHeight = startPointHitBoxHeight;
   311	    techLevelRect = cRectangle(techLevelX, techLevelY, techLevelHitBoxWidth, techLevelHitBoxHeight);
   312	
   313	    const int btnHPad = 8;
   314	    const int btnVPad = 2;
   315	    const int btnHeight = topBarHeight - (btnVPad * 2);
   316	
   317	    int backButtonWidth = 150;
   318	    int backButtonY = screen_y - topBarHeight;
   319	    int backButtonX = 0;
   320	    cRectangle backButtonRect(backButtonX, backButtonY, backButtonWidth, topBarHeight);
   321	    backButton = GuiButtonBuilder()
   322	            .withRect(backButtonRect)
   323	            .withLabel("Back")
   324	            .withTextDrawer(m_textDrawer)
   325	            .withRenderer(m_sdlDrawer)
   326	            .withTheme(GuiTheme::Remaster())
   327	            .withKind(GuiRenderKind::REMASTER_BUTTON)
   328	            .onClick([this]() {
   329	                m_stateTransitions->setNextStateWithFade(GAME_MENU);
   330	            })
   331	            .build();
   332	
   333	    const int btnGap = 15;
   334	    const int bottomY = screen_y - topBarHeight + btnVPad;
   335	
   336	    // Right group: [Surprise me] [START]
   337	    int startButtonWidth = 150;
   338	    int startButtonY = screen_y - topBarHeight;
   339	    int startButtonX = screen_x - startButtonWidth;
   340	    cRectangle startButtonRect = cRectangle(startButtonX, startButtonY, startButtonWidth, topBarHeight);
   341	    startButton = GuiButtonBuilder()
   342	            .withRect(startButtonRect)
   343	            .withLabel("Start")
   344	            .withTextDrawer(m_textDrawer)
   345	            .withRenderer(m_sdlDrawer)
   346	            .withTheme(GuiTheme::Remaster())
   347	            .withKind(GuiRenderKind::REMASTER_BUTTON)
   348	            .onClick([this]() {
   349	                if (m_previewMaps->isValidMap(iSkirmishMap)) {
   350	                    prepareSkirmishGameToPlayAndTransitionToCombatState(iSkirmishMap);
   351	                }
   352	            })
   353	            .build();
   354	
   355	    int surpriseMeButtonWidth = m_textDrawer->getTextLength("Surprise me") + btnHPad;
   356	    int surpriseMeButtonX = startButtonX - btnGap - surpriseMeButtonWidth;
   357	    cRectangle surpriseMeButtonRect = cRectangle(surpriseMeButtonX, bottomY, surpriseMeButtonWidth, btnHeight);
   358	    surpriseMeButton = GuiButtonBuilder()
   359	            .withRect(surpriseMeButtonRect)
   360	            .withLabel("Surprise me")
   361	            .withTextDrawer(m_textDrawer)
   362	            .withRenderer(m_sdlDrawer)
   363	            .withTheme(GuiTheme::Remaster())
   364	            .withKind(GuiRenderKind::REMASTER_BUTTON)
   365	            .onClick([this]() { surpriseMe(); })
   366	            .build();
   367	
   368	    // Center group: [New Map] [Modify]
   369	    int newMapButtonWidth = m_textDrawer->getTextLength("New Map") + btnHPad;
   370	    int modifyButtonWidth = m_textDrawer->getTextLength("Modify") + btnHPad;
   371	    int centerGroupWidth = newMapButtonWidth + btnGap + modifyButtonWidth;
   372	    int centerGroupX = screen_x / 2 - centerGroupWidth / 2;
   373	    cRectangle newMapButtonRect = cRectangle(centerGroupX, bottomY, newMapButtonWidth, btnHeight);
   374	    newMapButton = GuiButtonBuilder()
   375	            .withRect(newMapButtonRect)
   376	            .withLabel("New Map")
   377	            .withTextDrawer(m_textDrawer)
   378	            .withRenderer(m_sdlDrawer)
   379	            .withTheme(GuiTheme::Remaster())
   380	            .withKind(GuiRenderKind::REMASTER_BUTTON)
   381	            .onClick([this]() {
   382	                m_stateTransitions->setNextStateWithFade(GAME_NEW_MAP_EDITOR);
   383	            })
   384	            .build();
   385	
   386	    int modifyButtonX = centerGroupX + newMapButtonWidth + btnGap;
   387	    cRectangle modifyButtonRect = cRectangle(modifyButtonX, bottomY, modifyButtonWidth, btnHeight);
   388	    modifyButton = GuiButtonBuilder()
   389	            .withRect(modifyButtonRect)
   390	            .withLabel("Modify")
   391	            .withTextDrawer(m_textDrawer)
   392	            .withRenderer(m_sdlDrawer)
   393	            .withTheme(GuiTheme::Remaster())
   394	            .withKind(GuiRenderKind::REMASTER_BUTTON)
   395	            .onClick([this]() {
   396	                if (iSkirmishMap > -1) {
   397	                    m_scenarioFlow->loadMapFromEditor(iSkirmishMap);
   398	                    m_stateTransitions->fadeOut();
   399	                }
   400	            })
   401	            .build();
   402	}
```

### cSetupSkirmishState::draw — src/gamestates/cSetupSkirmishState.cpp@acddd29:436-534

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ PORT=acddd297b21ec200c7090dd2f1b73e014e2b74c0
$ git grep -n -E '^(.*[ *&])?cSetupSkirmishState::draw\(' $PORT -- src | grep -v ';$'
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSetupSkirmishState.cpp:436:void cSetupSkirmishState::draw() const
$ git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSetupSkirmishState.cpp | nl -ba | sed -n '436,534p'
   436	void cSetupSkirmishState::draw() const
   437	{
   438	    m_sdlDrawer->renderClearToColor(Color{10, 13, 15, 255});
   439	
   440	    const auto drawPanel = [this](const cRectangle &rect, Color fill, Color border) {
   441	        m_sdlDrawer->renderRectFillColor(rect, fill);
   442	        m_sdlDrawer->renderRectColor(rect, border);
   443	    };
   444	
   445	    drawPanel(topBar, Color{25, 31, 35, 255}, colorDarkishBorder);
   446	    m_textDrawer->drawTextCentered(
   447	        "Skirmish",
   448	        (topBarHeight - m_textDrawer->getFontHeight()) / 2,
   449	        Color{231, 190, 91, 255}
   450	    );
   451	    drawPanel(playerTitleBar, colorLightBackground, colorDarkishBorder);
   452	    drawPanel(topRightBox, Color{25, 31, 35, 255}, colorDarkishBorder);
   453	    drawPanel(playerList, colorLightBackground, colorDarkishBorder);
   454	    drawPanel(mapListTitle, colorLightBackground, colorDarkishBorder);
   455	    m_textDrawer->drawTextCentered(
   456	        "Maps",
   457	        mapListTitle.getX(),
   458	        mapListTitle.getWidth(),
   459	        mapListTitle.getY() + 4,
   460	        Color{231, 190, 91, 255}
   461	    );
   462	    drawPanel(previewMapTitle, colorLightBackground, colorDarkishBorder);
   463	    m_textDrawer->drawTextCentered(
   464	        "Preview",
   465	        previewMapTitle.getX(),
   466	        previewMapTitle.getWidth(),
   467	        previewMapTitle.getY() + 4,
   468	        Color{231, 190, 91, 255}
   469	    );
   470	    drawPanel(previewMap, colorLightBackground, colorDarkishBorder);
   471	    drawPanel(selectArea, colorLightBackground, colorDarkishBorder);
   472	
   473	    drawPreviewMapAndMore(previewMapRect);
   474	    drawStartPoints(iStartingPoints, startPointsRect);
   475	    drawWorms(wormsRect);
   476	    drawBlooms(bloomsRect);
   477	    drawDetonateBlooms(detonateBloomsRect);
   478	    drawTechLevel(techLevelRect);
   479	    drawMapList(selectArea);
   480	
   481	    const SkirmishPlayerTableLayout headerLayout(playerTitleBar.getY() + 3);
   482	    const std::array<const char *, 5> headerLabels = {
   483	        "Player", "House", "Credits", "Units", "Team"
   484	    };
   485	    const auto headerColumns = headerLayout.columns();
   486	    for (std::size_t column = 0; column < headerColumns.size(); ++column) {
   487	        const cRectangle &rect = headerColumns[column];
   488	        m_textDrawer->drawTextCentered(
   489	            headerLabels[column],
   490	            rect.getX(),
   491	            rect.getWidth(),
   492	            rect.getY(),
   493	            Color{231, 190, 91, 255}
   494	        );
   495	    }
   496	
   497	    for (int p = 0; p < (AI_WORM - 1); p++) {
   498	        const int iDrawY = playerList.getY() + 4 + (p * m_playerRowHeight);
   499	        const SkirmishPlayerTableLayout rowLayout(iDrawY);
   500	
   501	        const s_SkirmishPlayer &sSkirmishPlayer = skirmishPlayer[p];
   502	
   503	        if (p < iStartingPoints) {
   504	            drawPlayerBrain(sSkirmishPlayer, rowLayout.player);
   505	            drawHouse(sSkirmishPlayer, rowLayout.house);
   506	            drawCredits(sSkirmishPlayer, rowLayout.credits);
   507	            drawStartingUnits(sSkirmishPlayer, rowLayout.units);
   508	            drawTeams(sSkirmishPlayer, rowLayout.team);
   509	        }
   510	    }
   511	
   512	    drawPanel(
   513	        cRectangle(-1, screen_y - topBarHeight, screen_x + 2, topBarHeight + 2),
   514	        Color{25, 31, 35, 255},
   515	        colorDarkishBorder
   516	    );
   517	
   518	    const bool selectedMap = iSkirmishMap > -1;
   519	    startButton->setEnabled(selectedMap);
   520	    startButton->setTheme(selectedMap ? GuiTheme::Remaster() : GuiTheme::RemasterInactive());
   521	    modifyButton->setEnabled(selectedMap);
   522	    modifyButton->setTheme(selectedMap ? GuiTheme::Remaster() : GuiTheme::RemasterInactive());
   523	
   524	    backButton->draw();
   525	    startButton->draw();
   526	    modifyButton->draw();
   527	    newMapButton->draw();
   528	    surpriseMeButton->draw();
   529	    nextMapButton->draw();
   530	    previousMapButton->draw();
   531	
   532	    // MOUSE
   533	    m_mouse->draw();
   534	}
```

### cOptionsState::cOptionsState — src/gamestates/cOptionsState.cpp@acddd29:49-69

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ PORT=acddd297b21ec200c7090dd2f1b73e014e2b74c0
$ git grep -n -E '^(.*[ *&])?cOptionsState::cOptionsState\(' $PORT -- src | grep -v ';$'
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cOptionsState.cpp:49:cOptionsState::cOptionsState(sGameServices* services, int prevState)
$ git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cOptionsState.cpp | nl -ba | sed -n '49,69p'
    49	cOptionsState::cOptionsState(sGameServices* services, int prevState)
    50	    : cGameState(services),
    51	    m_textDrawer(m_ctx->getTextContext()->getBeneTextDrawer()),
    52	    m_settings(services->settings),
    53	    m_stateTransitions(services->stateTransitions),
    54	    m_mouse(services->mouse),
    55	    m_prevState(prevState),
    56	    m_guiWindow(nullptr)
    57	{
    58	    d2tm_assert(m_textDrawer != nullptr);
    59	    d2tm_assert(m_settings != nullptr);
    60	    d2tm_assert(m_stateTransitions != nullptr);
    61	    d2tm_assert(m_mouse != nullptr);
    62	
    63	    m_renderScaleChoices = renderScaleChoices(m_settings->getOutputW(), m_settings->getOutputH());
    64	    m_worldScaleChoices = worldScaleChoices();
    65	    m_selectedRenderScaleIndex = scaleChoiceIndex(m_renderScaleChoices, m_settings->getSavedRenderScalePercent());
    66	    m_selectedWorldScaleIndex = scaleChoiceIndex(m_worldScaleChoices, m_settings->getSavedWorldScalePercent());
    67	    refresh();
    68	    m_backgroundTexture = &services->screenTexture;
    69	}
```

### cOptionsState::draw — src/gamestates/cOptionsState.cpp@acddd29:596-605

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ PORT=acddd297b21ec200c7090dd2f1b73e014e2b74c0
$ git grep -n -E '^(.*[ *&])?cOptionsState::draw\(' $PORT -- src | grep -v ';$'
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cOptionsState.cpp:596:void cOptionsState::draw() const
$ git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cOptionsState.cpp | nl -ba | sed -n '596,605p'
   596	void cOptionsState::draw() const
   597	{
   598	    if (m_backgroundTexture && *m_backgroundTexture) {
   599	        m_sdlDrawer->renderSprite(*m_backgroundTexture,0,0);
   600	    }
   601	    m_guiWindow->draw();
   602	
   603	    // MOUSE
   604	    m_mouse->draw();
   605	}
```

### cCreditsState::cCreditsState — src/gamestates/cCreditsState.cpp@acddd29:39-100

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ PORT=acddd297b21ec200c7090dd2f1b73e014e2b74c0
$ git grep -n -E '^(.*[ *&])?cCreditsState::cCreditsState\(' $PORT -- src | grep -v ';$'
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cCreditsState.cpp:39:cCreditsState::cCreditsState(sGameServices* services) :
$ git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cCreditsState.cpp | nl -ba | sed -n '39,100p'
    39	cCreditsState::cCreditsState(sGameServices* services) :
    40	    cGameState(services),
    41	    m_textDrawer(m_ctx->getTextContext()->getBeneTextDrawer()),
    42	    m_settings(services->settings),
    43	    m_stateTransitions(services->stateTransitions),
    44	    m_mouse(services->mouse),
    45	    m_moveSpeed(0.15f)
    46	{
    47	    d2tm_assert(m_textDrawer != nullptr);
    48	    d2tm_assert(m_settings != nullptr);
    49	    d2tm_assert(m_stateTransitions != nullptr);
    50	    auto *gfxinter = m_ctx->getGraphicsContext()->gfxinter.get();
    51	    d2tm_assert(gfxinter != nullptr);
    52	
    53	    m_teamBmp = loadHdUiTexture(
    54	        m_sdlDrawer->getRenderer(),
    55	        "credits_team.png",
    56	        "HD credits team photo");
    57	    m_titleBmp = loadHdUiTexture(
    58	        m_sdlDrawer->getRenderer(),
    59	        "credits_title.png",
    60	        "HD credits title");
    61	    m_ownsTeamBmp = m_teamBmp != nullptr;
    62	    m_ownsTitleBmp = m_titleBmp != nullptr;
    63	    if (!m_teamBmp) {
    64	        m_teamBmp = gfxinter->getTexture(CREDITS_DUNE2_CORE_TEAM);
    65	    }
    66	    if (!m_titleBmp) {
    67	        m_titleBmp = gfxinter->getTexture(D2TM_TITLE);
    68	    }
    69	    const int teamAtTheRight = m_settings->getScreenW() - (m_teamBmp->w * 1.1f);
    70	    const int teamAlmostAtBottom = m_settings->getScreenH() - (m_teamBmp->h * 1.1f);
    71	    m_teamCoordinates = cPoint(teamAtTheRight, teamAlmostAtBottom);
    72	
    73	    int titleWidth = m_titleBmp->w;
    74	    m_titleHeight = m_titleBmp->h;
    75	
    76	    int centerOfScreen = m_settings->getScreenW() / 2;
    77	
    78	    m_titleX = centerOfScreen - (titleWidth / 2);
    79	    resetCrawler();
    80	
    81	    const int backButtonWidth = std::max(140, m_textDrawer->getTextLength("Back") + 24);
    82	    const int backButtonHeight = std::max(36, m_textDrawer->getFontHeight() + 10);
    83	    const int backButtonY = m_settings->getScreenH() - backButtonHeight;
    84	    const int backButtonX = 0;
    85	    cRectangle backButtonRect(backButtonX, backButtonY, backButtonWidth, backButtonHeight);
    86	    backButton = GuiButtonBuilder()
    87	            .withRect(backButtonRect)
    88	            .withLabel("Back")
    89	            .withTextDrawer(m_textDrawer)
    90	            .withRenderer(m_sdlDrawer)
    91	            .withTheme(GuiTheme::Remaster())
    92	            .withKind(GuiRenderKind::REMASTER_BUTTON)
    93	            .onClick([this]() {
    94	                m_stateTransitions->setNextStateWithFade(GAME_MENU);
    95	            })
    96	            .build();
    97	
    98	    m_lines = std::vector<s_CreditLine>();
    99	    prepareCrawlerLines();
   100	}
```

### cCreditsState::thinkFast — src/gamestates/cCreditsState.cpp@acddd29:427-439

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ PORT=acddd297b21ec200c7090dd2f1b73e014e2b74c0
$ git grep -n -E '^(.*[ *&])?cCreditsState::thinkFast\(' $PORT -- src | grep -v ';$'
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cCreditsState.cpp:427:void cCreditsState::thinkFast()
$ git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cCreditsState.cpp | nl -ba | sed -n '427,439p'
   427	void cCreditsState::thinkFast()
   428	{
   429	    m_crawlerY -= m_moveSpeed;
   430	
   431	    int textCrawlY = m_crawlerY + m_titleHeight;
   432	    for (auto &line : m_lines) {
   433	        textCrawlY += line.height;
   434	    }
   435	
   436	    if (textCrawlY < 0) {
   437	        resetCrawler();
   438	    }
   439	}
```

### cCreditsState::draw — src/gamestates/cCreditsState.cpp@acddd29:441-469

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ PORT=acddd297b21ec200c7090dd2f1b73e014e2b74c0
$ git grep -n -E '^(.*[ *&])?cCreditsState::draw\(' $PORT -- src | grep -v ';$'
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cCreditsState.cpp:441:void cCreditsState::draw() const
$ git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cCreditsState.cpp | nl -ba | sed -n '441,469p'
   441	void cCreditsState::draw() const
   442	{
   443	    m_sdlDrawer->renderSprite(m_teamBmp, m_teamCoordinates.x, m_teamCoordinates.y);
   444	
   445	    int halfScreen = m_settings->getScreenW() / 2;
   446	
   447	    // draw crawler
   448	    m_sdlDrawer->renderSprite(m_titleBmp, m_titleX, m_crawlerY);
   449	    int textCrawlY = m_crawlerY + m_titleHeight;
   450	    for (auto &line : m_lines) {
   451	        if (line.name.empty()) {
   452	            m_textDrawer->drawTextCentered(line.txt.c_str(), textCrawlY, line.color);
   453	        }
   454	        else if (line.txt.empty()) {
   455	            m_textDrawer->drawTextCentered(line.name.c_str(), textCrawlY, line.color);
   456	        }
   457	        else {
   458	            int spaceBetween = 4;
   459	            // both name and line given, then we render them differently.
   460	            m_textDrawer->drawText(halfScreen+spaceBetween, textCrawlY, line.txt.c_str());
   461	            int widthOfName = m_textDrawer->getTextLength(line.name.c_str());
   462	            m_textDrawer->drawText(halfScreen - (widthOfName + spaceBetween), textCrawlY, line.name.c_str());
   463	        }
   464	        textCrawlY += line.height;
   465	    }
   466	
   467	    backButton->draw();
   468	    m_mouse->draw();
   469	}
```

### cSelectYourNextConquestState::cSelectYourNextConquestState — src/gamestates/cSelectYourNextConquestState.cpp@acddd29:78-174

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ PORT=acddd297b21ec200c7090dd2f1b73e014e2b74c0
$ git grep -n -E '^(.*[ *&])?cSelectYourNextConquestState::cSelectYourNextConquestState\(' $PORT -- src | grep -v ';$'
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSelectYourNextConquestState.cpp:78:cSelectYourNextConquestState::cSelectYourNextConquestState(sGameServices* services, cIni* ini, s_DataCampaign* dataCompaign) :
$ git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSelectYourNextConquestState.cpp | nl -ba | sed -n '78,174p'
    78	cSelectYourNextConquestState::cSelectYourNextConquestState(sGameServices* services, cIni* ini, s_DataCampaign* dataCompaign) :
    79	    cGameState(services),
    80	    m_settings(services->settings),
    81	    m_scenarioFlow(services->scenarioFlow),
    82	    m_audioContext(m_ctx->getAudioContext()),
    83	    m_stateTransitions(services->stateTransitions),
    84	    m_mentatFlow(services->mentatFlow),
    85	    m_missionFlow(services->missionFlow),
    86	    m_textDrawer(m_ctx->getTextContext()->getBeneTextDrawer()),
    87	    m_objects(services->objects),
    88	    m_dataCampaign(dataCompaign),
    89	    m_gfxworld(m_ctx->getGraphicsContext()->gfxworld.get()),
    90	    m_gfxinter(m_ctx->getGraphicsContext()->gfxinter.get()),
    91	    m_cIni(ini)
    92	{
    93	    d2tm_assert(m_settings != nullptr);
    94	    d2tm_assert(m_scenarioFlow != nullptr);
    95	    d2tm_assert(m_audioContext != nullptr);
    96	    d2tm_assert(m_stateTransitions != nullptr);
    97	    d2tm_assert(m_mentatFlow != nullptr);
    98	    d2tm_assert(m_missionFlow != nullptr);
    99	    d2tm_assert(m_textDrawer != nullptr);
   100	    d2tm_assert(m_dataCampaign != nullptr);
   101	    d2tm_assert(m_gfxworld != nullptr);
   102	    d2tm_assert(m_gfxinter != nullptr);
   103	    d2tm_assert(m_cIni != nullptr);
   104	    state = eRegionState::REGSTATE_INIT;
   105	    regionSceneState = eRegionSceneState::SCENE_INIT;
   106	    m_mouse = services->mouse;
   107	    d2tm_assert(m_mouse != nullptr);
   108	
   109	    m_drawManager = services->drawManager;
   110		d2tm_assert(m_drawManager != nullptr);
   111	    iRegionSceneAlpha = 0;  // alpha for scene in introduction state
   112	
   113	    std::fill(std::begin(iRegionConquer), std::end(iRegionConquer), -1);
   114	    std::fill(std::begin(iRegionHouse), std::end(iRegionHouse), -1);
   115	    for (auto &text : cRegionText) {
   116	        text.clear();
   117	    }
   118	
   119	    m_hdCampaignLayout = CampaignMapLayout::create(
   120	        m_settings->getScreenW(),
   121	        m_settings->getScreenH()
   122	    );
   123	    m_hdBackground = loadHdUiTexture(
   124	        m_sdlDrawer->getRenderer(),
   125	        "main_menu_background.png",
   126	        "HD campaign map background"
   127	    );
   128	    m_hdCampaignMap = loadHdUiTexture(
   129	        m_sdlDrawer->getRenderer(),
   130	        "campaign_map.png",
   131	        "HD campaign map"
   132	    );
   133	
   134	    std::string houseCrestFile;
   135	    switch (m_objects->getPlayer(0)->getHouse()) {
   136	        case ATREIDES:
   137	            houseCrestFile = "hud_house_atreides.png";
   138	            break;
   139	        case HARKONNEN:
   140	            houseCrestFile = "hud_house_harkonnen.png";
   141	            break;
   142	        case ORDOS:
   143	            houseCrestFile = "hud_house_ordos.png";
   144	            break;
   145	        default:
   146	            break;
   147	    }
   148	    if (!houseCrestFile.empty()) {
   149	        m_hdHouseCrest = loadHdUiTexture(
   150	            m_sdlDrawer->getRenderer(),
   151	            houseCrestFile,
   152	            "HD campaign house crest"
   153	        );
   154	    }
   155	
   156	    calculateOffset();
   157	
   158	    regionClickMapBmp = nullptr;
   159	
   160	    regionMouseIsHoveringOver = -1;
   161	    isFinishedConqueringRegions = true;
   162	
   163	    const cRectangle toMissionSelectRect = m_hdCampaignLayout.missionButton;
   164	    m_guiBtnToMissionSelect = GuiButtonBuilder()
   165	            .withRect(toMissionSelectRect)        
   166	            .withLabel("Mission select")
   167	            .withKind(GuiRenderKind::REMASTER_BUTTON)
   168	            .withTextDrawer(m_textDrawer)
   169	            .withRenderer(m_sdlDrawer)
   170	            .withTheme(GuiTheme::Remaster())
   171	            .onClick([this]() {
   172	                m_stateTransitions->setNextState(GAME_MISSIONSELECT);})
   173	            .build();
   174	}
```

### cSelectYourNextConquestState::thinkFast — src/gamestates/cSelectYourNextConquestState.cpp@acddd29:194-339

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ PORT=acddd297b21ec200c7090dd2f1b73e014e2b74c0
$ git grep -n -E '^(.*[ *&])?cSelectYourNextConquestState::thinkFast\(' $PORT -- src | grep -v ';$'
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSelectYourNextConquestState.cpp:194:void cSelectYourNextConquestState::thinkFast()
$ git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSelectYourNextConquestState.cpp | nl -ba | sed -n '194,339p'
   194	void cSelectYourNextConquestState::thinkFast()
   195	{
   196	
   197	    // First time INIT
   198	    if (state == eRegionState::REGSTATE_INIT) {
   199	        // temp bitmap to read from
   200	        regionClickMapBmp = m_gfxworld->getSurface(WORLD_DUNE_CLICK); // 8 bit bitmap
   201	        if (m_hdRegionBorders == nullptr) {
   202	            m_hdRegionBorders = createHdRegionBordersTexture();
   203	        }
   204	        // NOTE: No need to use Offset here, as it is on a tempreg and we pretend our mouse is on that BMP as well
   205	        // we substract the offset from mouse coordinates to compensate
   206	        state = fastForward ? eRegionState::REGSTATE_CONQUER_REGIONS : eRegionState::REGSTATE_INTRODUCTION;
   207	        return;
   208	    }
   209	
   210	    if (state == eRegionState::REGSTATE_INTRODUCTION) {
   211	        if (iRegionSceneAlpha < 255) {
   212	            iRegionSceneAlpha += 1;
   213	        }
   214	
   215	        if (iRegionSceneAlpha > 255) {
   216	            iRegionSceneAlpha = 255;
   217	        }
   218	
   219	        int iHouse = m_objects->getPlayer(0)->getHouse();
   220	        int iMission = m_dataCampaign->mission;
   221	
   222	        bool hasMessage = m_drawManager->hasMessage();
   223	
   224	        if (regionSceneState == SCENE_INIT) {
   225	            regionSetupNextMission(iMission, iHouse);
   226	            m_drawManager->setMessage("3 Houses have come to Dune.");
   227	            transitionToNextRegionSceneState(SCENE_THREE_HOUSES_COME_FOR_DUNE);
   228	        }
   229	        else if (regionSceneState == SCENE_THREE_HOUSES_COME_FOR_DUNE) {
   230	            if (!hasMessage && iRegionSceneAlpha >= 255) {
   231	                m_drawManager->setMessage("To take control of the land.");
   232	                transitionToNextRegionSceneState(SCENE_TO_TAKE_CONTROL_OF_THE_LAND);
   233	            }
   234	        }
   235	        else if (regionSceneState == SCENE_TO_TAKE_CONTROL_OF_THE_LAND) {
   236	            if (!hasMessage && iRegionSceneAlpha >= 255) {
   237	                m_drawManager->setMessage("That has become divided.");
   238	                transitionToNextRegionSceneState(SCENE_THAT_HAS_BECOME_DIVIDED);
   239	            }
   240	        }
   241	        else if (regionSceneState == SCENE_THAT_HAS_BECOME_DIVIDED) {
   242	            if (iRegionSceneAlpha >= 255) {
   243	                transitionToNextRegionSceneState(SCENE_SELECT_YOUR_NEXT_CONQUEST);
   244	                conquerRegions(); // this will change the message bar and state
   245	            }
   246	        }
   247	    }
   248	
   249	    if (state == eRegionState::REGSTATE_CONQUER_REGIONS || state == eRegionState::REGSTATE_INTRODUCTION) {
   250	        for (int i = 0; i < 27; i++) {
   251	            cRegion &regionPiece = world[i];
   252	
   253	            if (regionPiece.iHouse < 0) continue; // skip pieces that do not belong to any house
   254	
   255	            if (regionPiece.iAlpha < 255) {
   256	                regionPiece.iAlpha += 3;
   257	
   258	                // speed up when holding mouse button
   259	                if (m_mouse->isLeftButtonPressed()) {
   260	                    regionPiece.iAlpha += 3;
   261	                }
   262	            }
   263	        }
   264	
   265	        isFinishedConqueringRegions = true;
   266	
   267	        for (int i = 0; i < MAX_REGIONS; i++) {
   268	            if (iRegionConquer[i] < 0) continue;
   269	            int houseThatConquersTheRegion = iRegionHouse[i];
   270	            if (houseThatConquersTheRegion < 0) continue;
   271	
   272	            int iRegNr = iRegionConquer[i];
   273	
   274	            cRegion &region = world[iRegNr];
   275	
   276	            // when the region is NOT this house, turn it into this house
   277	            if (region.iHouse != houseThatConquersTheRegion) {
   278	                const std::string &regionTextString = cRegionText[i];
   279	                bool isRegionTextGiven = !regionTextString.empty();
   280	                bool isRegionTextEmpty = regionTextString.empty();
   281	
   282	                if ((isRegionTextGiven && !m_drawManager->hasMessage()) || isRegionTextEmpty) {
   283	                    // set this up
   284	                    region.iHouse = houseThatConquersTheRegion;
   285	                    region.iAlpha = 1; // this makes it > 0 and thus it will become opaque over time (see THINK function)
   286	
   287	                    if (isRegionTextGiven) {
   288	                        m_drawManager->setMessage(regionTextString);
   289	                    }
   290	                    isFinishedConqueringRegions = false;
   291	                    break;
   292	                }
   293	                else {
   294	                    isFinishedConqueringRegions = false;
   295	                    break;
   296	
   297	                }
   298	            }
   299	            else {
   300	                // house = the same
   301	                if (region.iAlpha >= 255) {
   302	                    // remove this from the 'regionToConquer' index
   303	                    iRegionConquer[i] = -1;
   304	                    houseThatConquersTheRegion = -1; //
   305	                    isFinishedConqueringRegions = false;
   306	
   307	                    break;
   308	                }
   309	                else if (region.iAlpha < 255) {
   310	                    isFinishedConqueringRegions = false;
   311	                    break; // not done yet, so wait before we do another region!
   312	                }
   313	            }
   314	        }
   315	
   316	        if (isFinishedConqueringRegions) {
   317	            state = REGSTATE_SELECT_NEXT_CONQUEST;
   318	        }
   319	    }
   320	
   321	    // select your next conquest... always draw them in the human playing house color
   322	    if (state == REGSTATE_SELECT_NEXT_CONQUEST) {
   323	        if (selectNextConquestAlpha < 255) {
   324	            selectNextConquestAlpha += 1;
   325	        }
   326	        else {
   327	            selectNextConquestAlpha = 1;
   328	        }
   329	
   330	        for (int i = 0; i < 27; i++) {
   331	            cRegion &regionPiece = world[i];
   332	
   333	            if (!regionPiece.bSelectable) continue; // only animate selectable pieces
   334	
   335	            regionPiece.iAlpha = selectNextConquestAlpha;
   336	        }
   337	    }
   338	
   339	}
```

### cSelectYourNextConquestState::draw — src/gamestates/cSelectYourNextConquestState.cpp@acddd29:341-376

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ PORT=acddd297b21ec200c7090dd2f1b73e014e2b74c0
$ git grep -n -E '^(.*[ *&])?cSelectYourNextConquestState::draw\(' $PORT -- src | grep -v ';$'
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSelectYourNextConquestState.cpp:341:void cSelectYourNextConquestState::draw() const
$ git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cSelectYourNextConquestState.cpp | nl -ba | sed -n '341,376p'
   341	void cSelectYourNextConquestState::draw() const
   342	{
   343	    m_mouse->setTile(MOUSE_NORMAL); // global state of mouse
   344	    drawHdBackground();
   345	    drawHdChrome();
   346	
   347	    m_sdlDrawer->setClippingFor(
   348	        m_hdCampaignLayout.map.getX(),
   349	        m_hdCampaignLayout.map.getY(),
   350	        m_hdCampaignLayout.map.getEndX(),
   351	        m_hdCampaignLayout.map.getEndY()
   352	    );
   353	    if (state == eRegionState::REGSTATE_INTRODUCTION) {
   354	        drawStateIntroduction();
   355	    }
   356	    else if (state == eRegionState::REGSTATE_CONQUER_REGIONS) {
   357	        drawStateConquerRegions();
   358	    }
   359	    else if (state == eRegionState::REGSTATE_SELECT_NEXT_CONQUEST) {
   360	        drawStateSelectYourNextConquest();
   361	    }
   362	    else if (state == eRegionState::REGSTATE_FADEOUT) {
   363	        drawStateConquerRegions();
   364	    }
   365	
   366	    m_sdlDrawer->resetClippingFor();
   367	    m_sdlDrawer->renderRectColor(
   368	        m_hdCampaignLayout.map,
   369	        Color{190, 145, 58, 255}
   370	    );
   371	    drawHdMessage();
   372	
   373	    m_guiBtnToMissionSelect->draw();
   374	
   375	    m_drawManager->drawMouse();
   376	}
```

### AbstractMentat::AbstractMentat — src/gameobjects/mentat/AbstractMentat.cpp@acddd29:45-111

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ PORT=acddd297b21ec200c7090dd2f1b73e014e2b74c0
$ git grep -n -E '^(.*[ *&])?AbstractMentat::AbstractMentat\(' $PORT -- src | grep -v ';$'
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/mentat/AbstractMentat.cpp:45:AbstractMentat::AbstractMentat(GameContext* ctx, cGameSettings* settings, GameStateTransition* stateTransitions, MentatFlow* mentatFlow, bool canMissionSelect)
$ git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/mentat/AbstractMentat.cpp | nl -ba | sed -n '45,111p'
    45	AbstractMentat::AbstractMentat(GameContext* ctx, cGameSettings* settings, GameStateTransition* stateTransitions, MentatFlow* mentatFlow, bool canMissionSelect)
    46	{
    47	    d2tm_assert(ctx != nullptr);
    48	    d2tm_assert(settings != nullptr);
    49	    m_stateTransitions = stateTransitions;
    50	    d2tm_assert(m_stateTransitions != nullptr);
    51	    m_mentatFlow = mentatFlow;
    52	    gfxmentat = ctx->getGraphicsContext()->gfxmentat.get();
    53	    m_textDrawer = ctx->getTextContext()->getBeneTextDrawer();
    54	    m_sdlDrawer = ctx->getSDLDrawer();
    55	    iMentatSentence = -1;
    56	
    57	    TIMER_Speaking = -1;
    58	    TIMER_Mouth = 0;
    59	    TIMER_Eyes = 0;
    60	    TIMER_Other = 0;
    61	    TIMER_movie = 0;
    62	
    63	    iMentatMouth = 3;
    64	    iMentatEyes = 3;
    65	    iMovieFrame = -1;
    66	
    67	    iBackgroundFrame = -1;
    68	
    69	    house = GENERALHOUSE;
    70	
    71	    gfxmovie = nullptr;
    72	    leftButton = nullptr;
    73	    rightButton = nullptr;
    74	    // the mentat does not *own* the bitmaps
    75	    leftButtonBmp = nullptr;
    76	    rightButtonBmp = nullptr;
    77	    leftGuiButton = nullptr;
    78	    rightGuiButton = nullptr;
    79	
    80	    if (canMissionSelect) {
    81	
    82	        int length = m_textDrawer->getTextLength("Mission select");
    83	        const cRectangle &toMissionSelectRect = m_textDrawer->getAsRectangle(settings->getScreenW() - length,
    84	                                                settings->getScreenH() - m_textDrawer->getFontHeight(),
    85	                                                "Mission select");
    86	
    87	        auto gui_btn_toMissionSelect = GuiButtonBuilder()
    88	            .withRect(toMissionSelectRect)
    89	            .withLabel("Mission select")
    90	            .withTextDrawer(m_textDrawer)
    91	            .withRenderer(m_sdlDrawer)
    92	            .withTheme(cGuiThemeBuilder().light().build())
    93	            .withKind(GuiRenderKind::TRANSPARENT_WITHOUT_BORDER)
    94	            .onClick([this] {
    95	                m_stateTransitions->setNextState(GAME_MISSIONSELECT);
    96	            })
    97	            .build();
    98	        m_guiBtnToMissionSelect = std::move(gui_btn_toMissionSelect);
    99	    }
   100	    else {
   101	        m_guiBtnToMissionSelect = nullptr;
   102	    }
   103	
   104	    state = INIT;
   105	
   106	    offsetX = (settings->getScreenW() - MENTAT_SCREEN_W) / 2;
   107	    offsetY = (settings->getScreenH() - MENTAT_SCREEN_H) / 2;
   108	    movieTopleftX = offsetX + 256;
   109	    movieTopleftY = offsetY + 120;
   110	    Logger::info(COMP_GAME, "AbstractMentat::AbstractMentat", "Initialized AbstractMentat with mission select button: {}", canMissionSelect);
   111	}
```

### AbstractMentat::thinkFast — нет определения

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ PORT=acddd297b21ec200c7090dd2f1b73e014e2b74c0
$ git grep -n -E '^(.*[ *&])?AbstractMentat::thinkFast\(' $PORT -- src | grep -v ';$'
```

### AbstractMentat::draw — src/gameobjects/mentat/AbstractMentat.cpp@acddd29:273-314

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ PORT=acddd297b21ec200c7090dd2f1b73e014e2b74c0
$ git grep -n -E '^(.*[ *&])?AbstractMentat::draw\(' $PORT -- src | grep -v ';$'
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/mentat/AbstractMentat.cpp:273:void AbstractMentat::draw()
$ git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/mentat/AbstractMentat.cpp | nl -ba | sed -n '273,314p'
   273	void AbstractMentat::draw()
   274	{
   275	    m_sdlDrawer->renderClearToColor(Color{7,7,15,255});
   276	    m_sdlDrawer->renderRectColor(offsetX-1, offsetY-1, 641, 481, Color{64, 64,89,255});
   277	    m_sdlDrawer->renderRectColor(offsetX-2, offsetY-2, 642, 482, Color{40,40,60,255});
   278	    m_sdlDrawer->renderRectColor(offsetX-3, offsetY-3, 643, 483, Color{0,0,0,255});
   279	
   280	    // movie
   281	    draw_movie();
   282	
   283	    Texture *tmp = getBackgroundBitmap();
   284	    cRectangle dest = {offsetX, offsetY, MENTAT_SCREEN_W, MENTAT_SCREEN_H};
   285	    m_sdlDrawer->renderStrechFullSprite(tmp, dest);
   286	
   287	    draw_eyes();
   288	    draw_mouth();
   289	    draw_other();
   290	
   291	    if (state == SPEAKING) {
   292	        // draw text that is being spoken
   293	        if (iMentatSentence >= 0) {
   294	            m_textDrawer->drawText(offsetX + 17, offsetY + 17,Color{0, 0, 0,255},sentence[iMentatSentence]);
   295	            m_textDrawer->drawText(offsetX + 17, offsetY + 17,Color{255, 255, 255,255},sentence[iMentatSentence]);
   296	
   297	            m_textDrawer->drawText(offsetX + 17, offsetY + 37,Color{0, 0, 0,255},sentence[iMentatSentence+1]);
   298	            m_textDrawer->drawText(offsetX + 17, offsetY + 36,Color{255, 255, 255,255},sentence[iMentatSentence+1]);
   299	        }
   300	    }
   301	
   302	    if (state == AWAITING_RESPONSE) {
   303	        if (leftGuiButton) {
   304	            leftGuiButton->draw();
   305	        }
   306	        if (rightGuiButton){
   307	            rightGuiButton->draw();
   308	        }
   309	    }
   310	
   311	    if (m_guiBtnToMissionSelect) {
   312	        m_guiBtnToMissionSelect->draw();
   313	    }
   314	}
```

### CampaignProgress::nextMission — src/game/CampaignProgress.cpp@acddd29:155-158

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ PORT=acddd297b21ec200c7090dd2f1b73e014e2b74c0
$ git grep -n -E '^(.*[ *&])?CampaignProgress::nextMission\(' $PORT -- src | grep -v ';$'
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/CampaignProgress.cpp:155:int CampaignProgress::nextMission(int house) const
$ git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/CampaignProgress.cpp | nl -ba | sed -n '155,158p'
   155	int CampaignProgress::nextMission(int house) const
   156	{
   157	    return m_nextMission[houseIndex(house)];
   158	}
```

### CampaignProgress::highestUnlockedMission — src/game/CampaignProgress.cpp@acddd29:160-164

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ PORT=acddd297b21ec200c7090dd2f1b73e014e2b74c0
$ git grep -n -E '^(.*[ *&])?CampaignProgress::highestUnlockedMission\(' $PORT -- src | grep -v ';$'
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/CampaignProgress.cpp:160:int CampaignProgress::highestUnlockedMission(int house) const
$ git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/CampaignProgress.cpp | nl -ba | sed -n '160,164p'
   160	int CampaignProgress::highestUnlockedMission(int house) const
   161	{
   162	    const int next = nextMission(house);
   163	    return std::min(next, LAST_MISSION);
   164	}
```

### CampaignProgress::recordMissionVictory — src/game/CampaignProgress.cpp@acddd29:182-196

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ PORT=acddd297b21ec200c7090dd2f1b73e014e2b74c0
$ git grep -n -E '^(.*[ *&])?CampaignProgress::recordMissionVictory\(' $PORT -- src | grep -v ';$'
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/CampaignProgress.cpp:182:bool CampaignProgress::recordMissionVictory(int house, int mission)
$ git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/CampaignProgress.cpp | nl -ba | sed -n '182,196p'
   182	bool CampaignProgress::recordMissionVictory(int house, int mission)
   183	{
   184	    if (mission < FIRST_MISSION || mission > LAST_MISSION) {
   185	        throw std::invalid_argument("Campaign mission is outside the valid range");
   186	    }
   187	
   188	    int& next = m_nextMission[houseIndex(house)];
   189	    const int nextAfterVictory = mission + 1;
   190	    if (next >= nextAfterVictory) {
   191	        return false;
   192	    }
   193	
   194	    next = nextAfterVictory;
   195	    return true;
   196	}
```

### cGameConditionChecker::missionInit — src/game/cGameConditionChecker.cpp@acddd29:35-39

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ PORT=acddd297b21ec200c7090dd2f1b73e014e2b74c0
$ git grep -n -E '^(.*[ *&])?cGameConditionChecker::missionInit\(' $PORT -- src | grep -v ';$'
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGameConditionChecker.cpp:35:void cGameConditionChecker::missionInit()
$ git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGameConditionChecker.cpp | nl -ba | sed -n '35,39p'
    35	void cGameConditionChecker::missionInit()
    36	{
    37	    m_winFlags = 0;
    38	    m_loseFlags = 0;
    39	}
```

### cGameConditionChecker::isMissionWon — src/game/cGameConditionChecker.cpp@acddd29:53-83

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ PORT=acddd297b21ec200c7090dd2f1b73e014e2b74c0
$ git grep -n -E '^(.*[ *&])?cGameConditionChecker::isMissionWon\(' $PORT -- src | grep -v ';$'
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGameConditionChecker.cpp:53:bool cGameConditionChecker::isMissionWon() const
$ git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGameConditionChecker.cpp | nl -ba | sed -n '53,83p'
    53	bool cGameConditionChecker::isMissionWon() const
    54	{
    55	    cPlayer *humanPlayer = m_objects->getPlayer(HUMAN);
    56	    if (hasGameOverConditionHarvestForSpiceQuota()) {
    57	        if (humanPlayer->hasMetQuota()) {
    58	            return true;
    59	        }
    60	    }
    61	
    62	    if (hasGameOverConditionPlayerHasNoBuildings()) {
    63	        if (hasWinConditionHumanMustLoseAllBuildings()) {
    64	            if (!humanPlayer->isAlive()) {
    65	                return true;
    66	            }
    67	        }
    68	
    69	        if (hasWinConditionAIShouldLoseEverything()) {
    70	            if (allEnemyAIPlayersAreDestroyed()) {
    71	                return true;
    72	            }
    73	        }
    74	    }
    75	    else if (hasGameOverConditionAIHasNoBuildings()) {
    76	        if (hasWinConditionAIShouldLoseEverything()) {
    77	            if (allEnemyAIPlayersAreDestroyed()) {
    78	                return true;
    79	            }
    80	        }
    81	    }
    82	    return false;
    83	}
```

### cGameConditionChecker::isMissionFailed — src/game/cGameConditionChecker.cpp@acddd29:85-119

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ PORT=acddd297b21ec200c7090dd2f1b73e014e2b74c0
$ git grep -n -E '^(.*[ *&])?cGameConditionChecker::isMissionFailed\(' $PORT -- src | grep -v ';$'
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGameConditionChecker.cpp:85:bool cGameConditionChecker::isMissionFailed() const
$ git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGameConditionChecker.cpp | nl -ba | sed -n '85,119p'
    85	bool cGameConditionChecker::isMissionFailed() const
    86	{
    87	    if (hasGameOverConditionHarvestForSpiceQuota()) {
    88	        // check for non-human players if they have met spice quota, if so, they win (and thus human player loses)
    89	        for (int i = 1; i < MAX_PLAYERS; i++) {
    90	            cPlayer *player = m_objects->getPlayer(i);
    91	            if (player->isAlive() && player->hasMetQuota()) {
    92	                return true;
    93	            }
    94	        }
    95	    }
    96	
    97	    if (hasGameOverConditionPlayerHasNoBuildings()) {
    98	        cPlayer *humanPlayer = m_objects->getPlayer(HUMAN);
    99	        if (!humanPlayer->isAlive()) {
   100	            /**
   101	             * If any of the bits in “LoseFlags” is set and the corresponding condition holds true
   102	             * the player has won (and the computer has lost)
   103	             */
   104	            if (hasWinConditionHumanMustLoseAllBuildings()) {
   105	                // this means, if any other player has lost all, that player wins, this is not (yet)
   106	                // supported. Mainly because we can't distinguish yet between 'active' and non-active players
   107	                // since we have a fixed list of players.
   108	
   109	                // so for now just do this:
   110	                return false; // it is meant to win the game by drawStateLosing all...
   111	            }
   112	            else {
   113	                return true; // nope, it should lose mission now
   114	            }
   115	        }
   116	    }
   117	
   118	    return false;
   119	}
```

### cGame::missionInit — src/game/cGame_logic.cpp@acddd29:431-461

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ PORT=acddd297b21ec200c7090dd2f1b73e014e2b74c0
$ git grep -n -E '^(.*[ *&])?cGame::missionInit\(' $PORT -- src | grep -v ';$'
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGame_logic.cpp:431:void cGame::missionInit()
$ git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGame_logic.cpp | nl -ba | sed -n '431,461p'
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

### cGame::setMissionWon — src/game/cGame_logic.cpp@acddd29:472-498

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ PORT=acddd297b21ec200c7090dd2f1b73e014e2b74c0
$ git grep -n -E '^(.*[ *&])?cGame::setMissionWon\(' $PORT -- src | grep -v ';$'
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGame_logic.cpp:472:void cGame::setMissionWon()
$ git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGame_logic.cpp | nl -ba | sed -n '472,498p'
   472	void cGame::setMissionWon()
   473	{
   474	    m_missionWasWon = true;
   475	    if (!m_gameSettings->isSkirmish() && m_campaignProgress &&
   476	        CampaignProgress::supportsHouse(m_dataCampaign->housePlayer) &&
   477	        m_campaignProgress->recordMissionVictory(m_dataCampaign->housePlayer, m_dataCampaign->mission)) {
   478	        saveCampaignProgress();
   479	    }
   480	    setState(GAME_WINNING);
   481	
   482	    m_screenShake->reset();
   483	    m_mouse->setTile(MOUSE_NORMAL);
   484	
   485	    m_audioContext->playVoice(SOUND_VOICE_07_ATR, m_gameObjectsContext->getPlayer(HUMAN)->getHouse());
   486	
   487	    playMusicByType(eMusicType::WIN);
   488	
   489	    const MissionStats stats = m_missionStatsCollector->snapshot(m_timeManager->getElapsedSeconds());
   490	    Logger::info(COMP_GAME, "cGame::setMissionWon", "Mission stats: elapsedSeconds={}", stats.elapsedSeconds);
   491	    for (int playerId = 0; playerId < MAX_PLAYERS; playerId++) {
   492	        const PlayerMissionStats &playerStats = stats.players[playerId];
   493	        Logger::info(COMP_GAME, "cGame::setMissionWon", "Player {} stats: unitsBuilt={} unitsLost={} structuresBuilt={} structuresLost={}",
   494	            playerId, playerStats.unitsBuilt, playerStats.unitsLost, playerStats.structuresBuilt, playerStats.structuresLost);
   495	    }
   496	
   497	    takeBackGroundScreen();
   498	}
```

### cGame::setMissionLost — src/game/cGame_logic.cpp@acddd29:500-513

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ PORT=acddd297b21ec200c7090dd2f1b73e014e2b74c0
$ git grep -n -E '^(.*[ *&])?cGame::setMissionLost\(' $PORT -- src | grep -v ';$'
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGame_logic.cpp:500:void cGame::setMissionLost()
$ git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGame_logic.cpp | nl -ba | sed -n '500,513p'
   500	void cGame::setMissionLost()
   501	{
   502	    m_missionWasWon = false;
   503	    setState(GAME_LOSING);
   504	
   505	    m_screenShake->reset();
   506	    m_mouse->setTile(MOUSE_NORMAL);
   507	
   508	    m_audioContext->playVoice(SOUND_VOICE_08_ATR, m_gameObjectsContext->getPlayer(HUMAN)->getHouse());
   509	
   510	    playMusicByType(eMusicType::LOSE);
   511	
   512	    takeBackGroundScreen();
   513	}
```

### cGame::prepareMentatForPlayer — src/game/cGame_logic.cpp@acddd29:1239-1255

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ PORT=acddd297b21ec200c7090dd2f1b73e014e2b74c0
$ git grep -n -E '^(.*[ *&])?cGame::prepareMentatForPlayer\(' $PORT -- src | grep -v ';$'
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGame_logic.cpp:1239:void cGame::prepareMentatForPlayer()
$ git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGame_logic.cpp | nl -ba | sed -n '1239,1255p'
  1239	void cGame::prepareMentatForPlayer()
  1240	{
  1241	    if (m_state == GAME_BRIEFING) {
  1242	        missionInit();
  1243	        setupPlayers();
  1244	        auto *pState = dynamic_cast<cMentatState *>(m_creatorState->getState(eGameState::BRIEFING));
  1245	        pState->prepareMentat(m_dataCampaign->housePlayer);
  1246	    }
  1247	    else if (m_state == GAME_WINBRIEF) {
  1248	        auto *pState = dynamic_cast<cMentatState *>(m_creatorState->getState(eGameState::WINBRIEF));
  1249	        pState->prepareMentat(m_dataCampaign->housePlayer);
  1250	    }
  1251	    else if (m_state == GAME_LOSEBRIEF) {
  1252	        auto *pState = dynamic_cast<cMentatState *>(m_creatorState->getState(eGameState::LOSEBRIEF));
  1253	        pState->prepareMentat(m_dataCampaign->housePlayer);
  1254	    }
  1255	}
```

### cGame::prepareMentatToTellAboutHouse — src/game/cGame_logic.cpp@acddd29:1257-1285

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ PORT=acddd297b21ec200c7090dd2f1b73e014e2b74c0
$ git grep -n -E '^(.*[ *&])?cGame::prepareMentatToTellAboutHouse\(' $PORT -- src | grep -v ';$'
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGame_logic.cpp:1257:void cGame::prepareMentatToTellAboutHouse(int house)
$ git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGame_logic.cpp | nl -ba | sed -n '1257,1285p'
  1257	void cGame::prepareMentatToTellAboutHouse(int house)
  1258	{
  1259	    m_gameObjectsContext->getPlayer(HUMAN)->setHouse(house);
  1260	    m_dataCampaign->housePlayer = house;
  1261	    const int nextMission = m_campaignProgress && CampaignProgress::supportsHouse(house)
  1262	        ? m_campaignProgress->nextMission(house)
  1263	        : 0;
  1264	    if (nextMission >= CampaignProgress::FIRST_MISSION + 1) {
  1265	        setNextStateToTransitionTo(GAME_MISSIONSELECT);
  1266	        initiateFadingOut();
  1267	        return;
  1268	    }
  1269	    if (nextMission == CampaignProgress::FIRST_MISSION) {
  1270	        m_dataCampaign->mission = CampaignProgress::FIRST_MISSION;
  1271	        m_dataCampaign->region = 1;
  1272	        setNextStateToTransitionTo(GAME_BRIEFING);
  1273	        initiateFadingOut();
  1274	        return;
  1275	    }
  1276	
  1277	    bool stateAlreadyExisted = m_creatorState->hasState(eGameState::TELLHOUSE);
  1278	    auto *pState = dynamic_cast<cTellHouseState *>(m_creatorState->getState(eGameState::TELLHOUSE));
  1279	    if (!stateAlreadyExisted) {
  1280	        playMusicByTypeForStateTransition(eMusicType::BRIEFING);
  1281	    }
  1282	    pState->prepareMentat(house);
  1283	    setNextStateToTransitionTo(GAME_TELLHOUSE);
  1284	    initiateFadingOut();
  1285	}
```

### cGame::changeStateFromMentat — src/game/cGame_logic.cpp@acddd29:1307-1374

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ PORT=acddd297b21ec200c7090dd2f1b73e014e2b74c0
$ git grep -n -E '^(.*[ *&])?cGame::changeStateFromMentat\(' $PORT -- src | grep -v ';$'
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGame_logic.cpp:1307:void cGame::changeStateFromMentat()
$ git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGame_logic.cpp | nl -ba | sed -n '1307,1374p'
  1307	void cGame::changeStateFromMentat()
  1308	{
  1309	    if (isState(GAME_BRIEFING)) {
  1310	        // proceed, play mission (it is already loaded before we got here)
  1311	        setNextStateToTransitionTo(GAME_PLAYING);
  1312	        m_drawManager->missionInit();
  1313	
  1314	        // CENTER MOUSE
  1315	        setMousePosition(m_gameSettings->getScreenW() / 2, m_gameSettings->getScreenH() / 2);
  1316	
  1317	        initiateFadingOut();
  1318	
  1319	        playMusicByType(eMusicType::PEACE);
  1320	        return;
  1321	    }
  1322	
  1323	    if (m_gameSettings->isSkirmish()) {
  1324	        if (isState(GAME_WINBRIEF) || isState(GAME_LOSEBRIEF)) {
  1325	            // regardless of drawStateWinning or drawStateLosing, always go back to main menu
  1326	            setNextStateToTransitionTo(GAME_SETUPSKIRMISH);
  1327	            missionInit();
  1328	            initiateFadingOut();
  1329	        }
  1330	        else {
  1331	            Logger::warn(COMP_GAME, "cProceedButtonCommand", "pressed in skirmish mode but state is not WINBRIEF nor LOSEBRIEF");
  1332	        }
  1333	        return;
  1334	    }
  1335	
  1336	    // NOT a skirmish game
  1337	    Logger::info(COMP_GAME, "cGame::changeStateFromMentat", "state {}, campaign mission {}, region {}", m_state, m_dataCampaign->mission, m_dataCampaign->region);
  1338	
  1339	    // won the last mission, nothing left to conquer: show the credits (they lead back to the main menu)
  1340	    if (isState(GAME_WINBRIEF) && m_dataCampaign->mission >= LAST_CAMPAIGN_MISSION) {
  1341	        setNextStateToTransitionTo(GAME_CREDITS);
  1342	
  1343	        initiateFadingOut();
  1344	        return;
  1345	    }
  1346	
  1347	    // won mission, transition to region selection (Select your next Conquest)
  1348	    if (isState(GAME_WINBRIEF)) {
  1349	        setNextStateToTransitionTo(GAME_REGION);
  1350	
  1351	        initiateFadingOut();
  1352	        return;
  1353	    }
  1354	
  1355	    // lost mission
  1356	    if (isState(GAME_LOSEBRIEF)) {
  1357	        missionInit();
  1358	        // lost mission > 1, so we go back to region select
  1359	        if (m_dataCampaign->mission > 1)   {
  1360	            setNextStateToTransitionTo(GAME_REGION);
  1361	
  1362	            m_dataCampaign->mission--; // we did not win
  1363	        }
  1364	        else {
  1365	            // mission 1 failed, really?..., back to mentat with briefing
  1366	            setNextStateToTransitionTo(GAME_BRIEFING);
  1367	            prepareMentatForPlayer();
  1368	            playMusicByType(eMusicType::BRIEFING);
  1369	        }
  1370	
  1371	        initiateFadingOut();
  1372	        return;
  1373	    }
  1374	}
```

### cGame::checkMissionWinOrFail — src/game/cGame_logic.cpp@acddd29:1720-1731

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ PORT=acddd297b21ec200c7090dd2f1b73e014e2b74c0
$ git grep -n -E '^(.*[ *&])?cGame::checkMissionWinOrFail\(' $PORT -- src | grep -v ';$'
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGame_logic.cpp:1720:void cGame::checkMissionWinOrFail()
$ git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGame_logic.cpp | nl -ba | sed -n '1720,1731p'
  1720	void cGame::checkMissionWinOrFail()
  1721	{
  1722	    if (m_gameConditionChecker->isMissionFailed()) {
  1723	        setMissionLost();
  1724	        return;
  1725	    }
  1726	
  1727	    if (m_gameConditionChecker->isMissionWon()) {
  1728	        setMissionWon();
  1729	        return;
  1730	    }
  1731	}
```

### cMissionStatsCollector::cMissionStatsCollector — src/game/cMissionStatsCollector.cpp@acddd29:25-27

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ PORT=acddd297b21ec200c7090dd2f1b73e014e2b74c0
$ git grep -n -E '^(.*[ *&])?cMissionStatsCollector::cMissionStatsCollector\(' $PORT -- src | grep -v ';$'
acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cMissionStatsCollector.cpp:25:cMissionStatsCollector::cMissionStatsCollector(cGameObjectContext *objects) : m_objects(objects)
$ git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cMissionStatsCollector.cpp | nl -ba | sed -n '25,27p'
    25	cMissionStatsCollector::cMissionStatsCollector(cGameObjectContext *objects) : m_objects(objects)
    26	{
    27	}
```
