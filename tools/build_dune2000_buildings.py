#!/usr/bin/env python3
"""Import the matching Dune 2000 buildings into D2TM HD4 atlases.

The source sheets remain the artwork. Processing is limited to selecting the
healthy sprites for each House, removing keyed backgrounds, fitting them into
the existing D2TM logical footprint, repeating static frames where D2TM expects
an animation, generating House-colour masks, and deterministic shadows.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageFilter, ImageOps

from build_dune2000_units import (
    place_subject_hd4,
    save_hd4,
    save_master4,
)


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "resources" / "hd" / "source_references" / "ru4"
CLASSIC = ROOT / "resources" / "hd" / "classic" / "sdl_data"
MASTER = ROOT / "resources" / "hd" / "master4" / "sdl_data"
EXTRA = ROOT / "resources" / "hd" / "master4_extra_packs" / "sdl_data"

HOUSES = ("ATREIDES", "HARKONNEN", "ORDOS")
HOUSE_CODES = {
    "ATREIDES": "A",
    "HARKONNEN": "H",
    "ORDOS": "O",
}


@dataclass(frozen=True)
class BuildingSpec:
    source_name: str
    resource_id: int
    shadow_id: int
    resource_name: str
    frame_size: tuple[int, int]
    frame_count: int
    crops: dict[str, tuple[int, int, int, int]]
    content_size: tuple[int, int] | None = None


BUILDINGS = (
    BuildingSpec(
        "barracks",
        1,
        2,
        "BUILD_BARRACKS",
        (64, 64),
        1,
        {
            "ATREIDES": (0, 0, 73, 77),
            "HARKONNEN": (1, 78, 63, 153),
            "ORDOS": (1, 154, 64, 227),
        },
    ),
    BuildingSpec(
        "construction_yard",
        3,
        4,
        "BUILD_CONSTYARD",
        (64, 64),
        1,
        {
            "ATREIDES": (3, 2, 97, 86),
            "HARKONNEN": (2, 153, 97, 245),
            "ORDOS": (2, 313, 96, 399),
        },
    ),
    BuildingSpec(
        "heavy_factory",
        5,
        7,
        "BUILD_HEAVYFACTORY",
        (96, 64),
        11,
        {
            "ATREIDES": (94, 1, 187, 87),
            "HARKONNEN": (99, 89, 193, 170),
            "ORDOS": (100, 180, 190, 256),
        },
    ),
    BuildingSpec(
        "high_tech_factory",
        8,
        9,
        "BUILD_HIGHTECH",
        (96, 64),
        7,
        {
            "ATREIDES": (4, 1, 94, 103),
            "HARKONNEN": (4, 104, 94, 200),
            "ORDOS": (3, 201, 97, 294),
        },
    ),
    BuildingSpec(
        "light_factory",
        12,
        14,
        "BUILD_LIGHTFACTORY",
        (64, 64),
        1,
        {
            "ATREIDES": (102, 1, 185, 65),
            "HARKONNEN": (103, 66, 193, 125),
            "ORDOS": (104, 127, 191, 190),
        },
    ),
    BuildingSpec(
        "palace",
        15,
        16,
        "BUILD_PALACE",
        (96, 96),
        1,
        {
            "ATREIDES": (0, 0, 97, 109),
            "HARKONNEN": (0, 109, 97, 219),
            "ORDOS": (0, 219, 97, 334),
        },
    ),
    BuildingSpec(
        "outpost",
        26,
        27,
        "BUILD_RADAR",
        (64, 64),
        8,
        {
            "ATREIDES": (1, 1, 95, 75),
            "HARKONNEN": (1, 134, 97, 213),
            "ORDOS": (1, 304, 97, 383),
        },
    ),
    BuildingSpec(
        "refinery",
        28,
        29,
        "BUILD_REFINERY",
        (96, 64),
        8,
        {
            "ATREIDES": (109, 2, 217, 69),
            "HARKONNEN": (113, 70, 227, 145),
            "ORDOS": (107, 146, 215, 235),
        },
    ),
    BuildingSpec(
        "spice_silo",
        34,
        35,
        "BUILD_SILO",
        (64, 64),
        1,
        {
            "ATREIDES": (1, 1, 33, 30),
            "HARKONNEN": (1, 31, 33, 60),
            "ORDOS": (1, 61, 33, 90),
        },
        # Dune 2000 stores the silo as a compact one-cell object. Keep that
        # relative scale instead of stretching it across D2TM's 2x2 footprint.
        (40, 40),
    ),
    BuildingSpec(
        "starport",
        36,
        37,
        "BUILD_STARPORT",
        (96, 96),
        8,
        {
            "ATREIDES": (2, 61, 98, 148),
            "HARKONNEN": (3, 150, 98, 236),
            "ORDOS": (2, 238, 98, 327),
        },
    ),
    BuildingSpec(
        "windtrap",
        40,
        41,
        "BUILD_WINDTRAP",
        (64, 64),
        1,
        {
            "ATREIDES": (2, 2, 62, 78),
            "HARKONNEN": (4, 134, 65, 206),
            "ORDOS": (4, 272, 65, 345),
        },
    ),
)


def classic(index: int) -> Path:
    return next(CLASSIC.glob(f"{index:04d}_*.png"))


def master(index: int) -> Path:
    return MASTER / classic(index).name


def clean_crop(
    source_image: Image.Image,
    box: tuple[int, int, int, int],
) -> Image.Image:
    image = source_image.convert("RGBA").crop(box)
    pixels = []
    for r, g, b, a in image.getdata():
        keyed_magenta = r >= 245 and b >= 245 and g <= 16
        pixels.append((0, 0, 0, 0) if keyed_magenta else (r, g, b, a))
    image.putdata(pixels)
    bounds = image.getchannel("A").getbbox()
    if not bounds:
        raise ValueError(f"empty Dune 2000 building crop: {box}")
    return image.crop(bounds)


def build_atlas(
    subject: Image.Image,
    frame_size: tuple[int, int],
    frame_count: int,
    content_size: tuple[int, int] | None,
) -> Image.Image:
    frame = place_subject_hd4(subject, frame_size, content_size)
    frame_width = frame_size[0] * 4
    frame_height = frame_size[1] * 4
    atlas = Image.new(
        "RGBA",
        (frame_width, frame_height * frame_count),
    )
    for row in range(frame_count):
        atlas.alpha_composite(frame, (0, row * frame_height))
    return atlas


def neutralize_building(image: Image.Image) -> Image.Image:
    """Keep relief and lights while replacing House paint with neutral metal."""
    rgba = image.convert("RGBA")
    grayscale = ImageOps.grayscale(rgba)
    neutral = ImageOps.colorize(
        grayscale,
        black=(31, 30, 28),
        mid=(111, 105, 92),
        white=(211, 198, 169),
    ).convert("RGBA")
    neutral.putalpha(rgba.getchannel("A"))

    result = []
    for original, replacement in zip(rgba.getdata(), neutral.getdata()):
        red, green, blue, alpha = original
        neutral_red, neutral_green, neutral_blue, _ = replacement
        saturation = max(red, green, blue) - min(red, green, blue)
        emissive = max(red, green, blue) >= 185 and saturation >= 55
        original_share = 0.42 if emissive else 0.08
        result.append(
            (
                round(neutral_red * (1.0 - original_share) + red * original_share),
                round(neutral_green * (1.0 - original_share) + green * original_share),
                round(neutral_blue * (1.0 - original_share) + blue * original_share),
                alpha,
            )
        )
    neutral.putdata(result)
    return neutral


def build_shadow(
    atlas: Image.Image,
    frame_size: tuple[int, int],
    frame_count: int,
) -> Image.Image:
    result = Image.new("RGBA", atlas.size)
    frame_width = frame_size[0] * 4
    frame_height = frame_size[1] * 4
    for row in range(frame_count):
        alpha = atlas.crop(
            (
                0,
                row * frame_height,
                frame_width,
                (row + 1) * frame_height,
            )
        ).getchannel("A")
        alpha = alpha.filter(ImageFilter.GaussianBlur(2.2))
        alpha = alpha.point(lambda value: round(value * 0.20))
        silhouette = Image.new(
            "RGBA",
            (frame_width, frame_height),
            (7, 5, 3, 0),
        )
        silhouette.putalpha(alpha)
        shadow_frame = Image.new("RGBA", (frame_width, frame_height))
        shadow_frame.alpha_composite(silhouette, (8, 8))
        result.alpha_composite(
            shadow_frame,
            (0, row * frame_height),
        )
    return result


def save_variant_masks(
    variants: dict[str, Image.Image],
    resource_name: str,
) -> None:
    base = variants["ATREIDES"]
    transparent_mask = Image.new("RGBA", base.size)
    save_master4(
        transparent_mask,
        EXTRA / f"HOUSEMASK_{resource_name}.png",
    )
    for house, atlas in variants.items():
        variant_name = f"HV_{HOUSE_CODES[house]}_{resource_name}"
        save_master4(atlas, EXTRA / f"{variant_name}.png")
        save_master4(
            transparent_mask,
            EXTRA / f"HM_{variant_name}.png",
        )


def build_structure(spec: BuildingSpec) -> None:
    sheet = Image.open(
        SOURCE / f"dune2000_{spec.source_name}.png"
    ).convert("RGBA")
    variants = {
        house: neutralize_building(
            build_atlas(
                clean_crop(sheet, spec.crops[house]),
                spec.frame_size,
                spec.frame_count,
                spec.content_size,
            )
        )
        for house in HOUSES
    }
    base = variants["ATREIDES"]
    save_master4(base, master(spec.resource_id))
    save_master4(
        build_shadow(base, spec.frame_size, spec.frame_count),
        master(spec.shadow_id),
    )
    save_variant_masks(variants, spec.resource_name)


def build_wor() -> None:
    """Use the Harkonnen Dune 2000 barracks for D2TM's WOR."""
    sheet = Image.open(SOURCE / "dune2000_barracks.png").convert("RGBA")
    subject = clean_crop(sheet, (1, 78, 63, 153))
    atlas = neutralize_building(build_atlas(subject, (64, 64), 1, None))
    save_master4(atlas, master(42))
    save_master4(build_shadow(atlas, (64, 64), 1), master(43))
    save_master4(
        Image.new("RGBA", atlas.size),
        EXTRA / "HOUSEMASK_BUILD_WOR.png",
    )


def neutralize_fallback_buildings() -> None:
    # Dune 2000 has no matching IX, repair facility or turret sheets.
    # Build deterministic neutral HD4 reserves from their classic atlases.
    for resource_id in (10, 30, 32, 38):
        save_hd4(
            neutralize_building(Image.open(classic(resource_id))),
            master(resource_id),
        )


def clear_obsolete_factory_flashes() -> None:
    # The Dune 2000 sheets do not contain the separate D2TM flash layer.
    # Transparent replacements prevent the old flash geometry from appearing
    # over the newly imported buildings.
    for resource_id in (6, 13):
        size = Image.open(classic(resource_id)).size
        save_hd4(Image.new("RGBA", size), master(resource_id))


def build_all() -> None:
    MASTER.mkdir(parents=True, exist_ok=True)
    EXTRA.mkdir(parents=True, exist_ok=True)
    for spec in BUILDINGS:
        build_structure(spec)
    build_wor()
    neutralize_fallback_buildings()
    clear_obsolete_factory_flashes()
    print(
        "Dune 2000 buildings imported: 11 sheets, "
        "3 House variants, D2TM WOR mapped to Harkonnen Barracks"
    )
    print(
        "Current HD fallback retained: IX, Repair Facility, "
        "Gun Turret and Rocket Turret (no Dune 2000 sheet)"
    )


def main() -> None:
    build_all()


if __name__ == "__main__":
    main()
