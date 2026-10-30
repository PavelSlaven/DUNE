from __future__ import annotations

import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

import numpy as np

from tools.units3d.redraw_common import ROOT
from tools.units3d.redraw_shadow import run


class UnitFixture:
    def __init__(self, body, shadow, frame, rows):
        self._images = {'body': body, 'shadow': shadow}
        self.atlases = {'body': 'body', 'house_mask': None, 'shadow': 'shadow'}
        self.frame = frame
        self.rows = rows
        self.frames = [
            {'row': row, 'k': k}
            for row in range(rows)
            for k in range(8)
        ]

    def image(self, name):
        return self._images[name]

    def old_frame(self, role, record):
        fw, fh = self.frame
        x, y = record['k'] * fw, record['row'] * fh
        return self.image(self.atlases[role])[y:y + fh, x:x + fw].copy()


class RedrawShadowTests(unittest.TestCase):
    def setUp(self):
        temporary_root = ROOT / '.tmp'
        temporary_root.mkdir(exist_ok=True)
        temporary = tempfile.TemporaryDirectory(dir=temporary_root)
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)

    def evaluate(self, unit):
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            status = run(unit, SimpleNamespace())
        lines = stdout.getvalue().splitlines()
        rule = json.loads(lines[0]) if lines else None
        return status, lines, rule, stderr.getvalue()

    def test_unshifted_soft_alpha_uses_median_scale_and_shadow_rgb(self):
        fw, fh = 6, 5
        body = np.zeros((fh, fw * 8, 4), dtype=np.uint8)
        shadow = np.zeros_like(body)
        locations = ((0, 0, 64, 16), (0, 3, 128, 32), (2, 1, 192, 48), (4, 5, 255, 64))
        for y, x, body_alpha, shadow_alpha in locations:
            body[y, 3 * fw + x, 3] = body_alpha
            shadow[y, 3 * fw + x, :3] = (5, 4, 3)
            shadow[y, 3 * fw + x, 3] = shadow_alpha

        status, lines, rule, stderr = self.evaluate(UnitFixture(body, shadow, (fw, fh), 1))

        self.assertEqual(status, 0, stderr)
        self.assertEqual(len(lines), 1)
        self.assertEqual(rule['shift'], 0)
        self.assertEqual(rule['alpha'], 64)
        self.assertEqual(rule['rgb'], [5, 4, 3])
        self.assertEqual(rule['corr'], 1.0)

    def test_shift_stays_within_each_cell_and_correlates_the_whole_padded_atlas(self):
        fw, fh, rows = 6, 5, 2
        body = np.zeros((rows * fh + 4, fw * 8 + 4, 4), dtype=np.uint8)
        shadow = np.zeros_like(body)
        pattern = ((0, 0, 51), (0, 3, 102), (2, 1, 153), (3, 4, 204), (4, 5, 240))
        for row in range(rows):
            for k in range(8):
                x0, y0 = k * fw, row * fh
                for y, x, alpha in pattern:
                    body[y0 + y, x0 + x, 3] = alpha
                for y, x, alpha in pattern[:3]:
                    shadow[y0 + y + 2, x0 + x + 2, 3] = round(alpha * 75 / 255)
                    shadow[y0 + y + 2, x0 + x + 2, :3] = (5, 60, 70)

        border = shadow[:, fw * 8:, :]
        border_coords = np.argwhere(np.ones(border.shape[:2], dtype=bool))[:49]
        for y, x in border_coords:
            shadow[y, fw * 8 + x] = (200, 10, 20, 200)

        status, lines, rule, stderr = self.evaluate(UnitFixture(body, shadow, (fw, fh), rows))

        self.assertEqual(len(lines), 1)
        self.assertEqual(rule['shift'], 2)
        self.assertEqual(rule['alpha'], 75)
        self.assertEqual(rule['rgb'], [200, 10, 20])
        self.assertGreater(rule['corr'], 0.05)
        self.assertLess(rule['corr'], 0.95)
        self.assertEqual(status, 1, stderr)

    def test_no_finite_rule_does_not_emit_nan_json(self):
        body = np.zeros((5, 48, 4), dtype=np.uint8)
        shadow = np.zeros_like(body)
        shadow[..., 3] = 255
        status, lines, rule, stderr = self.evaluate(UnitFixture(body, shadow, (6, 5), 1))

        self.assertEqual(status, 1)
        self.assertEqual(lines, [])
        self.assertIsNone(rule)
        self.assertIn('no shift has an overlap', stderr)


if __name__ == '__main__':
    unittest.main()
