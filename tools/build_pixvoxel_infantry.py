#!/usr/bin/env python3
"""Build the four D2TM infantry atlases from the CC0 PixVoxel set."""

from __future__ import annotations

import json
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from build_dune2000_units import remaster_subject, resize_premultiplied


ROOT = Path(__file__).resolve().parents[1]
SOURCE = (
    ROOT
    / "resources"
    / "hd"
    / "source_references"
    / "pixvoxel_infantry"
)
CLASSIC = ROOT / "resources" / "hd" / "classic" / "sdl_data"
MASTER = ROOT / "resources" / "hd" / "master4" / "sdl_data"
EXTRA = ROOT / "resources" / "hd" / "master4_extra_packs" / "sdl_data"
PREVIEW = ROOT / "resources" / "hd" / "previews" / "ru4"

FRAME_SIZE = 128
ATLAS_COLUMNS = 8
ATLAS_ROWS = 4

# D2TM direction order: E, NE, N, NW, W, SW, S, SE.
DIRECTION_SOURCES = (
    ("orthogonal", 3),
    ("isometric", 3),
    ("orthogonal", 2),
    ("isometric", 2),
    ("orthogonal", 1),
    ("isometric", 1),
    ("orthogonal", 0),
    ("isometric", 0),
)
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

ROLE_RECIPES = (
    {
        "resource_id": 155,
        "resource_name": "UNIT_SOLDIER",
        "source_name": "Infantry_Large",
        "group": False,
        "label": "Солдат",
        "target_height": 50,
    },
    {
        "resource_id": 156,
        "resource_name": "UNIT_SOLDIERS",
        "source_name": "Infantry_Large",
        "group": True,
        "label": "Отряд автоматчиков",
        "target_height": 46,
    },
    {
        "resource_id": 165,
        "resource_name": "UNIT_TROOPER",
        "source_name": "Infantry_P_Large",
        "group": False,
        "label": "Гранатомётчик",
        "target_height": 52,
    },
    {
        "resource_id": 166,
        "resource_name": "UNIT_TROOPERS",
        "source_name": "Infantry_P_Large",
        "group": True,
        "label": "Отряд гранатомётчиков",
        "target_height": 48,
    },
)


def classic_path(resource_id: int) -> Path:
    return next(CLASSIC.glob(f"{resource_id:04d}_*.png"))


def master_path(resource_id: int) -> Path:
    return MASTER / classic_path(resource_id).name


def neutralize_palette(
    image: Image.Image,
) -> tuple[Image.Image, Image.Image]:
    """Return neutral body art and a restrained upper-body house mask."""
    source = image.convert("RGBA")
    alpha = source.getchannel("A")
    bounds = alpha.getbbox()
    if bounds is None:
        return source, Image.new("RGBA", source.size)

    top = bounds[1]
    height = max(1, bounds[3] - bounds[1])
    body = Image.new("RGBA", source.size)
    mask = Image.new("RGBA", source.size)
    body_pixels: list[tuple[int, int, int, int]] = []
    mask_pixels: list[tuple[int, int, int, int]] = []

    for y in range(source.height):
        for x in range(source.width):
            red, green, blue, opacity = source.getpixel((x, y))
            if opacity == 0:
                body_pixels.append((0, 0, 0, 0))
                mask_pixels.append((255, 255, 255, 0))
                continue

            luminance = 0.299 * red + 0.587 * green + 0.114 * blue
            red_uniform = (
                red > 72
                and red > green * 1.28
                and red > blue * 1.18
            )
            purple_weapon = (
                blue > 70
                and blue > green * 1.08
                and red > green * 1.02
            )
            skin = (
                red > 105
                and red > green * 1.08
                and green > blue * 1.18
            )

            if red_uniform:
                value = max(32, min(148, round(34 + luminance * 0.68)))
                color = (
                    min(255, round(value * 1.06)),
                    min(255, round(value * 0.98)),
                    min(255, round(value * 0.84)),
                    opacity,
                )
            elif purple_weapon:
                value = max(38, min(168, round(28 + luminance * 0.72)))
                color = (
                    min(255, round(value * 0.90)),
                    min(255, round(value * 0.94)),
                    min(255, round(value * 1.02)),
                    opacity,
                )
            elif skin:
                color = (
                    min(255, round(red * 0.94)),
                    min(255, round(green * 0.88)),
                    min(255, round(blue * 0.78)),
                    opacity,
                )
            else:
                color = (red, green, blue, opacity)
            body_pixels.append(color)

            relative_y = (y - top) / height
            upper_body = 0.18 <= relative_y <= 0.62
            strength = 225 if red_uniform and upper_body else 0
            mask_pixels.append((255, 255, 255, strength))

    body.putdata(body_pixels)
    mask.putdata(mask_pixels)
    return body, mask


def crop_pair(
    body: Image.Image,
    mask: Image.Image,
) -> tuple[Image.Image, Image.Image]:
    bounds = body.getchannel("A").getbbox()
    if bounds is None:
        raise ValueError("empty PixVoxel infantry frame")
    return body.crop(bounds), mask.crop(bounds)


def resize_pair(
    body: Image.Image,
    mask: Image.Image,
    target_height: int,
) -> tuple[Image.Image, Image.Image]:
    scale = target_height / body.height
    target_size = (
        max(1, round(body.width * scale)),
        max(1, target_height),
    )
    body = remaster_subject(body, target_size)
    mask = resize_premultiplied(mask, target_size)
    return body, mask


def source_frame(
    source_name: str,
    direction: int,
    animation: int,
    target_height: int,
) -> tuple[Image.Image, Image.Image]:
    source_kind, face = DIRECTION_SOURCES[direction]
    path = (
        SOURCE
        / source_kind
        / f"{source_name}_face{face}_{animation}.png"
    )
    body, mask = neutralize_palette(Image.open(path))
    body, mask = crop_pair(body, mask)
    body, mask = resize_pair(body, mask, target_height)

    return body, mask


def animation_offset(animation: int) -> tuple[int, int]:
    # PixVoxel's four movement files are identical. Preserve D2TM's four-row
    # animation contract with a small, deterministic marching bob.
    return (0, -1, 0, 1)[animation], (0, -2, 0, 1)[animation]


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


def single_frame(
    source_name: str,
    direction: int,
    animation: int,
    target_height: int,
) -> tuple[Image.Image, Image.Image]:
    body, mask = source_frame(
        source_name,
        direction,
        animation,
        target_height,
    )
    body_frame = Image.new("RGBA", (FRAME_SIZE, FRAME_SIZE))
    mask_frame = Image.new("RGBA", (FRAME_SIZE, FRAME_SIZE))
    offset_x, offset_y = animation_offset(animation)
    composite_at_anchor(body_frame, body, 64 + offset_x, 102 + offset_y)
    composite_at_anchor(mask_frame, mask, 64 + offset_x, 102 + offset_y)
    return body_frame, mask_frame


def group_frame(
    source_name: str,
    direction: int,
    animation: int,
    target_height: int,
) -> tuple[Image.Image, Image.Image]:
    forward_x, forward_y = DIRECTION_VECTORS[direction]
    perpendicular_x, perpendicular_y = -forward_y, forward_x
    placements = (
        (
            forward_x * 15,
            forward_y * 15,
            animation,
        ),
        (
            -forward_x * 8 + perpendicular_x * 18,
            -forward_y * 8 + perpendicular_y * 18,
            (animation + 1) % ATLAS_ROWS,
        ),
        (
            -forward_x * 8 - perpendicular_x * 18,
            -forward_y * 8 - perpendicular_y * 18,
            (animation + 3) % ATLAS_ROWS,
        ),
    )
    placements = tuple(sorted(placements, key=lambda item: item[1]))
    body_frame = Image.new("RGBA", (FRAME_SIZE, FRAME_SIZE))
    mask_frame = Image.new("RGBA", (FRAME_SIZE, FRAME_SIZE))
    for offset_x, offset_y, phase in placements:
        body, mask = source_frame(
            source_name,
            direction,
            phase,
            target_height,
        )
        animation_x, animation_y = animation_offset(phase)
        composite_at_anchor(
            body_frame,
            body,
            round(64 + offset_x + animation_x),
            round(102 + offset_y + animation_y),
        )
        composite_at_anchor(
            mask_frame,
            mask,
            round(64 + offset_x + animation_x),
            round(102 + offset_y + animation_y),
        )
    return body_frame, mask_frame


def build_role(recipe: dict[str, object]) -> tuple[Image.Image, Image.Image]:
    body_atlas = Image.new(
        "RGBA",
        (FRAME_SIZE * ATLAS_COLUMNS, FRAME_SIZE * ATLAS_ROWS),
    )
    mask_atlas = Image.new("RGBA", body_atlas.size)
    frame_builder = group_frame if recipe["group"] else single_frame
    for animation in range(ATLAS_ROWS):
        for direction in range(ATLAS_COLUMNS):
            body, mask = frame_builder(
                str(recipe["source_name"]),
                direction,
                animation,
                int(recipe["target_height"]),
            )
            position = (
                direction * FRAME_SIZE,
                animation * FRAME_SIZE,
            )
            body_atlas.alpha_composite(body, position)
            mask_atlas.alpha_composite(mask, position)

    resource_id = int(recipe["resource_id"])
    body_atlas.save(master_path(resource_id))
    mask_atlas.save(EXTRA / f"HOUSEMASK_{recipe['resource_name']}.png")
    return body_atlas, mask_atlas


def build_preview(atlases: list[tuple[dict[str, object], Image.Image]]) -> None:
    scale = 2
    cell_width = FRAME_SIZE * scale
    cell_height = FRAME_SIZE * scale
    label_height = 28
    preview = Image.new(
        "RGBA",
        (
            cell_width * ATLAS_COLUMNS,
            (cell_height + label_height) * len(atlases),
        ),
        (25, 27, 30, 255),
    )
    drawer = ImageDraw.Draw(preview)
    font = ImageFont.truetype(
        ROOT / "resources" / "bin" / "data" / "PTSansNarrow-Regular.ttf",
        20,
    )
    for row, (recipe, atlas) in enumerate(atlases):
        y = row * (cell_height + label_height)
        drawer.text(
            (8, y + 3),
            str(recipe["label"]),
            fill=(242, 211, 145, 255),
            font=font,
        )
        for direction in range(ATLAS_COLUMNS):
            frame = atlas.crop(
                (
                    direction * FRAME_SIZE,
                    0,
                    (direction + 1) * FRAME_SIZE,
                    FRAME_SIZE,
                )
            ).resize(
                (cell_width, cell_height),
                Image.Resampling.NEAREST,
            )
            preview.alpha_composite(
                frame,
                (direction * cell_width, y + label_height),
            )
    PREVIEW.mkdir(parents=True, exist_ok=True)
    preview.save(PREVIEW / "pixvoxel_infantry_roles.png")


def build_scale_preview(
    atlases: list[tuple[dict[str, object], Image.Image]],
) -> None:
    font = ImageFont.truetype(
        ROOT / "resources" / "bin" / "data" / "PTSansNarrow-Regular.ttf",
        20,
    )
    roles = {
        str(recipe["resource_name"]): atlas.crop((0, 0, 128, 128))
        for recipe, atlas in atlases
    }
    tank = Image.open(master_path(159)).convert("RGBA").crop((0, 0, 128, 128))
    tank_top = (
        Image.open(master_path(161))
        .convert("RGBA")
        .crop((0, 0, 128, 128))
    )
    tank.alpha_composite(tank_top)
    tank = tank.resize((143, 143), Image.Resampling.LANCZOS)

    entries = (
        ("Солдат", roles["UNIT_SOLDIER"]),
        ("Отряд автоматчиков", roles["UNIT_SOLDIERS"]),
        ("Гранатомётчик", roles["UNIT_TROOPER"]),
        ("Отряд гранатомётчиков", roles["UNIT_TROOPERS"]),
        ("Танк: размер Auto", tank),
    )
    cell_width = 180
    cell_height = 190
    preview = Image.new(
        "RGBA",
        (cell_width * len(entries), cell_height),
        (25, 27, 30, 255),
    )
    drawer = ImageDraw.Draw(preview)
    for column, (label, image) in enumerate(entries):
        cell_x = column * cell_width
        grid_x = cell_x + (cell_width - 128) // 2
        drawer.rectangle(
            (grid_x, 34, grid_x + 127, 161),
            outline=(78, 72, 61, 255),
            width=1,
        )
        preview.alpha_composite(
            image,
            (
                cell_x + (cell_width - image.width) // 2,
                34 + (128 - image.height) // 2,
            ),
        )
        drawer.text(
            (cell_x + 6, 165),
            label,
            fill=(242, 211, 145, 255),
            font=font,
        )
    PREVIEW.mkdir(parents=True, exist_ok=True)
    preview.save(PREVIEW / "infantry_vehicle_scale.png")


def write_manifest() -> None:
    manifest = {
        "source": "PixVoxel Colorful Isometric Wargame Sprites",
        "author": "Tommy Ettinger (TEttinger)",
        "url": (
            "https://opengameart.org/content/"
            "pixvoxel-colorful-isometric-wargame-sprites"
        ),
        "license": "CC0 1.0 / public domain dedication",
        "used_units": {
            "Infantry_Large": "rifle soldier",
            "Infantry_P_Large": "bazooka / grenade launcher soldier",
        },
        "d2tm_direction_order": [
            "E",
            "NE",
            "N",
            "NW",
            "W",
            "SW",
            "S",
            "SE",
        ],
        "direction_sources": [
            {"projection": projection, "face": face}
            for projection, face in DIRECTION_SOURCES
        ],
        "roles": [
            {
                "resource_id": recipe["resource_id"],
                "resource_name": recipe["resource_name"],
                "label": recipe["label"],
                "group": recipe["group"],
            }
            for recipe in ROLE_RECIPES
        ],
        "notes": [
            "Only the selected 64 source frames are retained.",
            "Colors, scale, formation, house mask and animation bob are D2TM edits.",
            "The original four movement files are identical, so D2TM's four rows use a deterministic bob.",
        ],
    }
    (SOURCE / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def build_all() -> None:
    MASTER.mkdir(parents=True, exist_ok=True)
    EXTRA.mkdir(parents=True, exist_ok=True)
    atlases: list[tuple[dict[str, object], Image.Image]] = []
    for recipe in ROLE_RECIPES:
        atlas, _mask = build_role(recipe)
        atlases.append((recipe, atlas))
    build_preview(atlases)
    build_scale_preview(atlases)
    write_manifest()
    print("PixVoxel infantry: 4 HD4 atlases, 4 house masks")


def main() -> None:
    build_all()


if __name__ == "__main__":
    main()
