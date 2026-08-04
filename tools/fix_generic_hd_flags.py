#!/usr/bin/env python3
"""Replace pixel flags with masked HD flags and remove house sirens."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import shutil
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops

from build_dune2000_units import resize_premultiplied
from hd_assets import PackEntry, decode_image, encode_png, read_pack, write_pack


ROOT = Path(__file__).resolve().parents[1]
GAME = Path(r"C:\Users\Slaven\Desktop\D2TM-v0.8.0.windows.ru")
OUT = ROOT / "artifacts" / "generic_hd_flags_v1"
MASTER = ROOT / "resources" / "hd" / "master4" / "sdl_data"
EXTRA = ROOT / "resources" / "hd" / "master4_extra_packs" / "sdl_data"
FLAG_SPECS = (
    (44, "BUILDING_FLAG_LARGE", "HM_BUILDING_FLAG_LARGE"),
    (45, "BUILDING_FLAG_SMALL", "HM_BUILDING_FLAG_SMALL"),
)
FORBIDDEN = {
    "HOUSE_BEACON_ATREIDES",
    "HOUSE_BEACON_HARKONNEN",
    "HOUSE_BEACON_ORDOS",
}
FRAME_COUNT = 12


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def render_hd_flag(classic: Image.Image) -> tuple[Image.Image, Image.Image]:
    classic = classic.convert("RGBA")
    if classic.height % FRAME_COUNT:
        raise AssertionError("classic flag atlas is not divisible into 12 frames")
    logical_frame_height = classic.height // FRAME_COUNT
    width = classic.width * 4
    height = logical_frame_height * 4
    atlas = Image.new("RGBA", (width, height * FRAME_COUNT), (0, 0, 0, 0))
    mask_atlas = Image.new("RGBA", atlas.size, (0, 0, 0, 0))
    for frame_index in range(FRAME_COUNT):
        source = classic.crop(
            (
                0,
                frame_index * logical_frame_height,
                classic.width,
                (frame_index + 1) * logical_frame_height,
            )
        )
        alpha = source.getchannel("A").resize(
            (width, height), Image.Resampling.LANCZOS
        )
        alpha_array = np.asarray(alpha, dtype=np.uint8)
        yy, xx = np.mgrid[0:height, 0:width]
        phase = frame_index * math.tau / FRAME_COUNT
        fold = 0.5 + 0.5 * np.cos(xx / max(1, width - 1) * math.tau * 1.7 + phase)
        vertical = 1.0 - yy / max(1, height - 1)
        shade = np.clip(76.0 + fold * 48.0 + vertical * 12.0, 62, 142)
        rgba = np.zeros((height, width, 4), dtype=np.uint8)
        rgba[..., 0] = shade.astype(np.uint8)
        rgba[..., 1] = shade.astype(np.uint8)
        rgba[..., 2] = shade.astype(np.uint8)
        rgba[..., 3] = alpha_array
        rgba[alpha_array == 0, :3] = 0
        frame = Image.fromarray(rgba, "RGBA")
        mask_rgba = np.zeros_like(rgba)
        mask_rgba[..., :3] = 255
        mask_rgba[..., 3] = alpha_array
        mask_rgba[alpha_array == 0, :3] = 0
        mask = Image.fromarray(mask_rgba, "RGBA")
        atlas.alpha_composite(frame, (0, frame_index * height))
        mask_atlas.alpha_composite(mask, (0, frame_index * height))
    return atlas, mask_atlas


def downsample_frames(image: Image.Image) -> Image.Image:
    frame_height = image.height // FRAME_COUNT
    target_width = image.width // 2
    target_height = frame_height // 2
    result = Image.new(
        "RGBA", (target_width, target_height * FRAME_COUNT), (0, 0, 0, 0)
    )
    for frame_index in range(FRAME_COUNT):
        frame = image.crop(
            (
                0,
                frame_index * frame_height,
                image.width,
                (frame_index + 1) * frame_height,
            )
        )
        result.alpha_composite(
            resize_premultiplied(frame, (target_width, target_height)),
            (0, frame_index * target_height),
        )
    return result


def patch_pack(
    source: Path,
    target: Path,
    flags: dict[int, Image.Image],
    masks: dict[str, Image.Image],
) -> dict[str, object]:
    before = read_pack(source)
    kept = [entry for entry in before if entry.name not in FORBIDDEN]
    after = [
        PackEntry(index, entry.name, entry.extension, entry.payload)
        for index, entry in enumerate(kept)
    ]
    changed_names = set(FORBIDDEN)
    for resource_id, image in flags.items():
        expected = next(name for rid, name, _ in FLAG_SPECS if rid == resource_id)
        if after[resource_id].name != expected:
            raise AssertionError(
                f"resource {resource_id} is {after[resource_id].name}, expected {expected}"
            )
        after[resource_id] = PackEntry(
            resource_id, expected, "PNG", encode_png(image)
        )
        changed_names.add(expected)

    mask_ids: dict[str, int] = {}
    for name, image in masks.items():
        matches = [entry.index for entry in after if entry.name == name]
        if len(matches) > 1:
            raise AssertionError(f"duplicate mask {name}")
        if matches:
            resource_id = matches[0]
            after[resource_id] = PackEntry(
                resource_id, name, "PNG", encode_png(image)
            )
        else:
            resource_id = len(after)
            after.append(PackEntry(resource_id, name, "PNG", encode_png(image)))
        mask_ids[name] = resource_id
        changed_names.add(name)

    target.parent.mkdir(parents=True, exist_ok=True)
    write_pack(target, after)
    packed = read_pack(target)
    if any(entry.name in FORBIDDEN for entry in packed):
        raise AssertionError("a forbidden siren remains in the staged pack")
    before_by_name = {entry.name: entry for entry in before}
    for entry in packed:
        if entry.name in changed_names:
            continue
        previous = before_by_name.get(entry.name)
        if (
            previous is None
            or previous.extension != entry.extension
            or previous.payload != entry.payload
        ):
            raise AssertionError(f"unrelated resource changed: {entry.name}")
    return {
        "path": str(target),
        "entries_before": len(before),
        "entries_after": len(packed),
        "removed": sorted(FORBIDDEN & set(before_by_name)),
        "changed_ids": sorted(flags),
        "mask_ids": mask_ids,
        "sha256": sha256(target),
    }


def install(staged: Path, live: Path) -> None:
    backup = OUT / "backup" / live.name
    backup.parent.mkdir(parents=True, exist_ok=True)
    if not backup.exists():
        shutil.copy2(live, backup)
    temporary = live.with_name(live.name + ".hd-flags.tmp")
    try:
        shutil.copy2(staged, temporary)
        if sha256(staged) != sha256(temporary):
            raise AssertionError(f"temporary copy differs for {live.name}")
        os.replace(temporary, live)
    finally:
        temporary.unlink(missing_ok=True)
    if sha256(staged) != sha256(live):
        raise AssertionError(f"installed pack differs for {live.name}")


def archive_beacon_masters() -> None:
    archive = OUT / "removed_house_beacon_masters"
    archive.mkdir(parents=True, exist_ok=True)
    for name in FORBIDDEN:
        source = EXTRA / f"{name}.png"
        if source.exists():
            target = archive / source.name
            if target.exists():
                target.unlink()
            shutil.move(str(source), str(target))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--install", action="store_true")
    args = parser.parse_args()

    classic = read_pack(GAME / "data" / "sdl_data.dat")
    flags4: dict[int, Image.Image] = {}
    masks4: dict[str, Image.Image] = {}
    for resource_id, name, mask_name in FLAG_SPECS:
        classic_image = decode_image(classic[resource_id].payload)
        if classic_image is None or classic[resource_id].name != name:
            raise AssertionError(f"cannot decode classic flag {name}")
        flag, mask = render_hd_flag(classic_image)
        flags4[resource_id] = flag
        masks4[mask_name] = mask
        flag.save(MASTER / f"{resource_id:04d}_{name}.png", optimize=True)
        mask.save(EXTRA / f"{mask_name}.png", optimize=True)

    flags2 = {resource_id: downsample_frames(image) for resource_id, image in flags4.items()}
    masks2 = {name: downsample_frames(image) for name, image in masks4.items()}
    stage = OUT / "data"
    builds = []
    for density, flags, masks in ((2, flags2, masks2), (4, flags4, masks4)):
        filename = f"sdl_data_hd{density}.dat"
        builds.append(
            patch_pack(
                GAME / "data" / filename,
                stage / filename,
                flags,
                masks,
            )
        )

    for resource_id in flags4:
        expected = downsample_frames(flags4[resource_id])
        if ImageChops.difference(expected, flags2[resource_id]).getbbox():
            raise AssertionError(f"HD2 flag {resource_id} is not derived from HD4")

    if args.install:
        for density in (2, 4):
            filename = f"sdl_data_hd{density}.dat"
            install(stage / filename, GAME / "data" / filename)
        archive_beacon_masters()

    report = {
        "status": "installed" if args.install else "built_not_installed",
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
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "manifest.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
