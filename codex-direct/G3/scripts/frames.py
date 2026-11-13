"""Frames of the chosen attempts with one common scale, and the magenta inputs for the recolour run.
usage: python -X utf8 frames.py <input dir for the recolour run>   (run from the repo root)"""
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

from common import S, CANVAS, FH, CHOICE, old_boxes, keyed, bbox, place

INB = Path(sys.argv[1])
INB.mkdir(parents=True, exist_ok=True)
OUT = S / 'g3/frames'
OUT.mkdir(exist_ok=True)
boxes = old_boxes()
raw = {k: keyed(S / f'g3/cand/g3_k{k}_{a}.png') for k, a in CHOICE.items()}
ratios, offsets = [], {}
for k, r in raw.items():
    x0, _, x1, _ = bbox(r[..., 3])
    ratios.append((boxes[k][2] - boxes[k][0]) / ((x1 - x0) * FH / CANVAS))
scale = float(np.median(ratios))
print('scale', round(scale, 4), 'per-direction', [round(x, 3) for x in ratios])
for k, r in raw.items():
    frame, clipped, offsets[k] = place(r, k, scale, boxes)
    Image.fromarray(frame).save(OUT / f'k{k}.png')
    x0, y0, x1, y1 = bbox(frame[..., 3])
    ox0, oy0, ox1, oy1 = boxes[k]
    print(f'k{k} {CHOICE[k]}: new {x1 - x0}x{y1 - y0} old {ox1 - ox0}x{oy1 - oy0} box {x0},{y0}-{x1},{y1} clipped={clipped}')
    a = r[..., 3:].astype(np.float32) / 255
    flat = (r[..., :3] * a + np.array([255, 0, 255]) * (1 - a)).round().astype(np.uint8)
    Image.fromarray(flat).save(INB / f'pick_k{k}.png')
(OUT / 'params.json').write_text(json.dumps({'scale': scale, 'choice': CHOICE, 'offsets': offsets}, indent=1), encoding='utf-8')
