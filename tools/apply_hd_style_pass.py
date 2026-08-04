#!/usr/bin/env python3
"""Apply the conservative, audit-backed D2TM HD style corrections.

This is intentionally not a blanket filter.  Approved world art, portraits,
facial masks and scene animations remain byte-identical.  Only the interface
entries identified by the style audit receive small locked-group corrections.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import math
import shutil
import sys
from dataclasses import replace
from pathlib import Path

from PIL import Image, ImageEnhance

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hd_assets import encode_png, read_pack, write_pack  # noqa: E402


ROOT = Path(__file__).resolve().parents[1]
INTEGRATED = ROOT / "artifacts" / "hd_completion" / "integrated" / "data"
OUTPUT = ROOT / "artifacts" / "hd_completion" / "styled" / "data"

# IDs come from artifacts/hd_completion/style_audit_interface.json.
EXPOSURE_GROUPS = {
    8: 1.05,       # BMP_GERALD_SIDEBAR_PIECE
    116: 1.04,     # READY01
    117: 1.04,     # READY02
    **{entry_id: 1.02 for entry_id in range(82, 116)},  # PROGRESS*
}
SABOTEUR_ID = 31


def sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def linear_exposure(image: Image.Image, factor: float) -> Image.Image:
    rgba = image.convert("RGBA")
    rgb = rgba.convert("RGB")
    alpha = rgba.getchannel("A")
    table = []
    for value in range(256):
        linear = (value / 255.0) ** 2.2
        corrected = min(1.0, linear * factor) ** (1.0 / 2.2)
        table.append(round(corrected * 255.0))
    red, green, blue = rgb.split()
    return Image.merge(
        "RGBA",
        (red.point(table), green.point(table), blue.point(table), alpha),
    )


def correct_saboteur(image: Image.Image) -> Image.Image:
    lifted = linear_exposure(image, 1.08)
    alpha = lifted.getchannel("A")
    contrasted = ImageEnhance.Contrast(lifted.convert("RGB")).enhance(1.10)
    red, green, blue = contrasted.split()
    return Image.merge("RGBA", (red, green, blue, alpha))


def metrics(image: Image.Image) -> dict[str, float]:
    rgba = image.convert("RGBA")
    alpha = rgba.getchannel("A")
    luminance = rgba.convert("RGB").convert("L")
    values = [
        value
        for value, opacity in zip(luminance.tobytes(), alpha.tobytes(), strict=True)
        if opacity > 8
    ]
    if not values:
        return {"luminance": 0.0, "contrast": 0.0}
    mean = sum(values) / len(values)
    variance = sum((value - mean) ** 2 for value in values) / len(values)
    return {"luminance": round(mean, 3), "contrast": round(math.sqrt(variance), 3)}


def patch_interface() -> dict[str, object]:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    reports: list[dict[str, object]] = []
    target_ids = set(EXPOSURE_GROUPS) | {SABOTEUR_ID}

    hd4_path = INTEGRATED / "sdl_inter_hd4.dat"
    hd4_entries = read_pack(hd4_path)
    patched_hd4 = []
    corrected_hd4: dict[int, Image.Image] = {}
    for entry in hd4_entries:
        if entry.index not in target_ids:
            patched_hd4.append(entry)
            continue
        with Image.open(io.BytesIO(entry.payload)) as source:
            before = source.convert("RGBA")
        after = (
            correct_saboteur(before)
            if entry.index == SABOTEUR_ID
            else linear_exposure(before, EXPOSURE_GROUPS[entry.index])
        )
        if before.getchannel("A").tobytes() != after.getchannel("A").tobytes():
            raise AssertionError(f"Alpha changed for sdl_inter[{entry.index}]")
        payload = encode_png(after)
        patched_hd4.append(replace(entry, extension="png", payload=payload))
        corrected_hd4[entry.index] = after
        reports.append(
            {
                "id": entry.index,
                "name": entry.name,
                "before": metrics(before),
                "after": metrics(after),
                "old_sha256": sha256(entry.payload),
                "new_sha256": sha256(payload),
            }
        )

    output4 = OUTPUT / "sdl_inter_hd4.dat"
    write_pack(output4, patched_hd4)

    hd2_path = INTEGRATED / "sdl_inter_hd2.dat"
    hd2_entries = read_pack(hd2_path)
    patched_hd2 = []
    for entry in hd2_entries:
        master = corrected_hd4.get(entry.index)
        if master is None:
            patched_hd2.append(entry)
            continue
        target_size = (master.width // 2, master.height // 2)
        downsampled = master.convert("RGBa").resize(
            target_size,
            Image.Resampling.LANCZOS,
        ).convert("RGBA")
        patched_hd2.append(
            replace(entry, extension="png", payload=encode_png(downsampled))
        )
    output2 = OUTPUT / "sdl_inter_hd2.dat"
    write_pack(output2, patched_hd2)

    for source_path, output_path in ((hd4_path, output4), (hd2_path, output2)):
        source_entries = read_pack(source_path)
        output_entries = read_pack(output_path)
        for before, after in zip(source_entries, output_entries, strict=True):
            if before.index not in target_ids and before.payload != after.payload:
                raise AssertionError(
                    f"Unrelated style payload changed: {source_path.name}[{before.index}]"
                )
            if before.name != after.name:
                raise AssertionError(
                    f"Entry name changed: {source_path.name}[{before.index}]"
                )

    return {
        "pack": "sdl_inter",
        "changed_count": len(target_ids),
        "changed": sorted(reports, key=lambda item: int(item["id"])),
    }


def copy_untouched_packs() -> list[str]:
    copied: list[str] = []
    for source in sorted(INTEGRATED.glob("*.dat")):
        if source.name.startswith("sdl_inter_hd"):
            continue
        destination = OUTPUT / source.name
        shutil.copy2(source, destination)
        if source.read_bytes() != destination.read_bytes():
            raise AssertionError(f"Untouched pack differs after copy: {source.name}")
        copied.append(source.name)
    return copied


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.parse_args()
    interface_report = patch_interface()
    untouched = copy_untouched_packs()
    report = {
        "format": 1,
        "policy": "audit-backed selective normalization; no global filter",
        "interface": interface_report,
        "untouched_packs": untouched,
        "world": "unchanged: audit confirmed coherent upper-left lighting",
        "mentat": "unchanged: approved portraits and facial masks",
        "scenes": "unchanged: approved animation sequences and stable grading",
    }
    report_path = OUTPUT.parent / "style_pass_report.json"
    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Style pass corrected {interface_report['changed_count']} interface entries")
    print(f"Output: {OUTPUT}")
    print(f"Report: {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
