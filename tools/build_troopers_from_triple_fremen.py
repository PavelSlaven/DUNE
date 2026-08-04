#!/usr/bin/env python3
"""Clone the approved triple-Fremen art into UNIT_TROOPERS HD packs."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
from pathlib import Path

from PIL import Image

from hd_assets import PackEntry, decode_image, encode_png, read_pack, write_pack


ROOT = Path(__file__).resolve().parents[1]
GAME = Path("C:/Users/Slaven/Desktop/D2TM-v0.8.0.windows.ru")
OUTPUT = ROOT / "artifacts" / "troopers_from_triple_fremen_v1"
SOURCE_ID = 164
SOURCE_NAME = "UNIT_TRIPLEFREMEN"
SOURCE_MASK = "HM_UNIT_TRIPLEFREMEN"
TARGET_ID = 166
TARGET_NAME = "UNIT_TROOPERS"
TARGET_MASK = "HM_UNIT_TROOPERS"
TARGET_MASK_ALIASES = (TARGET_MASK, "HOUSEMASK_UNIT_TROOPERS")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def install(source: Path, target: Path, backup: Path) -> None:
    backup.parent.mkdir(parents=True, exist_ok=True)
    if not backup.exists():
        shutil.copy2(target, backup)
    temporary = target.with_name(target.name + ".troopers.tmp")
    try:
        shutil.copy2(source, temporary)
        if sha256(source) != sha256(temporary):
            raise AssertionError("temporary pack copy differs")
        os.replace(temporary, target)
    finally:
        if temporary.exists():
            temporary.unlink()
    if sha256(source) != sha256(target):
        raise AssertionError("installed pack differs")


def patch_pack(source: Path, output: Path) -> dict[str, object]:
    entries = read_pack(source)
    if entries[SOURCE_ID].name != SOURCE_NAME:
        raise AssertionError(f"resource {SOURCE_ID} is {entries[SOURCE_ID].name}")
    if entries[TARGET_ID].name != TARGET_NAME:
        raise AssertionError(f"resource {TARGET_ID} is {entries[TARGET_ID].name}")

    source_masks = [entry for entry in entries if entry.name == SOURCE_MASK]
    if len(source_masks) != 1:
        raise AssertionError(f"expected one {SOURCE_MASK}, got {len(source_masks)}")
    target_masks = [
        entry for entry in entries if entry.name in TARGET_MASK_ALIASES
    ]
    if len(target_masks) > 1:
        raise AssertionError("multiple UNIT_TROOPERS house masks")
    mask_id = target_masks[0].index if target_masks else len(entries)

    source_unit = decode_image(entries[SOURCE_ID].payload)
    source_mask = decode_image(source_masks[0].payload)
    if source_unit is None or source_mask is None or source_unit.size != source_mask.size:
        raise AssertionError("invalid approved source atlas or mask")
    frame_width = source_unit.width // 8
    frame_height = source_unit.height // 4
    if frame_width != frame_height or frame_width not in (64, 128):
        raise AssertionError(f"unexpected atlas size: {source_unit.size}")
    frames = [
        source_unit.crop(
            (
                column * frame_width,
                row * frame_height,
                (column + 1) * frame_width,
                (row + 1) * frame_height,
            )
        )
        for row in range(4)
        for column in range(8)
    ]
    if len({frame.tobytes() for frame in frames}) != 32:
        raise AssertionError("approved source does not contain 32 unique frames")

    patched = list(entries)
    patched[TARGET_ID] = PackEntry(
        TARGET_ID, TARGET_NAME, "PNG", encode_png(source_unit)
    )
    mask_entry = PackEntry(mask_id, TARGET_MASK, "PNG", encode_png(source_mask))
    if target_masks:
        patched[mask_id] = mask_entry
    else:
        patched.append(mask_entry)
    write_pack(output, patched)

    packed = read_pack(output)
    changed = {TARGET_ID, mask_id}
    for before, after in zip(entries, packed, strict=False):
        if before.index in changed:
            continue
        if (
            before.index != after.index
            or before.name != after.name
            or before.extension != after.extension
            or before.payload != after.payload
        ):
            raise AssertionError(f"unrelated entry changed: {before.index}:{before.name}")
    target_unit = decode_image(packed[TARGET_ID].payload)
    target_mask = decode_image(packed[mask_id].payload)
    if target_unit is None or target_mask is None:
        raise AssertionError("cannot decode patched UNIT_TROOPERS resources")
    if target_unit.tobytes() != source_unit.tobytes():
        raise AssertionError("UNIT_TROOPERS pixels differ from UNIT_TRIPLEFREMEN")
    if target_mask.tobytes() != source_mask.tobytes():
        raise AssertionError("UNIT_TROOPERS mask differs from triple-Fremen mask")
    return {
        "source": str(source),
        "output": str(output),
        "entries": len(packed),
        "mask_id": mask_id,
        "changed_ids": sorted(changed),
        "sha256": sha256(output),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--install", action="store_true")
    args = parser.parse_args()

    data = OUTPUT / "data"
    data.mkdir(parents=True, exist_ok=True)
    builds = [
        patch_pack(
            GAME / "data" / f"sdl_data_hd{density}.dat",
            data / f"sdl_data_hd{density}.dat",
        )
        for density in (2, 4)
    ]
    if builds[0]["mask_id"] != builds[1]["mask_id"]:
        raise AssertionError("HD2/HD4 mask IDs differ")

    hd4_entries = read_pack(data / "sdl_data_hd4.dat")
    unit4 = decode_image(hd4_entries[TARGET_ID].payload)
    mask4 = decode_image(hd4_entries[int(builds[0]["mask_id"])].payload)
    if unit4 is None or mask4 is None:
        raise AssertionError("cannot decode HD4 masters")
    master = ROOT / "resources" / "hd" / "master4" / "sdl_data"
    extra = ROOT / "resources" / "hd" / "master4_extra_packs" / "sdl_data"
    master.mkdir(parents=True, exist_ok=True)
    extra.mkdir(parents=True, exist_ok=True)
    unit4.save(master / "0166_UNIT_TROOPERS.png", optimize=True)
    mask4.save(extra / f"{TARGET_MASK}.png", optimize=True)

    status = "built_not_installed"
    if args.install:
        for density in (2, 4):
            filename = f"sdl_data_hd{density}.dat"
            install(
                data / filename,
                GAME / "data" / filename,
                OUTPUT / "backup" / filename,
            )
        status = "installed"

    manifest = {
        "format": 1,
        "status": status,
        "source": {"id": SOURCE_ID, "name": SOURCE_NAME, "mask": SOURCE_MASK},
        "resource": {"id": TARGET_ID, "name": TARGET_NAME},
        "mask": {"id": builds[0]["mask_id"], "name": TARGET_MASK},
        "direction_order": ["E", "NE", "N", "NW", "W", "SW", "S", "SE"],
        "animation_rows": ["MOVE_0", "MOVE_1", "MOVE_2", "ATTACK"],
        "logical_frame": [32, 32],
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
    OUTPUT.mkdir(parents=True, exist_ok=True)
    (OUTPUT / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(manifest, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
