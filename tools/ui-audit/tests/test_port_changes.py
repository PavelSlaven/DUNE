import argparse
import json
import os
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import check_screens
import combos
import finalize_png
import find_hit_tests
import run_all
import run_combo

EXCLUSIONS = (
    "name\treason\n"
    "GAME_INTRO\tвступительный ролик без интерфейса игры\n"
    "GAME_OVER\tпереходное состояние без собственного экрана\n"
    "GAME_INITIALIZE\tслужебное состояние загрузки без собственного экрана\n"
    "GAME_MAX_STATES\tсчётчик перечисления, не состояние\n"
    "cGameState\tабстрактный базовый класс состояний\n"
    "AbstractMentat\tабстрактный базовый класс брифингов\n"
    "GAME_SKIRMISH\tопределение состояния нигде не используется в коде; игра по схватке идёт в состоянии GAME_PLAYING\n"
    "cRegion\tкласс данных области на карте завоевания, не экран; отрисовывается внутри cSelectYourNextConquestState\n"
    "cMentatState\tэкран брифинга ментата; сцены режима названы классами ментатов AtreidesMentat, HarkonnenMentat, OrdosMentat, SardaukarMentat\n"
    "cTellHouseState\tэкран рассказа о Доме; сцены режима названы классом ментата BeneMentat\n"
    "cCreatorState\tсоздаёт и хранит состояния игры, не экран\n"
)


class PortChanges(unittest.TestCase):
    def assert_run_dir_command(self, command, run_dir):
        self.assertIn(("--run-dir", run_dir), list(zip(command, command[1:])))
        self.assertNotIn("--exe", command)
        self.assertNotIn("--resources", command)

    def test_a_languages(self):
        self.assertEqual(combos.LANGUAGES, ("en",))

    def test_a_generated_combinations(self):
        generated = combos.generate({"1024x768": {"render": [100], "world": [100]}})
        self.assertEqual([combos.combo_id(combo) for combo in generated], [
            "1024x768/en/hd", "1024x768/en/hd/r100w0",
            "1024x768/en/hd/r0w100", "1024x768/en/hd/r100w100",
        ])

    def test_b1_removed_runtime_settings_api(self):
        self.assertFalse(hasattr(run_combo, "RUNTIME_LINKS"))
        self.assertFalse(hasattr(run_combo, "apply_settings"))

    def test_b2_runtime_constants(self):
        self.assertEqual(run_combo.RUNTIME_SKIP, ("nlog.txt", "nlog.txt.backup"))
        self.assertEqual(run_combo.PREFERENCES_PATH, ("xdg", "D2TM", "Dune II - The Maker", "preferences.ini"))

    def test_b3_runtime_links_and_preferences(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            installation = root / "installation"
            installation.mkdir()
            for name in ("d2tm", "nlog.txt", "nlog.txt.backup", "settings.ini", "game.ini"):
                (installation / name).write_text(name, encoding="utf-8")
            (installation / "data").mkdir()
            runtime = root / "runtime"
            runtime.mkdir()
            (runtime / "old.txt").write_text("старые данные", encoding="utf-8")
            combo = combos.parse_id("1366x768/en/hd/r125w110")
            self.assertEqual(run_combo.make_runtime(installation, runtime, combo), runtime)
            self.assertEqual({path.name for path in runtime.iterdir()}, {"d2tm", "settings.ini", "game.ini", "data", "xdg"})
            for name in ("d2tm", "settings.ini", "game.ini", "data"):
                self.assertTrue((runtime / name).is_symlink(), name)
                self.assertEqual(os.readlink(runtime / name), str(installation / name))
            preferences = runtime / "xdg" / "D2TM" / "Dune II - The Maker" / "preferences.ini"
            self.assertEqual(preferences.read_text(encoding="utf-8"),
                             "[SETTINGS]\nScreenWidth=1366\nScreenHeight=768\nFullScreen=false\nRenderScale=125\nWorldScale=110\n")
            self.assertFalse((runtime / "old.txt").exists())

    def test_b4_game_environment(self):
        with patch.dict(os.environ, {"XDG_DATA_HOME": "/keep", "P5TT_MARKER": "1"}):
            inherited = run_combo.game_environment()
            isolated = run_combo.game_environment(Path("/x/xdg"))
            self.assertEqual(inherited["XDG_DATA_HOME"], "/keep")
            self.assertEqual(isolated["XDG_DATA_HOME"], "/x/xdg")
            for environment in (inherited, isolated):
                self.assertEqual(environment["P5TT_MARKER"], "1")
                self.assertEqual(environment["SDL_VIDEODRIVER"], "dummy")
                self.assertEqual(environment["SDL_RENDER_DRIVER"], "software")
                self.assertEqual(environment["SDL_AUDIODRIVER"], "dummy")
            self.assertEqual(os.environ["XDG_DATA_HOME"], "/keep")

    def test_b5_scene_command_and_environment(self):
        with tempfile.TemporaryDirectory() as directory:
            runtime = Path(directory) / "runtime"
            out = Path(directory) / "out"
            with patch.object(run_combo.subprocess, "run") as launch:
                run_combo.run_scene(runtime, combos.parse_id("1366x768/en/hd"), "s1", out)
            launch.assert_called_once()
            self.assertEqual(launch.call_args.args[0], [
                str(runtime / "d2tm"), "-windowed", "-screenWidth", "1366", "-screenHeight", "768",
                "--ui-audit-scene", "s1", "--ui-audit-out", str(out),
            ])
            self.assertEqual(launch.call_args.kwargs["cwd"], runtime)
            self.assertEqual(launch.call_args.kwargs["env"]["XDG_DATA_HOME"], str(runtime / "xdg"))

    def test_b6_combo_creates_runtime_from_installation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            installation = root / "installation"
            installation.mkdir()
            runtime = root / "runtime"
            runtime.mkdir()
            combo = combos.parse_id("1024x768/en/hd")
            with patch.object(run_combo, "make_runtime", return_value=runtime) as make_runtime, \
                    patch.object(run_combo, "run_scene", return_value=subprocess.CompletedProcess([], 1, "", "")):
                run_combo.run_combo(installation, combo, root, [{"id": "s1"}])
            make_runtime.assert_called_once_with(installation, root / "work" / "1024x768_en_hd" / "runtime", combo)

    def test_b7_rejects_old_arguments(self):
        with tempfile.TemporaryDirectory() as directory:
            for arguments in (["--exe", "x", "--resources", "y"], ["--run-dir", directory, "--exe", "x"]):
                with self.subTest(arguments=arguments), redirect_stderr(StringIO()), \
                        patch.object(run_combo, "list_scenes", return_value=[]), \
                        patch.object(run_combo, "run_combo", return_value=[]):
                    with self.assertRaises(SystemExit) as raised:
                        run_combo.main([*arguments, "--out", directory, "--combo", "1024x768/en/hd"])
                    self.assertEqual(raised.exception.code, 2)

    def test_b7_resolves_installation_and_lists_scenes(self):
        with tempfile.TemporaryDirectory() as directory:
            run_dir = Path(directory) / "installation" / ".."
            scenes = [{"id": "main-menu"}]
            with patch.object(run_combo, "list_scenes", return_value=scenes) as list_scenes, \
                    patch.object(run_combo, "run_combo", return_value=[]) as capture:
                result = run_combo.main(["--run-dir", str(run_dir), "--out", directory,
                                         "--combo", "1024x768/en/hd", "--min-free-gb", "0"])
            self.assertEqual(result, 0)
            list_scenes.assert_called_once_with(run_dir.resolve() / "d2tm")
            capture.assert_called_once_with(str(run_dir.resolve()), combos.parse_id("1024x768/en/hd"),
                                            str(Path(directory).resolve()), scenes, None)

    def test_b7_help_uses_english_combination(self):
        output = StringIO()
        with redirect_stdout(output), self.assertRaises(SystemExit) as raised:
            run_combo.main(["--help"])
        self.assertEqual(raised.exception.code, 0)
        self.assertIn("1024x768/en/hd", output.getvalue())

    def test_c_rejects_old_arguments(self):
        with tempfile.TemporaryDirectory() as directory:
            catalog = Path(directory) / "catalog.json"
            catalog.write_text('{"scenes": []}', encoding="utf-8")
            for arguments in (["--exe", "x", "--resources", "y"], ["--run-dir", directory, "--resources", "y"]):
                with self.subTest(arguments=arguments), redirect_stderr(StringIO()), redirect_stdout(StringIO()), \
                        patch.object(run_all, "scales_for", return_value={}):
                    with self.assertRaises(SystemExit) as raised:
                        run_all.main([*arguments, "--out", directory, "--catalog", str(catalog)])
                    self.assertEqual(raised.exception.code, 2)

    def test_c_resolves_installation_for_scales(self):
        with tempfile.TemporaryDirectory() as directory:
            catalog = Path(directory) / "catalog.json"
            catalog.write_text('{"scenes": []}', encoding="utf-8")
            run_dir = Path(directory) / "installation" / ".."
            with patch.object(run_all, "scales_for", return_value={"1024x768": {"render": [], "world": []}}) as scales, \
                    redirect_stdout(StringIO()):
                result = run_all.main(["--run-dir", str(run_dir), "--out", directory, "--catalog", str(catalog),
                                       "--resolutions", "1024x768", "--list"])
            self.assertEqual(result, 0)
            scales.assert_called_once_with(run_dir.resolve() / "d2tm", ["1024x768"])

    def test_c_run_one_forwards_run_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            args = argparse.Namespace(run_dir=str(Path(directory) / "installation"), out=directory, min_free_gb=0)
            with patch.object(run_all.subprocess, "run", return_value=subprocess.CompletedProcess([], 0)) as launch:
                run_all.run_one(args, combos.parse_id("1024x768/en/hd"), StringIO())
            launch.assert_called_once()
            self.assert_run_dir_command(launch.call_args.args[0], args.run_dir)

    def test_d_rejects_old_arguments(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "order.json").write_text("[]", encoding="utf-8")
            flags = root / "flags.json"
            flags.write_text("[]", encoding="utf-8")
            for arguments in (["--exe", "x", "--resources", "y"], ["--run-dir", directory, "--exe", "x"]):
                with self.subTest(arguments=arguments), redirect_stderr(StringIO()), redirect_stdout(StringIO()), \
                        patch.object(finalize_png, "plan_actions", return_value=([], [])):
                    with self.assertRaises(SystemExit) as raised:
                        finalize_png.main([*arguments, "--out", directory, "--flags", str(flags)])
                    self.assertEqual(raised.exception.code, 2)

    def test_d_forwards_run_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "order.json").write_text('["1024x768/en/hd"]', encoding="utf-8")
            flags = root / "flags.json"
            flags.write_text("[]", encoding="utf-8")
            run_dir = str(root / "installation")
            with patch.object(finalize_png, "plan_actions", return_value=([("1024x768/en/hd", "main-menu")], [])), \
                    patch.object(finalize_png.subprocess, "run", return_value=subprocess.CompletedProcess([], 0)) as launch, \
                    redirect_stdout(StringIO()):
                result = finalize_png.main(["--run-dir", run_dir, "--out", directory, "--flags", str(flags)])
            self.assertEqual(result, 0)
            launch.assert_called_once()
            self.assert_run_dir_command(launch.call_args.args[0], run_dir)

    def test_e_constexpr_states(self):
        source = ("inline constexpr int GAME_INITIALIZE = -1;      // initialize game\n"
                  "inline constexpr int GAME_MENU = 1;      // in a menu\n#define GAME_OLD 3\n")
        self.assertEqual(check_screens.code_states(source), ["GAME_INITIALIZE", "GAME_MENU"])

    def test_e_collects_port_states_and_classes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            sources = {
                "src/include/eGameState.h": "inline constexpr int GAME_MENU = 1;\ninline constexpr int GAME_REGION = 6;\n",
                "src/gamestates/cA.h": "class cA {\n",
                "src/gameobjects/mentat/M.h": "class M : public X {\n",
            }
            for name, text in sources.items():
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(text, encoding="utf-8")
            self.assertEqual(check_screens.collect_code_names(root), ["GAME_MENU", "GAME_REGION", "M", "cA"])

    def test_e_has_no_class_files(self):
        self.assertFalse(hasattr(check_screens, "CLASS_FILES"))

    def test_f_directories(self):
        self.assertEqual(find_hit_tests.DIRECTORIES, (
            "src/gui", "src/drawers", "src/gamestates", "src/managers", "src/sidebar",
            "src/gameobjects/mentat", "src/controls", "src/debug",
        ))

    def test_f_scan_uses_port_mentat_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in ("src/gameobjects/mentat/x.cpp", "src/mentat/y.cpp", "src/save/z.cpp"):
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("void A::f()\n{\n    if (isInside(1, 2)) {\n    }\n}\n", encoding="utf-8")
            rows = find_hit_tests.scan(root)
            self.assertTrue(rows)
            self.assertEqual({row[0] for row in rows}, {"src/gameobjects/mentat/x.cpp"})

    def test_g_exclusions_text(self):
        path = Path(__file__).resolve().parents[1] / "exclusions.tsv"
        self.assertEqual(path.read_text(encoding="utf-8"), EXCLUSIONS)

    def test_g_exclusions_exist_in_port_code(self):
        path = Path(__file__).resolve().parents[1] / "exclusions.tsv"
        names = check_screens.collect_code_names(Path(__file__).resolve().parents[3])
        for line in path.read_text(encoding="utf-8").splitlines()[1:]:
            with self.subTest(line=line):
                self.assertIn(line.split("\t")[0], names)


if __name__ == "__main__":
    unittest.main()
