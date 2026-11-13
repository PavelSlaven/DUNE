#!/usr/bin/env python3
"""Build the v2 approval preview for the HD Light Factory."""

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
OUTPUT = ROOT / "artifacts" / "lightfactory_review_v2"
SOURCE = OUTPUT / "generated" / "lightfactory_chroma.png"
CLASSIC = OUTPUT / "0012_BUILD_LIGHTFACTORY_CLASSIC.png"
CLASSIC_FLASH = OUTPUT / "0013_BUILD_LIGHTFACTORY_FLASH_CLASSIC.png"
FLAG_REFERENCE = ROOT / "artifacts" / "ix_review_v1" / "user_reference.png"

FRAME = (256, 256)
LOGICAL_FRAME = (64, 64)
ANIMATION_FRAMES = 8
FLAG_ATTACH = (178, 24)

BUILDING_OUT = OUTPUT / "BUILD_LIGHTFACTORY_HD4_PREVIEW.png"
FLASH_OUT = OUTPUT / "BUILD_LIGHTFACTORY_FLASH_HD4_PREVIEW.png"
PRODUCTION_OUT = OUTPUT / "BUILD_LIGHTFACTORY_PRODUCTION_HD4_PREVIEW.png"
SHADOW_OUT = OUTPUT / "BUILD_LIGHTFACTORY_SHADOW_HD4_PREVIEW.png"
OVERLAY_OUT = OUTPUT / "BUILD_LIGHTFACTORY_FLAG_HD4_PREVIEW.png"
MASK_OUT = OUTPUT / "HM_BUILD_LIGHTFACTORY_FLAG_HD4_PREVIEW.png"
REVIEW_OUT = OUTPUT / "BUILD_LIGHTFACTORY_REVIEW.png"
ANIMATION_OUT = OUTPUT / "BUILD_LIGHTFACTORY_ANIMATION_PREVIEW.gif"


def fit_building(source: Image.Image) -> Image.Image:
    pixels = np.asarray(source.convert("RGBA"), dtype=np.uint8).copy()
    keyed = (
        (pixels[:, :, 0] > 225)
        & (pixels[:, :, 2] > 210)
        & (pixels[:, :, 1] < 75)
    )
    distance = np.sqrt(
        (pixels[:, :, 0].astype(np.float32) - 255.0) ** 2
        + pixels[:, :, 1].astype(np.float32) ** 2
        + (pixels[:, :, 2].astype(np.float32) - 255.0) ** 2
    )
    soft = np.clip((distance - 18.0) / 75.0, 0.0, 1.0)
    pixels[:, :, 3] = np.where(keyed, 0, pixels[:, :, 3] * soft).astype(np.uint8)
    magenta_spill = np.minimum(pixels[:, :, 0], pixels[:, :, 2]).astype(np.int16)
    pixels[:, :, 0] = np.clip(
        pixels[:, :, 0].astype(np.int16) - magenta_spill // 5,
        0,
        255,
    ).astype(np.uint8)
    pixels[:, :, 2] = np.clip(
        pixels[:, :, 2].astype(np.int16) - magenta_spill // 5,
        0,
        255,
    ).astype(np.uint8)
    pixels[pixels[:, :, 3] == 0, :3] = 0
    source = Image.fromarray(pixels, "RGBA")
    box = source.getchannel("A").getbbox()
    if box is None:
        raise AssertionError("generated Light Factory is transparent")
    subject = source.crop(box)
    # Keep a full logical pixel of breathing room on every side at HD4.
    scale = min(232 / subject.width, 232 / subject.height)
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
        FRAME[1] - subject.height - 8,
    )
    result = Image.new("RGBA", FRAME)
    result.alpha_composite(subject, position)
    return result


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
    center = (57, 58)
    draw.ellipse(
        (center[0] - 12, center[1] - 12, center[0] + 12, center[1] + 12),
        fill=(61, 217, 255, 105),
    )
    glow = glow.filter(ImageFilter.GaussianBlur(6.0))
    result.alpha_composite(glow)
    draw = ImageDraw.Draw(result)
    draw.ellipse(
        (center[0] - 5, center[1] - 5, center[0] + 5, center[1] + 5),
        outline=(109, 235, 255, 210),
        width=2,
    )
    return result


def build_production_atlas() -> Image.Image:
    """Eight subtle lamp-and-smoke phases; the base never shifts."""
    atlas = Image.new("RGBA", (FRAME[0], FRAME[1] * ANIMATION_FRAMES))
    lamp_center = (57, 58)
    chimney = (85, 15)
    lamp_alpha = (32, 58, 92, 126, 154, 118, 76, 45)
    for phase in range(ANIMATION_FRAMES):
        frame = Image.new("RGBA", FRAME)
        glow = Image.new("RGBA", FRAME)
        glow_draw = ImageDraw.Draw(glow)

        strength = lamp_alpha[phase]
        glow_draw.ellipse(
            (
                lamp_center[0] - 12,
                lamp_center[1] - 12,
                lamp_center[0] + 12,
                lamp_center[1] + 12,
            ),
            fill=(55, 211, 255, strength),
        )
        glow = glow.filter(ImageFilter.GaussianBlur(6.0))
        frame.alpha_composite(glow)

        draw = ImageDraw.Draw(frame)
        draw.ellipse(
            (
                lamp_center[0] - 5,
                lamp_center[1] - 5,
                lamp_center[0] + 5,
                lamp_center[1] + 5,
            ),
            outline=(112, 234, 255, min(230, 90 + strength)),
            width=1,
        )

        # Two small puffs rise and drift left with the same wind as the flag.
        smoke = Image.new("RGBA", FRAME)
        smoke_draw = ImageDraw.Draw(smoke)
        for puff in range(2):
            age = (phase + puff * 4) % ANIMATION_FRAMES
            x = chimney[0] - round(age * 0.75)
            y = chimney[1] - 2 - age * 2
            radius = 2 + age // 3
            alpha = max(0, 82 - age * 9)
            smoke_draw.ellipse(
                (x - radius, y - radius, x + radius, y + radius),
                fill=(130, 139, 145, alpha),
            )
        smoke = smoke.filter(ImageFilter.GaussianBlur(2.2))
        frame.alpha_composite(smoke)
        atlas.alpha_composite(frame, (0, phase * FRAME[1]))
    return atlas


def composed(
    building: Image.Image,
    overlay: Image.Image,
    mask: Image.Image,
    phase: int,
    color: tuple[int, int, int],
    flash: Image.Image | None = None,
    production: Image.Image | None = None,
) -> Image.Image:
    result = building.copy()
    result.alpha_composite(
        apply_tint(frame_from(overlay, phase), frame_from(mask, phase), color)
    )
    if flash is not None:
        result.alpha_composite(flash)
    if production is not None:
        result.alpha_composite(frame_from(production, phase))
    return result


def build_review(
    building: Image.Image,
    flash: Image.Image,
    overlay: Image.Image,
    mask: Image.Image,
    production: Image.Image,
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
        "Корпус 64×64; 8 фаз флага, лампы и небольшого дымка",
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
                None,
                production,
            ),
            34 + phase * 216,
            108,
            190,
            f"фаза {phase}",
        )

    draw.text(
        (34, 355),
        "Цвет Домов применяется только к ткани флага; корпус нейтрален",
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
        "лампа и дым",
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
        "• один неподвижный кадр корпуса — геометрия не плавает\n"
        "• при выпуске техники мягко пульсирует штатная лампа\n"
        "• из левой трубы идёт небольшой дымок без перекрытия корпуса\n"
        "• штатная вспышка ID 13 заменена свечением этой же лампы\n"
        "• флаг закреплён на встроенном в крышу флагштоке\n"
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
    production: Image.Image,
) -> dict[str, object]:
    if building.size != FRAME or flash.size != FRAME:
        raise AssertionError("invalid Light Factory HD4 dimensions")
    expected_atlas = (FRAME[0], FRAME[1] * ANIMATION_FRAMES)
    if overlay.size != expected_atlas or mask.size != expected_atlas:
        raise AssertionError("invalid Light Factory flag atlas")
    if production.size != expected_atlas:
        raise AssertionError("invalid Light Factory production atlas")
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
        "production_frames": ANIMATION_FRAMES,
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
    production = build_production_atlas()
    flag = extract_flag(Image.open(FLAG_REFERENCE).convert("RGBA"))
    overlay, mask = build_flag_atlases(flag, FLAG_ATTACH)
    shadow = build_shadow(building)

    building.save(BUILDING_OUT, optimize=True)
    flash.save(FLASH_OUT, optimize=True)
    production.save(PRODUCTION_OUT, optimize=True)
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
    production.resize((128, 1024), Image.Resampling.LANCZOS).save(
        OUTPUT / "BUILD_LIGHTFACTORY_PRODUCTION_HD2_PREVIEW.png",
        optimize=True,
    )
    build_review(building, flash, overlay, mask, production).save(
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
            None,
            production,
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
            "ImageGen base plus deterministic flag, lamp, smoke and shadow"
        ),
        "validation": validate(building, flash, overlay, mask, production),
    }
    (OUTPUT / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(manifest, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
