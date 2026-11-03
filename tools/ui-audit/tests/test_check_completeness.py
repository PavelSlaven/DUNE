import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import check_completeness  # noqa: E402

RESOLUTIONS = ("1024x768", "1280x720", "1366x768", "1600x900", "1920x1080", "2560x1440")
FULL_RESOLUTIONS = ("1024x768", "1920x1080")
COMBOS = [
    f"{resolution}/{language}/{graphics}"
    for resolution in RESOLUTIONS
    for language in ("ru", "en")
    for graphics in ("hd", "classic")
]
SCENES = [
    {"id": "main-menu__no-saves", "hud": False},
    {"id": "options-game__load-enabled", "hud": False},
    {"id": "game-hud__atreides", "hud": True},
]
FLAGGED = {("1280x720/ru/hd", "options-game__load-enabled")}


def png_path(combo, scene):
    return f"png/{combo}/{scene}.png"


def log_path(combo, scene):
    return f"logs/{combo}/{scene}.geometry.jsonl"


def expected_pngs(scenes, flagged, combos):
    result = set()
    for combo in combos:
        full = combo.split("/")[0] in FULL_RESOLUTIONS
        for scene in scenes:
            if full or scene["hud"] or (combo, scene["id"]) in flagged:
                result.add(png_path(combo, scene["id"]))
    return result


def build_tree(root, scenes=SCENES, flagged=FLAGGED, combos=COMBOS):
    for relative in expected_pngs(scenes, flagged, combos):
        touch(root, relative)
    for combo in combos:
        for scene in scenes:
            touch(root, log_path(combo, scene["id"]))


def touch(root, relative):
    path = Path(root) / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"")


def run_check(root, scenes=SCENES, flagged=FLAGGED, combos=COMBOS):
    return sorted(check_completeness.check(Path(root), scenes, flagged, combos))


class Completeness(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.root = Path(self.directory.name)
        build_tree(self.root)

    def tearDown(self):
        self.directory.cleanup()

    def test_full_set_succeeds(self):
        self.assertEqual(run_check(self.root), [])

    def test_missing_png_in_full_combo_is_refused(self):
        relative = png_path("1024x768/ru/hd", "main-menu__no-saves")
        (self.root / relative).unlink()
        self.assertEqual(run_check(self.root), [("missing-png", relative)])

    def test_missing_hud_png_in_reduced_combo_is_refused(self):
        relative = png_path("1600x900/en/classic", "game-hud__atreides")
        (self.root / relative).unlink()
        self.assertEqual(run_check(self.root), [("missing-png", relative)])

    def test_missing_png_of_flagged_scene_is_refused(self):
        relative = png_path("1280x720/ru/hd", "options-game__load-enabled")
        (self.root / relative).unlink()
        self.assertEqual(run_check(self.root), [("missing-png", relative)])

    def test_extra_png_in_reduced_combo_is_refused(self):
        relative = png_path("1600x900/en/classic", "main-menu__no-saves")
        touch(self.root, relative)
        self.assertEqual(run_check(self.root), [("extra-png", relative)])

    def test_png_of_unknown_scene_in_full_combo_is_refused(self):
        relative = png_path("1920x1080/en/hd", "no-such-scene")
        touch(self.root, relative)
        self.assertEqual(run_check(self.root), [("extra-png", relative)])

    def test_flagged_scene_png_is_not_extra_in_its_combo_only(self):
        relative = png_path("1280x720/en/hd", "options-game__load-enabled")
        touch(self.root, relative)
        self.assertEqual(run_check(self.root), [("extra-png", relative)])

    def test_missing_log_in_full_combo_is_refused(self):
        relative = log_path("1920x1080/en/classic", "options-game__load-enabled")
        (self.root / relative).unlink()
        self.assertEqual(run_check(self.root), [("missing-log", relative)])

    def test_missing_log_in_reduced_combo_is_refused(self):
        relative = log_path("2560x1440/ru/hd", "main-menu__no-saves")
        (self.root / relative).unlink()
        self.assertEqual(run_check(self.root), [("missing-log", relative)])

    def test_every_problem_is_reported(self):
        missing_png = png_path("1024x768/en/hd", "game-hud__atreides")
        missing_log = log_path("1366x768/ru/classic", "game-hud__atreides")
        extra_png = png_path("1366x768/ru/classic", "main-menu__no-saves")
        (self.root / missing_png).unlink()
        (self.root / missing_log).unlink()
        touch(self.root, extra_png)
        self.assertEqual(
            run_check(self.root),
            sorted([
                ("missing-png", missing_png),
                ("missing-log", missing_log),
                ("extra-png", extra_png),
            ]),
        )

    def test_empty_root_reports_every_expected_file(self):
        with tempfile.TemporaryDirectory() as empty:
            problems = run_check(empty)
        expected = len(expected_pngs(SCENES, FLAGGED, COMBOS)) + len(COMBOS) * len(SCENES)
        self.assertEqual(len(problems), expected)
        self.assertEqual({kind for kind, _ in problems}, {"missing-png", "missing-log"})


if __name__ == "__main__":
    unittest.main()
