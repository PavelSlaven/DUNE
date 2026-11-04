import json
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import check_options_geometry  # noqa: E402


def header(scene="options-menu-main", combo="1024x768/ru/hd"):
    resolution, language, graphics, *scale = combo.split("/")
    render_scale, world_scale = (0, 0)
    if scale:
        render_scale, world_scale = (int(value) for value in scale[0][1:].replace("w", " ").split())
    return {
        "k": "header", "scene": scene, "resolution": resolution, "language": language, "graphics": graphics,
        "canvas": {"w": 1024, "h": 768}, "game_screen": False, "render_scale": render_scale,
        "world_scale": world_scale,
    }


def gui(type_, x, y, w, h):
    return {"k": "gui", "t": type_, "x": x, "y": y, "w": w, "h": h}


def click(name, x, y, w, h):
    return {"k": "click", "name": name, "x": x, "y": y, "w": w, "h": h}


class Rule3(unittest.TestCase):
    def test_button_covering_a_nonclickable_row_is_flagged(self):
        records = [gui("GuiButton", 100, 100, 120, 30), gui("GuiLabel", 110, 108, 80, 12)]
        flags = check_options_geometry.check_rule3(header(), records)
        self.assertEqual([flag["rule"] for flag in flags], [3])

    def test_button_covering_a_slider_is_flagged(self):
        records = [gui("GuiButton", 100, 100, 120, 30), gui("GuiSlider", 110, 108, 80, 12)]
        flags = check_options_geometry.check_rule3(header(), records)
        self.assertEqual([flag["rule"] for flag in flags], [3])

    def test_button_contained_by_a_nonclickable_row_is_flagged(self):
        records = [gui("GuiSlider", 100, 100, 120, 30), gui("GuiButton", 110, 108, 80, 12)]
        flags = check_options_geometry.check_rule3(header(), records)
        self.assertEqual([flag["rule"] for flag in flags], [3])

    def test_button_inside_parent_window_is_not_flagged(self):
        records = [gui("GuiWindow", 50, 50, 400, 300), gui("GuiButton", 100, 100, 120, 30)]
        self.assertEqual(check_options_geometry.check_rule3(header(), records), [])

    def test_nonbutton_nested_pair_keeps_the_general_rule(self):
        records = [gui("GuiLabel", 100, 100, 120, 30), gui("GuiSlider", 110, 108, 80, 12)]
        self.assertEqual(check_options_geometry.check_rule3(header(), records), [])


class Rule9AndPlan(unittest.TestCase):
    def write_log(self, root, combo, scene, records):
        head = header(scene, combo)
        path = Path(root) / f"{scene}-{combo.replace('/', '_')}.geometry.jsonl"
        path.write_text("".join(json.dumps(row) + "\n" for row in [head] + records), encoding="utf-8")
        return path

    def test_rule9_is_checked_independently_of_rule3(self):
        with tempfile.TemporaryDirectory() as directory:
            self.write_log(directory, "1024x768/ru/hd", "options-menu-main", [
                click("Back", 0, 0, 100, 100), click("Next", 50, 0, 100, 100),
            ])
            flags = check_options_geometry.check_log(
                next(Path(directory).glob("*.geometry.jsonl")))
        self.assertEqual([flag["rule"] for flag in flags], [9])

    def test_checker_fails_on_flags_when_the_plan_matches(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            combos = root / "combos.txt"
            combos.write_text("1024x768/ru/hd\n", encoding="utf-8")
            self.write_log(root, "1024x768/ru/hd", "options-menu-main", [
                gui("GuiButton", 100, 100, 120, 30), gui("GuiLabel", 110, 108, 80, 12),
            ])
            for scene in check_options_geometry.OPTIONS_SCENES[1:]:
                self.write_log(root, "1024x768/ru/hd", scene, [])
            stdout, stderr = StringIO(), StringIO()
            with redirect_stdout(stdout), redirect_stderr(stderr):
                result = check_options_geometry.main([str(root), "--combos", str(combos)])
        self.assertEqual(result, 1)
        self.assertIn("logs: 3; planned: 3; flags: 1; rule 3: 1; rule 9: 0", stdout.getvalue())
        self.assertEqual(stderr.getvalue(), "")

    def test_scoped_check_fails_for_missing_and_extra_planned_pairs(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            combos = root / "combos.txt"
            combos.write_text("1024x768/ru/hd\n1280x720/en/hd\n", encoding="utf-8")
            for scene in check_options_geometry.OPTIONS_SCENES:
                self.write_log(root, "1024x768/ru/hd", scene, [])
            for scene in check_options_geometry.OPTIONS_SCENES[:2]:
                self.write_log(root, "1280x720/en/hd", scene, [])
            self.write_log(root, "1600x900/ru/hd", "options-game-main-nosaves", [])
            stdout, stderr = StringIO(), StringIO()
            with redirect_stdout(stdout), redirect_stderr(stderr):
                result = check_options_geometry.main([str(root), "--combos", str(combos)])
        self.assertEqual(result, 1)
        self.assertIn("logs: 6; planned: 6", stdout.getvalue())
        self.assertIn("('1280x720/en/hd', 'options-game-main-nosaves')", stderr.getvalue())
        self.assertIn("('1600x900/ru/hd', 'options-game-main-nosaves')", stderr.getvalue())

    def test_plan_entries_are_filtered_to_the_three_options_scenes(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "audit-plan.json"
            path.write_text(json.dumps([
                {"combo": "1024x768/ru/hd", "scene": "options-menu-main"},
                {"combo": "1024x768/ru/hd", "scene": "main-menu"},
            ]), encoding="utf-8")
            expected = check_options_geometry.planned_pairs(plan_path=path)
        self.assertEqual(expected, {("1024x768/ru/hd", "options-menu-main"): 1})

    def test_nonoptions_logs_are_outside_the_scoped_count(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            combos = root / "combos.txt"
            combos.write_text("1024x768/ru/hd\n", encoding="utf-8")
            for scene in check_options_geometry.OPTIONS_SCENES:
                self.write_log(root, "1024x768/ru/hd", scene, [])
            self.write_log(root, "1024x768/ru/hd", "main-menu", [])
            expected = check_options_geometry.planned_pairs(combos_path=combos)
            actual, flags, missing, extra = check_options_geometry.check_tree(root, expected)
        self.assertEqual(sum(actual.values()), 3)
        self.assertEqual(flags, [])
        self.assertFalse(missing)
        self.assertFalse(extra)


if __name__ == "__main__":
    unittest.main()
