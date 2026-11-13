"""Probe G3 input canvases (1024x1024 on magenta): old frames and 63-degree block guides. usage: make_inputs.py <g3 dir> <k...> (repo root)"""
import sys
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path('tools').resolve()))
from hd_assets import read_pack, decode_image  # noqa: E402

G3, DIRS = Path(sys.argv[1]), [int(k) for k in sys.argv[2:]]
FW, FH, CANVAS, MAGENTA = 152, 184, 1024, (255, 0, 255, 255)
out = G3 / 'input'
out.mkdir(exist_ok=True)
old = decode_image({e.name: e for e in read_pack(Path('resources/bin/data/sdl_data_hd4.dat'))}['UNIT_DEVASTATOR'].payload).convert('RGBA')


def on_magenta(img, pos):
    canvas = Image.new('RGBA', (CANVAS, CANVAS), MAGENTA)
    canvas.alpha_composite(img, pos)
    return canvas.convert('RGB')


for k in DIRS:
    frame = old.crop((k * FW, 0, (k + 1) * FW, FH)).resize((round(FW * CANVAS / FH), CANVAS), Image.LANCZOS)
    on_magenta(frame, ((CANVAS - frame.width) // 2, 0)).save(out / f'old_k{k}.png')
    on_magenta(Image.open(G3 / f'raw/guide_raw_k{k}.png').convert('RGBA'), (0, 0)).save(out / f'guide_k{k}.png')
preview = Image.new('RGB', (len(DIRS) * 384, 768))
for i, k in enumerate(DIRS):
    preview.paste(Image.open(out / f'old_k{k}.png').resize((384, 384)), (i * 384, 0))
    preview.paste(Image.open(out / f'guide_k{k}.png').resize((384, 384)), (i * 384, 384))
preview.save(G3 / 'inputs-preview.png')
