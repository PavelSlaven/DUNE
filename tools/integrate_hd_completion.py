#!/usr/bin/env python3
"""Safely integrate the reviewed 169 HD completion masters into D2TM packs.

The installed game is the canonical source because it contains later approved
changes that are not necessarily present in the source tree.  Only explicitly
listed entry IDs are replaced; every other entry payload is verified byte for
byte.  HD2 is always derived from HD4 with premultiplied-alpha Lanczos.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys
from dataclasses import replace
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hd_assets import PackEntry, encode_png, read_pack, safe_name, write_pack  # noqa: E402


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_GAME = Path(r"C:\Users\Slaven\Desktop\D2TM-v0.8.0.windows.ru")
ARTIFACT_ROOT = ROOT / "artifacts" / "hd_completion"
STAGE_ROOT = ARTIFACT_ROOT / "integrated"

PACK_SPECS = {
    "sdl_data": {
        "manifest": ARTIFACT_ROOT / "effects" / "manifest.json",
        "records": "resources",
        "asset_root": ARTIFACT_ROOT / "effects" / "sdl_data",
    },
    "sdl_inter": {
        "manifest": ARTIFACT_ROOT / "interface" / "manifest.json",
        "records": "assets",
        "asset_root": ARTIFACT_ROOT / "interface",
    },
    "sdl_world": {
        "manifest": ARTIFACT_ROOT / "world" / "manifest.json",
        "records": "resources",
        "asset_root": ARTIFACT_ROOT / "world",
    },
    "sdl_mentat": {
        "manifest": ARTIFACT_ROOT / "mentat" / "manifest.json",
        "records": "assets",
        "asset_root": ARTIFACT_ROOT / "mentat",
    },
}

# These accepted legacy resources are intentionally retained after user review.
# Keep this guard even if an older generated manifest is reused later.
PRESERVED_LEGACY_DATA_NAMES = {
    "MOUSE_ATTACK", "MOUSE_DOWN", "MOUSE_FORBIDDEN", "MOUSE_LEFT",
    "MOUSE_MOVE", "MOUSE_NORMAL", "MOUSE_PICK", "MOUSE_RALLY",
    "MOUSE_REPAIR", "MOUSE_RIGHT", "MOUSE_UP",
    "SHROUD", "SHROUD_SHADOW",
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def atomic_copy(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_name(destination.name + ".tmp")
    shutil.copy2(source, temporary)
    os.replace(temporary, destination)


def resize_rgba_premultiplied(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    rgba = image.convert("RGBA")
    # Pillow has no direct premultiplied resize primitive.  RGBa is the
    # premultiplied-alpha mode and therefore avoids bright/white edge halos.
    premultiplied = rgba.convert("RGBa")
    resized = premultiplied.resize(size, Image.Resampling.LANCZOS)
    return resized.convert("RGBA")


def load_records(pack_name: str) -> list[dict[str, object]]:
    spec = PACK_SPECS[pack_name]
    manifest = json.loads(Path(spec["manifest"]).read_text(encoding="utf-8"))
    records = list(manifest[str(spec["records"])])
    if pack_name == "sdl_data":
        records = [
            record
            for record in records
            if str(record["name"]) not in PRESERVED_LEGACY_DATA_NAMES
        ]
    if not records:
        raise ValueError(f"No records in {spec['manifest']}")
    return records


def record_asset_path(pack_name: str, record: dict[str, object]) -> Path:
    path = Path(PACK_SPECS[pack_name]["asset_root"]) / str(record["file"])
    if not path.is_file():
        raise FileNotFoundError(path)
    return path


def validate_master(
    master: Image.Image,
    classic: Image.Image,
    pack_name: str,
    entry: PackEntry,
) -> None:
    expected = (classic.width * 4, classic.height * 4)
    if master.size != expected:
        raise ValueError(
            f"{pack_name}[{entry.index}] {entry.name}: HD4 is {master.size}, "
            f"expected {expected}"
        )
    if master.mode not in {"RGB", "RGBA"}:
        raise ValueError(
            f"{pack_name}[{entry.index}] {entry.name}: unsupported mode {master.mode}"
        )


def patch_pack(
    pack_name: str,
    game_data: Path,
    stage_data: Path,
    master_root: Path,
) -> dict[str, object]:
    classic_path = game_data / f"{pack_name}.dat"
    classic_entries = read_pack(classic_path)
    records = load_records(pack_name)
    targets = {int(record["id"]): record for record in records}
    if len(targets) != len(records):
        raise ValueError(f"Duplicate target ID in {pack_name}")

    density_reports: list[dict[str, object]] = []
    outputs: dict[int, Path] = {}
    base_entries: dict[int, list[PackEntry]] = {}

    for density in (4, 2):
        source_path = game_data / f"{pack_name}_hd{density}.dat"
        source_entries = read_pack(source_path)
        if len(source_entries) != len(read_pack(game_data / f"{pack_name}_hd4.dat")):
            raise ValueError(f"Entry count differs between densities for {pack_name}")
        base_entries[density] = source_entries

        patched: list[PackEntry] = []
        changed: list[dict[str, object]] = []
        for entry in source_entries:
            record = targets.get(entry.index)
            if record is None:
                patched.append(entry)
                continue

            if entry.index >= len(classic_entries):
                raise ValueError(f"Target {pack_name}[{entry.index}] has no classic entry")
            classic_entry = classic_entries[entry.index]
            if entry.name != str(record["name"]) or classic_entry.name != entry.name:
                raise ValueError(
                    f"Name mismatch at {pack_name}[{entry.index}]: "
                    f"manifest={record['name']!r}, hd={entry.name!r}, "
                    f"classic={classic_entry.name!r}"
                )
            classic_image = Image.open(__import__("io").BytesIO(classic_entry.payload))
            classic_image.load()
            asset_path = record_asset_path(pack_name, record)
            with Image.open(asset_path) as source_master:
                master = source_master.convert("RGBA")
            validate_master(master, classic_image, pack_name, entry)
            output_image = (
                master
                if density == 4
                else resize_rgba_premultiplied(
                    master,
                    (classic_image.width * 2, classic_image.height * 2),
                )
            )
            payload = encode_png(output_image)
            patched.append(replace(entry, extension="png", payload=payload))
            changed.append(
                {
                    "id": entry.index,
                    "name": entry.name,
                    "master": str(asset_path.relative_to(ROOT)).replace("\\", "/"),
                    "size": list(output_image.size),
                    "old_sha256": hashlib.sha256(entry.payload).hexdigest(),
                    "new_sha256": hashlib.sha256(payload).hexdigest(),
                }
            )

            if density == 4:
                master_path = (
                    master_root
                    / pack_name
                    / f"{entry.index:04d}_{safe_name(entry.name)}.png"
                )
                master_path.parent.mkdir(parents=True, exist_ok=True)
                master_path.write_bytes(encode_png(master))

        output_path = stage_data / f"{pack_name}_hd{density}.dat"
        write_pack(output_path, patched)
        reread = read_pack(output_path)
        for before, after in zip(source_entries, reread, strict=True):
            if before.index not in targets and before.payload != after.payload:
                raise AssertionError(
                    f"Unrelated payload changed: {pack_name}_hd{density}[{before.index}]"
                )
            if before.name != after.name or before.index != after.index:
                raise AssertionError(
                    f"Entry identity changed: {pack_name}_hd{density}[{before.index}]"
                )
        outputs[density] = output_path
        density_reports.append(
            {
                "density": density,
                "source": str(source_path),
                "source_sha256": sha256_file(source_path),
                "output": str(output_path),
                "output_sha256": sha256_file(output_path),
                "entry_count": len(reread),
                "changed_count": len(changed),
                "changed": changed,
            }
        )

    # Pixel-exact requirement for the accepted master relationship.
    hd4_entries = read_pack(outputs[4])
    hd2_entries = read_pack(outputs[2])
    for target_id in targets:
        image4 = Image.open(__import__("io").BytesIO(hd4_entries[target_id].payload)).convert("RGBA")
        image2 = Image.open(__import__("io").BytesIO(hd2_entries[target_id].payload)).convert("RGBA")
        expected2 = resize_rgba_premultiplied(image4, image2.size)
        if image2.tobytes() != expected2.tobytes():
            raise AssertionError(f"HD2 drift at {pack_name}[{target_id}]")

    return {
        "pack": pack_name,
        "target_count": len(targets),
        "densities": density_reports,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--game", type=Path, default=DEFAULT_GAME)
    parser.add_argument("--install", action="store_true")
    args = parser.parse_args()

    game = args.game.resolve()
    game_data = game / "data"
    stage_data = STAGE_ROOT / "data"
    stage_data.mkdir(parents=True, exist_ok=True)
    master_root = ROOT / "resources" / "hd" / "master4"

    reports = [
        patch_pack(pack_name, game_data, stage_data, master_root)
        for pack_name in PACK_SPECS
    ]
    changed_total = sum(int(report["target_count"]) for report in reports)
    # The completion catalog originally contained 169 records.  Thirteen
    # cursor/shroud entries are now deliberately preserved from the classic
    # pack, so the active replacement set contains 156 resources.
    expected_total = 169 - len(PRESERVED_LEGACY_DATA_NAMES)
    if changed_total != expected_total:
        raise AssertionError(
            f"Expected {expected_total} replacements, got {changed_total}"
        )

    report = {
        "format": 1,
        "game": str(game),
        "changed_total": changed_total,
        "packs": reports,
        "installed": bool(args.install),
    }
    report_path = STAGE_ROOT / "integration_report.json"
    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    if args.install:
        repository_data = ROOT / "resources" / "bin" / "data"
        for pack_name in PACK_SPECS:
            for density in (2, 4):
                filename = f"{pack_name}_hd{density}.dat"
                source = stage_data / filename
                atomic_copy(source, game_data / filename)
                atomic_copy(source, repository_data / filename)

    print(f"Integrated and verified {changed_total} HD resources")
    print(f"Stage: {stage_data}")
    print(f"Report: {report_path}")
    print("Installed: yes" if args.install else "Installed: no (staged only)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
