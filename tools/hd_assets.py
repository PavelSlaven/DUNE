#!/usr/bin/env python3
"""Inventory, extract, build, and validate density-aware D2TM image packs."""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import struct
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from PIL import Image


PACK_MAGIC = b"D2TM"
ENTRY = struct.Struct("<40s4sII")
HEADER = struct.Struct("<4sH")
MAIN_PACKS = (
    "sdl_data.dat",
    "sdl_inter.dat",
    "sdl_world.dat",
    "sdl_mentat.dat",
)


@dataclass(frozen=True)
class PackEntry:
    index: int
    name: str
    extension: str
    payload: bytes


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def safe_name(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_.-]+", "_", value).strip("._")
    return cleaned or "unnamed"


def read_pack(path: Path) -> list[PackEntry]:
    blob = path.read_bytes()
    if len(blob) < HEADER.size:
        raise ValueError("file is shorter than a D2TM header")
    magic, count = HEADER.unpack_from(blob)
    if magic != PACK_MAGIC:
        raise ValueError("missing D2TM signature")

    directory_end = HEADER.size + count * ENTRY.size
    if directory_end > len(blob):
        raise ValueError("directory extends beyond end of file")

    entries: list[PackEntry] = []
    for index in range(count):
        raw_name, raw_extension, offset, size = ENTRY.unpack_from(
            blob,
            HEADER.size + index * ENTRY.size,
        )
        start = directory_end + offset
        end = start + size
        if start < directory_end or end > len(blob):
            raise ValueError(f"entry {index} points outside the pack")
        name = raw_name.split(b"\0", 1)[0].decode("utf-8", errors="replace")
        extension = raw_extension.split(b"\0", 1)[0].decode(
            "ascii",
            errors="replace",
        )
        entries.append(
            PackEntry(
                index=index,
                name=name,
                extension=extension,
                payload=blob[start:end],
            )
        )
    return entries


def write_pack(path: Path, entries: Iterable[PackEntry]) -> None:
    materialized = list(entries)
    if len(materialized) > 0xFFFF:
        raise ValueError("D2TM packs support at most 65535 entries")

    path.parent.mkdir(parents=True, exist_ok=True)
    offsets: list[int] = []
    cursor = 0
    for entry in materialized:
        offsets.append(cursor)
        cursor += len(entry.payload)
        if cursor > 0xFFFFFFFF:
            raise ValueError("D2TM pack data exceeds the 4 GiB offset limit")

    with path.open("wb") as output:
        output.write(HEADER.pack(PACK_MAGIC, len(materialized)))
        for entry, offset in zip(materialized, offsets, strict=True):
            raw_name = entry.name.encode("utf-8")
            raw_extension = entry.extension.encode("ascii")
            if len(raw_name) >= 40:
                raise ValueError(
                    f"entry name is too long for D2TM: {entry.name!r}"
                )
            if len(raw_extension) > 3:
                raise ValueError(
                    f"entry extension is too long: {entry.extension!r}"
                )
            output.write(
                ENTRY.pack(
                    raw_name.ljust(40, b"\0"),
                    raw_extension.ljust(4, b"\0"),
                    offset,
                    len(entry.payload),
                )
            )
        for entry in materialized:
            output.write(entry.payload)


def decode_image(payload: bytes) -> Image.Image | None:
    try:
        image = Image.open(io.BytesIO(payload))
        image.load()
        return image
    except Exception:
        return None


def encode_png(image: Image.Image) -> bytes:
    output = io.BytesIO()
    save_options: dict[str, object] = {"optimize": True}
    if image.mode == "P" and "transparency" in image.info:
        save_options["transparency"] = image.info["transparency"]
    image.save(output, format="PNG", **save_options)
    return output.getvalue()


def scale_image(image: Image.Image, density: int) -> Image.Image:
    target = (image.width * density, image.height * density)
    if image.mode == "P":
        return image.resize(target, Image.Resampling.NEAREST)
    return image.resize(target, Image.Resampling.LANCZOS)


def master_override_path(
    master_root: Path,
    pack_name: str,
    entry: PackEntry,
) -> Path:
    return (
        master_root
        / Path(pack_name).stem
        / f"{entry.index:04d}_{safe_name(entry.name)}.png"
    )


def extract_pack(
    pack_path: Path,
    extract_root: Path,
) -> dict[str, object]:
    entries = read_pack(pack_path)
    pack_dir = extract_root / pack_path.stem
    pack_dir.mkdir(parents=True, exist_ok=True)
    manifest_entries: list[dict[str, object]] = []

    for entry in entries:
        image = decode_image(entry.payload)
        record: dict[str, object] = {
            "index": entry.index,
            "name": entry.name,
            "extension": entry.extension,
            "size": len(entry.payload),
            "sha256": sha256(entry.payload),
            "is_image": image is not None,
        }
        if image is not None:
            extracted_name = (
                f"{entry.index:04d}_{safe_name(entry.name)}.png"
            )
            extracted_path = pack_dir / extracted_name
            extracted_path.write_bytes(encode_png(image))
            record.update(
                {
                    "width": image.width,
                    "height": image.height,
                    "mode": image.mode,
                    "extracted": extracted_path.as_posix(),
                }
            )
        manifest_entries.append(record)

    return {
        "source": pack_path.as_posix(),
        "name": pack_path.name,
        "entry_count": len(entries),
        "sha256": sha256(pack_path.read_bytes()),
        "entries": manifest_entries,
    }


def discover_packs(data_dir: Path, scenes_dir: Path) -> tuple[list[Path], list[Path]]:
    main = [data_dir / name for name in MAIN_PACKS]
    missing = [path for path in main if not path.is_file()]
    if missing:
        raise FileNotFoundError(
            "Missing main pack(s): " + ", ".join(str(path) for path in missing)
        )
    scenes = sorted(path for path in scenes_dir.glob("*.dat") if path.is_file())
    return main, scenes


def inventory(args: argparse.Namespace) -> int:
    data_dir = Path(args.data_dir).resolve()
    scenes_dir = Path(args.scenes_dir).resolve()
    extract_root = Path(args.extract_root).resolve()
    manifest_path = Path(args.manifest).resolve()
    main, scenes = discover_packs(data_dir, scenes_dir)

    manifest: dict[str, object] = {
        "format": 1,
        "main_packs": [],
        "scene_packs": [],
        "unsupported_scene_files": [],
    }
    for path in main:
        manifest["main_packs"].append(extract_pack(path, extract_root))
    for path in scenes:
        try:
            manifest["scene_packs"].append(
                extract_pack(path, extract_root / "scenes")
            )
        except ValueError as error:
            manifest["unsupported_scene_files"].append(
                {
                    "source": path.as_posix(),
                    "name": path.name,
                    "sha256": sha256(path.read_bytes()),
                    "reason": str(error),
                }
            )

    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        f"Inventory: {len(manifest['main_packs'])} main packs, "
        f"{len(manifest['scene_packs'])} scene packs, "
        f"{len(manifest['unsupported_scene_files'])} unsupported scenes"
    )
    print(f"Manifest: {manifest_path}")
    return 0


def hd_pack_name(classic_name: str, density: int) -> str:
    path = Path(classic_name)
    return f"{path.stem}_hd{density}{path.suffix}"


def build_one_pack(
    source_path: Path,
    output_path: Path,
    density: int,
    master_root: Path,
    extra_root: Path,
    logical_pack_name: str,
) -> tuple[int, int, int]:
    output_entries: list[PackEntry] = []
    overrides = 0
    images = 0
    for entry in read_pack(source_path):
        image = decode_image(entry.payload)
        if image is None:
            output_entries.append(entry)
            continue

        images += 1
        override = master_override_path(
            master_root,
            logical_pack_name,
            entry,
        )
        if override.is_file():
            master = Image.open(override)
            master.load()
            expected = (image.width * 4, image.height * 4)
            if master.size != expected:
                raise ValueError(
                    f"{override} has size {master.size}; expected {expected}"
                )
            scaled = (
                master.copy()
                if density == 4
                else master.resize(
                    (image.width * density, image.height * density),
                    Image.Resampling.LANCZOS,
                )
            )
            overrides += 1
        else:
            scaled = scale_image(image, density)

        output_entries.append(
            PackEntry(
                index=entry.index,
                name=entry.name,
                extension="PNG",
                payload=encode_png(scaled),
            )
        )

    existing_names = {entry.name for entry in output_entries}
    extras = 0
    extra_dir = extra_root / Path(logical_pack_name).stem
    if extra_dir.is_dir():
        for extra_path in sorted(extra_dir.glob("*.png")):
            extra_name = extra_path.stem
            if extra_name in existing_names:
                raise ValueError(
                    f"extra resource duplicates existing ID: {extra_name}"
                )
            if len(extra_name.encode("utf-8")) >= 40:
                # The legacy pack format cannot address longer identifiers.
                # Compact HV_/HM_ aliases are emitted for every active House
                # variant, so stale descriptive build artifacts are ignored.
                print(f"Skipped unaddressable extra resource: {extra_name}")
                continue
            master = Image.open(extra_path)
            master.load()
            if master.width % 4 or master.height % 4:
                raise ValueError(
                    f"{extra_path} must have dimensions divisible by 4"
                )
            scaled = (
                master.copy()
                if density == 4
                else master.resize(
                    (master.width // 2, master.height // 2),
                    Image.Resampling.LANCZOS,
                )
            )
            output_entries.append(
                PackEntry(
                    index=len(output_entries),
                    name=extra_name,
                    extension="PNG",
                    payload=encode_png(scaled),
                )
            )
            existing_names.add(extra_name)
            extras += 1
    write_pack(output_path, output_entries)
    return images, overrides, extras


def build(args: argparse.Namespace) -> int:
    density = int(args.density)
    if density not in (2, 4):
        raise ValueError("density must be 2 or 4")

    data_dir = Path(args.data_dir).resolve()
    scenes_dir = Path(args.scenes_dir).resolve()
    output_data_dir = Path(args.output_data_dir).resolve()
    output_scenes_dir = (
        Path(args.output_scenes_dir).resolve() / f"hd{density}"
    )
    master_root = Path(args.master_root).resolve()
    extra_root = (
        Path(args.extra_root).resolve()
        if args.extra_root
        else master_root.parent / "master4_extra_packs"
    )
    main, scenes = discover_packs(data_dir, scenes_dir)

    total_images = 0
    total_overrides = 0
    for source in main:
        output = output_data_dir / hd_pack_name(source.name, density)
        images, overrides, extras = build_one_pack(
            source,
            output,
            density,
            master_root,
            extra_root,
            source.name,
        )
        total_images += images
        total_overrides += overrides
        print(
            f"Built {output.name}: {images} images, "
            f"{overrides} masters, {extras} appended resources"
        )

    for source in scenes:
        try:
            read_pack(source)
        except ValueError:
            continue
        output = output_scenes_dir / source.name
        images, overrides, extras = build_one_pack(
            source,
            output,
            density,
            master_root / "scenes",
            extra_root / "scenes",
            source.name,
        )
        total_images += images
        total_overrides += overrides

    print(
        f"HD{density}: {total_images} images, "
        f"{total_overrides} approved master overrides"
    )
    return 0


def validate_pair(
    classic_path: Path,
    hd_path: Path,
    density: int,
) -> list[str]:
    errors: list[str] = []
    classic_entries = read_pack(classic_path)
    hd_entries = read_pack(hd_path)
    if len(hd_entries) < len(classic_entries):
        return [
            f"{hd_path}: {len(hd_entries)} entries; "
            f"expected at least {len(classic_entries)}"
        ]

    for classic, hd in zip(
        classic_entries,
        hd_entries[:len(classic_entries)],
        strict=True,
    ):
        prefix = f"{hd_path.name}[{classic.index}:{classic.name}]"
        if classic.name != hd.name:
            errors.append(f"{prefix}: ID/name changed to {hd.name!r}")
        classic_image = decode_image(classic.payload)
        hd_image = decode_image(hd.payload)
        if classic_image is None:
            if classic.payload != hd.payload:
                errors.append(f"{prefix}: non-image payload changed")
            continue
        if hd_image is None:
            errors.append(f"{prefix}: HD payload is not an image")
            continue
        expected = (
            classic_image.width * density,
            classic_image.height * density,
        )
        if hd_image.size != expected:
            errors.append(
                f"{prefix}: size {hd_image.size}; expected {expected}"
            )

    names = {entry.name for entry in classic_entries}
    for hd in hd_entries[len(classic_entries):]:
        prefix = f"{hd_path.name}[{hd.index}:{hd.name}]"
        if hd.name in names:
            errors.append(f"{prefix}: duplicate resource name")
        names.add(hd.name)
        hd_image = decode_image(hd.payload)
        if hd_image is None:
            errors.append(f"{prefix}: appended payload is not an image")
            continue
        if hd_image.width % density or hd_image.height % density:
            errors.append(
                f"{prefix}: dimensions {hd_image.size} are not "
                f"divisible by density {density}"
            )
    return errors


def validate(args: argparse.Namespace) -> int:
    density = int(args.density)
    data_dir = Path(args.data_dir).resolve()
    scenes_dir = Path(args.scenes_dir).resolve()
    output_data_dir = Path(args.output_data_dir).resolve()
    output_scenes_dir = (
        Path(args.output_scenes_dir).resolve() / f"hd{density}"
    )
    main, scenes = discover_packs(data_dir, scenes_dir)

    errors: list[str] = []
    for source in main:
        errors.extend(
            validate_pair(
                source,
                output_data_dir / hd_pack_name(source.name, density),
                density,
            )
        )
    for source in scenes:
        output = output_scenes_dir / source.name
        if not output.is_file():
            continue
        try:
            errors.extend(validate_pair(source, output, density))
        except ValueError as error:
            errors.append(f"{output}: {error}")

    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"HD{density} packs are structurally valid")
    return 0


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser()
    subparsers = result.add_subparsers(dest="command", required=True)

    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--data-dir", required=True)
    common.add_argument("--scenes-dir", required=True)

    inventory_parser = subparsers.add_parser(
        "inventory",
        parents=[common],
    )
    inventory_parser.add_argument("--extract-root", required=True)
    inventory_parser.add_argument("--manifest", required=True)
    inventory_parser.set_defaults(handler=inventory)

    build_parser = subparsers.add_parser("build", parents=[common])
    build_parser.add_argument("--density", type=int, required=True)
    build_parser.add_argument("--output-data-dir", required=True)
    build_parser.add_argument("--output-scenes-dir", required=True)
    build_parser.add_argument("--master-root", required=True)
    build_parser.add_argument("--extra-root")
    build_parser.set_defaults(handler=build)

    validate_parser = subparsers.add_parser("validate", parents=[common])
    validate_parser.add_argument("--density", type=int, required=True)
    validate_parser.add_argument("--output-data-dir", required=True)
    validate_parser.add_argument("--output-scenes-dir", required=True)
    validate_parser.set_defaults(handler=validate)
    return result


def main() -> int:
    args = parser().parse_args()
    try:
        return args.handler(args)
    except (OSError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
