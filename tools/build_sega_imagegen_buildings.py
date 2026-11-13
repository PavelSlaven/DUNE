#!/usr/bin/env python3
"""Build neutral HD4 D2TM structures from the preview3 ImageGen masters.

The ImageGen masters preserve the D2TM footprint and use the modular material
language of the Battle for Arrakis building sheet.  This script performs only
deterministic production work: alpha cleanup, bottom-anchored fitting, atlas
assembly, directional turret rotation, shadow creation and neutral House
variants.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageFilter, ImageOps

from build_dune2000_units import remaster_subject, resize_premultiplied


ROOT = Path(__file__).resolve().parents[1]
SOURCE = (
    ROOT
    / "resources"
    / "hd"
    / "source_references"
    / "preview3"
    / "battle_for_arrakis_buildings_239094.png"
)
GENERATED = (
    ROOT
    / "resources"
    / "hd"
    / "generated"
    / "preview3"
    / "buildings"
    / "alpha"
)
CLASSIC = ROOT / "resources" / "hd" / "classic" / "sdl_data"
MASTER = ROOT / "resources" / "hd" / "master4" / "sdl_data"
EXTRA = ROOT / "resources" / "hd" / "master4_extra_packs" / "sdl_data"
PREVIEW = ROOT / "resources" / "hd" / "previews" / "ru4"

HOUSE_CODES = ("A", "H", "O")


@dataclass(frozen=True)
class BuildingSpec:
    generated_name: str
    resource_id: int
    shadow_id: int
    resource_name: str
    frame_size: tuple[int, int]
    frame_count: int
    directional: bool = False
    content_scale: float = 0.82


BUILDINGS = (
    BuildingSpec("barracks", 1, 2, "BUILD_BARRACKS", (64, 64), 1),
    BuildingSpec(
        "construction_yard",
        3,
        4,
        "BUILD_CONSTYARD",
        (64, 64),
        1,
    ),
    BuildingSpec(
        "heavy_factory",
        5,
        7,
        "BUILD_HEAVYFACTORY",
        (96, 64),
        11,
    ),
    BuildingSpec(
        "high_tech_factory",
        8,
        9,
        "BUILD_HIGHTECH",
        (96, 64),
        7,
    ),
    BuildingSpec("ix", 10, 11, "BUILD_IX", (64, 64), 1),
    BuildingSpec(
        "light_factory",
        12,
        14,
        "BUILD_LIGHTFACTORY",
        (64, 64),
        1,
    ),
    BuildingSpec("palace", 15, 16, "BUILD_PALACE", (96, 96), 1),
    BuildingSpec("outpost", 26, 27, "BUILD_RADAR", (64, 64), 8),
    BuildingSpec(
        "refinery-v2",
        28,
        29,
        "BUILD_REFINERY",
        (96, 64),
        8,
    ),
    BuildingSpec(
        "repair_facility",
        30,
        31,
        "BUILD_REPAIR",
        (96, 64),
        8,
    ),
    BuildingSpec(
        "rocket_turret",
        32,
        33,
        "BUILD_RTURRET",
        (32, 32),
        8,
        directional=True,
        content_scale=0.80,
    ),
    BuildingSpec(
        "spice_silo",
        34,
        35,
        "BUILD_SILO",
        (64, 64),
        1,
        content_scale=0.72,
    ),
    BuildingSpec("starport", 36, 37, "BUILD_STARPORT", (96, 96), 8),
    BuildingSpec(
        "gun_turret",
        38,
        39,
        "BUILD_TURRET",
        (32, 32),
        8,
        directional=True,
        content_scale=0.80,
    ),
    BuildingSpec("windtrap", 40, 41, "BUILD_WINDTRAP", (64, 64), 1),
    BuildingSpec("wor", 42, 43, "BUILD_WOR", (64, 64), 1),
)


def classic(resource_id: int) -> Path:
    return next(CLASSIC.glob(f"{resource_id:04d}_*.png"))


def master(resource_id: int) -> Path:
    return MASTER / classic(resource_id).name


def keep_largest_component(image: Image.Image) -> Image.Image:
    rgba = image.convert("RGBA")
    alpha = np.array(rgba.getchannel("A"))
    binary = (alpha > 16).astype(np.uint8)
    count, labels, stats, _centroids = cv2.connectedComponentsWithStats(
        binary,
        connectivity=8,
    )
    if count <= 1:
        raise ValueError("generated building has no opaque component")
    largest = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
    keep = labels == largest
    output = np.array(rgba)
    output[~keep, 3] = 0
    cleaned = Image.fromarray(output, "RGBA")
    bounds = cleaned.getchannel("A").getbbox()
    if not bounds:
        raise ValueError("generated building became empty")
    return cleaned.crop(bounds)


def fit_bottom_anchored(
    subject: Image.Image,
    frame_size: tuple[int, int],
    content_scale: float,
) -> Image.Image:
    frame_width = frame_size[0] * 4
    frame_height = frame_size[1] * 4
    maximum_width = max(1, round((frame_width - 8) * content_scale))
    maximum_height = max(1, round((frame_height - 8) * content_scale))
    scale = min(
        maximum_width / subject.width,
        maximum_height / subject.height,
    )
    resized = resize_premultiplied(
        subject,
        (
            max(1, round(subject.width * scale)),
            max(1, round(subject.height * scale)),
        ),
    )
    frame = Image.new("RGBA", (frame_width, frame_height))
    x = (frame_width - resized.width) // 2
    y = frame_height - resized.height - 8
    frame.alpha_composite(resized, (x, y))
    return frame


def build_atlas(spec: BuildingSpec) -> Image.Image:
    source = keep_largest_component(
        Image.open(GENERATED / f"{spec.generated_name}.png")
    )
    frame_width = spec.frame_size[0] * 4
    frame_height = spec.frame_size[1] * 4
    atlas = Image.new(
        "RGBA",
        (frame_width, frame_height * spec.frame_count),
    )
    for row in range(spec.frame_count):
        subject = source
        if spec.directional:
            subject = source.rotate(
                -45 * row,
                resample=Image.Resampling.BICUBIC,
                expand=True,
            )
            bounds = subject.getchannel("A").getbbox()
            if bounds:
                subject = subject.crop(bounds)
        frame = fit_bottom_anchored(
            subject,
            spec.frame_size,
            spec.content_scale,
        )
        atlas.alpha_composite(frame, (0, row * frame_height))
    return atlas


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
        alpha = alpha.filter(ImageFilter.GaussianBlur(2.0))
        alpha = alpha.point(lambda value: round(value * 0.22))
        silhouette = Image.new(
            "RGBA",
            (frame_width, frame_height),
            (5, 4, 3, 0),
        )
        silhouette.putalpha(alpha)
        frame = Image.new("RGBA", (frame_width, frame_height))
        frame.alpha_composite(silhouette, (7, 7))
        result.alpha_composite(frame, (0, row * frame_height))
    return result


def save_neutral_variants(
    atlas: Image.Image,
    resource_name: str,
) -> None:
    transparent = Image.new("RGBA", atlas.size)
    transparent.save(EXTRA / f"HOUSEMASK_{resource_name}.png")
    for house in HOUSE_CODES:
        variant_name = f"HV_{house}_{resource_name}"
        atlas.save(EXTRA / f"{variant_name}.png")
        transparent.save(EXTRA / f"HM_{variant_name}.png")


def remaster_auxiliary(resource_id: int) -> None:
    source = Image.open(classic(resource_id)).convert("RGBA")
    target_size = (source.width * 4, source.height * 4)
    result = remaster_subject(source, target_size)
    result.save(master(resource_id))


def build_construction_previews_and_flags() -> None:
    for resource_id in range(17, 26):
        remaster_auxiliary(resource_id)
    for resource_id in (44, 45):
        remaster_auxiliary(resource_id)


def build_factory_flashes() -> None:
    for resource_id in (6, 13):
        source = Image.open(classic(resource_id)).convert("RGBA")
        target_size = (source.width * 4, source.height * 4)
        flash = resize_premultiplied(source, target_size)
        flash.save(master(resource_id))


def build_preview(atlases: list[tuple[BuildingSpec, Image.Image]]) -> None:
    cell_width = 240
    cell_height = 205
    columns = 4
    rows = (len(atlases) + columns - 1) // columns
    preview = Image.new(
        "RGBA",
        (cell_width * columns, cell_height * rows),
        (23, 25, 28, 255),
    )
    for index, (_spec, atlas) in enumerate(atlases):
        frame_height = atlas.height // _spec.frame_count
        frame = atlas.crop((0, 0, atlas.width, frame_height))
        bounds = frame.getchannel("A").getbbox()
        if bounds:
            frame = frame.crop(bounds)
        scale = min(190 / frame.width, 170 / frame.height)
        frame = resize_premultiplied(
            frame,
            (
                max(1, round(frame.width * scale)),
                max(1, round(frame.height * scale)),
            ),
        )
        x = (index % columns) * cell_width
        y = (index // columns) * cell_height
        preview.alpha_composite(
            frame,
            (
                x + (cell_width - frame.width) // 2,
                y + 6 + (170 - frame.height),
            ),
        )
    PREVIEW.mkdir(parents=True, exist_ok=True)
    preview.save(PREVIEW / "sega_imagegen_buildings.png")


def write_manifest() -> None:
    prompt_profile = {
        "use_case": "precise-object-edit",
        "style": "semi-realistic 2D RTS remaster",
        "source_role": (
            "Battle for Arrakis sheet provides modular panels, graphite, "
            "aged brass, vents, grilles and industrial mechanisms"
        ),
        "invariants": [
            "D2TM logical frame size and frame count",
            "bottom anchor",
            "neutral body colour",
            "no text, flag, logo or watermark",
        ],
    }
    manifest = {
        "release": "v0.8.0-ru4-preview3",
        "source": SOURCE.name,
        "source_page": (
            "https://www.spriters-resource.com/sega_genesis/"
            "duneiithebattleforarrakis/asset/239094/"
        ),
        "source_sha256": (
            "3f73042e24d2211011e44da22aa6da1c0"
            "24b8ba29203208fbf03a70184dad7ba"
        ),
        "prompt_profile": prompt_profile,
        "buildings": [
            {
                "generated_name": spec.generated_name,
                "resource_id": spec.resource_id,
                "shadow_id": spec.shadow_id,
                "resource_name": spec.resource_name,
                "frame_size": list(spec.frame_size),
                "frame_count": spec.frame_count,
                "directional": spec.directional,
            }
            for spec in BUILDINGS
        ],
    }
    output = GENERATED.parent / "manifest.json"
    output.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def build_all() -> None:
    if not SOURCE.is_file():
        raise FileNotFoundError(SOURCE)
    MASTER.mkdir(parents=True, exist_ok=True)
    EXTRA.mkdir(parents=True, exist_ok=True)
    atlases: list[tuple[BuildingSpec, Image.Image]] = []
    for spec in BUILDINGS:
        atlas = build_atlas(spec)
        atlas.save(master(spec.resource_id))
        build_shadow(
            atlas,
            spec.frame_size,
            spec.frame_count,
        ).save(master(spec.shadow_id))
        save_neutral_variants(atlas, spec.resource_name)
        atlases.append((spec, atlas))
    build_factory_flashes()
    build_construction_previews_and_flags()
    build_preview(atlases)
    write_manifest()
    print("Sega/ImageGen buildings: 16 bases, shadows and neutral variants")


if __name__ == "__main__":
    build_all()
