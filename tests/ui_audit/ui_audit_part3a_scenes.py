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
        "options-game-main-saves": check_options_game_main,
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
