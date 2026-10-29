"""Score every choice of attempts: mirror-pair silhouette agreement, width ratio spread, extents against the 63 degree prediction.
usage: python -X utf8 choose.py   (run from the repo root)"""
import itertools
import math

import numpy as np
from PIL import Image

from common import S, CANVAS, FH, old_frames, keyed, bbox

T0, T1, H = math.radians(36), math.radians(63), 49.0
PAIRS = [(0, 4), (1, 3), (5, 7)]
old = old_frames()
sil, width, err = {}, {}, {}
for k in range(8):
    x0, y0, x1, y1 = bbox(old[k][..., 3])
    w, h = x1 - x0, y1 - y0
    pred = ((h - H * math.cos(T0)) / math.sin(T0) * math.sin(T1) + H * math.cos(T1)) / w
    for a in 'ab':
        r = keyed(S / f'g3/cand/g3_k{k}_{a}.png')
        cx0, cy0, cx1, cy1 = bbox(r[..., 3])
        width[k, a] = (cx1 - cx0) / (w * CANVAS / FH)
        err[k, a] = abs((cy1 - cy0) / (cx1 - cx0) - pred)
        crop = Image.fromarray(r[cy0:cy1, cx0:cx1, 3])
        sil[k, a] = crop


def mirror_iou(p, q):
    a, b = sil[p], sil[q].transpose(Image.FLIP_LEFT_RIGHT)
    size = ((a.width + b.width) // 2, (a.height + b.height) // 2)
    a, b = np.array(a.resize(size)) > 127, np.array(b.resize(size)) > 127
    return (a & b).sum() / (a | b).sum()


def old_iou(p, q):
    def crop(k):
        x0, y0, x1, y1 = bbox(old[k][..., 3])
        return Image.fromarray(old[k][y0:y1, x0:x1, 3])
    a, b = crop(p), crop(q).transpose(Image.FLIP_LEFT_RIGHT)
    size = ((a.width + b.width) // 2, (a.height + b.height) // 2)
    a, b = np.array(a.resize(size)) > 127, np.array(b.resize(size)) > 127
    return (a & b).sum() / (a | b).sum()


print('old mirror IoU', {f'{p}-{q}': round(old_iou(p, q), 3) for p, q in PAIRS})
for p, q in PAIRS:
    print(f'{p}-{q}', {f'{a}{b}': round(mirror_iou((p, a), (q, b)), 3) for a in 'ab' for b in 'ab'})
for k in range(8):
    print(k, {a: (round(width[k, a], 3), round(err[k, a], 3)) for a in 'ab'})
rows = []
for choice in itertools.product('ab', repeat=8):
    ws = np.log([width[k, a] for k, a in enumerate(choice)])
    mir = np.mean([mirror_iou((p, choice[p]), (q, choice[q])) for p, q in PAIRS])
    rows.append((ws.std(), -mir, np.mean([err[k, a] for k, a in enumerate(choice)]), ''.join(choice)))
for key_idx, name in ((0, 'width spread'), (1, 'mirror IoU'), (2, 'angle error')):
    best = sorted(rows, key=lambda r: r[key_idx])[:3]
    print(name, [(r[3], round(r[0], 3), round(-r[1], 3), round(r[2], 3)) for r in best])
