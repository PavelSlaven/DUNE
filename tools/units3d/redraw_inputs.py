"""Build old-frame and guide canvases for one unit."""

from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
from pathlib import Path

from PIL import Image

from tools.units3d.redraw_common import InputError, ROOT, old_canvas, on_magenta

BLENDER_DEFAULT = Path('/srv/dune/tools/blender-5.2.3-linux-x64/blender')
GUIDE_SCRIPT = Path(__file__).with_name('guide_blender.py')


def blender_executable():
    configured = os.environ.get('BLENDER')
    value = configured or str(BLENDER_DEFAULT)
    found = shutil.which(value)
    if found:
        return found
    candidate = Path(value)
    if candidate.is_file() and os.access(candidate, os.X_OK):
        return str(candidate)
    raise InputError(f'Blender not found: {value}')


def _render_guides(unit, directions, raw_dir, executable):
    block = unit.data['block']
    arrow = unit.data['arrow']
    command = [
        executable,
        '-b',
        '--factory-startup',
        '--python-exit-code',
        '2',
        '--python',
        str(GUIDE_SCRIPT),
        '--',
        str(raw_dir),
        str(unit.maximum),
        *(str(value) for value in block),
        *(str(value) for value in arrow),
        *(str(direction) for direction in directions),
    ]
    result = subprocess.run(command, capture_output=True, text=True, check=False, timeout=1800)
    if result.returncode:
        transcript = (result.stderr or result.stdout).splitlines()
        detail = '\n'.join(transcript[-12:])
        suffix = f'\n{detail}' if detail else ''
        raise InputError(f'{executable}: guide render failed ({result.returncode}){suffix}')


def run(unit, args) -> int:
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    frames = unit.frames
    directions = sorted({record['k'] for record in frames})
    temporary_root = ROOT / '.tmp'
    temporary_root.mkdir(parents=True, exist_ok=True)
    executable = blender_executable()

    with tempfile.TemporaryDirectory(prefix='redraw-inputs-', dir=temporary_root) as temporary:
        raw_dir = Path(temporary)
        _render_guides(unit, directions, raw_dir, executable)
        guide_canvases = {}
        for direction in directions:
            raw_path = raw_dir / f'guide_raw_k{direction}.png'
            try:
                with Image.open(raw_path) as image:
                    guide_canvases[direction] = on_magenta(image.convert('RGBA'))
            except OSError as exc:
                raise InputError(f'{raw_path}: {exc}') from exc

    for record in frames:
        name = f"r{record['row']}k{record['k']}"
        old_canvas(unit.old_frame('body', record)).save(output / f'old_{name}.png')
        guide_canvases[record['k']].save(output / f'guide_{name}.png')

    print(f'inputs: {len(frames)} frames, {len(directions)} guides rendered')
    return 0
