#!/usr/bin/env python3
"""Build an approval-ready HD spice silo and animated House flag."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts" / "silo_review_v1"
SOURCE = OUTPUT / "silo_alpha.png"
CLASSIC = (
    ROOT / "resources" / "hd" / "classic" / "sdl_data"
    / "0034_BUILD_SILO.png"
)
WINDTRAP_FLAG = (
    ROOT / "artifacts" / "windtrap_review_v1"
    / "BUILD_WINDTRAP_FLAG_HD4_PREVIEW.png"
)
WINDTRAP_MASK = (
    ROOT / "artifacts" / "windtrap_review_v1"
    / "HM_BUILD_WINDTRAP_FLAG_HD4_PREVIEW.png"
)

FRAME = (256, 256)
LOGICAL_FRAME = (64, 64)
FLAG_FRAMES = 8
FLAG_SOURCE_BOX = (172, 117, 214, 144)
FLAG_SIZE = (38, 24)
FLAG_ATTACH = (180, 96)

BUILDING_OUT = OUTPUT / "BUILD_SILO_HD4_PREVIEW.png"
SHADOW_OUT = OUTPUT / "BUILD_SILO_SHADOW_HD4_PREVIEW.png"
FLAG_OUT = OUTPUT / "BUILD_SILO_FLAG_HD4_PREVIEW.png"
FLAG_MASK_OUT = OUTPUT / "HM_BUILD_SILO_FLAG_HD4_PREVIEW.png"
BUILDING_HD2_OUT = OUTPUT / "BUILD_SILO_HD2_PREVIEW.png"
SHADOW_HD2_OUT = OUTPUT / "BUILD_SILO_SHADOW_HD2_PREVIEW.png"
FLAG_HD2_OUT = OUTPUT / "BUILD_SILO_FLAG_HD2_PREVIEW.png"
FLAG_MASK_HD2_OUT = OUTPUT / "HM_BUILD_SILO_FLAG_HD2_PREVIEW.png"
REVIEW_OUT = OUTPUT / "BUILD_SILO_REVIEW.png"
ANIMATION_OUT = OUTPUT / "BUILD_SILO_ANIMATION_PREVIEW.gif"

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
        raise AssertionError("generated spice silo is transparent")
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


def flag_frame(atlas: Image.Image, phase: int) -> Image.Image:
    return atlas.crop(
        (0, phase * FRAME[1], FRAME[0], (phase + 1) * FRAME[1])
    )


def build_flag_atlases() -> tuple[Image.Image, Image.Image]:
    source = Image.open(WINDTRAP_FLAG).convert("RGBA")
    source_mask = Image.open(WINDTRAP_MASK).convert("RGBA")
    expected_size = (FRAME[0], FRAME[1] * FLAG_FRAMES)
    if source.size != expected_size or source_mask.size != expected_size:
        raise AssertionError("approved wind-trap flag contract changed")

    atlas = Image.new("RGBA", expected_size)
    mask_atlas = Image.new("RGBA", expected_size)
    position = (
        FLAG_ATTACH[0] - FLAG_SIZE[0] + 2,
        FLAG_ATTACH[1] - FLAG_SIZE[1] // 2,
    )
    for phase in range(FLAG_FRAMES):
        y = phase * FRAME[1]
        source_box = tuple(
            value + (y if index % 2 else 0)
            for index, value in enumerate(FLAG_SOURCE_BOX)
        )
        fabric = source.crop(source_box).resize(
            FLAG_SIZE,
            Image.Resampling.LANCZOS,
        )
        fabric_mask = source_mask.crop(source_box).resize(
            FLAG_SIZE,
            Image.Resampling.LANCZOS,
        )
        frame = Image.new("RGBA", FRAME)
        mask_frame = Image.new("RGBA", FRAME)
        frame.alpha_composite(fabric, position)
        mask_frame.alpha_composite(fabric_mask, position)
        atlas.alpha_composite(frame, (0, y))
        mask_atlas.alpha_composite(mask_frame, (0, y))
    return atlas, mask_atlas


def build_shadow(building: Image.Image) -> Image.Image:
    alpha = building.getchannel("A").filter(ImageFilter.GaussianBlur(1.5))
    alpha = alpha.point(lambda value: round(value * 0.17))
    silhouette = Image.new("RGBA", FRAME, (7, 5, 3, 0))
    silhouette.putalpha(alpha)
    result = Image.new("RGBA", FRAME)
    result.alpha_composite(silhouette, (2, 2))
    return result


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
        "Хранилище пряности — HD4",
        font=font(34, True),
        fill=(236, 219, 182, 255),
    )
    draw.text(
        (34, 69),
        "Корпус 64×64; исправленный флаг — отдельные 8 фаз",
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
        "Цвет Дома меняется только на ткани флага",
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
    draw_card(board, building, 1024, 395, 300, "корпус без ткани")
    draw_card(
        board,
        flag_frame(mask_atlas, 0),
        1354,
        395,
        300,
        "маска флага",
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
        "• нижняя граница сохранена\n"
        "• флаг закреплён на существующей мачте\n"
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
    if (
        building_box is None
        or building_box[0] < 3
        or building_box[1] < 3
        or building_box[2] > 253
        or building_box[3] > 253
    ):
        raise AssertionError(f"building touches boundary: {building_box}")
    if (
        shadow_box is None
        or shadow_box[0] < 1
        or shadow_box[1] < 1
        or shadow_box[2] > 255
        or shadow_box[3] > 255
    ):
        raise AssertionError(f"shadow touches boundary: {shadow_box}")

    flag_frames = [
        flag_frame(flag_atlas, phase) for phase in range(FLAG_FRAMES)
    ]
    mask_frames = [
        flag_frame(mask_atlas, phase) for phase in range(FLAG_FRAMES)
    ]
    if len({item.tobytes() for item in flag_frames}) != FLAG_FRAMES:
        raise AssertionError("flag animation phases are not unique")
    if len({item.tobytes() for item in mask_frames}) != FLAG_FRAMES:
        raise AssertionError("flag mask phases are not unique")

    flag_boxes = []
    for phase, item in enumerate(flag_frames):
        box = item.getchannel("A").getbbox()
        if box is None:
            raise AssertionError(f"flag phase {phase} is empty")
        flag_boxes.append(list(box))

    return {
        "resources": {
            "building": {"id": 34, "name": "BUILD_SILO"},
            "shadow": {"id": 35, "name": "BUILD_SILO_SHADOW"},
            "flag": "BUILD_SILO_FLAG",
            "flag_mask": "HM_BUILD_SILO_FLAG",
        },
        "logical_frame": list(LOGICAL_FRAME),
        "hd2_frame": [128, 128],
        "hd4_frame": list(FRAME),
        "footprint": [2, 2],
        "building_frames": 1,
        "flag_frames": FLAG_FRAMES,
        "building_box_hd4": list(building_box),
        "shadow_box_hd4": list(shadow_box),
        "flag_boxes_hd4": flag_boxes,
        "flag_attach_hd4": list(FLAG_ATTACH),
    }


def main() -> None:
    required = (SOURCE, CLASSIC, WINDTRAP_FLAG, WINDTRAP_MASK)
    for path in required:
        if not path.is_file():
            raise FileNotFoundError(path)

    building = fit_building(Image.open(SOURCE).convert("RGBA"))
    shadow = build_shadow(building)
    flag_atlas, mask_atlas = build_flag_atlases()
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
        "generation_mode": "built-in imagegen plus deterministic flag",
        "validation": validation,
    }
    (OUTPUT / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(manifest, ensure_ascii=False))


if __name__ == "__main__":
    main()
