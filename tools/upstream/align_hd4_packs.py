from __future__ import annotations

import argparse
import json
import os
import re
import stat
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

from tools import hd_assets


DEFINE_RE = re.compile(
    r"^\s*#define\s+([A-Za-z_]\w*)\s+([0-9]+)"
    r"(?:\s*(?://.*|/\*.*?\*/))?\s*$"
)
CONSTEXPR_RE = re.compile(
    r"^\s*(?:(?:inline|static)\s+)?constexpr\s+int\s+"
    r"([A-Za-z_]\w*)\s*=\s*([0-9]+)\s*;"
    r"(?:\s*(?://.*|/\*.*?\*/))?\s*$"
)


@dataclass(frozen=True)
class ResultEntry:
    entry: hd_assets.PackEntry
    source: str
    fork_index: int | None


def read_constants(path: Path) -> dict[int, str]:
    definitions: list[tuple[str, int]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        match = DEFINE_RE.match(line) or CONSTEXPR_RE.match(line)
        if match:
            definitions.append((match.group(1), int(match.group(2), 10)))

    if not definitions:
        raise ValueError(f"no graphic constants found in {path}")

    maximum = max(value for _, value in definitions)
    by_value: dict[int, list[str]] = {}
    for name, value in definitions:
        by_value.setdefault(value, []).append(name)

    for value in range(maximum + 1):
        names = by_value.get(value, [])
        if len(names) != 1:
            if names:
                raise ValueError(
                    f"duplicate constant value {value}: {', '.join(names)}"
                )
            raise ValueError(f"missing constant value {value}")

    return {value: by_value[value][0] for value in range(maximum + 1)}


def read_classic_without_hd(path: Path, output_name: str) -> list[str]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    names = value.get(output_name, [])
    if not isinstance(names, list) or any(not isinstance(name, str) for name in names):
        raise ValueError(
            f"classic-without-HD value for {output_name} must be a list of names"
        )
    return names


def entry_value(entry: hd_assets.PackEntry) -> tuple[str, str, bytes]:
    return entry.name, entry.extension, entry.payload


def align_entries(
    fork: list[hd_assets.PackEntry],
    classic: list[hd_assets.PackEntry],
    constants: dict[int, str],
    classic_without_hd: list[str],
) -> list[ResultEntry]:
    constant_names = set(constants.values())
    for entry in fork:
        if entry.index > max(constants) and entry.name in constant_names:
            raise ValueError(
                f"constant name {entry.name} at fork index {entry.index} "
                "appears after the last constant"
            )

    fork_by_name: dict[str, list[hd_assets.PackEntry]] = {}
    for entry in fork:
        fork_by_name.setdefault(entry.name, []).append(entry)

    used_fork: set[int] = set()
    used_classic_names: set[str] = set()
    result: list[ResultEntry] = []

    for index, name in constants.items():
        matching_fork = fork_by_name.get(name, [])
        if matching_fork:
            entry = matching_fork[0]
            used_fork.add(entry.index)
            result.append(ResultEntry(entry, "fork", entry.index))
            continue

        if name not in classic_without_hd:
            raise ValueError(
                f"no fork entry or classic-without-HD listing for "
                f"constant {name} at index {index}"
            )
        if index >= len(classic):
            raise ValueError(
                f"classic pack has no entry at index {index} for constant {name}"
            )

        classic_entry = classic[index]
        if classic_entry.name != name:
            raise ValueError(
                f"classic entry at index {index} is {classic_entry.name}, "
                f"expected {name}"
            )
        image = hd_assets.decode_image(classic_entry.payload)
        if image is None:
            raise ValueError(
                f"classic entry {name} at index {index} cannot be decoded as an image"
            )
        payload = hd_assets.encode_png(hd_assets.scale_image(image, 4))
        result.append(
            ResultEntry(
                hd_assets.PackEntry(index, name, classic_entry.extension, payload),
                "classic_x4",
                None,
            )
        )
        used_classic_names.add(name)

    for entry in fork:
        if entry.index > max(constants):
            if entry.name in constant_names:
                raise ValueError(
                    f"constant name {entry.name} at fork index {entry.index} "
                    "appears after the last constant"
                )
            used_fork.add(entry.index)
            result.append(ResultEntry(entry, "fork", entry.index))

    for entry in fork:
        if entry.index <= max(constants) and entry.index not in used_fork:
            used_fork.add(entry.index)
            result.append(ResultEntry(entry, "fork", entry.index))

    if used_fork != {entry.index for entry in fork}:
        raise ValueError("not every fork entry was placed exactly once")

    for entry in fork:
        if sum(item.fork_index == entry.index for item in result) != 1:
            raise ValueError(
                f"fork entry {entry.name} at index {entry.index} "
                "was not placed exactly once"
            )
        placed = next(item.entry for item in result if item.fork_index == entry.index)
        if entry_value(placed) != entry_value(entry):
            raise ValueError(
                f"fork entry {entry.name} at index {entry.index} changed during alignment"
            )

    seen_names: dict[str, int] = {}
    for index, item in enumerate(result):
        previous = seen_names.get(item.entry.name)
        if previous is not None:
            raise ValueError(
                f"duplicate result name {item.entry.name} at indices "
                f"{previous} and {index}"
            )
        seen_names[item.entry.name] = index

    unused_classic_names = [
        name for name in classic_without_hd if name not in used_classic_names
    ]
    if unused_classic_names:
        raise ValueError(
            "classic-without-HD names were not used: "
            + ", ".join(unused_classic_names)
        )

    return result


def result_report(entries: list[ResultEntry]) -> str:
    lines = ["index\tname\tsource\tfork_index\tsha256"]
    for index, item in enumerate(entries):
        fork_index = "-" if item.fork_index is None else str(item.fork_index)
        lines.append(
            "\t".join(
                (
                    str(index),
                    item.entry.name,
                    item.source,
                    fork_index,
                    hd_assets.sha256(item.entry.payload),
                )
            )
        )
    return "\n".join(lines) + "\n"


def write_outputs(
    output_path: Path,
    report_path: Path,
    fork_path: Path,
    fork: list[hd_assets.PackEntry],
    result: list[ResultEntry],
) -> None:
    result_entries = [item.entry for item in result]
    copy_fork = len(result_entries) == len(fork) and all(
        entry_value(left) == entry_value(right)
        for left, right in zip(result_entries, fork, strict=True)
    )
    destinations = (output_path, report_path)
    existed: dict[Path, bool] = {}
    for destination in destinations:
        try:
            mode = destination.lstat().st_mode
        except FileNotFoundError:
            existed[destination] = False
        else:
            if not stat.S_ISREG(mode):
                raise ValueError(
                    f"{destination}: destination exists and is not a regular file"
                )
            existed[destination] = True

    created_directories: list[Path] = []
    temporary_files: list[Path] = []
    installed_new_files: list[Path] = []

    def ensure_parent(directory: Path) -> None:
        missing: list[Path] = []
        current = directory
        while not current.exists():
            missing.append(current)
            parent = current.parent
            if parent == current:
                break
            current = parent
        if current.exists() and not current.is_dir():
            raise NotADirectoryError(f"{current} is not a directory")
        for path in reversed(missing):
            try:
                path.mkdir()
            except FileExistsError:
                if not path.is_dir():
                    raise
            else:
                created_directories.append(path)

    def make_temporary(destination: Path) -> Path:
        descriptor, name = tempfile.mkstemp(
            prefix=f".{destination.name}.",
            suffix=".tmp",
            dir=destination.parent,
        )
        temporary_path = Path(name)
        temporary_files.append(temporary_path)
        os.close(descriptor)
        return temporary_path

    try:
        ensure_parent(output_path.parent)
        ensure_parent(report_path.parent)

        temporary_output = make_temporary(output_path)
        if copy_fork:
            temporary_output.write_bytes(fork_path.read_bytes())
        else:
            hd_assets.write_pack(temporary_output, result_entries)

        temporary_report = make_temporary(report_path)
        temporary_report.write_bytes(result_report(result).encode("utf-8"))

        for temporary_path, destination in (
            (temporary_report, report_path),
            (temporary_output, output_path),
        ):
            os.replace(temporary_path, destination)
            if not existed[destination]:
                installed_new_files.append(destination)
    except Exception:
        for temporary_path in temporary_files:
            try:
                temporary_path.unlink(missing_ok=True)
            except OSError:
                pass
        for destination in installed_new_files:
            try:
                destination.unlink(missing_ok=True)
            except OSError:
                pass
        for directory in reversed(created_directories):
            try:
                directory.rmdir()
            except OSError:
                pass
        raise


def run(args: argparse.Namespace) -> int:
    fork_path = Path(args.fork_pack)
    classic_path = Path(args.classic_pack)
    header_path = Path(args.header)
    list_path = Path(args.list)
    output_path = Path(args.out)
    report_path = Path(args.report)

    try:
        constants = read_constants(header_path)
        without_hd = read_classic_without_hd(list_path, output_path.name)
        fork = hd_assets.read_pack(fork_path)
        classic = hd_assets.read_pack(classic_path)
        result = align_entries(fork, classic, constants, without_hd)
        write_outputs(output_path, report_path, fork_path, fork, result)
    except Exception as error:
        print(f"align_hd4_packs: {error}", file=sys.stderr)
        return 1
    return 0


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fork-pack", required=True)
    parser.add_argument("--classic-pack", required=True)
    parser.add_argument("--header", required=True)
    parser.add_argument("--list", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--report", required=True)
    return parser


def main() -> int:
    return run(make_parser().parse_args())


if __name__ == "__main__":
    raise SystemExit(main())
