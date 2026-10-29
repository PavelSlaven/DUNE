"""Leave-one-direction-out check: can a per-pixel colour classifier reproduce the old HM mask? (repo root)"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage

sys.path.insert(0, str(Path('tools').resolve()))
from hd_assets import read_pack, decode_image  # noqa: E402

FW, FH = 152, 184
pack = {e.name: e for e in read_pack(Path('resources/bin/data/sdl_data_hd4.dat'))}
img = np.array(decode_image(pack['UNIT_DEVASTATOR'].payload).convert('RGBA'))
hm = np.array(decode_image(pack['HM_UNIT_DEVASTATOR'].payload).convert('RGBA'))
sh = np.array(decode_image(pack['UNIT_DEVASTATOR_SHADOW'].payload).convert('RGBA'))


def features(frame):
    rgb = frame[..., :3].astype(np.float32)
    hsv = np.asarray(Image.fromarray(frame[..., :3]).convert('HSV'), np.float32)
    lum = rgb.mean(-1)
    local = [ndimage.uniform_filter(lum, s) for s in (3, 7)]
    var = ndimage.uniform_filter(lum ** 2, 5) - ndimage.uniform_filter(lum, 5) ** 2
    return np.dstack([rgb, hsv, *local, np.sqrt(np.maximum(var, 0))])


X, Y, M = [], [], []
for k in range(8):
    f = img[:FH, k * FW:(k + 1) * FW]
    on = f[..., 3] > 127
    strength = hm[:FH, k * FW:(k + 1) * FW, 3] / 255 * hm[:FH, k * FW:(k + 1) * FW, :3].max(-1) / 255
    X.append(features(f)[on]); Y.append(strength[on] > 0.5); M.append(on)
print('HM share per k:', [round(float(y.mean()), 2) for y in Y])
Q = 8


def bins(x):
    q = np.clip(x[:, :3] // (256 // Q), 0, Q - 1).astype(int)
    return (q[:, 0] * Q + q[:, 1]) * Q + q[:, 2]


for k in range(8):
    tr = [i for i in range(8) if i != k]
    b = np.concatenate([bins(X[i]) for i in tr]); y = np.concatenate([Y[i] for i in tr])
    hit = np.bincount(b, weights=y, minlength=Q ** 3); tot = np.bincount(b, minlength=Q ** 3)
    prob = np.where(tot > 0, hit / np.maximum(tot, 1), 0.5)
    p = prob[bins(X[k])] > 0.5
    iou = (p & Y[k]).sum() / (p | Y[k]).sum()
    print(f'k={k} IoU={iou:.3f} acc={(p == Y[k]).mean():.3f} share_true={Y[k].mean():.2f} share_pred={p.mean():.2f}')
s = sh[:FH, :, 3]
print('shadow alpha values:', np.unique(s)[:6], '... max', s.max(), 'shadow rgb max', sh[..., :3].max())
for k in (0, 2, 6):
    on = sh[:FH, k * FW:(k + 1) * FW, 3] > 0
    ys, xs = np.nonzero(on); bo = img[:FH, k * FW:(k + 1) * FW, 3] > 127; yb, xb = np.nonzero(bo)
    print(f'k={k} shadow bbox x{xs.min()}-{xs.max()} y{ys.min()}-{ys.max()} | body bbox x{xb.min()}-{xb.max()} y{yb.min()}-{yb.max()}')
