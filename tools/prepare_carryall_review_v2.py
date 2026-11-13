#!/usr/bin/env python3
"""Build a strict top-down Carryall atlas by rotating one accepted master."""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts" / "carryall_review_v2"
CARRYALL = OUT / "carryall_topdown_transparent.png"
HARVESTER = (
    ROOT
    / "artifacts"
    / "harvester_review_v1"
    / "UNIT_HARVESTER_HD4_PREVIEW.png"
)

DIRECTIONS = ("E", "NE", "N", "NW", "W", "SW", "S", "SE")
ANGLES = (0, 45, 90, 135, 180, 225, 270, 315)
# The loaded master faces S. These are the deltas required to obtain the
# public D2TM order E, NE, N, NW, W, SW, S, SE from that single master.
LOADED_ANGLES_FROM_S = (90, 135, 180, 225, 270, 315, 0, 45)
FRAME = 192
ATLAS = OUT / "UNIT_CARRYALL_TOPDOWN_HD4_PREVIEW.png"
REVIEW = OUT / "UNIT_CARRYALL_TOPDOWN_REVIEW.png"
SCALE_REVIEW = OUT / "UNIT_CARRYALL_SCALE_CHECK.png"
MANIFEST = OUT / "prepare_manifest.json"


def trim(image: Image.Image) -> Image.Image:
    image = image.convert("RGBA")
    box = image.getchannel("A").getbbox()
    if box is None:
        raise RuntimeError("empty source image")
    return image.crop(box)


def fit(image: Image.Image, max_width: int, max_height: int) -> Image.Image:
    scale = min(max_width / image.width, max_height / image.height)
    size = (
        max(1, round(image.width * scale)),
        max(1, round(image.height * scale)),
    )
    return image.resize(size, Image.Resampling.LANCZOS)


def centered_canvas(image: Image.Image, *, offset_y: int = 0) -> Image.Image:
    canvas = Image.new("RGBA", (FRAME, FRAME))
    x = (FRAME - image.width) // 2
    y = (FRAME - image.height) // 2 + offset_y
    canvas.alpha_composite(image, (x, y))
    return canvas


def rotate_fixed(image: Image.Image, angle: int) -> Image.Image:
    # One immutable top-down master is rotated around the exact frame center.
    # No per-direction rescaling, redrawing, perspective correction or offset.
    return image.rotate(
        angle,
        resample=Image.Resampling.BICUBIC,
        expand=False,
        center=(FRAME / 2, FRAME / 2),
    )


def build_master() -> Image.Image:
    # Match the classic logical footprint relative to the accepted Harvester:
    # Carryall E ≈ 36×39 logical px, Harvester E ≈ 46×34 logical px.
    # This preserves the classic relationship: the aircraft is slightly
    # narrower, but longer and visually larger than the ground vehicle.
    carryall = fit(trim(Image.open(CARRYALL)), 147, 156)
    return centered_canvas(carryall)


def build_atlas() -> Image.Image:
    empty = build_master()
    harvester_atlas = Image.open(HARVESTER).convert("RGBA")
    atlas = Image.new("RGBA", (FRAME * 8, FRAME * 2))
    frame_boxes: list[list[list[int]]] = [[], []]

    aircraft_s = rotate_fixed(empty, ANGLES[6])
    harvester_s = trim(
        harvester_atlas.crop((6 * 320, 0, 7 * 320, 208))
    )
    if harvester_s.width > FRAME or harvester_s.height > FRAME:
        raise RuntimeError(f"Harvester S does not fit 48×48: {harvester_s.size}")
    loaded_s = centered_canvas(harvester_s)
    loaded_s.alpha_composite(aircraft_s)

    for index, angle in enumerate(ANGLES):
        aircraft = rotate_fixed(empty, angle)
        atlas.alpha_composite(aircraft, (index * FRAME, 0))

        # The complete accepted S pair is rigidly rotated as one object.
        loaded = rotate_fixed(loaded_s, LOADED_ANGLES_FROM_S[index])
        atlas.alpha_composite(loaded, (index * FRAME, FRAME))

        for row, frame in enumerate((aircraft, loaded)):
            box = frame.getchannel("A").getbbox()
            if box is None:
                raise RuntimeError(f"empty frame row={row} direction={DIRECTIONS[index]}")
            frame_boxes[row].append(list(box))

    atlas.save(ATLAS)
    MANIFEST.write_text(
        json.dumps(
            {
                "direction_order": list(DIRECTIONS),
                "rotation_degrees_counter_clockwise": list(ANGLES),
                "rows": ["empty", "loaded_harvester"],
                "logical_frame": [48, 48],
                "hd4_frame": [FRAME, FRAME],
                "method": "one orthographic top-down master rotated around frame center",
                "harvester_method": "accepted loaded S frame rotated rigidly around the shared centre",
                "loaded_rotation_degrees_from_s": list(LOADED_ANGLES_FROM_S),
                "frame_boxes_hd4": frame_boxes,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    return atlas


def font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for path in (
        Path("C:/Windows/Fonts/arial.ttf"),
        Path("C:/Windows/Fonts/segoeui.ttf"),
    ):
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def build_review(atlas: Image.Image) -> None:
    margin, gap, cell = 20, 12, 172
    width = margin * 2 + cell * 8 + gap * 7 + 100
    height = 540
    board = Image.new("RGB", (width, height), "#0c1116")
    draw = ImageDraw.Draw(board)
    draw.text(
        (20, 14),
        "Транспортник — строго сверху, вращение по оси",
        font=font(27),
        fill="#f2dfba",
    )
    draw.text(
        (20, 52),
        "Пустой мастер E и загруженный мастер S вращаются целиком вокруг общего центра.",
        font=font(16),
        fill="#aeb8c3",
    )

    start_x, start_y = 110, 90
    for row, label in enumerate(("ПУСТОЙ", "ХАРВЕСТЕР")):
        y = start_y + row * 220
        draw.text((20, y + 74), label, font=font(16), fill="#e2b958")
        for index, direction in enumerate(DIRECTIONS):
            x = start_x + index * (cell + gap)
            draw.rectangle((x, y, x + cell, y + cell), fill="#171d23", outline="#ad7921")
            frame = atlas.crop(
                (
                    index * FRAME,
                    row * FRAME,
                    (index + 1) * FRAME,
                    (row + 1) * FRAME,
                )
            )
            preview = frame.resize((160, 160), Image.Resampling.LANCZOS)
            board.paste(preview, (x + 6, y + 4), preview)
            draw.text((x + 8, y + 148), direction, font=font(16), fill="#f6e4b9")

    board.save(REVIEW)


def build_scale_review(atlas: Image.Image) -> None:
    board = Image.new("RGB", (980, 330), "#0c1116")
    draw = ImageDraw.Draw(board)
    draw.text((20, 14), "Сопоставление игрового масштаба — одинаковая плотность HD4", font=font(24), fill="#f2dfba")
    draw.text((20, 50), "Одна крупная клетка = 8 логических пикселей", font=font(15), fill="#aeb8c3")
    carryall_empty = atlas.crop((0, 0, 192, 192))
    harvester_ground = Image.open(HARVESTER).convert("RGBA").crop((0, 0, 320, 208))
    carryall_loaded = atlas.crop((0, 192, 192, 384))
    panels = (
        ("Транспортник", carryall_empty),
        ("Харвестер на земле", harvester_ground),
        ("Транспортник с харвестером", carryall_loaded),
    )
    positions = (20, 330, 650)
    for (label, sprite), x in zip(panels, positions):
        box = sprite.getchannel("A").getbbox()
        if box is None:
            raise RuntimeError(f"empty scale-review sprite: {label}")
        logical = ((box[2] - box[0]) / 4, (box[3] - box[1]) / 4)
        draw.rectangle((x, 82, x + 290, 302), fill="#171d23", outline="#ad7921")
        for gx in range(x + 2, x + 290, 32):
            draw.line((gx, 82, gx, 302), fill="#29323a")
        for gy in range(82, 303, 32):
            draw.line((x, gy, x + 290, gy), fill="#29323a")
        px = x + (290 - sprite.width) // 2
        py = 92 + (192 - sprite.height) // 2
        board.paste(sprite, (px, py), sprite)
        draw.text((x + 8, 276), label, font=font(15), fill="#f6e4b9")
        draw.text((x + 8, 300), f"силуэт ≈ {logical[0]:g}×{logical[1]:g} лог. px", font=font(13), fill="#aeb8c3")
    board.save(SCALE_REVIEW)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    atlas = build_atlas()
    build_review(atlas)
    build_scale_review(atlas)
    print(MANIFEST.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
