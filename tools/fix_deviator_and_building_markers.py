#!/usr/bin/env python3
"""Normalize Deviator directions and install missing HD house beacons."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
from pathlib import Path

from PIL import Image, ImageChops

from build_dune2000_units import resize_premultiplied
from hd_assets import PackEntry, decode_image, encode_png, read_pack, write_pack


ROOT = Path(__file__).resolve().parents[1]
GAME = Path(r"C:\Users\Slaven\Desktop\D2TM-v0.8.0.windows.ru")
OUT = ROOT / "artifacts" / "deviator_and_building_markers_v1"
MASTER = ROOT / "resources" / "hd" / "master4" / "sdl_data"
EXTRA = ROOT / "resources" / "hd" / "master4_extra_packs" / "sdl_data"
DEVIATOR_ID = 134
DEVIATOR_MASK = "HM_UNIT_DEVIATOR"
FRAME_LOGICAL = 32
FRAME_COUNT = 8
BEACONS = (
    "HOUSE_BEACON_ATREIDES",
    "HOUSE_BEACON_HARKONNEN",
    "HOUSE_BEACON_ORDOS",
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def alpha_major(frame: Image.Image, density: int) -> float:
    bounds = frame.getchannel("A").getbbox()
    if bounds is None:
        raise AssertionError("transparent Deviator frame")
    return max(bounds[2] - bounds[0], bounds[3] - bounds[1]) / density


def crop_frames(image: Image.Image, density: int) -> list[Image.Image]:
    frame_size = FRAME_LOGICAL * density
    expected = (frame_size * FRAME_COUNT, frame_size)
    if image.size != expected:
        raise AssertionError(f"expected Deviator atlas {expected}, got {image.size}")
    return [
        image.crop((i * frame_size, 0, (i + 1) * frame_size, frame_size))
        for i in range(FRAME_COUNT)
    ]


def scale_centered(frame: Image.Image, factor: float) -> Image.Image:
    size = (
        max(1, round(frame.width * factor)),
        max(1, round(frame.height * factor)),
    )
    resized = resize_premultiplied(frame.convert("RGBA"), size)
    result = Image.new("RGBA", frame.size, (0, 0, 0, 0))
    left = (frame.width - resized.width) // 2
    top = (frame.height - resized.height) // 2
    if left >= 0 and top >= 0:
        result.alpha_composite(resized, (left, top))
        return result
    source_left = max(0, -left)
    source_top = max(0, -top)
    result.alpha_composite(
        resized.crop(
            (
                source_left,
                source_top,
                source_left + frame.width,
                source_top + frame.height,
            )
        )
    )
    return result


def normalize_deviator(
    classic: Image.Image,
    hd4: Image.Image,
    mask4: Image.Image,
) -> tuple[Image.Image, Image.Image, list[float], list[float]]:
    classic_frames = crop_frames(classic.convert("RGBA"), 1)
    base_frames = crop_frames(hd4.convert("RGBA"), 4)
    mask_frames = crop_frames(mask4.convert("RGBA"), 4)
    before = [
        alpha_major(base, 4) / alpha_major(reference, 1)
        for reference, base in zip(classic_frames, base_frames, strict=True)
    ]
    normalized_frames: list[Image.Image] = []
    normalized_masks: list[Image.Image] = []
    for reference, base, mask in zip(
        classic_frames, base_frames, mask_frames, strict=True
    ):
        factor = alpha_major(reference, 1) / alpha_major(base, 4)
        normalized_frames.append(scale_centered(base, factor))
        normalized_masks.append(scale_centered(mask, factor))

    atlas = Image.new("RGBA", hd4.size, (0, 0, 0, 0))
    mask_atlas = Image.new("RGBA", mask4.size, (0, 0, 0, 0))
    frame_size = FRAME_LOGICAL * 4
    for index, (frame, mask) in enumerate(
        zip(normalized_frames, normalized_masks, strict=True)
    ):
        atlas.alpha_composite(frame, (index * frame_size, 0))
        mask_atlas.alpha_composite(mask, (index * frame_size, 0))
    after = [
        alpha_major(frame, 4) / alpha_major(reference, 1)
        for reference, frame in zip(classic_frames, normalized_frames, strict=True)
    ]
    if max(after) - min(after) > 0.06:
        raise AssertionError(f"Deviator remains inconsistent: {after}")
    return atlas, mask_atlas, before, after


def downsample_deviator(image: Image.Image) -> Image.Image:
    source_frames = crop_frames(image.convert("RGBA"), 4)
    target_size = FRAME_LOGICAL * 2
    result = Image.new(
        "RGBA", (target_size * FRAME_COUNT, target_size), (0, 0, 0, 0)
    )
    for index, frame in enumerate(source_frames):
        result.alpha_composite(
            resize_premultiplied(frame, (target_size, target_size)),
            (index * target_size, 0),
        )
    return result


def downsample_beacon(image: Image.Image) -> Image.Image:
    if image.size != (576, 72):
        raise AssertionError(f"invalid HD4 beacon size {image.size}")
    result = Image.new("RGBA", (288, 36), (0, 0, 0, 0))
    for index in range(8):
        frame = image.crop((index * 72, 0, (index + 1) * 72, 72))
        result.alpha_composite(
            resize_premultiplied(frame, (36, 36)), (index * 36, 0)
        )
    return result


def patch_pack(
    source: Path,
    target: Path,
    deviator: Image.Image,
    mask: Image.Image,
    beacons: dict[str, Image.Image],
) -> dict[str, object]:
    before = read_pack(source)
    after = list(before)
    changed: set[int] = {DEVIATOR_ID}
    if before[DEVIATOR_ID].name != "UNIT_DEVIATOR":
        raise AssertionError("resource 134 is not UNIT_DEVIATOR")
    after[DEVIATOR_ID] = PackEntry(
        DEVIATOR_ID, "UNIT_DEVIATOR", "PNG", encode_png(deviator)
    )
    mask_matches = [entry.index for entry in before if entry.name == DEVIATOR_MASK]
    if len(mask_matches) != 1:
        raise AssertionError(f"expected one {DEVIATOR_MASK}")
    mask_id = mask_matches[0]
    after[mask_id] = PackEntry(mask_id, DEVIATOR_MASK, "PNG", encode_png(mask))
    changed.add(mask_id)

    marker_ids: dict[str, int] = {}
    for name, image in beacons.items():
        matches = [entry.index for entry in after if entry.name == name]
        if len(matches) > 1:
            raise AssertionError(f"duplicate marker {name}")
        if matches:
            resource_id = matches[0]
            after[resource_id] = PackEntry(
                resource_id, name, "PNG", encode_png(image)
            )
            changed.add(resource_id)
        else:
            resource_id = len(after)
            after.append(PackEntry(resource_id, name, "PNG", encode_png(image)))
        marker_ids[name] = resource_id

    target.parent.mkdir(parents=True, exist_ok=True)
    write_pack(target, after)
    packed = read_pack(target)
    if len(packed) != len(after):
        raise AssertionError("staged pack entry count mismatch")
    for entry in before:
        if entry.index in changed:
            continue
        current = packed[entry.index]
        if (
            entry.name != current.name
            or entry.extension != current.extension
            or entry.payload != current.payload
        ):
            raise AssertionError(
                f"unrelated resource changed: {entry.index}:{entry.name}"
            )
    return {
        "path": str(target),
        "entries_before": len(before),
        "entries_after": len(packed),
        "changed_ids": sorted(changed),
        "marker_ids": marker_ids,
        "sha256": sha256(target),
    }


def install(staged: Path, live: Path) -> None:
    backup = OUT / "backup" / live.name
    backup.parent.mkdir(parents=True, exist_ok=True)
    if not backup.exists():
        shutil.copy2(live, backup)
    temporary = live.with_name(live.name + ".deviator-marker.tmp")
    try:
        shutil.copy2(staged, temporary)
        if sha256(staged) != sha256(temporary):
            raise AssertionError(f"temporary copy differs for {live.name}")
        os.replace(temporary, live)
    finally:
        temporary.unlink(missing_ok=True)
    if sha256(staged) != sha256(live):
        raise AssertionError(f"installed pack differs for {live.name}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--install", action="store_true")
    args = parser.parse_args()

    classic_entries = read_pack(GAME / "data" / "sdl_data.dat")
    live4_entries = read_pack(GAME / "data" / "sdl_data_hd4.dat")
    classic = decode_image(classic_entries[DEVIATOR_ID].payload)
    hd4 = decode_image(live4_entries[DEVIATOR_ID].payload)
    mask_entry = next(
        entry for entry in live4_entries if entry.name == DEVIATOR_MASK
    )
    mask4 = decode_image(mask_entry.payload)
    if classic is None or hd4 is None or mask4 is None:
        raise AssertionError("cannot decode Deviator resources")
    normalized4, normalized_mask4, before, after = normalize_deviator(
        classic, hd4, mask4
    )
    normalized2 = downsample_deviator(normalized4)
    normalized_mask2 = downsample_deviator(normalized_mask4)

    beacons4 = {
        name: Image.open(EXTRA / f"{name}.png").convert("RGBA")
        for name in BEACONS
    }
    beacons2 = {name: downsample_beacon(image) for name, image in beacons4.items()}

    stage = OUT / "data"
    builds = []
    for density, unit, mask, beacons in (
        (2, normalized2, normalized_mask2, beacons2),
        (4, normalized4, normalized_mask4, beacons4),
    ):
        filename = f"sdl_data_hd{density}.dat"
        builds.append(
            patch_pack(
                GAME / "data" / filename,
                stage / filename,
                unit,
                mask,
                beacons,
            )
        )

    expected2 = downsample_deviator(normalized4)
    if ImageChops.difference(expected2, normalized2).getbbox():
        raise AssertionError("HD2 Deviator is not derived from HD4")
    normalized4.save(MASTER / "0134_UNIT_DEVIATOR.png", optimize=True)
    normalized_mask4.save(EXTRA / f"{DEVIATOR_MASK}.png", optimize=True)
    normalized_mask4.save(EXTRA / "HOUSEMASK_UNIT_DEVIATOR.png", optimize=True)

    if args.install:
        for density in (2, 4):
            filename = f"sdl_data_hd{density}.dat"
            install(stage / filename, GAME / "data" / filename)

    report = {
        "status": "installed" if args.install else "built_not_installed",
        "deviator_before": [round(value, 4) for value in before],
        "deviator_after": [round(value, 4) for value in after],
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
