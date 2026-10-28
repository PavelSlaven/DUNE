#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools import hd_assets


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
EXPECTED_HASHES = ("camera.json", "light.json", "render.json", "unit.json")
EXPECTED_ATLAS_HASHES = (*EXPECTED_HASHES, "render_manifest.json")
EXPECTED_RENDER_HASHES = (*EXPECTED_HASHES, "model")


class CheckError(ValueError):
    pass


def _finite_tree(value: Any, where: str) -> None:
    if isinstance(value, float) and not math.isfinite(value):
        raise CheckError(f"{where}: число не конечно")
    if isinstance(value, dict):
        for key, item in value.items():
            _finite_tree(item, f"{where}.{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _finite_tree(item, f"{where}[{index}]")


def _strict_json(path: Path, *, check_finite: bool = True) -> Any:
    def object_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise CheckError(f"{path}: повторяющийся ключ {key!r}")
            result[key] = value
        return result

    def invalid_constant(value: str) -> None:
        raise CheckError(f"{path}: недопустимое число {value}")

    try:
        value = json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=object_pairs,
            parse_constant=invalid_constant,
        )
    except CheckError:
        raise
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise CheckError(f"{path}: не удалось прочитать JSON ({error})") from error
    if check_finite:
        _finite_tree(value, str(path))
    return value


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise CheckError(message)


def _mapping(value: Any, name: str) -> dict[str, Any]:
    _require(isinstance(value, dict), f"{name}: ожидается объект")
    return value


def _number(value: Any, name: str) -> float:
    _require(isinstance(value, (int, float)) and not isinstance(value, bool), f"{name}: ожидается число")
    result = float(value)
    _require(math.isfinite(result), f"{name}: число не конечно")
    return result


def _positive_int(value: Any, name: str) -> int:
    _require(isinstance(value, int) and not isinstance(value, bool) and value > 0, f"{name}: ожидается положительное целое")
    return value


def _string(value: Any, name: str) -> str:
    _require(isinstance(value, str) and bool(value), f"{name}: ожидается непустая строка")
    return value


def _pair(value: Any, name: str, *, numeric: bool = False) -> tuple[Any, Any]:
    _require(isinstance(value, list) and len(value) == 2, f"{name}: ожидается пара")
    if numeric:
        return _number(value[0], f"{name}[0]"), _number(value[1], f"{name}[1]")
    return value[0], value[1]


def _dimensions(value: Any, name: str) -> tuple[int, int]:
    _require(isinstance(value, list) and len(value) == 2, f"{name}: ожидается пара")
    dimensions: list[int] = []
    for index, dimension in enumerate(value):
        _require(
            isinstance(dimension, int) and not isinstance(dimension, bool) and dimension > 0,
            f"{name}[{index}]: ожидается положительное целое",
        )
        dimensions.append(dimension)
    return dimensions[0], dimensions[1]


def _rgb(value: Any, name: str) -> None:
    _require(isinstance(value, list) and len(value) == 3, f"{name}: ожидается тройка")
    for index, channel in enumerate(value):
        _number(channel, f"{name}[{index}]")


def _unit_schema(data: Any) -> dict[str, Any]:
    unit = _mapping(data, "unit.json")
    parts = _mapping(unit.get("parts"), "unit.json.parts")
    _require("body" in parts, "unit.json.parts: отсутствует body")
    _require(set(parts).issubset({"body", "top"}), "unit.json.parts: неизвестная деталь")
    for part_name in ("body", "top"):
        if part_name not in parts:
            continue
        part = _mapping(parts[part_name], f"unit.json.parts.{part_name}")
        _require("atlas" in part, f"unit.json.parts.{part_name}: отсутствует atlas")
        for field, value in part.items():
            _require(field in {"atlas", "shadow", "mask"}, f"unit.json.parts.{part_name}: неизвестное поле {field}")
            _string(value, f"unit.json.parts.{part_name}.{field}")
    _dimensions(unit.get("frame_hd4"), "unit.json.frame_hd4")
    _dimensions(unit.get("atlas_hd4"), "unit.json.atlas_hd4")
    _number(unit.get("length_m"), "unit.json.length_m")
    share = unit.get("mask_share")
    _require(isinstance(share, list) and len(share) == 2, "unit.json.mask_share: ожидается пара")
    _number(share[0], "unit.json.mask_share[0]")
    _number(share[1], "unit.json.mask_share[1]")
    _number(unit.get("max_holes"), "unit.json.max_holes")
    _string(unit.get("model"), "unit.json.model")
    return unit


def _contract_schema(data: Any) -> dict[str, Any]:
    contract = _mapping(data, "contract")
    entries = contract.get("entries")
    _require(isinstance(entries, list), "contract.entries: ожидается список")
    light = _mapping(contract.get("light"), "contract.light")
    _number(light.get("median_angle_degrees"), "contract.light.median_angle_degrees")
    return contract


def _contract_record(contract: dict[str, Any], name: str) -> dict[str, Any]:
    matches = [entry for entry in contract["entries"] if isinstance(entry, dict) and entry.get("name") == name]
    _require(len(matches) == 1, f"contract: запись {name!r} отсутствует или повторяется")
    record = matches[0]
    for field in ("name", "role", "unit_types", "frame_hd4", "hd4_size", "columns", "column_meaning", "house_mask"):
        _require(field in record, f"contract.{name}: отсутствует поле {field}")
    _string(record["name"], f"contract.{name}.name")
    _string(record["role"], f"contract.{name}.role")
    _require(isinstance(record["unit_types"], list), f"contract.{name}.unit_types: ожидается список")
    for index, unit_type in enumerate(record["unit_types"]):
        _string(unit_type, f"contract.{name}.unit_types[{index}]")
    _dimensions(record["frame_hd4"], f"contract.{name}.frame_hd4")
    _dimensions(record["hd4_size"], f"contract.{name}.hd4_size")
    _number(record["columns"], f"contract.{name}.columns")
    meanings = record["column_meaning"]
    _require(isinstance(meanings, list), f"contract.{name}.column_meaning: ожидается список")
    for index, meaning in enumerate(meanings):
        meaning = _mapping(meaning, f"contract.{name}.column_meaning[{index}]")
        _require("column" in meaning and "yaw_deg" in meaning, f"contract.{name}.column_meaning[{index}]: отсутствует поле")
        _number(meaning["column"], f"contract.{name}.column_meaning[{index}].column")
        _number(meaning["yaw_deg"], f"contract.{name}.column_meaning[{index}].yaw_deg")
    _require(record["house_mask"] is None or isinstance(record["house_mask"], str), f"contract.{name}.house_mask: неверный тип")
    return record


def _camera_schema(data: Any) -> dict[str, Any]:
    camera = _mapping(data, "camera.json")
    _number(camera.get("elevation_deg"), "camera.json.elevation_deg")
    _number(camera.get("hd4_px_per_m"), "camera.json.hd4_px_per_m")
    return camera


def _light_schema(data: Any) -> dict[str, Any]:
    light = _mapping(data, "light.json")
    for field in ("sun_azimuth_deg", "sun_elevation_deg", "sun_strength", "sun_angle_deg", "ambient_strength"):
        _number(light.get(field), f"light.json.{field}")
    _rgb(light.get("sun_color"), "light.json.sun_color")
    _rgb(light.get("ambient_color"), "light.json.ambient_color")
    return light


def _render_config_schema(data: Any) -> dict[str, Any]:
    config = _mapping(data, "render.json")
    for field in ("blender", "engine", "device"):
        _string(config.get(field), f"render.json.{field}")
    for field in ("samples", "mask_samples", "seed"):
        _number(config.get(field), f"render.json.{field}")
    _require(isinstance(config.get("denoise"), bool), "render.json.denoise: ожидается boolean")
    return config


def _hash_map(value: Any, keys: tuple[str, ...], name: str) -> dict[str, Any]:
    hashes = _mapping(value, name)
    for key in keys:
        _string(hashes.get(key), f"{name}.{key}")
    return hashes


def _manifest_schema(data: Any, unit: dict[str, Any]) -> dict[str, Any]:
    manifest = _mapping(data, "render_manifest.json")
    _string(manifest.get("blender"), "render_manifest.json.blender")
    for field in ("elevation_deg", "hd4_px_per_m", "model_scale", "pivot_height_m", "cap_height_m", "hull_screen_length_px"):
        _number(manifest.get(field), f"render_manifest.json.{field}")
    _positive_int(manifest.get("supersample"), "render_manifest.json.supersample")
    _dimensions(manifest.get("frame_hd4"), "render_manifest.json.frame_hd4")
    _require(isinstance(manifest.get("parts"), list), "render_manifest.json.parts: ожидается список")
    directions = manifest.get("directions")
    _require(isinstance(directions, list), "render_manifest.json.directions: ожидается список")
    for index, direction in enumerate(directions):
        _number(direction, f"render_manifest.json.directions[{index}]")
    bbox = _mapping(manifest.get("bbox_hd4"), "render_manifest.json.bbox_hd4")
    parts = unit["parts"]
    for part_name in parts:
        bounds_by_direction = _mapping(bbox.get(part_name), f"render_manifest.json.bbox_hd4.{part_name}")
        for k in range(8):
            bounds = bounds_by_direction.get(str(k))
            _require(isinstance(bounds, list) and len(bounds) == 4, f"render_manifest.json.bbox_hd4.{part_name}.{k}: ожидается четверка")
            for index, value in enumerate(bounds):
                _number(value, f"render_manifest.json.bbox_hd4.{part_name}.{k}[{index}]")
    _hash_map(manifest.get("hashes"), EXPECTED_RENDER_HASHES, "render_manifest.json.hashes")
    return manifest


def _atlas_manifest_schema(data: Any) -> dict[str, Any]:
    manifest = _mapping(data, "atlases.json")
    entries = _mapping(manifest.get("entries"), "atlases.json.entries")
    _hash_map(manifest.get("hashes"), EXPECTED_ATLAS_HASHES, "atlases.json.hashes")
    for name, entry_value in entries.items():
        entry = _mapping(entry_value, f"atlases.json.entries.{name}")
        _string(entry.get("file"), f"atlases.json.entries.{name}.file")
        _dimensions(entry.get("size"), f"atlases.json.entries.{name}.size")
        _string(entry.get("sha256"), f"atlases.json.entries.{name}.sha256")
    return manifest


def _read_rgba(path: Path) -> np.ndarray:
    try:
        with Image.open(path) as image:
            _require(image.format == "PNG", f"{path}: файл не PNG")
            _require(image.mode == "RGBA", f"{path}: режим {image.mode}, требуется RGBA")
            image.load()
            return np.asarray(image, dtype=np.uint8).copy()
    except CheckError:
        raise
    except Exception as error:
        raise CheckError(f"{path}: не удалось прочитать PNG ({error})") from error


class Context:
    def __init__(self, args: argparse.Namespace):
        self.unit_dir: Path = args.unit
        self.render_dir: Path = args.render
        self.atlases_dir: Path = args.atlases
        self.contract_path: Path = args.contract
        self.common_dir = self.unit_dir.parent / "common"
        self.paths = {
            "unit.json": self.unit_dir / "unit.json",
            "camera.json": self.common_dir / "camera.json",
            "light.json": self.common_dir / "light.json",
            "render.json": self.common_dir / "render.json",
            "render_manifest.json": self.render_dir / "render_manifest.json",
            "atlases.json": self.atlases_dir / "atlases.json",
            "contract": self.contract_path,
        }
        self.json_cache: dict[str, Any] = {}
        self.image_cache: dict[Path, np.ndarray] = {}

    def json(self, name: str) -> Any:
        if name not in self.json_cache:
            self.json_cache[name] = _strict_json(self.paths[name], check_finite=name != "contract")
        return self.json_cache[name]

    def unit(self) -> dict[str, Any]:
        return _unit_schema(self.json("unit.json"))

    def contract(self) -> dict[str, Any]:
        return _contract_schema(self.json("contract"))

    def camera(self) -> dict[str, Any]:
        return _camera_schema(self.json("camera.json"))

    def light(self) -> dict[str, Any]:
        return _light_schema(self.json("light.json"))

    def render_config(self) -> dict[str, Any]:
        return _render_config_schema(self.json("render.json"))

    def atlases(self) -> dict[str, Any]:
        return _atlas_manifest_schema(self.json("atlases.json"))

    def manifest(self) -> dict[str, Any]:
        return _manifest_schema(self.json("render_manifest.json"), self.unit())

    def image(self, path: Path) -> np.ndarray:
        if path not in self.image_cache:
            self.image_cache[path] = _read_rgba(path)
        return self.image_cache[path]


def _records(unit: dict[str, Any]) -> list[tuple[str, str, str]]:
    result: list[tuple[str, str, str]] = []
    for part_name, part in unit["parts"].items():
        for field in ("atlas", "shadow", "mask"):
            if field in part:
                result.append((part_name, field, part[field]))
    return result


def _slot_role(part: str, field: str) -> str:
    if field == "atlas":
        return "body" if part == "body" else "top"
    if field == "shadow" and part == "body":
        return "shadow"
    _require(field == "mask", f"неподдерживаемое поле unit.json.parts.{part}.{field}")
    return "mask_body" if part == "body" else "mask_top"


def _validate_unit_contract(context: Context, unit: dict[str, Any], contract: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {name: _contract_record(contract, name) for _, _, name in _records(unit)}


def _entry_path(context: Context, atlas_data: dict[str, Any], name: str) -> Path:
    entry = atlas_data["entries"].get(name)
    _require(isinstance(entry, dict), f"atlases.json: отсутствует запись {name}")
    filename = entry["file"]
    _require(Path(filename).name == filename and filename not in (".", ".."), f"atlases.json: недопустимое имя файла {filename!r}")
    return context.atlases_dir / filename


def _atlas_frame(image: np.ndarray, k: int, frame_size: tuple[int, int]) -> np.ndarray:
    width, height = frame_size
    x0 = k * width
    x1 = min(x0 + width, image.shape[1])
    y1 = min(height, image.shape[0])
    if x0 >= image.shape[1] or y1 <= 0 or x1 <= x0:
        return image[:0, :0]
    return image[:y1, x0:x1]


def _check_composition(context: Context) -> str:
    unit = context.unit()
    contract = context.contract()
    atlas_data = context.atlases()
    manifest = context.manifest()
    records = _records(unit)
    names = [name for _, _, name in records]
    _require(len(set(names)) == len(names), "unit.json: повторяющееся имя записи")
    frame_size = _dimensions(unit["frame_hd4"], "unit.json.frame_hd4")
    expected_atlas_size = _dimensions(unit["atlas_hd4"], "unit.json.atlas_hd4")
    frame_w, frame_h = frame_size
    atlas_w, atlas_h = expected_atlas_size
    _require(atlas_w == 8 * frame_w and frame_h <= atlas_h < 2 * frame_h, "геометрия атласа не поддерживается")
    roles = {
        (part, field): _slot_role(part, field)
        for part, field, _ in records
    }
    selected: dict[str, dict[str, Any]] = {}
    for part, field, name in records:
        record = _contract_record(contract, name)
        _require(record["role"] == roles[(part, field)], f"{name}: роль {record['role']!r}, ожидается {roles[(part, field)]!r}")
        selected[name] = record
    for part_name, part in unit["parts"].items():
        atlas_record = selected[part["atlas"]]
        if "mask" in part:
            _require(part["mask"] == atlas_record["house_mask"], f"{part_name}.mask не равен house_mask атласа")
    unit_types = [record["unit_types"] for record in selected.values()]
    _require(not unit_types or all(value == unit_types[0] for value in unit_types), "unit_types записей R различаются")
    all_yaws: list[list[float]] = []
    for name, record in selected.items():
        _require(record["columns"] == 8, f"{name}: columns должно быть 8")
        _require(record["frame_hd4"] == list(frame_size), f"{name}: frame_hd4 не совпадает с unit.json")
        _require(record["hd4_size"] == list(expected_atlas_size), f"{name}: hd4_size не совпадает с unit.json")
        meanings = record["column_meaning"]
        _require(len(meanings) == 8, f"{name}: ожидается восемь column_meaning")
        yaws: list[float] = []
        for k, meaning in enumerate(meanings):
            _require(meaning["column"] == k, f"{name}: column_meaning[{k}].column не равен {k}")
            yaws.append(float(meaning["yaw_deg"]))
        all_yaws.append(yaws)
    _require(not all_yaws or all(yaws == all_yaws[0] for yaws in all_yaws), "yaw_deg записей R различаются")
    entries = atlas_data["entries"]
    _require(set(entries) == set(names), "ключи atlases.json не совпадают с именами R")
    filenames = [entries[name]["file"] for name in names]
    _require(len(set(filenames)) == len(filenames), "atlases.json назначает нескольким записям один файл")
    for name in names:
        path = _entry_path(context, atlas_data, name)
        image = context.image(path)
        entry_size = _dimensions(entries[name]["size"], f"atlases.json.entries.{name}.size")
        _require(image.shape[1::-1] == (atlas_w, atlas_h), f"{name}: размер PNG {image.shape[1::-1]} не равен unit.json.atlas_hd4")
        _require(entry_size == image.shape[1::-1], f"{name}: размер PNG не равен atlases.json.size")
        _require(image.shape[0] >= frame_h and not np.any(image[frame_h:] != 0), f"{name}: область ниже кадров не прозрачна")
    for part_name in unit["parts"]:
        body_folder = context.render_dir / part_name
        _require(body_folder.is_dir(), f"render/{part_name}: отсутствует папка детали")
    actual_part_dirs = {path.name for path in context.render_dir.iterdir() if path.is_dir() and path.name in {"body", "top"}}
    _require(actual_part_dirs == set(unit["parts"]), "папки деталей render не совпадают с unit.json")
    supersample = manifest["supersample"]
    expected_render_size = (frame_w * supersample, frame_h * supersample)
    for part_name in unit["parts"]:
        required_passes = {"color", "mask", "markers"}
        if part_name == "body":
            required_passes.add("shadow")
        folder = context.render_dir / part_name
        expected_files = {f"{pass_name}_{k}.png" for pass_name in required_passes for k in range(8)}
        actual_files = {path.name for path in folder.iterdir() if path.is_file()}
        actual_dirs = {path.name for path in folder.iterdir() if path.is_dir()}
        _require(actual_files == expected_files and not actual_dirs, f"render/{part_name}: список файлов не совпадает с ожидаемым")
        for filename in expected_files:
            image = context.image(folder / filename)
            _require(image.shape[1::-1] == expected_render_size, f"render/{part_name}/{filename}: размер не равен {expected_render_size}")
    expected_atlas_files = {"atlases.json", *filenames}
    actual_atlas_files = {path.name for path in context.atlases_dir.iterdir() if path.is_file()}
    actual_atlas_dirs = {path.name for path in context.atlases_dir.iterdir() if path.is_dir()}
    _require(actual_atlas_files == expected_atlas_files and not actual_atlas_dirs, "список файлов папки atlases не совпадает с atlases.json")
    _require(set(manifest["parts"]) == set(unit["parts"]), "render_manifest.parts не совпадает с unit.json")
    return f"записей={len(names)}, деталей={len(unit['parts'])}, кадров=8"


def _check_pack(context: Context, args: argparse.Namespace) -> str:
    unit = context.unit()
    atlas_data = context.atlases()
    names = {name for _, _, name in _records(unit)}
    for name in names:
        context.image(_entry_path(context, atlas_data, name))
    if args.pack_before is None:
        return "аргументы пака не переданы"
    try:
        before = hd_assets.read_pack(args.pack_before)
        after = hd_assets.read_pack(args.pack_after)
    except Exception as error:
        raise CheckError(f"ошибка чтения D2TM pack: {error}") from error
    before_names = [entry.name for entry in before]
    _require(len(before_names) == len(set(before_names)), "имена записей пака до установки повторяются")
    before_sequence = [(entry.name, entry.extension) for entry in before]
    after_sequence = [(entry.name, entry.extension) for entry in after]
    _require(after_sequence == before_sequence, "последовательность пар (имя, расширение) изменилась")
    after_by_name = {entry.name: entry for entry in after}
    for entry in before:
        if entry.name not in names:
            _require(after_by_name[entry.name].payload == entry.payload, f"байты записи вне R {entry.name} изменились")
    for name in names:
        _require(name in after_by_name, f"запись R {name} отсутствует в паке")
        path = _entry_path(context, atlas_data, name)
        try:
            expected_payload = path.read_bytes()
        except OSError as error:
            raise CheckError(f"{path}: не удалось прочитать файл для записи пака ({error})") from error
        _require(after_by_name[name].payload == expected_payload, f"байты записи {name} не совпадают с назначенным PNG")
    atlas_names = [unit["parts"][part]["atlas"] for part in ("body", "top") if part in unit["parts"]]
    for base_name in atlas_names:
        pattern = re.compile(rf"(?:HV_[^_]+_|HOUSEVARIANT_[^_]+_){re.escape(base_name)}")
        _require(not any(pattern.fullmatch(entry.name) for entry in after), f"в паке остался house variant для {base_name}")
    return f"записей={len(after)}, заменено={len(names)}"


def _marker_centroid(image: np.ndarray, channel: int, supersample: float, label: str) -> tuple[float, float]:
    weights = image[:, :, channel].astype(np.float64)
    total = float(weights.sum())
    _require(total > 0.0 and math.isfinite(total), f"{label}: маркер пуст")
    height, width = weights.shape
    x = (np.arange(width, dtype=np.float64) + 0.5) / supersample
    y = (np.arange(height, dtype=np.float64) + 0.5) / supersample
    cx = float((weights.sum(axis=0) * x).sum() / total)
    cy = float((weights.sum(axis=1) * y).sum() / total)
    _require(math.isfinite(cx) and math.isfinite(cy), f"{label}: центр маркера нечисловой")
    return cx, cy


def _angle_delta(first: float, second: float) -> float:
    return (first - second + 180.0) % 360.0 - 180.0


def _check_direction(context: Context) -> str:
    unit = context.unit()
    contract = context.contract()
    camera = context.camera()
    manifest = context.manifest()
    records = _validate_unit_contract(context, unit, contract)
    supersample = manifest["supersample"]
    theta = math.radians(_number(camera["elevation_deg"], "camera.elevation_deg"))
    _require(manifest["elevation_deg"] == camera["elevation_deg"], "render_manifest.elevation_deg не равен camera.elevation_deg")
    measured = 0
    for part_name, part in unit["parts"].items():
        record = records[part["atlas"]]
        meanings = record["column_meaning"]
        for k in range(8):
            image = context.image(context.render_dir / part_name / f"markers_{k}.png")
            green = _marker_centroid(image, 1, supersample, f"{part_name} k={k} зелёный")
            red = _marker_centroid(image, 0, supersample, f"{part_name} k={k} красный")
            dx = red[0] - green[0]
            dy = red[1] - green[1]
            _require(math.hypot(dx, dy) > 0.0, f"{part_name} k={k}: нулевой вектор маркеров")
            actual = math.degrees(math.atan2(-dy, dx))
            yaw = math.radians(_number(meanings[k]["yaw_deg"], f"{part_name} k={k} yaw_deg"))
            expected = math.degrees(math.atan2(math.sin(yaw) * math.sin(theta), math.cos(yaw)))
            _require(abs(_angle_delta(actual, expected)) <= 3.0, f"{part_name} k={k}: угол отличается на {abs(_angle_delta(actual, expected)):.6f}°")
            measured += 1
    return f"векторов={measured}, допуск=3°"


def _check_pivot(context: Context) -> str:
    unit = context.unit()
    frame_w, frame_h = (float(value) for value in unit["frame_hd4"])
    green_points: list[tuple[float, float]] = []
    blue_points: list[tuple[float, float]] = []
    for part_name in unit["parts"]:
        for k in range(8):
            image = context.image(context.render_dir / part_name / f"markers_{k}.png")
            supersample = image.shape[1] / frame_w
            _require(supersample > 0.0, f"{part_name} k={k}: неверный масштаб маркеров")
            green = _marker_centroid(image, 1, supersample, f"{part_name} k={k} зелёный")
            _require(math.hypot(green[0] - frame_w / 2.0, green[1] - frame_h / 2.0) <= 1.0, f"{part_name} k={k}: ось дальше 1 px от центра кадра")
            green_points.append(green)
            if "top" in unit["parts"]:
                blue_points.append(_marker_centroid(image, 2, supersample, f"{part_name} k={k} синий"))
    if "top" in unit["parts"]:
        mean_x = sum(point[0] for point in blue_points) / len(blue_points)
        mean_y = sum(point[1] for point in blue_points) / len(blue_points)
        for index, point in enumerate(blue_points):
            _require(math.hypot(point[0] - mean_x, point[1] - mean_y) <= 1.0, f"синий маркер {index}: центр кольца разошёлся более чем на 1 px")
    return f"зелёных={len(green_points)}, синих={len(blue_points)}"


def _preflight_unit_atlases(context: Context, unit: dict[str, Any]) -> dict[str, np.ndarray]:
    atlas_data = context.atlases()
    return {
        name: context.image(_entry_path(context, atlas_data, name))
        for _, _, name in _records(unit)
    }


def _iter_atlas_frames(unit: dict[str, Any], images: dict[str, np.ndarray]):
    frame_size = _dimensions(unit["frame_hd4"], "unit.json.frame_hd4")
    for part_name, field, name in _records(unit):
        image = images[name]
        for k in range(8):
            yield part_name, field, name, k, _atlas_frame(image, k, frame_size)


def _check_margin(context: Context) -> str:
    unit = context.unit()
    images = _preflight_unit_atlases(context, unit)
    frame_w, frame_h = _dimensions(unit["frame_hd4"], "unit.json.frame_hd4")
    opaque_count = 0
    for _, _, name, k, frame in _iter_atlas_frames(unit, images):
        if frame.size == 0:
            continue
        ys, xs = np.where(frame[:, :, 3] > 16)
        opaque_count += len(xs)
        _require(
            not np.any((xs < 2) | (xs > frame_w - 3) | (ys < 2) | (ys > frame_h - 3)),
            f"{name} k={k}: непрозрачные пиксели выходят за поле кадра",
        )
    return f"проверено пикселей={opaque_count}, отступ=2 px"


def _union_masks(masks: list[np.ndarray]) -> np.ndarray:
    height = max((mask.shape[0] for mask in masks), default=0)
    width = max((mask.shape[1] for mask in masks), default=0)
    result = np.zeros((height, width), dtype=bool)
    for mask in masks:
        result[: mask.shape[0], : mask.shape[1]] |= mask
    return result


def _opaque_frame(unit: dict[str, Any], images: dict[str, np.ndarray], part_name: str, k: int) -> np.ndarray:
    image = images[unit["parts"][part_name]["atlas"]]
    return _atlas_frame(image, k, _dimensions(unit["frame_hd4"], "unit.json.frame_hd4"))[:, :, 3] > 16


def _check_size(context: Context) -> str:
    unit = context.unit()
    contract = context.contract()
    camera = context.camera()
    manifest = context.manifest()
    images = _preflight_unit_atlases(context, unit)
    contract_records = _validate_unit_contract(context, unit, contract)
    frame_size = _dimensions(unit["frame_hd4"], "unit.json.frame_hd4")
    ref = _number(unit["length_m"], "unit.json.length_m") * _number(camera["hd4_px_per_m"], "camera.json.hd4_px_per_m")
    _require(ref > 0.0, "Lref должен быть положительным")
    body_record = contract_records[unit["parts"]["body"]["atlas"]]
    body_yaws = [float(item["yaw_deg"]) for item in body_record["column_meaning"]]
    for target in (0.0, 180.0):
        matches = [k for k, yaw in enumerate(body_yaws) if yaw == target]
        _require(bool(matches), f"нет столбца yaw={target:g}°")
        for k in matches:
            masks = [_opaque_frame(unit, images, part, k) for part in unit["parts"]]
            union = _union_masks(masks)
            ys, xs = np.where(union)
            _require(len(xs) > 0, f"объединение корпуса и башни пусто при yaw={target:g}°")
            measured = int(xs.max() - xs.min() + 1)
            _require(abs(measured - ref) <= 0.05 * ref, f"yaw={target:g}°: ширина {measured} px отличается от Lref={ref:.6f} px более чем на 5%")
    bounds = manifest["bbox_hd4"]
    comparisons = 0
    for part_name in unit["parts"]:
        image = images[unit["parts"][part_name]["atlas"]]
        for k in range(8):
            frame = _atlas_frame(image, k, frame_size)
            ys, xs = np.where(frame[:, :, 3] > 16)
            _require(len(xs) > 0, f"{part_name} k={k}: область непрозрачных пикселей пуста")
            measured_sizes = (float(xs.max() - xs.min() + 1), float(ys.max() - ys.min() + 1))
            box = bounds[part_name][str(k)]
            reference_sizes = (float(box[2] - box[0]), float(box[3] - box[1]))
            for axis, (measured, reference_size) in enumerate(zip(measured_sizes, reference_sizes)):
                tolerance = max(0.05 * reference_size, 2.0)
                _require(abs(measured - reference_size) <= tolerance, f"{part_name} k={k}: размер {axis} {measured:g} px отличается от bbox {reference_size:g} px более чем на {tolerance:g} px")
                comparisons += 1
    return f"Lref={ref:.6f} px, размеров={comparisons}"


def _run_count(mask: np.ndarray, connectivity: int) -> tuple[int, int]:
    height, width = mask.shape
    parent: list[int] = []
    edge: list[bool] = []

    def root(value: int) -> int:
        while parent[value] != value:
            parent[value] = parent[parent[value]]
            value = parent[value]
        return value

    def join(first: int, second: int) -> None:
        first_root = root(first)
        second_root = root(second)
        if first_root != second_root:
            parent[second_root] = first_root
            edge[first_root] = edge[first_root] or edge[second_root]

    previous: list[tuple[int, int, int]] = []
    for y in range(height):
        row = mask[y]
        padded = np.empty(width + 2, dtype=bool)
        padded[0] = False
        padded[-1] = False
        padded[1:-1] = row
        changes = np.diff(padded.astype(np.int8))
        starts = np.flatnonzero(changes == 1)
        ends = np.flatnonzero(changes == -1) - 1
        current: list[tuple[int, int, int]] = []
        for start_value, end_value in zip(starts, ends):
            start = int(start_value)
            end = int(end_value)
            component = len(parent)
            parent.append(component)
            edge.append(y == 0 or y == height - 1 or start == 0 or end == width - 1)
            current.append((start, end, component))
        reach = 1 if connectivity == 8 else 0
        previous_index = 0
        for start, end, component in current:
            while previous_index < len(previous) and previous[previous_index][1] + reach < start:
                previous_index += 1
            index = previous_index
            while index < len(previous) and previous[index][0] - reach <= end:
                join(component, previous[index][2])
                index += 1
        previous = current
    roots = {root(index) for index in range(len(parent))}
    edge_roots = {root(index) for index in range(len(parent)) if edge[index]}
    return len(roots), len(roots - edge_roots)


def _check_alpha(context: Context) -> str:
    unit = context.unit()
    images = _preflight_unit_atlases(context, unit)
    for _, _, name in _records(unit):
        image = images[name]
        low_alpha = image[:, :, 3] < 8
        nonblack = np.any(image[:, :, :3] != 0, axis=2)
        _require(not np.any(low_alpha & nonblack), f"{name}: пиксель α < 8 имеет ненулевой RGB")
    body_atlas = images[unit["parts"]["body"]["atlas"]]
    frame_size = _dimensions(unit["frame_hd4"], "unit.json.frame_hd4")
    maximum_holes = _number(unit["max_holes"], "unit.json.max_holes")
    for k in range(8):
        frame = _atlas_frame(body_atlas, k, frame_size)
        opaque = frame[:, :, 3] > 16
        components, _ = _run_count(opaque, 8)
        _require(components == 1, f"body k={k}: число 8-связных компонент силуэта {components}, ожидается 1")
        _, holes = _run_count(~opaque, 4)
        _require(holes <= maximum_holes, f"body k={k}: дыр {holes}, допустимо {maximum_holes:g}")
    return f"канонизация, связность и отверстия проверены; max_holes={maximum_holes:g}"


def _check_mask(context: Context) -> str:
    unit = context.unit()
    images = _preflight_unit_atlases(context, unit)
    frame_size = _dimensions(unit["frame_hd4"], "unit.json.frame_hd4")
    low, high = (float(value) for value in unit["mask_share"])
    _require(low <= high, "unit.json.mask_share: нижняя граница больше верхней")
    checked = 0
    for part_name, part in unit["parts"].items():
        if "mask" not in part:
            continue
        mask = images[part["mask"]]
        color = images[part["atlas"]]
        for k in range(8):
            mask_frame = _atlas_frame(mask, k, frame_size)
            color_frame = _atlas_frame(color, k, frame_size)
            alpha = mask_frame[:, :, 3]
            active = alpha > 0
            if not np.any(active):
                raise CheckError(f"{part_name} mask k={k}: маска пуста")
            white = np.all(mask_frame[:, :, :3] == 255, axis=2)
            _require(not np.any(active & ~white), f"{part_name} mask k={k}: пиксель маски не белый")
            support = color_frame[:, :, 3] > 16
            support_height = min(support.shape[0], active.shape[0])
            support_width = min(support.shape[1], active.shape[1])
            supported = np.zeros(active.shape, dtype=bool)
            supported[:support_height, :support_width] = support[:support_height, :support_width]
            _require(not np.any(active & ~supported), f"{part_name} mask k={k}: пиксель маски вне силуэта своей детали")
            denominator = int(np.count_nonzero(support))
            _require(denominator > 0, f"{part_name} k={k}: силуэт атласа пуст")
            share = float(alpha.astype(np.float64).sum() / 255.0 / denominator)
            _require(low <= share <= high, f"{part_name} mask k={k}: доля {share:.9f} вне [{low:g}, {high:g}]")
            strong = alpha >= 253
            _require(bool(np.any(strong)), f"{part_name} mask k={k}: нет пикселя с силой не ниже 0.99")
            checked += 1
    return f"кадров маски={checked}, доля=[{low:g}, {high:g}]"


def check_shadow_frame(frame: np.ndarray, unit_opaque: np.ndarray) -> float:
    image = np.asarray(frame)
    unit = np.asarray(unit_opaque, dtype=bool)
    if image.ndim != 3 or image.shape[2] != 4:
        raise ValueError("кадр тени должен иметь четыре канала")
    if unit.shape != image.shape[:2]:
        raise ValueError("размер объединённого силуэта должен совпадать с кадром тени")
    alpha = image[:, :, 3]
    if np.any((alpha > 0) & np.any(image[:, :, :3] != 0, axis=2)):
        raise ValueError("RGB тени не равен нулю при α > 0")
    peak = int(alpha.max()) if alpha.size else 0
    if peak < 49 or peak > 53:
        raise ValueError(f"максимум α тени {peak} вне [49, 53]")
    shadow = alpha > 16
    if not np.any(shadow):
        raise ValueError("в кадре нет пикселей тени с α > 16")
    exposed = shadow & ~unit
    if not np.any(exposed):
        raise ValueError("нет пикселей тени, открытых за силуэтом")
    sy, sx = np.where(exposed)
    uy, ux = np.where(unit)
    if not len(ux):
        raise ValueError("силуэт юнита пуст")
    dx = float(sx.mean() - ux.mean())
    dy = float(sy.mean() - uy.mean())
    if math.hypot(dx, dy) == 0.0:
        raise ValueError("нулевой вектор тени")
    angle = math.degrees(math.atan2(-dy, dx))
    if not math.isfinite(angle):
        raise ValueError("угол тени нечисловой")
    return angle


def _circle_median(angles: list[float]) -> float:
    _require(bool(angles), "нет углов для круговой медианы")
    ranked = []
    for index, angle in enumerate(angles):
        total = sum(abs(_angle_delta(angle, other)) for other in angles)
        ranked.append((total, index, angle))
    return min(ranked)[2]


def _pad_bool(array: np.ndarray, shape: tuple[int, int]) -> np.ndarray:
    result = np.zeros(shape, dtype=bool)
    height = min(shape[0], array.shape[0])
    width = min(shape[1], array.shape[1])
    result[:height, :width] = array[:height, :width]
    return result


def _check_shadow(context: Context) -> str:
    unit = context.unit()
    contract = context.contract()
    _validate_unit_contract(context, unit, contract)
    images = _preflight_unit_atlases(context, unit)
    median_target = _number(contract["light"]["median_angle_degrees"], "contract.light.median_angle_degrees")
    frame_size = _dimensions(unit["frame_hd4"], "unit.json.frame_hd4")
    if "shadow" not in unit["parts"]["body"]:
        return "теневая запись не объявлена"
    body_shadow = images[unit["parts"]["body"]["shadow"]]
    body_color = images[unit["parts"]["body"]["atlas"]]
    top_color = images[unit["parts"]["top"]["atlas"]] if "top" in unit["parts"] else None
    angles: list[float] = []
    for k in range(8):
        shadow = _atlas_frame(body_shadow, k, frame_size)
        masks = [_atlas_frame(body_color, k, frame_size)[:, :, 3] > 16]
        if top_color is not None:
            masks.append(_atlas_frame(top_color, k, frame_size)[:, :, 3] > 16)
        union = _union_masks(masks)
        shape = (max(shadow.shape[0], union.shape[0]), max(shadow.shape[1], union.shape[1]))
        padded_shadow = np.zeros((*shape, 4), dtype=np.uint8)
        padded_shadow[: shadow.shape[0], : shadow.shape[1]] = shadow
        padded_union = _pad_bool(union, shape)
        try:
            angles.append(check_shadow_frame(padded_shadow, padded_union))
        except ValueError as error:
            raise CheckError(f"shadow k={k}: {error}") from error
    median = _circle_median(angles)
    _require(abs(_angle_delta(median, median_target)) <= 10.0, f"медианный угол тени {median:.6f}° отличается от {median_target:.6f}° более чем на 10°")
    for k, angle in enumerate(angles):
        _require(abs(_angle_delta(angle, median_target)) <= 20.0, f"shadow k={k}: угол {angle:.6f}° отличается от {median_target:.6f}° более чем на 20°")
    return f"угол медианы={median:.6f}°, цель={median_target:.6f}°"


def _sha256_path(path: Path) -> str:
    try:
        digest = hashlib.sha256()
        with path.open("rb") as stream:
            for block in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(block)
        return digest.hexdigest()
    except OSError as error:
        raise CheckError(f"{path}: не удалось прочитать файл для SHA-256 ({error})") from error


def _verify_hashes(declarations: dict[str, Any], files: dict[str, Path], label: str) -> None:
    _require(set(declarations) == set(files), f"{label}: список хэшей не совпадает с требуемым")
    for key, path in files.items():
        expected = declarations[key]
        actual = _sha256_path(path)
        _require(actual == expected, f"{label}.{key}: SHA-256 не совпадает")


def _render_source(context: Context, part: str, pass_name: str, k: int, size: tuple[int, int]) -> np.ndarray:
    path = context.render_dir / part / f"{pass_name}_{k}.png"
    image = context.image(path)
    rgba = Image.fromarray(image, mode="RGBA").convert("RGBA").convert("RGBa")
    resized = rgba.resize(size, Image.Resampling.LANCZOS).convert("RGBA")
    result = np.asarray(resized, dtype=np.uint8).copy()
    result[result[:, :, 3] < 8] = 0
    return result


def _check_provenance(context: Context) -> str:
    unit = context.unit()
    camera = context.camera()
    light = context.light()
    render_config = context.render_config()
    contract = context.contract()
    _validate_unit_contract(context, unit, contract)
    manifest = context.manifest()
    atlas_data = context.atlases()
    model_path = context.unit_dir / unit["model"]
    source_files = {
        "camera.json": context.paths["camera.json"],
        "light.json": context.paths["light.json"],
        "render.json": context.paths["render.json"],
        "unit.json": context.paths["unit.json"],
        "model": model_path,
    }
    manifest_hashes = manifest["hashes"]
    _verify_hashes(manifest_hashes, source_files, "render_manifest.json.hashes")
    atlas_hash_files = {
        "camera.json": context.paths["camera.json"],
        "light.json": context.paths["light.json"],
        "render.json": context.paths["render.json"],
        "unit.json": context.paths["unit.json"],
        "render_manifest.json": context.paths["render_manifest.json"],
    }
    _verify_hashes(atlas_data["hashes"], atlas_hash_files, "atlases.json.hashes")
    names = [name for _, _, name in _records(unit)]
    for name, entry in atlas_data["entries"].items():
        path = _entry_path(context, atlas_data, name)
        _require(_sha256_path(path) == entry["sha256"], f"atlases.json.entries.{name}.sha256: не совпадает")
    _require(manifest["directions"] == list(range(8)), "render_manifest.directions должен быть [0..7]")
    frame_w, frame_h = _dimensions(unit["frame_hd4"], "unit.json.frame_hd4")
    size = (frame_w, frame_h)
    alpha_frames: list[np.ndarray] | None = None
    if any(field == "shadow" for _, field, _ in _records(unit)):
        shadow_frames = [_render_source(context, "body", "shadow", k, size) for k in range(8)]
        peak = max(int(frame[:, :, 3].max()) for frame in shadow_frames)
        _require(peak > 0, "shadow provenance: невозможно нормировать нулевой α")
        for frame in shadow_frames:
            frame[:, :, :3] = 0
            frame[:, :, 3] = np.round(frame[:, :, 3].astype(np.float32) * 51 / peak).astype(np.uint8)
        alpha_frames = [frame[:, :, 3].copy() for frame in shadow_frames]
    comparisons = 0
    for part_name, field, name in _records(unit):
        atlas_png = context.image(_entry_path(context, atlas_data, name))
        if field == "atlas":
            pass_name = "color"
        elif field == "mask":
            pass_name = "mask"
        else:
            pass_name = "shadow"
        transformed: list[np.ndarray]
        if pass_name == "shadow":
            if alpha_frames is None:
                raise CheckError("shadow provenance: нет кадров тени")
            transformed = []
            for alpha in alpha_frames:
                image = np.zeros((*alpha.shape, 4), dtype=np.uint8)
                image[:, :, 3] = alpha
                transformed.append(image)
        else:
            transformed = [_render_source(context, part_name, pass_name, k, size) for k in range(8)]
            if pass_name == "mask":
                color_frames = [_render_source(context, part_name, "color", k, size) for k in range(8)]
                for k in range(8):
                    transformed[k][color_frames[k][:, :, 3] <= 16] = 0
        for k in range(8):
            expected = transformed[k]
            actual = _atlas_frame(atlas_png, k, size)
            height = min(expected.shape[0], actual.shape[0])
            width = min(expected.shape[1], actual.shape[1])
            _require(actual.shape == expected.shape, f"{name} k={k}: неполный кадр в PNG атласа")
            _require(np.array_equal(actual[:height, :width], expected[:height, :width]), f"{name} k={k}: пиксели не совпадают с кадром рендера")
            comparisons += 1
    return f"хэшей и кадров проверено={len(manifest_hashes) + len(atlas_data['hashes']) + len(names) + comparisons}"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Проверка атласов и рендера 3D-юнита")
    parser.add_argument("--unit", required=True, type=Path)
    parser.add_argument("--render", required=True, type=Path)
    parser.add_argument("--atlases", required=True, type=Path)
    parser.add_argument("--contract", required=True, type=Path)
    parser.add_argument("--pack-before", type=Path)
    parser.add_argument("--pack-after", type=Path)
    parser.add_argument("--allow-skip", choices=("2",))
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if (args.pack_before is None) != (args.pack_after is None):
        parser.error("--pack-before и --pack-after должны передаваться вместе")
    context = Context(args)
    checks = (
        _check_composition,
        lambda ctx: _check_pack(ctx, args),
        _check_direction,
        _check_pivot,
        _check_margin,
        _check_size,
        _check_alpha,
        _check_mask,
        _check_shadow,
        _check_provenance,
    )
    failures = 0
    for index, (name, function) in enumerate(zip(CHECK_NAMES, checks), start=1):
        try:
            detail = function(context)
            if index == 2 and args.pack_before is None:
                status = "SKIP"
                detail = "проверка пропущена: не переданы аргументы пака"
            else:
                status = "PASS"
        except Exception as error:
            status = "FAIL"
            detail = str(error).replace("\t", " ").replace("\n", " ") or error.__class__.__name__
            failures += 1
        print(f"{index}\t{name}\t{status}\t{detail}")
    skipped_allowed = args.allow_skip == "2" and args.pack_before is None
    return 0 if failures == 0 and (args.pack_before is not None or skipped_allowed) else 1


if __name__ == "__main__":
    raise SystemExit(main())
