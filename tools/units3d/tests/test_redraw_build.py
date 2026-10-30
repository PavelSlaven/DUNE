import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

import numpy as np
from PIL import Image

from tools.hd_assets import PackEntry, encode_png, write_pack
from tools.units3d.redraw import main
from tools.units3d.redraw_build import _fit_scale, run
from tools.units3d.redraw_common import ROOT, load_unit


class BuildTests(unittest.TestCase):
    def setUp(self):
        (ROOT / '.tmp').mkdir(exist_ok=True)
        temporary = tempfile.TemporaryDirectory(dir=ROOT / '.tmp')
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.body = np.zeros((68, 512, 4), np.uint8)
        for row in range(2):
            for k in range(8):
                self.body[row * 32 + 8:row * 32 + 24, k * 64 + 8:k * 64 + 56] = (100, 110, 120, 255)
        self.pack = self.root / 'source.dat'
        canvas = np.full((1024, 1024, 3), (255, 0, 255), np.uint8)
        canvas[384:640, 128:896] = (100, 110, 120)
        self.attempt = self.root / 'attempt.png'
        Image.fromarray(canvas).save(self.attempt)
        self.data = {'atlases': {'body': 'BODY', 'house_mask': None, 'shadow': 'SHADOW'},
                     'frame': [64, 32], 'rows': 2,
                     'shadow_rule': {'shift': 0, 'alpha': 64, 'rgb': [5, 4, 3]},
                     'frames': [{'row': row, 'k': k, 'attempts': {'chosen': str(self.attempt)},
                                 'pick': 'chosen'} for row in range(2) for k in range(8)]}

    def _write_inputs(self):
        entries = [PackEntry(0, 'BODY', 'png', encode_png(Image.fromarray(self.body))),
                   PackEntry(1, 'SHADOW', 'png', encode_png(Image.fromarray(np.zeros_like(self.body))))]
        if self.data['atlases']['house_mask'] is not None:
            entries.append(PackEntry(2, 'MASK', 'png', encode_png(Image.fromarray(self.body))))
        write_pack(self.pack, entries)
        (self.root / 'unit.json').write_text(json.dumps(self.data), encoding='utf-8')

    def build(self):
        self._write_inputs()
        unit = load_unit(self.root, 'build', self.pack)
        output = self.root / 'out'
        stdout, stderr = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = run(unit, SimpleNamespace(output=output))
        return code, output, stderr.getvalue()

    def build_cli(self, output=None):
        self._write_inputs()
        output = output or self.root / 'cli-out'
        stdout, stderr = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = main(['build', str(self.root), str(output), '--pack', str(self.pack)])
        return code, output, stdout.getvalue(), stderr.getvalue()

    def test_multiple_rows_wide_frame_zero_shift_and_no_mask(self):
        code, output, stderr = self.build()
        self.assertEqual(code, 0, stderr)
        body = np.array(Image.open(output / 'BODY.png').convert('RGBA'))
        shadow = np.array(Image.open(output / 'SHADOW.png').convert('RGBA'))
        self.assertEqual(body.shape, self.body.shape)
        self.assertFalse(body[64:].any())
        self.assertFalse(shadow[64:].any())
        self.assertTrue(np.array_equal(shadow[:64, :, 3], np.round(body[:64, :, 3].astype(np.float32) * 64 / 255)))
        self.assertTrue(np.all(shadow[:64, :, :3] == (5, 4, 3)))
        for row in range(2):
            for k in range(8):
                self.assertTrue((output / 'frames' / f'r{row}k{k}.png').is_file())
        metrics = (output / 'metrics.txt').read_text(encoding='utf-8')
        self.assertIn('1\t7\tchosen\t-\t-\t-\t0\tTrue', metrics)
        self.assertTrue(metrics.endswith('corridor\t-\t-\nall frames pass\n'))
        self.assertEqual(len(json.loads((output / 'params.json').read_text())['frames']), 16)

    def test_empty_recolour_mask_fails_share_without_input_error(self):
        self.data['atlases']['house_mask'] = 'MASK'
        for record in self.data['frames']:
            record['recolour'] = str(self.attempt)
        code, output, stderr = self.build()
        self.assertEqual(code, 1)
        self.assertIn('r0k0: share', stderr)
        self.assertIn('r1k7: share', stderr)
        self.assertFalse((output / 'atlases.json').exists())
        self.assertFalse((output / 'BODY.png').exists())
        self.assertTrue((output / 'frames' / 'r1k7.png').exists())

    def test_without_shadow_needs_no_shadow_rule_and_emits_only_body(self):
        self.data['atlases']['shadow'] = None
        del self.data['shadow_rule']
        code, output, stderr = self.build()
        self.assertEqual(code, 0, stderr)
        entries = json.loads((output / 'atlases.json').read_text())['entries']
        self.assertEqual(set(entries), {'BODY'})
        self.assertFalse((output / 'SHADOW.png').exists())

    def test_r3_metrics_count_selected_attempt_stray_pixels(self):
        pixels = np.array(Image.open(self.attempt))
        pixels[20, 20] = (255, 80, 255)
        Image.fromarray(pixels).save(self.attempt)
        code, output, stderr = self.build()
        self.assertEqual(code, 0, stderr)
        lines = (output / 'metrics.txt').read_text().splitlines()
        self.assertEqual(lines[0], 'row\tk\tpick\tiou\tshare\told_share\tstray\tok')
        for line in lines[1:17]:
            self.assertEqual(line.split('\t')[6:], ['1', 'True'])

    def test_r6_blank_selected_attempt_reports_frame_and_path_as_input_error(self):
        Image.new('RGB', (1024, 1024), (255, 0, 255)).save(self.attempt)

        code, output, stdout, stderr = self.build_cli()

        self.assertEqual(code, 2, stdout + stderr)
        self.assertIn('r0k0', stderr)
        self.assertIn(str(self.attempt), stderr)

    def test_r6_blank_recolour_reports_frame_and_path_but_no_green_body_stays_share_failure(self):
        self.data['atlases']['house_mask'] = 'MASK'
        recolour = self.root / 'blank-recolour.png'
        Image.new('RGB', (1024, 1024), (255, 0, 255)).save(recolour)
        for record in self.data['frames']:
            record['recolour'] = str(recolour)

        code, output, stdout, stderr = self.build_cli()

        self.assertEqual(code, 2, stdout + stderr)
        self.assertIn('r0k0', stderr)
        self.assertIn(str(recolour), stderr)

    def test_fit_scale_uses_relative_floor_and_binary_search(self):
        median = 1.173
        threshold = 0.9752
        calls = []

        def fits(candidate):
            calls.append(candidate)
            return candidate <= threshold

        scale = _fit_scale(median, fits)
        expected = median - 0.001 * int(np.ceil((median - threshold) / 0.001))
        search_budget = int(np.ceil(np.log2(np.ceil(0.2 * median / 0.001) + 1))) + 1

        self.assertAlmostEqual(scale, expected)
        self.assertLessEqual(len(calls), search_budget)
        self.assertTrue(scale <= threshold)
        self.assertGreater(scale + 0.001, threshold)

        calls.clear()
        lowest = _fit_scale(median, lambda candidate: calls.append(candidate) or False)
        self.assertAlmostEqual(lowest, 0.939)
        self.assertGreaterEqual(lowest, 0.8 * median)
        self.assertLess(lowest - 0.001, 0.8 * median)
        self.assertLessEqual(len(calls), search_budget)

    def test_fit_scale_includes_exact_floor_and_supports_medians_below_half(self):
        self.assertEqual(_fit_scale(1.0, lambda candidate: False), 0.8)
        for median in (1.0, 0.4, 0.004):
            with self.subTest(median=median):
                lowest = _fit_scale(median, lambda candidate: False)
                self.assertGreaterEqual(lowest, 0.8 * median)
                self.assertLess(lowest - 0.001, 0.8 * median)
                steps = (median - lowest) / 0.001
                self.assertAlmostEqual(steps, round(steps))
                self.assertEqual(_fit_scale(median, lambda candidate: True), median)

    def test_r8_positive_explicit_scale_below_fit_floor_is_valid(self):
        self.data['scale'] = 0.4
        code, output, stdout, stderr = self.build_cli()

        self.assertEqual(code, 0, stdout + stderr)
        params = json.loads((output / 'params.json').read_text(encoding='utf-8'))
        self.assertEqual(params['scale'], 0.4)

    def test_r8_invalid_optional_unit_scale_is_rejected_by_cli(self):
        invalid_values = (
            ('null', None),
            ('true', True),
            ('false', False),
            ('zero', 0),
            ('negative', -1),
            ('string', 'automatic'),
            ('list', ['fit']),
            ('infinity', float('inf')),
            ('nan', float('nan')),
        )
        for label, value in invalid_values:
            with self.subTest(value=label):
                self.data['scale'] = value
                output = self.root / f'cli-scale-{label}'
                code, _, stdout, stderr = self.build_cli(output)
                self.assertEqual(code, 2, stdout + stderr)
                self.assertIn('scale', stderr)


if __name__ == '__main__':
    unittest.main()
