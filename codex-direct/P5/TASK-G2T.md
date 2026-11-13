# Задание P5G2T — приёмочные тесты сцен меню, кампании, ментатов и титров (шаг П5г, часть 2)

Исполнитель: корневая нить Codex `gpt-6.1-sol` `high`; прогоны игры делает один помощник `gpt-6-luna` `xhigh`.

Рабочая копия: `/srv/dune/worktrees/u34`, ветка `codex/p5g2`, `HEAD` — `91416fb0c6aae877242d55e08559c32ec80de3e0` (вершина ветки порта после частей 1 и 4 шага П5г). Файлы Git LFS в этой рабочей копии — настоящие данные. Временные файлы — в `.tmp/p5g2t/`. Коммитов не делай: коммиты делает ведущий по списку из сдачи.

## Цель

Положить в рабочую копию два скрипта Python приёмочных тестов второй части шага П5г ровно в том виде, что в шаге 1, получить их красные прогоны H и I на установленной игре части 1 и заморозить тесты хэшем. Код игры и другие файлы рабочей копии не менять.

## Что уже решено

Вторая часть шага П5г добавляет в каталог режима отладки интерфейса (`ui-audit`) порта 107 сцен экранов вне боя: карту кампании, выбор Дома, выбор миссии, рассказ о Доме, брифинги ментатов, настройку схватки, меню настроек и титры, — и записи режима из кода этих экранов. Сцены Дома Сардаукаров добавлены там же, где у трёх Домов форка: в порту есть кампания Сардаукаров. Сцены боя, экрана исхода миссии и меню настроек во время миссии — часть 3; сцены сохранений — шаг П8.

Тесты пишутся до кода. Их потом выполняет другой исполнитель, который пишет код по тому же контракту и тесты не меняет. Скрипты запускают установленную игру и в CTest не входят: в CI нет данных Git LFS. Скрипты создают временную папку через `tempfile.TemporaryDirectory` в системной временной папке и удаляют её при выходе — это исключение из правила о папке задачи для прогонов H и I.

Сборка в этой задаче не нужна. Установленная игра — `.tmp/out/run/bin/d2tm`, сборка кода части 1 (ядро режима: каталог из одной сцены `main-menu`); на ней все сцены части 2 неизвестны, и оба скрипта должны упасть.

## Прочитать до работы

Прочитай целиком до первого действия, каждый файл отдельным вызовом, пути — от корня рабочей копии: `tests/ui_audit/ui_audit_runtime_support.py`, `tests/ui_audit/ui_audit_main_menu_png.py`, `tools/ui-audit/check_credits.py`.

## Контракт поведения

Этот раздел дословно входит и в задание исполнителя кода части 2.

Пункты 1–4 контракта части 1 действуют без изменений. Игра запускается так же, как в пункте 2 части 1: из каталога установки сборки порта (рабочий каталог процесса — этот каталог) с аргументами `-windowed -screenWidth 1024 -screenHeight 768` и аргументами режима; переменные среды `SDL_VIDEODRIVER=dummy`, `SDL_RENDER_DRIVER=software`, `SDL_AUDIODRIVER=dummy`, `XDG_DATA_HOME=<пустая временная папка>`; `LD_LIBRARY_PATH` задаёт вызывающий процесс. Три скрипта части 1 в `tests/ui_audit/` остаются зелёными.

5. **Каталог части 2.** В выводе `--ui-audit-list` у каждой сцены ровно ключи части 1. Среди сцен, у которых `group` — одна из `region`, `choose-house`, `select-mission`, `tellhouse`, `mentat`, `skirmish-setup`, `options-menu`, `credits`, нет двух с одним `id`, и эти сцены ровно совпадают по `id` и значениям всех ключей со 107 сценами таблицы ниже. У каждой из 107 сцен `game_screen` — `false`, `hud` — `false`, `hover` — `null`, `hd_only` — `false`, кроме `credits-4` и `credits-5`, у которых `hd_only` — `true`. `<дом>` — каждое из `atreides`, `harkonnen`, `ordos`, `sardaukar`; `<фаза>` — каждое из `speak`, `await`; `<Ментат>` — `AtreidesMentat`, `HarkonnenMentat`, `OrdosMentat`, `SardaukarMentat` для `<дом>` в том же порядке; `""` — пустая строка.

   | `id` | `group` | `state` | `screen` | `house` | `readiness` |
   |---|---|---|---|---|---|
   | `region-<дом>-intro-<n>`, n = 1, 2, 3 | `region` | `GAME_REGION` | `cSelectYourNextConquestState` | `<дом>` | `RegionIntroScene` |
   | `region-<дом>-conquer-<n>`, n = 3, 5, 7, 9 | `region` | `GAME_REGION` | `cSelectYourNextConquestState` | `<дом>` | `RegionConquerMessage` |
   | `region-<дом>-select-<n>`, n = 2, 3, 4, 5, 6, 7, 8, 9 | `region` | `GAME_REGION` | `cSelectYourNextConquestState` | `<дом>` | `RegionStateSelect` |
   | `choose-house` | `choose-house` | `GAME_SELECT_HOUSE` | `cChooseHouseState` | `""` | `StateSettled` |
   | `select-mission-<дом>` | `select-mission` | `GAME_MISSIONSELECT` | `cSelectMissionState` | `<дом>` | `StateSettled` |
   | `tellhouse-<дом>-<фаза>` | `tellhouse` | `GAME_TELLHOUSE` | `BeneMentat` | `<дом>` | `MentatFrozen` |
   | `mentat-briefing-<дом>-<фаза>` | `mentat` | `GAME_BRIEFING` | `<Ментат>` | `<дом>` | `MentatFrozen` |
   | `mentat-win-<дом>-<фаза>` | `mentat` | `GAME_WINBRIEF` | `<Ментат>` | `<дом>` | `MentatFrozen` |
   | `mentat-lose-<дом>-<фаза>` | `mentat` | `GAME_LOSEBRIEF` | `<Ментат>` | `<дом>` | `MentatFrozen` |
   | `skirmish-setup-random`, `skirmish-setup-ready-map` | `skirmish-setup` | `GAME_SETUPSKIRMISH` | `cSetupSkirmishState` | `""` | `FixedFrames(2, no readiness flag)` |
   | `options-menu-main`, `options-menu-applied` | `options-menu` | `GAME_OPTIONS` | `cOptionsState` | `""` | `FixedFrames(14, no readiness flag)` |
   | `credits-title`, `credits-1`, `credits-2`, `credits-3`, `credits-4`, `credits-5` | `credits` | `GAME_CREDITS` | `cCreditsState` | `""` | `CreditsScrollPosition` |

6. **Прогон сцены.** Для каждой из 107 сцен пункта 5 запуск с `--ui-audit-scene <id> --ui-audit-out <папка>` завершается с кодом выхода 0 не позже чем через 120 секунд; в `<папка>` есть файлы `<id>.png` и `<id>.geometry.jsonl`. PNG — 1024 × 768 точек, в нём есть блок `IDAT`, файл заканчивается блоком `IEND`, размер файла — не меньше 10 000 байт (снимок экрана, а не одноцветный кадр). Файл геометрии — текст UTF-8 из строк, разделённых символом `
` (после последней строки может стоять `
`); каждая строка — объект JSON без значений `NaN`, `Infinity` и `-Infinity`. Первая строка — заголовок: в нём значения ключей `k`, `scene`, `resolution`, `language`, `graphics`, `canvas`, `game_screen`, `render_scale`, `world_scale` равны `"header"`, `"<id>"`, `"1024x768"`, `"en"`, `"hd"`, `{"w": 800, "h": 600}`, `false`, `0`, `0`, а `version` — строка; другие ключи заголовка не проверяются. Каждая следующая строка — запись одного из четырёх видов ровно с такими ключами: `"k": "text"` — `k`, `s`, `x`, `y`, `w`, `h`, `box`; `"k": "gui"` — `k`, `t`, `x`, `y`, `w`, `h`; `"k": "click"` — `k`, `name`, `x`, `y`, `w`, `h`; `"k": "credit"` — `k`, `name`, `s`. У записей `text`, `gui` и `click` значения `x`, `y`, `w`, `h` — целые числа JSON. У каждой записи `click` прямоугольник лежит внутри холста: `w` > 0, `h` > 0, `x` ≥ 0, `y` ≥ 0, `x + w` ≤ 800, `y + h` ≤ 600. После всех запусков в папке `XDG_DATA_HOME` нет файла с именем `preferences.ini` ни на каком уровне вложенности.

7. **Записи сцен.** «Одна запись click `<имя>`» — ровно одна запись `"k": "click"` с этим `name`; «на весь холст» — `x` 0, `y` 0, `w` 800, `h` 600; «запись text `<строка>`» — запись `"k": "text"` с `s`, равным строке; прямоугольник A «внутри» прямоугольника B — `A.x` ≥ `B.x`, `A.y` ≥ `B.y`, `A.x + A.w` ≤ `B.x + B.w`, `A.y + A.h` ≤ `B.y + B.h`. `<вид>` — каждое из `briefing`, `win`, `lose`; `<Дом>` — `Atreides`, `Harkonnen`, `Ordos`, `Sardaukar` для `<дом>` в том же порядке.
   - `choose-house`: для каждой пары (`house-atreides`, `ATREIDES`), (`house-ordos`, `ORDOS`), (`house-harkonnen`, `HARKONNEN`), (`house-sardaukar`, `SARDAUKAR`), (`house-back`, `Back`) — одна запись click с этим именем и хотя бы одна запись text с этой строкой внутри прямоугольника этой записи click (порт рисует подписи карточек Домов и кнопки возврата внутри них, `src/gamestates/cChooseHouseState.cpp@91416fb:111-142` и функция `drawHdHouseCard`); запись text `CHOOSE YOUR HOUSE`.
   - Каждая сцена `select-mission-<дом>`: запись text `REPLAY MISSION`.
   - Каждая сцена `tellhouse-<дом>-speak` и `mentat-<вид>-<дом>-speak`: одна запись click `mentat-skip` на весь холст; нет записи text, у которой `s` начинается с `Do you wish to join house`.
   - Каждая сцена `tellhouse-<дом>-await`: нет записи click `mentat-skip`; есть запись text `Do you wish to join house <Дом> ?`.
   - Каждая сцена `mentat-<вид>-<дом>-await`: нет записи click `mentat-skip`.
   - `skirmish-setup-ready-map`: записи click `skirmish-house:<r>`, `skirmish-credits:<r>`, `skirmish-units:<r>`, `skirmish-team:<r>` для каждого r из 1, 2, 3, 4, записи click `skirmish-brain:3`, `skirmish-brain:4`, `skirmish-blooms`, `skirmish-worms`, `skirmish-tech-level`, `skirmish-detonate-blooms` и хотя бы одна запись click, у которой `name` начинается с `skirmish-map:`; нет записей click `skirmish-start-points`, `skirmish-brain:1`, `skirmish-brain:2`; запись text `Skirmish`.
   - `skirmish-setup-random`: записи click `skirmish-start-points`, `skirmish-house:1`, `skirmish-house:2`; нет записей click `skirmish-house:3`, `skirmish-brain:3`.
   - В обеих сценах схватки каждая запись click с `name` вида `skirmish-<столбец>:<r>`, где `<столбец>` — `brain`, `house`, `credits`, `units` или `team`, а r — номер строки игрока сцены (1–4 в `skirmish-setup-ready-map`, 1–2 в `skirmish-setup-random`), единственная со своим `name`, её `h` — 16, а `x` и `w` — по столбцу раскладки `SkirmishPlayerTableLayout` порта (`src/gamestates/cSetupSkirmishState.cpp@91416fb:64-84`): `brain` — 4 и 68, `house` — 72 и 94, `credits` — 166 и 89, `units` — 255 и 70, `team` — 325 и 75. Записи `skirmish-house:<r>` есть для каждой строки игрока сцены, по одной, и у записи строки r + 1 `y` ровно на 26 больше, чем у записи строки r.
   - `options-menu-main`: хотя бы одна запись `"k": "gui"`; нет записи text `Saved. Restart the game.`.
   - `options-menu-applied`: запись text `Saved. Restart the game.`.
   - Каждая сцена `region-<дом>-intro-<n>` и `region-<дом>-conquer-<n>`: нет записи click `campaign-region-map`.
   - Каждая сцена `region-<дом>-select-<n>`: одна запись click `campaign-region-map`.
   - Каждая из шести сцен `credits-*`: одна запись click `credits-speed-up` на весь холст; хотя бы одна запись `"k": "credit"`; у каждой записи text `y` ≥ 0 и `y + h` ≤ 600.

8. **Титры целиком.** Функция `check_credits.check_credits(<папка>)` из `tools/ui-audit/check_credits.py` порта, вызванная для папки с файлами геометрии шести сцен титров, возвращает число комбинаций 1 и пустой список проблем: каждая строка титров (запись `credit`) целиком видна хотя бы в одной сцене титров.

## Шаг 1. Тесты — корневая нить сама

Перед созданием файлов: `test ! -e tests/ui_audit/ui_audit_part2_catalog.py && test ! -e tests/ui_audit/ui_audit_part2_scenes.py` — код выхода 0, иначе блок `## Q-P5G2T-05` и стоп.

### Новый файл `tests/ui_audit/ui_audit_part2_catalog.py`

Ровно такого вида:

```python
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import ui_audit_runtime_support as support  # noqa: E402

SCENE_KEYS = {"id", "group", "state", "screen", "game_screen", "house", "hud", "hd_only", "hover", "readiness"}
HOUSES = ("atreides", "harkonnen", "ordos", "sardaukar")
MENTAT_SCREENS = {
    "atreides": "AtreidesMentat",
    "harkonnen": "HarkonnenMentat",
    "ordos": "OrdosMentat",
    "sardaukar": "SardaukarMentat",
}
MENTAT_KINDS = (("briefing", "GAME_BRIEFING"), ("win", "GAME_WINBRIEF"), ("lose", "GAME_LOSEBRIEF"))
PART2_GROUPS = {"region", "choose-house", "select-mission", "tellhouse", "mentat", "skirmish-setup", "options-menu",
                "credits"}
EXPECTED_COUNT = 107


def scene(scene_id, group, state, screen, house, readiness, hd_only=False):
    return {
        "id": scene_id,
        "group": group,
        "state": state,
        "screen": screen,
        "game_screen": False,
        "house": house,
        "hud": False,
        "hd_only": hd_only,
        "hover": None,
        "readiness": readiness,
    }


def expected_scenes():
    scenes = []
    for house in HOUSES:
        for number in (1, 2, 3):
            scenes.append(scene(f"region-{house}-intro-{number}", "region", "GAME_REGION",
                                "cSelectYourNextConquestState", house, "RegionIntroScene"))
        for number in (3, 5, 7, 9):
            scenes.append(scene(f"region-{house}-conquer-{number}", "region", "GAME_REGION",
                                "cSelectYourNextConquestState", house, "RegionConquerMessage"))
        for number in range(2, 10):
            scenes.append(scene(f"region-{house}-select-{number}", "region", "GAME_REGION",
                                "cSelectYourNextConquestState", house, "RegionStateSelect"))
    scenes.append(scene("choose-house", "choose-house", "GAME_SELECT_HOUSE", "cChooseHouseState", "", "StateSettled"))
    for house in HOUSES:
        scenes.append(scene(f"select-mission-{house}", "select-mission", "GAME_MISSIONSELECT", "cSelectMissionState",
                            house, "StateSettled"))
    for house in HOUSES:
        for phase in ("speak", "await"):
            scenes.append(scene(f"tellhouse-{house}-{phase}", "tellhouse", "GAME_TELLHOUSE", "BeneMentat", house,
                                "MentatFrozen"))
    for house in HOUSES:
        for kind, state in MENTAT_KINDS:
            for phase in ("speak", "await"):
                scenes.append(scene(f"mentat-{kind}-{house}-{phase}", "mentat", state, MENTAT_SCREENS[house], house,
                                    "MentatFrozen"))
    for variant in ("random", "ready-map"):
        scenes.append(scene(f"skirmish-setup-{variant}", "skirmish-setup", "GAME_SETUPSKIRMISH",
                            "cSetupSkirmishState", "", "FixedFrames(2, no readiness flag)"))
    for variant in ("main", "applied"):
        scenes.append(scene(f"options-menu-{variant}", "options-menu", "GAME_OPTIONS", "cOptionsState", "",
                            "FixedFrames(14, no readiness flag)"))
    for frame in ("title", "1", "2", "3", "4", "5"):
        scenes.append(scene(f"credits-{frame}", "credits", "GAME_CREDITS", "cCreditsState", "",
                            "CreditsScrollPosition", hd_only=frame in ("4", "5")))
    return scenes


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
    actual = [entry for entry in scenes if entry["group"] in PART2_GROUPS]
    ids = [entry["id"] for entry in actual]
    duplicates = sorted({scene_id for scene_id in ids if ids.count(scene_id) > 1})
    if duplicates:
        return f"Duplicate scene ids: {duplicates}"
    missing = sorted(set(expected) - set(ids))
    extra = sorted(set(ids) - set(expected))
    if missing or extra:
        return f"Part 2 scenes differ: missing {missing}; extra {extra}"
    for entry in actual:
        if not support.same_json(entry, expected[entry["id"]]):
            return f"Unexpected scene entry: {entry}\nexpected: {expected[entry['id']]}"
    return None


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

### Новый файл `tests/ui_audit/ui_audit_part2_scenes.py`

Ровно такого вида:

```python
import argparse
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools" / "ui-audit"))

import check_credits  # noqa: E402
import ui_audit_part2_catalog as catalog  # noqa: E402
import ui_audit_runtime_support as support  # noqa: E402

HEADER = {
    "k": "header",
    "resolution": "1024x768",
    "language": "en",
    "graphics": "hd",
    "canvas": {"w": 800, "h": 600},
    "game_screen": False,
    "render_scale": 0,
    "world_scale": 0,
}
RECORD_KEYS = {
    "text": {"k", "s", "x", "y", "w", "h", "box"},
    "gui": {"k", "t", "x", "y", "w", "h"},
    "click": {"k", "name", "x", "y", "w", "h"},
    "credit": {"k", "name", "s"},
}
RECT_KEYS = ("x", "y", "w", "h")
CANVAS_W = 800
CANVAS_H = 600
CANVAS_RECT = {"x": 0, "y": 0, "w": CANVAS_W, "h": CANVAS_H}
MIN_PNG_BYTES = 10000
HOUSE_NAMES = {"atreides": "Atreides", "harkonnen": "Harkonnen", "ordos": "Ordos", "sardaukar": "Sardaukar"}
HOUSE_CARDS = (
    ("house-atreides", "ATREIDES"),
    ("house-ordos", "ORDOS"),
    ("house-harkonnen", "HARKONNEN"),
    ("house-sardaukar", "SARDAUKAR"),
    ("house-back", "Back"),
)
STATUS_TEXT = "Saved. Restart the game."
SKIRMISH_COLUMNS = {"brain": (4, 68), "house": (72, 94), "credits": (166, 89), "units": (255, 70), "team": (325, 75)}
SKIRMISH_ROW_HEIGHT = 16
SKIRMISH_ROW_STEP = 26


def reject_constant(name):
    raise ValueError(f"{name} is not a JSON number")


def clicks_named(body, name):
    return [record for record in body if record["k"] == "click" and record["name"] == name]


def click_names(body):
    return {record["name"] for record in body if record["k"] == "click"}


def text_records(body):
    return [record for record in body if record["k"] == "text"]


def rect(record):
    return {key: record[key] for key in RECT_KEYS}


def inside(inner, outer):
    return (inner["x"] >= outer["x"] and inner["y"] >= outer["y"] and
            inner["x"] + inner["w"] <= outer["x"] + outer["w"] and
            inner["y"] + inner["h"] <= outer["y"] + outer["h"])


def one_click(body, name):
    found = clicks_named(body, name)
    if len(found) != 1:
        return None, f"expected one click record {name}, got {found}"
    return found[0], None


def canvas_click(body, name):
    record, error = one_click(body, name)
    if error:
        return error
    if not support.same_json(rect(record), CANVAS_RECT):
        return f"the click record {name} must cover the canvas {CANVAS_RECT}, got {rect(record)}"
    return None


def require_clicks(body, names):
    missing = sorted(set(names) - click_names(body))
    return f"missing click records {missing}" if missing else None


def forbid_clicks(body, names):
    present = sorted(set(names) & click_names(body))
    return f"unexpected click records {present}" if present else None


def require_text(body, text):
    return None if any(record["s"] == text for record in text_records(body)) else f"no text record {text!r}"


def forbid_text_prefix(body, prefix):
    found = [record["s"] for record in text_records(body) if record["s"].startswith(prefix)]
    return f"unexpected text records {found}" if found else None


def first_error(*errors):
    return next((error for error in errors if error), None)


def check_choose_house(body):
    for name, label in HOUSE_CARDS:
        record, error = one_click(body, name)
        if error:
            return error
        if not any(text["s"] == label and inside(text, record) for text in text_records(body)):
            return f"no text record {label!r} inside the click record {name} {rect(record)}"
    return require_text(body, "CHOOSE YOUR HOUSE")


def check_select_mission(body):
    return require_text(body, "REPLAY MISSION")


def check_speaking(body):
    return first_error(canvas_click(body, "mentat-skip"), forbid_text_prefix(body, "Do you wish to join house"))


def check_tellhouse_awaiting(house_name):
    def check(body):
        return first_error(forbid_clicks(body, ["mentat-skip"]),
                           require_text(body, f"Do you wish to join house {house_name} ?"))
    return check


def check_awaiting(body):
    return forbid_clicks(body, ["mentat-skip"])


def check_skirmish_rows(body, rows):
    for column, (x, width) in SKIRMISH_COLUMNS.items():
        for row in rows:
            name = f"skirmish-{column}:{row}"
            found = clicks_named(body, name)
            if not found:
                continue
            record = found[0]
            if len(found) != 1 or record["x"] != x or record["w"] != width or record["h"] != SKIRMISH_ROW_HEIGHT:
                return f"the click record {name} must be x={x} w={width} h={SKIRMISH_ROW_HEIGHT}, got {found}"
    houses = [clicks_named(body, f"skirmish-house:{row}") for row in rows]
    if any(len(found) != 1 for found in houses):
        return f"expected one click record skirmish-house:<row> for rows {rows}, got {houses}"
    tops = [found[0]["y"] for found in houses]
    steps = {lower - upper for upper, lower in zip(tops, tops[1:])}
    if steps != {SKIRMISH_ROW_STEP}:
        return f"each player row must lie {SKIRMISH_ROW_STEP} below the previous one, got tops {tops}"
    return None


def check_skirmish_ready_map(body):
    rows = (1, 2, 3, 4)
    required = [f"skirmish-{column}:{row}" for column in ("house", "credits", "units", "team") for row in rows]
    required += ["skirmish-brain:3", "skirmish-brain:4", "skirmish-blooms", "skirmish-worms", "skirmish-tech-level",
                 "skirmish-detonate-blooms"]
    maps = sorted(name for name in click_names(body) if name.startswith("skirmish-map:"))
    return first_error(
        require_clicks(body, required),
        forbid_clicks(body, ["skirmish-start-points", "skirmish-brain:1", "skirmish-brain:2"]),
        None if maps else "no click record skirmish-map:<index>",
        check_skirmish_rows(body, rows),
        require_text(body, "Skirmish"),
    )


def check_skirmish_random(body):
    return first_error(
        require_clicks(body, ["skirmish-start-points", "skirmish-house:1", "skirmish-house:2"]),
        forbid_clicks(body, ["skirmish-house:3", "skirmish-brain:3"]),
        check_skirmish_rows(body, (1, 2)),
    )


def check_options_main(body):
    if not any(record["k"] == "gui" for record in body):
        return "no gui records"
    if any(record["s"] == STATUS_TEXT for record in text_records(body)):
        return f"the status text {STATUS_TEXT!r} must not be shown before applying"
    return None


def check_options_applied(body):
    return require_text(body, STATUS_TEXT)


def check_region_without_map_click(body):
    return forbid_clicks(body, ["campaign-region-map"])


def check_region_select(body):
    return one_click(body, "campaign-region-map")[1]


def check_credits_scene(body):
    credits = [record for record in body if record["k"] == "credit"]
    outside = [record for record in text_records(body) if record["y"] < 0 or record["y"] + record["h"] > CANVAS_H]
    return first_error(
        canvas_click(body, "credits-speed-up"),
        None if credits else "no credit records",
        f"text records outside the canvas height {CANVAS_H}: {outside[:3]}" if outside else None,
    )


def check_for(scene_id):
    fixed = {
        "choose-house": check_choose_house,
        "skirmish-setup-ready-map": check_skirmish_ready_map,
        "skirmish-setup-random": check_skirmish_random,
        "options-menu-main": check_options_main,
        "options-menu-applied": check_options_applied,
    }
    if scene_id in fixed:
        return fixed[scene_id]
    if scene_id.startswith("select-mission-"):
        return check_select_mission
    if scene_id.startswith(("tellhouse-", "mentat-")):
        if scene_id.endswith("-speak"):
            return check_speaking
        if scene_id.startswith("tellhouse-"):
            return check_tellhouse_awaiting(HOUSE_NAMES[scene_id.split("-")[1]])
        return check_awaiting
    if scene_id.startswith("region-"):
        return check_region_select if "-select-" in scene_id else check_region_without_map_click
    if scene_id.startswith("credits-"):
        return check_credits_scene
    raise ValueError(f"no check for scene {scene_id}")


def check_record(record):
    keys = RECORD_KEYS.get(record.get("k"))
    if keys is None or set(record) != keys:
        return f"unexpected record {record}"
    if record["k"] in ("text", "gui", "click") and not all(type(record[key]) is int for key in RECT_KEYS):
        return f"x, y, w, h must be integers: {record}"
    if record["k"] == "click" and (record["w"] <= 0 or record["h"] <= 0 or not inside(record, CANVAS_RECT)):
        return f"a click record must have an area inside the canvas {CANVAS_RECT}: {record}"
    return None


def run_scene(game, scene_id):
    try:
        result = game.run(["--ui-audit-scene", scene_id, "--ui-audit-out", str(game.out)])
    except subprocess.TimeoutExpired:
        return None, f"no exit within {support.TIMEOUT_SECONDS} seconds"
    if result.returncode != 0:
        return None, f"game exited with {result.returncode}\n{result.stdout}\n{result.stderr}"
    png = game.out / f"{scene_id}.png"
    log = game.out / f"{scene_id}.geometry.jsonl"
    if not png.is_file() or not log.is_file():
        return None, f"missing output: png={png.is_file()} log={log.is_file()}"
    try:
        size = support.png_size(png)
    except ValueError as error:
        return None, str(error)
    if size != (1024, 768):
        return None, f"unexpected PNG size {size[0]}x{size[1]}"
    if png.stat().st_size < MIN_PNG_BYTES:
        return None, f"the PNG is too small for a screen snapshot: {png.stat().st_size} bytes"
    lines = log.read_text(encoding="utf-8").split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    try:
        records = [json.loads(line, parse_constant=reject_constant) for line in lines]
    except ValueError as error:
        return None, f"a geometry line is not JSON: {error}"
    if not records or not all(isinstance(record, dict) for record in records):
        return None, "the geometry log must hold JSON objects"
    header = records[0]
    expected = dict(HEADER, scene=scene_id)
    if not support.same_json({key: header.get(key) for key in expected}, expected) or \
            not isinstance(header.get("version"), str):
        return None, f"unexpected header {header}"
    body = records[1:]
    for record in body:
        error = check_record(record)
        if error:
            return None, error
    return body, None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    args = parser.parse_args()
    errors = []
    with support.GameRun(args.run_dir) as game:
        for scene in catalog.expected_scenes():
            scene_id = scene["id"]
            body, error = run_scene(game, scene_id)
            if error is None:
                error = check_for(scene_id)(body)
            if error:
                errors.append(f"{scene_id}: {error}")
        combos, problems = check_credits.check_credits(game.out)
        if combos != 1 or problems:
            errors.append(f"credits coverage: combos {combos}, problems {problems}")
        preferences = game.preferences_files()
        if preferences:
            errors.append(f"An audit run must not write preferences: {preferences}")
    for error in errors:
        print(error, file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
```

Другие файлы `tests/` и весь код вне `tests/` не меняются.

## Шаг 2. Прогоны — помощник `gpt-6-luna` `xhigh`

Все команды — из корня рабочей копии `/srv/dune/worktrees/u34`.

1. `python3 -m py_compile tests/ui_audit/ui_audit_part2_catalog.py tests/ui_audit/ui_audit_part2_scenes.py; echo exit=$?` — ожидается `exit=0`.
2. **Прогон H** — `LD_LIBRARY_PATH=$PWD/.tmp/deps/prefix/lib python3 -B tests/ui_audit/ui_audit_part2_catalog.py --run-dir .tmp/out/run/bin > .tmp/p5g2t/run-h.log 2>&1; echo exit=$?`. Ожидается: `exit=1`; первая строка лога начинается с `Part 2 scenes differ: missing [` и содержит `'choose-house'` и `; extra []`; в логе нет строки, содержащей `must not write preferences`.
3. **Прогон I** — `LD_LIBRARY_PATH=$PWD/.tmp/deps/prefix/lib timeout 1800 python3 -B tests/ui_audit/ui_audit_part2_scenes.py --run-dir .tmp/out/run/bin > .tmp/p5g2t/run-i.log 2>&1; echo exit=$?`. Ожидается: `exit=1`; `grep -c 'game exited with 2' .tmp/p5g2t/run-i.log` выводит `107`; `grep -c 'ui-audit: unknown scene' .tmp/p5g2t/run-i.log` выводит `107`; последняя строка лога — `credits coverage: combos 0, problems []`; в логе нет строки, содержащей `must not write preferences`.
4. После прогонов — `rm -r tests/ui_audit/__pycache__`, если такая папка появилась.

Помощник сдаёт корневой нити каждую команду, её код выхода и вывод, первые 3 строки лога прогона H (каждая обрезана до 300 символов командой `cut -c1-300`) и последние 3 строки лога прогона I.

Ошибка синтаксиса или импорта в файле шага 1 — корневая нить сверяет файл с текстом шага 1 и исправляет расхождение с ним, затем помощник повторяет шаг 2 с пункта 1. Другой код выхода или другая причина в прогоне H или I при файлах, совпадающих с текстом шага 1, — блок `## Q-P5G2T-02` с этими строками и стоп. Ожидание теста под игру не подгоняй: тест, который требует правки текста шага 1, — тоже `## Q-P5G2T-02`.

## Шаг 3. Заморозка — корневая нить

`sha256sum tests/ui_audit/ui_audit_part2_catalog.py tests/ui_audit/ui_audit_part2_scenes.py tests/ui_audit/ui_audit_runtime_support.py tools/ui-audit/check_credits.py > .tmp/p5g2t/tests.sha256`. После этой команды эти четыре файла не меняются.

Проверка: `git -c lfs.storage=$PWD/.tmp/p5g2t/lfs status --short` выводит ровно две строки: `?? tests/ui_audit/ui_audit_part2_catalog.py` и `?? tests/ui_audit/ui_audit_part2_scenes.py`. Другие строки — блок `## Q-P5G2T-03` с выводом и стоп.

## Сдача

Последнее сообщение — блок `## DONE-P5G2T | <время UTC из date -u> | HEAD <sha>` по форме из правил ниже. В нём:

- каждая команда шага 2 с кодом выхода и выводом, первые 3 строки лога прогона H (до 300 символов каждая) и последние 3 строки лога прогона I;
- содержимое `.tmp/p5g2t/tests.sha256`;
- вывод `git status --short` из шага 3;
- список коммитов: один пункт — два новых файла шага 1, сообщение на английском о приёмочных тестах второй части режима отладки интерфейса: скрипты, которые запускают игру и проверяют каталог сцен меню, кампании, ментатов и титров и записи всех 107 сцен; последняя строка сообщения — `Behavior changes: none`;
- раздел «Рабочие места»: вывод `python3 /srv/dune/tools/task-places.py inventory .tmp/p5g2t --size`; у `.tmp/p5g2t` пометка `оставить — хэши тестов нужны исполнителю`. Папки `.tmp/out` и `.tmp/deps` созданы до этой задачи и в раздел не входят. Ничего не удаляй, кроме папки `tests/ui_audit/__pycache__`.

Числа в сдаче — только из вывода команд.

## Организация работы

- **Порядок:** раздел «Прочитать до работы» → шаг 1 → шаг 2 → шаг 3 → сдача и стоп.
- **Параллельно:** шаги зависят друг от друга, параллельных дорожек нет.
- **Помощники:** один помощник `gpt-6-luna` `xhigh`, без вложенных: шаг 2 — команды, их коды выхода и выписка строк логов. Бриф дословно содержит раздел «Шаг 2», абзац «Комментарии в коде» и запрет менять файлы, кроме папки `tests/ui_audit/__pycache__` и файлов в `.tmp/p5g2t/`. Шаги 1 и 3, сверку файлов с текстом шага 1 и сдачу делает корневая нить; механику — команды и выписку логов — только помощник.
- **Остановки:** только на `## DONE-P5G2T` и на блоках `## Q-P5G2T-NN`. Команда оболочки дважды подряд не завершилась (нет кода выхода) — блок `## Q-P5G2T-04` и стоп.
- **Рамка правок:** два новых файла шага 1, папка `tests/ui_audit/__pycache__` и папка `.tmp/p5g2t/`. Игра пишет в `.tmp/out/run/bin/` и во временные папки скриптов; это не правка.

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
