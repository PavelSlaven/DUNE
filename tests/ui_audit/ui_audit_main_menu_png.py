import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import ui_audit_runtime_support as support  # noqa: E402

SCENE = "main-menu"
HEADER = {
    "k": "header",
    "scene": SCENE,
    "resolution": "1024x768",
    "language": "en",
    "graphics": "hd",
    "canvas": {"w": 800, "h": 600},
    "game_screen": False,
    "render_scale": 0,
    "world_scale": 0,
}
TEXT_KEYS = {"k", "s", "x", "y", "w", "h", "box"}
GUI_KEYS = {"k", "t", "x", "y", "w", "h"}
MENU_LABELS = {"Campaign", "Skirmish", "Options", "Exit"}
MIN_PNG_BYTES = 50000
MIN_GUI_RECORDS = 8


def check(game):
    result = game.run(["--ui-audit-scene", SCENE, "--ui-audit-out", str(game.out)])
    if result.returncode != 0:
        return f"Game exited with {result.returncode}\n{result.stdout}\n{result.stderr}"
    png = game.out / f"{SCENE}.png"
    log = game.out / f"{SCENE}.geometry.jsonl"
    if not png.is_file() or not log.is_file():
        return f"Missing output: png={png.is_file()} log={log.is_file()}"
    try:
        size = support.png_size(png)
    except ValueError as error:
        return str(error)
    if size != (1024, 768):
        return f"Unexpected PNG size: {size[0]}x{size[1]}"
    if png.stat().st_size < MIN_PNG_BYTES:
        return f"The PNG is too small for a menu snapshot: {png.stat().st_size} bytes"
    try:
        records = [json.loads(line) for line in log.read_text(encoding="utf-8").splitlines()]
    except ValueError as error:
        return f"A geometry line is not JSON: {error}"
    if not records or not all(isinstance(record, dict) for record in records):
        return "The geometry log must hold JSON objects"
    header = records[0]
    if not support.same_json({key: header.get(key) for key in HEADER}, HEADER) or not isinstance(header.get("version"), str):
        return f"Unexpected header: {header}"
    texts = [record for record in records if record.get("k") == "text"]
    if not texts or any(set(record) != TEXT_KEYS for record in texts):
        return f"Text records are missing or malformed: {texts[:3]}"
    labels = {record["s"] for record in texts}
    if not MENU_LABELS <= labels:
        return f"Menu labels are missing from the text records: {sorted(MENU_LABELS - labels)}"
    guis = [record for record in records if record.get("k") == "gui"]
    if len(guis) < MIN_GUI_RECORDS or any(set(record) != GUI_KEYS for record in guis):
        return f"Expected at least {MIN_GUI_RECORDS} well-formed GUI records, got {len(guis)}: {guis[:3]}"
    preferences = game.preferences_files()
    if preferences:
        return f"An audit run must not write preferences: {preferences}"
    return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    args = parser.parse_args()
    with support.GameRun(args.run_dir) as game:
        error = check(game)
        if error:
            print(error, file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
