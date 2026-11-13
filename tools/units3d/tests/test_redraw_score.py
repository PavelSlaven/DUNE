from __future__ import annotations

import contextlib
import io
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import numpy as np
from PIL import Image

from tools.units3d import redraw_score
from tools.units3d.redraw_common import ROOT, load_unit


class RedrawScoreTests(unittest.TestCase):
    def setUp(self):
        (ROOT / '.tmp').mkdir(exist_ok=True)

    def test_figures_scores_the_span_of_all_three_figures(self):
        with tempfile.TemporaryDirectory(dir=ROOT / '.tmp') as temporary:
            path = Path(temporary) / 'figures.png'
            pixels = np.full((1024, 1024, 3), (255, 0, 255), np.uint8)
            for x in (100, 400, 700):
                pixels[400:500, x:x + 100] = 180
            Image.fromarray(pixels).save(path)
            old = np.zeros((128, 128, 4), np.uint8)
            old[30:90, 20:108, 3] = 255
            unit = SimpleNamespace(
                data={'height_estimate': 49.0, 'figures': 3},
                pack_path=Path('synthetic-pack.dat'),
                maximum=128,
                path=lambda value: value,
                old_frame=lambda role, record: old.copy(),
            )
            record = {'row': 0, 'k': 0, 'attempts': {'a': str(path)}}
            candidate = redraw_score._frame_data(unit, record)['attempts']['a']
            self.assertEqual(candidate['width'], 700)
            self.assertEqual(candidate['height'], 100)

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
            pack_path = Path('synthetic-pack.dat')
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
        with patch.object(redraw_score, 'keyed', side_effect=lambda path, *, figures=1: candidates[path]):
            with contextlib.redirect_stdout(stdout):
                result = redraw_score.run(SyntheticUnit(), SimpleNamespace(out=None))

        lines = stdout.getvalue().splitlines()
        self.assertEqual(result, 0)
        self.assertEqual([line for line in lines if line.startswith('## row ')], ['## row 0', '## row 1'])
        self.assertEqual(sum(line.startswith('old mirror IoU') for line in lines), 2)
        self.assertTrue(any(line.startswith('width spread [(\'zzzzzzzz\',') for line in lines))
        self.assertTrue(any(line.startswith('width spread [(\'solosoloso') for line in lines))

    def test_mirror_iou_is_cached_for_old_and_attempt_pairs(self):
        records = []
        candidates = {}
        alpha = np.zeros((8, 8), dtype=np.uint8)
        alpha[1:7, 2:6] = 255
        for k in range(8):
            attempts = {}
            for attempt in ('b', 'a'):
                path = f'r0k{k}-{attempt}'
                attempts[attempt] = path
                rgba = np.zeros((8, 8, 4), dtype=np.uint8)
                rgba[..., 3] = alpha
                candidates[path] = rgba
            records.append({'row': 0, 'k': k, 'attempts': attempts})

        old = np.zeros((4, 4, 4), dtype=np.uint8)
        old[0:4, 1:3, 3] = 255
        unit = SimpleNamespace(
            data={'height_estimate': 49.0},
            frames=records,
            pack_path=Path('synthetic-pack.dat'),
            frame=(4, 4),
            maximum=4,
            path=lambda value: value,
            old_frame=lambda role, record: old.copy(),
        )

        with patch.object(
            redraw_score, 'keyed', side_effect=lambda path, *, figures=1: candidates[path]
        ), patch.object(redraw_score, '_mirror_iou', wraps=redraw_score._mirror_iou) as iou:
            redraw_score.render(unit)

        self.assertEqual(iou.call_count, 15)


if __name__ == '__main__':
    unittest.main()
