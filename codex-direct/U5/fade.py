import hashlib
import io
import json
from pathlib import Path
import sys

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from tools.hd_assets import encode_png


BASE = ROOT / '.tmp' / 'out-c'
BUILD = BASE / 'build'
FINAL = BASE / 'final'
UNIT_PATH = ROOT / 'tools/units3d/units/UNIT_HARVESTER/unit.json'


def shadow_for(body, frame, rule):
    fw, fh = frame
    shadow = np.zeros_like(body)
    shadow[..., :3] = rule['rgb']
    shift = rule['shift']
    if shift < min(fw, fh):
        shadow[shift:, shift:, 3] = np.round(
            body[:fh - shift, :fw - shift, 3].astype(np.float32) * rule['alpha'] / 255
        ).astype(np.uint8)
    return shadow


def atlas_cell(atlas, row, k, fw, fh):
    return atlas[row * fh:(row + 1) * fh, k * fw:(k + 1) * fw]


def main():
    unit = json.loads(UNIT_PATH.read_text(encoding='utf-8'))
    frame = tuple(unit['frame'])
    fw, fh = frame
    rows = unit['rows']
    if frame != (320, 208) or rows != 4:
        raise ValueError(f'unexpected frame grid {frame} x {rows}')
    roles = unit['atlases']
    build_manifest = json.loads((BUILD / 'atlases.json').read_text(encoding='utf-8'))
    originals = {}
    manifest_entries = build_manifest['entries']
    for role in ('body', 'house_mask', 'shadow'):
        name = roles[role]
        entry = manifest_entries[name]
        with Image.open(BUILD / entry['file']) as image:
            originals[role] = np.asarray(image.convert('RGBA')).copy()
    finals = {role: pixels.copy() for role, pixels in originals.items()}
    rule = unit['shadow_rule']
    x = np.arange(fw, dtype=np.int16)[None, :]
    y = np.arange(fh, dtype=np.int16)[:, None]
    d = np.minimum(np.minimum(x, y), np.minimum(fw - 1 - x, fh - 1 - y))
    m = np.clip((d - 4) / 20, 0, 1)
    alpha_formula_violations = 0
    alpha_preserve_violations = 0
    zero_edge_violations = 0
    far_body_pixel_differences = 0
    body_rgb_differences = 0
    mask_alpha_formula_violations = 0
    mask_alpha_violations = 0
    row0_shadow_rebuild_mismatches = 0
    for k in range(8):
        h_alpha = atlas_cell(originals['body'], 0, k, fw, fh)[..., 3]
        expected_row0_shadow = shadow_for(atlas_cell(originals['body'], 0, k, fw, fh), frame, rule)
        actual_row0_shadow = atlas_cell(originals['shadow'], 0, k, fw, fh)
        row0_shadow_rebuild_mismatches += int(np.count_nonzero(np.any(expected_row0_shadow != actual_row0_shadow, axis=2)))
        for row in range(1, 4):
            body_before = atlas_cell(originals['body'], row, k, fw, fh)
            body_after = atlas_cell(finals['body'], row, k, fw, fh)
            preserve = (h_alpha > 0) | (d >= 24)
            faded_alpha = np.round(body_before[..., 3].astype(np.float32) * m).astype(np.uint8)
            alpha_after = np.where(preserve, body_before[..., 3], faded_alpha).astype(np.uint8)
            body_after[..., 3] = alpha_after
            alpha_formula_violations += int(np.count_nonzero(body_after[..., 3] != alpha_after))
            alpha_preserve_violations += int(np.count_nonzero(
                preserve & (body_after[..., 3] != body_before[..., 3])))
            zero_edge_violations += int(np.count_nonzero(
                (d < 4) & (h_alpha == 0) & (body_after[..., 3] != 0)))
            body_rgb_differences += int(np.count_nonzero(np.any(body_after[..., :3] != body_before[..., :3], axis=2)))
            far = d >= 24
            far_body_pixel_differences += int(np.count_nonzero(np.any(body_after[far] != body_before[far], axis=1)))
            mask_before = atlas_cell(originals['house_mask'], row, k, fw, fh)
            mask_after = atlas_cell(finals['house_mask'], row, k, fw, fh)
            expected_mask_alpha = np.minimum(mask_before[..., 3], alpha_after)
            mask_after[..., 3] = expected_mask_alpha
            mask_alpha_formula_violations += int(np.count_nonzero(mask_after[..., 3] != expected_mask_alpha))
            mask_alpha_violations += int(np.count_nonzero(mask_after[..., 3] > alpha_after))
            atlas_cell(finals['shadow'], row, k, fw, fh)[...] = shadow_for(body_after, frame, rule)
    row0_differences = {}
    for role in ('body', 'house_mask', 'shadow'):
        count = 0
        for k in range(8):
            before = atlas_cell(originals[role], 0, k, fw, fh)
            after = atlas_cell(finals[role], 0, k, fw, fh)
            count += int(np.count_nonzero(np.any(after != before, axis=2)))
        row0_differences[role] = count
    checks = {
        'row0_pixel_differences': row0_differences,
        'row0_shadow_rebuild_pixel_differences': row0_shadow_rebuild_mismatches,
        'rows1_3_alpha_formula_violations': alpha_formula_violations,
        'rows1_3_A_changed_where_H_positive_or_d_ge_24': alpha_preserve_violations,
        'rows1_3_A_nonzero_for_d_lt_4_and_H_zero': zero_edge_violations,
        'rows1_3_body_pixel_differences_at_d_ge_24': far_body_pixel_differences,
        'rows1_3_body_RGB_differences': body_rgb_differences,
        'rows1_3_mask_alpha_formula_violations': mask_alpha_formula_violations,
        'rows1_3_mask_alpha_above_body': mask_alpha_violations,
    }
    payloads = {}
    final_png_roundtrip_differences = 0
    for role in ('body', 'house_mask', 'shadow'):
        payloads[role] = encode_png(Image.fromarray(finals[role], 'RGBA'))
        with Image.open(io.BytesIO(payloads[role])) as image:
            saved = np.asarray(image.convert('RGBA'))
        final_png_roundtrip_differences += int(np.count_nonzero(np.any(saved != finals[role], axis=2)))
    checks['final_png_roundtrip_pixel_differences'] = final_png_roundtrip_differences
    failures = [name for name, value in checks.items()
                if (any(value.values()) if isinstance(value, dict) else value != 0)]
    log_lines = [f'{name}: {json.dumps(value, sort_keys=True)}' for name, value in checks.items()]
    if failures:
        log_lines.append('Q: ' + ', '.join(failures))
        log_path = BASE / 'fade.log'
        log_path.write_text('\n'.join(log_lines) + '\n', encoding='utf-8')
        with (ROOT / '.tmp/progress-c.md').open('a', encoding='utf-8') as stream:
            stream.write(f'Пункт 5 — Q: расхождение проверок {", ".join(failures)}; лог: .tmp/out-c/fade.log.\n')
        raise SystemExit('Q: fade validation failed; see .tmp/out-c/fade.log')
    if FINAL.exists():
        raise FileExistsError(f'refusing to overwrite {FINAL}')
    FINAL.mkdir()
    entries = {}
    for role in ('body', 'house_mask', 'shadow'):
        name = roles[role]
        filename = manifest_entries[name]['file']
        payload = payloads[role]
        (FINAL / filename).write_bytes(payload)
        entries[name] = {
            'file': filename,
            'sha256': hashlib.sha256(payload).hexdigest(),
            'size': [finals[role].shape[1], finals[role].shape[0]],
        }
    (FINAL / 'atlases.json').write_text(json.dumps({'entries': entries}, indent=2) + '\n', encoding='utf-8')
    log_lines.append('result: PASS')
    log_lines.append(f'final atlases: {FINAL.relative_to(ROOT)}')
    (BASE / 'fade.log').write_text('\n'.join(log_lines) + '\n', encoding='utf-8')
    with (ROOT / '.tmp/progress-c.md').open('a', encoding='utf-8') as stream:
        stream.write('Пункт 5 — fade завершён; все проверки PASS, атласы и atlases.json записаны в .tmp/out-c/final/; лог: .tmp/out-c/fade.log.\n')
    print('\n'.join(log_lines))


if __name__ == '__main__':
    main()
