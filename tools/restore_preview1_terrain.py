#!/usr/bin/env python3
"""Restore preview1 HD terrain and create seam-safe restrained variants."""

from __future__ import annotations

import argparse
import hashlib
import io
import json
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

from hd_assets import read_pack


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PACK = Path(
    r"C:\Users\Slaven\Desktop\D2TM-v0.8.0.windows.ru3-preview1-ready"
    r"\data\sdl_data_hd4.dat"
)
SOURCE = (
    ROOT
    / "resources"
    / "hd"
    / "source_references"
    / "preview3"
    / "terrain_previous_hd4"
)
CLASSIC = ROOT / "resources" / "hd" / "classic" / "sdl_data"
MASTER = ROOT / "resources" / "hd" / "master4" / "sdl_data"
EXTRA = ROOT / "resources" / "hd" / "master4_extra_packs" / "sdl_data"

TERRAIN_IDS = range(117, 126)
VARIANT_IDS = {
    118: "TERRAIN_HILL",
    119: "TERRAIN_MOUNTAIN",
    120: "TERRAIN_ROCK",
    121: "TERRAIN_SAND",
    123: "TERRAIN_SPICE",
    124: "TERRAIN_SPICEHILL",
}
TILE_SIZE = 128
EDGE_GUARD = 8


def classic_path(resource_id: int) -> Path:
    return next(CLASSIC.glob(f"{resource_id:04d}_*.png"))


def master_path(resource_id: int) -> Path:
    return MASTER / classic_path(resource_id).name


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def edge_safe_variant(
    image: Image.Image,
    seed: int,
    variant_index: int,
) -> Image.Image:
    rgba = np.array(image.convert("RGBA"), dtype=np.uint8)
    result = rgba.copy()
    rng = np.random.default_rng(seed + variant_index * 7919)

    for top in range(0, rgba.shape[0], TILE_SIZE):
        for left in range(0, rgba.shape[1], TILE_SIZE):
            bottom = min(top + TILE_SIZE, rgba.shape[0])
            right = min(left + TILE_SIZE, rgba.shape[1])
            height = bottom - top
            width = right - left
            if height <= EDGE_GUARD * 2 or width <= EDGE_GUARD * 2:
                continue

            coarse = rng.normal(0.0, 1.0, (9, 9)).astype(np.float32)
            noise = cv2.resize(
                coarse,
                (width, height),
                interpolation=cv2.INTER_CUBIC,
            )
            noise = cv2.GaussianBlur(noise, (0, 0), sigmaX=5.0)
            maximum = max(0.001, float(np.max(np.abs(noise))))
            noise /= maximum

            y0 = top + EDGE_GUARD
            y1 = bottom - EDGE_GUARD
            x0 = left + EDGE_GUARD
            x1 = right - EDGE_GUARD
            interior = result[y0:y1, x0:x1, :3].astype(np.float32)
            local_noise = noise[
                EDGE_GUARD : height - EDGE_GUARD,
                EDGE_GUARD : width - EDGE_GUARD,
            ][..., None]
            strength = 3.0 + variant_index * 0.65
            warm_shift = np.array(
                [
                    0.9 * variant_index,
                    0.25 * variant_index,
                    -0.35 * variant_index,
                ],
                dtype=np.float32,
            )
            interior += local_noise * strength + warm_shift
            alpha = result[y0:y1, x0:x1, 3:4].astype(np.float32) / 255.0
            original = rgba[y0:y1, x0:x1, :3].astype(np.float32)
            interior = interior * alpha + original * (1.0 - alpha)
            result[y0:y1, x0:x1, :3] = np.clip(
                interior,
                0,
                255,
            ).astype(np.uint8)

    return Image.fromarray(result, "RGBA")


def restore(pack_path: Path) -> None:
    entries = read_pack(pack_path)
    SOURCE.mkdir(parents=True, exist_ok=True)
    MASTER.mkdir(parents=True, exist_ok=True)
    EXTRA.mkdir(parents=True, exist_ok=True)

    records: list[dict[str, object]] = []
    for resource_id in TERRAIN_IDS:
        entry = entries[resource_id]
        image = Image.open(io.BytesIO(entry.payload)).convert("RGBA")
        source_path = SOURCE / master_path(resource_id).name
        image.save(source_path, optimize=True)
        image.save(master_path(resource_id), optimize=True)
        records.append(
            {
                "resource_id": resource_id,
                "name": entry.name,
                "width": image.width,
                "height": image.height,
                "pack_entry_sha256": sha256(entry.payload),
                "restored_png_sha256": sha256(source_path.read_bytes()),
            }
        )

        variant_name = VARIANT_IDS.get(resource_id)
        if not variant_name:
            continue
        for variant_index in range(1, 5):
            variant = edge_safe_variant(
                image,
                resource_id * 1009,
                variant_index,
            )
            variant.save(
                EXTRA / f"{variant_name}_VAR_{variant_index:02d}.png",
                optimize=True,
            )

    manifest = {
        "release": "v0.8.0-ru4-preview3",
        "source_pack": str(pack_path),
        "source_pack_sha256": sha256(pack_path.read_bytes()),
        "tile_size_hd4": TILE_SIZE,
        "edge_guard_hd4": EDGE_GUARD,
        "variant_policy": (
            "Only the tile interior changes; the outer eight HD4 pixels "
            "remain byte-identical to the restored preview1 master."
        ),
        "entries": records,
    }
    (SOURCE / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        "Preview1 terrain restored: IDs 117-125, "
        "24 edge-safe variants"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--pack",
        type=Path,
        default=DEFAULT_PACK,
    )
    args = parser.parse_args()
    if not args.pack.is_file():
        raise FileNotFoundError(args.pack)
    restore(args.pack)


if __name__ == "__main__":
    main()
