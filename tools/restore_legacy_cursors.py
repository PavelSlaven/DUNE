#!/usr/bin/env python3
"""Restore the accepted legacy cursors without changing any other pack entry."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

from hd_assets import PackEntry, read_pack, write_pack


ROOT = Path(__file__).resolve().parents[1]
BACKUP_DATA = Path(
    r"C:\Users\Slaven\Desktop\D2TM-v0.8.0.windows.ru.backup-before-style-pass-20260802-172412\data"
)
TARGET_DATA_DIRS = (
    ROOT / "artifacts" / "hd_completion" / "styled" / "data",
    ROOT / "resources" / "bin" / "data",
    Path(r"C:\Users\Slaven\Desktop\D2TM-v0.8.0.windows.ru\data"),
)
CURSOR_IDS = tuple(range(79, 90))
EXPECTED_NAMES = (
    "MOUSE_ATTACK",
    "MOUSE_DOWN",
    "MOUSE_FORBIDDEN",
    "MOUSE_LEFT",
    "MOUSE_MOVE",
    "MOUSE_NORMAL",
    "MOUSE_PICK",
    "MOUSE_RALLY",
    "MOUSE_REPAIR",
    "MOUSE_RIGHT",
    "MOUSE_UP",
)


def digest(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def replace_pack(source_path: Path, target_path: Path) -> dict[str, object]:
    source = read_pack(source_path)
    target = read_pack(target_path)
    if len(source) != len(target):
        raise ValueError(f"pack entry count differs: {source_path} -> {target_path}")

    original_payloads = [entry.payload for entry in target]
    replacements: list[dict[str, object]] = []
    updated: list[PackEntry] = []
    for index, (source_entry, target_entry) in enumerate(zip(source, target, strict=True)):
        if source_entry.index != index or target_entry.index != index:
            raise ValueError(f"unexpected entry index at {index}")
        if source_entry.name != target_entry.name:
            raise ValueError(f"entry contract differs at {index}: {source_entry.name!r} / {target_entry.name!r}")
        if index in CURSOR_IDS:
            expected_name = EXPECTED_NAMES[index - CURSOR_IDS[0]]
            if source_entry.name != expected_name:
                raise ValueError(f"cursor ID {index} is {source_entry.name!r}, expected {expected_name!r}")
            updated.append(source_entry)
            replacements.append(
                {
                    "id": index,
                    "name": source_entry.name,
                    "before_sha256": digest(target_entry.payload),
                    "restored_sha256": digest(source_entry.payload),
                }
            )
        else:
            updated.append(target_entry)

    temp_path = target_path.with_suffix(target_path.suffix + ".tmp")
    try:
        write_pack(temp_path, updated)
        verify = read_pack(temp_path)
        for index, entry in enumerate(verify):
            expected = source[index].payload if index in CURSOR_IDS else original_payloads[index]
            if entry.payload != expected:
                raise AssertionError(f"payload verification failed at {target_path}:{index}")
        os.replace(temp_path, target_path)
    finally:
        temp_path.unlink(missing_ok=True)

    return {
        "target": str(target_path),
        "pack_sha256": digest(target_path.read_bytes()),
        "replacements": replacements,
    }


def main() -> int:
    reports: list[dict[str, object]] = []
    for density in (2, 4):
        pack_name = f"sdl_data_hd{density}.dat"
        source_path = BACKUP_DATA / pack_name
        if not source_path.is_file():
            raise FileNotFoundError(source_path)
        for target_dir in TARGET_DATA_DIRS:
            target_path = target_dir / pack_name
            if not target_path.is_file():
                raise FileNotFoundError(target_path)
            reports.append(replace_pack(source_path, target_path))

    report_path = ROOT / "artifacts" / "hd_completion" / "legacy_cursor_restore_report.json"
    report_path.write_text(
        json.dumps(
            {
                "source": str(BACKUP_DATA),
                "cursor_ids": list(CURSOR_IDS),
                "cursor_names": list(EXPECTED_NAMES),
                "packs": reports,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"restored": len(CURSOR_IDS), "packs": len(reports)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
