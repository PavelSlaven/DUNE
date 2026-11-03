import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import combos  # noqa: E402
import run_all  # noqa: E402

SCALES = {"1024x768": {"render": [1, 2], "world": [3]}, "1280x720": {"render": [1], "world": [2]}}


class PlanTest(unittest.TestCase):
    def test_legacy_combinations_come_first(self):
        ordered = run_all.plan(combos.generate(SCALES))
        kinds = [combo["legacy"] for combo in ordered]
        self.assertEqual(kinds, sorted(kinds, reverse=True))

    def test_plan_keeps_every_combination_once(self):
        generated = combos.generate(SCALES)
        ordered = run_all.plan(generated)
        self.assertEqual(sorted(map(combos.combo_id, ordered)), sorted(map(combos.combo_id, generated)))

    def test_new_combinations_alternate_between_resolutions(self):
        new = [combo for combo in run_all.plan(combos.generate(SCALES)) if not combo["legacy"]]
        self.assertEqual({combo["resolution"] for combo in new[:2]}, {"1024x768", "1280x720"})

    def test_interleave_takes_one_item_from_each_chain_in_turn(self):
        self.assertEqual(run_all.interleave([[1, 2, 3], [4], [5, 6]]), [1, 4, 5, 2, 6, 3])


class SizeTest(unittest.TestCase):
    def test_forecast_scales_bytes_per_scene(self):
        self.assertAlmostEqual(run_all.forecast_gb(1024 ** 3, 100, 300), 3.0)

    def test_forecast_without_finished_scenes_is_zero(self):
        self.assertEqual(run_all.forecast_gb(0, 0, 10), 0.0)

    def test_combo_bytes_counts_logs_and_png(self):
        combo = combos.legacy_combo("1024x768/ru/hd")
        with tempfile.TemporaryDirectory() as root:
            for kind, size in (("logs", 10), ("png", 5)):
                directory = Path(root) / kind / "1024x768" / "ru" / "hd"
                directory.mkdir(parents=True)
                (directory / "a").write_bytes(b"x" * size)
            self.assertEqual(run_all.combo_bytes(root, combo), 15)

    def test_done_marker_path_has_no_slashes_in_name(self):
        marker = run_all.done_marker("out", combos.parse_id("1024x768/ru/hd/r1w2"))
        self.assertEqual(marker.name, "1024x768_ru_hd_r1w2")


if __name__ == "__main__":
    unittest.main()
