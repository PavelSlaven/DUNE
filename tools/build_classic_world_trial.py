#!/usr/bin/env python3
"""Build HD packs with the original D2TM world and the current HD interface."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageChops

from hd_assets import PackEntry, decode_image, encode_png, read_pack, write_pack


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "resources" / "bin" / "data"
OUTPUT = ROOT / "artifacts" / "classic_world_trial" / "data"

# World-facing resources only. Credits and mouse cursors keep their current HD
# artwork; buildings, projectiles, explosions, terrain, tracks and units return
# to the exact classic D2TM pixels.
WORLD_IDS = (
    {0, 78}
    | set(range(1, 53))
    | set(range(64, 78))
    | set(range(90, 108))
    | set(range(109, 167))
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def scale_classic(image: Image.Image, density: int) -> Image.Image:
    """Duplicate original pixels exactly; runtime filtering handles display."""
    return image.resize(
        (image.width * density, image.height * density),
        Image.Resampling.NEAREST,
    )


def verify_pack(
    classic_entries: list[PackEntry],
    base_entries: list[PackEntry],
    output_path: Path,
    density: int,
) -> None:
    result = read_pack(output_path)
    if len(result) != len(classic_entries):
        raise AssertionError(
            f"{output_path}: expected {len(classic_entries)} entries, got {len(result)}"
        )
    for index, (classic, base, trial) in enumerate(
        zip(classic_entries, base_entries[: len(classic_entries)], result, strict=True)
    ):
        if trial.index != index or trial.name != classic.name:
            raise AssertionError(f"ID/name mismatch at {index}: {trial.name}")
        if index not in WORLD_IDS:
            if trial.payload != base.payload:
                raise AssertionError(f"non-world HD resource changed: {index}:{trial.name}")
            continue

        classic_image = decode_image(classic.payload)
        trial_image = decode_image(trial.payload)
        if classic_image is None or trial_image is None:
            if classic.payload != trial.payload:
                raise AssertionError(f"non-image world payload changed: {index}")
            continue
        expected_size = (
            classic_image.width * density,
            classic_image.height * density,
        )
        if trial_image.size != expected_size:
            raise AssertionError(
                f"{index}:{trial.name} size {trial_image.size}, expected {expected_size}"
            )
        downsampled = trial_image.resize(
            classic_image.size,
            Image.Resampling.NEAREST,
        )
        if ImageChops.difference(
            downsampled.convert("RGBA"),
            classic_image.convert("RGBA"),
        ).getbbox():
            raise AssertionError(f"classic pixels changed: {index}:{trial.name}")


def build_density(classic_entries: list[PackEntry], density: int) -> dict[str, object]:
    base_path = DATA / f"sdl_data_hd{density}.dat"
    output_path = OUTPUT / base_path.name
    base_entries = read_pack(base_path)
    if len(base_entries) < len(classic_entries):
        raise AssertionError(f"{base_path} has too few entries")

    output_entries: list[PackEntry] = []
    for index, classic in enumerate(classic_entries):
        base = base_entries[index]
        if classic.name != base.name:
            raise AssertionError(
                f"base pack name mismatch at {index}: {classic.name} != {base.name}"
            )
        if index not in WORLD_IDS:
            output_entries.append(
                PackEntry(index, base.name, base.extension, base.payload)
            )
            continue

        image = decode_image(classic.payload)
        if image is None:
            payload = classic.payload
            extension = classic.extension
        else:
            payload = encode_png(scale_classic(image, density))
            extension = "PNG"
        output_entries.append(
            PackEntry(index, classic.name, extension, payload)
        )

    # Deliberately omit appended house variants, HD terrain variations,
    # foundations and beacons. This makes every world lookup fall back to the
    # original base atlas and its original palette swap.
    write_pack(output_path, output_entries)
    verify_pack(classic_entries, base_entries, output_path, density)
    return {
        "density": density,
        "path": str(output_path),
        "entries": len(output_entries),
        "world_resources": len(WORLD_IDS),
        "sha256": sha256(output_path),
        "bytes": output_path.stat().st_size,
    }


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    classic_path = DATA / "sdl_data.dat"
    classic_entries = read_pack(classic_path)
    if len(classic_entries) != 167:
        raise AssertionError(
            f"{classic_path}: expected 167 resources, got {len(classic_entries)}"
        )
    builds = [
        build_density(classic_entries, 2),
        build_density(classic_entries, 4),
    ]
    manifest = {
        "format": 1,
        "purpose": "Original D2TM world in density-aware HD packs",
        "classic_pack": str(classic_path),
        "classic_sha256": sha256(classic_path),
        "world_ids": sorted(WORLD_IDS),
        "builds": builds,
        "notes": [
            "Buildings, projectiles, effects, terrain, tracks and units are exact classic pixels.",
            "Current HD credits and cursors are retained.",
            "Appended HD world variants are intentionally omitted.",
            "Runtime WorldScale changes visual size only; cells and collisions remain unchanged.",
        ],
    }
    manifest_path = OUTPUT.parent / "manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(manifest, ensure_ascii=False))


if __name__ == "__main__":
    main()
