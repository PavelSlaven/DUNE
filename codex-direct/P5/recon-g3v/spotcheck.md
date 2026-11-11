# Сверка фактов

## Факты помощника 1

### Объявление `cScoringState` — `headers.md`, `src/gamestates/cScoringState.h@91416fb:15`

Команда:

```text
git show 91416fb0c6aae877242d55e08559c32ec80de3e0:src/gamestates/cScoringState.h | nl -ba | sed -n '15p'
```

Вывод:

```text
    15	class cScoringState : public cGameState {
```

Итог: совпало.

### Объявление `cVideoState` — `headers.md`, `src/gamestates/cVideoState.h@91416fb:28`

Команда:

```text
git show 91416fb0c6aae877242d55e08559c32ec80de3e0:src/gamestates/cVideoState.h | nl -ba | sed -n '28p'
```

Вывод:

```text
    28	class cVideoState : public cGameState {
```

Итог: совпало.

### Объявление `cEditorState` — `headers.md`, `src/gamestates/cEditorState.h@91416fb:44`

Команда:

```text
git show 91416fb0c6aae877242d55e08559c32ec80de3e0:src/gamestates/cEditorState.h | nl -ba | sed -n '44p'
```

Вывод:

```text
    44	class cEditorState : public cGameState {
```

Итог: совпало.

### Объявление `cNewMapEditorState` — `headers.md`, `src/gamestates/cNewMapEditorState.h@91416fb:40`

Команда:

```text
git show 91416fb0c6aae877242d55e08559c32ec80de3e0:src/gamestates/cNewMapEditorState.h | nl -ba | sed -n '40p'
```

Вывод:

```text
    40	class cNewMapEditorState : public cGameState {
```

Итог: совпало.

## Факты помощника 2

### Переход в `GAME_VIDEO` — `entries.md`, `src/game/cGame_logic.cpp@91416fb:238`

Команда:

```text
git show 91416fb0c6aae877242d55e08559c32ec80de3e0:src/game/cGame_logic.cpp | nl -ba | sed -n '233,243p'
```

Вывод:

```text
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

Итог: совпало.

### Переход из меню в `GAME_NEW_MAP_EDITOR` — `entries.md`, `src/gamestates/cMainMenuState.cpp@91416fb:164`

Команда:

```text
git show 91416fb0c6aae877242d55e08559c32ec80de3e0:src/gamestates/cMainMenuState.cpp | nl -ba | sed -n '159,169p'
```

Вывод:

```text
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

Итог: совпало.

### Переход из настройки сражения в `GAME_NEW_MAP_EDITOR` — `entries.md`, `src/gamestates/cSetupSkirmishState.cpp@91416fb:382`

Команда:

```text
git show 91416fb0c6aae877242d55e08559c32ec80de3e0:src/gamestates/cSetupSkirmishState.cpp | nl -ba | sed -n '377,387p'
```

Вывод:

```text
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

Итог: совпало.

### Переход в `GAME_SCORING` — `entries.md`, `src/gamestates/cWinLoseState.cpp@91416fb:141`

Команда:

```text
git show 91416fb0c6aae877242d55e08559c32ec80de3e0:src/gamestates/cWinLoseState.cpp | nl -ba | sed -n '136,146p'
```

Вывод:

```text
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

Итог: совпало.
