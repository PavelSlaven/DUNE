#!/usr/bin/env python3
"""Build an approval-ready HD Light Factory with House flag and flash."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

from prepare_ix_review import (
    HOUSE_COLORS,
    apply_tint,
    build_flag_atlases,
    card,
    extract_flag,
    font,
    frame_from,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts" / "lightfactory_review_v1"
SOURCE = OUTPUT / "generated" / "lightfactory_alpha.png"
CLASSIC = OUTPUT / "0012_BUILD_LIGHTFACTORY_CLASSIC.png"
CLASSIC_FLASH = OUTPUT / "0013_BUILD_LIGHTFACTORY_FLASH_CLASSIC.png"
FLAG_REFERENCE = ROOT / "artifacts" / "ix_review_v1" / "user_reference.png"

FRAME = (256, 256)
LOGICAL_FRAME = (64, 64)
ANIMATION_FRAMES = 8
FLAG_ATTACH = (164, 13)

BUILDING_OUT = OUTPUT / "BUILD_LIGHTFACTORY_HD4_PREVIEW.png"
FLASH_OUT = OUTPUT / "BUILD_LIGHTFACTORY_FLASH_HD4_PREVIEW.png"
SHADOW_OUT = OUTPUT / "BUILD_LIGHTFACTORY_SHADOW_HD4_PREVIEW.png"
OVERLAY_OUT = OUTPUT / "BUILD_LIGHTFACTORY_FLAG_HD4_PREVIEW.png"
MASK_OUT = OUTPUT / "HM_BUILD_LIGHTFACTORY_FLAG_HD4_PREVIEW.png"
REVIEW_OUT = OUTPUT / "BUILD_LIGHTFACTORY_REVIEW.png"
ANIMATION_OUT = OUTPUT / "BUILD_LIGHTFACTORY_ANIMATION_PREVIEW.gif"


def fit_building(source: Image.Image) -> Image.Image:
    source = source.convert("RGBA")
    box = source.getchannel("A").getbbox()
    if box is None:
        raise AssertionError("generated Light Factory is transparent")
    subject = source.crop(box)
    scale = min(250 / subject.width, 250 / subject.height)
    size = (
        max(1, round(subject.width * scale)),
        max(1, round(subject.height * scale)),
    )
    subject = subject.resize(size, Image.Resampling.LANCZOS)

    pixels = np.asarray(subject, dtype=np.uint8).copy()
    magenta_edge = (
        (pixels[:, :, 0] > 145)
        & (pixels[:, :, 2] > 145)
        & (pixels[:, :, 1] < 115)
        & (pixels[:, :, 3] < 240)
    )
    pixels[magenta_edge] = 0
    subject = Image.fromarray(pixels, "RGBA")
    position = (
        (FRAME[0] - subject.width) // 2,
        FRAME[1] - subject.height - 3,
    )
    result = Image.new("RGBA", FRAME)
    result.alpha_composite(subject, position)
    draw_flag_pole(result)
    return result


def draw_flag_pole(building: Image.Image) -> None:
    draw = ImageDraw.Draw(building)
    x = FLAG_ATTACH[0]
    top = 8
    bottom = 61
    draw.rounded_rectangle(
        (x - 4, top + 2, x + 4, bottom),
        radius=3,
        fill=(13, 17, 22, 255),
        outline=(68, 78, 90, 255),
        width=1,
    )
    draw.line((x - 1, top + 6, x - 1, bottom - 3), fill=(95, 105, 116, 230))
    draw.ellipse(
        (x - 5, top - 2, x + 5, top + 8),
        fill=(32, 38, 46, 255),
        outline=(133, 143, 153, 255),
        width=1,
    )
    draw.ellipse(
        (x - 2, top, x + 2, top + 4),
        fill=(198, 205, 211, 255),
    )
    draw.rounded_rectangle(
        (x - 8, bottom - 3, x + 8, bottom + 4),
        radius=2,
        fill=(24, 29, 35, 255),
        outline=(93, 103, 113, 255),
        width=1,
    )


def build_shadow(building: Image.Image) -> Image.Image:
    alpha = building.getchannel("A").filter(ImageFilter.GaussianBlur(2.0))
    alpha = alpha.point(lambda value: round(value * 0.18))
    silhouette = Image.new("RGBA", FRAME, (7, 5, 3, 0))
    silhouette.putalpha(alpha)
    result = Image.new("RGBA", FRAME)
    result.alpha_composite(silhouette, (4, 4))
    return result


def build_flash() -> Image.Image:
    result = Image.new("RGBA", FRAME)
    glow = Image.new("RGBA", FRAME)
    draw = ImageDraw.Draw(glow)
    center = (208, 176)
    draw.ellipse(
        (center[0] - 15, center[1] - 15, center[0] + 15, center[1] + 15),
        fill=(24, 255, 72, 150),
    )
    glow = glow.filter(ImageFilter.GaussianBlur(8.0))
    result.alpha_composite(glow)
    draw = ImageDraw.Draw(result)
    draw.ellipse(
        (center[0] - 7, center[1] - 7, center[0] + 7, center[1] + 7),
        fill=(21, 213, 57, 235),
    )
    draw.ellipse(
        (center[0] - 3, center[1] - 3, center[0] + 3, center[1] + 3),
        fill=(190, 255, 204, 255),
    )
    return result


def composed(
    building: Image.Image,
    overlay: Image.Image,
    mask: Image.Image,
    phase: int,
    color: tuple[int, int, int],
    flash: Image.Image | None = None,
) -> Image.Image:
    result = building.copy()
    result.alpha_composite(
        apply_tint(frame_from(overlay, phase), frame_from(mask, phase), color)
    )
    if flash is not None:
        result.alpha_composite(flash)
    return result


def build_review(
    building: Image.Image,
    flash: Image.Image,
    overlay: Image.Image,
    mask: Image.Image,
) -> Image.Image:
    board = Image.new("RGBA", (1780, 1220), (9, 12, 16, 255))
    draw = ImageDraw.Draw(board)
    draw.text(
        (34, 24),
        "Лёгкий завод — HD4",
        font=font(34, True),
        fill=(236, 219, 182, 255),
    )
    draw.text(
        (34, 69),
        "Корпус 64×64; восемь фаз флага и производственная вспышка",
        font=font(19),
        fill=(187, 193, 201, 255),
    )
    for phase in range(ANIMATION_FRAMES):
        card(
            board,
            composed(
                building,
                overlay,
                mask,
                phase,
                HOUSE_COLORS["Ордос"],
                flash if phase in (3, 4) else None,
            ),
            34 + phase * 216,
            108,
            190,
            f"фаза {phase}",
        )

    draw.text(
        (34, 355),
        "Цвет Домов применяется только к ткани флага",
        font=font(25, True),
        fill=(225, 188, 98, 255),
    )
    for column, (name, color) in enumerate(HOUSE_COLORS.items()):
        card(
            board,
            composed(building, overlay, mask, 1 + column * 2, color),
            34 + column * 330,
            400,
            300,
            name,
        )
    card(
        board,
        composed(
            building,
            overlay,
            mask,
            3,
            HOUSE_COLORS["Ордос"],
            flash,
        ),
        1024,
        400,
        300,
        "производственная вспышка",
    )
    card(board, frame_from(mask, 2), 1354, 400, 300, "маска флага")

    draw.text(
        (34, 780),
        "Размер и исходный контракт",
        font=font(25, True),
        fill=(225, 188, 98, 255),
    )
    card(
        board,
        Image.open(CLASSIC).convert("RGBA"),
        34,
        825,
        260,
        "классика 64×64",
    )
    card(
        board,
        composed(building, overlay, mask, 2, HOUSE_COLORS["Ордос"]),
        330,
        825,
        260,
        "HD4 256×256",
    )
    notes = (
        "• площадь здания 2×2 клетки\n"
        "• один неподвижный кадр корпуса\n"
        "• производственная вспышка сохранена как ID 13\n"
        "• флаг стоит в штатной точке 41×2\n"
        "• флаг имеет 8 уникальных фаз\n"
        "• отдельная детерминированная тень"
    )
    draw.multiline_text(
        (640, 835),
        notes,
        font=font(22),
        fill=(201, 205, 212, 255),
        spacing=13,
    )
    draw.text(
        (34, 1180),
        "Предварительный просмотр — в игру не установлено.",
        font=font(18),
        fill=(183, 188, 196, 255),
    )
    return board


def validate(
    building: Image.Image,
    flash: Image.Image,
    overlay: Image.Image,
    mask: Image.Image,
) -> dict[str, object]:
    if building.size != FRAME or flash.size != FRAME:
        raise AssertionError("invalid Light Factory HD4 dimensions")
    expected_atlas = (FRAME[0], FRAME[1] * ANIMATION_FRAMES)
    if overlay.size != expected_atlas or mask.size != expected_atlas:
        raise AssertionError("invalid Light Factory flag atlas")
    if building.getchannel("A").getbbox() is None:
        raise AssertionError("Light Factory is transparent")
    if flash.getchannel("A").getbbox() is None:
        raise AssertionError("Light Factory flash is transparent")
    phases = {
        frame_from(overlay, phase).tobytes()
        for phase in range(ANIMATION_FRAMES)
    }
    if len(phases) != ANIMATION_FRAMES:
        raise AssertionError("Light Factory flag phases are not unique")
    return {
        "resources": {
            "building": {"id": 12, "name": "BUILD_LIGHTFACTORY"},
            "flash": {"id": 13, "name": "BUILD_LIGHTFACTORY_FLASH"},
            "shadow": {"id": 14, "name": "BUILD_LIGHTFACTORY_SHADOW"},
            "overlay": "BUILD_LIGHTFACTORY_FLAG",
            "overlay_mask": "HM_BUILD_LIGHTFACTORY_FLAG",
        },
        "logical_frame": list(LOGICAL_FRAME),
        "hd4_frame": list(FRAME),
        "footprint": [2, 2],
        "base_frames": 1,
        "overlay_frames": ANIMATION_FRAMES,
        "building_box_hd4": list(building.getchannel("A").getbbox()),
        "flash_box_hd4": list(flash.getchannel("A").getbbox()),
        "flag_attach_hd4": list(FLAG_ATTACH),
    }


def main() -> int:
    for path in (SOURCE, CLASSIC, CLASSIC_FLASH, FLAG_REFERENCE):
        if not path.is_file():
            raise FileNotFoundError(path)
    building = fit_building(Image.open(SOURCE))
    flash = build_flash()
    flag = extract_flag(Image.open(FLAG_REFERENCE).convert("RGBA"))
    overlay, mask = build_flag_atlases(flag, FLAG_ATTACH)
    shadow = build_shadow(building)

    building.save(BUILDING_OUT, optimize=True)
    flash.save(FLASH_OUT, optimize=True)
    shadow.save(SHADOW_OUT, optimize=True)
    overlay.save(OVERLAY_OUT, optimize=True)
    mask.save(MASK_OUT, optimize=True)
    building.resize((128, 128), Image.Resampling.LANCZOS).save(
        OUTPUT / "BUILD_LIGHTFACTORY_HD2_PREVIEW.png",
        optimize=True,
    )
    flash.resize((128, 128), Image.Resampling.LANCZOS).save(
        OUTPUT / "BUILD_LIGHTFACTORY_FLASH_HD2_PREVIEW.png",
        optimize=True,
    )
    overlay.resize((128, 1024), Image.Resampling.LANCZOS).save(
        OUTPUT / "BUILD_LIGHTFACTORY_FLAG_HD2_PREVIEW.png",
        optimize=True,
    )
    mask.resize((128, 1024), Image.Resampling.LANCZOS).save(
        OUTPUT / "HM_BUILD_LIGHTFACTORY_FLAG_HD2_PREVIEW.png",
        optimize=True,
    )
    build_review(building, flash, overlay, mask).save(
        REVIEW_OUT,
        optimize=True,
    )
    animation = [
        composed(
            building,
            overlay,
            mask,
            phase,
            HOUSE_COLORS["Ордос"],
            flash if phase in (3, 4) else None,
        )
        .resize((640, 640), Image.Resampling.LANCZOS)
        .convert("P", palette=Image.Palette.ADAPTIVE)
        for phase in range(ANIMATION_FRAMES)
    ]
    animation[0].save(
        ANIMATION_OUT,
        save_all=True,
        append_images=animation[1:],
        duration=125,
        loop=0,
        disposal=2,
    )
    manifest = {
        "format": 1,
        "status": "preview_not_integrated",
        "source_reference": str(OUTPUT / "user_reference.png"),
        "generated_base": str(SOURCE),
        "classic_contract": str(CLASSIC),
        "generation_mode": (
            "ImageGen base plus deterministic flag, flash and shadow"
        ),
        "validation": validate(building, flash, overlay, mask),
    }
    (OUTPUT / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(manifest, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
