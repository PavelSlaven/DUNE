import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import reference_shots  # noqa: E402


def temporary_root(test_case):
    temporary = tempfile.TemporaryDirectory()
    test_case.addCleanup(temporary.cleanup)
    return Path(temporary.name)


def write_png(path, size, color=(0, 0, 0)):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    Image.new("RGB", size, color).save(path)
    return path


class FakeRunner:
    def __init__(self, catalog, exit_codes=None, timeouts=None, saves=False, render_scale=0, language="ru"):
        self.catalog = list(catalog)
        self.exit_codes = dict(exit_codes or {})
        self.timeouts = dict(timeouts or {})
        self.saves = saves
        self.render_scale = render_scale
        self.language = language
        self.calls = []
        self.scene_calls = {}

    def __call__(self, command, cwd, env, timeout):
        self.calls.append(list(command))
        if "--ui-audit-list" in command:
            stdout = json.dumps({"scenes": [{"id": scene} for scene in self.catalog]})
            return SimpleNamespace(returncode=0, stdout=stdout, stderr="")

        scene = command[command.index("--ui-audit-scene") + 1]
        out_dir = Path(command[command.index("--ui-audit-out") + 1])
        width = int(command[command.index("-screenWidth") + 1])
        height = int(command[command.index("-screenHeight") + 1])
        attempt = self.scene_calls.get(scene, 0)
        self.scene_calls[scene] = attempt + 1
        if attempt < self.timeouts.get(scene, 0):
            raise subprocess.TimeoutExpired(command, timeout)

        out_dir.mkdir(parents=True, exist_ok=True)
        write_png(out_dir / f"{scene}.png", (width, height))
        header = {
            "k": "header",
            "scene": scene,
            "resolution": f"{width}x{height}",
            "language": self.language,
            "graphics": "hd",
            "canvas": {"w": width, "h": height},
            "game_screen": False,
            "render_scale": self.render_scale,
            "world_scale": 0,
        }
        (out_dir / f"{scene}.geometry.jsonl").write_text(
            json.dumps(header) + "\n", encoding="utf-8"
        )
        if self.saves:
            saves_dir = out_dir / "saves"
            saves_dir.mkdir(parents=True, exist_ok=True)
            (saves_dir / "x.d2s").write_bytes(b"save")
        return SimpleNamespace(returncode=self.exit_codes.get(scene, 0), stdout="", stderr="")


class PairsFile(unittest.TestCase):
    def test_pairs_file_has_27_unique_pairs(self):
        path = Path(__file__).resolve().parents[1] / "reference_pairs.tsv"
        pairs = reference_shots.parse_pairs(path)
        self.assertEqual(len(pairs), 27)
        self.assertEqual(len({pair.name for pair in pairs}), 27)
        self.assertTrue(all(pair.port_scene for pair in pairs))

    def test_only_two_pairs_lack_a_fork_scene(self):
        path = Path(__file__).resolve().parents[1] / "reference_pairs.tsv"
        pairs = reference_shots.parse_pairs(path)
        self.assertEqual(
            {pair.name for pair in pairs if pair.fork_scene is None},
            {"skirmish-hud", "mentat-briefing-sardaukar"},
        )

    def test_battle_pairs_use_three_resolutions_and_the_rest_one(self):
        path = Path(__file__).resolve().parents[1] / "reference_pairs.tsv"
        pairs = reference_shots.parse_pairs(path)
        battles = {"skirmish-hud", "mission-hud"}
        self.assertEqual(
            {pair.name: pair.resolutions for pair in pairs if pair.name in battles},
            {
                "skirmish-hud": [(800, 600), (1920, 1080), (5120, 1440)],
                "mission-hud": [(800, 600), (1920, 1080), (5120, 1440)],
            },
        )
        self.assertTrue(
            all(pair.resolutions == [(1920, 1080)] for pair in pairs if pair.name not in battles)
        )
        self.assertEqual(sum(len(pair.resolutions) for pair in pairs), 31)

    def test_parse_rejects_bad_files(self):
        root = temporary_root(self)
        path = root / "bad.tsv"
        header = "pair\tfork_scene\tport_scene\tresolutions\tnote\n"
        cases = [
            "x\ta\tb\t800x600\t-\nx\ta\tb\t800x600\t-\n",
            "x\ta\tb\t800*600\t-\n",
            "x\ta\t-\t800x600\t-\n",
            "x\tsave-dialog-load\tb\t800x600\t-\n",
            "x\ta\tb\t800x600\n",
        ]
        for contents in cases:
            with self.subTest(contents=contents):
                path.write_text(header + contents, encoding="utf-8")
                with self.assertRaises(ValueError):
                    reference_shots.parse_pairs(path)

    def test_save_writing_fork_scenes_are_pinned(self):
        self.assertEqual(
            reference_shots.SAVE_WRITING_FORK_SCENES,
            frozenset(
                {
                    "main-menu-saves",
                    "save-dialog-menu",
                    "options-game-main-saves",
                    "options-game-applied",
                    "options-game-game",
                    "options-game-controls",
                    "options-game-diagnostics",
                    "options-game-keybind",
                    "save-dialog-load",
                    "save-dialog-save-new",
                    "save-dialog-overwrite",
                    "save-dialog-load-error",
                    "save-dialog-save-error",
                }
            ),
        )

    def test_gallery_file_lists_the_five_readme_files(self):
        path = Path(__file__).resolve().parents[1] / "reference_gallery.tsv"
        rows = reference_shots.parse_gallery(path)
        self.assertEqual(len(rows), 5)
        self.assertEqual(
            {row.file for row in rows},
            {
                "main-menu.png",
                "house-selection.png",
                "ordos-briefing.png",
                "skirmish-gameplay.png",
                "victory-screen.png",
            },
        )
        self.assertTrue(all(row.resolution == (1920, 1080) for row in rows))


class Command(unittest.TestCase):
    def test_fork_command_has_no_language_argument(self):
        self.assertEqual(
            reference_shots.scene_command(
                Path("d"), "old", "main-menu", 1920, 1080, Path("o"), "ru"
            ),
            [
                "d",
                "-windowed",
                "-screenWidth",
                "1920",
                "-screenHeight",
                "1080",
                "--ui-audit-scene",
                "main-menu",
                "--ui-audit-out",
                "o",
            ],
        )

    def test_port_command_ends_with_language_argument(self):
        self.assertEqual(
            reference_shots.scene_command(
                Path("d"), "new", "main-menu", 1920, 1080, Path("o"), "en"
            ),
            [
                "d",
                "-windowed",
                "-screenWidth",
                "1920",
                "-screenHeight",
                "1080",
                "--ui-audit-scene",
                "main-menu",
                "--ui-audit-out",
                "o",
                "--ui-audit-language",
                "en",
            ],
        )

    def test_executable_name_by_platform(self):
        self.assertEqual(reference_shots.executable_name("nt"), "d2tm.exe")
        self.assertEqual(reference_shots.executable_name("posix"), "d2tm")

    def test_headless_environment(self):
        headless = reference_shots.game_environment({"A": "1"}, True, Path("x"))
        self.assertEqual(
            headless,
            {
                "A": "1",
                "SDL_VIDEODRIVER": "dummy",
                "SDL_RENDER_DRIVER": "software",
                "SDL_AUDIODRIVER": "dummy",
                "XDG_DATA_HOME": str(Path("x")),
            },
        )
        self.assertEqual(reference_shots.game_environment({"A": "1"}, False, Path("x")), {"A": "1"})


class Checks(unittest.TestCase):
    def test_png_size_reads_the_header_and_rejects_other_files(self):
        root = temporary_root(self)
        png = write_png(root / "image.png", (7, 5))
        self.assertEqual(reference_shots.png_size(png), (7, 5))
        invalid = root / "invalid.png"
        invalid.write_bytes(b"x" * 30)
        short = root / "short.png"
        short.write_bytes(b"x" * 5)
        with self.assertRaises(ValueError):
            reference_shots.png_size(invalid)
        with self.assertRaises(ValueError):
            reference_shots.png_size(short)

    def test_read_header_returns_the_first_record(self):
        root = temporary_root(self)
        header = root / "header.jsonl"
        header.write_text('{"k":"header","a":1}\n{"k":"text"}\n', encoding="utf-8")
        self.assertEqual(reference_shots.read_header(header), {"k": "header", "a": 1})
        invalid = root / "invalid.jsonl"
        invalid.write_text('{"k":"text"}\n', encoding="utf-8")
        with self.assertRaises(ValueError):
            reference_shots.read_header(invalid)

    def test_cell_without_problems(self):
        self.assertEqual(
            reference_shots.cell_problems(
                "new", 0, (1920, 1080), {"render_scale": 0, "world_scale": 0, "language": "en"},
                1920, 1080, "ru"
            ),
            [],
        )
        self.assertEqual(
            reference_shots.cell_problems(
                "old", 0, (1920, 1080), {"render_scale": 0, "world_scale": 0, "language": "ru"},
                1920, 1080, "ru"
            ),
            [],
        )

    def test_cell_problems_are_named(self):
        def problems(exit_code=0, size=(1920, 1080), render_scale=0, world_scale=0, language="ru", header=True,
                     side="old"):
            geometry = (
                {"render_scale": render_scale, "world_scale": world_scale, "language": language}
                if header
                else None
            )
            return reference_shots.cell_problems(
                side, exit_code, size, geometry, 1920, 1080, "ru"
            )

        checks = [
            (problems(exit_code=1), ["exit=1"]),
            (problems(size=(1920, 1000)), ["png-size=1920x1000"]),
            (problems(render_scale=125), ["render-scale=125"]),
            (problems(world_scale=110), ["world-scale=110"]),
            (problems(language="en"), ["language=en"]),
            (problems(language="en", side="new"), []),
            (problems(size=None, header=False), []),
        ]
        for actual, expected in checks:
            with self.subTest(actual=actual, expected=expected):
                self.assertEqual(actual, expected)


class Sheet(unittest.TestCase):
    def test_sheet_size_per_resolution(self):
        root = temporary_root(self)
        expected = [
            ((1920, 1080), (2576, 748)),
            ((800, 600), (1616, 628)),
            ((5120, 1440), (2576, 388)),
        ]
        for index, (size, sheet_size) in enumerate(expected):
            with self.subTest(size=size):
                new_png = write_png(root / f"new-{index}.png", size)
                out_png = root / f"sheet-{index}.png"
                reference_shots.compose_sheet(None, new_png, out_png, "title")
                with Image.open(out_png) as sheet:
                    self.assertEqual(sheet.size, sheet_size)

    def test_sheet_colours(self):
        root = temporary_root(self)
        old_png = write_png(root / "old.png", (800, 600), (200, 0, 0))
        new_png = write_png(root / "new.png", (800, 600), (0, 0, 200))
        out_png = root / "sheet.png"
        reference_shots.compose_sheet(old_png, new_png, out_png, "title")
        with Image.open(out_png) as sheet:
            self.assertEqual(sheet.getpixel((10, 38)), (200, 0, 0))
            self.assertEqual(sheet.getpixel((1616 - 10, 38)), (0, 0, 200))
            self.assertEqual(sheet.getpixel((808, 100)), reference_shots.BACKGROUND)

    def test_sheet_without_old_picture_has_grey_cell(self):
        root = temporary_root(self)
        new_png = write_png(root / "new.png", (800, 600), (0, 0, 200))
        out_png = root / "sheet.png"
        reference_shots.compose_sheet(None, new_png, out_png, "title")
        with Image.open(out_png) as sheet:
            self.assertEqual(sheet.getpixel((400, 328)), reference_shots.PLACEHOLDER)
            self.assertEqual(sheet.getpixel((1200, 328)), (0, 0, 200))


class RunReference(unittest.TestCase):
    def setUp(self):
        self.root = temporary_root(self)
        self.old_exe = self.root / "old" / "d2tm"
        self.new_exe = self.root / "new" / "d2tm"
        self.old_exe.parent.mkdir(parents=True)
        self.new_exe.parent.mkdir(parents=True)

    def scene_commands(self, runner):
        return [
            command[command.index("--ui-audit-scene") + 1]
            for command in runner.calls
            if "--ui-audit-scene" in command
        ]

    def test_run_reference_writes_table_files_and_sheets(self):
        pairs = [
            reference_shots.Pair("p1", "a", "b", [(800, 600)], "-"),
            reference_shots.Pair("p2", None, "c", [(800, 600)], "-"),
        ]
        runner = FakeRunner(["a", "b", "c"])
        out = self.root / "out"
        self.assertTrue(
            reference_shots.run_reference(
                pairs, out, self.new_exe, self.old_exe, None, "ru", runner, {}
            )
        )
        self.assertEqual(self.scene_commands(runner), ["a", "b", "c"])
        for relative in (
            "old/800x600/a.png",
            "new/800x600/b.png",
            "new/800x600/c.png",
            "sheets/p1_800x600.png",
            "sheets/p2_800x600.png",
        ):
            self.assertTrue((out / relative).is_file())
        lines = (out / "reference.tsv").read_text(encoding="utf-8").splitlines()
        self.assertEqual(lines[0], "\t".join(reference_shots.TABLE_HEADER))
        self.assertEqual(
            lines[1],
            "p1\t800x600\ta\tb\t0\t0\t800x600\t800x600\t800x600\t800x600\t"
            "old/800x600/a.png\tnew/800x600/b.png\tsheets/p1_800x600.png\tok",
        )
        self.assertEqual(
            lines[2],
            "p2\t800x600\t-\tc\t-\t0\t-\t800x600\t-\t800x600\t-\t"
            "new/800x600/c.png\tsheets/p2_800x600.png\tok",
        )
        self.assertEqual(len(lines), 3)

    def test_a_failed_scene_is_named_in_problems_and_fails_the_run(self):
        pairs = [
            reference_shots.Pair("p1", "a", "b", [(800, 600)], "-"),
            reference_shots.Pair("p2", None, "c", [(800, 600)], "-"),
        ]
        runner = FakeRunner(["a", "b", "c"], exit_codes={"b": 1})
        out = self.root / "out"
        self.assertFalse(
            reference_shots.run_reference(
                pairs, out, self.new_exe, self.old_exe, None, "ru", runner, {}
            )
        )
        row = dict(zip(reference_shots.TABLE_HEADER, (out / "reference.tsv").read_text(encoding="utf-8").splitlines()[1].split("\t")))
        self.assertEqual(row["problems"], "new:exit=1")
        self.assertEqual(row["new_exit"], "1")

    def test_timeout_is_retried_once(self):
        pairs = [
            reference_shots.Pair("p1", None, "b", [(800, 600)], "-"),
            reference_shots.Pair("p2", None, "c", [(800, 600)], "-"),
        ]
        runner = FakeRunner(["b", "c"], timeouts={"b": 1, "c": 2})
        out = self.root / "out"
        self.assertFalse(
            reference_shots.run_reference(
                pairs, out, self.new_exe, None, None, "ru", runner, {}
            )
        )
        self.assertEqual(self.scene_commands(runner).count("b"), 2)
        self.assertEqual(self.scene_commands(runner).count("c"), 2)
        lines = (out / "reference.tsv").read_text(encoding="utf-8").splitlines()
        first = dict(zip(reference_shots.TABLE_HEADER, lines[1].split("\t")))
        second = dict(zip(reference_shots.TABLE_HEADER, lines[2].split("\t")))
        self.assertEqual(first["problems"], "ok")
        self.assertEqual(second["new_exit"], "timeout")
        self.assertEqual(second["problems"], "new:timeout")
        self.assertEqual(second["sheet"], "-")

    def test_old_png_directory_mode_does_not_run_the_old_build(self):
        old_png_dir = self.root / "oldpng"
        old_png = write_png(old_png_dir / "800x600" / "a.png", (800, 600))
        pair = reference_shots.Pair("p1", "a", "b", [(800, 600)], "-")
        runner = FakeRunner(["a", "b"])
        out = self.root / "out"
        self.assertTrue(
            reference_shots.run_reference(
                [pair], out, self.new_exe, None, old_png_dir, "ru", runner, {}
            )
        )
        self.assertEqual(self.scene_commands(runner), ["b"])
        lines = (out / "reference.tsv").read_text(encoding="utf-8").splitlines()
        row = dict(zip(reference_shots.TABLE_HEADER, lines[1].split("\t")))
        self.assertEqual(row["old_exit"], "-")
        self.assertEqual(row["old_png_size"], "800x600")
        self.assertEqual(row["problems"], "ok")

        old_png.unlink()
        self.assertFalse(
            reference_shots.run_reference(
                [pair], out, self.new_exe, None, old_png_dir, "ru", FakeRunner(["a", "b"]), {}
            )
        )
        row = dict(zip(reference_shots.TABLE_HEADER, (out / "reference.tsv").read_text(encoding="utf-8").splitlines()[1].split("\t")))
        self.assertEqual(row["problems"], "old:no-png")

    def test_unknown_scene_is_not_run(self):
        pair = reference_shots.Pair("p1", "a", "b", [(800, 600)], "-")
        runner = FakeRunner(["a"])
        out = self.root / "out"
        self.assertFalse(
            reference_shots.run_reference(
                [pair], out, self.new_exe, self.old_exe, None, "ru", runner, {}
            )
        )
        self.assertEqual(self.scene_commands(runner), ["a"])
        lines = (out / "reference.tsv").read_text(encoding="utf-8").splitlines()
        row = dict(zip(reference_shots.TABLE_HEADER, lines[1].split("\t")))
        self.assertEqual(row["problems"], "new:no-scene")
        self.assertEqual(row["sheet"], "-")

    def test_saves_folder_is_removed(self):
        pair = reference_shots.Pair("p1", None, "b", [(800, 600)], "-")
        out = self.root / "out"
        reference_shots.run_reference(
            [pair], out, self.new_exe, None, None, "ru", FakeRunner(["b"], saves=True), {}
        )
        self.assertFalse((out / "new" / "800x600" / "saves").exists())
        self.assertTrue((out / "new" / "800x600" / "b.png").is_file())


class Gallery(unittest.TestCase):
    def test_gallery_copies_the_five_pictures(self):
        rows = [
            reference_shots.GalleryRow("one.png", "a", (800, 600)),
            reference_shots.GalleryRow("two.png", "b", (800, 600)),
        ]
        root = temporary_root(self)
        out = root / "out"
        self.assertTrue(
            reference_shots.run_gallery(rows, out, root / "new" / "d2tm", "ru", FakeRunner(["a", "b"]), {})
        )
        self.assertTrue((out / "gallery" / "one.png").is_file())
        self.assertTrue((out / "gallery" / "two.png").is_file())
        lines = (out / "gallery.tsv").read_text(encoding="utf-8").splitlines()
        self.assertEqual(lines[0], "\t".join(reference_shots.GALLERY_HEADER))
        self.assertEqual(lines[1], "one.png\ta\t800x600\t0\t800x600\t800x600\tok")
        self.assertEqual(lines[2], "two.png\tb\t800x600\t0\t800x600\t800x600\tok")
        self.assertEqual(len(lines), 3)

        failed_out = root / "failed"
        self.assertFalse(
            reference_shots.run_gallery(
                rows, failed_out, root / "new" / "d2tm", "ru", FakeRunner(["a", "b"], exit_codes={"b": 1}), {}
            )
        )
        self.assertFalse((failed_out / "gallery" / "two.png").exists())
        failed_lines = (failed_out / "gallery.tsv").read_text(encoding="utf-8").splitlines()
        row = dict(zip(reference_shots.GALLERY_HEADER, failed_lines[2].split("\t")))
        self.assertEqual(row["problems"], "exit=1")


class MainOptions(unittest.TestCase):
    def test_main_option_errors(self):
        root = temporary_root(self)
        new_dir = root / "new"
        old_dir = root / "old"
        new_dir.mkdir()
        old_dir.mkdir()
        with self.assertRaises(SystemExit) as missing_old:
            reference_shots.main(["--out", str(root / "out"), "--new-dir", str(new_dir)])
        self.assertEqual(missing_old.exception.code, 2)
        with self.assertRaises(SystemExit) as conflicting_old:
            reference_shots.main(
                [
                    "--out",
                    str(root / "out"),
                    "--new-dir",
                    str(new_dir),
                    "--old-dir",
                    str(old_dir),
                    "--no-old",
                ]
            )
        self.assertEqual(conflicting_old.exception.code, 2)
