from __future__ import annotations

import contextlib
import io
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import numpy as np

from tools.units3d import redraw_score
from tools.units3d.redraw_common import ROOT, load_unit


class RedrawScoreTests(unittest.TestCase):
    def setUp(self):
        (ROOT / '.tmp').mkdir(exist_ok=True)

    def test_devastator_output_matches_g3_reference_and_out(self):
        unit_dir = ROOT / 'tools/units3d/units/UNIT_DEVASTATOR'
        unit = load_unit(unit_dir, 'score')
        with tempfile.TemporaryDirectory(dir=ROOT / '.tmp') as temporary:
            output_path = Path(temporary) / 'score.txt'
            stdout = io.StringIO()
            with contextlib.redirect_stdout(stdout):
                result = redraw_score.run(unit, SimpleNamespace(out=output_path))

            reference = (ROOT / 'codex-direct/G3/choice.txt').read_text(
                encoding='utf-8'
            ).splitlines()
            ratio_start = next(
                index for index, line in enumerate(reference)
                if line.startswith('k\told w×h\t')
            )
            ratio_lines = [reference[ratio_start], *reference[ratio_start + 1:ratio_start + 17]]
            mirror_start = next(
                index for index, line in enumerate(reference)
                if line.startswith('old mirror IoU')
            )
            angle_end = next(
                index for index, line in enumerate(reference[mirror_start:], mirror_start)
                if line.startswith('angle error [')
            )
            choice_lines = reference[mirror_start:angle_end + 1]
            choice_lines = [
                line.replace("'aa': 0.902", "'aa': 0.903", 1)
                if line.startswith('5-7 ')
                else line
                for line in choice_lines
            ]
            expected = '\n'.join(['## row 0', *ratio_lines, *choice_lines]) + '\n'

            self.assertEqual(result, 0)
            self.assertEqual(stdout.getvalue(), expected)
            self.assertEqual(output_path.read_text(encoding='utf-8'), expected)

    def test_multiple_rows_accept_ordered_arbitrary_attempt_keys_without_house_mask(self):
        records = []
        candidate_alpha = np.zeros((8, 8), dtype=np.uint8)
        candidate_alpha[1:7, 2:6] = 255
        candidates = {}
        for row in range(2):
            for k in range(8):
                attempts = {}
                keys = ('z', 'x', 'y') if row == 0 else ('solo',)
                for key in keys:
                    name = f'r{row}k{k}-{key}'
                    attempts[key] = name
                    rgba = np.zeros((8, 8, 4), dtype=np.uint8)
                    rgba[..., 3] = candidate_alpha
                    candidates[name] = rgba
                records.append({'row': row, 'k': k, 'attempts': attempts})

        old = np.zeros((4, 4, 4), dtype=np.uint8)
        old[0:4, 1:3, 3] = 255

        class SyntheticUnit:
            data = {
                'height_estimate': 49.0,
                'atlases': {'house_mask': None},
            }
            frame = (4, 4)
            maximum = 4
            rows = 2
            frames = records

            def path(self, value):
                return value

            def old_frame(self, role, record):
                self_outer.assertEqual(role, 'body')
                return old.copy()

        self_outer = self
        stdout = io.StringIO()
        with patch.object(redraw_score, 'keyed', side_effect=lambda path: candidates[path]):
            with contextlib.redirect_stdout(stdout):
                result = redraw_score.run(SyntheticUnit(), SimpleNamespace(out=None))

        lines = stdout.getvalue().splitlines()
        self.assertEqual(result, 0)
        self.assertEqual([line for line in lines if line.startswith('## row ')], ['## row 0', '## row 1'])
        self.assertEqual(sum(line.startswith('old mirror IoU') for line in lines), 2)
        self.assertTrue(any(line.startswith('width spread [(\'zzzzzzzz\',') for line in lines))
        self.assertTrue(any(line.startswith('width spread [(\'solosoloso') for line in lines))


if __name__ == '__main__':
    unittest.main()
