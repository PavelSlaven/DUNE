from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

import numpy as np
from PIL import Image

from tools.units3d.redraw_common import ROOT, InputError
from tools.units3d.redraw_sheets import run


class UnitFixture:
    def __init__(self, frames, frame, rows, atlases, images, data=None, entries=None):
        self._frames = frames
        self.frame = frame
        self.rows = rows
        self.atlases = atlases
        self.images = images
        self.data = data or {}
        self.entries = entries or []

    @property
    def frames(self):
        return sorted(self._frames, key=lambda record: (record['row'], record['k']))

    def path(self, value):
        value = Path(value)
        return value if value.is_absolute() else ROOT / value

    def image(self, name):
        if name not in self.images:
            raise InputError(f'pack: missing image {name}')
        return self.images[name]

    def old_frame(self, role, record):
        fw, fh = self.frame
        x, y = record['k'] * fw, record['row'] * fh
        return self.image(self.atlases[role])[y:y + fh, x:x + fw].copy()


class RedrawSheetsTests(unittest.TestCase):
    def setUp(self):
        temporary_root = ROOT / '.tmp'
        temporary_root.mkdir(exist_ok=True)
        temporary = tempfile.TemporaryDirectory(dir=temporary_root)
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)

    def save_rgba(self, path, pixels):
        Image.fromarray(np.asarray(pixels, dtype=np.uint8)).save(path)

    def test_contact_uses_max_attempt_count_and_preserves_attempt_key_order(self):
        inputs = self.root / 'inputs'
        inputs.mkdir()
        records = [
            {'row': 1, 'k': 1, 'attempts': {'b': str(self.root / 'b.png'), 'a': str(self.root / 'a.png')}},
            {'row': 0, 'k': 3, 'attempts': {'a': str(self.root / 'single.png')}},
        ]
        colors = {
            'old_r0k3.png': (10, 20, 30),
            'guide_r0k3.png': (40, 50, 60),
            'old_r1k1.png': (20, 30, 40),
            'guide_r1k1.png': (50, 60, 70),
        }
        for name, color in colors.items():
            Image.new('RGB', (9, 7), color).save(inputs / name)
        Image.new('RGB', (12, 12), (80, 90, 100)).save(self.root / 'single.png')
        Image.new('RGB', (12, 12), (110, 120, 130)).save(self.root / 'b.png')
        Image.new('RGB', (12, 12), (140, 150, 160)).save(self.root / 'a.png')
        unit = UnitFixture(records, (4, 3), 2, {}, {})
        output = self.root / 'contact.png'

        status = run(unit, SimpleNamespace(command='contact', inputs=inputs, output=output))

        self.assertEqual(status, 0)
        with Image.open(output) as image:
            self.assertEqual(image.size, (1200, 660))
            self.assertEqual(image.getpixel((150, 180)), (10, 20, 30))
            self.assertEqual(image.getpixel((450, 180)), (40, 50, 60))
            self.assertEqual(image.getpixel((750, 180)), (80, 90, 100))
            self.assertEqual(image.getpixel((750, 480)), (110, 120, 130))
            self.assertEqual(image.getpixel((1050, 480)), (140, 150, 160))
            self.assertEqual(image.getpixel((1050, 180)), (30, 30, 30))

    def test_r4_contact_keeps_raw_attempt_pixels(self):
        inputs = self.root / 'inputs'
        inputs.mkdir()
        Image.new('RGB', (30, 30), (10, 20, 30)).save(inputs / 'old_r0k0.png')
        Image.new('RGB', (30, 30), (40, 50, 60)).save(inputs / 'guide_r0k0.png')
        pixels = np.full((30, 30, 4), (255, 0, 255, 0), dtype=np.uint8)
        pixels[12:24, 12:24] = (255, 255, 0, 0)
        pixels[2, 2] = (0, 255, 0, 0)
        attempt = self.root / 'attempt.png'
        self.save_rgba(attempt, pixels)
        unit = UnitFixture(
            [{'row': 0, 'k': 0, 'attempts': {'a': str(attempt)}}],
            (4, 3),
            1,
            {},
            {},
        )
        output = self.root / 'contact.png'
        expected = Image.open(attempt).convert('RGB').resize(
            (300, 300), Image.Resampling.LANCZOS,
        )

        status = run(unit, SimpleNamespace(command='contact', inputs=inputs, output=output))

        self.assertEqual(status, 0)
        with Image.open(output) as image:
            actual = image.crop((600, 30, 900, 330))
            self.assertTrue(np.array_equal(np.asarray(actual), np.asarray(expected)))
            self.assertGreater(expected.getpixel((23, 23))[1], 200)

    def test_sheet_selects_requested_row_without_optional_masks_or_shadows(self):
        fw, fh, rows = 10, 8, 2
        body = np.zeros((rows * fh, fw * 8, 4), dtype=np.uint8)
        new_body = np.zeros_like(body)
        for row in range(rows):
            for k in range(8):
                x, y = k * fw, row * fh
                body[y + 1:y + 7, x + 1:x + 6] = (50 + row * 30 + k, 100 + row, 150, 255)
                new_body[y + 1:y + 7, x + 1:x + 6] = (100 + row * 40 + k, 60, 40, 255)
        sand = np.full((3, 4, 4), (30, 30, 30, 255), dtype=np.uint8)
        building = np.zeros((3, 4, 4), dtype=np.uint8)
        building[1:, 2:] = (210, 180, 150, 255)
        images = {'BODY': body, 'TERRAIN_SAND': sand, 'BUILDING': building}
        records = [{'row': row, 'k': k} for row in range(rows) for k in range(8)]
        unit = UnitFixture(
            records,
            (fw, fh),
            rows,
            {'body': 'BODY', 'house_mask': None, 'shadow': None},
            images,
            {'sheet_building': {'name': 'BUILDING', 'size': [4, 3]}},
        )
        atlases = self.root / 'atlases'
        atlases.mkdir()
        self.save_rgba(atlases / 'BODY.png', new_body)
        output = self.root / 'sheet.png'

        status = run(unit, SimpleNamespace(command='sheet', atlases=atlases, output=output, row=1))

        self.assertEqual(status, 0)
        with Image.open(output) as image:
            self.assertEqual(image.size, (390, 466))
            self.assertTrue(np.allclose(image.getpixel((298, 48)), (83, 101, 150), atol=6))
            self.assertTrue(np.allclose(image.getpixel((298, 64)), (143, 60, 40), atol=6))
            self.assertEqual(image.getpixel((248, 48)), (30, 30, 30))
            self.assertEqual(image.getpixel((232, 177)), (210, 180, 150))
            self.assertEqual(image.getpixel((230, 176)), (30, 30, 30))
            self.assertEqual(image.getpixel((254, 230)), (86, 101, 150))
            self.assertEqual(image.getpixel((354, 230)), (146, 60, 40))

    def test_r2_shadow_alpha_composes_for_unit_and_building(self):
        fw = fh = 2
        body = np.zeros((fh, fw * 8, 4), dtype=np.uint8)
        shadow = np.zeros_like(body)
        shadow[:] = (0, 0, 0, 128)
        building = np.zeros((2, 2, 4), dtype=np.uint8)
        building_shadow = shadow[:, :2].copy()
        sand = np.full((2, 2, 4), (200, 200, 200, 255), dtype=np.uint8)
        unit = UnitFixture(
            [{'row': 0, 'k': k} for k in range(8)],
            (fw, fh),
            1,
            {'body': 'BODY', 'house_mask': None, 'shadow': 'SHADOW'},
            {
                'BODY': body,
                'SHADOW': shadow,
                'TERRAIN_SAND': sand,
                'BUILDING': building,
                'BUILDING_SHADOW': building_shadow,
            },
            {'sheet_building': {'name': 'BUILDING', 'size': [2, 2]}},
            entries=[SimpleNamespace(name='BUILDING_SHADOW')],
        )
        atlases = self.root / 'atlases'
        atlases.mkdir()
        self.save_rgba(atlases / 'BODY.png', body)
        self.save_rgba(atlases / 'SHADOW.png', shadow)
        output = self.root / 'sheet-shadow.png'

        status = run(unit, SimpleNamespace(
            command='sheet', atlases=atlases, output=output, row=0,
        ))

        self.assertEqual(status, 0)
        expected = (137, 137, 137)
        with Image.open(output) as image:
            self.assertEqual(image.getpixel((231, 41)), expected)
            self.assertEqual(image.getpixel((231, 45)), expected)
            self.assertEqual(image.getpixel((231, 105)), expected)

    def test_sheet_rejects_out_of_range_row(self):
        unit = UnitFixture([], (10, 8), 1, {}, {})
        with self.assertRaisesRegex(InputError, 'row: expected integer from 0 to 0'):
            run(unit, SimpleNamespace(command='sheet', row=1))

    def test_contact_missing_input_reports_its_path(self):
        missing = self.root / 'inputs' / 'old_r0k0.png'
        unit = UnitFixture(
            [{'row': 0, 'k': 0, 'attempts': {'a': str(self.root / 'attempt.png')}}],
            (10, 8),
            1,
            {},
            {},
        )
        with self.assertRaisesRegex(InputError, str(missing)):
            run(unit, SimpleNamespace(command='contact', inputs=missing.parent, output=self.root / 'contact.png'))


if __name__ == '__main__':
    unittest.main()
