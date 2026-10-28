Ответ ведущего на `DONE-b0` третьего круга. Независимая приёмка нашла три ошибки отнесения. Ниже — механические правки, продиктованные дословно: плана не присылай, выполняй по порядку. Своих решений об отнесении не принимай; другие пути, маркеры и разделы карты не трогай. Если правка не ложится в файл так, как написано, или после правок тест краснеет — остановись и пришли `## Q-b0-NN` с выводом; тест не ослабляй и не меняй.

## REVIEW-b0 | 2026-10-28 | механика

Рамка правок прежняя: `tools/upstream/port_features.json`, `docs/upstream/port_inventory.json` (только пересборкой скриптом), `docs/upstream/PORT_MAP.md`. Файлы `tools/upstream/port_inventory.py` и `tools/upstream/tests/test_port_inventory.py` не меняются. Коммиты не создавай. Python запускай только с `PYTHONDONTWRITEBYTECODE=1`; рабочие файлы и логи — в `.tmp/`.

### Организация работы

- Порядок: пункты 1 → 2 → 3 → 4 → 5 строго по очереди; каждый следующий опирается на результат предыдущего.
- Параллельно: ничего.
- Помощники: не нужны — ноль одновременно; всё делаешь сам, работа механическая.
- Остановки: расхождение с ожидаемым итогом пункта 2, красный тест, правка, которая не ложится в файл дословно, — `## Q-b0-NN` и стоп.
- Рамка правок: три файла, перечисленные выше, и папка `.tmp/`.

### 1. `tools/upstream/port_features.json`

Строки маркеров ниже записаны так, как они стоят в файле JSON (с двойной обратной косой чертой).

Функция `localization`:
- в конец списка `include` добавь две строки: `"src/cGame.h"` и `"src/drawers/OrderButtonPolicy.hpp"`;
- в конец списка `markers` добавь два маркера: `"\\bm_hd(?:Victory|Defeat)(?:Ru|En)\\b"` и `"\\b(?:OrderButtonPolicy|shouldDrawOrderLabelShadow)\\b"`.

Функция `music-pools`:
- маркер `"\\b(?:m_playMusic|playMusicFile|releaseExternalMusic|m_externalMusic|m_lastEnemyWarningMs)\\b"` замени на `"\\b(?:playMusicFile|releaseExternalMusic|m_externalMusic|m_lastEnemyWarningMs)\\b"`;
- маркер `"\"playMusic\""` удали;
- из `include` удали строки `"src/gamestates/cMainMenuState.cpp"` и `"src/utils/common.cpp"`.

Функция `command-bar`:
- маркер `"\\b(?:CommandBindings|CommandBindingAction|CommandBarLayout|CommandBarPolicy|OrderButtonPolicy|CommandModePolicy|MOUSECELL_COMMAND_BAR|cCommandBarDrawer)\\b"` замени на `"\\b(?:CommandBindings|CommandBindingAction|CommandBarLayout|CommandBarPolicy|CommandModePolicy|MOUSECELL_COMMAND_BAR|cCommandBarDrawer)\\b"`;
- маркер `"\\b(?:getCommandKeyTextDrawer|m_commandKeyTextDrawer|commandKeyTextDrawer|m_commandBarDrawer|setRallyPointCommandMode|setCommandState|shouldDrawOrderLabelShadow)\\b"` замени на `"\\b(?:getCommandKeyTextDrawer|m_commandKeyTextDrawer|commandKeyTextDrawer|m_commandBarDrawer|setRallyPointCommandMode|setCommandState)\\b"`;
- из `include` удали строки `"src/drawers/OrderButtonPolicy.hpp"`, `"src/drawers/cOrderDrawer.cpp"` и `"src/drawers/cOrderDrawer.h"`.

### 2. Пересборка JSON

Перед пересборкой скопируй `docs/upstream/port_inventory.json` в `.tmp/port_inventory.round3.json`. Затем:

`PYTHONDONTWRITEBYTECODE=1 /srv/dune/venv/bin/python tools/upstream/port_inventory.py --packs /srv/dune/inputs/packs --out docs/upstream/port_inventory.json`

Ожидаемый итог (ведущий посчитал его своим скриптом по тем же диффам) — сверь скриптом новый JSON с копией `.tmp/port_inventory.round3.json`:
- `features` меняются ровно у шести путей: `src/cGame.h` +`localization`; `src/drawers/OrderButtonPolicy.hpp` −`command-bar` +`localization`; `src/drawers/cOrderDrawer.cpp` и `src/drawers/cOrderDrawer.h` −`command-bar`; `src/gamestates/cMainMenuState.cpp` и `src/utils/common.cpp` −`music-pools`;
- `marker_hits` меняются ровно у шести путей: `src/cGame.h` +`localization`; `src/drawers/OrderButtonPolicy.hpp` −`command-bar` +`localization`; `src/drawers/cOrderDrawer.cpp` −`command-bar`; `src/gamestates/cMainMenuState.cpp` и `src/utils/common.cpp` −`music-pools`; `tests/InteractionRegressionTests.cpp` +`localization`;
- `paths_count`: `localization` 189 → 191, `music-pools` 44 → 42, `command-bar` 41 → 38;
- остальное в JSON не меняется.

Любое другое расхождение — `Q`.

### 3. `docs/upstream/PORT_MAP.md`

Каждая строка внутри блоков ниже вставляется или ищется в карте целиком, как есть; сами строки ограждения блока в карту не входят.

Раздел `### localization`, список «Пути кода и тестов; судьба в апстриме» — добавь две строки, каждую на своё место по порядку сортировки этого списка:

```markdown
- `src/cGame.h` — удалён; код: `src/game/cGame.h@a51b97f:90` (**class cGame**).
- `src/drawers/OrderButtonPolicy.hpp` — не менялся.
```

Раздел `### music-pools` — удали две строки:

```markdown
- `src/gamestates/cMainMenuState.cpp` — изменён.
- `src/utils/common.cpp` — изменён.
```

Раздел `### command-bar` — удали три строки:

```markdown
- `src/drawers/OrderButtonPolicy.hpp` — не менялся.
- `src/drawers/cOrderDrawer.cpp` — изменён.
- `src/drawers/cOrderDrawer.h` — изменён.
```

Раздел `### graphics-modes` — после абзаца, который начинается словами «Тесты форка:», добавь пустую строку и абзац:

```markdown
Обратная зависимость от hd-render: загрузчик передаёт плотность в конструктор Texture — `src/utils/HdUiTextureLoader.cpp@6662b2f:34` (**new Texture**), — а параметр плотности добавлен вместе с hd-render (шаг Б4): `src/include/Texture.hpp@6662b2f:21` (**assetDensity**). Б3 переносить вместе с этим конструктором или после него.
```

Раздел `## Риски переноса` — в конец списка добавь пункт:

```markdown
- Отнесение путей к функциям проверено маркерами в одну сторону: тест 6 ловит недостающих владельцев, но не лишних. Около 85 отнесений у 46 путей кода не подтверждены ни одним маркером, а маркеры renderStrechSprite, buttonWidth, renderTargetStack, TTF_SizeUTF8, m_titleBmp, UNIT_RAIDER и CMAKE_CXX_COMPILER_ID встречаются и в коде апстрима. Исполнитель шага переноса сверяет список путей своей функции с диффом BASE..FORK этих путей.
```

Если в карте есть числа, которые тест 7 сверяет с JSON и которые изменились после пересборки, — приведи их к JSON; других правок текста нет.

### 4. Проверка

`PYTHONDONTWRITEBYTECODE=1 D2TM_PACK_DIR=/srv/dune/inputs/packs /srv/dune/venv/bin/python -m unittest discover -s tools/upstream/tests -v` — все 7 тестов зелёные. Убедись, что в рабочей копии нет новых `__pycache__`; старый `tools/upstream/tests/__pycache__/` перенеси в `.tmp/`.

### 5. Сдача

Блок `## DONE-b0 | время | HEAD <sha>`: журнал по пунктам 1–4 (строка на пункт), вывод сверки ожидаемого итога из пункта 2 (числа из лога), хвост вывода тестов, раздел «Не проверено», `git status --short --untracked-files=all`.
