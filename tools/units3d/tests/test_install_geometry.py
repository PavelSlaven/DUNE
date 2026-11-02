from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np
from PIL import Image

from tools.hd_assets import PackEntry, encode_png, read_pack, write_pack


ROOT = Path(__file__).resolve().parents[3]
SIEGE_NAMES = (
    "UNIT_SIEGEBASE",
    "UNIT_SIEGEBASE_SHADOW",
    "UNIT_SIEGETOP",
    "HM_UNIT_SIEGEBASE",
    "HM_UNIT_SIEGETOP",
)
OLD_SIEGE_SIZE = (1152, 152)
NEW_SIEGE_SIZE = (1408, 176)
FOREIGN_NAME = "UNIT_DEVASTATOR"
KEEP_NAME = "KEEP_SYNTH"


def _png(size: tuple[int, int], color: tuple[int, int, int, int]) -> bytes:
    image = np.zeros((size[1], size[0], 4), dtype=np.uint8)
    image[20:min(40, size[1]), 20:min(40, size[0])] = color
    return encode_png(Image.fromarray(image, "RGBA"))


def _write_source_pack(path: Path) -> tuple[int, int]:
    foreign_size = (1216, 192)
    entries = [
        PackEntry(index, name, "PNG", _png(OLD_SIEGE_SIZE, (70 + index, 60, 50, 255)))
        for index, name in enumerate(SIEGE_NAMES)
    ]
    entries.append(
        PackEntry(len(entries), FOREIGN_NAME, "PNG", _png(foreign_size, (80, 70, 60, 255)))
    )
    entries.append(PackEntry(len(entries), KEEP_NAME, "DAT", b"other payload stays byte for byte"))
    write_pack(path, entries)
    return foreign_size


def _write_atlases(directory: Path, sizes: dict[str, tuple[int, int]]) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    manifest: dict[str, dict[str, object]] = {}
    for index, (name, size) in enumerate(sizes.items()):
        filename = f"{name}.png"
        payload = _png(size, (20 + index, 160, 90, 255))
        (directory / filename).write_bytes(payload)
        manifest[name] = {
            "file": filename,
            "sha256": hashlib.sha256(payload).hexdigest(),
            "size": list(size),
        }
    (directory / "atlases.json").write_text(
        json.dumps({"entries": manifest}, indent=2) + "\n", encoding="utf-8"
    )


def _write_pack_unit(directory: Path, names: tuple[str, ...]) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    atlases: dict[str, str | None] = {"body": names[0], "house_mask": None, "shadow": None}
    for index, name in enumerate(names[1:], start=0):
        atlases[f"extra_{index}"] = name
    path = directory / "unit.json"
    path.write_text(json.dumps({"atlases": atlases}, indent=2) + "\n", encoding="utf-8")
    return directory


def _run_pack(unit: Path, atlases: Path, output: Path, source: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            "tools/units3d/redraw.py",
            "pack",
            str(unit),
            str(atlases),
            str(output),
            "--source",
            str(source),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
        timeout=1800,
    )


def _run_install(atlases: Path, pack: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "tools/units3d/install.py", "--atlases", str(atlases), "--pack", str(pack)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
        timeout=1800,
    )


def _pack_payloads(path: Path) -> tuple[list[tuple[int, str, str]], dict[str, bytes]]:
    entries = read_pack(path)
    return (
        [(entry.index, entry.name, entry.extension) for entry in entries],
        {entry.name: entry.payload for entry in entries},
    )


class InstallGeometryAcceptanceTests(unittest.TestCase):
    def test_pack_cli_geometry_policy(self) -> None:
        with tempfile.TemporaryDirectory(prefix="u9t1-pack-") as temporary:
            root = Path(temporary)
            base_pack = root / "base.dat"
            foreign_size = _write_source_pack(base_pack)
            base_before = base_pack.read_bytes()

            unit = _write_pack_unit(root / "unit-siege", SIEGE_NAMES)
            positive_atlases = root / "positive-atlases"
            _write_atlases(positive_atlases, {name: NEW_SIEGE_SIZE for name in SIEGE_NAMES})
            output = root / "installed.dat"
            with self.subTest(case="positive transition and repeat"):
                result = _run_pack(unit, positive_atlases, output, base_pack)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                first_signature, first_payloads = _pack_payloads(output)
                source_signature, source_payloads = _pack_payloads(base_pack)
                self.assertEqual(first_signature, source_signature)
                for name in SIEGE_NAMES:
                    self.assertEqual(first_payloads[name], (positive_atlases / f"{name}.png").read_bytes())
                for name in (FOREIGN_NAME, KEEP_NAME):
                    self.assertEqual(first_payloads[name], source_payloads[name])
                self.assertEqual(base_pack.read_bytes(), base_before)

                repeated = root / "repeated.dat"
                repeat_result = _run_pack(unit, positive_atlases, repeated, output)
                self.assertEqual(repeat_result.returncode, 0, repeat_result.stdout + repeat_result.stderr)
                self.assertEqual(_pack_payloads(repeated), _pack_payloads(output))

            failure_cases = (
                ("foreign_new_geometry", ((FOREIGN_NAME, NEW_SIEGE_SIZE),)),
                ("foreign_old_plus_one", ((FOREIGN_NAME, (foreign_size[0] + 1, foreign_size[1])),)),
                ("siege_tall", ((SIEGE_NAMES[0], (1408, 177)),)),
                ("siege_old_height", ((SIEGE_NAMES[0], (1152, 176)),)),
                (
                    "mixed_atomic",
                    ((SIEGE_NAMES[0], NEW_SIEGE_SIZE), (FOREIGN_NAME, (foreign_size[0] + 1, foreign_size[1]))),
                ),
            )
            for case, entries in failure_cases:
                with self.subTest(case=case):
                    source = root / f"{case}-source.dat"
                    shutil.copyfile(base_pack, source)
                    atlas_dir = root / f"{case}-atlases"
                    sizes = dict(entries)
                    _write_atlases(atlas_dir, sizes)
                    selected = tuple(sizes)
                    test_unit = _write_pack_unit(root / f"{case}-unit", selected)
                    destination = root / f"{case}-output.dat"
                    sentinel = f"existing output: {case}".encode("ascii")
                    destination.write_bytes(sentinel)
                    source_before = source.read_bytes()
                    output_before = destination.read_bytes()
                    rejected = _run_pack(test_unit, atlas_dir, destination, source)
                    self.assertNotEqual(rejected.returncode, 0, rejected.stdout + rejected.stderr)
                    self.assertEqual(source.read_bytes(), source_before)
                    self.assertEqual(destination.read_bytes(), output_before)
                    self.assertEqual(base_pack.read_bytes(), base_before)

    def test_install_cli_geometry_policy(self) -> None:
        with tempfile.TemporaryDirectory(prefix="u9t1-install-") as temporary:
            root = Path(temporary)
            base_pack = root / "base.dat"
            foreign_size = _write_source_pack(base_pack)
            base_before = base_pack.read_bytes()
            positive_atlases = root / "positive-atlases"
            _write_atlases(positive_atlases, {name: NEW_SIEGE_SIZE for name in SIEGE_NAMES})

            installed = root / "installed.dat"
            shutil.copyfile(base_pack, installed)
            with self.subTest(case="positive transition and repeat"):
                result = _run_install(positive_atlases, installed)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                first_signature, first_payloads = _pack_payloads(installed)
                source_signature, source_payloads = _pack_payloads(base_pack)
                self.assertEqual(first_signature, source_signature)
                for name in SIEGE_NAMES:
                    self.assertEqual(first_payloads[name], (positive_atlases / f"{name}.png").read_bytes())
                for name in (FOREIGN_NAME, KEEP_NAME):
                    self.assertEqual(first_payloads[name], source_payloads[name])

                repeated = _run_install(positive_atlases, installed)
                self.assertEqual(repeated.returncode, 0, repeated.stdout + repeated.stderr)
                self.assertEqual(_pack_payloads(installed), (first_signature, first_payloads))
                self.assertEqual(base_pack.read_bytes(), base_before)

            failure_cases = (
                ("foreign_new_geometry", ((FOREIGN_NAME, NEW_SIEGE_SIZE),)),
                ("foreign_old_plus_one", ((FOREIGN_NAME, (foreign_size[0] + 1, foreign_size[1])),)),
                ("siege_tall", ((SIEGE_NAMES[0], (1408, 177)),)),
                ("siege_old_height", ((SIEGE_NAMES[0], (1152, 176)),)),
                (
                    "mixed_atomic",
                    ((SIEGE_NAMES[0], NEW_SIEGE_SIZE), (FOREIGN_NAME, (foreign_size[0] + 1, foreign_size[1]))),
                ),
            )
            for case, entries in failure_cases:
                with self.subTest(case=case):
                    candidate = root / f"{case}-pack.dat"
                    shutil.copyfile(base_pack, candidate)
                    atlas_dir = root / f"{case}-atlases"
                    _write_atlases(atlas_dir, dict(entries))
                    before = candidate.read_bytes()
                    rejected = _run_install(atlas_dir, candidate)
                    self.assertNotEqual(rejected.returncode, 0, rejected.stdout + rejected.stderr)
                    self.assertEqual(candidate.read_bytes(), before)
                    self.assertEqual(base_pack.read_bytes(), base_before)
