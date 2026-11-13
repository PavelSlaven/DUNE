#!/usr/bin/env python3
"""Build HD2/HD4 packs containing the approved second Starport."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from PIL import Image, ImageChops

from build_starport_integration import patch_pack
from hd_assets import decode_image, read_pack


ROOT = Path(__file__).resolve().parents[1]
GAME = Path("C:/Users/Slaven/Desktop/D2TM-v0.8.0.windows.ru")
REVIEW = ROOT / "artifacts" / "starport_review_v2"
SOURCE = REVIEW / "BUILD_STARPORT_HD4_PREVIEW.png"
SHADOW_SOURCE = REVIEW / "BUILD_STARPORT_SHADOW_HD4_PREVIEW.png"
OVERLAY_SOURCE = REVIEW / "BUILD_STARPORT_FLAG_HD4_PREVIEW.png"
MASK_SOURCE = REVIEW / "HM_BUILD_STARPORT_FLAG_HD4_PREVIEW.png"
MASTER_DIR = ROOT / "resources" / "hd" / "master4" / "sdl_data"
EXTRA_DIR = (
    ROOT / "resources" / "hd" / "master4_extra_packs" / "sdl_data"
)
OUTPUT_DIR = ROOT / "artifacts" / "starport_integration_v2" / "data"

STARPORT_ID = 36
SHADOW_ID = 37
FRAME_COUNT = 8
HD4_FRAME = (384, 384)
HD2_FRAME = (192, 192)
HD4_ATLAS_SIZE = (384, 3072)
HD2_ATLAS_SIZE = (192, 1536)


def atlas_frame(
    atlas: Image.Image,
    frame_index: int,
    frame_size: tuple[int, int],
) -> Image.Image:
    return atlas.crop(
        (
            0,
            frame_index * frame_size[1],
            frame_size[0],
            (frame_index + 1) * frame_size[1],
        )
    )


def downscale_atlas(atlas: Image.Image) -> Image.Image:
    result = Image.new("RGBA", HD2_ATLAS_SIZE)
    for frame_index in range(FRAME_COUNT):
        frame = atlas_frame(atlas, frame_index, HD4_FRAME)
        result.alpha_composite(
            frame.resize(HD2_FRAME, Image.Resampling.LANCZOS),
            (0, frame_index * HD2_FRAME[1]),
        )
    return result


def validate_source(
    building: Image.Image,
    shadow: Image.Image,
    overlay: Image.Image,
    mask: Image.Image,
) -> None:
    for name, image in {
        "building": building,
        "shadow": shadow,
        "sphere overlay": overlay,
        "sphere mask": mask,
    }.items():
        if image.size != HD4_ATLAS_SIZE:
            raise AssertionError(f"{name} has invalid size {image.size}")
        if image.getchannel("A").getbbox() is None:
            raise AssertionError(f"{name} is fully transparent")

    building_bounds = [
        atlas_frame(building, index, HD4_FRAME).getchannel("A").getbbox()
        for index in range(FRAME_COUNT)
    ]
    if len(set(building_bounds)) != 1:
        raise AssertionError(f"Starport frame anchors differ: {building_bounds}")

    first_mask = atlas_frame(mask, 0, HD4_FRAME)
    if first_mask.getchannel("A").getbbox() != (292, 17, 357, 209):
        raise AssertionError("Starport sphere mask bounds changed")
    for frame_index in range(1, FRAME_COUNT):
        if ImageChops.difference(
            first_mask,
            atlas_frame(mask, frame_index, HD4_FRAME),
        ).getbbox():
            raise AssertionError("Starport sphere mask changes between frames")


def validate_packed_pair(
    hd2_path: Path,
    hd4_path: Path,
    resource_ids: tuple[int, ...],
) -> None:
    packed2 = read_pack(hd2_path)
    packed4 = read_pack(hd4_path)
    for resource_id in resource_ids:
        image2 = decode_image(packed2[resource_id].payload)
        image4 = decode_image(packed4[resource_id].payload)
        if image2 is None or image4 is None:
            raise AssertionError(f"unable to decode resource {resource_id}")
        if image2.size != HD2_ATLAS_SIZE or image4.size != HD4_ATLAS_SIZE:
            raise AssertionError(
                f"resource {resource_id} has invalid packed dimensions"
            )
        expected2 = downscale_atlas(image4)
        if ImageChops.difference(
            image2.convert("RGBA"),
            expected2,
        ).getbbox():
            raise AssertionError(
                f"HD2 resource {resource_id} is not the framewise HD4 derivative"
            )


def main() -> int:
    required = (SOURCE, SHADOW_SOURCE, OVERLAY_SOURCE, MASK_SOURCE)
    for path in required:
        if not path.is_file():
            raise FileNotFoundError(path)

    building4 = Image.open(SOURCE).convert("RGBA")
    shadow4 = Image.open(SHADOW_SOURCE).convert("RGBA")
    overlay4 = Image.open(OVERLAY_SOURCE).convert("RGBA")
    mask4 = Image.open(MASK_SOURCE).convert("RGBA")
    validate_source(building4, shadow4, overlay4, mask4)

    building2 = downscale_atlas(building4)
    shadow2 = downscale_atlas(shadow4)
    overlay2 = downscale_atlas(overlay4)
    mask2 = downscale_atlas(mask4)

    MASTER_DIR.mkdir(parents=True, exist_ok=True)
    EXTRA_DIR.mkdir(parents=True, exist_ok=True)
    building4.save(MASTER_DIR / "0036_BUILD_STARPORT.png", optimize=True)
    shadow4.save(
        MASTER_DIR / "0037_BUILD_STARPORT_SHADOW.png",
        optimize=True,
    )
    overlay4.save(EXTRA_DIR / "BUILD_STARPORT_FLAG.png", optimize=True)
    mask4.save(EXTRA_DIR / "HM_BUILD_STARPORT_FLAG.png", optimize=True)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    builds = [
        patch_pack(
            GAME / "data" / "sdl_data_hd2.dat",
            OUTPUT_DIR / "sdl_data_hd2.dat",
            building2,
            shadow2,
            overlay2,
            mask2,
        ),
        patch_pack(
            GAME / "data" / "sdl_data_hd4.dat",
            OUTPUT_DIR / "sdl_data_hd4.dat",
            building4,
            shadow4,
            overlay4,
            mask4,
        ),
    ]
    if builds[0]["flag_id"] != builds[1]["flag_id"]:
        raise AssertionError("HD2 and HD4 sphere overlay IDs differ")
    if builds[0]["mask_id"] != builds[1]["mask_id"]:
        raise AssertionError("HD2 and HD4 sphere mask IDs differ")

    resource_ids = (
        STARPORT_ID,
        SHADOW_ID,
        int(builds[0]["flag_id"]),
        int(builds[0]["mask_id"]),
    )
    validate_packed_pair(
        OUTPUT_DIR / "sdl_data_hd2.dat",
        OUTPUT_DIR / "sdl_data_hd4.dat",
        resource_ids,
    )

    manifest = {
        "format": 1,
        "status": "built_not_installed",
        "resource_id": STARPORT_ID,
        "shadow_id": SHADOW_ID,
        "sphere_overlay_name": "BUILD_STARPORT_FLAG",
        "sphere_overlay_id": builds[0]["flag_id"],
        "sphere_mask_name": "HM_BUILD_STARPORT_FLAG",
        "sphere_mask_id": builds[0]["mask_id"],
        "frames": FRAME_COUNT,
        "logical_frame": [96, 96],
        "hd2_frame": list(HD2_FRAME),
        "hd4_frame": list(HD4_FRAME),
        "animation": {
            "frames_0_to_6": "landing lights lead toward the center",
            "frame_7": "cargo covers the landing pad",
        },
        "house_marker": "two right-side spheres; no flag",
        "builds": builds,
    }
    (OUTPUT_DIR.parent / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(manifest, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, AssertionError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(1)
