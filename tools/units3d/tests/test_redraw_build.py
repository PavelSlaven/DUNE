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
from tools.units3d.redraw_build import run
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

    def build(self):
        entries = [PackEntry(0, 'BODY', 'png', encode_png(Image.fromarray(self.body))),
                   PackEntry(1, 'SHADOW', 'png', encode_png(Image.fromarray(np.zeros_like(self.body))))]
        if self.data['atlases']['house_mask'] is not None:
            entries.append(PackEntry(2, 'MASK', 'png', encode_png(Image.fromarray(self.body))))
        write_pack(self.pack, entries)
        (self.root / 'unit.json').write_text(json.dumps(self.data), encoding='utf-8')
        unit = load_unit(self.root, 'build', self.pack)
        output = self.root / 'out'
        stdout, stderr = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = run(unit, SimpleNamespace(output=output))
        return code, output, stderr.getvalue()

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
        self.assertIn('1\t7\tchosen\t-\t-\t-\tTrue', metrics)
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


if __name__ == '__main__':
    unittest.main()
