import json
import tempfile
import unittest
from pathlib import Path

import numpy as np
from PIL import Image

from tools.hd_assets import PackEntry, encode_png, write_pack
from tools.units3d.redraw import parser
from tools.units3d.redraw_common import ROOT, InputError, key, keyed, load_unit, place, prepare


class CommonTests(unittest.TestCase):
    def setUp(self):
        (ROOT / '.tmp').mkdir(exist_ok=True)
        temporary = tempfile.TemporaryDirectory(dir=ROOT / '.tmp')
        self.addCleanup(temporary.cleanup)
        self.directory = Path(temporary.name)

    def test_recolour_preserves_rgb_under_alpha_before_resize(self):
        path = self.directory / 'rgba.png'
        Image.new('RGBA', (4, 4), (0, 255, 0, 128)).save(path)
        image = prepare(path)
        self.assertEqual(image.mode, 'RGB')
        self.assertEqual(image.size, (1024, 1024))
        self.assertEqual(image.getpixel((500, 500)), (0, 255, 0))

    def test_attempt_keeps_rgba_during_resize_without_background_composition(self):
        path = self.directory / 'attempt.png'
        pixels = np.zeros((1024, 1024, 4), np.uint8)
        pixels[200:824, 200:824] = (200, 100, 50, 128)
        Image.fromarray(pixels).save(path)
        result = keyed(path)
        self.assertEqual(tuple(result[512, 512]), (200, 100, 50, 255))
        self.assertEqual(result[100, 100, 3], 0)

    def test_black_key_preserves_enclosed_black_region(self):
        pixels = np.zeros((40, 40, 3), np.uint8)
        pixels[8:32, 8:32] = 200
        pixels[16:24, 16:24] = 0
        result = key(Image.fromarray(pixels))
        self.assertEqual(result[0, 0, 3], 0)
        self.assertEqual(result[20, 20, 3], 255)

    def test_magenta_key_removes_detached_speck(self):
        pixels = np.full((40, 40, 3), (255, 0, 255), np.uint8)
        pixels[8:28, 8:28] = 180
        pixels[34:36, 34:36] = 180
        result = key(Image.fromarray(pixels))
        self.assertEqual(result[12, 12, 3], 255)
        self.assertEqual(result[34, 34, 3], 0)

    def test_clipping_uses_supplied_offset_and_detects_soft_alpha(self):
        pixels = np.zeros((1024, 1024, 4), np.uint8)
        pixels[400:600, 400:600] = (120, 120, 120, 255)
        pixels[100:200, 100:200] = (120, 120, 120, 1)
        _, normal, offset, _ = place(pixels, (64, 64), 1, (20, 20, 40, 40))
        self.assertFalse(normal)
        _, clipped, _, _ = place(pixels, (64, 64), 1, (20, 20, 40, 40), (-20, offset[1]))
        self.assertTrue(clipped)

    def test_empty_mask_can_be_placed_with_body_offset(self):
        mask = np.zeros((1024, 1024, 4), np.uint8)
        frame, clipped, _, _ = place(mask, (64, 48), 1, (0, 0, 1, 1), (-8, -10))
        self.assertFalse(clipped)
        self.assertFalse(frame.any())

    def test_minimal_shadow_description_and_duplicate_frame(self):
        atlas = Image.new('RGBA', (128, 24), (1, 2, 3, 255))
        pack = self.directory / 'pack.dat'
        write_pack(pack, [PackEntry(0, 'BODY', 'png', encode_png(atlas)),
                          PackEntry(1, 'SHADOW', 'png', encode_png(atlas))])
        data = {'atlases': {'body': 'BODY', 'house_mask': None, 'shadow': 'SHADOW'},
                'frame': [16, 12], 'rows': 2,
                'frames': [{'row': row, 'k': k} for row in range(2) for k in range(8)]}
        path = self.directory / 'unit.json'
        path.write_text(json.dumps(data), encoding='utf-8')
        unit = load_unit(self.directory, 'shadow-rule', pack)
        self.assertEqual(unit.old_frame('body', data['frames'][-1]).shape, (12, 16, 4))
        data['frames'][-1] = data['frames'][0]
        path.write_text(json.dumps(data), encoding='utf-8')
        with self.assertRaisesRegex(InputError, 'r0k0: duplicate'):
            load_unit(self.directory, 'shadow-rule', pack)

    def test_pack_cli_has_source_and_no_pack_option(self):
        args = parser().parse_args(['pack', 'unit', 'atlases', 'copy', '--source', 'old'])
        self.assertEqual(args.source, Path('old'))
        self.assertFalse(hasattr(args, 'pack'))


if __name__ == '__main__':
    unittest.main()
