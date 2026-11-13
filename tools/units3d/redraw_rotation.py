from __future__ import annotations

import io
import json
import math
from pathlib import Path

import numpy as np
from PIL import Image

from tools.hd_assets import read_pack
from tools.units3d.redraw_common import InputError, ROOT


UNITS = ['UNIT_QUAD', 'UNIT_TRIKE', 'UNIT_RAIDER', 'UNIT_LAUNCHER', 'UNIT_DEVIATOR', 'UNIT_SONICTANK', 'UNIT_MCV',
         'UNIT_TANKBASE', 'UNIT_TANKTOP', 'UNIT_SIEGEBASE', 'UNIT_SIEGETOP', 'UNIT_DEVASTATOR', 'UNIT_HARVESTER',
         'UNIT_SOLDIER', 'UNIT_SOLDIERS', 'UNIT_TROOPER', 'UNIT_TROOPERS', 'UNIT_SABOTEUR', 'UNIT_SINGLEFREMEN',
         'UNIT_TRIPLEFREMEN']
INFANTRY = ('UNIT_SOLDIER', 'UNIT_SOLDIERS', 'UNIT_TROOPER', 'UNIT_TROOPERS', 'UNIT_SABOTEUR', 'UNIT_SINGLEFREMEN',
            'UNIT_TRIPLEFREMEN')
BLOCK_OF = {'UNIT_SOLDIERS': 'UNIT_SOLDIER', 'UNIT_TROOPERS': 'UNIT_TROOPER', 'UNIT_TRIPLEFREMEN': 'UNIT_SINGLEFREMEN'}
CLASSIC = 'resources/bin/data/sdl_data.dat'
OLD_HD = 'tools/units3d/data/sdl_data_hd4_source.dat'
CONTRACT = 'docs/units/unit_contract.json'
THETA = math.radians(63)
SIZE_LIMIT = 0.05
MIDDLE_LIMIT = 4.0


def silhouette(cell):
    if cell[..., 3].min() < 255:
        return cell[..., 3] > 0
    return ~np.all(cell[..., :3] == cell[0, 0, :3], -1)


def cells(atlas, cols, rows):
    fh, fw = atlas.shape[0] // rows, atlas.shape[1] // cols
    return fw, fh, {(r, k): silhouette(atlas[r * fh:(r + 1) * fh, k * fw:(k + 1) * fw])
                    for r in range(rows) for k in range(cols)}


def area_by_direction(atlas, cols, rows):
    fw, fh, masks = cells(atlas, cols, rows)
    return [float(np.median([masks[r, k].sum() / (fw * fh) for r in range(rows)])) for k in range(cols)]


def normalised(values):
    median = float(np.median(values))
    return [value / median for value in values]


def size_measurements(new_area, reference_areas):
    deviations = [normalised([math.sqrt(new_area[k] / reference[k]) for k in range(len(new_area))])
                  for reference in reference_areas]
    combined = normalised([math.exp(sum(math.log(deviation[k]) for deviation in deviations) / len(deviations))
                           for k in range(len(new_area))])
    result = []
    for k in range(len(new_area)):
        agree = sum(abs(deviation[k] - 1) >= SIZE_LIMIT and (deviation[k] - 1) * (combined[k] - 1) > 0
                    for deviation in deviations)
        flag = 'size' if abs(combined[k] - 1) >= SIZE_LIMIT and agree >= 2 else '-'
        result.append({
            'classic': deviations[0][k],
            'old': deviations[1][k],
            'block': deviations[2][k],
            'combined': combined[k],
            'agree': agree,
            'flag': flag,
        })
    return result


def block_areas(block):
    length, width, height = block
    return [length * width * math.sin(THETA) + math.cos(THETA) * (
        length * height * abs(math.cos(math.radians(45 * k))) + width * height * abs(math.sin(math.radians(45 * k))))
        for k in range(8)]


def middle_from_boxes(boxes):
    values = [(box[1] + box[3]) / 2 for box in boxes if box is not None]
    return float(np.median(values))


def middle_from_cells(cell_masks):
    boxes = []
    for mask in cell_masks:
        ys, xs = np.nonzero(mask)
        if len(xs):
            boxes.append((int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1))
    return middle_from_boxes(boxes)


def middle_measurement(new_cells, classic_cells):
    new_height = new_cells[0].shape[0]
    classic_height = classic_cells[0].shape[0]
    new_middle = middle_from_cells(new_cells)
    classic_middle = middle_from_cells(classic_cells) * new_height / classic_height
    difference = new_middle - classic_middle
    flag = 'middle' if abs(difference) >= MIDDLE_LIMIT else '-'
    return new_middle, classic_middle, difference, flag


def _read_atlases(path, required_names):
    path = Path(path)
    try:
        entries = read_pack(path)
    except (OSError, ValueError) as exc:
        raise InputError(f'{path}: {exc}') from exc
    found = {}
    wanted = set(required_names)
    try:
        for entry in entries:
            if entry.name in wanted:
                found[entry.name] = np.asarray(Image.open(io.BytesIO(entry.payload)).convert('RGBA'))
    except (OSError, ValueError) as exc:
        raise InputError(f'{path}: {exc}') from exc
    missing = [name for name in required_names if name not in found]
    if missing:
        raise InputError(f'{path}: missing entries {", ".join(missing)}')
    return found


def _read_contract():
    path = ROOT / CONTRACT
    try:
        data = json.loads(path.read_text(encoding='utf-8'))
    except (OSError, ValueError) as exc:
        raise InputError(f'{path}: {exc}') from exc
    return {entry['name']: entry for entry in data['entries']}


def _block(name):
    unit_name = BLOCK_OF.get(name, name)
    path = ROOT / 'tools/units3d/units' / unit_name / 'unit.json'
    try:
        data = json.loads(path.read_text(encoding='utf-8'))
        return data['block']
    except (OSError, ValueError, KeyError) as exc:
        raise InputError(f'{path}: {exc}') from exc


def run(args):
    new = _read_atlases(args.pack, UNITS)
    classic = _read_atlases(ROOT / CLASSIC, UNITS)
    old = _read_atlases(ROOT / OLD_HD, UNITS)
    contract = _read_contract()
    print('unit\tk\tclassic\told\tblock\tcombined\tagree\tflag')
    for name in UNITS:
        cols, rows = contract[name]['columns'], contract[name]['rows']
        area = area_by_direction(new[name], cols, rows)
        references = [area_by_direction(classic[name], cols, rows), area_by_direction(old[name], cols, rows),
                      block_areas(_block(name))]
        for k, measurement in enumerate(size_measurements(area, references)):
            print(f'{name}\t{k}\t{measurement["classic"]:.3f}\t{measurement["old"]:.3f}\t'
                  f'{measurement["block"]:.3f}\t{measurement["combined"]:.3f}\t{measurement["agree"]}\t'
                  f'{measurement["flag"]}')
    print('unit\tmiddle_px\tclassic_px\tdiff_px\tflag')
    for name in INFANTRY:
        cols, rows = contract[name]['columns'], contract[name]['rows']
        new_cells = list(cells(new[name], cols, rows)[2].values())
        classic_cells = list(cells(classic[name], cols, rows)[2].values())
        new_middle, classic_middle, difference, flag = middle_measurement(new_cells, classic_cells)
        print(f'{name}\t{new_middle:.1f}\t{classic_middle:.1f}\t{difference:+.1f}\t{flag}')
    return 0
