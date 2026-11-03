from pathlib import Path

import numpy as np
from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / '.tmp/u23-fade/new'
OUT = ROOT / '.tmp/u23-shift/new'
NAMES = ('UNIT_HARVESTER.png', 'HM_UNIT_HARVESTER.png', 'UNIT_HARVESTER_SHADOW.png')


def main():
    if OUT.exists():
        raise FileExistsError(f'refusing to overwrite {OUT}')
    pending = []
    for name in NAMES:
        with Image.open(SOURCE / name) as image:
            if image.size != (2560, 832):
                raise ValueError(f'{name}: expected 2560x832, got {image.size}')
            original = np.asarray(image.convert('RGBA')).copy()
        shifted = original.copy()
        affected = np.zeros((832, 2560), dtype=bool)
        cleared_alpha = 0
        for row in range(4):
            y0 = row * 208
            for k in range(8):
                amount = 44 if k in (0, 4) else 16
                x0 = k * 320
                moved = original[y0 + amount:y0 + 208, x0:x0 + 320].copy()
                shifted[y0:y0 + 208 - amount, x0:x0 + 320] = moved
                shifted[y0 + 208 - amount:y0 + 208, x0:x0 + 320] = (0, 0, 0, 0)
                affected[y0:y0 + 208, x0:x0 + 320] = True
                cleared_alpha += int(np.count_nonzero(shifted[y0 + 208 - amount:y0 + 208, x0:x0 + 320, 3]))
        outside_differences = int(np.count_nonzero(np.any(shifted[~affected] != original[~affected], axis=1)))
        if outside_differences or cleared_alpha:
            raise ValueError(f'{name}: outside differences={outside_differences}, cleared alpha={cleared_alpha}')
        pending.append((name, shifted))
    OUT.mkdir(parents=True)
    for name, pixels in pending:
        Image.fromarray(pixels, 'RGBA').save(OUT / name)
    print(f'shifted {len(pending)} atlases; cells=32; directions=k0-k7; amounts=k0,k4:44,others:16; transparent_tail_alpha={0}')


if __name__ == '__main__':
    main()
