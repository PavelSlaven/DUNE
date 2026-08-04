#!/usr/bin/env python3
"""Prepare an approval-ready HD4 Starport atlas and animated House flag."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts" / "starport_review_v1"
SOURCE = OUTPUT / "starport_alpha.png"
CARGO_SOURCE = OUTPUT / "cargo_container_alpha.png"
CLASSIC = (
    ROOT / "resources" / "hd" / "classic" / "sdl_data"
    / "0036_BUILD_STARPORT.png"
)
CLASSIC_SHADOW = (
    ROOT / "resources" / "hd" / "classic" / "sdl_data"
    / "0037_BUILD_STARPORT_SHADOW.png"
)
FLAG_SOURCE = (
    ROOT / "artifacts" / "windtrap_review_v1"
    / "BUILD_WINDTRAP_FLAG_HD4_PREVIEW.png"
)
FLAG_MASK_SOURCE = (
    ROOT / "artifacts" / "windtrap_review_v1"
    / "HM_BUILD_WINDTRAP_FLAG_HD4_PREVIEW.png"
)

FRAME = 384
LOGICAL_FRAME = 96
FRAME_COUNT = 8
ATLAS_SIZE = (FRAME, FRAME * FRAME_COUNT)
FLAG_SOURCE_FRAME = 256
FLAG_SOURCE_BOX = (172, 117, 214, 144)
FLAG_SIZE = (38, 24)
# Attachment point after the reference is fitted into the 384x384 cell.
FLAG_ATTACH = (101, 235)

BUILDING_OUT = OUTPUT / "BUILD_STARPORT_HD4_PREVIEW.png"
SHADOW_OUT = OUTPUT / "BUILD_STARPORT_SHADOW_HD4_PREVIEW.png"
FLAG_OUT = OUTPUT / "BUILD_STARPORT_FLAG_HD4_PREVIEW.png"
FLAG_MASK_OUT = OUTPUT / "HM_BUILD_STARPORT_FLAG_HD4_PREVIEW.png"
BUILDING_HD2_OUT = OUTPUT / "BUILD_STARPORT_HD2_PREVIEW.png"
SHADOW_HD2_OUT = OUTPUT / "BUILD_STARPORT_SHADOW_HD2_PREVIEW.png"
FLAG_HD2_OUT = OUTPUT / "BUILD_STARPORT_FLAG_HD2_PREVIEW.png"
FLAG_MASK_HD2_OUT = OUTPUT / "HM_BUILD_STARPORT_FLAG_HD2_PREVIEW.png"
REVIEW_OUT = OUTPUT / "BUILD_STARPORT_REVIEW.png"
ANIMATION_OUT = OUTPUT / "BUILD_STARPORT_ANIMATION_PREVIEW.gif"

HOUSE_COLORS = {
    "Харконнены": (255, 0, 0),
    "Атрейдесы": (0, 90, 255),
    "Ордос": (0, 255, 0),
}


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    filename = "arialbd.ttf" if bold else "arial.ttf"
    return ImageFont.truetype(
        str(Path("C:/Windows/Fonts") / filename),
        size,
    )


def fit_building(source: Image.Image) -> Image.Image:
    box = source.getchannel("A").getbbox()
    if box is None:
        raise AssertionError("generated Starport is fully transparent")
    subject = source.crop(box)
    max_size = (372, 360)
    scale = min(
        max_size[0] / subject.width,
        max_size[1] / subject.height,
    )
    size = (
        round(subject.width * scale),
        round(subject.height * scale),
    )
    subject = subject.resize(size, Image.Resampling.LANCZOS)
    frame = Image.new("RGBA", (FRAME, FRAME))
    frame.alpha_composite(
        subject,
        (
            (FRAME - subject.width) // 2,
            FRAME - subject.height - 4,
        ),
    )
    return frame


def fit_cargo(source: Image.Image) -> Image.Image:
    box = source.getchannel("A").getbbox()
    if box is None:
        raise AssertionError("generated cargo container is transparent")
    cargo = source.crop(box)
    # Frame 7 replaces the whole inner loading platform, as in the classic
    # atlas. Its broader footprint is intentional; the dome is composited
    # back above it below, so the container remains behind the roof.
    cargo = cargo.resize((154, 202), Image.Resampling.LANCZOS)

    # The generated cargo concept has its own red/yellow marker lamps. In the
    # occupied Starport frame they can be mistaken for the runway beacons that
    # the container must cover, so keep the container visually inert.
    rgba = np.asarray(cargo, dtype=np.uint8).copy()
    opaque = rgba[:, :, 3] > 48
    red_marker = (
        opaque
        & (rgba[:, :, 0] > 70)
        & (rgba[:, :, 0] > rgba[:, :, 1] * 1.12)
        & (rgba[:, :, 0] > rgba[:, :, 2] * 1.05)
    )
    yellow_marker = (
        opaque
        & (rgba[:, :, 0] > 80)
        & (rgba[:, :, 1] > 50)
        & (rgba[:, :, 0] > rgba[:, :, 2] * 1.25)
        & (rgba[:, :, 1] > rgba[:, :, 2] * 1.15)
    )
    rgb16 = rgba[:, :, :3].astype(np.int16)
    warm_marker = (
        opaque
        & (rgb16[:, :, 0] > 45)
        & ((rgb16[:, :, 0] - rgb16[:, :, 1]) > 2)
        & ((rgb16[:, :, 0] - rgb16[:, :, 2]) > 5)
    )
    markers = red_marker | yellow_marker | warm_marker
    neutral = np.clip(
        rgba[:, :, :3].mean(axis=2) * 0.62,
        28,
        112,
    ).astype(np.uint8)
    for channel in range(3):
        rgba[:, :, channel][markers] = neutral[markers]
    return Image.fromarray(rgba, "RGBA")


def animate_starport(
    base: Image.Image,
    cargo: Image.Image,
    phase: int,
) -> Image.Image:
    """Recreate the seven beacon phases and the occupied eighth frame."""
    rgba = np.asarray(base.convert("RGBA"), dtype=np.float32).copy()
    red = (
        (rgba[:, :, 0] > 120)
        & (rgba[:, :, 0] > rgba[:, :, 1] * 1.32)
        & (rgba[:, :, 0] > rgba[:, :, 2] * 1.12)
        & (rgba[:, :, 3] > 64)
    )
    yy, xx = np.mgrid[0:FRAME, 0:FRAME]
    groups = (
        yy < 120,
        (xx >= 300) & (yy < 190),
        (xx >= 300) & (yy >= 190),
        (xx < 300) & (yy >= 175),
    )
    active_groups = {
        0: (),
        1: (0,),
        2: (0, 1),
        3: (1,),
        4: (1, 2),
        5: (2, 3),
        6: (0, 1, 2, 3),
        7: (0, 1, 2, 3),
    }[phase]
    red_channel = rgba[:, :, 0]
    green_channel = rgba[:, :, 1]
    blue_channel = rgba[:, :, 2]
    for index, group in enumerate(groups):
        selected = red & group
        if index in active_groups:
            red_channel[selected] = np.minimum(
                255,
                red_channel[selected] * 1.22 + 30,
            )
            green_channel[selected] *= 0.72
            blue_channel[selected] *= 0.72
        else:
            red_channel[selected] *= 0.55
            green_channel[selected] *= 0.55
            blue_channel[selected] *= 0.55

    result = Image.fromarray(
        np.clip(rgba, 0, 255).astype(np.uint8),
        "RGBA",
    )
    if phase == 7:
        # The classic final frame fills the loading platform with the delivered
        # container. Draw it first, then restore only the foreground dome so it
        # reads as sitting on the pad, behind the roof. Runway beacons remain
        # covered by the cargo.
        foreground = result.copy()
        position = (
            301 - cargo.width // 2,
            162 - cargo.height // 2,
        )
        cargo_backing = Image.new("RGBA", (FRAME, FRAME))
        backing_draw = ImageDraw.Draw(cargo_backing)
        backing_box = (
            position[0],
            position[1],
            position[0] + cargo.width - 1,
            position[1] + cargo.height - 1,
        )
        backing_draw.rounded_rectangle(
            backing_box,
            radius=5,
            fill=(65, 71, 86, 255),
            outline=(105, 111, 128, 255),
            width=2,
        )
        result.alpha_composite(cargo_backing)
        result.alpha_composite(cargo, position)

        dome_mask = Image.new("L", (FRAME, FRAME))
        dome_draw = ImageDraw.Draw(dome_mask)
        # Restore only the foreground dome and its collar. The continuous cargo
        # backing remains behind it and keeps every runway beacon covered.
        dome_draw.ellipse((142, 185, 330, 342), fill=255)
        dome_mask = dome_mask.filter(ImageFilter.GaussianBlur(0.25))
        result = Image.composite(foreground, result, dome_mask)

    return result


def vertical_atlas(frames: list[Image.Image]) -> Image.Image:
    atlas = Image.new("RGBA", (FRAME, FRAME * len(frames)))
    for index, frame in enumerate(frames):
        atlas.alpha_composite(frame, (0, index * FRAME))
    return atlas


def build_shadow(frame: Image.Image) -> Image.Image:
    alpha = frame.getchannel("A").filter(ImageFilter.GaussianBlur(1.5))
    alpha = alpha.point(lambda value: round(value * 0.18))
    silhouette = Image.new("RGBA", (FRAME, FRAME), (6, 5, 4, 0))
    silhouette.putalpha(alpha)
    result = Image.new("RGBA", (FRAME, FRAME))
    result.alpha_composite(silhouette, (-1, -1))
    return result


def build_flag_atlases() -> tuple[Image.Image, Image.Image]:
    source = Image.open(FLAG_SOURCE).convert("RGBA")
    source_mask = Image.open(FLAG_MASK_SOURCE).convert("RGBA")
    expected = (FLAG_SOURCE_FRAME, FLAG_SOURCE_FRAME * FRAME_COUNT)
    if source.size != expected or source_mask.size != expected:
        raise AssertionError("approved wind-trap flag contract changed")

    flag_atlas = Image.new("RGBA", ATLAS_SIZE)
    mask_atlas = Image.new("RGBA", ATLAS_SIZE)
    position = (
        FLAG_ATTACH[0] - FLAG_SIZE[0] + 2,
        FLAG_ATTACH[1] - FLAG_SIZE[1] // 2,
    )
    for phase in range(FRAME_COUNT):
        y = phase * FLAG_SOURCE_FRAME
        source_box = (
            FLAG_SOURCE_BOX[0],
            FLAG_SOURCE_BOX[1] + y,
            FLAG_SOURCE_BOX[2],
            FLAG_SOURCE_BOX[3] + y,
        )
        fabric = source.crop(source_box).resize(
            FLAG_SIZE,
            Image.Resampling.LANCZOS,
        )
        fabric_mask = source_mask.crop(source_box).resize(
            FLAG_SIZE,
            Image.Resampling.LANCZOS,
        )
        flag_atlas.alpha_composite(
            fabric,
            (position[0], position[1] + phase * FRAME),
        )
        mask_atlas.alpha_composite(
            fabric_mask,
            (position[0], position[1] + phase * FRAME),
        )
    return flag_atlas, mask_atlas


def atlas_frame(atlas: Image.Image, phase: int) -> Image.Image:
    return atlas.crop(
        (0, phase * FRAME, FRAME, (phase + 1) * FRAME)
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
    building_atlas: Image.Image,
    flag_atlas: Image.Image,
    mask_atlas: Image.Image,
    phase: int,
    color: tuple[int, int, int],
) -> Image.Image:
    result = atlas_frame(building_atlas, phase)
    result.alpha_composite(
        apply_engine_tint(
            atlas_frame(flag_atlas, phase),
            atlas_frame(mask_atlas, phase),
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
        (x + 7, y + size + 5),
        label,
        font=font(16, True),
        fill=(231, 214, 177, 255),
    )


def build_review(
    building: Image.Image,
    flag: Image.Image,
    mask: Image.Image,
) -> Image.Image:
    board = Image.new("RGBA", (1740, 1220), (9, 12, 16, 255))
    draw = ImageDraw.Draw(board)
    draw.text(
        (34, 24),
        "Космопорт — HD4, 8 кадров + флаг",
        font=font(34, True),
        fill=(236, 219, 182, 255),
    )
    draw.text(
        (34, 69),
        "ID 36/37 · логический кадр 96×96 · HD4 384×384",
        font=font(19),
        fill=(187, 193, 201, 255),
    )

    for phase in range(FRAME_COUNT):
        draw_card(
            board,
            composed(
                building,
                flag,
                mask,
                phase,
                HOUSE_COLORS["Ордос"],
            ),
            34 + phase * 210,
            108,
            184,
            f"кадр {phase}",
        )

    draw.text(
        (34, 350),
        "Флаг: 8 фаз ветра, окраска только маской Дома",
        font=font(25, True),
        fill=(225, 188, 98, 255),
    )
    for index, (name, color) in enumerate(HOUSE_COLORS.items()):
        draw_card(
            board,
            composed(building, flag, mask, 2 + index * 2, color),
            34 + index * 390,
            400,
            350,
            name,
        )
    draw_card(
        board,
        atlas_frame(mask, 0),
        1204,
        400,
        350,
        "маска флага",
    )

    draw.text(
        (34, 815),
        "Сверка с классическим атласом",
        font=font(25, True),
        fill=(225, 188, 98, 255),
    )
    classic = Image.open(CLASSIC).convert("RGBA")
    classic_first = classic.crop((0, 0, 96, 96))
    classic_last = classic.crop((0, 7 * 96, 96, 8 * 96))
    draw_card(board, classic_first, 34, 860, 300, "классика: кадр 0")
    draw_card(board, classic_last, 364, 860, 300, "классика: кадр 7")
    draw_card(
        board,
        composed(building, flag, mask, 0, HOUSE_COLORS["Ордос"]),
        714,
        860,
        300,
        "HD4: кадр 0",
    )
    draw_card(
        board,
        composed(building, flag, mask, 7, HOUSE_COLORS["Ордос"]),
        1044,
        860,
        300,
        "HD4: кадр 7",
    )
    return board


def save_gif(
    building: Image.Image,
    flag: Image.Image,
    mask: Image.Image,
) -> None:
    frames = [
        composed(
            building,
            flag,
            mask,
            phase,
            HOUSE_COLORS["Ордос"],
        ).resize((288, 288), Image.Resampling.LANCZOS)
        for phase in range(FRAME_COUNT)
    ]
    frames[0].save(
        ANIMATION_OUT,
        save_all=True,
        append_images=frames[1:],
        duration=[180] * 7 + [420],
        loop=0,
        disposal=2,
    )


def validate(
    building: Image.Image,
    shadow: Image.Image,
    flag: Image.Image,
    mask: Image.Image,
) -> None:
    classic = Image.open(CLASSIC)
    classic_shadow = Image.open(CLASSIC_SHADOW)
    if classic.size != (96, 768) or classic_shadow.size != (96, 768):
        raise AssertionError("classic Starport atlas contract changed")
    for name, image in {
        "building": building,
        "shadow": shadow,
        "flag": flag,
        "flag mask": mask,
    }.items():
        if image.size != ATLAS_SIZE:
            raise AssertionError(f"{name} has size {image.size}")
        if image.getchannel("A").getbbox() is None:
            raise AssertionError(f"{name} is fully transparent")

    frames = [atlas_frame(building, phase) for phase in range(FRAME_COUNT)]
    base_box = frames[0].getchannel("A").getbbox()
    if any(
        frame.getchannel("A").getbbox() != base_box
        for frame in frames[1:7]
    ):
        raise AssertionError("Starport anchor changes in frames 0-6")
    delivery_box = frames[7].getchannel("A").getbbox()
    if delivery_box is None:
        raise AssertionError("Starport delivery frame is empty")
    if (
        delivery_box[0] <= 0
        or delivery_box[1] <= 0
        or delivery_box[2] >= FRAME
        or delivery_box[3] >= FRAME
    ):
        raise AssertionError(
            f"Starport delivery frame touches its cell: {delivery_box}"
        )
    shadow_frames = [
        atlas_frame(shadow, phase)
        for phase in range(FRAME_COUNT)
    ]
    for phase, shadow_frame in enumerate(shadow_frames):
        box = shadow_frame.getchannel("A").getbbox()
        if box is None:
            raise AssertionError(f"shadow frame {phase} is empty")
        if box[0] <= 0 or box[1] <= 0 or box[2] >= FRAME or box[3] >= FRAME:
            raise AssertionError(
                f"shadow frame {phase} touches its cell boundary: {box}"
            )
    if any(
        not ImageChops.difference(
            frames[index - 1].convert("RGB"),
            frames[index].convert("RGB"),
        ).getbbox()
        for index in range(1, FRAME_COUNT)
    ):
        raise AssertionError("duplicate Starport animation frames")

    hd2 = building.resize(
        (FRAME // 2, FRAME * FRAME_COUNT // 2),
        Image.Resampling.LANCZOS,
    )
    if hd2.size != (192, 1536):
        raise AssertionError("unexpected HD2 Starport size")


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    source = Image.open(SOURCE).convert("RGBA")
    cargo = fit_cargo(Image.open(CARGO_SOURCE).convert("RGBA"))
    base = fit_building(source)
    building_frames = [
        animate_starport(base, cargo, phase)
        for phase in range(FRAME_COUNT)
    ]
    building = vertical_atlas(building_frames)
    shadow_frame = build_shadow(base)
    shadow = vertical_atlas([shadow_frame] * FRAME_COUNT)
    flag, flag_mask = build_flag_atlases()
    validate(building, shadow, flag, flag_mask)

    building.save(BUILDING_OUT, optimize=True)
    shadow.save(SHADOW_OUT, optimize=True)
    flag.save(FLAG_OUT, optimize=True)
    flag_mask.save(FLAG_MASK_OUT, optimize=True)
    for image, path in (
        (building, BUILDING_HD2_OUT),
        (shadow, SHADOW_HD2_OUT),
        (flag, FLAG_HD2_OUT),
        (flag_mask, FLAG_MASK_HD2_OUT),
    ):
        image.resize(
            (image.width // 2, image.height // 2),
            Image.Resampling.LANCZOS,
        ).save(path, optimize=True)

    build_review(building, flag, flag_mask).save(
        REVIEW_OUT,
        optimize=True,
    )
    save_gif(building, flag, flag_mask)

    manifest = {
        "format": 1,
        "status": "preview_not_integrated",
        "source": str(SOURCE.relative_to(ROOT)),
        "resource": {
            "id": 36,
            "name": "BUILD_STARPORT",
            "shadow_id": 37,
            "shadow_name": "BUILD_STARPORT_SHADOW",
            "frames": FRAME_COUNT,
            "logical_frame": [LOGICAL_FRAME, LOGICAL_FRAME],
            "classic_atlas": [96, 768],
            "hd2_atlas": [192, 1536],
            "hd4_atlas": list(ATLAS_SIZE),
        },
        "animation": {
            "frames_0_to_6": "landing beacon sequence",
            "frame_7": "delivered cargo container on landing pad",
        },
        "flag": {
            "name": "BUILD_STARPORT_FLAG",
            "mask_name": "HM_BUILD_STARPORT_FLAG",
            "frames": FRAME_COUNT,
            "house_colors": list(HOUSE_COLORS),
        },
    }
    (OUTPUT / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(manifest, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
