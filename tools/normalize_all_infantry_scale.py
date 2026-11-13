#!/usr/bin/env python3
"""Normalize every HD infantry sprite to its classic apparent size."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
from pathlib import Path

import numpy as np
from PIL import Image

from check_all_infantry_original_scale import (
    CLASSIC,
    GROUPS,
    GROUP_SINGLE,
    INFANTRY,
    individual_heights,
    visible_areas,
)
from hd_assets import PackEntry, decode_image, encode_png, read_pack, write_pack
from prepare_pistol_soldier_reference import premultiplied_resize


ROOT = Path(__file__).resolve().parents[1]
GAME = Path("C:/Users/Slaven/Desktop/D2TM-v0.8.0.windows.ru")
STAGED = ROOT / "artifacts" / "pistol_soldier_integration_v1" / "data"
OUT = ROOT / "artifacts" / "infantry_scale_normalization_v1"
MASTER = ROOT / "resources" / "hd" / "master4" / "sdl_data"
EXTRA = ROOT / "resources" / "hd" / "master4_extra_packs" / "sdl_data"
ROWS = 4
COLUMNS = 8
FRAME4 = 128
TOLERANCE = 0.6


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def median_individual_height(
    resource_id: int,
    atlas: Image.Image,
    entries: list[PackEntry],
    density: int,
) -> float:
    heights = individual_heights(atlas, density, resource_id in GROUPS)
    if heights:
        return float(np.median(heights))
    single_id = GROUP_SINGLE[resource_id]
    single = decode_image(entries[single_id].payload)
    if single is None:
        raise AssertionError(f"cannot decode {INFANTRY[single_id]}")
    single_median = float(
        np.median(individual_heights(single, density, False))
    )
    per_member_area_ratio = float(
        np.median(visible_areas(atlas) / (3.0 * visible_areas(single)))
    )
    return single_median * np.sqrt(per_member_area_ratio)


def scale_frame_pair(
    unit: Image.Image,
    mask: Image.Image,
    scale: float,
) -> tuple[Image.Image, Image.Image]:
    alpha = np.asarray(unit.getchannel("A"), dtype=np.uint8)
    coordinates = np.argwhere(alpha > 0)
    if not len(coordinates):
        raise AssertionError("empty infantry frame")
    top, left = coordinates.min(axis=0)
    bottom, right = coordinates.max(axis=0) + 1
    box = (int(left), int(top), int(right), int(bottom))
    unit_crop = unit.crop(box)
    mask_crop = mask.crop(box)
    new_width = max(1, round(unit_crop.width * scale))
    new_height = max(1, round(unit_crop.height * scale))
    resized_unit = premultiplied_resize(unit_crop, (new_width, new_height))
    resized_mask = premultiplied_resize(mask_crop, (new_width, new_height))

    anchor_x = unit.width / 2.0
    destination_x = round(anchor_x + (left - anchor_x) * scale)
    destination_y = int(bottom) - new_height
    if (
        destination_x < 0
        or destination_y < 0
        or destination_x + new_width > unit.width
        or destination_y + new_height > unit.height
    ):
        raise AssertionError(
            f"scaled infantry frame would clip at {(destination_x, destination_y)}"
        )

    output_unit = Image.new("RGBA", unit.size)
    output_mask = Image.new("RGBA", mask.size)
    output_unit.alpha_composite(resized_unit, (destination_x, destination_y))
    output_mask.alpha_composite(resized_mask, (destination_x, destination_y))
    return output_unit, clamp_mask(output_mask, output_unit)


def scale_atlas_pair(
    unit: Image.Image,
    mask: Image.Image,
    scale: float,
) -> tuple[Image.Image, Image.Image]:
    frame_width = unit.width // COLUMNS
    frame_height = unit.height // ROWS
    if (frame_width, frame_height) != (FRAME4, FRAME4):
        raise AssertionError(f"invalid HD4 infantry frame {frame_width}x{frame_height}")
    output_unit = Image.new("RGBA", unit.size)
    output_mask = Image.new("RGBA", mask.size)
    for row in range(ROWS):
        for column in range(COLUMNS):
            box = (
                column * frame_width,
                row * frame_height,
                (column + 1) * frame_width,
                (row + 1) * frame_height,
            )
            frame_unit, frame_mask = scale_frame_pair(
                unit.crop(box), mask.crop(box), scale
            )
            output_unit.alpha_composite(
                frame_unit, (column * frame_width, row * frame_height)
            )
            output_mask.alpha_composite(
                frame_mask, (column * frame_width, row * frame_height)
            )
    return output_unit, clamp_mask(output_mask, output_unit)


def clamp_mask(mask: Image.Image, unit: Image.Image) -> Image.Image:
    rgba = np.asarray(mask.convert("RGBA"), dtype=np.uint8).copy()
    unit_alpha = np.asarray(unit.getchannel("A"), dtype=np.uint8)
    rgba[:, :, 3] = np.minimum(rgba[:, :, 3], unit_alpha)
    rgba[rgba[:, :, 3] == 0, :3] = 0
    return Image.fromarray(rgba, "RGBA")


def resize_atlas_pair(
    unit: Image.Image, mask: Image.Image, density: int
) -> tuple[Image.Image, Image.Image]:
    target_frame = 32 * density
    output_unit = Image.new("RGBA", (target_frame * COLUMNS, target_frame * ROWS))
    output_mask = Image.new("RGBA", output_unit.size)
    for row in range(ROWS):
        for column in range(COLUMNS):
            box = (
                column * FRAME4,
                row * FRAME4,
                (column + 1) * FRAME4,
                (row + 1) * FRAME4,
            )
            destination = (column * target_frame, row * target_frame)
            output_unit.alpha_composite(
                unit.crop(box).resize(
                    (target_frame, target_frame), Image.Resampling.LANCZOS
                ),
                destination,
            )
            output_mask.alpha_composite(
                mask.crop(box).resize(
                    (target_frame, target_frame), Image.Resampling.LANCZOS
                ),
                destination,
            )
    return output_unit, clamp_mask(output_mask, output_unit)


def mask_ids(entries: list[PackEntry]) -> dict[int, int]:
    result: dict[int, int] = {}
    for resource_id, name in INFANTRY.items():
        mask_name = f"HM_{name}"
        matches = [entry.index for entry in entries if entry.name == mask_name]
        if len(matches) != 1:
            raise AssertionError(f"expected one {mask_name}, got {len(matches)}")
        result[resource_id] = matches[0]
    return result


def build_assets(
    entries: list[PackEntry], masks: dict[int, int]
) -> tuple[dict[int, tuple[Image.Image, Image.Image]], list[dict[str, object]]]:
    assets: dict[int, tuple[Image.Image, Image.Image]] = {}
    metrics: list[dict[str, object]] = []
    for resource_id, name in INFANTRY.items():
        unit = decode_image(entries[resource_id].payload)
        mask = decode_image(entries[masks[resource_id]].payload)
        if unit is None or mask is None:
            raise AssertionError(f"cannot decode {name} or its mask")
        classic = Image.open(CLASSIC / f"{resource_id:04d}_{name}.png").convert(
            "RGBA"
        )
        target = float(
            np.median(individual_heights(classic, 1, resource_id in GROUPS))
        )
        before = median_individual_height(resource_id, unit, entries, 4)
        scale = target / before
        if abs(before - target) <= TOLERANCE:
            scale = 1.0
        if scale != 1.0:
            unit, mask = scale_atlas_pair(unit, mask, scale)
        assets[resource_id] = (unit, clamp_mask(mask, unit))
        after = median_individual_height_from_assets(
            resource_id, assets, entries, target
        )
        metrics.append(
            {
                "id": resource_id,
                "name": name,
                "classic": target,
                "before": before,
                "scale": scale,
                "after": after,
            }
        )
    return assets, metrics


def median_individual_height_from_assets(
    resource_id: int,
    assets: dict[int, tuple[Image.Image, Image.Image]],
    entries: list[PackEntry],
    fallback: float,
) -> float:
    unit = assets[resource_id][0]
    heights = individual_heights(unit, 4, resource_id in GROUPS)
    if heights:
        return float(np.median(heights))
    single_id = GROUP_SINGLE.get(resource_id)
    if single_id is None or single_id not in assets:
        return fallback
    single = assets[single_id][0]
    return float(np.median(individual_heights(single, 4, False))) * np.sqrt(
        float(np.median(visible_areas(unit) / (3.0 * visible_areas(single))))
    )


def patch_pack(
    source: Path,
    output: Path,
    assets: dict[int, tuple[Image.Image, Image.Image]],
    masks: dict[int, int],
    density: int,
) -> dict[str, object]:
    entries = read_pack(source)
    patched = list(entries)
    changed = set(INFANTRY) | set(masks.values())
    for resource_id, name in INFANTRY.items():
        unit, mask = assets[resource_id]
        if density != 4:
            unit, mask = resize_atlas_pair(unit, mask, density)
        patched[resource_id] = PackEntry(
            resource_id, name, "PNG", encode_png(unit)
        )
        mask_id = masks[resource_id]
        patched[mask_id] = PackEntry(
            mask_id, f"HM_{name}", "PNG", encode_png(mask)
        )
    output.parent.mkdir(parents=True, exist_ok=True)
    write_pack(output, patched)
    packed = read_pack(output)
    for before, after in zip(entries, packed, strict=True):
        if before.index not in changed and (
            before.name != after.name
            or before.extension != after.extension
            or before.payload != after.payload
        ):
            raise AssertionError(f"unrelated entry changed: {before.index}:{before.name}")
    return {
        "path": str(output),
        "density": density,
        "changed_ids": sorted(changed),
        "sha256": sha256(output),
    }


def install(source: Path, target: Path, backup: Path) -> None:
    backup.parent.mkdir(parents=True, exist_ok=True)
    if not backup.exists():
        shutil.copy2(target, backup)
    temporary = target.with_name(target.name + ".infantry-scale.tmp")
    try:
        shutil.copy2(source, temporary)
        if sha256(source) != sha256(temporary):
            raise AssertionError("temporary pack differs from build")
        os.replace(temporary, target)
    finally:
        if temporary.exists():
            temporary.unlink()
    if sha256(source) != sha256(target):
        raise AssertionError("installed pack differs from build")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--install", action="store_true")
    args = parser.parse_args()

    staged4 = STAGED / "sdl_data_hd4.dat"
    entries4 = read_pack(staged4)
    masks = mask_ids(entries4)
    assets, metrics = build_assets(entries4, masks)

    MASTER.mkdir(parents=True, exist_ok=True)
    EXTRA.mkdir(parents=True, exist_ok=True)
    for resource_id, name in INFANTRY.items():
        unit, mask = assets[resource_id]
        unit.save(MASTER / f"{resource_id:04d}_{name}.png", optimize=True)
        mask.save(EXTRA / f"HM_{name}.png", optimize=True)

    data = OUT / "data"
    builds = [
        patch_pack(
            GAME / "data" / "sdl_data_hd2.dat",
            data / "sdl_data_hd2.dat",
            assets,
            masks,
            2,
        ),
        patch_pack(staged4, data / "sdl_data_hd4.dat", assets, masks, 4),
    ]

    status = "built_not_installed"
    if args.install:
        for density in (2, 4):
            filename = f"sdl_data_hd{density}.dat"
            install(
                data / filename,
                GAME / "data" / filename,
                OUT / "backup" / filename,
            )
        status = "installed"

    report = {
        "format": 1,
        "status": status,
        "metrics": metrics,
        "builds": builds,
        "installed_sha256": (
            {
                f"hd{density}": sha256(
                    GAME / "data" / f"sdl_data_hd{density}.dat"
                )
                for density in (2, 4)
            }
            if args.install
            else {}
        ),
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "manifest.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
