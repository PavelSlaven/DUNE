#!/usr/bin/env python3
"""Build derived pictures for the concept pages (battlefield crops, minimaps) from game screenshots.
Input: .cache/ui-redesign/battle-ref (screenshots of the current game). Output: .cache/ui-redesign/derived."""
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[4]
REF = ROOT / ".cache/ui-redesign/battle-ref"
OUT = ROOT / ".cache/ui-redesign/derived"


def field(source, box, size, name):
    image = Image.open(REF / source).convert("RGB").crop(box).resize(size, Image.LANCZOS)
    image.save(OUT / name, quality=92)
    return image


def minimap(image, cells, size, view, name):
    """Radar picture: the map fills the inner field of the radar (SYSTEM-ui.md 10.6), one map cell = size / cells points."""
    small = image.resize(cells, Image.BOX).quantize(48).convert("RGB")
    scale = min(size[0] / cells[0], size[1] / cells[1])
    big = small.resize((round(cells[0] * scale), round(cells[1] * scale)), Image.NEAREST)
    canvas = Image.new("RGB", size, (0, 0, 0))
    origin = ((size[0] - big.width) // 2, (size[1] - big.height) // 2)
    canvas.paste(big, origin)
    draw = ImageDraw.Draw(canvas)
    x0, y0, x1, y1 = (round(value * scale) for value in view)
    draw.rectangle((origin[0] + x0, origin[1] + y0, origin[0] + x1, origin[1] + y1), outline=(255, 255, 255))
    canvas.save(OUT / name)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    atreides = field("s_1920x1080_en_hd_game-hud.png", (296, 76, 1170, 962), (560, 568), "field-atreides-560x568.jpg")
    minimap(atreides, (38, 38), (138, 138), (6, 8, 30, 30), "minimap-atreides-138.png")
    minimap(atreides, (38, 38), (146, 146), (6, 8, 30, 30), "minimap-atreides-146.png")
    ordos = field("pc_docs_skirmish-gameplay.png", (0, 85, 1840, 1290), (1600, 1048), "field-ordos-1600x1048.jpg")
    minimap(ordos, (66, 44), (194, 194), (8, 6, 58, 40), "minimap-ordos-194.png")
    wide = field("s_1920x1080_en_hd_game-hud.png", (52, 76, 1217, 962), (747, 568), "field-atreides-747x568.jpg")
    ultra = field("pc_docs_skirmish-gameplay.png", (0, 85, 1840, 661), (1813, 568), "field-ordos-wide.jpg")
    minimap(ordos, (66, 44), (146, 146), (8, 6, 58, 40), "minimap-ordos-146.png")
    shot = Image.open(ROOT / ".cache/ui-redesign/before/png/1024x768/en/hd/skirmish-setup-ready-map.png").convert("RGB")
    for name, box in (("sietch", (684, 339, 976, 631)), ("broken", (426, 346, 596, 498)), ("golek", (15, 557, 185, 709)),
                      ("delta", (219, 557, 391, 709)), ("division", (425, 557, 596, 709))):
        shot.crop(box).resize((128, 128), Image.NEAREST).save(OUT / f"map-{name}.png")
    region = ROOT / ".cache/ui-redesign/before/png/1920x1080/en/hd/r100w0/region-atreides-select-5.png"
    if region.is_file():
        Image.open(region).convert("RGB").crop((59, 144, 1861, 855)).save(OUT / "campaign-map-tinted.jpg", quality=92)
    print("ok", sorted(path.name for path in OUT.iterdir()))


if __name__ == "__main__":
    main()
