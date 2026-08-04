#!/usr/bin/env python3
"""Build approval-ready HD barracks and two animated House flags."""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from scipy import ndimage


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts" / "barracks_review_v1"
SOURCE = OUTPUT / "barracks_alpha.png"
FLAGS_SOURCE = OUTPUT / "twin_flags_alpha.png"
CLASSIC = (
    ROOT / "resources" / "hd" / "classic" / "sdl_data"
    / "0001_BUILD_BARRACKS.png"
)

FRAME = (256, 256)
LOGICAL_FRAME = (64, 64)
FLAG_FRAMES = 8
FLAG_ASSEMBLY_SIZE = (70, 76)
FLAG_POSITION = (180, 172)

BUILDING_OUT = OUTPUT / "BUILD_BARRACKS_HD4_PREVIEW.png"
SHADOW_OUT = OUTPUT / "BUILD_BARRACKS_SHADOW_HD4_PREVIEW.png"
FLAG_OUT = OUTPUT / "BUILD_BARRACKS_FLAG_HD4_PREVIEW.png"
FLAG_MASK_OUT = OUTPUT / "HM_BUILD_BARRACKS_FLAG_HD4_PREVIEW.png"
BUILDING_HD2_OUT = OUTPUT / "BUILD_BARRACKS_HD2_PREVIEW.png"
SHADOW_HD2_OUT = OUTPUT / "BUILD_BARRACKS_SHADOW_HD2_PREVIEW.png"
FLAG_HD2_OUT = OUTPUT / "BUILD_BARRACKS_FLAG_HD2_PREVIEW.png"
FLAG_MASK_HD2_OUT = OUTPUT / "HM_BUILD_BARRACKS_FLAG_HD2_PREVIEW.png"
REVIEW_OUT = OUTPUT / "BUILD_BARRACKS_REVIEW.png"
ANIMATION_OUT = OUTPUT / "BUILD_BARRACKS_ANIMATION_PREVIEW.gif"

HOUSE_COLORS = {
    "Харконнены": (255, 0, 0),
    "Атрейдесы": (0, 90, 255),
    "Ордос": (0, 255, 0),
}


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    filename = "arialbd.ttf" if bold else "arial.ttf"
    return ImageFont.truetype(str(Path("C:/Windows/Fonts") / filename), size)


def fit_building(source: Image.Image) -> Image.Image:
    box = source.getchannel("A").getbbox()
    if box is None:
        raise AssertionError("generated barracks are transparent")
    subject = source.crop(box)
    max_size = (244, 240)
    scale = min(max_size[0] / subject.width, max_size[1] / subject.height)
    size = (
        round(subject.width * scale),
        round(subject.height * scale),
    )
    subject = subject.resize(size, Image.Resampling.LANCZOS)
    frame = Image.new("RGBA", FRAME)
    frame.alpha_composite(
        subject,
        (
            (FRAME[0] - subject.width) // 2,
            FRAME[1] - subject.height - 8,
        ),
    )
    return frame


def split_flag_assembly(
    source: Image.Image,
) -> tuple[Image.Image, Image.Image]:
    box = source.getchannel("A").getbbox()
    if box is None:
        raise AssertionError("generated twin flags are transparent")
    subject = source.crop(box).convert("RGBA")
    rgba = np.asarray(subject, dtype=np.uint8).copy()
    red, green, blue, alpha = (rgba[:, :, index] for index in range(4))
    green_fabric = (
        (alpha > 6)
        & (green > 55)
        & (green.astype(np.float32) > red * 1.24)
        & (green.astype(np.float32) > blue * 1.16)
    )
    green_fabric = ndimage.binary_dilation(green_fabric, iterations=2)
    fabric_rgba = rgba.copy()
    fabric_rgba[:, :, 3] = np.where(
        green_fabric,
        rgba[:, :, 3],
        0,
    )
    poles_rgba = rgba.copy()
    poles_rgba[green_fabric] = 0
    fabric = Image.fromarray(fabric_rgba, "RGBA").resize(
        FLAG_ASSEMBLY_SIZE,
        Image.Resampling.LANCZOS,
    )
    poles = Image.fromarray(poles_rgba, "RGBA").resize(
        FLAG_ASSEMBLY_SIZE,
        Image.Resampling.LANCZOS,
    )
    return poles, fabric


def wave_component(component: Image.Image, phase: int) -> Image.Image:
    source = np.asarray(component.convert("RGBA"), dtype=np.float32)
    height, width = source.shape[:2]
    output = np.zeros_like(source)
    phase_angle = phase * 2.0 * math.pi / FLAG_FRAMES
    for x in range(width):
        distance_from_pole = (width - 1 - x) / max(1, width - 1)
        shift = (
            1.8
            * distance_from_pole
            * math.sin(
                phase_angle + x / max(1, width - 1) * math.pi * 1.7
            )
        )
        for y in range(height):
            source_y = y - shift
            lower = math.floor(source_y)
            upper = lower + 1
            fraction = source_y - lower
            if 0 <= lower < height:
                output[y, x] += source[lower, x] * (1.0 - fraction)
            if 0 <= upper < height:
                output[y, x] += source[upper, x] * fraction
    return Image.fromarray(
        np.clip(output, 0, 255).astype(np.uint8),
        "RGBA",
    )


def wave_fabrics(fabric: Image.Image, phase: int) -> Image.Image:
    alpha = np.asarray(fabric.getchannel("A"), dtype=np.uint8)
    labels, count = ndimage.label(alpha > 8)
    components = []
    for label_id in range(1, count + 1):
        ys, xs = np.nonzero(labels == label_id)
        if len(xs) >= 20:
            components.append((len(xs), label_id, xs, ys))
    components.sort(reverse=True)
    if len(components) < 2:
        raise AssertionError("unable to separate two flag fabrics")

    result = Image.new("RGBA", fabric.size)
    for offset, (_, label_id, xs, ys) in enumerate(components[:2]):
        margin = 2
        box = (
            max(0, int(xs.min()) - margin),
            max(0, int(ys.min()) - margin),
            min(fabric.width, int(xs.max()) + margin + 1),
            min(fabric.height, int(ys.max()) + margin + 1),
        )
        component_mask = Image.fromarray(
            np.where(labels == label_id, 255, 0).astype(np.uint8),
            "L",
        ).crop(box)
        piece = fabric.crop(box)
        piece.putalpha(
            Image.fromarray(
                np.minimum(
                    np.asarray(piece.getchannel("A"), dtype=np.uint8),
                    np.asarray(component_mask, dtype=np.uint8),
                ),
                "L",
            )
        )
        result.alpha_composite(
            wave_component(piece, (phase + offset * 2) % FLAG_FRAMES),
            (box[0], box[1]),
        )
    return result


def build_flag_atlases(
    poles: Image.Image,
    fabric: Image.Image,
) -> tuple[Image.Image, Image.Image]:
    atlas_size = (FRAME[0], FRAME[1] * FLAG_FRAMES)
    atlas = Image.new("RGBA", atlas_size)
    mask_atlas = Image.new("RGBA", atlas_size)
    for phase in range(FLAG_FRAMES):
        waved = wave_fabrics(fabric, phase)
        frame = Image.new("RGBA", FRAME)
        frame.alpha_composite(poles, FLAG_POSITION)
        frame.alpha_composite(waved, FLAG_POSITION)
        atlas.alpha_composite(frame, (0, phase * FRAME[1]))

        mask_piece = Image.new("RGBA", waved.size, (255, 255, 255, 0))
        mask_piece.putalpha(waved.getchannel("A"))
        mask_frame = Image.new("RGBA", FRAME)
        mask_frame.alpha_composite(mask_piece, FLAG_POSITION)
        mask_atlas.alpha_composite(mask_frame, (0, phase * FRAME[1]))
    return atlas, mask_atlas


def build_shadow(building: Image.Image) -> Image.Image:
    alpha = building.getchannel("A").filter(ImageFilter.GaussianBlur(1.5))
    alpha = alpha.point(lambda value: round(value * 0.17))
    silhouette = Image.new("RGBA", FRAME, (7, 5, 3, 0))
    silhouette.putalpha(alpha)
    result = Image.new("RGBA", FRAME)
    result.alpha_composite(silhouette, (2, 2))
    return result


def flag_frame(atlas: Image.Image, phase: int) -> Image.Image:
    return atlas.crop(
        (0, phase * FRAME[1], FRAME[0], (phase + 1) * FRAME[1])
    )


def apply_engine_tint(
    image: Image.Image,
    mask: Image.Image,
    color: tuple[int, int, int],
) -> Image.Image:
    rgba = np.asarray(image.convert("RGBA"), dtype=np.float32).copy()
    mask_rgba = np.asarray(mask.convert("RGBA"), dtype=np.float32)
    strength = (
        mask_rgba[:, :, 3] / 255.0
        * np.max(mask_rgba[:, :, :3], axis=2) / 255.0
    )
    luminance = (
        0.299 * rgba[:, :, 0]
        + 0.587 * rgba[:, :, 1]
        + 0.114 * rgba[:, :, 2]
    ) / 128.0
    for channel, target in enumerate(color):
        colored = np.minimum(255.0, target * luminance)
        rgba[:, :, channel] = (
            rgba[:, :, channel] * (1.0 - strength)
            + colored * strength
        )
    return Image.fromarray(
        np.clip(rgba, 0, 255).astype(np.uint8),
        "RGBA",
    )


def composed(
    building: Image.Image,
    flag_atlas: Image.Image,
    mask_atlas: Image.Image,
    phase: int,
    color: tuple[int, int, int],
) -> Image.Image:
    result = building.copy()
    result.alpha_composite(
        apply_engine_tint(
            flag_frame(flag_atlas, phase),
            flag_frame(mask_atlas, phase),
            color,
        )
    )
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
        (x, y, x + size, y + size + 36),
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
        (x + 8, y + size + 6),
        label,
        font=font(17, True),
        fill=(231, 214, 177, 255),
    )


def build_review(
    building: Image.Image,
    flag_atlas: Image.Image,
    mask_atlas: Image.Image,
) -> Image.Image:
    board = Image.new("RGBA", (1760, 1260), (9, 12, 16, 255))
    draw = ImageDraw.Draw(board)
    draw.text(
        (34, 24),
        "Казармы — HD4",
        font=font(34, True),
        fill=(236, 219, 182, 255),
    )
    draw.text(
        (34, 69),
        "Корпус 64×64; две штатные точки флагов, 8 фаз",
        font=font(19),
        fill=(187, 193, 201, 255),
    )

    for phase in range(FLAG_FRAMES):
        draw_card(
            board,
            composed(
                building,
                flag_atlas,
                mask_atlas,
                phase,
                HOUSE_COLORS["Ордос"],
            ),
            34 + phase * 214,
            108,
            188,
            f"фаза {phase}",
        )

    draw.text(
        (34, 350),
        "Цвет Дома применяется только к двум тканям",
        font=font(25, True),
        fill=(225, 188, 98, 255),
    )
    for index, (name, color) in enumerate(HOUSE_COLORS.items()):
        draw_card(
            board,
            composed(
                building,
                flag_atlas,
                mask_atlas,
                2 + index * 2,
                color,
            ),
            34 + index * 330,
            395,
            300,
            name,
        )
    draw_card(board, building, 1024, 395, 300, "корпус без флагов")
    draw_card(
        board,
        flag_frame(mask_atlas, 0),
        1354,
        395,
        300,
        "маска тканей",
    )

    draw.text(
        (34, 785),
        "Размер и привязка к исходному атласу",
        font=font(25, True),
        fill=(225, 188, 98, 255),
    )
    classic = Image.open(CLASSIC).convert("RGBA")
    draw_card(board, classic, 34, 830, 350, "классика 64×64")
    draw_card(
        board,
        composed(
            building,
            flag_atlas,
            mask_atlas,
            0,
            HOUSE_COLORS["Ордос"],
        ),
        420,
        830,
        350,
        "HD4 256×256",
    )
    draw.text(
        (820, 870),
        "• исходная площадь 2×2 клетки\n"
        "• один неподвижный кадр корпуса\n"
        "• сохранена трёхмодульная компоновка\n"
        "• две точки флагов в нижней правой зоне\n"
        "• 8 уникальных фаз без изменения габаритов\n"
        "• отдельная детерминированная тень",
        font=font(23),
        fill=(204, 208, 213, 255),
        spacing=16,
    )
    draw.text(
        (34, 1210),
        "Предварительный просмотр — в игру не установлено.",
        font=font(20),
        fill=(188, 194, 202, 255),
    )
    return board


def build_animation(
    building: Image.Image,
    flag_atlas: Image.Image,
    mask_atlas: Image.Image,
) -> None:
    frames = []
    for phase in range(FLAG_FRAMES):
        sprite = composed(
            building,
            flag_atlas,
            mask_atlas,
            phase,
            HOUSE_COLORS["Ордос"],
        )
        shown = Image.new("RGBA", (512, 512), (16, 20, 26, 255))
        shown.alpha_composite(
            sprite.resize((512, 512), Image.Resampling.LANCZOS)
        )
        frames.append(
            shown.convert("P", palette=Image.Palette.ADAPTIVE)
        )
    frames[0].save(
        ANIMATION_OUT,
        save_all=True,
        append_images=frames[1:],
        duration=125,
        loop=0,
        disposal=2,
    )


def validate(
    building: Image.Image,
    shadow: Image.Image,
    flag_atlas: Image.Image,
    mask_atlas: Image.Image,
) -> dict[str, object]:
    if building.size != FRAME or shadow.size != FRAME:
        raise AssertionError("building or shadow dimensions changed")
    expected_atlas = (FRAME[0], FRAME[1] * FLAG_FRAMES)
    if flag_atlas.size != expected_atlas or mask_atlas.size != expected_atlas:
        raise AssertionError("flag atlas dimensions changed")

    building_box = building.getchannel("A").getbbox()
    shadow_box = shadow.getchannel("A").getbbox()
    for name, box in (
        ("building", building_box),
        ("shadow", shadow_box),
    ):
        if (
            box is None
            or box[0] < 1
            or box[1] < 1
            or box[2] > 255
            or box[3] > 255
        ):
            raise AssertionError(f"{name} touches boundary: {box}")

    flag_frames = [
        flag_frame(flag_atlas, phase) for phase in range(FLAG_FRAMES)
    ]
    if len({item.tobytes() for item in flag_frames}) != FLAG_FRAMES:
        raise AssertionError("flag animation phases are not unique")
    flag_boxes = []
    for phase, item in enumerate(flag_frames):
        box = item.getchannel("A").getbbox()
        if (
            box is None
            or box[0] < 1
            or box[1] < 1
            or box[2] > 255
            or box[3] > 255
        ):
            raise AssertionError(
                f"flag phase {phase} touches boundary: {box}"
            )
        flag_boxes.append(list(box))

    return {
        "resources": {
            "building": {"id": 1, "name": "BUILD_BARRACKS"},
            "shadow": {"id": 2, "name": "BUILD_BARRACKS_SHADOW"},
            "flag": "BUILD_BARRACKS_FLAG",
            "flag_mask": "HM_BUILD_BARRACKS_FLAG",
        },
        "logical_frame": list(LOGICAL_FRAME),
        "hd2_frame": [128, 128],
        "hd4_frame": list(FRAME),
        "footprint": [2, 2],
        "building_frames": 1,
        "flag_frames": FLAG_FRAMES,
        "original_flag_points": [[60, 47], [51, 50]],
        "building_box_hd4": list(building_box),
        "shadow_box_hd4": list(shadow_box),
        "flag_boxes_hd4": flag_boxes,
        "flag_position_hd4": list(FLAG_POSITION),
    }


def main() -> None:
    for path in (SOURCE, FLAGS_SOURCE, CLASSIC):
        if not path.is_file():
            raise FileNotFoundError(path)

    building = fit_building(Image.open(SOURCE).convert("RGBA"))
    poles, fabric = split_flag_assembly(
        Image.open(FLAGS_SOURCE).convert("RGBA")
    )
    flag_atlas, mask_atlas = build_flag_atlases(poles, fabric)
    shadow = build_shadow(building)
    validation = validate(building, shadow, flag_atlas, mask_atlas)

    building.save(BUILDING_OUT, optimize=True)
    shadow.save(SHADOW_OUT, optimize=True)
    flag_atlas.save(FLAG_OUT, optimize=True)
    mask_atlas.save(FLAG_MASK_OUT, optimize=True)
    building.resize((128, 128), Image.Resampling.LANCZOS).save(
        BUILDING_HD2_OUT,
        optimize=True,
    )
    shadow.resize((128, 128), Image.Resampling.LANCZOS).save(
        SHADOW_HD2_OUT,
        optimize=True,
    )
    flag_atlas.resize((128, 1024), Image.Resampling.LANCZOS).save(
        FLAG_HD2_OUT,
        optimize=True,
    )
    mask_atlas.resize((128, 1024), Image.Resampling.LANCZOS).save(
        FLAG_MASK_HD2_OUT,
        optimize=True,
    )
    build_review(building, flag_atlas, mask_atlas).save(
        REVIEW_OUT,
        optimize=True,
    )
    build_animation(building, flag_atlas, mask_atlas)
    manifest = {
        "format": 1,
        "status": "preview_not_integrated",
        "source_reference": str(OUTPUT / "user_reference.png"),
        "generation_mode": "built-in imagegen plus deterministic flags",
        "validation": validation,
    }
    (OUTPUT / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(manifest, ensure_ascii=False))


if __name__ == "__main__":
    main()
