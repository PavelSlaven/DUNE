"""Old and new Devastator, 8 directions, in three House colours with shadows, and both next to the heavy factory at game scale.
usage: python -X utf8 sheet.py <atlas dir> <out png>   (run from the repo root)"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from common import FW, FH, pack_img

ATLAS, OUT = Path(sys.argv[1]), Path(sys.argv[2])
REF_LUM, SHADOW_TRANS, Z, LW = 166 / 255, 160, 2, 230
HOUSES = [('Харконнен', (255, 0, 0)), ('Атрейдес', (0, 0, 255)), ('Ордос', (0, 255, 0))]
DIRS = ['восток', 'северо-восток', 'север', 'северо-запад', 'запад', 'юго-запад', 'юг', 'юго-восток']
font = ImageFont.truetype('resources/bin/data/PTSansNarrow-Regular.ttf', 22)


def tint(frame, mask, color):
    rgb = frame[..., :3].astype(np.float32)
    strength = mask[..., 3] / 255 * mask[..., :3].max(-1) / 255
    lum = (0.299 * rgb[..., 0] + 0.587 * rgb[..., 1] + 0.114 * rgb[..., 2]) / 128
    full = (strength >= 0.99) & (frame[..., 3] != 0)
    avg = lum[full].mean() if full.any() else REF_LUM
    colored = np.round(np.clip(np.array(color, np.float32) * lum[..., None] * (REF_LUM / max(0.01, avg)), 0, 255))
    s = np.where((strength > 0) & (frame[..., 3] != 0), strength, 0)[..., None]
    out = frame.copy()
    out[..., :3] = np.clip(rgb * (1 - s) + colored * s, 0, 255).astype(np.uint8)
    return out


def frames(load):
    body, hm, shadow = (load(n) for n in ('UNIT_DEVASTATOR', 'HM_UNIT_DEVASTATOR', 'UNIT_DEVASTATOR_SHADOW'))
    shadow = shadow.copy()
    shadow[..., 3] = np.round(shadow[..., 3] * SHADOW_TRANS / 255).astype(np.uint8)
    cut = lambda a, k: a[:FH, k * FW:(k + 1) * FW]
    return lambda k, color: (Image.fromarray(cut(shadow, k)), Image.fromarray(tint(cut(body, k), cut(hm, k), color)))


sets = [('старый', frames(pack_img)), ('новый, 63°', frames(lambda n: np.array(Image.open(ATLAS / f'{n}.png').convert('RGBA'))))]
cw, ch = FW * Z, FH * Z
panel_h = 330
sheet = Image.new('RGBA', (LW + 8 * cw, 40 + 6 * ch + panel_h))
sand = Image.fromarray(pack_img('TERRAIN_SAND'))
for x in range(0, sheet.width, sand.width):
    for y in range(0, sheet.height, sand.height):
        sheet.paste(sand, (x, y))
d = ImageDraw.Draw(sheet)
d.rectangle((0, 0, sheet.width, 40), fill=(30, 30, 30))
d.text((10, 8), '×2', fill='white', font=font)
for k, name in enumerate(DIRS):
    d.text((LW + k * cw + 10, 8), f'k{k} {name}', fill='white', font=font)
row = 0
for house, color in HOUSES:
    for label, get in sets:
        y = 40 + row * ch
        d.text((10, y + ch // 2 - 24), f'{house}\n{label}', fill='white', font=font, stroke_width=2, stroke_fill='black')
        for k in range(8):
            for layer in get(k, color):
                sheet.alpha_composite(layer.resize((cw, ch), Image.LANCZOS), (LW + k * cw, y))
        row += 1
y = 40 + 6 * ch
d.text((10, y + 20), 'масштаб игры:\nслева старый,\nсправа новый', fill='white', font=font, stroke_width=2, stroke_fill='black')
factory = pack_img('BUILD_HEAVYFACTORY')[:256, :384]
factory_shadow = pack_img('BUILD_HEAVYFACTORY_SHADOW')[:256, :384].copy()
factory_shadow[..., 3] = np.round(factory_shadow[..., 3] * SHADOW_TRANS / 255).astype(np.uint8)
x = LW
sheet.alpha_composite(Image.fromarray(factory_shadow), (x, y + 40))
sheet.alpha_composite(Image.fromarray(factory), (x, y + 40))
x += 400
for _, get in sets:
    for k in (6, 7, 0, 1):
        for layer in get(k, HOUSES[0][1]):
            sheet.alpha_composite(layer, (x, y + 90))
        x += FW
    x += 60
sheet.convert('RGB').save(OUT)
print('saved', sheet.size)
