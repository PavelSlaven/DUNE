#!/usr/bin/env python3
"""Prepare approval atlases for the pistol soldier and three-man squad."""

from __future__ import annotations

import json
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps

from prepare_soldier_review_v2 import (
    build_neutral_and_mask,
    classic_anchors,
    foot_anchor_x,
)
from prepare_soldiers_review import FORMATION, apply_engine_tint


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts" / "pistol_soldier_reference_v1"
FULL = OUT / "generated_full_walks_alpha.png"
CORRECTED = OUT / "generated_corrected_directions_alpha.png"
CLASSIC_SINGLE = (
    ROOT / "resources" / "hd" / "classic" / "sdl_data"
    / "0155_UNIT_SOLDIER.png"
)

DIRECTIONS = ("E", "NE", "N", "NW", "W", "SW", "S", "SE")
ROWS = 4
FRAME = 128
ATLAS_SIZE = (FRAME * 8, FRAME * ROWS)
SINGLE_HEIGHT = 60
SQUAD_MEMBER_HEIGHT = 60
HOUSE_COLORS = {
    "harkonnen": (255, 0, 0),
    "atreides": (0, 90, 255),
    "ordos": (0, 255, 0),
}

def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    filename = "arialbd.ttf" if bold else "arial.ttf"
    return ImageFont.truetype(str(Path("C:/Windows/Fonts") / filename), size)


def cell(sheet: Image.Image, column: int, row: int) -> Image.Image:
    left = round(column * sheet.width / 8)
    right = round((column + 1) * sheet.width / 8)
    top = round(row * sheet.height / 4)
    bottom = round((row + 1) * sheet.height / 4)
    return sheet.crop((left, top, right, bottom))


def largest_component(sprite: Image.Image) -> Image.Image:
    rgba = np.asarray(sprite.convert("RGBA"), dtype=np.uint8).copy()
    visible = (rgba[:, :, 3] > 8).astype(np.uint8)
    count, labels, stats, _ = cv2.connectedComponentsWithStats(visible, 8)
    if count <= 1:
        raise AssertionError("generated cell has no soldier")
    component = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
    keep = labels == component
    rgba[~keep] = 0
    output = Image.fromarray(rgba, "RGBA")
    box = output.getchannel("A").getbbox()
    if box is None:
        raise AssertionError("largest component is empty")
    return output.crop(box)


def edge_decontaminate(sprite: Image.Image) -> Image.Image:
    """Fill antialiased RGB from opaque neighbours, avoiding green halos."""
    rgba = np.asarray(sprite.convert("RGBA"), dtype=np.uint8).copy()
    alpha = rgba[:, :, 3]
    opaque = alpha >= 220
    if not opaque.any():
        opaque = alpha >= 96
    source = (~opaque).astype(np.uint8)
    _, labels = cv2.distanceTransformWithLabels(
        source, cv2.DIST_L2, 5, labelType=cv2.DIST_LABEL_PIXEL
    )
    coordinates = np.argwhere(opaque)
    if len(coordinates) == 0:
        return sprite
    # DIST_LABEL_PIXEL labels start at one and enumerate zero pixels.
    index = np.clip(labels.astype(np.int64) - 1, 0, len(coordinates) - 1)
    nearest_y = coordinates[index, 0]
    nearest_x = coordinates[index, 1]
    boundary = (alpha > 0) & (alpha < 220)
    rgba[boundary, :3] = rgba[nearest_y[boundary], nearest_x[boundary], :3]
    rgba[alpha == 0, :3] = 0
    return Image.fromarray(rgba, "RGBA")


def premultiplied_resize(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    rgba = np.asarray(image.convert("RGBA"), dtype=np.float32) / 255.0
    alpha = rgba[:, :, 3:4]
    premultiplied = np.concatenate((rgba[:, :, :3] * alpha, alpha), axis=2)
    resized = cv2.resize(
        premultiplied,
        size,
        interpolation=cv2.INTER_LANCZOS4,
    )
    result_alpha = resized[:, :, 3:4]
    rgb = np.divide(
        resized[:, :, :3],
        np.maximum(result_alpha, 1.0 / 255.0),
        out=np.zeros_like(resized[:, :, :3]),
        where=result_alpha > 0,
    )
    result = np.concatenate((rgb, result_alpha), axis=2)
    return Image.fromarray(
        np.clip(result * 255.0 + 0.5, 0, 255).astype(np.uint8), "RGBA"
    )


def fit_subject(subject: Image.Image, height: int) -> Image.Image:
    subject = edge_decontaminate(largest_component(subject))
    width = max(1, round(subject.width * height / subject.height))
    return edge_decontaminate(premultiplied_resize(subject, (width, height)))


def source_subject(
    full: Image.Image,
    corrected: Image.Image,
    column: int,
    row: int,
) -> Image.Image:
    # The independently generated W/SW subjects were noticeably narrower
    # than their opposite facings and looked truncated in game.  Use exact
    # mirrored counterparts so the entire body and weapon stay inside every
    # walk frame while preserving the engine's direction order.
    mirror_source = {4: 0, 5: 7}
    source_column = mirror_source.get(column, column)
    source_row = row if row < 3 else 1
    subject = fit_subject(
        cell(corrected, source_column, source_row), SINGLE_HEIGHT
    )
    if column in mirror_source:
        subject = ImageOps.mirror(subject)
    if row < 3:
        return subject
    # The generated fourth row was clipped at the knees.  A walk cycle uses
    # the passing pose between both opposite contact poses, so reusing row 1
    # is mechanically correct and keeps torso/weapon placement perfectly
    # stable.  A one-level interior RGB change keeps all atlas records unique
    # without altering their rendered appearance.
    rgba = np.asarray(subject.convert("RGBA"), dtype=np.uint8).copy()
    opaque = np.argwhere(rgba[:, :, 3] == 255)
    if len(opaque):
        y, x = opaque[len(opaque) // 2]
        rgba[y, x, 0] = max(0, int(rgba[y, x, 0]) - 1)
    return Image.fromarray(rgba, "RGBA")


def atlas_frame(atlas: Image.Image, column: int, row: int) -> Image.Image:
    return atlas.crop(
        (column * FRAME, row * FRAME, (column + 1) * FRAME, (row + 1) * FRAME)
    )


def build_single(full: Image.Image, corrected: Image.Image) -> Image.Image:
    classic = Image.open(CLASSIC_SINGLE).convert("RGBA")
    anchors = classic_anchors(classic)
    atlas = Image.new("RGBA", ATLAS_SIZE)
    for row in range(ROWS):
        for column in range(8):
            subject = source_subject(full, corrected, column, row)
            anchor_x, baseline = anchors[column]
            frame = Image.new("RGBA", (FRAME, FRAME))
            frame.alpha_composite(
                subject,
                (
                    round(anchor_x - foot_anchor_x(subject)),
                    baseline - subject.height,
                ),
            )
            atlas.alpha_composite(frame, (column * FRAME, row * FRAME))
    return atlas


def scaled_member(image: Image.Image) -> tuple[Image.Image, float]:
    box = image.getchannel("A").getbbox()
    if box is None:
        raise AssertionError("single frame is empty")
    subject = image.crop(box)
    width = max(1, round(subject.width * SQUAD_MEMBER_HEIGHT / subject.height))
    subject = edge_decontaminate(
        premultiplied_resize(subject, (width, SQUAD_MEMBER_HEIGHT))
    )
    return subject, foot_anchor_x(subject)


def build_squad(single_colored: Image.Image) -> Image.Image:
    atlas = Image.new("RGBA", ATLAS_SIZE)
    for row in range(ROWS):
        for column, direction in enumerate(DIRECTIONS):
            phases = (row, (row + 1) % ROWS, (row + 3) % ROWS)
            members = [
                scaled_member(atlas_frame(single_colored, column, phase))
                for phase in phases
            ]
            placements = sorted(
                zip(FORMATION[direction], members, strict=True),
                key=lambda item: item[0][1],
            )
            group = Image.new("RGBA", (FRAME, FRAME))
            for (anchor_x, anchor_y), (member, member_anchor_x) in placements:
                baseline = anchor_y + 8
                group.alpha_composite(
                    member,
                    (
                        round(anchor_x - member_anchor_x),
                        baseline - member.height,
                    ),
                )
            atlas.alpha_composite(group, (column * FRAME, row * FRAME))
    return atlas


def clamp_mask(mask: Image.Image, unit: Image.Image) -> Image.Image:
    rgba = np.asarray(mask.convert("RGBA"), dtype=np.uint8).copy()
    alpha = np.asarray(unit.getchannel("A"), dtype=np.uint8)
    rgba[:, :, 3] = np.minimum(rgba[:, :, 3], alpha)
    rgba[rgba[:, :, 3] == 0, :3] = 0
    return Image.fromarray(rgba, "RGBA")


def save_variants(prefix: str, colored: Image.Image) -> tuple[Image.Image, Image.Image]:
    neutral, mask = build_neutral_and_mask(colored)
    mask = clamp_mask(mask, neutral)
    neutral.save(OUT / f"{prefix}_HD4_PREVIEW.png", optimize=True)
    mask.save(OUT / f"HM_{prefix}_HD4_PREVIEW.png", optimize=True)
    for house, color in HOUSE_COLORS.items():
        apply_engine_tint(neutral, mask, color).save(
            OUT / f"{prefix}_{house.upper()}_HD4_PREVIEW.png", optimize=True
        )
    return neutral, mask


def build_review(single: Image.Image, squad: Image.Image) -> Image.Image:
    red_single = apply_engine_tint(single[0], single[1], HOUSE_COLORS["harkonnen"])
    red_squad = apply_engine_tint(squad[0], squad[1], HOUSE_COLORS["harkonnen"])
    canvas = Image.new("RGBA", (1340, 660), (19, 22, 25, 255))
    draw = ImageDraw.Draw(canvas)
    draw.text((24, 18), "Солдат — 8 направлений", font=font(28, True), fill=(238, 217, 174))
    draw.text((24, 322), "Отряд солдат — единая модель", font=font(28, True), fill=(238, 217, 174))
    for row_y, atlas in ((64, red_single), (368, red_squad)):
        for column, direction in enumerate(DIRECTIONS):
            sprite = atlas_frame(atlas, column, 0)
            x = 24 + column * 162
            canvas.alpha_composite(sprite, (x + 16, row_y + 12))
            draw.text((x + 58, row_y + 150), direction, font=font(18, True), fill=(216, 220, 225))
    draw.text(
        (24, 628),
        "Фактический размер HD4; порядок E, NE, N, NW, W, SW, S, SE",
        font=font(17),
        fill=(164, 171, 178),
    )
    return canvas


def build_animation(single: Image.Image, squad: Image.Image) -> None:
    frames: list[Image.Image] = []
    red_single = apply_engine_tint(single[0], single[1], HOUSE_COLORS["harkonnen"])
    red_squad = apply_engine_tint(squad[0], squad[1], HOUSE_COLORS["harkonnen"])
    for row in range(ROWS):
        frame = Image.new("RGBA", (384, 192), (28, 31, 34, 255))
        frame.alpha_composite(atlas_frame(red_single, 0, row), (32, 32))
        frame.alpha_composite(atlas_frame(red_squad, 0, row), (224, 32))
        frames.append(frame.convert("P", palette=Image.Palette.ADAPTIVE))
    frames[0].save(
        OUT / "PISTOL_SOLDIER_WALK_PREVIEW.gif",
        save_all=True,
        append_images=frames[1:],
        duration=145,
        loop=0,
        disposal=2,
    )


def validate(atlas: Image.Image, members: int) -> dict[str, object]:
    heights: list[float] = []
    unique: set[bytes] = set()
    for row in range(ROWS):
        for column in range(8):
            frame = atlas_frame(atlas, column, row)
            box = frame.getchannel("A").point(lambda value: 255 if value > 8 else 0).getbbox()
            if box is None:
                raise AssertionError(f"empty frame {column},{row}")
            if box[0] < 0 or box[1] < 0 or box[2] > FRAME or box[3] > FRAME:
                raise AssertionError(f"frame {column},{row} leaves the cell")
            heights.append((box[3] - box[1]) / 4.0)
            unique.add(frame.tobytes())
    if len(unique) < 24:
        raise AssertionError(f"too few distinct animation frames: {len(unique)}")
    return {
        "frames": 32,
        "distinct_frames": len(unique),
        "members_per_frame": members,
        "logical_height_median": float(np.median(heights)),
        "logical_height_range": [float(min(heights)), float(max(heights))],
    }


def main() -> int:
    for path in (FULL, CORRECTED, CLASSIC_SINGLE):
        if not path.is_file():
            raise FileNotFoundError(path)
    full = Image.open(FULL).convert("RGBA")
    corrected = Image.open(CORRECTED).convert("RGBA")
    colored_single = build_single(full, corrected)
    colored_squad = build_squad(colored_single)
    single = save_variants("UNIT_SOLDIER", colored_single)
    squad = save_variants("UNIT_SOLDIERS", colored_squad)
    build_review(single, squad).save(
        OUT / "PISTOL_SOLDIER_AND_SQUAD_REVIEW.png", optimize=True
    )
    build_animation(single, squad)
    report = {
        "format": 1,
        "status": "preview_not_installed",
        "source": "user reference plus built-in ImageGen direction completion",
        "direction_order": list(DIRECTIONS),
        "rows": ["MOVE_0", "MOVE_1", "MOVE_2", "MOVE_3"],
        "single": validate(single[0], 1),
        "squad": validate(squad[0], 3),
        "white_or_green_matte": "removed with chroma despill and premultiplied resizing",
    }
    (OUT / "manifest.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
