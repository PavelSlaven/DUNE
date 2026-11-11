import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools" / "ui-audit"))

import check_screens  # noqa: E402
import ui_audit_runtime_support as support  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[2]
SCENE_KEYS = {"id", "group", "state", "screen", "game_screen", "house", "hud", "hd_only", "hover", "readiness"}
UNIT_TYPES = (
    ("trike", "TRIKE"),
    ("raider", "RAIDER"),
    ("quad", "QUAD"),
    ("tank", "TANK"),
    ("siegetank", "SIEGETANK"),
    ("launcher", "LAUNCHER"),
    ("deviator", "DEVIATOR"),
    ("sonictank", "SONICTANK"),
    ("devastator", "DEVASTATOR"),
    ("harvester", "HARVESTER"),
    ("mcv", "MCV"),
    ("soldier", "SOLDIER"),
    ("infantry", "INFANTRY"),
    ("trooper", "TROOPER"),
    ("troopers", "TROOPERS"),
    ("unit-fremen-one", "UNIT_FREMEN_ONE"),
    ("unit-fremen-three", "UNIT_FREMEN_THREE"),
    ("saboteur", "SABOTEUR"),
)
GAME_READINESS = "FixedFrames(5, no readiness flag)"
OUTCOME_READINESS = "FixedFrames(8, no readiness flag)"
OPTIONS_READINESS = "FixedFrames(14, no readiness flag)"
EXPECTED_COUNT = 24
LATER_SCREENS = ("GAME_EDITOR", "GAME_NEW_MAP_EDITOR", "GAME_SCORING", "GAME_VIDEO", "cEditorState",
                 "cNewMapEditorState", "cScoringState", "cVideoState")


def scene(scene_id, group, state, screen, house, readiness, game_screen=False, hover=None):
    return {
        "id": scene_id,
        "group": group,
        "state": state,
        "screen": screen,
        "game_screen": game_screen,
        "house": house,
        "hud": False,
        "hd_only": False,
        "hover": hover,
        "readiness": readiness,
    }


def expected_scenes():
    scenes = []
    for name, _ in UNIT_TYPES:
        scenes.append(scene(f"units-label-{name}", "game-playing", "GAME_PLAYING", "cGamePlaying", "atreides",
                            GAME_READINESS, game_screen=True))
    for edge in ("top", "right"):
        scenes.append(scene(f"structure-label-{edge}", "game-playing", "GAME_PLAYING", "cGamePlaying", "atreides",
                            GAME_READINESS, game_screen=True, hover={"x": 0, "y": 0}))
    scenes.append(scene("outcome-win", "outcome", "GAME_WINNING", "cWinLoseState", "atreides", OUTCOME_READINESS))
    scenes.append(scene("outcome-lose", "outcome", "GAME_LOSING", "cWinLoseState", "atreides", OUTCOME_READINESS))
    for variant in ("main-nosaves", "applied"):
        scenes.append(scene(f"options-game-{variant}", "options-game", "GAME_OPTIONS", "cOptionsState", "",
                            OPTIONS_READINESS))
    return scenes


def in_part3a(entry):
    scene_id = entry["id"]
    return (isinstance(scene_id, str) and scene_id.startswith(("units-label-", "structure-label-"))) or \
        entry["group"] in ("outcome", "options-game")


def check_coverage(scenes):
    exclusions, problems = check_screens.load_exclusions(
        (REPO_ROOT / "tools" / "ui-audit" / "exclusions.tsv").read_text(encoding="utf-8"))
    problems += check_screens.check_screens(scenes, check_screens.collect_code_names(REPO_ROOT), exclusions)
    allowed = {f"no scene and no exclusion for {name}" for name in LATER_SCREENS}
    unexpected = [problem for problem in problems if problem not in allowed]
    return f"Screen coverage problems: {unexpected}" if unexpected else None


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
    actual = [entry for entry in scenes if in_part3a(entry)]
    ids = [entry["id"] for entry in actual]
    duplicates = sorted({scene_id for scene_id in ids if ids.count(scene_id) > 1})
    if duplicates:
        return f"Duplicate scene ids: {duplicates}"
    missing = sorted(set(expected) - set(ids))
    extra = sorted(set(ids) - set(expected))
    if missing or extra:
        return f"Part 3a scenes differ: missing {missing}; extra {extra}"
    for entry in actual:
        if not support.same_json(entry, expected[entry["id"]]):
            return f"Unexpected scene entry: {entry}\nexpected: {expected[entry['id']]}"
    return check_coverage(scenes)


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
