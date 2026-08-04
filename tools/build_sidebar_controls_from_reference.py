#!/usr/bin/env python3
"""Prepare and integrate the user-approved HD sidebar controls.

The reference is a review sheet rather than a sprite atlas.  This tool crops
the six artwork cells, normalizes them to the original logical dimensions and
rebuilds HD2 exclusively from the accepted HD4 masters.  BTN_ORDER is kept
text-free because its localized caption is rendered by the game.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys
from dataclasses import replace
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hd_assets import decode_image, encode_png, read_pack, safe_name, write_pack  # noqa: E402


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REFERENCE = Path(
    r"C:\Users\Slaven\AppData\Local\Temp\codex-clipboard-d186eb82-5db7-4dd4-85ec-12b6c17ededa.png"
)
OUTPUT = ROOT / "artifacts" / "sidebar_controls_v1"
MASTER_ROOT = ROOT / "resources" / "hd" / "master4" / "sdl_inter"
COMPLETION_ROOT = ROOT / "artifacts" / "hd_completion" / "interface"

# Pixel coordinates in the supplied 1672x941 review sheet.  The labels beneath
# the images are deliberately excluded.
CROPS = {
    19: (18, 18, 962, 207),
    72: (1210, 17, 1419, 190),
    73: (316, 249, 527, 423),
    74: (1211, 249, 1419, 423),
    75: (316, 475, 527, 649),
    76: (1211, 475, 1419, 649),
    77: (316, 700, 527, 875),
}


def sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def resize_premultiplied(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    return image.convert("RGBA").convert("RGBa").resize(
        size, Image.Resampling.LANCZOS
    ).convert("RGBA")


def make_blank_order_button(reference_crop: Image.Image, size: tuple[int, int]) -> Image.Image:
    """Retain the approved frame while replacing the baked caption with metal."""
    image = reference_crop.convert("RGBA").resize(size, Image.Resampling.LANCZOS)
    draw = ImageDraw.Draw(image)
    width, height = size
    left, top, right, bottom = 28, 24, width - 29, height - 24

    # The reference uses a warm gold plate.  A deterministic brushed gradient
    # avoids inpainting artefacts and leaves the engine-owned caption legible.
    for y in range(top, bottom + 1):
        position = (y - top) / max(1, bottom - top)
        highlight = int(25 * (1.0 - abs(position - 0.43) * 2.0))
        red = min(255, 202 + highlight)
        green = min(255, 128 + highlight)
        blue = min(255, 18 + highlight // 3)
        draw.line((left, y, right, y), fill=(red, green, blue, 255))

    # Subtle machining lines; no language-specific pixels are stored here.
    draw.line((left, top, right, top), fill=(255, 207, 73, 255), width=2)
    draw.line((left, bottom, right, bottom), fill=(103, 57, 8, 255), width=2)
    draw.line((left + 8, top + 7, right - 8, top + 7), fill=(233, 169, 39, 180), width=1)
    draw.line((left + 8, bottom - 7, right - 8, bottom - 7), fill=(154, 87, 9, 180), width=1)
    return image


def atomic_copy(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_name(destination.name + ".tmp")
    shutil.copy2(source, temporary)
    os.replace(temporary, destination)


def update_completion_manifest(records: dict[int, dict[str, object]]) -> None:
    manifest_path = COMPLETION_ROOT / "manifest.json"
    if not manifest_path.is_file():
        return
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    by_id = {int(record["id"]): record for record in manifest.get("assets", [])}
    for resource_id, generated in records.items():
        existing = by_id.get(resource_id)
        if existing is None:
            continue
        existing["sha256"] = generated["sha256"]
        existing["file"] = generated["completion_file"]
        existing["hd_size"] = generated["hd4_size"]
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def patch_pack(source: Path, destination: Path, masters: dict[int, Image.Image], density: int) -> None:
    before = read_pack(source)
    after = []
    for entry in before:
        master = masters.get(entry.index)
        if master is None:
            after.append(entry)
            continue
        logical_width = master.width // 4
        logical_height = master.height // 4
        image = master if density == 4 else resize_premultiplied(
            master, (logical_width * 2, logical_height * 2)
        )
        after.append(replace(entry, extension="png", payload=encode_png(image)))
    write_pack(destination, after)
    reread = read_pack(destination)
    targets = set(masters)
    for old, new in zip(before, reread, strict=True):
        if old.index not in targets and old.payload != new.payload:
            raise AssertionError(f"Unrelated resource changed: {old.index} {old.name}")
        if old.index != new.index or old.name != new.name:
            raise AssertionError(f"Pack identity changed at {old.index}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--reference", type=Path, default=DEFAULT_REFERENCE)
    parser.add_argument(
        "--data-dir", type=Path, default=ROOT / "resources" / "bin" / "data"
    )
    parser.add_argument("--install-dir", type=Path)
    args = parser.parse_args()

    reference = args.reference.resolve()
    if not reference.is_file():
        raise FileNotFoundError(reference)
    sheet = Image.open(reference).convert("RGBA")
    if sheet.size != (1672, 941):
        raise ValueError(f"Unexpected reference size {sheet.size}; expected 1672x941")

    classic_entries = read_pack(args.data_dir / "sdl_inter.dat")
    OUTPUT.mkdir(parents=True, exist_ok=True)
    MASTER_ROOT.mkdir(parents=True, exist_ok=True)
    masters: dict[int, Image.Image] = {}
    records: dict[int, dict[str, object]] = {}

    for resource_id, box in CROPS.items():
        classic = decode_image(classic_entries[resource_id].payload)
        if classic is None:
            raise ValueError(f"Classic resource {resource_id} is not an image")
        target_size = (classic.width * 4, classic.height * 4)
        crop = sheet.crop(box)
        master = (
            make_blank_order_button(crop, target_size)
            if resource_id == 19
            else resize_premultiplied(crop, target_size)
        )
        masters[resource_id] = master
        filename = f"{resource_id:04d}_{safe_name(classic_entries[resource_id].name)}.png"
        master_path = MASTER_ROOT / filename
        master_path.write_bytes(encode_png(master))

        completion_path = COMPLETION_ROOT / "controls" / filename
        completion_path.parent.mkdir(parents=True, exist_ok=True)
        completion_path.write_bytes(encode_png(master))
        preview_path = OUTPUT / filename
        preview_path.write_bytes(encode_png(master))
        records[resource_id] = {
            "id": resource_id,
            "name": classic_entries[resource_id].name,
            "crop": list(box),
            "logical_size": [classic.width, classic.height],
            "hd4_size": list(master.size),
            "sha256": sha256(preview_path.read_bytes()),
            "completion_file": completion_path.relative_to(COMPLETION_ROOT).as_posix(),
        }

    update_completion_manifest(records)

    stage_data = OUTPUT / "data"
    stage_data.mkdir(parents=True, exist_ok=True)
    for density in (2, 4):
        source = args.data_dir / f"sdl_inter_hd{density}.dat"
        destination = stage_data / source.name
        patch_pack(source, destination, masters, density)

    contact = Image.new("RGBA", (720, 360), (9, 12, 14, 255))
    order = masters[19].copy()
    order.thumbnail((640, 128), Image.Resampling.LANCZOS)
    contact.alpha_composite(order, ((contact.width - order.width) // 2, 16))
    for column, resource_id in enumerate(range(72, 78)):
        icon = masters[resource_id].copy()
        icon.thumbnail((132, 108), Image.Resampling.LANCZOS)
        x = 18 + column * 117
        contact.alpha_composite(icon, (x, 190))
    contact.save(OUTPUT / "contact_sheet.png", optimize=True)

    report = {
        "format": 1,
        "reference": str(reference),
        "caption": "runtime-owned: ЗАКАЗ",
        "assets": list(records.values()),
    }
    (OUTPUT / "manifest.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    for destination_root in filter(None, (args.install_dir, args.data_dir)):
        destination_root = Path(destination_root)
        for density in (2, 4):
            atomic_copy(
                stage_data / f"sdl_inter_hd{density}.dat",
                destination_root / f"sdl_inter_hd{density}.dat",
            )

    print(f"Prepared {len(masters)} controls in {OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
