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
