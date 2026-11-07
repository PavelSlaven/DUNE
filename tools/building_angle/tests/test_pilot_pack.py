import os
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "tools" / "building_angle"))

import angle
from hd_assets import decode_image, read_pack

PACK = Path(os.environ.get("D2TM_PACK_DIR", ROOT / "resources/bin/data")) / "sdl_data_hd4.dat"


@unittest.skipUnless(PACK.is_file() and PACK.stat().st_size > 1_000_000, "HD4 pack is not checked out")
class PilotPackTests(unittest.TestCase):
    def setUp(self):
        self.entries = {entry.name: entry for entry in read_pack(PACK)}

    def image(self, name):
        image = decode_image(self.entries[name].payload)
        self.assertIsNotNone(image, name)
        return image.convert("RGBA")

    def test_build_radar_reaches_every_edge(self):
        ok, rows = angle.check(self.image("BUILD_RADAR"), (2, 2), 32)
        self.assertTrue(ok, rows)

    def test_build_windtrap_reaches_every_edge(self):
        ok, rows = angle.check(self.image("BUILD_WINDTRAP"), (2, 2), 1)
        self.assertTrue(ok, rows)

    def test_build_windtrap_flag_pole_is_opaque(self):
        flag = self.image("BUILD_WINDTRAP_FLAG")
        for frame in range(8):
            area = flag.crop((208, frame * 256 + 150, 214, frame * 256 + 179)).getchannel("A")
            self.assertEqual(area.getextrema(), (255, 255), f"frame {frame}")


if __name__ == "__main__":
    unittest.main()
