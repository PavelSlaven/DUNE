#!/usr/bin/env python3
"""Prepare an approval-ready HD4 gun-turret direction atlas."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont
from scipy import ndimage


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts" / "gun_turret_review_v1"
SOURCE = OUTPUT / "turret_alpha_v3.png"
CLASSIC = (
    ROOT
    / "resources"
    / "hd"
    / "classic"
    / "sdl_data"
    / "0038_BUILD_TURRET.png"
)

DIRECTIONS = ("E", "NE", "N", "NW", "W", "SW", "S", "SE")
DIRECTION_VECTORS = (
    (1.0, 0.0),
    (2**-0.5, -(2**-0.5)),
    (0.0, -1.0),
    (-(2**-0.5), -(2**-0.5)),
    (-1.0, 0.0),
    (-(2**-0.5), 2**-0.5),
    (0.0, 1.0),
    (2**-0.5, 2**-0.5),
)
FRAME = (128, 128)
ATLAS = (128, 1024)
GRID = (4, 2)
MARGIN = 5
DESIRED_FOUNDATION_WIDTH = 100.0
# The rotating housing is not circular in projection, so the barrel begins at
# a different radius in every direction. These joins are measured from the
# visible housing edge in the assembled HD4 frames.
BARREL_JOIN_RADII = (37.0, 32.0, 35.0, 33.0, 37.0, 28.0, 22.0, 28.0)
BARREL_TARGET_VISIBLE_LENGTH = 16.0

ATLAS_OUT = OUTPUT / "BUILD_TURRET_HD4_PREVIEW.png"
SHADOW_OUT = OUTPUT / "BUILD_TURRET_SHADOW_HD4_PREVIEW.png"
HD2_OUT = OUTPUT / "BUILD_TURRET_HD2_PREVIEW.png"
REVIEW_OUT = OUTPUT / "BUILD_TURRET_REVIEW.png"
ROTATION_OUT = OUTPUT / "BUILD_TURRET_ROTATION_PREVIEW.gif"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    filename = "arialbd.ttf" if bold else "arial.ttf"
    return ImageFont.truetype(
        str(Path("C:/Windows/Fonts") / filename),
        size,
    )


def largest_component(image: Image.Image) -> Image.Image:
    rgba = np.asarray(image.convert("RGBA"), dtype=np.uint8).copy()
    alpha = rgba[:, :, 3]
    labels, count = ndimage.label(alpha > 8)
    if count < 1:
        raise AssertionError("generated turret cell is empty")
    sizes = ndimage.sum(alpha > 8, labels, range(1, count + 1))
    largest = int(np.argmax(sizes)) + 1
    keep = ndimage.binary_dilation(labels == largest, iterations=2)
    rgba[~keep] = 0
    rgba[rgba[:, :, 3] < 3] = 0
    return Image.fromarray(rgba, "RGBA")


def split_source(source: Image.Image) -> list[Image.Image]:
    if source.width % GRID[0] or source.height % GRID[1]:
        raise AssertionError("generated source does not match the 4x2 grid")
    width = source.width // GRID[0]
    height = source.height // GRID[1]
    frames = []
    for index in range(8):
        column = index % GRID[0]
        row = index // GRID[0]
        frames.append(
            largest_component(
                source.crop(
                    (
                        column * width,
                        row * height,
                        (column + 1) * width,
                        (row + 1) * height,
                    )
                )
            )
        )
    return frames


def foundation_bbox(image: Image.Image) -> tuple[int, int, int, int]:
    rgba = np.asarray(image.convert("RGBA"), dtype=np.float32)
    red, green, blue, alpha = (rgba[:, :, index] for index in range(4))
    olive = (
        (alpha > 24)
        & (red > blue * 1.03)
        & (green > blue * 1.03)
        & (red > 38)
        & (green > 38)
        & (np.abs(red - green) < 72)
    )
    olive = ndimage.binary_closing(olive, iterations=3)
    labels, count = ndimage.label(olive)
    if count < 1:
        raise AssertionError("unable to locate turret foundation")
    sizes = ndimage.sum(olive, labels, range(1, count + 1))
    order = np.argsort(sizes)[::-1]
    combined = np.zeros_like(olive)
    for item in order[:6]:
        if sizes[item] < 80:
            continue
        combined |= labels == int(item + 1)
    ys, xs = np.nonzero(combined)
    if len(xs) < 100:
        raise AssertionError("turret foundation mask is too small")
    return int(xs.min()), int(ys.min()), int(xs.max() + 1), int(ys.max() + 1)


def subject_bbox(image: Image.Image) -> tuple[int, int, int, int]:
    box = image.getchannel("A").getbbox()
    if box is None:
        raise AssertionError("turret direction is empty")
    return box


def safe_foundation_width(frames: list[Image.Image]) -> float:
    allowed = DESIRED_FOUNDATION_WIDTH
    for image in frames:
        base = foundation_bbox(image)
        subject = subject_bbox(image)
        base_width = base[2] - base[0]
        center_x = (base[0] + base[2]) / 2.0
        center_y = (base[1] + base[3]) / 2.0
        extents = (
            center_x - subject[0],
            subject[2] - center_x,
            center_y - subject[1],
            subject[3] - center_y,
        )
        limits = (
            (FRAME[0] / 2 - MARGIN) * base_width / extents[0],
            (FRAME[0] / 2 - MARGIN) * base_width / extents[1],
            (FRAME[1] / 2 - MARGIN) * base_width / extents[2],
            (FRAME[1] / 2 - MARGIN) * base_width / extents[3],
        )
        allowed = min(allowed, *limits)
    return allowed


def assemble(frames: list[Image.Image]) -> tuple[Image.Image, float]:
    target_foundation_width = safe_foundation_width(frames)
    if target_foundation_width < 88:
        raise AssertionError(
            "generated barrel leaves insufficient room for the foundation"
        )

    atlas = Image.new("RGBA", ATLAS)
    for index, image in enumerate(frames):
        base = foundation_bbox(image)
        subject = subject_bbox(image)
        base_width = base[2] - base[0]
        scale = target_foundation_width / base_width
        cropped = image.crop(subject)
        size = (
            max(1, round(cropped.width * scale)),
            max(1, round(cropped.height * scale)),
        )
        cropped = cropped.resize(size, Image.Resampling.LANCZOS)
        base_center_in_crop = (
            ((base[0] + base[2]) / 2.0 - subject[0]) * scale,
            ((base[1] + base[3]) / 2.0 - subject[1]) * scale,
        )
        position = (
            round(FRAME[0] / 2 - base_center_in_crop[0]),
            round(index * FRAME[1] + FRAME[1] / 2 - base_center_in_crop[1]),
        )
        atlas.alpha_composite(cropped, position)
    return atlas, target_foundation_width


def atlas_frame(atlas: Image.Image, index: int) -> Image.Image:
    return atlas.crop(
        (
            0,
            index * FRAME[1],
            FRAME[0],
            (index + 1) * FRAME[1],
        )
    )


def turret_module_mask(frame: Image.Image) -> np.ndarray:
    rgba = np.asarray(frame.convert("RGBA"), dtype=np.float32)
    red, green, blue, alpha = (rgba[:, :, index] for index in range(4))
    return (
        (alpha > 24)
        & (blue > green * 1.02)
        & (blue > red * 0.96)
        & (blue > 45)
    )


def measure_barrel_reach(
    frame: Image.Image,
    direction_index: int,
) -> float:
    dx, dy = DIRECTION_VECTORS[direction_index]
    module = turret_module_mask(frame)
    yy, xx = np.indices(module.shape)
    offset_x = xx - FRAME[0] / 2
    offset_y = yy - FRAME[1] / 2
    forward = offset_x * dx + offset_y * dy
    perpendicular = np.abs(-offset_x * dy + offset_y * dx)
    samples = forward[
        module
        & (perpendicular < 14)
        & (forward > 0)
    ]
    if samples.size == 0:
        raise AssertionError("unable to measure gun barrel")
    return float(samples.max())


def transform_barrel_layer(
    layer: Image.Image,
    direction_index: int,
    scale: float,
    join_radius: float,
) -> Image.Image:
    dx, dy = DIRECTION_VECTORS[direction_index]
    inverse_scale = 1.0 / scale
    factor = inverse_scale - 1.0
    a = 1.0 + factor * dx * dx
    b = factor * dx * dy
    d = factor * dx * dy
    e = 1.0 + factor * dy * dy
    anchor_x = FRAME[0] / 2 + dx * join_radius
    anchor_y = FRAME[1] / 2 + dy * join_radius
    c = anchor_x - a * anchor_x - b * anchor_y
    f = anchor_y - d * anchor_x - e * anchor_y
    return layer.transform(
        FRAME,
        Image.Transform.AFFINE,
        (a, b, c, d, e, f),
        resample=Image.Resampling.BICUBIC,
    )


def normalize_barrel_lengths(atlas: Image.Image) -> Image.Image:
    frames = [atlas_frame(atlas, index) for index in range(8)]
    stack = np.stack(
        [np.asarray(frame.convert("RGBA"), dtype=np.float32) for frame in frames]
    )
    static_background = np.median(stack, axis=0)
    corrected = Image.new("RGBA", ATLAS)

    for index, frame in enumerate(frames):
        dx, dy = DIRECTION_VECTORS[index]
        join_radius = BARREL_JOIN_RADII[index]
        rgba = np.asarray(frame.convert("RGBA"), dtype=np.float32)
        module = turret_module_mask(frame)
        yy, xx = np.indices(module.shape)
        offset_x = xx - FRAME[0] / 2
        offset_y = yy - FRAME[1] / 2
        forward = offset_x * dx + offset_y * dy
        perpendicular = np.abs(-offset_x * dy + offset_y * dx)
        barrel = (
            module
            & (forward > join_radius - 2.0)
            & (perpendicular < 18.0)
        )
        barrel = ndimage.binary_closing(barrel, iterations=1)
        barrel = ndimage.binary_dilation(barrel, iterations=1)

        erase = ndimage.binary_dilation(barrel, iterations=2)
        erase_strength = ndimage.gaussian_filter(
            erase.astype(np.float32),
            0.8,
        )[:, :, None]
        base = (
            rgba * (1.0 - erase_strength)
            + static_background * erase_strength
        )

        soft_barrel = ndimage.gaussian_filter(
            barrel.astype(np.float32),
            0.45,
        )
        layer_rgba = rgba.copy()
        layer_rgba[:, :, 3] *= soft_barrel
        layer_rgba[layer_rgba[:, :, 3] < 1.0] = 0
        layer = Image.fromarray(
            np.clip(layer_rgba, 0, 255).astype(np.uint8),
            "RGBA",
        )

        source_reach = measure_barrel_reach(frame, index)
        source_length = source_reach - join_radius
        if source_length <= 1.0:
            raise AssertionError(
                f"barrel {DIRECTIONS[index]} is too short to normalize"
            )
        transformed = transform_barrel_layer(
            layer,
            index,
            BARREL_TARGET_VISIBLE_LENGTH / source_length,
            join_radius,
        )
        base_image = Image.fromarray(
            np.clip(base, 0, 255).astype(np.uint8),
            "RGBA",
        )
        base_image.alpha_composite(transformed)
        corrected.alpha_composite(base_image, (0, index * FRAME[1]))
    return corrected


def build_shadow(atlas: Image.Image) -> Image.Image:
    result = Image.new("RGBA", ATLAS)
    for index in range(8):
        frame = atlas_frame(atlas, index)
        alpha = frame.getchannel("A").filter(
            ImageFilter.GaussianBlur(1.5)
        ).point(lambda value: round(value * 0.18))
        shadow = Image.new("RGBA", FRAME, (7, 5, 3, 0))
        shadow.putalpha(alpha)
        shadow_frame = Image.new("RGBA", FRAME)
        shadow_frame.alpha_composite(shadow, (2, 2))
        result.alpha_composite(shadow_frame, (0, index * FRAME[1]))
    return result


def draw_card(
    board: Image.Image,
    sprite: Image.Image,
    x: int,
    y: int,
    size: int,
    label: str,
) -> None:
    draw = ImageDraw.Draw(board)
    draw.rounded_rectangle(
        (x, y, x + size, y + size + 34),
        radius=7,
        fill=(22, 26, 31, 255),
        outline=(138, 105, 48, 255),
        width=2,
    )
    board.alpha_composite(
        sprite.resize((size, size), Image.Resampling.LANCZOS),
        (x, y),
    )
    draw.text(
        (x + 8, y + size + 5),
        label,
        font=font(17, True),
        fill=(231, 214, 177, 255),
    )


def build_review(atlas: Image.Image) -> Image.Image:
    board = Image.new("RGBA", (1775, 735), (9, 12, 16, 255))
    draw = ImageDraw.Draw(board)
    draw.text(
        (34, 24),
        "Орудийная башня — 8 направлений",
        font=font(34, True),
        fill=(236, 219, 182, 255),
    )
    draw.text(
        (34, 70),
        "HD4: вертикальный атлас 128×1024; кадр 128×128",
        font=font(19),
        fill=(187, 193, 201, 255),
    )
    for index, direction in enumerate(DIRECTIONS):
        draw_card(
            board,
            atlas_frame(atlas, index),
            34 + index * 216,
            112,
            190,
            direction,
        )

    draw.text(
        (34, 365),
        "Сравнение размера и ориентации",
        font=font(25, True),
        fill=(225, 188, 98, 255),
    )
    classic = Image.open(CLASSIC).convert("RGBA")
    classic_ne = classic.crop((0, 32, 32, 64)).resize(
        FRAME,
        Image.Resampling.NEAREST,
    )
    draw_card(board, classic_ne, 34, 415, 200, "классика NE")
    draw_card(board, atlas_frame(atlas, 1), 270, 415, 200, "HD4 NE")
    draw.text(
        (515, 440),
        "• основание остаётся неподвижным\n"
        "• вращается только орудийный модуль\n"
        "• порядок E, NE, N, NW, W, SW, S, SE\n"
        "• контракт 32×32 и центральная ось сохранены",
        font=font(22),
        fill=(204, 208, 213, 255),
        spacing=14,
    )
    draw.text(
        (34, 703),
        "Предварительный просмотр — в игру не установлено.",
        font=font(19),
        fill=(188, 194, 202, 255),
    )
    return board


def build_rotation(atlas: Image.Image) -> None:
    frames = []
    for index in range(8):
        shown = Image.new("RGBA", (512, 512), (16, 20, 26, 255))
        shown.alpha_composite(
            atlas_frame(atlas, index).resize(
                (512, 512),
                Image.Resampling.LANCZOS,
            )
        )
        frames.append(shown.convert("P", palette=Image.Palette.ADAPTIVE))
    frames[0].save(
        ROTATION_OUT,
        save_all=True,
        append_images=frames[1:],
        duration=220,
        loop=0,
        disposal=2,
    )


def validate(
    atlas: Image.Image,
    shadow: Image.Image,
    hd2: Image.Image,
    target_foundation_width: float,
) -> dict[str, object]:
    for name, image in (("turret", atlas), ("shadow", shadow)):
        if image.size != ATLAS:
            raise AssertionError(f"{name} atlas size changed: {image.size}")
        if image.getchannel("A").getbbox() is None:
            raise AssertionError(f"{name} atlas is empty")

    frames = [atlas_frame(atlas, index) for index in range(8)]
    if len({frame.tobytes() for frame in frames}) != 8:
        raise AssertionError("turret directions are not unique")

    frame_boxes = {}
    base_boxes = {}
    for index, image in enumerate(frames):
        box = subject_bbox(image)
        shadow_box = subject_bbox(atlas_frame(shadow, index))
        if (
            box[0] < 2
            or box[1] < 2
            or box[2] > 126
            or box[3] > 126
        ):
            raise AssertionError(
                f"{DIRECTIONS[index]} touches boundary: {box}"
            )
        if (
            shadow_box[0] < 1
            or shadow_box[1] < 1
            or shadow_box[2] > 127
            or shadow_box[3] > 127
        ):
            raise AssertionError(
                f"{DIRECTIONS[index]} shadow touches boundary: {shadow_box}"
            )
        frame_boxes[DIRECTIONS[index]] = list(box)
        base_boxes[DIRECTIONS[index]] = list(foundation_bbox(image))

    widths = [box[2] - box[0] for box in base_boxes.values()]
    centers = [
        ((box[0] + box[2]) / 2.0, (box[1] + box[3]) / 2.0)
        for box in base_boxes.values()
    ]
    if max(widths) - min(widths) > 4:
        raise AssertionError(f"foundation width is unstable: {widths}")
    if max(x for x, _ in centers) - min(x for x, _ in centers) > 3:
        raise AssertionError(f"foundation X center is unstable: {centers}")
    if max(y for _, y in centers) - min(y for _, y in centers) > 3:
        raise AssertionError(f"foundation Y center is unstable: {centers}")

    expected_hd2 = atlas.resize((64, 512), Image.Resampling.LANCZOS)
    if ImageChops.difference(hd2, expected_hd2).getbbox():
        raise AssertionError("HD2 is not the deterministic HD4 derivative")

    barrel_tips = [
        measure_barrel_reach(frame, index)
        for index, frame in enumerate(frames)
    ]
    visible_barrel_lengths = [
        tip - join
        for tip, join in zip(
            barrel_tips,
            BARREL_JOIN_RADII,
            strict=True,
        )
    ]
    barrel_spread = (
        max(visible_barrel_lengths) - min(visible_barrel_lengths)
    )
    if barrel_spread > 2.0:
        raise AssertionError(
            "visible barrel length remains inconsistent: "
            f"{visible_barrel_lengths}"
        )

    return {
        "resources": {
            "turret": {"id": 38, "name": "BUILD_TURRET"},
            "shadow": {"id": 39, "name": "BUILD_TURRET_SHADOW"},
        },
        "direction_order": list(DIRECTIONS),
        "logical_frame": [32, 32],
        "classic_atlas": [32, 256],
        "hd2_frame": [64, 64],
        "hd2_atlas": [64, 512],
        "hd4_frame": list(FRAME),
        "hd4_atlas": list(ATLAS),
        "frames": 8,
        "frame_boxes_hd4": frame_boxes,
        "foundation_boxes_hd4": base_boxes,
        "target_foundation_width_hd4": round(target_foundation_width, 3),
        "barrel_join_radii_hd4": list(BARREL_JOIN_RADII),
        "barrel_tip_radii_hd4": [
            round(value, 3) for value in barrel_tips
        ],
        "visible_barrel_lengths_hd4": [
            round(value, 3) for value in visible_barrel_lengths
        ],
        "visible_barrel_length_spread_hd4": round(barrel_spread, 3),
        "pivot_hd4": [64, 64],
        "pivot_logical": [16, 16],
    }


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    source = Image.open(SOURCE).convert("RGBA")
    source_frames = split_source(source)
    atlas, target_foundation_width = assemble(source_frames)
    atlas = normalize_barrel_lengths(atlas)
    shadow = build_shadow(atlas)
    hd2 = atlas.resize((64, 512), Image.Resampling.LANCZOS)
    validation = validate(atlas, shadow, hd2, target_foundation_width)

    atlas.save(ATLAS_OUT, optimize=True)
    shadow.save(SHADOW_OUT, optimize=True)
    hd2.save(HD2_OUT, optimize=True)
    build_review(atlas).save(REVIEW_OUT, optimize=True)
    build_rotation(atlas)

    manifest = {
        "format": 1,
        "status": "preview_not_integrated",
        "source_reference": str(OUTPUT / "user_reference.png"),
        "generation_source": str(OUTPUT / "turret_chroma_v3.png"),
        "validation": validation,
    }
    (OUTPUT / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(manifest, ensure_ascii=False))


if __name__ == "__main__":
    main()
