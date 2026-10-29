"""Shared pieces of the G3 one-off pipeline: pack access, magenta keying, frame fitting."""
import sys
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage

sys.path.insert(0, str(Path('tools').resolve()))
from hd_assets import read_pack, decode_image  # noqa: E402

S = Path(__file__).resolve().parent.parent
FW, FH, CANVAS = 152, 184, 1024
MAGENTA = np.array([255, 0, 255], np.float32)
PACK = Path('resources/bin/data/sdl_data_hd4.dat')
_pack = None


def pack_img(name):
    global _pack
    if _pack is None:
        _pack = {e.name: e for e in read_pack(PACK)}
    return np.array(decode_image(_pack[name].payload).convert('RGBA'))


def old_frames(name='UNIT_DEVASTATOR'):
    atlas = pack_img(name)
    return [atlas[:FH, k * FW:(k + 1) * FW] for k in range(8)]


def key(img):
    rgb = np.asarray(img.convert('RGB'), np.float32)
    corners = rgb[[0, 0, -1, -1], [0, -1, 0, -1]]
    if corners.max() < 16:
        # One generation came back on flat black; the background is the black region connected to the border.
        labels, _ = ndimage.label(rgb.max(-1) < 12)
        border = np.unique(np.concatenate([labels[0], labels[-1], labels[:, 0], labels[:, -1]]))
        a = (~np.isin(labels, border[border > 0])).astype(np.float32)
        a = ndimage.uniform_filter(a, 3)
        return np.dstack([rgb, a * 255]).round().astype(np.uint8)
    a = np.clip((np.linalg.norm(rgb - MAGENTA, axis=-1) - 60) / 70, 0, 1)
    labels, n = ndimage.label(a > 0.5)
    if n > 1:
        # Generators leave specks of non-magenta noise in the background; only the tank body is kept.
        sizes = ndimage.sum(np.ones_like(a), labels, range(1, n + 1))
        a[(labels > 0) & (labels != 1 + int(np.argmax(sizes)))] = 0
    safe = np.maximum(a, 1e-3)[..., None]
    color = np.clip((rgb - (1 - a[..., None]) * MAGENTA) / safe, 0, 255)
    return np.dstack([color, a * 255]).round().astype(np.uint8)


def keyed(path):
    return key(Image.open(path).resize((CANVAS, CANVAS), Image.LANCZOS))


def bbox(alpha):
    ys, xs = np.nonzero(alpha > 127)
    return int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1

CHOICE = dict(enumerate('bbababaa'))


def old_boxes():
    return [bbox(f[..., 3]) for f in old_frames()]


def place(rgba, k, scale, boxes, offset=None):
    """Scale a 1024 canvas into the 152x184 frame and put the alpha bbox centre on the old frame's bbox centre,
    or use a given offset so that an edit of the same picture lands exactly where its frame did."""
    size = round(CANVAS * FH / CANVAS * scale)
    small = np.array(Image.fromarray(rgba).convert('RGBa').resize((size, size), Image.LANCZOS))
    x0, y0, x1, y1 = bbox(small[..., 3])
    ox0, oy0, ox1, oy1 = boxes[k]
    cx, cy = round((ox0 + ox1 - x0 - x1) / 2), round((oy0 + oy1 - y0 - y1) / 2)
    ys, xs = np.nonzero(small[..., 3])
    # The old sprites touch the frame edge in some directions; the soft edge is kept whole by moving the tank inward.
    dx = min(max(cx, -int(xs.min())), FW - 1 - int(xs.max()))
    dy = min(max(cy, -int(ys.min())), FH - 1 - int(ys.max()))
    frame = np.zeros((FH, FW, 4), np.uint8)
    clipped = bool((xs + dx < 0).any() or (xs + dx >= FW).any() or (ys + dy < 0).any() or (ys + dy >= FH).any())
    if offset is not None:
        dx, dy = offset
    elif (dx, dy) != (cx, cy):
        print(f'k{k}: moved inward by {dx - cx},{dy - cy} px')
    fx0, fy0 = max(dx, 0), max(dy, 0)
    fx1, fy1 = min(dx + size, FW), min(dy + size, FH)
    frame[fy0:fy1, fx0:fx1] = small[fy0 - dy:fy1 - dy, fx0 - dx:fx1 - dx]
    return np.array(Image.fromarray(frame, 'RGBa').convert('RGBA')), clipped, (dx, dy)
