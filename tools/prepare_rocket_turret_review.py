#!/usr/bin/env python3
"""Build an approval-ready HD4 rocket-turret direction atlas."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from scipy import ndimage


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts" / "rocket_turret_review_v1"
CLASSIC = (
    ROOT
    / "resources"
    / "hd"
    / "classic"
    / "sdl_data"
    / "0032_BUILD_RTURRET.png"
)
GUN_TURRET = (
    ROOT
    / "artifacts"
    / "gun_turret_review_v1"
    / "BUILD_TURRET_HD4_PREVIEW.png"
)
DIRECTIONS = ("E", "NE", "N", "NW", "W", "SW", "S", "SE")
MODULE_SOURCE_OVERRIDES = {
    "E": "module_E_alpha_v2.png",
    "SW": "module_SW_alpha_v2.png",
    "SE": "module_SE_alpha_v2.png",
}
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
PIVOT = (64.0, 64.0)
CLASSIC_EXTENT_SCALE = 0.82

ATLAS_OUT = OUTPUT / "BUILD_RTURRET_HD4_PREVIEW.png"
SHADOW_OUT = OUTPUT / "BUILD_RTURRET_SHADOW_HD4_PREVIEW.png"
HD2_OUT = OUTPUT / "BUILD_RTURRET_HD2_PREVIEW.png"
REVIEW_OUT = OUTPUT / "BUILD_RTURRET_REVIEW.png"
ROTATION_OUT = OUTPUT / "BUILD_RTURRET_ROTATION_PREVIEW.gif"


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
        raise AssertionError("generated rocket module is empty")
    sizes = ndimage.sum(alpha > 8, labels, range(1, count + 1))
    largest = int(np.argmax(sizes)) + 1
    keep = ndimage.binary_dilation(labels == largest, iterations=2)
    rgba[~keep] = 0
    rgba[rgba[:, :, 3] < 3] = 0
    return Image.fromarray(rgba, "RGBA")


def module_pivot(image: Image.Image) -> tuple[float, float]:
    rgba = np.asarray(image.convert("RGBA"), dtype=np.uint8)
    red, green, blue, alpha = (rgba[:, :, index] for index in range(4))
    cyan = (
        (alpha > 80)
        & (blue > 130)
        & (green > 115)
        & (blue.astype(np.float32) > red * 1.15)
        & (green.astype(np.float32) > red * 1.10)
    )
    labels, count = ndimage.label(cyan)
    image_center = np.array([image.width / 2.0, image.height / 2.0])
    centers: list[tuple[int, float, float]] = []
    for label_id in range(1, count + 1):
        yy, xx = np.nonzero(labels == label_id)
        if xx.size < 12:
            continue
        center = np.array([float(xx.mean()), float(yy.mean())])
        if np.linalg.norm(center - image_center) <= 150.0:
            centers.append(
                (int(xx.size), float(center[0]), float(center[1]))
            )
    if not centers:
        box = image.getchannel("A").getbbox()
        if box is None:
            raise AssertionError("empty rocket module")
        return (
            (box[0] + box[2]) / 2.0,
            (box[1] + box[3]) / 2.0,
        )
    strongest = sorted(centers, reverse=True)[:3]
    return (
        float(np.median([center[1] for center in strongest])),
        float(np.median([center[2] for center in strongest])),
    )


def oriented_extents(
    image: Image.Image,
    direction_index: int,
) -> tuple[float, float]:
    alpha = np.asarray(image.convert("RGBA"))[:, :, 3]
    yy, xx = np.nonzero(alpha > 24)
    if xx.size == 0:
        raise AssertionError("empty rocket-turret frame")
    dx, dy = DIRECTION_VECTORS[direction_index]
    forward = xx * dx + yy * dy
    lateral = -xx * dy + yy * dx
    return (
        float(forward.max() - forward.min() + 1.0),
        float(lateral.max() - lateral.min() + 1.0),
    )


def classic_frame(classic: Image.Image, index: int) -> Image.Image:
    return classic.crop((0, index * 32, 32, (index + 1) * 32))


def transform_module(
    image: Image.Image,
    direction_index: int,
    source_pivot: tuple[float, float],
    target_extents: tuple[float, float],
) -> Image.Image:
    source_forward, source_lateral = oriented_extents(
        image,
        direction_index,
    )
    forward_scale = target_extents[0] / source_forward
    lateral_scale = target_extents[1] / source_lateral
    dx, dy = DIRECTION_VECTORS[direction_index]
    inverse_forward = 1.0 / forward_scale
    inverse_lateral = 1.0 / lateral_scale
    a = inverse_forward * dx * dx + inverse_lateral * dy * dy
    b = (inverse_forward - inverse_lateral) * dx * dy
    d = b
    e = inverse_forward * dy * dy + inverse_lateral * dx * dx
    c = source_pivot[0] - a * PIVOT[0] - b * PIVOT[1]
    f = source_pivot[1] - d * PIVOT[0] - e * PIVOT[1]
    return image.transform(
        FRAME,
        Image.Transform.AFFINE,
        (a, b, c, d, e, f),
        resample=Image.Resampling.BICUBIC,
    )


def static_foundation() -> Image.Image:
    gun = Image.open(GUN_TURRET).convert("RGBA")
    if gun.size != ATLAS:
        raise AssertionError(f"unexpected gun-turret atlas: {gun.size}")
    frames = [
        np.asarray(
            gun.crop((0, index * 128, 128, (index + 1) * 128)),
            dtype=np.float32,
        )
        for index in range(8)
    ]
    median = np.median(np.stack(frames), axis=0)
    return Image.fromarray(
        np.clip(median, 0, 255).astype(np.uint8),
        "RGBA",
    )


def assemble() -> tuple[Image.Image, Image.Image]:
    classic = Image.open(CLASSIC).convert("RGBA")
    foundation = static_foundation()
    atlas = Image.new("RGBA", ATLAS)
    modules = Image.new("RGBA", ATLAS)
    for index, direction in enumerate(DIRECTIONS):
        source_name = MODULE_SOURCE_OVERRIDES.get(
            direction,
            f"module_{direction}_alpha.png",
        )
        source = largest_component(
            Image.open(OUTPUT / source_name).convert("RGBA")
        )
        classic_forward, classic_lateral = oriented_extents(
            classic_frame(classic, index),
            index,
        )
        module = transform_module(
            source,
            index,
            module_pivot(source),
            (
                classic_forward * 4.0 * CLASSIC_EXTENT_SCALE,
                classic_lateral * 4.0 * CLASSIC_EXTENT_SCALE,
            ),
        )
        frame = foundation.copy()
        frame.alpha_composite(module)
        atlas.alpha_composite(frame, (0, index * 128))
        modules.alpha_composite(module, (0, index * 128))
    return atlas, modules


def build_shadow(atlas: Image.Image) -> Image.Image:
    result = Image.new("RGBA", ATLAS)
    for index in range(8):
        frame = atlas.crop((0, index * 128, 128, (index + 1) * 128))
        alpha = frame.getchannel("A").filter(
            ImageFilter.GaussianBlur(1.5)
        ).point(lambda value: round(value * 0.18))
        shadow = Image.new("RGBA", FRAME, (7, 5, 3, 0))
        shadow.putalpha(alpha)
        shifted = Image.new("RGBA", FRAME)
        shifted.alpha_composite(shadow, (2, 2))
        result.alpha_composite(shifted, (0, index * 128))
    return result


def atlas_frame(atlas: Image.Image, index: int) -> Image.Image:
    return atlas.crop((0, index * 128, 128, (index + 1) * 128))


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
        "Ракетная башня — 8 направлений",
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
    classic_ne = classic_frame(classic, 1).resize(
        FRAME,
        Image.Resampling.NEAREST,
    )
    draw_card(board, classic_ne, 34, 415, 200, "классика NE")
    draw_card(board, atlas_frame(atlas, 1), 270, 415, 200, "HD4 NE")
    draw.text(
        (515, 440),
        "• платформа неподвижна во всех кадрах\n"
        "• вращаются два контейнера и центральный модуль\n"
        "• порядок E, NE, N, NW, W, SW, S, SE\n"
        "• передние и задние торцы контейнеров различаются",
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
    modules: Image.Image,
    shadow: Image.Image,
    hd2: Image.Image,
) -> dict[str, object]:
    if atlas.size != ATLAS or shadow.size != ATLAS:
        raise AssertionError("rocket-turret atlas dimensions changed")
    if hd2.size != (64, 512):
        raise AssertionError("rocket-turret HD2 dimensions changed")
    frames = [atlas_frame(atlas, index) for index in range(8)]
    if len({frame.tobytes() for frame in frames}) != 8:
        raise AssertionError("rocket-turret directions are not unique")

    module_boxes = {}
    for index, direction in enumerate(DIRECTIONS):
        module = atlas_frame(modules, index)
        box = module.getchannel("A").getbbox()
        if (
            box is None
            or box[0] < 2
            or box[1] < 2
            or box[2] > 126
            or box[3] > 126
        ):
            raise AssertionError(
                f"{direction} module touches frame boundary: {box}"
            )
        module_boxes[direction] = list(box)

    foundation = static_foundation()
    if foundation.getchannel("A").getbbox() is None:
        raise AssertionError("static foundation is empty")

    return {
        "resources": {
            "turret": {"id": 32, "name": "BUILD_RTURRET"},
            "shadow": {"id": 33, "name": "BUILD_RTURRET_SHADOW"},
        },
        "direction_order": list(DIRECTIONS),
        "frames": 8,
        "logical_frame": [32, 32],
        "classic_atlas": [32, 256],
        "hd2_atlas": [64, 512],
        "hd4_atlas": list(ATLAS),
        "pivot_hd4": [64, 64],
        "pivot_logical": [16, 16],
        "module_boxes_hd4": module_boxes,
    }


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    atlas, modules = assemble()
    shadow = build_shadow(atlas)
    hd2 = atlas.resize((64, 512), Image.Resampling.LANCZOS)
    validation = validate(atlas, modules, shadow, hd2)

    atlas.save(ATLAS_OUT, optimize=True)
    shadow.save(SHADOW_OUT, optimize=True)
    hd2.save(HD2_OUT, optimize=True)
    build_review(atlas).save(REVIEW_OUT, optimize=True)
    build_rotation(atlas)
    manifest = {
        "format": 1,
        "status": "preview_not_integrated",
        "source_reference": str(OUTPUT / "user_reference.png"),
        "generation_mode": "built-in imagegen, per-direction",
        "validation": validation,
    }
    (OUTPUT / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(manifest, ensure_ascii=False))


if __name__ == "__main__":
    main()
