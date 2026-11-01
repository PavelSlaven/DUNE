import json
from pathlib import Path

import numpy as np
from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / '.tmp' / 'out-c'
OUT = BASE / 'cut'
UNIT_PATH = ROOT / 'tools/units3d/units/UNIT_HARVESTER/unit.json'
PARAMS_PATH = BASE / 'row0-b/params.json'
SOURCE = ROOT / 'units-gen/UNIT_HARVESTER'


def main():
    unit = json.loads(UNIT_PATH.read_text(encoding='utf-8'))
    params = json.loads(PARAMS_PATH.read_text(encoding='utf-8'))
    scale = float(unit['scale'])
    s = round(320 * scale)
    if round(320 * float(params['scale'])) != s:
        raise ValueError('row0 build scale differs from unit.json')
    frames = {(frame['row'], frame['k']): frame for frame in unit['frames']}
    row0 = {k: frames[0, k] for k in range(8)}
    records = [frames[row, k] for row in range(1, 4) for k in range(8)]
    if len(records) != 24:
        raise ValueError(f'expected 24 records for rows 1-3, got {len(records)}')
    lines = []
    pending = []
    for row in range(1, 4):
        for k in range(8):
            frame_name = f'r{row}k{k}'
            row0_record = row0[k]
            row0_path = ROOT / row0_record['attempts'][row0_record['pick']]
            with Image.open(row0_path) as image:
                b = np.asarray(image.convert('RGB').resize((1024, 1024), Image.Resampling.LANCZOS), dtype=np.int32)
            near_magenta = np.sum((b - np.array([255, 0, 255], dtype=np.int32)) ** 2, axis=2) <= 60 ** 2
            placement = params['frames'][f'r0k{k}']['offset']
            dx, dy = int(placement[0]), int(placement[1])
            xs = (np.arange(1024, dtype=np.float64) + 0.5) * s / 1024 + dx - 0.5
            ys = (np.arange(1024, dtype=np.float64) + 0.5) * s / 1024 + dy - 0.5
            x = xs[None, :]
            y = ys[:, None]
            d = np.minimum(np.minimum(x, y), np.minimum(319 - x, 207 - y))
            z = (d < 4) & near_magenta
            z_count = int(z.sum())
            for attempt in ('a', 'b'):
                names = (
                    f'harvester_r{row}k{k}_{attempt}.png',
                    f'harvester_recolour_r{row}k{k}_{attempt}.png',
                )
                images = []
                for name in names:
                    source_path = SOURCE / name
                    with Image.open(source_path) as image:
                        if image.size != (1024, 1024):
                            raise ValueError(f'{source_path}: expected 1024x1024, got {image.size}')
                        pixels = np.asarray(image.convert('RGB')).copy()
                    pixels[z] = (255, 0, 255)
                    images.append((OUT / name, pixels))
                for target, pixels in images:
                    pending.append((target, pixels))
                lines.append(f'{frame_name}_{attempt}\tZ={z_count}\t{names[0]}\t{names[1]}')
    if len(lines) != 48 or len(pending) != 96:
        raise ValueError(f'expected 48 masks and 96 outputs, got {len(lines)} and {len(pending)}')
    existing = [str(path) for path, _ in pending if path.exists()]
    if existing:
        raise FileExistsError('refusing to overwrite cut outputs: ' + ', '.join(existing))
    OUT.mkdir(parents=True, exist_ok=True)
    for target, pixels in pending:
        Image.fromarray(pixels, 'RGB').save(target)
    log = '\n'.join(lines) + '\n' + f'processed masks: {len(lines)}; saved PNGs: {len(pending)}; scale={scale:.6f}; s={s}\n'
    (BASE / 'cut.log').write_text(log, encoding='utf-8')
    with (ROOT / '.tmp/progress-c.md').open('a', encoding='utf-8') as stream:
        stream.write(f'Пункт 3 — обработано {len(lines)} масок для 24 кадров × 2 попытки, сохранено PNG: {len(pending)}; scale={scale:.6f}, s={s}; лог: .tmp/out-c/cut.log.\n')
    print(log, end='')


if __name__ == '__main__':
    main()
