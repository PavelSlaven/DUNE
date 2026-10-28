from __future__ import annotations

import hashlib
import io
import json
import math
import subprocess
import sys
import tempfile
import unittest
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import numpy as np
from PIL import Image

from tools import hd_assets
from tools.hd_assets import PackEntry, read_pack, write_pack


CHECK_NAMES = (
    "composition",
    "pack",
    "direction",
    "pivot",
    "margin",
    "size",
    "alpha",
    "mask",
    "shadow",
    "provenance",
)
CHECKER_PATH = Path(__file__).resolve().parents[1] / "check_unit.py"
REPO_ROOT = Path(__file__).resolve().parents[3]
FRAME_SIZE = (128, 128)
ATLAS_SIZE = (1024, 129)
YAW_DEGREES = (0, 45, 90, 135, 180, 225, 270, 315)
ROLE_SPECS = {
    "UNIT_SYNTH_BODY": ("body", "body", "HM_SYNTH_BODY", "body", "color"),
    "UNIT_SYNTH_SHADOW": ("shadow", "body", None, "shadow", "shadow"),
    "HM_SYNTH_BODY": ("mask_body", "body", None, "mask", "mask"),
    "UNIT_SYNTH_TOP": ("top", "top", "HM_SYNTH_TOP", "top", "color"),
    "HM_SYNTH_TOP": ("mask_top", "top", None, "mask", "mask"),
}


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def _write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(_json_bytes(value))


def _encode_png(array: np.ndarray, mode: str = "RGBA") -> bytes:
    output = io.BytesIO()
    Image.fromarray(np.asarray(array, dtype=np.uint8), mode=mode).save(output, format="PNG")
    return output.getvalue()


def _save_png(path: Path, array: np.ndarray, mode: str = "RGBA") -> bytes:
    payload = _encode_png(array, mode)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(payload)
    return payload


def _base_contract_entry(name: str, role: str, house_mask: str | None) -> dict[str, object]:
    return {
        "name": name,
        "role": role,
        "unit_types": ["SYNTH"],
        "frame_hd4": list(FRAME_SIZE),
        "hd4_size": list(ATLAS_SIZE),
        "columns": 8,
        "column_meaning": [
            {"column": k, "direction": direction, "yaw_deg": yaw}
            for k, (direction, yaw) in enumerate(
                zip(("E", "NE", "N", "NW", "W", "SW", "S", "SE"), YAW_DEGREES)
            )
        ],
        "house_mask": house_mask,
    }


def _marker_channel(frame: np.ndarray, channel: int, x: float, y: float) -> None:
    px = x - 0.5
    py = y - 0.5
    x0 = math.floor(px)
    y0 = math.floor(py)
    fx = px - x0
    fy = py - y0
    weights = np.rint(255 * np.outer((1 - fy, fy), (1 - fx, fx))).astype(np.uint8)
    height, width = frame.shape[:2]
    for iy in range(2):
        for ix in range(2):
            if weights[iy, ix] and 0 <= x0 + ix < width and 0 <= y0 + iy < height:
                frame[y0 + iy, x0 + ix, channel] = weights[iy, ix]


def _full_frame(part: str, pass_name: str, k: int, with_top: bool) -> np.ndarray:
    frame = np.zeros((FRAME_SIZE[1], FRAME_SIZE[0], 4), dtype=np.uint8)
    if pass_name == "color":
        if part == "body":
            frame[59:69, 14:114] = (72, 57, 41, 255)
        elif with_top:
            frame[61:66, 54:74] = (91, 75, 54, 255)
    elif pass_name == "mask":
        if part == "body":
            frame[59:69, 14:34] = (255, 255, 255, 255)
        elif with_top:
            frame[61:66, 54:58] = (255, 255, 255, 255)
    elif pass_name == "markers":
        _marker_channel(frame, 1, 64, 64)
        if with_top:
            _marker_channel(frame, 2, 64, 64)
        theta = math.radians(63)
        yaw = math.radians(YAW_DEGREES[k])
        screen_angle = math.atan2(math.sin(yaw) * math.sin(theta), math.cos(yaw))
        screen_x = math.cos(screen_angle)
        screen_y = math.sin(screen_angle)
        screen_x = 0 if abs(screen_x) < 1e-12 else screen_x
        screen_y = 0 if abs(screen_y) < 1e-12 else screen_y
        red_x = 64 + 30 * screen_x
        red_y = 64 - 30 * screen_y
        _marker_channel(frame, 0, red_x, red_y)
        frame[:, :, 3] = np.maximum.reduce((frame[:, :, 0], frame[:, :, 1], frame[:, :, 2]))
    elif pass_name == "shadow" and part == "body":
        frame[59:69, 115:123] = (0, 0, 0, 255)
    return frame


def _resize_render_frame(frame: np.ndarray) -> np.ndarray:
    image = Image.fromarray(np.asarray(frame, dtype=np.uint8), "RGBA")
    resized = image.convert("RGBa").resize(FRAME_SIZE, Image.Resampling.LANCZOS).convert("RGBA")
    return np.asarray(resized, dtype=np.uint8).copy()


def _canonical_atlas_frame(
    entry_name: str,
    render_frames: dict[tuple[str, str], np.ndarray],
    k: int,
) -> np.ndarray:
    role, part, _, _, pass_name = ROLE_SPECS[entry_name]
    resized_frames = [_resize_render_frame(render_frames[(part, pass_name)][i]) for i in range(8)]
    for image in resized_frames:
        image[image[:, :, 3] < 8] = 0
    frame = resized_frames[k].copy()
    if pass_name == "shadow":
        frame[:, :, :3] = 0
        peak = max(int(image[:, :, 3].max()) for image in resized_frames)
        if peak:
            alpha = frame[:, :, 3].astype(np.float32) * 51 / peak
            frame[:, :, 3] = np.round(alpha).astype(np.uint8)
        return frame
    elif pass_name == "mask":
        color = _resize_render_frame(render_frames[(part, "color")][k])
        frame[color[:, :, 3] <= 16] = 0
    return frame


@dataclass(frozen=True)
class RunResult:
    stdout: str
    stderr: str
    lines: tuple[str, ...]
    statuses: dict[int, str]
    exit_code: int


class Fixture:
    def __init__(
        self,
        with_top: bool = False,
        packs: bool = True,
        case: str = "honest body-only fixture",
        supersample: int = 1,
    ) -> None:
        self._temporary = tempfile.TemporaryDirectory(prefix="units3d-check-")
        self.root = Path(self._temporary.name)
        self.case = case
        self.with_top = with_top
        self.packs = packs
        self.supersample = supersample
        self.unit_dir = self.root / "units3d" / "synth"
        self.common_dir = self.root / "units3d" / "common"
        self.render_dir = self.root / "render"
        self.atlases_dir = self.root / "atlases"
        self.contract_path = self.root / "unit_contract.json"
        self.pack_before = self.root / "pack-before.dat"
        self.pack_after = self.root / "pack-after.dat"
        self.model_path = self.unit_dir / "source" / "synth.glb"
        self.unit_path = self.unit_dir / "unit.json"
        self.camera_path = self.common_dir / "camera.json"
        self.light_path = self.common_dir / "light.json"
        self.render_json_path = self.common_dir / "render.json"
        self.render_manifest_path = self.render_dir / "render_manifest.json"
        self.atlases_json_path = self.atlases_dir / "atlases.json"
        self.entries = self._entry_names(with_top)
        self.entry_files = {name: f"{name}.png" for name in self.entries}
        self.atlas_files_to_omit: set[str] = set()
        self.atlas_padding: dict[str, list[tuple[int, int, tuple[int, int, int, int]]]] = {}
        self.render_frames: dict[tuple[str, str], np.ndarray] = {}
        parts = ["body", "top"] if with_top else ["body"]
        for part in parts:
            for pass_name in (("color", "mask", "markers", "shadow") if part == "body" else ("color", "mask", "markers")):
                frames = np.stack(
                    [_full_frame(part, pass_name, k, with_top) for k in range(8)], axis=0
                )
                if supersample > 1:
                    frames = np.repeat(np.repeat(frames, supersample, axis=1), supersample, axis=2)
                self.render_frames[(part, pass_name)] = frames
        self.atlas_frames = {
            name: np.stack(
                [_canonical_atlas_frame(name, self.render_frames, k) for k in range(8)],
                axis=0,
            )
            for name in self.entries
        }
        self.unit_data = self._unit_data(with_top)
        if supersample > 1:
            self.unit_data["mask_share"] = [0.15, 0.25]
        self.contract_data = {
            "entries": [
                _base_contract_entry(name, *self._contract_spec(name))
                for name in self.entries
            ],
            "light": {"median_angle_degrees": 0.0},
        }
        self.camera_data = {
            "elevation_deg": 63,
            "hd4_px_per_m": 1,
            "supersample": supersample,
        }
        self.light_data: dict[str, object] = {
            "sun_azimuth_deg": 0,
            "sun_elevation_deg": 45,
            "sun_strength": 4.0,
            "sun_color": [1.0, 1.0, 1.0],
            "sun_angle_deg": 3.0,
            "ambient_color": [1.0, 1.0, 1.0],
            "ambient_strength": 0.2,
        }
        self.render_json_data: dict[str, object] = {
            "blender": "synthetic",
            "engine": "CYCLES",
            "device": "CPU",
            "samples": 1,
            "mask_samples": 1,
            "seed": 1,
            "denoise": False,
        }
        self.manifest_data = self._manifest_data(with_top, supersample)
        self.atlases_data = self._atlases_data()
        self._write_sources()
        self.commit()

    @staticmethod
    def _entry_names(with_top: bool) -> tuple[str, ...]:
        names = ("UNIT_SYNTH_BODY", "UNIT_SYNTH_SHADOW", "HM_SYNTH_BODY")
        if with_top:
            names += ("UNIT_SYNTH_TOP", "HM_SYNTH_TOP")
        return names

    @staticmethod
    def _contract_spec(name: str) -> tuple[str, str | None]:
        role, _, house_mask, _, _ = ROLE_SPECS[name]
        return role, house_mask

    def _unit_data(self, with_top: bool) -> dict[str, object]:
        parts: dict[str, object] = {
            "body": {
                "atlas": "UNIT_SYNTH_BODY",
                "shadow": "UNIT_SYNTH_SHADOW",
                "mask": "HM_SYNTH_BODY",
            }
        }
        if with_top:
            parts["top"] = {"atlas": "UNIT_SYNTH_TOP", "mask": "HM_SYNTH_TOP"}
        return {
            "parts": parts,
            "model": "source/synth.glb",
            "frame_hd4": list(FRAME_SIZE),
            "atlas_hd4": list(ATLAS_SIZE),
            "length_m": 100,
            "mask_share": [0.2, 0.2],
            "max_holes": 0,
        }

    def _manifest_data(self, with_top: bool, supersample: int) -> dict[str, object]:
        bbox: dict[str, dict[str, list[int]]] = {}
        for part in (["body", "top"] if with_top else ["body"]):
            bounds = [14, 59, 114, 69] if part == "body" else [54, 61, 74, 66]
            bbox[part] = {str(k): list(bounds) for k in range(8)}
        return {
            "blender": "synthetic",
            "elevation_deg": 63,
            "hd4_px_per_m": 1,
            "supersample": supersample,
            "frame_hd4": list(FRAME_SIZE),
            "model_scale": 1,
            "pivot_height_m": 0,
            "cap_height_m": 0,
            "hull_screen_length_px": 100,
            "parts": ["body", "top"] if with_top else ["body"],
            "directions": list(range(8)),
            "bbox_hd4": bbox,
            "hashes": {},
        }

    def _atlases_data(self) -> dict[str, object]:
        return {
            "entries": {
                name: {
                    "file": self.entry_files[name],
                    "size": list(ATLAS_SIZE),
                    "sha256": "",
                }
                for name in self.entries
            },
            "hashes": {},
        }

    def __enter__(self) -> Fixture:
        case = self.case
        self.case = f"honest set before {case}"
        try:
            if self.packs:
                assert_run(self)
            else:
                assert_run(self, extra_args=("--allow-skip", "2"), expected_skip_set={2}, use_fixture_packs=False)
        except BaseException:
            self.close()
            raise
        finally:
            self.case = case
        return self

    def __exit__(self, exc_type: object, exc: object, traceback: object) -> None:
        self.close()

    def close(self) -> None:
        self._temporary.cleanup()

    def set_frame(
        self,
        entry_name: str,
        k: int,
        rgba: np.ndarray,
        *,
        sync_render: bool = False,
        commit: bool = False,
    ) -> None:
        self.atlas_frames[entry_name][k] = np.asarray(rgba, dtype=np.uint8)
        if sync_render:
            _, part, _, _, pass_name = ROLE_SPECS[entry_name]
            self.render_frames[(part, pass_name)][k] = np.asarray(rgba, dtype=np.uint8)
        if commit:
            self.commit()

    def set_render_frame(
        self,
        part: str,
        pass_name: str,
        k: int,
        rgba: np.ndarray,
        *,
        sync_atlas: bool = False,
        commit: bool = False,
    ) -> None:
        self.render_frames[(part, pass_name)][k] = np.asarray(rgba, dtype=np.uint8)
        if sync_atlas:
            for name in self.entries:
                _, entry_part, _, _, entry_pass = ROLE_SPECS[name]
                if (entry_part, entry_pass) == (part, pass_name):
                    self.atlas_frames[name] = np.stack(
                        [_canonical_atlas_frame(name, self.render_frames, i) for i in range(8)],
                        axis=0,
                    )
        if commit:
            self.commit()

    def add_contract_entry(self, entry: dict[str, object], filename: str, frames: np.ndarray) -> None:
        self.contract_data["entries"].append(entry)
        self.atlases_data["entries"][entry["name"]] = {
            "file": filename,
            "size": list(ATLAS_SIZE),
            "sha256": "",
        }
        self.entry_files[entry["name"]] = filename
        self.atlas_frames[entry["name"]] = np.asarray(frames, dtype=np.uint8)

    def _write_sources(self) -> None:
        self.unit_dir.mkdir(parents=True, exist_ok=True)
        self.common_dir.mkdir(parents=True, exist_ok=True)
        self.render_dir.mkdir(parents=True, exist_ok=True)
        self.atlases_dir.mkdir(parents=True, exist_ok=True)
        self.model_path.parent.mkdir(parents=True, exist_ok=True)
        self.model_path.write_bytes(b"synthetic glTF model bytes")
        _write_json(self.unit_path, self.unit_data)
        _write_json(self.camera_path, self.camera_data)
        _write_json(self.light_path, self.light_data)
        _write_json(self.render_json_path, self.render_json_data)
        _write_json(self.contract_path, self.contract_data)

    def _atlas_png(self, entry_name: str) -> np.ndarray:
        frames = self.atlas_frames[entry_name]
        height = max(self.unit_data["atlas_hd4"][1], frames.shape[1])
        width = max(self.unit_data["atlas_hd4"][0], frames.shape[2] * 8)
        atlas = np.zeros((height, width, 4), dtype=np.uint8)
        for k, frame in enumerate(frames):
            y_end = min(height, frame.shape[0])
            x_start = k * frame.shape[1]
            x_end = min(width, x_start + frame.shape[1])
            if x_start < width and y_end > 0:
                atlas[:y_end, x_start:x_end] = frame[:y_end, : x_end - x_start]
        for x, y, rgba in self.atlas_padding.get(entry_name, ()):
            atlas[y, x] = rgba
        return atlas

    def _write_render_files(self) -> None:
        for (part, pass_name), frames in self.render_frames.items():
            folder = self.render_dir / part
            for k in range(8):
                _save_png(folder / f"{pass_name}_{k}.png", frames[k])

    def _write_atlas_files(self) -> dict[str, bytes]:
        payloads: dict[str, bytes] = {}
        for name in self.atlas_frames:
            filename = self.entry_files[name]
            payload = _encode_png(self._atlas_png(name))
            if filename not in self.atlas_files_to_omit:
                (self.atlases_dir / filename).write_bytes(payload)
            else:
                (self.atlases_dir / filename).unlink(missing_ok=True)
            payloads[name] = payload
        return payloads

    def _source_hashes(self) -> dict[str, str]:
        return {
            "camera.json": _sha(self.camera_path.read_bytes()),
            "light.json": _sha(self.light_path.read_bytes()),
            "render.json": _sha(self.render_json_path.read_bytes()),
            "unit.json": _sha(self.unit_path.read_bytes()),
            "model": _sha(self.model_path.read_bytes()),
        }

    def _write_packs(self, atlas_payloads: dict[str, bytes]) -> None:
        if not self.packs:
            return
        before_entries = [
            PackEntry(i, name, "png", f"old:{name}".encode())
            for i, name in enumerate(self.entries)
        ]
        before_entries.append(PackEntry(len(before_entries), "KEEP_SYNTH", "dat", b"preserve me"))
        after_entries = [
            PackEntry(i, name, "png", atlas_payloads[name])
            for i, name in enumerate(self.entries)
        ]
        after_entries.append(PackEntry(len(after_entries), "KEEP_SYNTH", "dat", b"preserve me"))
        write_pack(self.pack_before, before_entries)
        write_pack(self.pack_after, after_entries)

    def commit(
        self,
        *,
        sync_render: bool = False,
        sync_atlas: bool = False,
        update_hashes: bool = True,
        update_packs: bool = True,
    ) -> None:
        if sync_render:
            for name in self.entries:
                _, part, _, _, pass_name = ROLE_SPECS[name]
                self.render_frames[(part, pass_name)] = self.atlas_frames[name].copy()
        if sync_atlas:
            for name in self.entries:
                _, part, _, _, pass_name = ROLE_SPECS[name]
                self.atlas_frames[name] = np.stack(
                    [_canonical_atlas_frame(name, self.render_frames, k) for k in range(8)], axis=0
                )
        self._write_sources()
        self._write_render_files()
        if update_hashes:
            self.manifest_data["hashes"] = self._source_hashes()
        _write_json(self.render_manifest_path, self.manifest_data)
        atlas_payloads = self._write_atlas_files()
        for name, payload in atlas_payloads.items():
            if name in self.atlases_data["entries"] and update_hashes:
                self.atlases_data["entries"][name]["sha256"] = _sha(payload)
        if update_hashes:
            self.atlases_data["hashes"] = {
                **{key: self._source_hashes()[key] for key in ("camera.json", "light.json", "render.json", "unit.json")},
                "render_manifest.json": _sha(self.render_manifest_path.read_bytes()),
            }
        _write_json(self.atlases_json_path, self.atlases_data)
        if update_packs:
            self._write_packs(atlas_payloads)


def run_checker(
    fixture: Fixture,
    extra_args: Iterable[str] = (),
    *,
    use_fixture_packs: bool = True,
) -> RunResult:
    extras = tuple(str(value) for value in extra_args)
    command = [
        sys.executable,
        str(CHECKER_PATH),
        "--unit",
        str(fixture.unit_dir),
        "--render",
        str(fixture.render_dir),
        "--atlases",
        str(fixture.atlases_dir),
        "--contract",
        str(fixture.contract_path),
    ]
    supplied_pack_flag = "--pack-before" in extras or "--pack-after" in extras
    if fixture.packs and use_fixture_packs and not supplied_pack_flag:
        command.extend(("--pack-before", str(fixture.pack_before), "--pack-after", str(fixture.pack_after)))
    command.extend(extras)
    completed = subprocess.run(command, cwd=REPO_ROOT, capture_output=True, text=True, check=False)
    lines = tuple(line for line in completed.stdout.splitlines() if line.strip())
    statuses: dict[int, str] = {}
    for line in lines:
        columns = line.split("\t")
        if len(columns) >= 3:
            try:
                statuses[int(columns[0])] = columns[2]
            except ValueError:
                continue
    return RunResult(completed.stdout, completed.stderr, lines, statuses, completed.returncode)


def assert_run(
    fixture: Fixture,
    expected_fail_set: Iterable[int] = (),
    extra_args: Iterable[str] = (),
    *,
    expected_skip_set: Iterable[int] = (),
    expected_exit_code: int | None = None,
    use_fixture_packs: bool = True,
) -> RunResult:
    expected_fail = set(expected_fail_set)
    expected_skip = set(expected_skip_set)
    extras = tuple(str(value) for value in extra_args)
    result = run_checker(fixture, extras, use_fixture_packs=use_fixture_packs)
    actual_fail = {number for number, status in result.statuses.items() if status == "FAIL"}
    actual_skip = {number for number, status in result.statuses.items() if status == "SKIP"}
    expected_statuses = {
        number: "FAIL" if number in expected_fail else "SKIP" if number in expected_skip else "PASS"
        for number in range(1, 11)
    }
    output = (
        f"{fixture.case}: expected FAIL={sorted(expected_fail)}, SKIP={sorted(expected_skip)}; "
        f"actual FAIL={sorted(actual_fail)}, SKIP={sorted(actual_skip)}, exit={result.exit_code}\n"
        + result.stdout
        + result.stderr
    )
    print(output, end="" if output.endswith("\n") else "\n")
    if "Traceback (most recent call last)" in result.stderr:
        raise AssertionError(f"{output}Checker raised an unhandled exception.")
    if len(result.lines) != 10:
        raise AssertionError(f"{output}Expected ten checker rows, got {len(result.lines)}.")
    row_numbers: list[int] = []
    row_names: list[str] = []
    for line in result.lines:
        columns = line.split("\t")
        if len(columns) != 4 or not columns[3].strip():
            raise AssertionError(f"{output}Malformed checker row: {line!r}.")
        try:
            row_numbers.append(int(columns[0]))
            row_names.append(columns[1])
        except ValueError as error:
            raise AssertionError(f"{output}Malformed checker row: {line!r}.") from error
    if row_numbers != list(range(1, 11)) or row_names != list(CHECK_NAMES):
        raise AssertionError(f"{output}Checker row names or order do not match the specification.")
    if result.statuses != expected_statuses:
        raise AssertionError(f"{output}Status set did not match the exact expected result.")
    allowed_skip = expected_skip == {2} and "--allow-skip" in extras and "2" in extras
    if expected_exit_code is not None:
        if result.exit_code != expected_exit_code:
            raise AssertionError(f"{output}Expected exit code {expected_exit_code}.")
    elif (not expected_fail and (not expected_skip or allowed_skip)) != (result.exit_code == 0):
        raise AssertionError(f"{output}Exit code does not match the statuses.")
    return result


def assert_read_error(
    fixture: Fixture,
    required_fail_set: Iterable[int],
    *,
    extra_args: Iterable[str] = (),
) -> RunResult:
    required_fail = set(required_fail_set)
    result = run_checker(fixture, extra_args)
    actual_fail = {number for number, status in result.statuses.items() if status == "FAIL"}
    output = (
        f"{fixture.case}: damaged input requires FAIL={sorted(required_fail)}; "
        f"actual FAIL={sorted(actual_fail)}, exit={result.exit_code}\n"
        + result.stdout
        + result.stderr
    )
    print(output, end="" if output.endswith("\n") else "\n")
    if "Traceback (most recent call last)" in result.stderr:
        raise AssertionError(f"{output}Checker raised an unhandled exception.")
    if len(result.lines) != 10:
        raise AssertionError(f"{output}Expected all ten checker rows for a read error.")
    row_numbers: list[int] = []
    row_names: list[str] = []
    for line in result.lines:
        columns = line.split("\t")
        if len(columns) != 4 or not columns[3].strip():
            raise AssertionError(f"{output}Malformed checker row: {line!r}.")
        try:
            row_numbers.append(int(columns[0]))
            row_names.append(columns[1])
        except ValueError as error:
            raise AssertionError(f"{output}Malformed checker row: {line!r}.") from error
    if row_numbers != list(range(1, 11)) or row_names != list(CHECK_NAMES):
        raise AssertionError(f"{output}Checker rows do not match the required protocol.")
    if set(result.statuses) != set(range(1, 11)):
        raise AssertionError(f"{output}Every check must have a status.")
    if any(status not in {"PASS", "FAIL", "SKIP"} for status in result.statuses.values()):
        raise AssertionError(f"{output}Unexpected status value.")
    if any(result.statuses[number] != "FAIL" for number in required_fail):
        raise AssertionError(f"{output}A check reading the damaged input did not FAIL.")
    if result.exit_code == 0:
        raise AssertionError(f"{output}A read error must produce a nonzero exit code.")
    return result


def _pack_entries(path: Path) -> list[PackEntry]:
    return hd_assets.read_pack(path)


def _write_pack_entries(path: Path, entries: Iterable[PackEntry]) -> None:
    hd_assets.write_pack(
        path,
        [hd_assets.PackEntry(i, entry.name, entry.extension, entry.payload) for i, entry in enumerate(entries)],
    )


def _new_entry(name: str, extension: str, payload: bytes) -> PackEntry:
    return hd_assets.PackEntry(0, name, extension, payload)


def _r_names(fixture: Fixture) -> list[str]:
    names: list[str] = []
    for part in fixture.unit_data["parts"].values():
        names.extend(part[key] for key in ("atlas", "shadow", "mask") if key in part)
    return names


def _atlas_names(fixture: Fixture) -> list[str]:
    return [part["atlas"] for part in fixture.unit_data["parts"].values() if "atlas" in part]


def _assigned_pngs(fixture: Fixture) -> dict[str, bytes]:
    return {
        name: (fixture.atlases_dir / item["file"]).read_bytes()
        for name, item in fixture.atlases_data["entries"].items()
    }


def _pack_offsets(path: Path) -> dict[str, int]:
    blob = path.read_bytes()
    _, count = hd_assets.HEADER.unpack_from(blob)
    offsets: dict[str, int] = {}
    for i in range(count):
        raw_name, _, offset, _ = hd_assets.ENTRY.unpack_from(
            blob,
            hd_assets.HEADER.size + i * hd_assets.ENTRY.size,
        )
        offsets[raw_name.split(b"\0", 1)[0].decode("utf-8")] = offset
    return offsets


class SupersampledProvenanceFixtureTests(unittest.TestCase):
    def test_supersampled_atlas_passes_use_premultiplied_lanczos(self) -> None:
        with Fixture(
            with_top=True,
            packs=True,
            case="provenance supersample=2 premultiplied Lanczos for each atlas pass",
            supersample=2,
        ) as fixture:
            source = fixture.render_frames[("body", "color")][0].copy()
            source[:, :, :3] = (255, 0, 0)
            source[source[:, :, 3] > 0, :3] = (72, 57, 41)
            fixture.set_render_frame("body", "color", 0, source)
            fixture.commit(sync_atlas=True)
            resized: dict[tuple[str, str], list[np.ndarray]] = {}
            for key, frames in fixture.render_frames.items():
                resized[key] = []
                for raw in frames:
                    image = Image.fromarray(raw, "RGBA").convert("RGBa")
                    image = image.resize(FRAME_SIZE, Image.Resampling.LANCZOS).convert("RGBA")
                    value = np.asarray(image, dtype=np.uint8).copy()
                    value[value[:, :, 3] < 8] = 0
                    resized[key].append(value)
            shadow_frames = resized[("body", "shadow")]
            peak = max(int(frame[:, :, 3].max()) for frame in shadow_frames)
            for k in range(8):
                for entry_name in fixture.entries:
                    _, part, _, _, pass_name = ROLE_SPECS[entry_name]
                    expected = resized[(part, pass_name)][k].copy()
                    if pass_name == "shadow":
                        expected[:, :, :3] = 0
                        if peak:
                            expected[:, :, 3] = np.round(
                                expected[:, :, 3].astype(np.float32) * 51 / peak
                            ).astype(np.uint8)
                    elif pass_name == "mask":
                        color = resized[(part, "color")][k]
                        expected[color[:, :, 3] <= 16] = 0
                    alpha = expected[:, :, 3]
                    self.assertTrue(np.any((alpha >= 8) & (alpha < 255)), entry_name)
                    np.testing.assert_array_equal(fixture.atlas_frames[entry_name][k], expected)
            assert_run(fixture)


class CompositionCheckTests(unittest.TestCase):
    def test_atlas_height_can_equal_frame_height(self) -> None:
        with Fixture(with_top=True, case="composition atlas height equals one frame") as fixture:
            fixture.unit_data["atlas_hd4"][1] = FRAME_SIZE[1]
            for entry in fixture.contract_data["entries"]:
                entry["hd4_size"][1] = FRAME_SIZE[1]
            for entry in fixture.atlases_data["entries"].values():
                entry["size"][1] = FRAME_SIZE[1]
            fixture.commit()
            assert_run(fixture)

    def run_case(
        self,
        label: str,
        mutation,
        *,
        with_top: bool = False,
        expected_fail_set: Iterable[int] = (1,),
    ) -> RunResult:
        with Fixture(with_top=with_top, case=label) as fixture:
            mutation(fixture)
            fixture.commit()
            return assert_run(fixture, expected_fail_set)

    def test_honest_body_only_and_body_with_top(self) -> None:
        for with_top, label in ((False, "composition honest body-only"), (True, "composition honest body+top")):
            with self.subTest(with_top=with_top), Fixture(with_top=with_top, case=label):
                pass

    def test_each_contract_role_matches_its_unit_slot(self) -> None:
        mappings = (
            ("UNIT_SYNTH_BODY", "role", "shadow", False),
            ("UNIT_SYNTH_SHADOW", "role", "body", False),
            ("HM_SYNTH_BODY", "role", "top", False),
            ("UNIT_SYNTH_TOP", "role", "body", True),
            ("HM_SYNTH_TOP", "role", "mask_body", True),
        )
        for name, key, bad_value, with_top in mappings:
            with self.subTest(name=name):
                def mutate(fixture: Fixture, target: str = name, field: str = key, value: str = bad_value) -> None:
                    self._contract_record(fixture, target)[field] = value

                self.run_case(
                    f"composition wrong role {name}",
                    mutate,
                    with_top=with_top,
                )

    def test_each_mask_name_matches_its_atlas_house_mask(self) -> None:
        for atlas_name, with_top in (("UNIT_SYNTH_BODY", False), ("UNIT_SYNTH_TOP", True)):
            with self.subTest(atlas=atlas_name):
                self.run_case(
                    f"composition house mask mismatch {atlas_name}",
                    lambda fx, target=atlas_name: self._contract_record(fx, target).__setitem__("house_mask", "HM_WRONG"),
                    with_top=with_top,
                )

    def test_all_records_share_unit_types(self) -> None:
        for name in Fixture._entry_names(True):
            with self.subTest(name=name):
                self.run_case(
                    f"composition different unit_types {name}",
                    lambda fx, target=name: self._contract_record(fx, target).__setitem__("unit_types", ["OTHER"]),
                    with_top=True,
                )

    def test_every_record_has_eight_columns(self) -> None:
        for name, with_top in ((name, name.endswith("TOP")) for name in ("UNIT_SYNTH_BODY", "UNIT_SYNTH_SHADOW", "HM_SYNTH_BODY", "UNIT_SYNTH_TOP", "HM_SYNTH_TOP")):
            with self.subTest(name=name):
                self.run_case(
                    f"composition columns count {name}",
                    lambda fx, target=name: self._contract_record(fx, target).__setitem__("columns", 7),
                    with_top=with_top,
                )

    def test_unit_frame_size_matches_each_contract_record(self) -> None:
        for name, with_top in (
            ("UNIT_SYNTH_BODY", False),
            ("UNIT_SYNTH_SHADOW", False),
            ("HM_SYNTH_BODY", False),
            ("UNIT_SYNTH_TOP", True),
            ("HM_SYNTH_TOP", True),
        ):
            with self.subTest(name=name):
                self.run_case(
                    f"composition frame size mismatch {name}",
                    lambda fx, target=name: self._contract_record(fx, target).__setitem__("frame_hd4", [127, 128]),
                    with_top=with_top,
                )

    def test_column_numbers_are_checked_at_zero_seven_and_internal_column(self) -> None:
        for name in Fixture._entry_names(True):
            for k in (0, 7, 3):
                with self.subTest(name=name, k=k):
                    def mutate(fixture: Fixture, target: str = name, column: int = k) -> None:
                        self._contract_record(fixture, target)["column_meaning"][column]["column"] = (column + 1) % 8

                    self.run_case(f"composition wrong column number {name} k={k}", mutate, with_top=True)

    def test_yaw_lists_must_match_across_records(self) -> None:
        for name in Fixture._entry_names(True):
            for k in (0, 7, 3):
                with self.subTest(name=name, k=k), Fixture(
                    with_top=True, case=f"composition yaw list mismatch {name} k={k}",
                ) as fixture:
                    for entry in fixture.contract_data["entries"]:
                        entry["column_meaning"][1]["yaw_deg"] = 0
                    DirectionMarkerHelpers()._install_direction_markers(fixture, 63)
                    fixture.commit()
                    assert_run(fixture)
                    self._contract_record(fixture, name)["column_meaning"][k]["yaw_deg"] += 1
                    fixture.commit()
                    assert_run(fixture, {1})

    def test_atlas_keys_are_exactly_the_unit_record_names(self) -> None:
        def mutate(fixture: Fixture) -> None:
            fixture.add_contract_entry(
                _base_contract_entry("OUTSIDE", "body", None),
                "OUTSIDE.png",
                fixture.atlas_frames["UNIT_SYNTH_BODY"].copy(),
            )
            fixture.case = "composition extra atlases.json entry outside unit R"

        self.run_case("composition extra atlases.json entry outside unit R", mutate, with_top=False)

    def test_duplicate_atlas_filename_is_rejected_without_breaking_other_checks(self) -> None:
        with Fixture(with_top=True, case="composition repeated atlas filename") as fixture:
            fixture.render_frames[("top", "color")] = fixture.render_frames[("body", "color")].copy()
            fixture.render_frames[("top", "mask")] = fixture.render_frames[("body", "mask")].copy()
            fixture.atlas_frames["UNIT_SYNTH_TOP"] = fixture.atlas_frames["UNIT_SYNTH_BODY"].copy()
            fixture.atlas_frames["HM_SYNTH_TOP"] = fixture.atlas_frames["HM_SYNTH_BODY"].copy()
            fixture.manifest_data["bbox_hd4"]["top"] = fixture.manifest_data["bbox_hd4"]["body"].copy()
            fixture.atlases_data["entries"]["HM_SYNTH_TOP"]["file"] = fixture.atlases_data["entries"]["HM_SYNTH_BODY"]["file"]
            fixture.atlas_files_to_omit.add("HM_SYNTH_TOP.png")
            fixture.commit()
            assert_run(fixture, {1})

    def test_unit_and_contract_atlas_sizes_must_match(self) -> None:
        cases = [("unit", None, [1024, 130])]
        cases.extend(("contract", name, [1023, 129]) for name in Fixture._entry_names(True))
        for field, name, size in cases:
            with self.subTest(field=field, name=name):
                def mutate(fixture: Fixture, where: str = field, target: str | None = name, value: list[int] = size) -> None:
                    if where == "unit":
                        fixture.unit_data["atlas_hd4"] = value
                    else:
                        self._contract_record(fixture, target)["hd4_size"] = value

                self.run_case(f"composition mismatched atlas size {field} {name}", mutate, with_top=True)

    def test_atlas_width_and_height_constraints(self) -> None:
        for size in ([1023, 128], [1024, 256], [1024, 127]):
            with self.subTest(size=size):
                result = self.run_case(
                    f"composition unsupported unit atlas size {size}",
                    lambda fx, bad_size=size: fx.unit_data.__setitem__("atlas_hd4", bad_size),
                )
                self.assertIn("не поддерживается", result.lines[0])

    def test_nontransparent_pixels_below_the_first_row_are_rejected(self) -> None:
        for name in Fixture._entry_names(True):
            with self.subTest(name=name), Fixture(with_top=True, case=f"composition padding pixel {name}") as fixture:
                fixture.atlas_padding[name] = [(0, 128, (255, 255, 255, 16) if name.startswith("HM_") else (0, 0, 0, 16))]
                fixture.commit()
                assert_run(fixture, {1})

    def test_render_directory_cannot_contain_extra_files_or_unused_part_directories(self) -> None:
        def extra_file(fixture: Fixture) -> None:
            (fixture.render_dir / "body" / "extra.txt").write_text("extra", encoding="utf-8")

        def extra_part(fixture: Fixture) -> None:
            (fixture.render_dir / "top").mkdir()

        def extra_top_file(fixture: Fixture) -> None:
            (fixture.render_dir / "top" / "extra.txt").write_text("extra", encoding="utf-8")

        def extra_nested_folder(fixture: Fixture) -> None:
            (fixture.render_dir / "body" / "unexpected").mkdir()

        def extra_top_nested_folder(fixture: Fixture) -> None:
            (fixture.render_dir / "top" / "unexpected").mkdir()

        self.run_case("composition extra file in body directory", extra_file)
        self.run_case("composition extra file in top directory", extra_top_file, with_top=True)
        self.run_case("composition nested folder in body directory", extra_nested_folder)
        self.run_case("composition nested folder in top directory", extra_top_nested_folder, with_top=True)
        self.run_case("composition unused top directory", extra_part)

    def test_atlas_directory_cannot_contain_unlisted_files(self) -> None:
        def mutate(fixture: Fixture) -> None:
            _save_png(fixture.atlases_dir / "UNLISTED.png", fixture._atlas_png("UNIT_SYNTH_BODY"))

        def extra_folder(fixture: Fixture) -> None:
            (fixture.atlases_dir / "unexpected").mkdir()

        self.run_case("composition extra file in atlas directory", mutate)
        self.run_case("composition directory in atlas folder", extra_folder)

    def test_manifest_entry_outside_unit_r_does_not_grant_pack_permission(self) -> None:
        with Fixture(case="composition OUTSIDE manifest name is not in unit-derived R") as fixture:
            fixture.add_contract_entry(
                _base_contract_entry("OUTSIDE", "body", None),
                "OUTSIDE.png",
                fixture.atlas_frames["UNIT_SYNTH_BODY"].copy(),
            )
            fixture.commit()
            before = read_pack(fixture.pack_before)
            after = read_pack(fixture.pack_after)
            outside = b"outside pack bytes deliberately different from OUTSIDE.png"
            write_pack(
                fixture.pack_before,
                [*before, PackEntry(len(before), "OUTSIDE", "DAT", outside)],
            )
            write_pack(
                fixture.pack_after,
                [*after, PackEntry(len(after), "OUTSIDE", "DAT", outside)],
            )
            self.assertNotEqual(
                outside,
                (fixture.atlases_dir / "OUTSIDE.png").read_bytes(),
            )
            assert_run(fixture, {1})

    def test_other_render_top_level_files_and_directories_are_ignored(self) -> None:
        with Fixture(case="composition unrelated render metadata") as fixture:
            (fixture.render_dir / "notes.txt").write_text("metadata", encoding="utf-8")
            (fixture.render_dir / "review").mkdir()
            assert_run(fixture)

    def test_contract_metadata_outside_the_allowed_fields_is_ignored(self) -> None:
        with Fixture(with_top=True, case="composition contract metadata does not set alpha threshold") as fixture:
            fixture.contract_data["light"]["alpha_threshold_exclusive"] = 254
            fixture.contract_data["draw_rules"] = {"alpha_threshold_exclusive": 254}
            for entry in fixture.contract_data["entries"]:
                entry["alpha_threshold_exclusive"] = 254
            fixture.commit()
            assert_run(fixture)

    def test_assigned_atlas_filenames_can_differ_from_record_names(self) -> None:
        with Fixture(with_top=True, case="composition uses filenames assigned by atlases.json") as fixture:
            for index, name in enumerate(fixture.entries):
                (fixture.atlases_dir / fixture.entry_files[name]).unlink()
                filename = f"rendered-{index}.png"
                fixture.entry_files[name] = filename
                fixture.atlases_data["entries"][name]["file"] = filename
            fixture.commit()
            assert_run(fixture)

    def test_render_dimensions_are_checked_for_every_pass_part_and_column(self) -> None:
        for part, pass_name in (
            ("body", "color"), ("body", "mask"), ("body", "markers"), ("body", "shadow"),
            ("top", "color"), ("top", "mask"), ("top", "markers"),
        ):
            for k in (0, 7, 3):
                with self.subTest(part=part, pass_name=pass_name, k=k), Fixture(
                    with_top=True, case=f"composition render dimensions {part}/{pass_name} k={k}",
                ) as fixture:
                    fixture.unit_data["mask_share"] = [0.08, 0.35]
                    frame = fixture.render_frames[(part, pass_name)][k]
                    frame = np.pad(frame, ((0, 1), (0, 1), (0, 0)))
                    path = fixture.render_dir / part / f"{pass_name}_{k}.png"
                    if pass_name != "markers":
                        for name in fixture.entries:
                            _, entry_part, _, _, entry_pass = ROLE_SPECS[name]
                            if (entry_part, entry_pass) == (part, pass_name):
                                frames = dict(fixture.render_frames)
                                frames[(part, pass_name)] = list(frames[(part, pass_name)])
                                frames[(part, pass_name)][k] = frame
                                fixture.atlas_frames[name][k] = _canonical_atlas_frame(name, frames, k)
                    fixture.commit()
                    _save_png(path, frame)
                    assert_run(fixture, {1})

    def test_actual_atlas_size_matches_unit_size_for_every_resource(self) -> None:
        for name in Fixture._entry_names(True):
            with self.subTest(name=name), Fixture(with_top=True, case=f"composition PNG dimensions {name}") as fixture:
                path = fixture.atlases_dir / fixture.entry_files[name]
                _save_png(path, np.pad(fixture._atlas_png(name), ((0, 1), (0, 0), (0, 0))))
                InputReadFailureTests._sync_atlas_png_input(fixture, name)
                assert_run(fixture, {1})

    @staticmethod
    def _contract_record(fixture: Fixture, name: str) -> dict[str, object]:
        return next(entry for entry in fixture.contract_data["entries"] if entry["name"] == name)


class DirectionMarkerHelpers:
    @staticmethod
    def _set_marker_centroid(rgba: np.ndarray, channel: int, x_hd4: float, y_hd4: float, supersample: int) -> None:
        px = x_hd4 * supersample - 0.5
        py = y_hd4 * supersample - 0.5
        x0 = math.floor(px)
        y0 = math.floor(py)
        fx = px - x0
        fy = py - y0
        weights = np.rint(255 * np.outer((1 - fy, fy), (1 - fx, fx))).astype(np.uint8)
        height, width = rgba.shape[:2]
        for iy in range(2):
            for ix in range(2):
                if weights[iy, ix] and 0 <= x0 + ix < width and 0 <= y0 + iy < height:
                    rgba[y0 + iy, x0 + ix, channel] = weights[iy, ix]

    @staticmethod
    def _projected_angle(yaw_deg: float, elevation_deg: float) -> float:
        yaw = math.radians(yaw_deg)
        elevation = math.radians(elevation_deg)
        return math.degrees(math.atan2(math.sin(yaw) * math.sin(elevation), math.cos(yaw)))

    @staticmethod
    def _circular_delta(a: float, b: float) -> float:
        return ((a - b + 180) % 360) - 180

    @staticmethod
    def _set_blue_offset(rgba: np.ndarray, axis: str, distance: int) -> None:
        rgba[..., 2] = 0
        if axis == "x" and distance == 1:
            rgba[63, 64, 2], rgba[63, 65, 2] = 111, 144
            rgba[64, 64, 2], rgba[64, 65, 2] = 110, 145
        elif axis == "x" and distance == 2:
            rgba[63, 65, 2], rgba[63, 66, 2] = 93, 162
            rgba[64, 65, 2], rgba[64, 66, 2] = 94, 161
        elif axis == "y" and distance == 1:
            rgba[64, 63, 2], rgba[64, 64, 2] = 110, 111
            rgba[65, 63, 2], rgba[65, 64, 2] = 145, 144
        elif axis == "y" and distance == 2:
            rgba[65, 63, 2], rgba[65, 64, 2] = 93, 94
            rgba[66, 63, 2], rgba[66, 64, 2] = 162, 161
        elif axis == "xy" and distance == 1:
            rgba[64, 64, 2], rgba[64, 65, 2] = 85, 110
            rgba[65, 64, 2], rgba[65, 65, 2] = 110, 145
        else:
            raise AssertionError((axis, distance))
        rgba[..., 3] = np.max(rgba[..., :3], axis=2)

    def _install_direction_markers(
        self,
        fixture: Fixture,
        theta: float,
        deltas: dict[tuple[str, int], float] | None = None,
        overrides: dict[tuple[str, int], float] | None = None,
        green_shifts: dict[tuple[str, int], tuple[int, int]] | None = None,
        blue_offsets: dict[tuple[str, int], tuple[str, int]] | None = None,
    ) -> None:
        deltas = deltas or {}
        overrides = overrides or {}
        green_shifts = green_shifts or {}
        blue_offsets = blue_offsets or {}
        for part in fixture.unit_data["parts"]:
            atlas_name = fixture.unit_data["parts"][part]["atlas"]
            entry = next(record for record in fixture.contract_data["entries"] if record["name"] == atlas_name)
            for k in range(8):
                source = fixture.render_frames[(part, "markers")][k]
                supersample = source.shape[0] // FRAME_SIZE[1]
                rgba = np.zeros_like(source)
                yaw = entry["column_meaning"][k]["yaw_deg"]
                expected = self._projected_angle(yaw, theta)
                target = overrides.get((part, k), expected + deltas.get((part, k), 0.0))
                dx, dy = green_shifts.get((part, k), (0, 0))
                red_x = 64 + dx + 36 * math.cos(math.radians(target))
                red_y = 64 + dy - 36 * math.sin(math.radians(target))
                self._set_marker_centroid(rgba, 0, red_x, red_y, supersample)
                self._set_marker_centroid(rgba, 1, 64.0 + dx, 64.0 + dy, supersample)
                if "top" in fixture.unit_data["parts"]:
                    if (part, k) in blue_offsets:
                        axis, distance = blue_offsets[(part, k)]
                        self._set_blue_offset(rgba, axis, distance)
                    else:
                        self._set_marker_centroid(rgba, 2, 64.0, 64.0, supersample)
                rgba[..., 3] = np.max(rgba[..., :3], axis=2)
                fixture.set_render_frame(part, "markers", k, rgba)

    def _direction_cli(
        self,
        case: str,
        expected_fail: Iterable[int],
        *,
        theta: float = 30.0,
        manifest_theta: float | None = None,
        deltas: dict[tuple[str, int], float] | None = None,
        overrides: dict[tuple[str, int], float] | None = None,
        empty_channel: tuple[str, int, str] | None = None,
        zero_vector: tuple[str, int] | None = None,
        green_shifts: dict[tuple[str, int], tuple[int, int]] | None = None,
        blue_offsets: dict[tuple[str, int], tuple[str, int]] | None = None,
        empty_blue: tuple[str, int] | None = None,
    ) -> None:
        with Fixture(with_top=True, packs=True, case=case, supersample=1) as fixture:
            fixture.camera_data["elevation_deg"] = theta
            fixture.manifest_data["elevation_deg"] = theta if manifest_theta is None else manifest_theta
            self._install_direction_markers(
                fixture,
                theta,
                deltas=deltas,
                overrides=overrides,
                green_shifts=green_shifts,
                blue_offsets=blue_offsets,
            )
            if empty_channel is not None:
                part, k, channel = empty_channel
                rgba = fixture.render_frames[(part, "markers")][k].copy()
                rgba[..., 0 if channel == "R" else 1] = 0
                rgba[..., 3] = np.max(rgba[..., :3], axis=2)
                fixture.set_render_frame(part, "markers", k, rgba)
            if empty_blue is not None:
                part, k = empty_blue
                rgba = fixture.render_frames[(part, "markers")][k].copy()
                rgba[..., 2] = 0
                rgba[..., 3] = np.max(rgba[..., :3], axis=2)
                fixture.set_render_frame(part, "markers", k, rgba)
            if zero_vector is not None:
                part, k = zero_vector
                rgba = fixture.render_frames[(part, "markers")][k].copy()
                rgba[..., 0] = rgba[..., 1]
                rgba[..., 3] = np.max(rgba[..., :3], axis=2)
                fixture.set_render_frame(part, "markers", k, rgba)
            fixture.commit(update_hashes=True, update_packs=True)
            assert_run(fixture, expected_fail_set=set(expected_fail))

    def _check4_cli(
        self,
        case: str,
        expected_fail: Iterable[int],
        *,
        green_shifts: dict[tuple[str, int], tuple[int, int]] | None = None,
        blue_offsets: dict[tuple[str, int], tuple[str, int]] | None = None,
        empty_blue: tuple[str, int] | None = None,
        with_top: bool = True,
    ) -> None:
        with Fixture(with_top=with_top, packs=True, case=case, supersample=1) as fixture:
            fixture.camera_data["elevation_deg"] = 30.0
            fixture.manifest_data["elevation_deg"] = 30.0
            self._install_direction_markers(
                fixture,
                30.0,
                green_shifts=green_shifts,
                blue_offsets=blue_offsets,
            )
            if empty_blue is not None:
                part, k = empty_blue
                rgba = fixture.render_frames[(part, "markers")][k].copy()
                rgba[..., 2] = 0
                rgba[..., 3] = np.max(rgba[..., :3], axis=2)
                fixture.set_render_frame(part, "markers", k, rgba)
            fixture.commit(update_hashes=True, update_packs=True)
            assert_run(fixture, expected_fail_set=set(expected_fail))

class DirectionAndMarkerTests(DirectionMarkerHelpers, unittest.TestCase):
    def test_marker_centroids_use_channel_weights_and_render_pixel_centers(self) -> None:
        for supersample in (1, 2):
            for part in ("body", "top"):
                for channel in (0, 1, 2):
                    for k in (0, 7, 3):
                        for dx, dy in ((0, 0), (-1, 0), (0, -1)):
                            with self.subTest(s=supersample, part=part, channel=channel, k=k, shift=(dx, dy)), Fixture(
                                with_top=True, supersample=supersample,
                                case=f"weighted marker s={supersample} {part} channel={channel} k={k} shift=({dx},{dy})",
                            ) as fixture:
                                frame = fixture.render_frames[(part, "markers")][k].copy()
                                if channel == 0:
                                    frame[2 * supersample, 2 * supersample, channel] = 1
                                else:
                                    frame[..., channel] = 0
                                    near = 64 * supersample - 1
                                    far = near + 51 * supersample
                                    weight = 102 * supersample - 1
                                    for row in (near, near + 1):
                                        frame[row, near, channel] = weight
                                        frame[row, far, channel] = 1
                                frame[..., 3] = frame[..., :3].max(axis=2)
                                frame = _translate_rgba(frame, dx * supersample, dy * supersample)
                                fixture.set_render_frame(part, "markers", k, frame)
                                fixture.commit()
                                assert_run(fixture)

    def test_direction_honest_projection_for_both_parts_and_all_columns(self) -> None:
        for theta in (30.0, 63.0):
            self._direction_cli(f"direction_theta_{theta}", set(), theta=theta)

    def test_direction_3deg_is_inside_threshold_for_body_top_k0_k7_k3(self) -> None:
        for part in ("body", "top"):
            for k in (0, 7, 3):
                with self.subTest(part=part, k=k):
                    self._direction_cli(f"direction_3deg_{part}_{k}", set(), deltas={(part, k): 2.95})

    def test_direction_4deg_fails_only_3_for_body_top_k0_k7_k3(self) -> None:
        for part in ("body", "top"):
            for k in (0, 7, 3):
                with self.subTest(part=part, k=k):
                    self._direction_cli(f"direction_4deg_{part}_{k}", {3}, deltas={(part, k): 4.0})

    def test_direction_manifest_elevation_must_equal_camera(self) -> None:
        self._direction_cli("direction_elevation_mismatch", {3}, theta=30.0, manifest_theta=30.01)

    def test_direction_circular_wrap_near_180(self) -> None:
        self._direction_cli("direction_wrap", set(), theta=30.0, overrides={("body", 4): -179.0})

    def test_direction_empty_red_fails_only_3_for_both_parts_and_k0_k7_k3(self) -> None:
        for part in ("body", "top"):
            for k in (0, 7, 3):
                with self.subTest(part=part, k=k):
                    self._direction_cli(f"direction_empty_R_{part}_{k}", {3}, empty_channel=(part, k, "R"))

    def test_direction_empty_green_fails_3_and_4_for_both_parts_and_k0_k7_k3(self) -> None:
        for part in ("body", "top"):
            for k in (0, 7, 3):
                with self.subTest(part=part, k=k):
                    self._direction_cli(f"direction_empty_G_{part}_{k}", {3, 4}, empty_channel=(part, k, "G"))

    def test_direction_zero_red_green_vector_fails_only_3(self) -> None:
        for part in ("body", "top"):
            for k in (0, 7, 3):
                with self.subTest(part=part, k=k):
                    self._direction_cli(f"direction_zero_vector_{part}_{k}", {3}, zero_vector=(part, k))

    def test_green_marker_distance_1_inclusive_for_body_top_k0_k7_k3_xy(self) -> None:
        for part in ("body", "top"):
            for k in (0, 7, 3):
                for axis in ("x", "y"):
                    shift = (1, 0) if axis == "x" else (0, 1)
                    with self.subTest(part=part, k=k, axis=axis):
                        self._check4_cli(f"green_d1_{part}_{k}_{axis}", set(), green_shifts={(part, k): shift})

    def test_green_marker_distance_2_fails_only_4_for_body_top_k0_k7_k3_xy(self) -> None:
        for part in ("body", "top"):
            for k in (0, 7, 3):
                for axis in ("x", "y"):
                    shift = (2, 0) if axis == "x" else (0, 2)
                    with self.subTest(part=part, k=k, axis=axis):
                        self._check4_cli(f"green_d2_{part}_{k}_{axis}", {4}, green_shifts={(part, k): shift})

    def test_blue_marker_distance_1_from_mean_is_inclusive_xy(self) -> None:
        for part in ("body", "top"):
            for k in (0, 7, 3):
                for axis in ("x", "y"):
                    with self.subTest(part=part, k=k, axis=axis):
                        self._check4_cli(f"blue_d1_{part}_{k}_{axis}", set(), blue_offsets={(part, k): (axis, 1)})

    def test_blue_marker_distance_2_from_mean_fails_only_4_xy(self) -> None:
        for part in ("body", "top"):
            for k in (0, 7, 3):
                for axis in ("x", "y"):
                    with self.subTest(part=part, k=k, axis=axis):
                        self._check4_cli(f"blue_d2_{part}_{k}_{axis}", {4}, blue_offsets={(part, k): (axis, 2)})

    def test_empty_blue_marker_fails_only_4_for_body_top_k0_k7_k3(self) -> None:
        for part in ("body", "top"):
            for k in (0, 7, 3):
                with self.subTest(part=part, k=k):
                    self._check4_cli(f"blue_empty_{part}_{k}", {4}, empty_blue=(part, k))

    def test_body_only_zero_blue_channels_are_allowed(self) -> None:
        self._check4_cli("blue_zero_without_top", set(), with_top=False)

    def test_green_and_blue_distances_use_euclidean_norm(self) -> None:
        for part in ("body", "top"):
            for k in (0, 7, 3):
                with self.subTest(part=part, k=k, channel="green"):
                    self._check4_cli(f"green diagonal {part} k={k}", {4}, green_shifts={(part, k): (1, 1)})
                with self.subTest(part=part, k=k, channel="blue"):
                    self._check4_cli(f"blue diagonal {part} k={k}", {4}, blue_offsets={(part, k): ("xy", 1)})


def _opaque_bounds(frame: np.ndarray) -> tuple[int, int, int, int]:
    ys, xs = np.where(frame[:, :, 3] > 16)
    if not len(xs):
        raise AssertionError("fixture frame unexpectedly empty")
    return int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())


def _translate_rgba(frame: np.ndarray, dx: int, dy: int) -> np.ndarray:
    height, width = frame.shape[:2]
    moved = np.zeros_like(frame)
    sx0, sx1 = max(0, -dx), min(width, width - dx)
    sy0, sy1 = max(0, -dy), min(height, height - dy)
    if sx0 < sx1 and sy0 < sy1:
        moved[sy0 + dy : sy1 + dy, sx0 + dx : sx1 + dx] = frame[sy0:sy1, sx0:sx1]
    return moved


def _set_bbox_shift(fixture: Fixture, part: str, k: int, dx: int, dy: int) -> None:
    box = fixture.manifest_data["bbox_hd4"][part][str(k)]
    fixture.manifest_data["bbox_hd4"][part][str(k)] = [box[0] + dx, box[1] + dy, box[2] + dx, box[3] + dy]


def _margin_part(fixture: Fixture, part: str, k: int, x: int, y: int) -> None:
    width = 120 if part == "body" else 20
    rgb = (72, 57, 41) if part == "body" else (91, 75, 54)
    color = np.zeros((FRAME_SIZE[1], FRAME_SIZE[0], 4), dtype=np.uint8)
    color[y:y + 10, x:x + width] = (*rgb, 255)
    mask = np.zeros_like(color)
    if part == "body":
        mask[y + 2:y + 8, x + 40:x + 80] = (255, 255, 255, 255)
    else:
        mask[y + 2:y + 7, x + 6:x + 14] = (255, 255, 255, 255)
    fixture.render_frames[(part, "color")][k] = color
    fixture.render_frames[(part, "mask")][k] = mask
    fixture.manifest_data["bbox_hd4"][part][str(k)] = [x, y, x + width, y + 10]


def _margin_shadows(fixture: Fixture, side: str) -> None:
    fixture.contract_data["light"]["median_angle_degrees"] = 180 if side == "right" else 0
    for k in range(8):
        union = fixture.render_frames[("body", "color")][k][..., 3] > 16
        union |= fixture.render_frames[("top", "color")][k][..., 3] > 16
        y = max(2, min(124, int(round(float(np.where(union)[0].mean()) - 0.5))))
        x = 2 if side == "right" else 124
        shadow = np.zeros_like(fixture.render_frames[("body", "shadow")][k])
        shadow[y:y + 2, x:x + 2] = (0, 0, 0, 255)
        fixture.render_frames[("body", "shadow")][k] = shadow


def _margin_baseline(fixture: Fixture) -> None:
    fixture.unit_data["length_m"] = 120
    fixture.unit_data["mask_share"] = [0.08, 0.35]
    for k in range(8):
        _margin_part(fixture, "body", k, 4, 59)
        _margin_part(fixture, "top", k, 54, 59)
    _margin_shadows(fixture, "left")


def _put_unit_resource_at_margin(fixture: Fixture, target: str, k: int, side: str, edge: int) -> None:
    _, part, _, _, _ = ROLE_SPECS[target]
    width = 120 if part == "body" else 20
    x, y = (4 if part == "body" else 54), 59
    if side == "left":
        x = edge
    elif side == "right":
        x = edge - width + 1
    elif side == "top":
        y = edge
    else:
        y = edge - 10 + 1
    _margin_part(fixture, part, k, x, y)
    _margin_shadows(fixture, side)


def _outside_margin() -> np.ndarray:
    ys, xs = np.indices(FRAME_SIZE[::-1])
    return (xs < 2) | (xs > FRAME_SIZE[0] - 3) | (ys < 2) | (ys > FRAME_SIZE[1] - 3)


def _set_extreme_pixel_alpha(fixture: Fixture, target: str, k: int, side: str, alpha: int) -> None:
    _, part, _, _, pass_name = ROLE_SPECS[target]
    frame = fixture.render_frames[(part, pass_name)][k].copy()
    outside = _outside_margin() & (frame[..., 3] > 0)
    frame[outside, 3] = alpha
    fixture.render_frames[(part, pass_name)][k] = frame


def _put_shadow_pixel(fixture: Fixture, k: int, side: str, edge: int, alpha: int) -> None:
    frame = fixture.render_frames[("body", "shadow")][k].copy()
    x, y = {
        "left": (edge, 64),
        "right": (edge, 64),
        "top": (120, edge),
        "bottom": (120, edge),
    }[side]
    raw_alpha = {16: 80, 17: 85}[alpha]
    frame[y, x] = (0, 0, 0, raw_alpha)
    fixture.render_frames[("body", "shadow")][k] = frame


class MarginCheckTests(unittest.TestCase):
    TARGETS = ("UNIT_SYNTH_BODY", "UNIT_SYNTH_TOP", "UNIT_SYNTH_SHADOW", "HM_SYNTH_BODY", "HM_SYNTH_TOP")
    SIDES = ("left", "right", "top", "bottom")
    DIRECTIONS = (0, 7, 3)

    def _edge_case(self, target: str, side: str, k: int, edge: int, expected_fail: Iterable[int], label: str) -> None:
        with Fixture(with_top=True, case=f"margin {label} {target} {side} k={k}") as fixture:
            is_mask = target.startswith("HM_")
            is_alpha17 = label == "alpha17 outer edge"
            if target == "UNIT_SYNTH_SHADOW":
                _put_shadow_pixel(fixture, k, side, edge, 17)
                fixture.commit(sync_atlas=True)
            else:
                _margin_baseline(fixture)
                if not is_mask or not set(expected_fail):
                    _put_unit_resource_at_margin(fixture, target, k, side, edge)
                    if is_alpha17:
                        _set_extreme_pixel_alpha(fixture, target, k, side, 17)
                fixture.commit(sync_atlas=True)
                if is_mask:
                    _, part, _, _, _ = ROLE_SPECS[target]
                    x, y = (edge, 64) if side in ("left", "right") else (64, edge)
                    support = fixture.atlas_frames[fixture.unit_data["parts"][part]["atlas"]][k, y, x, 3]
                    if set(expected_fail):
                        self.assertLessEqual(int(support), 16)
                    else:
                        self.assertGreater(int(support), 16)
                    frame = fixture.atlas_frames[target][k].copy()
                    frame[y, x] = (255, 255, 255, 17 if is_alpha17 else 255)
                    fixture.set_frame(target, k, frame, sync_render=True)
                    fixture.commit()
            outside = _outside_margin()
            for name in fixture.entries:
                if name != target:
                    self.assertFalse(np.any(fixture.atlas_frames[name][k, ..., 3][outside] > 16), name)
            protruding = fixture.atlas_frames[target][k, ..., 3][outside]
            if is_alpha17:
                self.assertTrue(np.any(protruding == 17))
                self.assertFalse(np.any(protruding > 17))
            assert_run(fixture, expected_fail)

    def test_inset_boundary_index_2_or_w_minus_3_passes_for_each_resource_and_direction(self) -> None:
        for target in self.TARGETS:
            for side in self.SIDES:
                edge = 2 if side in ("left", "top") else 125
                for k in self.DIRECTIONS:
                    with self.subTest(target=target, side=side, k=k):
                        self._edge_case(target, side, k, edge, (), "included boundary")

    def test_neighbor_index_1_or_w_minus_2_fails_only_check5(self) -> None:
        for target in self.TARGETS:
            for side in self.SIDES:
                edge = 1 if side in ("left", "top") else 126
                for k in self.DIRECTIONS:
                    with self.subTest(target=target, side=side, k=k):
                        self._edge_case(target, side, k, edge, {5, 8, 10} if target.startswith("HM_") else {5}, "outside boundary")

    def test_alpha_17_at_outer_frame_edge_fails_only_check5(self) -> None:
        for target in self.TARGETS:
            for side in self.SIDES:
                edge = 0 if side in ("left", "top") else 127
                for k in self.DIRECTIONS:
                    with self.subTest(target=target, side=side, k=k):
                        self._edge_case(target, side, k, edge, {5, 8, 10} if target.startswith("HM_") else {5}, "alpha17 outer edge")

    def test_alpha_16_outer_edge_is_ignored_for_color_and_shadow(self) -> None:
        for target in ("UNIT_SYNTH_BODY", "UNIT_SYNTH_TOP", "UNIT_SYNTH_SHADOW"):
            for side in self.SIDES:
                for k in self.DIRECTIONS:
                    with self.subTest(target=target, side=side, k=k):
                        with Fixture(with_top=True, case=f"margin alpha16 {target} {side} k={k}") as fixture:
                            if target == "UNIT_SYNTH_SHADOW":
                                _put_shadow_pixel(fixture, k, side, 0 if side in ("left", "top") else 127, 16)
                                fixture.commit(sync_atlas=True)
                            else:
                                frame = fixture.atlas_frames[target][k].copy()
                                x, y = {
                                    "left": (0, 64),
                                    "right": (127, 64),
                                    "top": (64, 0),
                                    "bottom": (64, 127),
                                }[side]
                                rgb = (72, 57, 41) if target == "UNIT_SYNTH_BODY" else (91, 75, 54)
                                frame[y, x] = (*rgb, 16)
                                fixture.set_frame(target, k, frame, sync_render=True)
                                fixture.commit(sync_atlas=True)
                            result = assert_run(fixture)
                            self.assertEqual(result.statuses[5], "PASS")

    def test_alpha_16_mask_edge_fails_8_and_10_but_not_5(self) -> None:
        for target in ("HM_SYNTH_BODY", "HM_SYNTH_TOP"):
            for side in self.SIDES:
                for k in self.DIRECTIONS:
                    with self.subTest(target=target, side=side, k=k):
                        with Fixture(with_top=True, case=f"margin alpha16 mask {target} {side} k={k}") as fixture:
                            fixture.unit_data["mask_share"] = [0.08, 0.35]
                            frame = fixture.atlas_frames[target][k].copy()
                            x, y = {
                                "left": (0, 64),
                                "right": (127, 64),
                                "top": (64, 0),
                                "bottom": (64, 127),
                            }[side]
                            frame[y, x] = (255, 255, 255, 16)
                            fixture.set_frame(target, k, frame)
                            fixture.commit()
                            result = assert_run(fixture, {8, 10})
                            self.assertEqual(result.statuses[5], "PASS")


def _rect_rgba(width: int, height: int, x: int, y: int, rgba: tuple[int, int, int, int]) -> np.ndarray:
    frame = np.zeros((FRAME_SIZE[1], FRAME_SIZE[0], 4), dtype=np.uint8)
    frame[y : y + height, x : x + width] = rgba
    return frame


def _set_part_rect(
    fixture: Fixture,
    part: str,
    k: int,
    x: int,
    y: int,
    width: int,
    height: int,
    *,
    bbox_width: int | None = None,
    bbox_height: int | None = None,
) -> None:
    color = (72, 57, 41, 255) if part == "body" else (91, 75, 54, 255)
    mask = (255, 255, 255, 255)
    fixture.render_frames[(part, "color")][k] = _rect_rgba(width, height, x, y, color)
    mask_width = min(20 if part == "body" else 4, width)
    mask_height = min(10 if part == "body" else 5, height)
    fixture.render_frames[(part, "mask")][k] = _rect_rgba(mask_width, mask_height, x, y, mask)
    fixture.manifest_data["bbox_hd4"][part][str(k)] = [
        x,
        y,
        x + (width if bbox_width is None else bbox_width),
        y + (height if bbox_height is None else bbox_height),
    ]


def _place_shadow_at_union_center(fixture: Fixture, k: int) -> None:
    union = fixture.render_frames[("body", "color")][k][:, :, 3] > 16
    if fixture.with_top:
        union |= fixture.render_frames[("top", "color")][k][:, :, 3] > 16
    ys = np.where(union)[0]
    center_y = float(ys.mean())
    y = int(round(center_y - 4.5))
    fixture.render_frames[("body", "shadow")][k] = _rect_rgba(8, 10, 118, y, (0, 0, 0, 255))


def _width_case_6a(fixture: Fixture, k: int, width: int, combined: bool) -> None:
    fixture.unit_data["mask_share"] = [0.0, 1.0]
    if not combined:
        x = (128 - width) // 2
        _set_part_rect(fixture, "body", k, x, 59, width, 10)
        return
    body_width, top_width, union_left = 80, 30, 2
    _set_part_rect(fixture, "body", k, union_left + width - body_width, 59, body_width, 10)
    _set_part_rect(fixture, "top", k, union_left, 61, top_width, 5)


class SizeCheckTests(unittest.TestCase):
    def test_6a_reference_width_thresholds_for_body_and_body_top_union_at_yaw_0_and_180(self) -> None:
        for combined in (False, True):
            for k in (0, 4):
                for width, fail in ((95, False), (105, False), (94, True), (106, True)):
                    with self.subTest(combined=combined, k=k, width=width):
                        with Fixture(
                            with_top=combined,
                            case=f"size 6a combined={combined} k={k} width={width}",
                        ) as fixture:
                            _width_case_6a(fixture, k, width, combined)
                            _place_shadow_at_union_center(fixture, k)
                            fixture.commit(sync_atlas=True)
                            assert_run(fixture, {6} if fail else set())

    def _size_bbox_case(self, part: str, k: int, axis: str, measured: int, bbox_size: int, fail: bool) -> None:
        with Fixture(with_top=True, case=f"size 6b {part} k={k} {axis} M={measured} B={bbox_size}") as fixture:
            fixture.unit_data["mask_share"] = [0.0, 1.0]
            if axis == "width":
                if k in (0, 4):
                    x = (128 - measured) // 2
                    fixture.unit_data["length_m"] = measured
                    for direction in (0, 4):
                        _set_part_rect(fixture, "body", direction, x, 59, measured, 10)
                        _set_part_rect(fixture, "top", direction, x, 61, measured, 5)
                        _place_shadow_at_union_center(fixture, direction)
                else:
                    baseline_height = 10 if part == "body" else 5
                    baseline_y = 59 if part == "body" else 61
                    x = (128 - measured) // 2
                    _set_part_rect(fixture, part, k, x, baseline_y, measured, baseline_height)
                    _place_shadow_at_union_center(fixture, k)
                box = fixture.manifest_data["bbox_hd4"][part][str(k)]
                box[2] = box[0] + bbox_size
            else:
                width = 100 if part == "body" else 20
                x = 14 if part == "body" else 54
                y = (128 - measured) // 2
                _set_part_rect(fixture, part, k, x, y, width, measured)
                box = fixture.manifest_data["bbox_hd4"][part][str(k)]
                box[3] = box[1] + bbox_size
                _place_shadow_at_union_center(fixture, k)
            fixture.commit(sync_atlas=True)
            assert_run(fixture, {6} if fail else set())

    def test_6b_width_uses_both_max_tolerance_branches_for_body_and_top(self) -> None:
        for part in ("body", "top"):
            for k in (0, 7, 3):
                for measured, bbox_size, fail in (
                    (95, 100, False),
                    (94, 100, True),
                    (105, 100, False),
                    (106, 100, True),
                    (20, 22, False),
                    (20, 23, True),
                    (22, 20, False),
                    (23, 20, True),
                ):
                    with self.subTest(part=part, k=k, measured=measured, bbox_size=bbox_size):
                        self._size_bbox_case(part, k, "width", measured, bbox_size, fail)

    def test_6b_height_uses_both_max_tolerance_branches_for_body_and_top(self) -> None:
        for part in ("body", "top"):
            base_height = 10 if part == "body" else 5
            for k in (0, 7, 3):
                for measured, bbox_size, fail in (
                    (95, 100, False),
                    (94, 100, True),
                    (105, 100, False),
                    (106, 100, True),
                    (base_height, base_height + 2, False),
                    (base_height, base_height + 3, True),
                    (base_height, base_height - 2, False),
                    (base_height, base_height - 3, True),
                ):
                    with self.subTest(part=part, k=k, measured=measured, bbox_size=bbox_size):
                        self._size_bbox_case(part, k, "height", measured, bbox_size, fail)

    def test_6a_nonpositive_lref_fails_only_check_6(self) -> None:
        with Fixture(case="size Lref zero") as fixture:
            fixture.camera_data["hd4_px_per_m"] = 0
            fixture.commit()
            assert_run(fixture, {6})

    def test_missing_yaw_zero_or_180_fails_only_check_6_with_markers_updated(self) -> None:
        for k, replacement in ((0, 1.0), (4, 181.0)):
            with self.subTest(k=k), Fixture(with_top=True, case=f"size missing yaw at k={k}") as fixture:
                for entry in fixture.contract_data["entries"]:
                    entry["column_meaning"][k]["yaw_deg"] = replacement
                yaw = math.radians(replacement)
                theta = math.radians(63)
                angle = math.atan2(math.sin(yaw) * math.sin(theta), math.cos(yaw))
                for part in ("body", "top"):
                    marker = fixture.render_frames[(part, "markers")][k].copy()
                    marker[:, :, 0] = 0
                    _marker_channel(marker, 0, 64 + 20 * math.cos(angle), 64 - 20 * math.sin(angle))
                    marker[:, :, 3] = np.maximum.reduce((marker[:, :, 0], marker[:, :, 1], marker[:, :, 2]))
                    fixture.render_frames[(part, "markers")][k] = marker
                fixture.commit()
                assert_run(fixture, {6})

    def test_empty_top_direction_fails_six_and_eight(self) -> None:
        with Fixture(with_top=True, case="size top empty k=1") as fixture:
            fixture.render_frames[("top", "color")][1] = np.zeros_like(fixture.render_frames[("top", "color")][1])
            fixture.render_frames[("top", "mask")][1] = np.zeros_like(fixture.render_frames[("top", "mask")][1])
            fixture.commit(sync_atlas=True)
            assert_run(fixture, {6, 8})

    def test_empty_body_direction_with_top_fails_six_seven_and_eight(self) -> None:
        with Fixture(with_top=True, case="size body empty k=1 with top") as fixture:
            fixture.render_frames[("body", "color")][1] = np.zeros_like(fixture.render_frames[("body", "color")][1])
            fixture.render_frames[("body", "mask")][1] = np.zeros_like(fixture.render_frames[("body", "mask")][1])
            fixture.commit(sync_atlas=True)
            assert_run(fixture, {6, 7, 8})


class PackAndCliTests(unittest.TestCase):
    def _append_same_entry(self, fixture: Fixture, name: str, payload: bytes = b"outside bytes", extension: str = "DAT") -> None:
        before = _pack_entries(fixture.pack_before)
        after = _pack_entries(fixture.pack_after)
        before.append(_new_entry(name, extension, payload))
        after.append(_new_entry(name, extension, payload))
        _write_pack_entries(fixture.pack_before, before)
        _write_pack_entries(fixture.pack_after, after)

    def test_honest_replacement_allows_directory_offsets_to_change(self) -> None:
        with Fixture(with_top=True, packs=True, case="check2 offsets may move") as fixture:
            assigned = _assigned_pngs(fixture)
            names = _r_names(fixture)
            before = [_new_entry(name, "PNG", b"x") for name in names]
            after = [_new_entry(name, "PNG", assigned[name]) for name in names]
            before.append(_new_entry("KEEP_SYNTH", "DAT", b"preserve me"))
            after.append(_new_entry("KEEP_SYNTH", "DAT", b"preserve me"))
            _write_pack_entries(fixture.pack_before, before)
            _write_pack_entries(fixture.pack_after, after)
            self.assertNotEqual(
                _pack_offsets(fixture.pack_before)["KEEP_SYNTH"],
                _pack_offsets(fixture.pack_after)["KEEP_SYNTH"],
            )
            result = assert_run(fixture)
            self.assertEqual(result.statuses[2], "PASS")

    def test_duplicate_name_in_before_fails_even_when_extensions_differ(self) -> None:
        with Fixture(with_top=True, packs=True, case="check2 duplicate old name") as fixture:
            before = _pack_entries(fixture.pack_before)
            after = _pack_entries(fixture.pack_after)
            before.append(_new_entry("KEEP_SYNTH", "BIN", b"second old entry"))
            after.append(_new_entry("KEEP_SYNTH", "BIN", b"second old entry"))
            _write_pack_entries(fixture.pack_before, before)
            _write_pack_entries(fixture.pack_after, after)
            assert_run(fixture, {2})

    def test_sequence_order_change_fails(self) -> None:
        with Fixture(with_top=True, packs=True, case="check2 pair order") as fixture:
            before = _pack_entries(fixture.pack_before)
            after = _pack_entries(fixture.pack_after)
            before.extend((_new_entry("SEQ_A", "DAT", b"a"), _new_entry("SEQ_B", "DAT", b"b")))
            after.extend((_new_entry("SEQ_A", "DAT", b"a"), _new_entry("SEQ_B", "DAT", b"b")))
            after[-2], after[-1] = after[-1], after[-2]
            _write_pack_entries(fixture.pack_before, before)
            _write_pack_entries(fixture.pack_after, after)
            assert_run(fixture, {2})

    def test_sequence_extension_change_fails(self) -> None:
        with Fixture(with_top=True, packs=True, case="check2 pair extension") as fixture:
            before = _pack_entries(fixture.pack_before)
            after = _pack_entries(fixture.pack_after)
            before.append(_new_entry("SEQ_EXT", "DAT", b"same bytes"))
            after.append(_new_entry("SEQ_EXT", "BIN", b"same bytes"))
            _write_pack_entries(fixture.pack_before, before)
            _write_pack_entries(fixture.pack_after, after)
            assert_run(fixture, {2})

    def test_non_r_payload_must_remain_byte_identical(self) -> None:
        with Fixture(with_top=True, packs=True, case="check2 outside bytes") as fixture:
            before = _pack_entries(fixture.pack_before)
            after = _pack_entries(fixture.pack_after)
            before.append(_new_entry("OUTSIDE_BYTES", "DAT", b"old bytes"))
            after.append(_new_entry("OUTSIDE_BYTES", "DAT", b"changed bytes"))
            _write_pack_entries(fixture.pack_before, before)
            _write_pack_entries(fixture.pack_after, after)
            assert_run(fixture, {2})

    def test_missing_unit_derived_r_entry_fails_even_if_absent_in_both_packs(self) -> None:
        with Fixture(with_top=True, packs=True, case="check2 missing R") as fixture:
            missing = _r_names(fixture)[0]
            before = [entry for entry in _pack_entries(fixture.pack_before) if entry.name != missing]
            after = [entry for entry in _pack_entries(fixture.pack_after) if entry.name != missing]
            _write_pack_entries(fixture.pack_before, before)
            _write_pack_entries(fixture.pack_after, after)
            assert_run(fixture, {2})

    def test_r_payload_must_equal_assigned_atlas_png_bytes(self) -> None:
        for name in Fixture._entry_names(True):
            with self.subTest(name=name), Fixture(with_top=True, packs=True, case=f"check2 R bytes {name}") as fixture:
                before = _pack_entries(fixture.pack_before)
                after = _pack_entries(fixture.pack_after)
                index = next(i for i, entry in enumerate(after) if entry.name == name)
                entry = after[index]
                after[index] = PackEntry(entry.index, entry.name, entry.extension, entry.payload + b"x")
                _write_pack_entries(fixture.pack_before, before)
                _write_pack_entries(fixture.pack_after, after)
                assert_run(fixture, {2})

    def test_each_exact_house_variant_pattern_is_rejected_for_body_and_top(self) -> None:
        for target in ("UNIT_SYNTH_BODY", "UNIT_SYNTH_TOP"):
            for prefix in ("HV_RED_", "HOUSEVARIANT_RED_"):
                name = prefix + target
                with self.subTest(name=name), Fixture(with_top=True, packs=True, case=f"check2 forbidden {name}") as fixture:
                    self.assertIn(target, _atlas_names(fixture))
                    self._append_same_entry(fixture, name, b"variant", "PNG")
                    assert_run(fixture, {2})

    def test_fullmatch_and_case_sensitive_near_matches_pass(self) -> None:
        with Fixture(with_top=True, packs=True, case="check2 variant near matches") as fixture:
            candidates = set()
            for target in ("UNIT_SYNTH_BODY", "UNIT_SYNTH_TOP"):
                self.assertIn(target, _atlas_names(fixture))
                for family in ("HV", "HOUSEVARIANT"):
                    exact = f"{family}_RED_{target}"
                    candidates.update(
                        {
                            "X" + exact,
                            exact + "_X",
                            f"{family}_RED_{target}X",
                            f"{family}_RED_BLUE_{target}",
                            f"{family}__{target}",
                            f"{family.lower()}_RED_{target}",
                            f"{family}_RED_{target.lower()}",
                        }
                    )
            for name in sorted(candidates):
                self._append_same_entry(fixture, name, b"near match", "PNG")
            assert_run(fixture)

    def test_optional_pack_arguments_and_allow_skip_control_exit(self) -> None:
        with Fixture(with_top=True, packs=True, case="check2 no pack skip") as fixture:
            assert_run(fixture, expected_skip_set={2}, use_fixture_packs=False)
        with Fixture(with_top=True, packs=True, case="check2 allowed skip") as fixture:
            assert_run(
                fixture,
                extra_args=("--allow-skip", "2"),
                expected_skip_set={2},
                use_fixture_packs=False,
            )

    def test_each_single_pack_argument_is_argument_error(self) -> None:
        with Fixture(with_top=True, packs=True, case="check2 one pack argument") as fixture:
            for args in (
                ("--pack-before", str(fixture.pack_before)),
                ("--pack-after", str(fixture.pack_after)),
            ):
                with self.subTest(args=args):
                    result = run_checker(fixture, extra_args=args)
                    print(f"{fixture.case}: only one pack path; exit={result.exit_code}")
                    self.assertEqual(result.exit_code, 2)
                    self.assertEqual(result.statuses, {})

    def test_allow_skip_accepts_only_value_2(self) -> None:
        with Fixture(with_top=True, packs=True, case="check2 invalid allow-skip") as fixture:
            for value in ("1", "3"):
                with self.subTest(value=value):
                    result = run_checker(fixture, extra_args=("--allow-skip", value))
                    print(f"{fixture.case}: --allow-skip {value}; exit={result.exit_code}")
                    self.assertEqual(result.exit_code, 2)
                    self.assertEqual(result.statuses, {})

    def test_allow_skip_with_pack_pair_runs_check_2_instead_of_skipping(self) -> None:
        with Fixture(with_top=True, packs=True, case="check2 bad pack with allow-skip") as fixture:
            fixture.pack_after.write_bytes(b"not a D2TM pack")
            assert_run(fixture, {2}, extra_args=("--allow-skip", "2"))

    def test_missing_before_and_after_pack_files_fail_only_check_2(self) -> None:
        for missing in ("before", "after"):
            with self.subTest(missing=missing), Fixture(with_top=True, packs=True, case=f"check2 missing {missing} pack") as fixture:
                (fixture.pack_before if missing == "before" else fixture.pack_after).unlink()
                assert_run(fixture, {2})

    def test_corrupt_before_and_after_pack_headers_fail_only_check_2(self) -> None:
        for damaged in ("before", "after"):
            with self.subTest(damaged=damaged), Fixture(with_top=True, packs=True, case=f"check2 corrupt {damaged} pack") as fixture:
                (fixture.pack_before if damaged == "before" else fixture.pack_after).write_bytes(b"not a D2TM pack")
                assert_run(fixture, {2})


class AlphaConnectivityTests(DirectionMarkerHelpers, unittest.TestCase):
    def test_alpha_7_nonblack_atlas_fails_7_and_10(self) -> None:
        for part in ("body", "top"):
            for k in (0, 7, 3):
                with self.subTest(part=part, k=k), Fixture(
                    with_top=True, case=f"alpha7 nonblack {part} k={k}",
                ) as fixture:
                    name = fixture.unit_data["parts"][part]["atlas"]
                    frame = fixture.atlas_frames[name][k].copy()
                    frame[0, 0] = (1, 0, 0, 7)
                    fixture.set_frame(name, k, frame)
                    fixture.commit()
                    assert_run(fixture, {7, 10})

    @staticmethod
    def _body_rect_points() -> set[tuple[int, int]]:
        return {(x, y) for y in range(59, 69) for x in range(14, 114)}

    def _run_body_shape(
        self,
        case: str,
        opaque_points: set[tuple[int, int]],
        expected_fail: Iterable[int],
        *,
        max_holes: int = 0,
        mask_count: int = 200,
        frame_k: int = 0,
    ) -> None:
        with Fixture(with_top=False, packs=True, case=case, supersample=1) as fixture:
            fixture.camera_data["elevation_deg"] = 30.0
            fixture.manifest_data["elevation_deg"] = 30.0
            fixture.unit_data["max_holes"] = max_holes
            fixture.unit_data["mask_share"] = [0.08, 0.35]
            self._install_direction_markers(fixture, 30.0)
            ordered = sorted(opaque_points, key=lambda point: (point[1], point[0]))
            color = np.zeros_like(fixture.render_frames[("body", "color")][frame_k])
            for x, y in ordered:
                color[y, x] = (100, 120, 140, 255)
            mask = np.zeros_like(fixture.render_frames[("body", "mask")][frame_k])
            for x, y in ordered[:mask_count]:
                mask[y, x] = (255, 255, 255, 255)
            fixture.set_render_frame("body", "color", frame_k, color, sync_atlas=True)
            fixture.set_render_frame("body", "mask", frame_k, mask, sync_atlas=True)
            fixture.manifest_data["bbox_hd4"]["body"][str(frame_k)] = [14.0, 59.0, 114.0, 69.0]
            fixture.commit(update_hashes=True, update_packs=True)
            assert_run(fixture, expected_fail_set=set(expected_fail))

    def test_alpha_below_8_nonblack_fails_7_and_10_for_each_resource_and_column(self) -> None:
        with Fixture(with_top=True, case="alpha below 8 target names") as probe:
            entries = [(part, kind, probe.unit_data["parts"][part][kind])
                       for part in ("body", "top") for kind in ("atlas", "mask")]
            entries.append(("body", "shadow", probe.unit_data["parts"]["body"]["shadow"]))
        for part, kind, name in entries:
            for k in (0, 7, 3):
                for channel, component in enumerate("RGB"):
                    with self.subTest(part=part, kind=kind, k=k, component=component), Fixture(
                        with_top=True,
                        case=f"alpha below 8 {part}/{kind} k={k} {component}",
                    ) as fixture:
                        rgba = fixture.atlas_frames[name][k].copy()
                        rgba[0, 0] = (0, 0, 0, 0)
                        rgba[0, 0, channel] = 1
                        fixture.set_frame(name, k, rgba)
                        fixture.commit(update_hashes=True, update_packs=True)
                        assert_run(fixture, expected_fail_set={7, 10})

    def test_alpha_7_black_is_pass_7_but_not_canonical(self) -> None:
        with Fixture(with_top=True, case="alpha7 black final pixel") as fixture:
            name = fixture.unit_data["parts"]["body"]["atlas"]
            rgba = fixture.atlas_frames[name][0].copy()
            rgba[0, 0] = (0, 0, 0, 7)
            fixture.set_frame(name, 0, rgba)
            fixture.commit()
            assert_run(fixture, expected_fail_set={10})

    def test_alpha_8_values_are_canonical_for_each_resource_and_column(self) -> None:
        with Fixture(with_top=True, case="alpha8 resource targets") as probe:
            entries = [(part, kind, probe.unit_data["parts"][part][kind])
                       for part in ("body", "top") for kind in ("atlas", "mask")]
            entries.append(("body", "shadow", probe.unit_data["parts"]["body"]["shadow"]))
        for part, kind, name in entries:
            for k in (0, 7, 3):
                with self.subTest(part=part, kind=kind, k=k), Fixture(
                    with_top=True,
                    case=f"alpha8 canonical {part}/{kind} k={k}",
                ) as fixture:
                    if kind == "atlas":
                        frame = fixture.render_frames[(part, "color")][k].copy()
                        frame[0, 0] = (255, 255, 255, 8)
                        fixture.set_render_frame(part, "color", k, frame, sync_atlas=True)
                    elif kind == "mask":
                        color = fixture.render_frames[(part, "color")][k]
                        y, x = np.argwhere(color[:, :, 3] > 16)[0]
                        frame = fixture.render_frames[(part, "mask")][k].copy()
                        frame[y, x] = (255, 255, 255, 8)
                        fixture.unit_data["mask_share"] = [0.08, 0.35]
                        fixture.set_render_frame(part, "mask", k, frame, sync_atlas=True)
                    else:
                        frame = fixture.render_frames[("body", "shadow")][k].copy()
                        frame[58, 125] = (0, 0, 0, 40)
                        fixture.set_render_frame("body", "shadow", k, frame, sync_atlas=True)
                    fixture.commit(update_hashes=True, update_packs=True)
                    assert_run(fixture)

    def test_shadow_alpha_7_after_normalization_is_canonical(self) -> None:
        with Fixture(with_top=False, case="shadow alpha 7 after normalization") as fixture:
            for k in range(8):
                frame = np.zeros_like(fixture.render_frames[("body", "shadow")][k])
                frame[59:69, 115:125] = (0, 0, 0, 255)
                if k == 0:
                    frame[58, 125] = (0, 0, 0, 35)
                fixture.set_render_frame("body", "shadow", k, frame, sync_atlas=True)
            fixture.commit(update_hashes=True, update_packs=True)
            assert_run(fixture)

    def test_diagonal_contact_is_one_eight_connected_component(self) -> None:
        left = {(x, y) for y in range(59, 64) for x in range(14, 64)}
        right = {(x, y) for y in range(64, 69) for x in range(64, 114)}
        self._run_body_shape("body diagonal 8-connected", left | right, set(), mask_count=100)

    def test_two_components_fail_only_check_7_for_columns_zero_seven_and_internal(self) -> None:
        left = {(x, y) for y in range(59, 64) for x in range(14, 64)}
        right = {(x, y) for y in range(64, 69) for x in range(65, 114)}
        for k in (0, 7, 3):
            with self.subTest(k=k):
                self._run_body_shape(f"body two components k={k}", left | right, {7}, frame_k=k, mask_count=100)

    def test_internal_holes_obey_max_holes_boundary(self) -> None:
        body = self._body_rect_points()
        for k in (0, 7, 3):
            with self.subTest(k=k):
                self._run_body_shape(f"one hole max holes one k={k}", body - {(50, 63)}, set(), max_holes=1, frame_k=k)
                self._run_body_shape(f"one hole max holes zero k={k}", body - {(50, 63)}, {7}, max_holes=0, frame_k=k)
                self._run_body_shape(f"two holes max holes one k={k}", body - {(50, 63), (54, 63)}, {7}, max_holes=1, frame_k=k)

    def test_edge_connected_transparency_is_not_an_internal_hole(self) -> None:
        body = self._body_rect_points() - {(50, 59)}
        self._run_body_shape("edge-connected void", body, set(), max_holes=0)

    def test_four_connected_diagonal_hole_is_counted(self) -> None:
        upper = {(x, y) for y in range(59, 63) for x in range(50, 114)}
        lower = {(x, y) for y in range(63, 69) for x in range(14, 114)}
        opening = (upper | lower) - {(50, 63)}
        self._run_body_shape("diagonal opening max holes zero", opening, {7}, max_holes=0, mask_count=171)
        self._run_body_shape("diagonal opening max holes one", opening, set(), max_holes=1, mask_count=171)


class MaskCheckTests(DirectionMarkerHelpers, unittest.TestCase):
    def test_mask_support_uses_alpha_16_and_17_boundary(self) -> None:
        for part in ("body", "top"):
            for k in (0, 7, 3):
                for alpha in (16, 17):
                    with self.subTest(part=part, k=k, alpha=alpha), Fixture(
                        with_top=True, case=f"mask support {part} alpha={alpha} k={k}",
                    ) as fixture:
                        fixture.unit_data["mask_share"] = [0.08, 0.35]
                        source = fixture.render_frames[(part, "color")][k].copy()
                        mask_name = fixture.unit_data["parts"][part]["mask"]
                        y, x = np.argwhere(fixture.atlas_frames[mask_name][k, ..., 3] == 255)[0]
                        source[y, x, 3] = alpha
                        fixture.set_render_frame(part, "color", k, source)
                        fixture.commit(sync_atlas=True)
                        mask = fixture.atlas_frames[mask_name][k].copy()
                        mask[y, x] = (255, 255, 255, 255)
                        fixture.set_frame(mask_name, k, mask)
                        fixture.commit()
                        assert_run(fixture, {8, 10} if alpha == 16 else set())

    @staticmethod
    def _mask_rect_points() -> list[tuple[int, int]]:
        return [(x, y) for y in range(59, 69) for x in range(14, 114)]

    def _mask_bbox_sample_points(self) -> list[tuple[int, int]]:
        points = self._mask_rect_points()
        corners = [(14, 59), (113, 59), (14, 68), (113, 68)]
        corner_set = set(corners)
        return corners + [point for point in points if point not in corner_set]

    def _set_mask_case_frame(
        self,
        fixture: Fixture,
        part: str,
        k: int,
        alphas: list[int],
        *,
        nonwhite_channel: int | None = None,
        remove_color_corner: bool = False,
    ) -> None:
        color = np.zeros_like(fixture.render_frames[(part, "color")][k])
        for x, y in self._mask_rect_points():
            if remove_color_corner and (x, y) == (14, 59):
                continue
            color[y, x] = (100, 120, 140, 255)
        fixture.set_render_frame(part, "color", k, color, sync_atlas=True)
        fixture.manifest_data["bbox_hd4"][part][str(k)] = [14.0, 59.0, 114.0, 69.0]
        mask = np.zeros_like(fixture.render_frames[(part, "mask")][k])
        for i, ((x, y), alpha) in enumerate(zip(self._mask_bbox_sample_points(), alphas)):
            rgb = [255, 255, 255]
            if nonwhite_channel is not None and i == 0:
                rgb[nonwhite_channel] = 254
            mask[y, x] = (*rgb, alpha)
        fixture.set_render_frame(part, "mask", k, mask, sync_atlas=True)

    def _mask_case_cli(
        self,
        case: str,
        part: str,
        k: int,
        alphas: list[int],
        expected_fail: Iterable[int],
        *,
        nonwhite_channel: int | None = None,
        outside_final: bool = False,
        edge_alpha16_final: bool = False,
    ) -> RunResult:
        with Fixture(with_top=True, case=case, supersample=1) as fixture:
            fixture.camera_data["elevation_deg"] = 30.0
            fixture.manifest_data["elevation_deg"] = 30.0
            fixture.unit_data["mask_share"] = [0.08, 0.35]
            self._install_direction_markers(fixture, 30.0)
            self._set_mask_case_frame(
                fixture,
                part,
                k,
                alphas,
                nonwhite_channel=nonwhite_channel,
                remove_color_corner=outside_final,
            )
            fixture.commit(update_hashes=True, update_packs=True)
            if outside_final or edge_alpha16_final:
                name = fixture.unit_data["parts"][part]["mask"]
                rgba = fixture.atlas_frames[name][k].copy()
                if outside_final:
                    rgba[59, 14] = (255, 255, 255, 255)
                if edge_alpha16_final:
                    rgba[0, 0] = (255, 255, 255, 16)
                fixture.set_frame(name, k, rgba)
                fixture.commit(update_hashes=True, update_packs=True)
            return assert_run(fixture, expected_fail_set=set(expected_fail))

    def test_mask_is_white_or_fails_for_body_top_and_boundary_columns(self) -> None:
        for part in ("body", "top"):
            for k in (0, 7, 3):
                with self.subTest(part=part, k=k, color="white"):
                    self._mask_case_cli(f"mask white {part} k={k}", part, k, [255] * 200, set())
                for channel, component in enumerate("RGB"):
                    with self.subTest(part=part, k=k, component=component):
                        self._mask_case_cli(
                            f"mask nonwhite {component} {part} k={k}",
                            part,
                            k,
                            [255] * 200,
                            {8},
                            nonwhite_channel=channel,
                        )

    def test_mask_share_inclusive_and_exclusive_boundaries(self) -> None:
        cases = (
            ("lower 0.08", [255] * 80, set()),
            ("upper 0.35", [255] * 350, set()),
            ("below 0.08 at 0.079", [255] * 79, {8}),
            ("above 0.35", [255] * 351, {8}),
            ("fractional exactly 0.08", [255] * 79 + [128, 127], set()),
        )
        for part in ("body", "top"):
            for k in (0, 7, 3):
                for label, alphas, expected in cases:
                    with self.subTest(part=part, k=k, case=label):
                        self._mask_case_cli(f"mask share {label} {part} k={k}", part, k, alphas, expected)

    def test_mask_strong_pixel_threshold_is_253(self) -> None:
        for part in ("body", "top"):
            for k in (0, 7, 3):
                for alpha, expected in ((253, set()), (252, {8})):
                    with self.subTest(part=part, k=k, alpha=alpha):
                        self._mask_case_cli(
                            f"mask strong alpha {alpha} {part} k={k}",
                            part,
                            k,
                            [alpha] * 200,
                            expected,
                        )

    def test_mask_must_belong_to_its_own_body_or_top_atlas(self) -> None:
        for part in ("body", "top"):
            for k in (0, 7, 3):
                with self.subTest(part=part, k=k):
                    self._mask_case_cli(
                        f"mask outside own {part} atlas k={k}",
                        part,
                        k,
                        [255] * 200,
                        {8, 10},
                        outside_final=True,
                    )

    def test_alpha16_mask_at_outer_edge_fails_mask_and_provenance_not_margin(self) -> None:
        for part in ("body", "top"):
            for k in (0, 7, 3):
                with self.subTest(part=part, k=k):
                    result = self._mask_case_cli(
                        f"mask alpha16 outer edge {part} k={k}",
                        part,
                        k,
                        [255] * 200,
                        {8, 10},
                        edge_alpha16_final=True,
                    )
                    self.assertEqual(result.statuses[5], "PASS")


class ShadowCheckTests(DirectionMarkerHelpers, unittest.TestCase):
    @staticmethod
    def _shadow_rgba(points: Iterable[tuple[int, int]] = (), alpha: int = 255) -> np.ndarray:
        rgba = np.zeros((FRAME_SIZE[1], FRAME_SIZE[0], 4), dtype=np.uint8)
        for x, y in points:
            rgba[y, x] = (0, 0, 0, alpha)
        return rgba

    def _set_render_shadow(self, fixture: Fixture, k: int, points: Iterable[tuple[int, int]], alpha: int = 255) -> None:
        fixture.set_render_frame(
            "body", "shadow", k, self._shadow_rgba(points, alpha), sync_atlas=True
        )

    def _set_centroid_geometry(
        self,
        fixture: Fixture,
        k: int,
        *,
        body_alpha: int,
        top_alpha: int,
        shadow_pixels: Iterable[tuple[int, int, int]],
    ) -> None:
        body_color = np.zeros_like(fixture.render_frames[("body", "color")][k])
        body_color[54:74, 75:125] = (72, 57, 41, body_alpha)
        fixture.set_render_frame("body", "color", k, body_color, sync_atlas=True)
        body_mask = np.zeros_like(fixture.render_frames[("body", "mask")][k])
        body_mask[54:74, 75:85] = (255, 255, 255, 255)
        fixture.set_render_frame("body", "mask", k, body_mask, sync_atlas=True)
        top_color = np.zeros_like(fixture.render_frames[("top", "color")][k])
        top_color[2:7, 54:74] = (91, 75, 54, top_alpha)
        fixture.set_render_frame("top", "color", k, top_color, sync_atlas=True)
        top_mask = np.zeros_like(fixture.render_frames[("top", "mask")][k])
        top_mask[2:7, 54:58] = (255, 255, 255, 255)
        fixture.set_render_frame("top", "mask", k, top_mask, sync_atlas=True)
        fixture.manifest_data["bbox_hd4"]["body"][str(k)] = [75, 54, 125, 74]
        fixture.manifest_data["bbox_hd4"]["top"][str(k)] = [54, 2, 74, 7]
        shadow = np.zeros_like(fixture.render_frames[("body", "shadow")][k])
        for x, y, alpha in shadow_pixels:
            shadow[y, x] = (0, 0, 0, alpha)
        fixture.set_render_frame("body", "shadow", k, shadow, sync_atlas=True)

    @staticmethod
    def _angle_pixels(label: str) -> list[tuple[int, int]]:
        if label == "10":
            return [(x, y) for y in (52, 54, 55) for x in range(115, 125)]
        if label == "11":
            return [(x, y) for y in (51, 53, 54) for x in range(115, 125)]
        if label == "20":
            return (
                [(x, 42) for x in range(116, 124)]
                + [(x, y) for y in (43, 44) for x in range(115, 125)]
                + [(x, 45) for x in (119, 120)]
            )
        if label == "21":
            return [(x, y) for y in (41, 42, 43) for x in range(115, 125)]
        if label == "minus5":
            return (
                [(x, 67) for x in range(115, 125)]
                + [(x, 68) for x in range(118, 122)]
                + [(x, 69) for x in range(115, 125)]
                + [(x, 70) for x in range(117, 123)]
            )
        if label == "plus15":
            return (
                [(x, 47) for x in range(117, 122)]
                + [(x, y) for y in (48, 49) for x in range(115, 125)]
                + [(x, 50) for x in range(118, 123)]
            )
        return [(x, y) for y in range(59, 69) for x in range(115, 125)]

    def _shadow_cli(
        self,
        case: str,
        expected_fail: Iterable[int],
        per_frame=None,
    ) -> RunResult:
        with Fixture(with_top=True, case=case) as fixture:
            fixture.contract_data["light"]["median_angle_degrees"] = 0.0
            for k in range(8):
                label = per_frame(k) if per_frame else "0"
                self._set_render_shadow(fixture, k, self._angle_pixels(label))
            fixture.commit()
            return assert_run(fixture, expected_fail_set=set(expected_fail))

    def test_shadow_angle_median_10_is_inclusive(self) -> None:
        self._shadow_cli("shadow median angle 10", set(), lambda k: "10")

    def test_shadow_angle_median_11_fails_only_check_9(self) -> None:
        self._shadow_cli("shadow median angle 11", {9}, lambda k: "11")

    def test_shadow_single_frame_angle_20_is_inclusive(self) -> None:
        for k in (0, 7, 3):
            with self.subTest(k=k):
                self._shadow_cli(
                    f"shadow single frame angle 20 k={k}",
                    set(),
                    lambda frame_k, target=k: "20" if frame_k == target else "0",
                )

    def test_shadow_single_frame_angle_21_fails_only_check_9(self) -> None:
        for k in (0, 7, 3):
            with self.subTest(k=k):
                self._shadow_cli(
                    f"shadow single frame angle 21 k={k}",
                    {9},
                    lambda frame_k, target=k: "21" if frame_k == target else "0",
                )

    def test_shadow_circular_median_tie_uses_lower_column(self) -> None:
        self._shadow_cli(
            "shadow circular median tie",
            set(),
            lambda k: "minus5" if k < 4 else "plus15",
        )

    def test_shadow_circular_median_reverse_tie_uses_lower_column(self) -> None:
        self._shadow_cli(
            "shadow circular median reverse tie",
            {9},
            lambda k: "plus15" if k < 4 else "minus5",
        )

    def test_shadow_alpha_49_passes_and_48_fails_only_check_9(self) -> None:
        for k in (0, 7, 3):
            for raw_alpha, expected in ((245, set()), (240, {9})):
                with self.subTest(k=k, raw_alpha=raw_alpha), Fixture(
                    with_top=True,
                    case=f"shadow alpha boundary {raw_alpha} k={k}",
                ) as fixture:
                    fixture.contract_data["light"]["median_angle_degrees"] = 0.0
                    for frame_k in range(8):
                        points = self._angle_pixels("0")
                        alpha = raw_alpha if frame_k == k else 255
                        self._set_render_shadow(fixture, frame_k, points, alpha)
                    fixture.commit()
                    assert_run(fixture, expected_fail_set=expected)

    def test_shadow_alpha_54_fails_check_9_and_provenance(self) -> None:
        for k in (0, 7, 3):
            with self.subTest(k=k), Fixture(
                with_top=True,
                case=f"shadow alpha 54 in final atlas k={k}",
            ) as fixture:
                name = fixture.unit_data["parts"]["body"]["shadow"]
                rgba = fixture.atlas_frames[name][k].copy()
                y, x = np.argwhere(rgba[:, :, 3] > 0)[0]
                rgba[y, x, 3] = 54
                fixture.set_frame(name, k, rgba)
                fixture.commit()
                assert_run(fixture, expected_fail_set={9, 10})

    def test_shadow_nonblack_rgb_fails_check_9_and_provenance(self) -> None:
        for k in (0, 7, 3):
            for channel, component in enumerate("RGB"):
                with self.subTest(k=k, channel=component), Fixture(
                    with_top=True,
                    case=f"shadow {component} nonzero under alpha k={k}",
                ) as fixture:
                    name = fixture.unit_data["parts"]["body"]["shadow"]
                    rgba = fixture.atlas_frames[name][k].copy()
                    y, x = np.argwhere(rgba[:, :, 3] > 0)[0]
                    rgba[y, x, channel] = 1
                    fixture.set_frame(name, k, rgba)
                    fixture.commit()
                    assert_run(fixture, expected_fail_set={9, 10})

    def test_one_empty_shadow_frame_fails_only_check_9(self) -> None:
        for k in (0, 7, 3):
            with self.subTest(k=k), Fixture(
                with_top=True,
                case=f"shadow one empty frame k={k}",
            ) as fixture:
                self._set_render_shadow(fixture, k, ())
                fixture.commit()
                assert_run(fixture, expected_fail_set={9})

    def test_all_empty_shadow_frames_fail_check_9_and_10(self) -> None:
        with Fixture(with_top=True, case="shadow all frames empty") as fixture:
            for k in range(8):
                self._set_render_shadow(fixture, k, ())
            fixture.commit()
            assert_run(fixture, expected_fail_set={9, 10})

    def test_shadow_without_exposed_pixels_fails_only_check_9(self) -> None:
        for k in (0, 7, 3):
            with self.subTest(k=k), Fixture(
                with_top=True,
                case=f"shadow all pixels covered k={k}",
            ) as fixture:
                self._set_render_shadow(fixture, k, [(63, 63)])
                fixture.commit()
                assert_run(fixture, expected_fail_set={9})

    def test_exposed_shadow_threshold_is_strictly_above_16(self) -> None:
        for k in (0, 7, 3):
            for raw_alpha, expected in ((85, set()), (80, {9})):
                with self.subTest(k=k, raw_alpha=raw_alpha), Fixture(
                    with_top=True, case=f"shadow exposed alpha {raw_alpha / 5:g} k={k}",
                ) as fixture:
                    frame = np.zeros_like(fixture.render_frames[("body", "shadow")][k])
                    frame[63, 63] = (0, 0, 0, 255)
                    frame[63, 120] = (0, 0, 0, raw_alpha)
                    fixture.set_render_frame("body", "shadow", k, frame, sync_atlas=True)
                    fixture.commit()
                    assert_run(fixture, expected)

    def test_shadow_unit_union_uses_alpha_above_16_for_each_part(self) -> None:
        for part in ("body", "top"):
            for k in (0, 7, 3):
                for alpha, expected in ((16, set()), (17, {9})):
                    with self.subTest(part=part, k=k, alpha=alpha), Fixture(
                        with_top=True, case=f"shadow union {part} alpha={alpha} k={k}",
                    ) as fixture:
                        fixture.unit_data["mask_share"] = [0.0, 1.0]
                        frame = fixture.render_frames[(part, "color")][k].copy()
                        frame[2:59, 80:110] = (72, 57, 41, alpha)
                        fixture.set_render_frame(part, "color", k, frame, sync_atlas=True)
                        if alpha == 17:
                            fixture.manifest_data["bbox_hd4"][part][str(k)] = (
                                [14, 2, 114, 69] if part == "body" else [54, 2, 110, 66]
                            )
                        fixture.commit()
                        assert_run(fixture, expected)

    def test_shadow_zero_vector_fails_only_check_9(self) -> None:
        for k in (0, 7, 3):
            with self.subTest(k=k), Fixture(
                with_top=True,
                case=f"shadow zero vector k={k}",
            ) as fixture:
                points = [(x, y) for x in (13, 114) for y in (63, 64)]
                self._set_render_shadow(fixture, k, points)
                fixture.commit()
                assert_run(fixture, expected_fail_set={9})

    def test_shadow_centroid_excludes_body_and_top_pixels(self) -> None:
        for k in (0, 7, 3):
            with self.subTest(k=k), Fixture(
                with_top=True,
                case=f"shadow union excludes covered body and top pixels k={k}",
            ) as fixture:
                top_color = fixture.render_frames[("top", "color")][k]
                x0, y0, _, _ = _opaque_bounds(top_color)
                dx, dy = 9 - x0, 2 - y0
                moved_color = _translate_rgba(top_color, dx, dy)
                fixture.set_render_frame("top", "color", k, moved_color, sync_atlas=True)
                top_mask = fixture.render_frames[("top", "mask")][k]
                fixture.set_render_frame("top", "mask", k, _translate_rgba(top_mask, dx, dy), sync_atlas=True)
                _set_bbox_shift(fixture, "top", k, dx, dy)
                self._set_render_shadow(fixture, k, [(10, 2), (14, 59), (115, 63)])
                fixture.commit()
                assert_run(fixture)

    def test_shadow_centroids_use_unweighted_pixels_for_s_and_union(self) -> None:
        with Fixture(with_top=True, case="shadow binary centroids despite varied alpha") as fixture:
            self._set_centroid_geometry(
                fixture,
                3,
                body_alpha=17,
                top_alpha=255,
                shadow_pixels=((125, 40, 83), (125, 87, 255)),
            )
            fixture.commit()
            assert_run(fixture)

    def test_shadow_unweighted_s_centroid_violation_fails_only_check_9(self) -> None:
        with Fixture(with_top=True, case="shadow unweighted S centroid violation") as fixture:
            self._set_centroid_geometry(
                fixture,
                3,
                body_alpha=255,
                top_alpha=255,
                shadow_pixels=((125, 40, 255), (125, 105, 83)),
            )
            fixture.commit()
            assert_run(fixture, expected_fail_set={9})

    def test_shadow_unweighted_union_centroid_violation_fails_only_check_9(self) -> None:
        with Fixture(with_top=True, case="shadow unweighted union centroid violation") as fixture:
            self._set_centroid_geometry(
                fixture,
                3,
                body_alpha=17,
                top_alpha=255,
                shadow_pixels=((125, 30, 255),),
            )
            fixture.commit()
            assert_run(fixture, expected_fail_set={9})

    def test_shadow_direct_alpha_53_and_54_boundaries(self) -> None:
        from tools.units3d.check_unit import check_shadow_frame

        union = np.zeros(FRAME_SIZE[::-1], dtype=bool)
        union[64, 64] = True
        for alpha, raises in ((53, False), (54, True)):
            with self.subTest(alpha=alpha):
                frame = np.zeros((FRAME_SIZE[1], FRAME_SIZE[0], 4), dtype=np.uint8)
                frame[64, 100] = (0, 0, 0, alpha)
                if raises:
                    with self.assertRaises(ValueError) as error:
                        check_shadow_frame(frame, union)
                    print(f"check9 direct alpha={alpha}: FAIL 9; {error.exception}")
                else:
                    angle = check_shadow_frame(frame, union)
                    self.assertTrue(math.isfinite(angle))
                    print(f"check9 direct alpha={alpha}: PASS 9; angle={angle:.6f}")

    def test_shadow_float32_numpy_round_order_and_ties_to_even(self) -> None:
        samples = (
            (102, {(119, 63): 9, (120, 63): 11, (119, 64): 13, (120, 64): 15},
             {(119, 63): 4, (120, 63): 6, (119, 64): 6, (120, 64): 8}),
            (170, {(119, 63): 95}, {(119, 63): 28}),
            (194, {(119, 63): 97}, {(119, 63): 26}),
        )
        for peak, raw_pixels, expected_alpha in samples:
            with self.subTest(peak=peak), Fixture(
                with_top=False,
                case=f"shadow normalization peak {peak}",
            ) as fixture:
                name = fixture.unit_data["parts"]["body"]["shadow"]
                for k in range(8):
                    rgba = np.zeros_like(fixture.render_frames[("body", "shadow")][k])
                    rgba[59:69, 115:125] = (0, 0, 0, peak)
                    if k == 0:
                        for (x, y), raw_alpha in raw_pixels.items():
                            rgba[y, x] = (0, 0, 0, raw_alpha)
                    fixture.set_render_frame("body", "shadow", k, rgba, sync_atlas=True)
                fixture.commit(update_hashes=True, update_packs=True)
                assert_run(fixture)
                filename = fixture.atlases_data["entries"][name]["file"]
                with Image.open(fixture.atlases_dir / filename) as image:
                    atlas = np.asarray(image)
                for (x, y), alpha in expected_alpha.items():
                    self.assertEqual(int(atlas[y, x, 3]), alpha)


class InputReadFailureTests(unittest.TestCase):
    JSON_SOURCES = (
        ("unit.json", "unit_path", set(range(1, 11))),
        ("contract", "contract_path", {1, 3, 6, 9, 10}),
        ("camera.json", "camera_path", {3, 6, 10}),
        ("light.json", "light_path", {10}),
        ("render.json", "render_json_path", {10}),
        ("render_manifest.json", "render_manifest_path", {1, 3, 6, 10}),
        ("atlases.json", "atlases_json_path", {1, 2, 10}),
    )

    def _damage_json(self, path: Path, damage: str) -> None:
        if damage == "missing":
            path.unlink()
        elif damage == "invalid JSON":
            path.write_text("{", encoding="utf-8")
        elif damage == "duplicate key":
            payload = path.read_text(encoding="utf-8")
            path.write_text('{"duplicate": 1, "duplicate": 2,' + payload[1:], encoding="utf-8")
        else:
            raise AssertionError(damage)

    def _set_nonfinite(self, fixture: Fixture, source: str, value: float) -> None:
        if source == "unit.json":
            fixture.unit_data["length_m"] = value
            _write_json(fixture.unit_path, fixture.unit_data)
        elif source == "contract":
            fixture.contract_data["light"]["median_angle_degrees"] = value
            _write_json(fixture.contract_path, fixture.contract_data)
        elif source == "camera.json":
            fixture.camera_data["elevation_deg"] = value
            _write_json(fixture.camera_path, fixture.camera_data)
        elif source == "light.json":
            fixture.light_data["sun_azimuth_deg"] = value
            _write_json(fixture.light_path, fixture.light_data)
        elif source == "render.json":
            fixture.render_json_data["samples"] = value
            _write_json(fixture.render_json_path, fixture.render_json_data)
        elif source == "render_manifest.json":
            fixture.manifest_data["bbox_hd4"]["body"]["0"][0] = value
            _write_json(fixture.render_manifest_path, fixture.manifest_data)
        elif source == "atlases.json":
            fixture.atlases_data["entries"]["UNIT_SYNTH_BODY"]["size"][0] = value
            _write_json(fixture.atlases_json_path, fixture.atlases_data)
        else:
            raise AssertionError(source)

    @staticmethod
    def _refresh_json_hashes(fixture: Fixture, source: str) -> None:
        hash_key = {
            "unit.json": "unit.json",
            "camera.json": "camera.json",
            "light.json": "light.json",
            "render.json": "render.json",
        }.get(source)
        if hash_key is not None:
            path = getattr(fixture, {
                "unit.json": "unit_path",
                "camera.json": "camera_path",
                "light.json": "light_path",
                "render.json": "render_json_path",
            }[source])
            digest = _sha(path.read_bytes())
            fixture.manifest_data["hashes"][hash_key] = digest
            fixture.atlases_data["hashes"][hash_key] = digest
            _write_json(fixture.render_manifest_path, fixture.manifest_data)
            fixture.atlases_data["hashes"]["render_manifest.json"] = _sha(fixture.render_manifest_path.read_bytes())
            _write_json(fixture.atlases_json_path, fixture.atlases_data)
        elif source == "render_manifest.json":
            fixture.atlases_data["hashes"]["render_manifest.json"] = _sha(fixture.render_manifest_path.read_bytes())
            _write_json(fixture.atlases_json_path, fixture.atlases_data)

    @staticmethod
    def _sync_atlas_png_input(fixture: Fixture, name: str) -> None:
        path = fixture.atlases_dir / fixture.entry_files[name]
        payload = path.read_bytes()
        fixture.atlases_data["entries"][name]["sha256"] = _sha(payload)
        _write_json(fixture.atlases_json_path, fixture.atlases_data)
        after = read_pack(fixture.pack_after)
        write_pack(
            fixture.pack_after,
            [PackEntry(entry.index, entry.name, entry.extension, payload if entry.name == name else entry.payload) for entry in after],
        )

    def test_json_missing_invalid_and_duplicate_keys_fail_every_reader(self) -> None:
        for source, path_attr, readers in self.JSON_SOURCES:
            for damage in ("missing", "invalid JSON", "duplicate key"):
                with self.subTest(source=source, damage=damage), Fixture(case=f"read error {source} {damage}") as fixture:
                    self._damage_json(getattr(fixture, path_attr), damage)
                    if damage != "missing":
                        self._refresh_json_hashes(fixture, source)
                    assert_read_error(fixture, readers)

    def test_nonfinite_json_values_fail_every_reader(self) -> None:
        for source, _, readers in self.JSON_SOURCES:
            for label, value in (("infinity", math.inf), ("NaN", math.nan)):
                with self.subTest(source=source, value=label), Fixture(case=f"read error {label} {source}") as fixture:
                    self._set_nonfinite(fixture, source, value)
                    self._refresh_json_hashes(fixture, source)
                    assert_read_error(fixture, readers)

    def test_non_numeric_json_parameters_fail_their_readers(self) -> None:
        cases = (
            ("unit length", "unit_path", {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}, lambda fx: fx.unit_data.__setitem__("length_m", "100px"), "unit.json"),
            ("contract median", "contract_path", {1, 3, 6, 9, 10}, lambda fx: fx.contract_data["light"].__setitem__("median_angle_degrees", "zero"), "contract"),
            ("camera elevation", "camera_path", {3, 6, 10}, lambda fx: fx.camera_data.__setitem__("elevation_deg", "north"), "camera.json"),
            ("light azimuth", "light_path", {10}, lambda fx: fx.light_data.__setitem__("sun_azimuth_deg", "east"), "light.json"),
            ("render samples", "render_json_path", {10}, lambda fx: fx.render_json_data.__setitem__("samples", "many"), "render.json"),
            ("manifest bbox", "render_manifest_path", {1, 3, 6, 10}, lambda fx: fx.manifest_data["bbox_hd4"]["body"]["0"].__setitem__(0, "14px"), "render_manifest.json"),
            ("atlas size", "atlases_json_path", {1, 2, 10}, lambda fx: fx.atlases_data["entries"]["UNIT_SYNTH_BODY"]["size"].__setitem__(0, "1024px"), "atlases.json"),
        )
        data_names = {
            "unit_path": "unit_data",
            "contract_path": "contract_data",
            "camera_path": "camera_data",
            "light_path": "light_data",
            "render_json_path": "render_json_data",
            "render_manifest_path": "manifest_data",
            "atlases_json_path": "atlases_data",
        }
        for label, path_attr, readers, mutation, source in cases:
            with self.subTest(parameter=label), Fixture(case=f"read error nonnumeric {label}") as fixture:
                mutation(fixture)
                _write_json(getattr(fixture, path_attr), getattr(fixture, data_names[path_attr]))
                self._refresh_json_hashes(fixture, source)
                assert_read_error(fixture, readers)

    def test_missing_required_json_fields_fail_the_readers(self) -> None:
        cases = (
            ("unit parts", "unit_path", {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}, lambda fx: fx.unit_data.pop("parts")),
            ("unit length_m", "unit_path", {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}, lambda fx: fx.unit_data.pop("length_m")),
            ("contract entries", "contract_path", {1, 3, 6, 9, 10}, lambda fx: fx.contract_data.pop("entries")),
            ("contract body record", "contract_path", {1, 3, 6, 9, 10}, lambda fx: fx.contract_data["entries"].pop(0)),
            ("contract light median", "contract_path", {1, 3, 6, 9, 10}, lambda fx: fx.contract_data["light"].pop("median_angle_degrees")),
            ("contract yaw_deg", "contract_path", {1, 3, 6, 9, 10}, lambda fx: fx.contract_data["entries"][0]["column_meaning"][0].pop("yaw_deg")),
            ("camera elevation", "camera_path", {3, 6, 10}, lambda fx: fx.camera_data.pop("elevation_deg")),
            ("camera scale", "camera_path", {3, 6, 10}, lambda fx: fx.camera_data.pop("hd4_px_per_m")),
            ("manifest bbox", "render_manifest_path", {1, 3, 6, 10}, lambda fx: fx.manifest_data.pop("bbox_hd4")),
            ("manifest hashes", "render_manifest_path", {1, 3, 6, 10}, lambda fx: fx.manifest_data.pop("hashes")),
            ("manifest camera hash", "render_manifest_path", {1, 3, 6, 10}, lambda fx: fx.manifest_data["hashes"].pop("camera.json")),
            ("manifest supersample", "render_manifest_path", {1, 3, 6, 10}, lambda fx: fx.manifest_data.pop("supersample")),
            ("manifest directions", "render_manifest_path", {1, 3, 6, 10}, lambda fx: fx.manifest_data.pop("directions")),
            ("atlas entry", "atlases_json_path", {1, 2, 10}, lambda fx: fx.atlases_data["entries"].pop("UNIT_SYNTH_BODY")),
            ("atlas hashes", "atlases_json_path", {1, 2, 10}, lambda fx: fx.atlases_data.pop("hashes")),
            ("atlas camera hash", "atlases_json_path", {1, 2, 10}, lambda fx: fx.atlases_data["hashes"].pop("camera.json")),
            ("atlas entry PNG hash", "atlases_json_path", {1, 2, 10}, lambda fx: fx.atlases_data["entries"]["UNIT_SYNTH_BODY"].pop("sha256")),
            ("atlas entry file", "atlases_json_path", {1, 2, 10}, lambda fx: fx.atlases_data["entries"]["UNIT_SYNTH_BODY"].pop("file")),
            ("atlas entry size", "atlases_json_path", {1, 2, 10}, lambda fx: fx.atlases_data["entries"]["UNIT_SYNTH_BODY"].pop("size")),
        )
        for label, path_attr, readers, mutation in cases:
            with self.subTest(field=label), Fixture(case=f"read error missing field {label}") as fixture:
                mutation(fixture)
                _write_json(getattr(fixture, path_attr), getattr(fixture, {
                    "unit_path": "unit_data",
                    "contract_path": "contract_data",
                    "camera_path": "camera_data",
                    "render_manifest_path": "manifest_data",
                    "atlases_json_path": "atlases_data",
                }[path_attr]))
                source = {
                    "unit_path": "unit.json",
                    "contract_path": "contract",
                    "camera_path": "camera.json",
                    "render_manifest_path": "render_manifest.json",
                    "atlases_json_path": "atlases.json",
                }[path_attr]
                self._refresh_json_hashes(fixture, source)
                assert_read_error(fixture, readers)

    def test_missing_model_file_fails_check_10(self) -> None:
        with Fixture(case="read error missing model") as fixture:
            fixture.model_path.unlink()
            assert_read_error(fixture, {10})

    def test_render_png_missing_corrupt_or_wrong_mode_fails_its_readers(self) -> None:
        resources = (
            ("body", "color", {1, 10}),
            ("body", "mask", {1, 10}),
            ("body", "markers", {1, 3, 4}),
            ("body", "shadow", {1, 10}),
            ("top", "color", {1, 10}),
            ("top", "mask", {1, 10}),
            ("top", "markers", {1, 3, 4}),
        )
        for part, pass_name, readers in resources:
            for k in (0, 7, 3):
                for damage in ("missing", "corrupt", "wrong mode"):
                    with self.subTest(part=part, pass_name=pass_name, k=k, damage=damage), Fixture(
                        with_top=True,
                        case=f"read error render {part}/{pass_name}_{k}.png {damage}",
                    ) as fixture:
                        path = fixture.render_dir / part / f"{pass_name}_{k}.png"
                        self._damage_png(path, damage)
                        assert_read_error(fixture, readers)

    def test_atlas_png_missing_corrupt_or_wrong_mode_fails_its_readers(self) -> None:
        readers = {1, 2, 5, 6, 7, 8, 9, 10}
        for name in Fixture._entry_names(True):
            for damage in ("missing", "corrupt", "wrong mode"):
                with self.subTest(name=name, damage=damage), Fixture(
                    with_top=True,
                    case=f"read error atlas {name}.png {damage}",
                ) as fixture:
                    path = fixture.atlases_dir / fixture.entry_files[name]
                    self._damage_png(path, damage)
                    if damage != "missing":
                        self._sync_atlas_png_input(fixture, name)
                    assert_read_error(fixture, readers)

    @staticmethod
    def _damage_png(path: Path, damage: str) -> None:
        if damage == "missing":
            path.unlink()
        elif damage == "corrupt":
            path.write_bytes(b"not a PNG image")
        elif damage == "wrong mode":
            with Image.open(path) as image:
                size = image.size
            Image.new("RGB", size, (70, 50, 30)).save(path, format="PNG")
        else:
            raise AssertionError(damage)


class ProvenanceCheckTests(unittest.TestCase):
    def test_distinct_render_frames_keep_their_own_column_for_every_pass(self) -> None:
        with Fixture(with_top=True, case="provenance distinct pixels in all eight columns") as fixture:
            fixture.unit_data["mask_share"] = [0.08, 0.35]
            for part, pass_name in fixture.render_frames:
                if pass_name == "markers":
                    continue
                for k in range(8):
                    frame = fixture.render_frames[(part, pass_name)][k].copy()
                    y, x = np.argwhere(frame[..., 3] > 16)[0]
                    if pass_name == "color":
                        frame[y, x, 0] += k
                    elif pass_name == "mask":
                        frame[y, x, 3] = 255 - k
                    else:
                        frame[y, x, 3] = 255 - 5 * k
                    fixture.render_frames[(part, pass_name)][k] = frame
            fixture.commit(sync_atlas=True)
            for name in fixture.entries:
                self.assertEqual(len({frame.tobytes() for frame in fixture.atlas_frames[name]}), 8, name)
            assert_run(fixture)

    def test_every_manifest_source_hash_is_checked_independently(self) -> None:
        for key in ("camera.json", "light.json", "render.json", "unit.json", "model"):
            with self.subTest(source="render_manifest", key=key), Fixture(
                with_top=True,
                case=f"provenance bad render_manifest hash {key}",
            ) as fixture:
                fixture.manifest_data["hashes"][key] = "0" * 64
                fixture.commit(update_hashes=False)
                fixture.atlases_data["hashes"]["render_manifest.json"] = _sha(fixture.render_manifest_path.read_bytes())
                _write_json(fixture.atlases_json_path, fixture.atlases_data)
                assert_run(fixture, {10})

    def test_every_atlases_source_hash_is_checked_independently(self) -> None:
        for key in ("camera.json", "light.json", "render.json", "unit.json", "render_manifest.json"):
            with self.subTest(source="atlases", key=key), Fixture(
                with_top=True,
                case=f"provenance bad atlases hash {key}",
            ) as fixture:
                fixture.atlases_data["hashes"][key] = "0" * 64
                fixture.commit(update_hashes=False)
                assert_run(fixture, {10})

    def test_each_atlas_png_hash_is_checked_independently(self) -> None:
        for name in Fixture._entry_names(True):
            with self.subTest(entry=name), Fixture(
                with_top=True,
                case=f"provenance bad entry PNG hash {name}",
            ) as fixture:
                fixture.atlases_data["entries"][name]["sha256"] = "0" * 64
                fixture.commit(update_hashes=False)
                assert_run(fixture, {10})

    def test_wrong_existing_hash_in_one_dictionary_does_not_hide_the_other_declaration(self) -> None:
        with Fixture(with_top=True, case="provenance only render manifest camera hash is wrong") as fixture:
            fixture.manifest_data["hashes"]["camera.json"] = "0" * 64
            fixture.commit(update_hashes=False)
            fixture.atlases_data["hashes"]["render_manifest.json"] = _sha(fixture.render_manifest_path.read_bytes())
            _write_json(fixture.atlases_json_path, fixture.atlases_data)
            self.assertNotEqual(fixture.manifest_data["hashes"]["camera.json"], fixture.atlases_data["hashes"]["camera.json"])
            assert_run(fixture, {10})

    def test_each_render_frame_source_maps_to_its_atlas_entry_and_column(self) -> None:
        targets = (
            ("body", "atlas", "UNIT_SYNTH_BODY", "color"),
            ("body", "mask", "HM_SYNTH_BODY", "mask"),
            ("body", "shadow", "UNIT_SYNTH_SHADOW", "shadow"),
            ("top", "atlas", "UNIT_SYNTH_TOP", "color"),
            ("top", "mask", "HM_SYNTH_TOP", "mask"),
        )
        for part, field, name, pass_name in targets:
            for k in (0, 7, 3):
                with self.subTest(part=part, field=field, k=k), Fixture(
                    with_top=True,
                    case=f"provenance pixel mismatch {part}/{field} k={k}",
                ) as fixture:
                    frame = fixture.atlas_frames[name][k].copy()
                    if pass_name == "color":
                        y, x = np.argwhere(frame[:, :, 3] > 16)[0]
                        frame[y, x, 0] = (int(frame[y, x, 0]) + 1) % 256
                    elif pass_name == "mask":
                        fixture.unit_data["mask_share"] = [0.08, 0.35]
                        y, x = np.argwhere(frame[:, :, 3] == 255)[0]
                        frame[y, x, 3] = 254
                    else:
                        y, x = np.argwhere(frame[:, :, 3] == 51)[0]
                        frame[y, x, 3] = 50
                    fixture.set_frame(name, k, frame)
                    fixture.commit()
                    assert_run(fixture, {10})

    def test_directions_must_be_in_column_order(self) -> None:
        with Fixture(with_top=True, case="provenance wrong render directions") as fixture:
            fixture.manifest_data["directions"] = [1, 0, 2, 3, 4, 5, 6, 7]
            fixture.commit()
            assert_run(fixture, {10})


if __name__ == "__main__":
    unittest.main()
