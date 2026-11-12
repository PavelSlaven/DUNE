import argparse
import concurrent.futures
import json
import os
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import ui_audit_runtime_support as support  # noqa: E402


LATIN = re.compile(r"[A-Za-z]")
CYRILLIC = re.compile(r"[А-Яа-яЁё]")


def read_allowlist():
    path = Path(__file__).resolve().parent / "data" / "latin-ru-allowed.tsv"
    lines = path.read_text(encoding="utf-8").splitlines()
    return [re.compile(line.split("\t", 1)[0]) for line in lines[1:]]


def list_scenes(run_dir):
    environment = dict(os.environ)
    environment.update(
        SDL_VIDEODRIVER="dummy",
        SDL_RENDER_DRIVER="software",
        SDL_AUDIODRIVER="dummy",
    )
    result = subprocess.run(
        [str(run_dir / "d2tm"), "--ui-audit-list"],
        cwd=run_dir,
        env=environment,
        capture_output=True,
        text=True,
        timeout=60,
        check=True,
    )
    return [scene["id"] for scene in json.loads(result.stdout)["scenes"]]


def capture_scene(run_dir, scene_id, language):
    for _ in range(2):
        with support.GameRun(run_dir) as game:
            try:
                result = game.run([
                    "--ui-audit-scene",
                    scene_id,
                    "--ui-audit-out",
                    str(game.out),
                    "--ui-audit-language",
                    language,
                ])
            except subprocess.TimeoutExpired:
                continue
            geometry = game.out / f"{scene_id}.geometry.jsonl"
            if result.returncode != 0 or not geometry.is_file():
                continue
            records = [
                json.loads(line)
                for line in geometry.read_text(encoding="utf-8").splitlines()
            ]
            return [record["s"] for record in records if record.get("k") == "text"], None
    return None, f"{language} {scene_id}: the scene did not finish"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    args = parser.parse_args()
    run_dir = Path(args.run_dir).resolve()
    scenes = list_scenes(run_dir)
    allowlist = read_allowlist()
    captures = {}
    errors = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        futures = {
            executor.submit(capture_scene, run_dir, scene_id, language): (language, scene_id)
            for language in ("ru", "en")
            for scene_id in scenes
        }
        for future in concurrent.futures.as_completed(futures):
            language, scene_id = futures[future]
            texts, error = future.result()
            if error:
                errors.append(error)
            else:
                captures[(language, scene_id)] = texts

    russian_texts = []
    for (language, scene_id), texts in captures.items():
        if language == "ru":
            russian_texts.extend(texts)
            for text in texts:
                if LATIN.search(text) and not CYRILLIC.search(text) and not any(
                    pattern.fullmatch(text) for pattern in allowlist
                ):
                    errors.append(f"ru {scene_id}: untranslated text '{text}'")
        else:
            for text in texts:
                if CYRILLIC.search(text):
                    errors.append(f"en {scene_id}: Russian text '{text}'")

    for pattern in allowlist:
        if not any(pattern.fullmatch(text) for text in russian_texts):
            errors.append(f"allowlist entry '{pattern.pattern}' matched no text")

    for error in sorted(errors):
        print(error)
    print(f"translation: {len(scenes)} scenes, {len(errors)} failures")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
