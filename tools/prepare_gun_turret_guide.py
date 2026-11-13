#!/usr/bin/env python3
"""Export an enlarged direction guide for the classic gun turret."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts" / "gun_turret_review_v1"
CLASSIC = (
    ROOT
    / "resources"
    / "hd"
    / "classic"
    / "sdl_data"
    / "0038_BUILD_TURRET.png"
)
DIRECTIONS = ("E", "NE", "N", "NW", "W", "SW", "S", "SE")


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    classic = Image.open(CLASSIC).convert("RGBA")
    board = Image.new("RGBA", (1024, 512), (255, 0, 255, 255))
    draw = ImageDraw.Draw(board)
    font = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 28)
    for index, direction in enumerate(DIRECTIONS):
        column = index % 4
        row = index // 4
        frame = classic.crop((0, index * 32, 32, (index + 1) * 32))
        enlarged = frame.resize((224, 224), Image.Resampling.NEAREST)
        x = column * 256 + 16
        y = row * 256 + 4
        board.alpha_composite(enlarged, (x, y))
        draw.text((x + 6, y + 218), direction, font=font, fill=(255, 255, 255))
    board.convert("RGB").save(
        OUTPUT / "classic_direction_guide.png",
        optimize=True,
    )


if __name__ == "__main__":
    main()
