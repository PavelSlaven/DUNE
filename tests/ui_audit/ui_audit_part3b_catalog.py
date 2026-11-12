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
               "game-list-scroll-end", "game-rally-point", "game-command-damaged-unit", "game-command-harvester",
               "game-command-mcv")
EXPECTED_COUNT = 38


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
