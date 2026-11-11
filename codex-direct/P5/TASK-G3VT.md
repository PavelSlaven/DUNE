# Задание P5G3VT — приёмочные тесты экранов итогов миссии и редактора карт (шаг П5г, часть 3в)

Исполнитель: корневая нить Codex `gpt-6.1-sol` `high`; прогоны тестов делает один помощник `gpt-6-luna` `xhigh`.

Рабочая копия: `/srv/dune/worktrees/u34`, ветка `codex/p5g3v`, `HEAD` — `c5834615f8fc71789bba7108078a461018cc7d56` (часть 3б шага П5г). Файлы Git LFS в этой рабочей копии — настоящие данные. Временные файлы — в `.tmp/p5g3vt/`. Коммитов не делай: коммиты делает ведущий по списку из сдачи.

## Цель

Положить в рабочую копию два новых скрипта Python приёмочных тестов части 3в шага П5г и поправить ожидание теста `test_g_exclusions_text` ровно в том виде, что в шаге 1, получить красные прогоны H, I и K и заморозить тесты хэшем. Код игры и другие файлы рабочей копии не менять.

## Что уже решено

Часть 3в добавляет в каталог режима отладки интерфейса (`ui-audit`) порта сцены экранов апстрима, у которых нет сцен форка: итоги миссии (`cScoringState`), окно настройки новой карты (`cNewMapEditorState`) и редактор карт (`cEditorState`) с каждой из трёх правых панелей — рельеф, стартовые клетки, симметрия. Экран видеоролика (`cVideoState`) рисует только кадры видео и курсор (`src/gamestates/cVideoState.cpp@c583461:91-99`), поэтому он и его состояние `GAME_VIDEO` получают исключения с причиной в `tools/ui-audit/exclusions.tsv`. После части 3в проверка покрытия экранов не находит ни одной проблемы.

Элементы интерфейса редактора, которые сейчас ничего не пишут в журнал геометрии, — `GuiBar`, `GuiStateButton`, `GuiValueButton`, `GuiCycleButton`, `GuiTextInput` — будут писать запись `gui` с типом, равным имени класса, как уже пишет `GuiLabel`. Включённые `GuiStateButton`, `GuiValueButton`, `GuiCycleButton` и каждый `GuiTextInput` будут писать ещё запись `click` с именем, равным имени класса, как уже пишет `GuiCheckBox`; `GuiBar` записи `click` не пишет. Экран редактора будет писать запись `area` `editor-map` — область карты. Всё это вводит код части 3в; этим тестам оно нужно как ожидания.

Тесты пишутся до кода. Их потом выполняет другой исполнитель, который пишет код по тому же контракту и тесты не меняет. Скрипты запускают установленную игру и в CTest не входят: в CI нет данных Git LFS. Скрипты создают временную папку через `tempfile.TemporaryDirectory` в системной временной папке и удаляют её при выходе — это исключение из правила о папке задачи для прогонов H и I. Тест `tools/ui-audit/tests/test_port_changes.py` входит в CTest и игру не запускает.

Сборка в этой задаче не нужна. Установленная игра — `.tmp/out/run/bin/d2tm`; сцен части 3в в ней нет, и оба новых скрипта должны упасть. Ведущий проверил оба скрипта на поддельной игре: зелёный прогон по контракту и 35 атак — каждая падает по своей причине. Правку `test_port_changes.py` ведущий проверил так: при нынешнем `exclusions.tsv` падает только `test_g_exclusions_text`, при `exclusions.tsv` с двумя новыми строками пункта 17 все тесты файла проходят.

## Прочитать до работы

Прочитай целиком до первого действия, каждый файл отдельным вызовом, пути — от корня рабочей копии: `tests/ui_audit/ui_audit_runtime_support.py`, `tests/ui_audit/ui_audit_part3a_catalog.py`, `tests/ui_audit/ui_audit_part3a_scenes.py`, `tools/ui-audit/check_screens.py`, `tools/ui-audit/tests/test_port_changes.py`.

## Контракт поведения

Этот раздел дословно входит и в задание исполнителя кода части 3в.

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

## Шаг 1. Тесты — корневая нить сама

Перед созданием файлов: `test ! -e tests/ui_audit/ui_audit_part3c_catalog.py && test ! -e tests/ui_audit/ui_audit_part3c_scenes.py && git branch --show-current` — код выхода 0 и вывод `codex/p5g3v`, иначе блок `## Q-P5G3VT-05` и стоп.

### Новый файл `tests/ui_audit/ui_audit_part3c_catalog.py`

Ровно такого вида:

```python
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import ui_audit_part3a_catalog as part3a  # noqa: E402
import ui_audit_runtime_support as support  # noqa: E402

SCORING_READINESS = "FixedFrames(8, no readiness flag)"
EDITOR_READINESS = "StateSettled"
EDITOR_BARS = ("topology", "start-cells", "symmetry")
GROUPS = ("scoring", "new-map-editor", "editor")
EXPECTED_COUNT = 5


def expected_scenes():
    scenes = [
        part3a.scene("scoring", "scoring", "GAME_SCORING", "cScoringState", "atreides", SCORING_READINESS),
        part3a.scene("editor-new-map", "new-map-editor", "GAME_NEW_MAP_EDITOR", "cNewMapEditorState", "",
                     EDITOR_READINESS),
    ]
    return scenes + [part3a.scene(f"editor-{bar}", "editor", "GAME_EDITOR", "cEditorState", "", EDITOR_READINESS)
                     for bar in EDITOR_BARS]


def in_part3c(entry):
    return entry["group"] in GROUPS


def check_coverage(scenes):
    screens = part3a.check_screens
    exclusions, problems = screens.load_exclusions(
        (part3a.REPO_ROOT / "tools" / "ui-audit" / "exclusions.tsv").read_text(encoding="utf-8"))
    problems += screens.check_screens(scenes, screens.collect_code_names(part3a.REPO_ROOT), exclusions)
    return f"Screen coverage problems: {problems}" if problems else None


def check(game):
    expected = {entry["id"]: entry for entry in expected_scenes()}
    if len(expected) != EXPECTED_COUNT:
        return f"The expected list holds {len(expected)} scenes instead of {EXPECTED_COUNT}"
    result = game.run(["--ui-audit-list"])
    if result.returncode != 0:
        return f"--ui-audit-list exited with {result.returncode}\n{result.stderr}"
    try:
        scenes = support.read_json(result.stdout)["scenes"]
    except (ValueError, KeyError, TypeError) as error:
        return f"--ui-audit-list did not print a catalog: {error}\n{result.stdout}"
    if not isinstance(scenes, list):
        return f"The catalog scenes are not a list: {scenes}"
    for entry in scenes:
        if not isinstance(entry, dict) or set(entry) != part3a.SCENE_KEYS:
            return f"Scene keys differ: {entry}"
    actual = [entry for entry in scenes if in_part3c(entry)]
    ids = [entry["id"] for entry in actual]
    duplicates = sorted({scene_id for scene_id in ids if ids.count(scene_id) > 1})
    if duplicates:
        return f"Duplicate scene ids: {duplicates}"
    missing = sorted(set(expected) - set(ids))
    extra = sorted(set(ids) - set(expected))
    if missing or extra:
        return f"Part 3c scenes differ: missing {missing}; extra {extra}"
    for entry in actual:
        if not support.same_json(entry, expected[entry["id"]]):
            return f"Unexpected scene entry: {entry}\nexpected: {expected[entry['id']]}"
    return check_coverage(scenes)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    args = parser.parse_args()
    errors = []
    with support.GameRun(args.run_dir) as game:
        error = check(game)
        if error:
            errors.append(error)
        preferences = game.preferences_files()
        if preferences:
            errors.append(f"An audit run must not write preferences: {preferences}")
    for error in errors:
        print(error, file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
```

### Новый файл `tests/ui_audit/ui_audit_part3c_scenes.py`

Ровно такого вида:

```python
import argparse
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import ui_audit_part3a_scenes as base  # noqa: E402
import ui_audit_part3c_catalog as catalog  # noqa: E402
import ui_audit_runtime_support as support  # noqa: E402

SCORING_TEXTS = ("MISSION REPORT", "Click to continue", "YOU - Atreides")
MISSION_TIME = re.compile(r"Mission time: [0-9]{2}:[0-9]{2}")
UNITS_LINE = "Units built: "
NEW_MAP_WINDOW = {"x": 180, "y": 180, "w": 440, "h": 240}
NEW_MAP_GUI = {"GuiWindow": 1, "GuiLabel": 7, "GuiTextInput": 4, "GuiCycleButton": 2, "GuiCheckBox": 1,
               "GuiButton": 2}
NEW_MAP_CLICKS = {"GuiButton:Return to menu": 1, "GuiButton:Create map": 1, "GuiTextInput": 4, "GuiCycleButton": 2}
NEW_MAP_TEXTS = ("Map editor configuration", "Name your map:", "Name of author:", "Description:", "Width size:",
                 "Height size:", "Random:", "Return to menu", "Create map")
SELECT_BAR = {"x": 0, "y": 0, "w": 800, "h": 48}
SIDE_BAR = {"x": 752, "y": 48, "w": 48, "h": 552}
EDITOR_MAP = {"x": 0, "y": 48, "w": 752, "h": 552}
SAVE_CLICK = "GuiButton:"
SELECT_BUTTONS = 3
SIDE_BUTTONS = {"editor-topology": (6, 1), "editor-start-cells": (5, 0), "editor-symmetry": (8, 0)}


def count_by(records, key):
    return dict(Counter(record[key] for record in records))


def of_type(body, type_name):
    return [record for record in base.records_of(body, "gui") if record["t"] == type_name]


def click_type(record):
    return record["name"].split(":", 1)[0]


def rects_of(records):
    return sorted((record["x"], record["y"], record["w"], record["h"]) for record in records)


def check_click_owners(body):
    clicks = base.records_of(body, "click")
    for type_name in sorted({click_type(record) for record in clicks}):
        click_rects = rects_of(record for record in clicks if click_type(record) == type_name)
        gui_rects = rects_of(of_type(body, type_name))
        if click_rects != gui_rects:
            return f"the click records of {type_name} {click_rects} do not match its gui records {gui_rects} " \
                   f"one to one"
    return None


def check_counts(what, actual, expected):
    return None if actual == expected else f"{what} {actual} differ from {expected}"


def check_scoring(scene_id, body):
    texts = [record["s"] for record in base.records_of(body, "text")]
    times = [text for text in texts if MISSION_TIME.fullmatch(text)]
    return base.first_error(
        base.forbid_kinds(body, ("gui", "area", "label", "click")),
        *(base.require_text(body, text) for text in SCORING_TEXTS),
        None if len(times) == 1 else f"expected one text record Mission time: MM:SS, got {times}",
        None if any(text.startswith(UNITS_LINE) for text in texts) else f"no text record starting with {UNITS_LINE!r}",
    )


def check_new_map(scene_id, body):
    windows = of_type(body, "GuiWindow")
    return base.first_error(
        base.forbid_kinds(body, ("area", "label")),
        check_counts("gui records by type", count_by(base.records_of(body, "gui"), "t"), NEW_MAP_GUI),
        None if len(windows) == 1 and support.same_json(base.rect(windows[0]), NEW_MAP_WINDOW)
        else f"the GuiWindow record must be {NEW_MAP_WINDOW}: {windows}",
        check_counts("click records by name", count_by(base.records_of(body, "click"), "name"), NEW_MAP_CLICKS),
        check_click_owners(body),
        *(base.require_text(body, text) for text in NEW_MAP_TEXTS),
    )


def check_editor(scene_id, body):
    side_states, side_values = SIDE_BUTTONS[scene_id]
    expected_gui = {"GuiBar": 2, "GuiStateButton": SELECT_BUTTONS + side_states, "GuiButton": 1}
    expected_clicks = {"GuiStateButton": SELECT_BUTTONS + side_states, SAVE_CLICK: 1}
    if side_values:
        expected_gui["GuiValueButton"] = side_values
        expected_clicks["GuiValueButton"] = side_values
    bars = sorted((base.rect(record) for record in of_type(body, "GuiBar")), key=lambda rect: (rect["x"], rect["y"]))
    states = of_type(body, "GuiStateButton")
    in_select = [record for record in states if base.inside(record, SELECT_BAR)]
    in_side = [record for record in states if base.inside(record, SIDE_BAR)]
    values_outside = [record for record in of_type(body, "GuiValueButton") if not base.inside(record, SIDE_BAR)]
    save_outside = [record for record in of_type(body, "GuiButton") if not base.inside(record, SELECT_BAR)]
    return base.first_error(
        base.forbid_kinds(body, ("label",)),
        base.exact_rect(body, "area", "n", "editor-map", EDITOR_MAP),
        check_counts("area records by name", count_by(base.records_of(body, "area"), "n"), {"editor-map": 1}),
        check_counts("gui records by type", count_by(base.records_of(body, "gui"), "t"), expected_gui),
        None if support.same_json(bars, [SELECT_BAR, SIDE_BAR])
        else f"the GuiBar records must be {SELECT_BAR} and {SIDE_BAR}: {bars}",
        None if len(in_select) == SELECT_BUTTONS and len(in_side) == side_states
        else f"expected {SELECT_BUTTONS} GuiStateButton records inside {SELECT_BAR} and {side_states} inside "
             f"{SIDE_BAR}, got {len(in_select)} and {len(in_side)}",
        f"GuiValueButton records outside {SIDE_BAR}: {values_outside}" if values_outside else None,
        f"GuiButton records outside {SELECT_BAR}: {save_outside}" if save_outside else None,
        check_counts("click records by name", count_by(base.records_of(body, "click"), "name"), expected_clicks),
        check_click_owners(body),
    )


def check_for(scene_id):
    if scene_id == "scoring":
        return check_scoring
    if scene_id == "editor-new-map":
        return check_new_map
    if scene_id in SIDE_BUTTONS:
        return check_editor
    raise ValueError(f"no check for scene {scene_id}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    args = parser.parse_args()
    errors = []
    with support.GameRun(args.run_dir) as game:
        for scene in catalog.expected_scenes():
            scene_id = scene["id"]
            header, body, error = base.run_scene(game, scene)
            if error is None:
                error = check_for(scene_id)(scene_id, body)
            if error:
                errors.append(f"{scene_id}: {error}")
        preferences = game.preferences_files()
        if preferences:
            errors.append(f"An audit run must not write preferences: {preferences}")
    for error in errors:
        print(error, file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
```

### Правка `tools/ui-audit/tests/test_port_changes.py`

В константе `EXCLUSIONS` строку

```python
    "cCreatorState\tсоздаёт и хранит состояния игры, не экран\n"
```

замени ровно этими тремя строками (первая — та же строка без изменений, перевод строки внутри кавычек — два символа `\n` исходного текста, как в соседних строках):

```python
    "cCreatorState\tсоздаёт и хранит состояния игры, не экран\n"
    "GAME_VIDEO\tсостояние показа видеоролика; его экран cVideoState рисует только кадры видео, элементов интерфейса нет\n"
    "cVideoState\tэкран видеоролика: рисует только кадры видео и курсор, элементов интерфейса нет\n"
```

Проверка правки: последняя строка вывода `git -c lfs.storage=$PWD/.tmp/p5g3vt/lfs diff --stat tools/ui-audit/tests/test_port_changes.py` содержит `1 file changed, 2 insertions(+)`.

Другие файлы `tests/`, `tools/` и весь код вне `tests/` и `tools/` не меняются; `tools/ui-audit/exclusions.tsv` в этой задаче не меняется.

## Шаг 2. Прогоны — помощник `gpt-6-luna` `xhigh`

Все команды — из корня рабочей копии `/srv/dune/worktrees/u34`.

1. `mkdir -p .tmp/p5g3vt && python3 -m py_compile tests/ui_audit/ui_audit_part3c_catalog.py tests/ui_audit/ui_audit_part3c_scenes.py tools/ui-audit/tests/test_port_changes.py; echo exit=$?` — ожидается `exit=0`.
2. **Прогон H** — `LD_LIBRARY_PATH=$PWD/.tmp/deps/prefix/lib python3 -B tests/ui_audit/ui_audit_part3c_catalog.py --run-dir .tmp/out/run/bin > .tmp/p5g3vt/run-h.log 2>&1; echo exit=$?`. Ожидается: `exit=1`; первая строка лога ровно `Part 3c scenes differ: missing ['editor-new-map', 'editor-start-cells', 'editor-symmetry', 'editor-topology', 'scoring']; extra []`; в логе нет строки, содержащей `must not write preferences`.
3. **Прогон I** — `LD_LIBRARY_PATH=$PWD/.tmp/deps/prefix/lib timeout 1800 python3 -B tests/ui_audit/ui_audit_part3c_scenes.py --run-dir .tmp/out/run/bin > .tmp/p5g3vt/run-i.log 2>&1; echo exit=$?`. Ожидается: `exit=1`; `grep -c 'game exited with 2' .tmp/p5g3vt/run-i.log` выводит `5`; `grep -c 'ui-audit: unknown scene' .tmp/p5g3vt/run-i.log` выводит `5`; в логе нет строки, содержащей `must not write preferences`.
4. **Прогон K** — `python3 -B tools/ui-audit/tests/test_port_changes.py > .tmp/p5g3vt/run-k.log 2>&1; echo exit=$?`. Ожидается: `exit=1`; `grep -c '^FAIL: ' .tmp/p5g3vt/run-k.log` выводит `1`, и эта строка начинается с `FAIL: test_g_exclusions_text`; `grep -c '^ERROR: ' .tmp/p5g3vt/run-k.log` выводит `0`; последняя строка лога — `FAILED (failures=1)`.
5. После прогонов — `rm -r tests/ui_audit/__pycache__ tools/ui-audit/__pycache__ tools/ui-audit/tests/__pycache__` для тех из этих папок, что появились.

Помощник сдаёт корневой нити каждую команду, её код выхода и вывод, первые 3 строки лога прогона H (каждая обрезана до 300 символов командой `cut -c1-300`), выводы двух `grep -c` прогона I, выводы двух `grep -c` прогона K, строку `FAIL:` и последнюю строку лога прогона K.

Ошибка синтаксиса или импорта в файле шага 1 — корневая нить сверяет файл с текстом шага 1 и исправляет расхождение с ним, затем помощник повторяет шаг 2 с пункта 1. Другой код выхода или другая причина в прогоне H, I или K при файлах, совпадающих с текстом шага 1, — блок `## Q-P5G3VT-02` с этими строками и стоп. Ожидание теста под игру не подгоняй: тест, который требует правки текста шага 1, — тоже `## Q-P5G3VT-02`.

## Шаг 3. Заморозка — корневая нить

`sha256sum tests/ui_audit/ui_audit_part3c_catalog.py tests/ui_audit/ui_audit_part3c_scenes.py tools/ui-audit/tests/test_port_changes.py tests/ui_audit/ui_audit_part3a_catalog.py tests/ui_audit/ui_audit_part3a_scenes.py tests/ui_audit/ui_audit_runtime_support.py tools/ui-audit/check_scenes.py tools/ui-audit/check_geometry.py tools/ui-audit/check_screens.py > .tmp/p5g3vt/tests.sha256`. После этой команды эти девять файлов не меняются.

Проверка: `git -c lfs.storage=$PWD/.tmp/p5g3vt/lfs status --short` выводит ровно три строки: ` M tools/ui-audit/tests/test_port_changes.py`, `?? tests/ui_audit/ui_audit_part3c_catalog.py` и `?? tests/ui_audit/ui_audit_part3c_scenes.py`. Другие строки — блок `## Q-P5G3VT-03` с выводом и стоп.

## Сдача

Последнее сообщение — блок `## DONE-P5G3VT | <время UTC из date -u> | HEAD <sha>` по форме из правил ниже. В нём:

- каждая команда шага 2 с кодом выхода и выводом, первые 3 строки лога прогона H (до 300 символов каждая), выводы двух `grep -c` прогона I, выводы двух `grep -c`, строка `FAIL:` и последняя строка лога прогона K;
- содержимое `.tmp/p5g3vt/tests.sha256`;
- вывод `git status --short` из шага 3;
- список коммитов: один пункт — три файла шага 1, сообщение на английском о приёмочных тестах части 3c режима отладки интерфейса: скрипты, которые запускают игру и проверяют каталог и записи пяти сцен итогов миссии и редактора карт, и ожидание двух новых исключений экрана видеоролика в тесте текста `exclusions.tsv`; последняя строка сообщения — `Behavior changes: none`;
- раздел «Рабочие места»: вывод `python3 /srv/dune/tools/task-places.py inventory .tmp/p5g3vt --size`; у `.tmp/p5g3vt` пометка `оставить — хэши тестов нужны исполнителю`. Остальные папки в `.tmp/` созданы до этой задачи и в раздел не входят. Ничего не удаляй, кроме папок `__pycache__` пункта 5 шага 2.

Числа в сдаче — только из вывода команд.

## Организация работы

- **Порядок:** `create_goal` (первым действием, по правилам исполнителя ниже; objective — текст раздела «Цель» дословно) → раздел «Прочитать до работы» → шаг 1 → шаг 2 → шаг 3 → сдача и стоп.
- **Параллельно:** шаги зависят друг от друга, параллельных дорожек нет.
- **Помощники:** один помощник `gpt-6-luna` `xhigh`, без вложенных: шаг 2 — команды, их коды выхода и выписка строк логов. Бриф дословно содержит раздел «Шаг 2», абзац «Комментарии в коде» и запрет менять файлы, кроме папок `__pycache__` пункта 5 шага 2 и файлов в `.tmp/p5g3vt/`. Шаги 1 и 3, сверку файлов с текстом шага 1 и сдачу делает корневая нить; механику — команды и выписку логов — только помощник.
- **Остановки:** только на `## DONE-P5G3VT` и на блоках `## Q-P5G3VT-NN`. Команда оболочки дважды подряд не завершилась (нет кода выхода) — блок `## Q-P5G3VT-04` и стоп.
- **Рамка правок:** два новых файла и правка `tools/ui-audit/tests/test_port_changes.py` шага 1, папки `__pycache__` пункта 5 шага 2 и папка `.tmp/p5g3vt/`. Игра пишет в `.tmp/out/run/bin/` и во временные папки скриптов; это не правка.

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
