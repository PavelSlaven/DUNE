#!/usr/bin/env python3
"""Build a deterministic inventory of the fork's changes against upstream."""

from __future__ import annotations

import argparse
import fnmatch
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path
from typing import Iterable


BASE = "e17379ad660fca46859b403a6c3d33ec8d831a40"
FORK = "6662b2f4857c679425ea2166092a21f4bde7d6e7"
UPSTREAM = "a51b97f15d0eee2d323a1737f140eb2cbd60973c"
ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT = ROOT / "docs" / "upstream" / "port_inventory.json"
FEATURES_PATH = ROOT / "tools" / "upstream" / "port_features.json"

PACKS = {
    "src/data/gfxdata.h": "sdl_data_hd4.dat",
    "src/data/gfxinter.h": "sdl_inter_hd4.dat",
    "src/data/gfxmentat.h": "sdl_mentat_hd4.dat",
    "src/data/gfxworld.h": "sdl_world_hd4.dat",
}

DEFINE_LINE = re.compile(r"^\s*#\s*define\s+([A-Za-z_][A-Za-z0-9_]*)(.*)$")
INTEGER_DEFINE = re.compile(
    r"^([+-]?(?:0[xX][0-9A-Fa-f]+|0[bB][01]+|0[0-7]+|[1-9][0-9]*|0))"
    r"(?:[uU](?:[lL]{0,2})?|[lL]{1,2}[uU]?|)$"
)
SDL_IDENTIFIER = re.compile(r"\b(?:SDL|Mix|MIX|IMG|TTF)_\w+")
SDL2_INCLUDE = re.compile(
    r"^\s*#\s*include\s*[<\"]([^>\"]*\bSDL2/[^>\"]+)[>\"]"
)


def git(*args: str, input_data: bytes | None = None) -> bytes:
    result = subprocess.run(
        ["git", "-C", str(ROOT), *args],
        input=input_data,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode:
        detail = result.stderr.decode("utf-8", "replace").strip()
        raise RuntimeError(f"git {' '.join(args)} failed: {detail}")
    return result.stdout


def decode_path(value: bytes) -> str:
    return value.decode("utf-8", "surrogateescape")


def parse_name_status(data: bytes) -> list[tuple[str, str, str | None]]:
    tokens = data.split(b"\0")
    result = []
    index = 0
    while index < len(tokens) and tokens[index]:
        status = tokens[index].decode("ascii", "replace")
        index += 1
        if status.startswith(("R", "C")):
            source = decode_path(tokens[index])
            destination = decode_path(tokens[index + 1])
            index += 2
            result.append(("R" if status.startswith("R") else "C", destination, source))
        else:
            path = decode_path(tokens[index])
            index += 1
            result.append((status[0], path, None))
    return result


def parse_numstat(data: bytes) -> dict[str, dict[str, int | bool | None]]:
    tokens = data.split(b"\0")
    result: dict[str, dict[str, int | bool | None]] = {}
    index = 0
    while index < len(tokens) and tokens[index]:
        columns = tokens[index].split(b"\t", 2)
        if len(columns) != 3:
            raise RuntimeError("unexpected git diff --numstat record")
        added_text, deleted_text, path_bytes = columns
        index += 1
        if path_bytes:
            paths = [decode_path(path_bytes)]
        else:
            paths = [decode_path(tokens[index]), decode_path(tokens[index + 1])]
            index += 2
        binary = added_text == b"-" or deleted_text == b"-"
        added = None if binary else int(added_text)
        deleted = None if binary else int(deleted_text)
        record = {"added": added, "deleted": deleted, "binary": binary}
        for path in paths:
            result[path] = record.copy()
    return result


def comparison(base: str, target: str) -> tuple[dict[str, dict], set[str]]:
    prefix = ("--no-ext-diff", "--no-textconv")
    changes = parse_name_status(
        git("diff", "--name-status", "-M", "-z", *prefix, base, target)
    )
    numstat = parse_numstat(
        git("diff", "--numstat", "-M", "-z", *prefix, base, target)
    )
    records: dict[str, dict] = {}
    touched: set[str] = set()
    for status, path, source in changes:
        stats = numstat.get(path) or (numstat.get(source) if source else None)
        if stats is None:
            stats = {"added": 0, "deleted": 0, "binary": False}
        record = {"status": status, **stats}
        touched.add(path)
        if status == "R" and source is not None:
            record["source_path"] = source
            touched.add(source)
            records[path] = record
            records[source] = {"status": "R", "target_path": path, **stats}
        else:
            records[path] = record
    return records, touched


def marker_code_path(path: str) -> bool:
    return path.startswith(("src/", "tests/")) or path == "CMakeLists.txt"


def fork_code_diffs(changes: dict[str, dict]) -> dict[str, str]:
    diffs: dict[str, str] = {}
    for path in sorted(changes):
        change = changes[path]
        if change.get("status") == "R":
            source = change.get("source_path")
            if source is None:
                continue
            if not (marker_code_path(path) or marker_code_path(source)):
                continue
            raw = git("diff", "-U0", f"{BASE}:{source}", f"{FORK}:{path}")
            patch = raw.decode("utf-8", "surrogateescape")
            for alias in (source, path):
                if marker_code_path(alias):
                    diffs[alias] = patch
            continue
        if not marker_code_path(path):
            continue
        raw = git("diff", "-U0", BASE, FORK, "--", path)
        diffs[path] = raw.decode("utf-8", "surrogateescape")
    return diffs


def changed_diff_lines(patch: str) -> list[str]:
    changed = []
    for line in patch.splitlines():
        if line.startswith(("+++ ", "--- ")):
            continue
        if line.startswith(("+", "-")):
            changed.append(line[1:])
    return changed


def marker_hits_by_path(
    diffs: dict[str, str], feature_rules: list[dict]
) -> dict[str, list[str]]:
    hits: dict[str, list[str]] = {}
    compiled = []
    for feature in feature_rules:
        markers = feature.get("markers", [])
        if not isinstance(markers, list) or any(not isinstance(marker, str) for marker in markers):
            raise RuntimeError(f"feature {feature.get('id')!r} markers must be a list of regex strings")
        for marker in markers:
            try:
                re.compile(marker)
            except re.error as error:
                raise RuntimeError(f"feature {feature.get('id')!r} has an invalid marker regex {marker!r}: {error}") from error
        compiled.append((feature["id"], markers))

    for path, patch in sorted(diffs.items()):
        lines = changed_diff_lines(patch)
        matches = []
        for feature_id, markers in compiled:
            if any(re.search(marker, line) for marker in markers for line in lines):
                matches.append(feature_id)
        hits[path] = sorted(matches)
    return hits


def commit_list() -> list[dict]:
    raw = git(
        "log",
        "--first-parent",
        "--reverse",
        "--format=%H%x00%cI%x00%s%x00",
        f"{BASE}..{FORK}",
    )
    fields = raw.split(b"\0")
    commits = []
    for index in range(0, len(fields) - 2, 3):
        sha = fields[index].strip(b"\r\n").decode("ascii")
        if not sha:
            continue
        date = fields[index + 1].strip().decode("ascii")
        subject = fields[index + 2].strip(b"\r\n").decode("utf-8", "surrogateescape")
        changed = parse_name_status(
            git(
                "diff",
                "--name-status",
                "-M",
                "-z",
                "--no-ext-diff",
                "--no-textconv",
                f"{sha}^1",
                sha,
            )
        )
        paths = sorted(
            {path for _, destination, source in changed for path in (destination, source) if path}
        )
        commits.append({"sha": sha, "date": date, "subject": subject, "paths": paths})
    return commits


def tree_entries(revision: str, pathspec: str) -> dict[str, str]:
    raw = git("ls-tree", "-r", "-z", "--full-tree", revision, "--", pathspec)
    entries: dict[str, str] = {}
    for record in raw.split(b"\0"):
        if not record:
            continue
        metadata, path_bytes = record.split(b"\t", 1)
        mode, kind, oid = metadata.decode("ascii").split(" ", 2)
        if kind == "blob" and mode != "160000":
            entries[decode_path(path_bytes)] = oid
    return entries


def cat_blobs(entries: dict[str, str]) -> dict[str, bytes]:
    if not entries:
        return {}
    paths = list(entries)
    request = b"".join(entries[path].encode("ascii") + b"\n" for path in paths)
    raw = git("cat-file", "--batch", input_data=request)
    result: dict[str, bytes] = {}
    offset = 0
    for path in paths:
        end = raw.find(b"\n", offset)
        if end < 0:
            raise RuntimeError("truncated git cat-file --batch response")
        header = raw[offset:end].split()
        offset = end + 1
        if len(header) != 3 or header[1] != b"blob":
            raise RuntimeError(f"unexpected git cat-file response for {path!r}")
        size = int(header[2])
        data = raw[offset:offset + size]
        if len(data) != size or raw[offset + size:offset + size + 1] != b"\n":
            raise RuntimeError(f"truncated git cat-file blob for {path!r}")
        result[path] = data
        offset += size + 1
    return result


def source_entries(revision: str) -> dict[str, str]:
    return tree_entries(revision, "src")


def load_sources(revision: str) -> dict[str, list[str]]:
    blobs = cat_blobs(source_entries(revision))
    return {
        path: data.decode("utf-8", "surrogateescape").splitlines()
        for path, data in blobs.items()
    }


def lfs_paths(paths: Iterable[str]) -> dict[str, bool]:
    materialized = list(paths)
    if not materialized:
        return {}
    payload = b"\0".join(path.encode("utf-8", "surrogateescape") for path in materialized) + b"\0"
    raw = git("check-attr", f"--source={FORK}", "--stdin", "-z", "filter", input_data=payload)
    fields = raw.split(b"\0")
    if fields and not fields[-1]:
        fields.pop()
    if len(fields) % 3:
        raise RuntimeError("unexpected git check-attr -z response")
    result = {}
    for index in range(0, len(fields), 3):
        path = decode_path(fields[index])
        attribute = fields[index + 1].decode("ascii", "replace")
        value = fields[index + 2].decode("ascii", "replace")
        if attribute == "filter":
            result[path] = value == "lfs"
    return {path: result.get(path, False) for path in materialized}


def parse_defines(sources: dict[str, list[str]]) -> dict[str, dict[str, dict]]:
    defines: dict[str, dict[str, dict]] = defaultdict(dict)
    for path in sorted(sources):
        if not re.fullmatch(r"src/data/[^/]+\.h", path):
            continue
        for line_number, line in enumerate(sources[path], start=1):
            match = DEFINE_LINE.match(line)
            if not match:
                continue
            name, remainder = match.groups()
            body = remainder.split("//", 1)[0].split("/*", 1)[0].strip()
            token = body.split(None, 1)[0] if body else ""
            integer = INTEGER_DEFINE.fullmatch(token)
            value = None
            if integer:
                literal = integer.group(1)
                unsigned = literal.lstrip("+-")
                if unsigned.lower().startswith("0x") or unsigned.lower().startswith("0b"):
                    value = int(literal, 0)
                elif len(unsigned) > 1 and unsigned.startswith("0"):
                    sign = -1 if literal.startswith("-") else 1
                    value = sign * int(unsigned, 8)
                else:
                    value = int(literal, 10)
            defines[path][name] = {
                "name": name,
                "value": value,
                "path": path,
                "line": line_number,
                "integer": value is not None,
            }
    return defines


def new_defines(
    base_defines: dict[str, dict[str, dict]],
    target_defines: dict[str, dict[str, dict]],
) -> list[dict]:
    added: list[dict] = []
    for path in sorted(target_defines):
        original_names = base_defines.get(path, {})
        for name, define in sorted(target_defines[path].items()):
            if name in original_names:
                continue
            if define["integer"]:
                added.append(define)
    return added


def id_collisions(
    base_defines: dict[str, dict[str, dict]],
    fork_defines: dict[str, dict[str, dict]],
    upstream_defines: dict[str, dict[str, dict]],
) -> list[dict]:
    fork_added = new_defines(base_defines, fork_defines)
    upstream_added = new_defines(base_defines, upstream_defines)
    upstream_by_header_value: dict[tuple[str, int], list[str]] = defaultdict(list)
    for define in upstream_added:
        if define["integer"]:
            upstream_by_header_value[(define["path"], define["value"])].append(define["name"])
    collisions = []
    for define in fork_added:
        if not define["integer"]:
            continue
        for upstream_name in upstream_by_header_value.get((define["path"], define["value"]), []):
            if define["name"] != upstream_name:
                collisions.append(
                    {
                        "kind": "define_pair",
                        "header": define["path"],
                        "value": define["value"],
                        "fork_name": define["name"],
                        "upstream_name": upstream_name,
                    }
                )
    return sorted(
        collisions,
        key=lambda item: (item["header"], item["value"], item["fork_name"], item["upstream_name"]),
    )


def lfs_oid(pointer: bytes, path: str) -> str:
    match = re.search(rb"(?m)^oid sha256:([0-9a-f]{64})$", pointer)
    if not match:
        raise RuntimeError(f"FORK pack is not a SHA-256 Git LFS pointer: {path}")
    return match.group(1).decode("ascii")


def load_pack_reader():
    module_path = ROOT / "tools" / "hd_assets.py"
    module_name = "port_inventory_hd_assets"
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load pack reader at {module_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module.read_pack


def read_verified_packs(
    fork_tree: dict[str, str],
    packs_dir: Path,
) -> tuple[dict[str, str], dict[str, dict[int, str]]]:
    pack_hashes: dict[str, str] = {}
    pack_entries: dict[str, dict[int, str]] = {}
    pack_paths = {
        pack_name: f"resources/bin/data/{pack_name}"
        for pack_name in PACKS.values()
    }
    pointer_blobs = cat_blobs(
        {path: fork_tree[path] for path in pack_paths.values() if path in fork_tree}
    )
    read_pack = load_pack_reader()
    for pack_name, path in sorted(pack_paths.items()):
        pointer = pointer_blobs.get(path)
        if pointer is None:
            raise RuntimeError(f"FORK pack is missing from the tree: {path}")
        expected = lfs_oid(pointer, path)
        pack_hashes[pack_name] = expected
        local_path = packs_dir / pack_name
        if not local_path.is_file():
            raise RuntimeError(f"verified pack is missing from --packs directory: {local_path}")
        actual = hashlib.sha256(local_path.read_bytes()).hexdigest()
        if actual != expected:
            raise RuntimeError(
                f"pack SHA-256 mismatch for {local_path}: expected {expected}, got {actual}"
            )
        entries = read_pack(local_path)
        pack_entries[pack_name] = {entry.index: entry.name for entry in entries}
    return pack_hashes, pack_entries


def pack_index_findings(
    upstream_new: list[dict],
    pack_entries: dict[str, dict[int, str]],
) -> list[dict]:
    findings: list[dict] = []
    for define in upstream_new:
        pack_name = PACKS.get(define["path"])
        if pack_name is None or not define["integer"]:
            continue
        entries = pack_entries.get(pack_name)
        if entries is None:
            continue
        entry_name = entries.get(define["value"])
        record = {
            "kind": "pack_index_missing" if entry_name is None else "pack_index_taken",
            "header": define["path"],
            "pack": pack_name,
            "define": define["name"],
            "value": define["value"],
            "fork_entry": entry_name,
        }
        if entry_name is None or entry_name != define["name"]:
            findings.append(record)
    return sorted(findings, key=lambda item: (item["header"], item["value"], item["define"], item["kind"]))


def source_tokens(lines: list[str]) -> tuple[dict[str, int], dict[str, int], dict[int, dict]]:
    identifiers: dict[str, int] = defaultdict(int)
    includes: dict[str, int] = defaultdict(int)
    line_records: dict[int, dict] = {}
    for line_number, line in enumerate(lines, start=1):
        line_identifiers = SDL_IDENTIFIER.findall(line)
        include_match = SDL2_INCLUDE.match(line)
        line_includes = [include_match.group(1)] if include_match else []
        for identifier in line_identifiers:
            identifiers[identifier] += 1
        for include in line_includes:
            includes[include] += 1
        if line_identifiers or line_includes:
            line_records[line_number] = {
                "identifiers": line_identifiers,
                "includes": line_includes,
            }
    return identifiers, includes, line_records


def sdl2_report(
    fork_sources: dict[str, list[str]],
    upstream_sources: dict[str, list[str]],
    fork_changes: dict[str, dict],
) -> tuple[dict[str, dict], int]:
    confirmed: set[str] = set()
    for lines in upstream_sources.values():
        identifiers, includes, _ = source_tokens(lines)
        confirmed.update(identifiers)
        confirmed.update(includes)

    files: dict[str, dict] = {}
    total_lines = 0
    for path in sorted(fork_changes):
        change = fork_changes[path]
        if (
            change.get("status") not in {"A", "M", "R"}
            or not path.startswith("src/")
            or path not in fork_sources
        ):
            continue
        identifiers, includes, line_records = source_tokens(fork_sources[path])
        remaining = sorted(
            {name for name in identifiers if name not in confirmed}
            | {name for name in includes if name not in confirmed}
        )
        line_count = sum(
            any(name not in confirmed for name in line_record["identifiers"] + line_record["includes"])
            for line_record in line_records.values()
        )
        if line_count:
            files[path] = {
                "identifiers": remaining,
                "lines": line_count,
            }
        total_lines += line_count
    return files, total_lines


def load_feature_metadata(paths: dict[str, dict], code_diffs: dict[str, str]) -> list[dict]:
    if not FEATURES_PATH.is_file():
        raise RuntimeError(f"missing feature input: {FEATURES_PATH}")
    payload = json.loads(FEATURES_PATH.read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or not isinstance(payload.get("features"), list):
        raise RuntimeError("port_features.json must contain a features array")
    features = []
    for feature in payload["features"]:
        required = (
            "id",
            "title",
            "source",
            "port_class",
            "depends_on",
            "steps",
            "include",
            "markers",
            "marker_exceptions",
        )
        if not isinstance(feature, dict) or any(field not in feature for field in required):
            raise RuntimeError(
                "each port feature must contain id, title, source, port_class, depends_on, steps, include, markers, marker_exceptions"
            )
        patterns = feature["include"]
        if not isinstance(patterns, list) or any(not isinstance(pattern, str) for pattern in patterns):
            raise RuntimeError(f"feature {feature.get('id')!r} include must be a list of glob strings")
        exceptions = feature.get("marker_exceptions", [])
        if not isinstance(exceptions, list) or any(
            not isinstance(exception, dict)
            or not isinstance(exception.get("path"), str)
            or not isinstance(exception.get("reason"), str)
            for exception in exceptions
        ):
            raise RuntimeError(f"feature {feature.get('id')!r} marker_exceptions must contain path and reason strings")
        feature_id = feature["id"]
        matched_paths = sorted(
            path
            for path, record in paths.items()
            if record["fork"] is not None
            and any(fnmatch.fnmatchcase(path, pattern) for pattern in patterns)
        )
        for path in matched_paths:
            paths[path].setdefault("features", []).append(feature_id)
        features.append(
            {
                key: value
                for key, value in feature.items()
                if key not in {"include", "markers", "marker_exceptions"}
            }
            | {"paths_count": len(matched_paths)}
        )
    for path, matches in marker_hits_by_path(code_diffs, payload["features"]).items():
        paths[path]["marker_hits"] = matches
    for record in paths.values():
        if "features" in record:
            record["features"] = sorted(set(record["features"]))
    return features


def build_inventory(packs_dir: Path) -> dict:
    merge_base = git("merge-base", FORK, UPSTREAM).decode("ascii").strip()
    if merge_base != BASE:
        raise RuntimeError(f"unexpected merge base: {merge_base}")

    fork_changes, fork_touched = comparison(BASE, FORK)
    upstream_changes, upstream_touched = comparison(BASE, UPSTREAM)
    all_paths = sorted(fork_touched | upstream_touched)
    lfs = lfs_paths(all_paths)
    paths = {
        path: {
            "fork": fork_changes.get(path),
            "upstream": upstream_changes.get(path),
            "overlap": path in fork_touched and path in upstream_touched,
            "lfs": lfs[path],
        }
        for path in all_paths
    }

    base_sources = load_sources(BASE)
    fork_sources = load_sources(FORK)
    upstream_sources = load_sources(UPSTREAM)
    base_defines = parse_defines(base_sources)
    fork_defines = parse_defines(fork_sources)
    upstream_defines = parse_defines(upstream_sources)
    upstream_new = new_defines(base_defines, upstream_defines)

    fork_tree = tree_entries(FORK, "resources/bin/data")
    packs, pack_entries = read_verified_packs(fork_tree, packs_dir)
    pack_findings = pack_index_findings(upstream_new, pack_entries)
    collisions = id_collisions(base_defines, fork_defines, upstream_defines) + pack_findings
    collisions.sort(
        key=lambda item: (
            item["kind"],
            item["header"],
            item["value"],
            item.get("fork_name", item.get("define", "")),
            item.get("upstream_name", item.get("fork_entry") or ""),
        )
    )

    code_diffs = fork_code_diffs(fork_changes)
    features = load_feature_metadata(paths, code_diffs)
    sdl2_in_fork_code, sdl2_lines_total = sdl2_report(fork_sources, upstream_sources, fork_changes)
    return {
        "base": BASE,
        "fork": FORK,
        "upstream": UPSTREAM,
        "snapshot_method": "Committed source blobs read from the Git object database with git cat-file --batch.",
        "paths": paths,
        "fork_commits": commit_list(),
        "id_collisions": collisions,
        "features": features,
        "packs": packs,
        "sdl2_in_fork_code": sdl2_in_fork_code,
        "sdl2_lines_total": sdl2_lines_total,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate the deterministic fork/upstream port inventory.")
    parser.add_argument("--packs", type=Path, required=True, help="directory containing verified HD4 packs")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUTPUT, help="JSON output path")
    args = parser.parse_args()
    output = args.out if args.out.is_absolute() else ROOT / args.out
    packs_dir = args.packs if args.packs.is_absolute() else ROOT / args.packs
    inventory = build_inventory(packs_dir)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(inventory, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
