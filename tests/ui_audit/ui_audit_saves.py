import argparse
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import ui_audit_runtime_support as support  # noqa: E402

SCENES = (
    "main-menu",
    "main-menu-saves",
    "options-game-main-nosaves",
    "options-game-main-saves",
    "save-dialog-menu",
    "save-dialog-load",
    "save-dialog-save-new",
    "save-dialog-overwrite",
    "save-dialog-load-error",
    "save-dialog-save-error",
    "save-roundtrip",
)
DIALOG = {*(f"save-slot:{slot}" for slot in range(1, 11)), "save-name"}


def read_scene(game, scene_id):
    try:
        result = game.run(["--ui-audit-scene", scene_id, "--ui-audit-out", str(game.out)])
    except subprocess.TimeoutExpired:
        return None, None, f"{scene_id}: no exit within {support.TIMEOUT_SECONDS} seconds"
    if result.returncode != 0:
        return None, None, f"{scene_id}: exited with {result.returncode}\n{result.stdout}\n{result.stderr}"

    png = game.out / f"{scene_id}.png"
    log = game.out / f"{scene_id}.geometry.jsonl"
    if not png.is_file() or not log.is_file():
        return None, None, f"{scene_id}: missing PNG or geometry log"
    try:
        records = [json.loads(line) for line in log.read_text(encoding="utf-8").splitlines() if line]
    except (OSError, ValueError) as error:
        return None, None, f"{scene_id}: invalid geometry log: {error}"
    if not records or any(not isinstance(record, dict) for record in records):
        return None, None, f"{scene_id}: geometry log has no JSON object records"

    clicks = {record["name"] for record in records if record.get("k") == "click" and "name" in record}
    texts = [record["s"] for record in records if record.get("k") == "text" and "s" in record]
    return clicks, texts, None


def check_scene(scene_id, clicks, texts):
    errors = []

    def require_click(name):
        if name not in clicks:
            errors.append(f"{scene_id}: missing click {name!r}")

    def forbid_click(name):
        if name in clicks:
            errors.append(f"{scene_id}: unexpected click {name!r}")

    def require_text(name):
        if name not in texts:
            errors.append(f"{scene_id}: missing text {name!r}")

    def require_text_prefix(prefix):
        if not any(text.startswith(prefix) for text in texts):
            errors.append(f"{scene_id}: no text starts with {prefix!r}")

    if scene_id == "main-menu":
        require_text("Saved games")
        forbid_click("GuiButton:Saved games")
    elif scene_id == "main-menu-saves":
        require_click("GuiButton:Saved games")
    elif scene_id == "options-game-main-nosaves":
        require_click("GuiButton:Save game")
        forbid_click("GuiButton:Load game")
    elif scene_id == "options-game-main-saves":
        require_click("GuiButton:Save game")
        require_click("GuiButton:Load game")
    elif scene_id == "save-dialog-menu":
        if not DIALOG <= clicks:
            errors.append(f"{scene_id}: missing dialog click records {sorted(DIALOG - clicks)}")
        require_click("GuiButton:Load")
        require_click("GuiButton:Close")
        forbid_click("GuiButton:Save")
        for text in ("SAVED GAMES", "01. Save 1", "03. <corrupted>", "04. <empty>"):
            require_text(text)
    elif scene_id == "save-dialog-load":
        if not DIALOG <= clicks:
            errors.append(f"{scene_id}: missing dialog click records {sorted(DIALOG - clicks)}")
        for name in ("GuiButton:Save", "GuiButton:Load", "GuiButton:Close"):
            require_click(name)
        require_text("01. Save 1")
    elif scene_id == "save-dialog-save-new":
        if not DIALOG <= clicks:
            errors.append(f"{scene_id}: missing dialog click records {sorted(DIALOG - clicks)}")
        require_click("GuiButton:Save")
        require_click("GuiButton:Close")
        forbid_click("GuiButton:Load")
        require_text("Save 4 |")
    elif scene_id == "save-dialog-overwrite":
        for name in ("GuiButton:Save", "GuiButton:Load", "GuiButton:Close"):
            require_click(name)
        require_text_prefix("A very long save name")
    elif scene_id == "save-dialog-load-error":
        require_click("GuiButton:Save")
        require_click("GuiButton:Close")
        forbid_click("GuiButton:Load")
        require_text("The selected slot has no valid save.")
    elif scene_id == "save-dialog-save-error":
        require_click("GuiButton:Save")
        require_click("GuiButton:Close")
        forbid_click("GuiButton:Load")
        require_text_prefix("Could not replace save file")

    return errors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    args = parser.parse_args()
    errors = []
    with support.GameRun(args.run_dir) as game:
        for scene_id in SCENES:
            clicks, texts, error = read_scene(game, scene_id)
            if error:
                errors.append(error)
                continue
            if scene_id == "save-roundtrip":
                first = game.out / "saves" / "roundtrip-first.d2s"
                second = game.out / "saves" / "quicksave.d2s"
                if not first.is_file() or not second.is_file():
                    errors.append("save-roundtrip: missing saved game files")
                    continue
                first_bytes = first.read_bytes()
                second_bytes = second.read_bytes()
                if not first_bytes.startswith(b"D2TM_SAVE 3 "):
                    errors.append("save-roundtrip: first save does not start with D2TM_SAVE 3")
                if b"\nFACTORYPADS 2\n" not in first_bytes:
                    errors.append("save-roundtrip: first save has no FACTORYPADS section with two pads")
                if first_bytes.count(b"\nFACTORYPAD ") != 2:
                    errors.append("save-roundtrip: first save does not hold two FACTORYPAD records")
                if first_bytes != second_bytes:
                    errors.append("save-roundtrip: quick save bytes differ after loading and saving")
            else:
                errors.extend(check_scene(scene_id, clicks, texts))

        preferences = game.preferences_files()
        if preferences:
            errors.append(f"An audit run must not write preferences: {preferences}")

    for error in errors:
        print(error, file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
