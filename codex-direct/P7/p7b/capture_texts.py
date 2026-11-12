#!/usr/bin/env python3
"""Run every UI audit scene in one language and list the drawn texts (lead's one-off fact collection)."""
import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

run_dir = Path(sys.argv[1]).resolve()
out_dir = Path(sys.argv[2]).resolve()
language = sys.argv[3]
workers = int(sys.argv[4]) if len(sys.argv) > 4 else 6

env = dict(os.environ, SDL_VIDEODRIVER="dummy", SDL_RENDER_DRIVER="software", SDL_AUDIODRIVER="dummy")
listing = subprocess.run([str(run_dir / "d2tm"), "--ui-audit-list"], cwd=run_dir, env=env,
                         capture_output=True, text=True, timeout=60, check=True)
scenes = [scene["id"] for scene in json.loads(listing.stdout)["scenes"]]


def run(scene_id):
    target = out_dir / language / scene_id
    target.mkdir(parents=True, exist_ok=True)
    scene_env = dict(env, XDG_DATA_HOME=str(target / "xdg"))
    result = subprocess.run([str(run_dir / "d2tm"), "-windowed", "-screenWidth", "1024", "-screenHeight", "768",
                             "--ui-audit-scene", scene_id, "--ui-audit-out", str(target),
                             "--ui-audit-language", language],
                            cwd=run_dir, env=scene_env, capture_output=True, text=True, timeout=600)
    texts = []
    for log in target.glob("*.geometry.jsonl"):
        for line in log.read_text(encoding="utf-8").splitlines():
            record = json.loads(line)
            if record.get("k") == "text":
                texts.append(record["s"])
    for png in target.glob("*.png"):
        png.unlink()
    return scene_id, result.returncode, texts


with ThreadPoolExecutor(workers) as pool:
    results = list(pool.map(run, scenes))

with open(out_dir / f"texts-{language}.tsv", "w", encoding="utf-8") as table:
    table.write("scene\tcode\ttext\n")
    for scene_id, code, texts in results:
        if not texts:
            table.write(f"{scene_id}\t{code}\t\n")
        for text in dict.fromkeys(texts):
            table.write(f"{scene_id}\t{code}\t{text}\n")
print(f"scenes={len(scenes)} failed={sum(1 for _, code, _ in results if code != 0)}")
