from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path
from copy import deepcopy

import numpy as np
from PIL import Image

from tools.hd_assets import encode_png, read_pack, write_pack
from tools.units3d.tests.test_check_unit import Fixture, run_checker


ROOT = Path(__file__).resolve().parents[3]
SIEGE_NAMES = (
    "UNIT_SIEGEBASE",
    "UNIT_SIEGEBASE_SHADOW",
    "UNIT_SIEGETOP",
    "HM_UNIT_SIEGEBASE",
    "HM_UNIT_SIEGETOP",
)
SIZE_FIELDS = (
    "classic_size",
    "hd4_size",
    "frame_classic",
    "frame_hd4",
    "columns",
    "rows",
    "remainder_px",
)


def _transparent_atlas() -> bytes:
    pixels = np.zeros((176, 1408, 4), dtype=np.uint8)
    for k in range(8):
        pixels[60:70, k * 176 + 40:k * 176 + 140] = (80, 65, 48, 255)
    return encode_png(Image.fromarray(pixels, "RGBA"))


def _padding_frames(frames: np.ndarray) -> np.ndarray:
    padded = np.zeros((frames.shape[0], 176, 176, 4), dtype=np.uint8)
    inset = (176 - frames.shape[1]) // 2
    padded[:, inset:inset + frames.shape[1], inset:inset + frames.shape[2]] = frames
    return padded


def _prepare_checker_fixture(
    fixture: Fixture,
    body_name: str,
    *,
    contract_new_geometry: bool,
    baseline: dict[str, dict[str, object]] | None = None,
) -> None:
    rename = {
        "UNIT_SYNTH_BODY": body_name,
        "UNIT_SYNTH_SHADOW": "UNIT_SIEGEBASE_SHADOW" if body_name == "UNIT_SIEGEBASE" else f"{body_name}_SHADOW",
        "HM_SYNTH_BODY": "HM_UNIT_SIEGEBASE" if body_name == "UNIT_SIEGEBASE" else f"HM_{body_name}",
    }
    fixture.entries = tuple(rename[name] for name in fixture.entries)
    fixture.entry_files = {name: f"{name}.png" for name in fixture.entries}
    fixture.atlas_frames = {
        rename[name]: _padding_frames(frames)
        for name, frames in fixture.atlas_frames.items()
    }
    fixture.render_frames = {
        key: _padding_frames(frames) for key, frames in fixture.render_frames.items()
    }
    body_part = fixture.unit_data["parts"]["body"]
    body_part["atlas"] = rename["UNIT_SYNTH_BODY"]
    body_part["shadow"] = rename["UNIT_SYNTH_SHADOW"]
    body_part["mask"] = rename["HM_SYNTH_BODY"]
    fixture.unit_data["frame_hd4"] = [176, 176]
    fixture.unit_data["atlas_hd4"] = [1408, 176]
    fixture.manifest_data["frame_hd4"] = [176, 176]
    for bounds_by_frame in fixture.manifest_data["bbox_hd4"].values():
        for bounds in bounds_by_frame.values():
            bounds[:] = [value + 24 for value in bounds]
    if contract_new_geometry:
        for entry in fixture.contract_data["entries"]:
            entry["name"] = rename[entry["name"]]
            if entry["house_mask"] is not None:
                entry["house_mask"] = rename[entry["house_mask"]]
            entry["frame_hd4"] = [176, 176]
            entry["hd4_size"] = [1408, 176]
    else:
        if baseline is None:
            raise AssertionError("foreign checker case requires baseline contract records")
        fixture.contract_data["entries"] = [deepcopy(baseline[name]) for name in fixture.entries]
    fixture.atlases_data = fixture._atlases_data()
    for entry in fixture.atlases_data["entries"].values():
        entry["size"] = [1408, 176]
    for path in fixture.atlases_dir.glob("*.png"):
        path.unlink()
    fixture.commit()


class SiegeContractAcceptanceTests(unittest.TestCase):
    def test_generator_and_checker_siege_geometry(self) -> None:
        with tempfile.TemporaryDirectory(prefix="u9t1-contract-") as temporary:
            root = Path(temporary)
            source_dir = Path(os.environ["D2TM_PACK_DIR"])
            pack_dir = root / "packs"
            pack_dir.mkdir()
            shutil.copyfile(source_dir / "sdl_data.dat", pack_dir / "sdl_data.dat")
            original_hd = read_pack(source_dir / "sdl_data_hd4.dat")
            synthetic = _transparent_atlas()
            write_pack(
                pack_dir / "sdl_data_hd4.dat",
                [replace(entry, payload=synthetic) if entry.name in SIEGE_NAMES else entry for entry in original_hd],
            )
            output_dir = root / "generated"
            result = subprocess.run(
                [
                    sys.executable,
                    "tools/units3d/unit_contract.py",
                    "--pack-dir",
                    str(pack_dir),
                    "--output-dir",
                    str(output_dir),
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
                encoding="utf-8",
                check=False,
                timeout=1800,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            generated = json.loads((output_dir / "unit_contract.json").read_text(encoding="utf-8"))
            generated_by_name = {entry["name"]: entry for entry in generated["entries"]}

            old_contract_result = subprocess.run(
                ["git", "show", "bb2f1b37:docs/units/unit_contract.json"],
                cwd=ROOT,
                capture_output=True,
                text=True,
                encoding="utf-8",
                check=False,
                timeout=30,
            )
            self.assertEqual(old_contract_result.returncode, 0, old_contract_result.stderr)
            old_contract = json.loads(old_contract_result.stdout)
            old_by_name = {entry["name"]: entry for entry in old_contract["entries"]}

            with self.subTest(contract="siege geometry"):
                for name in SIEGE_NAMES:
                    entry = generated_by_name[name]
                    self.assertEqual(entry["frame_classic"], [36, 36], name)
                    self.assertEqual(entry["frame_hd4"], [176, 176], name)
                    self.assertEqual(entry["hd4_size"], [1408, 176], name)
                    self.assertEqual(entry["columns"], 8, name)
                    self.assertEqual(entry["rows"], 1, name)
                    self.assertEqual(entry["remainder_px"], [0, 0], name)

            with self.subTest(contract="other entries retain baseline geometry"):
                self.assertEqual(set(generated_by_name), set(old_by_name))
                for name, previous in old_by_name.items():
                    if name in SIEGE_NAMES:
                        continue
                    self.assertEqual(
                        {field: generated_by_name[name][field] for field in SIZE_FIELDS},
                        {field: previous[field] for field in SIZE_FIELDS},
                        name,
                    )

        with self.subTest(checker="accepts Siege profile and contract"):
            fixture = Fixture(case="Siege profile with updated frame geometry")
            with fixture:
                _prepare_checker_fixture(fixture, "UNIT_SIEGEBASE", contract_new_geometry=True)
                checked = run_checker(fixture)
                self.assertEqual(checked.exit_code, 0, checked.stdout + checked.stderr)
                self.assertEqual(set(checked.statuses.values()), {"PASS"})

        with self.subTest(checker="rejects foreign profile with the old contract"):
            fixture = Fixture(case="foreign unit has Siege geometry but an unchanged contract")
            with fixture:
                _prepare_checker_fixture(
                    fixture,
                    "UNIT_DEVASTATOR",
                    contract_new_geometry=False,
                    baseline=old_by_name,
                )
                contract_before = fixture.contract_path.read_bytes()
                checked = run_checker(fixture)
                self.assertNotEqual(checked.exit_code, 0, checked.stdout + checked.stderr)
                self.assertEqual(checked.statuses[1], "FAIL", checked.stdout + checked.stderr)
                self.assertIn(
                    "UNIT_DEVASTATOR: frame_hd4 не совпадает с unit.json",
                    checked.stdout,
                )
                self.assertEqual(fixture.contract_path.read_bytes(), contract_before)
