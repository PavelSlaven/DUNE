"""House mask from the green recolour, shadow by the old pack's rule, and the three Devastator atlases.
usage: python -X utf8 atlas.py <recolour dir> <out dir>   (run from the repo root)"""
import hashlib
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

from common import S, CANVAS, FW, FH, CHOICE, old_boxes, pack_img, key, place

sys.path.insert(0, str(Path('tools').resolve()))
from hd_assets import encode_png  # noqa: E402

EDITS, OUT = Path(sys.argv[1]), Path(sys.argv[2])
OUT.mkdir(parents=True, exist_ok=True)
params = json.loads((S / 'g3/frames/params.json').read_text(encoding='utf-8'))
scale, offsets = params['scale'], {int(k): tuple(v) for k, v in params['offsets'].items()}
boxes = old_boxes()
SHARE, IOU = (0.29, 0.58), 0.97
SHADOW_SHIFT, SHADOW_ALPHA, SHADOW_RGB = 4, 46, (5, 4, 3)
old_hm, old_body = pack_img('HM_UNIT_DEVASTATOR'), pack_img('UNIT_DEVASTATOR')
atlases = {n: np.zeros((192, 8 * FW, 4), np.uint8) for n in ('UNIT_DEVASTATOR', 'HM_UNIT_DEVASTATOR', 'UNIT_DEVASTATOR_SHADOW')}
metrics, failed = ['k\tpick\tiou\tshare\told_share\tok'], []
for k in range(8):
    body = np.array(Image.open(S / f'g3/frames/k{k}.png'))
    on = body[..., 3] > 127
    edit = Image.open(EDITS / f'g3b_k{k}.png').convert('RGB').resize((CANVAS, CANVAS), Image.LANCZOS)
    edit_frame, _, _ = place(key(edit), k, scale, boxes, offsets[k])
    edit_on = edit_frame[..., 3] > 127
    iou = (on & edit_on).sum() / (on | edit_on).sum()
    rgb = np.asarray(edit, np.int16)
    green = (rgb[..., 1] - np.maximum(rgb[..., 0], rgb[..., 2])) >= 80
    white = np.dstack([np.full(green.shape + (3,), 255, np.uint8), green.astype(np.uint8) * 255])
    hm, _, _ = place(white, k, scale, boxes, offsets[k])
    hm[..., :3] = 255
    hm[..., 3] = np.round(hm[..., 3].astype(np.float32) * body[..., 3] / 255).astype(np.uint8)
    share = (hm[..., 3] > 127).sum() / on.sum()
    old_share = (old_hm[:FH, k * FW:(k + 1) * FW, 3] > 127).sum() / (old_body[:FH, k * FW:(k + 1) * FW, 3] > 127).sum()
    shadow = np.zeros_like(body)
    shadow[..., :3] = SHADOW_RGB
    shadow[SHADOW_SHIFT:, SHADOW_SHIFT:, 3] = np.round(body[:-SHADOW_SHIFT, :-SHADOW_SHIFT, 3].astype(np.float32) * SHADOW_ALPHA / 255).astype(np.uint8)
    ok = iou >= IOU and SHARE[0] <= share <= SHARE[1]
    if not ok:
        failed.append(k)
    metrics.append(f'{k}\t{CHOICE[k]}\t{iou:.3f}\t{share:.3f}\t{old_share:.3f}\t{ok}')
    for name, img in (('UNIT_DEVASTATOR', body), ('HM_UNIT_DEVASTATOR', hm), ('UNIT_DEVASTATOR_SHADOW', shadow)):
        atlases[name][:FH, k * FW:(k + 1) * FW] = img
entries = {}
for name, arr in atlases.items():
    data = encode_png(Image.fromarray(arr))
    (OUT / f'{name}.png').write_bytes(data)
    entries[name] = {'file': f'{name}.png', 'sha256': hashlib.sha256(data).hexdigest(), 'size': [arr.shape[1], arr.shape[0]]}
(OUT / 'atlases.json').write_text(json.dumps({'entries': entries}, indent=2), encoding='utf-8')
metrics.append(f'failed: {failed}' if failed else 'all directions pass')
(OUT / 'metrics.txt').write_text('\n'.join(metrics) + '\n', encoding='utf-8')
print('\n'.join(metrics))
sys.exit(1 if failed else 0)
