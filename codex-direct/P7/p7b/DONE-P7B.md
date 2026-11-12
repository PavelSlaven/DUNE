## DONE-P7B | 2026-11-12 10:14:56 UTC | HEAD db8cdba91e09c2e523f7cdc85020fbd4e42b23e2

- Интерфейс переведён по обновлённой таблице: `rows=285 missing=0`. T6: `172 scenes, 0 failures`. Английские литералы сохранены.
- Коммиты не созданы. Изменения данных кампаний и карт в P7B не входили.
- От ведущего нужны ревью, приёмка и создание коммитов по списку ниже.

### Чтение

Прочитаны целиком `Localization.hpp`, исходная `STRINGS-P7B.tsv`, `latin-ru-allowed.tsv`, `cTextWriter.h`, `ui_audit_runtime_support.py`, `ui_audit_language.py`; прочитан заданный фрагмент `test_OptionsMenu.cpp`. Исправленная строка A-P7B-01 и новые строки A-P7B-02 перечитаны, SHA-256 проверены.

Дополнительно прочитан `/srv/dune/tasks/p7b/task.md` для полного брифа помощников. Недостающих норм не выявлено. Навык `caveman` не применялся.

### Журнал хода

Полный журнал: [progress.md](/srv/dune/worktrees/u34/.tmp/p7b/progress.md).

1. Добавлены T6, неизменённая копия списка исключений и переключение языка в указанном тестовом случае.
2. Красный T6 завершился с `exit=1`: `172 scenes, 900 failures`.
3. Применены строки таблицы для `src/gamestates/*`.
4. Применены строки таблицы для `src/context/*` и `src/gameobjects/*`.
5. Применены остальные строки и дополнение A-P7B-02.
6. Создан `check_table.py`; исправлены полное ожидание R1 и перебор всех EN для R4.
7. После A-P7B-02 проверки 1–7 повторены по порядку и пройдены.

Исходная команда `git diff --stat b9f6b0242 HEAD -- <пути таблицы>`: пустой вывод, `exit=0`.

### Красный T6

Последние 30 строк [red-t6.log](/srv/dune/worktrees/u34/.tmp/p7b/red-t6.log), `exit=1`:

```text
ru units-label-trike: untranslated text 'Windtrap'
ru units-label-trooper: untranslated text 'CREDITS'
ru units-label-trooper: untranslated text 'Concrete Slab'
ru units-label-trooper: untranslated text 'HOUSE ATREIDES'
ru units-label-trooper: untranslated text 'OPTIONS'
ru units-label-trooper: untranslated text 'PWR'
ru units-label-trooper: untranslated text 'SPC'
ru units-label-trooper: untranslated text 'Windtrap'
ru units-label-troopers: untranslated text 'CREDITS'
ru units-label-troopers: untranslated text 'Concrete Slab'
ru units-label-troopers: untranslated text 'HOUSE ATREIDES'
ru units-label-troopers: untranslated text 'OPTIONS'
ru units-label-troopers: untranslated text 'PWR'
ru units-label-troopers: untranslated text 'SPC'
ru units-label-troopers: untranslated text 'Windtrap'
ru units-label-unit-fremen-one: untranslated text 'CREDITS'
ru units-label-unit-fremen-one: untranslated text 'Concrete Slab'
ru units-label-unit-fremen-one: untranslated text 'HOUSE ATREIDES'
ru units-label-unit-fremen-one: untranslated text 'OPTIONS'
ru units-label-unit-fremen-one: untranslated text 'PWR'
ru units-label-unit-fremen-one: untranslated text 'SPC'
ru units-label-unit-fremen-one: untranslated text 'Windtrap'
ru units-label-unit-fremen-three: untranslated text 'CREDITS'
ru units-label-unit-fremen-three: untranslated text 'Concrete Slab'
ru units-label-unit-fremen-three: untranslated text 'HOUSE ATREIDES'
ru units-label-unit-fremen-three: untranslated text 'OPTIONS'
ru units-label-unit-fremen-three: untranslated text 'PWR'
ru units-label-unit-fremen-three: untranslated text 'SPC'
ru units-label-unit-fremen-three: untranslated text 'Windtrap'
translation: 172 scenes, 900 failures
```

### Проверки 1–7 после A-P7B-02

**1. Место и сборка.**

```text
Filesystem           1M-blocks  Used Available Use% Mounted on
/dev/mapper/pve-root    112317 99931      6800  94% /
df exit=0
build exit=0
100% tests passed, 0 tests failed out of 337
```

Сборка выполнена с `CCACHE_DISABLE=1`. Логи: [build.log](/srv/dune/worktrees/u34/.tmp/p7b/build.log), [ctest.log](/srv/dune/worktrees/u34/.tmp/out/logs/20261112T094827-4/ctest.log).

**2. Предупреждения по путям таблицы и теста.** Вывод пустой; `exit=1` означает отсутствие совпадений `grep`. Обновлённый `table-paths.txt` содержит 41 путь.

**3. `Imminent crash`.** В `game-dummy.log` и `stdout-dummy.log` совпадений нет; вывод пустой, `exit=1` от `grep`.

**4. Скрипты режима отладки интерфейса.**

```text
ui_audit_list_and_scales.py exit=0
ui_audit_unknown_scene.py exit=0
ui_audit_main_menu_png.py exit=0
ui_audit_tools_run_combo.py exit=0
ui_audit_part2_catalog.py exit=0
ui_audit_part2_scenes.py exit=0
ui_audit_part3a_catalog.py exit=0
ui_audit_part3a_scenes.py exit=0
ui_audit_part3b_catalog.py exit=0
ui_audit_part3b_scenes.py exit=0
ui_audit_frames.py exit=0
ui_audit_part3c_catalog.py exit=0
ui_audit_part3c_scenes.py exit=0
ui_audit_language.py exit=0
ui_audit_translation.py exit=0
translation: 172 scenes, 0 failures
```

Логи сохранены в `.tmp/p7b/run-<скрипт>.log`. Итог T6: [лог](/srv/dune/worktrees/u34/.tmp/p7b/run-ui_audit_translation.py.log).

**5. Модульные тесты инструмента.**

```text
Ran 199 tests in 0.367s

OK
exit=0
```

[run-j.log](/srv/dune/worktrees/u34/.tmp/p7b/run-j.log). Указанные папки `__pycache__` не появились.

**6. Применение таблицы.**

```text
rows=285 missing=0
exit=0
```

[check-table.log](/srv/dune/worktrees/u34/.tmp/p7b/check-table.log).

**7. Git-статус.** `exit=0`. Все изменённые пути входят в обновлённую таблицу или являются `tests/utils/test_OptionsMenu.cpp`. Фрагмент вывода:

```text
 M src/debug/UiAuditAccess.cpp
 M tests/utils/test_OptionsMenu.cpp
?? tests/ui_audit/data/
?? tests/ui_audit/ui_audit_translation.py
```

Полный вывод: [status.log](/srv/dune/worktrees/u34/.tmp/p7b/status.log).

### `git diff --stat`

```text
 src/building/cItemBuilder.cpp                     |   3 +-
 src/context/cInfoContextCreator.cpp               | 119 +++++++++++-----------
 src/controls/mousestates/cMouseNormalState.cpp    |   3 +-
 src/controls/mousestates/cMousePlaceState.cpp     |   3 +-
 src/debug/UiAuditAccess.cpp                       |   3 +-
 src/drawers/CreditsDrawer.cpp                     |   3 +-
 src/drawers/cBuildingListDrawer.cpp               |  19 ++--
 src/drawers/cMouseDrawer.cpp                      |  35 +++----
 src/drawers/cSideBarDrawer.cpp                    |  15 +--
 src/game/cGame_logic.cpp                          |  15 +--
 src/game/cSDLSystem.cpp                           |   3 +-
 src/gameobjects/map/cPreviewMaps.cpp              |  13 +--
 src/gameobjects/mentat/AbstractMentat.cpp         |   7 +-
 src/gameobjects/mentat/AtreidesMentat.cpp         |   5 +-
 src/gameobjects/mentat/BeneMentat.cpp             |   7 +-
 src/gameobjects/mentat/HarkonnenMentat.cpp        |   5 +-
 src/gameobjects/mentat/OrdosMentat.cpp            |   5 +-
 src/gameobjects/mentat/SardaukarMentat.cpp        |   5 +-
 src/gameobjects/players/cPlayer.cpp               |  29 +++---
 src/gameobjects/structures/cAbstractStructure.cpp |   3 +-
 src/gameobjects/structures/cOrderProcesser.cpp    |   7 +-
 src/gameobjects/structures/cWindTrap.cpp          |   3 +-
 src/gameobjects/units/cUnit.cpp                   |   5 +-
 src/gamestates/cChooseHouseState.cpp              |  13 +--
 src/gamestates/cCreditsState.cpp                  |  65 ++++++------
 src/gamestates/cEditorState.cpp                   |   3 +-
 src/gamestates/cGamePlaying.cpp                   |   3 +-
 src/gamestates/cMainMenuState.cpp                 |  19 ++--
 src/gamestates/cNewmapEditorState.cpp             |  21 ++--
 src/gamestates/cOptionsState.cpp                  |  42 ++++----
 src/gamestates/cScoringState.cpp                  |  17 ++--
 src/gamestates/cSelectMissionState.cpp            |  11 +-
 src/gamestates/cSelectYourNextConquestState.cpp   |  17 ++--
 src/gamestates/cSetupSkirmishState.cpp            |  45 ++++----
 src/gamestates/cWinLoseState.cpp                  |   7 +-
 src/gui/GuiConsole/GuiConsoleMessageParser.cpp    |   5 +-
 src/managers/cDrawManager.cpp                     |   3 +-
 src/sidebar/cBuildingListItem.cpp                 |  15 +--
 src/sidebar/cSideBar.cpp                          |   5 +-
 src/utils/ScaleChoices.cpp                        |   3 +-
 tests/utils/test_OptionsMenu.cpp                  |   3 +
 41 files changed, 327 insertions(+), 285 deletions(-)
```

Новые файлы T6 и списка исключений в этот вывод не входят.

### Список для коммитов

1. Тесты: `tests/ui_audit/ui_audit_translation.py`, `tests/ui_audit/data/latin-ru-allowed.tsv`, `tests/utils/test_OptionsMenu.cpp`.

```text
Add UI translation audit for Russian and English

Behavior changes: audit all UI scenes for untranslated text, Russian text in English, and unused allowlist entries; select English for scale label assertions and restore Russian afterward.
```

2. Код: все пути `src/` из приведённого `git diff --stat`, то есть файлы обновлённой таблицы.

```text
Localize code-rendered interface strings

Behavior changes: Russian games use translated interface text, unit and building names, and outcome images; UI audit status text follows the selected language; English text remains unchanged.
```

### Решено исполнителем

- Решено исполнителем: чтение кавычек в TSV → разбирать строки через `split("\t")`; файл: `.tmp/p7b/check_table.py:22`, `csv.DictReader` снял бы кавычки → `split("\t")` сохраняет поле R4 буквально; основание: точная замена выражений R4.
- Решено исполнителем: ожидание R1/R4 в сверке таблицы → R1 проверяется целиком, R4 для каждого EN; файл: `.tmp/p7b/check_table.py:71`, `zip` обрезал бы список EN R4 → каждый EN проверяется отдельно; основание: контракт проверки 6.

Вне рамки задачи: существующие `build_sheets.py` и его тесты выдают `ResourceWarning` и `DeprecationWarning`; модульные тесты проходят. Эти файлы не менялись.

### Рабочие места

Вывод `python3 /srv/dune/tools/task-places.py inventory .tmp/p7b --size`:

```text
path	kind	branch	head_date	size	dirty	untracked	unpushed	worktrees	procs	refs
/srv/dune/worktrees/u34/.tmp/p7b	dir	-	-	186573	-	-	-	-	0	0
```

`.tmp/p7b` — **оставить — логи проверок нужны ревью**. Остальные папки `.tmp/` существовали до задачи; копия `previous-run` не удалялась.