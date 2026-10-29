"""Build frames, house masks, shadows and validated unit atlases."""

import hashlib
import json
import sys

import numpy as np
from PIL import Image

from tools.hd_assets import encode_png
from tools.units3d.redraw_common import CANVAS, InputError, bbox, frame_name, key, keyed, place, prepare


def run(unit, args):
    output = args.output
    if output.exists() and (not output.is_dir() or any(output.iterdir())):
        raise InputError(f'{output}: output must be absent or empty')
    records = unit.frames
    boxes = {frame_name(f): bbox(unit.old_frame('body', f)[..., 3]) for f in records}
    raw = {frame_name(f): keyed(unit.path(f['attempts'][f['pick']])) for f in records}
    ratios = []
    for record in records:
        name = frame_name(record)
        x0, _, x1, _ = bbox(raw[name][..., 3])
        box = boxes[name]
        ratios.append((box[2] - box[0]) / ((x1 - x0) * unit.maximum / CANVAS))
    scale = float(np.median(ratios))
    has_mask = unit.atlases['house_mask'] is not None
    old_shares = {}
    if has_mask:
        for record in records:
            body = unit.old_frame('body', record)[..., 3] > 127
            mask = unit.old_frame('house_mask', record)[..., 3] > 127
            old_shares[frame_name(record)] = float(mask.sum() / body.sum())
        corridor = (min(old_shares.values()) - 0.05, max(old_shares.values()) + 0.05)
    else:
        corridor = None
    output.mkdir(parents=True, exist_ok=True)
    (output / 'frames').mkdir()
    atlases = {role: np.zeros_like(unit.image(unit.atlases['body']))
               for role, name in unit.atlases.items() if name is not None}
    params = {'scale': scale, 'frames': {}}
    metrics = ['row\tk\tpick\tiou\tshare\told_share\tok']
    failed = []
    fw, fh = unit.frame
    for record in records:
        name = frame_name(record)
        body, clipped, offset, moved = place(raw[name], unit.frame, scale, boxes[name])
        (output / 'frames' / f'{name}.png').write_bytes(encode_png(Image.fromarray(body)))
        params['frames'][name] = {'offset': list(offset), 'moved': list(moved)}
        reasons = []
        images = {'body': body}
        if has_mask:
            edit = prepare(unit.path(record['recolour']))
            edit_frame, edit_clipped, _, _ = place(key(edit), unit.frame, scale, boxes[name], offset)
            clipped = clipped or edit_clipped
            on, edit_on = body[..., 3] > 127, edit_frame[..., 3] > 127
            union = (on | edit_on).sum()
            iou = float((on & edit_on).sum() / union) if union else 1.0
            rgb = np.asarray(edit, np.int16)
            green = rgb[..., 1] - np.maximum(rgb[..., 0], rgb[..., 2]) >= 80
            white = np.dstack([np.full(green.shape + (3,), 255, np.uint8),
                               green.astype(np.uint8) * 255])
            mask, _, _, _ = place(white, unit.frame, scale, boxes[name], offset)
            mask[..., :3] = 255
            mask[..., 3] = np.round(mask[..., 3].astype(np.float32) * body[..., 3] / 255).astype(np.uint8)
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
        metrics.append(f"{record['row']}\t{record['k']}\t{record['pick']}\t{values}\t{ok}")
        if reasons:
            failed.append(name)
            print(f"{name}: {', '.join(reasons)}", file=sys.stderr)
    if corridor is None:
        metrics.append('corridor\t-\t-')
    else:
        metrics.append(f'corridor\t{corridor[0]:.5f}\t{corridor[1]:.5f}')
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
