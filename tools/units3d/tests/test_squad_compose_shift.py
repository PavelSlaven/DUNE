from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np
from PIL import Image


ROOT = Path(__file__).resolve().parents[3]
COMPOSE_PATH = ROOT / "codex-direct/U6/squads/compose.py"
PLACEMENTS_PATH = ROOT / "codex-direct/U6/squads/UNIT_SOLDIERS/placements.json"
PACK_PATH = Path(os.environ.get("D2TM_PACK_DIR", ROOT / "resources/bin/data")) / "sdl_data_hd4.dat"


def load_compose_module():
    spec = importlib.util.spec_from_file_location("u12_squad_compose", COMPOSE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"не удалось загрузить модуль {COMPOSE_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def atlas_cells(path: Path) -> dict[tuple[int, int], np.ndarray]:
    with Image.open(path) as image:
        pixels = np.asarray(image.convert("RGBA"), dtype=np.uint8)
    return {
        (k, r): pixels[r * 128:(r + 1) * 128, k * 128:(k + 1) * 128]
        for r in range(4)
        for k in range(8)
    }


class SquadComposeShiftTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.compose_module = load_compose_module()
        entries = cls.compose_module.read_pack(PACK_PATH)
        wanted = {"UNIT_SOLDIER", "HM_UNIT_SOLDIER"}
        cls.atlases = {}
        for entry in entries:
            if entry.name in wanted:
                image = cls.compose_module.decode_image(entry.payload)
                if image is None:
                    raise AssertionError(f"запись {entry.name} не декодируется как изображение")
                cls.atlases[entry.name] = image.convert("RGBA")
        missing = wanted - set(cls.atlases)
        if missing:
            raise AssertionError("в паке отсутствуют записи: " + ", ".join(sorted(missing)))

    def run_compose(self, temporary: Path, name: str, source: Path, body: Path,
                    placements: Path, mask: bool = False) -> Path:
        output = temporary / f"{name}.png"
        sheet = temporary / f"{name}-sheet.png"
        report = temporary / f"{name}-checks.json"
        result = self.compose_module.compose(
            type("ComposeArgs", (), {
                "squad": "UNIT_SOLDIERS",
                "out_root": str(temporary / f"{name}-root"),
                "source": str(source),
                "body": str(body),
                "mask": mask,
                "placements": str(placements),
                "output": str(output),
                "sheet": str(sheet),
                "report": str(report),
            })()
        )
        self.assertEqual(result, 0)
        self.assertTrue(output.is_file())
        self.assertTrue(sheet.is_file())
        self.assertTrue(report.is_file())
        return output

    def test_shift_moves_body_and_house_mask_and_rejects_invalid_values(self):
        (ROOT / ".tmp").mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="u12-compose-", dir=ROOT / ".tmp") as directory:
            temporary = Path(directory)
            body_source = temporary / "UNIT_SOLDIER.png"
            mask_source = temporary / "HM_UNIT_SOLDIER.png"
            self.atlases["UNIT_SOLDIER"].save(body_source)
            self.atlases["HM_UNIT_SOLDIER"].save(mask_source)

            shifted_placements = json.loads(PLACEMENTS_PATH.read_text(encoding="utf-8"))
            self.assertEqual(shifted_placements.get("shift"), [0, 13])
            baseline_placements = dict(shifted_placements)
            baseline_placements.pop("shift")
            baseline_path = temporary / "placements-without-shift.json"
            baseline_path.write_text(
                json.dumps(baseline_placements, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )

            baseline_body = self.run_compose(
                temporary, "body-baseline", body_source, body_source, baseline_path
            )
            shifted_body = self.run_compose(
                temporary, "body-shifted", body_source, body_source, PLACEMENTS_PATH
            )
            baseline_mask = self.run_compose(
                temporary, "mask-baseline", mask_source, body_source, baseline_path, mask=True
            )
            shifted_mask = self.run_compose(
                temporary, "mask-shifted", mask_source, body_source, PLACEMENTS_PATH, mask=True
            )

            for baseline_path, shifted_path in (
                (baseline_body, shifted_body),
                (baseline_mask, shifted_mask),
            ):
                baseline_cells = atlas_cells(baseline_path)
                shifted_cells = atlas_cells(shifted_path)
                for (k, r), cell in baseline_cells.items():
                    self.assertTrue(
                        np.all(cell[-13:, :, 3] == 0),
                        f"в последних 13 строках baseline альфа не нулевая: k={k}, r={r}",
                    )
                for (k, r), cell in baseline_cells.items():
                    expected = np.roll(cell, 13, axis=0)
                    np.testing.assert_array_equal(
                        shifted_cells[(k, r)], expected, err_msg=f"клетка k={k}, r={r}"
                    )

            for index, invalid_shift in enumerate(([0], [0, 1.5], [True, 0])):
                invalid_doc = dict(baseline_placements)
                invalid_doc["shift"] = invalid_shift
                invalid_path = temporary / f"placements-invalid-{index}.json"
                invalid_path.write_text(
                    json.dumps(invalid_doc, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8",
                )
                completed = subprocess.run(
                    [
                        sys.executable, str(COMPOSE_PATH), "compose",
                        "--squad", "UNIT_SOLDIERS",
                        "--source", str(body_source),
                        "--body", str(body_source),
                        "--placements", str(invalid_path),
                        "--out-root", str(temporary / f"invalid-root-{index}"),
                        "--output", str(temporary / f"invalid-{index}.png"),
                        "--sheet", str(temporary / f"invalid-{index}-sheet.png"),
                        "--report", str(temporary / f"invalid-{index}-checks.json"),
                    ],
                    cwd=ROOT,
                    capture_output=True,
                    text=True,
                    env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
                    check=False,
                )
                self.assertNotEqual(completed.returncode, 0, invalid_shift)
                self.assertIn("shift", completed.stderr, invalid_shift)


if __name__ == "__main__":
    unittest.main()
