"""Shared unit description, pack access, image preparation and frame placement."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage

from tools.hd_assets import decode_image, read_pack

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PACK = ROOT / 'resources/bin/data/sdl_data_hd4.dat'
CANVAS = 1024
MAGENTA = np.array([255, 0, 255], np.float32)


class InputError(ValueError):
    pass


def frame_name(record):
    return f"r{record['row']}k{record['k']}"


def required(data, name, context='unit.json'):
    if name not in data or data[name] is None:
        raise InputError(f'{context}: missing {name}')
    return data[name]


def vector(data, name, length, positive=False):
    value = required(data, name)
    if (not isinstance(value, list) or len(value) != length
            or any(not isinstance(x, (int, float)) or not np.isfinite(x) for x in value)
            or (positive and any(x <= 0 for x in value))):
        raise InputError(f'{name}: expected {length} numeric values')
    return value


@dataclass
class Unit:
    data: dict
    pack_path: Path
    entries: list
    _images: dict = field(default_factory=dict)

    @property
    def atlases(self):
        return self.data['atlases']

    @property
    def frame(self):
        return tuple(self.data['frame'])

    @property
    def rows(self):
        return self.data['rows']

    @property
    def frames(self):
        return sorted(self.data['frames'], key=lambda f: (f['row'], f['k']))

    @property
    def maximum(self):
        return max(self.frame)

    def path(self, value):
        return ROOT / value

    def image(self, name):
        if name not in self._images:
            entry = next((e for e in self.entries if e.name == name), None)
            if entry is None:
                raise InputError(f'{self.pack_path}: missing entry {name}')
            image = decode_image(entry.payload)
            if image is None:
                raise InputError(f'{self.pack_path}: invalid image {name}')
            self._images[name] = np.array(image.convert('RGBA'))
        return self._images[name]

    def old_frame(self, role, record):
        fw, fh = self.frame
        x, y = record['k'] * fw, record['row'] * fh
        return self.image(self.atlases[role])[y:y + fh, x:x + fw].copy()


def load_unit(directory, command, pack_path=DEFAULT_PACK):
    source = Path(directory) / 'unit.json'
    try:
        data = json.loads(source.read_text(encoding='utf-8'))
    except (OSError, ValueError) as exc:
        raise InputError(f'{source}: {exc}') from exc
    if not isinstance(data, dict):
        raise InputError(f'{source}: expected object')
    atlases = required(data, 'atlases')
    if not isinstance(atlases, dict):
        raise InputError('atlases: expected object')
    for role in ('body', 'house_mask', 'shadow'):
        if role not in atlases:
            raise InputError(f'atlases.{role}: missing field')
        if (role == 'body' or atlases[role] is not None) and (
                not isinstance(atlases[role], str) or not atlases[role]):
            raise InputError(f'atlases.{role}: expected nonempty name')
    if command != 'pack':
        frame = vector(data, 'frame', 2, positive=True)
        if any(not isinstance(x, int) for x in frame):
            raise InputError('frame: expected integer dimensions')
        rows = required(data, 'rows')
        if not isinstance(rows, int) or rows <= 0:
            raise InputError('rows: expected positive integer')
        records = required(data, 'frames')
        if not isinstance(records, list):
            raise InputError('frames: expected list')
        seen = set()
        for record in records:
            if not isinstance(record, dict):
                raise InputError('frames: expected object')
            row, k = required(record, 'row', 'frames'), required(record, 'k', 'frames')
            if not isinstance(row, int) or not isinstance(k, int):
                raise InputError(f'frames: invalid row={row}, k={k}')
            name = frame_name(record)
            if not 0 <= row < rows or not 0 <= k < 8:
                raise InputError(f'{name}: frame outside rows or directions')
            if (row, k) in seen:
                raise InputError(f'{name}: duplicate frame')
            seen.add((row, k))
        for row in range(rows):
            for k in range(8):
                if (row, k) not in seen:
                    raise InputError(f'r{row}k{k}: missing frame')
        if command in ('score', 'contact', 'recolour-inputs', 'build'):
            for record in records:
                name = frame_name(record)
                attempts = required(record, 'attempts', name)
                if not isinstance(attempts, dict) or not attempts:
                    raise InputError(f'{name}: attempts must be nonempty')
                for value in attempts.values():
                    if not isinstance(value, str) or not value or not (ROOT / value).is_file():
                        raise InputError(f'{name}: attempts file {value}')
                if command in ('build', 'recolour-inputs'):
                    pick = required(record, 'pick', name)
                    if not isinstance(pick, str) or pick not in attempts:
                        raise InputError(f'{name}: pick {pick} missing from attempts')
                if command == 'build' and atlases['house_mask'] is not None:
                    value = required(record, 'recolour', name)
                    if not isinstance(value, str) or not value or not (ROOT / value).is_file():
                        raise InputError(f'{name}: recolour file {value}')
        if command == 'inputs':
            vector(data, 'block', 3, positive=True)
            vector(data, 'arrow', 3)
        if command == 'score':
            height = required(data, 'height_estimate')
            if not isinstance(height, (int, float)) or not np.isfinite(height) or height <= 0:
                raise InputError('height_estimate: expected positive number')
        if command == 'recolour-inputs' and atlases['house_mask'] is None:
            raise InputError('atlases.house_mask: recolour-inputs requires a mask')
        if command == 'shadow-rule' and atlases['shadow'] is None:
            raise InputError('atlases.shadow: shadow-rule requires a shadow')
        if command == 'build' and atlases['shadow'] is not None:
            rule = required(data, 'shadow_rule')
            if not isinstance(rule, dict):
                raise InputError('shadow_rule: expected object')
            shift = required(rule, 'shift', 'shadow_rule')
            alpha = required(rule, 'alpha', 'shadow_rule')
            if not isinstance(shift, int) or shift < 0:
                raise InputError('shadow_rule.shift: expected nonnegative integer')
            if not isinstance(alpha, (int, float)) or not 0 <= alpha <= 255:
                raise InputError('shadow_rule.alpha: expected 0..255')
            rgb = vector(rule, 'rgb', 3)
            if any(not isinstance(x, int) or not 0 <= x <= 255 for x in rgb):
                raise InputError('shadow_rule.rgb: expected integers 0..255')
        if command == 'sheet':
            building = required(data, 'sheet_building')
            if not isinstance(building, dict) or not isinstance(required(building, 'name', 'sheet_building'), str):
                raise InputError('sheet_building.name: expected name')
            size = vector(building, 'size', 2, positive=True)
            if any(not isinstance(x, int) for x in size):
                raise InputError('sheet_building.size: expected integer dimensions')
    pack_path = Path(pack_path)
    try:
        entries = read_pack(pack_path)
    except (OSError, ValueError) as exc:
        raise InputError(f'{pack_path}: {exc}') from exc
    unit = Unit(data, pack_path, entries)
    for name in atlases.values():
        if name is not None:
            unit.image(name)
    if command != 'pack':
        height, width = unit.image(atlases['body']).shape[:2]
        if 8 * frame[0] > width or rows * frame[1] > height:
            raise InputError('frame/rows: cells exceed body atlas')
        for name in atlases.values():
            if name is not None and unit.image(name).shape[:2] != (height, width):
                raise InputError(f'{name}: atlas size differs from body')
    if command == 'sheet':
        unit.image(data['sheet_building']['name'])
    return unit


def prepare(path):
    with Image.open(path) as image:
        return image.convert('RGB').resize((CANVAS, CANVAS), Image.Resampling.LANCZOS)


def key(img):
    rgb = np.asarray(img.convert('RGB'), np.float32)
    corners = rgb[[0, 0, -1, -1], [0, -1, 0, -1]]
    if corners.max() < 16:
        labels, _ = ndimage.label(rgb.max(-1) < 12)
        border = np.unique(np.concatenate([labels[0], labels[-1], labels[:, 0], labels[:, -1]]))
        a = (~np.isin(labels, border[border > 0])).astype(np.float32)
        a = ndimage.uniform_filter(a, 3)
        return np.dstack([rgb, a * 255]).round().astype(np.uint8)
    a = np.clip((np.linalg.norm(rgb - MAGENTA, axis=-1) - 60) / 70, 0, 1)
    labels, n = ndimage.label(a > 0.5)
    if n > 1:
        sizes = ndimage.sum(np.ones_like(a), labels, range(1, n + 1))
        a[(labels > 0) & (labels != 1 + int(np.argmax(sizes)))] = 0
    safe = np.maximum(a, 1e-3)[..., None]
    color = np.clip((rgb - (1 - a[..., None]) * MAGENTA) / safe, 0, 255)
    return np.dstack([color, a * 255]).round().astype(np.uint8)


def keyed(path):
    with Image.open(path) as image:
        return key(image.resize((CANVAS, CANVAS), Image.Resampling.LANCZOS))


def bbox(alpha):
    ys, xs = np.nonzero(alpha > 127)
    if not len(xs):
        raise InputError('bbox: no opaque pixels')
    return int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1


def on_magenta(image, position=(0, 0)):
    canvas = Image.new('RGBA', (CANVAS, CANVAS), (255, 0, 255, 255))
    canvas.alpha_composite(image.convert('RGBA'), position)
    return canvas.convert('RGB')


def old_canvas(frame):
    fh, fw = frame.shape[:2]
    maximum = max(fw, fh)
    image = Image.fromarray(frame).resize(
        (round(fw * CANVAS / maximum), round(fh * CANVAS / maximum)), Image.Resampling.LANCZOS)
    return on_magenta(image, ((CANVAS - image.width) // 2, (CANVAS - image.height) // 2))


def flat(rgba):
    alpha = rgba[..., 3:].astype(np.float32) / 255
    return Image.fromarray((rgba[..., :3] * alpha + MAGENTA.astype(np.int64) * (1 - alpha)).round().astype(np.uint8))


def place(rgba, frame_size, scale, box, offset=None):
    fw, fh = frame_size
    size = round(max(fw, fh) * scale)
    if size <= 0:
        raise InputError('scale: resized canvas is empty')
    small = np.array(Image.fromarray(rgba).convert('RGBa').resize((size, size), Image.Resampling.LANCZOS))
    ys, xs = np.nonzero(small[..., 3])
    if offset is None:
        x0, y0, x1, y1 = bbox(small[..., 3])
        ox0, oy0, ox1, oy1 = box
        cx, cy = round((ox0 + ox1 - x0 - x1) / 2), round((oy0 + oy1 - y0 - y1) / 2)
        dx = min(max(cx, -int(xs.min())), fw - 1 - int(xs.max()))
        dy = min(max(cy, -int(ys.min())), fh - 1 - int(ys.max()))
    else:
        dx, dy = offset
        cx, cy = offset
    clipped = bool((xs + dx < 0).any() or (xs + dx >= fw).any()
                   or (ys + dy < 0).any() or (ys + dy >= fh).any())
    frame = np.zeros((fh, fw, 4), np.uint8)
    fx0, fy0 = max(dx, 0), max(dy, 0)
    fx1, fy1 = min(dx + size, fw), min(dy + size, fh)
    if fx1 > fx0 and fy1 > fy0:
        frame[fy0:fy1, fx0:fx1] = small[fy0 - dy:fy1 - dy, fx0 - dx:fx1 - dx]
    return (np.array(Image.fromarray(frame, 'RGBa').convert('RGBA')), clipped,
            (dx, dy), (dx - cx, dy - cy))
