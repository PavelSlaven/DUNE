#!/usr/bin/env python3
"""Build HD2/HD4 data packs containing the approved construction sites."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

from PIL import Image, ImageChops

from hd_assets import PackEntry, decode_image, encode_png, read_pack, write_pack


ROOT = Path(__file__).resolve().parents[1]
GAME = Path("C:/Users/Slaven/Desktop/D2TM-v0.8.0.windows.ru")
REVIEW = ROOT / "artifacts" / "prebuild_review_v1"
CLASSIC_PACK = ROOT / "resources" / "bin" / "data" / "sdl_data.dat"
MASTER_DIR = ROOT / "resources" / "hd" / "master4" / "sdl_data"
OUTPUT_DIR = ROOT / "artifacts" / "prebuild_integration_v1" / "data"

RESOURCES = {
    17: ("BUILD_PRE_1X1", (32, 32), "BUILD_PRE_1X1_HD4_PREVIEW.png"),
    18: (
        "BUILD_PRE_1X1_SHADOW",
        (32, 32),
        "BUILD_PRE_1X1_SHADOW_HD4_PREVIEW.png",
    ),
    19: ("BUILD_PRE_2X2", (64, 64), "BUILD_PRE_2X2_HD4_PREVIEW.png"),
    20: (
        "BUILD_PRE_2X2_SHADOW",
        (64, 64),
        "BUILD_PRE_2X2_SHADOW_HD4_PREVIEW.png",
    ),
    21: ("BUILD_PRE_3X2", (96, 64), "BUILD_PRE_3X2_HD4_PREVIEW.png"),
    22: (
        "BUILD_PRE_3X2_SHADOW",
        (96, 64),
        "BUILD_PRE_3X2_SHADOW_HD4_PREVIEW.png",
    ),
    23: ("BUILD_PRE_3X3", (96, 96), "BUILD_PRE_3X3_HD4_PREVIEW.png"),
    24: (
        "BUILD_PRE_3X3_SHADOW",
        (96, 96),
        "BUILD_PRE_3X3_SHADOW_HD4_PREVIEW.png",
    ),
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def replacement_entry(entry: PackEntry, image: Image.Image) -> PackEntry:
    return PackEntry(
        index=entry.index,
        name=entry.name,
        extension="PNG",
        payload=encode_png(image),
    )


def load_approved_hd4() -> dict[int, Image.Image]:
    classic = read_pack(CLASSIC_PACK)
    approved: dict[int, Image.Image] = {}
    for resource_id, (name, logical_size, filename) in RESOURCES.items():
        if resource_id >= len(classic):
            raise AssertionError(f"classic resource ID {resource_id} is absent")
        entry = classic[resource_id]
        if entry.name != name:
            raise AssertionError(
                f"classic resource ID {resource_id} is {entry.name}, not {name}"
            )
        classic_image = decode_image(entry.payload)
        if classic_image is None or classic_image.size != logical_size:
            raise AssertionError(
                f"classic {name} has size "
                f"{None if classic_image is None else classic_image.size}; "
                f"expected {logical_size}"
            )

        path = REVIEW / filename
        if not path.is_file():
            raise FileNotFoundError(path)
        image = Image.open(path).convert("RGBA")
        expected_hd4 = (logical_size[0] * 4, logical_size[1] * 4)
        if image.size != expected_hd4:
            raise AssertionError(
                f"{filename} has size {image.size}; expected {expected_hd4}"
            )
        bbox = image.getchannel("A").getbbox()
        if bbox is None:
            raise AssertionError(f"{filename} is fully transparent")
        if (
            bbox[0] <= 1
            or bbox[1] <= 1
            or bbox[2] >= image.width - 1
            or bbox[3] >= image.height - 1
        ):
            raise AssertionError(
                f"{filename} touches the atlas boundary: {bbox}"
            )
        approved[resource_id] = image
    return approved


def patch_pack(
    base_path: Path,
    output_path: Path,
    images: dict[int, Image.Image],
    density: int,
) -> dict[str, object]:
    entries = read_pack(base_path)
    before_count = len(entries)
    output_entries = list(entries)

    for resource_id, (expected_name, _, _) in RESOURCES.items():
        if resource_id >= len(entries):
            raise AssertionError(f"resource ID {resource_id} is absent")
        if entries[resource_id].name != expected_name:
            raise AssertionError(
                f"resource ID {resource_id} is "
                f"{entries[resource_id].name}, not {expected_name}"
            )
        output_entries[resource_id] = replacement_entry(
            entries[resource_id],
            images[resource_id],
        )

    write_pack(output_path, output_entries)
    packed = read_pack(output_path)
    if len(packed) != before_count:
        raise AssertionError("entry count changed")

    changed_ids = set(RESOURCES)
    for before, after in zip(entries, packed, strict=True):
        if before.index in changed_ids:
            continue
        if (
            before.index != after.index
            or before.name != after.name
            or before.extension != after.extension
            or before.payload != after.payload
        ):
            raise AssertionError(
                f"unrelated resource changed: {before.index}:{before.name}"
            )

    for resource_id, image in images.items():
        packed_image = decode_image(packed[resource_id].payload)
        if packed_image is None or packed_image.size != image.size:
            raise AssertionError(
                f"packed resource {resource_id} has invalid dimensions"
            )

    return {
        "density": density,
        "base": str(base_path),
        "base_sha256": sha256(base_path),
        "output": str(output_path),
        "output_sha256": sha256(output_path),
        "entries": len(packed),
        "changed_ids": sorted(changed_ids),
        "bytes": output_path.stat().st_size,
    }


def main() -> int:
    approved4 = load_approved_hd4()
    approved2 = {
        resource_id: image.resize(
            (image.width // 2, image.height // 2),
            Image.Resampling.LANCZOS,
        )
        for resource_id, image in approved4.items()
    }

    MASTER_DIR.mkdir(parents=True, exist_ok=True)
    for resource_id, image in approved4.items():
        name = RESOURCES[resource_id][0]
        image.save(
            MASTER_DIR / f"{resource_id:04d}_{name}.png",
            optimize=True,
        )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    builds = [
        patch_pack(
            GAME / "data" / "sdl_data_hd2.dat",
            OUTPUT_DIR / "sdl_data_hd2.dat",
            approved2,
            2,
        ),
        patch_pack(
            GAME / "data" / "sdl_data_hd4.dat",
            OUTPUT_DIR / "sdl_data_hd4.dat",
            approved4,
            4,
        ),
    ]

    packed2 = read_pack(OUTPUT_DIR / "sdl_data_hd2.dat")
    packed4 = read_pack(OUTPUT_DIR / "sdl_data_hd4.dat")
    for resource_id in RESOURCES:
        image2 = decode_image(packed2[resource_id].payload)
        image4 = decode_image(packed4[resource_id].payload)
        if image2 is None or image4 is None:
            raise AssertionError(
                f"unable to decode packed resource {resource_id}"
            )
        expected2 = image4.resize(image2.size, Image.Resampling.LANCZOS)
        if ImageChops.difference(
            image2.convert("RGBA"),
            expected2.convert("RGBA"),
        ).getbbox():
            raise AssertionError(
                f"HD2 resource {resource_id} is not the HD4 derivative"
            )

    # BUILD_PRE_CONST is intentionally outside the replacement set.
    for density, output in (
        (2, OUTPUT_DIR / "sdl_data_hd2.dat"),
        (4, OUTPUT_DIR / "sdl_data_hd4.dat"),
    ):
        source = read_pack(GAME / "data" / f"sdl_data_hd{density}.dat")
        result = read_pack(output)
        if source[25].payload != result[25].payload:
            raise AssertionError("BUILD_PRE_CONST changed unexpectedly")

    manifest = {
        "format": 1,
        "status": "built_not_installed",
        "classic_pack": str(CLASSIC_PACK),
        "resource_ids": sorted(RESOURCES),
        "logical_sizes": {
            str(resource_id): list(values[1])
            for resource_id, values in RESOURCES.items()
        },
        "hd4_sizes": {
            str(resource_id): list(approved4[resource_id].size)
            for resource_id in RESOURCES
        },
        "build_pre_const_id": 25,
        "build_pre_const_action": "preserved",
        "builds": builds,
    }
    manifest_path = OUTPUT_DIR.parent / "manifest.json"
    manifest_path.write_text(
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
