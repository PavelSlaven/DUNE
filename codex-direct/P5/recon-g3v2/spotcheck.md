# Spotcheck P5G3V2

## 1. Окно новой карты задаёт заголовок «Map editor configuration».

Источник: помощник 1 — screens.md.

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show c5834615f8fc71789bba7108078a461018cc7d56:src/gamestates/cNewmapEditorState.cpp | nl -ba | sed -n '84,85p'
```

Вывод:

```text
    84	    // Title
    85	    m_guiWindow->setTitle("Map editor configuration");
```

Итог: совпало

## 2. Конструктор отчёта миссии сохраняет snapshot сборщика статистики с прошедшим временем миссии.

Источник: помощник 1 — screens.md.

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show c5834615f8fc71789bba7108078a461018cc7d56:src/gamestates/cScoringState.cpp | nl -ba | sed -n '39,40p'
```

Вывод:

```text
    39	    m_stats = services->missionStatsCollector->snapshot(m_ctx->getTimeManager()->getElapsedSeconds());
    40	}
```

Итог: совпало

## 3. GuiObject записывает геометрию GUI и клика через uiaudit::recordGui и uiaudit::recordClick.

Источник: помощник 1 — gui.md.

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show c5834615f8fc71789bba7108078a461018cc7d56:src/gui/GuiObject.cpp | nl -ba | sed -n '35,43p'
```

Вывод:

```text
    35	void GuiObject::auditRecord(const char *type) const
    36	{
    37	    uiaudit::recordGui(type, m_rect.getX(), m_rect.getY(), m_rect.getWidth(), m_rect.getHeight());
    38	}
    39	
    40	void GuiObject::auditClick(const std::string &name) const
    41	{
    42	    uiaudit::recordClick(name.c_str(), m_rect.getX(), m_rect.getY(), m_rect.getWidth(), m_rect.getHeight());
    43	}
```

Итог: совпало

## 4. GuiBar принимает событие мыши только внутри своей рамки и затем рассылает его GUI-элементам.

Источник: помощник 1 — gui.md.

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show c5834615f8fc71789bba7108078a461018cc7d56:src/gui/GuiBar.cpp | nl -ba | sed -n '73,80p'
```

Вывод:

```text
    73	void GuiBar::onNotifyMouseEvent(const s_MouseEvent &event)
    74	{
    75	    if (!event.coords.isWithinRectangle(&m_rect))
    76	        return;
    77	    for (auto &guiObject : gui_objects) {
    78	        guiObject->onNotifyMouseEvent(event);
    79	    }
    80	}
```

Итог: совпало

## 5. На экране исхода поражение ведёт в GAME_LOSEBRIEF, победа — в GAME_SCORING; затем выполняется fadeOut.

Источник: помощник 2 — data.md.

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show c5834615f8fc71789bba7108078a461018cc7d56:src/gamestates/cWinLoseState.cpp | nl -ba | sed -n '136,145p'
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

Итог: совпало

## 6. cMissionStatsCollector объявляет приём игровых событий и создание snapshot по elapsedSeconds.

Источник: помощник 2 — data.md.

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show c5834615f8fc71789bba7108078a461018cc7d56:src/game/cMissionStatsCollector.h | nl -ba | sed -n '25,30p'
```

Вывод:

```text
    25	class cMissionStatsCollector {
    26	public:
    27	    explicit cMissionStatsCollector(cGameObjectContext *objects);
    28	    void onNotifyGameEvent(const s_GameEvent &event);
    29	    [[nodiscard]] MissionStats snapshot(uint64_t elapsedSeconds) const;
    30	
```

Итог: совпало

## 7. В игровой логике callback передаёт индекс карты схватки в loadMapFromEditor.

Источник: помощник 2 — data.md.

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show c5834615f8fc71789bba7108078a461018cc7d56:src/game/cGame_logic.cpp | nl -ba | sed -n '264,274p'
```

Вывод:

```text
   264	        },
   265	        [this]() {
   266	            loadScenario();
   267	        },
   268	        [this](int iSkirmishMap) {
   269	            loadMapFromEditor(iSkirmishMap);
   270	        },
   271	        [this](cPlayer* player) {
   272	            setPlayerToInteractFor(player);
   273	        }
   274	    );
```

Итог: совпало

## 8. cPreviewMaps предоставляет setEditorMap для замены карты, передаваемой редактору при loadMapFromEditor(-1).

Источник: помощник 2 — data.md.

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show c5834615f8fc71789bba7108078a461018cc7d56:src/gameobjects/map/cPreviewMaps.h | nl -ba | sed -n '59,63p'
```

Вывод:

```text
    59	    void createEmptyMap(const std::string &name, const std::string &author,
    60	            const std::string &desciption, int width, int height);
    61	
    62	    // replaces the map that loadMapFromEditor(-1) hands to the editor
    63	    void setEditorMap(s_PreviewMap &&map);
```

Итог: совпало

