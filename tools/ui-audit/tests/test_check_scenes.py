import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import check_scenes  # noqa: E402

VIEWPORT = {"x": 0, "y": 30, "w": 600, "h": 570}
TOP = {"x": 300, "y": 30, "w": 32, "h": 32}
RIGHT = {"x": 580, "y": 300, "w": 32, "h": 32}
BOTTOM = {"x": 300, "y": 570, "w": 32, "h": 32}
MIDDLE = {"x": 300, "y": 300, "w": 32, "h": 32}


def header(scene, **extra):
    head = {
        "k": "header", "scene": scene, "resolution": "1280x720", "language": "en", "graphics": "hd",
        "canvas": {"w": 1067, "h": 600}, "game_screen": True, "version": "test",
        "render_scale": 0, "world_scale": 0, "map_viewport": dict(VIEWPORT),
    }
    head.update(extra)
    return head


def label(kind, obj, type_, owner):
    return {"k": "label", "kind": kind, "obj": obj, "type": type_,
            "x": owner["x"], "y": owner["y"] - 6, "w": 32, "h": 4, "owner": dict(owner)}


def text(s, x, y, w, h):
    return {"k": "text", "s": s, "x": x, "y": y, "w": w, "h": h, "box": None}


def unit_records(type_, owners, kinds=("health", "group", "experience")):
    records = []
    for index, owner in enumerate(owners, start=1):
        for kind in kinds:
            records.append(label(kind, index, type_, owner))
    return records


def scene_of(type_):
    return "units-label-" + type_.lower().replace("_", "-")


class UnitLabelScenes(unittest.TestCase):
    def check(self, type_, records, **header_extra):
        return check_scenes.check_scene(header(scene_of(type_), **header_extra), records)

    def test_correct_scene_is_ok(self):
        records = unit_records("TRIKE", [TOP, RIGHT, BOTTOM])
        self.assertEqual(self.check("TRIKE", records), "OK")

    def test_scene_name_with_underscore_type_is_ok(self):
        records = unit_records("COMBAT_TANK", [BOTTOM, TOP, RIGHT])
        self.assertEqual(self.check("COMBAT_TANK", records), "OK")

    def test_harvester_needs_a_spice_label(self):
        without_spice = unit_records("HARVESTER", [TOP, RIGHT, BOTTOM])
        self.assertIn("spice", self.check("HARVESTER", without_spice))
        with_spice = unit_records("HARVESTER", [TOP, RIGHT, BOTTOM], ("health", "group", "experience", "spice"))
        self.assertEqual(self.check("HARVESTER", with_spice), "OK")

    def test_other_types_do_not_need_spice(self):
        records = unit_records("QUAD", [TOP, RIGHT, BOTTOM])
        self.assertEqual(self.check("QUAD", records), "OK")

    def test_missing_group_label_fails(self):
        records = unit_records("TRIKE", [TOP, RIGHT, BOTTOM])
        records = [r for r in records if not (r["obj"] == 2 and r["kind"] == "group")]
        self.assertIn("group", self.check("TRIKE", records))

    def test_two_objects_fail(self):
        records = unit_records("TRIKE", [TOP, RIGHT])
        self.assertIn("object", self.check("TRIKE", records))

    def test_four_objects_fail(self):
        records = unit_records("TRIKE", [TOP, RIGHT, BOTTOM, MIDDLE])
        self.assertIn("object", self.check("TRIKE", records))

    def test_copy_not_at_an_edge_fails(self):
        records = unit_records("TRIKE", [TOP, RIGHT, MIDDLE])
        self.assertIn("edge", self.check("TRIKE", records))

    def test_all_copies_at_the_top_fail(self):
        top_left = {"x": 100, "y": 30, "w": 32, "h": 32}
        top_right = {"x": 200, "y": 30, "w": 32, "h": 32}
        records = unit_records("TRIKE", [TOP, top_left, top_right])
        self.assertIn("edge", self.check("TRIKE", records))

    def test_copy_beyond_the_edge_is_allowed(self):
        beyond = {"x": 640, "y": 300, "w": 32, "h": 32}
        records = unit_records("TRIKE", [TOP, beyond, BOTTOM])
        self.assertEqual(self.check("TRIKE", records), "OK")

    def test_text_record_inside_the_group_label_fails(self):
        records = unit_records("TRIKE", [TOP, RIGHT, BOTTOM])
        group = next(r for r in records if r["kind"] == "group")
        records.append(text("1", group["x"] + 1, group["y"] + 1, 2, 2))
        self.assertIn("text", self.check("TRIKE", records))

    def test_text_record_elsewhere_is_ok(self):
        records = unit_records("TRIKE", [TOP, RIGHT, BOTTOM])
        records.append(text("Menu", 5, 5, 40, 12))
        self.assertEqual(self.check("TRIKE", records), "OK")

    def test_scene_that_is_not_checked_gives_none(self):
        self.assertIsNone(check_scenes.check_scene(header("main-menu"), []))


class StructureLabelScene(unittest.TestCase):
    def records(self, owners):
        return [label("structure-health", index, "CONSTYARD", owner) for index, owner in enumerate(owners, 1)]

    def test_building_at_the_top_is_ok(self):
        result = check_scenes.check_scene(header("structure-label-top"), self.records([TOP]))
        self.assertEqual(result, "OK")

    def test_building_at_the_right_is_ok(self):
        result = check_scenes.check_scene(header("structure-label-right"), self.records([RIGHT]))
        self.assertEqual(result, "OK")

    def test_missing_health_record_fails(self):
        result = check_scenes.check_scene(header("structure-label-top"), self.records([]))
        self.assertIn("object", result)

    def test_two_buildings_fail(self):
        result = check_scenes.check_scene(header("structure-label-top"), self.records([TOP, RIGHT]))
        self.assertIn("object", result)

    def test_building_in_the_middle_fails(self):
        result = check_scenes.check_scene(header("structure-label-top"), self.records([MIDDLE]))
        self.assertIn("edge", result)

    def test_building_at_the_wrong_edge_fails(self):
        result = check_scenes.check_scene(header("structure-label-right"), self.records([TOP]))
        self.assertIn("edge", result)


class OutputLines(unittest.TestCase):
    def test_line_has_scene_combination_and_result(self):
        line = check_scenes.format_line(header("units-label-trike"), "OK")
        self.assertEqual(line, "units-label-trike; 1280x720/en/hd; OK")

    def test_log_file_is_checked_and_formatted(self):
        records = unit_records("TRIKE", [TOP, RIGHT, MIDDLE])
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "units-label-trike.geometry.jsonl"
            lines = [header("units-label-trike")] + records
            path.write_text("".join(json.dumps(line) + "\n" for line in lines), encoding="utf-8")
            line = check_scenes.check_file(path)
        self.assertTrue(line.startswith("units-label-trike; 1280x720/en/hd; "))
        self.assertIn("edge", line)

    def test_log_file_of_an_unchecked_scene_gives_no_line(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "main-menu.geometry.jsonl"
            path.write_text(json.dumps(header("main-menu")) + "\n", encoding="utf-8")
            self.assertIsNone(check_scenes.check_file(path))


if __name__ == "__main__":
    unittest.main()
