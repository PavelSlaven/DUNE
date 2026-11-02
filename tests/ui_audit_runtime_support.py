import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

RUNTIME_LINKS = ("campaign", "campaign_en", "data", "skirmish", "skirmish_en")
SETTINGS = {
    "ScreenWidth": "1024",
    "ScreenHeight": "768",
    "FullScreen": "false",
    "RenderScale": "0",
    "WorldScale": "0",
    "GraphicsMode": "HD",
    "Language": "ru",
}
TIMEOUT_SECONDS = 120


def apply_settings(text, values):
    for key, value in values.items():
        pattern = re.compile(rf"^{key}\s*=.*$", re.MULTILINE)
        line = f"{key}={value}"
        if pattern.search(text):
            text = pattern.sub(line, text, count=1)
        else:
            text = text.replace("[SETTINGS]", f"[SETTINGS]\n{line}", 1)
    return text


def make_runtime(executable, resources, directory):
    runtime = Path(directory) / "runtime"
    runtime.mkdir()
    shutil.copy2(executable, runtime / "d2tm")
    bin_dir = Path(resources) / "bin"
    for name in RUNTIME_LINKS:
        os.symlink(bin_dir / name, runtime / name)
    shutil.copy2(Path(resources) / "game.ini", runtime / "game.ini")
    settings = (bin_dir / "settings.ini").read_text(encoding="utf-8")
    (runtime / "settings.ini").write_text(apply_settings(settings, SETTINGS), encoding="utf-8")
    return runtime


def run_game(runtime, extra_args):
    environment = dict(os.environ)
    environment.update(
        SDL_VIDEODRIVER="dummy",
        SDL_RENDER_DRIVER="software",
        SDL_AUDIODRIVER="dummy",
    )
    command = [
        str(runtime / "d2tm"),
        "-windowed",
        "-screenWidth", "1024",
        "-screenHeight", "768",
        *extra_args,
    ]
    return subprocess.run(
        command,
        cwd=runtime,
        env=environment,
        check=False,
        capture_output=True,
        text=True,
        timeout=TIMEOUT_SECONDS,
    )


class GameRun:
    def __init__(self, executable, resources):
        self.executable = executable
        self.resources = resources
        self.directory = tempfile.TemporaryDirectory(prefix="ui-audit-test-")
        self.out = Path(self.directory.name) / "out"
        self.out.mkdir()
        self.runtime = make_runtime(executable, resources, self.directory.name)

    def run(self, extra_args):
        return run_game(self.runtime, extra_args)

    def close(self):
        self.directory.cleanup()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()
        return False


def png_size(path):
    data = Path(path).read_bytes()
    if len(data) < 24 or data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
        raise ValueError(f"not a PNG: {path}")
    return int.from_bytes(data[16:20], "big"), int.from_bytes(data[20:24], "big")


def read_catalog(stdout):
    import json

    catalog = json.loads(stdout)
    scenes = catalog["scenes"]
    return {scene["id"]: scene for scene in scenes}
