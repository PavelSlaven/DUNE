"""Large side-by-side of old frame and both attempts for given directions, cropped to the tank.
usage: python -X utf8 zoom.py <out png> <k...>   (run from the repo root)"""
import sys

import numpy as np
from PIL import Image

from common import S, CANVAS, FW, FH, old_frames, keyed, bbox

out, ks = sys.argv[1], [int(k) for k in sys.argv[2:]]
old = old_frames()
X0 = (CANVAS - round(FW * CANVAS / FH)) // 2
tile = 460
sheet = Image.new('RGB', (3 * tile, len(ks) * tile), (200, 180, 140))
for r, k in enumerate(ks):
    big = np.zeros((CANVAS, CANVAS, 4), np.uint8)
    big[:, X0:CANVAS - X0] = np.array(Image.fromarray(old[k]).resize((CANVAS - 2 * X0, CANVAS), Image.LANCZOS))
    for c, img in enumerate([big] + [keyed(S / f'g3/cand/g3_k{k}_{a}.png') for a in 'ab']):
        x0, y0, x1, y1 = bbox(img[..., 3])
        cx, cy, half = (x0 + x1) // 2, (y0 + y1) // 2, 440
        crop = Image.fromarray(img).crop((cx - half, cy - half, cx + half, cy + half)).resize((tile, tile), Image.LANCZOS)
        sheet.paste(crop, (c * tile, r * tile), crop)
sheet.save(out)
