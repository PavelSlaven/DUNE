import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import ui_audit_part3a_catalog as part3a  # noqa: E402
import ui_audit_runtime_support as support  # noqa: E402

SCORING_READINESS = "FixedFrames(8, no readiness flag)"
EDITOR_READINESS = "StateSettled"
EDITOR_BARS = ("topology", "start-cells", "symmetry")
GROUPS = ("scoring", "new-map-editor", "editor")
EXPECTED_COUNT = 5


def expected_scenes():
    scenes = [
        part3a.scene("scoring", "scoring", "GAME_SCORING", "cScoringState", "atreides", SCORING_READINESS),
        part3a.scene("editor-new-map", "new-map-editor", "GAME_NEW_MAP_EDITOR", "cNewMapEditorState", "",
                     EDITOR_READINESS),
    ]
    return scenes + [part3a.scene(f"editor-{bar}", "editor", "GAME_EDITOR", "cEditorState", "", EDITOR_READINESS)
                     for bar in EDITOR_BARS]


def in_part3c(entry):
    return entry["group"] in GROUPS


def check_coverage(scenes):
    screens = part3a.check_screens
    exclusions, problems = screens.load_exclusions(
        (part3a.REPO_ROOT / "tools" / "ui-audit" / "exclusions.tsv").read_text(encoding="utf-8"))
    problems += screens.check_screens(scenes, screens.collect_code_names(part3a.REPO_ROOT), exclusions)
    return f"Screen coverage problems: {problems}" if problems else None


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
    actual = [entry for entry in scenes if in_part3c(entry)]
    ids = [entry["id"] for entry in actual]
    duplicates = sorted({scene_id for scene_id in ids if ids.count(scene_id) > 1})
    if duplicates:
        return f"Duplicate scene ids: {duplicates}"
    missing = sorted(set(expected) - set(ids))
    extra = sorted(set(ids) - set(expected))
    if missing or extra:
        return f"Part 3c scenes differ: missing {missing}; extra {extra}"
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
