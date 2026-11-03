import argparse
import json
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage


def disk(radius):
    y, x = np.ogrid[-radius:radius + 1, -radius:radius + 1]
    return x * x + y * y <= radius * radius


def tone(pick, recolour, factor, radius, margin):
    rgb = np.asarray(Image.open(pick).convert('RGB')).astype(np.float32)
    edit = np.asarray(Image.open(recolour).convert('RGB')).astype(np.int16)
    green = edit[..., 1] - np.maximum(edit[..., 0], edit[..., 2]) >= 80
    body = np.sqrt(((rgb - (255, 0, 255)) ** 2).sum(axis=2)) > 60
    # Pixels touching the magenta background keep their colour: the build derives alpha from it.
    zone = ndimage.binary_dilation(green, disk(radius)) & ndimage.binary_erosion(body, disk(margin))
    grey = np.round((0.299 * rgb[..., 0] + 0.587 * rgb[..., 1] + 0.114 * rgb[..., 2]) * factor)
    out = rgb.copy()
    out[zone] = grey[zone][:, None]
    return Image.fromarray(out.astype(np.uint8), 'RGB')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('unit_json', type=Path)
    parser.add_argument('out_dir', type=Path)
    parser.add_argument('--factor', type=float, required=True)
    parser.add_argument('--radius', type=int, required=True)
    parser.add_argument('--margin', type=int, required=True)
    args = parser.parse_args()
    root = Path.cwd()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    for record in json.loads(args.unit_json.read_text())['frames']:
        key = record['pick'].removesuffix('_tone')
        name = f"launcher_k{record['k']}_{key}_tone.png"
        tone(root / record['attempts'][key], root / record['recolour'], args.factor, args.radius, args.margin).save(args.out_dir / name)
        print(name)


if __name__ == '__main__':
    main()
