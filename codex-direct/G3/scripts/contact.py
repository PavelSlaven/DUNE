"""Raw contact sheet of G3 candidates: per direction the old frame, the guide and both attempts.
usage: python -X utf8 contact.py   (run from the repo root)"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

S = Path(__file__).resolve().parent.parent
G3 = Path('codex-direct/G3/input')
font = ImageFont.truetype('resources/bin/data/PTSansNarrow-Regular.ttf', 22)
tile = 300
sheet = Image.new('RGB', (4 * tile, 8 * (tile + 30)), (30, 30, 30))
d = ImageDraw.Draw(sheet)
for k in range(8):
    src = S / 'g2/input' if k in (1, 6) else G3
    tiles = [src / f'old_k{k}.png', src / f'guide_k{k}.png', S / f'g3/cand/g3_k{k}_a.png', S / f'g3/cand/g3_k{k}_b.png']
    y = k * (tile + 30)
    for c, (p, name) in enumerate(zip(tiles, ('old', 'guide', 'a', 'b'))):
        d.text((c * tile + 8, y + 4), f'k{k} {name}', fill='white', font=font)
        sheet.paste(Image.open(p).convert('RGB').resize((tile, tile), Image.LANCZOS), (c * tile, y + 30))
sheet.save(S / 'g3/contact-raw.png')
