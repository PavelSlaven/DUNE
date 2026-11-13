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
from tools.units3d import redraw, redraw_pack
from tools.units3d.redraw_common import InputError, ROOT


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

    def _write_cli_unit(self):
        unit_dir = self.root / 'unit'
        unit_dir.mkdir(exist_ok=True)
        (unit_dir / 'unit.json').write_text(
            json.dumps(
                {'atlases': {'body': 'UNIT_TEST', 'house_mask': None, 'shadow': None}}
            ) + '\n',
            encoding='utf-8',
        )
        return unit_dir

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

    def test_install_launch_error_returns_one_on_stderr(self):
        with patch(
            'tools.units3d.redraw_pack.subprocess.run',
            side_effect=FileNotFoundError('python not found'),
        ):
            stdout = io.StringIO()
            stderr = io.StringIO()
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                result = redraw_pack.run(self.unit, self.args)

        self.assertEqual(result, 1)
        self.assertEqual(stdout.getvalue(), '')
        self.assertIn('python not found', stderr.getvalue())

    def test_manifest_schema_errors_raise_input_error_before_copy(self):
        valid_info = self.manifest['entries']['UNIT_TEST'].copy()
        invalid_manifests = (
            {},
            {'entries': []},
            {'entries': {'UNIT_TEST': {'sha256': valid_info['sha256'], 'size': [4, 3]}}},
            {
                'entries': {
                    'UNIT_TEST': {
                        'file': 7,
                        'sha256': valid_info['sha256'],
                        'size': [4, 3],
                    }
                }
            },
            {'entries': {'UNIT_TEST': {'file': 'UNIT_TEST.png', 'size': [4, 3]}}},
            {'entries': {'UNIT_TEST': {'file': 'UNIT_TEST.png', 'sha256': 9, 'size': [4, 3]}}},
            {
                'entries': {
                    'UNIT_TEST': {
                        'file': 'UNIT_TEST.png',
                        'sha256': valid_info['sha256'],
                        'size': [4],
                    }
                }
            },
            {
                'entries': {
                    'UNIT_TEST': {
                        'file': 'UNIT_TEST.png',
                        'sha256': valid_info['sha256'],
                        'size': [4, True],
                    }
                }
            },
        )

        for manifest in invalid_manifests:
            with self.subTest(manifest=manifest):
                self.manifest = manifest
                self._save_manifest()
                with patch('tools.units3d.redraw_pack.subprocess.run') as installer:
                    with self.assertRaises(InputError):
                        redraw_pack.run(self.unit, self.args)

                self.assertFalse(self.output.exists())
                installer.assert_not_called()

    def test_manifest_entry_name_mismatch_returns_one_before_copy(self):
        info = self.manifest['entries'].pop('UNIT_TEST')
        self.manifest['entries']['UNIT_OTHER'] = info
        self._save_manifest()
        stderr = io.StringIO()

        with patch('tools.units3d.redraw_pack.subprocess.run') as installer:
            with contextlib.redirect_stderr(stderr):
                result = redraw_pack.run(self.unit, self.args)

        self.assertEqual(result, 1)
        self.assertTrue(stderr.getvalue())
        self.assertFalse(self.output.exists())
        installer.assert_not_called()

    def test_source_output_collision_raises_input_error(self):
        self.args.output = self.source

        with patch('tools.units3d.redraw_pack.subprocess.run') as installer:
            with self.assertRaises(InputError):
                redraw_pack.run(self.unit, self.args)

        installer.assert_not_called()

    def test_missing_atlas_file_propagates_oserror_before_copy(self):
        self.manifest['entries']['UNIT_TEST']['file'] = 'missing.png'
        self._save_manifest()

        with patch('tools.units3d.redraw_pack.subprocess.run') as installer:
            with self.assertRaises(FileNotFoundError):
                redraw_pack.run(self.unit, self.args)

        self.assertFalse(self.output.exists())
        installer.assert_not_called()

    def test_cli_returns_two_for_invalid_manifest_and_missing_atlas_file(self):
        unit_dir = self._write_cli_unit()
        valid_info = self.manifest['entries']['UNIT_TEST'].copy()
        mismatched_hash_info = valid_info.copy()
        mismatched_hash_info['sha256'] = '0' * 64
        cases = (
            {},
            {
                'entries': {
                    'UNIT_TEST': {
                        'file': 'missing.png',
                        'sha256': self.manifest['entries']['UNIT_TEST']['sha256'],
                        'size': [4, 3],
                    }
                }
            },
            {
                'entries': {
                    'UNIT_TEST': mismatched_hash_info,
                    'UNIT_EXTRA': {'sha256': valid_info['sha256'], 'size': [4, 3]},
                }
            },
        )

        for manifest in cases:
            with self.subTest(manifest=manifest):
                self.manifest = manifest
                self._save_manifest()
                stdout = io.StringIO()
                stderr = io.StringIO()
                argv = [
                    'pack',
                    str(unit_dir),
                    str(self.atlases),
                    str(self.output),
                    '--source',
                    str(self.source),
                ]
                with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                    result = redraw.main(argv)

                self.assertEqual(result, 2)
                self.assertEqual(stdout.getvalue(), '')
                self.assertTrue(stderr.getvalue())
                self.assertFalse(self.output.exists())

    def test_atlas_hash_mismatch_returns_one_on_stderr(self):
        self.manifest['entries']['UNIT_TEST']['sha256'] = '0' * 64
        self._save_manifest()
        stdout = io.StringIO()
        stderr = io.StringIO()

        with patch('tools.units3d.redraw_pack.subprocess.run') as installer:
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                result = redraw_pack.run(self.unit, self.args)

        self.assertEqual(result, 1)
        self.assertEqual(stdout.getvalue(), '')
        self.assertIn('SHA-256', stderr.getvalue())
        self.assertFalse(self.output.exists())
        installer.assert_not_called()

    def test_post_install_payload_mismatch_returns_one_on_stderr(self):
        changed = list(self.unit.entries)
        changed[0] = PackEntry(
            index=changed[0].index,
            name=changed[0].name,
            extension=changed[0].extension,
            payload=b'different payload',
        )
        stdout = io.StringIO()
        stderr = io.StringIO()

        with (
            patch(
                'tools.units3d.redraw_pack.subprocess.run',
                return_value=SimpleNamespace(returncode=0),
            ),
            patch('tools.units3d.redraw_pack.read_pack', return_value=changed),
            contextlib.redirect_stdout(stdout),
            contextlib.redirect_stderr(stderr),
        ):
            result = redraw_pack.run(self.unit, self.args)

        self.assertEqual(result, 1)
        self.assertEqual(stdout.getvalue(), '')
        self.assertIn('payload', stderr.getvalue())

    def test_unrelated_value_key_and_type_errors_propagate(self):
        failures = (
            ('tools.units3d.redraw_pack.decode_image', ValueError('decode bug')),
            ('tools.units3d.redraw_pack.shutil.copyfile', KeyError('copy bug')),
            ('tools.units3d.redraw_pack.subprocess.run', TypeError('launch bug')),
        )

        for target, error in failures:
            with self.subTest(error=type(error).__name__), patch(target, side_effect=error):
                with self.assertRaises(type(error)):
                    redraw_pack.run(self.unit, self.args)


if __name__ == '__main__':
    unittest.main()
