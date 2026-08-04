#!/usr/bin/env python3
"""Build and install the remaining HD world effects without changing gameplay geometry."""

from __future__ import annotations

import hashlib
import json
import math
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageChops, ImageEnhance, ImageFilter, ImageOps, ImageStat

from hd_assets import PackEntry, decode_image, encode_png, read_pack, write_pack


ROOT = Path(__file__).resolve().parents[1]
GAME = Path("C:/Users/Slaven/Desktop/D2TM-v0.8.0.windows.ru")
CLASSIC = ROOT / "resources" / "hd" / "classic" / "sdl_data"
MASTER4 = ROOT / "resources" / "hd" / "master4" / "sdl_data"
SOURCE = ROOT / "resources" / "hd" / "source_references" / "effects_remaster"
OUTPUT = ROOT / "artifacts" / "effects_remaster_v1"
OUTPUT_DATA = OUTPUT / "data"
BACKUP = OUTPUT / "backup_before_install"


@dataclass(frozen=True)
class Spec:
    index: int
    frame_width: int
    frame_height: int
    columns: int
    rows: int
    builder: str


# The dimensions below come from cIniGameRessouces and the original atlases.
# Carry-puff intentionally retains the unused 64-pixel tail in its 96x640 atlas.
SPECS = (
    Spec(0, 32, 32, 10, 1, "indicator_attack"),
    Spec(46, 16, 16, 1, 1, "bullet_large"),
    Spec(47, 8, 8, 1, 1, "bullet_medium"),
    Spec(48, 6, 6, 1, 1, "bullet_small"),
    Spec(49, 18, 18, 8, 1, "puff"),
    Spec(51, 32, 32, 16, 2, "rocket_normal"),
    Spec(52, 16, 16, 16, 2, "rocket_small"),
    Spec(64, 32, 32, 3, 1, "impact_sequence"),
    Spec(65, 32, 32, 3, 1, "fire_sequence"),
    Spec(66, 48, 48, 5, 1, "gas_sequence"),
    Spec(67, 32, 32, 1, 1, "orni_debris"),
    Spec(69, 32, 32, 5, 1, "small_explosion"),
    Spec(70, 32, 32, 1, 1, "blood_small"),
    Spec(71, 32, 32, 1, 1, "blood_medium"),
    Spec(72, 32, 32, 1, 1, "blood_large"),
    Spec(73, 48, 48, 5, 1, "structure_a"),
    Spec(74, 48, 48, 5, 1, "structure_b"),
    Spec(75, 48, 48, 5, 1, "vehicle_a"),
    Spec(76, 48, 48, 5, 1, "vehicle_b"),
    Spec(77, 48, 48, 2, 1, "trike_sequence"),
    Spec(78, 32, 32, 1, 1, "focus"),
    Spec(90, 32, 32, 10, 1, "indicator_move"),
    Spec(91, 512, 512, 1, 1, "boom"),
    Spec(92, 256, 256, 1, 1, "boom"),
    Spec(93, 128, 128, 1, 1, "boom"),
    Spec(94, 64, 64, 1, 1, "boom"),
    Spec(95, 96, 96, 1, 6, "carry_puff"),
    Spec(96, 32, 32, 1, 1, "classic_detail"),
    Spec(97, 32, 32, 1, 1, "classic_detail"),
    Spec(98, 32, 32, 3, 1, "siege_die"),
    Spec(99, 64, 64, 8, 1, "muzzle_directions"),
    Spec(100, 32, 48, 3, 1, "smoke_sequence"),
    Spec(101, 36, 38, 3, 1, "smoke_shadow"),
    Spec(102, 9, 9, 1, 1, "star"),
    Spec(103, 9, 9, 1, 1, "star"),
    Spec(104, 9, 9, 1, 1, "star"),
    Spec(106, 48, 48, 5, 1, "worm_eat"),
    Spec(107, 48, 48, 5, 1, "worm_trail"),
    Spec(115, 32, 32, 10, 4, "smudges"),
    Spec(116, 10, 10, 1, 1, "pickup"),
    Spec(126, 32, 32, 1, 1, "track_dia"),
    Spec(127, 32, 32, 1, 1, "track_dia2"),
    Spec(128, 32, 32, 1, 1, "track_hor"),
    Spec(129, 32, 32, 1, 1, "track_ver"),
)

# These already have accepted, real HD4 masters and are validated with this set.
RETAINED_HD_IDS = (50, 68, 105, 112)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def classic_path(index: int) -> Path:
    return next(CLASSIC.glob(f"{index:04d}_*.png"))


def master_path(index: int) -> Path:
    return MASTER4 / classic_path(index).name


def black_to_alpha(image: Image.Image) -> Image.Image:
    rgba = image.convert("RGBA")
    result = []
    for red, green, blue, _alpha in rgba.getdata():
        peak = max(red, green, blue)
        alpha = max(0, min(255, round((peak - 3) * 1.42)))
        result.append((red, green, blue, alpha))
    rgba.putdata(result)
    rgba.putalpha(rgba.getchannel("A").filter(ImageFilter.GaussianBlur(0.35)))
    return rgba


def grid_subjects(path: Path, columns: int, rows: int) -> list[Image.Image]:
    source = Image.open(path).convert("RGBA")
    result = []
    for row in range(rows):
        for column in range(columns):
            box = (
                round(column * source.width / columns),
                round(row * source.height / rows),
                round((column + 1) * source.width / columns),
                round((row + 1) * source.height / rows),
            )
            result.append(crop_subject(black_to_alpha(source.crop(box))))
    return result


def crop_subject(image: Image.Image, threshold: int = 20) -> Image.Image:
    alpha = image.getchannel("A")
    bbox = alpha.point(lambda value: 255 if value > threshold else 0).getbbox()
    return image.crop(bbox) if bbox else Image.new("RGBA", (1, 1))


def foreground_bbox(image: Image.Image) -> tuple[int, int, int, int]:
    rgba = image.convert("RGBA")
    alpha = rgba.getchannel("A")
    if alpha.getextrema()[0] < 255:
        bbox = alpha.point(lambda value: 255 if value > 8 else 0).getbbox()
    else:
        luminance = rgba.convert("RGB").convert("L")
        bbox = luminance.point(lambda value: 255 if value > 10 else 0).getbbox()
    return bbox or (0, 0, image.width, image.height)


def classic_frames(spec: Spec) -> tuple[Image.Image, list[Image.Image]]:
    atlas = Image.open(classic_path(spec.index)).convert("RGBA")
    frames = []
    for row in range(spec.rows):
        for column in range(spec.columns):
            frames.append(
                atlas.crop(
                    (
                        column * spec.frame_width,
                        row * spec.frame_height,
                        (column + 1) * spec.frame_width,
                        (row + 1) * spec.frame_height,
                    )
                )
            )
    return atlas, frames


def place_like_classic(
    subject: Image.Image,
    classic_frame: Image.Image,
    density: int = 4,
    expansion: float = 1.05,
    opacity: float = 1.0,
) -> Image.Image:
    size = (classic_frame.width * density, classic_frame.height * density)
    left, top, right, bottom = foreground_bbox(classic_frame)
    center_x = (left + right) * density / 2
    center_y = (top + bottom) * density / 2
    target_width = max(density, round((right - left) * density * expansion))
    target_height = max(density, round((bottom - top) * density * expansion))
    cropped = crop_subject(subject)
    scale = min(target_width / cropped.width, target_height / cropped.height)
    resized = cropped.resize(
        (
            max(1, round(cropped.width * scale)),
            max(1, round(cropped.height * scale)),
        ),
        Image.Resampling.LANCZOS,
    )
    if opacity != 1.0:
        resized.putalpha(resized.getchannel("A").point(lambda value: round(value * opacity)))
    canvas = Image.new("RGBA", size)
    canvas.alpha_composite(
        resized,
        (round(center_x - resized.width / 2), round(center_y - resized.height / 2)),
    )
    return canvas


def detail_upscale(frame: Image.Image, density: int = 4) -> Image.Image:
    """Smooth the original pose, then restore restrained edge/material detail."""
    rgba = frame.convert("RGBA")
    target = (rgba.width * density, rgba.height * density)
    color = rgba.convert("RGB").resize(target, Image.Resampling.LANCZOS)
    color = color.filter(ImageFilter.UnsharpMask(radius=1.15, percent=90, threshold=3))
    alpha = rgba.getchannel("A").resize(target, Image.Resampling.LANCZOS)
    alpha = alpha.filter(ImageFilter.GaussianBlur(0.28))
    color.putalpha(alpha)
    return color


def compose_atlas(spec: Spec, frames: list[Image.Image], original: Image.Image) -> Image.Image:
    expected = spec.columns * spec.rows
    if len(frames) != expected:
        raise AssertionError(f"ID {spec.index}: {len(frames)} frames, expected {expected}")
    result = detail_upscale(original)
    for index, frame in enumerate(frames):
        if frame.size != (spec.frame_width * 4, spec.frame_height * 4):
            raise AssertionError(f"ID {spec.index} frame {index}: wrong size {frame.size}")
        x = (index % spec.columns) * spec.frame_width * 4
        y = (index // spec.columns) * spec.frame_height * 4
        result.paste(frame, (x, y), frame)
    return result


def tint(image: Image.Image, color: tuple[int, int, int], strength: float) -> Image.Image:
    rgba = image.convert("RGBA")
    gray = ImageOps.grayscale(rgba)
    colored = ImageOps.colorize(gray, (0, 0, 0), color).convert("RGBA")
    colored.putalpha(rgba.getchannel("A"))
    return Image.blend(rgba, colored, strength)


def rotate(subject: Image.Image, degrees: float) -> Image.Image:
    return subject.rotate(degrees, resample=Image.Resampling.BICUBIC, expand=True)


def build_frames(
    spec: Spec,
    old_frames: list[Image.Image],
    vfx: list[Image.Image],
    ground: list[Image.Image],
    explosion_phases: list[Image.Image],
    retained: dict[int, Image.Image],
) -> list[Image.Image]:
    builder = spec.builder

    if builder in {"indicator_attack", "indicator_move", "focus", "classic_detail"}:
        return [detail_upscale(frame) for frame in old_frames]

    if builder.startswith("bullet_"):
        subject = vfx[0 if builder != "bullet_large" else 1]
        return [place_like_classic(subject, old_frames[0], expansion=1.08)]

    if builder == "puff":
        result = []
        for index, old in enumerate(old_frames):
            subject = vfx[8] if index > 3 else vfx[11]
            result.append(place_like_classic(subject, old, expansion=0.9 + index * 0.045, opacity=1 - index * 0.065))
        return result

    if builder in {"rocket_normal", "rocket_small"}:
        large = retained[50]
        result = []
        # All three rocket atlases use 16 directions and two animation rows.
        for index, old in enumerate(old_frames):
            direction = index % 16
            animation = index // 16
            source = large.crop(
                (
                    direction * 192,
                    animation * 192,
                    (direction + 1) * 192,
                    (animation + 1) * 192,
                )
            )
            result.append(place_like_classic(source, old, expansion=1.0))
        return result

    if builder == "impact_sequence":
        refs = (vfx[0], vfx[1], vfx[4])
        return [place_like_classic(refs[i], old, expansion=1.05) for i, old in enumerate(old_frames)]

    if builder == "fire_sequence":
        return [
            place_like_classic(rotate(vfx[4], (-5, 4, 0)[i]), old, expansion=1.03, opacity=(0.9, 1.0, 0.82)[i])
            for i, old in enumerate(old_frames)
        ]

    if builder == "gas_sequence":
        return [place_like_classic(vfx[7], old, expansion=1.03, opacity=max(0.55, 1 - i * 0.08)) for i, old in enumerate(old_frames)]

    if builder == "orni_debris":
        return [place_like_classic(vfx[11], old_frames[0], expansion=1.06)]

    if builder in {"small_explosion", "structure_a", "structure_b", "vehicle_a", "vehicle_b"}:
        if builder.startswith("structure"):
            base = vfx[6]
        elif builder.startswith("vehicle"):
            base = vfx[5]
        else:
            base = vfx[4]
        result = []
        for index, old in enumerate(old_frames):
            # The old generated sheet's fifth cell contains a low-resolution
            # remnant. Finish large blasts with clean smoke instead.
            phase = vfx[8] if index == 4 else explosion_phases[min(index, 3)]
            mixed = Image.blend(
                place_like_classic(phase, old, expansion=1.02),
                place_like_classic(base, old, expansion=1.02),
                0.32 if index < 4 else 0.08,
            )
            if builder.endswith("b"):
                mixed = ImageOps.mirror(mixed)
            result.append(mixed)
        return result

    if builder == "trike_sequence":
        return [place_like_classic(explosion_phases[min(i + 1, 4)], old, expansion=1.04) for i, old in enumerate(old_frames)]

    if builder.startswith("blood_"):
        ref_index = {"blood_small": 0, "blood_medium": 1, "blood_large": 2}[builder]
        return [place_like_classic(ground[ref_index], old_frames[0], expansion=1.0)]

    if builder == "boom":
        subject = vfx[2]
        frame = old_frames[0]
        canvas = place_like_classic(subject, frame, expansion=1.14)
        # Preserve the classic white-yellow additive bloom.
        return [ImageEnhance.Brightness(tint(canvas, (255, 220, 118), 0.28)).enhance(1.16)]

    if builder == "carry_puff":
        result = []
        for index, old in enumerate(old_frames):
            subject = vfx[11] if index < 3 else vfx[8]
            result.append(place_like_classic(subject, old, expansion=0.72 + index * 0.07, opacity=1 - index * 0.09))
        return result

    if builder == "siege_die":
        return [place_like_classic(explosion_phases[min(i + 1, 4)], old, expansion=1.03) for i, old in enumerate(old_frames)]

    if builder == "muzzle_directions":
        result = []
        for index, old in enumerate(old_frames):
            result.append(place_like_classic(rotate(vfx[2], index * 45), old, expansion=1.0))
        return result

    if builder == "smoke_sequence":
        return [
            place_like_classic(
                vfx[8],
                old,
                expansion=0.94 + index * 0.05,
                opacity=1.0 - index * 0.09,
            )
            for index, old in enumerate(old_frames)
        ]

    if builder == "smoke_shadow":
        result = []
        for index, old in enumerate(old_frames):
            source = place_like_classic(vfx[8], old, expansion=0.92 + index * 0.04)
            alpha = source.getchannel("A")
            shadow = Image.new("RGBA", (144, 152), (18, 13, 10, 0))
            shadow.putalpha(alpha.point(lambda value: round(value * 0.42)).filter(ImageFilter.GaussianBlur(5.0)))
            result.append(place_like_classic(shadow, old, expansion=1.0))
        return result

    if builder in {"star", "pickup"}:
        size = spec.frame_width * 4, spec.frame_height * 4
        canvas = Image.new("RGBA", size)
        pixels = []
        cx, cy = (size[0] - 1) / 2, (size[1] - 1) / 2
        radius = max(1.0, min(size) * 0.47)
        for y in range(size[1]):
            for x in range(size[0]):
                dx, dy = abs(x - cx), abs(y - cy)
                radial = max(0.0, 1.0 - math.hypot(dx, dy) / radius)
                rays = max(0.0, 1.0 - min(dx, dy) / max(1.0, radius * 0.22)) * max(0.0, 1.0 - max(dx, dy) / radius)
                energy = max(radial ** 2.4, rays ** 3.0)
                pixels.append((255, 230, 112, round(255 * energy)))
        canvas.putdata(pixels)
        return [canvas]

    if builder == "worm_eat":
        return [place_like_classic(ground[4], old, expansion=1.02, opacity=max(0.65, 1 - i * 0.07)) for i, old in enumerate(old_frames)]

    if builder == "worm_trail":
        return [place_like_classic(ground[5], old, expansion=1.0, opacity=max(0.45, 1 - i * 0.1)) for i, old in enumerate(old_frames)]

    if builder == "smudges":
        result = []
        for index, old in enumerate(old_frames):
            row, column = divmod(index, spec.columns)
            subject = ground[3] if row != 1 else vfx[10]
            subject = rotate(subject, (column % 5) * 17 - 34)
            frame = place_like_classic(subject, old, expansion=0.94 + (column % 3) * 0.04, opacity=0.88)
            # Match each classic row: sand/rock/wall damage keeps its original hue family.
            stat = ImageStat.Stat(old.convert("RGB"), old.getchannel("A"))
            mean = tuple(max(24, min(220, round(value))) for value in stat.mean[:3])
            result.append(tint(frame, mean, 0.38))
        return result

    if builder.startswith("track_"):
        if builder in {"track_dia", "track_dia2"}:
            degrees = -45 if builder == "track_dia" else 45
            subject = rotate(ground[6], degrees)
        else:
            subject = ground[7]
            if builder == "track_ver":
                subject = rotate(subject, 90)
        return [place_like_classic(subject, old_frames[0], expansion=1.0, opacity=0.72)]

    raise AssertionError(f"unknown builder {builder}")


def replacement(entry: PackEntry, image: Image.Image) -> PackEntry:
    return PackEntry(entry.index, entry.name, "PNG", encode_png(image))


def validate_master(spec: Spec, classic_image: Image.Image, image: Image.Image) -> dict[str, object]:
    expected = (classic_image.width * 4, classic_image.height * 4)
    if image.size != expected:
        raise AssertionError(f"ID {spec.index}: {image.size}, expected {expected}")
    if image.mode != "RGBA":
        raise AssertionError(f"ID {spec.index}: expected RGBA, got {image.mode}")
    if image.getchannel("A").getbbox() is None:
        raise AssertionError(f"ID {spec.index}: empty alpha channel")
    return {
        "id": spec.index,
        "name": classic_path(spec.index).stem[5:],
        "classic_size": list(classic_image.size),
        "hd4_size": list(image.size),
        "frame_size": [spec.frame_width, spec.frame_height],
        "frames": spec.columns * spec.rows,
        "layout": [spec.columns, spec.rows],
        "builder": spec.builder,
    }


def patch_pack(base_path: Path, output_path: Path, images: dict[int, Image.Image], density: int) -> dict[str, object]:
    before = read_pack(base_path)
    entries = list(before)
    for index, master4 in images.items():
        expected_name = classic_path(index).stem[5:]
        if entries[index].name != expected_name:
            raise AssertionError(f"HD{density} ID {index}: {entries[index].name}, expected {expected_name}")
        image = master4 if density == 4 else master4.resize((master4.width // 2, master4.height // 2), Image.Resampling.LANCZOS)
        entries[index] = replacement(entries[index], image)
    write_pack(output_path, entries)
    after = read_pack(output_path)
    for old, new in zip(before, after, strict=True):
        if old.index in images:
            continue
        if (old.name, old.extension, old.payload) != (new.name, new.extension, new.payload):
            raise AssertionError(f"HD{density}: unrelated entry changed: {old.index}:{old.name}")
    return {
        "density": density,
        "base_sha256": sha256(base_path),
        "output_sha256": sha256(output_path),
        "entries": len(after),
        "changed_ids": sorted(images),
    }


def contact_sheet(images: dict[int, Image.Image]) -> None:
    thumbs = []
    for spec in SPECS:
        image = images[spec.index]
        frame = image.crop((0, 0, spec.frame_width * 4, spec.frame_height * 4))
        frame.thumbnail((180, 140), Image.Resampling.LANCZOS)
        card = Image.new("RGBA", (200, 180), (20, 22, 24, 255))
        card.alpha_composite(frame, ((200 - frame.width) // 2, 20 + (130 - frame.height) // 2))
        thumbs.append(card)
    sheet = Image.new("RGBA", (1000, math.ceil(len(thumbs) / 5) * 180), (10, 11, 12, 255))
    for index, thumb in enumerate(thumbs):
        sheet.alpha_composite(thumb, ((index % 5) * 200, (index // 5) * 180))
    sheet.save(OUTPUT / "effects_hd4_contact_sheet.png", optimize=True)


def main() -> int:
    vfx = grid_subjects(SOURCE / "vfx_reference_4x3.png", 4, 3)
    ground = grid_subjects(SOURCE / "ground_reference_4x2.png", 4, 2)
    explosion_phases = grid_subjects(
        ROOT / "resources" / "hd" / "generated" / "ru4_preview1" / "explosion_sheet.png",
        5,
        1,
    )
    retained = {index: Image.open(master_path(index)).convert("RGBA") for index in RETAINED_HD_IDS}

    OUTPUT.mkdir(parents=True, exist_ok=True)
    OUTPUT_DATA.mkdir(parents=True, exist_ok=True)
    BACKUP.mkdir(parents=True, exist_ok=True)
    MASTER4.mkdir(parents=True, exist_ok=True)

    images: dict[int, Image.Image] = {}
    manifest_entries = []
    for spec in SPECS:
        original, old_frames = classic_frames(spec)
        frames = build_frames(spec, old_frames, vfx, ground, explosion_phases, retained)
        atlas = compose_atlas(spec, frames, original)
        atlas.save(master_path(spec.index), optimize=True)
        images[spec.index] = atlas
        manifest_entries.append(validate_master(spec, original, atlas))

    # Validate retained masters too, so the released set covers every runtime VFX resource.
    for index in RETAINED_HD_IDS:
        classic_image = Image.open(classic_path(index))
        master = retained[index]
        if master.size != (classic_image.width * 4, classic_image.height * 4):
            raise AssertionError(f"retained ID {index}: wrong HD4 dimensions")

    for density in (2, 4):
        source = GAME / "data" / f"sdl_data_hd{density}.dat"
        if not source.is_file():
            raise FileNotFoundError(source)
        shutil.copy2(source, BACKUP / source.name)

    builds = []
    for density in (2, 4):
        builds.append(
            patch_pack(
                GAME / "data" / f"sdl_data_hd{density}.dat",
                OUTPUT_DATA / f"sdl_data_hd{density}.dat",
                images,
                density,
            )
        )

    # Verify HD2 is the deterministic Lanczos derivative of every HD4 replacement.
    hd2_entries = read_pack(OUTPUT_DATA / "sdl_data_hd2.dat")
    for index, master4 in images.items():
        expected = master4.resize((master4.width // 2, master4.height // 2), Image.Resampling.LANCZOS)
        actual = decode_image(hd2_entries[index].payload)
        if actual is None or ImageChops.difference(expected, actual.convert("RGBA")).getbbox():
            raise AssertionError(f"ID {index}: packed HD2 is not the HD4 derivative")

    contact_sheet(images)
    manifest = {
        "format": 1,
        "status": "built_not_installed",
        "source_sheets": [
            str(SOURCE / "vfx_reference_4x3.png"),
            str(SOURCE / "ground_reference_4x2.png"),
        ],
        "changed_resources": manifest_entries,
        "retained_approved_hd_resources": list(RETAINED_HD_IDS),
        "builds": builds,
        "backup": str(BACKUP),
    }
    (OUTPUT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"changed": len(images), "retained": len(RETAINED_HD_IDS), "output": str(OUTPUT)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, AssertionError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(1)
