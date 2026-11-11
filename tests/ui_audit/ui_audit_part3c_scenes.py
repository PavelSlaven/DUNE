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
