# Задание P5G3V — сцены итогов миссии и редактора карт режима отладки интерфейса (шаг П5г, часть 3в)

Исполнитель: корневая нить Codex `gpt-6.1-sol` `high` и два помощника `gpt-6-luna` `xhigh` (раздел «Организация работы»).

Рабочая копия: `/srv/dune/worktrees/u34`, ветка `codex/p5g3v`, `HEAD` — `c5834615f8fc71789bba7108078a461018cc7d56` (код части 3б шага П5г). Файлы Git LFS в этой рабочей копии — настоящие данные. Временные файлы — в `.tmp/p5g3v/`. Коммитов не делай: коммиты делает ведущий по списку из сдачи.

## Цель

Добавить в каталог режима отладки интерфейса порта пять сцен части 3в — итоги миссии, окно настройки новой карты и редактор карт с каждой из трёх правых панелей, — записи журнала геометрии элементов интерфейса редактора и исключения экрана видеоролика по плану `PLAN-P5G3V` ниже. Готово, когда три приёмочных теста ведущего (два новых скрипта `tests/ui_audit/ui_audit_part3c_catalog.py` и `tests/ui_audit/ui_audit_part3c_scenes.py` и новый текст `tools/ui-audit/tests/test_port_changes.py`; их не меняй) сначала красные на установленной игре без кода этого задания, а после кода зелёные, и остались зелёными сборка (319 тестов), десять скриптов Python частей 1, 2, 3а, 3б и 4 и весь набор `tools/ui-audit/tests`.

## Что уже решено

- Сцену каталога задаёт элемент вектора `g_catalog` в `src/debug/UiAuditScenes.cpp` (`@c583461:282-401`) через `scene(<id>, <group>, <house>, <readiness>, <prepare>, <ready>)`; `state` и `screen` сцены берутся по `group` из таблицы `kGroupScreens` (`src/debug/UiAuditScenes.cpp@c583461:39-70`). Сцена снимается на первом кадре, когда состояние игры два кадра подряд не меняется и `ready` (если задана) вернула `true` (`src/debug/UiAuditCapture.cpp@c583461:466-486`).
- Итоги миссии. `cGame::setState(GAME_SCORING)` каждый раз создаёт новый `cScoringState` (`src/game/cGame_logic.cpp@c583461:944-1060`), а он в конструкторе снимает статистику миссии (`src/gamestates/cScoringState.cpp@c583461:22-40`). Дом игрока статистика берёт в начале миссии, на событии `GAME_EVENT_ABOUT_TO_BEGIN`, которое игра шлёт при переходе в `GAME_PLAYING` (`src/game/cMissionStatsCollector.cpp@c583461:48-65`, `src/game/cGame_logic.cpp@c583461:1180-1200`). Поэтому сцена `scoring` входит в бой так же, как сцены исхода боя (`prepareOutcome<true>`: Дом Атрейдес, область 1), а через три кадра переводит игру в `GAME_SCORING`.
- Окно настройки новой карты. `cGame::setState(GAME_NEW_MAP_EDITOR)` создаёт `cNewMapEditorState`; окно строится в конструкторе (`src/gamestates/cNewmapEditorState.cpp@c583461:48-279`).
- Редактор карт. `cGame::loadMapFromEditor(-1)` переводит игру в `GAME_EDITOR` и загружает в редактор карту, которую перед этим положил `cPreviewMaps::createEmptyMap` (`src/game/cGame_logic.cpp@c583461:1735-1740`, `src/gameobjects/map/cPreviewMaps.cpp@c583461:44-56`) — так делает кнопка `Create map` окна новой карты (`src/gamestates/cNewmapEditorState.cpp@c583461:272-276`, `377`). Правую панель выбирает закрытый метод `cEditorState::setCurrentBar` (панели — закрытые поля `m_topologyBar`, `m_startCellBar`, `m_symmetricBar`, `src/gamestates/cEditorState.h@c583461:74,100-102`); после загрузки выбрана панель рельефа (`src/gamestates/cEditorState.cpp@c583461:103`). Доступ режима к закрытым членам классов игры — через `friend class UiAuditAccess;`, как в `cMouse` и `cSideBarDrawer` (`src/controls/cMouse.h@c583461:29-30`).
- Записи элементов интерфейса. `GuiButton`, `GuiCheckBox`, `GuiLabel`, `GuiSlider` и `GuiWindow` пишут запись `gui` вызовом `auditRecord("<класс>")` в начале `draw()` под `if (uiaudit::isEnabled())`, а `GuiButton` и `GuiCheckBox` — ещё запись `click` вызовом `auditClick(...)`, если элемент включён (`src/gui/GuiButton.cpp@c583461:47-54`, `src/gui/GuiCheckBox.cpp@c583461:40-47`). `GuiBar`, `GuiStateButton`, `GuiValueButton`, `GuiCycleButton` и `GuiTextInput` записей не пишут; они есть только в `cEditorState` и `cNewMapEditorState`. У `GuiStateButton`, `GuiValueButton` и `GuiCycleButton` есть поле `m_enabled` (по умолчанию `true`), у `GuiTextInput` его нет.
- Экран видеоролика `cVideoState` рисует только кадры видео и курсор (`src/gamestates/cVideoState.cpp@c583461:91-99`); сцены для него нет, он и `GAME_VIDEO` получают исключения в `tools/ui-audit/exclusions.tsv`.
- Ожидание теста `test_g_exclusions_text` в `tools/ui-audit/tests/test_port_changes.py` меняет само это задание (шаг 1 плана: новый текст файла от ведущего); правило исполнителя «ожидания существующих тестов не менять» запрещает любые другие правки этого файла и других тестов.
- Приёмочные тесты написал ведущий и проверил на поддельной игре: зелёный прогон по контракту и 35 атак, каждая падает по своей причине; новый текст `test_port_changes.py` при нынешнем `exclusions.tsv` валит только `test_g_exclusions_text`. Файлы тестов — в папке `/srv/dune/tasks/p5g3v-tests/`, их SHA-256 — в шаге 1 плана.

## Прочитать до работы

Прочитай целиком до первого действия, каждый файл отдельным вызовом, пути — от корня рабочей копии:

- `/srv/dune/tasks/p5g3v-tests/ui_audit_part3c_catalog.py` и `/srv/dune/tasks/p5g3v-tests/ui_audit_part3c_scenes.py` — приёмочные скрипты;
- `tests/ui_audit/ui_audit_runtime_support.py`, `tests/ui_audit/ui_audit_part3a_scenes.py` — как скрипты запускают игру и проверяют записи;
- `src/debug/UiAudit.hpp`, `src/debug/UiAuditScenes.cpp`;
- строки 70–90 и 473–486 файла `src/debug/UiAuditAccess.cpp` (вывод `nl -ba src/debug/UiAuditAccess.cpp | sed -n '70,90p;473,486p'`);
- `src/gamestates/cEditorState.h`, строки 60–110 и 411–432 файла `src/gamestates/cEditorState.cpp`;
- `src/gui/GuiBar.cpp`, `src/gui/GuiStateButton.cpp`, `src/gui/GuiValueButton.cpp`, `src/gui/GuiCycleButton.cpp`, `src/gui/GuiTextInput.cpp`;
- `tools/ui-audit/exclusions.tsv`.

Перед командами Git: `export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH`.

## Контракт поведения

Пункты 1–15 контрактов частей 1, 2, 3а и 3б действуют без изменений, кроме одного места пункта 10: после части 3в итоговый список проблем покрытия экранов пуст. Скрипты частей 1, 2, 3а, 3б и 4 в `tests/ui_audit/` остаются зелёными. Игра запускается так же, как в пункте 2 части 1.

17. **Каталог части 3в.** В выводе `--ui-audit-list` у каждой сцены ровно ключи части 1. Среди сцен, у которых `group` — `scoring`, `new-map-editor` или `editor`, нет двух с одним `id`, и эти сцены ровно совпадают по `id` и значениям всех ключей с пятью сценами ниже. У каждой из пяти сцен `game_screen`, `hud` и `hd_only` — `false`, `hover` — `null`; `""` — пустая строка.
    - `scoring`: `group` — `scoring`, `state` — `GAME_SCORING`, `screen` — `cScoringState`, `house` — `atreides`, `readiness` — `FixedFrames(8, no readiness flag)`;
    - `editor-new-map`: `group` — `new-map-editor`, `state` — `GAME_NEW_MAP_EDITOR`, `screen` — `cNewMapEditorState`, `house` — `""`, `readiness` — `StateSettled`;
    - `editor-topology`, `editor-start-cells`, `editor-symmetry`: `group` — `editor`, `state` — `GAME_EDITOR`, `screen` — `cEditorState`, `house` — `""`, `readiness` — `StateSettled`.

    Покрытие экранов — как в пункте 10, но итоговый список проблем пуст. Файл `tools/ui-audit/exclusions.tsv` — прежние двенадцать строк и в конце две строки (поля разделены одной табуляцией, каждая строка кончается переводом строки):
    - `GAME_VIDEO` — `состояние показа видеоролика; его экран cVideoState рисует только кадры видео, элементов интерфейса нет`;
    - `cVideoState` — `экран видеоролика: рисует только кадры видео и курсор, элементов интерфейса нет`.

    Текст файла целиком сверяет тест `test_g_exclusions_text` (`tools/ui-audit/tests/test_port_changes.py`).

18. **Прогон сцены части 3в.** Для каждой из пяти сцен пункта 17 — всё, что пункт 11 требует от сцен с `game_screen` `false`: код выхода 0 не позже чем через 120 секунд, файлы `<id>.png` и `<id>.geometry.jsonl`, PNG и заголовок как там, ключа `map_viewport` в заголовке нет, записи пяти видов с теми же ключами и ограничениями, нет файла `preferences.ini` в папке `XDG_DATA_HOME`.

19. **Записи сцен части 3в.** «Одна запись», «внутри» и «прямоугольник (x, y, w, h)» — как в пункте 12. «Тип» записи `gui` — значение `t`; «имя» записи `click` — значение `name`, записи `area` — значение `n`. «Записи `gui` по типам — ровно: <тип> <число>, …» — у сцены ровно столько записей `gui` каждого названного типа и нет записей `gui` других типов; «записи `click` по именам — ровно …» — так же по именам записей `click`. Числа ниже — для холста 800 × 600.
    - `scoring` (`src/gamestates/cScoringState.cpp@c583461:56-111`): нет записей `gui`, `area`, `label`, `click`; есть записи `text` со значениями `s` `MISSION REPORT`, `Click to continue` и `YOU - Atreides`; ровно одна запись `text`, у которой `s` целиком совпадает с регулярным выражением `Mission time: [0-9]{2}:[0-9]{2}`; есть запись `text`, у которой `s` начинается с `Units built: `.
    - `editor-new-map` (`src/gamestates/cNewmapEditorState.cpp@c583461:68-279`):
      - нет записей `area` и `label`;
      - записи `gui` по типам — ровно: `GuiWindow` 1, `GuiLabel` 7, `GuiTextInput` 4, `GuiCycleButton` 2, `GuiCheckBox` 1, `GuiButton` 2;
      - прямоугольник записи `GuiWindow` — (180, 180, 440, 240): поля окна — 0,3 высоты холста (`src/gamestates/cNewmapEditorState.cpp@c583461:70-80`);
      - записи `click` по именам — ровно: `GuiButton:Return to menu` 1, `GuiButton:Create map` 1, `GuiTextInput` 4, `GuiCycleButton` 2. Записи `click` `GuiCheckBox` нет: флажок `Random:` выключен, потому что оба размера по умолчанию — 16, а случайной карте нужно не меньше 64 (`src/gamestates/cNewmapEditorState.cpp@c583461:319-328`);
      - есть записи `text` со значениями `s` `Map editor configuration`, `Name your map:`, `Name of author:`, `Description:`, `Width size:`, `Height size:`, `Random:`, `Return to menu`, `Create map`.
    - `editor-topology`, `editor-start-cells`, `editor-symmetry` (`src/gamestates/cEditorState.cpp@c583461:81-409`). `<n>` — число кнопок правой панели: 6 у `editor-topology`, 5 у `editor-start-cells`, 8 у `editor-symmetry`.
      - нет записей `label`; записи `area` — ровно одна: `editor-map` с прямоугольником (0, 48, 752, 552);
      - записи `gui` по типам — ровно: `GuiBar` 2, `GuiButton` 1, `GuiStateButton` 3 + `<n>`, у `editor-topology` ещё `GuiValueButton` 1;
      - прямоугольники двух записей `GuiBar` — (0, 0, 800, 48) (верхняя панель) и (752, 48, 48, 552) (правая панель);
      - внутри прямоугольника верхней панели — ровно 3 записи `GuiStateButton`, внутри прямоугольника правой — ровно `<n>`; каждая запись `GuiValueButton` — внутри правой панели; запись `GuiButton` — внутри верхней панели;
      - записи `click` по именам — ровно: `GuiStateButton` 3 + `<n>`, `GuiButton:` 1 (кнопка сохранения без подписи), у `editor-topology` ещё `GuiValueButton` 1.
    - `editor-new-map` и три сцены редактора: «тип» записи `click` — часть её имени до первого символа `:` (всё имя, если `:` в нём нет). Для каждого типа `T` записей `click` сцены прямоугольники записей `click` типа `T` и прямоугольники записей `gui` с типом `T` совпадают как наборы с повторами: у каждой записи `click` — своя запись `gui` с тем же прямоугольником.

## PLAN-P5G3V

| шаг | файлы | что сделать | кто |
|---|---|---|---|
| 1 | `tests/ui_audit/ui_audit_part3c_catalog.py`, `tests/ui_audit/ui_audit_part3c_scenes.py`, `tools/ui-audit/tests/test_port_changes.py` | `cp /srv/dune/tasks/p5g3v-tests/ui_audit_part3c_catalog.py /srv/dune/tasks/p5g3v-tests/ui_audit_part3c_scenes.py tests/ui_audit/ && cp /srv/dune/tasks/p5g3v-tests/test_port_changes.py tools/ui-audit/tests/test_port_changes.py`; затем `sha256sum tests/ui_audit/ui_audit_part3c_catalog.py tests/ui_audit/ui_audit_part3c_scenes.py tools/ui-audit/tests/test_port_changes.py` — три суммы раздела «Суммы тестов» ниже. | помощник A |
| 2 | — | Красные прогоны H, I и K раздела «Красные прогоны» ниже. | помощник D |
| 3 | `src/gui/GuiBar.cpp`, `src/gui/GuiStateButton.cpp`, `src/gui/GuiValueButton.cpp`, `src/gui/GuiCycleButton.cpp`, `src/gui/GuiTextInput.cpp` | Правки (а)–(д) раздела «Код» ниже, каждая дословно. | помощник A |
| 4 | `src/gamestates/cEditorState.h`, `src/gamestates/cEditorState.cpp` | Правки (е) и (ж) раздела «Код». | помощник A |
| 5 | `tools/ui-audit/exclusions.tsv` | Правка (з) раздела «Код». | помощник A |
| 6 | `src/debug/UiAudit.hpp`, `src/debug/UiAuditAccess.cpp` | Правки (и) и (к) раздела «Код». | помощник A |
| 7 | `src/debug/UiAuditScenes.cpp` | Правки (л), (м) и (н) раздела «Код». | помощник A |
| 8 | — | Проверки раздела «Проверки» по порядку. | помощник D |

В каждом файле шагов 3–7 других правок, кроме названных, нет.

## Суммы тестов

```text
fb13c37bf05d6c0f9345d30a85765a74bdd9e170fb3b27bad8db509a83b9d30e  tests/ui_audit/ui_audit_part3c_catalog.py
24626f244f50e58a0f24205af7b0dfdc7a435442a5abe52d8ecb5d12899bf9ac  tests/ui_audit/ui_audit_part3c_scenes.py
0247017e0c44e019ebc29c99d78b8339054793a7cee8fb8ea8c95cbfc1474370  tools/ui-audit/tests/test_port_changes.py
```

## Красные прогоны

Все команды — из корня рабочей копии `/srv/dune/worktrees/u34`, до правок шагов 3–7; установленная игра `.tmp/out/run/bin/d2tm` — сборка без кода этого задания.

1. **Прогон H** — `mkdir -p .tmp/p5g3v && LD_LIBRARY_PATH=$PWD/.tmp/deps/prefix/lib python3 -B tests/ui_audit/ui_audit_part3c_catalog.py --run-dir .tmp/out/run/bin > .tmp/p5g3v/red-h.log 2>&1; echo exit=$?`. Ожидается: `exit=1`; первая строка лога ровно `Part 3c scenes differ: missing ['editor-new-map', 'editor-start-cells', 'editor-symmetry', 'editor-topology', 'scoring']; extra []`.
2. **Прогон I** — `LD_LIBRARY_PATH=$PWD/.tmp/deps/prefix/lib timeout 1800 python3 -B tests/ui_audit/ui_audit_part3c_scenes.py --run-dir .tmp/out/run/bin > .tmp/p5g3v/red-i.log 2>&1; echo exit=$?`. Ожидается: `exit=1`; `grep -c 'game exited with 2' .tmp/p5g3v/red-i.log` выводит `5`; `grep -c 'ui-audit: unknown scene' .tmp/p5g3v/red-i.log` выводит `5`.
3. **Прогон K** — `python3 -B tools/ui-audit/tests/test_port_changes.py > .tmp/p5g3v/red-k.log 2>&1; echo exit=$?`. Ожидается: `exit=1`; `grep -c '^FAIL: ' .tmp/p5g3v/red-k.log` выводит `1`, и эта строка начинается с `FAIL: test_g_exclusions_text`; `grep -c '^ERROR: ' .tmp/p5g3v/red-k.log` выводит `0`; последняя строка лога — `FAILED (failures=1)`.
4. Затем `rm -r tests/ui_audit/__pycache__ tools/ui-audit/__pycache__ tools/ui-audit/tests/__pycache__` для тех из этих папок, что появились.

Другой результат красного прогона — блок `## Q-P5G3V-NN` с выводом и стоп.

## Код

Отступы — четыре пробела на уровень, как в файлах; текст в блоках кода ниже — дословный, с его отступами. «Первые строки тела функции» — строки сразу после открывающей `{` функции, перед её прежней первой строкой.

(а) `src/gui/GuiBar.cpp`. Сразу после строки `#include "gui/GuiBar.h"` — строка `#include "debug/UiAudit.hpp"`. Первые строки тела функции `GuiBar::draw() const`:

```cpp
    if (uiaudit::isEnabled()) {
        auditRecord("GuiBar");
    }
```

(б) `src/gui/GuiStateButton.cpp`. Сразу после строки `#include "gui/GuiStateButton.h"` — строка `#include "debug/UiAudit.hpp"`. Первые строки тела функции `GuiStateButton::draw() const`:

```cpp
    if (uiaudit::isEnabled()) {
        auditRecord("GuiStateButton");
        if (m_enabled) {
            auditClick("GuiStateButton");
        }
    }
```

(в) `src/gui/GuiValueButton.cpp`. Сразу после строки `#include "gui/GuiValueButton.h"` — строка `#include "debug/UiAudit.hpp"`. Первые строки тела функции `GuiValueButton::draw() const`:

```cpp
    if (uiaudit::isEnabled()) {
        auditRecord("GuiValueButton");
        if (m_enabled) {
            auditClick("GuiValueButton");
        }
    }
```

(г) `src/gui/GuiCycleButton.cpp`. Сразу после строки `#include "gui/GuiCycleButton.h"` — строка `#include "debug/UiAudit.hpp"`. Первые строки тела функции `GuiCycleButton::draw() const`:

```cpp
    if (uiaudit::isEnabled()) {
        auditRecord("GuiCycleButton");
        if (m_enabled) {
            auditClick("GuiCycleButton");
        }
    }
```

(д) `src/gui/GuiTextInput.cpp`. Сразу после строки `#include "gui/GuiTextInput.h"` — строка `#include "debug/UiAudit.hpp"`. Первые строки тела функции `GuiTextInput::draw() const`:

```cpp
    if (uiaudit::isEnabled()) {
        auditRecord("GuiTextInput");
        auditClick("GuiTextInput");
    }
```

(е) `src/gamestates/cEditorState.h`. Сразу после строки `class cEditorState : public cGameState {` — две строки: `    friend class UiAuditAccess;` и пустая строка (так же, как в `src/controls/cMouse.h`).

(ж) `src/gamestates/cEditorState.cpp`. Сразу после строки `#include "gamestates/cEditorState.h"` — строка `#include "debug/UiAudit.hpp"`. Первые строки тела функции `cEditorState::draw() const`:

```cpp
    if (uiaudit::isEnabled()) {
        uiaudit::recordArea("editor-map", mapSizeArea.getX(), mapSizeArea.getY(), mapSizeArea.getWidth(),
                            mapSizeArea.getHeight());
    }
```

(з) `tools/ui-audit/exclusions.tsv`. В конец файла, после строки `cCreatorState` — две строки ровно в таком виде (поле имени, одна табуляция, причина; каждая строка кончается переводом строки):

```text
GAME_VIDEO	состояние показа видеоролика; его экран cVideoState рисует только кадры видео, элементов интерфейса нет
cVideoState	экран видеоролика: рисует только кадры видео и курсор, элементов интерфейса нет
```

Между именем и причиной — один символ табуляции (код 9), не пробелы. Проверка: `tail -2 tools/ui-audit/exclusions.tsv | cut -f1` выводит `GAME_VIDEO` и `cVideoState`.

(и) `src/debug/UiAudit.hpp`. В классе `UiAuditAccess` сразу после строки `    static bool enterPlaying(cGame &game, int house, int region);` — строка:

```cpp
    static bool openEditor(cGame &game, int bar);
```

(к) `src/debug/UiAuditAccess.cpp`. Сразу после строки `#include "gamestates/cCreditsState.h"` — две строки:

```cpp
#include "gamestates/cCreatorState.h"
#include "gamestates/cEditorState.h"
```

Сразу после строки `#include "gameobjects/map/cMapCamera.h"` — строка `#include "gameobjects/map/cPreviewMaps.h"`. Сразу после закрывающей `}` функции `UiAuditAccess::enterPlaying` — пустая строка и функция:

```cpp
bool UiAuditAccess::openEditor(cGame &currentGame, int bar)
{
    // 64 cells plus the one-cell border on each side, as the new map window adds it
    const int side = 64 + 2;
    currentGame.m_gameObjectsContext->getPreviewMaps()->createEmptyMap("UI audit", "UI audit", "UI audit", side, side);
    currentGame.loadMapFromEditor(-1);
    auto *editor = dynamic_cast<cEditorState *>(currentGame.m_creatorState->getState(eGameState::EDITOR));
    GuiBar *bars[] = {editor->m_topologyBar.get(), editor->m_startCellBar.get(), editor->m_symmetricBar.get()};
    editor->setCurrentBar(bars[bar]);
    return currentGame.m_state == GAME_EDITOR;
}
```

(л) `src/debug/UiAuditScenes.cpp`, таблица `kGroupScreens`. Сразу после строки `    {"options-game", "GAME_OPTIONS", "cOptionsState"},` — три строки:

```cpp
    {"scoring", "GAME_SCORING", "cScoringState"},
    {"new-map-editor", "GAME_NEW_MAP_EDITOR", "cNewMapEditorState"},
    {"editor", "GAME_EDITOR", "cEditorState"},
```

(м) `src/debug/UiAuditScenes.cpp`, функции. Сразу после закрывающей `}` шаблона функции `readyOutcome` — пустая строка и три функции, разделённые пустой строкой:

```cpp
bool readyScoring(cGame &game)
{
    if (g_step == 0) {
        if (!pause(3)) {
            return false;
        }
        UiAuditAccess::setState(game, GAME_SCORING);
        g_step = 1;
        return false;
    }
    return pause(3);
}

bool prepareNewMapEditor(cGame &game)
{
    UiAuditAccess::setState(game, GAME_NEW_MAP_EDITOR);
    return true;
}

template <int Bar>
bool prepareEditor(cGame &game)
{
    return UiAuditAccess::openEditor(game, Bar);
}
```

(н) `src/debug/UiAuditScenes.cpp`, вектор `g_catalog`. Сразу после двух строк сцены `outcome-lose` (вторая из них — `                     readyOutcome<false>), "GAME_LOSING", "cWinLoseState"),`) — пять строк:

```cpp
    scene("scoring", "scoring", "atreides", "FixedFrames(8, no readiness flag)", prepareOutcome<true>, readyScoring),
    scene("editor-new-map", "new-map-editor", "", "StateSettled", prepareNewMapEditor),
    scene("editor-topology", "editor", "", "StateSettled", prepareEditor<0>),
    scene("editor-start-cells", "editor", "", "StateSettled", prepareEditor<1>),
    scene("editor-symmetry", "editor", "", "StateSettled", prepareEditor<2>),
```

Номер панели в `prepareEditor<N>` и `openEditor` — индекс в массиве `bars` правки (к): 0 — рельеф, 1 — стартовые клетки, 2 — симметрия.

## Проверки

Все команды — из корня рабочей копии `/srv/dune/worktrees/u34`.

1. `sha256sum tests/ui_audit/ui_audit_part3c_catalog.py tests/ui_audit/ui_audit_part3c_scenes.py tools/ui-audit/tests/test_port_changes.py` — три суммы раздела «Суммы тестов».
2. `df -m /srv` — в столбце `Available` не меньше 5000, иначе блок `## Q-P5G3V-01` и стоп. Сборка: `CCACHE_DISABLE=1 DUNE_DEPS_DIR=$PWD/.tmp/deps DUNE_OUT_DIR=$PWD/.tmp/out bash tools/upstream/build_upstream_linux.sh d06f2fcd2a347182c3774fb96e9a85570405c489 > .tmp/p5g3v/build.log 2>&1; echo exit=$?` — `exit=0`; итоговая строка `ctest.log` последней папки логов `.tmp/out/logs/` — `100% tests passed, 0 tests failed out of 319`. `CCACHE_DISABLE=1` обязателен: `ccache` пишет в `/root/.cache`, который песочница нити держит только для чтения.
3. `grep -n 'warning:' .tmp/out/logs/<последняя папка>/full.log | grep -E 'src/(debug|gui)/|src/gamestates/cEditorState'` — пустой вывод.
4. В `game-dummy.log` и `stdout-dummy.log` последней папки логов нет строки `Imminent crash`; файл `.tmp/out/xdg/D2TM/Dune II - The Maker/preferences.ini` есть.
5. Для каждого скрипта `<скрипт>` из `ui_audit_list_and_scales.py`, `ui_audit_unknown_scene.py`, `ui_audit_main_menu_png.py`, `ui_audit_tools_run_combo.py`, `ui_audit_part2_catalog.py`, `ui_audit_part2_scenes.py`, `ui_audit_part3a_catalog.py`, `ui_audit_part3a_scenes.py`, `ui_audit_part3b_catalog.py`, `ui_audit_part3b_scenes.py`, `ui_audit_part3c_catalog.py`, `ui_audit_part3c_scenes.py`: `LD_LIBRARY_PATH=$PWD/.tmp/deps/prefix/lib timeout 1800 python3 -B tests/ui_audit/<скрипт> --run-dir .tmp/out/run/bin > .tmp/p5g3v/run-<скрипт>.log 2>&1; echo exit=$?` — у каждого `exit=0`.
6. `mkdir -p .tmp/p5g3v/tmp && (cd tools/ui-audit && TMPDIR=$PWD/../../.tmp/p5g3v/tmp python3 -B -m unittest discover -s tests) > .tmp/p5g3v/run-j.log 2>&1; echo exit=$?` — `exit=0`, последняя строка `.tmp/p5g3v/run-j.log` — `OK`. После проверок 5 и 6 — `rm -r tests/ui_audit/__pycache__ tools/ui-audit/__pycache__ tools/ui-audit/tests/__pycache__` для тех из этих папок, что появились.
7. Снимки для ведущего: для каждой сцены `<id>` из `scoring`, `editor-new-map`, `editor-topology`, `editor-start-cells`, `editor-symmetry` по очереди: `(cd .tmp/out/run/bin && SDL_VIDEODRIVER=dummy SDL_RENDER_DRIVER=software SDL_AUDIODRIVER=dummy XDG_DATA_HOME=/srv/dune/worktrees/u34/.tmp/p5g3v/xdg LD_LIBRARY_PATH=/srv/dune/worktrees/u34/.tmp/deps/prefix/lib timeout 120 ./d2tm -windowed -screenWidth 1024 -screenHeight 768 --ui-audit-scene <id> --ui-audit-out /srv/dune/worktrees/u34/.tmp/p5g3v/png) > .tmp/p5g3v/png-<id>.log 2>&1; echo exit=$?` — `exit=0`; затем `ls .tmp/p5g3v/png` — десять файлов `<id>.png` и `<id>.geometry.jsonl`.
8. Сверки `grep` (в скобках — ожидаемый вывод):
   - `grep -l 'debug/UiAudit.hpp' src/gui/GuiBar.cpp src/gui/GuiStateButton.cpp src/gui/GuiValueButton.cpp src/gui/GuiCycleButton.cpp src/gui/GuiTextInput.cpp src/gamestates/cEditorState.cpp | wc -l` (6);
   - `grep -c 'friend class UiAuditAccess;' src/gamestates/cEditorState.h` (1);
   - `grep -c 'openEditor' src/debug/UiAudit.hpp src/debug/UiAuditAccess.cpp src/debug/UiAuditScenes.cpp` (`src/debug/UiAudit.hpp:1`, `src/debug/UiAuditAccess.cpp:1`, `src/debug/UiAuditScenes.cpp:1`);
   - `grep -c '"editor-map"' src/gamestates/cEditorState.cpp` (1).
9. `git -c lfs.storage=$PWD/.tmp/p5g3v/lfs status --short` — ровно четырнадцать строк: ` M src/debug/UiAudit.hpp`, ` M src/debug/UiAuditAccess.cpp`, ` M src/debug/UiAuditScenes.cpp`, ` M src/gamestates/cEditorState.cpp`, ` M src/gamestates/cEditorState.h`, ` M src/gui/GuiBar.cpp`, ` M src/gui/GuiCycleButton.cpp`, ` M src/gui/GuiStateButton.cpp`, ` M src/gui/GuiTextInput.cpp`, ` M src/gui/GuiValueButton.cpp`, ` M tools/ui-audit/exclusions.tsv`, ` M tools/ui-audit/tests/test_port_changes.py`, `?? tests/ui_audit/ui_audit_part3c_catalog.py`, `?? tests/ui_audit/ui_audit_part3c_scenes.py`.

Расхождение в любой проверке, которое не убирается правкой в рамке правок по плану, — блок `## Q-P5G3V-NN` с выводом и стоп. Три файла тестов шага 1 и скрипты частей 1–4 не подгоняй и не меняй.

## Сдача

Последнее сообщение — блок `## DONE-P5G3V | <время UTC из date -u> | HEAD <sha>` по форме из правил ниже. В нём:

- журнал хода (`.tmp/p5g3v/progress.md`): строка на каждый шаг плана;
- вывод красных прогонов шага 2 (не больше 20 строк на прогон) и вывод каждой проверки 1–9 с кодами выхода (не больше 40 строк на проверку);
- `git diff --stat` и список для коммита: один пункт — все файлы рамки правок, сообщение на английском о сценах итогов миссии и редактора карт режима отладки интерфейса, записях элементов интерфейса редактора и исключениях экрана видеоролика, последняя строка — `Behavior changes: …` со списком;
- раздел «Решено исполнителем» — каждая такая строка по правилам исполнителя ниже;
- раздел «Рабочие места»: вывод `python3 /srv/dune/tools/task-places.py inventory .tmp/p5g3v --size`; у `.tmp/p5g3v` пометка `оставить — логи проверок и снимки нужны ревью`. Остальные папки в `.tmp/` созданы до этой задачи и в раздел не входят; копию `previous-run` в папке логов сборки не удаляй — её удаляет ведущий после приёмки.

Числа в сдаче — только из вывода команд.

## Организация работы

- **Порядок:** `create_goal` (первым действием, по правилам исполнителя ниже; objective — текст раздела «Цель» дословно) → раздел «Прочитать до работы» → шаг 1 (помощник A) → шаг 2 (помощник D) → шаги 3–7 (помощник A) → шаг 8 (помощник D) → сдача и стоп.
- **Параллельно:** нет: каждый шаг опирается на предыдущий (красные прогоны — до кода, проверки — после кода).
- **Помощники:** два, `gpt-6-luna` `xhigh`, без вложенных. В бриф каждого дословно входят разделы «Что уже решено», «Контракт поведения», его строки таблицы `PLAN-P5G3V` (помощнику A — строки шагов 1 и 3–7, раздел «Суммы тестов» и раздел «Код»; помощнику D — строки шагов 2 и 8, разделы «Красные прогоны» и «Проверки»), абзац «Комментарии в коде» и запрет править файлы вне своих строк плана и `.tmp/p5g3v/`. Корневая нить сама не правит код, не запускает сборку и проверки: механику — правки, сборку, проверки, выписку логов — делают только помощники; корневая нить читает раздел «Прочитать до работы», раздаёт шаги, разбирает ошибки сборки и проверок по выводу помощников, отвечает на вопросы помощников в рамке плана и сдаёт. Ошибку сборки в файле помощника A корневая нить отдаёт помощнику A.
- **Остановки:** только на `## DONE-P5G3V` и на блоках `## Q-P5G3V-NN`. Команда оболочки дважды подряд не завершилась (нет кода выхода) — блок `## Q-P5G3V-NN` и стоп.
- **Рамка правок:** десять файлов шагов 3–7, три файла тестов шага 1 и папка `.tmp/p5g3v/`. Понадобился другой файл — блок `## Q-P5G3V-NN` и стоп. Сборка пишет в `.tmp/out/` и `.tmp/deps/`, игра — в `.tmp/out/run/bin/`, `.tmp/p5g3v/` и временные папки скриптов; это не правка.

Не отступай от плана, не переусложняй.

## Комментарии в коде

Категорически запрещено писать комментарий по принципу «полезен, если верен и относится к делу». По умолчанию комментария нет; он должен доказать право на существование: только неочевидное «почему» — инвариант, причина обхода, ссылка на внешнее ограничение. Пересказ кода, планы и история — нет. Внутренние номера находок, планов и решений (`F7`, `A-11b`, `D88`) в комментарий не писать: суть словами. Субагентам и исполнителям этот абзац передавать в бриф дословно.

<!-- team-process:executor-rules sha256=2d86ef51aef14ab0cfe146d96e8768450f1161cc5c1f859bbf13ba4b7ae869e7 -->
## Обязательно: правила исполнителя

- Ожидания существующих тестов не менять; единственное исключение и порядок вопроса — раздел «Вопросы и остановки». Новый тест добавлять можно. Тест падает из-за программы — чинить программу, а не обходить ошибку в тесте.
- Не утверждать прогон без лога. Не выдумывать файлы, API, цитаты, результаты. Непроверенное пометить «не проверено». Уверенность данных не выше источника. Отметку о выполнении в списке задач ставить только со следом проверки — тестом или строкой вывода.
- Один круг самоаудита на сдачу; повторный обход того же — `Q`.
- Без фоновых команд: после остановки исполнителя никто его не разбудит. Длинные прогоны — в переднем плане, с таймаутом до 30 минут.
- Git по договорённости с ревьюером. Например: Codex по договорённости не пишет в git — ветку и коммиты делает ревьюер после ревью; Claude и Cursor коммитят сами; никто не делает `push`, `rebase`, `reset --hard`, `clean`, `gh … create/edit/merge`. Пуш — через ревьюера.
- Добавлять в коммит только свои файлы по именам, без `git add -A`; перед коммитом смотреть `git diff --cached --summary` и `--stat`; всё, что не относится к пункту, — отдельным коммитом.
- Режимы файлов (chmod от `npm ci`) и машинные пути в коммит не попадают.
- Общая машина: чужие сервисы и контейнеры не трогать, секреты не печатать, писать только в отведённую папку, тесты с БД — только через выданный слот. Временные файлы — только в отведённой временной папке, в репозиторий и в корень рабочей копии ничего временного не класть. Крупные артефакты (сборки, дампы, модели) — в одном экземпляре. Удалять что-либо вне своей временной папки — только по правилу «Уборка»; чужое, общее и постоянное — не удаляешь. Останавливать только свои процессы — по PID или группе, записанным при запуске; `pkill` и `killall` по имени запрещены: тем же именем на общей машине идут чужие прогоны.
- Папка задачи. Всё, что создаёшь вне рабочей копии (клоны, деревья сборки, копии для стендов, временные файлы), клади только в папку задачи из задания; временные файлы — в её `tmp`, системные `/tmp` и `%TEMP%` не используй. Новую полную копию исходников не создавай, если можно обойтись `git worktree add` от имеющегося клона. Нужно место вне папки задачи — `Q`. В `DONE` — раздел «Рабочие места»: каждый созданный путь, его размер (`du -sh`) и что это — доказательство (на него ссылаются DONE, PR или журнал) или промежуточное. Объекты сборки, ненужные для повторной проверки, удаляешь только по правилу «Уборка»; до `CLEAN-OK` пути задачи не удаляешь.
- Уборка (владелец). В DONE — раздел «Рабочие места»: каждый путь из вывода `task-places.py inventory` и каждый путь вне коммитов ветки, созданный задачей и не попавший в вывод. У каждого — размер, назначение и пометка: `удалить` или `оставить — <почему>`; доказательства — только `оставить`. Удаляешь только после ответа ведущего-ревьюера `CLEAN-OK-<id задачи>` и только пути из его перечня. Молчание и `CLEAN-CHANGES-<id задачи>` — не удаляешь. Порядок: `task-places.py remove <пути> --refs <живые файлы из задания> --archive <архив из задания> --dry-run`; если в выводе есть путь не из перечня `CLEAN-OK` — `Q` и стоп; иначе тот же вызов без `--dry-run`. Итог (удалено, освобождено, архив) — последним сообщением `## CLEAN-DONE-<id задачи>`. Свою `tmp` в папке задачи удаляешь сам, без `CLEAN-OK`. Чужое, общее и постоянное не удаляешь.
- Механику — субагентам младших моделей и скриптам; сам — суждение и итоговая сверка.
- **Чтение (владелец).** До разведки и работы прочитать целиком всё из раздела задания «Прочитать до работы». В разведке `RECON`, а без неё в первой сдаче, — раздел «Чтение»: что прочитано из списка, и «не хватает в задании» — правило, норма или контракт, на которые опираются действия задания, но которых нет в списке (ссылка в задании или в прочитанном документе); их прочитать до этой сдачи и назвать с причиной. Каждый файл — отдельным вызовом; вывод обрезан (`Warning: truncated output`) — дочитать частями до конца. Ведущий проверяет чтение скриптом по журналу: обрезанный вывод — не чтение.
- Задание даёт цель нити — первым действием вызвать `create_goal` с objective из задания дословно; после каждого сжатия контекста и перед каждым подпунктом читать файл цели и работать по нему; `update_goal` со статусом `complete` — только после сообщения ведущего о приёмке; помощникам цель не ставить.

## Вопросы и остановки

Каждое препятствие сверяй в таком порядке:

1. Подходит под список «`Q` и стоп» — `Q` и стоп, даже если оно подходит и под список «Без вопроса».
2. Иначе подходит под список «Без вопроса» — решай сам и работай дальше.
3. Иначе: без ответа идущий подпункт выполнить нельзя — `Q` и стоп; можно — неблокирующий вопрос: запиши его в сдачу и работай дальше по списку, не простаивай.

`Q` в любом другом пункте этих правил — тоже «`Q` и стоп».

**`Q` и стоп.**
- ответ требует правки вне рамки правок, правки промптов, норм, governance, контрактов или замороженных тестов (файл, assert, смысл проверки);
- удаление данных, сеть или установка пакетов;
- смена цели, рамки или критерия готовности; новый механизм; решение по продукту;
- дословное исполнение задания оставляет обход цели, отвергает честный случай или спорит с целью — `Q` до работы, а не пометка в DONE;
- конфликт плана с кодом, нормой или данными;
- у технического вопроса нет рекомендации;
- исправление своего инструмента задевает замороженные файлы, assert или production-код, либо тот же инструмент ломается третий раз.

**Без вопроса (владелец).** В журнал хода и в сдачу — строка «Решено исполнителем: <что> → <решение>; файл:строка, было → стало; основание: <требование задания, вывод команды или проверка>».
- технический вопрос с твоей рекомендацией — выбор способа внутри рамки правок и критерия готовности задания: имя и место своего файла, порядок своих действий внутри одного шага плана, толкование формата вывода, которое не меняет результат проверки;
- подготовка данных своего теста, в том числе способом, уже применённым в том же файле;
- ошибка компиляции или времени жизни в тестовом помощнике, если проверки не меняются;
- ожидание существующего незамороженного теста, которое прямо противоречит требованию задания;
- известный обход среды, названный в задании;
- ошибка своего инструмента (скрипт сверки, подготовка запроса теста, сбор логов): исправь и повтори в том же прогоне, сохранив вывод каждого запуска; «один круг самоаудита» относится к сдаче, а не к своим инструментам.

**Вопросы — одним блоком.** До первой остановки пройди этап до первого действия, меняющего файлы, и задай все вопросы этапа одним блоком `Q`.

## Объём и порядок работы

- Делать продукт, а не доказательства. Отчётных артефактов сверх формы сдачи и журнала хода не заводить: квитанций, «официальных прогонов», привязки к хэшам сборки, новых отчётных документов. Доказательство — коммит, тест и строка вывода прогона. Журнал хода — один файл, по строке на законченный подпункт (что сделано, коммит, тест); отдельных документов на подпункт не заводить. Причина: исполнитель уже тратил около трёх четвертей работы на квитанции, журналы и «официальные прогоны» вместо продукта.
- Не заводить себе правил, которые останавливают работу (например, полный прогон после каждой правки): по ходу — точечные тесты, полный прогон — полная команда проверки, названная в задании (другие наборы проверок репозитория не добавлять), после последней правки (упал — исправить причину и повторить).
- Не добавлять цели и результаты, которых нет в задании (примеры из практики: установщики, аудиты лицензий, подготовка к распространению); шаги реализации требуемого результата допускаются. Новый результат — только с согласия ведущего или владельца; найденное вне задачи — перечислить в сдаче.
- **Обязательно: простейшее решение, которое полностью закрывает задачу.** Не предусматривать сценарии, которых нет ни в задании, ни в данных продукта; не строить «на будущее» защиту, обобщения, настройки и проверки случаев, невозможность которых следует из контракта продукта (отсутствие случая в выборке данных невозможность не доказывает). Сомнение, нужен ли случай, — неблокирующий вопрос в сдаче, а не код. Причина: исполнитель склонен переусложнять и тратить токены на непрошенное вместо функциональности.
- План и сдача — буквальным языком: каждое утверждение допускает одно прочтение. Вместо «по возможности», «при необходимости», «и т. п.», «аналогично» — точный список, условие или число; вместо «это», «там», «такой» без ясного предмета — название предмета.
- План пишет ведущий (владелец); исполнитель планов не пишет. Не хватает фактов — сдать разведку `RECON` (факты файл:строка, команды и выводы) без развилок, предложений, рекомендаций, плана и правок; план ведущего выполнять дословно и в его порядке; конфликт плана с кодом, нормой или данными — `Q` и стоп.
- Задачи — строго по порядку списка.
- Замечания ревьюера выполнять до следующей задачи. Пришло новое замечание посреди работы — зафиксировать начатое (коммитом, если исполнитель коммитит; иначе строкой журнала хода: что сделано, какие файлы изменены) и перейти к замечанию.
- Не раздувать задачу: тестировать путь пользователя и найденные ошибки, без перебора всех сочетаний.

## Коммиты

- Если исполнитель коммитит по договорённости — коммит на каждый законченный подпункт; от первой правки после последнего коммита до следующего коммита — не дольше 2 часов. Если не коммитит — после законченного подпункта строка журнала хода со списком изменений поведения; DONE — один на задачу, после REVIEW — новый DONE.
- Если исполнитель коммитит — незаконченное хранить в своей ветке WIP-коммитом, а не патчами во временной папке. Голый `git stash` не использовать: список stash общий для всех рабочих копий и сессий.
- Перенос и переформатирование кода — отдельным коммитом, изменение поведения — следующим. «Без изменения поведения» писать, только если это правда.
- Последняя строка сообщения коммита — `Behavior changes: …` со списком или `Behavior changes: none`. Называть и мелочи: запасной вариант, удалённое поле, удалённую настройку в тесте, изменённый предел.
- Заголовок не преувеличивает: «finish», «complete» — только если пункт закрыт целиком; остатки назвать в теле.

## Тесты

- Тест проходит путь пользователя через тот вход продукта, которым пользуется пользователь в сценарии: для интерфейса — события мыши и клавиатуры, для API — вызов API. Тестируемый код не подменять заглушками.
- Тест проверяет поведение, а не совпадение хэша или вывода с прошлой сборкой. Изображения сравнивать с эталоном с допуском из задания, а если в задании его нет — из действующего эталонного теста или конфигурации сравнения; ни один источник допуск не задаёт — `Q`.
- Асинхронный результат ждать по нему самому (нужное значение, запись, пиксель), а не по косвенному флагу.
- Нестабильный тест разбирать сразу, с логом и санитайзером, если он уже настроен в проекте. «Не воспроизвелось» проблему не закрывает: исполнитель перечисляет её в сдаче с логом, issue заводит ведущий.
- Тесты пишут только в свои временные папки; общее состояние (синглтоны, кэши) сбрасывать перед каждым тестом.
- Общие помощники тестов и константы — в одном месте, не копировать по файлам.
- Сливать в целевую ветку только ветку с зелёным CI на её последнем коммите; после слияния проверить CI целевой ветки и красной её не оставлять.

## Замеры

- «Проверено на <данных>» — только с цифрами: команда замера и строка её вывода (что измерено и сколько вышло, например «страница 244, 126 нажатий, P95 18 мс»); отдельного отчёта о замере не заводить.
- Бюджет скорости задан в задании, правилах проекта или контракте продукта — замерить фактическое значение и сравнить с бюджетом. Превышение — в сдачу с замером; issue заводит ведущий.

## Отчёт владельцу

- Три пункта на языке владельца — простыми словами: что изменилось для пользователя, что не сделано, что нужно от владельца. Эти три пункта — часть DONE; отдельного отчёта владельцу не создавать.

<!-- /team-process:executor-rules -->
