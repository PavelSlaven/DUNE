"""Old and new frames side by side on sand, x2.
usage: python -X utf8 preview.py <out png>   (run from the repo root)"""
import sys

from PIL import Image

from common import S, FW, FH, old_frames, pack_img

Z = 2
old = old_frames()
sand = Image.fromarray(pack_img('TERRAIN_SAND'))
sheet = Image.new('RGBA', (8 * FW * Z, 2 * FH * Z))
for x in range(0, sheet.width, sand.width):
    for y in range(0, sheet.height, sand.height):
        sheet.paste(sand, (x, y))
for k in range(8):
    for r, img in enumerate((Image.fromarray(old[k]), Image.open(S / f'g3/frames/k{k}.png'))):
        sheet.alpha_composite(img.resize((FW * Z, FH * Z), Image.LANCZOS), (k * FW * Z, r * FH * Z))
sheet.convert('RGB').save(sys.argv[1])
