import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import ui_audit_runtime_support as support  # noqa: E402

SCENE_KEYS = {"id", "group", "state", "screen", "game_screen", "house", "hud", "hd_only", "hover", "readiness"}
MAIN_MENU = {
    "id": "main-menu",
    "group": "main-menu",
    "state": "GAME_MENU",
    "screen": "cMainMenuState",
    "game_screen": False,
    "house": "",
    "hud": False,
    "hd_only": False,
    "hover": None,
    "readiness": "StateSettled",
}
WORLD_SCALES = [0, 100, 110, 125, 150]


def check_list(game):
    result = game.run(["--ui-audit-list"])
    if result.returncode != 0:
        return f"--ui-audit-list exited with {result.returncode}\n{result.stderr}"
    try:
        scenes = support.read_json(result.stdout)["scenes"]
    except (ValueError, KeyError, TypeError) as error:
        return f"--ui-audit-list did not print a catalog: {error}\n{result.stdout}"
    for scene in scenes:
        if set(scene) != SCENE_KEYS:
            return f"Scene keys differ: {sorted(scene)}"
    main_menu = [scene for scene in scenes if scene["id"] == "main-menu"]
    if len(main_menu) != 1 or not support.same_json(main_menu[0], MAIN_MENU):
        return f"Unexpected main-menu entry: {main_menu}"
    return None


def check_scales(game):
    result = game.run(["--ui-audit-scales", "1024x768"])
    if result.returncode != 0:
        return f"--ui-audit-scales exited with {result.returncode}\n{result.stderr}"
    try:
        scales = support.read_json(result.stdout)
    except ValueError as error:
        return f"--ui-audit-scales did not print JSON: {error}\n{result.stdout}"
    if set(scales) != {"resolution", "render", "world"} or scales["resolution"] != "1024x768":
        return f"Unexpected scales: {scales}"
    render = scales["render"]
    if not render or render[0] != 0 or not all(type(value) is int for value in render):
        return f"Unexpected render scales: {render}"
    if not support.same_json(scales["world"], WORLD_SCALES):
        return f"Unexpected world scales: {scales['world']}"
    bad = game.run(["--ui-audit-scales", "abc"])
    if bad.returncode != 2 or "ui-audit: bad resolution abc" not in bad.stderr:
        return f"A bad resolution must exit with 2 and be named: {bad.returncode}\n{bad.stderr}"
    return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    args = parser.parse_args()
    with support.GameRun(args.run_dir) as game:
        for check in (check_list, check_scales):
            error = check(game)
            if error:
                print(error, file=sys.stderr)
                return 1
        preferences = game.preferences_files()
        if preferences:
            print(f"An audit run must not write preferences: {preferences}", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
