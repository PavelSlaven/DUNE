"""Silhouette extents of every candidate against the extents a 63 degree camera should give.
usage: python -X utf8 ratios.py   (run from the repo root)"""
import math

import numpy as np

from common import S, old_frames, keyed, bbox

T0, T1 = math.radians(36), math.radians(63)
H = 49.0
old = old_frames()
print('k\told w×h\tpred h/w\tcand\tw\th\th/w')
for k in range(8):
    x0, y0, x1, y1 = bbox(old[k][..., 3])
    w, h = x1 - x0, y1 - y0
    # Old bbox height = ground depth * sin36 + vertical height * cos36; the same parts at 63 degrees give the target.
    depth = (h - H * math.cos(T0)) / math.sin(T0)
    pred = (depth * math.sin(T1) + H * math.cos(T1)) / w
    for a in 'ab':
        r = keyed(S / f'g3/cand/g3_k{k}_{a}.png')
        cx0, cy0, cx1, cy1 = bbox(r[..., 3])
        cw, ch = cx1 - cx0, cy1 - cy0
        print(f'{k}\t{w}×{h} ({h / w:.2f})\t{pred:.2f}\t{a}\t{cw}\t{ch}\t{ch / cw:.2f}')
