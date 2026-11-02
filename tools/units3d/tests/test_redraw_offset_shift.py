import contextlib
import copy
import io
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

import numpy as np
from PIL import Image

from tools.hd_assets import PackEntry, encode_png, write_pack
from tools.units3d.redraw import main
from tools.units3d.redraw_common import ROOT, bbox, keyed, load_unit, place


class OffsetShiftTests(unittest.TestCase):
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
        disk = subprocess.run(['df', '-BG', '/'], check=True, capture_output=True, text=True)
        available = int(disk.stdout.splitlines()[-1].split()[3].removesuffix('G'))
        if available < 5:
            raise RuntimeError(f'df -BG / reports only {available}G available')
        output = self.root / label
        stdout, stderr = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = main(['build', str(self.root), str(output), '--pack', str(self.pack)])
        log_path = ROOT / '.tmp' / f'u12-offset-{self.root.name}-{label}.log'
        log_path.write_text(
            f'{disk.stdout}exit={code}\nstdout:\n{stdout.getvalue()}stderr:\n{stderr.getvalue()}',
            encoding='utf-8',
        )
        return code, output, stdout.getvalue(), stderr.getvalue()

    @staticmethod
    def _files(directory):
        return {path.relative_to(directory): path.read_bytes()
                for path in directory.rglob('*') if path.is_file()}

    @staticmethod
    def _atlas(output, name):
        return np.array(Image.open(output / f'{name}.png').convert('RGBA'))

    @staticmethod
    def _cell(atlas, row, k):
        y, x = row * 64, k * 64
        return atlas[y:y + 64, x:x + 64]

    def _assert_baseline_fixture(self, output):
        params = json.loads((output / 'params.json').read_text(encoding='utf-8'))
        body = self._atlas(output, 'BODY')
        house_mask = self._atlas(output, 'MASK')
        for row in range(2):
            for k in range(8):
                name = f'r{row}k{k}'
                self.assertEqual(params['frames'][name]['moved'], [0, 0])
                for atlas in (body, house_mask):
                    cell = self._cell(atlas, row, k)
                    ys, xs = np.nonzero(cell[..., 3])
                    self.assertGreater(len(xs), 0)
                    self.assertGreaterEqual(int(ys.min()), 12)
                    self.assertGreaterEqual(63 - int(ys.max()), 12)
                    self.assertGreaterEqual(int(xs.min()), 12)
                    self.assertGreaterEqual(63 - int(xs.max()), 12)

    def _assert_half_rounding_case(self):
        unit = load_unit(self.root, 'build', self.pack)
        attempt = keyed(self.attempt)
        size = round(unit.maximum * self.data['scale'])
        small = np.array(Image.fromarray(attempt).convert('RGBa').resize(
            (size, size), Image.Resampling.LANCZOS,
        ))
        source_box = bbox(small[..., 3])
        found = False
        for record in unit.frames:
            old_box = unit.output_box(bbox(unit.old_frame('body', record)[..., 3]))
            numerator = old_box[1] + old_box[3] - source_box[1] - source_box[3]
            if numerator % 2:
                _, _, offset, _ = place(
                    attempt, unit.frame, self.data['scale'], old_box,
                    source_maximum=unit.maximum,
                )
                self.assertEqual(offset[1], round(numerator / 2))
                found = True
                break
        self.assertTrue(found, 'fixture must contain an odd vertical centering numerator')

    def test_unset_and_zero_shift_outputs_match_byte_for_byte(self):
        base_code, base_output, base_stdout, base_stderr = self._build('no-shift')
        zero_data = copy.deepcopy(self.data)
        zero_data['offset_shift'] = [0, 0]
        zero_code, zero_output, zero_stdout, zero_stderr = self._build('zero-shift', zero_data)

        self.assertEqual(base_code, 0, base_stdout + base_stderr)
        self.assertEqual(zero_code, 0, zero_stdout + zero_stderr)
        self._assert_baseline_fixture(base_output)
        self.assertEqual(self._files(base_output), self._files(zero_output))

    def test_body_cells_equal_roll(self):
        base_code, base_output, base_stdout, base_stderr = self._build('body-roll-base')
        self.assertEqual(base_code, 0, base_stdout + base_stderr)
        self._assert_baseline_fixture(base_output)
        self._assert_half_rounding_case()
        base = self._atlas(base_output, 'BODY')

        for index, (dx, dy) in enumerate(((0, -10), (0, 7), (5, 0))):
            data = copy.deepcopy(self.data)
            data['offset_shift'] = [dx, dy]
            code, output, stdout, stderr = self._build(f'body-roll-{index}', data)
            self.assertEqual(code, 0, stdout + stderr)
            shifted = self._atlas(output, 'BODY')
            params = json.loads((output / 'params.json').read_text(encoding='utf-8'))
            base_params = json.loads((base_output / 'params.json').read_text(encoding='utf-8'))
            for row in range(2):
                for k in range(8):
                    name = f'r{row}k{k}'
                    expected = np.roll(self._cell(base, row, k), (dy, dx), axis=(0, 1))
                    self.assertTrue(np.array_equal(self._cell(shifted, row, k), expected), name)
                    old_offset = base_params['frames'][name]['offset']
                    self.assertEqual(params['frames'][name]['offset'], [old_offset[0] + dx, old_offset[1] + dy])
                    if row == 1:
                        source = params['frames'][f'r0k{k}']
                        self.assertEqual(params['frames'][name]['offset'], source['offset'])
                        self.assertTrue(np.array_equal(
                            self._cell(shifted, row, k), self._cell(shifted, 0, k),
                        ))

    def test_house_mask_cells_equal_roll(self):
        base_code, base_output, base_stdout, base_stderr = self._build('mask-roll-base')
        self.assertEqual(base_code, 0, base_stdout + base_stderr)
        self._assert_baseline_fixture(base_output)
        base = self._atlas(base_output, 'MASK')

        for index, (dx, dy) in enumerate(((0, -10), (0, 7), (5, 0))):
            data = copy.deepcopy(self.data)
            data['offset_shift'] = [dx, dy]
            code, output, stdout, stderr = self._build(f'mask-roll-{index}', data)
            self.assertEqual(code, 0, stdout + stderr)
            shifted = self._atlas(output, 'MASK')
            params = json.loads((output / 'params.json').read_text(encoding='utf-8'))
            for row in range(2):
                for k in range(8):
                    expected = np.roll(self._cell(base, row, k), (dy, dx), axis=(0, 1))
                    self.assertTrue(np.array_equal(self._cell(shifted, row, k), expected), f'r{row}k{k}')
                    self.assertGreater(int(self._cell(shifted, row, k)[..., 3].sum()), 0)
            self.assertEqual(
                params['frames']['r1k0']['offset'], params['frames']['r0k0']['offset'],
            )

    def test_shifted_offset_is_reported_and_clipping_is_checked_after_shift(self):
        base_code, base_output, base_stdout, base_stderr = self._build('clipping-base')
        self.assertEqual(base_code, 0, base_stdout + base_stderr)
        base_params = json.loads((base_output / 'params.json').read_text(encoding='utf-8'))
        data = copy.deepcopy(self.data)
        data['offset_shift'] = [0, 100]
        code, output, stdout, stderr = self._build('clipping-shift', data)

        self.assertEqual(code, 1, stdout + stderr)
        self.assertIn('clipped', stderr)
        params = json.loads((output / 'params.json').read_text(encoding='utf-8'))
        for row in range(2):
            for k in range(8):
                name = f'r{row}k{k}'
                base = base_params['frames'][name]['offset']
                self.assertEqual(params['frames'][name]['offset'], [base[0], base[1] + 100])

    def test_invalid_offset_shift_values_are_input_errors(self):
        invalid = (
            None, False, [], [0], [0, 1.5], [0, 1.0], [True, 0], [0, True],
            '0,1', [0, 0, 0],
        )
        for index, value in enumerate(invalid):
            with self.subTest(value=value):
                data = copy.deepcopy(self.data)
                data['offset_shift'] = value
                code, _, stdout, stderr = self._build(f'invalid-{index}', data)
                self.assertEqual(code, 2, stdout + stderr)
                self.assertTrue(stderr.startswith('offset_shift:'), stderr)


if __name__ == '__main__':
    unittest.main()
