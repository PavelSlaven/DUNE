"""Assemble HD4 atlases from the frames written by render_unit.py.

  python tools/units3d/build_atlases.py --unit resources/hd/units3d/<key> --render <dir> --out <dir>

Behaviour is specified in docs/units/UNITS3D_SPEC.md.
"""

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image

COLUMNS = 8
SHADOW_MAX_ALPHA = 51
MIN_ALPHA = 8
OPAQUE_ALPHA = 16


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def downsample(path, frame):
    # Premultiplied resampling keeps transparent black from bleeding into edge colours.
    return np.array(Image.open(path).convert('RGBA').convert('RGBa').resize(frame, Image.LANCZOS).convert('RGBA'))


def atlas_from(frames, frame, atlas_size):
    atlas = np.zeros((atlas_size[1], atlas_size[0], 4), dtype=np.uint8)
    for k, pixels in enumerate(frames):
        atlas[:frame[1], k * frame[0]:(k + 1) * frame[0]] = pixels
    return atlas


def clean(pixels):
    faint = pixels[..., 3] < MIN_ALPHA
    pixels[faint] = 0
    return pixels


def shadow_frames(frames):
    peak = max(int(f[..., 3].max()) for f in frames)
    result = []
    for f in frames:
        out = np.zeros_like(f)
        out[..., 3] = np.round(f[..., 3].astype(np.float32) * SHADOW_MAX_ALPHA / peak).astype(np.uint8)
        result.append(out)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--unit', required=True, type=Path)
    parser.add_argument('--render', required=True, type=Path)
    parser.add_argument('--out', required=True, type=Path)
    args = parser.parse_args()

    unit = json.loads((args.unit / 'unit.json').read_text(encoding='utf-8'))
    frame = tuple(unit['frame_hd4'])
    atlas_size = tuple(unit['atlas_hd4'])
    args.out.mkdir(parents=True, exist_ok=True)
    built = {}

    def write(name, frames):
        path = args.out / f'{name}.png'
        Image.fromarray(atlas_from(frames, frame, atlas_size), 'RGBA').save(path, optimize=True)
        built[name] = {'file': path.name, 'size': list(atlas_size), 'sha256': sha256(path)}

    for part, entries in unit['parts'].items():
        source = args.render / part
        colors = [clean(downsample(source / f'color_{k}.png', frame)) for k in range(COLUMNS)]
        write(entries['atlas'], colors)
        if entries.get('mask'):
            masks = [clean(downsample(source / f'mask_{k}.png', frame)) for k in range(COLUMNS)]
            for mask, color in zip(masks, colors):
                mask[color[..., 3] <= OPAQUE_ALPHA] = 0
            write(entries['mask'], masks)
        if entries.get('shadow'):
            write(entries['shadow'], shadow_frames([clean(downsample(source / f'shadow_{k}.png', frame)) for k in range(COLUMNS)]))

    common = args.unit.parent / 'common'
    manifest = {
        'entries': built,
        'hashes': {
            **{name: sha256(common / name) for name in ('camera.json', 'light.json', 'render.json')},
            'unit.json': sha256(args.unit / 'unit.json'),
            'render_manifest.json': sha256(args.render / 'render_manifest.json'),
        },
    }
    (args.out / 'atlases.json').write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
