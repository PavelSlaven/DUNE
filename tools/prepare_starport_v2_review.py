#!/usr/bin/env python3
"""Prepare the second approval preview of the HD Starport."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts" / "starport_review_v2"
SOURCE = OUTPUT / "starport_v2_alpha.png"
CARGO_SOURCE = (
    ROOT / "artifacts" / "starport_review_v1"
    / "cargo_container_alpha.png"
)
CLASSIC = (
    ROOT / "resources" / "hd" / "classic" / "sdl_data"
    / "0036_BUILD_STARPORT.png"
)
CLASSIC_SHADOW = (
    ROOT / "resources" / "hd" / "classic" / "sdl_data"
    / "0037_BUILD_STARPORT_SHADOW.png"
)

FRAME = 384
LOGICAL_FRAME = 96
FRAME_COUNT = 8
ATLAS_SIZE = (FRAME, FRAME * FRAME_COUNT)

BUILDING_OUT = OUTPUT / "BUILD_STARPORT_HD4_PREVIEW.png"
SHADOW_OUT = OUTPUT / "BUILD_STARPORT_SHADOW_HD4_PREVIEW.png"
OVERLAY_OUT = OUTPUT / "BUILD_STARPORT_FLAG_HD4_PREVIEW.png"
MASK_OUT = OUTPUT / "HM_BUILD_STARPORT_FLAG_HD4_PREVIEW.png"
BUILDING_HD2_OUT = OUTPUT / "BUILD_STARPORT_HD2_PREVIEW.png"
SHADOW_HD2_OUT = OUTPUT / "BUILD_STARPORT_SHADOW_HD2_PREVIEW.png"
OVERLAY_HD2_OUT = OUTPUT / "BUILD_STARPORT_FLAG_HD2_PREVIEW.png"
MASK_HD2_OUT = OUTPUT / "HM_BUILD_STARPORT_FLAG_HD2_PREVIEW.png"
REVIEW_OUT = OUTPUT / "BUILD_STARPORT_REVIEW.png"
ANIMATION_OUT = OUTPUT / "BUILD_STARPORT_ANIMATION_PREVIEW.gif"

HOUSE_COLORS = {
    "Харконнены": (228, 28, 24),
    "Атрейдесы": (30, 94, 230),
    "Ордос": (26, 210, 64),
    "Император": (142, 52, 190),
    "Наёмники": (218, 180, 38),
    "Фримены": (22, 174, 176),
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
    scale = min(372 / subject.width, 372 / subject.height)
    subject = subject.resize(
        (
            round(subject.width * scale),
            round(subject.height * scale),
        ),
        Image.Resampling.LANCZOS,
    )
    frame = Image.new("RGBA", (FRAME, FRAME))
    frame.alpha_composite(
        subject,
        (
            (FRAME - subject.width) // 2,
            FRAME - subject.height - 4,
        ),
    )
    return frame


def landing_light_mask(base: Image.Image) -> np.ndarray:
    rgba = np.asarray(base.convert("RGBA"), dtype=np.float32)
    yy, xx = np.mgrid[0:FRAME, 0:FRAME]
    return (
        (rgba[:, :, 3] > 64)
        & (rgba[:, :, 0] > 100)
        & (rgba[:, :, 0] > rgba[:, :, 1] * 1.35)
        & (rgba[:, :, 0] > rgba[:, :, 2] * 1.12)
        & (xx < 270)
        & (yy > 132)
    )


def animate_landing_lights(base: Image.Image, phase: int) -> Image.Image:
    if phase == 7:
        return base.copy()

    rgba = np.asarray(base.convert("RGBA"), dtype=np.float32).copy()
    red = landing_light_mask(base)
    yy, _ = np.mgrid[0:FRAME, 0:FRAME]
    groups = (
        yy < 205,
        (yy >= 205) & (yy < 245),
        (yy >= 245) & (yy < 280),
        (yy >= 280) & (yy < 320),
        yy >= 320,
    )
    active_groups = {
        0: (),
        1: (0,),
        2: (0, 1),
        3: (1, 2),
        4: (2, 3),
        5: (3, 4),
        6: (0, 1, 2, 3, 4),
    }[phase]
    for index, group in enumerate(groups):
        selected = red & group
        if index in active_groups:
            rgba[:, :, 0][selected] = np.minimum(
                255,
                rgba[:, :, 0][selected] * 1.18 + 28,
            )
            rgba[:, :, 1][selected] *= 0.72
            rgba[:, :, 2][selected] *= 0.72
        else:
            rgba[:, :, 0][selected] *= 0.40
            rgba[:, :, 1][selected] *= 0.46
            rgba[:, :, 2][selected] *= 0.46
    return Image.fromarray(
        np.clip(rgba, 0, 255).astype(np.uint8),
        "RGBA",
    )


def neutralize_cargo_lamps(cargo: Image.Image) -> Image.Image:
    rgba = np.asarray(cargo.convert("RGBA"), dtype=np.uint8).copy()
    rgb = rgba[:, :, :3].astype(np.int16)
    warm = (
        (rgba[:, :, 3] > 48)
        & (rgb[:, :, 0] > 55)
        & ((rgb[:, :, 0] - rgb[:, :, 1]) > 5)
        & ((rgb[:, :, 0] - rgb[:, :, 2]) > 10)
    )
    neutral = np.clip(
        rgba[:, :, :3].mean(axis=2) * 0.65,
        30,
        118,
    ).astype(np.uint8)
    for channel in range(3):
        rgba[:, :, channel][warm] = neutral[warm]
    return Image.fromarray(rgba, "RGBA")


def cargo_frame(base: Image.Image, cargo_source: Image.Image) -> Image.Image:
    result = base.copy()
    draw = ImageDraw.Draw(result)
    pad_box = (30, 135, 270, 378)
    draw.rounded_rectangle(
        pad_box,
        radius=7,
        fill=(52, 57, 67, 255),
        outline=(112, 116, 126, 255),
        width=3,
    )

    cargo_box = cargo_source.getchannel("A").getbbox()
    if cargo_box is None:
        raise AssertionError("cargo source is fully transparent")
    cargo = neutralize_cargo_lamps(cargo_source.crop(cargo_box))
    cargo = cargo.resize((103, 224), Image.Resampling.LANCZOS)
    left = cargo
    right = cargo.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    result.alpha_composite(left, (42, 144))
    result.alpha_composite(right, (151, 144))

    # Restore the terminal roof where it overlaps the upper edge of the pad.
    terminal_mask = Image.new("L", (FRAME, FRAME))
    terminal_draw = ImageDraw.Draw(terminal_mask)
    terminal_draw.polygon(
        (
            (133, 14),
            (251, 14),
            (272, 50),
            (257, 111),
            (225, 144),
            (151, 144),
            (119, 111),
            (108, 52),
        ),
        fill=255,
    )
    terminal_mask = terminal_mask.filter(ImageFilter.GaussianBlur(0.35))
    return Image.composite(base, result, terminal_mask)


def sphere_mask(base: Image.Image) -> Image.Image:
    mask = Image.new("L", (FRAME, FRAME))
    draw = ImageDraw.Draw(mask)
    # Only the faceted spherical surfaces, not their tan collars or towers.
    draw.ellipse((296, 19, 354, 78), fill=255)
    draw.ellipse((294, 147, 353, 206), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(0.45))
    alpha = base.getchannel("A")
    return ImageChops.multiply(mask, alpha)


def build_house_overlay(
    base: Image.Image,
) -> tuple[Image.Image, Image.Image]:
    mask_alpha = sphere_mask(base)
    overlay_frame = Image.new("RGBA", (FRAME, FRAME))
    overlay_frame.paste(base, (0, 0), mask_alpha)
    mask_frame = Image.new("RGBA", (FRAME, FRAME), (255, 255, 255, 0))
    mask_frame.putalpha(mask_alpha)
    return (
        vertical_atlas([overlay_frame] * FRAME_COUNT),
        vertical_atlas([mask_frame] * FRAME_COUNT),
    )


def build_shadow(base: Image.Image) -> Image.Image:
    alpha = base.getchannel("A").filter(ImageFilter.GaussianBlur(1.5))
    alpha = alpha.point(lambda value: round(value * 0.18))
    shadow = Image.new("RGBA", (FRAME, FRAME), (5, 4, 3, 0))
    shadow.putalpha(alpha)
    result = Image.new("RGBA", (FRAME, FRAME))
    result.alpha_composite(shadow, (-1, -1))
    return result


def vertical_atlas(frames: list[Image.Image]) -> Image.Image:
    atlas = Image.new("RGBA", (FRAME, FRAME * len(frames)))
    for index, frame in enumerate(frames):
        atlas.alpha_composite(frame, (0, index * FRAME))
    return atlas


def atlas_frame(atlas: Image.Image, phase: int) -> Image.Image:
    return atlas.crop(
        (0, phase * FRAME, FRAME, (phase + 1) * FRAME)
    )


def downscale_atlas(atlas: Image.Image) -> Image.Image:
    result = Image.new("RGBA", (FRAME // 2, FRAME * FRAME_COUNT // 2))
    for phase in range(FRAME_COUNT):
        frame = atlas_frame(atlas, phase).resize(
            (FRAME // 2, FRAME // 2),
            Image.Resampling.LANCZOS,
        )
        result.alpha_composite(frame, (0, phase * FRAME // 2))
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
    overlay: Image.Image,
    mask: Image.Image,
    phase: int,
    color: tuple[int, int, int],
) -> Image.Image:
    result = atlas_frame(building, phase)
    result.alpha_composite(
        apply_engine_tint(
            atlas_frame(overlay, phase),
            atlas_frame(mask, phase),
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
    overlay: Image.Image,
    mask: Image.Image,
) -> Image.Image:
    board = Image.new("RGBA", (1740, 1390), (9, 12, 16, 255))
    draw = ImageDraw.Draw(board)
    draw.text(
        (34, 24),
        "Космопорт — HD4, 8 кадров, цветные сферы",
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
                overlay,
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
        "Окраска Дома: только две сферы справа, без флага",
        font=font(25, True),
        fill=(225, 188, 98, 255),
    )
    preview_names = ("Харконнены", "Атрейдесы", "Ордос")
    for index, name in enumerate(preview_names):
        draw_card(
            board,
            composed(
                building,
                overlay,
                mask,
                3,
                HOUSE_COLORS[name],
            ),
            34 + index * 390,
            400,
            350,
            name,
        )
    draw_card(board, atlas_frame(mask, 0), 1204, 400, 350, "маска сфер")

    draw.text(
        (34, 815),
        "Кадр доставки и сверка с классическим атласом",
        font=font(25, True),
        fill=(225, 188, 98, 255),
    )
    classic = Image.open(CLASSIC).convert("RGBA")
    draw_card(
        board,
        classic.crop((0, 0, 96, 96)),
        34,
        860,
        300,
        "классика: кадр 0",
    )
    draw_card(
        board,
        classic.crop((0, 7 * 96, 96, 8 * 96)),
        364,
        860,
        300,
        "классика: кадр 7",
    )
    draw_card(
        board,
        composed(
            building,
            overlay,
            mask,
            0,
            HOUSE_COLORS["Ордос"],
        ),
        714,
        860,
        300,
        "HD4: ожидание",
    )
    draw_card(
        board,
        composed(
            building,
            overlay,
            mask,
            7,
            HOUSE_COLORS["Ордос"],
        ),
        1044,
        860,
        300,
        "HD4: груз доставлен",
    )
    draw.text(
        (34, 1245),
        "Кадры 0–6 циклически ведут огни к центру; кадр 7 "
        "показывает груз на всей площадке.",
        font=font(21),
        fill=(187, 193, 201, 255),
    )
    return board


def validate(
    building: Image.Image,
    shadow: Image.Image,
    overlay: Image.Image,
    mask: Image.Image,
) -> dict[str, object]:
    classic = Image.open(CLASSIC)
    classic_shadow = Image.open(CLASSIC_SHADOW)
    if classic.size != (96, 768) or classic_shadow.size != (96, 768):
        raise AssertionError("classic Starport atlas contract changed")
    for name, image in {
        "building": building,
        "shadow": shadow,
        "house overlay": overlay,
        "house mask": mask,
    }.items():
        if image.size != ATLAS_SIZE:
            raise AssertionError(f"{name} has size {image.size}")
        if image.getchannel("A").getbbox() is None:
            raise AssertionError(f"{name} is fully transparent")

    frames = [atlas_frame(building, phase) for phase in range(FRAME_COUNT)]
    base_boxes = [frame.getchannel("A").getbbox() for frame in frames]
    if len(set(base_boxes)) != 1:
        raise AssertionError(f"Starport anchor changes: {base_boxes}")
    if any(
        not ImageChops.difference(
            frames[index - 1].convert("RGB"),
            frames[index].convert("RGB"),
        ).getbbox()
        for index in range(1, FRAME_COUNT)
    ):
        raise AssertionError("duplicate Starport animation frames")

    mask_frames = [atlas_frame(mask, phase) for phase in range(FRAME_COUNT)]
    if any(
        ImageChops.difference(mask_frames[0], item).getbbox()
        for item in mask_frames[1:]
    ):
        raise AssertionError("sphere mask changes between animation frames")
    mask_box = mask_frames[0].getchannel("A").getbbox()
    if mask_box is None or mask_box[0] < 290 or mask_box[2] > 360:
        raise AssertionError(f"sphere mask escaped right-side domes: {mask_box}")

    building2 = downscale_atlas(building)
    if building2.size != (192, 1536):
        raise AssertionError("unexpected HD2 Starport size")
    return {
        "frame_bounds": base_boxes,
        "sphere_mask_bounds": mask_box,
        "hd2_size": building2.size,
    }


def save_animation(
    building: Image.Image,
    overlay: Image.Image,
    mask: Image.Image,
) -> None:
    phases = [0, 1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1, 0, 7]
    frames = [
        composed(
            building,
            overlay,
            mask,
            phase,
            HOUSE_COLORS["Ордос"],
        ).resize((320, 320), Image.Resampling.LANCZOS)
        for phase in phases
    ]
    frames[0].save(
        ANIMATION_OUT,
        save_all=True,
        append_images=frames[1:],
        duration=[180] * (len(frames) - 1) + [650],
        loop=0,
        disposal=2,
    )


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    if not SOURCE.is_file() or not CARGO_SOURCE.is_file():
        raise FileNotFoundError("Starport source or cargo source is missing")

    base = fit_building(Image.open(SOURCE).convert("RGBA"))
    frames = [
        animate_landing_lights(base, phase)
        for phase in range(7)
    ]
    frames.append(
        cargo_frame(
            base,
            Image.open(CARGO_SOURCE).convert("RGBA"),
        )
    )
    building = vertical_atlas(frames)
    shadow = vertical_atlas([build_shadow(base)] * FRAME_COUNT)
    overlay, mask = build_house_overlay(base)
    validation = validate(building, shadow, overlay, mask)

    building.save(BUILDING_OUT, optimize=True)
    shadow.save(SHADOW_OUT, optimize=True)
    overlay.save(OVERLAY_OUT, optimize=True)
    mask.save(MASK_OUT, optimize=True)
    for atlas, output in (
        (building, BUILDING_HD2_OUT),
        (shadow, SHADOW_HD2_OUT),
        (overlay, OVERLAY_HD2_OUT),
        (mask, MASK_HD2_OUT),
    ):
        downscale_atlas(atlas).save(output, optimize=True)

    build_review(building, overlay, mask).save(REVIEW_OUT, optimize=True)
    save_animation(building, overlay, mask)

    manifest = {
        "format": 1,
        "status": "approval_preview",
        "resource": {
            "id": 36,
            "name": "BUILD_STARPORT",
            "shadow_id": 37,
            "shadow_name": "BUILD_STARPORT_SHADOW",
            "frames": FRAME_COUNT,
            "logical_frame": [LOGICAL_FRAME, LOGICAL_FRAME],
            "hd2_atlas": [192, 1536],
            "hd4_atlas": list(ATLAS_SIZE),
        },
        "animation": {
            "frames_0_to_6": "landing lights lead toward the pad center",
            "frame_7": "two-module cargo covering the landing pad",
        },
        "house_marker": {
            "resource_name": "BUILD_STARPORT_FLAG",
            "mask_name": "HM_BUILD_STARPORT_FLAG",
            "description": "two right-side spherical domes only",
            "frames": FRAME_COUNT,
            "house_colors": list(HOUSE_COLORS),
        },
        "validation": validation,
        "installed": False,
    }
    (OUTPUT / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(manifest, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
