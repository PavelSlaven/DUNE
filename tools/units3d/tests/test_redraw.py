from __future__ import annotations

import csv
import hashlib
import io
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np
from PIL import Image

from tools.hd_assets import PackEntry, decode_image, encode_png, read_pack, write_pack


ROOT = Path(__file__).resolve().parents[3]
UNIT_DIR = ROOT / "tools/units3d/units/UNIT_DEVASTATOR"
REFERENCE_ATLASES = ROOT / "codex-direct/G3/atlas"
REPO_PACK = ROOT / "resources/bin/data/sdl_data_hd4.dat"
SOURCE_PACK = ROOT / "tools/units3d/data/sdl_data_hd4_source.dat"


class RedrawAcceptanceTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)

    def run_tool(self, command, *args, unit=None):
        self.assertTrue(
            (ROOT / "tools/units3d/redraw.py").is_file(),
            "Отсутствует инструмент tools/units3d/redraw.py",
        )
        return subprocess.run(
            [sys.executable, "tools/units3d/redraw.py", command,
             str(UNIT_DIR if unit is None else unit), *(str(arg) for arg in args)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
            timeout=1800,
        )

    def copy_unit(self):
        unit_dir = self.root / "unit"
        unit_dir.mkdir()
        shutil.copy2(UNIT_DIR / "unit.json", unit_dir / "unit.json")
        return unit_dir, json.loads((unit_dir / "unit.json").read_text(encoding="utf-8"))

    def save_unit(self, unit_dir, data):
        (unit_dir / "unit.json").write_text(
            json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )

    def frame(self, data, k, row=0):
        return next(frame for frame in data["frames"] if frame["row"] == row and frame["k"] == k)

    def assert_rgba_equal(self, actual, expected):
        with Image.open(actual) as image:
            actual_pixels = np.asarray(image.convert("RGBA"))
        with Image.open(expected) as image:
            expected_pixels = np.asarray(image.convert("RGBA"))
        self.assertEqual(actual_pixels.shape, expected_pixels.shape)
        self.assertTrue(np.array_equal(actual_pixels, expected_pixels), f"Пиксели различаются: {actual}")

    def build_atlases(self):
        output = self.root / "atlases"
        result = self.run_tool("build", output)
        self.assertEqual(result.returncode, 0, f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}")
        return output

    def test_01_build_atlases(self):
        atlas_dir = self.build_atlases()
        names = (
            "UNIT_DEVASTATOR",
            "HM_UNIT_DEVASTATOR",
            "UNIT_DEVASTATOR_SHADOW",
        )
        entries = json.loads(
            (atlas_dir / "atlases.json").read_text(encoding="utf-8")
        )["entries"]
        self.assertEqual(set(entries), set(names))
        for name in names:
            with self.subTest(atlas=name):
                image_path = atlas_dir / f"{name}.png"
                entry = entries[name]
                self.assertEqual(entry["file"], f"{name}.png")
                self.assertEqual(entry["size"], [1216, 192])
                with Image.open(image_path) as image:
                    self.assertEqual(list(image.size), [1216, 192])
                self.assertEqual(
                    entry["sha256"],
                    hashlib.sha256(image_path.read_bytes()).hexdigest(),
                )
                self.assert_rgba_equal(
                    image_path, REFERENCE_ATLASES / f"{name}.png"
                )

    def test_02_build_metrics(self):
        atlas_dir = self.build_atlases()
        metrics_paths = (
            atlas_dir / "metrics.txt",
            ROOT / "codex-direct/G3/metrics.txt",
        )
        metrics = []
        for path in metrics_paths:
            rows = list(
                csv.reader(io.StringIO(path.read_text(encoding="utf-8")), delimiter="\t")
            )
            header = next(
                row
                for row in rows
                if {"k", "iou", "share", "old_share"}.issubset(row)
            )
            columns = {name: header.index(name) for name in ("k", "iou", "share", "old_share")}
            values = {}
            for row in rows:
                if len(row) <= max(columns.values()):
                    continue
                try:
                    k = int(row[columns["k"]])
                except ValueError:
                    continue
                if 0 <= k <= 7:
                    values[k] = tuple(row[columns[name]] for name in ("iou", "share", "old_share"))
            metrics.append(values)

        self.assertEqual(set(metrics[0]), set(range(8)))
        self.assertEqual(set(metrics[1]), set(range(8)))
        self.assertEqual(metrics[0], metrics[1])

    def test_03_pack_replaces_only_unit(self):
        atlas_dir = self.build_atlases()
        copy_path = self.root / "devastator-pack.dat"
        repo_sha_before = hashlib.sha256(REPO_PACK.read_bytes()).hexdigest()
        source_sha_before = hashlib.sha256(SOURCE_PACK.read_bytes()).hexdigest()
        result = self.run_tool("pack", atlas_dir, copy_path, "--source", SOURCE_PACK)
        self.assertEqual(
            result.returncode,
            0,
            msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )

        before = read_pack(SOURCE_PACK)
        after = read_pack(copy_path)
        self.assertEqual(
            [(entry.index, entry.name, entry.extension) for entry in before],
            [(entry.index, entry.name, entry.extension) for entry in after],
        )
        changed = [
            (old, new)
            for old, new in zip(before, after, strict=True)
            if old.payload != new.payload
        ]
        expected_names = {
            "UNIT_DEVASTATOR",
            "HM_UNIT_DEVASTATOR",
            "UNIT_DEVASTATOR_SHADOW",
        }
        self.assertEqual(len(changed), 3)
        self.assertEqual({new.name for _, new in changed}, expected_names)
        for _, entry in changed:
            self.assertEqual(
                entry.payload,
                (atlas_dir / f"{entry.name}.png").read_bytes(),
                msg=entry.name,
            )
        self.assertEqual(
            hashlib.sha256(REPO_PACK.read_bytes()).hexdigest(),
            repo_sha_before,
        )
        self.assertEqual(
            hashlib.sha256(SOURCE_PACK.read_bytes()).hexdigest(),
            source_sha_before,
        )

    def test_04_recolour_shift_fails_iou(self):
        unit_dir, data = self.copy_unit()
        record = self.frame(data, 3)
        source = ROOT / record["recolour"]
        with Image.open(source) as image:
            if "A" in image.getbands():
                rgba = image.convert("RGBA")
                background = Image.new("RGBA", rgba.size, (255, 0, 255, 255))
                rgb = Image.alpha_composite(background, rgba).convert("RGB")
            else:
                rgb = image.convert("RGB")
            canvas = np.asarray(
                rgb.resize((1024, 1024), Image.Resampling.LANCZOS)
            ).copy()
        shifted = np.full((1024, 1024, 3), (255, 0, 255), dtype=np.uint8)
        shifted[:, 200:] = canvas[:, :824]
        modified = self.root / "recolour_k3_shifted.png"
        Image.fromarray(shifted, "RGB").save(modified)
        record["recolour"] = str(modified.resolve())
        self.save_unit(unit_dir, data)

        output = self.root / "build_recolour_shift"
        result = self.run_tool("build", output, unit=unit_dir)
        transcript = result.stdout + result.stderr
        self.assertEqual(result.returncode, 1, transcript)
        self.assertTrue(
            any(line.startswith("r0k3: ") and "iou" in line for line in result.stderr.splitlines()),
            transcript,
        )
        self.assertFalse((output / "atlases.json").exists(), transcript)

    def test_05_recolour_all_body_pixels_fails_share(self):
        unit_dir, data = self.copy_unit()
        record = self.frame(data, 5)
        source = ROOT / record["recolour"]
        with Image.open(source) as image:
            if "A" in image.getbands():
                rgba = image.convert("RGBA")
                background = Image.new("RGBA", rgba.size, (255, 0, 255, 255))
                rgb = Image.alpha_composite(background, rgba).convert("RGB")
            else:
                rgb = image.convert("RGB")
            pixels = np.asarray(
                rgb.resize((1024, 1024), Image.Resampling.LANCZOS)
            ).copy()
        magenta = np.array((255, 0, 255), dtype=np.int16)
        distance = np.linalg.norm(pixels.astype(np.int16) - magenta, axis=2)
        pixels[distance > 60] = (0, 255, 0)
        modified = self.root / "recolour_k5_all_green.png"
        Image.fromarray(pixels, "RGB").save(modified)
        record["recolour"] = str(modified.resolve())
        self.save_unit(unit_dir, data)

        output = self.root / "build_recolour_share"
        result = self.run_tool("build", output, unit=unit_dir)
        transcript = result.stdout + result.stderr
        self.assertEqual(result.returncode, 1, transcript)
        self.assertTrue(
            any(line.startswith("r0k5: ") and "share" in line for line in result.stderr.splitlines()),
            transcript,
        )
        self.assertFalse((output / "atlases.json").exists(), transcript)

    def test_06_recolour_selected_attempt_fails_share(self):
        unit_dir, data = self.copy_unit()
        record = self.frame(data, 5)
        source = ROOT / record["attempts"][record["pick"]]
        modified = self.root / "recolour_k5_from_pick.png"
        shutil.copyfile(source, modified)
        record["recolour"] = str(modified.resolve())
        self.save_unit(unit_dir, data)

        output = self.root / "build_recolour_from_pick"
        result = self.run_tool("build", output, unit=unit_dir)
        transcript = result.stdout + result.stderr
        self.assertEqual(result.returncode, 1, transcript)
        self.assertTrue(
            any(line.startswith("r0k5: ") and "share" in line for line in result.stderr.splitlines()),
            transcript,
        )
        self.assertFalse((output / "atlases.json").exists(), transcript)

    def test_07_oversized_pick_is_reported_clipped(self):
        unit_dir, data = self.copy_unit()
        record = self.frame(data, 0)
        source = ROOT / record["attempts"][record["pick"]]
        with Image.open(source) as image:
            if "A" in image.getbands():
                rgba = image.convert("RGBA")
                background = Image.new("RGBA", rgba.size, (255, 0, 255, 255))
                rgb = Image.alpha_composite(background, rgba).convert("RGB")
            else:
                rgb = image.convert("RGB")
            canvas = rgb.resize((1024, 1024), Image.Resampling.LANCZOS)
        enlarged_size = round(1024 * 1.4)
        enlarged = canvas.resize(
            (enlarged_size, enlarged_size), Image.Resampling.LANCZOS
        )
        cropped = Image.new("RGB", (1024, 1024), (255, 0, 255))
        cropped.paste(
            enlarged,
            ((1024 - enlarged_size) // 2, (1024 - enlarged_size) // 2),
        )
        modified = self.root / "attempt_k0_enlarged.png"
        cropped.save(modified)
        record["attempts"][record["pick"]] = str(modified.resolve())
        self.save_unit(unit_dir, data)

        output = self.root / "build_oversized_pick"
        result = self.run_tool("build", output, unit=unit_dir)
        transcript = result.stdout + result.stderr
        self.assertEqual(result.returncode, 1, transcript)
        self.assertTrue(
            any(line.startswith("r0k0: ") and "clipped" in line for line in result.stderr.splitlines()),
            transcript,
        )
        self.assertFalse((output / "atlases.json").exists(), transcript)

    def test_08_black_background_key_builds_reference_shape_without_house_mask(self):
        unit_dir, data = self.copy_unit()
        record = self.frame(data, 0)
        source = ROOT / record["attempts"][record["pick"]]
        with Image.open(source) as image:
            if "A" in image.getbands():
                rgba = image.convert("RGBA")
                background = Image.new("RGBA", rgba.size, (255, 0, 255, 255))
                rgb = Image.alpha_composite(background, rgba).convert("RGB")
            else:
                rgb = image.convert("RGB")
            pixels = np.asarray(
                rgb.resize((1024, 1024), Image.Resampling.LANCZOS)
            ).copy()
        magenta = np.array((255, 0, 255), dtype=np.int16)
        distance = np.linalg.norm(pixels.astype(np.int16) - magenta, axis=2)
        pixels[distance <= 60] = (0, 0, 0)
        modified = self.root / "attempt_k0_black_background.png"
        Image.fromarray(pixels, "RGB").save(modified)
        record["attempts"][record["pick"]] = str(modified.resolve())
        data["atlases"]["house_mask"] = None
        self.save_unit(unit_dir, data)

        output = self.root / "build_black_background"
        result = self.run_tool("build", output, unit=unit_dir)
        transcript = result.stdout + result.stderr
        self.assertEqual(result.returncode, 0, transcript)
        body_path = output / f"{data['atlases']['body']}.png"
        self.assertTrue(body_path.is_file(), transcript)
        with Image.open(body_path) as image:
            actual = np.asarray(image.convert("RGBA"))
        with Image.open(REFERENCE_ATLASES / f"{data['atlases']['body']}.png") as image:
            expected = np.asarray(image.convert("RGBA"))
        frame_width, frame_height = data["frame"]
        actual_alpha = actual[:frame_height, :frame_width, 3]
        expected_alpha = expected[:frame_height, :frame_width, 3]
        for y, x in (
            (0, 0),
            (0, frame_width - 1),
            (frame_height - 1, 0),
            (frame_height - 1, frame_width - 1),
        ):
            self.assertEqual(int(actual_alpha[y, x]), 0, transcript)
        actual_opaque = actual_alpha > 127
        expected_opaque = expected_alpha > 127
        union = np.logical_or(actual_opaque, expected_opaque).sum()
        intersection = np.logical_and(actual_opaque, expected_opaque).sum()
        iou = intersection / union if union else 1.0
        self.assertGreaterEqual(iou, 0.97, transcript)

    def test_09_missing_attempts_and_pick_are_invalid_for_build_and_score(self):
        unit_dir, data = self.copy_unit()
        record = self.frame(data, 2)
        record["attempts"] = {}
        record.pop("pick")
        self.save_unit(unit_dir, data)

        for command in ("build", "score"):
            if command == "build":
                result = self.run_tool(
                    "build", self.root / "build_missing_k2_inputs", unit=unit_dir
                )
            else:
                result = self.run_tool("score", unit=unit_dir)
            self.assertEqual(
                result.returncode,
                2,
                result.stdout + result.stderr,
            )

    def test_10_inputs(self):
        output = self.root / "inputs"
        result = self.run_tool("inputs", output, unit=UNIT_DIR)
        self.assertEqual(
            result.returncode,
            0,
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )

        for k in range(8):
            source_dir = ROOT / "codex-direct" / ("G2" if k in (1, 6) else "G3") / "input"
            actual_old = output / f"old_r0k{k}.png"
            expected_old = source_dir / f"old_k{k}.png"
            self.assert_rgba_equal(actual_old, expected_old)

            actual_guide = np.asarray(
                Image.open(output / f"guide_r0k{k}.png").convert("RGB"), dtype=np.int16
            )
            expected_guide_image = Image.open(source_dir / f"guide_k{k}.png").convert("RGB")
            expected_guide = np.asarray(expected_guide_image, dtype=np.int16)
            self.assertEqual(actual_guide.shape, expected_guide.shape, f"guide k{k} size differs")
            difference = np.abs(actual_guide - expected_guide)
            self.assertLessEqual(int(difference.max()), 24, f"guide k{k} channel difference exceeds 24")
            self.assertLessEqual(float(difference.mean()), 0.01, f"guide k{k} mean difference exceeds 0.01")

    def test_11_recolour_inputs(self):
        output = self.root / "recolour-inputs"
        result = self.run_tool("recolour-inputs", output, unit=UNIT_DIR)
        self.assertEqual(
            result.returncode,
            0,
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )

        unit_data = json.loads((UNIT_DIR / "unit.json").read_text(encoding="utf-8"))
        packed = {entry.name: entry for entry in read_pack(SOURCE_PACK)}
        body = decode_image(packed[unit_data["atlases"]["body"]].payload).convert("RGBA")
        old_mask = decode_image(packed[unit_data["atlases"]["house_mask"]].payload).convert("RGBA")
        frame_width, frame_height = unit_data["frame"]
        max_frame = max(frame_width, frame_height)
        canvas_size = 1024
        resized_size = (
            round(frame_width * canvas_size / max_frame),
            round(frame_height * canvas_size / max_frame),
        )

        for k in range(8):
            actual_pick = output / f"pick_r0k{k}.png"
            expected_pick = ROOT / "codex-direct" / "G3" / "input" / f"pick_k{k}.png"
            self.assert_rgba_equal(actual_pick, expected_pick)

            box = (k * frame_width, 0, (k + 1) * frame_width, frame_height)
            body_frame = np.asarray(body.crop(box), dtype=np.uint8).copy()
            mask_alpha = np.asarray(old_mask.crop(box), dtype=np.uint8)[..., 3]
            body_frame[mask_alpha > 127, :3] = (0, 255, 0)
            recoloured = Image.fromarray(body_frame, "RGBA").resize(
                resized_size, Image.Resampling.LANCZOS
            )
            expected_oldmask = Image.new("RGBA", (canvas_size, canvas_size), (255, 0, 255, 255))
            position = (
                (canvas_size - recoloured.width) // 2,
                (canvas_size - recoloured.height) // 2,
            )
            expected_oldmask.alpha_composite(recoloured, position)
            expected_path = self.root / f"expected_oldmask_r0k{k}.png"
            expected_oldmask.save(expected_path)
            self.assert_rgba_equal(output / f"oldmask_r0k{k}.png", expected_path)

    def test_12_shadow_rule(self):
        result = self.run_tool("shadow-rule")
        self.assertEqual(
            result.returncode,
            0,
            msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )
        lines = result.stdout.splitlines()
        self.assertEqual(len(lines), 1, msg=result.stdout)
        rule = json.loads(lines[0])
        self.assertEqual(rule["shift"], 4)
        self.assertEqual(rule["alpha"], 46)
        self.assertEqual(rule["rgb"], [5, 4, 3])
        self.assertGreaterEqual(rule["corr"], 0.984)
        self.assertLessEqual(rule["corr"], 0.994)

    def test_13_score(self):
        result = self.run_tool("score")
        self.assertEqual(
            result.returncode,
            0,
            msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )
        expected_lines = (ROOT / "codex-direct/G3/choice.txt").read_text(
            encoding="utf-8"
        ).splitlines()
        header_index = next(
            index
            for index, line in enumerate(expected_lines)
            if line.startswith("k\told w×h\t")
        )
        required = [expected_lines[header_index], *expected_lines[header_index + 1 : header_index + 17]]
        start_index = next(
            index
            for index, line in enumerate(expected_lines)
            if line.startswith("old mirror IoU")
        )
        end_index = next(
            index
            for index, line in enumerate(expected_lines[start_index:], start_index)
            if line.startswith("angle error [")
        )
        required.extend(expected_lines[start_index : end_index + 1])
        # choice.txt was written with Pillow 12; Pillow 13 resizes the k5a/k7a silhouettes
        # so that their mirror IoU 0.90250836 rounds to 0.903 instead of 0.902.
        required = [
            line.replace("'aa': 0.902,", "'aa': 0.903,") if line.startswith("5-7 ") else line
            for line in required
        ]
        actual_lines = result.stdout.splitlines()
        for line in required:
            with self.subTest(line=line):
                self.assertIn(line, actual_lines)

    def test_14_inputs_contact_sheet(self):
        inputs_dir = self.root / "inputs"
        inputs_result = self.run_tool("inputs", inputs_dir)
        self.assertEqual(
            inputs_result.returncode,
            0,
            msg=f"stdout:\n{inputs_result.stdout}\nstderr:\n{inputs_result.stderr}",
        )

        atlas_dir = self.build_atlases()
        contact_path = self.root / "contact.png"
        contact_result = self.run_tool("contact", inputs_dir, contact_path)
        self.assertEqual(
            contact_result.returncode,
            0,
            msg=f"stdout:\n{contact_result.stdout}\nstderr:\n{contact_result.stderr}",
        )
        with Image.open(contact_path) as image:
            self.assertEqual(image.size, (1200, 2640))

        sheet_path = self.root / "sheet.png"
        sheet_result = self.run_tool("sheet", atlas_dir, sheet_path)
        self.assertEqual(
            sheet_result.returncode,
            0,
            msg=f"stdout:\n{sheet_result.stdout}\nstderr:\n{sheet_result.stderr}",
        )
        with Image.open(sheet_path) as image:
            self.assertEqual(image.size, (2662, 2578))

    def test_15_pack_rejects_extra_entry(self):
        atlas_dir = self.build_atlases()
        manifest_path = atlas_dir / "atlases.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        body_entry = manifest["entries"]["UNIT_DEVASTATOR"]
        extra_path = atlas_dir / "UNIT_QUAD.png"
        shutil.copyfile(atlas_dir / body_entry["file"], extra_path)
        with Image.open(extra_path) as image:
            extra_size = list(image.size)
        manifest["entries"]["UNIT_QUAD"] = {
            "file": extra_path.name,
            "sha256": hashlib.sha256(extra_path.read_bytes()).hexdigest(),
            "size": extra_size,
        }
        manifest_path.write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

        copy_path = self.root / "extra-entry-pack.dat"
        result = self.run_tool("pack", atlas_dir, copy_path)
        self.assertEqual(
            result.returncode,
            1,
            msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )
        self.assertFalse(copy_path.exists())

    def test_16_pack_rejects_bad_hash(self):
        atlas_dir = self.build_atlases()
        manifest_path = atlas_dir / "atlases.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        entry = manifest["entries"]["HM_UNIT_DEVASTATOR"]
        digest = entry["sha256"]
        entry["sha256"] = digest[:-1] + ("0" if digest[-1] != "0" else "1")
        manifest_path.write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

        copy_path = self.root / "bad-hash-pack.dat"
        result = self.run_tool("pack", atlas_dir, copy_path)
        self.assertEqual(
            result.returncode,
            1,
            msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )
        self.assertFalse(copy_path.exists())

    def test_17_pack_is_idempotent(self):
        atlas_dir = self.build_atlases()
        first_copy = self.root / "first-pack.dat"
        first_result = self.run_tool("pack", atlas_dir, first_copy)
        self.assertEqual(
            first_result.returncode,
            0,
            msg=f"stdout:\n{first_result.stdout}\nstderr:\n{first_result.stderr}",
        )

        second_copy = self.root / "second-pack.dat"
        second_result = self.run_tool(
            "pack", atlas_dir, second_copy, "--source", first_copy
        )
        self.assertEqual(
            second_result.returncode,
            0,
            msg=f"stdout:\n{second_result.stdout}\nstderr:\n{second_result.stderr}",
        )
        self.assertEqual(first_copy.read_bytes(), second_copy.read_bytes())

    def test_18_build_rejects_nonempty_output(self):
        output_dir = self.root / "atlases"
        output_dir.mkdir()
        sentinel_path = output_dir / "atlases.json"
        sentinel = b"keep this manifest unchanged\n"
        sentinel_path.write_bytes(sentinel)

        result = self.run_tool("build", output_dir)
        self.assertEqual(
            result.returncode,
            2,
            msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )
        self.assertEqual(sentinel_path.read_bytes(), sentinel)

    def test_19_shadow_rule_respects_frame_boundaries(self):
        frame_width, frame_height, rows = 16, 12, 2
        atlas_width, atlas_height = frame_width * 8, frame_height * rows
        body = np.zeros((atlas_height, atlas_width, 4), dtype=np.uint8)
        body[..., :3] = (17, 31, 47)
        shadow = np.zeros_like(body)
        shadow[..., :3] = (5, 4, 3)
        for row in range(rows):
            for k in range(8):
                x0, y0 = k * frame_width, row * frame_height
                body[y0 + 4 : y0 + frame_height, x0 + 6 : x0 + frame_width, 3] = 128
                body_alpha = body[
                    y0 : y0 + frame_height,
                    x0 : x0 + frame_width,
                    3,
                ]
                shadow_alpha = shadow[
                    y0 : y0 + frame_height,
                    x0 : x0 + frame_width,
                    3,
                ]
                shadow_alpha[4:, 4:] = np.round(
                    body_alpha[:-4, :-4].astype(np.float32) * 46 / 255
                ).astype(np.uint8)

        source_pack = self.root / "synthetic-pack.dat"
        write_pack(
            source_pack,
            [
                PackEntry(
                    index=0,
                    name="UNIT_SYN",
                    extension="png",
                    payload=encode_png(Image.fromarray(body)),
                ),
                PackEntry(
                    index=1,
                    name="UNIT_SYN_SHADOW",
                    extension="png",
                    payload=encode_png(Image.fromarray(shadow)),
                ),
            ],
        )
        unit_dir = self.root / "synthetic-unit"
        unit_dir.mkdir()
        unit_data = {
            "atlases": {
                "body": "UNIT_SYN",
                "house_mask": None,
                "shadow": "UNIT_SYN_SHADOW",
            },
            "frame": [frame_width, frame_height],
            "rows": rows,
            "frames": [
                {"row": row, "k": k}
                for row in range(rows)
                for k in range(8)
            ],
        }
        (unit_dir / "unit.json").write_text(
            json.dumps(unit_data, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

        result = self.run_tool(
            "shadow-rule", "--pack", source_pack, unit=unit_dir
        )
        self.assertEqual(
            result.returncode,
            0,
            msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )
        lines = result.stdout.splitlines()
        self.assertEqual(len(lines), 1, msg=result.stdout)
        rule = json.loads(lines[0])
        self.assertEqual(rule["shift"], 4)
        self.assertEqual(rule["alpha"], 46)
        self.assertEqual(rule["rgb"], [5, 4, 3])
        self.assertGreaterEqual(rule["corr"], 0.99)

    def test_20_missing_k7_frame_is_invalid_for_build(self):
        unit_dir, data = self.copy_unit()
        data["frames"] = [frame for frame in data["frames"] if frame["k"] != 7]
        self.save_unit(unit_dir, data)

        result = self.run_tool("build", self.root / "build_missing_k7", unit=unit_dir)
        transcript = result.stdout + result.stderr
        self.assertEqual(result.returncode, 2, transcript)
        self.assertIn("r0k7", result.stderr, transcript)


    def enlarge_on_canvas(self, source, target, factor=1.4):
        with Image.open(source) as image:
            if "A" in image.getbands():
                rgba = image.convert("RGBA")
                background = Image.new("RGBA", rgba.size, (255, 0, 255, 255))
                rgb = Image.alpha_composite(background, rgba).convert("RGB")
            else:
                rgb = image.convert("RGB")
            canvas = rgb.resize((1024, 1024), Image.Resampling.LANCZOS)
        size = round(1024 * factor)
        enlarged = canvas.resize((size, size), Image.Resampling.LANCZOS)
        cropped = Image.new("RGB", (1024, 1024), (255, 0, 255))
        cropped.paste(enlarged, ((1024 - size) // 2, (1024 - size) // 2))
        cropped.save(target)
        return str(target.resolve())

    def test_21_fit_scale_removes_clipping(self):
        unit_dir, data = self.copy_unit()
        record = self.frame(data, 0)
        record["attempts"][record["pick"]] = self.enlarge_on_canvas(
            ROOT / record["attempts"][record["pick"]], self.root / "attempt_k0_enlarged.png"
        )
        record["recolour"] = self.enlarge_on_canvas(
            ROOT / record["recolour"], self.root / "recolour_k0_enlarged.png"
        )
        data["scale"] = "fit"
        self.save_unit(unit_dir, data)

        output = self.root / "build_fit"
        result = self.run_tool("build", output, unit=unit_dir)
        transcript = result.stdout + result.stderr
        self.assertEqual(result.returncode, 0, transcript)
        self.assertTrue((output / "atlases.json").is_file(), transcript)
        params = json.loads((output / "params.json").read_text(encoding="utf-8"))
        self.assertLess(params["scale"], params["scale_median"])
        self.assertAlmostEqual(params["scale_median"], 1.0714527591528187, places=9)
        self.assertIn("all frames pass", (output / "metrics.txt").read_text(encoding="utf-8").splitlines())

    def test_22_explicit_scale_is_used(self):
        unit_dir, data = self.copy_unit()
        data["scale"] = 1.0
        self.save_unit(unit_dir, data)

        output = self.root / "build_explicit_scale"
        result = self.run_tool("build", output, unit=unit_dir)
        transcript = result.stdout + result.stderr
        self.assertEqual(result.returncode, 0, transcript)
        params = json.loads((output / "params.json").read_text(encoding="utf-8"))
        self.assertEqual(params["scale"], 1.0)
        self.assertAlmostEqual(params["scale_median"], 1.0714527591528187, places=9)

    def test_23_share_corridor_from_unit(self):
        unit_dir, data = self.copy_unit()
        record = self.frame(data, 5)
        with Image.open(ROOT / record["recolour"]) as image:
            pixels = np.asarray(image.convert("RGB").resize((1024, 1024), Image.Resampling.LANCZOS)).copy()
        distance = np.linalg.norm(pixels.astype(np.int16) - np.array((255, 0, 255), dtype=np.int16), axis=2)
        pixels[distance > 60] = (0, 255, 0)
        modified = self.root / "recolour_k5_all_green.png"
        Image.fromarray(pixels, "RGB").save(modified)
        record["recolour"] = str(modified.resolve())
        data["share_corridor"] = [0.0, 1.0]
        self.save_unit(unit_dir, data)

        output = self.root / "build_share_corridor"
        result = self.run_tool("build", output, unit=unit_dir)
        transcript = result.stdout + result.stderr
        self.assertEqual(result.returncode, 0, transcript)
        self.assertIn(
            "corridor	0.00000	1.00000	set",
            (output / "metrics.txt").read_text(encoding="utf-8").splitlines(),
        )


if __name__ == "__main__":
    unittest.main()
