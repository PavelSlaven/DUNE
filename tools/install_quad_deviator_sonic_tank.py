#!/usr/bin/env python3
"""Atomically install approved Quad, Deviator and Sonic Tank HD atlases."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageChops

from hd_assets import PackEntry, decode_image, encode_png, read_pack, write_pack


ROOT = Path(__file__).resolve().parents[1]
GAME = Path(r"C:\Users\Slaven\Desktop\D2TM-v0.8.0.windows.ru")
OUTPUT = ROOT / "artifacts" / "quad_deviator_sonic_integration_v2"
STAGE = OUTPUT / "data"
BACKUP = OUTPUT / "backup"
MASTER = ROOT / "resources" / "hd" / "master4" / "sdl_data"
EXTRA = ROOT / "resources" / "hd" / "master4_extra_packs" / "sdl_data"

HD4_SIZE = (1024, 128)
HD2_SIZE = (512, 64)


@dataclass(frozen=True)
class Resource:
    resource_id: int
    name: str
    source: Path


@dataclass(frozen=True)
class Mask:
    name: str
    source: Path


QUAD = ROOT / "artifacts" / "quad_review_v2"
DEVIATOR = ROOT / "artifacts" / "deviator_review_v2"
SONIC = ROOT / "artifacts" / "sonic_tank_review_v2"

RESOURCES = (
    Resource(134, "UNIT_DEVIATOR", DEVIATOR / "UNIT_DEVIATOR_HD4_PREVIEW.png"),
    Resource(145, "UNIT_QUAD", QUAD / "UNIT_QUAD_HD4_PREVIEW.png"),
    Resource(146, "UNIT_QUAD_SHADOW", QUAD / "UNIT_QUAD_SHADOW_HD4_PREVIEW.png"),
    Resource(157, "UNIT_SONICTANK", SONIC / "UNIT_SONICTANK_HD4_PREVIEW.png"),
    Resource(158, "UNIT_SONICTANK_SHADOW", SONIC / "UNIT_SONICTANK_SHADOW_HD4_PREVIEW.png"),
)

MASKS = (
    Mask("HM_UNIT_DEVIATOR", DEVIATOR / "HM_UNIT_DEVIATOR_HD4_PREVIEW.png"),
    Mask("HM_UNIT_QUAD", QUAD / "HM_UNIT_QUAD_HD4_PREVIEW.png"),
    Mask("HM_UNIT_SONICTANK", SONIC / "HM_UNIT_SONICTANK_HD4_PREVIEW.png"),
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_sources() -> tuple[dict[int, Image.Image], dict[str, Image.Image]]:
    resources: dict[int, Image.Image] = {}
    masks: dict[str, Image.Image] = {}
    for resource in RESOURCES:
        image = Image.open(resource.source).convert("RGBA")
        if image.size != HD4_SIZE:
            raise AssertionError(f"{resource.name}: expected {HD4_SIZE}, got {image.size}")
        if image.getchannel("A").getbbox() is None:
            raise AssertionError(f"{resource.name} is fully transparent")
        resources[resource.resource_id] = image
    for mask in MASKS:
        image = Image.open(mask.source).convert("RGBA")
        if image.size != HD4_SIZE:
            raise AssertionError(f"{mask.name}: expected {HD4_SIZE}, got {image.size}")
        if image.getchannel("A").getbbox() is None:
            raise AssertionError(f"{mask.name} is fully transparent")
        masks[mask.name] = image
    return resources, masks


def upsert_mask(entries: list[PackEntry], name: str, image: Image.Image) -> int:
    aliases = {name, name.replace("HM_", "HOUSEMASK_", 1)}
    indices = [entry.index for entry in entries if entry.name in aliases]
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


def build_pack(
    source_path: Path,
    output_path: Path,
    resources: dict[int, Image.Image],
    masks: dict[str, Image.Image],
) -> dict[str, object]:
    before = read_pack(source_path)
    after = list(before)
    changed: set[int] = set()

    for resource in RESOURCES:
        current = before[resource.resource_id]
        if current.name != resource.name:
            raise AssertionError(
                f"resource {resource.resource_id} is {current.name}, not {resource.name}"
            )
        after[resource.resource_id] = PackEntry(
            resource.resource_id,
            resource.name,
            "PNG",
            encode_png(resources[resource.resource_id]),
        )
        changed.add(resource.resource_id)

    mask_ids: dict[str, int] = {}
    for name, image in masks.items():
        index = upsert_mask(after, name, image)
        mask_ids[name] = index
        changed.add(index)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    write_pack(output_path, after)
    packed = read_pack(output_path)

    for entry in before:
        if entry.index in changed:
            continue
        installed = packed[entry.index]
        if (
            entry.name != installed.name
            or entry.extension != installed.extension
            or entry.payload != installed.payload
        ):
            raise AssertionError(f"unrelated resource changed: {entry.index}:{entry.name}")

    for resource in RESOURCES:
        image = decode_image(packed[resource.resource_id].payload)
        if image is None or image.size != resources[resource.resource_id].size:
            raise AssertionError(f"invalid packed image for {resource.name}")
    for name, index in mask_ids.items():
        image = decode_image(packed[index].payload)
        if image is None or image.size != masks[name].size:
            raise AssertionError(f"invalid packed image for {name}")

    return {
        "pack": str(output_path),
        "entries": len(packed),
        "changed_ids": sorted(changed),
        "mask_ids": mask_ids,
        "sha256": sha256(output_path),
    }


def save_masters(resources: dict[int, Image.Image], masks: dict[str, Image.Image]) -> None:
    MASTER.mkdir(parents=True, exist_ok=True)
    EXTRA.mkdir(parents=True, exist_ok=True)
    for resource in RESOURCES:
        resources[resource.resource_id].save(
            MASTER / f"{resource.resource_id:04d}_{resource.name}.png",
            optimize=True,
        )
    for name, image in masks.items():
        image.save(EXTRA / f"{name}.png", optimize=True)
        image.save(EXTRA / f"{name.replace('HM_', 'HOUSEMASK_', 1)}.png", optimize=True)


def validate_derivatives(hd2_path: Path, hd4_path: Path, mask_ids: dict[str, int]) -> None:
    hd2 = read_pack(hd2_path)
    hd4 = read_pack(hd4_path)
    ids = [resource.resource_id for resource in RESOURCES] + list(mask_ids.values())
    for resource_id in ids:
        image2 = decode_image(hd2[resource_id].payload)
        image4 = decode_image(hd4[resource_id].payload)
        if image2 is None or image4 is None:
            raise AssertionError(f"cannot decode installed resource {resource_id}")
        expected = image4.resize(image2.size, Image.Resampling.LANCZOS)
        if ImageChops.difference(image2.convert("RGBA"), expected).getbbox():
            raise AssertionError(f"HD2 resource {resource_id} is not the HD4 derivative")


def install(staged: Path, live: Path) -> None:
    BACKUP.mkdir(parents=True, exist_ok=True)
    shutil.copy2(live, BACKUP / live.name)
    temporary = live.with_suffix(live.suffix + ".units-install.tmp")
    shutil.copy2(staged, temporary)
    os.replace(temporary, live)
    if sha256(live) != sha256(staged):
        raise AssertionError(f"installed pack differs from staged pack: {live.name}")


def main() -> int:
    resources4, masks4 = load_sources()
    resources2 = {
        resource_id: image.resize(HD2_SIZE, Image.Resampling.LANCZOS)
        for resource_id, image in resources4.items()
    }
    masks2 = {
        name: image.resize(HD2_SIZE, Image.Resampling.LANCZOS)
        for name, image in masks4.items()
    }
    save_masters(resources4, masks4)

    live2 = GAME / "data" / "sdl_data_hd2.dat"
    live4 = GAME / "data" / "sdl_data_hd4.dat"
    staged2 = STAGE / live2.name
    staged4 = STAGE / live4.name
    result2 = build_pack(live2, staged2, resources2, masks2)
    result4 = build_pack(live4, staged4, resources4, masks4)
    if result2["mask_ids"] != result4["mask_ids"]:
        raise AssertionError("HD2 and HD4 mask IDs differ")
    validate_derivatives(staged2, staged4, result4["mask_ids"])

    install(staged2, live2)
    install(staged4, live4)
    validate_derivatives(live2, live4, result4["mask_ids"])

    manifest = {
        "status": "installed",
        "resources": [{"id": item.resource_id, "name": item.name} for item in RESOURCES],
        "masks": result4["mask_ids"],
        "direction_order": list(("E", "NE", "N", "NW", "W", "SW", "S", "SE")),
        "logical_frame": [32, 32],
        "hd2_frame": [64, 64],
        "hd4_frame": [128, 128],
        "packs": [result2, result4],
    }
    OUTPUT.mkdir(parents=True, exist_ok=True)
    (OUTPUT / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(manifest, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
