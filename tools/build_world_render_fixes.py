#!/usr/bin/env python3
"""Build true-detail HD terrain and smooth shroud."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
GENERATED = ROOT / "resources" / "hd" / "generated" / "preview3" / "world_fixes"
CLASSIC = ROOT / "resources" / "hd" / "classic" / "sdl_data"
MASTER = ROOT / "resources" / "hd" / "master4" / "sdl_data"
EXTRA = ROOT / "resources" / "hd" / "master4_extra_packs" / "sdl_data"

TILE_SIZE = 128
EDGE_GUARD = 10
BEACON_FRAME = 72
BEACON_LOGICAL_FRAME = 18
BEACON_FRAMES = 8

MATERIAL_SOURCE = {
    "sand": GENERATED / "sand_source.png",
    "rock": GENERATED / "rock_source.png",
    "spice": GENERATED / "spice_source.png",
}
TERRAIN_MATERIAL = {
    118: "sand",
    119: "rock",
    120: "rock",
    121: "sand",
    123: "spice",
    124: "spice",
}
TERRAIN_VARIANTS = {
    118: "TERRAIN_HILL",
    119: "TERRAIN_MOUNTAIN",
    120: "TERRAIN_ROCK",
    121: "TERRAIN_SAND",
    123: "TERRAIN_SPICE",
    124: "TERRAIN_SPICEHILL",
}
HOUSE_COLORS = {
    "ATREIDES": (65, 119, 184),
    "HARKONNEN": (178, 54, 46),
    "ORDOS": (54, 145, 82),
}


def resource(folder: Path, resource_id: int) -> Path:
    return next(folder.glob(f"{resource_id:04d}_*.png"))


def master_path(resource_id: int) -> Path:
    return MASTER / resource(CLASSIC, resource_id).name


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def matching_edges(image: Image.Image, guard: int = EDGE_GUARD) -> Image.Image:
    """Feather opposite borders to the same pixels without flattening the center."""
    array = np.asarray(image.convert("RGB"), dtype=np.float32).copy()
    height, width = array.shape[:2]
    for offset in range(guard):
        amount = 1.0 - offset / guard
        left = offset
        right = width - 1 - offset
        average = (array[:, left] + array[:, right]) * 0.5
        array[:, left] = array[:, left] * (1.0 - amount) + average * amount
        array[:, right] = array[:, right] * (1.0 - amount) + average * amount
    for offset in range(guard):
        amount = 1.0 - offset / guard
        top = offset
        bottom = height - 1 - offset
        average = (array[top] + array[bottom]) * 0.5
        array[top] = array[top] * (1.0 - amount) + average * amount
        array[bottom] = array[bottom] * (1.0 - amount) + average * amount
    return Image.fromarray(np.clip(array, 0, 255).astype(np.uint8), "RGB")


def material_tile(name: str) -> Image.Image:
    source = Image.open(MATERIAL_SOURCE[name]).convert("RGB")
    side = min(source.size)
    left = (source.width - side) // 2
    top = (source.height - side) // 2
    source = source.crop((left, top, left + side, top + side))
    source = source.resize((TILE_SIZE, TILE_SIZE), Image.Resampling.LANCZOS)
    contrast = {"sand": 0.72, "rock": 0.78, "spice": 0.72}[name]
    source = ImageEnhance.Contrast(source).enhance(contrast)
    source = matching_edges(source)
    return source.filter(
        ImageFilter.UnsharpMask(radius=0.75, percent=110, threshold=2)
    )


def transition_mask(frame: Image.Image, old_sand: Image.Image) -> Image.Image:
    frame_array = np.asarray(frame.convert("RGB"), dtype=np.float32)
    sand_array = np.asarray(old_sand.convert("RGB"), dtype=np.float32)
    difference = np.mean(np.abs(frame_array - sand_array), axis=2)
    mask = np.clip((difference - 3.5) / 23.0, 0.0, 1.0)
    # Reconstruct the low-resolution topology as a broad material blend. The
    # old 1 px edge became a visibly cut 4 px staircase in HD4.
    mask = cv2.GaussianBlur(mask, (0, 0), 3.2)
    mask = mask * mask * (3.0 - 2.0 * mask)
    return Image.fromarray(np.round(mask * 255).astype(np.uint8), "L")


def subtle_relief(frame: Image.Image) -> np.ndarray:
    gray = np.asarray(frame.convert("L"), dtype=np.float32)
    broad = cv2.GaussianBlur(gray, (0, 0), 7.5)
    median = max(1.0, float(np.median(broad)))
    return np.clip(broad / median, 0.86, 1.14)[..., None]


def retexture_frame(
    old_frame: Image.Image,
    old_sand: Image.Image,
    sand: Image.Image,
    material: Image.Image,
    use_transition: bool,
) -> Image.Image:
    if use_transition:
        mask = transition_mask(old_frame, old_sand)
        result = Image.composite(material, sand, mask)
    else:
        result = material.copy()
    array = np.asarray(result.convert("RGB"), dtype=np.float32)
    array *= subtle_relief(old_frame)
    return Image.fromarray(np.clip(array, 0, 255).astype(np.uint8), "RGB")


def enhance_technical_surface(image: Image.Image, detail: Image.Image) -> Image.Image:
    result = Image.new("RGBA", image.size)
    for left in range(0, image.width, TILE_SIZE):
        frame = image.crop((left, 0, left + TILE_SIZE, TILE_SIZE)).convert("RGBA")
        base = frame.convert("RGB").filter(
            ImageFilter.UnsharpMask(radius=1.0, percent=130, threshold=2)
        )
        texture = detail.resize(base.size, Image.Resampling.LANCZOS)
        texture = ImageEnhance.Contrast(texture).enhance(0.55)
        mixed = Image.blend(base, texture, 0.10)
        mixed.putalpha(frame.getchannel("A"))
        result.alpha_composite(mixed, (left, 0))
    return result


def build_terrain() -> dict[str, object]:
    materials = {name: material_tile(name) for name in MATERIAL_SOURCE}
    old_sand = Image.open(resource(MASTER, 121)).convert("RGBA")

    for resource_id, material_name in TERRAIN_MATERIAL.items():
        path = resource(MASTER, resource_id)
        old = Image.open(path).convert("RGBA")
        rebuilt = Image.new("RGBA", old.size)
        for left in range(0, old.width, TILE_SIZE):
            old_frame = old.crop((left, 0, left + TILE_SIZE, TILE_SIZE))
            use_transition = resource_id not in (118, 121)
            frame = retexture_frame(
                old_frame,
                old_sand,
                materials["sand"],
                materials[material_name],
                use_transition,
            )
            if left == 0 and resource_id in (120, 121, 123):
                frame = matching_edges(frame)
            frame.putalpha(old_frame.getchannel("A"))
            rebuilt.alpha_composite(frame, (left, 0))
        rebuilt.save(path, optimize=True)

    for resource_id in (122, 125):
        path = resource(MASTER, resource_id)
        enhanced = enhance_technical_surface(
            Image.open(path).convert("RGBA"),
            materials["rock"],
        )
        enhanced.save(path, optimize=True)

    for resource_id, name in TERRAIN_VARIANTS.items():
        base = Image.open(resource(MASTER, resource_id)).convert("RGBA")
        material = materials[TERRAIN_MATERIAL[resource_id]]
        for variant_index in range(1, 5):
            variant = base.copy()
            rolled = ImageChops.offset(
                material,
                17 * variant_index,
                29 * variant_index,
            )
            rng = np.random.default_rng(
                resource_id * 1009 + variant_index * 9176
            )
            organic_noise = cv2.GaussianBlur(
                rng.random((TILE_SIZE, TILE_SIZE)).astype(np.float32),
                (0, 0),
                18.0,
            )
            organic_noise -= float(organic_noise.min())
            organic_noise /= max(
                1.0e-6,
                float(organic_noise.max()),
            )
            yy, xx = np.mgrid[0:TILE_SIZE, 0:TILE_SIZE]
            edge_distance = np.minimum.reduce(
                (
                    xx,
                    yy,
                    TILE_SIZE - 1 - xx,
                    TILE_SIZE - 1 - yy,
                )
            ).astype(np.float32)
            edge_fade = np.clip(
                (edge_distance - EDGE_GUARD) / 24.0,
                0.0,
                1.0,
            )
            edge_fade = edge_fade * edge_fade * (
                3.0 - 2.0 * edge_fade
            )
            organic_mask = np.clip(
                edge_fade * (0.24 + organic_noise * 0.46),
                0.0,
                0.62,
            )
            for left in range(0, base.width, TILE_SIZE):
                frame = variant.crop((left, 0, left + TILE_SIZE, TILE_SIZE))
                textured = Image.blend(
                    frame.convert("RGB"),
                    rolled,
                    0.07,
                )
                blend_mask = Image.fromarray(
                    np.round(organic_mask * 255).astype(np.uint8),
                    "L",
                )
                textured = Image.composite(
                    textured,
                    frame.convert("RGB"),
                    blend_mask,
                )
                textured.putalpha(frame.getchannel("A"))
                textured_array = np.asarray(textured, dtype=np.uint8).copy()
                frame_array = np.asarray(frame, dtype=np.uint8)
                textured_array[:EDGE_GUARD] = frame_array[:EDGE_GUARD]
                textured_array[-EDGE_GUARD:] = frame_array[-EDGE_GUARD:]
                textured_array[:, :EDGE_GUARD] = frame_array[:, :EDGE_GUARD]
                textured_array[:, -EDGE_GUARD:] = frame_array[:, -EDGE_GUARD:]
                variant.paste(Image.fromarray(textured_array, "RGBA"), (left, 0))
            variant.save(
                EXTRA / f"{name}_VAR_{variant_index:02d}.png",
                optimize=True,
            )

    foundation_size = TILE_SIZE * 3
    foundation = materials["rock"].resize(
        (foundation_size, foundation_size),
        Image.Resampling.BICUBIC,
    )
    foundation = ImageEnhance.Color(foundation).enhance(0.35)
    foundation = ImageEnhance.Brightness(foundation).enhance(1.10)
    foundation_array = np.asarray(
        foundation.convert("RGBA"),
        dtype=np.uint8,
    ).copy()
    yy, xx = np.mgrid[0:foundation_size, 0:foundation_size]
    edge_distance = np.minimum.reduce(
        (
            xx,
            yy,
            foundation_size - 1 - xx,
            foundation_size - 1 - yy,
        )
    ).astype(np.float32)
    rng = np.random.default_rng(80421)
    edge_noise = cv2.GaussianBlur(
        rng.random((foundation_size, foundation_size)).astype(np.float32),
        (0, 0),
        11.0,
    )
    edge_noise = (edge_noise - 0.5) * 9.0
    alpha = np.clip(
        (edge_distance + edge_noise - 2.0) / 12.0,
        0.0,
        1.0,
    )
    alpha = alpha * alpha * (3.0 - 2.0 * alpha)
    foundation_array[..., 3] = np.round(alpha * 238).astype(np.uint8)
    Image.fromarray(foundation_array, "RGBA").save(
        EXTRA / "BUILDING_FOUNDATION_HD.png",
        optimize=True,
    )

    material_dir = GENERATED / "accepted_materials"
    material_dir.mkdir(parents=True, exist_ok=True)
    for name, material in materials.items():
        material.save(material_dir / f"{name}_hd4_tile.png", optimize=True)
    return {
        "tile_size": TILE_SIZE,
        "edge_guard": EDGE_GUARD,
        "materials": {
            name: {
                "source": str(MATERIAL_SOURCE[name].relative_to(ROOT)),
                "source_sha256": sha256(MATERIAL_SOURCE[name]),
            }
            for name in materials
        },
    }


def build_shroud() -> None:
    for resource_id in (113, 114):
        source = Image.open(resource(CLASSIC, resource_id)).convert("RGBA")
        output = Image.new(
            "RGBA",
            (source.width * 4, source.height * 4),
        )
        for frame_index in range(source.width // 32):
            frame = source.crop(
                (frame_index * 32, 0, (frame_index + 1) * 32, 32)
            )
            alpha = frame.getchannel("A").resize(
                (TILE_SIZE, TILE_SIZE),
                Image.Resampling.BICUBIC,
            ).filter(ImageFilter.GaussianBlur(0.45))
            smooth = Image.new("RGBA", (TILE_SIZE, TILE_SIZE), (0, 0, 0, 255))
            smooth.putalpha(alpha)
            output.alpha_composite(smooth, (frame_index * TILE_SIZE, 0))
        output.save(master_path(resource_id), optimize=True)


def recolor_beacon(image: Image.Image, color: tuple[int, int, int]) -> Image.Image:
    array = np.asarray(image.convert("RGBA"), dtype=np.float32).copy()
    red, green, blue, alpha = np.moveaxis(array, 2, 0)
    chroma = np.maximum(red - np.maximum(green, blue), 0.0)
    glass = np.clip((chroma - 8.0) / 105.0, 0.0, 1.0) * (alpha / 255.0)
    luminance = 0.299 * red + 0.587 * green + 0.114 * blue
    for channel, target in enumerate(color):
        tinted = np.clip(target * (0.42 + luminance / 190.0), 0, 255)
        array[..., channel] = (
            array[..., channel] * (1.0 - glass * 0.82)
            + tinted * glass * 0.82
        )
    return Image.fromarray(np.clip(array, 0, 255).astype(np.uint8), "RGBA")


def build_beacons() -> dict[str, object]:
    source = Image.open(GENERATED / "beacon_cutout.png").convert("RGBA")
    bounds = source.getchannel("A").getbbox()
    if bounds is None:
        raise ValueError("beacon cutout is empty")
    source = source.crop(bounds)
    source.thumbnail((62, 62), Image.Resampling.LANCZOS)

    for house, color in HOUSE_COLORS.items():
        base = recolor_beacon(source, color)
        atlas = Image.new(
            "RGBA",
            (BEACON_FRAME * BEACON_FRAMES, BEACON_FRAME),
        )
        for frame_index in range(BEACON_FRAMES):
            frame = Image.new("RGBA", (BEACON_FRAME, BEACON_FRAME))
            frame.alpha_composite(
                base,
                (
                    (BEACON_FRAME - base.width) // 2,
                    BEACON_FRAME - base.height - 3,
                ),
            )
            angle = frame_index * math.tau / BEACON_FRAMES
            glow_x = round(BEACON_FRAME / 2 + math.cos(angle) * 11)
            glow_y = round(BEACON_FRAME * 0.40 + math.sin(angle) * 4)
            glow = Image.new("RGBA", frame.size)
            drawer = ImageDraw.Draw(glow)
            drawer.ellipse(
                (glow_x - 5, glow_y - 3, glow_x + 5, glow_y + 3),
                fill=(*color, 120),
            )
            glow = glow.filter(ImageFilter.GaussianBlur(2.2))
            frame = Image.alpha_composite(frame, glow)
            atlas.alpha_composite(frame, (frame_index * BEACON_FRAME, 0))
        atlas.save(EXTRA / f"HOUSE_BEACON_{house}.png", optimize=True)
    return {
        "logical_frame": BEACON_LOGICAL_FRAME,
        "hd4_frame": BEACON_FRAME,
        "frames": BEACON_FRAMES,
        "source": str((GENERATED / "beacon_cutout.png").relative_to(ROOT)),
        "source_sha256": sha256(GENERATED / "beacon_cutout.png"),
    }


def main() -> None:
    missing = [path for path in MATERIAL_SOURCE.values() if not path.is_file()]
    if missing:
        raise FileNotFoundError(", ".join(str(path) for path in missing))
    MASTER.mkdir(parents=True, exist_ok=True)
    EXTRA.mkdir(parents=True, exist_ok=True)
    manifest = {
        "release": "v0.8.0-ru4-preview3",
        "terrain": build_terrain(),
        "beacons": {"enabled": False, "reason": "disabled by art direction"},
        "shroud": {
            "resources": [113, 114],
            "policy": "frame-local bicubic alpha reconstruction",
        },
    }
    build_shroud()
    (GENERATED / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print("World render fixes: terrain and shroud")


if __name__ == "__main__":
    main()
