from __future__ import annotations

import itertools
import math
from pathlib import Path

import numpy as np
from PIL import Image

from tools.units3d.redraw_common import bbox, frame_input, keyed


CANVAS = 1024
PAIRS = ((0, 4), (1, 3), (5, 7))
T0 = math.radians(36)
T1 = math.radians(63)
RATIO_HEADER = "k\told w×h\tpred h/w\tcand\tw\th\th/w"


def _crop(alpha):
    x0, y0, x1, y1 = bbox(alpha)
    return Image.fromarray(alpha[y0:y1, x0:x1])


def _mirror_iou(first, second):
    second = second.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    size = ((first.width + second.width) // 2, (first.height + second.height) // 2)
    a = np.asarray(first.resize(size)) > 127
    b = np.asarray(second.resize(size)) > 127
    union = np.logical_or(a, b).sum()
    return float(np.logical_and(a, b).sum() / union) if union else 1.0


def _frame_data(unit, record):
    k = record['k']
    with frame_input(record, unit.pack_path):
        old = unit.old_frame('body', record)[..., 3]
        x0, y0, x1, y1 = bbox(old)
    old_width, old_height = x1 - x0, y1 - y0
    estimate = unit.data['height_estimate']
    depth = (old_height - estimate * math.cos(T0)) / math.sin(T0)
    predicted = (depth * math.sin(T1) + estimate * math.cos(T1)) / old_width
    attempts = {}
    for key_name, value in record['attempts'].items():
        path = unit.path(value)
        with frame_input(record, path):
            rgba = keyed(path, figures=unit.data.get('figures', 1))
            cx0, cy0, cx1, cy1 = bbox(rgba[..., 3])
        width, height = cx1 - cx0, cy1 - cy0
        attempts[key_name] = {
            'width': width,
            'height': height,
            'ratio': height / width,
            'width_ratio': width / (old_width * CANVAS / unit.maximum),
            'angle_error': abs(height / width - predicted),
            'silhouette': _crop(rgba[..., 3]),
        }
    return {
        'old_width': old_width,
        'old_height': old_height,
        'predicted': predicted,
        'old_silhouette': _crop(old),
        'attempts': attempts,
    }


def _report_row(row, records, frame_data):
    lines = [f'## row {row}', RATIO_HEADER]
    mirror_cache = {}
    for record in records:
        k = record['k']
        info = frame_data[k]
        for attempt, candidate in info['attempts'].items():
            lines.append(
                f"{k}\t{info['old_width']}×{info['old_height']} "
                f"({info['old_height'] / info['old_width']:.2f})\t"
                f"{info['predicted']:.2f}\t{attempt}\t"
                f"{candidate['width']}\t{candidate['height']}\t"
                f"{candidate['ratio']:.2f}"
            )

    def old_iou(p, q):
        return _mirror_iou(
            frame_data[p]['old_silhouette'], frame_data[q]['old_silhouette']
        )

    def candidate_iou(p, p_key, q, q_key):
        key = (p, p_key, q, q_key)
        if key not in mirror_cache:
            mirror_cache[key] = _mirror_iou(
                frame_data[p]['attempts'][p_key]['silhouette'],
                frame_data[q]['attempts'][q_key]['silhouette'],
            )
        return mirror_cache[key]

    lines.append(
        'old mirror IoU '
        + str({f'{p}-{q}': round(old_iou(p, q), 3) for p, q in PAIRS})
    )
    for p, q in PAIRS:
        scores = {
            f'{a}{b}': round(candidate_iou(p, a, q, b), 3)
            for a in frame_data[p]['attempts']
            for b in frame_data[q]['attempts']
        }
        lines.append(f'{p}-{q} {scores}')

    for record in records:
        k = record['k']
        scores = {
            attempt: (
                round(candidate['width_ratio'], 3),
                round(candidate['angle_error'], 3),
            )
            for attempt, candidate in frame_data[k]['attempts'].items()
        }
        lines.append(f'{k} {scores}')

    combinations = []
    attempt_keys = [list(frame_data[k]['attempts']) for k in range(8)]
    for choice in itertools.product(*attempt_keys):
        widths = np.log(
            [frame_data[k]['attempts'][attempt]['width_ratio']
             for k, attempt in enumerate(choice)]
        )
        mirror = np.mean(
            [candidate_iou(p, choice[p], q, choice[q]) for p, q in PAIRS]
        )
        angle = np.mean(
            [frame_data[k]['attempts'][attempt]['angle_error']
             for k, attempt in enumerate(choice)]
        )
        combinations.append((widths.std(), -mirror, angle, ''.join(choice)))

    for index, name in ((0, 'width spread'), (1, 'mirror IoU'), (2, 'angle error')):
        best = sorted(combinations, key=lambda result: result[index])[:3]
        rendered = [
            (
                result[3],
                round(float(result[0]), 3),
                round(float(-result[1]), 3),
                round(float(result[2]), 3),
            )
            for result in best
        ]
        lines.append(f'{name} {rendered}')
    return lines


def render(unit):
    output = []
    records_by_row = {}
    for record in unit.frames:
        records_by_row.setdefault(record['row'], []).append(record)
    for row, records in records_by_row.items():
        frame_data = {record['k']: _frame_data(unit, record) for record in records}
        output.extend(_report_row(row, records, frame_data))
    return '\n'.join(output) + '\n'


def run(unit, args) -> int:
    output = render(unit)
    if args.out:
        Path(args.out).write_text(output, encoding='utf-8')
    print(output, end='')
    return 0
