from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[4]
CACHE = ROOT / ".cache" / "ui-redesign"
BEFORE = CACHE / "before" / "png" / "1024x768" / "en" / "hd"
BATTLE = CACHE / "battle-ref"
CONCEPTS = ROOT / "codex-direct" / "ui-redesign" / "concepts"
OUT = CONCEPTS / "compare"
FONT = CACHE / "fonts" / "RussoOne-Regular.ttf"

BG = (16, 20, 24)
LABEL_COLOR = (231, 190, 91)
FRAME_COLOR = (147, 112, 47)
HEIGHT = 600
GAP = 24
MARGIN = 20
BAND = 40
LABEL_SIZE = 22
LEFT_LABEL = "Сейчас"
RIGHT_LABEL = "Образец"

PAIRS = [
    ("1-main-menu", BEFORE / "main-menu.png", CONCEPTS / "1-main-menu-800x600.png"),
    ("2-options", BEFORE / "options-menu-main.png", CONCEPTS / "2-options-800x600.png"),
    ("3-choose-house", BEFORE / "choose-house.png", CONCEPTS / "3-choose-house-800x600.png"),
    ("3b-campaign-map", BEFORE / "region-atreides-select-5.png", CONCEPTS / "3b-campaign-map-800x600.png"),
    ("3c-mission-select", BEFORE / "select-mission-atreides.png", CONCEPTS / "3c-mission-select-800x600.png"),
    ("4-mentat", BEFORE / "mentat-briefing-atreides-await.png", CONCEPTS / "4-mentat-800x600.png"),
    ("5-skirmish", BEFORE / "skirmish-setup-ready-map.png", CONCEPTS / "5-skirmish-800x600.png"),
    ("6-battle-4x3", BATTLE / "s_1024x768_en_hd_game-hud.png", CONCEPTS / "6-battle-800x600.png"),
    ("6-battle-16x9", BATTLE / "s_1920x1080_en_hd_game-hud.png", CONCEPTS / "6-battle-1067x600.png"),
    ("8-credits", BEFORE / "credits-2.png", CONCEPTS / "8-credits-800x600.png"),
]


def load(path):
    img = Image.open(path).convert("RGBA")
    base = Image.new("RGBA", img.size, BG + (255,))
    base.alpha_composite(img)
    return base.convert("RGB")


def scaled(img):
    width = round(img.width * HEIGHT / img.height)
    return img.resize((width, HEIGHT), Image.Resampling.LANCZOS)


def panel(canvas, draw, x, img, label, font):
    w = img.width
    top = MARGIN + BAND
    draw.text((x + (w + 2) // 2, MARGIN + BAND // 2), label, font=font, fill=LABEL_COLOR, anchor="mm")
    canvas.paste(img, (x + 1, top + 1))
    draw.rectangle([x, top, x + w + 1, top + HEIGHT + 1], outline=FRAME_COLOR, width=1)
    return x + w + 2


def build(name, left_path, right_path, font):
    if not left_path.is_file() or not right_path.is_file():
        return None
    left = scaled(load(left_path))
    right = scaled(load(right_path))
    width = MARGIN + left.width + 2 + GAP + right.width + 2 + MARGIN
    height = MARGIN + BAND + HEIGHT + 2 + MARGIN
    canvas = Image.new("RGB", (width, height), BG)
    draw = ImageDraw.Draw(canvas)
    x = panel(canvas, draw, MARGIN, left, LEFT_LABEL, font)
    panel(canvas, draw, x + GAP, right, RIGHT_LABEL, font)
    canvas.save(OUT / f"{name}.jpg", "JPEG", quality=90)
    return canvas.size


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    font = ImageFont.truetype(str(FONT), LABEL_SIZE)
    skipped = []
    for name, left_path, right_path in PAIRS:
        size = build(name, left_path, right_path, font)
        if size is None:
            skipped.append(name)
            print(f"SKIP {name}")
        else:
            print(f"{name}.jpg {size[0]}x{size[1]}")
    print(f"built {len(PAIRS) - len(skipped)}, skipped {len(skipped)}: {', '.join(skipped) or '-'}")


if __name__ == "__main__":
    main()
