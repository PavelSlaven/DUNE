import os
import sys
import unittest
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "tools" / "building_angle"))

import angle  # noqa: E402

PACK = Path(os.environ.get("D2TM_PACK_DIR", ROOT / "resources/bin/data")) / "sdl_data_hd4.dat"


def block(size, box):
    image = Image.new("RGB", size, angle.MAGENTA)
    ImageDraw.Draw(image).rectangle(box, fill=(120, 110, 100))
    return image


class GuideTests(unittest.TestCase):
    def test_faces_follow_outpost_proportions(self):
        g = angle.guide((1024, 1024))
        self.assertEqual(g.getpixel((0, 0)), angle.MAGENTA)
        self.assertEqual(g.getpixel((512, 10)), angle.ROOF)
        self.assertEqual(g.getpixel((2, 400)), angle.ROOF)
        self.assertEqual(g.getpixel((512, 1000)), angle.FRONT_WALL)
        self.assertEqual(g.getpixel((512, 740)), angle.ROOF)
        self.assertEqual(g.getpixel((512, 760)), angle.FRONT_WALL)

    def test_fitted_guide_reaches_every_edge(self):
        ok, rows = angle.check(angle.fit(angle.guide((1536, 1024)), (3, 2)), (3, 2), 1)
        self.assertTrue(ok, rows)


class FitTests(unittest.TestCase):
    def test_block_with_margins_is_stretched_edge_to_edge(self):
        frame = angle.fit(block((1024, 1024), (100, 150, 900, 950)), (2, 2))
        self.assertEqual(frame.size, (256, 256))
        coverage = angle.edge_coverage(frame)
        for edge in ("top", "bottom", "left", "right"):
            self.assertGreaterEqual(coverage[edge], 0.99, edge)

    def test_stray_speck_is_dropped(self):
        image = block((1024, 1024), (100, 150, 900, 950))
        ImageDraw.Draw(image).rectangle((10, 10, 14, 14), fill=(0, 0, 0))
        frame = angle.fit(image, (2, 2))
        self.assertGreaterEqual(angle.edge_coverage(frame)["left"], 0.99)

    def test_transparent_background_stays_transparent(self):
        image = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
        ImageDraw.Draw(image).rectangle((40, 40, 215, 215), fill=(120, 120, 120, 255))
        frame = angle.fit(image, (2, 2))
        self.assertEqual(frame.size, (256, 256))
        self.assertEqual(angle.opaque_box(frame), (0, 0, 256, 256))
        r, g, b, a = frame.getpixel((0, 0))
        self.assertEqual((r, g, b), (120, 120, 120))
        self.assertGreater(a, 127)


class CheckTests(unittest.TestCase):
    def test_margins_fail(self):
        frame = Image.new("RGBA", (256, 256))
        ImageDraw.Draw(frame).rectangle((20, 10, 235, 245), fill=(90, 90, 90, 255))
        ok, rows = angle.check(frame, (2, 2), 1)
        self.assertFalse(ok)
        self.assertEqual(rows[0]["left"], 0.0)

    def test_transparent_rim_fails(self):
        frame = Image.new("RGBA", (256, 256))
        ImageDraw.Draw(frame).rectangle((2, 2, 253, 253), fill=(90, 90, 90, 255))
        ok, rows = angle.check(frame, (2, 2), 1)
        self.assertFalse(ok, rows)


class StretchTests(unittest.TestCase):
    def test_all_frames_share_one_box(self):
        frames = []
        for dx in (0, 30):
            f = Image.new("RGBA", (256, 256))
            d = ImageDraw.Draw(f)
            d.rectangle((20, 10, 235, 245), fill=(90, 90, 90, 255))
            d.rectangle((100 + dx, 40, 110 + dx, 50), fill=(250, 0, 0, 255))
            frames.append(f)
        out = angle.frames_of(angle.stretch(angle.join(frames), (2, 2), 2), (2, 2), 2)
        ok, _ = angle.check(angle.join(out), (2, 2), 2)
        self.assertTrue(ok)
        self.assertEqual(out[0].getpixel((5, 200)), out[1].getpixel((5, 200)))


class ShadowTests(unittest.TestCase):
    def test_shadow_is_offset_and_faint(self):
        f = Image.new("RGBA", (256, 256))
        ImageDraw.Draw(f).rectangle((0, 0, 255, 255), fill=(90, 90, 90, 255))
        s = angle.shadow(f, (2, 2), 1)
        self.assertEqual(s.getpixel((3, 3))[3], 0)
        self.assertEqual(s.getpixel((128, 128))[3], round(255 * 0.22))


@unittest.skipUnless(PACK.is_file() and PACK.stat().st_size > 1_000_000, "HD4 pack is not checked out")
class OutpostPackTests(unittest.TestCase):
    def setUp(self):
        from hd_assets import decode_image, read_pack
        entries = {e.name: e for e in read_pack(PACK)}
        self.radar = decode_image(entries["BUILD_RADAR"].payload).convert("RGBA")

    def test_current_outpost_leaves_margins(self):
        ok, rows = angle.check(self.radar, (2, 2), 16)
        if ok:
            self.skipTest("pack already holds an edge-to-edge Outpost")
        self.assertLess(rows[0]["left"], angle.MIN_EDGE_COVERAGE)

    def test_stretched_outpost_reaches_every_edge(self):
        ok, rows = angle.check(angle.stretch(self.radar, (2, 2), 16), (2, 2), 16)
        self.assertTrue(ok, rows)


if __name__ == "__main__":
    unittest.main()
