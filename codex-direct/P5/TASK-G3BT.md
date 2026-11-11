# Задание P5G3BT — приёмочные тесты сцен базы в бою (шаг П5г, часть 3б)

Исполнитель: корневая нить Codex `gpt-6.1-sol` `high`; прогоны игры и тестов делает один помощник `gpt-6-luna` `xhigh`.

Рабочая копия: `/srv/dune/worktrees/u34`, ветка `codex/p5g3b`, `HEAD` — `af6a2e1e4f2baba4ff52e4812c7dc798cfd46aaf` (часть 3а шага П5г). Файлы Git LFS в этой рабочей копии — настоящие данные. Временные файлы — в `.tmp/p5g3bt/`. Коммитов не делай: коммиты делает ведущий по списку из сдачи.

## Цель

Положить в рабочую копию два скрипта Python приёмочных тестов части 3б шага П5г ровно в том виде, что в шаге 1, получить красные прогоны H и I и заморозить тесты хэшем. Код игры и другие файлы рабочей копии не менять.

## Что уже решено

Часть 3б шага П5г добавляет в каталог режима отладки интерфейса (`ui-audit`) порта 35 сцен базы в бою: интерфейс боя с радаром, выделенное здание, списки построек шести видов для Домов Атрейдес, Харконнен, Ордос и Сардаукар, мини-карта без радара и без энергии, установка здания на разрешённое и запрещённое место, выделение группы рамкой, сообщение и уведомления, наведение на карточку списка, список, прокрученный до конца, и точка сбора. Сцены идут в бою области 22 на базе со всеми зданиями и уровнем технологий 9, как у форка (`src/debug/UiAuditAccess.cpp@9208dcf:641-934`). Сцены форка `game-music` и `game-command-*` сюда не входят: музыка — шаг П9, панель команд — шаг П10.

Своих правил для этих сцен у форка нет. Поэтому к записям частей 1–3а режим порта добавляет пять новых, по которым проверяется смысл сцены: метки `structure-selected` (выделенное здание), `rally-point` (точка сбора), `place-cell` (клетка установки здания с её цветом `GOOD`, `NEUTRAL` или `BAD` — так порт красит клетки, `src/drawers/cPlaceItDrawer.cpp@af6a2e1:137-184`), `card-hover` (карточка списка под курсором) и область `selection-box` (рамка выделения группы). Их вводит код части 3б; этим тестам они нужны как ожидания.

Тесты пишутся до кода. Их потом выполняет другой исполнитель, который пишет код по тому же контракту и тесты не меняет. Скрипты запускают установленную игру и в CTest не входят: в CI нет данных Git LFS. Скрипты создают временную папку через `tempfile.TemporaryDirectory` в системной временной папке и удаляют её при выходе — это исключение из правила о папке задачи для прогонов H и I.

Сборка в этой задаче не нужна. Установленная игра — `.tmp/out/run/bin/d2tm`, сборка части 3а (132 сцены, сцен части 3б нет); на ней все сцены части 3б неизвестны, и оба скрипта должны упасть. Ведущий проверил оба скрипта на поддельной игре: зелёный прогон по контракту и 24 атаки — каждая падает по своей причине.

## Прочитать до работы

Прочитай целиком до первого действия, каждый файл отдельным вызовом, пути — от корня рабочей копии: `tests/ui_audit/ui_audit_runtime_support.py`, `tests/ui_audit/ui_audit_part3a_catalog.py`, `tests/ui_audit/ui_audit_part3a_scenes.py`, `tools/ui-audit/check_screens.py`.

## Контракт поведения

Этот раздел дословно входит и в задание исполнителя кода части 3б.

Пункты 1–12 контрактов частей 1, 2 и 3а действуют без изменений; скрипты частей 1, 2, 3а и 4 в `tests/ui_audit/` остаются зелёными. Игра запускается так же, как в пункте 2 части 1.

13. **Каталог части 3б.** В выводе `--ui-audit-list` у каждой сцены ровно ключи части 1. Среди сцен, у которых `id` начинается с `game-`, нет двух с одним `id`, и эти сцены ровно совпадают по `id` и значениям всех ключей с 35 сценами ниже. У каждой из 35 сцен `group` — `game-playing`, `state` — `GAME_PLAYING`, `screen` — `cGamePlaying`, `game_screen` — `true`, `readiness` — `FixedFrames(5, no readiness flag)`; `hud` — `true` только у `game-hud`; `hd_only` — `true` только у `game-list-scroll-end`; `hover` — `{"x": 0, "y": 0}` у `game-place-allowed`, `game-place-forbidden`, `game-group-select` и `game-item-hover` и `null` у остальных; `house` — `harkonnen` у сцен `game-harkonnen-list-<вид>`, `ordos` у `game-ordos-list-<вид>`, `sardaukar` у `game-sardaukar-list-<вид>` и `atreides` у остальных. Сцены: `game-list-<вид>`, `game-harkonnen-list-<вид>`, `game-ordos-list-<вид>`, `game-sardaukar-list-<вид>` (`<вид>` — каждое из `build`, `infantry`, `vehicles`, `starport`, `palace`, `upgrades`), `game-hud`, `game-structure-selected`, `game-radar-none`, `game-radar-nopower`, `game-place-allowed`, `game-place-forbidden`, `game-group-select`, `game-messages`, `game-item-hover`, `game-list-scroll-end`, `game-rally-point`. Покрытие экранов — как в пункте 10: итоговый список содержит только восемь строк экранов части 3в.

14. **Прогон сцены части 3б.** Для каждой из 35 сцен пункта 13 — всё, что пункт 11 требует от сцен части 3а с `game_screen` `true`: код выхода 0 не позже чем через 120 секунд, файлы `<id>.png` и `<id>.geometry.jsonl`, PNG и заголовок как там, ключ `map_viewport` со значением `{"x": 0, "y": 42, "w": 520, "h": 558}`, записи пяти видов с теми же ключами и ограничениями, нет файла `preferences.ini` в папке `XDG_DATA_HOME`.

15. **Записи сцен части 3б.** «Одна запись», «внутри» и «прямоугольник (x, y, w, h)» — как в пункте 12; у записи `label` её имя — значение `kind`. Прямоугольники A и B «пересекаются», если `A.x < B.x + B.w`, `B.x < A.x + A.w`, `A.y < B.y + B.h` и `B.y < A.y + A.h`. «Номер» записи click `list-button:<n>` или `build-item:<n>` — число `<n>`.
    - Каждая сцена части 3б:
      - одна запись area `top-panel` с прямоугольником (0, 0, 800, 42); одна запись area `sidebar` с прямоугольником (520, 42, 280, 558); одна запись area `build-list` внутри прямоугольника `sidebar`; одна запись click `top-options` с прямоугольником (7, 4, 126, 33); нет записи click `order-button`;
      - каждая запись click, у которой `name` начинается с `list-button:` или `build-item:` либо равно `build-scrollbar`, лежит внутри прямоугольника `sidebar`; есть хотя бы одна запись click, у которой `name` начинается с `list-button:` или `build-item:`;
      - у каждой записи label `kind` — одно из `structure-health`, `structure-selected`, `rally-point`, `place-cell`, `card-hover` (меток юнитов нет: юниты базы не выделены);
      - запись area `selection-box` есть только у `game-group-select`; записи label `place-cell` — только у `game-place-allowed` и `game-place-forbidden`; `card-hover` — только у `game-item-hover`; `structure-selected` — только у `game-structure-selected` и `game-rally-point`; `rally-point` — только у `game-rally-point`.
    - Радар. У каждой сцены, кроме `game-radar-none`, одна запись area `minimap` внутри прямоугольника `sidebar` и одна запись click `minimap` с тем же прямоугольником (у игрока есть радар; в `game-radar-nopower` ему не хватает энергии, и порт всё равно рисует мини-карту, `src/drawers/cMiniMapDrawer.cpp@dc6e5ff:116-130`). У `game-radar-none` нет записей area и click `minimap`.
    - Списки. У сцены `game-list-<вид>`, `game-harkonnen-list-<вид>`, `game-ordos-list-<вид>`, `game-sardaukar-list-<вид>` выбран список с номером `<n>`: `build` — 1, `infantry` — 2, `vehicles` — 3, `starport` — 4, `palace` — 5, `upgrades` — 6 (номера списков порта, `src/include/enums/ListEnums.h@af6a2e1:44-63`). У такой сцены нет записи click `list-button:<n>` (кнопку выбранного списка режим не записывает, `src/debug/UiAuditAccess.cpp@af6a2e1:297-309`); есть хотя бы одна запись click `list-button:<m>`; номер каждой записи click `list-button:<m>` — целое от 1 до 6; есть хотя бы одна запись click `build-item:<i>`.
    - `game-structure-selected`: одна запись label `structure-selected`; её `type` — `STRUCTURE`, `w` > 0, `h` > 0.
    - `game-rally-point`: одна запись label `structure-selected` с тем же требованием и одна запись label `rally-point`, у которой `type` — `STRUCTURE`, `w` > 0, `h` > 0, `obj` равно `obj` записи `structure-selected`, а её прямоугольник не пересекается с прямоугольником её `owner` (точка сбора стоит на клетке в стороне от здания).
    - `game-place-allowed`: ровно четыре записи label `place-cell` (ветряная электростанция — 2 × 2 клетки), у всех одно значение `obj`, у каждой `w` > 0 и `h` > 0, `type` каждой — `GOOD` или `NEUTRAL`.
    - `game-place-forbidden`: ровно четыре записи label `place-cell`, у всех одно значение `obj`, у каждой `w` > 0 и `h` > 0, `type` каждой — `GOOD`, `NEUTRAL` или `BAD`, и хотя бы у одной — `BAD`.
    - `game-group-select`: одна запись area `selection-box` внутри прямоугольника (0, 42, 520, 558) — области карты.
    - `game-messages`: записи text, у которых `s` равно `Construction complete: the Windtrap is ready to be placed`, `Neutral notification`, `Priority notification: Harvester is full` и `Bad news: a structure is under attack` — по одной на каждую из четырёх строк.
    - `game-item-hover`: одна запись label `card-hover`; её `obj` — 2, `type` — `ITEM`; точка (x + w // 2, y + h // 2) её прямоугольника лежит в прямоугольнике единственной записи click `build-item:2` (`X ≤ x < X + W`, `Y ≤ y < Y + H`).
    - `game-list-scroll-end`: одна запись click `build-scrollbar`; есть хотя бы одна запись click `build-item:<i>`; нет записи click `build-item:0`; наибольший номер записей click `build-item:<i>` этой сцены больше наибольшего номера записей click `build-item:<i>` сцены `game-list-build`.

## Шаг 1. Тесты — корневая нить сама

Перед созданием файлов: `test ! -e tests/ui_audit/ui_audit_part3b_catalog.py && test ! -e tests/ui_audit/ui_audit_part3b_scenes.py && git branch --show-current` — код выхода 0 и вывод `codex/p5g3b`, иначе блок `## Q-P5G3BT-05` и стоп.

### Новый файл `tests/ui_audit/ui_audit_part3b_catalog.py`

Ровно такого вида:

```python
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import ui_audit_part3a_catalog as part3a  # noqa: E402
import ui_audit_runtime_support as support  # noqa: E402

LIST_KINDS = (("build", 1), ("infantry", 2), ("vehicles", 3), ("starport", 4), ("palace", 5), ("upgrades", 6))
HOUSE_LIST_PREFIXES = (("atreides", "game-list-"), ("harkonnen", "game-harkonnen-list-"),
                       ("ordos", "game-ordos-list-"), ("sardaukar", "game-sardaukar-list-"))
HOVER_SCENES = ("game-place-allowed", "game-place-forbidden", "game-group-select", "game-item-hover")
BASE_SCENES = ("game-hud", "game-structure-selected", "game-radar-none", "game-radar-nopower", "game-place-allowed",
               "game-place-forbidden", "game-group-select", "game-messages", "game-item-hover",
               "game-list-scroll-end", "game-rally-point")
EXPECTED_COUNT = 35


def game_scene(scene_id, house="atreides"):
    entry = part3a.scene(scene_id, "game-playing", "GAME_PLAYING", "cGamePlaying", house, part3a.GAME_READINESS,
                         game_screen=True, hover={"x": 0, "y": 0} if scene_id in HOVER_SCENES else None)
    entry["hud"] = scene_id == "game-hud"
    entry["hd_only"] = scene_id == "game-list-scroll-end"
    return entry


def expected_scenes():
    scenes = [game_scene(f"{prefix}{kind}", house) for house, prefix in HOUSE_LIST_PREFIXES for kind, _ in LIST_KINDS]
    return scenes + [game_scene(scene_id) for scene_id in BASE_SCENES]


def in_part3b(entry):
    scene_id = entry["id"]
    return isinstance(scene_id, str) and scene_id.startswith("game-")


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
    actual = [entry for entry in scenes if in_part3b(entry)]
    ids = [entry["id"] for entry in actual]
    duplicates = sorted({scene_id for scene_id in ids if ids.count(scene_id) > 1})
    if duplicates:
        return f"Duplicate scene ids: {duplicates}"
    missing = sorted(set(expected) - set(ids))
    extra = sorted(set(ids) - set(expected))
    if missing or extra:
        return f"Part 3b scenes differ: missing {missing}; extra {extra}"
    for entry in actual:
        if not support.same_json(entry, expected[entry["id"]]):
            return f"Unexpected scene entry: {entry}\nexpected: {expected[entry['id']]}"
    return part3a.check_coverage(scenes)


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

### Новый файл `tests/ui_audit/ui_audit_part3b_scenes.py`

Ровно такого вида:

```python
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import ui_audit_part3a_scenes as base  # noqa: E402
import ui_audit_part3b_catalog as catalog  # noqa: E402
import ui_audit_runtime_support as support  # noqa: E402

MESSAGE_TEXT = "Construction complete: the Windtrap is ready to be placed"
NOTIFICATION_TEXTS = ("Neutral notification", "Priority notification: Harvester is full",
                      "Bad news: a structure is under attack")
LABEL_KINDS = {"structure-health", "structure-selected", "rally-point", "place-cell", "card-hover"}
OWN_RECORDS = {
    ("area", "selection-box"): {"game-group-select"},
    ("label", "place-cell"): {"game-place-allowed", "game-place-forbidden"},
    ("label", "card-hover"): {"game-item-hover"},
    ("label", "structure-selected"): {"game-structure-selected", "game-rally-point"},
    ("label", "rally-point"): {"game-rally-point"},
}
NAME_KEYS = {"area": "n", "click": "name", "label": "kind"}
PLACE_CELLS = 4
HOVERED_ITEM = 2
LIST_BUTTON = "list-button:"
BUILD_ITEM = "build-item:"


def named(body, kind, name):
    return [record for record in base.records_of(body, kind) if record[NAME_KEYS[kind]] == name]


def one_label(body, kind):
    found = named(body, "label", kind)
    if len(found) != 1:
        return None, f"expected one label record {kind}, got {found}"
    return found[0], None


def numbers(body, prefix):
    found = []
    for record in base.records_of(body, "click"):
        if record["name"].startswith(prefix):
            suffix = record["name"][len(prefix):]
            found.append(int(suffix) if suffix.isdigit() else -1)
    return found


def visible(record):
    return record["w"] > 0 and record["h"] > 0


def intersects(a, b):
    return (a["x"] < b["x"] + b["w"] and b["x"] < a["x"] + a["w"] and
            a["y"] < b["y"] + b["h"] and b["y"] < a["y"] + a["h"])


def check_radar(scene_id, body):
    areas = named(body, "area", "minimap")
    clicks = named(body, "click", "minimap")
    if scene_id == "game-radar-none":
        return f"unexpected minimap records {areas + clicks}" if areas or clicks else None
    if len(areas) != 1 or len(clicks) != 1:
        return f"expected one area and one click record minimap, got {areas} and {clicks}"
    if not base.inside(areas[0], base.SIDEBAR):
        return f"the area record minimap lies outside {base.SIDEBAR}: {areas[0]}"
    if not support.same_json(base.rect(areas[0]), base.rect(clicks[0])):
        return f"the click record minimap {base.rect(clicks[0])} differs from the area {base.rect(areas[0])}"
    return None


def check_common(scene_id, body):
    build_list, error = base.one_record(body, "area", "n", "build-list")
    if error:
        return error
    sidebar_clicks = [record for record in base.records_of(body, "click")
                      if record["name"].startswith(base.SIDEBAR_CLICK_PREFIXES) or record["name"] == "build-scrollbar"]
    outside = [record for record in sidebar_clicks if not base.inside(record, base.SIDEBAR)]
    wrong_labels = [record for record in base.records_of(body, "label") if record["kind"] not in LABEL_KINDS]
    foreign = sorted(f"{kind} {name}" for (kind, name), owners in OWN_RECORDS.items()
                     if scene_id not in owners and named(body, kind, name))
    return base.first_error(
        base.exact_rect(body, "area", "n", "top-panel", base.TOP_PANEL),
        base.exact_rect(body, "area", "n", "sidebar", base.SIDEBAR),
        None if base.inside(build_list, base.SIDEBAR)
        else f"the area record build-list lies outside {base.SIDEBAR}: {build_list}",
        base.exact_rect(body, "click", "name", "top-options", base.TOP_OPTIONS),
        base.forbid_clicks(body, ["order-button"]),
        f"sidebar click records outside {base.SIDEBAR}: {outside[:3]}" if outside else None,
        None if any(record["name"].startswith(base.SIDEBAR_CLICK_PREFIXES) for record in sidebar_clicks)
        else "no click record list-button:<n> or build-item:<n>",
        f"unexpected label records {wrong_labels[:3]}" if wrong_labels else None,
        f"records that belong to other scenes: {foreign}" if foreign else None,
        check_radar(scene_id, body),
    )


def check_nothing_more(scene_id, header, body, bodies):
    return None


def check_list(number):
    def check(scene_id, header, body, bodies):
        buttons = numbers(body, LIST_BUTTON)
        return base.first_error(
            f"the selected list {number} has a click record {LIST_BUTTON}{number}" if number in buttons else None,
            None if buttons else f"no click record {LIST_BUTTON}<n>",
            f"list button numbers outside 1..6: {sorted(buttons)}" if any(not 1 <= n <= 6 for n in buttons) else None,
            None if numbers(body, BUILD_ITEM) else f"no click record {BUILD_ITEM}<n>",
        )
    return check


def check_structure_selected(scene_id, header, body, bodies):
    selected, error = one_label(body, "structure-selected")
    if error:
        return error
    if selected["type"] != "STRUCTURE" or not visible(selected):
        return f"the label record structure-selected must have type STRUCTURE, w > 0 and h > 0: {selected}"
    return None


def check_rally_point(scene_id, header, body, bodies):
    error = check_structure_selected(scene_id, header, body, bodies)
    if error:
        return error
    selected = named(body, "label", "structure-selected")[0]
    rally, error = one_label(body, "rally-point")
    if error:
        return error
    if rally["type"] != "STRUCTURE" or not visible(rally) or rally["obj"] != selected["obj"]:
        return f"the label record rally-point must have type STRUCTURE, w > 0, h > 0 and obj {selected['obj']}: {rally}"
    if intersects(rally, rally["owner"]):
        return f"the rally point {base.rect(rally)} overlaps its building {rally['owner']}"
    return None


def check_place(allowed_types, needs_bad):
    def check(scene_id, header, body, bodies):
        cells = named(body, "label", "place-cell")
        if len(cells) != PLACE_CELLS:
            return f"expected {PLACE_CELLS} label records place-cell, got {len(cells)}: {cells}"
        types = {record["type"] for record in cells}
        return base.first_error(
            None if len({record["obj"] for record in cells}) == 1
            else f"the place-cell records name different structures: {cells}",
            None if all(visible(record) for record in cells) else f"place-cell records need w > 0 and h > 0: {cells}",
            None if types <= allowed_types else f"unexpected place-cell types {sorted(types)}",
            None if not needs_bad or "BAD" in types else "no place-cell record of type BAD",
        )
    return check


def check_group_select(scene_id, header, body, bodies):
    boxes = named(body, "area", "selection-box")
    if len(boxes) != 1:
        return f"expected one area record selection-box, got {boxes}"
    if not base.inside(boxes[0], base.MAP_VIEWPORT):
        return f"the selection box lies outside the map {base.MAP_VIEWPORT}: {boxes[0]}"
    return None


def check_messages(scene_id, header, body, bodies):
    return base.first_error(*(base.require_text(body, text) for text in (MESSAGE_TEXT,) + NOTIFICATION_TEXTS))


def check_item_hover(scene_id, header, body, bodies):
    hover, error = one_label(body, "card-hover")
    if error:
        return error
    if hover["obj"] != HOVERED_ITEM or hover["type"] != "ITEM":
        return f"the label record card-hover must have obj {HOVERED_ITEM} and type ITEM: {hover}"
    card, error = base.one_record(body, "click", "name", f"{BUILD_ITEM}{HOVERED_ITEM}")
    if error:
        return error
    x = hover["x"] + hover["w"] // 2
    y = hover["y"] + hover["h"] // 2
    if not (card["x"] <= x < card["x"] + card["w"] and card["y"] <= y < card["y"] + card["h"]):
        return f"the hovered card {base.rect(hover)} is not the card {base.rect(card)}"
    return None


def check_scroll_end(scene_id, header, body, bodies):
    items = numbers(body, BUILD_ITEM)
    first_items = numbers(bodies.get("game-list-build", []), BUILD_ITEM)
    return base.first_error(
        base.one_record(body, "click", "name", "build-scrollbar")[1],
        None if items else f"no click record {BUILD_ITEM}<n>",
        f"the list is not scrolled: the click record {BUILD_ITEM}0 is present" if 0 in items else None,
        None if items and first_items and max(items) > max(first_items)
        else f"the last card {max(items, default=None)} does not pass the last card "
             f"{max(first_items, default=None)} of game-list-build",
    )


def check_for(scene_id):
    fixed = {
        "game-hud": check_nothing_more,
        "game-radar-none": check_nothing_more,
        "game-radar-nopower": check_nothing_more,
        "game-structure-selected": check_structure_selected,
        "game-rally-point": check_rally_point,
        "game-place-allowed": check_place({"GOOD", "NEUTRAL"}, False),
        "game-place-forbidden": check_place({"GOOD", "NEUTRAL", "BAD"}, True),
        "game-group-select": check_group_select,
        "game-messages": check_messages,
        "game-item-hover": check_item_hover,
        "game-list-scroll-end": check_scroll_end,
    }
    if scene_id in fixed:
        return fixed[scene_id]
    for _, prefix in catalog.HOUSE_LIST_PREFIXES:
        for kind, number in catalog.LIST_KINDS:
            if scene_id == f"{prefix}{kind}":
                return check_list(number)
    raise ValueError(f"no check for scene {scene_id}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    args = parser.parse_args()
    errors = []
    with support.GameRun(args.run_dir) as game:
        results = {scene["id"]: base.run_scene(game, scene) for scene in catalog.expected_scenes()}
        bodies = {scene_id: body for scene_id, (_, body, error) in results.items() if error is None}
        for scene_id, (header, body, error) in results.items():
            if error is None:
                error = check_common(scene_id, body) or check_for(scene_id)(scene_id, header, body, bodies)
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

Другие файлы `tests/`, `tools/` и весь код вне `tests/` и `tools/` не меняются.

## Шаг 2. Прогоны — помощник `gpt-6-luna` `xhigh`

Все команды — из корня рабочей копии `/srv/dune/worktrees/u34`.

1. `mkdir -p .tmp/p5g3bt && python3 -m py_compile tests/ui_audit/ui_audit_part3b_catalog.py tests/ui_audit/ui_audit_part3b_scenes.py; echo exit=$?` — ожидается `exit=0`.
2. **Прогон H** — `LD_LIBRARY_PATH=$PWD/.tmp/deps/prefix/lib python3 -B tests/ui_audit/ui_audit_part3b_catalog.py --run-dir .tmp/out/run/bin > .tmp/p5g3bt/run-h.log 2>&1; echo exit=$?`. Ожидается: `exit=1`; первая строка лога начинается с `Part 3b scenes differ: missing [` и содержит `'game-hud'`, `'game-sardaukar-list-upgrades'` и `; extra []`; в логе нет строки, содержащей `must not write preferences`.
3. **Прогон I** — `LD_LIBRARY_PATH=$PWD/.tmp/deps/prefix/lib timeout 3000 python3 -B tests/ui_audit/ui_audit_part3b_scenes.py --run-dir .tmp/out/run/bin > .tmp/p5g3bt/run-i.log 2>&1; echo exit=$?`. Ожидается: `exit=1`; `grep -c 'game exited with 2' .tmp/p5g3bt/run-i.log` выводит `35`; `grep -c 'ui-audit: unknown scene' .tmp/p5g3bt/run-i.log` выводит `35`; в логе нет строки, содержащей `must not write preferences`.
4. После прогонов — `rm -r tests/ui_audit/__pycache__ tools/ui-audit/__pycache__` для тех из этих папок, что появились.

Помощник сдаёт корневой нити каждую команду, её код выхода и вывод, первые 3 строки лога прогона H (каждая обрезана до 300 символов командой `cut -c1-300`) и выводы двух `grep -c` прогона I.

Ошибка синтаксиса или импорта в файле шага 1 — корневая нить сверяет файл с текстом шага 1 и исправляет расхождение с ним, затем помощник повторяет шаг 2 с пункта 1. Другой код выхода или другая причина в прогоне H или I при файлах, совпадающих с текстом шага 1, — блок `## Q-P5G3BT-02` с этими строками и стоп. Ожидание теста под игру не подгоняй: тест, который требует правки текста шага 1, — тоже `## Q-P5G3BT-02`.

## Шаг 3. Заморозка — корневая нить

`sha256sum tests/ui_audit/ui_audit_part3b_catalog.py tests/ui_audit/ui_audit_part3b_scenes.py tests/ui_audit/ui_audit_part3a_catalog.py tests/ui_audit/ui_audit_part3a_scenes.py tests/ui_audit/ui_audit_runtime_support.py tools/ui-audit/check_scenes.py tools/ui-audit/check_geometry.py tools/ui-audit/check_screens.py > .tmp/p5g3bt/tests.sha256`. После этой команды эти восемь файлов не меняются.

Проверка: `git -c lfs.storage=$PWD/.tmp/p5g3bt/lfs status --short` выводит ровно две строки: `?? tests/ui_audit/ui_audit_part3b_catalog.py` и `?? tests/ui_audit/ui_audit_part3b_scenes.py`. Другие строки — блок `## Q-P5G3BT-03` с выводом и стоп.

## Сдача

Последнее сообщение — блок `## DONE-P5G3BT | <время UTC из date -u> | HEAD <sha>` по форме из правил ниже. В нём:

- каждая команда шага 2 с кодом выхода и выводом, первые 3 строки лога прогона H (до 300 символов каждая) и выводы двух `grep -c` прогона I;
- содержимое `.tmp/p5g3bt/tests.sha256`;
- вывод `git status --short` из шага 3;
- список коммитов: один пункт — два новых файла шага 1, сообщение на английском о приёмочных тестах части 3б режима отладки интерфейса: скрипты, которые запускают игру и проверяют каталог и записи 35 сцен базы в бою; последняя строка сообщения — `Behavior changes: none`;
- раздел «Рабочие места»: вывод `python3 /srv/dune/tools/task-places.py inventory .tmp/p5g3bt --size`; у `.tmp/p5g3bt` пометка `оставить — хэши тестов нужны исполнителю`. Папки `.tmp/out`, `.tmp/deps`, `.tmp/p5g3a`, `.tmp/p5g3at`, `.tmp/p5g3c` созданы до этой задачи и в раздел не входят. Ничего не удаляй, кроме папок `__pycache__` пункта 4 шага 2.

Числа в сдаче — только из вывода команд.

## Организация работы

- **Порядок:** раздел «Прочитать до работы» → шаг 1 → шаг 2 → шаг 3 → сдача и стоп.
- **Параллельно:** шаги зависят друг от друга, параллельных дорожек нет.
- **Помощники:** один помощник `gpt-6-luna` `xhigh`, без вложенных: шаг 2 — команды, их коды выхода и выписка строк логов. Бриф дословно содержит раздел «Шаг 2», абзац «Комментарии в коде» и запрет менять файлы, кроме папок `__pycache__` пункта 4 шага 2 и файлов в `.tmp/p5g3bt/`. Шаги 1 и 3, сверку файлов с текстом шага 1 и сдачу делает корневая нить; механику — команды и выписку логов — только помощник.
- **Остановки:** только на `## DONE-P5G3BT` и на блоках `## Q-P5G3BT-NN`. Команда оболочки дважды подряд не завершилась (нет кода выхода) — блок `## Q-P5G3BT-04` и стоп.
- **Рамка правок:** два новых файла шага 1, папки `__pycache__` пункта 4 шага 2 и папка `.tmp/p5g3bt/`. Игра пишет в `.tmp/out/run/bin/` и во временные папки скриптов; это не правка.

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
