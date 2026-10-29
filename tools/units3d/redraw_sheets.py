from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from tools.units3d.redraw_common import ROOT, InputError, flat, frame_name, keyed


TILE = 300
CAPTION = 30
LEFT_WIDTH = 230
ZOOM = 2
REF_LUM = 166 / 255
HOUSES = (
    ('Харконнен', (255, 0, 0)),
    ('Атрейдес', (0, 0, 255)),
    ('Ордос', (0, 255, 0)),
)
DIRECTIONS = (
    'восток', 'северо-восток', 'север', 'северо-запад',
    'запад', 'юго-запад', 'юг', 'юго-восток',
)
FONT_PATH = ROOT / 'resources/bin/data/PTSansNarrow-Regular.ttf'


def _image(path, mode):
    path = Path(path)
    if not path.is_file():
        raise InputError(f'{path}: image not found')
    try:
        with Image.open(path) as image:
            return image.convert(mode)
    except OSError as exc:
        raise InputError(f'{path}: {exc}') from exc


def _font():
    if not FONT_PATH.is_file():
        raise InputError(f'{FONT_PATH}: font not found')
    try:
        return ImageFont.truetype(str(FONT_PATH), 22)
    except OSError as exc:
        raise InputError(f'{FONT_PATH}: {exc}') from exc


def _tint(frame, mask, color):
    rgb = frame[..., :3].astype(np.float32)
    strength = mask[..., 3] / 255 * mask[..., :3].max(-1) / 255
    lum = (0.299 * rgb[..., 0] + 0.587 * rgb[..., 1] + 0.114 * rgb[..., 2]) / 128
    full = (strength >= 0.99) & (frame[..., 3] != 0)
    avg = lum[full].mean() if full.any() else REF_LUM
    colored = np.round(np.clip(np.array(color, np.float32) * lum[..., None]
                               * (REF_LUM / max(0.01, avg)), 0, 255))
    strength = np.where((strength > 0) & (frame[..., 3] != 0), strength, 0)[..., None]
    out = frame.copy()
    out[..., :3] = np.clip(rgb * (1 - strength) + colored * strength, 0, 255).astype(np.uint8)
    return out


def _attenuate_shadow(shadow):
    shadow = shadow.copy()
    shadow[..., 3] = np.round(shadow[..., 3] * 160 / 255).astype(np.uint8)
    return shadow


def _new_atlases(unit, directory):
    images = {}
    for role in ('body', 'house_mask', 'shadow'):
        name = unit.atlases[role]
        if name is None:
            images[role] = None
            continue
        path = Path(directory) / f'{name}.png'
        images[role] = np.asarray(_image(path, 'RGBA'))
    return images


def _frame_from_atlas(atlas, role, unit, record, path):
    fw, fh = unit.frame
    x, y = record['k'] * fw, record['row'] * fh
    frame = atlas[y:y + fh, x:x + fw]
    if frame.shape[:2] != (fh, fw):
        raise InputError(f'{path}: frame r{record["row"]}k{record["k"]} is outside atlas')
    return frame.copy()


def _layers(body, mask, shadow, color):
    if mask is not None:
        body = _tint(body, mask, color)
    result = []
    if shadow is not None:
        result.append(Image.fromarray(_attenuate_shadow(shadow)))
    result.append(Image.fromarray(body))
    return result


def contact(unit, args):
    records = unit.frames
    if not records:
        raise InputError('frames: expected at least one frame')
    inputs = Path(args.inputs)
    columns = 2 + max(len(record['attempts']) for record in records)
    sheet = Image.new('RGB', (columns * TILE, len(records) * (TILE + CAPTION)), (30, 30, 30))
    draw = ImageDraw.Draw(sheet)
    font = _font()
    for index, record in enumerate(records):
        name = frame_name(record)
        y = index * (TILE + CAPTION)
        paths = (
            inputs / f'old_{name}.png',
            inputs / f'guide_{name}.png',
        )
        labels = (f'{name}: старый кадр', f'{name}: направляющая')
        attempts = list(record['attempts'].items())
        for attempt_name, value in attempts:
            paths += (unit.path(value),)
            labels += (f'{name}: попытка {attempt_name}',)
        for column, (path, label) in enumerate(zip(paths, labels)):
            draw.text((column * TILE + 8, y + 4), label, fill='white', font=font)
            if column < 2:
                image = _image(path, 'RGB')
            else:
                if not path.is_file():
                    raise InputError(f'{path}: image not found')
                try:
                    image = flat(keyed(path))
                except OSError as exc:
                    raise InputError(f'{path}: {exc}') from exc
            sheet.paste(image.resize((TILE, TILE), Image.Resampling.LANCZOS),
                        (column * TILE, y + CAPTION))
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output)
    return 0


def _paste_layers(sheet, layers, position, size=None):
    x, y = position
    for layer in layers:
        if size is not None:
            layer = layer.resize(size, Image.Resampling.LANCZOS)
        sheet.alpha_composite(layer, (x, y))


def sheet(unit, args):
    row = args.row
    if not isinstance(row, int) or not 0 <= row < unit.rows:
        raise InputError(f'row: expected integer from 0 to {unit.rows - 1}, got {row}')
    records = {record['k']: record for record in unit.frames if record['row'] == row}
    if set(records) != set(range(8)):
        missing = next(k for k in range(8) if k not in records)
        raise InputError(f'r{row}k{missing}: missing frame')

    atlases = _new_atlases(unit, args.atlases)
    fw, fh = unit.frame
    cw, ch = fw * ZOOM, fh * ZOOM
    panel_height = 330
    width = LEFT_WIDTH + 8 * cw
    height = 40 + 6 * ch + panel_height
    image = Image.new('RGBA', (width, height))
    sand = Image.fromarray(unit.image('TERRAIN_SAND'))
    for x in range(0, width, sand.width):
        for y in range(0, height, sand.height):
            image.paste(sand, (x, y))

    draw = ImageDraw.Draw(image)
    font = _font()
    draw.rectangle((0, 0, width, 40), fill=(30, 30, 30))
    draw.text((10, 8), 'Масштаб ×2', fill='white', font=font)
    for k, direction in enumerate(DIRECTIONS):
        draw.text((LEFT_WIDTH + k * cw + 10, 8), f'k{k} {direction}', fill='white', font=font)

    sprite_rows = []
    for house, color in HOUSES:
        for is_new in (False, True):
            label = 'новый, 63°' if is_new else 'старый'
            sprite_rows.append((house, color, is_new, label))
    for sprite_row, (house, color, is_new, label) in enumerate(sprite_rows):
        y = 40 + sprite_row * ch
        draw.text((10, y + ch // 2 - 24), f'{house}\n{label}', fill='white', font=font,
                  stroke_width=2, stroke_fill='black')
        for k in range(8):
            record = records[k]
            if is_new:
                body_path = Path(args.atlases) / f'{unit.atlases["body"]}.png'
                body = _frame_from_atlas(atlases['body'], 'body', unit, record, body_path)
                mask = None if atlases['house_mask'] is None else _frame_from_atlas(
                    atlases['house_mask'], 'house_mask', unit, record,
                    Path(args.atlases) / f'{unit.atlases["house_mask"]}.png')
                shadow = None if atlases['shadow'] is None else _frame_from_atlas(
                    atlases['shadow'], 'shadow', unit, record,
                    Path(args.atlases) / f'{unit.atlases["shadow"]}.png')
            else:
                body = unit.old_frame('body', record)
                mask = None if unit.atlases['house_mask'] is None else unit.old_frame('house_mask', record)
                shadow = None if unit.atlases['shadow'] is None else unit.old_frame('shadow', record)
            layers = _layers(body, mask, shadow, color)
            _paste_layers(image, layers, (LEFT_WIDTH + k * cw, y), (cw, ch))

    panel_y = 40 + 6 * ch
    draw.text((10, panel_y + 20), 'Игровой масштаб:\nслева старый,\nсправа новый', fill='white', font=font,
              stroke_width=2, stroke_fill='black')
    building = unit.data['sheet_building']
    building_name = building['name']
    building_width, building_height = building['size']
    old_building = unit.image(building_name)[:building_height, :building_width].copy()
    if old_building.shape[:2] != (building_height, building_width):
        raise InputError(f'{building_name}: image is smaller than requested crop')
    building_shadow_name = f'{building_name}_SHADOW'
    entry_names = {entry.name for entry in unit.entries}
    old_building_shadow = None
    if building_shadow_name in entry_names:
        old_building_shadow = unit.image(building_shadow_name)[:building_height, :building_width].copy()
        if old_building_shadow.shape[:2] != (building_height, building_width):
            raise InputError(f'{building_shadow_name}: image is smaller than requested crop')
    if old_building_shadow is not None:
        _paste_layers(image, [Image.fromarray(_attenuate_shadow(old_building_shadow))],
                      (LEFT_WIDTH, panel_y + 40))
    _paste_layers(image, [Image.fromarray(old_building)], (LEFT_WIDTH, panel_y + 40))

    x = LEFT_WIDTH + building_width + 16
    for is_new in (False, True):
        for k in (6, 7, 0, 1):
            record = records[k]
            if is_new:
                body = _frame_from_atlas(
                    atlases['body'], 'body', unit, record,
                    Path(args.atlases) / f'{unit.atlases["body"]}.png')
                mask = None if atlases['house_mask'] is None else _frame_from_atlas(
                    atlases['house_mask'], 'house_mask', unit, record,
                    Path(args.atlases) / f'{unit.atlases["house_mask"]}.png')
                shadow = None if atlases['shadow'] is None else _frame_from_atlas(
                    atlases['shadow'], 'shadow', unit, record,
                    Path(args.atlases) / f'{unit.atlases["shadow"]}.png')
            else:
                body = unit.old_frame('body', record)
                mask = None if unit.atlases['house_mask'] is None else unit.old_frame('house_mask', record)
                shadow = None if unit.atlases['shadow'] is None else unit.old_frame('shadow', record)
            _paste_layers(image, _layers(body, mask, shadow, HOUSES[0][1]),
                          (x, panel_y + 90))
            x += fw
        x += 60

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    image.convert('RGB').save(output)
    print(f'saved {image.size}')
    return 0


def run(unit, args):
    if args.command == 'contact':
        return contact(unit, args)
    if args.command == 'sheet':
        return sheet(unit, args)
    raise InputError(f'unsupported sheets command {args.command}')
