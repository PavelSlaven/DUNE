#!/usr/bin/env python3
"""Build the true-HD post-House-selection Bene Gesserit screen."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps

from hd_assets import PackEntry, decode_image, encode_png, read_pack, write_pack


ROOT = Path(__file__).resolve().parents[1]
GAME = Path(r"C:\Users\Slaven\Desktop\D2TM-v0.8.0.windows.ru")
ARTIFACT = ROOT / "artifacts" / "mentat_hd_v1"
GENERATED = ARTIFACT / "generated"
OUTPUT = ARTIFACT / "data"
MASTER = ROOT / "resources" / "hd" / "master4"

BACKGROUND_ID = 39
EYE_IDS = range(10, 15)
MOUTH_IDS = range(15, 20)
SCENES = ("platr", "plhar", "plord")
BACKGROUND_SIZE = (2560, 1920)
SCENE_SIZE = (1472, 896)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replace(entries: list[PackEntry], index: int, image: Image.Image) -> None:
    old = entries[index]
    entries[index] = PackEntry(old.index, old.name, "PNG", encode_png(image))


def master_background() -> Image.Image:
    with Image.open(GENERATED / "bene_background.png") as source:
        image = ImageOps.fit(
            source.convert("RGB"),
            BACKGROUND_SIZE,
            Image.Resampling.LANCZOS,
        )
    return image.filter(ImageFilter.UnsharpMask(1.1, 82, 2)).convert("RGBA")


def feathered_feature_overlay(
    source: Image.Image,
    boxes: tuple[tuple[int, int, int, int], ...],
    strength: float,
    blur_radius: int,
) -> Image.Image:
    """Return a fixed-size overlay without opaque rectangular patch edges."""
    overlay = source.convert("RGBA")
    mask = Image.new("L", source.size, 0)
    draw = ImageDraw.Draw(mask)
    for box in boxes:
        draw.ellipse(box, fill=round(255 * strength))
    mask = mask.filter(ImageFilter.GaussianBlur(blur_radius))
    edge_fade = Image.new("L", source.size, 0)
    edge_draw = ImageDraw.Draw(edge_fade)
    inset = max(12, blur_radius * 2)
    edge_draw.rectangle(
        (inset, inset, source.width - inset - 1, source.height - inset - 1),
        fill=255,
    )
    edge_fade = edge_fade.filter(ImageFilter.GaussianBlur(max(4, blur_radius // 2)))
    mask = ImageChops.multiply(mask, edge_fade)
    # The texture may be linearly filtered at a fractional UI scale.  Keeping
    # the outermost texels fully transparent prevents texture-clamp seams.
    mask.paste(0, (0, 0, source.width, 2))
    mask.paste(0, (0, source.height - 2, source.width, source.height))
    mask.paste(0, (0, 0, 2, source.height))
    mask.paste(0, (source.width - 2, 0, source.width, source.height))
    overlay.putalpha(mask)
    return overlay


def make_face_frames(background: Image.Image) -> tuple[list[Image.Image], list[Image.Image]]:
    # ImageGen supplies one natural, registered facial-animation endpoint.  We
    # only take the eyelids and lips from it; the background and portrait stay
    # pixel-identical to the accepted master.  Feathered alpha is essential:
    # an opaque crop is sampled differently from the full background at
    # fractional UI scales and produces visible rectangular seams.
    with Image.open(GENERATED / "bene_face_endpoint.png") as source:
        endpoint = source.convert("RGBA").resize(BACKGROUND_SIZE, Image.Resampling.LANCZOS)

    eyes_box = (96 * 4, 180 * 4, (96 + 96) * 4, (180 + 32) * 4)
    eyes_endpoint = endpoint.crop(eyes_box)
    eye_regions = (
        (30, 20, 142, 116),
        (138, 18, 262, 116),
    )
    # Open frames are transparent because the accepted background already
    # contains the open-eyed pose.  Closed frames use the same registered
    # endpoint instead of resizing strips of the face.
    # Every non-open eyelid frame must be opaque over the iris.  Alpha-fading
    # the closed endpoint over the open-eyed background creates ghost eyes.
    eye_strengths = (0.0, 0.0, 1.0, 0.0, 1.0)
    eyes = [
        feathered_feature_overlay(eyes_endpoint, eye_regions, strength, 10)
        for strength in eye_strengths
    ]

    mouth_box = (100 * 4, 210 * 4, (100 + 112) * 4, (210 + 80) * 4)
    mouth_endpoint = endpoint.crop(mouth_box)
    mouth_region = ((62, 104, 218, 212),)
    mouth_strengths = (0.0, 0.42, 0.72, 1.0, 0.58)
    mouths = [
        feathered_feature_overlay(mouth_endpoint, mouth_region, strength, 12)
        for strength in mouth_strengths
    ]
    return eyes, mouths


def prepare_scene(source_path: Path) -> Image.Image:
    with Image.open(source_path) as source:
        image = ImageOps.fit(
            source.convert("RGB"),
            (SCENE_SIZE[0] + 36, SCENE_SIZE[1] + 24),
            Image.Resampling.LANCZOS,
        )
    return image.filter(ImageFilter.UnsharpMask(0.9, 72, 2))


def animate_scene(master: Image.Image) -> list[Image.Image]:
    frames: list[Image.Image] = []
    for index in range(33):
        phase = math.tau * index / 32.0
        x = 18 + int(round(math.sin(phase) * 12))
        y = 12 + int(round(math.cos(phase) * 6))
        frame = master.crop((x, y, x + SCENE_SIZE[0], y + SCENE_SIZE[1])).convert("RGBA")
        pulse = 1.0 + 0.025 * math.sin(phase * 2.0)
        frame = ImageEnhance.Brightness(frame).enhance(pulse)
        overlay = Image.new("RGBA", SCENE_SIZE, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay, "RGBA")
        scan_x = int((index / 32.0) * (SCENE_SIZE[0] + 120)) - 60
        draw.rectangle((scan_x - 12, 0, scan_x + 12, SCENE_SIZE[1]), fill=(120, 220, 255, 12))
        for scan_y in range((index * 7) % 24, SCENE_SIZE[1], 24):
            draw.line((0, scan_y, SCENE_SIZE[0], scan_y), fill=(110, 210, 255, 9), width=2)
        frame = Image.alpha_composite(frame, overlay)
        frames.append(frame)
    return frames


def patch_mentat(background: Image.Image, eyes: list[Image.Image], mouths: list[Image.Image], density: int) -> Path:
    base = GAME / "data" / f"sdl_mentat_hd{density}.dat"
    entries = read_pack(base)
    output_entries = list(entries)
    factor = density / 4

    def scaled(image: Image.Image) -> Image.Image:
        if density == 4:
            return image.copy()
        return image.resize(
            (round(image.width * factor), round(image.height * factor)),
            Image.Resampling.LANCZOS,
        )

    replace(output_entries, BACKGROUND_ID, scaled(background))
    for resource_id, image in zip(EYE_IDS, eyes, strict=True):
        replace(output_entries, resource_id, scaled(image))
    for resource_id, image in zip(MOUTH_IDS, mouths, strict=True):
        replace(output_entries, resource_id, scaled(image))

    output = OUTPUT / f"sdl_mentat_hd{density}.dat"
    write_pack(output, output_entries)
    changed = [
        i for i, (old, new) in enumerate(zip(entries, output_entries, strict=True))
        if old.payload != new.payload
    ]
    allowed_changes = {*EYE_IDS, *MOUTH_IDS, BACKGROUND_ID}
    if not changed or not set(changed).issubset(allowed_changes):
        raise AssertionError(f"unexpected mentat changes: {changed}")
    return output


def patch_scene(name: str, frames: list[Image.Image], density: int) -> Path:
    base = GAME / "data" / "scenes" / f"hd{density}" / f"sdl_{name}.dat"
    entries = read_pack(base)
    if len(entries) != len(frames):
        raise AssertionError(f"{name}: {len(entries)} entries, {len(frames)} frames")
    output_entries: list[PackEntry] = []
    for old, frame in zip(entries, frames, strict=True):
        image = frame if density == 4 else frame.resize(
            (SCENE_SIZE[0] // 2, SCENE_SIZE[1] // 2),
            Image.Resampling.LANCZOS,
        )
        output_entries.append(PackEntry(old.index, old.name, "PNG", encode_png(image)))
    output = OUTPUT / "scenes" / f"hd{density}" / f"sdl_{name}.dat"
    write_pack(output, output_entries)
    return output


def save_masters(background: Image.Image, eyes: list[Image.Image], mouths: list[Image.Image], scenes: dict[str, list[Image.Image]]) -> None:
    mentat_dir = MASTER / "sdl_mentat"
    mentat_dir.mkdir(parents=True, exist_ok=True)
    background.save(mentat_dir / "0039_MENTATM.png", optimize=True)
    for resource_id, image in zip(EYE_IDS, eyes, strict=True):
        image.save(mentat_dir / f"{resource_id:04d}_BEN_EYES{resource_id - 9:02d}.png", optimize=True)
    for resource_id, image in zip(MOUTH_IDS, mouths, strict=True):
        image.save(mentat_dir / f"{resource_id:04d}_BEN_MOUTH{resource_id - 14:02d}.png", optimize=True)
    for name, frames in scenes.items():
        pack = read_pack(GAME / "data" / "scenes" / "hd4" / f"sdl_{name}.dat")
        directory = MASTER / "scenes" / f"sdl_{name}"
        directory.mkdir(parents=True, exist_ok=True)
        for entry, frame in zip(pack, frames, strict=True):
            frame.save(directory / f"{entry.index:04d}_{entry.name}.png", optimize=True)


def review(background: Image.Image, first_frames: dict[str, Image.Image]) -> None:
    logical = (1920, 1080)
    scale = min(logical[0] * 0.9 / 640, logical[1] * 0.9 / 480, 2.25)
    panel_size = (round(640 * scale), round(480 * scale))
    panel = background.resize(panel_size, Image.Resampling.LANCZOS).convert("RGB")
    movie = first_frames["platr"].resize((round(385 * scale), round(210 * scale)), Image.Resampling.LANCZOS)
    panel.paste(movie.convert("RGB"), (round(205 * scale), round(105 * scale)))
    draw = ImageDraw.Draw(panel)
    font_path = ROOT / "resources" / "bin" / "data" / "RussoOne-Regular.ttf"
    title_font = ImageFont.truetype(str(font_path), 30)
    button_font = ImageFont.truetype(str(font_path), 30)

    def centered_text(value: str, center_y: int) -> None:
        bbox = draw.textbbox((0, 0), value, font=title_font, stroke_width=1)
        width = bbox[2] - bbox[0]
        height = bbox[3] - bbox[1]
        draw.text(
            ((panel.width - width) // 2, center_y - height // 2 - bbox[1]),
            value,
            font=title_font,
            fill=(255, 226, 165),
            stroke_width=2,
            stroke_fill=(0, 0, 0),
        )

    centered_text("Дом Атрейдес чтит долг, верность и справедливость.", 38)
    centered_text("Вы желаете вступить в Дом Атрейдес?", 80)
    for label, x in (("НЕТ", 293), ("ДА", 466)):
        rect = (round(x * scale), round(423 * scale), round((x + 154) * scale), round((423 + 46) * scale))
        draw.rounded_rectangle(rect, radius=9, fill=(28, 31, 38), outline=(186, 139, 55), width=3)
        bbox = draw.textbbox((0, 0), label, font=button_font)
        draw.text(((rect[0] + rect[2] - bbox[2]) // 2, (rect[1] + rect[3] - bbox[3]) // 2 - 2), label, font=button_font, fill=(255, 226, 165))
    canvas = Image.new("RGB", logical, (7, 7, 15))
    canvas.paste(panel, ((logical[0] - panel_size[0]) // 2, (logical[1] - panel_size[1]) // 2))
    canvas.save(ARTIFACT / "mentat_hd_review_1920x1080.png", optimize=True)


def main() -> int:
    ARTIFACT.mkdir(parents=True, exist_ok=True)
    background = master_background()
    eyes, mouths = make_face_frames(background)
    scenes = {
        name: animate_scene(prepare_scene(GENERATED / f"{name}.png"))
        for name in SCENES
    }
    save_masters(background, eyes, mouths, scenes)
    outputs = [patch_mentat(background, eyes, mouths, density) for density in (2, 4)]
    for density in (2, 4):
        outputs.extend(patch_scene(name, scenes[name], density) for name in SCENES)
    review(background, {name: frames[0] for name, frames in scenes.items()})
    manifest = {
        "format": 1,
        "status": "built_not_installed",
        "generated": {name: str(GENERATED / f"{name}.png") for name in ("bene_background", *SCENES)},
        "mentat_changed_ids": [*EYE_IDS, *MOUTH_IDS, BACKGROUND_ID],
        "scene_frames": 33,
        "outputs": [{"path": str(path), "sha256": digest(path), "bytes": path.stat().st_size} for path in outputs],
    }
    (ARTIFACT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
