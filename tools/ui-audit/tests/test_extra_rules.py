import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import check_geometry  # noqa: E402

CANVAS = {"w": 800, "h": 600}
OWNER = {"x": 100, "y": 100, "w": 32, "h": 32}


def header(scene="game-screen", resolution="1024x768", language="en", graphics="hd", game_screen=True, **extra):
    head = {
        "k": "header", "scene": scene, "resolution": resolution, "language": language,
        "graphics": graphics, "canvas": dict(CANVAS), "game_screen": game_screen, "version": "test",
    }
    head.update(extra)
    return head


def text(s, x, y, w, h):
    return {"k": "text", "s": s, "x": x, "y": y, "w": w, "h": h, "box": None}


def gui(t, x, y, w, h):
    return {"k": "gui", "t": t, "x": x, "y": y, "w": w, "h": h}


def area(n, x, y, w, h):
    return {"k": "area", "n": n, "x": x, "y": y, "w": w, "h": h}


def label(kind, obj, x, y, w, h, type_="TRIKE", owner=None):
    return {"k": "label", "kind": kind, "obj": obj, "type": type_, "x": x, "y": y, "w": w, "h": h,
            "owner": dict(owner or OWNER)}


def click(name, x, y, w, h):
    return {"k": "click", "name": name, "x": x, "y": y, "w": w, "h": h}


def rules(flags):
    return sorted(flag["rule"] for flag in flags)


def extra(records, **header_args):
    return check_geometry.check_extra_records(header(**header_args), records)


class LabelOverPanelRule(unittest.TestCase):
    def test_label_drawn_over_an_earlier_panel_is_flagged(self):
        records = [area("sidebar", 600, 0, 200, 600), label("health", 1, 590, 50, 20, 4)]
        flags = extra(records)
        self.assertEqual(rules(flags), [7])
        self.assertEqual(flags[0]["a"], {"x": 590, "y": 50, "w": 20, "h": 4})
        self.assertEqual(flags[0]["b"], {"x": 600, "y": 0, "w": 200, "h": 600})
        self.assertEqual(flags[0]["texts"], ["health", "sidebar"])

    def test_label_recorded_before_the_panel_is_not_flagged(self):
        records = [label("health", 1, 590, 50, 20, 4), area("sidebar", 600, 0, 200, 600)]
        self.assertEqual(extra(records), [])

    def test_label_touching_the_panel_edge_is_honest(self):
        records = [area("sidebar", 600, 0, 200, 600), label("health", 1, 580, 50, 20, 4)]
        self.assertEqual(extra(records), [])

    def test_empty_clipped_label_is_not_flagged(self):
        records = [area("sidebar", 600, 0, 200, 600), label("health", 1, 610, 50, 0, 4)]
        self.assertEqual(extra(records), [])

    def test_label_far_from_the_panel_is_honest(self):
        records = [area("minimap", 0, 400, 100, 100), label("group", 1, 300, 50, 8, 8)]
        self.assertEqual(extra(records), [])


class LabelsOfOneObjectRule(unittest.TestCase):
    def test_intersecting_labels_of_one_object_are_flagged(self):
        records = [label("health", 3, 100, 90, 32, 4), label("group", 3, 120, 92, 10, 10)]
        flags = extra(records)
        self.assertEqual(rules(flags), [8])
        self.assertEqual(flags[0]["texts"], ["health", "group"])
        self.assertEqual(flags[0]["obj"], 3)
        self.assertEqual(flags[0]["type"], "TRIKE")

    def test_same_rectangles_of_different_objects_are_honest(self):
        records = [label("health", 3, 100, 90, 32, 4), label("group", 4, 100, 90, 32, 4)]
        self.assertEqual(extra(records), [])

    def test_separate_labels_of_one_object_are_honest(self):
        records = [label("health", 3, 100, 90, 32, 4), label("group", 3, 100, 100, 10, 10)]
        self.assertEqual(extra(records), [])

    def test_every_intersecting_pair_gives_its_own_flag(self):
        records = [
            label("health", 3, 100, 90, 32, 10),
            label("group", 3, 105, 92, 10, 10),
            label("experience", 3, 110, 95, 10, 10),
        ]
        self.assertEqual(rules(extra(records)), [8, 8, 8])

    def test_summary_counts_objects_with_a_crossing_pair_and_all_objects_of_the_type(self):
        crossing = [label("health", 1, 0, 0, 20, 10), label("group", 1, 5, 5, 10, 10),
                    label("health", 2, 0, 0, 20, 4), label("group", 2, 0, 20, 10, 10),
                    label("health", 3, 0, 0, 20, 4, type_="TANK")]
        clean = [label("health", 1, 0, 0, 20, 4), label("group", 1, 0, 20, 10, 10)]
        rows = check_geometry.summarize_rule8([
            (header(scene="a"), crossing),
            (header(scene="b"), clean),
        ])
        self.assertEqual(rows, [{
            "type": "TRIKE", "kinds": ["group", "health"], "objects_intersecting": 1, "objects_total": 3,
        }])


class ClickZonesRule(unittest.TestCase):
    def test_overlapping_zones_are_flagged(self):
        records = [click("Back", 10, 10, 50, 20), click("Next", 40, 10, 50, 20)]
        flags = extra(records, game_screen=False)
        self.assertEqual(rules(flags), [9])
        self.assertEqual(flags[0]["texts"], ["Back", "Next"])

    def test_zone_inside_another_zone_is_flagged(self):
        records = [click("Window", 0, 0, 400, 300), click("Ok", 10, 10, 50, 20)]
        self.assertEqual(rules(extra(records, game_screen=False)), [9])

    def test_adjacent_zones_are_honest(self):
        records = [click("Back", 10, 10, 50, 20), click("Next", 60, 10, 50, 20)]
        self.assertEqual(extra(records, game_screen=False), [])

    def test_zone_of_the_whole_canvas_overlaps_every_other_zone(self):
        records = [click("skip-speech", 0, 0, 800, 600), click("Back", 10, 10, 50, 20)]
        self.assertEqual(rules(extra(records, game_screen=False)), [9])


class NewRecordsStayOutsideRulesOneToSix(unittest.TestCase):
    BASE = [
        gui("GuiButton", 100, 100, 50, 20),
        gui("GuiButton", 140, 100, 50, 20),
        text("Apply", 90, 105, 40, 12),
        area("minimap", 10, 590, 50, 20),
    ]
    NEW = [
        label("health", 1, 780, 10, 40, 4),
        label("group", 1, 785, 12, 10, 10),
        click("Window", 0, 0, 400, 300),
        click("Ok", 10, 10, 50, 20),
        label("spice", 2, -5, 0, 10, 4),
    ]

    def test_label_and_click_records_do_not_change_the_flags_of_rules_one_to_six(self):
        without = check_geometry.check_records(header(), list(self.BASE))
        with_new = check_geometry.check_records(header(), self.BASE + self.NEW)
        self.assertGreater(len(without), 0)
        self.assertEqual(without, with_new)

    def test_extra_rules_ignore_the_old_record_kinds(self):
        self.assertEqual(extra(list(self.BASE)), [])

    def test_resolution_comparison_ignores_label_and_click_records(self):
        first = (header(resolution="1280x720"), self.BASE + [label("health", 1, 10, 10, 20, 4)])
        second = (header(resolution="1600x900"), self.BASE + [click("Ok", 10, 10, 50, 20)])
        self.assertEqual(check_geometry.compare_resolutions([first, second]), [])


class CombinationNameAndOutput(unittest.TestCase):
    def test_combination_without_scales_keeps_the_old_name(self):
        self.assertEqual(check_geometry.combo_of(header()), "1024x768/en/hd")
        self.assertEqual(check_geometry.combo_of(header(render_scale=0, world_scale=0)), "1024x768/en/hd")

    def test_manual_scales_are_part_of_the_name(self):
        self.assertEqual(check_geometry.combo_of(header(render_scale=125, world_scale=0)),
                         "1024x768/en/hd/r125w0")
        self.assertEqual(check_geometry.combo_of(header(render_scale=0, world_scale=110)),
                         "1024x768/en/hd/r0w110")

    def test_new_rules_have_names_and_one_line_format(self):
        for rule in (7, 8, 9, 10):
            self.assertIn(rule, check_geometry.RULE_NAMES)
        flags = extra([click("Back", 10, 10, 50, 20), click("Next", 40, 10, 50, 20)], game_screen=False)
        line = check_geometry.format_flag(flags[0])
        self.assertNotIn("\n", line)
        for part in ("game-screen", "1024x768/en/hd", "rule 9", "Back", "Next"):
            self.assertIn(part, line)

    def test_tree_check_reports_extra_rules_and_counts_scale_combinations_apart(self):
        with tempfile.TemporaryDirectory() as directory:
            for name, scale in (("a", 0), ("b", 125)):
                lines = [header(scene="options", game_screen=False, render_scale=scale, world_scale=0)]
                lines += [click("Back", 10, 10, 50, 20), click("Next", 40, 10, 50, 20)]
                path = Path(directory) / f"{name}.geometry.jsonl"
                path.write_text("".join(json.dumps(line) + "\n" for line in lines), encoding="utf-8")
            count, flags = check_geometry.check_tree(directory)
        self.assertEqual(count, 2)
        self.assertEqual(rules(flags), [9, 9])
        self.assertEqual(sorted(flag["combo"] for flag in flags),
                         ["1024x768/en/hd", "1024x768/en/hd/r125w0"])


if __name__ == "__main__":
    unittest.main()
