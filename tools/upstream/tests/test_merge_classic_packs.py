import struct
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
TEMP_ROOT = ROOT / ".tmp/p2t"
HEADER = struct.Struct("<4sH")
ENTRY = struct.Struct("<40s4sII")


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


class MergeClassicPacksTests(unittest.TestCase):
    def setUp(self):
        TEMP_ROOT.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(prefix="merge-classic-", dir=TEMP_ROOT)
        self.work = Path(self.temp.name)
        self.base_dir = self.work / "base"
        self.fork_dir = self.work / "fork"
        self.upstream_dir = self.work / "upstream"
        self.out_dir = self.work / "out"
        self.report = self.work / "report.tsv"
        for directory in (
            self.base_dir, self.fork_dir, self.upstream_dir, self.out_dir
        ):
            directory.mkdir()

    def tearDown(self):
        self.temp.cleanup()

    def write_pack(self, side, relative, entries, reverse_payload=False):
        path = self.side_dir(side) / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(make_pack(entries, reverse_payload=reverse_payload))
        return path

    def side_dir(self, side):
        return {
            "base": self.base_dir,
            "fork": self.fork_dir,
            "upstream": self.upstream_dir,
        }[side]

    def run_merge(self):
        return subprocess.run(
            [
                sys.executable,
                "-m",
                "tools.upstream.merge_classic_packs",
                "--base-dir", str(self.base_dir),
                "--fork-dir", str(self.fork_dir),
                "--upstream-dir", str(self.upstream_dir),
                "--out-dir", str(self.out_dir),
                "--report", str(self.report),
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )

    def assert_exit_code(self, result, expected):
        if expected == 1:
            self.assertNotIn("No module named", result.stderr, msg=result.stderr)
        self.assertEqual(result.returncode, expected, msg=result.stderr)

    def assert_no_output_files(self):
        self.assertEqual(
            [path for path in self.out_dir.rglob("*") if path.is_file()], []
        )

    def test_fork_only_change_uses_fork_entry(self):
        base = [("A", "bin", b"base")]
        self.write_pack("base", "sdl_test.dat", base)
        self.write_pack("fork", "sdl_test.dat", [("A", "bin", b"fork")])
        self.write_pack("upstream", "sdl_test.dat", base)

        result = self.run_merge()

        self.assert_exit_code(result, 0)
        self.assertEqual(
            read_pack(self.out_dir / "sdl_test.dat"),
            [("A", "bin", b"fork")],
        )
        self.assertIn("sdl_test.dat\t0\tA#1\tchanged\tunchanged\tfork", self.report.read_text())

    def test_upstream_change_and_append_preserve_upstream_order_and_sources(self):
        base = [
            ("A", "bin", b"a-base"),
            ("B", "bin", b"b-base"),
            ("C", "bin", b"c-base"),
        ]
        upstream = [
            ("C", "bin", b"c-base"),
            ("A", "bin", b"a-upstream"),
            ("B", "bin", b"b-base"),
            ("D", "dat", b"d-added"),
        ]
        self.write_pack("base", "sdl_order.dat", base)
        self.write_pack("fork", "sdl_order.dat", base)
        self.write_pack("upstream", "sdl_order.dat", upstream)

        result = self.run_merge()

        self.assert_exit_code(result, 0)
        self.assertEqual(read_pack(self.out_dir / "sdl_order.dat"), upstream)
        self.assertEqual(
            self.report.read_text().splitlines(),
            [
                "pack\tindex\tkey\tfork\tupstream\tsource",
                "sdl_order.dat\t0\tC#1\tunchanged\tunchanged\tbase",
                "sdl_order.dat\t1\tA#1\tunchanged\tchanged\tupstream",
                "sdl_order.dat\t2\tB#1\tunchanged\tunchanged\tbase",
                "sdl_order.dat\t3\tD#1\tunchanged\tadded\tupstream",
            ],
        )

    def test_divergent_double_change_fails_without_outputs_and_names_key(self):
        self.write_pack("base", "conflict.dat", [("X", "bin", b"base")])
        self.write_pack("fork", "conflict.dat", [("X", "bin", b"fork")])
        self.write_pack("upstream", "conflict.dat", [("X", "bin", b"upstream")])

        result = self.run_merge()

        self.assert_exit_code(result, 1)
        self.assertIn("conflict.dat", result.stderr)
        self.assertIn("X#1", result.stderr)
        self.assert_no_output_files()

    def test_equal_double_change_succeeds(self):
        self.write_pack("base", "same_change.dat", [("X", "bin", b"base")])
        self.write_pack("fork", "same_change.dat", [("X", "bin", b"shared")])
        self.write_pack("upstream", "same_change.dat", [("X", "bin", b"shared")])

        result = self.run_merge()

        self.assert_exit_code(result, 0)
        self.assertEqual(
            read_pack(self.out_dir / "same_change.dat"),
            [("X", "bin", b"shared")],
        )

    def test_fork_added_entry_fails(self):
        self.write_pack("base", "added.dat", [("A", "bin", b"a")])
        self.write_pack("fork", "added.dat", [
            ("A", "bin", b"a"), ("B", "bin", b"b")
        ])
        self.write_pack("upstream", "added.dat", [("A", "bin", b"a")])

        result = self.run_merge()

        self.assert_exit_code(result, 1)
        self.assertIn("added.dat", result.stderr)
        self.assert_no_output_files()

    def test_fork_deleted_entry_fails(self):
        original = [("A", "bin", b"a"), ("B", "bin", b"b")]
        self.write_pack("base", "deleted.dat", original)
        self.write_pack("fork", "deleted.dat", [original[0]])
        self.write_pack("upstream", "deleted.dat", original)

        result = self.run_merge()

        self.assert_exit_code(result, 1)
        self.assertIn("deleted.dat", result.stderr)
        self.assert_no_output_files()

    def test_fork_reordered_entries_fails(self):
        original = [("A", "bin", b"a"), ("B", "bin", b"b")]
        self.write_pack("base", "reordered.dat", original)
        self.write_pack("fork", "reordered.dat", list(reversed(original)))
        self.write_pack("upstream", "reordered.dat", original)

        result = self.run_merge()

        self.assert_exit_code(result, 1)
        self.assertIn("reordered.dat", result.stderr)
        self.assert_no_output_files()

    def test_duplicate_names_use_occurrence_number_in_keys(self):
        base = [("X", "bin", b"first"), ("X", "bin", b"second")]
        fork = [("X", "bin", b"first"), ("X", "bin", b"fork-second")]
        upstream = [("X", "bin", b"upstream-first"), ("X", "bin", b"second")]
        self.write_pack("base", "duplicates.dat", base)
        self.write_pack("fork", "duplicates.dat", fork)
        self.write_pack("upstream", "duplicates.dat", upstream)

        result = self.run_merge()

        self.assert_exit_code(result, 0)
        self.assertEqual(read_pack(self.out_dir / "duplicates.dat"), [
            ("X", "bin", b"upstream-first"),
            ("X", "bin", b"fork-second"),
        ])
        self.assertEqual(
            [line.split("\t")[2] for line in self.report.read_text().splitlines()[1:]],
            ["X#1", "X#2"],
        )

    def test_upstream_equal_result_is_copied_byte_for_byte_with_reverse_payload(self):
        entries = [("A", "bin", b"first-data"), ("B", "dat", b"second-data")]
        self.write_pack("base", "copy_upstream.dat", entries)
        self.write_pack("fork", "copy_upstream.dat", entries)
        upstream_path = self.write_pack(
            "upstream", "copy_upstream.dat", entries, reverse_payload=True
        )

        result = self.run_merge()

        self.assert_exit_code(result, 0)
        self.assertEqual(
            (self.out_dir / "copy_upstream.dat").read_bytes(), upstream_path.read_bytes()
        )

    def test_fork_equal_result_is_copied_byte_for_byte_with_reverse_payload(self):
        base = [("A", "bin", b"first-data"), ("B", "dat", b"second-data")]
        fork = [("A", "bin", b"fork-data"), base[1]]
        self.write_pack("base", "copy_fork.dat", base)
        fork_path = self.write_pack(
            "fork", "copy_fork.dat", fork, reverse_payload=True
        )
        self.write_pack("upstream", "copy_fork.dat", base)

        result = self.run_merge()

        self.assert_exit_code(result, 0)
        self.assertEqual(
            (self.out_dir / "copy_fork.dat").read_bytes(), fork_path.read_bytes()
        )

    def test_only_upstream_pack_is_copied_and_reported(self):
        entries = [("UP_ONLY", "bin", b"upstream")]
        upstream_path = self.write_pack("upstream", "only_upstream.dat", entries)

        result = self.run_merge()

        self.assert_exit_code(result, 0)
        self.assertEqual(
            (self.out_dir / "only_upstream.dat").read_bytes(), upstream_path.read_bytes()
        )
        self.assertIn(
            "only_upstream.dat\t-\t-\t-\t-\tupstream-file",
            self.report.read_text(),
        )

    def test_only_fork_pack_is_copied_and_reported(self):
        entries = [("FORK_ONLY", "bin", b"fork")]
        fork_path = self.write_pack("fork", "only_fork.dat", entries)

        result = self.run_merge()

        self.assert_exit_code(result, 0)
        self.assertEqual(
            (self.out_dir / "only_fork.dat").read_bytes(), fork_path.read_bytes()
        )
        self.assertIn(
            "only_fork.dat\t-\t-\t-\t-\tfork-file",
            self.report.read_text(),
        )

    def test_no_base_equal_files_choose_upstream(self):
        entries = [("SAME", "bin", b"same")]
        self.write_pack("fork", "no_base_equal.dat", entries)
        upstream_path = self.write_pack("upstream", "no_base_equal.dat", entries)

        result = self.run_merge()

        self.assert_exit_code(result, 0)
        self.assertEqual(
            (self.out_dir / "no_base_equal.dat").read_bytes(), upstream_path.read_bytes()
        )
        self.assertIn(
            "no_base_equal.dat\t-\t-\t-\t-\tupstream-file",
            self.report.read_text(),
        )

    def test_no_base_equal_entries_with_different_physical_order_are_rejected(self):
        entries = [("A", "bin", b"first-data"), ("B", "dat", b"second-data")]
        fork_path = self.write_pack(
            "fork", "no_base_layout.dat", entries, reverse_payload=True
        )
        upstream_path = self.write_pack("upstream", "no_base_layout.dat", entries)
        self.assertEqual(read_pack(fork_path), read_pack(upstream_path))
        self.assertNotEqual(fork_path.read_bytes(), upstream_path.read_bytes())

        result = self.run_merge()

        self.assert_exit_code(result, 1)
        self.assertIn("no_base_layout.dat", result.stderr)
        self.assert_no_output_files()

    def test_no_base_different_files_fail(self):
        self.write_pack("fork", "no_base_different.dat", [("F", "bin", b"fork")])
        self.write_pack(
            "upstream", "no_base_different.dat", [("U", "bin", b"upstream")]
        )

        result = self.run_merge()

        self.assert_exit_code(result, 1)
        self.assertIn("no_base_different.dat", result.stderr)
        self.assert_no_output_files()

    def test_base_pack_missing_from_fork_with_upstream_fails(self):
        self.write_pack("base", "removed_with_upstream.dat", [("A", "bin", b"base")])
        self.write_pack(
            "upstream", "removed_with_upstream.dat", [("A", "bin", b"upstream")]
        )

        result = self.run_merge()

        self.assert_exit_code(result, 1)
        self.assertIn("removed_with_upstream.dat", result.stderr)
        self.assert_no_output_files()

    def test_base_pack_missing_from_fork_without_upstream_fails(self):
        self.write_pack("base", "removed_everywhere.dat", [("A", "bin", b"base")])

        result = self.run_merge()

        self.assert_exit_code(result, 1)
        self.assertIn("removed_everywhere.dat", result.stderr)
        self.assert_no_output_files()

    def test_base_pack_missing_from_upstream_fails(self):
        self.write_pack("base", "removed_upstream.dat", [("A", "bin", b"base")])
        self.write_pack("fork", "removed_upstream.dat", [("A", "bin", b"fork")])

        result = self.run_merge()

        self.assert_exit_code(result, 1)
        self.assertIn("removed_upstream.dat", result.stderr)
        self.assert_no_output_files()

    def test_hd4_files_and_hd4_scene_paths_are_excluded(self):
        for side in ("base", "fork", "upstream"):
            self.write_pack(side, "x_hd4.dat", [("EXCLUDED", "bin", b"x")])
            self.write_pack(side, "scenes/hd4/y.dat", [("EXCLUDED", "bin", b"y")])

        result = self.run_merge()

        self.assert_exit_code(result, 0)
        self.assertEqual(self.report.read_text(), "pack\tindex\tkey\tfork\tupstream\tsource\n")
        self.assertEqual(list(self.out_dir.rglob("*.dat")), [])

    def test_report_header_rows_indices_and_sorted_pack_paths_are_exact(self):
        only_fork_path = self.write_pack(
            "fork", "a_only_fork.dat", [("FORK_ONLY", "bin", b"fork file")]
        )
        only_upstream_path = self.write_pack(
            "upstream", "b_only_upstream.dat", [("UP_ONLY", "bin", b"upstream file")]
        )
        base = [("KEEP", "bin", b"same"), ("F", "dat", b"base")]
        fork = [("KEEP", "bin", b"same"), ("F", "dat", b"fork")]
        upstream = [
            ("KEEP", "bin", b"same"),
            ("U", "bin", b"added"),
            ("F", "dat", b"base"),
        ]
        self.write_pack("base", "c_merge.dat", base)
        self.write_pack("fork", "c_merge.dat", fork)
        self.write_pack("upstream", "c_merge.dat", upstream)

        result = self.run_merge()

        self.assert_exit_code(result, 0)
        self.assertEqual(
            (self.out_dir / "a_only_fork.dat").read_bytes(), only_fork_path.read_bytes()
        )
        self.assertEqual(
            (self.out_dir / "b_only_upstream.dat").read_bytes(),
            only_upstream_path.read_bytes(),
        )
        self.assertEqual(
            self.report.read_text(),
            "pack\tindex\tkey\tfork\tupstream\tsource\n"
            "a_only_fork.dat\t-\t-\t-\t-\tfork-file\n"
            "b_only_upstream.dat\t-\t-\t-\t-\tupstream-file\n"
            "c_merge.dat\t0\tKEEP#1\tunchanged\tunchanged\tbase\n"
            "c_merge.dat\t1\tU#1\tunchanged\tadded\tupstream\n"
            "c_merge.dat\t2\tF#1\tchanged\tunchanged\tfork\n",
        )

    def test_mixed_merge_keeps_entries_changed_by_neither_side(self):
        base = [
            ("FORK_ONLY", "bin", b"f-base"),
            ("UP_ONLY", "bin", b"u-base"),
            ("NEITHER", "bin", b"same"),
        ]
        fork = [
            ("FORK_ONLY", "bin", b"f-fork"),
            ("UP_ONLY", "bin", b"u-base"),
            ("NEITHER", "bin", b"same"),
        ]
        upstream = [
            ("UP_ONLY", "bin", b"u-upstream"),
            ("FORK_ONLY", "bin", b"f-base"),
            ("NEITHER", "bin", b"same"),
        ]
        self.write_pack("base", "mixed.dat", base)
        self.write_pack("fork", "mixed.dat", fork)
        self.write_pack("upstream", "mixed.dat", upstream)

        result = self.run_merge()

        self.assert_exit_code(result, 0)
        self.assertEqual(read_pack(self.out_dir / "mixed.dat"), [
            ("UP_ONLY", "bin", b"u-upstream"),
            ("FORK_ONLY", "bin", b"f-fork"),
            ("NEITHER", "bin", b"same"),
        ])
        rows = self.report.read_text().splitlines()[1:]
        self.assertEqual([row.rsplit("\t", 1)[1] for row in rows], [
            "upstream", "fork", "base"
        ])

    def test_upstream_deletion_of_fork_changed_key_is_conflict(self):
        base = [("X", "bin", b"base"), ("Y", "bin", b"y")]
        fork = [("X", "bin", b"fork"), ("Y", "bin", b"y")]
        upstream = [("Y", "bin", b"y")]
        self.write_pack("base", "deleted_key.dat", base)
        self.write_pack("fork", "deleted_key.dat", fork)
        self.write_pack("upstream", "deleted_key.dat", upstream)

        result = self.run_merge()

        self.assert_exit_code(result, 1)
        self.assertIn("deleted_key.dat", result.stderr)
        self.assertIn("X#1", result.stderr)
        self.assert_no_output_files()

    def test_error_across_several_packs_is_atomic(self):
        valid = [("A", "bin", b"base")]
        self.write_pack("base", "a_valid.dat", valid)
        self.write_pack("fork", "a_valid.dat", valid)
        self.write_pack("upstream", "a_valid.dat", valid)
        self.write_pack("base", "z_conflict.dat", [("X", "bin", b"base")])
        self.write_pack("fork", "z_conflict.dat", [("X", "bin", b"fork")])
        self.write_pack("upstream", "z_conflict.dat", [("X", "bin", b"upstream")])

        result = self.run_merge()

        self.assert_exit_code(result, 1)
        self.assertIn("z_conflict.dat", result.stderr)
        self.assert_no_output_files()

    def test_invalid_arguments_return_two(self):
        result = subprocess.run(
            [sys.executable, "-m", "tools.upstream.merge_classic_packs"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )

        self.assert_exit_code(result, 2)


if __name__ == "__main__":
    unittest.main()
