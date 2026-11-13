#!/usr/bin/env python3
"""Build an approval-ready HD4 Construction Yard and animated flag."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts" / "constyard_review_v1"
SOURCE = OUTPUT / "constyard_alpha.png"
CLASSIC = (
    ROOT / "resources" / "hd" / "classic" / "sdl_data"
    / "0003_BUILD_CONSTYARD.png"
)
WINDTRAP_FLAG = (
    ROOT / "artifacts" / "windtrap_review_v1"
    / "BUILD_WINDTRAP_FLAG_HD4_PREVIEW.png"
)

FRAME = (256, 256)
FLAG_ATLAS = (256, 2048)
FLAG_FRAMES = 8
BODY_OUT = OUTPUT / "BUILD_CONSTYARD_HD4_PREVIEW.png"
SHADOW_OUT = OUTPUT / "BUILD_CONSTYARD_SHADOW_HD4_PREVIEW.png"
FLAG_OUT = OUTPUT / "BUILD_CONSTYARD_FLAG_HD4_PREVIEW.png"
FLAG_MASK_OUT = OUTPUT / "HM_BUILD_CONSTYARD_FLAG_HD4_PREVIEW.png"
REVIEW_OUT = OUTPUT / "BUILD_CONSTYARD_REVIEW.png"
ANIMATION_OUT = OUTPUT / "BUILD_CONSTYARD_ANIMATION_PREVIEW.gif"

HOUSE_COLORS = {
    "Харконнены": (255, 0, 0),
    "Атрейдесы": (0, 90, 255),
    "Ордос": (0, 255, 0),
}


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    filename = "arialbd.ttf" if bold else "arial.ttf"
    return ImageFont.truetype(str(Path("C:/Windows/Fonts") / filename), size)


def clean_alpha(image: Image.Image) -> Image.Image:
    rgba = np.asarray(image.convert("RGBA"), dtype=np.uint8).copy()
    rgba[rgba[:, :, 3] < 4] = 0
    return Image.fromarray(rgba, "RGBA")


def build_body(source: Image.Image) -> Image.Image:
    source = clean_alpha(source)
    box = source.getchannel("A").getbbox()
    if box is None:
        raise AssertionError("Construction Yard source is empty")
    subject = source.crop(box)
    scale = min(248 / subject.width, 244 / subject.height)
    size = (
        max(1, round(subject.width * scale)),
        max(1, round(subject.height * scale)),
    )
    subject = subject.resize(size, Image.Resampling.LANCZOS)
    body = Image.new("RGBA", FRAME)
    body.alpha_composite(
        subject,
        (
            round((FRAME[0] - subject.width) / 2),
            FRAME[1] - 4 - subject.height,
        ),
    )
    return clean_alpha(body)


def build_shadow(body: Image.Image) -> Image.Image:
    alpha = body.getchannel("A").filter(ImageFilter.GaussianBlur(2.2))
    alpha = alpha.point(lambda value: round(value * 0.18))
    shadow = Image.new("RGBA", FRAME, (8, 6, 4, 0))
    shadow.putalpha(alpha)
    shifted = Image.new("RGBA", FRAME)
    shifted.alpha_composite(shadow, (4, 5))
    return shifted


def flag_source_frame(atlas: Image.Image, index: int) -> Image.Image:
    source_height = atlas.height // FLAG_FRAMES
    frame = atlas.crop(
        (
            0,
            index * source_height,
            atlas.width,
            (index + 1) * source_height,
        )
    )
    box = frame.getchannel("A").getbbox()
    if box is None:
        raise AssertionError(f"flag source frame {index} is empty")
    return frame.crop(box).transpose(Image.Transpose.FLIP_LEFT_RIGHT)


def build_flag() -> tuple[Image.Image, Image.Image]:
    source = Image.open(WINDTRAP_FLAG).convert("RGBA")
    flag = Image.new("RGBA", FLAG_ATLAS)
    mask = Image.new("RGBA", FLAG_ATLAS)
    for index in range(FLAG_FRAMES):
        fabric = flag_source_frame(source, index)
        scale = min(46 / fabric.width, 24 / fabric.height)
        fabric = fabric.resize(
            (
                max(1, round(fabric.width * scale)),
                max(1, round(fabric.height * scale)),
            ),
            Image.Resampling.LANCZOS,
        )
        position = (
            87 - fabric.width,
            index * FRAME[1] + 77,
        )
        flag.alpha_composite(fabric, position)
        fabric_mask = Image.new("RGBA", fabric.size, (255, 255, 255, 0))
        fabric_mask.putalpha(fabric.getchannel("A"))
        mask.alpha_composite(fabric_mask, position)
    return clean_alpha(flag), clean_alpha(mask)


def apply_tint(
    image: Image.Image,
    mask: Image.Image,
    color: tuple[int, int, int],
) -> Image.Image:
    rgba = np.asarray(image.convert("RGBA"), dtype=np.float32).copy()
    mask_alpha = (
        np.asarray(mask.getchannel("A"), dtype=np.float32) / 255.0
    )
    luminance = (
        0.299 * rgba[:, :, 0]
        + 0.587 * rgba[:, :, 1]
        + 0.114 * rgba[:, :, 2]
    ) / 128.0
    for channel, target in enumerate(color):
        colored = np.minimum(255.0, target * luminance)
        rgba[:, :, channel] = (
            rgba[:, :, channel] * (1.0 - mask_alpha)
            + colored * mask_alpha
        )
    return Image.fromarray(np.clip(rgba, 0, 255).astype(np.uint8), "RGBA")


def overlay_frame(
    body: Image.Image,
    flag: Image.Image,
    mask: Image.Image,
    phase: int,
    color: tuple[int, int, int],
) -> Image.Image:
    result = body.copy()
    source = flag.crop(
        (
            0,
            phase * FRAME[1],
            FRAME[0],
            (phase + 1) * FRAME[1],
        )
    )
    source_mask = mask.crop(
        (
            0,
            phase * FRAME[1],
            FRAME[0],
            (phase + 1) * FRAME[1],
        )
    )
    result.alpha_composite(apply_tint(source, source_mask, color))
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
        radius=8,
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
    body: Image.Image,
    flag: Image.Image,
    mask: Image.Image,
) -> Image.Image:
    board = Image.new("RGBA", (1700, 1280), (9, 12, 16, 255))
    draw = ImageDraw.Draw(board)
    draw.text(
        (34, 24),
        "Строительный двор — HD4",
        font=font(34, True),
        fill=(236, 219, 182, 255),
    )
    draw.text(
        (34, 70),
        "Исходный контракт 64×64; мастер 256×256; площадь 2×2",
        font=font(19),
        fill=(187, 193, 201, 255),
    )

    draw_card(
        board,
        overlay_frame(
            body,
            flag,
            mask,
            0,
            HOUSE_COLORS["Ордос"],
        ),
        34,
        110,
        430,
        "общий вид",
    )

    classic = Image.open(CLASSIC).convert("RGBA")
    draw_card(board, classic, 500, 110, 300, "классический атлас")
    draw_card(board, body, 836, 110, 430, "нейтральная основа")
    draw_card(
        board,
        mask.crop((0, 0, 256, 256)),
        1302,
        110,
        300,
        "маска флага",
    )

    draw.text(
        (34, 600),
        "Восемь фаз развевающегося флага",
        font=font(25, True),
        fill=(225, 188, 98, 255),
    )
    for index in range(FLAG_FRAMES):
        draw_card(
            board,
            overlay_frame(
                body,
                flag,
                mask,
                index,
                HOUSE_COLORS["Ордос"],
            ),
            34 + index * 202,
            645,
            180,
            f"фаза {index}",
        )

    draw.text(
        (34, 875),
        "Цвета Домов",
        font=font(25, True),
        fill=(225, 188, 98, 255),
    )
    for index, (name, color) in enumerate(HOUSE_COLORS.items()):
        draw_card(
            board,
            overlay_frame(body, flag, mask, 3, color),
            34 + index * 322,
            920,
            290,
            name,
        )

    draw.text(
        (1040, 900),
        "Состав сохранён:",
        font=font(23, True),
        fill=(225, 188, 98, 255),
    )
    draw.text(
        (1040, 945),
        "• два цилиндрических резервуара\n"
        "• верхний портальный кран\n"
        "• закрытый производственный модуль\n"
        "• открытая сборочная площадка\n"
        "• нижняя привязка и размер 2×2\n"
        "• отдельный флаг без окраски корпуса",
        font=font(21),
        fill=(204, 208, 213, 255),
        spacing=13,
    )
    draw.text(
        (34, 1240),
        "Предварительный просмотр — в игру не установлено.",
        font=font(19),
        fill=(188, 194, 202, 255),
    )
    return board


def build_animation(
    body: Image.Image,
    flag: Image.Image,
    mask: Image.Image,
) -> None:
    frames = []
    for phase in range(FLAG_FRAMES):
        shown = Image.new("RGBA", (512, 512), (16, 20, 26, 255))
        shown.alpha_composite(
            overlay_frame(
                body,
                flag,
                mask,
                phase,
                HOUSE_COLORS["Ордос"],
            ).resize((512, 512), Image.Resampling.LANCZOS)
        )
        frames.append(shown.convert("P", palette=Image.Palette.ADAPTIVE))
    frames[0].save(
        ANIMATION_OUT,
        save_all=True,
        append_images=frames[1:],
        duration=125,
        loop=0,
        disposal=2,
    )


def validate(
    body: Image.Image,
    shadow: Image.Image,
    flag: Image.Image,
    mask: Image.Image,
) -> dict[str, object]:
    for name, image, expected in (
        ("body", body, FRAME),
        ("shadow", shadow, FRAME),
        ("flag", flag, FLAG_ATLAS),
        ("flag mask", mask, FLAG_ATLAS),
    ):
        if image.size != expected:
            raise AssertionError(f"{name} size is {image.size}")
        if image.getchannel("A").getbbox() is None:
            raise AssertionError(f"{name} is empty")
    body_box = body.getchannel("A").getbbox()
    if (
        body_box is None
        or body_box[0] < 4
        or body_box[1] < 4
        or body_box[2] > 252
        or body_box[3] > 252
    ):
        raise AssertionError(f"body touches frame boundary: {body_box}")
    flag_boxes = []
    flag_payloads = set()
    for phase in range(FLAG_FRAMES):
        flag_frame = flag.crop(
            (0, phase * 256, 256, (phase + 1) * 256)
        )
        mask_frame = mask.crop(
            (0, phase * 256, 256, (phase + 1) * 256)
        )
        box = flag_frame.getchannel("A").getbbox()
        if box is None:
            raise AssertionError(f"flag phase {phase} is empty")
        if (
            flag_frame.getchannel("A").tobytes()
            != mask_frame.getchannel("A").tobytes()
        ):
            raise AssertionError(f"flag mask phase {phase} changed alpha")
        flag_boxes.append(list(box))
        flag_payloads.add(flag_frame.tobytes())
    if len(flag_payloads) != FLAG_FRAMES:
        raise AssertionError("waving flag phases are not unique")
    return {
        "resources": {
            "body": {"id": 3, "name": "BUILD_CONSTYARD"},
            "shadow": {"id": 4, "name": "BUILD_CONSTYARD_SHADOW"},
            "flag": {"name": "BUILD_CONSTYARD_FLAG"},
            "flag_mask": {"name": "HM_BUILD_CONSTYARD_FLAG"},
        },
        "logical_frame": [64, 64],
        "hd4_frame": list(FRAME),
        "footprint_cells": [2, 2],
        "body_frames": 1,
        "flag_frames": FLAG_FRAMES,
        "unique_flag_frames": len(flag_payloads),
        "body_box_hd4": list(body_box),
        "flag_boxes_hd4": flag_boxes,
        "bottom_anchor_hd4": 252,
    }


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    body = build_body(Image.open(SOURCE).convert("RGBA"))
    shadow = build_shadow(body)
    flag, mask = build_flag()
    validation = validate(body, shadow, flag, mask)

    body.save(BODY_OUT, optimize=True)
    shadow.save(SHADOW_OUT, optimize=True)
    flag.save(FLAG_OUT, optimize=True)
    mask.save(FLAG_MASK_OUT, optimize=True)
    body.resize((128, 128), Image.Resampling.LANCZOS).save(
        OUTPUT / "BUILD_CONSTYARD_HD2_PREVIEW.png",
        optimize=True,
    )
    build_review(body, flag, mask).save(REVIEW_OUT, optimize=True)
    build_animation(body, flag, mask)

    manifest = {
        "format": 1,
        "status": "preview_not_integrated",
        "source_reference": str(OUTPUT / "user_reference.png"),
        "classic_contract": str(CLASSIC),
        "imagegen_source": str(OUTPUT / "constyard_chroma.png"),
        "validation": validation,
    }
    (OUTPUT / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(manifest, ensure_ascii=False))


if __name__ == "__main__":
    main()
