import json
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import build_sheets  # noqa: E402
import combos  # noqa: E402

META = {f"s{i}": {"id": f"s{i}", "screen": "cScreen", "state": "GAME_X", "house": "Atreides" if i == 0 else ""}
        for i in range(8)}


def make_png(root, combo_id, scene, size=(320, 240), color=(10, 20, 30)):
    path = Path(root) / "png" / combo_id / f"{scene}.png"
    path.parent.mkdir(parents=True, exist_ok=True)
    Image.new("RGB", size, color).save(path)
    return path


def make_log(root, combo_id, scene, width):
    path = Path(root) / "logs" / combo_id / f"{scene}.geometry.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"k": "header", "canvas": {"w": width, "h": 100}}) + "\n", encoding="utf-8")


class HelpersTest(unittest.TestCase):
    def test_chunks_of_six(self):
        self.assertEqual([len(group) for group in build_sheets.chunks(list(range(13)))], [6, 6, 1])

    def test_caption_names_screen_state_house_resolution_language_graphics_and_scales(self):
        combo = combos.parse_id("1024x768/ru/hd/r150w125")
        text = " ".join(build_sheets.caption_lines(META["s0"], combo))
        for part in ("s0", "cScreen", "GAME_X", "Atreides", "1024x768", "ru", "hd", "render 150", "world 125"):
            self.assertIn(part, text)

    def test_zero_scale_is_called_auto(self):
        self.assertEqual(build_sheets.scale_text(combos.legacy_combo("1024x768/ru/hd")), "render auto / world auto")

    def test_flag_rects_scale_by_factor_and_use_two_colors(self):
        flag = {"a": {"x": 1, "y": 2, "w": 3, "h": 4}, "b": {"x": 5, "y": 6, "w": 7, "h": 8}}
        rects = build_sheets.flag_rects(flag, 2.0)
        self.assertEqual(rects[0][0], {"x": 2.0, "y": 4.0, "w": 6.0, "h": 8.0})
        self.assertNotEqual(rects[0][1], rects[1][1])

    def test_duplicate_flags_collapse(self):
        flag = {"rule": 2, "scene": "s0", "combo": "c", "a": {"x": 0}, "b": None}
        self.assertEqual(len(build_sheets.unique_flags([flag, dict(flag)])), 1)


class SheetsTest(unittest.TestCase):
    def test_catalog_sheets_hold_six_frames_in_three_by_two_grid(self):
        with tempfile.TemporaryDirectory() as root:
            for scene in META:
                make_png(root, "1024x768/ru/hd", scene)
            written = build_sheets.build_catalog_sheets(Path(root) / "png", META, "1024x768/ru/hd", Path(root) / "out")
            self.assertEqual(len(written), 2)
            width, height = Image.open(written[0]).size
            self.assertGreater(width, height)
            self.assertEqual(written[0].suffix, ".jpg")

    def test_frames_missing_from_png_folder_are_skipped(self):
        with tempfile.TemporaryDirectory() as root:
            make_png(root, "1024x768/ru/hd", "s1")
            written = build_sheets.build_catalog_sheets(Path(root) / "png", META, "1024x768/ru/hd", Path(root) / "out")
            self.assertEqual(len(written), 1)

    def test_flag_sheet_draws_rectangles_over_the_frame(self):
        with tempfile.TemporaryDirectory() as root:
            png = make_png(root, "1024x768/ru/hd", "s1", size=(640, 480), color=(0, 0, 0))
            make_log(root, "1024x768/ru/hd", "s1", 320)
            flag = {"rule": 2, "scene": "s1", "combo": "1024x768/ru/hd", "a": {"x": 10, "y": 10, "w": 50, "h": 50},
                    "b": None, "texts": ["Hello"]}
            self.assertEqual(build_sheets.canvas_factor(png, Path(root) / "logs", "1024x768/ru/hd", "s1"), 2.0)
            written, missing = build_sheets.build_flag_sheets(
                Path(root) / "png", Path(root) / "logs", META, [flag], Path(root) / "out")
            self.assertEqual((len(written), missing), (1, []))
            reddish = any(r > 180 and g < 80 and b < 80 for r, g, b in Image.open(written[0]).getdata())
            self.assertTrue(reddish)

    def test_flag_without_png_is_reported_missing(self):
        with tempfile.TemporaryDirectory() as root:
            flag = {"rule": 6, "scene": "s1", "combo": "1024x768/ru/hd", "a": None, "b": None, "texts": []}
            written, missing = build_sheets.build_flag_sheets(
                Path(root) / "png", Path(root) / "logs", META, [flag], Path(root) / "out")
            self.assertEqual((written, missing), ([], [("s1", "1024x768/ru/hd", 6)]))


class IndexTest(unittest.TestCase):
    def test_index_links_every_png_and_has_filters(self):
        with tempfile.TemporaryDirectory() as root:
            make_png(root, "1024x768/ru/hd", "s0")
            make_png(root, "1280x720/en/classic/r150w0", "s1")
            index = Path(root) / "out" / "index.html"
            index.parent.mkdir()
            rows = build_sheets.build_index(Path(root) / "png", META, [], [], index)
            text = index.read_text(encoding="utf-8")
            self.assertEqual(rows, 2)
            self.assertIn("../png/1024x768/ru/hd/s0.png", text)
            self.assertIn("../png/1280x720/en/classic/r150w0/s1.png", text)
            self.assertIn('data-col="6"', text)

    def test_index_counts_flags_per_frame(self):
        with tempfile.TemporaryDirectory() as root:
            make_png(root, "1024x768/ru/hd", "s0")
            flag = {"rule": 2, "scene": "s0", "combo": "1024x768/ru/hd", "a": None, "b": None}
            index = Path(root) / "index.html"
            build_sheets.build_index(Path(root) / "png", META, [flag], [], index)
            self.assertIn("<td>1</td></tr>", index.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
