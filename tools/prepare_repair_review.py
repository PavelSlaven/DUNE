#!/usr/bin/env python3
"""Prepare an approval-ready eight-frame HD Repair Facility atlas."""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts" / "repair_review_v1"
BODY_SOURCE = OUTPUT / "repair_body_alpha.png"
PLATFORM_SOURCE = OUTPUT / "repair_platform_alpha.png"
CLASSIC = (
    ROOT / "resources" / "hd" / "classic" / "sdl_data"
    / "0030_BUILD_REPAIR.png"
)
CLASSIC_SHADOW = (
    ROOT / "resources" / "hd" / "classic" / "sdl_data"
    / "0031_BUILD_REPAIR_SHADOW.png"
)

FRAME_SIZE = (384, 256)
LOGICAL_FRAME = (96, 64)
FRAME_COUNT = 8
ATLAS_SIZE = (384, 2048)
BODY_SIZE = (368, 248)
BODY_POSITION = (8, 4)
PLATFORM_SIZE = (160, 67)
PLATFORM_POSITION = (215, 181)
DOOR_OPENING = (
    (252, 184),
    (346, 184),
    (370, 226),
    (371, 238),
    (212, 238),
    (218, 214),
)
DOOR_TRAVEL = 58

BUILDING_OUT = OUTPUT / "BUILD_REPAIR_HD4_PREVIEW.png"
SHADOW_OUT = OUTPUT / "BUILD_REPAIR_SHADOW_HD4_PREVIEW.png"
BUILDING_HD2_OUT = OUTPUT / "BUILD_REPAIR_HD2_PREVIEW.png"
SHADOW_HD2_OUT = OUTPUT / "BUILD_REPAIR_SHADOW_HD2_PREVIEW.png"
REVIEW_OUT = OUTPUT / "BUILD_REPAIR_REVIEW.png"
ANIMATION_OUT = OUTPUT / "BUILD_REPAIR_ANIMATION_PREVIEW.gif"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    filename = "arialbd.ttf" if bold else "arial.ttf"
    return ImageFont.truetype(
        str(Path("C:/Windows/Fonts") / filename),
        size,
    )


def crop_subject(image: Image.Image, name: str) -> Image.Image:
    box = image.getchannel("A").getbbox()
    if box is None:
        raise AssertionError(f"{name} is fully transparent")
    return image.crop(box)


def fit_body(source: Image.Image) -> Image.Image:
    subject = crop_subject(source, "Repair Facility body")
    subject = subject.resize(BODY_SIZE, Image.Resampling.LANCZOS)
    frame = Image.new("RGBA", FRAME_SIZE)
    frame.alpha_composite(subject, BODY_POSITION)
    return frame


def fit_platform(source: Image.Image) -> Image.Image:
    subject = crop_subject(source, "repair platform")
    return subject.resize(PLATFORM_SIZE, Image.Resampling.LANCZOS)


def door_mask() -> Image.Image:
    mask = Image.new("L", FRAME_SIZE)
    ImageDraw.Draw(mask).polygon(DOOR_OPENING, fill=255)
    return mask


def build_frame(
    body: Image.Image,
    platform: Image.Image,
    phase: int,
) -> Image.Image:
    if phase == 0:
        return body.copy()

    opening = door_mask()
    platform_layer = Image.new("RGBA", FRAME_SIZE)
    platform_layer.alpha_composite(platform, PLATFORM_POSITION)

    result = body.copy()
    bay_background = Image.new("RGBA", FRAME_SIZE, (9, 13, 19, 255))
    result.paste(bay_background, (0, 0), opening)
    platform_layer.putalpha(
        ImageChops.multiply(platform_layer.getchannel("A"), opening)
    )
    result.alpha_composite(platform_layer)

    door = Image.new("RGBA", FRAME_SIZE)
    door.paste(body, (0, 0), opening)
    offset = round(DOOR_TRAVEL * phase / (FRAME_COUNT - 1))
    moved_door = Image.new("RGBA", FRAME_SIZE)
    moved_door.alpha_composite(door, (0, -offset))
    moved_door.putalpha(
        ImageChops.multiply(moved_door.getchannel("A"), opening)
    )
    result.alpha_composite(moved_door)
    return result


def build_shadow(frame: Image.Image) -> Image.Image:
    alpha = frame.getchannel("A").filter(ImageFilter.GaussianBlur(1.4))
    alpha = alpha.point(lambda value: round(value * 0.18))
    shadow = Image.new("RGBA", FRAME_SIZE, (5, 4, 3, 0))
    shadow.putalpha(alpha)
    result = Image.new("RGBA", FRAME_SIZE)
    result.alpha_composite(shadow, (-1, -1))
    return result


def vertical_atlas(frames: list[Image.Image]) -> Image.Image:
    atlas = Image.new("RGBA", ATLAS_SIZE)
    for index, frame in enumerate(frames):
        atlas.alpha_composite(frame, (0, index * FRAME_SIZE[1]))
    return atlas


def atlas_frame(atlas: Image.Image, phase: int) -> Image.Image:
    return atlas.crop(
        (
            0,
            phase * FRAME_SIZE[1],
            FRAME_SIZE[0],
            (phase + 1) * FRAME_SIZE[1],
        )
    )


def downscale_atlas(atlas: Image.Image) -> Image.Image:
    target_frame = (192, 128)
    target = Image.new("RGBA", (192, 1024))
    for phase in range(FRAME_COUNT):
        frame = atlas_frame(atlas, phase).resize(
            target_frame,
            Image.Resampling.LANCZOS,
        )
        target.alpha_composite(frame, (0, phase * target_frame[1]))
    return target


def draw_card(
    board: Image.Image,
    sprite: Image.Image,
    x: int,
    y: int,
    width: int,
    label: str,
) -> None:
    height = round(width * 2 / 3)
    draw = ImageDraw.Draw(board)
    draw.rounded_rectangle(
        (x, y, x + width, y + height + 35),
        radius=7,
        fill=(22, 26, 31, 255),
        outline=(138, 105, 48, 255),
        width=2,
    )
    board.alpha_composite(
        sprite.resize((width, height), Image.Resampling.LANCZOS),
        (x, y),
    )
    draw.text(
        (x + 7, y + height + 6),
        label,
        font=font(16, True),
        fill=(231, 214, 177, 255),
    )


def build_review(building: Image.Image) -> Image.Image:
    board = Image.new("RGBA", (1780, 1040), (9, 12, 16, 255))
    draw = ImageDraw.Draw(board)
    draw.text(
        (34, 24),
        "Ремонтный завод — HD4, 8 кадров",
        font=font(34, True),
        fill=(236, 219, 182, 255),
    )
    draw.text(
        (34, 69),
        "ID 30/31 · логический кадр 96×64 · HD4 384×256",
        font=font(19),
        fill=(187, 193, 201, 255),
    )

    for phase in range(FRAME_COUNT):
        draw_card(
            board,
            atlas_frame(building, phase),
            34 + phase * 216,
            112,
            198,
            f"кадр {phase}",
        )

    draw.text(
        (34, 330),
        "Сверка с исходным атласом и крайние состояния",
        font=font(25, True),
        fill=(225, 188, 98, 255),
    )
    classic = Image.open(CLASSIC).convert("RGBA")
    draw_card(
        board,
        classic.crop((0, 0, 96, 64)),
        34,
        385,
        360,
        "классика: ворота закрыты",
    )
    draw_card(
        board,
        classic.crop((0, 7 * 64, 96, 8 * 64)),
        424,
        385,
        360,
        "классика: ворота открыты",
    )
    draw_card(
        board,
        atlas_frame(building, 0),
        824,
        385,
        420,
        "HD4: кадр 0",
    )
    draw_card(
        board,
        atlas_frame(building, 7),
        1274,
        385,
        420,
        "HD4: кадр 7",
    )
    draw.text(
        (34, 765),
        "Корпус и ремонтная площадка неподвижны. "
        "Внутри проёма поднимаются только створки ворот.",
        font=font(22),
        fill=(187, 193, 201, 255),
    )
    draw.text(
        (34, 807),
        "Игровая последовательность: ворота 0 → 7, удержание, "
        "затем 7 → 0 при выпуске отремонтированного юнита.",
        font=font(22),
        fill=(187, 193, 201, 255),
    )
    return board


def validate(
    body: Image.Image,
    platform: Image.Image,
    building: Image.Image,
    shadow: Image.Image,
) -> dict[str, object]:
    classic = Image.open(CLASSIC)
    classic_shadow = Image.open(CLASSIC_SHADOW)
    if classic.size != (96, 512) or classic_shadow.size != (96, 512):
        raise AssertionError("classic Repair Facility contract changed")
    if building.size != ATLAS_SIZE or shadow.size != ATLAS_SIZE:
        raise AssertionError("invalid Repair Facility atlas size")

    frames = [atlas_frame(building, phase) for phase in range(FRAME_COUNT)]
    bounds = [frame.getchannel("A").getbbox() for frame in frames]
    if len(set(bounds)) != 1:
        raise AssertionError(f"Repair Facility anchors differ: {bounds}")

    opening = door_mask()
    outside = ImageChops.invert(opening)
    static_changed_pixels: list[int] = []
    for frame in frames:
        difference = ImageChops.difference(body, frame)
        outside_difference = Image.new("RGBA", FRAME_SIZE)
        outside_difference.paste(difference, (0, 0), outside)
        static_changed_pixels.append(
            0 if outside_difference.convert("RGB").getbbox() is None else 1
        )
    if any(static_changed_pixels):
        raise AssertionError(
            f"static body changes outside platform: {static_changed_pixels}"
        )

    door_offsets = [
        round(DOOR_TRAVEL * phase / (FRAME_COUNT - 1))
        for phase in range(FRAME_COUNT)
    ]
    if door_offsets != sorted(door_offsets):
        raise AssertionError(f"door motion is not monotonic: {door_offsets}")

    hd2 = downscale_atlas(building)
    if hd2.size != (192, 1024):
        raise AssertionError("invalid HD2 Repair Facility size")
    return {
        "frame_bounds": bounds,
        "door_offsets": door_offsets,
        "static_changed_pixels": static_changed_pixels,
        "hd2_size": list(hd2.size),
    }


def save_animation(building: Image.Image) -> None:
    phases = list(range(8)) + [7, 7] + list(range(6, -1, -1))
    frames = [
        atlas_frame(building, phase).resize(
            (480, 320),
            Image.Resampling.LANCZOS,
        )
        for phase in phases
    ]
    frames[0].save(
        ANIMATION_OUT,
        save_all=True,
        append_images=frames[1:],
        duration=[160] * 8 + [400, 400] + [160] * 7,
        loop=0,
        disposal=2,
    )


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for path in (BODY_SOURCE, PLATFORM_SOURCE):
        if not path.is_file():
            raise FileNotFoundError(path)

    body = fit_body(Image.open(BODY_SOURCE).convert("RGBA"))
    platform = fit_platform(
        Image.open(PLATFORM_SOURCE).convert("RGBA")
    )
    frames = [
        build_frame(body, platform, phase)
        for phase in range(FRAME_COUNT)
    ]
    building = vertical_atlas(frames)
    static_shadow = build_shadow(body)
    shadow = vertical_atlas(
        [static_shadow.copy() for _ in range(FRAME_COUNT)]
    )
    validation = validate(body, platform, building, shadow)

    building.save(BUILDING_OUT, optimize=True)
    shadow.save(SHADOW_OUT, optimize=True)
    downscale_atlas(building).save(BUILDING_HD2_OUT, optimize=True)
    downscale_atlas(shadow).save(SHADOW_HD2_OUT, optimize=True)
    build_review(building).save(REVIEW_OUT, optimize=True)
    save_animation(building)

    manifest = {
        "format": 1,
        "status": "approval_preview",
        "resource": {
            "id": 30,
            "name": "BUILD_REPAIR",
            "shadow_id": 31,
            "shadow_name": "BUILD_REPAIR_SHADOW",
            "frames": FRAME_COUNT,
            "logical_frame": list(LOGICAL_FRAME),
            "hd2_atlas": [192, 1024],
            "hd4_atlas": list(ATLAS_SIZE),
        },
        "animation": {
            "frame_0": "repair bay door closed",
            "frames_1_to_6": "door moves upward",
            "frame_7": "door fully open and held",
            "runtime": "0 to 7, hold, 7 to 0",
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
