import json
import tempfile
import unittest
from pathlib import Path

from PIL import Image

from tools.hd_assets import PackEntry, encode_png, write_pack
from tools.units3d.redraw_common import InputError, load_unit


class BooleanDirectionTests(unittest.TestCase):
    def test_boolean_direction_values_are_input_errors(self):
        with tempfile.TemporaryDirectory(prefix='units3d-boolean-k-') as temporary:
            directory = Path(temporary)
            atlas = Image.new('RGBA', (128, 12), (1, 2, 3, 255))
            pack = directory / 'pack.dat'
            write_pack(pack, [PackEntry(0, 'BODY', 'png', encode_png(atlas))])
            for value in (True, False):
                with self.subTest(k=value):
                    data = {'atlases': {'body': 'BODY', 'house_mask': None, 'shadow': None},
                            'frame': [16, 12], 'rows': 1,
                            'frames': [{'row': 0, 'k': k} for k in range(8) if k != int(value)]}
                    data['frames'].append({'row': 0, 'k': value})
                    (directory / 'unit.json').write_text(json.dumps(data), encoding='utf-8')
                    with self.assertRaisesRegex(InputError, f'frames: invalid row=0, k={value}'):
                        load_unit(directory, 'inputs', pack)
