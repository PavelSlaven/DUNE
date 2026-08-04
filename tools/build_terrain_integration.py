#!/usr/bin/env python3
"""Build validated HD2/HD4 packs with the approved terrain resources."""

from __future__ import annotations

import hashlib
import json
import shutil
import sys
from pathlib import Path

from PIL import Image, ImageChops

from hd_assets import PackEntry, decode_image, encode_png, read_pack, write_pack


ROOT = Path(__file__).resolve().parents[1]
GAME = Path("C:/Users/Slaven/Desktop/D2TM-v0.8.0.windows.ru")
REVIEW = ROOT / "artifacts" / "terrain_review_v1"
CLASSIC_PACK = ROOT / "resources" / "bin" / "data" / "sdl_data.dat"
MASTER_DIR = ROOT / "resources" / "hd" / "master4" / "sdl_data"
EXTRA_DIR = (
    ROOT / "resources" / "hd" / "master4_extra_packs" / "sdl_data"
)
OUTPUT = ROOT / "artifacts" / "terrain_integration_v1"
OUTPUT_DATA = OUTPUT / "data"

RESOURCE_IDS = tuple(range(117, 126))
VARIANT_PREFIXES = (
    "TERRAIN_HILL_VAR_",
    "TERRAIN_MOUNTAIN_VAR_",
    "TERRAIN_ROCK_VAR_",
    "TERRAIN_SAND_VAR_",
    "TERRAIN_SPICE_VAR_",
    "TERRAIN_SPICEHILL_VAR_",
)
VARIANT_RESOURCE_IDS = {
    "TERRAIN_HILL_VAR_": 118,
    "TERRAIN_MOUNTAIN_VAR_": 119,
    "TERRAIN_ROCK_VAR_": 120,
    "TERRAIN_SAND_VAR_": 121,
    "TERRAIN_SPICE_VAR_": 123,
    "TERRAIN_SPICEHILL_VAR_": 124,
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def image_difference(left: Image.Image, right: Image.Image) -> bool:
    return bool(
        ImageChops.difference(
            left.convert("RGBA"),
            right.convert("RGBA"),
        ).getbbox()
    )


def replacement(entry: PackEntry, image: Image.Image) -> PackEntry:
    return PackEntry(
        index=entry.index,
        name=entry.name,
        extension="PNG",
        payload=encode_png(image),
    )


def load_terrain(
    density: int,
) -> tuple[dict[int, Image.Image], dict[str, Image.Image]]:
    classic = read_pack(CLASSIC_PACK)
    masters: dict[int, Image.Image] = {}
    source_folder = REVIEW / f"masters_hd{density}" / "sdl_data"
    for resource_id in RESOURCE_IDS:
        classic_entry = classic[resource_id]
        classic_image = decode_image(classic_entry.payload)
        if classic_image is None:
            raise AssertionError(
                f"classic resource {resource_id}:{classic_entry.name} "
                "is not an image"
            )
        source = (
            source_folder
            / f"{resource_id:04d}_{classic_entry.name}.png"
        )
        if not source.is_file():
            raise FileNotFoundError(source)
        image = Image.open(source).convert("RGBA")
        expected = (
            classic_image.width * density,
            classic_image.height * density,
        )
        if image.size != expected:
            raise AssertionError(
                f"{source.name}: size {image.size}, expected {expected}"
            )
        masters[resource_id] = image

    variants: dict[str, Image.Image] = {}
    variant_folder = REVIEW / f"extras_hd{density}" / "sdl_data"
    for prefix in VARIANT_PREFIXES:
        for number in range(1, 5):
            name = f"{prefix}{number:02d}"
            source = variant_folder / f"{name}.png"
            if not source.is_file():
                raise FileNotFoundError(source)
            image = Image.open(source).convert("RGBA")
            expected = masters[VARIANT_RESOURCE_IDS[prefix]].size
            if image.size != expected:
                raise AssertionError(
                    f"{source.name}: size {image.size}, expected {expected}"
                )
            variants[name] = image
    return masters, variants


def verify_density_pair(
    hd2: dict[int, Image.Image],
    hd4: dict[int, Image.Image],
    variants2: dict[str, Image.Image],
    variants4: dict[str, Image.Image],
) -> None:
    for resource_id in RESOURCE_IDS:
        expected = hd4[resource_id].resize(
            hd2[resource_id].size,
            Image.Resampling.LANCZOS,
        )
        if image_difference(hd2[resource_id], expected):
            raise AssertionError(
                f"resource {resource_id}: HD2 is not the HD4 derivative"
            )
    if variants2.keys() != variants4.keys():
        raise AssertionError("HD2 and HD4 terrain variant names differ")
    for name in variants4:
        expected = variants4[name].resize(
            variants2[name].size,
            Image.Resampling.LANCZOS,
        )
        if image_difference(variants2[name], expected):
            raise AssertionError(
                f"{name}: HD2 is not the HD4 derivative"
            )


def patch_pack(
    base: Path,
    output: Path,
    masters: dict[int, Image.Image],
    variants: dict[str, Image.Image],
    density: int,
) -> dict[str, object]:
    before = read_pack(base)
    entries = list(before)
    classic = read_pack(CLASSIC_PACK)

    for resource_id in RESOURCE_IDS:
        if entries[resource_id].name != classic[resource_id].name:
            raise AssertionError(
                f"HD{density} ID {resource_id} is "
                f"{entries[resource_id].name}, expected "
                f"{classic[resource_id].name}"
            )
        entries[resource_id] = replacement(
            entries[resource_id],
            masters[resource_id],
        )

    by_name = {entry.name: entry.index for entry in entries}
    appended: list[str] = []
    replaced_variants: list[str] = []
    for name, image in variants.items():
        if name in by_name:
            index = by_name[name]
            entries[index] = replacement(entries[index], image)
            replaced_variants.append(name)
        else:
            index = len(entries)
            entries.append(
                PackEntry(
                    index=index,
                    name=name,
                    extension="PNG",
                    payload=encode_png(image),
                )
            )
            by_name[name] = index
            appended.append(name)

    write_pack(output, entries)
    packed = read_pack(output)
    if len(packed) != len(before) + len(appended):
        raise AssertionError("unexpected HD pack entry count")

    target_names = set(variants)
    for old, new in zip(before, packed[: len(before)], strict=True):
        if old.index in RESOURCE_IDS or old.name in target_names:
            continue
        if (
            old.index != new.index
            or old.name != new.name
            or old.extension != new.extension
            or old.payload != new.payload
        ):
            raise AssertionError(
                f"unrelated resource changed: {old.index}:{old.name}"
            )

    for resource_id, expected in masters.items():
        actual = decode_image(packed[resource_id].payload)
        if actual is None or image_difference(actual, expected):
            raise AssertionError(
                f"packed HD{density} terrain ID {resource_id} differs"
            )
    packed_by_name = {entry.name: entry for entry in packed}
    for name, expected in variants.items():
        actual = decode_image(packed_by_name[name].payload)
        if actual is None or image_difference(actual, expected):
            raise AssertionError(
                f"packed HD{density} terrain variant {name} differs"
            )

    return {
        "density": density,
        "base": str(base),
        "base_sha256": sha256(base),
        "output": str(output),
        "output_sha256": sha256(output),
        "entries_before": len(before),
        "entries_after": len(packed),
        "replaced_ids": list(RESOURCE_IDS),
        "replaced_variants": replaced_variants,
        "appended_variants": appended,
    }


def install_masters(
    hd4: dict[int, Image.Image],
    variants4: dict[str, Image.Image],
) -> None:
    classic = read_pack(CLASSIC_PACK)
    MASTER_DIR.mkdir(parents=True, exist_ok=True)
    EXTRA_DIR.mkdir(parents=True, exist_ok=True)
    for resource_id, image in hd4.items():
        image.save(
            MASTER_DIR
            / f"{resource_id:04d}_{classic[resource_id].name}.png",
            optimize=True,
        )
    for name, image in variants4.items():
        image.save(EXTRA_DIR / f"{name}.png", optimize=True)


def main() -> int:
    hd2, variants2 = load_terrain(2)
    hd4, variants4 = load_terrain(4)
    verify_density_pair(hd2, hd4, variants2, variants4)

    OUTPUT_DATA.mkdir(parents=True, exist_ok=True)
    backup = OUTPUT / "backup_before_install"
    backup.mkdir(parents=True, exist_ok=True)
    for density in (2, 4):
        source = GAME / "data" / f"sdl_data_hd{density}.dat"
        if not source.is_file():
            raise FileNotFoundError(source)
        shutil.copy2(source, backup / source.name)

    builds = [
        patch_pack(
            GAME / "data" / "sdl_data_hd2.dat",
            OUTPUT_DATA / "sdl_data_hd2.dat",
            hd2,
            variants2,
            2,
        ),
        patch_pack(
            GAME / "data" / "sdl_data_hd4.dat",
            OUTPUT_DATA / "sdl_data_hd4.dat",
            hd4,
            variants4,
            4,
        ),
    ]
    install_masters(hd4, variants4)

    manifest = {
        "format": 1,
        "status": "built_not_installed",
        "resource_ids": list(RESOURCE_IDS),
        "resource_count": len(RESOURCE_IDS),
        "variant_count": len(variants4),
        "classic_frame_counts": {
            "117": 1,
            "118": 16,
            "119": 17,
            "120": 16,
            "121": 1,
            "122": 5,
            "123": 16,
            "124": 16,
            "125": 16,
        },
        "builds": builds,
        "backup": str(backup),
    }
    (OUTPUT / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(manifest, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, AssertionError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(1)
