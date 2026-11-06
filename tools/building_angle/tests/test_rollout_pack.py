import os
import sys
import unittest
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "tools" / "building_angle"))

import angle
from hd_assets import decode_image, read_pack

PACK = Path(os.environ.get("D2TM_PACK_DIR", ROOT / "resources/bin/data")) / "sdl_data_hd4.dat"


@unittest.skipUnless(PACK.is_file() and PACK.stat().st_size > 1_000_000, "HD4 pack is not checked out")
class RolloutPackTests(unittest.TestCase):
    def setUp(self):
        self.entries = {entry.name: entry for entry in read_pack(PACK)}

    def image(self, name):
        image = decode_image(self.entries[name].payload)
        self.assertIsNotNone(image, name)
        return image.convert("RGBA")

    @staticmethod
    def rect_mask(size, rectangles, expansion=0):
        mask = np.zeros((size[1], size[0]), dtype=bool)
        for x0, y0, x1, y1 in rectangles:
            x0 = max(0, x0 - expansion)
            y0 = max(0, y0 - expansion)
            x1 = min(size[0] - 1, x1 + expansion)
            y1 = min(size[1] - 1, y1 + expansion)
            mask[y0:y1 + 1, x0:x1 + 1] = True
        return mask

    def test_buildings_fill_their_slab(self):
        records = (
            ("BUILD_BARRACKS", (2, 2), 1),
            ("BUILD_CONSTYARD", (2, 2), 1),
            ("BUILD_IX", (2, 2), 1),
            ("BUILD_LIGHTFACTORY", (2, 2), 8),
            ("BUILD_RADAR", (2, 2), 16),
            ("BUILD_SILO", (2, 2), 1),
            ("BUILD_WOR", (2, 2), 1),
            ("BUILD_PALACE", (3, 3), 1),
            ("BUILD_REFINERY", (3, 2), 8),
            ("BUILD_REPAIR", (3, 2), 8),
            ("BUILD_HEAVYFACTORY", (3, 2), 11),
        )
        for name, slab, count in records:
            with self.subTest(record=name):
                ok, rows = angle.check(self.image(name), slab, count)
                self.assertTrue(ok, rows)

    def test_radar_dish_turns_inside_its_circle(self):
        frames = angle.frames_of(self.image("BUILD_RADAR"), (2, 2), 16)
        baseline = np.asarray(frames[0])
        y, x = np.ogrid[:256, :256]
        allowed = (x - 130) ** 2 + (y - 114) ** 2 <= 128 ** 2
        arrays = [baseline]
        for frame_index in range(1, 16):
            current = np.asarray(frames[frame_index])
            arrays.append(current)
            changed = np.any(current != baseline, axis=2)
            with self.subTest(frame=frame_index):
                self.assertFalse(np.any(changed & ~allowed), "pixels changed outside the dish circle")
                self.assertGreaterEqual(int(changed.sum()), 5000, "too few pixels changed")
        for left in range(16):
            for right in range(left + 1, 16):
                with self.subTest(frame_pair=(left, right)):
                    self.assertFalse(np.array_equal(arrays[left], arrays[right]), "frames are identical")

    def test_radar_has_no_flag(self):
        alpha = np.asarray(self.image("BUILD_RADAR_FLAG"))[..., 3]
        self.assertTrue(np.all(alpha == 0), "BUILD_RADAR_FLAG is not fully transparent")

    def test_stretched_buildings_touch_every_edge(self):
        records = (("BUILD_HIGHTECH", (3, 2), 7), ("BUILD_STARPORT", (3, 3), 8))
        for name, slab, count in records:
            frames = angle.frames_of(self.image(name), slab, count)
            for frame_index, frame in enumerate(frames):
                with self.subTest(record=name, frame=frame_index):
                    self.assertEqual(angle.edge_coverage(frame)["touch"], 1.0)

    def test_factory_pad_lights_stay_inside_the_pad(self):
        records = (
            ("BUILD_LIGHTFACTORY", (2, 2), 8, 128),
            ("BUILD_HEAVYFACTORY", (3, 2), 11, 236),
        )
        for name, slab, count, pad_x in records:
            frames = angle.frames_of(self.image(name), slab, count)
            baseline = np.asarray(frames[0])
            allowed = self.rect_mask(frames[0].size, [(pad_x, 0, frames[0].width, frames[0].height)])
            for frame_index in range(1, 7):
                current = np.asarray(frames[frame_index])
                changed = np.any(current != baseline, axis=2)
                with self.subTest(record=name, frame=frame_index):
                    self.assertFalse(np.any(changed & ~allowed), "pixels changed outside the pad")
                    self.assertTrue(np.any(changed & allowed), "pad lights did not change")
            for frame_index in range(7, count):
                with self.subTest(record=name, frame=frame_index):
                    self.assertTrue(np.array_equal(np.asarray(frames[frame_index]), baseline))

    def test_repair_gate_rises_inside_the_gate(self):
        frames = angle.frames_of(self.image("BUILD_REPAIR"), (3, 2), 8)
        baseline = np.asarray(frames[0])
        allowed = self.rect_mask(frames[0].size, [(201, 201, 361, 249)])
        for frame_index in range(1, 8):
            current = np.asarray(frames[frame_index])
            changed = np.any(current != baseline, axis=2)
            with self.subTest(record="BUILD_REPAIR", frame=frame_index):
                self.assertFalse(np.any(changed & ~allowed), "pixels changed outside the gate")
                if frame_index == 7:
                    self.assertGreaterEqual(int(changed.sum()), 5000)

    def test_refinery_lights_stay_in_the_slots(self):
        slots = (
            (247, 40, 333, 50),
            (228, 60, 263, 71),
            (317, 60, 352, 71),
            (267, 70, 314, 111),
            (228, 110, 263, 122),
            (317, 110, 352, 122),
            (247, 133, 333, 149),
        )
        building_frames = angle.frames_of(self.image("BUILD_REFINERY"), (3, 2), 8)
        building_baseline = np.asarray(building_frames[0])
        building_allowed = self.rect_mask(building_frames[0].size, slots, expansion=3)
        with self.subTest(record="BUILD_REFINERY"):
            for frame_index in range(1, 8):
                changed = np.any(np.asarray(building_frames[frame_index]) != building_baseline, axis=2)
                with self.subTest(frame=frame_index):
                    self.assertFalse(np.any(changed & ~building_allowed), "pixels changed outside the light slots")

        mask_frames = angle.frames_of(self.image("HM_BUILD_REFINERY"), (3, 2), 8)
        mask_allowed = self.rect_mask(mask_frames[0].size, slots, expansion=8)
        with self.subTest(record="HM_BUILD_REFINERY"):
            for frame_index, frame in enumerate(mask_frames):
                opaque = np.asarray(frame)[..., 3] > 0
                with self.subTest(frame=frame_index):
                    self.assertFalse(np.any(opaque & ~mask_allowed), "mask pixels extend outside the light slots")


if __name__ == "__main__":
    unittest.main()
