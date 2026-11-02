import json
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import build_sheets  # noqa: E402
import check_completeness  # noqa: E402
import combos  # noqa: E402

LEGACY = "1280x720/ru/hd"
SECOND = "1280x720/ru/hd/r100w110"
THIRD = "1280x720/ru/hd/r125w110"
ORDER = [LEGACY, SECOND, THIRD]
SCENES = [{"id": "s", "hud": False, "game_screen": True}]


def touch(root, relative, data=b"x"):
    path = Path(root) / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def flag(combo, names, rect):
    return {"rule": 3, "scene": "s", "combo": combo, "names": names, "texts": [], "a": rect, "b": None}


class CompletenessOrderTest(unittest.TestCase):
    def run_check(self, root, flags, png_combos):
        for identifier in ORDER:
            touch(root, f"logs/{identifier}/s.geometry.jsonl")
        for identifier in png_combos:
            touch(root, f"png/{identifier}/s.png")
        flagged = {(f["combo"], f["scene"]) for f in flags}
        return check_completeness.check_combinations(
            root, SCENES, flagged, [combos.parse_id(i) for i in ORDER], combos.png_required(flags, ORDER))

    def test_new_combination_with_repeated_key_needs_no_png(self):
        flags = [flag(LEGACY, ["a"], {"x": 0}), flag(SECOND, ["a"], {"x": 5})]
        with tempfile.TemporaryDirectory() as root:
            self.assertEqual(self.run_check(root, flags, [LEGACY]), [])

    def test_png_of_repeated_key_is_reported_as_extra(self):
        flags = [flag(LEGACY, ["a"], {"x": 0}), flag(SECOND, ["a"], {"x": 5})]
        with tempfile.TemporaryDirectory() as root:
            problems = self.run_check(root, flags, [LEGACY, SECOND])
        self.assertEqual(problems, [("extra-png", f"png/{SECOND}/s.png")])

    def test_new_key_without_png_is_reported_as_missing(self):
        flags = [flag(LEGACY, ["a"], {"x": 0}), flag(THIRD, ["b"], {"x": 0})]
        with tempfile.TemporaryDirectory() as root:
            problems = self.run_check(root, flags, [LEGACY])
        self.assertEqual(problems, [("missing-png", f"png/{THIRD}/s.png")])


class DisplayFlagsTest(unittest.TestCase):
    def test_flag_without_own_png_shows_the_first_combination_with_the_same_key(self):
        flags = [flag(LEGACY, ["a"], {"x": 1, "y": 1, "w": 1, "h": 1}),
                 flag(SECOND, ["a"], {"x": 9, "y": 9, "w": 1, "h": 1})]
        with tempfile.TemporaryDirectory() as root:
            png_root = Path(root) / "png"
            touch(png_root, f"{LEGACY}/s.png")
            shown = build_sheets.display_flags(png_root, flags, ORDER)
        self.assertEqual([item["combo"] for item in shown], [LEGACY, LEGACY])
        self.assertEqual(len(build_sheets.unique_flags(shown)), 1)

    def test_flag_with_own_png_keeps_its_own_combination(self):
        flags = [flag(LEGACY, ["a"], {"x": 1}), flag(SECOND, ["a"], {"x": 9})]
        with tempfile.TemporaryDirectory() as root:
            png_root = Path(root) / "png"
            touch(png_root, f"{LEGACY}/s.png")
            touch(png_root, f"{SECOND}/s.png")
            shown = build_sheets.display_flags(png_root, flags, ORDER)
        self.assertEqual([item["combo"] for item in shown], [LEGACY, SECOND])

    def test_flag_sheet_caption_names_the_source_combination(self):
        flags = [flag(LEGACY, ["a"], {"x": 1, "y": 1, "w": 5, "h": 5}),
                 flag(SECOND, ["a"], {"x": 9, "y": 9, "w": 5, "h": 5})]
        with tempfile.TemporaryDirectory() as root:
            png_root = Path(root) / "png"
            png = png_root / LEGACY / "s.png"
            png.parent.mkdir(parents=True)
            Image.new("RGB", (320, 240)).save(png)
            logs = Path(root) / "logs" / LEGACY / "s.geometry.jsonl"
            logs.parent.mkdir(parents=True)
            logs.write_text(json.dumps({"k": "header", "canvas": {"w": 320, "h": 240}}) + "\n", encoding="utf-8")
            written, missing = build_sheets.build_flag_sheets(
                png_root, Path(root) / "logs", {"s": {"id": "s"}}, flags, Path(root) / "out", ORDER)
        self.assertEqual((len(written), missing), (1, []))


if __name__ == "__main__":
    unittest.main()
