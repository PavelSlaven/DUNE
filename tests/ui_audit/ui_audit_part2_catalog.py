import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import ui_audit_runtime_support as support  # noqa: E402

SCENE_KEYS = {"id", "group", "state", "screen", "game_screen", "house", "hud", "hd_only", "hover", "readiness"}
HOUSES = ("atreides", "harkonnen", "ordos", "sardaukar")
MENTAT_SCREENS = {
    "atreides": "AtreidesMentat",
    "harkonnen": "HarkonnenMentat",
    "ordos": "OrdosMentat",
    "sardaukar": "SardaukarMentat",
}
MENTAT_KINDS = (("briefing", "GAME_BRIEFING"), ("win", "GAME_WINBRIEF"), ("lose", "GAME_LOSEBRIEF"))
PART2_GROUPS = {"region", "choose-house", "select-mission", "tellhouse", "mentat", "skirmish-setup", "options-menu",
                "credits"}
EXPECTED_COUNT = 107


def scene(scene_id, group, state, screen, house, readiness, hd_only=False):
    return {
        "id": scene_id,
        "group": group,
        "state": state,
        "screen": screen,
        "game_screen": False,
        "house": house,
        "hud": False,
        "hd_only": hd_only,
        "hover": None,
        "readiness": readiness,
    }


def expected_scenes():
    scenes = []
    for house in HOUSES:
        for number in (1, 2, 3):
            scenes.append(scene(f"region-{house}-intro-{number}", "region", "GAME_REGION",
                                "cSelectYourNextConquestState", house, "RegionIntroScene"))
        for number in (3, 5, 7, 9):
            scenes.append(scene(f"region-{house}-conquer-{number}", "region", "GAME_REGION",
                                "cSelectYourNextConquestState", house, "RegionConquerMessage"))
        for number in range(2, 10):
            scenes.append(scene(f"region-{house}-select-{number}", "region", "GAME_REGION",
                                "cSelectYourNextConquestState", house, "RegionStateSelect"))
    scenes.append(scene("choose-house", "choose-house", "GAME_SELECT_HOUSE", "cChooseHouseState", "", "StateSettled"))
    for house in HOUSES:
        scenes.append(scene(f"select-mission-{house}", "select-mission", "GAME_MISSIONSELECT", "cSelectMissionState",
                            house, "StateSettled"))
    for house in HOUSES:
        for phase in ("speak", "await"):
            scenes.append(scene(f"tellhouse-{house}-{phase}", "tellhouse", "GAME_TELLHOUSE", "BeneMentat", house,
                                "MentatFrozen"))
    for house in HOUSES:
        for kind, state in MENTAT_KINDS:
            for phase in ("speak", "await"):
                scenes.append(scene(f"mentat-{kind}-{house}-{phase}", "mentat", state, MENTAT_SCREENS[house], house,
                                    "MentatFrozen"))
    for variant in ("random", "ready-map"):
        scenes.append(scene(f"skirmish-setup-{variant}", "skirmish-setup", "GAME_SETUPSKIRMISH",
                            "cSetupSkirmishState", "", "FixedFrames(2, no readiness flag)"))
    for variant in ("main", "applied"):
        scenes.append(scene(f"options-menu-{variant}", "options-menu", "GAME_OPTIONS", "cOptionsState", "",
                            "FixedFrames(14, no readiness flag)"))
    for frame in ("title", "1", "2", "3", "4", "5"):
        scenes.append(scene(f"credits-{frame}", "credits", "GAME_CREDITS", "cCreditsState", "",
                            "CreditsScrollPosition", hd_only=frame in ("4", "5")))
    return scenes


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
    actual = [entry for entry in scenes if entry["group"] in PART2_GROUPS]
    ids = [entry["id"] for entry in actual]
    duplicates = sorted({scene_id for scene_id in ids if ids.count(scene_id) > 1})
    if duplicates:
        return f"Duplicate scene ids: {duplicates}"
    missing = sorted(set(expected) - set(ids))
    extra = sorted(set(ids) - set(expected))
    if missing or extra:
        return f"Part 2 scenes differ: missing {missing}; extra {extra}"
    for entry in actual:
        if not support.same_json(entry, expected[entry["id"]]):
            return f"Unexpected scene entry: {entry}\nexpected: {expected[entry['id']]}"
    return None


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
