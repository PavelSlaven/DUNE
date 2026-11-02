"""Build frames, house masks, shadows and validated unit atlases."""

import hashlib
import json
import sys

import numpy as np
from PIL import Image

from tools.hd_assets import encode_png
from tools.units3d.redraw_common import CANVAS, InputError, bbox, clean_keyed, frame_input, frame_name, key, keyed, place, prepare


def _fit_scale(scale_median, fits):
    minimum = 0.8 * scale_median
    low, high = 0, int(np.ceil((scale_median - minimum) / 0.001))
    if scale_median - 0.001 * high < minimum:
        high -= 1
    while low < high:
        middle = (low + high) // 2
        candidate = scale_median - 0.001 * middle
        if fits(candidate):
            high = middle
        else:
            low = middle + 1
    return scale_median - 0.001 * low


def run(unit, args):
    output = args.output
    if output.exists() and (not output.is_dir() or any(output.iterdir())):
        raise InputError(f'{output}: output must be absent or empty')
    records = unit.frames
    figures = unit.data.get('figures', 1)
    despill = unit.data.get('despill', True)
    boxes = {}
    for record in records:
        name = frame_name(record)
        with frame_input(record, unit.pack_path):
            boxes[name] = unit.output_box(bbox(unit.old_frame('body', record)[..., 3]))
    prepared = {}
    raw = {}
    cleaned = {}
    for record in records:
        name = frame_name(record)
        attempt_path = unit.path(record['attempts'][record['pick']])
        with frame_input(record, attempt_path):
            prepared[name] = keyed(attempt_path, figures=figures, return_stray=True)
            bbox(prepared[name][0][..., 3])
            if despill:
                cleaned[name] = keyed(attempt_path, figures=figures, despill=True)
        raw[name] = prepared[name][0]
    ratios = []
    for record in records:
        if 'offset_from' in record:
            continue
        name = frame_name(record)
        attempt_path = unit.path(record['attempts'][record['pick']])
        with frame_input(record, attempt_path):
            x0, _, x1, _ = bbox(raw[name][..., 3])
        box = boxes[name]
        ratios.append((box[2] - box[0]) / ((x1 - x0) * unit.maximum / CANVAS))
    scale_median = float(np.median(ratios))

    def frame_scale(record, scale):
        return scale * record.get('scale_factor', 1)

    has_mask = unit.atlases['house_mask'] is not None
    recolours = {}
    if has_mask:
        for record in records:
            recolour_path = unit.path(record['recolour'])
            with frame_input(record, recolour_path):
                edit = prepare(recolour_path)
                cleaned_edit, _ = clean_keyed(key(edit, figures), figures)
                bbox(cleaned_edit[..., 3])
            recolours[frame_name(record)] = edit, cleaned_edit

    placement_records = sorted(records, key=lambda record: 'offset_from' in record)
    offset_shift = unit.data.get('offset_shift', (0, 0))

    def place_frame(rgba, scale, box, offset=None):
        if offset is not None:
            return place(rgba, unit.frame, scale, box, offset, source_maximum=unit.maximum)
        frame = place(rgba, unit.frame, scale, box, source_maximum=unit.maximum)
        base_offset = frame[2]
        final_offset = (base_offset[0] + offset_shift[0], base_offset[1] + offset_shift[1])
        if final_offset == base_offset:
            return frame
        shifted, clipped, _, _ = place(
            rgba, unit.frame, scale, box, final_offset, source_maximum=unit.maximum,
        )
        return shifted, clipped, final_offset, frame[3]

    def place_bodies(candidate):
        placed = {}
        for record in placement_records:
            name = frame_name(record)
            offset = None
            if 'offset_from' in record:
                source_name = f"r{record['offset_from']}k{record['k']}"
                offset = placed[source_name][2]
            attempt_path = unit.path(record['attempts'][record['pick']])
            with frame_input(record, attempt_path):
                placed[name] = place_frame(
                    raw[name], frame_scale(record, candidate), boxes[name], offset,
                )
        return placed

    def fits(candidate):
        placed = place_bodies(candidate)
        for record in records:
            name = frame_name(record)
            _, clipped, offset, _ = placed[name]
            if clipped:
                return False
            if has_mask:
                with frame_input(record, unit.path(record['recolour'])):
                    _, clipped, _, _ = place(
                        recolours[name][1], unit.frame, frame_scale(record, candidate), boxes[name], offset,
                        source_maximum=unit.maximum,
                    )
                if clipped:
                    return False
        return True

    scale = unit.data.get('scale', scale_median)
    if scale == 'fit':
        scale = _fit_scale(scale_median, fits)
    placed = place_bodies(scale)
    old_shares = {}
    if has_mask:
        for record in records:
            body = unit.old_frame('body', record)[..., 3] > 127
            mask = unit.old_frame('house_mask', record)[..., 3] > 127
            old_shares[frame_name(record)] = float(mask.sum() / body.sum())
        corridor = unit.data.get('share_corridor',
                                 (min(old_shares.values()) - 0.05, max(old_shares.values()) + 0.05))
        corridor_source = 'set' if 'share_corridor' in unit.data else 'old'
    else:
        corridor = None
    output.mkdir(parents=True, exist_ok=True)
    (output / 'frames').mkdir()
    atlas_width, atlas_height = unit.atlas_size
    atlases = {role: np.zeros((atlas_height, atlas_width, 4), np.uint8)
               for role, name in unit.atlases.items() if name is not None}
    params = {'scale': scale, 'scale_median': scale_median, 'frames': {}}
    metrics = ['row\tk\tpick\tiou\tshare\told_share\tstray\tok']
    failed = []
    fw, fh = unit.frame
    for record in records:
        name = frame_name(record)
        body, clipped, offset, moved = placed[name]
        colour = body
        if despill:
            with frame_input(record, unit.path(record['attempts'][record['pick']])):
                colour = place(
                    cleaned[name], unit.frame, frame_scale(record, scale), boxes[name], offset,
                    source_maximum=unit.maximum,
                )[0]
        (output / 'frames' / f'{name}.png').write_bytes(encode_png(Image.fromarray(colour)))
        params['frames'][name] = {'offset': list(offset), 'moved': list(moved)}
        reasons = []
        images = {'body': colour}
        if has_mask:
            recolour_path = unit.path(record['recolour'])
            with frame_input(record, recolour_path):
                edit, cleaned_edit = recolours[name]
                edit_frame, edit_clipped, _, _ = place(
                    cleaned_edit, unit.frame, frame_scale(record, scale), boxes[name], offset,
                    source_maximum=unit.maximum,
                )
            clipped = clipped or edit_clipped
            on, edit_on = body[..., 3] > 127, edit_frame[..., 3] > 127
            union = (on | edit_on).sum()
            iou = float((on & edit_on).sum() / union) if union else 1.0
            rgb = np.asarray(edit, np.int16)
            green = rgb[..., 1] - np.maximum(rgb[..., 0], rgb[..., 2]) >= 80
            white = np.dstack([np.full(green.shape + (3,), 255, np.uint8),
                               green.astype(np.uint8) * 255])
            mask, _, _, _ = place(
                white, unit.frame, frame_scale(record, scale), boxes[name], offset,
                source_maximum=unit.maximum,
            )
            mask[..., :3] = 255
            mask[..., 3] = np.round(mask[..., 3].astype(np.float32) * body[..., 3] / 255).astype(np.uint8)
            if 'red_fill' in unit.data:
                body_rgb = body[..., :3].astype(np.int16)
                red = body_rgb[..., 0] - np.maximum(body_rgb[..., 1], body_rgb[..., 2]) >= unit.data['red_fill']
                mask[red, 3] = body[red, 3]
            share = float((mask[..., 3] > 127).sum() / on.sum()) if on.any() else 0.0
            if iou < 0.97:
                reasons.append('iou')
            if not corridor[0] <= share <= corridor[1]:
                reasons.append('share')
            values = f'{iou:.3f}\t{share:.3f}\t{old_shares[name]:.3f}'
            images['house_mask'] = mask
        else:
            values = '-\t-\t-'
        if clipped:
            reasons.append('clipped')
        if unit.atlases['shadow'] is not None:
            rule = unit.data['shadow_rule']
            shadow = np.zeros_like(body)
            shadow[..., :3] = rule['rgb']
            shift = rule['shift']
            if shift < min(fw, fh):
                shadow[shift:, shift:, 3] = np.round(
                    body[:fh - shift, :fw - shift, 3].astype(np.float32) * rule['alpha'] / 255
                ).astype(np.uint8)
            images['shadow'] = shadow
        for role, image in images.items():
            x, y = record['k'] * fw, record['row'] * fh
            atlases[role][y:y + fh, x:x + fw] = image
        ok = not reasons
        metrics.append(f"{record['row']}\t{record['k']}\t{record['pick']}\t{values}\t{prepared[name][1]}\t{ok}")
        if reasons:
            failed.append(name)
            print(f"{name}: {', '.join(reasons)}", file=sys.stderr)
    if corridor is None:
        metrics.append('corridor\t-\t-')
    else:
        metrics.append(f'corridor\t{corridor[0]:.5f}\t{corridor[1]:.5f}\t{corridor_source}')
    metrics.append(f"failed: {', '.join(failed)}" if failed else 'all frames pass')
    text = '\n'.join(metrics) + '\n'
    (output / 'params.json').write_text(json.dumps(params, indent=2) + '\n', encoding='utf-8')
    (output / 'metrics.txt').write_text(text, encoding='utf-8')
    print(f'scale {scale:.4f}')
    print(text, end='')
    if failed:
        return 1
    entries = {}
    for role, pixels in atlases.items():
        name = unit.atlases[role]
        payload = encode_png(Image.fromarray(pixels))
        filename = f'{name}.png'
        (output / filename).write_bytes(payload)
        entries[name] = {'file': filename, 'sha256': hashlib.sha256(payload).hexdigest(),
                         'size': [pixels.shape[1], pixels.shape[0]]}
    (output / 'atlases.json').write_text(json.dumps({'entries': entries}, indent=2) + '\n', encoding='utf-8')
    return 0
