#!/usr/bin/env python3
"""Stage the approved artistic cursors while preserving all other pack entries."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageChops

from hd_assets import PackEntry, decode_image, encode_png, read_pack, write_pack


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_ROOT = ROOT / "artifacts" / "cursor_hd_redraw_v2"
LIVE_DATA = Path(r"C:\Users\Slaven\Desktop\D2TM-v0.8.0.windows.ru\data")
STAGED_DATA = ARTIFACT_ROOT / "staged" / "data"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def assert_same_pixels(actual: Image.Image, expected: Image.Image, label: str) -> None:
    actual_rgba = actual.convert("RGBA")
    expected_rgba = expected.convert("RGBA")
    if actual_rgba.size != expected_rgba.size:
        raise AssertionError(
            f"{label}: size differs: {actual_rgba.size} != {expected_rgba.size}"
        )
    if ImageChops.difference(actual_rgba, expected_rgba).getbbox() is not None:
        raise AssertionError(f"{label}: decoded pixels differ")


def stage_pack(density: int, resources: list[dict[str, object]]) -> dict[str, object]:
    pack_name = f"sdl_data_hd{density}.dat"
    source_path = LIVE_DATA / pack_name
    staged_path = STAGED_DATA / pack_name
    source = read_pack(source_path)
    replacements = {int(resource["id"]): resource for resource in resources}

    updated: list[PackEntry] = []
    changed: list[dict[str, object]] = []
    expected_images: dict[int, Image.Image] = {}
    for entry in source:
        resource = replacements.get(entry.index)
        if resource is None:
            updated.append(entry)
            continue

        expected_name = str(resource["name"])
        if entry.name != expected_name:
            raise ValueError(
                f"{pack_name}:{entry.index} is {entry.name!r}, expected {expected_name!r}"
            )
        image_path = ARTIFACT_ROOT / f"hd{density}" / str(resource["file"])
        with Image.open(image_path) as opened:
            image = opened.convert("RGBA")
        expected_size = tuple(int(value) for value in resource[f"hd{density}_size"])
        if image.size != expected_size:
            raise ValueError(
                f"{image_path}: size {image.size} differs from {expected_size}"
            )
        current_image = decode_image(entry.payload)
        if current_image is None:
            raise ValueError(f"{pack_name}:{entry.index} is not a decodable image")
        if current_image.size != expected_size:
            raise ValueError(
                f"{pack_name}:{entry.index} contract changed: "
                f"{current_image.size} != {expected_size}"
            )

        payload = encode_png(image)
        updated.append(
            PackEntry(
                index=entry.index,
                name=entry.name,
                extension=entry.extension,
                payload=payload,
            )
        )
        expected_images[entry.index] = image
        changed.append(
            {
                "id": entry.index,
                "name": entry.name,
                "before_sha256": digest(entry.payload),
                "after_sha256": digest(payload),
                "size": list(image.size),
            }
        )

    if len(changed) != len(resources):
        raise AssertionError(
            f"{pack_name}: replaced {len(changed)} resources, expected {len(resources)}"
        )

    write_pack(staged_path, updated)
    verified = read_pack(staged_path)
    if len(verified) != len(source):
        raise AssertionError(f"{pack_name}: entry count changed")
    for original, staged in zip(source, verified, strict=True):
        if (original.index, original.name, original.extension) != (
            staged.index,
            staged.name,
            staged.extension,
        ):
            raise AssertionError(f"{pack_name}:{original.index}: metadata changed")
        if original.index not in replacements:
            if staged.payload != original.payload:
                raise AssertionError(
                    f"{pack_name}:{original.index}: non-cursor payload changed"
                )
            continue
        staged_image = decode_image(staged.payload)
        if staged_image is None:
            raise AssertionError(f"{pack_name}:{original.index}: staged image is invalid")
        assert_same_pixels(
            staged_image,
            expected_images[original.index],
            f"{pack_name}:{original.index}",
        )

    return {
        "source": str(source_path),
        "staged": str(staged_path),
        "source_sha256": digest(source_path.read_bytes()),
        "staged_sha256": digest(staged_path.read_bytes()),
        "entry_count": len(source),
        "changed": changed,
    }


def main() -> int:
    manifest = json.loads((ARTIFACT_ROOT / "manifest.json").read_text(encoding="utf-8"))
    resources = manifest["resources"]
    reports = [stage_pack(density, resources) for density in (2, 4)]
    report = {
        "status": "staged_and_verified",
        "live_data": str(LIVE_DATA),
        "cursor_ids": [int(resource["id"]) for resource in resources],
        "packs": reports,
    }
    report_path = ARTIFACT_ROOT / "install_report.json"
    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
