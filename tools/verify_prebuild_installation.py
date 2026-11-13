#!/usr/bin/env python3
"""Verify the installed construction-site HD resources and pack isolation."""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

from PIL import Image, ImageChops

from hd_assets import decode_image, read_pack


ROOT = Path(__file__).resolve().parents[1]
GAME_DATA = Path(
    "C:/Users/Slaven/Desktop/D2TM-v0.8.0.windows.ru/data"
)
OUTPUT_DATA = ROOT / "artifacts" / "prebuild_integration_v1" / "data"
BACKUP_DATA = (
    ROOT
    / "artifacts"
    / "prebuild_integration_v1"
    / "backup_before_install"
)

EXPECTED = {
    17: ("BUILD_PRE_1X1", (32, 32)),
    18: ("BUILD_PRE_1X1_SHADOW", (32, 32)),
    19: ("BUILD_PRE_2X2", (64, 64)),
    20: ("BUILD_PRE_2X2_SHADOW", (64, 64)),
    21: ("BUILD_PRE_3X2", (96, 64)),
    22: ("BUILD_PRE_3X2_SHADOW", (96, 64)),
    23: ("BUILD_PRE_3X3", (96, 96)),
    24: ("BUILD_PRE_3X3_SHADOW", (96, 96)),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    changed = set(EXPECTED)
    installed_by_density = {}
    for density in (2, 4):
        name = f"sdl_data_hd{density}.dat"
        installed_path = GAME_DATA / name
        built_path = OUTPUT_DATA / name
        backup_path = BACKUP_DATA / name
        for path in (installed_path, built_path, backup_path):
            if not path.is_file():
                raise FileNotFoundError(path)

        if sha256(installed_path) != sha256(built_path):
            raise AssertionError(f"installed {name} differs from built pack")

        installed = read_pack(installed_path)
        backup = read_pack(backup_path)
        if len(installed) != len(backup):
            raise AssertionError(f"{name}: entry count changed")
        for before, after in zip(backup, installed, strict=True):
            if before.index in changed:
                continue
            if (
                before.index != after.index
                or before.name != after.name
                or before.extension != after.extension
                or before.payload != after.payload
            ):
                raise AssertionError(
                    f"{name}: unrelated resource changed: "
                    f"{before.index}:{before.name}"
                )

        for resource_id, (expected_name, logical_size) in EXPECTED.items():
            entry = installed[resource_id]
            if entry.name != expected_name:
                raise AssertionError(
                    f"{name}[{resource_id}] is {entry.name}, "
                    f"not {expected_name}"
                )
            image = decode_image(entry.payload)
            expected_size = (
                logical_size[0] * density,
                logical_size[1] * density,
            )
            if image is None or image.size != expected_size:
                raise AssertionError(
                    f"{name}[{resource_id}] has invalid size"
                )
            if image.getchannel("A").getbbox() is None:
                raise AssertionError(
                    f"{name}[{resource_id}] is fully transparent"
                )

        if backup[25].payload != installed[25].payload:
            raise AssertionError(f"{name}: BUILD_PRE_CONST changed")
        installed_by_density[density] = installed

    for resource_id in EXPECTED:
        image2 = decode_image(installed_by_density[2][resource_id].payload)
        image4 = decode_image(installed_by_density[4][resource_id].payload)
        if image2 is None or image4 is None:
            raise AssertionError(f"unable to decode resource {resource_id}")
        expected2 = image4.resize(image2.size, Image.Resampling.LANCZOS)
        if ImageChops.difference(
            image2.convert("RGBA"),
            expected2.convert("RGBA"),
        ).getbbox():
            raise AssertionError(
                f"resource {resource_id}: HD2 is not the HD4 derivative"
            )

    print(
        "Installed construction sites verified: IDs 17-24; "
        "all unrelated entries preserved"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, AssertionError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(1)
