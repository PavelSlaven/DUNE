import argparse
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import ui_audit_runtime_support as support  # noqa: E402

MENU = "main-menu"
HUD = "game-hud"
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
TIMED_RUNS = [(MENU, 1), (HUD, 300)]
BAD_COUNTS = ["0", "-1", "abc", "10001", "05", "1.5", "+3"]
TIMING_KEYS = ("frames", "frame_ms")


def is_int(value):
    return isinstance(value, int) and not isinstance(value, bool)


def is_number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def read_header(game, scene_id):
    png = game.out / f"{scene_id}.png"
    log = game.out / f"{scene_id}.geometry.jsonl"
    if not png.is_file() or not log.is_file():
        return None, f"{scene_id}: missing output: png={png.is_file()} log={log.is_file()}"
    try:
        size = support.png_size(png)
    except ValueError as error:
        return None, f"{scene_id}: {error}"
    if size != (1024, 768):
        return None, f"{scene_id}: unexpected PNG size {size[0]}x{size[1]}"
    try:
        first = log.read_text(encoding="utf-8").splitlines()[0]
        header = json.loads(first)
    except (IndexError, ValueError) as error:
        return None, f"{scene_id}: the first geometry line is not JSON: {error}"
    if not isinstance(header, dict):
        return None, f"{scene_id}: the header is not a JSON object: {header}"
    expected = dict(HEADER, scene=scene_id, game_screen=scene_id == HUD)
    if not support.same_json({key: header.get(key) for key in expected}, expected) or \
            not isinstance(header.get("version"), str):
        return None, f"{scene_id}: unexpected header: {header}"
    if scene_id == HUD and not support.same_json(header.get("map_viewport"), MAP_VIEWPORT):
        return None, f"{scene_id}: unexpected map_viewport: {header.get('map_viewport')}"
    return header, None


def check_preferences(game, label):
    preferences = game.preferences_files()
    if preferences:
        return f"{label}: an audit run must not write preferences: {preferences}"
    return None


def check_plain(run_dir):
    with support.GameRun(run_dir) as game:
        result = game.run(["--ui-audit-scene", MENU, "--ui-audit-out", str(game.out)])
        if result.returncode != 0:
            return f"{MENU} without frames: exit {result.returncode}\n{result.stdout}\n{result.stderr}"
        header, error = read_header(game, MENU)
        if error:
            return error
        present = [key for key in TIMING_KEYS if key in header]
        if present:
            return f"{MENU} without frames: the header must not have {present}: {header}"
        return check_preferences(game, f"{MENU} without frames")


def check_timed(run_dir, scene_id, count):
    label = f"{scene_id} with {count} frames"
    with support.GameRun(run_dir) as game:
        result = game.run(["--ui-audit-scene", scene_id, "--ui-audit-out", str(game.out),
                           "--ui-audit-frames", str(count)])
        if result.returncode != 0:
            return f"{label}: exit {result.returncode}\n{result.stdout}\n{result.stderr}"
        header, error = read_header(game, scene_id)
        if error:
            return error
        frames = header.get("frames")
        if not is_int(frames) or frames != count:
            return f"{label}: frames must be the integer {count}: {header}"
        frame_ms = header.get("frame_ms")
        if not is_number(frame_ms) or not math.isfinite(frame_ms) or not 0 < frame_ms < 1000:
            return f"{label}: frame_ms must be a number above 0 and below 1000: {header}"
        return check_preferences(game, label)


def check_bad(run_dir, value):
    label = f"bad frame count {value!r}"
    with support.GameRun(run_dir) as game:
        result = game.run(["--ui-audit-scene", MENU, "--ui-audit-out", str(game.out),
                           "--ui-audit-frames", value])
        if result.returncode != 2:
            return f"{label}: must exit with 2, got {result.returncode}\n{result.stderr}"
        if f"ui-audit: bad frame count {value}" not in result.stderr:
            return f"{label}: the value is not named on stderr:\n{result.stderr}"
        leftovers = sorted(path.name for path in game.out.rglob("*") if path.is_file())
        if leftovers:
            return f"{label}: must not create files: {leftovers}"
        return check_preferences(game, label)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    args = parser.parse_args()
    errors = []
    error = check_plain(args.run_dir)
    if error:
        errors.append(error)
    for scene_id, count in TIMED_RUNS:
        error = check_timed(args.run_dir, scene_id, count)
        if error:
            errors.append(error)
    for value in BAD_COUNTS:
        error = check_bad(args.run_dir, value)
        if error:
            errors.append(error)
    for error in errors:
        print(error, file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
