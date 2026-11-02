from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np

from tools.hd_assets import PackEntry, write_pack
from tools.units3d.redraw_rotation import middle_measurement, size_measurements


ROOT = Path(__file__).resolve().parents[3]


def size_case(target_ratios):
    new_area = [1.0] * 8
    new_area[0] = 1.44
    references = [[1.0] * 8 for _ in range(3)]
    for index, ratio in enumerate(target_ratios):
        references[index][0] = new_area[0] / ratio**2
    return size_measurements(new_area, references)


def frame_mask(height, middle, width=8):
    mask = np.zeros((height, width), dtype=bool)
    top = int(middle) - 2
    mask[top:top + 4, 1:5] = True
    return mask


def classic_and_new(new_centres):
    classic = [frame_mask(32, 16) for _ in range(32)]
    new = [frame_mask(128, centre) for centre in new_centres]
    return new, classic


def ratios(result):
    return result['classic'], result['old'], result['block']


class RedrawRotationTests(unittest.TestCase):
    def test_three_supports_flag_size(self):
        results = size_case((1.20, 1.20, 1.20))
        for value in ratios(results[0]):
            self.assertAlmostEqual(value, 1.200, delta=0.001)
        self.assertAlmostEqual(results[0]['combined'], 1.200, delta=0.001)
        self.assertEqual(results[0]['agree'], 3)
        self.assertEqual(results[0]['flag'], 'size')
        for row in results[1:]:
            self.assertAlmostEqual(row['combined'], 1.0, delta=0.001)
            self.assertEqual(row['flag'], '-')

    def test_two_supports_flag_size(self):
        results = size_case((1.20, 1.20, 1.00))
        result = results[0]
        for actual, expected in zip(ratios(result), (1.20, 1.20, 1.00), strict=True):
            self.assertAlmostEqual(actual, expected, delta=0.001)
        self.assertAlmostEqual(result['combined'], 1.129, delta=0.001)
        self.assertEqual(result['agree'], 2)
        self.assertEqual(result['flag'], 'size')
        for row in results[1:]:
            self.assertAlmostEqual(row['combined'], 1.0, delta=0.001)
            self.assertEqual(row['flag'], '-')

    def test_one_support_does_not_flag_size(self):
        results = size_case((1.20, 1.00, 1.00))
        result = results[0]
        for actual, expected in zip(ratios(result), (1.20, 1.00, 1.00), strict=True):
            self.assertAlmostEqual(actual, expected, delta=0.001)
        self.assertAlmostEqual(result['combined'], 1.063, delta=0.001)
        self.assertEqual(result['agree'], 1)
        self.assertEqual(result['flag'], '-')
        for row in results[1:]:
            self.assertAlmostEqual(row['combined'], 1.0, delta=0.001)
            self.assertEqual(row['flag'], '-')

    def test_area_ratio_uses_square_root(self):
        result = size_case((1.20, 1.20, 1.20))[0]
        for value in ratios(result):
            self.assertAlmostEqual(value, 1.200, delta=0.001)
            self.assertNotAlmostEqual(value, 1.440, delta=0.001)

    def test_uniform_deviation_is_normalised(self):
        new_area = [1.0] * 8
        reference_areas = [[1 / 1.10**2] * 8 for _ in range(3)]
        results = size_measurements(new_area, reference_areas)
        self.assertEqual(len(results), 8)
        for result in results:
            for key in ('classic', 'old', 'block', 'combined'):
                self.assertAlmostEqual(result[key], 1.000, delta=0.001)
            self.assertEqual(result['agree'], 0)
            self.assertEqual(result['flag'], '-')

    def test_opposite_support_does_not_agree(self):
        results = size_case((1.40, 1.00, 0.94))
        self.assertEqual(len(results), 8)
        result = results[0]
        for key, expected in zip(('classic', 'old', 'block'), (1.40, 1.00, 0.94), strict=True):
            self.assertAlmostEqual(result[key], expected, delta=0.001)
        self.assertAlmostEqual(result['combined'], 1.096, delta=0.001)
        self.assertEqual(result['agree'], 1)
        self.assertEqual(result['flag'], '-')
        for row in results[1:]:
            self.assertAlmostEqual(row['combined'], 1.000, delta=0.001)
            self.assertEqual(row['flag'], '-')

    def test_middle_uses_median_of_32_bbox_centres(self):
        new, classic = classic_and_new([72] * 20 + [64] * 12)
        _, _, difference, flag = middle_measurement(new, classic)
        self.assertEqual(difference, 8.0)
        self.assertEqual(flag, 'middle')

    def test_middle_four_pixels_lower_is_flagged(self):
        new, classic = classic_and_new([68] * 32)
        _, _, difference, flag = middle_measurement(new, classic)
        self.assertEqual(difference, 4.0)
        self.assertEqual(flag, 'middle')

    def test_middle_eight_pixels_above_is_flagged(self):
        new, classic = classic_and_new([56] * 32)
        _, _, difference, flag = middle_measurement(new, classic)
        self.assertEqual(difference, -8.0)
        self.assertEqual(flag, 'middle')

    def test_middle_three_pixels_lower_is_not_flagged(self):
        new, classic = classic_and_new([67] * 32)
        _, _, difference, flag = middle_measurement(new, classic)
        self.assertEqual(difference, 3.0)
        self.assertEqual(flag, '-')

    def test_middle_uses_bbox_not_centroid(self):
        classic_mask = np.zeros((32, 8), dtype=bool)
        classic_mask[8:24, 2:6] = True
        classic = [classic_mask.copy() for _ in range(32)]

        new_mask = np.zeros((128, 8), dtype=bool)
        new_mask[40:64, 2:3] = True
        new_mask[64:88, 2:6] = True
        new = [new_mask.copy() for _ in range(32)]

        classic_y = np.nonzero(classic_mask)[0]
        classic_bbox_middle = (classic_y.min() + classic_y.max() + 1) / 2
        classic_centroid_middle = float(np.mean(classic_y + 0.5))
        self.assertEqual(classic_bbox_middle, classic_centroid_middle)

        new_y = np.nonzero(new_mask)[0]
        new_bbox_middle = (new_y.min() + new_y.max() + 1) / 2
        new_centroid_middle = float(np.mean(new_y + 0.5))
        self.assertGreaterEqual(new_centroid_middle - new_bbox_middle, 6.0)

        _, _, difference, flag = middle_measurement(new, classic)
        self.assertEqual(difference, 0.0)
        self.assertEqual(flag, '-')

    def test_missing_pack_returns_input_error_code(self):
        (ROOT / '.tmp').mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=ROOT / '.tmp') as temporary:
            missing = Path(temporary) / 'missing.dat'
            result = self.run_rotation(missing)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, '')
        self.assertIn(str(missing), result.stderr)

    def test_missing_entry_returns_input_error_code(self):
        (ROOT / '.tmp').mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=ROOT / '.tmp') as temporary:
            pack = Path(temporary) / 'missing-entry.dat'
            write_pack(pack, [PackEntry(0, 'UNRELATED', 'png', b'x')])
            result = self.run_rotation(pack)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, '')
        self.assertIn('missing entries', result.stderr)

    @staticmethod
    def run_rotation(pack):
        return subprocess.run(
            [sys.executable, 'tools/units3d/redraw.py', 'rotation', str(pack)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding='utf-8',
            check=False,
            timeout=30,
        )


if __name__ == '__main__':
    unittest.main()
