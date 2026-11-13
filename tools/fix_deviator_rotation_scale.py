#!/usr/bin/env python3
"""Normalize the apparent size of all eight HD Deviator directions.

The accepted oblique artwork uses source renders with different camera crops.
Matching only the longest alpha-bounds edge therefore leaves side views much
smaller than diagonal views.  This tool preserves each pose and normalizes its
visible alpha area to the directional proportions of the classic atlas.
"""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from hd_assets import PackEntry, decode_image, encode_png, read_pack, write_pack


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "resources" / "bin" / "data"
OUT = ROOT / "artifacts" / "deviator_rotation_scale_fix_v1"
MASTER = ROOT / "resources" / "hd" / "master4" / "sdl_data"
EXTRA = ROOT / "resources" / "hd" / "master4_extra_packs" / "sdl_data"
DEVIATOR_ID = 134
DEVIATOR_MASK = "HM_UNIT_DEVIATOR"
DIRECTIONS = ("E", "NE", "N", "NW", "W", "SW", "S", "SE")
FRAME_LOGICAL = 32
FRAME_COUNT = 8
HD4_FRAME = FRAME_LOGICAL * 4
TARGET_MEDIAN_AREA = 6600.0
ALPHA_THRESHOLD = 12


def resize_premultiplied(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    """Resize RGBA with Lanczos while keeping transparent edges fringe-free."""
    rgba = np.asarray(image.convert("RGBA"), dtype=np.float32)
    alpha = rgba[:, :, 3:4] / 255.0
    premultiplied = np.concatenate((rgba[:, :, :3] * alpha, rgba[:, :, 3:4]), axis=2)
    resized = np.asarray(
        Image.fromarray(np.uint8(np.clip(premultiplied + 0.5, 0, 255)), "RGBA").resize(
            size, Image.Resampling.LANCZOS
        ),
        dtype=np.float32,
    )
    resized_alpha = resized[:, :, 3:4]
    rgb = np.zeros_like(resized[:, :, :3])
    np.divide(
        resized[:, :, :3] * 255.0,
        resized_alpha,
        out=rgb,
        where=resized_alpha > 1.0,
    )
    output = np.concatenate((np.clip(rgb, 0, 255), resized_alpha), axis=2)
    output[resized[:, :, 3] <= 1.0] = 0
    return Image.fromarray(np.uint8(np.clip(output + 0.5, 0, 255)), "RGBA")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def crop_frames(image: Image.Image, density: int) -> list[Image.Image]:
    frame_size = FRAME_LOGICAL * density
    expected = (frame_size * FRAME_COUNT, frame_size)
    if image.size != expected:
        raise AssertionError(f"expected atlas {expected}, got {image.size}")
    return [
        image.crop((index * frame_size, 0, (index + 1) * frame_size, frame_size))
        for index in range(FRAME_COUNT)
    ]


def alpha_area(image: Image.Image, threshold: int = ALPHA_THRESHOLD) -> int:
    alpha = np.asarray(image.getchannel("A"))
    return int(np.count_nonzero(alpha > threshold))


def alpha_box(image: Image.Image) -> tuple[int, int, int, int]:
    box = image.getchannel("A").point(
        lambda value: 255 if value > ALPHA_THRESHOLD else 0
    ).getbbox()
    if box is None:
        raise AssertionError("transparent Deviator frame")
    return box


def max_centered_factor(frame: Image.Image, margin: int = 1) -> float:
    left, top, right, bottom = alpha_box(frame)
    center = frame.width / 2.0
    limits: list[float] = []
    if left < center:
        limits.append((center - margin) / (center - left))
    if right > center:
        limits.append((frame.width - margin - center) / (right - center))
    if top < center:
        limits.append((center - margin) / (center - top))
    if bottom > center:
        limits.append((frame.height - margin - center) / (bottom - center))
    return min(limits) if limits else 1.0


def scale_centered(frame: Image.Image, factor: float) -> Image.Image:
    new_size = (
        max(1, round(frame.width * factor)),
        max(1, round(frame.height * factor)),
    )
    resized = resize_premultiplied(frame.convert("RGBA"), new_size)
    result = Image.new("RGBA", frame.size, (0, 0, 0, 0))
    destination = (
        (frame.width - resized.width) // 2,
        (frame.height - resized.height) // 2,
    )
    source_left = max(0, -destination[0])
    source_top = max(0, -destination[1])
    source_right = min(resized.width, frame.width - destination[0])
    source_bottom = min(resized.height, frame.height - destination[1])
    result.alpha_composite(
        resized.crop((source_left, source_top, source_right, source_bottom)),
        (max(0, destination[0]), max(0, destination[1])),
    )
    return result


def normalize_frames(
    classic_frames: list[Image.Image],
    base_frames: list[Image.Image],
    mask_frames: list[Image.Image],
) -> tuple[list[Image.Image], list[Image.Image], list[float], list[int]]:
    classic_areas = [alpha_area(frame, 0) for frame in classic_frames]
    classic_median = float(np.median(classic_areas))
    targets = [
        TARGET_MEDIAN_AREA * classic_area / classic_median
        for classic_area in classic_areas
    ]
    normalized: list[Image.Image] = []
    normalized_masks: list[Image.Image] = []
    factors: list[float] = []
    for base, mask, target in zip(base_frames, mask_frames, targets, strict=True):
        current_area = alpha_area(base)
        factor = (target / current_area) ** 0.5
        factor = min(factor, max_centered_factor(base))
        normalized.append(scale_centered(base, factor))
        normalized_masks.append(scale_centered(mask, factor))
        factors.append(factor)
    return normalized, normalized_masks, factors, classic_areas


def make_atlas(frames: list[Image.Image]) -> Image.Image:
    atlas = Image.new(
        "RGBA", (frames[0].width * len(frames), frames[0].height), (0, 0, 0, 0)
    )
    for index, frame in enumerate(frames):
        atlas.alpha_composite(frame, (index * frame.width, 0))
    return atlas


def downsample_atlas(atlas4: Image.Image) -> Image.Image:
    frames4 = crop_frames(atlas4, 4)
    frames2 = [
        resize_premultiplied(frame, (FRAME_LOGICAL * 2, FRAME_LOGICAL * 2))
        for frame in frames4
    ]
    return make_atlas(frames2)


def patch_pack(source: Path, target: Path, base: Image.Image, mask: Image.Image) -> dict[str, object]:
    before = read_pack(source)
    after = list(before)
    if before[DEVIATOR_ID].name != "UNIT_DEVIATOR":
        raise AssertionError("resource 134 is not UNIT_DEVIATOR")
    mask_ids = [entry.index for entry in before if entry.name == DEVIATOR_MASK]
    if len(mask_ids) != 1:
        raise AssertionError(f"expected exactly one {DEVIATOR_MASK}")
    mask_id = mask_ids[0]
    changed = {DEVIATOR_ID, mask_id}
    after[DEVIATOR_ID] = PackEntry(
        DEVIATOR_ID, "UNIT_DEVIATOR", "PNG", encode_png(base)
    )
    after[mask_id] = PackEntry(mask_id, DEVIATOR_MASK, "PNG", encode_png(mask))
    target.parent.mkdir(parents=True, exist_ok=True)
    write_pack(target, after)
    packed = read_pack(target)
    for entry in before:
        if entry.index in changed:
            continue
        current = packed[entry.index]
        if (
            current.name != entry.name
            or current.extension != entry.extension
            or current.payload != entry.payload
        ):
            raise AssertionError(
                f"unrelated resource changed: {entry.index}:{entry.name}"
            )
    return {
        "path": str(target),
        "sha256": sha256(target),
        "changed_ids": sorted(changed),
        "entries": len(packed),
    }


def review_sheet(before: list[Image.Image], after: list[Image.Image]) -> Image.Image:
    cell = HD4_FRAME
    label_height = 22
    sheet = Image.new("RGB", (cell * 8, (cell + label_height) * 2), "#15191d")
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    for row, frames in enumerate((before, after)):
        title = "BEFORE" if row == 0 else "AFTER"
        y = row * (cell + label_height)
        for index, frame in enumerate(frames):
            x = index * cell
            checker = Image.new("RGBA", (cell, cell), "#282d32")
            checker.alpha_composite(frame)
            sheet.paste(checker.convert("RGB"), (x, y))
            draw.rectangle((x, y, x + cell - 1, y + cell - 1), outline="#8b6d25")
            draw.text((x + 4, y + cell + 4), f"{title} {DIRECTIONS[index]}", fill="#ead59a", font=font)
    return sheet


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    classic_entries = read_pack(DATA / "sdl_data.dat")
    source4 = DATA / "sdl_data_hd4.dat"
    source2 = DATA / "sdl_data_hd2.dat"
    entries4 = read_pack(source4)
    classic = decode_image(classic_entries[DEVIATOR_ID].payload)
    base4 = decode_image(entries4[DEVIATOR_ID].payload)
    mask_entry = next(entry for entry in entries4 if entry.name == DEVIATOR_MASK)
    mask4 = decode_image(mask_entry.payload)
    if classic is None or base4 is None or mask4 is None:
        raise AssertionError("cannot decode Deviator resources")

    classic_frames = crop_frames(classic.convert("RGBA"), 1)
    before_frames = crop_frames(base4.convert("RGBA"), 4)
    mask_frames = crop_frames(mask4.convert("RGBA"), 4)
    after_frames, after_masks, factors, classic_areas = normalize_frames(
        classic_frames, before_frames, mask_frames
    )
    corrected4 = make_atlas(after_frames)
    corrected_mask4 = make_atlas(after_masks)
    corrected2 = downsample_atlas(corrected4)
    corrected_mask2 = downsample_atlas(corrected_mask4)

    before_areas = [alpha_area(frame) for frame in before_frames]
    after_areas = [alpha_area(frame) for frame in after_frames]
    classic_ratio = max(classic_areas) / min(classic_areas)
    after_ratio = max(after_areas) / min(after_areas)
    if after_ratio > classic_ratio + 0.15:
        raise AssertionError(
            f"apparent size remains inconsistent: {after_ratio:.4f}"
        )
    for direction, frame in zip(DIRECTIONS, after_frames, strict=True):
        left, top, right, bottom = alpha_box(frame)
        if left < 1 or top < 1 or right > HD4_FRAME - 1 or bottom > HD4_FRAME - 1:
            raise AssertionError(f"{direction} frame clips at {left, top, right, bottom}")

    backup = OUT / "backup_repo"
    backup.mkdir(exist_ok=True)
    for source in (source2, source4):
        destination = backup / f"{source.stem}_{sha256(source)[:12]}{source.suffix}"
        if not destination.exists():
            shutil.copy2(source, destination)

    stage = OUT / "data"
    builds = [
        patch_pack(source2, stage / source2.name, corrected2, corrected_mask2),
        patch_pack(source4, stage / source4.name, corrected4, corrected_mask4),
    ]
    corrected4.save(OUT / "UNIT_DEVIATOR_HD4.png", optimize=True)
    corrected_mask4.save(OUT / "HM_UNIT_DEVIATOR_HD4.png", optimize=True)
    review_sheet(before_frames, after_frames).save(
        OUT / "UNIT_DEVIATOR_SCALE_REVIEW.png", optimize=True
    )

    report = {
        "directions": list(DIRECTIONS),
        "classic_areas": classic_areas,
        "before_areas": before_areas,
        "after_areas": after_areas,
        "scale_factors": [round(value, 5) for value in factors],
        "classic_area_ratio": round(classic_ratio, 5),
        "before_area_ratio": round(max(before_areas) / min(before_areas), 5),
        "after_area_ratio": round(after_ratio, 5),
        "builds": builds,
    }
    (OUT / "manifest.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
