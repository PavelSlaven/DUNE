import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import check_completeness  # noqa: E402
import combos  # noqa: E402

WORLD = [100, 110, 125, 150]
RENDER_COUNTS = {"1024x768": 2, "1280x720": 1, "1366x768": 2, "1600x900": 3, "1920x1080": 4, "2560x1440": 5}
SCALES = {res: {"render": [100 + 25 * i for i in range(count)], "world": list(WORLD)}
          for res, count in RENDER_COUNTS.items()}

SCENES = [
    {"id": "main-menu", "hd_only": False, "game_screen": False, "hud": False},
    {"id": "hd-extra", "hd_only": True, "game_screen": False, "hud": False},
    {"id": "game-screen", "hd_only": False, "game_screen": True, "hud": True},
    {"id": "units-label-trike", "hd_only": False, "game_screen": True, "hud": False},
    {"id": "units-label-hd", "hd_only": True, "game_screen": True, "hud": False},
]


def find(generated, **fields):
    return [c for c in generated if all(c[key] == value for key, value in fields.items())]


class ScaleListParsing(unittest.TestCase):
    def test_game_output_is_parsed(self):
        text = json.dumps({"resolution": "1280x720", "render": [100], "world": [100, 110, 125, 150]})
        self.assertEqual(combos.parse_scales(text), ("1280x720", [100], [100, 110, 125, 150]))


class CombinationCounts(unittest.TestCase):
    def setUp(self):
        self.generated = combos.generate(SCALES)

    def test_total_is_230_with_12_old_and_218_new(self):
        self.assertEqual(len(self.generated), 230)
        self.assertEqual(len([c for c in self.generated if c["legacy"]]), 12)
        self.assertEqual(len([c for c in self.generated if not c["legacy"]]), 218)

    def test_every_combination_is_unique(self):
        ids = [combos.combo_id(c) for c in self.generated]
        self.assertEqual(len(set(ids)), 230)

    def test_old_combinations_are_the_automatic_scales_of_hd(self):
        legacy = [c for c in self.generated if c["legacy"]]
        self.assertTrue(all(c["render"] == 0 and c["world"] == 0 and c["scope"] == "all" for c in legacy))
        self.assertEqual({c["graphics"] for c in legacy}, {"hd"})
        self.assertEqual({c["language"] for c in legacy}, {"ru", "en"})
        self.assertEqual({c["resolution"] for c in legacy}, set(RENDER_COUNTS))

    def test_hd_has_46_full_and_184_game_only_combinations(self):
        hd = find(self.generated, graphics="hd")
        self.assertEqual(len(hd), 230)
        self.assertEqual(len([c for c in hd if c["scope"] == "all"]), 46)
        game = [c for c in hd if c["scope"] == "game"]
        self.assertEqual(len(game), 184)
        self.assertTrue(all(c["world"] != 0 for c in game))

    def test_full_scope_hd_combinations_have_automatic_object_size(self):
        full = [c for c in find(self.generated, graphics="hd") if c["scope"] == "all"]
        self.assertTrue(all(c["world"] == 0 for c in full))

    def test_game_scale_variants_per_resolution_are_automatic_plus_manual(self):
        for res, count in RENDER_COUNTS.items():
            renders = {c["render"] for c in find(self.generated, resolution=res, graphics="hd", language="ru")}
            self.assertEqual(len(renders), count + 1)
            self.assertIn(0, renders)

    def test_manual_object_sizes_cover_every_game_scale_variant(self):
        subset = find(self.generated, resolution="1280x720", language="ru", graphics="hd", scope="game")
        self.assertEqual(sorted((c["render"], c["world"]) for c in subset),
                         sorted((r, w) for r in (0, 100) for w in WORLD))


class CombinationNames(unittest.TestCase):
    def test_old_combination_keeps_the_old_name(self):
        legacy = find(combos.generate(SCALES), resolution="1024x768", language="ru", graphics="hd", render=0, world=0)
        self.assertEqual(len(legacy), 1)
        self.assertEqual(combos.combo_id(legacy[0]), "1024x768/ru/hd")

    def test_new_combination_name_ends_with_the_scales(self):
        new = find(combos.generate(SCALES), resolution="1024x768", language="ru", graphics="hd", render=125, world=110)
        self.assertEqual(len(new), 1)
        self.assertEqual(combos.combo_id(new[0]), "1024x768/ru/hd/r125w110")

    def test_automatic_object_size_with_manual_game_scale(self):
        new = find(combos.generate(SCALES), resolution="1024x768", language="en", graphics="hd", render=125, world=0)
        self.assertEqual(combos.combo_id(new[0]), "1024x768/en/hd/r125w0")


class ScenesAndPng(unittest.TestCase):
    def setUp(self):
        self.generated = combos.generate(SCALES)

    def pick(self, **fields):
        return find(self.generated, **fields)[0]

    def test_game_scope_keeps_only_game_screen_scenes(self):
        game = self.pick(graphics="hd", scope="game", resolution="1280x720", language="ru", render=0, world=110)
        ids = [s["id"] for s in combos.scenes_for(game, SCENES)]
        self.assertEqual(ids, ["game-screen", "units-label-trike", "units-label-hd"])

    def test_full_scope_hd_keeps_all_scenes(self):
        full = self.pick(graphics="hd", scope="all", resolution="1280x720", language="ru", render=100, world=0)
        self.assertEqual(len(combos.scenes_for(full, SCENES)), 5)

    def test_old_combination_keeps_png_of_full_resolution_hud_and_flagged_scenes(self):
        low = self.pick(legacy=True, resolution="1280x720", language="ru", graphics="hd")
        full = self.pick(legacy=True, resolution="1920x1080", language="ru", graphics="hd")
        by_id = {s["id"]: s for s in SCENES}
        self.assertFalse(combos.keep_png(low, by_id["main-menu"], set()))
        self.assertTrue(combos.keep_png(low, by_id["game-screen"], set()))
        self.assertTrue(combos.keep_png(low, by_id["main-menu"], {("1280x720/ru/hd", "main-menu")}))
        self.assertTrue(combos.keep_png(full, by_id["main-menu"], set()))

    def test_new_combination_keeps_png_only_of_flagged_scenes(self):
        new = self.pick(legacy=False, resolution="1920x1080", language="ru", graphics="hd", render=0, world=110)
        by_id = {s["id"]: s for s in SCENES}
        self.assertFalse(combos.keep_png(new, by_id["game-screen"], set()))
        self.assertTrue(combos.keep_png(new, by_id["game-screen"], {("1920x1080/ru/hd/r0w110", "game-screen")}))


class NewCombinationCompleteness(unittest.TestCase):
    def combo(self):
        return find(combos.generate(SCALES), resolution="1280x720", language="ru", graphics="hd", render=100, world=0)[0]

    def write(self, root, relative):
        path = Path(root) / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"x")

    def test_logs_of_all_scenes_and_png_of_flagged_scenes_are_complete(self):
        combo = self.combo()
        combo_id = combos.combo_id(combo)
        with tempfile.TemporaryDirectory() as root:
            for scene in combos.scenes_for(combo, SCENES):
                self.write(root, f"logs/{combo_id}/{scene['id']}.geometry.jsonl")
            self.write(root, f"png/{combo_id}/main-menu.png")
            problems = check_completeness.check_combinations(
                root, SCENES, {(combo_id, "main-menu")}, [combo])
        self.assertEqual(problems, [])

    def test_missing_log_and_missing_flagged_png_are_reported(self):
        combo = self.combo()
        combo_id = combos.combo_id(combo)
        with tempfile.TemporaryDirectory() as root:
            self.write(root, f"logs/{combo_id}/main-menu.geometry.jsonl")
            problems = check_completeness.check_combinations(
                root, SCENES, {(combo_id, "main-menu")}, [combo])
        kinds = sorted(kind for kind, _ in problems)
        self.assertEqual(kinds, ["missing-log"] * 4 + ["missing-png"])

    def test_png_of_an_unflagged_scene_is_extra(self):
        combo = self.combo()
        combo_id = combos.combo_id(combo)
        with tempfile.TemporaryDirectory() as root:
            for scene in combos.scenes_for(combo, SCENES):
                self.write(root, f"logs/{combo_id}/{scene['id']}.geometry.jsonl")
            self.write(root, f"png/{combo_id}/game-screen.png")
            problems = check_completeness.check_combinations(root, SCENES, set(), [combo])
        self.assertEqual(problems, [("extra-png", f"png/{combo_id}/game-screen.png")])


if __name__ == "__main__":
    unittest.main()
