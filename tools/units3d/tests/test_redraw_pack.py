from __future__ import annotations

import contextlib
import hashlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import numpy as np
from PIL import Image

from tools.hd_assets import PackEntry, encode_png, read_pack, write_pack
from tools.units3d import redraw_pack
from tools.units3d.redraw_common import ROOT


class RedrawPackTests(unittest.TestCase):
    def setUp(self):
        (ROOT / '.tmp').mkdir(exist_ok=True)
        temporary = tempfile.TemporaryDirectory(dir=ROOT / '.tmp')
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.atlases = self.root / 'atlases'
        self.atlases.mkdir()
        self.source = self.root / 'source.dat'
        self.output = self.root / 'copy.dat'
        self.source_image = Image.new('RGBA', (4, 3), (15, 25, 35, 255))
        write_pack(
            self.source,
            [
                PackEntry(
                    index=0,
                    name='UNIT_TEST',
                    extension='PNG',
                    payload=encode_png(self.source_image),
                ),
                PackEntry(index=1, name='BINARY_TEST', extension='bin', payload=b'unchanged'),
            ],
        )
        self.unit = SimpleNamespace(
            pack_path=self.source,
            entries=None,
            atlases={'body': 'UNIT_TEST', 'house_mask': None, 'shadow': None},
            image=lambda name: np.asarray(self.source_image),
        )
        self.unit.entries = read_pack(self.source)
        self.payload = encode_png(Image.new('RGBA', (4, 3), (200, 40, 60, 255)))
        self.manifest = {
            'entries': {
                'UNIT_TEST': {
                    'file': 'UNIT_TEST.png',
                    'sha256': hashlib.sha256(self.payload).hexdigest(),
                    'size': [4, 3],
                }
            }
        }
        (self.atlases / 'UNIT_TEST.png').write_bytes(self.payload)
        self._save_manifest()
        self.args = SimpleNamespace(
            atlases=self.atlases,
            output=self.output,
            source=self.source,
        )

    def _save_manifest(self):
        (self.atlases / 'atlases.json').write_text(
            json.dumps(self.manifest, indent=2) + '\n', encoding='utf-8'
        )

    def test_invalid_decoded_size_returns_one_before_copy(self):
        self.manifest['entries']['UNIT_TEST']['size'] = [3, 4]
        self._save_manifest()

        with patch('tools.units3d.redraw_pack.subprocess.run') as installer:
            with contextlib.redirect_stderr(io.StringIO()):
                result = redraw_pack.run(self.unit, self.args)

        self.assertEqual(result, 1)
        self.assertFalse(self.output.exists())
        installer.assert_not_called()

    def test_missing_source_entry_returns_one_before_copy(self):
        info = self.manifest['entries'].pop('UNIT_TEST')
        self.manifest['entries']['UNIT_MISSING'] = info
        self.unit.atlases['body'] = 'UNIT_MISSING'
        self._save_manifest()

        with patch('tools.units3d.redraw_pack.subprocess.run') as installer:
            with contextlib.redirect_stderr(io.StringIO()):
                result = redraw_pack.run(self.unit, self.args)

        self.assertEqual(result, 1)
        self.assertFalse(self.output.exists())
        installer.assert_not_called()

    def test_install_command_runs_and_its_failure_returns_one(self):
        installer_result = SimpleNamespace(returncode=1)
        with patch(
            'tools.units3d.redraw_pack.subprocess.run',
            return_value=installer_result,
        ) as installer:
            with contextlib.redirect_stderr(io.StringIO()):
                result = redraw_pack.run(self.unit, self.args)

        self.assertEqual(result, 1)
        self.assertTrue(self.output.is_file())
        command = installer.call_args.args[0]
        self.assertEqual(command[0], sys.executable)
        self.assertEqual(command[1:3], ['tools/units3d/install.py', '--atlases'])
        self.assertEqual(command[3], str(self.atlases.resolve()))
        self.assertEqual(command[4:6], ['--pack', str(self.output.resolve())])
        self.assertEqual(installer.call_args.kwargs['cwd'], ROOT)
        self.assertLessEqual(installer.call_args.kwargs['timeout'], 1800)


if __name__ == '__main__':
    unittest.main()
