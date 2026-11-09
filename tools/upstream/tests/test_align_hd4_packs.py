import hashlib
import io
import json
from pathlib import Path
import struct
import subprocess
import sys
import tempfile
import unittest

from PIL import Image


ROOT = Path(__file__).resolve().parents[3]
TMP_ROOT = ROOT / ".tmp/p2t"
HEADER = struct.Struct("<4sH")
ENTRY = struct.Struct("<40s4sII")


def png_rgba(seed=0):
    pixels = [
        (240, 25, 35, 255),
        (20, 215, 90, 160),
        (15, 55, 235, 40),
        (210, 180, 25, 90),
        (145, 20, 195, 220),
        (10, 240, 200, 255),
    ]
    output = io.BytesIO()
    image = Image.new("RGBA", (3, 2))
    image.putdata([
        ((red + seed * (index + 1)) % 256,
         (green + seed * (index + 2)) % 256,
         (blue + seed * (index + 3)) % 256,
         alpha)
        for index, (red, green, blue, alpha) in enumerate(pixels)
    ])
    image.save(output, format="PNG")
    return output.getvalue()


def png_palette_transparency():
    image = Image.new("P", (2, 1))
    palette = [255, 0, 0, 0, 255, 0] + [0, 0, 0] * 254
    image.putpalette(palette)
    image.putdata([0, 1])
    image.info["transparency"] = 0
    output = io.BytesIO()
    image.save(output, format="PNG", transparency=0)
    return output.getvalue()


def make_pack(entries, reverse_payload=False):
    physical_order = list(range(len(entries)))
    if reverse_payload:
        physical_order.reverse()
    offsets = [0] * len(entries)
    cursor = 0
    for index in physical_order:
        offsets[index] = cursor
        cursor += len(entries[index][2])

    result = bytearray(HEADER.pack(b"D2TM", len(entries)))
    for (name, extension, payload), offset in zip(entries, offsets):
        result.extend(ENTRY.pack(
            name.encode("ascii").ljust(40, b"\0"),
            extension.encode("ascii").ljust(4, b"\0"),
            offset,
            len(payload),
        ))
    for index in physical_order:
        result.extend(entries[index][2])
    return bytes(result)


def write_pack(path, entries, reverse_payload=False):
    path.write_bytes(make_pack(entries, reverse_payload=reverse_payload))


def read_pack(path):
    raw = path.read_bytes()
    magic, count = HEADER.unpack_from(raw)
    if magic != b"D2TM":
        raise ValueError(f"invalid pack signature: {path}")
    payload_start = HEADER.size + count * ENTRY.size
    result = []
    for index in range(count):
        raw_name, raw_extension, offset, size = ENTRY.unpack_from(
            raw, HEADER.size + index * ENTRY.size
        )
        start = payload_start + offset
        result.append((
            raw_name.split(b"\0", 1)[0].decode("ascii"),
            raw_extension.split(b"\0", 1)[0].decode("ascii"),
            raw[start:start + size],
        ))
    return result


class AlignHD4PacksTests(unittest.TestCase):
    def setUp(self):
        TMP_ROOT.mkdir(parents=True, exist_ok=True)

    def make_case(self, root, *, header, fork, classic, list_value,
                  out_name="aligned_hd4.dat", reverse_payload=False):
        header_path = root / "constants.h"
        fork_path = root / "fork.dat"
        classic_path = root / "classic.dat"
        list_path = root / "without_hd.json"
        out_path = root / out_name
        report_path = root / "alignment.tsv"
        header_path.write_text(header, encoding="utf-8")
        write_pack(fork_path, fork, reverse_payload=reverse_payload)
        write_pack(classic_path, classic)
        list_path.write_text(json.dumps(list_value), encoding="utf-8")
        return {
            "header": header_path,
            "fork": fork_path,
            "classic": classic_path,
            "list": list_path,
            "out": out_path,
            "report": report_path,
        }

    def run_cli(self, paths):
        command = [
            sys.executable,
            "-m",
            "tools.upstream.align_hd4_packs",
            "--fork-pack", str(paths["fork"]),
            "--classic-pack", str(paths["classic"]),
            "--header", str(paths["header"]),
            "--list", str(paths["list"]),
            "--out", str(paths["out"]),
            "--report", str(paths["report"]),
        ]
        result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
        self.assertNotIn("No module named", result.stderr, msg=result.stderr)
        return result

    def assert_success(self, result):
        self.assertEqual(result.returncode, 0, msg=result.stderr)

    def assert_failure_without_outputs(self, result, paths):
        self.assertEqual(result.returncode, 1, msg=result.stderr)
        self.assertTrue(result.stderr.strip(), msg=result.stderr)
        self.assertFalse(paths["out"].exists())
        self.assertFalse(paths["report"].exists())

    def assert_invalid_case(self, *, header, fork, classic, list_value):
        with tempfile.TemporaryDirectory(prefix="align-invalid-", dir=TMP_ROOT) as temp:
            paths = self.make_case(
                Path(temp),
                header=header,
                fork=fork,
                classic=classic,
                list_value=list_value,
            )
            result = self.run_cli(paths)
            self.assert_failure_without_outputs(result, paths)

    def test_constant_layout_and_report(self):
        fork = [
            ("C0", "png", png_rgba(1)),
            ("C1", "png", png_rgba(2)),
            ("HM_X", "png", png_rgba(3)),
            ("C3", "png", png_rgba(4)),
            ("HM_Y", "png", png_rgba(5)),
        ]
        classic = [
            ("C0", "png", png_rgba(6)),
            ("C1", "png", png_rgba(7)),
            ("C2", "png", png_rgba(8)),
            ("C3", "png", png_rgba(9)),
        ]
        header = (
            "#define C0 0 // first\n"
            "inline constexpr int C1 = 1; // second\n"
            "static constexpr int C2 = 2; /* third */\n"
            "constexpr int C3 = 3; // fourth\n"
        )
        with tempfile.TemporaryDirectory(prefix="align-layout-", dir=TMP_ROOT) as temp:
            root = Path(temp)
            paths = self.make_case(
                root,
                header=header,
                fork=fork,
                classic=classic,
                list_value={"aligned_hd4.dat": ["C2"]},
            )
            result = self.run_cli(paths)
            self.assert_success(result)
            actual = read_pack(paths["out"])
            self.assertEqual(
                [(name, extension) for name, extension, _ in actual],
                [("C0", "png"), ("C1", "png"), ("C2", "png"),
                 ("C3", "png"), ("HM_Y", "png"), ("HM_X", "png")],
            )
            self.assertEqual(
                [entry for entry in actual if entry[0] != "C2"],
                [fork[0], fork[1], fork[3], fork[4], fork[2]],
            )
            report_lines = paths["report"].read_text(encoding="utf-8").splitlines()
            self.assertEqual(
                report_lines[0], "index\tname\tsource\tfork_index\tsha256"
            )
            self.assertEqual(
                report_lines,
                [
                    "index\tname\tsource\tfork_index\tsha256",
                    *[
                        "\t".join((str(index), name, source, fork_index,
                                   hashlib.sha256(data).hexdigest()))
                        for index, (name, _, data), source, fork_index in zip(
                            range(6), actual,
                            ["fork", "fork", "classic_x4", "fork", "fork", "fork"],
                            ["0", "1", "-", "3", "4", "2"],
                        )
                    ],
                ],
            )

    def test_palette_classic_x4_preserves_transparency(self):
        from tools import hd_assets

        classic_bytes = png_palette_transparency()
        with tempfile.TemporaryDirectory(prefix="align-palette-", dir=TMP_ROOT) as temp:
            root = Path(temp)
            paths = self.make_case(
                root,
                header="#define C0 0\n",
                fork=[],
                classic=[("C0", "png", classic_bytes)],
                list_value={"aligned_hd4.dat": ["C0"]},
            )
            result = self.run_cli(paths)
            self.assert_success(result)
            output_entry = read_pack(paths["out"])[0]
            original = hd_assets.decode_image(classic_bytes)
            self.assertIsNotNone(original)
            scaled = hd_assets.scale_image(original, 4)
            output = hd_assets.decode_image(output_entry[2])
            self.assertIsNotNone(output)
            self.assertEqual(original.mode, "P")
            self.assertEqual(original.info.get("transparency"), 0)
            self.assertEqual(output.size, scaled.size)
            self.assertEqual(output.convert("RGBA").tobytes(),
                             scaled.convert("RGBA").tobytes())

    def test_rgba_classic_x4_pixels(self):
        from tools import hd_assets

        classic_bytes = png_rgba(10)
        with tempfile.TemporaryDirectory(prefix="align-rgba-", dir=TMP_ROOT) as temp:
            root = Path(temp)
            paths = self.make_case(
                root,
                header="#define C0 0\n",
                fork=[],
                classic=[("C0", "png", classic_bytes)],
                list_value={"aligned_hd4.dat": ["C0"]},
            )
            result = self.run_cli(paths)
            self.assert_success(result)
            output_entry = read_pack(paths["out"])[0]
            original = hd_assets.decode_image(classic_bytes)
            self.assertIsNotNone(original)
            scaled = hd_assets.scale_image(original, 4)
            output = hd_assets.decode_image(output_entry[2])
            self.assertIsNotNone(output)
            self.assertEqual(original.mode, "RGBA")
            self.assertEqual(output.size, scaled.size)
            self.assertEqual(output.convert("RGBA").tobytes(),
                             scaled.convert("RGBA").tobytes())

    def test_fork_pack_is_copied_byte_for_byte_with_reversed_payloads(self):
        fork = [("C0", "png", png_rgba(11)), ("C1", "png", png_rgba(12))]
        with tempfile.TemporaryDirectory(prefix="align-copy-", dir=TMP_ROOT) as temp:
            root = Path(temp)
            paths = self.make_case(
                root,
                header="#define C0 0\n#define C1 1\n",
                fork=fork,
                classic=[("C0", "png", png_rgba(13)),
                         ("C1", "png", png_rgba(14))],
                list_value={},
                reverse_payload=True,
            )
            source_bytes = paths["fork"].read_bytes()
            result = self.run_cli(paths)
            self.assert_success(result)
            self.assertEqual(paths["out"].read_bytes(), source_bytes)

    def test_list_uses_output_basename_and_missing_key_is_empty(self):
        with tempfile.TemporaryDirectory(prefix="align-list-", dir=TMP_ROOT) as temp:
            root = Path(temp)
            paths = self.make_case(
                root,
                header="#define C0 0\n",
                fork=[],
                classic=[("C0", "png", png_rgba(15))],
                list_value={"other_hd4.dat": ["OTHER"],
                            "selected_hd4.dat": ["C0"]},
                out_name="selected_hd4.dat",
            )
            result = self.run_cli(paths)
            self.assert_success(result)
            self.assertEqual(read_pack(paths["out"])[0][0], "C0")

        with tempfile.TemporaryDirectory(prefix="align-list-missing-", dir=TMP_ROOT) as temp:
            root = Path(temp)
            paths = self.make_case(
                root,
                header="#define C0 0\n",
                fork=[],
                classic=[("C0", "png", png_rgba())],
                list_value={"other_hd4.dat": ["C0"]},
                out_name="selected_hd4.dat",
            )
            result = self.run_cli(paths)
            self.assert_failure_without_outputs(result, paths)

    def test_gap_in_constant_values_fails(self):
        self.assert_invalid_case(
            header="#define C0 0\n#define C2 2\n",
            fork=[],
            classic=[],
            list_value={},
        )

    def test_duplicate_constant_values_fail(self):
        self.assert_invalid_case(
            header="#define C0 0\n#define C1 0\n",
            fork=[],
            classic=[],
            list_value={},
        )

    def test_constant_missing_from_fork_and_list_fails(self):
        self.assert_invalid_case(
            header="#define C0 0\n",
            fork=[],
            classic=[("C0", "png", png_rgba(16))],
            list_value={},
        )

    def test_unused_classic_without_hd_name_fails(self):
        self.assert_invalid_case(
            header="#define C0 0\n",
            fork=[("C0", "png", png_rgba(17))],
            classic=[("C0", "png", png_rgba(18))],
            list_value={"aligned_hd4.dat": ["C0"]},
        )

    def test_wrong_classic_name_at_index_fails(self):
        self.assert_invalid_case(
            header="#define C0 0\n",
            fork=[],
            classic=[("WRONG", "png", png_rgba(19))],
            list_value={"aligned_hd4.dat": ["C0"]},
        )

    def test_constant_name_in_fork_tail_fails(self):
        self.assert_invalid_case(
            header="#define C0 0\n#define C1 1\n",
            fork=[("C1", "png", png_rgba(20)),
                  ("EXTRA", "png", png_rgba(21)),
                  ("C0", "png", png_rgba(22))],
            classic=[("C0", "png", png_rgba(23)),
                     ("C1", "png", png_rgba(24))],
            list_value={},
        )

    def test_invalid_classic_image_fails_without_outputs(self):
        with tempfile.TemporaryDirectory(prefix="align-image-error-", dir=TMP_ROOT) as temp:
            root = Path(temp)
            paths = self.make_case(
                root,
                header="#define C0 0\n",
                fork=[],
                classic=[("C0", "png", b"not an image")],
                list_value={"aligned_hd4.dat": ["C0"]},
            )
            result = self.run_cli(paths)
            self.assert_failure_without_outputs(result, paths)

    def test_duplicate_result_names_fail_without_outputs(self):
        with tempfile.TemporaryDirectory(prefix="align-duplicate-", dir=TMP_ROOT) as temp:
            root = Path(temp)
            paths = self.make_case(
                root,
                header="#define C0 0\n",
                fork=[("C0", "png", png_rgba(25)),
                      ("EXTRA", "png", png_rgba(26)),
                      ("EXTRA", "png", png_rgba(27))],
                classic=[("C0", "png", png_rgba(28))],
                list_value={},
            )
            result = self.run_cli(paths)
            self.assert_failure_without_outputs(result, paths)

    def test_invalid_arguments_return_two(self):
        result = subprocess.run(
            [sys.executable, "-m", "tools.upstream.align_hd4_packs"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertNotIn("No module named", result.stderr, msg=result.stderr)
        self.assertEqual(result.returncode, 2, msg=result.stderr)


if __name__ == "__main__":
    unittest.main()
