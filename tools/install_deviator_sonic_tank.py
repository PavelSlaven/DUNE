#!/usr/bin/env python3
"""Install the approved Deviator and Sonic Tank atlases into HD packs."""

from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageChops

from hd_assets import PackEntry, decode_image, encode_png, read_pack, write_pack


ROOT = Path(__file__).resolve().parents[1]
GAME = Path(r"C:\Users\Slaven\Desktop\D2TM-v0.8.0.windows.ru")
OUTPUT = ROOT / "artifacts" / "deviator_sonic_tank_integration_v1"
MASTER = ROOT / "resources" / "hd" / "master4" / "sdl_data"
EXTRA = ROOT / "resources" / "hd" / "master4_extra_packs" / "sdl_data"


@dataclass(frozen=True)
class Asset:
    resource_id: int
    name: str
    source: Path
    mask_name: str | None = None
    mask_source: Path | None = None


DEVIATOR_DIR = ROOT / "artifacts" / "deviator_review_v1"
SONIC_DIR = ROOT / "artifacts" / "sonic_tank_review_v1"
ASSETS = (
    Asset(
        134,
        "UNIT_DEVIATOR",
        DEVIATOR_DIR / "UNIT_DEVIATOR_HD4_PREVIEW.png",
        "HM_UNIT_DEVIATOR",
        DEVIATOR_DIR / "HM_UNIT_DEVIATOR_HD4_PREVIEW.png",
    ),
    Asset(
        157,
        "UNIT_SONICTANK",
        SONIC_DIR / "UNIT_SONICTANK_HD4_PREVIEW.png",
        "HM_UNIT_SONICTANK",
        SONIC_DIR / "HM_UNIT_SONICTANK_HD4_PREVIEW.png",
    ),
    Asset(
        158,
        "UNIT_SONICTANK_SHADOW",
        SONIC_DIR / "UNIT_SONICTANK_SHADOW_HD4_PREVIEW.png",
    ),
)
ATLAS_HD4 = (1024, 128)
ATLAS_HD2 = (512, 64)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_sources() -> tuple[dict[int, Image.Image], dict[str, Image.Image]]:
    images: dict[int, Image.Image] = {}
    masks: dict[str, Image.Image] = {}
    for asset in ASSETS:
        image = Image.open(asset.source).convert("RGBA")
        if image.size != ATLAS_HD4:
            raise AssertionError(
                f"{asset.name}: expected {ATLAS_HD4}, got {image.size}"
            )
        if image.getchannel("A").getbbox() is None:
            raise AssertionError(f"{asset.name} is fully transparent")
        images[asset.resource_id] = image
        if asset.mask_name and asset.mask_source:
            mask = Image.open(asset.mask_source).convert("RGBA")
            if mask.size != ATLAS_HD4:
                raise AssertionError(
                    f"{asset.mask_name}: expected {ATLAS_HD4}, got {mask.size}"
                )
            if mask.getchannel("A").getbbox() is None:
                raise AssertionError(f"{asset.mask_name} is fully transparent")
            masks[asset.mask_name] = mask
    return images, masks


def upsert_mask(
    entries: list[PackEntry], name: str, image: Image.Image
) -> int:
    accepted = {name, name.replace("HM_", "HOUSEMASK_", 1)}
    indices = [entry.index for entry in entries if entry.name in accepted]
    if len(indices) > 1:
        raise AssertionError(f"multiple masks found for {name}")
    payload = encode_png(image)
    if indices:
        index = indices[0]
        entries[index] = PackEntry(index, name, "PNG", payload)
        return index
    index = len(entries)
    entries.append(PackEntry(index, name, "PNG", payload))
    return index


def patch_pack(
    path: Path,
    images: dict[int, Image.Image],
    masks: dict[str, Image.Image],
) -> dict[str, object]:
    before = read_pack(path)
    output = list(before)
    changed: set[int] = set()

    for asset in ASSETS:
        if before[asset.resource_id].name != asset.name:
            raise AssertionError(
                f"resource {asset.resource_id} is {before[asset.resource_id].name}, "
                f"not {asset.name}"
            )
        output[asset.resource_id] = PackEntry(
            asset.resource_id,
            asset.name,
            "PNG",
            encode_png(images[asset.resource_id]),
        )
        changed.add(asset.resource_id)

    mask_ids: dict[str, int] = {}
    for name, image in masks.items():
        index = upsert_mask(output, name, image)
        mask_ids[name] = index
        changed.add(index)

    temp = path.with_suffix(path.suffix + ".units.tmp")
    write_pack(temp, output)
    packed = read_pack(temp)

    for entry in before:
        if entry.index in changed:
            continue
        after = packed[entry.index]
        if (
            entry.name != after.name
            or entry.extension != after.extension
            or entry.payload != after.payload
        ):
            temp.unlink(missing_ok=True)
            raise AssertionError(
                f"unrelated resource changed: {entry.index}:{entry.name}"
            )

    for asset in ASSETS:
        image = decode_image(packed[asset.resource_id].payload)
        if image is None or image.size != images[asset.resource_id].size:
            temp.unlink(missing_ok=True)
            raise AssertionError(f"invalid packed image for {asset.name}")
    for name, index in mask_ids.items():
        image = decode_image(packed[index].payload)
        if image is None or image.size != masks[name].size:
            temp.unlink(missing_ok=True)
            raise AssertionError(f"invalid packed image for {name}")

    os.replace(temp, path)
    return {
        "pack": str(path),
        "entries": len(packed),
        "changed_ids": sorted(changed),
        "mask_ids": mask_ids,
        "sha256": sha256(path),
    }


def save_masters(
    images4: dict[int, Image.Image], masks4: dict[str, Image.Image]
) -> None:
    MASTER.mkdir(parents=True, exist_ok=True)
    EXTRA.mkdir(parents=True, exist_ok=True)
    for asset in ASSETS:
        images4[asset.resource_id].save(
            MASTER / f"{asset.resource_id:04d}_{asset.name}.png", optimize=True
        )
    for name, image in masks4.items():
        image.save(EXTRA / f"{name}.png", optimize=True)
        image.save(
            EXTRA / f"{name.replace('HM_', 'HOUSEMASK_', 1)}.png", optimize=True
        )


def validate_derivatives(
    hd2_path: Path, hd4_path: Path, mask_ids: dict[str, int]
) -> None:
    hd2 = read_pack(hd2_path)
    hd4 = read_pack(hd4_path)
    ids = [asset.resource_id for asset in ASSETS] + list(mask_ids.values())
    for resource_id in ids:
        image2 = decode_image(hd2[resource_id].payload)
        image4 = decode_image(hd4[resource_id].payload)
        if image2 is None or image4 is None:
            raise AssertionError(f"cannot decode installed resource {resource_id}")
        expected = image4.resize(image2.size, Image.Resampling.LANCZOS)
        if ImageChops.difference(image2.convert("RGBA"), expected).getbbox():
            raise AssertionError(
                f"HD2 resource {resource_id} is not the HD4 derivative"
            )


def main() -> int:
    images4, masks4 = load_sources()
    images2 = {
        index: image.resize(ATLAS_HD2, Image.Resampling.LANCZOS)
        for index, image in images4.items()
    }
    masks2 = {
        name: image.resize(ATLAS_HD2, Image.Resampling.LANCZOS)
        for name, image in masks4.items()
    }
    save_masters(images4, masks4)

    hd2_path = GAME / "data" / "sdl_data_hd2.dat"
    hd4_path = GAME / "data" / "sdl_data_hd4.dat"
    result2 = patch_pack(hd2_path, images2, masks2)
    result4 = patch_pack(hd4_path, images4, masks4)
    if result2["mask_ids"] != result4["mask_ids"]:
        raise AssertionError("HD2 and HD4 mask IDs differ")
    validate_derivatives(hd2_path, hd4_path, result4["mask_ids"])

    OUTPUT.mkdir(parents=True, exist_ok=True)
    manifest = {
        "status": "installed",
        "resources": [
            {"id": asset.resource_id, "name": asset.name} for asset in ASSETS
        ],
        "direction_order": list(("E", "NE", "N", "NW", "W", "SW", "S", "SE")),
        "logical_frame": [32, 32],
        "hd2_frame": [64, 64],
        "hd4_frame": [128, 128],
        "packs": [result2, result4],
    }
    (OUTPUT / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(manifest, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
