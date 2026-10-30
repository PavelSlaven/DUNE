import json
import contextlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import numpy as np
from PIL import Image

from tools.hd_assets import PackEntry, encode_png, write_pack
from tools.units3d.redraw import main, parser
from tools.units3d import redraw_common as common
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

    def test_r1_default_source_and_pack_destination_are_distinct(self):
        unit_dir = ROOT / 'tools/units3d/units/UNIT_DEVASTATOR'
        unit = load_unit(unit_dir, 'shadow-rule')
        self.assertEqual(unit.pack_path, ROOT / 'tools/units3d/data/sdl_data_hd4_source.dat')
        args = parser().parse_args(['pack', str(unit_dir), 'atlases', 'copy'])
        self.assertEqual(args.source, ROOT / 'resources/bin/data/sdl_data_hd4.dat')

    def test_r1_changed_default_is_rejected_before_reading_but_explicit_pack_is_allowed(self):
        source = ROOT / 'tools/units3d/data/sdl_data_hd4_source.dat'
        changed = self.directory / 'changed.dat'
        changed.write_bytes(source.read_bytes() + b'extra')
        unit_dir = ROOT / 'tools/units3d/units/UNIT_DEVASTATOR'
        with patch.object(common, 'DEFAULT_PACK', changed):
            stderr = io.StringIO()
            with patch.object(common, 'read_pack', wraps=common.read_pack) as reader:
                with contextlib.redirect_stderr(stderr):
                    code = main(['shadow-rule', str(unit_dir)])
                self.assertEqual(code, 2)
                reader.assert_not_called()
            self.assertIn(str(changed), stderr.getvalue())
            explicit = load_unit(unit_dir, 'shadow-rule', changed)
            self.assertEqual(explicit.pack_path, changed)

    def test_r3_cleanup_keeps_six_pixel_soft_margin_and_counts_removed_pixels(self):
        pixels = np.zeros((1024, 1024, 4), np.uint8)
        pixels[300:700, 300:700] = (100, 100, 100, 255)
        pixels[500, 294] = (50, 20, 50, 50)
        pixels[500, 293] = (50, 20, 50, 50)
        pixels[20, 20] = (50, 20, 50, 50)
        cleaned, stray = common.clean_keyed(pixels)
        self.assertEqual(stray, 2)
        self.assertEqual(cleaned[500, 294, 3], 50)
        self.assertEqual(cleaned[500, 293, 3], 0)
        self.assertEqual(cleaned[20, 20, 3], 0)
        self.assertTrue(np.array_equal(cleaned[..., :3], pixels[..., :3]))

    def test_r3_keyed_cleans_magenta_soft_noise_and_black_detached_object(self):
        for background in ('magenta', 'black'):
            with self.subTest(background=background):
                color = (255, 0, 255) if background == 'magenta' else (0, 0, 0)
                pixels = np.full((1024, 1024, 3), color, np.uint8)
                pixels[300:700, 300:700] = 180
                if background == 'magenta':
                    pixels[20, 20] = (255, 80, 255)
                else:
                    pixels[18:23, 18:23] = 180
                path = self.directory / f'{background}.png'
                Image.fromarray(pixels).save(path)
                result = keyed(path)
                self.assertEqual(result[20, 20, 3], 0)
                self.assertEqual(result[500, 500, 3], 255)

    def test_r7_non_square_attempt_and_recolour_report_frame_and_path(self):
        original = json.loads((ROOT / 'tools/units3d/units/UNIT_DEVASTATOR/unit.json').read_text())
        path = self.directory / 'non-square.png'
        Image.new('RGB', (80, 60), (180, 180, 180)).save(path)
        for kind, command in (('attempts', 'score'), ('recolour', 'build')):
            with self.subTest(kind=kind):
                data = json.loads(json.dumps(original))
                if kind == 'attempts':
                    data['frames'][3]['attempts']['a'] = str(path)
                else:
                    data['frames'][3]['recolour'] = str(path)
                (self.directory / 'unit.json').write_text(json.dumps(data), encoding='utf-8')
                with self.assertRaises(InputError) as caught:
                    load_unit(self.directory, command)
                self.assertIn('r0k3', str(caught.exception))
                self.assertIn(str(path), str(caught.exception))
                argv = [command, str(self.directory)]
                if command == 'build':
                    argv.append(str(self.directory / 'build-output'))
                stderr = io.StringIO()
                with contextlib.redirect_stderr(stderr):
                    code = main(argv)
                self.assertEqual(code, 2)
                self.assertIn('r0k3', stderr.getvalue())
                self.assertIn(str(path), stderr.getvalue())

    def test_r6_frame_input_adds_frame_and_path_only_for_input_errors(self):
        record = {'row': 1, 'k': 6}
        path = self.directory / 'input.png'
        for error in (InputError('empty silhouette'), OSError('unreadable')):
            with self.subTest(error=type(error).__name__):
                with self.assertRaises(InputError) as caught:
                    with common.frame_input(record, path):
                        raise error
                self.assertIn('r1k6', str(caught.exception))
                self.assertIn(str(path), str(caught.exception))

        with self.assertRaisesRegex(ValueError, 'unexpected'):
            with common.frame_input(record, path):
                raise ValueError('unexpected')

    def test_r6_cli_only_converts_input_errors_and_os_errors(self):
        from tools.units3d.redraw import main

        unit_dir = self.directory / 'unit'
        output = self.directory / 'out'
        for error in (InputError('invalid input'), OSError('missing file')):
            with self.subTest(error=type(error).__name__):
                stderr = io.StringIO()
                with patch('tools.units3d.redraw.load_unit', return_value=object()), \
                        patch('tools.units3d.redraw_build.run', side_effect=error), \
                        contextlib.redirect_stderr(stderr):
                    code = main(['build', str(unit_dir), str(output)])
                self.assertEqual(code, 2)
                self.assertIn(str(error), stderr.getvalue())

        for error_type in (ValueError, TypeError, KeyError):
            with self.subTest(error=error_type.__name__):
                with patch('tools.units3d.redraw.load_unit', return_value=object()), \
                        patch('tools.units3d.redraw_build.run', side_effect=error_type('unexpected')):
                    with self.assertRaises(error_type):
                        main(['build', str(unit_dir), str(output)])


if __name__ == '__main__':
    unittest.main()
