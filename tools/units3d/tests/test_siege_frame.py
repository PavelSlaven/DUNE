from __future__ import annotations

import json
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
BUILD_NAMES = ("UNIT_SIEGEBASE", "HM_UNIT_SIEGEBASE", "UNIT_SIEGEBASE_SHADOW")


def _png(array: np.ndarray) -> bytes:
    return encode_png(Image.fromarray(np.asarray(array, dtype=np.uint8), "RGBA"))


def _write_build_fixture(root: Path, protective: bool) -> tuple[Path, Path]:
    unit_dir = root / "siege"
    unit_dir.mkdir()
    pack_path = root / "source.dat"
    body = np.zeros((152, 1152, 4), dtype=np.uint8)
    mask = np.zeros_like(body)
    shadow = np.zeros_like(body)
    for k in range(8):
        left = k * 144
        if protective and k == 0:
            body[0:10, left:left + 10] = (70, 60, 45, 255)
            mask[2:6, left + 2:left + 6] = (255, 255, 255, 255)
        elif k == 1:
            body[34:110, left:left + 76] = (70, 60, 45, 255)
            body[34:38, left:left + 4] = (20, 40, 240, 255)
            mask[40:50, left + 40:left + 50] = (255, 255, 255, 255)
            mask[34:38, left:left + 4] = (255, 255, 255, 255)
        else:
            body[34:110, left + 34:left + 110] = (70, 60, 45, 255)
            mask[40:50, left + 40:left + 50] = (255, 255, 255, 255)

    # Этот маркер начинается сразу за кадром k0 и выявляет захват пикселей соседнего направления.
    body[0:4, 144:148] = (20, 240, 40, 255)
    mask[0:4, 144:148] = (255, 255, 255, 255)
    entries = [
        PackEntry(index, name, "PNG", _png(image))
        for index, (name, image) in enumerate(
            zip(BUILD_NAMES, (body, mask, shadow), strict=True)
        )
    ]
    write_pack(pack_path, entries)

    attempt = np.zeros((1024, 1024, 3), dtype=np.uint8)
    attempt[:] = (255, 0, 255)
    attempt[474:550, 474:550] = (70, 60, 45)
    attempt[480:490, 480:490] = (230, 20, 10)
    recolour = attempt.copy()
    recolour[480:490, 480:490] = (0, 255, 0)
    attempt_path = root / "attempt.png"
    recolour_path = root / "recolour.png"
    Image.fromarray(attempt, "RGB").save(attempt_path)
    Image.fromarray(recolour, "RGB").save(recolour_path)

    records = []
    for k in range(8):
        records.append({
            "row": 0,
            "k": k,
            "attempts": {"only": str(attempt_path)},
            "pick": "only",
            "recolour": str(recolour_path),
        })
    description = {
        "atlases": {
            "body": "UNIT_SIEGEBASE",
            "house_mask": "HM_UNIT_SIEGEBASE",
            "shadow": "UNIT_SIEGEBASE_SHADOW",
        },
        "reference_frame": [144, 152],
        "reference_anchor": [72, 72],
        "frame": [176, 176],
        "atlas_size": [1408, 176],
        "rows": 1,
        "figures": 1,
        "despill": False,
        "share_corridor": [0.0, 1.0],
        "scale": 1024 / 152,
        "shadow_rule": {"shift": 4, "alpha": 51, "rgb": [7, 5, 3]},
        "frames": records,
    }
    (unit_dir / "unit.json").write_text(
        json.dumps(description, indent=2) + "\n", encoding="utf-8"
    )
    return unit_dir, pack_path


def _run_build(unit_dir: Path, pack_path: Path, output: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            "tools/units3d/redraw.py",
            "build",
            str(unit_dir),
            str(output),
            "--pack",
            str(pack_path),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
        timeout=1800,
    )


def _alpha_bbox(image_path: Path) -> list[int]:
    with Image.open(image_path) as image:
        alpha = np.asarray(image.convert("RGBA"))[:, :, 3]
    ys, xs = np.where(alpha > 0)
    if not len(xs):
        return []
    return [int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1]


def _metrics_row(path: Path, k: int) -> dict[str, str]:
    rows = path.read_text(encoding="utf-8").splitlines()
    header = rows[0].split("\t")
    for row in rows[1:]:
        values = row.split("\t")
        if len(values) == len(header) and values[1].isdigit() and int(values[1]) == k:
            return dict(zip(header, values, strict=True))
    raise AssertionError(f"В metrics.txt отсутствует кадр k={k}")


class SiegeFrameAcceptanceTests(unittest.TestCase):
    def test_build_reference_geometry_and_anchor(self) -> None:
        with tempfile.TemporaryDirectory(prefix="u9t1-reference-") as temporary:
            root = Path(temporary)
            unit_dir, pack_path = _write_build_fixture(root, protective=False)
            output = root / "build"
            result = _run_build(unit_dir, pack_path, output)
            transcript = result.stdout + result.stderr
            self.assertEqual(result.returncode, 0, transcript)

            manifest = json.loads((output / "atlases.json").read_text(encoding="utf-8"))
            self.assertEqual(set(manifest["entries"]), set(BUILD_NAMES))
            for name in BUILD_NAMES:
                with self.subTest(atlas=name):
                    self.assertEqual(manifest["entries"][name]["size"], [1408, 176])
                    with Image.open(output / manifest["entries"][name]["file"]) as image:
                        self.assertEqual(list(image.size), [1408, 176])

            params = json.loads((output / "params.json").read_text(encoding="utf-8"))
            self.assertEqual(params["scale_median"], 1024 / 152)
            self.assertEqual(params["frames"]["r0k0"]["offset"], [-424, -424])
            self.assertEqual(_metrics_row(output / "metrics.txt", 0)["old_share"], "0.017")
            self.assertEqual(_alpha_bbox(output / "frames/r0k0.png"), [50, 50, 126, 126])

    def test_build_protective_shift_keeps_layers_aligned(self) -> None:
        with tempfile.TemporaryDirectory(prefix="u9t1-protective-") as temporary:
            root = Path(temporary)
            unit_dir, pack_path = _write_build_fixture(root, protective=True)
            output = root / "build"
            result = _run_build(unit_dir, pack_path, output)
            transcript = result.stdout + result.stderr
            self.assertEqual(result.returncode, 0, transcript)

            params = json.loads((output / "params.json").read_text(encoding="utf-8"))
            self.assertEqual(params["scale_median"], 1024 / 152)
            self.assertEqual(params["frames"]["r0k0"]["moved"], [17, 17])
            self.assertEqual(_alpha_bbox(output / "frames/r0k0.png"), [0, 0, 76, 76])
            with Image.open(output / "frames/r0k0.png") as image:
                body = np.asarray(image.convert("RGBA"))
            with Image.open(output / "HM_UNIT_SIEGEBASE.png") as image:
                mask_atlas = np.asarray(image.convert("RGBA"))
            mask_alpha = mask_atlas[:176, :176, 3]
            ys, xs = np.where(mask_alpha > 0)
            self.assertEqual([int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1], [6, 6, 16, 16])
            self.assertTrue(np.all(body[6:16, 6:16, :3] == (230, 20, 10)))
            self.assertEqual(_metrics_row(output / "metrics.txt", 0)["ok"], "True")

    def test_real_siege_descriptions(self) -> None:
        expectations = {
            "UNIT_SIEGEBASE": {
                "scale": 1.179349500917,
                "recolour_prefix": "units-gen/UNIT_SIEGEBASE/siegebase_recolour9_k",
                "share_corridor": [0.10, 0.45],
            },
            "UNIT_SIEGETOP": {
                "scale": 1.148390687555,
                "recolour_prefix": "units-gen/UNIT_SIEGETOP/siegetop_recolour9_k",
                "share_corridor": [0.15, 0.60],
            },
        }
        for name, expected in expectations.items():
            with self.subTest(unit=name):
                data = json.loads(
                    (ROOT / f"tools/units3d/units/{name}/unit.json").read_text(encoding="utf-8")
                )
                self.assertEqual(data.get("reference_frame"), [144, 152])
                self.assertEqual(data.get("reference_anchor"), [72, 72])
                self.assertEqual(data.get("frame"), [176, 176])
                self.assertEqual(data.get("atlas_size"), [1408, 176])
                self.assertEqual(data["scale"], expected["scale"])
                self.assertEqual(data["share_corridor"], expected["share_corridor"])
                self.assertNotEqual(data.get("scale"), "fit")
                records = data["frames"]
                self.assertEqual(len(records), 8)
                recolours = {
                    (record["row"], record["k"]): record["recolour"]
                    for record in records
                }
                self.assertEqual(
                    recolours,
                    {
                        (0, k): f"{expected['recolour_prefix']}{k}.png"
                        for k in range(8)
                    },
                )
