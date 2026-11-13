import contextlib
import copy
import io
import json
import tempfile
import unittest
from pathlib import Path

import numpy as np
from PIL import Image

from tools.hd_assets import PackEntry, encode_png, write_pack
from tools.units3d.redraw import main
from tools.units3d.redraw_common import ROOT


class DirectionalOffsetShiftTests(unittest.TestCase):
    def setUp(self):
        (ROOT / '.tmp').mkdir(exist_ok=True)
        temporary = tempfile.TemporaryDirectory(dir=ROOT / '.tmp')
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.pack = self.root / 'source.dat'
        self.attempt = self.root / 'attempt.png'
        self.recolour = self.root / 'recolour.png'

        body = np.zeros((128, 512, 4), np.uint8)
        house_mask = np.zeros_like(body)
        for row in range(2):
            for k in range(8):
                y = row * 64
                x = k * 64
                body[y + 20:y + 43, x + 20:x + 44] = (100, 110, 120, 255)
                house_mask[y + 20:y + 43, x + 20:x + 44] = (255, 255, 255, 255)
        write_pack(self.pack, [
            PackEntry(0, 'BODY', 'png', encode_png(Image.fromarray(body))),
            PackEntry(1, 'MASK', 'png', encode_png(Image.fromarray(house_mask))),
        ])

        attempt = np.full((1024, 1024, 3), (255, 0, 255), np.uint8)
        attempt[320:704, 320:704] = (100, 110, 120)
        Image.fromarray(attempt).save(self.attempt)
        recolour = attempt.copy()
        recolour[400:624, 400:624] = (0, 255, 0)
        Image.fromarray(recolour).save(self.recolour)

        self.data = {
            'atlases': {'body': 'BODY', 'house_mask': 'MASK', 'shadow': None},
            'frame': [64, 64],
            'rows': 2,
            'scale': 1,
            'share_corridor': [0, 1],
            'frames': [
                {
                    'row': row,
                    'k': k,
                    'attempts': {'chosen': str(self.attempt)},
                    'pick': 'chosen',
                    'recolour': str(self.recolour),
                    **({'offset_from': 0} if row == 1 else {}),
                }
                for row in range(2) for k in range(8)
            ],
        }
        self._write_unit(self.data)

    def _write_unit(self, data):
        (self.root / 'unit.json').write_text(json.dumps(data), encoding='utf-8')

    def _build(self, label, data=None):
        current = copy.deepcopy(self.data if data is None else data)
        self._write_unit(current)
        output = self.root / label
        stdout, stderr = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = main(['build', str(self.root), str(output), '--pack', str(self.pack)])
        return code, output, stdout.getvalue(), stderr.getvalue()

    @staticmethod
    def _atlas(output, name):
        return np.array(Image.open(output / f'{name}.png').convert('RGBA'))

    @staticmethod
    def _cell(atlas, row, k):
        y, x = row * 64, k * 64
        return atlas[y:y + 64, x:x + 64]

    def test_directional_shift_applies_to_one_direction_and_is_inherited(self):
        base_code, base_output, base_stdout, base_stderr = self._build('base')
        self.assertEqual(base_code, 0, base_stdout + base_stderr)
        base_params = json.loads((base_output / 'params.json').read_text(encoding='utf-8'))
        base_body = self._atlas(base_output, 'BODY')

        data = copy.deepcopy(self.data)
        data['offset_shift'] = [3, -4]
        data['offset_shift_by_direction'] = {'0': [0, -10]}
        code, output, stdout, stderr = self._build('directional', data)
        self.assertEqual(code, 0, stdout + stderr)
        params = json.loads((output / 'params.json').read_text(encoding='utf-8'))
        body = self._atlas(output, 'BODY')

        for row in range(2):
            for k in range(8):
                name = f'r{row}k{k}'
                base_x, base_y = base_params['frames'][name]['offset']
                dy = -14 if k == 0 else -4
                self.assertEqual(params['frames'][name]['offset'], [base_x + 3, base_y + dy])
                expected = np.roll(self._cell(base_body, row, k), (dy, 3), axis=(0, 1))
                self.assertTrue(np.array_equal(self._cell(body, row, k), expected), name)
            if row == 1:
                for k in range(8):
                    self.assertEqual(
                        params['frames'][f'r1k{k}']['offset'],
                        params['frames'][f'r0k{k}']['offset'],
                    )

    def test_invalid_direction_keys_and_values_are_input_errors(self):
        invalid = (
            None,
            [],
            {'8': [0, 0]},
            {'x': [0, 0]},
            {'0': [0]},
            {'0': [0, 1.5]},
            {'0': [True, 0]},
        )
        for index, value in enumerate(invalid):
            with self.subTest(value=value):
                data = copy.deepcopy(self.data)
                data['offset_shift_by_direction'] = value
                code, _, stdout, stderr = self._build(f'invalid-{index}', data)
                self.assertEqual(code, 2, stdout + stderr)
                self.assertTrue(stderr.startswith('offset_shift_by_direction:'), stderr)

    def test_fit_scale_rejects_directional_offset_shift(self):
        data = copy.deepcopy(self.data)
        data['scale'] = 'fit'
        data['offset_shift_by_direction'] = {'0': [0, -10]}
        code, _, stdout, stderr = self._build('fit-scale-offset', data)

        self.assertEqual(code, 2, stdout + stderr)
        self.assertTrue(stderr.startswith('offset_shift_by_direction:'), stderr)


if __name__ == '__main__':
    unittest.main()
