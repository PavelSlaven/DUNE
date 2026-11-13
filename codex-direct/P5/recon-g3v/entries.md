# Пункт 2. Где игра входит в состояния

Команда: `git grep -n -E 'GAME_SCORING|GAME_VIDEO|GAME_EDITOR|GAME_NEW_MAP_EDITOR|eGameState::(SCORING|VIDEO|EDITOR|NEW_MAP_EDITOR)\b' 91416fb0c6aae877242d55e08559c32ec80de3e0 -- src`

```text
91416fb0c6aae877242d55e08559c32ec80de3e0:src/game/cGame_logic.cpp:238:            setNextStateToTransitionTo(GAME_VIDEO);
91416fb0c6aae877242d55e08559c32ec80de3e0:src/game/cGame_logic.cpp:961:            case GAME_EDITOR: mapped = eGameState::EDITOR; return true;
91416fb0c6aae877242d55e08559c32ec80de3e0:src/game/cGame_logic.cpp:967:            case GAME_SCORING: mapped = eGameState::SCORING; return true;
91416fb0c6aae877242d55e08559c32ec80de3e0:src/game/cGame_logic.cpp:974:            case GAME_NEW_MAP_EDITOR: mapped = eGameState::NEW_MAP_EDITOR; return true;
91416fb0c6aae877242d55e08559c32ec80de3e0:src/game/cGame_logic.cpp:990:                               newState != GAME_EDITOR &&
91416fb0c6aae877242d55e08559c32ec80de3e0:src/game/cGame_logic.cpp:1144:            else if (newState == GAME_EDITOR) {
91416fb0c6aae877242d55e08559c32ec80de3e0:src/game/cGame_logic.cpp:1145:                newStatePtr = m_creatorState->getState(eGameState::EDITOR);
91416fb0c6aae877242d55e08559c32ec80de3e0:src/game/cGame_logic.cpp:1147:            else if (newState == GAME_VIDEO) {
91416fb0c6aae877242d55e08559c32ec80de3e0:src/game/cGame_logic.cpp:1148:                newStatePtr = m_creatorState->getState(eGameState::VIDEO);
91416fb0c6aae877242d55e08559c32ec80de3e0:src/game/cGame_logic.cpp:1155:            else if (newState == GAME_NEW_MAP_EDITOR) {
91416fb0c6aae877242d55e08559c32ec80de3e0:src/game/cGame_logic.cpp:1156:                newStatePtr = m_creatorState->getState(eGameState::NEW_MAP_EDITOR);
91416fb0c6aae877242d55e08559c32ec80de3e0:src/game/cGame_logic.cpp:1204:            else if (newState == GAME_SCORING) {
91416fb0c6aae877242d55e08559c32ec80de3e0:src/game/cGame_logic.cpp:1205:                newStatePtr = m_creatorState->getState(eGameState::SCORING);
91416fb0c6aae877242d55e08559c32ec80de3e0:src/game/cGame_logic.cpp:1735:    setState(GAME_EDITOR);
91416fb0c6aae877242d55e08559c32ec80de3e0:src/game/cGame_logic.cpp:1736:    auto *pState = dynamic_cast<cEditorState*>(m_creatorState->getState(eGameState::EDITOR));
91416fb0c6aae877242d55e08559c32ec80de3e0:src/gamestates/cCreatorState.cpp:82:    m_states[eGameState::VIDEO] = std::make_unique<cVideoState>(m_services, filename);
91416fb0c6aae877242d55e08559c32ec80de3e0:src/gamestates/cCreatorState.cpp:105:        case eGameState::EDITOR:
91416fb0c6aae877242d55e08559c32ec80de3e0:src/gamestates/cCreatorState.cpp:106:            m_states[eGameState::EDITOR] = std::make_unique<cEditorState>(m_services);
91416fb0c6aae877242d55e08559c32ec80de3e0:src/gamestates/cCreatorState.cpp:109:        case eGameState::NEW_MAP_EDITOR:
91416fb0c6aae877242d55e08559c32ec80de3e0:src/gamestates/cCreatorState.cpp:110:            m_states[eGameState::NEW_MAP_EDITOR] = std::make_unique<cNewMapEditorState>(m_services, m_cIni);
91416fb0c6aae877242d55e08559c32ec80de3e0:src/gamestates/cCreatorState.cpp:121:        case eGameState::SCORING:
91416fb0c6aae877242d55e08559c32ec80de3e0:src/gamestates/cCreatorState.cpp:122:            m_states[eGameState::SCORING] = std::make_unique<cScoringState>(m_services);
91416fb0c6aae877242d55e08559c32ec80de3e0:src/gamestates/cGameState.h:31:    GAMESTATE_EDITOR,                       // #define GAME_EDITOR      4      // running the editor
91416fb0c6aae877242d55e08559c32ec80de3e0:src/gamestates/cGameState.h:32:    GAMESTATE_NEW_MAP_EDITOR,               // #define GAME_NEW_MAP_EDITOR 19    // new map editor
91416fb0c6aae877242d55e08559c32ec80de3e0:src/gamestates/cGameState.h:39:    GAMESTATE_SCORING,                      // #define GAME_SCORING     20      // crude mission scoring screen, shown after winning
91416fb0c6aae877242d55e08559c32ec80de3e0:src/gamestates/cMainMenuState.cpp:164:        m_stateTransitions->setNextStateWithFade(GAME_NEW_MAP_EDITOR);
91416fb0c6aae877242d55e08559c32ec80de3e0:src/gamestates/cNewmapEditorState.cpp:275:            m_stateTransitions->setNextStateWithFade(GAME_EDITOR);
91416fb0c6aae877242d55e08559c32ec80de3e0:src/gamestates/cSetupSkirmishState.cpp:382:                m_stateTransitions->setNextStateWithFade(GAME_NEW_MAP_EDITOR);
91416fb0c6aae877242d55e08559c32ec80de3e0:src/gamestates/cWinLoseState.cpp:141:        m_stateTransitions->setNextState(GAME_SCORING);
91416fb0c6aae877242d55e08559c32ec80de3e0:src/include/eGameState.cpp:34:        case GAME_EDITOR:
91416fb0c6aae877242d55e08559c32ec80de3e0:src/include/eGameState.cpp:35:            return "GAME_EDITOR";
91416fb0c6aae877242d55e08559c32ec80de3e0:src/include/eGameState.cpp:36:        case GAME_NEW_MAP_EDITOR:
91416fb0c6aae877242d55e08559c32ec80de3e0:src/include/eGameState.cpp:37:            return "GAME_NEW_MAP_EDITOR";
91416fb0c6aae877242d55e08559c32ec80de3e0:src/include/eGameState.cpp:60:        case GAME_SCORING:
91416fb0c6aae877242d55e08559c32ec80de3e0:src/include/eGameState.cpp:61:            return "GAME_SCORING";
91416fb0c6aae877242d55e08559c32ec80de3e0:src/include/eGameState.cpp:62:        case GAME_VIDEO:
91416fb0c6aae877242d55e08559c32ec80de3e0:src/include/eGameState.cpp:63:            return "GAME_VIDEO";
91416fb0c6aae877242d55e08559c32ec80de3e0:src/include/eGameState.cpp:80:        case eGameState::EDITOR: return "EDITOR";
91416fb0c6aae877242d55e08559c32ec80de3e0:src/include/eGameState.cpp:81:        case eGameState::NEW_MAP_EDITOR: return "NEW_MAP_EDITOR";
91416fb0c6aae877242d55e08559c32ec80de3e0:src/include/eGameState.cpp:88:        case eGameState::SCORING: return "SCORING";
91416fb0c6aae877242d55e08559c32ec80de3e0:src/include/eGameState.cpp:96:        case eGameState::VIDEO: return "VIDEO";
91416fb0c6aae877242d55e08559c32ec80de3e0:src/include/eGameState.h:52:inline constexpr int GAME_EDITOR = 4;      // running the editor
91416fb0c6aae877242d55e08559c32ec80de3e0:src/include/eGameState.h:66:inline constexpr int GAME_NEW_MAP_EDITOR = 19;    // new map editor
91416fb0c6aae877242d55e08559c32ec80de3e0:src/include/eGameState.h:67:inline constexpr int GAME_SCORING = 20;      // crude mission scoring screen, shown after winning
91416fb0c6aae877242d55e08559c32ec80de3e0:src/include/eGameState.h:68:inline constexpr int GAME_VIDEO = 21;           // playing a video
```

### src/game/cGame_logic.cpp@91416fb:238

Команда и вывод:

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git show 91416fb0c6aae877242d55e08559c32ec80de3e0:src/game/cGame_logic.cpp | nl -ba | sed -n '233,243p'
   233	        }
   234	    );
   235	    m_videoFlow = std::make_unique<VideoFlow>(
   236	        [this](const std::string &filename) {
   237	            m_creatorState->createVideoState(filename);
   238	            setNextStateToTransitionTo(GAME_VIDEO);
   239	        }
   240	    );
   241	    m_missionFlow = std::make_unique<MissionFlow>(
   242	        [this]() {
   243	            missionInit();
```

### src/game/cGame_logic.cpp@91416fb:961

Команда и вывод:

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git show 91416fb0c6aae877242d55e08559c32ec80de3e0:src/game/cGame_logic.cpp | nl -ba | sed -n '956,966p'
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
```

### src/game/cGame_logic.cpp@91416fb:967

Команда и вывод:

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git show 91416fb0c6aae877242d55e08559c32ec80de3e0:src/game/cGame_logic.cpp | nl -ba | sed -n '962,972p'
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
```

### src/game/cGame_logic.cpp@91416fb:974

Команда и вывод:

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git show 91416fb0c6aae877242d55e08559c32ec80de3e0:src/game/cGame_logic.cpp | nl -ba | sed -n '969,979p'
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
```

### src/game/cGame_logic.cpp@91416fb:990

Команда и вывод:

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git show 91416fb0c6aae877242d55e08559c32ec80de3e0:src/game/cGame_logic.cpp | nl -ba | sed -n '985,995p'
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
```

### src/game/cGame_logic.cpp@91416fb:1144

Команда и вывод:

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git show 91416fb0c6aae877242d55e08559c32ec80de3e0:src/game/cGame_logic.cpp | nl -ba | sed -n '1139,1149p'
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
```

### src/game/cGame_logic.cpp@91416fb:1145

Команда и вывод:

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git show 91416fb0c6aae877242d55e08559c32ec80de3e0:src/game/cGame_logic.cpp | nl -ba | sed -n '1140,1150p'
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
```

### src/game/cGame_logic.cpp@91416fb:1147

Команда и вывод:

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git show 91416fb0c6aae877242d55e08559c32ec80de3e0:src/game/cGame_logic.cpp | nl -ba | sed -n '1142,1152p'
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
```

### src/game/cGame_logic.cpp@91416fb:1148

Команда и вывод:

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git show 91416fb0c6aae877242d55e08559c32ec80de3e0:src/game/cGame_logic.cpp | nl -ba | sed -n '1143,1153p'
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
```

### src/game/cGame_logic.cpp@91416fb:1155

Команда и вывод:

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git show 91416fb0c6aae877242d55e08559c32ec80de3e0:src/game/cGame_logic.cpp | nl -ba | sed -n '1150,1160p'
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
```

### src/game/cGame_logic.cpp@91416fb:1156

Команда и вывод:

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git show 91416fb0c6aae877242d55e08559c32ec80de3e0:src/game/cGame_logic.cpp | nl -ba | sed -n '1151,1161p'
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
```

### src/game/cGame_logic.cpp@91416fb:1204

Команда и вывод:

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git show 91416fb0c6aae877242d55e08559c32ec80de3e0:src/game/cGame_logic.cpp | nl -ba | sed -n '1199,1209p'
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
```

### src/game/cGame_logic.cpp@91416fb:1205

Команда и вывод:

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git show 91416fb0c6aae877242d55e08559c32ec80de3e0:src/game/cGame_logic.cpp | nl -ba | sed -n '1200,1210p'
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
```

### src/game/cGame_logic.cpp@91416fb:1735

Команда и вывод:

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git show 91416fb0c6aae877242d55e08559c32ec80de3e0:src/game/cGame_logic.cpp | nl -ba | sed -n '1730,1740p'
  1730	    }
  1731	}
  1732	
  1733	void cGame::loadMapFromEditor(int map)
  1734	{
  1735	    setState(GAME_EDITOR);
  1736	    auto *pState = dynamic_cast<cEditorState*>(m_creatorState->getState(eGameState::EDITOR));
  1737	    pState->loadMap(map);
  1738	}
```

### src/game/cGame_logic.cpp@91416fb:1736

Команда и вывод:

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git show 91416fb0c6aae877242d55e08559c32ec80de3e0:src/game/cGame_logic.cpp | nl -ba | sed -n '1731,1741p'
  1731	}
  1732	
  1733	void cGame::loadMapFromEditor(int map)
  1734	{
  1735	    setState(GAME_EDITOR);
  1736	    auto *pState = dynamic_cast<cEditorState*>(m_creatorState->getState(eGameState::EDITOR));
  1737	    pState->loadMap(map);
  1738	}
```

### src/gamestates/cCreatorState.cpp@91416fb:82

Команда и вывод:

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git show 91416fb0c6aae877242d55e08559c32ec80de3e0:src/gamestates/cCreatorState.cpp | nl -ba | sed -n '77,87p'
    77	bool cCreatorState::hasState(eGameState gameState) const {
    78	    return m_states[gameState].has_value();
    79	}
    80	
    81	void cCreatorState::createVideoState(const std::string &filename) {
    82	    m_states[eGameState::VIDEO] = std::make_unique<cVideoState>(m_services, filename);
    83	}
    84	
    85	void cCreatorState::destroyState(eGameState gameState) {
    86	    m_states[gameState].reset();
    87	}
```

### src/gamestates/cCreatorState.cpp@91416fb:105

Команда и вывод:

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git show 91416fb0c6aae877242d55e08559c32ec80de3e0:src/gamestates/cCreatorState.cpp | nl -ba | sed -n '100,110p'
   100	
   101	        case eGameState::CREDITS:
   102	            m_states[eGameState::CREDITS] = std::make_unique<cCreditsState>(m_services);
   103	            break;
   104	
   105	        case eGameState::EDITOR:
   106	            m_states[eGameState::EDITOR] = std::make_unique<cEditorState>(m_services);
   107	            break;
   108	
   109	        case eGameState::NEW_MAP_EDITOR:
   110	            m_states[eGameState::NEW_MAP_EDITOR] = std::make_unique<cNewMapEditorState>(m_services, m_cIni);
```

### src/gamestates/cCreatorState.cpp@91416fb:106

Команда и вывод:

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git show 91416fb0c6aae877242d55e08559c32ec80de3e0:src/gamestates/cCreatorState.cpp | nl -ba | sed -n '101,111p'
   101	        case eGameState::CREDITS:
   102	            m_states[eGameState::CREDITS] = std::make_unique<cCreditsState>(m_services);
   103	            break;
   104	
   105	        case eGameState::EDITOR:
   106	            m_states[eGameState::EDITOR] = std::make_unique<cEditorState>(m_services);
   107	            break;
   108	
   109	        case eGameState::NEW_MAP_EDITOR:
   110	            m_states[eGameState::NEW_MAP_EDITOR] = std::make_unique<cNewMapEditorState>(m_services, m_cIni);
   111	            break;
```

### src/gamestates/cCreatorState.cpp@91416fb:109

Команда и вывод:

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git show 91416fb0c6aae877242d55e08559c32ec80de3e0:src/gamestates/cCreatorState.cpp | nl -ba | sed -n '104,114p'
   104	
   105	        case eGameState::EDITOR:
   106	            m_states[eGameState::EDITOR] = std::make_unique<cEditorState>(m_services);
   107	            break;
   108	
   109	        case eGameState::NEW_MAP_EDITOR:
   110	            m_states[eGameState::NEW_MAP_EDITOR] = std::make_unique<cNewMapEditorState>(m_services, m_cIni);
   111	            break;
   112	
   113	        case eGameState::WINNING:
   114	            m_states[eGameState::WINNING] = std::make_unique<cWinLoseState>(m_services, Outcome::Win);
```

### src/gamestates/cCreatorState.cpp@91416fb:110

Команда и вывод:

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git show 91416fb0c6aae877242d55e08559c32ec80de3e0:src/gamestates/cCreatorState.cpp | nl -ba | sed -n '105,115p'
   105	        case eGameState::EDITOR:
   106	            m_states[eGameState::EDITOR] = std::make_unique<cEditorState>(m_services);
   107	            break;
   108	
   109	        case eGameState::NEW_MAP_EDITOR:
   110	            m_states[eGameState::NEW_MAP_EDITOR] = std::make_unique<cNewMapEditorState>(m_services, m_cIni);
   111	            break;
   112	
   113	        case eGameState::WINNING:
   114	            m_states[eGameState::WINNING] = std::make_unique<cWinLoseState>(m_services, Outcome::Win);
   115	            break;
```

### src/gamestates/cCreatorState.cpp@91416fb:121

Команда и вывод:

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git show 91416fb0c6aae877242d55e08559c32ec80de3e0:src/gamestates/cCreatorState.cpp | nl -ba | sed -n '116,126p'
   116	
   117	        case eGameState::LOSING:
   118	            m_states[eGameState::LOSING] = std::make_unique<cWinLoseState>(m_services, Outcome::Lose);
   119	            break;
   120	
   121	        case eGameState::SCORING:
   122	            m_states[eGameState::SCORING] = std::make_unique<cScoringState>(m_services);
   123	            break;
   124	
   125	        case eGameState::BRIEFING:
   126	            m_states[eGameState::BRIEFING] = std::make_unique<cMentatState>(
```

### src/gamestates/cCreatorState.cpp@91416fb:122

Команда и вывод:

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git show 91416fb0c6aae877242d55e08559c32ec80de3e0:src/gamestates/cCreatorState.cpp | nl -ba | sed -n '117,127p'
   117	        case eGameState::LOSING:
   118	            m_states[eGameState::LOSING] = std::make_unique<cWinLoseState>(m_services, Outcome::Lose);
   119	            break;
   120	
   121	        case eGameState::SCORING:
   122	            m_states[eGameState::SCORING] = std::make_unique<cScoringState>(m_services);
   123	            break;
   124	
   125	        case eGameState::BRIEFING:
   126	            m_states[eGameState::BRIEFING] = std::make_unique<cMentatState>(
   127	                m_services, MentatMode::Briefing, m_cIni, m_dataCampaign);
```

### src/gamestates/cGameState.h@91416fb:31

Команда и вывод:

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git show 91416fb0c6aae877242d55e08559c32ec80de3e0:src/gamestates/cGameState.h | nl -ba | sed -n '26,36p'
    26	class cLog;
    27	
    28	enum eGameStateType {
    29	    GAMESTATE_CHOOSE_HOUSE,                 // #define GAME_SELECT_HOUSE  8		// pick a house
    30	    GAMESTATE_CREDITS,                      // #define GAME_CREDITS       17    // credits
    31	    GAMESTATE_EDITOR,                       // #define GAME_EDITOR      4      // running the editor
    32	    GAMESTATE_NEW_MAP_EDITOR,               // #define GAME_NEW_MAP_EDITOR 19    // new map editor
    33	    GAMESTATE_MAIN_MENU,                    // #define GAME_MENU          1     // in a menu    
    34	    GAMESTATE_MENTAT,                       // #define GAME_WINNING     11      // when winning, do some cool animation
    35	                                            // #define GAME_LOSEBRIEF   13      // briefing when losing
    36	                                            // #define GAME_BRIEFING     3      // doing some briefing
```

### src/gamestates/cGameState.h@91416fb:32

Команда и вывод:

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git show 91416fb0c6aae877242d55e08559c32ec80de3e0:src/gamestates/cGameState.h | nl -ba | sed -n '27,37p'
    27	
    28	enum eGameStateType {
    29	    GAMESTATE_CHOOSE_HOUSE,                 // #define GAME_SELECT_HOUSE  8		// pick a house
    30	    GAMESTATE_CREDITS,                      // #define GAME_CREDITS       17    // credits
    31	    GAMESTATE_EDITOR,                       // #define GAME_EDITOR      4      // running the editor
    32	    GAMESTATE_NEW_MAP_EDITOR,               // #define GAME_NEW_MAP_EDITOR 19    // new map editor
    33	    GAMESTATE_MAIN_MENU,                    // #define GAME_MENU          1     // in a menu    
    34	    GAMESTATE_MENTAT,                       // #define GAME_WINNING     11      // when winning, do some cool animation
    35	                                            // #define GAME_LOSEBRIEF   13      // briefing when losing
    36	                                            // #define GAME_BRIEFING     3      // doing some briefing
    37	    GAMESTATE_OPTIONS,                      // #define GAME_OPTIONS	      5     // options menu
```

### src/gamestates/cGameState.h@91416fb:39

Команда и вывод:

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git show 91416fb0c6aae877242d55e08559c32ec80de3e0:src/gamestates/cGameState.h | nl -ba | sed -n '34,44p'
    34	    GAMESTATE_MENTAT,                       // #define GAME_WINNING     11      // when winning, do some cool animation
    35	                                            // #define GAME_LOSEBRIEF   13      // briefing when losing
    36	                                            // #define GAME_BRIEFING     3      // doing some briefing
    37	    GAMESTATE_OPTIONS,                      // #define GAME_OPTIONS	      5     // options menu
    38	    GAMESTATE_PLAYING,                      // #define GAME_PLAYING      2      // playing the actual game
    39	    GAMESTATE_SCORING,                      // #define GAME_SCORING     20      // crude mission scoring screen, shown after winning
    40	    GAMESTATE_SELECT_MISSION,               // #define GAME_MISSIONSELECT 18    // mission select
    41	    GAMESTATE_SELECT_YOUR_NEXT_CONQUEST,    // #define GAME_REGION		  6	    // select a region / select your next conquest
    42	    GAMESTATE_SETUP_SKIRMISH,               // #define GAME_SETUPSKIRMISH 16    // set up a skirmish game
    43	    GAMESTATE_TELLHOUSE,                    // #define GAME_TELLHOUSE	10		// tell about the house
    44	    GAMESTATE_WINLOSE,                      // #define GAME_LOSING      14      // when losing, do something cool
```

### src/gamestates/cMainMenuState.cpp@91416fb:164

Команда и вывод:

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git show 91416fb0c6aae877242d55e08559c32ec80de3e0:src/gamestates/cMainMenuState.cpp | nl -ba | sed -n '159,169p'
   159	        m_missionFlow->init();
   160	        m_stateTransitions->setNextStateWithFade(GAME_SETUPSKIRMISH);
   161	    });
   162	    addButton("Load", false, nullptr);
   163	    addButton("Map Editor", true, [this]() {
   164	        m_stateTransitions->setNextStateWithFade(GAME_NEW_MAP_EDITOR);
   165	    });
   166	    addButton("Options", true, [this]() {
   167	        m_stateTransitions->setNextState(GAME_OPTIONS);
   168	    });
   169	    addButton("Hall of Fame", false, nullptr);
```

### src/gamestates/cNewmapEditorState.cpp@91416fb:275

Команда и вывод:

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git show 91416fb0c6aae877242d55e08559c32ec80de3e0:src/gamestates/cNewmapEditorState.cpp | nl -ba | sed -n '270,280p'
   270	        .withRenderer(m_sdlDrawer)
   271	        .withTheme(cGuiThemeBuilder().light().build())
   272	        .onClick([this](){
   273	            this->constructEmptyMap();
   274	            m_scenarioFlow->loadMapFromEditor(-1); // -1 means load the map from the editor, instead of loading a skirmish map
   275	            m_stateTransitions->setNextStateWithFade(GAME_EDITOR);
   276	        })
   277	        .build();
   278	    m_guiWindow->addGuiObject(std::move(gui_btn_Back));
   279	}
   280	
```

### src/gamestates/cSetupSkirmishState.cpp@91416fb:382

Команда и вывод:

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git show 91416fb0c6aae877242d55e08559c32ec80de3e0:src/gamestates/cSetupSkirmishState.cpp | nl -ba | sed -n '377,387p'
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
```

### src/gamestates/cWinLoseState.cpp@91416fb:141

Команда и вывод:

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git show 91416fb0c6aae877242d55e08559c32ec80de3e0:src/gamestates/cWinLoseState.cpp | nl -ba | sed -n '136,146p'
   136	void cWinLoseState::onMouseLeftButtonClicked(const s_MouseEvent &) const
   137	{
   138	    if (m_statement == Outcome::Lose) {
   139	        m_missionFlow->goingToWinLoseBrief(GAME_LOSEBRIEF);
   140	    } else {
   141	        m_stateTransitions->setNextState(GAME_SCORING);
   142	    }
   143	    // FADE OUT
   144	    m_stateTransitions->fadeOut();
   145	}
```
