import contextlib
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


class RedrawFrameScaleTests(unittest.TestCase):
    def setUp(self):
        (ROOT / '.tmp').mkdir(exist_ok=True)
        temporary = tempfile.TemporaryDirectory(dir=ROOT / '.tmp')
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.body = np.zeros((64, 512, 4), np.uint8)
        for k in range(8):
            self.body[20:44, k * 64 + 12:k * 64 + 52] = (100, 110, 120, 255)
        self.pack = self.root / 'source.dat'
        self.attempt = self._image('attempt.png', (255, 0, 255), (312, 392, 712, 632), (100, 110, 120))
        self.recolour = self._recolour('recolour.png', (312, 392, 712, 632), (432, 472, 592, 552))
        self.data = {
            'atlases': {'body': 'BODY', 'house_mask': None, 'shadow': 'SHADOW'},
            'frame': [64, 64],
            'rows': 1,
            'shadow_rule': {'shift': 0, 'alpha': 64, 'rgb': [5, 4, 3]},
            'frames': [
                {
                    'row': 0,
                    'k': k,
                    'attempts': {'chosen': str(self.attempt)},
                    'pick': 'chosen',
                }
                for k in range(8)
            ],
        }
        self._write_pack()

    def _image(self, name, background, box, color):
        pixels = np.full((1024, 1024, 3), background, np.uint8)
        x0, y0, x1, y1 = box
        pixels[y0:y1, x0:x1] = color
        path = self.root / name
        Image.fromarray(pixels).save(path)
        return path

    def _recolour(self, name, body_box, green_box):
        pixels = np.full((1024, 1024, 3), (255, 0, 255), np.uint8)
        x0, y0, x1, y1 = body_box
        pixels[y0:y1, x0:x1] = (100, 110, 120)
        gx0, gy0, gx1, gy1 = green_box
        pixels[gy0:gy1, gx0:gx1] = (0, 255, 0)
        path = self.root / name
        Image.fromarray(pixels).save(path)
        return path

    def _write_pack(self, data=None):
        entries = [
            PackEntry(0, 'BODY', 'png', encode_png(Image.fromarray(self.body))),
            PackEntry(1, 'SHADOW', 'png', encode_png(Image.fromarray(np.zeros_like(self.body)))),
        ]
        if (data or self.data)['atlases']['house_mask'] is not None:
            entries.append(PackEntry(2, 'MASK', 'png', encode_png(Image.fromarray(self.body))))
        write_pack(self.pack, entries)

    def _write_unit(self, data):
        (self.root / 'unit.json').write_text(json.dumps(data), encoding='utf-8')

    def _build(self, data, label):
        self._write_unit(data)
        self._write_pack(data)
        output = self.root / label
        stdout, stderr = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = main(['build', str(self.root), str(output), '--pack', str(self.pack)])
        return code, output, stdout.getvalue(), stderr.getvalue()

    def _with_house_mask(self):
        data = json.loads(json.dumps(self.data))
        data['atlases']['house_mask'] = 'MASK'
        data['share_corridor'] = [0, 1]
        for record in data['frames']:
            record['recolour'] = str(self.recolour)
        return data

    @staticmethod
    def _cell(atlas, k, frame=(64, 64)):
        fw, fh = frame
        return atlas[:fh, k * fw:(k + 1) * fw]

    @staticmethod
    def _bbox_size(image):
        ys, xs = np.nonzero(image[..., 3] > 127)
        return int(xs.max() - xs.min() + 1), int(ys.max() - ys.min() + 1)

    @staticmethod
    def _atlas(path, name):
        return np.array(Image.open(path / f'{name}.png').convert('RGBA'))

    def test_factor_one_matches_default_outputs(self):
        baseline_data = self._with_house_mask()
        factor_one_data = self._with_house_mask()
        factor_one_data['frames'][0]['scale_factor'] = 1

        base_code, base_output, base_stdout, base_stderr = self._build(baseline_data, 'default')
        factor_code, factor_output, factor_stdout, factor_stderr = self._build(factor_one_data, 'factor-one')

        self.assertEqual(base_code, 0, base_stdout + base_stderr)
        self.assertEqual(factor_code, 0, factor_stdout + factor_stderr)
        base_files = {path.relative_to(base_output): path.read_bytes() for path in base_output.rglob('*') if path.is_file()}
        factor_files = {path.relative_to(factor_output): path.read_bytes() for path in factor_output.rglob('*') if path.is_file()}
        self.assertEqual(base_files, factor_files)

    def test_factor_scales_selected_body(self):
        baseline_data = json.loads(json.dumps(self.data))
        factor_data = json.loads(json.dumps(self.data))
        factor_data['frames'][0]['scale_factor'] = 0.8

        base_code, base_output, base_stdout, base_stderr = self._build(baseline_data, 'body-default')
        factor_code, factor_output, factor_stdout, factor_stderr = self._build(factor_data, 'body-scaled')

        self.assertEqual(base_code, 0, base_stdout + base_stderr)
        self.assertEqual(factor_code, 0, factor_stdout + factor_stderr)
        base_atlas = self._atlas(base_output, 'BODY')
        factor_atlas = self._atlas(factor_output, 'BODY')
        base_size = self._bbox_size(self._cell(base_atlas, 0))
        factor_size = self._bbox_size(self._cell(factor_atlas, 0))
        for actual, original in zip(factor_size, base_size, strict=True):
            self.assertLessEqual(abs(actual - round(0.8 * original)), 1)
        base_params = json.loads((base_output / 'params.json').read_text())
        factor_params = json.loads((factor_output / 'params.json').read_text())
        self.assertEqual(factor_params['scale'], base_params['scale'])
        self.assertEqual(factor_params['scale_median'], base_params['scale_median'])

    def test_factor_scales_selected_house_mask(self):
        baseline_data = self._with_house_mask()
        factor_data = self._with_house_mask()
        factor_data['frames'][0]['scale_factor'] = 0.8

        base_code, base_output, base_stdout, base_stderr = self._build(baseline_data, 'mask-default')
        factor_code, factor_output, factor_stdout, factor_stderr = self._build(factor_data, 'mask-scaled')

        self.assertEqual(base_code, 0, base_stdout + base_stderr)
        self.assertEqual(factor_code, 0, factor_stdout + factor_stderr)
        body = self._cell(self._atlas(factor_output, 'BODY'), 0)
        base_mask = self._cell(self._atlas(base_output, 'MASK'), 0)
        factor_mask = self._cell(self._atlas(factor_output, 'MASK'), 0)
        base_size = self._bbox_size(base_mask)
        factor_size = self._bbox_size(factor_mask)
        body_size = self._bbox_size(body)
        self.assertLess(base_size[0] * 2, self._bbox_size(self._cell(self._atlas(base_output, 'BODY'), 0))[0])
        for actual, original in zip(factor_size, base_size, strict=True):
            self.assertLessEqual(abs(actual - round(0.8 * original)), 1)
        self.assertLess(factor_size[0], body_size[0])

    def test_factor_preserves_other_frames(self):
        baseline_data = self._with_house_mask()
        factor_data = self._with_house_mask()
        factor_data['frames'][0]['scale_factor'] = 0.8

        base_code, base_output, base_stdout, base_stderr = self._build(baseline_data, 'cells-default')
        factor_code, factor_output, factor_stdout, factor_stderr = self._build(factor_data, 'cells-scaled')

        self.assertEqual(base_code, 0, base_stdout + base_stderr)
        self.assertEqual(factor_code, 0, factor_stdout + factor_stderr)
        for name in ('BODY', 'MASK'):
            with self.subTest(atlas=name):
                base_atlas = self._atlas(base_output, name)
                factor_atlas = self._atlas(factor_output, name)
                for k in range(1, 8):
                    self.assertTrue(np.array_equal(self._cell(base_atlas, k), self._cell(factor_atlas, k)))
                self.assertFalse(np.array_equal(self._cell(base_atlas, 0), self._cell(factor_atlas, 0)))

    def test_invalid_scale_factor_cli(self):
        for label, value in (
            ('zero', 0),
            ('negative', -1),
            ('string', '0.8'),
            ('boolean', True),
            ('infinity', float('inf')),
        ):
            with self.subTest(value=label):
                data = json.loads(json.dumps(self.data))
                data['frames'][0]['scale_factor'] = value
                code, _, stdout, stderr = self._build(data, f'invalid-{label}')
                self.assertEqual(code, 2, stdout + stderr)
                self.assertTrue(stderr.startswith('scale_factor:'), stderr)

    def test_scale_factor_composes_with_explicit_unit_scale(self):
        factor_data = json.loads(json.dumps(self.data))
        factor_data['scale'] = 1.25
        factor_data['frames'][0]['scale_factor'] = 0.8
        equivalent_data = json.loads(json.dumps(self.data))
        equivalent_data['scale'] = 1.0

        equivalent_code, equivalent_output, equivalent_stdout, equivalent_stderr = self._build(
            equivalent_data, 'explicit-one'
        )
        factor_code, factor_output, factor_stdout, factor_stderr = self._build(
            factor_data, 'explicit-composed'
        )

        self.assertEqual(equivalent_code, 0, equivalent_stdout + equivalent_stderr)
        self.assertEqual(factor_code, 0, factor_stdout + factor_stderr)
        self.assertEqual(
            (factor_output / 'frames' / 'r0k0.png').read_bytes(),
            (equivalent_output / 'frames' / 'r0k0.png').read_bytes(),
        )
        for atlas_name in ('BODY', 'SHADOW'):
            self.assertTrue(np.array_equal(
                self._cell(self._atlas(factor_output, atlas_name), 0),
                self._cell(self._atlas(equivalent_output, atlas_name), 0),
            ))
        params = json.loads((factor_output / 'params.json').read_text())
        self.assertEqual(params['scale'], 1.25)

    def test_scale_factor_is_used_for_fit_and_clipping(self):
        data = self._with_house_mask()
        oversized = self._image('oversized.png', (255, 0, 255), (187, 392, 837, 632), (100, 110, 120))
        oversized_recolour = self._recolour(
            'oversized-recolour.png', (187, 392, 837, 632), (187, 392, 837, 632)
        )
        data['frames'][0]['attempts']['chosen'] = str(oversized)
        data['frames'][0]['recolour'] = str(oversized_recolour)
        data['frames'][0]['scale_factor'] = 0.8
        data['scale'] = 1.6

        explicit_code, explicit_output, explicit_stdout, explicit_stderr = self._build(data, 'explicit-fit-check')
        self.assertEqual(explicit_code, 0, explicit_stdout + explicit_stderr)
        self.assertIn('all frames pass', (explicit_output / 'metrics.txt').read_text())

        unscaled_data = json.loads(json.dumps(data))
        unscaled_data['frames'][0].pop('scale_factor')
        clipped_code, _, clipped_stdout, clipped_stderr = self._build(unscaled_data, 'explicit-clipped')
        self.assertEqual(clipped_code, 1, clipped_stdout + clipped_stderr)
        self.assertIn('r0k0: clipped', clipped_stderr)

        data['scale'] = 'fit'
        fit_code, fit_output, fit_stdout, fit_stderr = self._build(data, 'factor-fit')
        self.assertEqual(fit_code, 0, fit_stdout + fit_stderr)
        fit_params = json.loads((fit_output / 'params.json').read_text())
        self.assertEqual(fit_params['scale'], fit_params['scale_median'])

        unscaled_data['scale'] = 'fit'
        unscaled_fit_code, unscaled_fit_output, unscaled_fit_stdout, unscaled_fit_stderr = self._build(
            unscaled_data, 'unscaled-fit'
        )
        self.assertEqual(unscaled_fit_code, 0, unscaled_fit_stdout + unscaled_fit_stderr)
        unscaled_fit_params = json.loads((unscaled_fit_output / 'params.json').read_text())
        self.assertLess(unscaled_fit_params['scale'], unscaled_fit_params['scale_median'])

    def test_missing_reference_frame_keeps_cells_error_prefix(self):
        data = json.loads(json.dumps(self.data))
        data['frame'] = [65, 64]
        code, _, stdout, stderr = self._build(data, 'bad-atlas-grid')
        self.assertEqual(code, 2, stdout + stderr)
        self.assertTrue(stderr.startswith('frame/rows: cells exceed body atlas'), stderr)


if __name__ == '__main__':
    unittest.main()
