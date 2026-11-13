#!/usr/bin/env python3
"""Make the Raider Trike use the installed Trike HD artwork."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

from hd_assets import PackEntry, decode_image, read_pack, write_pack


GAME = Path(r"C:\Users\Slaven\Desktop\D2TM-v0.8.0.windows.ru")
OUTPUT = Path(__file__).resolve().parents[1] / "artifacts" / "raider_trike_copy"

RAIDER_ID = 147
RAIDER_SHADOW_ID = 148
TRIKE_ID = 162
TRIKE_SHADOW_ID = 163
TRIKE_MASK_NAME = "HM_UNIT_TRIKE"
RAIDER_MASK_NAMES = ("HM_UNIT_RAIDER", "HOUSEMASK_UNIT_RAIDER")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def patch_pack(path: Path) -> dict[str, object]:
    before = read_pack(path)
    expected = {
        RAIDER_ID: "UNIT_RAIDER",
        RAIDER_SHADOW_ID: "UNIT_RAIDER_SHADOW",
        TRIKE_ID: "UNIT_TRIKE",
        TRIKE_SHADOW_ID: "UNIT_TRIKE_SHADOW",
    }
    for index, name in expected.items():
        if before[index].name != name:
            raise AssertionError(f"resource {index} is {before[index].name}, not {name}")

    by_name = {entry.name: entry for entry in before}
    trike_mask = by_name.get(TRIKE_MASK_NAME) or by_name.get(
        "HOUSEMASK_UNIT_TRIKE"
    )
    if trike_mask is None:
        raise AssertionError("installed pack has no Trike house mask")

    output = list(before)
    output[RAIDER_ID] = PackEntry(
        RAIDER_ID,
        "UNIT_RAIDER",
        before[TRIKE_ID].extension,
        before[TRIKE_ID].payload,
    )
    output[RAIDER_SHADOW_ID] = PackEntry(
        RAIDER_SHADOW_ID,
        "UNIT_RAIDER_SHADOW",
        before[TRIKE_SHADOW_ID].extension,
        before[TRIKE_SHADOW_ID].payload,
    )

    mask_indices = [
        entry.index for entry in before if entry.name in RAIDER_MASK_NAMES
    ]
    if len(mask_indices) > 1:
        raise AssertionError("installed pack contains duplicate Raider masks")
    if mask_indices:
        mask_id = mask_indices[0]
        output[mask_id] = PackEntry(
            mask_id, RAIDER_MASK_NAMES[0], trike_mask.extension, trike_mask.payload
        )
    else:
        mask_id = len(output)
        output.append(
            PackEntry(
                mask_id,
                RAIDER_MASK_NAMES[0],
                trike_mask.extension,
                trike_mask.payload,
            )
        )

    temp = path.with_suffix(path.suffix + ".raider.tmp")
    write_pack(temp, output)
    packed = read_pack(temp)

    changed = {RAIDER_ID, RAIDER_SHADOW_ID, mask_id}
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

    for target, source in (
        (RAIDER_ID, TRIKE_ID),
        (RAIDER_SHADOW_ID, TRIKE_SHADOW_ID),
        (mask_id, trike_mask.index),
    ):
        target_image = decode_image(packed[target].payload)
        source_image = decode_image(packed[source].payload)
        if target_image is None or source_image is None:
            temp.unlink(missing_ok=True)
            raise AssertionError(f"cannot decode copied resource {target}")
        if target_image.size != source_image.size:
            temp.unlink(missing_ok=True)
            raise AssertionError(f"resource {target} has incorrect dimensions")
        if packed[target].payload != packed[source].payload:
            temp.unlink(missing_ok=True)
            raise AssertionError(f"resource {target} is not an exact copy")

    os.replace(temp, path)
    return {
        "pack": str(path),
        "entry_count": len(packed),
        "mask_id": mask_id,
        "unit_size": list(decode_image(packed[RAIDER_ID].payload).size),
        "unit_sha256": digest(packed[RAIDER_ID].payload),
        "shadow_sha256": digest(packed[RAIDER_SHADOW_ID].payload),
        "mask_sha256": digest(packed[mask_id].payload),
    }


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    results = [
        patch_pack(GAME / "data" / "sdl_data_hd2.dat"),
        patch_pack(GAME / "data" / "sdl_data_hd4.dat"),
    ]
    manifest = {
        "status": "installed",
        "source": "UNIT_TRIKE",
        "target": "UNIT_RAIDER",
        "copied": ["unit", "shadow", "house_mask"],
        "packs": results,
    }
    (OUTPUT / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(manifest, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
