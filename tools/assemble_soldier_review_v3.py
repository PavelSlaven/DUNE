#!/usr/bin/env python3
"""Assemble eight generated direction strips into the D2TM soldier atlas."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFont

from prepare_soldier_review_v2 import (
    apply_engine_tint,
    build_neutral_and_mask,
    classic_anchors,
    downscale_atlas,
    foot_anchor_x,
    frame,
    remove_connected_black,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts" / "soldier_review_v3"
SOURCE_DIR = OUTPUT / "source_strips"
CLASSIC = (
    ROOT / "resources" / "hd" / "classic" / "sdl_data"
    / "0155_UNIT_SOLDIER.png"
)
REFERENCE_COPY = OUTPUT / "reference.png"

DIRECTIONS = ("E", "NE", "N", "NW", "W", "SW", "S", "SE")
FRAME = (128, 128)
ATLAS = (1024, 512)
TARGET_HEIGHT = 44
HOUSE_COLORS = {
    "Харконнены": (255, 0, 0),
    "Атрейдесы": (0, 90, 255),
    "Ордос": (0, 255, 0),
}

BASE_OUT = OUTPUT / "UNIT_SOLDIER_HD4_PREVIEW.png"
MASK_OUT = OUTPUT / "HM_UNIT_SOLDIER_HD4_PREVIEW.png"
HD2_OUT = OUTPUT / "UNIT_SOLDIER_HD2_PREVIEW.png"
RED_OUT = OUTPUT / "UNIT_SOLDIER_HARKONNEN_HD4_PREVIEW.png"
BLUE_OUT = OUTPUT / "UNIT_SOLDIER_ATREIDES_HD4_PREVIEW.png"
GREEN_OUT = OUTPUT / "UNIT_SOLDIER_ORDOS_HD4_PREVIEW.png"
REVIEW_OUT = OUTPUT / "UNIT_SOLDIER_V3_REVIEW.png"
ANIMATION_OUT = OUTPUT / "UNIT_SOLDIER_V3_ANIMATION.gif"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    filename = "arialbd.ttf" if bold else "arial.ttf"
    return ImageFont.truetype(
        str(Path("C:/Windows/Fonts") / filename),
        size,
    )


def strip_cell(strip: Image.Image, phase: int) -> Image.Image:
    left = round(phase * strip.width / 4)
    right = round((phase + 1) * strip.width / 4)
    return strip.crop((left, 0, right, strip.height))


def fit_subject(cell: Image.Image) -> tuple[Image.Image, float]:
    subject = remove_connected_black(cell)
    scale = TARGET_HEIGHT / subject.height
    subject = subject.resize(
        (
            max(1, round(subject.width * scale)),
            TARGET_HEIGHT,
        ),
        Image.Resampling.LANCZOS,
    )
    visible_box = subject.getchannel("A").point(
        lambda value: 255 if value > 8 else 0
    ).getbbox()
    if visible_box is None:
        raise AssertionError("generated cell has no visible soldier")
    subject = subject.crop(visible_box)
    if subject.height != TARGET_HEIGHT:
        subject = subject.resize(
            (
                max(
                    1,
                    round(
                        subject.width
                        * TARGET_HEIGHT
                        / subject.height
                    ),
                ),
                TARGET_HEIGHT,
            ),
            Image.Resampling.LANCZOS,
        )
    return subject, foot_anchor_x(subject)


def build_atlas(classic: Image.Image) -> Image.Image:
    anchors = classic_anchors(classic)
    atlas = Image.new("RGBA", ATLAS)
    for column, direction in enumerate(DIRECTIONS):
        source_path = SOURCE_DIR / f"{direction}.png"
        if not source_path.is_file():
            raise FileNotFoundError(source_path)
        strip = Image.open(source_path).convert("RGBA")
        if strip.width / strip.height < 1.45:
            raise AssertionError(
                f"unexpected direction-strip aspect ratio: "
                f"{direction} {strip.size}"
            )
        for row in range(4):
            subject, source_anchor_x = fit_subject(
                strip_cell(strip, row)
            )
            anchor_x, anchor_y = anchors[column]
            output = Image.new("RGBA", FRAME)
            output.alpha_composite(
                subject,
                (
                    round(anchor_x - source_anchor_x),
                    anchor_y - subject.height,
                ),
            )
            atlas.alpha_composite(
                output,
                (column * FRAME[0], row * FRAME[1]),
            )
    return atlas


def subject_closeup(sprite: Image.Image, size: int) -> Image.Image:
    box = sprite.getchannel("A").point(
        lambda value: 255 if value > 8 else 0
    ).getbbox()
    if box is None:
        raise AssertionError("empty preview sprite")
    padding = 6
    crop = sprite.crop(
        (
            max(0, box[0] - padding),
            max(0, box[1] - padding),
            min(FRAME[0], box[2] + padding),
            min(FRAME[1], box[3] + padding),
        )
    )
    return crop.resize((size, size), Image.Resampling.LANCZOS)


def build_review(colored: Image.Image) -> Image.Image:
    cell_size = 180
    board = Image.new(
        "RGBA",
        (100 + cell_size * 4, 70 + cell_size * 8),
        (9, 12, 16, 255),
    )
    draw = ImageDraw.Draw(board)
    draw.text(
        (18, 14),
        "Одиночный солдат — новый атлас 8×4",
        font=font(25, True),
        fill=(236, 219, 182, 255),
    )
    for column, direction in enumerate(DIRECTIONS):
        y = 62 + column * cell_size
        draw.text(
            (18, y + 75),
            direction,
            font=font(18, True),
            fill=(225, 188, 98, 255),
        )
        for row in range(4):
            board.alpha_composite(
                subject_closeup(
                    frame(colored, column, row),
                    cell_size,
                ),
                (90 + row * cell_size, y),
            )
    return board


def build_animation(colored: Image.Image) -> None:
    animation_frames = []
    for row in range(4):
        shown = Image.new("RGBA", (1024, 512), (16, 20, 26, 255))
        draw = ImageDraw.Draw(shown)
        for column, direction in enumerate(DIRECTIONS):
            x = (column % 4) * 256
            y = (column // 4) * 256
            shown.alpha_composite(
                frame(colored, column, row).resize(
                    (256, 256),
                    Image.Resampling.LANCZOS,
                ),
                (x, y),
            )
            draw.text(
                (x + 12, y + 10),
                direction,
                font=font(18, True),
                fill=(225, 188, 98, 255),
            )
        animation_frames.append(
            shown.convert("P", palette=Image.Palette.ADAPTIVE)
        )
    animation_frames[0].save(
        ANIMATION_OUT,
        save_all=True,
        append_images=animation_frames[1:],
        duration=180,
        loop=0,
        disposal=2,
    )


def validate(
    colored: Image.Image,
    neutral: Image.Image,
    mask: Image.Image,
) -> dict[str, object]:
    if colored.size != ATLAS:
        raise AssertionError(f"unexpected atlas size {colored.size}")
    if ImageChops.difference(
        colored.getchannel("A"),
        neutral.getchannel("A"),
    ).getbbox():
        raise AssertionError("neutralization changed alpha")

    unique = set()
    bounds = []
    for row in range(4):
        row_bounds = []
        for column in range(8):
            sprite = frame(neutral, column, row)
            box = sprite.getchannel("A").point(
                lambda value: 255 if value > 8 else 0
            ).getbbox()
            if box is None:
                raise AssertionError(f"empty frame {column},{row}")
            if box[0] < 2 or box[1] < 2 or box[2] > 126 or box[3] > 126:
                raise AssertionError(
                    f"frame touches boundary {column},{row}: {box}"
                )
            row_bounds.append(list(box))
            unique.add(sprite.tobytes())
        bounds.append(row_bounds)
    if len(unique) != 32:
        raise AssertionError(
            f"expected 32 unique frames, got {len(unique)}"
        )

    for column, direction in enumerate(DIRECTIONS):
        baselines = [bounds[row][column][3] for row in range(4)]
        if len(set(baselines)) != 1:
            raise AssertionError(
                f"baseline jumps in {direction}: {baselines}"
            )

    return {
        "resource_id": 155,
        "resource": "UNIT_SOLDIER",
        "logical_frame": [32, 32],
        "hd4_frame": list(FRAME),
        "atlas_size": list(ATLAS),
        "direction_order": list(DIRECTIONS),
        "walk_phases": [
            "left_stride",
            "passing",
            "right_stride",
            "passing_return",
        ],
        "target_height_hd4": TARGET_HEIGHT,
        "target_height_logical": TARGET_HEIGHT // 4,
        "unique_frames": len(unique),
        "frame_bounds": bounds,
        "mask_pixels": int(
            np.count_nonzero(np.asarray(mask.getchannel("A")) > 8)
        ),
    }


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    classic = Image.open(CLASSIC).convert("RGBA")
    if classic.size != (256, 128):
        raise AssertionError(f"unexpected classic size {classic.size}")

    colored = build_atlas(classic)
    neutral, mask = build_neutral_and_mask(colored)
    red = apply_engine_tint(
        neutral,
        mask,
        HOUSE_COLORS["Харконнены"],
    )
    blue = apply_engine_tint(
        neutral,
        mask,
        HOUSE_COLORS["Атрейдесы"],
    )
    green = apply_engine_tint(
        neutral,
        mask,
        HOUSE_COLORS["Ордос"],
    )
    validation = validate(colored, neutral, mask)

    neutral.save(BASE_OUT, optimize=True)
    mask.save(MASK_OUT, optimize=True)
    downscale_atlas(neutral).save(HD2_OUT, optimize=True)
    red.save(RED_OUT, optimize=True)
    blue.save(BLUE_OUT, optimize=True)
    green.save(GREEN_OUT, optimize=True)
    build_review(red).save(REVIEW_OUT, optimize=True)
    build_animation(red)

    manifest = {
        "format": 1,
        "status": "preview_not_integrated",
        "source_reference": str(REFERENCE_COPY),
        "source_strips": {
            direction: str(SOURCE_DIR / f"{direction}.png")
            for direction in DIRECTIONS
        },
        "classic_contract": str(CLASSIC),
        "image_generation": (
            "built-in image_gen; one direction strip per prompt"
        ),
        "prompt_contract": {
            "directions": list(DIRECTIONS),
            "frames_per_direction": 4,
            "gait": (
                "left stride, passing, right stride, passing return"
            ),
            "invariants": [
                "same character, scale, camera, baseline and lighting",
                "pistol always visible in anatomical right hand",
                "connected full-body motion without floating limbs",
                "flat black background without labels or shadows",
            ],
        },
        "operation": (
            "generated direction strips, connected-black extraction, "
            "fixed-height scaling, classic anchor alignment, "
            "8x4 transpose, faction-mask derivation"
        ),
        "validation": validation,
    }
    (OUTPUT / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(manifest, ensure_ascii=False))


if __name__ == "__main__":
    main()
