#!/usr/bin/env python3
"""Verify user-approved legacy sdl_data resources in every distributable pack."""

from __future__ import annotations

from pathlib import Path

from hd_assets import read_pack


ROOT = Path(__file__).resolve().parents[1]
BACKUP_DATA = Path(
    r"C:\Users\Slaven\Desktop\D2TM-v0.8.0.windows.ru.backup-before-style-pass-20260802-172412\data"
)
TARGET_DATA_DIRS = (
    ROOT / "artifacts" / "hd_completion" / "styled" / "data",
    ROOT / "resources" / "bin" / "data",
    Path(r"C:\Users\Slaven\Desktop\D2TM-v0.8.0.windows.ru\data"),
)
PRESERVED_RESOURCES = {
    **dict(enumerate(
        (
            "MOUSE_ATTACK", "MOUSE_DOWN", "MOUSE_FORBIDDEN", "MOUSE_LEFT",
            "MOUSE_MOVE", "MOUSE_NORMAL", "MOUSE_PICK", "MOUSE_RALLY",
            "MOUSE_REPAIR", "MOUSE_RIGHT", "MOUSE_UP",
        ),
        start=79,
    )),
    113: "SHROUD",
    114: "SHROUD_SHADOW",
}


def main() -> int:
    checked = 0
    for density in (2, 4):
        pack_name = f"sdl_data_hd{density}.dat"
        accepted = read_pack(BACKUP_DATA / pack_name)
        for target_dir in TARGET_DATA_DIRS:
            current = read_pack(target_dir / pack_name)
            for resource_id, expected_name in PRESERVED_RESOURCES.items():
                source_entry = accepted[resource_id]
                target_entry = current[resource_id]
                if source_entry.name != expected_name or target_entry.name != expected_name:
                    raise AssertionError(
                        f"resource identity mismatch at HD{density} ID {resource_id}: "
                        f"{source_entry.name!r} / {target_entry.name!r}"
                    )
                if (
                    source_entry.extension != target_entry.extension
                    or source_entry.payload != target_entry.payload
                ):
                    raise AssertionError(
                        f"legacy resource changed: HD{density} {expected_name} in {target_dir}"
                    )
                checked += 1
    print(f"preserved_legacy_resources=ok; checks={checked}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
