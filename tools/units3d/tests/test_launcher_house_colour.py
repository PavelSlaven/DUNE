import configparser
import os
from pathlib import Path
import statistics
import sys
import unittest


ROOT = Path(__file__).resolve().parents[3]
PACK_PATH = Path(os.environ.get("D2TM_PACK_DIR", ROOT / "resources/bin/data")) / "sdl_data_hd4.dat"
sys.path.insert(0, str(ROOT / "tools"))


def _measure(body, mask, house_rgb):
    pixels = zip(body.get_flattened_data(), mask.get_flattened_data())
    full_luminance = []
    effective_mask = []
    selected_luminance = []

    for body_pixel, mask_pixel in pixels:
        red, green, blue, alpha = mask_pixel
        s = (alpha / 255) * max(red, green, blue) / 255
        body_red, body_green, body_blue, body_alpha = body_pixel
        luminance = (0.299 * body_red + 0.587 * body_green + 0.114 * body_blue) / 128

        if s >= 0.99 and body_alpha != 0:
            full_luminance.append(luminance)
        if body_alpha > 127:
            effective_mask.append(s)
            if s >= 0.5:
                selected_luminance.append(luminance)

    avg = statistics.mean(full_luminance) if full_luminance else 166 / 255
    eff = statistics.mean(effective_mask) if effective_mask else 0
    std_l_over_avg = (
        statistics.pstdev(selected_luminance) / avg if selected_luminance else 0
    )
    clipped = sum(
        any(channel * luminance * (166 / 255) / avg > 255 for channel in house_rgb)
        for luminance in selected_luminance
    )
    clip = clipped / len(selected_luminance) if selected_luminance else 0

    return {
        "avg": avg,
        "eff": eff,
        "stdL_over_avg": std_l_over_avg,
        "clip": clip,
    }


class LauncherHouseColourTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from hd_assets import decode_image, read_pack

        packed_entries = {entry.name: entry for entry in read_pack(PACK_PATH)}
        cls.images = {}
        for name in (
            "UNIT_LAUNCHER",
            "HM_UNIT_LAUNCHER",
            "UNIT_DEVIATOR",
            "HM_UNIT_DEVIATOR",
        ):
            image = decode_image(packed_entries[name].payload)
            if image is None:
                raise AssertionError(f"{name}: pack entry is not a decodable image")
            cls.images[name] = image.convert("RGBA")

        config = configparser.ConfigParser()
        config.read(ROOT / "resources/game.ini", encoding="utf-8")
        house_keys = {
            "ORDOS": "ORDOS_MINIMAPCOLOR",
            "ATREIDES": "ATREIDES_MINIMAPCOLOR",
            "HARKONNEN": "HARKONNEN_MINIMAPCOLOR",
        }
        cls.house_colours = {
            house: tuple(
                int(channel.strip())
                for channel in config.get("HOUSES", key).split(",")
            )
            for house, key in house_keys.items()
        }

    def _metrics(self, unit, house_rgb):
        body = self.images[f"UNIT_{unit}"]
        mask = self.images[f"HM_UNIT_{unit}"]
        self.assertEqual(body.size, mask.size, f"{unit}: body and mask sizes differ")
        return _measure(body, mask, house_rgb)

    def test_launcher_effective_mask_is_between_045_and_055(self):
        metrics = self._metrics("LAUNCHER", self.house_colours["ORDOS"])
        self.assertGreaterEqual(metrics["eff"], 0.45)
        self.assertLessEqual(metrics["eff"], 0.55)

    def test_launcher_luminance_ratio_is_at_least_80_percent_of_deviator(self):
        launcher = self._metrics("LAUNCHER", self.house_colours["ORDOS"])
        deviator = self._metrics("DEVIATOR", self.house_colours["ORDOS"])
        self.assertGreaterEqual(
            launcher["stdL_over_avg"], 0.8 * deviator["stdL_over_avg"]
        )

    def test_launcher_clip_rate_is_within_five_points_for_each_house(self):
        for house, house_rgb in self.house_colours.items():
            with self.subTest(house=house):
                launcher = self._metrics("LAUNCHER", house_rgb)
                deviator = self._metrics("DEVIATOR", house_rgb)
                self.assertLessEqual(launcher["clip"], deviator["clip"] + 0.05)


if __name__ == "__main__":
    unittest.main()
