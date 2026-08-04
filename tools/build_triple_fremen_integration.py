#!/usr/bin/env python3
"""Patch UNIT_TRIPLEFREMEN into the current HD2/HD4 game packs."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops

from hd_assets import PackEntry, decode_image, encode_png, read_pack, write_pack


ROOT = Path(__file__).resolve().parents[1]
GAME = Path("C:/Users/Slaven/Desktop/D2TM-v0.8.0.windows.ru")
REVIEW = ROOT / "artifacts" / "triple_fremen_gemini_v1"
OUTPUT = ROOT / "artifacts" / "triple_fremen_integration_v1"
UNIT_ID = 164
UNIT_NAME = "UNIT_TRIPLEFREMEN"
MASK_NAME = "HM_UNIT_TRIPLEFREMEN"
MASK_ALIASES = (MASK_NAME, "HOUSEMASK_UNIT_TRIPLEFREMEN")
FRAME4 = 128
FRAME2 = 64
COLUMNS = 8
ROWS = 4


def resize_rgba(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    rgba = np.asarray(image.convert("RGBA"), dtype=np.float32)
    alpha = rgba[:, :, 3] / 255.0
    premultiplied = rgba[:, :, :3] * alpha[:, :, None]
    resized_alpha = np.clip(
        np.asarray(
            Image.fromarray(alpha, "F").resize(size, Image.Resampling.LANCZOS)
        ),
        0.0,
        1.0,
    )
    resized_rgb = np.stack(
        [
            np.asarray(
                Image.fromarray(premultiplied[:, :, channel], "F").resize(
                    size, Image.Resampling.LANCZOS
                )
            )
            for channel in range(3)
        ],
        axis=2,
    )
    visible = resized_alpha > (1.0 / 255.0)
    result = np.zeros((size[1], size[0], 4), dtype=np.uint8)
    result[:, :, 3] = np.round(resized_alpha * 255.0).astype(np.uint8)
    result[visible, :3] = np.clip(
        resized_rgb[visible] / resized_alpha[visible, None], 0, 255
    ).astype(np.uint8)
    return Image.fromarray(result, "RGBA")


def resize_atlas(image: Image.Image, frame_size: int) -> Image.Image:
    """Resize every atlas frame separately so Lanczos cannot bleed between poses."""
    source_frame_width = image.width // COLUMNS
    source_frame_height = image.height // ROWS
    result = Image.new("RGBA", (frame_size * COLUMNS, frame_size * ROWS))
    for row in range(ROWS):
        for column in range(COLUMNS):
            frame = image.crop(
                (
                    column * source_frame_width,
                    row * source_frame_height,
                    (column + 1) * source_frame_width,
                    (row + 1) * source_frame_height,
                )
            )
            resized = resize_rgba(frame, (frame_size, frame_size))
            result.alpha_composite(resized, (column * frame_size, row * frame_size))
    return result


def clamp_mask_to_unit(mask: Image.Image, unit: Image.Image) -> Image.Image:
    rgba = np.asarray(mask.convert("RGBA")).copy()
    unit_alpha = np.asarray(unit.getchannel("A"))
    rgba[:, :, 3] = np.minimum(rgba[:, :, 3], unit_alpha)
    rgba[rgba[:, :, 3] == 0, :3] = 0
    return Image.fromarray(rgba, "RGBA")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def replacement(entry: PackEntry, image: Image.Image) -> PackEntry:
    return PackEntry(entry.index, entry.name, "PNG", encode_png(image))


def validate(unit: Image.Image, mask: Image.Image) -> None:
    expected = (FRAME4 * COLUMNS, FRAME4 * ROWS)
    for name, image in ((UNIT_NAME, unit), (MASK_NAME, mask)):
        if image.size != expected or image.getchannel("A").getbbox() is None:
            raise AssertionError(f"invalid {name}: {image.size}")
    frames = [
        unit.crop((x * FRAME4, y * FRAME4, (x + 1) * FRAME4, (y + 1) * FRAME4))
        for y in range(ROWS)
        for x in range(COLUMNS)
    ]
    if len({frame.tobytes() for frame in frames}) != 32:
        raise AssertionError("UNIT_TRIPLEFREMEN frames are not unique")
    for index, frame in enumerate(frames):
        bbox = frame.getchannel("A").getbbox()
        if bbox is None or bbox[3] != 126:
            raise AssertionError(f"invalid frame {index}: {bbox}")
    if np.any(
        (np.asarray(mask.getchannel("A")) > 0)
        & (np.asarray(unit.getchannel("A")) == 0)
    ):
        raise AssertionError("mask extends outside the unit")


def patch_pack(source: Path, output: Path, unit: Image.Image, mask: Image.Image) -> dict:
    entries = read_pack(source)
    if entries[UNIT_ID].name != UNIT_NAME:
        raise AssertionError(f"resource {UNIT_ID} is {entries[UNIT_ID].name}")
    indices = [entry.index for entry in entries if entry.name in MASK_ALIASES]
    if len(indices) > 1:
        raise AssertionError("multiple triple-Fremen masks")
    mask_id = indices[0] if indices else len(entries)
    patched = list(entries)
    patched[UNIT_ID] = replacement(entries[UNIT_ID], unit)
    mask_entry = PackEntry(mask_id, MASK_NAME, "PNG", encode_png(mask))
    if indices:
        patched[mask_id] = mask_entry
    else:
        patched.append(mask_entry)
    write_pack(output, patched)
    packed = read_pack(output)
    changed = {UNIT_ID, mask_id}
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
    for resource_id, expected in ((UNIT_ID, unit), (mask_id, mask)):
        decoded = decode_image(packed[resource_id].payload)
        if decoded is None or decoded.size != expected.size:
            raise AssertionError(f"invalid packed resource {resource_id}")
    return {
        "source": str(source),
        "output": str(output),
        "entries": len(packed),
        "mask_id": mask_id,
        "changed_ids": sorted(changed),
        "sha256": sha256(output),
    }


def install(source: Path, target: Path, backup: Path) -> None:
    backup.parent.mkdir(parents=True, exist_ok=True)
    if not backup.exists():
        shutil.copy2(target, backup)
    temporary = target.with_name(target.name + ".triple-fremen.tmp")
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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--install", action="store_true")
    args = parser.parse_args()
    unit4 = Image.open(REVIEW / "UNIT_TRIPLEFREMEN_HD4.png").convert("RGBA")
    mask4 = Image.open(REVIEW / "HM_UNIT_TRIPLEFREMEN_HD4.png").convert("RGBA")
    validate(unit4, mask4)
    unit2 = resize_atlas(unit4, FRAME2)
    mask2 = clamp_mask_to_unit(resize_atlas(mask4, FRAME2), unit2)

    master = ROOT / "resources" / "hd" / "master4" / "sdl_data"
    extra = ROOT / "resources" / "hd" / "master4_extra_packs" / "sdl_data"
    master.mkdir(parents=True, exist_ok=True)
    extra.mkdir(parents=True, exist_ok=True)
    unit4.save(master / "0164_UNIT_TRIPLEFREMEN.png", optimize=True)
    mask4.save(extra / f"{MASK_NAME}.png", optimize=True)

    data = OUTPUT / "data"
    data.mkdir(parents=True, exist_ok=True)
    builds = []
    for density, unit, mask in ((2, unit2, mask2), (4, unit4, mask4)):
        builds.append(
            patch_pack(
                GAME / "data" / f"sdl_data_hd{density}.dat",
                data / f"sdl_data_hd{density}.dat",
                unit,
                mask,
            )
        )
    if builds[0]["mask_id"] != builds[1]["mask_id"]:
        raise AssertionError("HD2/HD4 mask IDs differ")
    mask_id = int(builds[0]["mask_id"])

    pack2 = read_pack(data / "sdl_data_hd2.dat")
    pack4 = read_pack(data / "sdl_data_hd4.dat")
    for resource_id in (UNIT_ID, mask_id):
        image2 = decode_image(pack2[resource_id].payload)
        image4 = decode_image(pack4[resource_id].payload)
        if image2 is None or image4 is None:
            raise AssertionError(f"cannot decode {resource_id}")
        derivative = resize_atlas(image4, FRAME2)
        if resource_id == mask_id:
            unit2_derivative = decode_image(pack2[UNIT_ID].payload)
            if unit2_derivative is None:
                raise AssertionError("cannot decode HD2 unit for mask validation")
            derivative = clamp_mask_to_unit(derivative, unit2_derivative)
        if ImageChops.difference(image2, derivative).getbbox():
            raise AssertionError(f"HD2 resource {resource_id} is not derived from HD4")

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
        "resource": {"id": UNIT_ID, "name": UNIT_NAME},
        "mask": {"id": mask_id, "name": MASK_NAME},
        "direction_order": ["E", "NE", "N", "NW", "W", "SW", "S", "SE"],
        "animation_rows": ["MOVE_0", "MOVE_1", "MOVE_2", "ATTACK"],
        "logical_frame": [32, 32],
        "builds": builds,
        "installed_sha256": (
            {
                f"hd{density}": sha256(GAME / "data" / f"sdl_data_hd{density}.dat")
                for density in (2, 4)
            }
            if args.install
            else {}
        ),
    }
    OUTPUT.mkdir(parents=True, exist_ok=True)
    (OUTPUT / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(manifest, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
