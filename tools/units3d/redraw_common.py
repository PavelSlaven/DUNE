"""Shared unit description, pack access, image preparation and frame placement."""

from __future__ import annotations

import json
import hashlib
from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage

from tools.hd_assets import decode_image, read_pack

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PACK = ROOT / 'tools/units3d/data/sdl_data_hd4_source.dat'
SOURCE_PACK_SHA256 = 'e2a87ce8cf9143f9d11ee0a54dcf10b7a57d109b49e713dadf4133c12d882045'
REPO_PACK = ROOT / 'resources/bin/data/sdl_data_hd4.dat'
CANVAS = 1024
DESPILL_BAND = 6
MAGENTA = np.array([255, 0, 255], np.float32)


class InputError(ValueError):
    pass


def frame_name(record):
    return f"r{record['row']}k{record['k']}"


@contextmanager
def frame_input(record, path):
    try:
        yield
    except (InputError, OSError) as exc:
        raise InputError(f'{frame_name(record)}: {path}: {exc}') from exc


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
    def reference_frame(self):
        return tuple(self.data.get('reference_frame', self.data['frame']))

    @property
    def reference_anchor(self):
        return tuple(self.data.get(
            'reference_anchor',
            (self.reference_frame[0] // 2, self.reference_frame[1] // 2),
        ))

    @property
    def output_anchor(self):
        return self.frame[0] // 2, self.frame[1] // 2

    @property
    def anchor_shift(self):
        return tuple(output - reference for output, reference in zip(
            self.output_anchor, self.reference_anchor, strict=True
        ))

    def output_box(self, box):
        dx, dy = self.anchor_shift
        x0, y0, x1, y1 = box
        return x0 + dx, y0 + dy, x1 + dx, y1 + dy

    @property
    def atlas_size(self):
        if 'atlas_size' in self.data:
            return tuple(self.data['atlas_size'])
        image = self.image(self.atlases['body'])
        return image.shape[1], image.shape[0]

    @property
    def rows(self):
        return self.data['rows']

    @property
    def frames(self):
        return sorted(self.data['frames'], key=lambda f: (f['row'], f['k']))

    @property
    def maximum(self):
        return max(self.reference_frame)

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
        fw, fh = self.reference_frame
        x, y = record['k'] * fw, record['row'] * fh
        return self.image(self.atlases[role])[y:y + fh, x:x + fw].copy()


def load_unit(directory, command, pack_path=None):
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
    figures = data.get('figures', 1)
    if isinstance(figures, bool) or not isinstance(figures, int) or not 1 <= figures <= 8:
        raise InputError('figures: expected an integer from 1 to 8')
    if 'despill' in data and not isinstance(data['despill'], bool):
        raise InputError('despill: expected true or false')
    if command != 'pack':
        frame = vector(data, 'frame', 2, positive=True)
        if any(isinstance(x, bool) or not isinstance(x, int) for x in frame):
            raise InputError('frame: expected integer dimensions')
        reference_frame = vector(data, 'reference_frame', 2, positive=True) if 'reference_frame' in data else frame
        if any(isinstance(x, bool) or not isinstance(x, int) for x in reference_frame):
            raise InputError('reference_frame: expected integer dimensions')
        if 'reference_anchor' in data:
            anchor = vector(data, 'reference_anchor', 2)
            if any(isinstance(x, bool) or not isinstance(x, int) for x in anchor):
                raise InputError('reference_anchor: expected integer coordinates')
            if any(not 0 <= anchor[axis] <= reference_frame[axis] for axis in range(2)):
                raise InputError('reference_anchor: coordinates must be inside reference_frame')
        rows = required(data, 'rows')
        if isinstance(rows, bool) or not isinstance(rows, int) or rows <= 0:
            raise InputError('rows: expected positive integer')
        if 'atlas_size' in data:
            atlas_size = vector(data, 'atlas_size', 2, positive=True)
            if any(isinstance(x, bool) or not isinstance(x, int) for x in atlas_size):
                raise InputError('atlas_size: expected integer dimensions')
            if atlas_size[0] < 8 * frame[0] or atlas_size[1] < rows * frame[1]:
                raise InputError('atlas_size: too small for frame grid')
        records = required(data, 'frames')
        if not isinstance(records, list):
            raise InputError('frames: expected list')
        seen = set()
        for record in records:
            if not isinstance(record, dict):
                raise InputError('frames: expected object')
            if 'scale_factor' in record:
                scale_factor = record['scale_factor']
                if (isinstance(scale_factor, bool)
                        or not isinstance(scale_factor, (int, float))
                        or not np.isfinite(scale_factor) or scale_factor <= 0):
                    raise InputError('scale_factor: expected a positive finite number')
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
        frames_by_position = {(record['row'], record['k']): record for record in records}
        for record in records:
            if 'offset_from' not in record:
                continue
            source_row = record['offset_from']
            if (isinstance(source_row, bool) or not isinstance(source_row, int)
                    or not 0 <= source_row < rows or source_row == record['row']):
                raise InputError(f'{frame_name(record)}: offset_from must name a different valid row')
            if 'offset_from' in frames_by_position[source_row, record['k']]:
                raise InputError(f'{frame_name(record)}: offset_from source must have no offset_from')
        if command in ('score', 'contact', 'recolour-inputs', 'build'):
            for record in records:
                name = frame_name(record)
                attempts = required(record, 'attempts', name)
                if not isinstance(attempts, dict) or not attempts:
                    raise InputError(f'{name}: attempts must be nonempty')
                for value in attempts.values():
                    if not isinstance(value, str) or not value or not (ROOT / value).is_file():
                        raise InputError(f'{name}: attempts file {value}')
                    validate_square(ROOT / value, record)
                if command in ('build', 'recolour-inputs'):
                    pick = required(record, 'pick', name)
                    if not isinstance(pick, str) or pick not in attempts:
                        raise InputError(f'{name}: pick {pick} missing from attempts')
                if command == 'build' and atlases['house_mask'] is not None:
                    value = required(record, 'recolour', name)
                    if not isinstance(value, str) or not value or not (ROOT / value).is_file():
                        raise InputError(f'{name}: recolour file {value}')
                    validate_square(ROOT / value, record)
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
        if command == 'build':
            if 'offset_shift' in data:
                offset_shift = data['offset_shift']
                if (not isinstance(offset_shift, list) or len(offset_shift) != 2
                        or any(type(value) is not int for value in offset_shift)):
                    raise InputError('offset_shift: expected two integer coordinates')
                if data.get('scale') == 'fit':
                    raise InputError('offset_shift: incompatible with scale="fit"')
            if 'scale' in data:
                scale = data['scale']
                if scale != 'fit' and (
                        isinstance(scale, bool) or not isinstance(scale, (int, float))
                        or not np.isfinite(scale) or scale <= 0):
                    raise InputError('scale: expected a positive finite number or "fit"')
            if 'share_corridor' in data:
                corridor = vector(data, 'share_corridor', 2)
                if any(isinstance(x, bool) for x in corridor) or corridor[0] > corridor[1]:
                    raise InputError('share_corridor: expected ordered numeric bounds')
            if 'red_fill' in data:
                threshold = data['red_fill']
                if isinstance(threshold, bool) or not isinstance(threshold, int) or not 1 <= threshold <= 255:
                    raise InputError('red_fill: expected an integer from 1 to 255')
                if atlases['house_mask'] is None:
                    raise InputError('red_fill: requires atlases.house_mask')
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
    if pack_path is None:
        pack_path = REPO_PACK if command == 'pack' else DEFAULT_PACK
        if command != 'pack':
            digest = hashlib.sha256(pack_path.read_bytes()).hexdigest()
            if digest != SOURCE_PACK_SHA256:
                raise InputError(f'{pack_path}: SHA-256 differs from the pinned source pack')
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
        if 8 * reference_frame[0] > width or rows * reference_frame[1] > height:
            grid = 'reference_frame/rows' if 'reference_frame' in data else 'frame/rows'
            raise InputError(f'{grid}: cells exceed body atlas')
        for name in atlases.values():
            if name is not None and unit.image(name).shape[:2] != (height, width):
                raise InputError(f'{name}: atlas size differs from body')
    if command == 'sheet':
        unit.image(data['sheet_building']['name'])
    return unit


def validate_square(path, record=None):
    prefix = f'{frame_name(record)}: ' if record is not None else ''
    try:
        with Image.open(path) as image:
            if image.width != image.height:
                raise InputError(f'{prefix}{path}: image must be square')
    except OSError as exc:
        raise InputError(f'{prefix}{path}: {exc}') from exc


def prepare(path):
    validate_square(path)
    with Image.open(path) as image:
        return image.convert('RGB').resize((CANVAS, CANVAS), Image.Resampling.LANCZOS)


def _kept_regions(labels, figures):
    sizes = np.bincount(labels.ravel())[1:]
    if not sizes.size:
        return np.zeros(labels.shape, bool)
    largest = np.argsort(-sizes, kind='stable')[:figures]
    kept = largest[sizes[largest] * 10 >= sizes.max()] + 1
    return np.isin(labels, kept)


def black_background(rgb):
    return rgb[[0, 0, -1, -1], [0, -1, 0, -1]].max() < 16


def key(img, figures=1):
    rgb = np.asarray(img.convert('RGB'), np.float32)
    if black_background(rgb):
        labels, _ = ndimage.label(rgb.max(-1) < 12)
        border = np.unique(np.concatenate([labels[0], labels[-1], labels[:, 0], labels[:, -1]]))
        a = (~np.isin(labels, border[border > 0])).astype(np.float32)
        a = ndimage.uniform_filter(a, 3)
        return np.dstack([rgb, a * 255]).round().astype(np.uint8)
    a = np.clip((np.linalg.norm(rgb - MAGENTA, axis=-1) - 60) / 70, 0, 1)
    labels, n = ndimage.label(a > 0.5)
    if n > 1:
        a[(labels > 0) & ~_kept_regions(labels, figures)] = 0
    safe = np.maximum(a, 1e-3)[..., None]
    color = np.clip((rgb - (1 - a[..., None]) * MAGENTA) / safe, 0, 255)
    return np.dstack([color, a * 255]).round().astype(np.uint8)


def clean_keyed(rgba, figures=1):
    labels, _ = ndimage.label(rgba[..., 3] > 127)
    kept = _kept_regions(labels, figures)
    allowed = ndimage.binary_dilation(kept, structure=np.ones((3, 3), bool), iterations=6)
    stray = (rgba[..., 3] > 0) & ~allowed
    result = rgba.copy()
    result[stray, 3] = 0
    return result, int(stray.sum())


def despill_edge(rgba):
    opaque = rgba[..., 3] > 0
    band = opaque & (ndimage.distance_transform_edt(opaque) <= DESPILL_BAND)
    rgb = rgba[..., :3].astype(np.int16)
    spill = np.where(band, np.maximum(np.minimum(rgb[..., 0], rgb[..., 2]) - rgb[..., 1], 0), 0)
    result = rgba.copy()
    result[..., 0] = rgb[..., 0] - spill
    result[..., 2] = rgb[..., 2] - spill
    return result


def keyed(path, *, figures=1, return_stray=False, despill=False):
    validate_square(path)
    with Image.open(path) as image:
        resized = image.resize((CANVAS, CANVAS), Image.Resampling.LANCZOS)
        rgba, stray = clean_keyed(key(resized, figures), figures)
        if despill and not black_background(np.asarray(resized.convert('RGB'), np.float32)):
            rgba = despill_edge(rgba)
        return (rgba, stray) if return_stray else rgba


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


def place(rgba, frame_size, scale, box, offset=None, source_maximum=None):
    fw, fh = frame_size
    source_maximum = max(fw, fh) if source_maximum is None else source_maximum
    size = round(source_maximum * scale)
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
