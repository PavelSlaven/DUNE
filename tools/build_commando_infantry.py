#!/usr/bin/env python3
"""Build D2TM infantry from the Commando enemy-soldier sheet.

The RUN section contains eight directions with five animation frames each.
Only four frames are needed by D2TM.  The original pose and silhouette are
preserved; the HD4 pass adds antialiased edges, neutral materials, a restrained
House mask and a direction-locked launcher for the two trooper resources.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from build_dune2000_units import remaster_subject, resize_premultiplied


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "resources" / "hd" / "source_references" / "preview3"
SOURCE = SOURCE_DIR / "commando_enemy_soldiers_281892.png"
CLASSIC = ROOT / "resources" / "hd" / "classic" / "sdl_data"
MASTER = ROOT / "resources" / "hd" / "master4" / "sdl_data"
EXTRA = ROOT / "resources" / "hd" / "master4_extra_packs" / "sdl_data"
PREVIEW = ROOT / "resources" / "hd" / "previews" / "ru4"

FRAME_SIZE = 128
ATLAS_COLUMNS = 8
ATLAS_ROWS = 4

# D2TM: E, NE, N, NW, W, SW, S, SE.
DIRECTION_NAMES = ("E", "NE", "N", "NW", "W", "SW", "S", "SE")
DIRECTION_VECTORS = (
    (1.0, 0.0),
    (math.sqrt(0.5), -math.sqrt(0.5)),
    (0.0, -1.0),
    (-math.sqrt(0.5), -math.sqrt(0.5)),
    (-1.0, 0.0),
    (-math.sqrt(0.5), math.sqrt(0.5)),
    (0.0, 1.0),
    (math.sqrt(0.5), math.sqrt(0.5)),
)

# Commando RUN groups are ordered SW, S, SE, E, NE, N, NW, W.
COMMANDO_GROUP_FOR_D2TM = (3, 4, 5, 6, 7, 0, 1, 2)

ROLE_RECIPES = (
    {
        "resource_id": 155,
        "resource_name": "UNIT_SOLDIER",
        "label": "Солдат",
        "group": False,
        "launcher": False,
        "target_height": 32,
    },
    {
        "resource_id": 156,
        "resource_name": "UNIT_SOLDIERS",
        "label": "Отряд автоматчиков",
        "group": True,
        "launcher": False,
        "target_height": 29,
    },
    {
        "resource_id": 165,
        "resource_name": "UNIT_TROOPER",
        "label": "Гранатомётчик",
        "group": False,
        "launcher": True,
        "target_height": 33,
    },
    {
        "resource_id": 166,
        "resource_name": "UNIT_TROOPERS",
        "label": "Отряд гранатомётчиков",
        "group": True,
        "launcher": True,
        "target_height": 30,
    },
)


def classic_path(resource_id: int) -> Path:
    return next(CLASSIC.glob(f"{resource_id:04d}_*.png"))


def master_path(resource_id: int) -> Path:
    return MASTER / classic_path(resource_id).name


def is_background(red: int, green: int, blue: int) -> bool:
    magenta = (
        red > 135
        and blue > 135
        and red > green * 1.55
        and blue > green * 1.55
    )
    sheet_red = red > 135 and green < 24 and blue < 24
    frame_blue = blue > 190 and red < 120 and green < 140
    return magenta or sheet_red or frame_blue


def extract_run_frame(direction: int, animation: int) -> Image.Image:
    sheet = Image.open(SOURCE).convert("RGBA")
    group = COMMANDO_GROUP_FOR_D2TM[direction]
    source_index = group * 5 + animation
    left = 1 + source_index * 19
    frame = sheet.crop((left, 11, left + 18, 37))

    cleaned = Image.new("RGBA", frame.size)
    pixels: list[tuple[int, int, int, int]] = []
    for red, green, blue, alpha in frame.getdata():
        if alpha == 0 or is_background(red, green, blue):
            pixels.append((0, 0, 0, 0))
        else:
            pixels.append((red, green, blue, alpha))
    cleaned.putdata(pixels)
    bounds = cleaned.getchannel("A").getbbox()
    if bounds is None:
        raise ValueError(
            f"empty Commando frame: direction={direction}, "
            f"animation={animation}"
        )
    return cleaned.crop(bounds)


def neutralize(
    image: Image.Image,
) -> tuple[Image.Image, Image.Image]:
    source = image.convert("RGBA")
    bounds = source.getchannel("A").getbbox()
    if bounds is None:
        raise ValueError("empty Commando subject")
    left = bounds[0]
    top = bounds[1]
    width = max(1, bounds[2] - bounds[0])
    height = max(1, bounds[3] - bounds[1])

    body = Image.new("RGBA", source.size)
    mask = Image.new("RGBA", source.size)
    body_pixels: list[tuple[int, int, int, int]] = []
    mask_pixels: list[tuple[int, int, int, int]] = []
    for y in range(source.height):
        for x in range(source.width):
            red, green, blue, alpha = source.getpixel((x, y))
            if alpha == 0:
                body_pixels.append((0, 0, 0, 0))
                mask_pixels.append((255, 255, 255, 0))
                continue

            luminance = 0.299 * red + 0.587 * green + 0.114 * blue
            uniform = (
                green > red * 0.82
                and green > blue * 0.92
                and luminance > 34
            )
            metal = blue > red * 1.12 and blue > green * 1.05
            if uniform:
                value = max(34, min(172, round(30 + luminance * 0.78)))
                color = (
                    round(value * 0.96),
                    value,
                    round(value * 0.83),
                    alpha,
                )
            elif metal:
                value = max(30, min(178, round(24 + luminance * 0.82)))
                color = (
                    round(value * 0.78),
                    round(value * 0.88),
                    value,
                    alpha,
                )
            else:
                color = (red, green, blue, alpha)
            body_pixels.append(color)

            relative_x = (x - left) / width
            relative_y = (y - top) / height
            armour_panel = (
                uniform
                and 0.27 <= relative_x <= 0.73
                and 0.22 <= relative_y <= 0.39
            )
            mask_alpha = 110 if armour_panel else 0
            mask_pixels.append((255, 255, 255, mask_alpha))

    body.putdata(body_pixels)
    mask.putdata(mask_pixels)
    return body, mask


def resize_pair(
    body: Image.Image,
    mask: Image.Image,
    target_height: int,
) -> tuple[Image.Image, Image.Image]:
    scale = target_height / max(1, body.height)
    target_size = (
        max(1, round(body.width * scale)),
        target_height,
    )
    return (
        remaster_subject(body, target_size),
        resize_premultiplied(mask, target_size),
    )


def source_frame(
    direction: int,
    animation: int,
    target_height: int,
) -> tuple[Image.Image, Image.Image]:
    body, mask = neutralize(extract_run_frame(direction, animation))
    return resize_pair(body, mask, target_height)


def composite_at_anchor(
    canvas: Image.Image,
    subject: Image.Image,
    center_x: int,
    bottom_y: int,
) -> None:
    canvas.alpha_composite(
        subject,
        (
            round(center_x - subject.width / 2),
            bottom_y - subject.height,
        ),
    )


def draw_launcher(
    frame: Image.Image,
    direction: int,
    center_x: int,
    bottom_y: int,
    target_height: int,
) -> None:
    forward_x, forward_y = DIRECTION_VECTORS[direction]
    shoulder_y = bottom_y - round(target_height * 0.66)
    start = (
        round(center_x - forward_x * 11),
        round(shoulder_y - forward_y * 7),
    )
    end = (
        round(center_x + forward_x * 18),
        round(shoulder_y + forward_y * 12),
    )
    drawer = ImageDraw.Draw(frame)
    drawer.line((start, end), fill=(9, 25, 31, 255), width=7)
    drawer.line((start, end), fill=(21, 104, 126, 255), width=4)
    muzzle = (
        round(end[0] + forward_x * 2),
        round(end[1] + forward_y * 2),
    )
    drawer.ellipse(
        (muzzle[0] - 3, muzzle[1] - 3, muzzle[0] + 3, muzzle[1] + 3),
        fill=(18, 45, 52, 255),
    )


def single_frame(
    direction: int,
    animation: int,
    target_height: int,
    launcher: bool,
) -> tuple[Image.Image, Image.Image]:
    body, mask = source_frame(direction, animation, target_height)
    body_frame = Image.new("RGBA", (FRAME_SIZE, FRAME_SIZE))
    mask_frame = Image.new("RGBA", (FRAME_SIZE, FRAME_SIZE))
    bob = (0, -2, 0, 1)[animation]
    composite_at_anchor(body_frame, body, 64, 102 + bob)
    composite_at_anchor(mask_frame, mask, 64, 102 + bob)
    if launcher:
        draw_launcher(body_frame, direction, 64, 102 + bob, target_height)
    return body_frame, mask_frame


def group_frame(
    direction: int,
    animation: int,
    target_height: int,
    launcher: bool,
) -> tuple[Image.Image, Image.Image]:
    forward_x, forward_y = DIRECTION_VECTORS[direction]
    side_x, side_y = -forward_y, forward_x
    placements = (
        (forward_x * 14, forward_y * 14, animation),
        (
            -forward_x * 7 + side_x * 17,
            -forward_y * 7 + side_y * 17,
            (animation + 1) % ATLAS_ROWS,
        ),
        (
            -forward_x * 7 - side_x * 17,
            -forward_y * 7 - side_y * 17,
            (animation + 3) % ATLAS_ROWS,
        ),
    )
    placements = tuple(sorted(placements, key=lambda item: item[1]))
    body_frame = Image.new("RGBA", (FRAME_SIZE, FRAME_SIZE))
    mask_frame = Image.new("RGBA", (FRAME_SIZE, FRAME_SIZE))
    for offset_x, offset_y, phase in placements:
        body, mask = source_frame(direction, phase, target_height)
        bob = (0, -2, 0, 1)[phase]
        center_x = round(64 + offset_x)
        bottom_y = round(102 + offset_y + bob)
        composite_at_anchor(body_frame, body, center_x, bottom_y)
        composite_at_anchor(mask_frame, mask, center_x, bottom_y)
        if launcher:
            draw_launcher(
                body_frame,
                direction,
                center_x,
                bottom_y,
                target_height,
            )
    return body_frame, mask_frame


def build_role(recipe: dict[str, object]) -> tuple[Image.Image, Image.Image]:
    body_atlas = Image.new(
        "RGBA",
        (FRAME_SIZE * ATLAS_COLUMNS, FRAME_SIZE * ATLAS_ROWS),
    )
    mask_atlas = Image.new("RGBA", body_atlas.size)
    builder = group_frame if bool(recipe["group"]) else single_frame
    for animation in range(ATLAS_ROWS):
        for direction in range(ATLAS_COLUMNS):
            body, mask = builder(
                direction,
                animation,
                int(recipe["target_height"]),
                bool(recipe["launcher"]),
            )
            position = (
                direction * FRAME_SIZE,
                animation * FRAME_SIZE,
            )
            body_atlas.alpha_composite(body, position)
            mask_atlas.alpha_composite(mask, position)

    resource_id = int(recipe["resource_id"])
    body_atlas.save(master_path(resource_id))
    mask_atlas.putalpha(
        mask_atlas.getchannel("A").point(lambda value: min(value, 110))
    )
    mask_atlas.save(
        EXTRA / f"HOUSEMASK_{recipe['resource_name']}.png"
    )
    return body_atlas, mask_atlas


def build_preview(
    atlases: list[tuple[dict[str, object], Image.Image]],
) -> None:
    cell = 128
    label_height = 26
    preview = Image.new(
        "RGBA",
        (
            cell * ATLAS_COLUMNS,
            (cell + label_height) * len(atlases),
        ),
        (23, 25, 28, 255),
    )
    font = ImageFont.truetype(
        ROOT / "resources" / "bin" / "data" / "PTSansNarrow-Regular.ttf",
        19,
    )
    drawer = ImageDraw.Draw(preview)
    for row, (recipe, atlas) in enumerate(atlases):
        y = row * (cell + label_height)
        drawer.text(
            (6, y + 2),
            str(recipe["label"]),
            font=font,
            fill=(238, 211, 153, 255),
        )
        for direction in range(ATLAS_COLUMNS):
            frame = atlas.crop(
                (
                    direction * FRAME_SIZE,
                    0,
                    (direction + 1) * FRAME_SIZE,
                    FRAME_SIZE,
                )
            )
            preview.alpha_composite(
                frame,
                (direction * cell, y + label_height),
            )
    PREVIEW.mkdir(parents=True, exist_ok=True)
    preview.save(PREVIEW / "commando_infantry_roles.png")


def write_manifest() -> None:
    manifest = {
        "release": "v0.8.0-ru4-preview3",
        "source": "Enemy Soldiers (DE) - Commando",
        "page_url": (
            "https://www.spriters-resource.com/"
            "arcade/commando/asset/281892/"
        ),
        "source_file": SOURCE.name,
        "source_sha256": (
            "fbf0fb089333fe46ba3a879545a67e75"
            "aa8a6fd9f5284086c69443961bbee0cf"
        ),
        "direction_order": list(DIRECTION_NAMES),
        "source_group_order": [
            "SW",
            "S",
            "SE",
            "E",
            "NE",
            "N",
            "NW",
            "W",
        ],
        "roles": [
            {
                key: recipe[key]
                for key in (
                    "resource_id",
                    "resource_name",
                    "label",
                    "group",
                    "launcher",
                    "target_height",
                )
            }
            for recipe in ROLE_RECIPES
        ],
        "notes": [
            "RUN supplies the eight body directions and four walk frames.",
            "The launcher uses the cyan/steel visual language of the source ROCKET LAUNCHER group and is locked to the D2TM direction vector.",
            "Uniforms are neutralized; only a restrained symmetric chest armour panel receives House colour.",
        ],
    }
    (SOURCE_DIR / "commando_infantry_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def build_all() -> None:
    if not SOURCE.is_file():
        raise FileNotFoundError(SOURCE)
    MASTER.mkdir(parents=True, exist_ok=True)
    EXTRA.mkdir(parents=True, exist_ok=True)
    atlases: list[tuple[dict[str, object], Image.Image]] = []
    for recipe in ROLE_RECIPES:
        atlas, _mask = build_role(recipe)
        atlases.append((recipe, atlas))
    build_preview(atlases)
    write_manifest()
    print("Commando infantry: 4 HD4 atlases, 8 directions, 4 rows")


if __name__ == "__main__":
    build_all()
