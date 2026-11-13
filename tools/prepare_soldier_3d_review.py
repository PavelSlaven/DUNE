#!/usr/bin/env python3
"""Assemble the synthesized GLB walk cycle into the D2TM HD contract."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFont

from prepare_soldier_review_v2 import (
    build_neutral_and_mask,
    classic_anchors,
    downscale_atlas,
)
from prepare_soldiers_review import apply_engine_tint


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts" / "soldier_3d_review_v1"
RENDERS = OUTPUT / "rigged_walk_renders"
CLASSIC = ROOT / "resources" / "hd" / "classic" / "sdl_data" / "0155_UNIT_SOLDIER.png"
SQUAD_MASTER = ROOT / "resources" / "hd" / "master4" / "sdl_data" / "0156_UNIT_SOLDIERS.png"
SQUAD_MASK = ROOT / "resources" / "hd" / "master4_extra_packs" / "sdl_data" / "HM_UNIT_SOLDIERS.png"

DIRECTIONS = ("E", "NE", "N", "NW", "W", "SW", "S", "SE")
ROWS = 4
FRAME = 128
# The classic UNIT_SOLDIER median silhouette is 15 logical pixels high.
# HD4 therefore uses 15 * 4, preserving the original apparent game size.
TARGET_HEIGHT = 60
ATLAS_SIZE = (FRAME * 8, FRAME * ROWS)
HOUSE_COLORS = {
    "Харконнены": (255, 0, 0),
    "Атрейдесы": (0, 90, 255),
    "Ордос": (0, 255, 0),
}

BASE_OUT = OUTPUT / "UNIT_SOLDIER_3D_HD4_PREVIEW.png"
MASK_OUT = OUTPUT / "HM_UNIT_SOLDIER_3D_HD4_PREVIEW.png"
HD2_OUT = OUTPUT / "UNIT_SOLDIER_3D_HD2_PREVIEW.png"
RED_OUT = OUTPUT / "UNIT_SOLDIER_3D_HARKONNEN_HD4_PREVIEW.png"
BLUE_OUT = OUTPUT / "UNIT_SOLDIER_3D_ATREIDES_HD4_PREVIEW.png"
GREEN_OUT = OUTPUT / "UNIT_SOLDIER_3D_ORDOS_HD4_PREVIEW.png"
REVIEW_OUT = OUTPUT / "UNIT_SOLDIER_3D_REVIEW.png"
ANIMATION_OUT = OUTPUT / "UNIT_SOLDIER_3D_ALL_DIRECTIONS.gif"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(
        str(Path("C:/Windows/Fonts") / ("arialbd.ttf" if bold else "arial.ttf")),
        size,
    )


def source_path(row: int, column: int, direction: str) -> Path:
    path = RENDERS / f"r{row}_c{column}_{direction}.png"
    if not path.is_file():
        raise FileNotFoundError(path)
    return path


def alpha_box(image: Image.Image) -> tuple[int, int, int, int]:
    box = image.getchannel("A").point(lambda value: 255 if value > 8 else 0).getbbox()
    if box is None:
        raise AssertionError("render contains no visible soldier")
    return box


def build_colored_atlas(classic: Image.Image) -> tuple[Image.Image, float]:
    sources: list[Image.Image] = []
    heights: list[int] = []
    for row in range(ROWS):
        for column, direction in enumerate(DIRECTIONS):
            image = Image.open(source_path(row, column, direction)).convert("RGBA")
            sources.append(image)
            box = alpha_box(image)
            heights.append(box[3] - box[1])

    # One global scale is essential: it preserves true 3D proportions and
    # prevents the unit growing or shrinking between gait phases/directions.
    reference_height = float(np.median(heights))
    scale = TARGET_HEIGHT / reference_height
    resized_canvas = max(1, round(512 * scale))
    anchors = classic_anchors(classic)
    atlas = Image.new("RGBA", ATLAS_SIZE)

    for index, source in enumerate(sources):
        row, column = divmod(index, 8)
        scaled = source.resize((resized_canvas, resized_canvas), Image.Resampling.LANCZOS)
        box = alpha_box(scaled)
        visible = scaled.crop(box)
        # The Blender camera is fixed and centered, so the render-center offset
        # is a more stable anchor than feet that naturally move during walking.
        source_center_x = resized_canvas / 2.0
        visible_center_offset = source_center_x - box[0]
        target_x = round(anchors[column][0] - visible_center_offset)
        target_y = anchors[column][1] - visible.height
        if target_x < 1 or target_y < 1 or target_x + visible.width > 127 or target_y + visible.height > 127:
            raise AssertionError(
                f"frame {direction}/{row} exceeds cell: {(target_x, target_y, visible.width, visible.height)}"
            )
        atlas.alpha_composite(visible, (column * FRAME + target_x, row * FRAME + target_y))
    return atlas, scale


def frame(atlas: Image.Image, column: int, row: int) -> Image.Image:
    return atlas.crop((column * FRAME, row * FRAME, (column + 1) * FRAME, (row + 1) * FRAME))


def masked_luminance(image: Image.Image, mask: Image.Image) -> float:
    rgba = np.asarray(image.convert("RGBA"), dtype=np.float32)
    weight = np.asarray(mask.getchannel("A"), dtype=np.float32) / 255.0
    weight[weight < 0.20] = 0.0
    if float(weight.sum()) < 1.0:
        raise AssertionError("empty faction mask")
    luminance = 0.2126 * rgba[:, :, 0] + 0.7152 * rgba[:, :, 1] + 0.0722 * rgba[:, :, 2]
    return float((luminance * weight).sum() / weight.sum())


def match_squad_armor_tone(
    neutral: Image.Image,
    mask: Image.Image,
) -> tuple[Image.Image, dict[str, float]]:
    squad = Image.open(SQUAD_MASTER).convert("RGBA")
    squad_mask = Image.open(SQUAD_MASK).convert("RGBA")
    target = masked_luminance(squad, squad_mask)

    rgba = np.asarray(neutral.convert("RGBA"), dtype=np.float32).copy()
    mask_alpha = np.asarray(mask.getchannel("A"), dtype=np.float32)
    weight = mask_alpha / 255.0
    selected = weight >= 0.20
    strength = np.clip(mask_alpha / 205.0, 0.0, 1.0)
    luminance = 0.2126 * rgba[:, :, 0] + 0.7152 * rgba[:, :, 1] + 0.0722 * rgba[:, :, 2]
    denominator = float(weight[selected].sum())
    darkest = float((luminance[selected] * (1.0 - strength[selected]) * weight[selected]).sum() / denominator)
    original = float((luminance[selected] * weight[selected]).sum() / denominator)
    factor = max(0.0, min(1.0, (target - darkest) / max(0.001, original - darkest)))
    multiplier = 1.0 - strength * (1.0 - factor)
    rgba[:, :, :3] *= multiplier[:, :, None]
    corrected = Image.fromarray(np.clip(rgba, 0, 255).astype(np.uint8), "RGBA")
    return corrected, {
        "squad_target_luminance": target,
        "soldier_before_luminance": original,
        "soldier_after_luminance": masked_luminance(corrected, mask),
        "armor_brightness_factor": factor,
    }


def checker(size: tuple[int, int]) -> Image.Image:
    image = Image.new("RGBA", size, (24, 27, 31, 255))
    draw = ImageDraw.Draw(image)
    step = 16
    for y in range(0, size[1], step):
        for x in range(0, size[0], step):
            if (x // step + y // step) % 2:
                draw.rectangle((x, y, x + step - 1, y + step - 1), fill=(31, 35, 40, 255))
    return image


def make_review(red: Image.Image, blue: Image.Image, green: Image.Image, mask: Image.Image) -> Image.Image:
    board = Image.new("RGBA", (1800, 1370), (13, 16, 20, 255))
    draw = ImageDraw.Draw(board)
    draw.text((42, 30), "UNIT_SOLDIER — синтез из 3D-модели", font=font(42, True), fill=(234, 196, 100, 255))
    draw.text(
        (42, 86),
        "8 точных ракурсов × 4 фазы ходьбы; корпус и оружие неизменны",
        font=font(25),
        fill=(205, 211, 220, 255),
    )

    for column, direction in enumerate(DIRECTIONS):
        card_x = 42 + (column % 4) * 430
        card_y = 145 + (column // 4) * 360
        draw.rounded_rectangle((card_x, card_y, card_x + 390, card_y + 325), 12, fill=(23, 27, 33, 255), outline=(113, 91, 47, 255), width=2)
        shown = checker((300, 256))
        sprite = frame(red, column, 1).resize((256, 256), Image.Resampling.NEAREST)
        shown.alpha_composite(sprite, (22, 0))
        board.alpha_composite(shown, (card_x + 45, card_y + 38))
        draw.text((card_x + 18, card_y + 12), direction, font=font(22, True), fill=(234, 196, 100, 255))

    y = 905
    draw.text((42, y), "Цветовые маски Домов", font=font(30, True), fill=(234, 196, 100, 255))
    samples = (("Харконнены", red), ("Атрейдесы", blue), ("Ордос", green), ("Маска", mask))
    for index, (label, atlas) in enumerate(samples):
        x = 42 + index * 430
        draw.rounded_rectangle((x, y + 55, x + 390, y + 325), 12, fill=(23, 27, 33, 255), outline=(113, 91, 47, 255), width=2)
        shown = checker((256, 220))
        shown.alpha_composite(frame(atlas, 7, 1).resize((220, 220), Image.Resampling.NEAREST), (18, 0))
        board.alpha_composite(shown, (x + 67, y + 86))
        draw.text((x + 18, y + 60), label, font=font(21, True), fill=(218, 221, 225, 255))

    draw.text((42, 1310), "Контракт: ID 155, кадр 32×32 логических px, HD4 128×128, высота бойца ≈11 логических px.", font=font(20), fill=(184, 191, 201, 255))
    return board


def make_animation(red: Image.Image) -> None:
    frames: list[Image.Image] = []
    for row in range(ROWS):
        board = Image.new("RGBA", (1024, 512), (17, 20, 25, 255))
        draw = ImageDraw.Draw(board)
        for column, direction in enumerate(DIRECTIONS):
            x = (column % 4) * 256
            y = (column // 4) * 256
            tile = checker((256, 256))
            tile.alpha_composite(frame(red, column, row).resize((256, 256), Image.Resampling.NEAREST))
            board.alpha_composite(tile, (x, y))
            draw.text((x + 8, y + 8), direction, font=font(18, True), fill=(255, 222, 122, 255))
        frames.append(board.convert("P", palette=Image.Palette.ADAPTIVE))
    frames[0].save(ANIMATION_OUT, save_all=True, append_images=frames[1:], duration=170, loop=0, disposal=2)


def validate(
    colored: Image.Image,
    neutral: Image.Image,
    mask: Image.Image,
    scale: float,
    tone_match: dict[str, float],
) -> dict[str, object]:
    if colored.size != ATLAS_SIZE or neutral.size != ATLAS_SIZE or mask.size != ATLAS_SIZE:
        raise AssertionError("invalid atlas size")
    if ImageChops.difference(colored.getchannel("A"), neutral.getchannel("A")).getbbox():
        raise AssertionError("neutralization changed alpha")
    bounds: list[list[list[int]]] = []
    hashes: set[bytes] = set()
    for row in range(ROWS):
        row_bounds = []
        for column, direction in enumerate(DIRECTIONS):
            sprite = frame(neutral, column, row)
            box = alpha_box(sprite)
            if box[0] < 1 or box[1] < 1 or box[2] > 127 or box[3] > 127:
                raise AssertionError(f"frame touches boundary: {direction}/{row} {box}")
            row_bounds.append(list(box))
            hashes.add(sprite.tobytes())
        bounds.append(row_bounds)
    if len(hashes) != 32:
        raise AssertionError(f"expected 32 unique frames, found {len(hashes)}")
    for column, direction in enumerate(DIRECTIONS):
        baselines = [bounds[row][column][3] for row in range(ROWS)]
        if len(set(baselines)) != 1:
            raise AssertionError(f"baseline jumps in {direction}: {baselines}")
    mask_pixels = int(np.count_nonzero(np.asarray(mask.getchannel("A")) > 8))
    if mask_pixels < 1000:
        raise AssertionError(f"faction mask is too small: {mask_pixels}")
    return {
        "resource_id": 155,
        "resource": "UNIT_SOLDIER",
        "source": "red armor trooper 3d model.glb",
        "source_has_skin": False,
        "source_has_animation": False,
        "synthesis": "deterministic four-phase lower-body rig",
        "direction_order": list(DIRECTIONS),
        "animation_rows": ["MOVE_0", "MOVE_1", "MOVE_2", "MOVE_3"],
        "atlas_size_hd4": list(ATLAS_SIZE),
        "frame_size_hd4": [FRAME, FRAME],
        "target_height_hd4": TARGET_HEIGHT,
        "global_scale": scale,
        "unique_frames": len(hashes),
        "mask_pixels": mask_pixels,
        "tone_match": tone_match,
        "frame_bounds": bounds,
        "installed": False,
    }


def main() -> None:
    classic = Image.open(CLASSIC).convert("RGBA")
    if classic.size != (256, 128):
        raise AssertionError(f"unexpected classic atlas size {classic.size}")
    colored, scale = build_colored_atlas(classic)
    neutral, mask = build_neutral_and_mask(colored)
    neutral, tone_match = match_squad_armor_tone(neutral, mask)
    red = apply_engine_tint(neutral, mask, HOUSE_COLORS["Харконнены"])
    blue = apply_engine_tint(neutral, mask, HOUSE_COLORS["Атрейдесы"])
    green = apply_engine_tint(neutral, mask, HOUSE_COLORS["Ордос"])
    manifest = validate(colored, neutral, mask, scale, tone_match)

    neutral.save(BASE_OUT, optimize=True)
    mask.save(MASK_OUT, optimize=True)
    downscale_atlas(neutral).save(HD2_OUT, optimize=True)
    red.save(RED_OUT, optimize=True)
    blue.save(BLUE_OUT, optimize=True)
    green.save(GREEN_OUT, optimize=True)
    make_review(red, blue, green, mask).save(REVIEW_OUT, optimize=True)
    make_animation(red)
    (OUTPUT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
