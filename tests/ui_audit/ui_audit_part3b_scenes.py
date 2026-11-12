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
MUSIC_CLICKS = ("music-previous", "music-next", "music-speed-slider")


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
    if not support.same_json(rally["owner"], selected["owner"]):
        return f"the rally point owner {rally['owner']} is not the selected building {selected['owner']}"
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


def check_music(scene_id, header, body, bodies):
    clicks = []
    for name in MUSIC_CLICKS:
        record, error = base.one_record(body, "click", "name", name)
        if error:
            return error
        clicks.append(record)
    previous, following, slider = clicks
    options = named(body, "click", "top-options")[0]
    outside = [record for record in clicks if not base.inside(record, base.TOP_PANEL)]
    return base.first_error(
        f"click records outside {base.TOP_PANEL}: {outside}" if outside else None,
        None if options["x"] + options["w"] <= previous["x"]
        else f"the music buttons overlap the options button: {options} and {previous}",
        None if previous["x"] + previous["w"] <= following["x"]
        else f"the previous button overlaps the next button: {previous} and {following}",
        None if following["x"] + following["w"] <= slider["x"]
        else f"the next button overlaps the speed slider: {following} and {slider}",
        base.require_text(body, "<"),
        base.require_text(body, ">"),
        base.require_text(body, "SPEED"),
        None if any(record["s"].endswith("...") for record in base.records_of(body, "text"))
        else "no text record with a truncated track name",
    )


def check_for(scene_id):
    fixed = {
        "game-hud": check_nothing_more,
        "game-music": check_music,
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
