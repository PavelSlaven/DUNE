#!/usr/bin/env python3
"""Prepare and install corrected NE/NW Trike directions."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

from hd_assets import PackEntry, decode_image, encode_png, read_pack, write_pack
from prepare_trike_review import neutral_and_mask


ROOT = Path(__file__).resolve().parents[1]
GAME = Path(r"C:\Users\Slaven\Desktop\D2TM-v0.8.0.windows.ru")
OUTPUT = ROOT / "artifacts" / "trike_direction_fix_v3"
SOURCE = OUTPUT / "trike_upper_diagonals_alpha.png"
MASTER = ROOT / "resources" / "hd" / "master4" / "sdl_data"
EXTRA = ROOT / "resources" / "hd" / "master4_extra_packs" / "sdl_data"

FRAME = (112, 104)
ATLAS = (896, 104)
DIRECTIONS = ("E", "NE", "N", "NW", "W", "SW", "S", "SE")
UNIT_IDS = {147: "UNIT_RAIDER", 162: "UNIT_TRIKE"}
SHADOW_IDS = {148: "UNIT_RAIDER_SHADOW", 163: "UNIT_TRIKE_SHADOW"}
MASK_NAMES = (
    "HM_UNIT_TRIKE",
    "HOUSEMASK_UNIT_TRIKE",
    "HM_UNIT_RAIDER",
    "HOUSEMASK_UNIT_RAIDER",
)
VARIANT_NAMES = tuple(
    f"{prefix}_UNIT_{unit}"
    for unit in ("TRIKE", "RAIDER")
    for prefix in (
        "HV_A",
        "HV_H",
        "HV_O",
        "HOUSEVARIANT_ATREIDES",
        "HOUSEVARIANT_HARKONNEN",
        "HOUSEVARIANT_ORDOS",
    )
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def frame(atlas: Image.Image, index: int) -> Image.Image:
    return atlas.crop((index * FRAME[0], 0, (index + 1) * FRAME[0], FRAME[1]))


def replace_frame(atlas: Image.Image, index: int, image: Image.Image) -> None:
    box = (index * FRAME[0], 0, (index + 1) * FRAME[0], FRAME[1])
    atlas.paste((0, 0, 0, 0), box)
    atlas.alpha_composite(image, (index * FRAME[0], 0))


def extract_upper_directions() -> dict[str, Image.Image]:
    source = Image.open(SOURCE).convert("RGBA")
    rgba = np.asarray(source, dtype=np.uint8)
    count, labels, stats, centroids = cv2.connectedComponentsWithStats(
        (rgba[:, :, 3] > 8).astype(np.uint8),
        8,
    )
    components: list[tuple[float, int, int, int, int, int]] = []
    for label in range(1, count):
        x, y, width, height, area = stats[label]
        if area >= 20_000:
            components.append((centroids[label][0], label, x, y, width, height))
    if len(components) != 2:
        raise AssertionError(f"expected two Trikes, found {len(components)}")
    components.sort()

    result: dict[str, Image.Image] = {}
    # The generated sheet contains NW on the left and NE on the right.
    for direction, (_, label, x, y, width, height) in zip(
        ("NW", "NE"), components, strict=True
    ):
        crop = rgba[y : y + height, x : x + width].copy()
        component_alpha = (
            (labels[y : y + height, x : x + width] == label).astype(np.uint8)
            * 255
        )
        crop[:, :, 3] = np.minimum(crop[:, :, 3], component_alpha)
        crop[crop[:, :, 3] == 0, :3] = 0
        result[direction] = Image.fromarray(crop, "RGBA")
    return result


def place_matching_coverage(subject: Image.Image, target_sum: int) -> Image.Image:
    box = subject.getchannel("A").getbbox()
    if box is None:
        raise AssertionError("empty generated Trike direction")
    subject = subject.crop(box)
    candidates: list[tuple[int, Image.Image]] = []
    # The legacy atlas stretches every direction to a common silhouette box.
    # Search the same narrow envelope and choose the closest opaque coverage,
    # while retaining a one-pixel safety margin on every side.
    for width in range(102, 111):
        for height in range(96, 103):
            image = subject.resize((width, height), Image.Resampling.LANCZOS)
            alpha_sum = int(
                np.asarray(image.getchannel("A"), dtype=np.uint64).sum()
            )
            candidates.append((abs(alpha_sum - target_sum), image))
    _, candidate = min(candidates, key=lambda item: item[0])
    placed = Image.new("RGBA", FRAME)
    x = round((FRAME[0] - candidate.width) / 2)
    y = round((FRAME[1] - candidate.height) / 2)
    placed.alpha_composite(candidate, (x, y))
    return placed


def shadow_frame(image: Image.Image) -> Image.Image:
    alpha = (
        image.getchannel("A")
        .filter(ImageFilter.GaussianBlur(1.6))
        .point(lambda value: round(value * 0.22))
    )
    shadow = Image.new("RGBA", FRAME, (5, 4, 3, 0))
    shadow.putalpha(alpha)
    shifted = Image.new("RGBA", FRAME)
    shifted.alpha_composite(shadow, (3, 3))
    return shifted


def mask_entry(entries: list[PackEntry], name: str) -> PackEntry:
    aliases = (name, name.replace("HM_", "HOUSEMASK_"))
    matches = [entry for entry in entries if entry.name in aliases]
    if not matches:
        raise AssertionError(f"pack has no {name}")
    return matches[0]


def prepare() -> dict[str, object]:
    entries = read_pack(GAME / "data" / "sdl_data_hd4.dat")
    base = decode_image(entries[162].payload)
    shadow = decode_image(entries[163].payload)
    mask = decode_image(mask_entry(entries, "HM_UNIT_TRIKE").payload)
    if base is None or shadow is None or mask is None:
        raise AssertionError("cannot decode installed Trike resources")
    if base.size != ATLAS or shadow.size != ATLAS or mask.size != ATLAS:
        raise AssertionError("installed Trike resources have unexpected dimensions")

    base = base.convert("RGBA")
    shadow = shadow.convert("RGBA")
    mask = mask.convert("RGBA")
    corrected = extract_upper_directions()
    changed: dict[str, dict[str, object]] = {}
    for direction in ("NE", "NW"):
        index = DIRECTIONS.index(direction)
        old_frame = frame(base, index)
        target_sum = int(
            np.asarray(old_frame.getchannel("A"), dtype=np.uint64).sum()
        )
        placed = place_matching_coverage(corrected[direction], target_sum)
        neutral, direction_mask = neutral_and_mask(placed)
        replace_frame(base, index, neutral)
        replace_frame(mask, index, direction_mask)
        replace_frame(shadow, index, shadow_frame(neutral))
        changed[direction] = {
            "index": index,
            "bbox": list(neutral.getchannel("A").getbbox() or ()),
            "alpha_sum": int(
                np.asarray(neutral.getchannel("A"), dtype=np.uint64).sum()
            ),
            "target_alpha_sum": target_sum,
        }

    for name, image in (("unit", base), ("shadow", shadow), ("mask", mask)):
        if image.size != ATLAS or image.getchannel("A").getbbox() is None:
            raise AssertionError(f"invalid corrected {name} atlas")

    OUTPUT.mkdir(parents=True, exist_ok=True)
    unit_path = OUTPUT / "UNIT_TRIKE_HD4_FIXED.png"
    shadow_path = OUTPUT / "UNIT_TRIKE_SHADOW_HD4_FIXED.png"
    mask_path = OUTPUT / "HM_UNIT_TRIKE_HD4_FIXED.png"
    base.save(unit_path, optimize=True)
    shadow.save(shadow_path, optimize=True)
    mask.save(mask_path, optimize=True)

    preview = Image.new("RGBA", (FRAME[0] * 4, FRAME[1] * 2 + 42), (12, 14, 17, 255))
    draw = ImageDraw.Draw(preview)
    for column, direction in enumerate(("NE до", "NE после", "NW до", "NW после")):
        index = 1 if column < 2 else 3
        image = frame(decode_image(entries[162].payload).convert("RGBA"), index) if column % 2 == 0 else frame(base, index)
        preview.alpha_composite(image, (column * FRAME[0], 0))
        draw.text((column * FRAME[0] + 8, FRAME[1] + 8), direction, fill=(235, 210, 145, 255))
    preview.save(OUTPUT / "trike_upper_directions_before_after.png", optimize=True)

    manifest = {
        "format": 1,
        "status": "prepared_not_installed",
        "direction_order": list(DIRECTIONS),
        "corrected": changed,
        "source": str(SOURCE),
        "unit_sha256": sha256(unit_path),
        "prompt": (
            "Fixed-camera oblique RTS views: NW on the left, NE on the right; "
            "single front wheel and gun point upward; flat magenta chroma key."
        ),
    }
    (OUTPUT / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return manifest


def replacement(entry: PackEntry, image: Image.Image) -> PackEntry:
    return PackEntry(entry.index, entry.name, "PNG", encode_png(image))


def patch_pack(path: Path, density: int) -> dict[str, object]:
    entries = read_pack(path)
    unit4 = Image.open(OUTPUT / "UNIT_TRIKE_HD4_FIXED.png").convert("RGBA")
    shadow4 = Image.open(OUTPUT / "UNIT_TRIKE_SHADOW_HD4_FIXED.png").convert("RGBA")
    mask4 = Image.open(OUTPUT / "HM_UNIT_TRIKE_HD4_FIXED.png").convert("RGBA")
    if density == 2:
        size = (ATLAS[0] // 2, ATLAS[1] // 2)
        unit = unit4.resize(size, Image.Resampling.LANCZOS)
        shadow = shadow4.resize(size, Image.Resampling.LANCZOS)
        mask = mask4.resize(size, Image.Resampling.LANCZOS)
    else:
        unit, shadow, mask = unit4, shadow4, mask4

    output = list(entries)
    changed: set[int] = set()
    for index, expected in UNIT_IDS.items():
        if entries[index].name != expected:
            raise AssertionError(f"resource {index} is not {expected}")
        output[index] = replacement(entries[index], unit)
        changed.add(index)
    for index, expected in SHADOW_IDS.items():
        if entries[index].name != expected:
            raise AssertionError(f"resource {index} is not {expected}")
        output[index] = replacement(entries[index], shadow)
        changed.add(index)
    for entry in entries:
        if entry.name in MASK_NAMES:
            output[entry.index] = replacement(entry, mask)
            changed.add(entry.index)
        elif entry.name in VARIANT_NAMES:
            output[entry.index] = replacement(entry, unit)
            changed.add(entry.index)

    temp = path.with_suffix(path.suffix + ".trike.tmp")
    write_pack(temp, output)
    packed = read_pack(temp)
    for before, after in zip(entries, packed, strict=True):
        if before.index in changed:
            continue
        if (
            before.name != after.name
            or before.extension != after.extension
            or before.payload != after.payload
        ):
            temp.unlink(missing_ok=True)
            raise AssertionError(f"unrelated resource changed: {before.index}:{before.name}")
    os.replace(temp, path)
    return {"path": str(path), "density": density, "changed_ids": sorted(changed)}


def update_masters() -> None:
    unit = Image.open(OUTPUT / "UNIT_TRIKE_HD4_FIXED.png").convert("RGBA")
    shadow = Image.open(OUTPUT / "UNIT_TRIKE_SHADOW_HD4_FIXED.png").convert("RGBA")
    mask = Image.open(OUTPUT / "HM_UNIT_TRIKE_HD4_FIXED.png").convert("RGBA")
    MASTER.mkdir(parents=True, exist_ok=True)
    EXTRA.mkdir(parents=True, exist_ok=True)
    for resource_id, name in UNIT_IDS.items():
        unit.save(MASTER / f"{resource_id:04d}_{name}.png", optimize=True)
    for resource_id, name in SHADOW_IDS.items():
        shadow.save(MASTER / f"{resource_id:04d}_{name}.png", optimize=True)
    for name in MASK_NAMES:
        mask.save(EXTRA / f"{name}.png", optimize=True)
    for name in VARIANT_NAMES:
        path = EXTRA / f"{name}.png"
        if path.exists():
            unit.save(path, optimize=True)


def install() -> dict[str, object]:
    builds = [
        patch_pack(GAME / "data" / "sdl_data_hd2.dat", 2),
        patch_pack(GAME / "data" / "sdl_data_hd4.dat", 4),
    ]
    update_masters()
    manifest_path = OUTPUT / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["status"] = "installed"
    manifest["packs"] = builds
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--install", action="store_true")
    args = parser.parse_args()
    manifest = prepare()
    if args.install:
        manifest = install()
    print(json.dumps(manifest, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
