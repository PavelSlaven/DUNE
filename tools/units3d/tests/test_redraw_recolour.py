from __future__ import annotations

import tempfile
import unittest
import contextlib
import io
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import numpy as np
from PIL import Image

from tools.units3d.redraw import main
from tools.units3d.redraw_common import ROOT
from tools.units3d.redraw_recolour import run


class UnitFixture:
    def __init__(self, records, sources, bodies, masks):
        self._frames = records
        self.data = {}
        self.sources = sources
        self.bodies = bodies
        self.masks = masks
        self.frame = (4, 2)
        self.maximum = max(self.frame)
        self.atlases = {'body': 'body', 'house_mask': 'mask'}
        self.pack_path = Path('fixture-pack.dat')

    @property
    def frames(self):
        return sorted(self._frames, key=lambda record: (record['row'], record['k']))

    def path(self, value):
        return Path(value)

    def old_frame(self, role, record):
        frames = self.bodies if role == 'body' else self.masks
        return frames[(record['row'], record['k'])].copy()


class RedrawRecolourTests(unittest.TestCase):
    def setUp(self):
        self.temp_root = ROOT / '.tmp'
        self.temp_root.mkdir(exist_ok=True)
        temporary = tempfile.TemporaryDirectory(dir=self.temp_root)
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)

    def test_figures_preserves_three_separate_recolour_inputs(self):
        source = self.root / 'three-figures.png'
        pixels = np.full((1024, 1024, 3), (255, 0, 255), np.uint8)
        for x in (100, 400, 700):
            pixels[400:500, x:x + 100] = 180
        Image.fromarray(pixels).save(source)
        blank = np.zeros((2, 4, 4), np.uint8)
        record = {'row': 0, 'k': 0, 'attempts': {'a': str(source)}, 'pick': 'a'}
        unit = UnitFixture([record], {}, {(0, 0): blank}, {(0, 0): blank})
        unit.data['figures'] = 3
        output = self.root / 'three-out'
        with redirect_stdout(StringIO()):
            run(unit, SimpleNamespace(output=output))
        with Image.open(output / 'pick_r0k0.png') as image:
            for x in (150, 450, 750):
                self.assertEqual(image.getpixel((x, 450)), (180, 180, 180))

    def test_alpha_candidate_is_resized_without_composition_before_keying(self):
        source = self.root / 'source.png'
        pixels = np.zeros((512, 512, 4), dtype=np.uint8)
        pixels[..., :3] = (0, 0, 0)
        pixels[100:412, 100:412] = (240, 10, 20, 128)
        Image.fromarray(pixels).save(source)

        output = self.root / 'out'
        blank = np.zeros((2, 4, 4), dtype=np.uint8)
        unit = UnitFixture(
            [{'row': 0, 'k': 0, 'attempts': {'chosen': str(source)}, 'pick': 'chosen'}],
            {}, {(0, 0): blank}, {(0, 0): blank},
        )
        transcript = StringIO()
        with redirect_stdout(transcript):
            run(unit, SimpleNamespace(output=output))
        with Image.open(output / 'pick_r0k0.png') as image:
            actual = np.asarray(image.convert('RGB'))
        self.assertTrue(np.allclose(actual[512, 512], (240, 10, 20), atol=2))
        self.assertEqual(tuple(actual[100, 100]), (255, 0, 255))
        self.assertEqual(transcript.getvalue().strip(), f'2 recolour inputs: {output}')

    def test_uses_maximum_frame_dimension_across_multiple_rows_and_keeps_old_alpha(self):
        sources = {}
        records = []
        bodies = {}
        masks = {}
        for row, k, color in ((0, 5, (230, 30, 40)), (1, 2, (40, 210, 70))):
            source = self.root / f'source_{row}_{k}.png'
            Image.new('RGB', (12, 12), color).save(source)
            sources[(row, k)] = source
            records.append({
                'row': row,
                'k': k,
                'attempts': {'selected': str(source)},
                'pick': 'selected',
            })

            body = np.zeros((2, 4, 4), dtype=np.uint8)
            body[..., :3] = (20, 30, 40)
            body[..., 3] = 64
            body[1, 3, 3] = 0
            mask = np.zeros_like(body)
            mask[0, 1, 3] = 255
            mask[1, 3, 3] = 255
            bodies[(row, k)] = body
            masks[(row, k)] = mask

        unit = UnitFixture(records[::-1], sources, bodies, masks)
        output = self.root / 'out'
        transcript = StringIO()
        with redirect_stdout(transcript):
            result = run(unit, SimpleNamespace(output=output))

        self.assertEqual(result, 0)
        self.assertEqual(transcript.getvalue().strip(), f'4 recolour inputs: {output}')
        self.assertEqual(sorted(path.name for path in output.iterdir()), [
            'oldmask_r0k5.png', 'oldmask_r1k2.png', 'pick_r0k5.png', 'pick_r1k2.png',
        ])
        with Image.open(output / 'oldmask_r1k2.png') as image:
            oldmask = np.asarray(image.convert('RGB'))
        self.assertEqual(oldmask.shape, (1024, 1024, 3))
        self.assertEqual(tuple(oldmask[100, 384]), (255, 0, 255))
        self.assertTrue(np.allclose(oldmask[384, 384], (191, 64, 191), atol=2))
        self.assertEqual(tuple(oldmask[640, 896]), (255, 0, 255))

        for row, k, color in ((0, 5, (230, 30, 40)), (1, 2, (40, 210, 70))):
            with Image.open(output / f'pick_r{row}k{k}.png') as image:
                self.assertEqual(image.size, (1024, 1024))
                self.assertEqual(image.getpixel((512, 512)), color)

    def test_r6_blank_selected_attempt_reports_frame_and_path_as_input_error(self):
        source = self.root / 'blank.png'
        Image.new('RGB', (1024, 1024), (255, 0, 255)).save(source)
        record = {'row': 1, 'k': 6, 'attempts': {'chosen': str(source)}, 'pick': 'chosen'}
        blank = np.zeros((2, 4, 4), dtype=np.uint8)
        unit = UnitFixture([record], {}, {(1, 6): blank}, {(1, 6): blank})
        output = self.root / 'out'
        stderr = io.StringIO()
        with patch('tools.units3d.redraw.load_unit', return_value=unit), contextlib.redirect_stderr(stderr):
            code = main(['recolour-inputs', str(self.root / 'unit'), str(output)])

        self.assertEqual(code, 2)
        self.assertIn('r1k6', stderr.getvalue())
        self.assertIn(str(source), stderr.getvalue())


if __name__ == '__main__':
    unittest.main()
