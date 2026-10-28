from __future__ import annotations

import fnmatch
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
MANIFEST = ROOT / "docs/upstream/port_inventory.json"
GENERATOR = ROOT / "tools/upstream/port_inventory.py"
PORT_MAP = ROOT / "docs/upstream/PORT_MAP.md"
FEATURE_RULES = ROOT / "tools/upstream/port_features.json"

BASE_SHA = "e17379ad660fca46859b403a6c3d33ec8d831a40"
FORK_SHA = "6662b2f4857c679425ea2166092a21f4bde7d6e7"
UPSTREAM_SHA = "a51b97f15d0eee2d323a1737f140eb2cbd60973c"

FENCE_OPEN_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})")
INLINE_CODE_RE = re.compile(r"(?<!`)(`+)(?!`)(.*?)(?<!`)\1(?!`)")
LINE_SUFFIX_RE = re.compile(r":\d+(?:[-–—]\d+)?$")
LIST_SEPARATOR_RE = re.compile(r"\s*(?:[,;]|\band\b|\n)\s*", re.IGNORECASE)
MAP_FEATURE_RE = re.compile(r"^###\s+([a-z0-9][a-z0-9-]*)\s+—")
MAP_PATH_RE = re.compile(r"^\s*-\s+`([^`]+)`\s+—")
MAP_REMAINDER_RE = re.compile(
    r"^Остальные пути по каталогу второго уровня:\s*(.*?)\s*$"
)
MAP_COUNT_RE = re.compile(r"^(.+):\s*(\d+)$")

EXPECTED_PATH_FEATURES = {
    "src/gameobjects/structures/cWindTrap.cpp": ({"localization"}, {"hd-render"}),
    "src/gameobjects/structures/cHeavyFactory.cpp": ({"hd-render"}, {"localization"}),
    "src/gameobjects/structures/cLightFactory.cpp": (
        {"hd-render", "hd4-assets"},
        {"localization"},
    ),
    "src/include/definitions.h": ({"command-bar"}, {"hd-render"}),
    "src/gamestates/cMainMenuState.cpp": ({"save-slots"}, set()),
    "src/utils/GameSettings.hpp": ({"command-bar", "hd-render"}, set()),
    "src/gamestates/cOptionsState.cpp": ({"hd-render"}, set()),
    "src/gamestates/cOptionsState.h": ({"hd-render"}, set()),
    "src/drawers/cMiniMapDrawer.cpp": ({"adaptive-layout"}, set()),
    "src/drawers/cMessageDrawer.cpp": ({"adaptive-layout", "music-pools"}, set()),
    "src/drawers/cMouseDrawer.cpp": ({"localization"}, set()),
}


def run_git(*args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if check and result.returncode != 0:
        raise AssertionError(
            f"git {' '.join(args)} exited {result.returncode}: "
            f"{result.stderr.decode(errors='replace')}"
        )
    return result


def load_inventory() -> dict:
    with MANIFEST.open("r", encoding="utf-8") as source:
        data = json.load(source)
    if not isinstance(data, dict):
        raise AssertionError("port_inventory.json must contain a JSON object")
    return data


def revision_from(data: dict, name: str, expected: str) -> str:
    value = data.get(name)
    if not isinstance(value, str) or not value:
        raise AssertionError(f"inventory is missing its {name} SHA")

    resolved = run_git("rev-list", "-1", value).stdout.decode().strip()
    if resolved != expected:
        raise AssertionError(
            f"inventory {name} SHA resolves to {resolved}, expected {expected}"
        )
    return resolved


def tree_paths(revision: str) -> set[str]:
    result = run_git("ls-tree", "-r", "--full-tree", "--name-only", "-z", revision)
    return {item.decode(errors="surrogateescape") for item in result.stdout.split(b"\0") if item}


def diff_quiet(base: str, revision: str, path: str) -> int:
    result = run_git("diff", "--quiet", base, revision, "--", path, check=False)
    if result.returncode not in (0, 1):
        raise AssertionError(
            f"git diff --quiet {base} {revision} -- {path} exited "
            f"{result.returncode}: {result.stderr.decode(errors='replace')}"
        )
    return result.returncode


def changed_by_move_or_deletion(base: str, revision: str, paths: set[str]) -> bool:
    result = run_git(
        "diff", "--name-status", "--find-renames", "-z", base, revision, "--"
    )
    fields = result.stdout.split(b"\0")
    index = 0
    while index < len(fields) and fields[index]:
        status = fields[index].decode(errors="replace")
        index += 1
        if status.startswith(("R", "C")):
            old_path = fields[index].decode(errors="surrogateescape")
            new_path = fields[index + 1].decode(errors="surrogateescape")
            index += 2
            if status.startswith("R") and ({old_path, new_path} & paths):
                return True
        else:
            path = fields[index].decode(errors="surrogateescape")
            index += 1
            if status == "D" and path in paths:
                return True
    return False


def inline_code_spans(markdown: str) -> list[str]:
    visible_lines: list[str] = []
    fence_marker: str | None = None
    fence_length = 0

    for line in markdown.splitlines():
        opening = FENCE_OPEN_RE.match(line)
        if fence_marker is None:
            if opening:
                fence_marker = opening.group(1)[0]
                fence_length = len(opening.group(1))
            else:
                visible_lines.append(line)
            continue

        stripped = line.lstrip(" ")
        if len(line) - len(stripped) <= 3:
            run = re.match(re.escape(fence_marker) + r"+", stripped)
            if run and len(run.group(0)) >= fence_length and not stripped[run.end() :].strip():
                fence_marker = None
                fence_length = 0

    spans: list[str] = []
    for line in visible_lines:
        spans.extend(match.group(2) for match in INLINE_CODE_RE.finditer(line))
    return spans


def path_candidates(span: str, known_paths: set[str]) -> set[str]:
    candidates: set[str] = set()
    for part in LIST_SEPARATOR_RE.split(span):
        token = part.strip().strip("'\"`()[]{}<>")
        token = token.lstrip("-*• ").rstrip(",;.")
        if not token or token.startswith(("http://", "https://")):
            continue

        token = token.split("@", 1)[0]
        token = LINE_SUFFIX_RE.sub("", token)
        token = token.rstrip(",;.")
        if not token:
            continue

        if token in known_paths:
            candidates.add(token)
            continue
        if token in (".", "..") or re.fullmatch(r"\d+(?:\.\d+)*", token):
            continue

        if "/" in token or "\\" in token or ("." in token and not token.startswith("..")):
            candidates.add(token.replace("\\", "/"))
    return candidates


def feature_rules_by_id() -> dict[str, dict]:
    if not FEATURE_RULES.is_file():
        raise AssertionError(f"missing feature rules: {FEATURE_RULES}")
    data = json.loads(FEATURE_RULES.read_text(encoding="utf-8"))
    raw_rules = data.get("features") if isinstance(data, dict) else None
    if not isinstance(raw_rules, list):
        raise AssertionError("feature rules must contain a features list")
    rules: dict[str, dict] = {}
    for rule in raw_rules:
        if not isinstance(rule, dict) or not isinstance(rule.get("id"), str):
            raise AssertionError("each feature rule must be an object with a string id")
        rules[rule["id"]] = rule
    return rules


def _is_code_path(path: str) -> bool:
    return path == "CMakeLists.txt" or path.startswith(("src/", "tests/"))


def _fork_code_paths(data: dict) -> set[str]:
    paths = data.get("paths")
    if not isinstance(paths, dict):
        raise AssertionError("inventory paths must be an object")
    return {
        path
        for path, record in paths.items()
        if isinstance(path, str)
        and isinstance(record, dict)
        and record.get("fork") is not None
        and _is_code_path(path)
    }


def _changed_code_lines(data: dict) -> dict[str, list[str]]:
    base = data.get("base")
    fork = data.get("fork")
    if not isinstance(base, str) or not isinstance(fork, str):
        raise AssertionError("inventory must contain base and fork SHAs")

    paths = data.get("paths")
    if not isinstance(paths, dict):
        raise AssertionError("inventory paths must be an object")
    allowed_paths = _fork_code_paths(data)
    changed_lines: dict[str, list[str]] = {path: [] for path in allowed_paths}
    for path in sorted(allowed_paths):
        record = paths[path]
        fork_record = record["fork"]
        if not isinstance(fork_record, dict):
            raise AssertionError(f"inventory fork record for {path!r} must be an object")
        if fork_record.get("status") == "R":
            source_path = fork_record.get("source_path", path)
            target_path = fork_record.get("target_path", path)
            result = run_git(
                "diff",
                "-U0",
                f"{base}:{source_path}",
                f"{fork}:{target_path}",
            )
        else:
            result = run_git("diff", "-U0", base, fork, "--", path)

        for line in result.stdout.decode(errors="surrogateescape").splitlines():
            if line.startswith(("+++ ", "--- ")):
                continue
            if line.startswith(("+", "-")):
                changed_lines[path].append(line[1:])
    return changed_lines


def marker_coverage_errors(
    data: dict, rules: dict[str, dict], map_text: str
) -> list[str]:
    del map_text
    errors: list[str] = []
    paths = data.get("paths")
    if not isinstance(paths, dict):
        return ["inventory paths must be an object"]

    rule_ids = set(rules)
    for identifier, rule in rules.items():
        markers = rule.get("markers")
        if markers is None:
            markers = []
        elif isinstance(markers, str):
            markers = [markers]
        elif not isinstance(markers, list):
            errors.append(f"feature {identifier!r} markers must be a string list")
            markers = []

        code_paths = [
            path
            for path in _fork_code_paths(data)
            if identifier in (paths[path].get("features") or [])
        ]
        if code_paths and not markers:
            errors.append(f"feature {identifier!r} has code paths but no markers")

    try:
        changed_lines = _changed_code_lines(data)
    except (AssertionError, subprocess.SubprocessError) as error:
        return errors + [str(error)]

    hits: dict[str, set[str]] = {path: set() for path in changed_lines}
    valid_exceptions: set[tuple[str, str]] = set()
    for identifier, rule in rules.items():
        markers = rule.get("markers", [])
        if isinstance(markers, str):
            markers = [markers]
        if not isinstance(markers, list):
            continue

        for index, pattern in enumerate(markers):
            if not isinstance(pattern, str) or not pattern:
                errors.append(f"feature {identifier!r} marker {index} must be a nonempty string")
                continue
            try:
                marker = re.compile(pattern)
            except re.error as error:
                errors.append(f"feature {identifier!r} marker {pattern!r} is invalid: {error}")
                continue

            matched_paths = {
                path
                for path, lines in changed_lines.items()
                if any(marker.search(line) for line in lines)
            }
            if not matched_paths:
                errors.append(f"feature {identifier!r} marker {pattern!r} matches no changed code line")
            for path in matched_paths:
                hits[path].add(identifier)

        exceptions = rule.get("marker_exceptions", [])
        if exceptions is None:
            exceptions = []
        if not isinstance(exceptions, list):
            errors.append(f"feature {identifier!r} marker_exceptions must be a list")
            continue
        for index, exception in enumerate(exceptions):
            if not isinstance(exception, dict):
                errors.append(f"feature {identifier!r} marker exception {index} must be an object")
                continue
            path = exception.get("path")
            reason = exception.get("reason")
            if not isinstance(path, str) or path not in paths:
                errors.append(f"feature {identifier!r} marker exception {index} path must exist in inventory")
                continue
            if not isinstance(reason, str) or not reason.strip():
                errors.append(f"feature {identifier!r} marker exception for {path!r} needs a reason")
            if identifier not in hits.get(path, set()):
                errors.append(
                    f"feature {identifier!r} marker exception for {path!r} has no matching marker hit"
                )
            valid_exceptions.add((path, identifier))

    for path, marker_features in hits.items():
        record = paths.get(path)
        if not isinstance(record, dict):
            continue
        path_features = record.get("features", [])
        if not isinstance(path_features, list):
            errors.append(f"path {path!r} features must be a list to explain marker hits")
            path_features = []
        explained = set(path_features)
        pending = list(path_features)
        while pending:
            dependency_owner = pending.pop()
            dependency_rule = rules.get(dependency_owner)
            if not isinstance(dependency_rule, dict):
                continue
            dependencies = dependency_rule.get("depends_on", [])
            if not isinstance(dependencies, list):
                continue
            for dependency in dependencies:
                if dependency not in explained:
                    explained.add(dependency)
                    pending.append(dependency)
        for identifier in sorted(marker_features):
            if identifier not in rule_ids:
                continue
            if identifier not in explained and (path, identifier) not in valid_exceptions:
                errors.append(
                    f"marker hit for feature {identifier!r} in {path!r} is not explained by path features or an exception"
                )

    for path in changed_lines:
        record = paths.get(path)
        if not isinstance(record, dict):
            errors.append(f"changed code path {path!r} is missing from inventory")
            continue
        output_hits = record.get("marker_hits")
        expected_hits = sorted(hits[path])
        if not isinstance(output_hits, list) or output_hits != expected_hits:
            errors.append(
                f"marker_hits for {path!r} differ from git diff; "
                f"expected={expected_hits}, actual={output_hits!r}"
            )
    for path, record in paths.items():
        if isinstance(record, dict) and "marker_hits" in record and path not in changed_lines:
            errors.append(f"path {path!r} has marker_hits outside the changed code path set")
    return errors


def _directory_two_level(path: str) -> str:
    directories = path.split("/")[:-1]
    if not directories:
        return "корень"
    return "/".join(directories[:2])


def _parse_map_counts(line: str) -> dict[str, int] | None:
    match = MAP_REMAINDER_RE.match(line)
    if not match:
        return None
    body = match.group(1).rstrip(".")
    if body == "нет":
        return {}
    counts: dict[str, int] = {}
    for entry in body.split(";"):
        item = MAP_COUNT_RE.match(entry.strip())
        if not item:
            return {}
        counts[item.group(1).strip()] = int(item.group(2))
    return counts


def _parse_map_feature_sections(
    map_text: str,
) -> tuple[list[str], dict[str, set[str]], dict[str, dict[str, int]]]:
    identifiers: list[str] = []
    code_paths: dict[str, set[str]] = {}
    remainder_counts: dict[str, dict[str, int]] = {}
    current: str | None = None
    in_code_paths = False

    for line in map_text.splitlines():
        heading = MAP_FEATURE_RE.match(line)
        if heading:
            current = heading.group(1)
            identifiers.append(current)
            code_paths[current] = set()
            in_code_paths = False
            continue
        if current is None:
            continue
        if line.startswith("Пути кода и тестов"):
            in_code_paths = True
            continue
        counts = _parse_map_counts(line)
        if counts is not None:
            remainder_counts[current] = counts
            in_code_paths = False
            continue
        if in_code_paths:
            path = MAP_PATH_RE.match(line)
            if path:
                code_paths[current].add(path.group(1))
    return identifiers, code_paths, remainder_counts


def port_map_errors(data: dict, rules: dict[str, dict], map_text: str) -> list[str]:
    del rules
    errors: list[str] = []
    raw_features = data.get("features")
    paths = data.get("paths")
    if not isinstance(raw_features, list) or not isinstance(paths, dict):
        return ["inventory must contain feature and path collections"]

    expected_features: list[str] = []
    feature_paths: dict[str, set[str]] = {}
    for feature in raw_features:
        if not isinstance(feature, dict) or not isinstance(feature.get("id"), str):
            errors.append("each inventory feature must have a string id")
            continue
        identifier = feature["id"]
        expected_features.append(identifier)
        feature_paths[identifier] = set()
    for path, record in paths.items():
        if not isinstance(path, str) or not isinstance(record, dict) or record.get("fork") is None:
            continue
        identifiers = record.get("features", [])
        if not isinstance(identifiers, list):
            continue
        for identifier in identifiers:
            if identifier in feature_paths:
                feature_paths[identifier].add(path)

    map_ids, map_code_paths, map_counts = _parse_map_feature_sections(map_text)
    if len(map_ids) != len(expected_features) or sorted(map_ids) != sorted(expected_features):
        errors.append(
            "PORT_MAP feature sections must have the same number of entries and exact IDs as inventory"
        )

    for identifier in expected_features:
        expected_code = {path for path in feature_paths[identifier] if _is_code_path(path)}
        expected_counts: dict[str, int] = {}
        for path in feature_paths[identifier] - expected_code:
            directory = _directory_two_level(path)
            expected_counts[directory] = expected_counts.get(directory, 0) + 1

        actual_code = map_code_paths.get(identifier)
        if actual_code is None:
            errors.append(f"PORT_MAP is missing feature section {identifier!r}")
        elif actual_code != expected_code:
            missing = sorted(expected_code - actual_code)
            extra = sorted(actual_code - expected_code)
            errors.append(
                f"PORT_MAP code paths for {identifier!r} differ from inventory; "
                f"missing={missing}, extra={extra}"
            )
        actual_counts = map_counts.get(identifier)
        if actual_counts is None:
            errors.append(f"PORT_MAP is missing remainder counts for {identifier!r}")
        elif actual_counts != expected_counts:
            errors.append(
                f"PORT_MAP remainder counts for {identifier!r} differ from inventory; "
                f"expected={expected_counts}, actual={actual_counts}"
            )
    return errors


class PortInventoryTests(unittest.TestCase):
    def test_generator_output_matches_committed_inventory_byte_for_byte(self) -> None:
        self.assertTrue(GENERATOR.is_file(), f"missing generator: {GENERATOR}")
        self.assertTrue(MANIFEST.is_file(), f"missing committed inventory: {MANIFEST}")

        packs = os.environ.get("D2TM_PACK_DIR")
        if not packs:
            self.skipTest("D2TM_PACK_DIR is not set; pack-dependent inventory generation is skipped")
        with tempfile.TemporaryDirectory() as temporary_directory:
            generated = Path(temporary_directory) / "port_inventory.json"
            result = subprocess.run(
                [
                    sys.executable,
                    str(GENERATOR),
                    "--packs",
                    packs,
                    "--out",
                    str(generated),
                ],
                cwd=ROOT,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            self.assertEqual(
                result.returncode,
                0,
                result.stderr.decode(errors="replace"),
            )
            self.assertTrue(generated.is_file(), "generator did not write --out")
            self.assertEqual(generated.read_bytes(), MANIFEST.read_bytes())

    def test_feature_includes_dependencies_and_path_counts_are_consistent(self) -> None:
        data = load_inventory()
        paths = data.get("paths")
        self.assertIsInstance(paths, dict, "inventory paths must be an object")
        fork_paths = {
            path
            for path, record in paths.items()
            if isinstance(record, dict) and record.get("fork") is not None
        }
        self.assertTrue(fork_paths, "inventory contains no fork-changed paths")
        fork_tree_paths = tree_paths(FORK_SHA)
        current_fork_paths = fork_paths & fork_tree_paths
        self.assertTrue(current_fork_paths, "inventory contains no changed paths present in FORK")

        self.assertTrue(FEATURE_RULES.is_file(), f"missing feature rules: {FEATURE_RULES}")
        rules_data = json.loads(FEATURE_RULES.read_text(encoding="utf-8"))
        raw_rules = rules_data.get("features") if isinstance(rules_data, dict) else None
        self.assertIsInstance(raw_rules, list, "feature rules must contain a features list")
        raw_output = data.get("features")
        self.assertIsInstance(raw_output, list, "inventory features must be a list")

        rules: dict[str, dict] = {}
        for feature in raw_rules:
            self.assertIsInstance(feature, dict, "each feature rule must be an object")
            identifier = feature.get("id")
            self.assertIsInstance(identifier, str, "each feature rule must have a string id")
            self.assertNotIn(identifier, rules, f"duplicate feature rule id: {identifier}")
            rules[identifier] = feature

        features: dict[str, dict] = {}
        for feature in raw_output:
            self.assertIsInstance(feature, dict, "each inventory feature must be an object")
            self.assertNotIn("include", feature, "inventory feature must not contain include rules")
            self.assertNotIn("markers", feature, "inventory feature must not contain marker rules")
            self.assertNotIn(
                "marker_exceptions",
                feature,
                "inventory feature must not contain marker exception rules",
            )
            identifier = feature.get("id")
            self.assertIsInstance(identifier, str, "each inventory feature must have a string id")
            self.assertNotIn(identifier, features, f"duplicate inventory feature id: {identifier}")
            features[identifier] = feature

        self.assertTrue(rules, "feature rules contain no features")
        self.assertEqual(set(features), set(rules), "inventory features must match feature rule IDs")
        matched_by: dict[str, set[str]] = {path: set() for path in fork_paths}
        for identifier, rule in rules.items():
            with self.subTest(feature=identifier):
                include = rule.get("include")
                if isinstance(include, str):
                    include_patterns = [include]
                else:
                    self.assertIsInstance(include, list, "feature rule include must be a string or list")
                    include_patterns = include
                self.assertTrue(include_patterns, "feature must define at least one include pattern")

                feature_paths: set[str] = set()
                for pattern in include_patterns:
                    self.assertIsInstance(pattern, str, "feature include patterns must be strings")
                    current_matches = {
                        path for path in current_fork_paths
                        if fnmatch.fnmatchcase(path, pattern)
                    }
                    self.assertTrue(current_matches, f"include pattern {pattern!r} matches no path in FORK")
                    matches = {
                        path for path in fork_paths
                        if fnmatch.fnmatchcase(path, pattern)
                    }
                    feature_paths.update(matches)
                    for path in matches:
                        matched_by[path].add(identifier)

                feature = features[identifier]
                dependencies = feature.get("depends_on", [])
                self.assertIsInstance(dependencies, list, "feature depends_on must be a list")
                for dependency in dependencies:
                    self.assertIsInstance(dependency, str, "feature dependencies must be strings")
                    self.assertIn(dependency, features, f"unknown dependency {dependency!r}")

                paths_count = feature.get("paths_count")
                self.assertIs(type(paths_count), int, "feature paths_count must be an integer")
                self.assertGreater(paths_count, 0, "feature paths_count must be positive")
                self.assertEqual(
                    paths_count,
                    len(feature_paths),
                    "feature paths_count must equal the number of unique matched fork paths",
                )
                expected_metadata = {
                    key: value
                    for key, value in rule.items()
                    if key not in {"include", "markers", "marker_exceptions"}
                }
                expected_metadata["paths_count"] = paths_count
                self.assertEqual(feature, expected_metadata, "inventory feature must contain rule metadata and paths_count")

        uncovered = sorted(path for path, owners in matched_by.items() if not owners)
        self.assertEqual(uncovered, [], "fork-changed paths have no matching feature: " + ", ".join(uncovered))
        for path, record in paths.items():
            if record.get("fork") is None:
                self.assertNotIn("features", record, f"non-fork path {path!r} must not have features")
            elif path in fork_paths:
                self.assertEqual(
                    record.get("features"),
                    sorted(matched_by[path]),
                    f"path {path!r} must list every feature whose include rule matches it",
                )

    def test_port_map_is_at_most_80000_bytes(self) -> None:
        self.assertTrue(PORT_MAP.is_file(), f"missing port map: {PORT_MAP}")
        self.assertLessEqual(PORT_MAP.stat().st_size, 80000, "PORT_MAP.md exceeds 80000 bytes")

    def test_overlap_entries_match_real_git_diffs_on_both_sides(self) -> None:
        data = load_inventory()
        base = revision_from(data, "base", BASE_SHA)
        fork = revision_from(data, "fork", FORK_SHA)
        upstream = revision_from(data, "upstream", UPSTREAM_SHA)
        paths = data.get("paths")
        self.assertIsInstance(paths, dict, "inventory paths must be an object")

        overlap_paths = [path for path, record in paths.items() if record.get("overlap") is True]
        self.assertTrue(overlap_paths, "inventory contains no overlap=True paths")

        for path in overlap_paths:
            with self.subTest(path=path):
                record = paths[path]
                for side_name, revision in (("fork", fork), ("upstream", upstream)):
                    with self.subTest(path=path, side=side_name):
                        side = record.get(side_name)
                        self.assertIsInstance(
                            side,
                            dict,
                            f"overlap path {path!r} has no {side_name} record",
                        )
                        aliases = {path}
                        for alias_name in ("source_path", "target_path"):
                            alias = side.get(alias_name)
                            if alias:
                                self.assertIsInstance(alias, str)
                                aliases.add(alias)

                        direct_diff = diff_quiet(base, revision, path)
                        moved_or_deleted = False
                        if direct_diff == 0:
                            moved_or_deleted = changed_by_move_or_deletion(
                                base, revision, aliases
                            )
                        self.assertTrue(
                            direct_diff == 1 or moved_or_deleted,
                            f"overlap={path!r} is unchanged in {side_name} by actual Git diff",
                        )

    def test_inline_file_paths_in_port_map_exist_in_fork_or_upstream(self) -> None:
        self.assertTrue(PORT_MAP.is_file(), f"missing port map: {PORT_MAP}")
        data = load_inventory()
        fork = revision_from(data, "fork", FORK_SHA)
        upstream = revision_from(data, "upstream", UPSTREAM_SHA)
        known_paths = tree_paths(fork) | tree_paths(upstream)

        markdown = PORT_MAP.read_text(encoding="utf-8")
        references = {
            path
            for span in inline_code_spans(markdown)
            for path in path_candidates(span, known_paths)
        }
        self.assertTrue(references, "PORT_MAP.md contains no inline file paths")

        missing = sorted(references - known_paths)
        self.assertEqual(
            missing,
            [],
            "PORT_MAP.md references files absent from both historical Git trees: "
            + ", ".join(missing),
        )

    def test_marker_hits_are_explained_by_feature_paths(self) -> None:
        data = load_inventory()
        rules = feature_rules_by_id()
        markdown = PORT_MAP.read_text(encoding="utf-8")

        errors = marker_coverage_errors(data, rules, markdown)
        self.assertEqual(errors, [], "marker coverage errors:\n" + "\n".join(errors))

        paths = data["paths"]
        for path, (required, forbidden) in EXPECTED_PATH_FEATURES.items():
            with self.subTest(path=path):
                record = paths.get(path)
                self.assertIsInstance(record, dict, f"missing inventory path {path!r}")
                features = set(record.get("features", []))
                self.assertTrue(
                    required <= features,
                    f"{path!r} is missing expected features: {sorted(required - features)}",
                )
                self.assertTrue(
                    not forbidden & features,
                    f"{path!r} has forbidden features: {sorted(forbidden & features)}",
                )

    def test_port_map_feature_paths_and_counts_match_inventory(self) -> None:
        data = load_inventory()
        rules = feature_rules_by_id()
        markdown = PORT_MAP.read_text(encoding="utf-8")

        errors = port_map_errors(data, rules, markdown)
        self.assertEqual(errors, [], "PORT_MAP inventory errors:\n" + "\n".join(errors))


if __name__ == "__main__":
    unittest.main()
