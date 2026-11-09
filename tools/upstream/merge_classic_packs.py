from __future__ import annotations

import argparse
import csv
import io
import os
import stat
import sys
import tempfile
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

from tools import hd_assets


REPORT_HEADER = ("pack", "index", "key", "fork", "upstream", "source")


@dataclass(frozen=True)
class Record:
    key: str
    entry: hd_assets.PackEntry
    index: int


@dataclass
class PlannedOutput:
    relative: Path
    copied_data: bytes | None = None
    merged_entries: list[hd_assets.PackEntry] | None = None
    fork_entries: list[hd_assets.PackEntry] | None = None
    upstream_entries: list[hd_assets.PackEntry] | None = None
    upstream_data: bytes | None = None
    fork_data: bytes | None = None


def is_excluded(relative: Path) -> bool:
    parts = relative.parts
    return relative.name.endswith("_hd4.dat") or any(
        parts[index:index + 2] == ("scenes", "hd4")
        for index in range(len(parts) - 1)
    )


def discover(root: Path) -> dict[str, Path]:
    if not root.is_dir():
        raise OSError(f"input directory does not exist: {root}")
    result: dict[str, Path] = {}
    for path in root.rglob("*.dat"):
        if not path.is_file():
            continue
        relative = path.relative_to(root)
        if not is_excluded(relative):
            result[relative.as_posix()] = path
    return result


def records(entries: list[hd_assets.PackEntry]) -> tuple[list[Record], dict[str, Record]]:
    occurrences: defaultdict[str, int] = defaultdict(int)
    ordered: list[Record] = []
    keyed: dict[str, Record] = {}
    for index, entry in enumerate(entries):
        occurrences[entry.name] += 1
        record = Record(f"{entry.name}#{occurrences[entry.name]}", entry, index)
        ordered.append(record)
        keyed[record.key] = record
    return ordered, keyed


def entry_equal(left: hd_assets.PackEntry, right: hd_assets.PackEntry) -> bool:
    return (
        left.name == right.name
        and left.extension == right.extension
        and left.payload == right.payload
    )


def entries_equal(
    left: list[hd_assets.PackEntry],
    right: list[hd_assets.PackEntry],
) -> bool:
    return len(left) == len(right) and all(
        entry_equal(left_entry, right_entry)
        for left_entry, right_entry in zip(left, right, strict=True)
    )


def tsv_text(rows: list[tuple[object, ...]]) -> str:
    output = io.StringIO(newline="")
    writer = csv.writer(output, delimiter="\t", lineterminator="\n")
    writer.writerows(rows)
    return output.getvalue()


def ensure_parent_directory(path: Path, created_directories: list[Path]) -> None:
    missing: list[Path] = []
    parent = path.parent
    while not parent.exists():
        missing.append(parent)
        if parent == parent.parent:
            break
        parent = parent.parent
    for directory in reversed(missing):
        directory.mkdir()
        created_directories.append(directory)


def validate_destinations(destinations: list[Path]) -> None:
    for destination in destinations:
        try:
            mode = destination.lstat().st_mode
        except FileNotFoundError:
            continue
        if not stat.S_ISREG(mode):
            raise ValueError(f"{destination}: destination is not a regular file")


def write_outputs(
    outputs: list[tuple[Path, bytes]],
    report_path: Path,
) -> None:
    destinations = [destination for destination, _ in outputs]
    validate_destinations(destinations)

    existed_before = {destination for destination in destinations if os.path.lexists(destination)}
    created_directories: list[Path] = []
    temporary_files: list[Path] = []
    installed_destinations: list[Path] = []
    try:
        staged: list[tuple[Path, Path]] = []
        for destination, data in outputs:
            ensure_parent_directory(destination, created_directories)
            descriptor, temporary_name = tempfile.mkstemp(
                prefix=f".{destination.name}.",
                suffix=".tmp",
                dir=destination.parent,
            )
            temporary = Path(temporary_name)
            temporary_files.append(temporary)
            with os.fdopen(descriptor, "wb") as output:
                output.write(data)
            staged.append((destination, temporary))

        staged.sort(key=lambda item: item[0] != report_path)
        for destination, temporary in staged:
            os.replace(temporary, destination)
            temporary_files.remove(temporary)
            installed_destinations.append(destination)
    except Exception:
        for temporary in temporary_files:
            try:
                temporary.unlink(missing_ok=True)
            except OSError:
                pass
        for destination in installed_destinations:
            if destination not in existed_before:
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


def whole_file_plan(relative: Path, source: Path, label: str) -> tuple[PlannedOutput, tuple[object, ...]]:
    data = source.read_bytes()
    return (
        PlannedOutput(relative=relative, copied_data=data),
        (relative.as_posix(), "-", "-", "-", "-", label),
    )


def has_d2tm_signature(path: Path) -> bool:
    with path.open("rb") as source:
        return source.read(4) == b"D2TM"


def merge_one(
    relative: Path,
    base_path: Path,
    fork_path: Path,
    upstream_path: Path,
) -> tuple[PlannedOutput, list[tuple[object, ...]]]:
    label = relative.as_posix()
    try:
        base_data = base_path.read_bytes()
        fork_data = fork_path.read_bytes()
        upstream_data = upstream_path.read_bytes()
        base_entries = hd_assets.read_pack(base_path)
        fork_entries = hd_assets.read_pack(fork_path)
        upstream_entries = hd_assets.read_pack(upstream_path)
    except Exception as error:
        raise ValueError(f"{label}: cannot read pack: {error}") from error

    _, base = records(base_entries)
    _, fork = records(fork_entries)
    upstream_order, upstream = records(upstream_entries)

    structural_errors: list[str] = []
    if set(fork) != set(base):
        added = sorted(set(fork) - set(base))
        deleted = sorted(set(base) - set(fork))
        details = []
        if added:
            details.append("added: " + ", ".join(added))
        if deleted:
            details.append("deleted: " + ", ".join(deleted))
        suffix = " (" + "; ".join(details) + ")" if details else ""
        structural_errors.append("fork added or deleted records" + suffix)
    reordered = sorted(
        key for key in set(base) & set(fork)
        if base[key].index != fork[key].index
    )
    if reordered:
        structural_errors.append("fork reordered records: " + ", ".join(reordered))
    if structural_errors:
        raise ValueError(f"{label}: " + "; ".join(structural_errors))

    fork_changed = {
        key: not entry_equal(fork[key].entry, base[key].entry)
        for key in base
    }
    upstream_changed = {
        key: key not in upstream or not entry_equal(upstream[key].entry, base[key].entry)
        for key in base
    }
    conflicts = sorted(
        key for key in base
        if fork_changed[key]
        and upstream_changed[key]
        and (key not in upstream or not entry_equal(fork[key].entry, upstream[key].entry))
    )
    if conflicts:
        raise ValueError(f"{label}: conflicting records: " + ", ".join(conflicts))

    merged: list[hd_assets.PackEntry] = []
    rows: list[tuple[object, ...]] = []
    for record in upstream_order:
        key = record.key
        fork_did_change = key in fork_changed and fork_changed[key]
        upstream_added = key not in base
        upstream_did_change = not upstream_added and upstream_changed[key]
        if fork_did_change:
            selected = fork[key].entry
            source = "fork"
        elif upstream_added or upstream_did_change:
            selected = record.entry
            source = "upstream"
        else:
            selected = record.entry
            source = "base"
        merged.append(selected)
        rows.append((
            label,
            len(merged) - 1,
            key,
            "changed" if fork_did_change else "unchanged",
            "added" if upstream_added else ("changed" if upstream_did_change else "unchanged"),
            source,
        ))

    return (
        PlannedOutput(
            relative=relative,
            merged_entries=merged,
            fork_entries=fork_entries,
            upstream_entries=upstream_entries,
            upstream_data=upstream_data,
            fork_data=fork_data,
        ),
        rows,
    )


def run(args: argparse.Namespace) -> int:
    base_dir = Path(args.base_dir)
    fork_dir = Path(args.fork_dir)
    upstream_dir = Path(args.upstream_dir)
    out_dir = Path(args.out_dir)
    report_path = Path(args.report)

    try:
        base_files = discover(base_dir)
        fork_files = discover(fork_dir)
        upstream_files = discover(upstream_dir)
    except OSError as error:
        print(str(error), file=sys.stderr)
        return 1

    paths = sorted(set(base_files) | set(fork_files) | set(upstream_files))
    plans: list[PlannedOutput] = []
    report_rows: list[tuple[object, ...]] = [REPORT_HEADER]
    errors: list[str] = []

    for name in paths:
        relative = Path(name)
        base_path = base_files.get(name)
        fork_path = fork_files.get(name)
        upstream_path = upstream_files.get(name)
        try:
            present_paths = [
                path for path in (base_path, fork_path, upstream_path)
                if path is not None
            ]
            if not any(has_d2tm_signature(path) for path in present_paths):
                if (
                    base_path is not None
                    and fork_path is not None
                    and upstream_path is not None
                    and base_path.read_bytes()
                    == fork_path.read_bytes()
                    == upstream_path.read_bytes()
                ):
                    continue
                errors.append(f"{name}: не пак D2TM")
                continue

            if base_path is None:
                if fork_path is None:
                    assert upstream_path is not None
                    plan, row = whole_file_plan(relative, upstream_path, "upstream-file")
                elif upstream_path is None:
                    plan, row = whole_file_plan(relative, fork_path, "fork-file")
                else:
                    fork_data = fork_path.read_bytes()
                    upstream_data = upstream_path.read_bytes()
                    if fork_data != upstream_data:
                        raise ValueError(f"{name}: pack exists in fork and upstream without a base and files differ")
                    plan = PlannedOutput(relative=relative, copied_data=upstream_data)
                    row = (name, "-", "-", "-", "-", "upstream-file")
                plans.append(plan)
                report_rows.append(row)
                continue

            if fork_path is None:
                raise ValueError(f"{name}: pack deleted by fork")
            if upstream_path is None:
                raise ValueError(f"{name}: pack deleted by upstream")

            plan, rows = merge_one(relative, base_path, fork_path, upstream_path)
            plans.append(plan)
            report_rows.extend(rows)
        except (OSError, ValueError) as error:
            errors.append(str(error))

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    destinations = [out_dir / plan.relative for plan in plans] + [report_path]
    try:
        validate_destinations(destinations)
    except (OSError, ValueError) as error:
        print(f"cannot write merge results: {error}", file=sys.stderr)
        return 1

    temporary_root = Path.cwd() / ".tmp" / "p2"
    try:
        temporary_root.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="merge-classic-packs-", dir=temporary_root) as temporary:
            temporary_dir = Path(temporary)
            for plan in plans:
                if plan.merged_entries is None:
                    continue
                assert plan.upstream_entries is not None
                assert plan.fork_entries is not None
                if entries_equal(plan.merged_entries, plan.upstream_entries):
                    plan.copied_data = plan.upstream_data
                elif entries_equal(plan.merged_entries, plan.fork_entries):
                    plan.copied_data = plan.fork_data
                else:
                    staged_pack = temporary_dir / plan.relative
                    hd_assets.write_pack(staged_pack, plan.merged_entries)
                    plan.copied_data = staged_pack.read_bytes()
    except Exception as error:
        print(f"cannot prepare merged packs: {error}", file=sys.stderr)
        return 1

    outputs: list[tuple[Path, bytes]] = []
    for plan in plans:
        destination = out_dir / plan.relative
        assert plan.copied_data is not None
        outputs.append((destination, plan.copied_data))
    outputs.append((report_path, tsv_text(report_rows).encode("utf-8")))
    try:
        write_outputs(outputs, report_path)
    except (OSError, ValueError) as error:
        print(f"cannot write merge results: {error}", file=sys.stderr)
        return 1
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-dir", required=True)
    parser.add_argument("--fork-dir", required=True)
    parser.add_argument("--upstream-dir", required=True)
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--report", required=True)
    return parser


def main() -> int:
    return run(build_parser().parse_args())


if __name__ == "__main__":
    raise SystemExit(main())
