#!/usr/bin/env python3
"""Atomically install the completed HD packs and Release executable."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GAME = Path(r"C:\Users\Slaven\Desktop\D2TM-v0.8.0.windows.ru").resolve()
STYLED_DATA = ROOT / "artifacts" / "hd_completion" / "styled" / "data"
REPOSITORY_BIN = ROOT / "resources" / "bin"
REPORT = ROOT / "artifacts" / "hd_completion" / "install_report.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def protected_files() -> list[Path]:
    candidates = [GAME / "settings.ini", GAME / "log.txt"]
    for directory in (GAME / "save", GAME / "saves"):
        if directory.is_dir():
            candidates.extend(path for path in directory.rglob("*") if path.is_file())
    return sorted(set(path.resolve() for path in candidates if path.is_file()))


def atomic_copy(source: Path, destination: Path) -> None:
    source = source.resolve()
    destination = destination.resolve()
    allowed = (GAME, REPOSITORY_BIN.resolve())
    if not any(destination.is_relative_to(root) for root in allowed):
        raise ValueError(f"Destination is outside approved roots: {destination}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_name(destination.name + ".tmp")
    shutil.copy2(source, temporary)
    os.replace(temporary, destination)


def main() -> int:
    before = {str(path): sha256(path) for path in protected_files()}
    installed: list[dict[str, str]] = []

    # These directories belong to the user. Updates only ensure that they exist;
    # their contents are never copied, removed, or replaced.
    for relative in (
        "music/gameplay",
        "music/menu",
        "music/conquest",
        "music/briefing/atreides",
        "music/briefing/harkonnen",
        "music/briefing/ordos",
        "music/victory",
        "music/defeat",
    ):
        (GAME / relative).mkdir(parents=True, exist_ok=True)

    pack_names = [
        f"sdl_{family}_hd{density}.dat"
        for family in ("data", "inter", "world", "mentat")
        for density in (2, 4)
    ]
    for name in pack_names:
        source = STYLED_DATA / name
        if not source.is_file():
            raise FileNotFoundError(source)
        for destination in (GAME / "data" / name, REPOSITORY_BIN / "data" / name):
            atomic_copy(source, destination)
            if sha256(source) != sha256(destination):
                raise AssertionError(f"Copy verification failed: {destination}")
            installed.append(
                {
                    "source": str(source),
                    "destination": str(destination),
                    "sha256": sha256(destination),
                }
            )

    executable = ROOT / "build-ru" / "d2tm.exe"
    for destination in (GAME / "d2tm.exe", REPOSITORY_BIN / "d2tm.exe"):
        atomic_copy(executable, destination)
        if sha256(executable) != sha256(destination):
            raise AssertionError(f"Executable copy verification failed: {destination}")
        installed.append(
            {
                "source": str(executable),
                "destination": str(destination),
                "sha256": sha256(destination),
            }
        )

    for name in ("README_RU.txt", "THIRD_PARTY_ASSETS_RU.txt"):
        source = REPOSITORY_BIN / name
        destination = GAME / name
        atomic_copy(source, destination)
        installed.append(
            {
                "source": str(source),
                "destination": str(destination),
                "sha256": sha256(destination),
            }
        )

    for language_directory in ("campaign_en", "skirmish_en"):
        source_root = REPOSITORY_BIN / language_directory
        for source in sorted(path for path in source_root.rglob("*.ini") if path.is_file()):
            destination = GAME / source.relative_to(REPOSITORY_BIN)
            atomic_copy(source, destination)
            if sha256(source) != sha256(destination):
                raise AssertionError(f"Language resource copy verification failed: {destination}")
            installed.append(
                {
                    "source": str(source),
                    "destination": str(destination),
                    "sha256": sha256(destination),
                }
            )

    after = {str(path): sha256(path) for path in protected_files()}
    if before != after:
        changed = sorted(set(before) | set(after))
        raise AssertionError(
            "Protected settings/log/save files changed: "
            + ", ".join(path for path in changed if before.get(path) != after.get(path))
        )

    report = {
        "format": 1,
        "game": str(GAME),
        "installed": installed,
        "protected_files": before,
        "protected_unchanged": True,
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Installed {len(installed)} files")
    print(f"Protected files unchanged: {len(before)}")
    print(f"Report: {REPORT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
