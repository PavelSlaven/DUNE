#!/usr/bin/env python3
"""Build stable true-HD campaign mentat and briefing scene packs."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter, ImageOps

from hd_assets import PackEntry, decode_image, encode_png, read_pack, write_pack


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_GAME = Path(r"C:\Users\Slaven\Desktop\D2TM-v0.8.0.windows.ru")
ARTIFACT = ROOT / "artifacts" / "campaign_hd_v1"
SOURCE = ARTIFACT / "source"
GENERATED = ARTIFACT / "generated"
OUTPUT = ARTIFACT / "data"
MASTER = ROOT / "resources" / "hd" / "master4"

BACKGROUND_SIZE = (2560, 1920)
SCENE_SIZE = (1472, 896)
SCENES = (
    "harvest", "headqrts", "hitcftry", "hvyftry", "ix", "liteftry",
    "lose01", "lose02", "ltank", "palace", "platr", "plhar", "plord",
    "quad", "repair", "sardukar", "win01", "win02",
)
ANIMATED_SCENES = {"harvest", "headqrts", "hvyftry", "liteftry"}
HOLOGRAM_SCENES = {"platr", "plhar", "plord"}

MENTATS = {
    "atreides": {
        "background": 37, "eyes": range(0, 5), "mouths": range(5, 10),
        "eye_origin": (96, 180), "mouth_origin": (100, 210),
        # Tight feature masks are intentional: the facial endpoint is an
        # independently rendered frame.  Wide masks also replaced eyebrows,
        # nose and cheeks, making the portrait visibly jump during animation.
        "eye_regions": ((54, 0, 190, 66), (202, 0, 338, 66)),
        "mouth_region": ((92, 62, 262, 158),),
        # The independently rendered speaking endpoint has its lip line about
        # 2.5 logical pixels lower than the resting portrait.  Register the
        # feature to the face instead of moving its runtime draw rectangle.
        "mouth_shift": (0, -2),
    },
    "harkonnen": {
        "background": 38, "eyes": range(24, 29), "mouths": range(29, 34),
        "eye_origin": (96, 180), "mouth_origin": (100, 210),
    },
    "ordos": {
        "background": 40, "eyes": range(41, 46), "mouths": range(46, 51),
        "eye_origin": (48, 174), "mouth_origin": (52, 207),
    },
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replace(entries: list[PackEntry], index: int, image: Image.Image) -> None:
    old = entries[index]
    entries[index] = PackEntry(old.index, old.name, "PNG", encode_png(image))


def fit_master(path: Path, size: tuple[int, int]) -> Image.Image:
    with Image.open(path) as source:
        image = ImageOps.fit(source.convert("RGB"), size, Image.Resampling.LANCZOS)
    return image.filter(ImageFilter.UnsharpMask(1.0, 76, 2)).convert("RGBA")


def extract_references(game: Path) -> None:
    scene_dir = SOURCE / "scenes"
    scene_dir.mkdir(parents=True, exist_ok=True)
    for name in SCENES:
        entries = read_pack(game / "data" / "scenes" / f"sdl_{name}.dat")
        frames = [decode_image(entry.payload).convert("RGBA") for entry in entries]
        key_index = len(frames) // 2 if name in ANIMATED_SCENES else 0
        frames[key_index].save(scene_dir / f"{name}.png", optimize=True)

        if len(frames) > 1:
            width, height = frames[0].size
            sheet = Image.new("RGBA", (width * 3, height), (0, 0, 0, 255))
            for column, index in enumerate((0, key_index, len(frames) - 1)):
                sheet.alpha_composite(frames[index], (column * width, 0))
            sheet.save(scene_dir / f"{name}_motion_reference.png", optimize=True)

    mentat_dir = SOURCE / "mentats"
    mentat_dir.mkdir(parents=True, exist_ok=True)
    # Always anchor regenerated portraits and facial overlays to the original
    # campaign art. Reading the already-remastered pack here made an incorrect
    # generated portrait self-perpetuating on every subsequent rebuild.
    entries = read_pack(game / "data" / "sdl_mentat.dat")
    for name, ids in MENTATS.items():
        decode_image(entries[ids["background"]].payload).convert("RGBA").save(
            mentat_dir / f"{name}.png", optimize=True
        )


def feathered_feature_overlay(
    source: Image.Image,
    ellipses: tuple[tuple[int, int, int, int], ...],
    strength: float,
    blur_radius: int,
) -> Image.Image:
    overlay = source.convert("RGBA")
    mask = Image.new("L", source.size, 0)
    draw = ImageDraw.Draw(mask)
    for ellipse in ellipses:
        draw.ellipse(ellipse, fill=round(255 * strength))
    mask = mask.filter(ImageFilter.GaussianBlur(blur_radius))
    mask.paste(0, (0, 0, source.width, 2))
    mask.paste(0, (0, source.height - 2, source.width, source.height))
    mask.paste(0, (0, 0, 2, source.height))
    mask.paste(0, (source.width - 2, 0, source.width, source.height))
    overlay.putalpha(mask)
    return overlay


def make_face_frames(
    endpoint_path: Path,
    eye_origin: tuple[int, int],
    mouth_origin: tuple[int, int],
    eye_regions: tuple[tuple[int, int, int, int], ...] | None = None,
    mouth_region: tuple[tuple[int, int, int, int], ...] | None = None,
    mouth_shift: tuple[int, int] = (0, 0),
) -> tuple[list[Image.Image], list[Image.Image]]:
    endpoint = fit_master(endpoint_path, BACKGROUND_SIZE)
    eye_x, eye_y = eye_origin
    eyes_endpoint = endpoint.crop((eye_x * 4, eye_y * 4, (eye_x + 96) * 4, (eye_y + 32) * 4))
    eye_regions = eye_regions or ((30, 20, 142, 116), (138, 18, 262, 116))
    # Closed eyelids are fully opaque over the irises.  Partial alpha causes
    # the open eyes in the background to shine through during a blink.
    eyes = [
        feathered_feature_overlay(eyes_endpoint, eye_regions, strength, 10)
        for strength in (0.0, 0.0, 1.0, 0.0, 1.0)
    ]

    mouth_x, mouth_y = mouth_origin
    shift_x, shift_y = mouth_shift
    source_x = (mouth_x - shift_x) * 4
    source_y = (mouth_y - shift_y) * 4
    mouth_endpoint = endpoint.crop(
        (source_x, source_y, source_x + 112 * 4, source_y + 80 * 4)
    )
    mouth_region = mouth_region or ((62, 104, 218, 212),)
    mouths = [
        feathered_feature_overlay(mouth_endpoint, mouth_region, strength, 12)
        for strength in (0.0, 0.42, 0.72, 1.0, 0.58)
    ]
    return eyes, mouths


def classic_scene_frames(game: Path, name: str) -> list[Image.Image]:
    entries = read_pack(game / "data" / "scenes" / f"sdl_{name}.dat")
    return [decode_image(entry.payload).convert("RGBA") for entry in entries]


def animation_delta_mask(first: Image.Image, current: Image.Image) -> Image.Image:
    difference = ImageChops.difference(first.convert("RGB"), current.convert("RGB")).convert("L")
    difference = difference.point(lambda value: 0 if value < 20 else min(255, (value - 20) * 3))
    return difference.resize(SCENE_SIZE, Image.Resampling.BICUBIC).filter(ImageFilter.GaussianBlur(5))


def build_scene_frames(game: Path, name: str, master: Image.Image) -> list[Image.Image]:
    classic = classic_scene_frames(game, name)
    frames: list[Image.Image] = []
    for index, classic_frame in enumerate(classic):
        frame = master.copy()
        if len(classic) > 1:
            phase = math.tau * index / len(classic)
            mask = animation_delta_mask(classic[0], classic_frame)
            glow = Image.new("RGBA", SCENE_SIZE, (112, 224, 255, 0))
            glow.putalpha(mask.point(lambda value: value * 92 // 255))
            frame = Image.alpha_composite(frame, glow)
            # A restrained luminance pulse makes machinery visibly active while
            # keeping every frame registered to the same geometry.
            frame = ImageEnhance.Brightness(frame).enhance(1.0 + 0.012 * math.sin(phase))

        if name in HOLOGRAM_SCENES:
            overlay = Image.new("RGBA", SCENE_SIZE, (0, 0, 0, 0))
            draw = ImageDraw.Draw(overlay, "RGBA")
            scan_x = int((index / max(1, len(classic) - 1)) * (SCENE_SIZE[0] + 80)) - 40
            draw.rectangle((scan_x - 8, 0, scan_x + 8, SCENE_SIZE[1]), fill=(90, 210, 255, 18))
            for y in range((index * 5) % 20, SCENE_SIZE[1], 20):
                draw.line((0, y, SCENE_SIZE[0], y), fill=(90, 180, 255, 10), width=2)
            frame = Image.alpha_composite(frame, overlay)
        frames.append(frame)
    return frames


def patch_scenes(game: Path) -> list[Path]:
    outputs: list[Path] = []
    scene_master_dir = MASTER / "scenes"
    for name in SCENES:
        master = fit_master(GENERATED / f"{name}.png", SCENE_SIZE)
        frames = build_scene_frames(game, name, master)
        master_dir = scene_master_dir / f"sdl_{name}"
        master_dir.mkdir(parents=True, exist_ok=True)

        for density in (2, 4):
            base = game / "data" / "scenes" / f"hd{density}" / f"sdl_{name}.dat"
            entries = read_pack(base)
            if len(entries) != len(frames):
                raise AssertionError(f"{name}: expected {len(entries)} frames, built {len(frames)}")
            output_entries: list[PackEntry] = []
            for entry, frame in zip(entries, frames, strict=True):
                image = frame if density == 4 else frame.resize(
                    (SCENE_SIZE[0] // 2, SCENE_SIZE[1] // 2), Image.Resampling.LANCZOS
                )
                output_entries.append(PackEntry(entry.index, entry.name, "PNG", encode_png(image)))
                if density == 4:
                    frame.save(master_dir / f"{entry.index:04d}_{entry.name}.png", optimize=True)
            output = OUTPUT / "scenes" / f"hd{density}" / f"sdl_{name}.dat"
            write_pack(output, output_entries)
            outputs.append(output)
    return outputs


def patch_mentats(game: Path) -> list[Path]:
    fixed_pack = ROOT / "artifacts" / "mentat_hd_v1" / "data"
    outputs: list[Path] = []
    for density in (2, 4):
        preferred = fixed_pack / f"sdl_mentat_hd{density}.dat"
        base = preferred if preferred.exists() else game / "data" / f"sdl_mentat_hd{density}.dat"
        entries = read_pack(base)
        output_entries = list(entries)
        factor = density / 4

        for name, ids in MENTATS.items():
            background = fit_master(GENERATED / f"mentat_{name}.png", BACKGROUND_SIZE)
            eyes, mouths = make_face_frames(
                GENERATED / f"mentat_{name}_face_endpoint.png",
                ids["eye_origin"],
                ids["mouth_origin"],
                ids.get("eye_regions"),
                ids.get("mouth_region"),
                ids.get("mouth_shift", (0, 0)),
            )

            def scaled(image: Image.Image) -> Image.Image:
                if density == 4:
                    return image.copy()
                return image.resize(
                    (round(image.width * factor), round(image.height * factor)),
                    Image.Resampling.LANCZOS,
                )

            replace(output_entries, ids["background"], scaled(background))
            for resource_id, image in zip(ids["eyes"], eyes, strict=True):
                replace(output_entries, resource_id, scaled(image))
            for resource_id, image in zip(ids["mouths"], mouths, strict=True):
                replace(output_entries, resource_id, scaled(image))

            if density == 4:
                directory = MASTER / "sdl_mentat"
                directory.mkdir(parents=True, exist_ok=True)
                background.save(directory / f"{ids['background']:04d}_MENTAT_{name.upper()}.png", optimize=True)

        output = OUTPUT / f"sdl_mentat_hd{density}.dat"
        write_pack(output, output_entries)
        outputs.append(output)
    return outputs


def validate(game: Path, outputs: list[Path]) -> dict[str, object]:
    report: dict[str, object] = {"status": "PASS", "files": []}
    for path in outputs:
        entries = read_pack(path)
        file_info: dict[str, object] = {
            "path": str(path),
            "sha256": digest(path),
            "entries": len(entries),
        }
        if "scenes" in path.parts:
            density = 4 if "hd4" in path.parts else 2
            expected = (SCENE_SIZE[0] * density // 4, SCENE_SIZE[1] * density // 4)
            sizes = {decode_image(entry.payload).size for entry in entries}
            if sizes != {expected}:
                raise AssertionError(f"{path.name}: unexpected sizes {sizes}, expected {expected}")
            file_info["size"] = list(expected)
        report["files"].append(file_info)
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--game", type=Path, default=DEFAULT_GAME)
    parser.add_argument("--extract", action="store_true")
    args = parser.parse_args()

    SOURCE.mkdir(parents=True, exist_ok=True)
    GENERATED.mkdir(parents=True, exist_ok=True)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    if args.extract:
        extract_references(args.game)
        return 0

    missing = [
        GENERATED / f"{name}.png" for name in SCENES
        if not (GENERATED / f"{name}.png").exists()
    ]
    for name in MENTATS:
        for suffix in ("", "_face_endpoint"):
            path = GENERATED / f"mentat_{name}{suffix}.png"
            if not path.exists():
                missing.append(path)
    if missing:
        raise FileNotFoundError("Missing generated masters:\n" + "\n".join(map(str, missing)))

    outputs = patch_mentats(args.game) + patch_scenes(args.game)
    report = validate(args.game, outputs)
    report_path = ARTIFACT / "campaign_hd_build_report.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"PASS: wrote {len(outputs)} packs; report={report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
