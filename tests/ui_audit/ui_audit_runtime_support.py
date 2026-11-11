import json
import os
import subprocess
import tempfile
from pathlib import Path

TIMEOUT_SECONDS = 120
SCREEN_ARGS = ["-windowed", "-screenWidth", "1024", "-screenHeight", "768"]
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
PNG_END = b"\x00\x00\x00\x00IEND\xaeB`\x82"


class GameRun:
    def __init__(self, run_dir):
        self.run_dir = Path(run_dir).resolve()
        self.directory = tempfile.TemporaryDirectory(prefix="ui-audit-test-")
        root = Path(self.directory.name)
        self.out = root / "out"
        self.out.mkdir()
        self.xdg = root / "xdg"
        self.xdg.mkdir()

    def run(self, extra_args):
        environment = dict(os.environ)
        environment.update(
            SDL_VIDEODRIVER="dummy",
            SDL_RENDER_DRIVER="software",
            SDL_AUDIODRIVER="dummy",
            XDG_DATA_HOME=str(self.xdg),
        )
        return subprocess.run(
            [str(self.run_dir / "d2tm"), *SCREEN_ARGS, *extra_args],
            cwd=self.run_dir,
            env=environment,
            check=False,
            capture_output=True,
            text=True,
            timeout=TIMEOUT_SECONDS,
        )

    def preferences_files(self):
        return sorted(str(path) for path in self.xdg.rglob("preferences.ini") if path.is_file())

    def close(self):
        self.directory.cleanup()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()
        return False


def png_size(path):
    data = Path(path).read_bytes()
    if len(data) < 24 or data[:8] != PNG_SIGNATURE or data[12:16] != b"IHDR":
        raise ValueError(f"not a PNG: {path}")
    if b"IDAT" not in data or not data.endswith(PNG_END):
        raise ValueError(f"incomplete PNG: {path}")
    return int.from_bytes(data[16:20], "big"), int.from_bytes(data[20:24], "big")


def read_json(stdout):
    return json.loads(stdout.strip())


def same_json(actual, expected):
    return json.dumps(actual, sort_keys=True) == json.dumps(expected, sort_keys=True)
