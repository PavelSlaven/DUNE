# Задание P5G3AT — приёмочные тесты основы боевых сцен, исхода и меню настроек в бою (шаг П5г, часть 3а)

Исполнитель: корневая нить Codex `gpt-6.1-sol` `high`; прогоны игры и тестов делает один помощник `gpt-6-luna` `xhigh`.

Рабочая копия: `/srv/dune/worktrees/u34`, ветка `codex/p5g3a`, `HEAD` — `dc6e5ffd74f6275390a9c4a676aafdca058df7dd` (часть 2 шага П5г с исправлением указателя правил местности). Файлы Git LFS в этой рабочей копии — настоящие данные. Временные файлы — в `.tmp/p5g3at/`. Коммитов не делай: коммиты делает ведущий по списку из сдачи.

## Цель

Положить в рабочую копию два скрипта Python приёмочных тестов части 3а шага П5г ровно в том виде, что в шаге 1, дополнить ожидание `EXCLUSIONS` теста `tools/ui-audit/tests/test_port_changes.py` тремя строками шага 1, получить красные прогоны H, I и J и заморозить тесты хэшем. Код игры и другие файлы рабочей копии не менять.

## Что уже решено

Часть 3а шага П5г добавляет в каталог режима отладки интерфейса (`ui-audit`) порта 24 сцены: метки юнитов (18 типов) и зданий (2) в бою, экран исхода миссии (2) и меню настроек в бою (2), — а также записи режима для экранов боя: области `area` (верхняя панель, боковая панель, список построек, мини-карта), метки `label` (полоски здоровья и пряности, номер группы и звёзды опыта юнитов, полоска здоровья здания), заголовок `map_viewport`, наведение курсора и записи `click` верхней и боковой панелей. Сцены боя идут в бою миссии 1 Атрейдесов, как у форка: у игрока строительная площадка, радара нет. Сцены базы в бою (списки построек, радар, установка здания) — часть 3б; экраны апстрима без сцен форка (`cScoringState`, `cVideoState`, `cEditorState`, `cNewMapEditorState`) — часть 3в. Сцены `options-game-main-saves` (шаг П8), `options-game-game`, `options-game-controls`, `options-game-diagnostics`, `options-game-keybind` (в меню настроек порта нет страниц и назначения клавиш) не переносятся.

Тесты пишутся до кода. Их потом выполняет другой исполнитель, который пишет код по тому же контракту и тесты не меняет. Скрипты запускают установленную игру и в CTest не входят: в CI нет данных Git LFS. Скрипты создают временную папку через `tempfile.TemporaryDirectory` в системной временной папке и удаляют её при выходе — это исключение из правила о папке задачи для прогонов H и I.

Сборка в этой задаче не нужна. Установленная игра — `.tmp/out/run/bin/d2tm`, сборка `HEAD` (части 1, 2 и 4: 108 сцен, сцен части 3а нет); на ней все сцены части 3а неизвестны, и оба скрипта должны упасть.

## Прочитать до работы

Прочитай целиком до первого действия, каждый файл отдельным вызовом, пути — от корня рабочей копии: `tests/ui_audit/ui_audit_runtime_support.py`, `tests/ui_audit/ui_audit_part2_scenes.py`, `tools/ui-audit/check_scenes.py`, `tools/ui-audit/check_screens.py`, `tools/ui-audit/tests/test_port_changes.py`.

## Контракт поведения

Этот раздел дословно входит и в задание исполнителя кода части 3а.

Пункты 1–8 контрактов частей 1 и 2 действуют без изменений; скрипты частей 1, 2 и 4 в `tests/ui_audit/` остаются зелёными. Игра запускается так же, как в пункте 2 части 1: из каталога установки сборки порта (рабочий каталог процесса — этот каталог) с аргументами `-windowed -screenWidth 1024 -screenHeight 768` и аргументами режима; переменные среды `SDL_VIDEODRIVER=dummy`, `SDL_RENDER_DRIVER=software`, `SDL_AUDIODRIVER=dummy`, `XDG_DATA_HOME=<пустая временная папка>`; `LD_LIBRARY_PATH` задаёт вызывающий процесс.

9. **Каталог части 3а.** В выводе `--ui-audit-list` у каждой сцены ровно ключи части 1. Среди сцен, у которых `id` начинается с `units-label-` или `structure-label-` либо `group` — `outcome` или `options-game`, нет двух с одним `id`, и эти сцены ровно совпадают по `id` и значениям всех ключей с 24 сценами таблицы ниже. У каждой из 24 сцен `hud` — `false`, `hd_only` — `false`; `game_screen` — `true` у сцен `units-label-*` и `structure-label-*` и `false` у остальных; `hover` — `{"x": 0, "y": 0}` у `structure-label-top` и `structure-label-right` и `null` у остальных. `<тип>` — каждое из `trike`, `raider`, `quad`, `tank`, `siegetank`, `launcher`, `deviator`, `sonictank`, `devastator`, `harvester`, `mcv`, `soldier`, `infantry`, `trooper`, `troopers`, `unit-fremen-one`, `unit-fremen-three`, `saboteur`; `""` — пустая строка.

   | `id` | `group` | `state` | `screen` | `house` | `readiness` |
   |---|---|---|---|---|---|
   | `units-label-<тип>` | `game-playing` | `GAME_PLAYING` | `cGamePlaying` | `atreides` | `FixedFrames(5, no readiness flag)` |
   | `structure-label-top`, `structure-label-right` | `game-playing` | `GAME_PLAYING` | `cGamePlaying` | `atreides` | `FixedFrames(5, no readiness flag)` |
   | `outcome-win` | `outcome` | `GAME_WINNING` | `cWinLoseState` | `atreides` | `FixedFrames(8, no readiness flag)` |
   | `outcome-lose` | `outcome` | `GAME_LOSING` | `cWinLoseState` | `atreides` | `FixedFrames(8, no readiness flag)` |
   | `options-game-main-nosaves`, `options-game-applied` | `options-game` | `GAME_OPTIONS` | `cOptionsState` | `""` | `FixedFrames(14, no readiness flag)` |

10. **Покрытие экранов.** Функции `tools/ui-audit/check_screens.py` порта: `load_exclusions(<текст tools/ui-audit/exclusions.tsv>)` возвращает исключения и список проблем; к этому списку добавляется результат `check_screens(<сцены вывода --ui-audit-list>, collect_code_names(<корень рабочей копии>), <исключения>)`. Итоговый список содержит только строки `no scene and no exclusion for <имя>`, где `<имя>` — одно из `GAME_EDITOR`, `GAME_NEW_MAP_EDITOR`, `GAME_SCORING`, `GAME_VIDEO`, `cEditorState`, `cNewMapEditorState`, `cScoringState`, `cVideoState` (экраны апстрима, их сцены — часть 3в). Файл `tools/ui-audit/exclusions.tsv` — прежние девять строк и в конце три строки (поля разделены одной табуляцией, каждая строка кончается переводом строки):
    - `cMentatState` — `экран брифинга ментата; сцены режима названы классами ментатов AtreidesMentat, HarkonnenMentat, OrdosMentat, SardaukarMentat`;
    - `cTellHouseState` — `экран рассказа о Доме; сцены режима названы классом ментата BeneMentat`;
    - `cCreatorState` — `создаёт и хранит состояния игры, не экран`.
    Текст файла целиком сверяет тест `test_g_exclusions_text` (`tools/ui-audit/tests/test_port_changes.py`).

11. **Прогон сцены части 3а.** Для каждой из 24 сцен пункта 9 запуск с `--ui-audit-scene <id> --ui-audit-out <папка>` завершается с кодом выхода 0 не позже чем через 120 секунд; в `<папка>` есть файлы `<id>.png` и `<id>.geometry.jsonl`. PNG — как в пункте 6 части 2 (1024 × 768 точек, блоки `IDAT` и `IEND`, не меньше 10 000 байт). Файл геометрии — как в пункте 6 части 2 (строки JSON без `NaN`, `Infinity` и `-Infinity`, разделённые символом перевода строки). Первая строка — заголовок: значения ключей `k`, `scene`, `resolution`, `language`, `graphics`, `canvas`, `render_scale`, `world_scale` равны `"header"`, `"<id>"`, `"1024x768"`, `"en"`, `"hd"`, `{"w": 800, "h": 600}`, `0`, `0`; `game_screen` равно значению этой сцены в каталоге; `version` — строка. У сцен с `game_screen` `true` в заголовке есть ключ `map_viewport` со значением `{"x": 0, "y": 42, "w": 520, "h": 558}` (область карты при холсте 800 × 600: под верхней панелью высотой 42 и левее боковой панели шириной 280 — `src/sidebar/HudLayout.hpp@dc6e5ff:14,46`, `src/game/cGame_logic.cpp@dc6e5ff:783,833`); у остальных сцен ключа `map_viewport` нет. Другие ключи заголовка не проверяются. Каждая следующая строка — запись одного из пяти видов ровно с такими ключами: `"k": "text"` — `k`, `s`, `x`, `y`, `w`, `h`, `box`; `"k": "gui"` — `k`, `t`, `x`, `y`, `w`, `h`; `"k": "click"` — `k`, `name`, `x`, `y`, `w`, `h`; `"k": "area"` — `k`, `n`, `x`, `y`, `w`, `h`; `"k": "label"` — `k`, `kind`, `obj`, `type`, `x`, `y`, `w`, `h`, `owner`. У всех записей `x`, `y`, `w`, `h` — целые числа JSON. У записей `click` и `area` `name` и `n` — строки, прямоугольник лежит внутри холста: `w` > 0, `h` > 0, `x` ≥ 0, `y` ≥ 0, `x + w` ≤ 800, `y + h` ≤ 600. У записи `label`: `owner` — объект ровно с ключами `x`, `y`, `w`, `h`, значения — целые числа JSON; `obj` — целое число JSON не меньше 0; `w` ≥ 0, `h` ≥ 0; `kind` и `type` — строки. После всех запусков в папке `XDG_DATA_HOME` нет файла с именем `preferences.ini` ни на каком уровне вложенности.

12. **Записи сцен части 3а.** «Одна запись `<вид>` `<имя>`» — ровно одна запись этого вида с этим значением `name` (`click`) или `n` (`area`); прямоугольник A «внутри» прямоугольника B — как в пункте 7 части 2; «прямоугольник (x, y, w, h)» — значения `x`, `y`, `w`, `h` записи.
    - Каждая сцена `units-label-*` и `structure-label-*` (экран боя):
      - одна запись area `top-panel` с прямоугольником (0, 0, 800, 42); одна запись area `sidebar` с прямоугольником (520, 42, 280, 558); одна запись area `build-list`, внутри прямоугольника `sidebar`; нет записи area `minimap` (у игрока миссии 1 нет радара, а порт не рисует мини-карту без радара, `src/drawers/cMiniMapDrawer.cpp@dc6e5ff:116-118`);
      - одна запись click `top-options` с прямоугольником (7, 4, 126, 33) (кнопка «Options» верхней панели, `src/managers/cDrawManager.cpp@dc6e5ff:318`);
      - нет записей click `minimap` и `order-button`;
      - каждая запись click, у которой `name` начинается с `list-button:` или `build-item:` либо равно `build-scrollbar`, лежит внутри прямоугольника `sidebar`; есть хотя бы одна запись click, у которой `name` начинается с `list-button:` или `build-item:` (у игрока миссии 1 есть строительная площадка, и её список построек доступен).
    - Каждая сцена `units-label-<тип>`: у каждой записи label `kind` — одно из `health`, `group`, `experience`, `spice`, а `type` — `<ТИП>`, имя константы типа юнита порта (`src/include/definitions.h@dc6e5ff:169-191`): `TRIKE`, `RAIDER`, `QUAD`, `TANK`, `SIEGETANK`, `LAUNCHER`, `DEVIATOR`, `SONICTANK`, `DEVASTATOR`, `HARVESTER`, `MCV`, `SOLDIER`, `INFANTRY`, `TROOPER`, `TROOPERS`, `UNIT_FREMEN_ONE`, `UNIT_FREMEN_THREE`, `SABOTEUR` для `<тип>` в порядке пункта 9. Функция `check_scenes.check_scene(<заголовок>, <записи после заголовка>)` из `tools/ui-audit/check_scenes.py` порта возвращает `"OK"`: ровно три юнита (три разных `obj`) с метками `health`, `group`, `experience` (у комбайна ещё `spice`), один у верхнего, один у правого и один у нижнего края области карты, и ни одна запись text не пересекает метку `group`.
    - `structure-label-top`, `structure-label-right`: у каждой записи label `kind` — `structure-health`, `type` — `STRUCTURE`; `check_scenes.check_scene` возвращает `"OK"`: одно здание с меткой здоровья у верхнего (`structure-label-top`) или правого (`structure-label-right`) края области карты.
    - `outcome-win`, `outcome-lose`: запись text `Click to continue` (`src/gamestates/cWinLoseState.cpp@dc6e5ff:87`); нет записей area, label и click.
    - `options-game-main-nosaves`: хотя бы одна запись gui; записи text `Mission select`, `Save game`, `Load game` (меню настроек из боя кампании, `src/gamestates/cOptionsState.cpp@dc6e5ff:163-203`); нет записи text `Saved. Restart the game.`; нет записей area и label.
    - `options-game-applied`: записи text `Saved. Restart the game.` и `Mission select`; нет записей area и label.

## Шаг 1. Тесты — корневая нить сама

Перед созданием файлов: `test ! -e tests/ui_audit/ui_audit_part3a_catalog.py && test ! -e tests/ui_audit/ui_audit_part3a_scenes.py && git diff --quiet -- tools/ui-audit/tests/test_port_changes.py` — код выхода 0, иначе блок `## Q-P5G3AT-05` и стоп.

### Новый файл `tests/ui_audit/ui_audit_part3a_catalog.py`

Ровно такого вида:

```python
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools" / "ui-audit"))

import check_screens  # noqa: E402
import ui_audit_runtime_support as support  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[2]
SCENE_KEYS = {"id", "group", "state", "screen", "game_screen", "house", "hud", "hd_only", "hover", "readiness"}
UNIT_TYPES = (
    ("trike", "TRIKE"),
    ("raider", "RAIDER"),
    ("quad", "QUAD"),
    ("tank", "TANK"),
    ("siegetank", "SIEGETANK"),
    ("launcher", "LAUNCHER"),
    ("deviator", "DEVIATOR"),
    ("sonictank", "SONICTANK"),
    ("devastator", "DEVASTATOR"),
    ("harvester", "HARVESTER"),
    ("mcv", "MCV"),
    ("soldier", "SOLDIER"),
    ("infantry", "INFANTRY"),
    ("trooper", "TROOPER"),
    ("troopers", "TROOPERS"),
    ("unit-fremen-one", "UNIT_FREMEN_ONE"),
    ("unit-fremen-three", "UNIT_FREMEN_THREE"),
    ("saboteur", "SABOTEUR"),
)
GAME_READINESS = "FixedFrames(5, no readiness flag)"
OUTCOME_READINESS = "FixedFrames(8, no readiness flag)"
OPTIONS_READINESS = "FixedFrames(14, no readiness flag)"
EXPECTED_COUNT = 24
LATER_SCREENS = ("GAME_EDITOR", "GAME_NEW_MAP_EDITOR", "GAME_SCORING", "GAME_VIDEO", "cEditorState",
                 "cNewMapEditorState", "cScoringState", "cVideoState")


def scene(scene_id, group, state, screen, house, readiness, game_screen=False, hover=None):
    return {
        "id": scene_id,
        "group": group,
        "state": state,
        "screen": screen,
        "game_screen": game_screen,
        "house": house,
        "hud": False,
        "hd_only": False,
        "hover": hover,
        "readiness": readiness,
    }


def expected_scenes():
    scenes = []
    for name, _ in UNIT_TYPES:
        scenes.append(scene(f"units-label-{name}", "game-playing", "GAME_PLAYING", "cGamePlaying", "atreides",
                            GAME_READINESS, game_screen=True))
    for edge in ("top", "right"):
        scenes.append(scene(f"structure-label-{edge}", "game-playing", "GAME_PLAYING", "cGamePlaying", "atreides",
                            GAME_READINESS, game_screen=True, hover={"x": 0, "y": 0}))
    scenes.append(scene("outcome-win", "outcome", "GAME_WINNING", "cWinLoseState", "atreides", OUTCOME_READINESS))
    scenes.append(scene("outcome-lose", "outcome", "GAME_LOSING", "cWinLoseState", "atreides", OUTCOME_READINESS))
    for variant in ("main-nosaves", "applied"):
        scenes.append(scene(f"options-game-{variant}", "options-game", "GAME_OPTIONS", "cOptionsState", "",
                            OPTIONS_READINESS))
    return scenes


def in_part3a(entry):
    scene_id = entry["id"]
    return (isinstance(scene_id, str) and scene_id.startswith(("units-label-", "structure-label-"))) or \
        entry["group"] in ("outcome", "options-game")


def check_coverage(scenes):
    exclusions, problems = check_screens.load_exclusions(
        (REPO_ROOT / "tools" / "ui-audit" / "exclusions.tsv").read_text(encoding="utf-8"))
    problems += check_screens.check_screens(scenes, check_screens.collect_code_names(REPO_ROOT), exclusions)
    allowed = {f"no scene and no exclusion for {name}" for name in LATER_SCREENS}
    unexpected = [problem for problem in problems if problem not in allowed]
    return f"Screen coverage problems: {unexpected}" if unexpected else None


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
        if not isinstance(entry, dict) or set(entry) != SCENE_KEYS:
            return f"Scene keys differ: {entry}"
    actual = [entry for entry in scenes if in_part3a(entry)]
    ids = [entry["id"] for entry in actual]
    duplicates = sorted({scene_id for scene_id in ids if ids.count(scene_id) > 1})
    if duplicates:
        return f"Duplicate scene ids: {duplicates}"
    missing = sorted(set(expected) - set(ids))
    extra = sorted(set(ids) - set(expected))
    if missing or extra:
        return f"Part 3a scenes differ: missing {missing}; extra {extra}"
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

### Новый файл `tests/ui_audit/ui_audit_part3a_scenes.py`

Ровно такого вида:

```python
import argparse
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools" / "ui-audit"))

import check_scenes  # noqa: E402
import ui_audit_part3a_catalog as catalog  # noqa: E402
import ui_audit_runtime_support as support  # noqa: E402

HEADER = {
    "k": "header",
    "resolution": "1024x768",
    "language": "en",
    "graphics": "hd",
    "canvas": {"w": 800, "h": 600},
    "render_scale": 0,
    "world_scale": 0,
}
MAP_VIEWPORT = {"x": 0, "y": 42, "w": 520, "h": 558}
RECORD_KEYS = {
    "text": {"k", "s", "x", "y", "w", "h", "box"},
    "gui": {"k", "t", "x", "y", "w", "h"},
    "click": {"k", "name", "x", "y", "w", "h"},
    "area": {"k", "n", "x", "y", "w", "h"},
    "label": {"k", "kind", "obj", "type", "x", "y", "w", "h", "owner"},
}
RECT_KEYS = ("x", "y", "w", "h")
CANVAS_W = 800
CANVAS_H = 600
CANVAS_RECT = {"x": 0, "y": 0, "w": CANVAS_W, "h": CANVAS_H}
MIN_PNG_BYTES = 10000
TOP_PANEL = {"x": 0, "y": 0, "w": 800, "h": 42}
SIDEBAR = {"x": 520, "y": 42, "w": 280, "h": 558}
TOP_OPTIONS = {"x": 7, "y": 4, "w": 126, "h": 33}
SIDEBAR_CLICK_PREFIXES = ("list-button:", "build-item:")
UNIT_LABEL_KINDS = {"health", "group", "experience", "spice"}
STATUS_TEXT = "Saved. Restart the game."
OUTCOME_TEXT = "Click to continue"
IN_GAME_OPTIONS_TEXTS = ("Mission select", "Save game", "Load game")


def reject_constant(name):
    raise ValueError(f"{name} is not a JSON number")


def records_of(body, kind):
    return [record for record in body if record["k"] == kind]


def clicks_named(body, name):
    return [record for record in records_of(body, "click") if record["name"] == name]


def click_names(body):
    return {record["name"] for record in records_of(body, "click")}


def rect(record):
    return {key: record[key] for key in RECT_KEYS}


def inside(inner, outer):
    return (inner["x"] >= outer["x"] and inner["y"] >= outer["y"] and
            inner["x"] + inner["w"] <= outer["x"] + outer["w"] and
            inner["y"] + inner["h"] <= outer["y"] + outer["h"])


def first_error(*errors):
    return next((error for error in errors if error), None)


def one_record(body, kind, key, name):
    found = [record for record in records_of(body, kind) if record[key] == name]
    if len(found) != 1:
        return None, f"expected one {kind} record {name}, got {found}"
    return found[0], None


def exact_rect(body, kind, key, name, expected):
    record, error = one_record(body, kind, key, name)
    if error:
        return error
    if not support.same_json(rect(record), expected):
        return f"the {kind} record {name} must be {expected}, got {rect(record)}"
    return None


def forbid_clicks(body, names):
    present = sorted(set(names) & click_names(body))
    return f"unexpected click records {present}" if present else None


def forbid_kinds(body, kinds):
    present = sorted({record["k"] for record in body if record["k"] in kinds})
    return f"unexpected {present} records" if present else None


def require_text(body, text):
    return None if any(record["s"] == text for record in records_of(body, "text")) else f"no text record {text!r}"


def check_game_screen(body):
    build_list, error = one_record(body, "area", "n", "build-list")
    if error:
        return error
    sidebar_clicks = [record for record in records_of(body, "click")
                      if record["name"].startswith(SIDEBAR_CLICK_PREFIXES) or record["name"] == "build-scrollbar"]
    outside = [record for record in sidebar_clicks if not inside(record, SIDEBAR)]
    return first_error(
        exact_rect(body, "area", "n", "top-panel", TOP_PANEL),
        exact_rect(body, "area", "n", "sidebar", SIDEBAR),
        None if inside(build_list, SIDEBAR) else f"the area record build-list lies outside {SIDEBAR}: {build_list}",
        None if not any(record["n"] == "minimap" for record in records_of(body, "area"))
        else "unexpected area record minimap",
        exact_rect(body, "click", "name", "top-options", TOP_OPTIONS),
        forbid_clicks(body, ["minimap", "order-button"]),
        f"sidebar click records outside {SIDEBAR}: {outside[:3]}" if outside else None,
        None if any(record["name"].startswith(SIDEBAR_CLICK_PREFIXES) for record in sidebar_clicks)
        else "no click record list-button:<n> or build-item:<n>",
    )


def check_scene_rules(header, body):
    result = check_scenes.check_scene(header, body)
    return None if result == "OK" else f"check_scenes: {result}"


def check_unit_labels(type_name):
    def check(header, body):
        wrong = [record for record in records_of(body, "label")
                 if record["kind"] not in UNIT_LABEL_KINDS or record["type"] != type_name]
        return first_error(
            check_game_screen(body),
            f"unexpected label records {wrong[:3]}" if wrong else None,
            check_scene_rules(header, body),
        )
    return check


def check_structure_label(header, body):
    wrong = [record for record in records_of(body, "label")
             if record["kind"] != "structure-health" or record["type"] != "STRUCTURE"]
    return first_error(
        check_game_screen(body),
        f"unexpected label records {wrong[:3]}" if wrong else None,
        check_scene_rules(header, body),
    )


def check_outcome(header, body):
    return first_error(forbid_kinds(body, ("area", "label", "click")), require_text(body, OUTCOME_TEXT))


def check_options_game_main(header, body):
    return first_error(
        forbid_kinds(body, ("area", "label")),
        None if records_of(body, "gui") else "no gui records",
        *(require_text(body, text) for text in IN_GAME_OPTIONS_TEXTS),
        f"the status text {STATUS_TEXT!r} must not be shown before applying"
        if any(record["s"] == STATUS_TEXT for record in records_of(body, "text")) else None,
    )


def check_options_game_applied(header, body):
    return first_error(forbid_kinds(body, ("area", "label")), require_text(body, STATUS_TEXT),
                       require_text(body, "Mission select"))


def check_for(scene_id):
    fixed = {
        "structure-label-top": check_structure_label,
        "structure-label-right": check_structure_label,
        "outcome-win": check_outcome,
        "outcome-lose": check_outcome,
        "options-game-main-nosaves": check_options_game_main,
        "options-game-applied": check_options_game_applied,
    }
    if scene_id in fixed:
        return fixed[scene_id]
    for name, type_name in catalog.UNIT_TYPES:
        if scene_id == f"units-label-{name}":
            return check_unit_labels(type_name)
    raise ValueError(f"no check for scene {scene_id}")


def integers(record, keys):
    return all(type(record[key]) is int for key in keys)


def check_record(record):
    keys = RECORD_KEYS.get(record.get("k"))
    if keys is None or set(record) != keys:
        return f"unexpected record {record}"
    if not integers(record, RECT_KEYS):
        return f"x, y, w, h must be integers: {record}"
    if record["k"] in ("click", "area") and not isinstance(record["name" if record["k"] == "click" else "n"], str):
        return f"the name of a {record['k']} record must be a string: {record}"
    if record["k"] in ("click", "area") and (record["w"] <= 0 or record["h"] <= 0 or
                                           not inside(record, CANVAS_RECT)):
        return f"a {record['k']} record must have an area inside the canvas {CANVAS_RECT}: {record}"
    if record["k"] == "label":
        owner = record["owner"]
        if not isinstance(owner, dict) or set(owner) != set(RECT_KEYS) or not integers(owner, RECT_KEYS):
            return f"the owner of a label record must be integer x, y, w, h: {record}"
        if type(record["obj"]) is not int or record["obj"] < 0 or record["w"] < 0 or record["h"] < 0:
            return f"a label record must have obj >= 0, w >= 0 and h >= 0: {record}"
        if not isinstance(record["kind"], str) or not isinstance(record["type"], str):
            return f"kind and type of a label record must be strings: {record}"
    return None


def run_scene(game, scene):
    scene_id = scene["id"]
    try:
        result = game.run(["--ui-audit-scene", scene_id, "--ui-audit-out", str(game.out)])
    except subprocess.TimeoutExpired:
        return None, None, f"no exit within {support.TIMEOUT_SECONDS} seconds"
    if result.returncode != 0:
        return None, None, f"game exited with {result.returncode}\n{result.stdout}\n{result.stderr}"
    png = game.out / f"{scene_id}.png"
    log = game.out / f"{scene_id}.geometry.jsonl"
    if not png.is_file() or not log.is_file():
        return None, None, f"missing output: png={png.is_file()} log={log.is_file()}"
    try:
        size = support.png_size(png)
    except ValueError as error:
        return None, None, str(error)
    if size != (1024, 768):
        return None, None, f"unexpected PNG size {size[0]}x{size[1]}"
    if png.stat().st_size < MIN_PNG_BYTES:
        return None, None, f"the PNG is too small for a screen snapshot: {png.stat().st_size} bytes"
    lines = log.read_text(encoding="utf-8").split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    try:
        records = [json.loads(line, parse_constant=reject_constant) for line in lines]
    except ValueError as error:
        return None, None, f"a geometry line is not JSON: {error}"
    if not records or not all(isinstance(record, dict) for record in records):
        return None, None, "the geometry log must hold JSON objects"
    header = records[0]
    expected = dict(HEADER, scene=scene_id, game_screen=scene["game_screen"])
    if scene["game_screen"]:
        expected["map_viewport"] = MAP_VIEWPORT
    if not support.same_json({key: header.get(key) for key in expected}, expected) or \
            not isinstance(header.get("version"), str) or \
            (not scene["game_screen"] and "map_viewport" in header):
        return None, None, f"unexpected header {header}"
    body = records[1:]
    for record in body:
        error = check_record(record)
        if error:
            return None, None, error
    return header, body, None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    args = parser.parse_args()
    errors = []
    with support.GameRun(args.run_dir) as game:
        for scene in catalog.expected_scenes():
            scene_id = scene["id"]
            header, body, error = run_scene(game, scene)
            if error is None:
                error = check_for(scene_id)(header, body)
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

В константе `EXCLUSIONS` сразу после строки

```python
    "cRegion\tкласс данных области на карте завоевания, не экран; отрисовывается внутри cSelectYourNextConquestState\n"
```

и перед закрывающей скобкой `)` константы добавь ровно три строки:

```python
    "cMentatState\tэкран брифинга ментата; сцены режима названы классами ментатов AtreidesMentat, HarkonnenMentat, OrdosMentat, SardaukarMentat\n"
    "cTellHouseState\tэкран рассказа о Доме; сцены режима названы классом ментата BeneMentat\n"
    "cCreatorState\tсоздаёт и хранит состояния игры, не экран\n"
```

Другие строки этого файла не меняются. Другие файлы `tests/`, `tools/` и весь код вне `tests/` и `tools/` не меняются.

## Шаг 2. Прогоны — помощник `gpt-6-luna` `xhigh`

Все команды — из корня рабочей копии `/srv/dune/worktrees/u34`.

1. `python3 -m py_compile tests/ui_audit/ui_audit_part3a_catalog.py tests/ui_audit/ui_audit_part3a_scenes.py tools/ui-audit/tests/test_port_changes.py; echo exit=$?` — ожидается `exit=0`.
2. **Прогон H** — `LD_LIBRARY_PATH=$PWD/.tmp/deps/prefix/lib python3 -B tests/ui_audit/ui_audit_part3a_catalog.py --run-dir .tmp/out/run/bin > .tmp/p5g3at/run-h.log 2>&1; echo exit=$?`. Ожидается: `exit=1`; первая строка лога начинается с `Part 3a scenes differ: missing [` и содержит `'outcome-win'` и `; extra []`; в логе нет строки, содержащей `must not write preferences`.
3. **Прогон I** — `LD_LIBRARY_PATH=$PWD/.tmp/deps/prefix/lib timeout 1800 python3 -B tests/ui_audit/ui_audit_part3a_scenes.py --run-dir .tmp/out/run/bin > .tmp/p5g3at/run-i.log 2>&1; echo exit=$?`. Ожидается: `exit=1`; `grep -c 'game exited with 2' .tmp/p5g3at/run-i.log` выводит `24`; `grep -c 'ui-audit: unknown scene' .tmp/p5g3at/run-i.log` выводит `24`; в логе нет строки, содержащей `must not write preferences`.
4. **Прогон J** — `(cd tools/ui-audit && python3 -B -m unittest discover -s tests) > .tmp/p5g3at/run-j.log 2>&1; echo exit=$?`. Ожидается: `exit=1`; `grep -c '^FAIL: test_g_exclusions_text' .tmp/p5g3at/run-j.log` выводит `1`; последняя непустая строка лога — `FAILED (failures=1)`.
5. После прогонов — `rm -r tests/ui_audit/__pycache__ tools/ui-audit/__pycache__ tools/ui-audit/tests/__pycache__` для тех из этих папок, что появились.

Помощник сдаёт корневой нити каждую команду, её код выхода и вывод, первые 3 строки лога прогона H (каждая обрезана до 300 символов командой `cut -c1-300`), выводы двух `grep -c` прогона I, вывод `grep -c` и последние 3 строки лога прогона J.

Ошибка синтаксиса или импорта в файле шага 1 — корневая нить сверяет файл с текстом шага 1 и исправляет расхождение с ним, затем помощник повторяет шаг 2 с пункта 1. Другой код выхода или другая причина в прогоне H, I или J при файлах, совпадающих с текстом шага 1, — блок `## Q-P5G3AT-02` с этими строками и стоп. Ожидание теста под игру не подгоняй: тест, который требует правки текста шага 1, — тоже `## Q-P5G3AT-02`.

## Шаг 3. Заморозка — корневая нить

`sha256sum tests/ui_audit/ui_audit_part3a_catalog.py tests/ui_audit/ui_audit_part3a_scenes.py tests/ui_audit/ui_audit_runtime_support.py tools/ui-audit/check_scenes.py tools/ui-audit/check_geometry.py tools/ui-audit/check_screens.py tools/ui-audit/tests/test_port_changes.py > .tmp/p5g3at/tests.sha256`. После этой команды эти семь файлов не меняются.

Проверка: `git -c lfs.storage=$PWD/.tmp/p5g3at/lfs status --short` выводит ровно три строки: ` M tools/ui-audit/tests/test_port_changes.py`, `?? tests/ui_audit/ui_audit_part3a_catalog.py` и `?? tests/ui_audit/ui_audit_part3a_scenes.py`. Другие строки — блок `## Q-P5G3AT-03` с выводом и стоп.

## Сдача

Последнее сообщение — блок `## DONE-P5G3AT | <время UTC из date -u> | HEAD <sha>` по форме из правил ниже. В нём:

- каждая команда шага 2 с кодом выхода и выводом, первые 3 строки лога прогона H (до 300 символов каждая), выводы `grep -c` прогонов I и J и последние 3 строки лога прогона J;
- содержимое `.tmp/p5g3at/tests.sha256`;
- вывод `git status --short` из шага 3;
- список коммитов: один пункт — два новых файла и правка `test_port_changes.py` шага 1, сообщение на английском о приёмочных тестах части 3а режима отладки интерфейса: скрипты, которые запускают игру и проверяют каталог и записи сцен меток юнитов и зданий, исхода миссии и меню настроек в бою, и три новых исключения экранов в ожидании теста инструментов; последняя строка сообщения — `Behavior changes: none`;
- раздел «Рабочие места»: вывод `python3 /srv/dune/tools/task-places.py inventory .tmp/p5g3at --size`; у `.tmp/p5g3at` пометка `оставить — хэши тестов нужны исполнителю`. Папки `.tmp/out`, `.tmp/deps`, `.tmp/p5g2`, `.tmp/p5g2t` созданы до этой задачи и в раздел не входят. Ничего не удаляй, кроме папок `__pycache__` пункта 5 шага 2.

Числа в сдаче — только из вывода команд.

## Организация работы

- **Порядок:** раздел «Прочитать до работы» → `mkdir -p .tmp/p5g3at` → шаг 1 → шаг 2 → шаг 3 → сдача и стоп.
- **Параллельно:** шаги зависят друг от друга, параллельных дорожек нет.
- **Помощники:** один помощник `gpt-6-luna` `xhigh`, без вложенных: шаг 2 — команды, их коды выхода и выписка строк логов. Бриф дословно содержит раздел «Шаг 2», абзац «Комментарии в коде» и запрет менять файлы, кроме папок `__pycache__` пункта 5 шага 2 и файлов в `.tmp/p5g3at/`. Шаги 1 и 3, сверку файлов с текстом шага 1 и сдачу делает корневая нить; механику — команды и выписку логов — только помощник.
- **Остановки:** только на `## DONE-P5G3AT` и на блоках `## Q-P5G3AT-NN`. Команда оболочки дважды подряд не завершилась (нет кода выхода) — блок `## Q-P5G3AT-04` и стоп.
- **Рамка правок:** два новых файла и правка `tools/ui-audit/tests/test_port_changes.py` шага 1, папки `__pycache__` пункта 5 шага 2 и папка `.tmp/p5g3at/`. Игра пишет в `.tmp/out/run/bin/` и во временные папки скриптов; это не правка.

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
