import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import combos  # noqa: E402
import finalize_png  # noqa: E402
import run_combo  # noqa: E402

RESOLUTION = "1280x720"
ORDER = [f"{RESOLUTION}/en/hd", f"{RESOLUTION}/en/hd/r100w110", f"{RESOLUTION}/en/hd/r125w110"]


def header(identifier, scene):
    parts = identifier.split("/")
    extra = {}
    if len(parts) == 4:
        render, world = parts[3][1:].split("w")
        extra = {"render_scale": int(render), "world_scale": int(world)}
    head = {"k": "header", "scene": scene, "resolution": parts[0], "language": parts[1], "graphics": parts[2],
            "canvas": {"w": 800, "h": 600}, "game_screen": True, "version": "test"}
    head.update(extra)
    return head


def area(name, x, y, w, h):
    return {"k": "area", "n": name, "x": x, "y": y, "w": w, "h": h}


def write_log(root, identifier, scene, records):
    path = Path(root) / "logs" / identifier / f"{scene}.geometry.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(json.dumps(r) for r in [header(identifier, scene)] + records) + "\n", encoding="utf-8")
    return path


def flagged(root, identifier, scene):
    path = Path(root) / "logs" / identifier / f"{scene}.geometry.jsonl"
    return run_combo.has_new_flag(root, ORDER, combos.parse_id(identifier), scene, path)


class CaptureDecisionTest(unittest.TestCase):
    def test_same_key_with_other_coordinates_gives_no_png_and_a_new_key_does(self):
        with tempfile.TemporaryDirectory() as root:
            write_log(root, ORDER[0], "s", [area("left", 0, 0, 100, 100), area("right", 50, 0, 100, 100)])
            write_log(root, ORDER[1], "s", [area("left", 0, 0, 120, 100), area("right", 60, 10, 100, 100)])
            write_log(root, ORDER[2], "s", [area("left", 0, 0, 100, 100), area("top", 50, 0, 100, 100)])
            self.assertTrue(flagged(root, ORDER[0], "s"))
            self.assertFalse(flagged(root, ORDER[1], "s"))
            self.assertTrue(flagged(root, ORDER[2], "s"))

    def test_scene_without_flags_gets_no_png(self):
        with tempfile.TemporaryDirectory() as root:
            write_log(root, ORDER[0], "s", [area("left", 0, 0, 10, 10)])
            self.assertFalse(flagged(root, ORDER[0], "s"))

    def test_other_resolution_does_not_count_as_earlier(self):
        order = ["1024x768/en/hd", *ORDER]
        self.assertEqual(combos.earlier_ids(order, ORDER[1]), [ORDER[0]])


def flag(combo, scene, rule, names):
    return {"rule": rule, "scene": scene, "combo": combo, "names": names, "texts": []}


class FinalSelectionTest(unittest.TestCase):
    def test_png_goes_to_the_first_combination_with_the_key(self):
        flags = [flag(ORDER[1], "s", 3, ["b", "a"]), flag(ORDER[2], "s", 3, ["a", "b"]),
                 flag(ORDER[2], "s", 3, ["a", "c"])]
        self.assertEqual(combos.png_required(flags, ORDER), {(ORDER[1], "s"), (ORDER[2], "s")})
        self.assertEqual(combos.first_combo_by_key(flags, ORDER)[(RESOLUTION, ("s", 3, ("a", "b")))], ORDER[1])

    def test_legacy_combination_always_keeps_flagged_scene(self):
        flags = [flag(ORDER[0], "s", 3, ["a"]), flag(ORDER[1], "s", 3, ["a"])]
        self.assertEqual(combos.png_required(flags, ORDER), {(ORDER[0], "s")})

    def test_finalize_lists_extra_and_missing_png(self):
        flags = [flag(ORDER[1], "s", 3, ["a"]), flag(ORDER[2], "s", 3, ["a"]), flag(ORDER[2], "t", 6, [])]
        with tempfile.TemporaryDirectory() as root:
            for identifier, scene in ((ORDER[1], "s"), (ORDER[2], "s")):
                path = Path(root) / "png" / identifier / f"{scene}.png"
                path.parent.mkdir(parents=True)
                path.write_bytes(b"x")
            missing, extra = finalize_png.plan_actions(root, flags, ORDER)
        self.assertEqual(missing, [(ORDER[2], "t")])
        self.assertEqual(extra, [(ORDER[2], "s")])


if __name__ == "__main__":
    unittest.main()
