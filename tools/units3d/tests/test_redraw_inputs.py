from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import numpy as np
from PIL import Image

from tools.units3d.redraw_common import ROOT, old_canvas
from tools.units3d import redraw_inputs


class RedrawInputsTests(unittest.TestCase):
    def test_renders_one_guide_per_direction_and_reuses_it_across_rows(self):
        (ROOT / '.tmp').mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=ROOT / '.tmp') as temporary:
            output = Path(temporary) / 'inputs'
            frames = [
                {'row': 0, 'k': 2},
                {'row': 1, 'k': 2},
            ]
            old_frames = {
                (0, 2): np.full((3, 2, 4), (10, 20, 30, 255), dtype=np.uint8),
                (1, 2): np.full((3, 2, 4), (40, 50, 60, 255), dtype=np.uint8),
            }
            unit = SimpleNamespace(
                data={'block': [5, 4, 3], 'arrow': [1, 2, 3]},
                frames=frames,
                maximum=3,
                old_frame=lambda role, record: old_frames[(record['row'], record['k'])],
            )
            observed = {}

            def fake_blender(command, **kwargs):
                separator = command.index('--')
                script_args = command[separator + 1:]
                raw_dir = Path(script_args[0])
                observed['command'] = command
                observed['args'] = script_args
                pixels = np.zeros((1024, 1024, 4), dtype=np.uint8)
                pixels[:] = (0, 0, 0, 0)
                pixels[3, 4] = (20, 80, 120, 128)
                Image.fromarray(pixels, 'RGBA').save(raw_dir / 'guide_raw_k2.png')
                return SimpleNamespace(returncode=0, stdout='', stderr='')

            with patch.object(redraw_inputs, 'blender_executable', return_value='/blender'), \
                    patch.object(redraw_inputs.subprocess, 'run', side_effect=fake_blender):
                result = redraw_inputs.run(unit, SimpleNamespace(output=output))

            self.assertEqual(result, 0)
            self.assertEqual(
                observed['command'][observed['command'].index('--python-exit-code') + 1], '2'
            )
            self.assertEqual(observed['args'], [
                observed['args'][0], '3', '5', '4', '3', '1', '2', '3', '2',
            ])
            self.assertEqual(
                {path.name for path in output.iterdir()},
                {
                    'old_r0k2.png', 'old_r1k2.png',
                    'guide_r0k2.png', 'guide_r1k2.png',
                },
            )
            with Image.open(output / 'old_r0k2.png') as actual:
                self.assertTrue(np.array_equal(np.asarray(actual), np.asarray(old_canvas(old_frames[(0, 2)]))))
            with Image.open(output / 'old_r1k2.png') as actual:
                self.assertTrue(np.array_equal(np.asarray(actual), np.asarray(old_canvas(old_frames[(1, 2)]))))
            with Image.open(output / 'guide_r0k2.png') as first, Image.open(output / 'guide_r1k2.png') as second:
                self.assertTrue(np.array_equal(np.asarray(first), np.asarray(second)))
                self.assertEqual(first.mode, 'RGB')
                self.assertEqual(first.size, (1024, 1024))
