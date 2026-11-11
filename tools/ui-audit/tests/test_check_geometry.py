import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import check_geometry  # noqa: E402

CANVAS = {"w": 800, "h": 600}
WIDE_CANVAS = {"w": 1067, "h": 600}


def header(scene="scene", resolution="1024x768", language="ru", graphics="hd",
           canvas=CANVAS, game_screen=False):
    return {
        "k": "header",
        "scene": scene,
        "resolution": resolution,
        "language": language,
        "graphics": graphics,
        "canvas": dict(canvas),
        "game_screen": game_screen,
        "version": "test",
    }


def text(s, x, y, w, h, box=None):
    return {"k": "text", "s": s, "x": x, "y": y, "w": w, "h": h, "box": box}


def gui(t, x, y, w, h):
    return {"k": "gui", "t": t, "x": x, "y": y, "w": w, "h": h}


def area(n, x, y, w, h):
    return {"k": "area", "n": n, "x": x, "y": y, "w": w, "h": h}


def rect(x, y, w, h):
    return {"x": x, "y": y, "w": w, "h": h}


def rules(flags):
    return sorted(flag["rule"] for flag in flags)


def check(records, **header_args):
    return check_geometry.check_records(header(**header_args), records)


class OffCanvasRule(unittest.TestCase):
    def test_text_beyond_right_edge_is_flagged(self):
        self.assertEqual(rules(check([text("Back", 780, 10, 40, 12)])), [1])

    def test_gui_with_negative_origin_is_flagged(self):
        self.assertEqual(rules(check([gui("GuiButton", -1, 10, 50, 20)])), [1])

    def test_area_below_canvas_is_flagged(self):
        self.assertEqual(rules(check([area("minimap", 10, 590, 50, 20)])), [1])

    def test_rectangles_ending_exactly_on_the_edge_are_honest(self):
        records = [
            text("Back", 760, 588, 40, 12),
            gui("GuiButton", 0, 0, 800, 600),
        ]
        self.assertEqual(check(records), [])

    def test_wide_canvas_is_taken_from_the_header(self):
        records = [text("Back", 1000, 10, 60, 12)]
        self.assertEqual(check(records, canvas=WIDE_CANVAS), [])
        self.assertEqual(rules(check(records, canvas=CANVAS)), [1])


class TextAcrossElementRule(unittest.TestCase):
    def test_text_crossing_a_button_edge_is_flagged(self):
        records = [gui("GuiButton", 100, 5, 50, 20), text("Apply", 90, 10, 40, 12)]
        self.assertEqual(rules(check(records)), [2])

    def test_text_crossing_an_area_is_flagged(self):
        records = [area("minimap", 600, 400, 150, 150), text("Radar", 580, 410, 40, 12)]
        self.assertEqual(rules(check(records)), [2])

    def test_text_covering_a_whole_button_is_flagged(self):
        records = [gui("GuiButton", 100, 5, 50, 20), text("Wide", 90, 0, 100, 40)]
        self.assertEqual(rules(check(records)), [2])

    def test_text_inside_a_button_is_honest(self):
        records = [gui("GuiButton", 100, 5, 50, 20), text("Apply", 110, 10, 30, 12)]
        self.assertEqual(check(records), [])

    def test_text_outside_every_element_is_honest(self):
        records = [gui("GuiButton", 100, 5, 50, 20), text("Title", 300, 300, 40, 12)]
        self.assertEqual(check(records), [])

    def test_text_touching_a_button_edge_is_honest(self):
        records = [gui("GuiButton", 100, 5, 50, 20), text("Apply", 60, 10, 40, 12)]
        self.assertEqual(check(records), [])

    def test_text_inside_window_and_button_is_honest(self):
        records = [
            gui("GuiWindow", 50, 50, 400, 300),
            gui("GuiButton", 100, 100, 120, 30),
            text("Save game", 110, 108, 80, 12),
        ]
        self.assertEqual(check(records), [])

    def test_text_inside_window_crossing_a_button_is_flagged(self):
        records = [
            gui("GuiWindow", 50, 50, 400, 300),
            gui("GuiButton", 100, 100, 120, 30),
            text("Fullscreen mode", 90, 108, 100, 12),
        ]
        self.assertEqual(rules(check(records)), [2])


class ElementsOverlapRule(unittest.TestCase):
    def test_partially_overlapping_buttons_are_flagged(self):
        records = [gui("GuiButton", 100, 100, 50, 20), gui("GuiButton", 140, 100, 50, 20)]
        self.assertEqual(rules(check(records)), [3])

    def test_gui_partially_overlapping_an_area_is_flagged(self):
        records = [area("command-bar", 600, 400, 150, 150), gui("GuiButton", 700, 500, 100, 20)]
        self.assertEqual(rules(check(records)), [3])

    def test_button_inside_window_is_honest(self):
        records = [gui("GuiWindow", 50, 50, 400, 300), gui("GuiButton", 100, 100, 120, 30)]
        self.assertEqual(check(records), [])

    def test_buttons_touching_by_edges_are_honest(self):
        records = [
            gui("GuiButton", 100, 100, 50, 20),
            gui("GuiButton", 150, 100, 50, 20),
            gui("GuiButton", 100, 120, 50, 20),
        ]
        self.assertEqual(check(records), [])

    def test_identical_rectangles_are_honest(self):
        records = [gui("GuiWindow", 50, 50, 400, 300), gui("GuiLabel", 50, 50, 400, 300)]
        self.assertEqual(check(records), [])


class TextOnTextRule(unittest.TestCase):
    def test_overlapping_texts_are_flagged(self):
        records = [text("First", 10, 10, 50, 12), text("Second", 40, 15, 50, 12)]
        self.assertEqual(rules(check(records)), [4])

    def test_texts_touching_by_edges_are_honest(self):
        records = [
            text("First", 10, 10, 50, 12),
            text("Right", 60, 10, 50, 12),
            text("Below", 10, 22, 50, 12),
        ]
        self.assertEqual(check(records), [])

    def test_separated_texts_are_honest(self):
        records = [text("First", 10, 10, 50, 12), text("Second", 300, 300, 50, 12)]
        self.assertEqual(check(records), [])


class TextWiderThanBoxRule(unittest.TestCase):
    def test_text_wider_than_its_box_is_flagged(self):
        records = [text("Advanced settings", 20, 20, 120, 12, box=rect(20, 20, 100, 20))]
        self.assertEqual(rules(check(records)), [5])

    def test_text_taller_than_its_box_is_flagged(self):
        records = [text("Apply", 20, 20, 40, 12, box=rect(20, 20, 100, 10))]
        self.assertEqual(rules(check(records)), [5])

    def test_text_of_exactly_the_box_size_is_honest(self):
        records = [text("Apply", 20, 20, 100, 20, box=rect(20, 20, 100, 20))]
        self.assertEqual(check(records), [])

    def test_text_smaller_than_its_box_is_honest(self):
        records = [text("Apply", 40, 24, 60, 12, box=rect(20, 20, 100, 20))]
        self.assertEqual(check(records), [])

    def test_text_without_a_box_is_not_compared_with_one(self):
        self.assertEqual(check([text("Long caption", 20, 20, 500, 12)]), [])


class ResolutionDifferenceRule(unittest.TestCase):
    def pair(self, first, second, **second_header):
        base = {"scene": "options-main", "canvas": WIDE_CANVAS}
        first_header = header(resolution="1280x720", **base)
        other = dict(base, resolution="1366x768")
        other.update(second_header)
        return check_geometry.compare_resolutions(
            [(first_header, first), (header(**other), second)]
        )

    def test_moved_text_between_resolutions_is_flagged(self):
        flags = self.pair([text("Apply", 10, 10, 40, 12)], [text("Apply", 11, 10, 40, 12)])
        self.assertEqual(rules(flags), [6])

    def test_extra_record_between_resolutions_is_flagged(self):
        flags = self.pair([text("Apply", 10, 10, 40, 12)],
                          [text("Apply", 10, 10, 40, 12), gui("GuiButton", 0, 0, 5, 5)])
        self.assertEqual(rules(flags), [6])

    def test_identical_logs_are_honest(self):
        records = [text("Apply", 10, 10, 40, 12), gui("GuiButton", 5, 5, 60, 20)]
        self.assertEqual(self.pair(records, list(records)), [])

    def test_record_order_does_not_matter(self):
        first = [text("Apply", 10, 10, 40, 12), gui("GuiButton", 5, 5, 60, 20)]
        self.assertEqual(self.pair(first, list(reversed(first))), [])

    def test_different_canvas_is_not_compared(self):
        flags = check_geometry.compare_resolutions([
            (header(scene="s", resolution="1024x768", canvas=CANVAS),
             [text("Apply", 10, 10, 40, 12)]),
            (header(scene="s", resolution="1280x720", canvas=WIDE_CANVAS),
             [text("Apply", 99, 10, 40, 12)]),
        ])
        self.assertEqual(flags, [])

    def test_different_language_is_not_compared(self):
        flags = self.pair([text("Apply", 10, 10, 40, 12)],
                          [text("Применить", 10, 10, 80, 12)], language="en")
        self.assertEqual(flags, [])

    def test_different_graphics_is_not_compared(self):
        flags = self.pair([text("Apply", 10, 10, 40, 12)],
                          [text("Apply", 99, 10, 40, 12)], graphics="classic")
        self.assertEqual(flags, [])

    def test_different_scene_is_not_compared(self):
        flags = self.pair([text("Apply", 10, 10, 40, 12)],
                          [text("Apply", 99, 10, 40, 12)], scene="options-game")
        self.assertEqual(flags, [])

    def game_pair(self, first, second):
        return check_geometry.compare_resolutions([
            (header(scene="hud", resolution="1280x720", canvas=WIDE_CANVAS, game_screen=True),
             first),
            (header(scene="hud", resolution="1366x768", canvas=WIDE_CANVAS, game_screen=True),
             second),
        ])

    def test_game_screen_ignores_a_different_area(self):
        flags = self.game_pair([area("minimap", 10, 10, 100, 100)],
                               [area("minimap", 12, 12, 110, 110)])
        self.assertEqual(flags, [])

    def test_game_screen_compares_gui(self):
        flags = self.game_pair([gui("GuiButton", 10, 10, 100, 20)],
                               [gui("GuiButton", 10, 10, 101, 20)])
        self.assertEqual(rules(flags), [6])

    def test_game_screen_compares_texts(self):
        flags = self.game_pair([text("Credits 100", 10, 10, 80, 12)],
                               [text("Credits 100", 10, 11, 80, 12)])
        self.assertEqual(rules(flags), [6])

    def test_menu_screen_compares_areas(self):
        flags = self.pair([area("panel", 10, 10, 100, 100)], [area("panel", 10, 10, 101, 100)])
        self.assertEqual(rules(flags), [6])


class WholeScene(unittest.TestCase):
    def test_window_with_buttons_labels_and_texts_is_honest(self):
        records = [
            gui("GuiWindow", 100, 100, 400, 300),
            gui("GuiLabel", 120, 110, 360, 16),
            text("Options", 130, 112, 60, 12),
            gui("GuiButton", 120, 150, 160, 30),
            text("Save game", 130, 158, 80, 12, box=rect(120, 150, 160, 30)),
            gui("GuiButton", 300, 150, 160, 30),
            text("Load game", 310, 158, 80, 12, box=rect(300, 150, 160, 30)),
        ]
        self.assertEqual(check(records), [])

    def test_flag_carries_scene_combo_rectangles_and_texts(self):
        records = [gui("GuiButton", 100, 5, 50, 20), text("Apply", 90, 10, 40, 12)]
        flags = check(records, scene="options-game", resolution="1024x768",
                      language="ru", graphics="hd")
        self.assertEqual(len(flags), 1)
        flag = flags[0]
        self.assertEqual(flag["rule"], 2)
        self.assertEqual(flag["scene"], "options-game")
        self.assertEqual(flag["combo"], "1024x768/ru/hd")
        self.assertIn("Apply", flag["texts"])
        self.assertEqual(flag["a"], rect(90, 10, 40, 12))
        self.assertEqual(flag["b"], rect(100, 5, 50, 20))

    def test_format_flag_is_one_line_with_every_part(self):
        records = [gui("GuiButton", 100, 5, 50, 20), text("Apply", 90, 10, 40, 12)]
        flag = check(records, scene="options-game")[0]
        line = check_geometry.format_flag(flag)
        self.assertNotIn("\n", line)
        for part in ("options-game", "1024x768/ru/hd", "2", "Apply"):
            self.assertIn(part, line)


class LogFile(unittest.TestCase):
    def write_log(self, directory, records, head=None):
        path = Path(directory) / "scene.geometry.jsonl"
        lines = [head or header()] + records
        path.write_text("".join(json.dumps(line) + "\n" for line in lines), encoding="utf-8")
        return path

    def test_clean_file_has_no_flags(self):
        with tempfile.TemporaryDirectory() as directory:
            path = self.write_log(directory, [text("Back", 10, 10, 40, 12)])
            self.assertEqual(check_geometry.check_log(path), [])

    def test_file_with_overlapping_elements_is_flagged(self):
        with tempfile.TemporaryDirectory() as directory:
            path = self.write_log(directory, [
                gui("GuiButton", 100, 100, 50, 20),
                gui("GuiButton", 140, 100, 50, 20),
            ])
            self.assertEqual(rules(check_geometry.check_log(path)), [3])

    def test_file_without_header_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "scene.geometry.jsonl"
            path.write_text(json.dumps(text("Back", 10, 10, 40, 12)) + "\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                check_geometry.check_log(path)


if __name__ == "__main__":
    unittest.main()
