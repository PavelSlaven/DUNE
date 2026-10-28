#!/usr/bin/env python3
"""Собрать контракт атласов юнитов и правил отрисовки из исходников и паков."""

from __future__ import annotations

import argparse
import ast
import json
import math
import os
from pathlib import Path
import re
import statistics
import sys
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
TOOLS_DIR = ROOT / "tools"
sys.path.insert(0, str(TOOLS_DIR))

from hd_assets import decode_image, read_pack


UNIT_TYPE_RE = re.compile(r"#define\s+(\w+)\s+(\d+)\b")
UNIT_ASSIGNMENT_RE = re.compile(
    r"sUnitInfo\[(?P<type>\w+)\]\.(?P<field>bmp|top|shadow|bmp_width|bmp_height)\s*=\s*(?P<value>.*?);"
)
RESOURCE_REF_RE = re.compile(r"get(?:Surface|Texture)\((\w+)\)")
RAW_CPP_STRING_RE = re.compile(r'(?:u8|u|U|L)?R"([^ ()\\\t\r\n]{0,16})\(')
MANIFEST_PATH = "resources/hd/source_references/battle_for_arrakis_complete/manifest.json"


def strip_cpp_comments(source: str) -> str:
    output: list[str] = []
    index = 0
    state = "code"
    quote = None
    while index < len(source):
        char = source[index]
        if state == "line":
            if char == "\n":
                output.append(char)
                state = "code"
            else:
                output.append(" ")
            index += 1
            continue
        if state == "block":
            if source.startswith("*/", index):
                output.extend((" ", " "))
                index += 2
                state = "code"
            elif char == "\n":
                output.append(char)
                index += 1
            else:
                output.append(" ")
                index += 1
            continue
        if state == "string":
            output.append(char)
            index += 1
            if char == "\\" and index < len(source):
                output.append(source[index])
                index += 1
            elif char == quote:
                quote = None
                state = "code"
            continue
        if char in "uULR":
            raw_match = RAW_CPP_STRING_RE.match(source, index)
            if raw_match:
                terminator = ")" + raw_match.group(1) + '"'
                end = source.find(terminator, raw_match.end())
                end = len(source) if end < 0 else end + len(terminator)
                output.extend(source[index:end])
                index = end
                continue
        if source.startswith("//", index):
            output.extend((" ", " "))
            index += 2
            state = "line"
            continue
        if source.startswith("/*", index):
            output.extend((" ", " "))
            index += 2
            state = "block"
            continue
        if char in {'"', "'"}:
            quote = char
            state = "string"
        output.append(char)
        index += 1
    return "".join(output)


class SourceIndex:
    def __init__(self, root: Path) -> None:
        self.root = root
        self._lines: dict[str, list[str]] = {}
        self._search_lines: dict[str, list[str]] = {}
        self._text: dict[str, str] = {}
        self._functions: dict[tuple[str, str], list[tuple[int, str]]] = {}

    def lines(self, relative_path: str) -> list[str]:
        if relative_path not in self._lines:
            self._lines[relative_path] = (
                self.root / relative_path
            ).read_text(encoding="utf-8").splitlines()
        return self._lines[relative_path]

    def text(self, relative_path: str) -> str:
        if relative_path not in self._text:
            self._text[relative_path] = "\n".join(self.lines(relative_path))
        return self._text[relative_path]

    def search_lines(self, relative_path: str) -> list[str]:
        if relative_path not in self._search_lines:
            lines = self.lines(relative_path)
            if Path(relative_path).suffix in {".cpp", ".h", ".hpp"}:
                lines = strip_cpp_comments("\n".join(lines)).splitlines()
            self._search_lines[relative_path] = lines
        return self._search_lines[relative_path]

    def ref(self, relative_path: str, identifier: str, occurrence: int = 0) -> dict[str, str]:
        matches = [
            line_number
            for line_number, line in enumerate(self.search_lines(relative_path), 1)
            if identifier in line
        ]
        if occurrence >= len(matches):
            raise ValueError(f"cannot find source anchor {identifier!r} in {relative_path}")
        return {
            "ref": f"{relative_path}:{matches[occurrence]}",
            "identifier": identifier,
        }

    def ref_matching(self, relative_path: str, identifier: str, predicate) -> dict[str, str]:
        for line_number, line in enumerate(self.search_lines(relative_path), 1):
            if identifier in line and predicate(line):
                return {"ref": f"{relative_path}:{line_number}", "identifier": identifier}
        raise ValueError(f"cannot find source anchor {identifier!r} in {relative_path}")

    def function_lines(self, relative_path: str, signature: str) -> list[tuple[int, str]]:
        cache_key = (relative_path, signature)
        if cache_key in self._functions:
            return self._functions[cache_key]
        source_lines = self.search_lines(relative_path)
        start = next(
            (index for index, line in enumerate(source_lines) if signature in line),
            None,
        )
        if start is None:
            raise ValueError(f"cannot find function {signature!r} in {relative_path}")
        depth = 0
        opened = False
        result: list[tuple[int, str]] = []
        for index in range(start, len(source_lines)):
            line = source_lines[index]
            result.append((index + 1, line))
            depth += line.count("{") - line.count("}")
            opened = opened or "{" in line
            if opened and depth == 0:
                self._functions[cache_key] = result
                return result
        raise ValueError(f"unterminated function {signature!r} in {relative_path}")

    def function_ref(
        self,
        relative_path: str,
        signature: str,
        identifier: str,
        occurrence: int = 0,
    ) -> dict[str, str]:
        matches = [
            line_number
            for line_number, line in self.function_lines(relative_path, signature)
            if identifier in line
        ]
        if occurrence >= len(matches):
            raise ValueError(f"cannot find {identifier!r} in {signature!r}")
        return {
            "ref": f"{relative_path}:{matches[occurrence]}",
            "identifier": identifier,
        }

    def source_call_refs(self, pattern: re.Pattern[str]) -> list[dict[str, str]]:
        refs: list[dict[str, str]] = []
        for path in sorted((self.root / "src").rglob("*")):
            if not path.is_file() or path.suffix not in {".cpp", ".h", ".hpp"}:
                continue
            relative_path = path.relative_to(self.root).as_posix()
            for line_number, line in enumerate(self.search_lines(relative_path), 1):
                for match in pattern.finditer(line):
                    prefix = line[:match.start()]
                    if not re.search(r"(?:->|\.)\s*$", prefix):
                        continue
                    refs.append({
                        "ref": f"{relative_path}:{line_number}",
                        "identifier": match.group(0),
                    })
        return refs


def unique_refs(refs: list[dict[str, str]]) -> list[dict[str, str]]:
    seen: set[tuple[str, str]] = set()
    result: list[dict[str, str]] = []
    for ref in refs:
        key = (ref["ref"], ref["identifier"])
        if key not in seen:
            seen.add(key)
            result.append(ref)
    return result


def parse_integer_expression(expression: str) -> int:
    node = ast.parse(expression.strip(), mode="eval").body

    def evaluate(value: ast.AST) -> int:
        if isinstance(value, ast.Constant) and isinstance(value.value, int):
            return value.value
        if isinstance(value, ast.UnaryOp) and isinstance(value.op, ast.USub):
            return -evaluate(value.operand)
        if isinstance(value, ast.BinOp):
            left = evaluate(value.left)
            right = evaluate(value.right)
            if isinstance(value.op, ast.Mult):
                return left * right
            if isinstance(value.op, ast.Add):
                return left + right
            if isinstance(value.op, ast.Sub):
                return left - right
        raise ValueError(f"unsupported C++ integer expression: {expression!r}")

    return evaluate(node)


def parse_type_ids(source: SourceIndex) -> dict[str, int]:
    result: dict[str, int] = {}
    for line in source.lines("src/include/definitions.h"):
        match = UNIT_TYPE_RE.match(line.strip())
        if match and match.group(1) not in {
            "MAX_UNITTYPES",
            "SPECIAL_SABOTEUR",
            "SPECIAL_FREMEN",
        }:
            result[match.group(1)] = int(match.group(2))
    return result


def parse_unit_records(source: SourceIndex) -> dict[str, dict[str, Any]]:
    relative_path = "src/utils/cIniGameRessouces.cpp"
    records: dict[str, dict[str, Any]] = {}
    for line_number, line in enumerate(source.lines(relative_path), 1):
        match = UNIT_ASSIGNMENT_RE.search(line)
        if not match:
            continue
        unit_type = match.group("type")
        field = match.group("field")
        expression = match.group("value").strip()
        record = records.setdefault(
            unit_type,
            {"type": unit_type, "resources": {}, "sizes": {}, "source_refs": {}},
        )
        identifier = f"sUnitInfo[{unit_type}].{field}"
        if field in {"bmp", "top", "shadow"}:
            resource_match = RESOURCE_REF_RE.search(expression)
            if resource_match:
                value: Any = resource_match.group(1)
            elif expression == "nullptr":
                value = None
            else:
                raise ValueError(f"unsupported unit bitmap assignment: {line.strip()}")
            record["resources"][field] = value
        else:
            value = parse_integer_expression(expression)
            record["sizes"][field] = value
        record["source_refs"][field] = {
            "ref": f"{relative_path}:{line_number}",
            "identifier": identifier,
        }
    return records


def build_unit_resource_index(
    records: dict[str, dict[str, Any]],
) -> dict[str, list[dict[str, Any]]]:
    by_resource: dict[str, list[dict[str, Any]]] = {}
    for record in records.values():
        for resource in record["resources"].values():
            if resource:
                by_resource.setdefault(resource, []).append(record)
    return by_resource


def parse_density(source: SourceIndex) -> tuple[int, dict[str, Any]]:
    relative_path = "src/cGame_logic.cpp"
    match = re.search(r"constexpr int density\s*=\s*(\d+)\s*;", source.text(relative_path))
    if match is None:
        raise ValueError("HD4 density assignment was not found in cGame_logic.cpp")
    density = int(match.group(1))
    return density, {
        "value": density,
        "sources": unique_refs([
            source.ref(relative_path, f"constexpr int density = {density};"),
            source.ref("src/drawers/SDLDrawer.cpp", "srcRect.w *= src->density;"),
            source.ref("src/drawers/SDLDrawer.cpp", "srcRect.h *= src->density;"),
        ]),
    }


def parse_tile_dimensions(source: SourceIndex) -> tuple[dict[str, int], list[dict[str, str]]]:
    path = "src/map/cMap.h"
    values: dict[str, int] = {}
    refs = []
    for axis in ("WIDTH", "HEIGHT"):
        match = re.search(
            rf"#define\s+TILESIZE_{axis}_PIXELS\s+(.+?)\s*$",
            source.text(path),
            re.MULTILINE,
        )
        if match is None:
            raise ValueError(f"tile dimension not found: TILESIZE_{axis}_PIXELS")
        values[axis.lower()] = parse_integer_expression(match.group(1))
        refs.append(source.ref(path, f"#define TILESIZE_{axis}_PIXELS"))
    return values, refs


def parse_angle_mapping(source: SourceIndex) -> tuple[list[dict[str, Any]], dict[str, Any], dict[str, Any]]:
    declaration_path = "src/utils/d2tm_math.h"
    declaration = next(
        (
            line.strip()
            for line in source.lines(declaration_path)
            if "int convertAngleToDrawIndex(" in line
        ),
        None,
    )
    if declaration is None:
        raise ValueError("convertAngleToDrawIndex declaration was not found")
    defaults = re.search(
        r"bool\s+clockWiseBitmap\s*=\s*(true|false)\s*,\s*"
        r"int\s+offset\s*=\s*(\d+)\s*,\s*int\s+maxFacings\s*=\s*(\d+)",
        declaration,
    )
    if defaults is None:
        raise ValueError("convertAngleToDrawIndex default parameters could not be parsed")
    clockwise = defaults.group(1) == "true"
    offset, facing_count = int(defaults.group(2)), int(defaults.group(3))
    math_path = "src/utils/d2tm_math.cpp"
    function = source.function_lines(math_path, "int convertAngleToDrawIndex(")
    function_text = "\n".join(line for _, line in function)
    if "if (clockWiseBitmap)" not in function_text:
        raise ValueError("convertAngleToDrawIndex direction branch was not found")
    if "int angle = offset - faceAngle;" not in function_text:
        raise ValueError("counter-clockwise angle formula was not found")
    if "int angle = offset + faceAngle;" not in function_text:
        raise ValueError("clockwise angle formula was not found")

    face_names = {
        "UP": "N",
        "UPRIGHT": "NE",
        "RIGHT": "E",
        "DOWNRIGHT": "SE",
        "DOWN": "S",
        "DOWNLEFT": "SW",
        "LEFT": "W",
        "UPLEFT": "NW",
    }
    definitions = source.lines("src/include/definitions.h")
    face_angles: dict[str, int] = {}
    face_refs: list[dict[str, str]] = []
    for name in face_names:
        match = next(
            (
                re.match(rf"\s*#define\s+FACE_{name}\s+(\d+)\b", line)
                for line in definitions
                if re.match(rf"\s*#define\s+FACE_{name}\s+\d+\b", line)
            ),
            None,
        )
        if match is None:
            raise ValueError(f"FACE_{name} definition was not found")
        face_angles[name] = int(match.group(1))
        face_refs.append(source.ref_matching(
            "src/include/definitions.h",
            f"#define FACE_{name}",
            lambda line, name=name: re.match(rf"\s*#define\s+FACE_{name}\s+\d+\b", line) is not None,
        ))

    def draw_index(face_angle: int) -> int:
        angle = offset + face_angle if clockwise else offset - face_angle
        if clockwise and angle > facing_count - 1:
            angle -= facing_count
        elif not clockwise and angle < 0:
            angle += facing_count
        return angle

    by_column = {
        draw_index(face_angle): face_names[name]
        for name, face_angle in face_angles.items()
    }
    if sorted(by_column) != list(range(facing_count)):
        raise ValueError("FACE_* definitions do not cover all draw columns")
    yaw_step = 360 // facing_count
    direction_columns = [
        {"column": column, "direction": by_column[column], "yaw_deg": yaw_step * column}
        for column in range(facing_count)
    ]
    implementation_refs = [
        source.ref(math_path, "if (clockWiseBitmap)"),
        source.ref(math_path, "int angle = offset + faceAngle;"),
        source.ref(math_path, "int angle = offset - faceAngle;"),
        source.ref(math_path, "if (angle > (maxFacings - 1))"),
        source.ref(math_path, "if (angle < 0)"),
        source.ref(declaration_path, "int convertAngleToDrawIndex("),
    ]
    rule = {
        "value": direction_columns,
        "sources": unique_refs(implementation_refs + face_refs),
    }
    converter = {
        "clockwise": clockwise,
        "offset": offset,
        "max_facings": facing_count,
        "draw_index": draw_index,
        "face_angles": face_angles,
    }
    return direction_columns, rule, converter


def image_for(entry, cache: dict[int, Any]):
    key = id(entry)
    if key not in cache:
        cache[key] = decode_image(entry.payload)
    return cache[key]


def image_size(entry, cache: dict[int, Any]) -> list[int] | None:
    image = image_for(entry, cache)
    return list(image.size) if image is not None else None


def load_sega_manifest(source: SourceIndex) -> dict[str, Any]:
    return json.loads(source.text(MANIFEST_PATH))


def parse_sega_asset_specs(source: SourceIndex, manifest: dict[str, Any]) -> dict[str, dict[str, Any]]:
    asset_path = "tools/build_review_asset_pack.py"
    asset_text = source.text(asset_path)
    tree = ast.parse(asset_text, filename=asset_path)
    spec_fields = next(
        (
            [
                item.target.id
                for item in node.body
                if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name)
            ]
            for node in tree.body
            if isinstance(node, ast.ClassDef) and node.name == "AssetSpec"
        ),
        None,
    )
    if spec_fields is None:
        raise ValueError(f"AssetSpec fields were not found in {asset_path}")

    units_assignment = next(
        (
            node.value
            for node in tree.body
            if isinstance(node, ast.Assign)
            and any(isinstance(target, ast.Name) and target.id == "UNITS" for target in node.targets)
        ),
        None,
    )
    if not isinstance(units_assignment, ast.List):
        raise ValueError(f"UNITS AssetSpec list was not found in {asset_path}")

    manifest_files = {
        item.get("file")
        for item in manifest.get("files", [])
        if isinstance(item, dict) and isinstance(item.get("file"), str)
    }
    result: dict[str, dict[str, Any]] = {}
    for call in units_assignment.elts:
        if not isinstance(call, ast.Call) or not isinstance(call.func, ast.Name) or call.func.id != "AssetSpec":
            continue
        argument_nodes: dict[str, ast.AST] = {
            field: argument
            for field, argument in zip(spec_fields, call.args)
        }
        argument_nodes.update(
            {keyword.arg: keyword.value for keyword in call.keywords if keyword.arg is not None}
        )
        try:
            symbol = ast.literal_eval(argument_nodes["symbol"])
            filename = ast.literal_eval(argument_nodes["source_file"])
        except (KeyError, ValueError, TypeError) as error:
            raise ValueError(f"cannot read symbol/source_file in {asset_path}:{call.lineno}") from error
        if not isinstance(symbol, str) or not isinstance(filename, str):
            raise ValueError(f"invalid symbol/source_file in {asset_path}:{call.lineno}")
        filename_node = argument_nodes["source_file"]
        if filename not in manifest_files:
            raise ValueError(f"{symbol}: Sega file {filename!r} is missing from manifest.files")
        if symbol in result:
            raise ValueError(f"duplicate UNIT AssetSpec symbol {symbol!r} in {asset_path}")
        source_file_ref = {
            "ref": f"{asset_path}:{filename_node.lineno}",
            "identifier": ast.get_source_segment(asset_text, filename_node) or filename,
        }
        manifest_file_ref = source.ref(MANIFEST_PATH, f'"{filename}"')
        result[symbol] = {
            "reference": f"resources/hd/source_references/battle_for_arrakis_complete/{filename}",
            "sources": [source_file_ref, manifest_file_ref],
        }
    return result


def sega_mapping(
    source: SourceIndex,
    manifest: dict[str, Any],
    records: dict[str, dict[str, Any]],
) -> dict[str, tuple[str, list[dict[str, str]]]]:
    asset_specs = parse_sega_asset_specs(source, manifest)
    result: dict[str, tuple[str, list[dict[str, str]]]] = {}

    def assign(symbol: str, mapped: dict[str, Any], unit_type: str) -> None:
        value = (mapped["reference"], mapped["sources"])
        existing = result.get(symbol)
        if existing is not None and existing[0] != value[0]:
            raise ValueError(f"{symbol}: unit types resolve to different Sega files (including {unit_type})")
        if existing is None:
            result[symbol] = value
        else:
            result[symbol] = (existing[0], unique_refs(existing[1] + value[1]))

    for unit_type, record in records.items():
        for field in ("bmp", "top"):
            symbol = record["resources"].get(field)
            if not symbol:
                continue
            mapped = asset_specs.get(symbol)
            if mapped is None:
                raise ValueError(f"{symbol}: no UNITS AssetSpec for {unit_type}.{field}")
            assign(symbol, mapped, unit_type)
    return result


def parse_infantry_assignments(source: SourceIndex) -> dict[str, dict[str, str]]:
    init = "src/utils/cIniGameRessouces.cpp"
    pattern = re.compile(r"sUnitInfo\[(?P<type>\w+)\]\.infantry\s*=\s*true\s*;")
    assignments: dict[str, dict[str, str]] = {}
    for line_number, line in enumerate(source.search_lines(init), 1):
        match = pattern.search(line)
        if match is None:
            continue
        unit_type = match.group("type")
        assignments[unit_type] = {
            "ref": f"{init}:{line_number}",
            "identifier": match.group(0),
        }
    return assignments


def unit_row_usage(
    source: SourceIndex,
    unit_type: str,
    infantry_assignments: dict[str, dict[str, str]],
) -> tuple[str, list[dict[str, str]]]:
    cpp = "src/gameobjects/units/cUnit.cpp"
    init = "src/utils/cIniGameRessouces.cpp"
    if unit_type in infantry_assignments:
        refs = [
            source.function_ref(cpp, "eUnitMoveToCellResult cUnit::moveToNextCellLogic()", anchor)
            for anchor in (
                "if (isInfantryUnit())", "if (TIMER_frame > 3)", "iFrame++",
                "if (iFrame > 3)", "iFrame = 0;",
            )
        ]
        refs.append(infantry_assignments[unit_type])
        return "Строки соответствуют циклу кадров пехоты 0–3 при движении.", refs
    if unit_type == "HARVESTER":
        return "При сборе используются строки 1–3; код возвращает кадр к 1 и сбрасывает его в 0 вне цикла сбора.", [
            source.function_ref(cpp, "void cUnit::think_harvester()", "iFrame++"),
            source.function_ref(cpp, "void cUnit::think_harvester()", "if (iFrame > 3)"),
            source.function_ref(cpp, "void cUnit::think_harvester()", "iFrame = 1;"),
            source.function_ref(cpp, "void cUnit::think_harvester()", "iFrame = 0;"),
        ]
    if unit_type == "CARRYALL":
        return "Строка 0 используется без груза, строка 1 — при переноске или передаче груза.", [
            source.function_ref(cpp, "void cUnit::think_carryAll()", "iFrame = 1;"),
            source.function_ref(cpp, "void cUnit::think_carryAll()", "iFrame = 0;"),
        ]
    if unit_type == "ORNITHOPTER":
        return "Кадры полёта циклически проходят строки 0–3.", [
            source.function_ref(cpp, "void cUnit::think_ornithopter()", "iFrame++"),
            source.function_ref(cpp, "void cUnit::think_ornithopter()", "if (iFrame > 3)"),
        ]
    if unit_type == "SANDWORM":
        return "cUnit::draw немедленно выходит для червя; кадры UNIT_SANDWORM не выбираются через iFrame.", [
            source.function_ref(cpp, "void cUnit::draw()", "if (isSandworm())"),
            source.function_ref(cpp, "void cUnit::draw()", "return;", occurrence=1),
            source.ref(init, "sUnitInfo[SANDWORM].bmp ="),
        ]
    return "В обычной логике этот тип остаётся на строке 0, установленной при создании cUnit.", [
        source.ref(cpp, "iFrame = 0;"),
        source.function_ref(cpp, "void cUnit::draw()", "int start_y = bmp_height * iFrame;"),
    ]


def parse_draw_sites(
    source: SourceIndex,
    records: dict[str, dict[str, Any]],
    converter: dict[str, Any],
) -> dict[str, list[dict[str, Any]]]:
    pattern = re.compile(r"getUnit(?:Top|Shadow)?Bitmap\s*\([^)]*\)")
    refs = source.source_call_refs(pattern)
    unit_draw_lines = {
        line_number
        for line_number, _ in source.function_lines(
            "src/gameobjects/units/cUnit.cpp", "void cUnit::draw()"
        )
    }
    refinery_pad_lines = {
        line_number
        for line_number, _ in source.function_lines(
            "src/drawers/cStructureDrawer.cpp",
            "void cStructureDrawer::drawHarvesterOnRefineryPad(",
        )
    }
    sites_by_resource: dict[str, list[dict[str, Any]]] = {}
    for ref in refs:
        path, line_number = ref["ref"].rsplit(":", 1)
        line_number_int = int(line_number)
        identifier = ref["identifier"]
        method = re.match(r"(getUnitTopBitmap|getUnitShadowBitmap|getUnitBitmap)", identifier)
        if method is None:
            continue
        method_name = method.group(1)
        field = {
            "getUnitTopBitmap": "top",
            "getUnitShadowBitmap": "shadow",
            "getUnitBitmap": "bmp",
        }[method_name]
        argument = identifier[identifier.find("(") + 1:-1].strip()
        target_records: list[dict[str, Any]]
        if path == "src/gameobjects/units/cUnit.cpp" and line_number_int in unit_draw_lines:
            if argument != "iType":
                raise ValueError(f"{path}:{line_number_int}: unhandled {method_name} argument {argument!r}")
            site: dict[str, Any] = {
                "source": ref,
                "column": "convertAngleToDrawIndex(iHeadFacing)" if field == "top" else "convertAngleToDrawIndex(iBodyFacing)",
                "row": "iFrame",
            }
            target_records = [
                record for record in records.values()
                if record["resources"].get(field) and record["type"] != "SANDWORM"
            ]
        elif path == "src/drawers/cStructureDrawer.cpp" and line_number_int in refinery_pad_lines:
            if argument != "HARVESTER" or field != "bmp":
                raise ValueError(f"{path}:{line_number_int}: unhandled {method_name} argument {argument!r}")
            site = {
                "source": ref,
                "column": converter["draw_index"](converter["face_angles"]["DOWN"]),
                "row": 0,
            }
            target_records = [record for record in records.values() if record["type"] == "HARVESTER"]
        else:
            if argument not in records:
                raise ValueError(f"{path}:{line_number_int}: unknown {method_name} argument {argument!r}")
            raise ValueError(f"{path}:{line_number_int}: unparsed {method_name} draw site for {argument!r}")

        for record in target_records:
            resource = record["resources"].get(field)
            if resource:
                sites_by_resource.setdefault(resource, []).append(site)
    return {
        resource: _dedupe_sites(sites)
        for resource, sites in sites_by_resource.items()
    }


def _dedupe_sites(sites: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[tuple[Any, ...]] = set()
    result = []
    for site in sites:
        key = (
            site["source"]["ref"], site["source"]["identifier"],
            site["column"], site["row"],
        )
        if key not in seen:
            seen.add(key)
            result.append(site)
    return result


def parse_carryall_offset(source: SourceIndex) -> tuple[int, dict[str, Any]]:
    path = "src/gameobjects/units/cUnit.cpp"
    lines = source.function_lines(path, "void cUnit::draw()")
    branch_start = next(
        (index for index, (_, line) in enumerate(lines) if "if (iType == CARRYALL)" in line),
        None,
    )
    if branch_start is None:
        raise ValueError("CARRYALL shadow branch was not found in cUnit::draw")
    depth = 0
    opened = False
    branch: list[tuple[int, str]] = []
    for line_number, line in lines[branch_start:]:
        clean = re.sub(r"//.*$", "", line)
        branch.append((line_number, line))
        depth += clean.count("{") - clean.count("}")
        opened = opened or "{" in clean
        if opened and depth == 0:
            break
    match = next(
        (match for _, line in branch if (match := re.search(r"visualY\s*\+\s*(\d+)", line))),
        None,
    )
    if match is None:
        raise ValueError("CARRYALL visualY offset was not found in its branch")
    offset = int(match.group(1))
    line_number, line = next(
        (line_number, line)
        for line_number, line in branch
        if "visualY" in line and re.search(r"visualY\s*\+\s*\d+", line)
    )
    return offset, {"ref": f"{path}:{line_number}", "identifier": "visualY + " + str(offset)}


def parse_draw_geometry(
    source: SourceIndex,
    density: int,
    density_rule: dict[str, Any],
    tile: dict[str, int],
    tile_refs: list[dict[str, str]],
    direction_rule: dict[str, Any],
) -> dict[str, Any]:
    cpp = "src/gameobjects/units/cUnit.cpp"
    draw_func = "void cUnit::draw()"
    body_index_ref = source.function_ref(
        cpp, draw_func, "const int bmp_body = convertAngleToDrawIndex(iBodyFacing);"
    )
    head_index_ref = source.function_ref(
        cpp, draw_func, "const int bmp_head = convertAngleToDrawIndex(iHeadFacing);"
    )
    start_x_body = source.function_ref(cpp, draw_func, "int start_x = bmp_body * bmp_width;")
    start_y = source.function_ref(cpp, draw_func, "int start_y = bmp_height * iFrame;")
    start_x_top = source.function_ref(cpp, draw_func, "start_x = bmp_head * bmp_width;")
    shadow_render = source.function_ref(cpp, draw_func, "renderStrechSprite(shadow,src, dest, ShadowTrans);")
    body_render = source.function_ref(cpp, draw_func, "renderStrechSprite(bitmap,src, dest);")
    top_render = source.function_ref(cpp, draw_func, "renderStrechSprite(top,src, dest);")

    draw_x_func = "int cUnit::draw_x(int bmpWidth)"
    draw_y_func = "int cUnit::draw_y(int bmpHeight)"
    visual_rectangle_func = "cRectangle cUnit::getVisualRectangle()"
    draw_x_lines = source.function_lines(cpp, draw_x_func)
    draw_y_lines = source.function_lines(cpp, draw_y_func)
    draw_x_expr = next((match.group(1) for _, line in draw_x_lines if (match := re.search(r"int bmpOffset\s*=\s*(.+);", line))), None)
    draw_y_expr = next((match.group(1) for _, line in draw_y_lines if (match := re.search(r"int bmpOffset\s*=\s*(.+);", line))), None)
    if draw_x_expr is None or draw_y_expr is None:
        raise ValueError("unit draw anchor formulas are missing")
    draw_x_sources = unique_refs([
        source.function_ref(cpp, draw_x_func, "(TILESIZE_WIDTH_PIXELS - bmpWidth) / 2"),
        source.function_ref(cpp, draw_x_func, "return mapCamera->getWindowXPositionWithOffset"),
        source.ref("src/map/cMapCamera.h", "return std::round(factorZoomLevel((absoluteXPosition - m_viewportStartX) + offset));"),
    ])
    draw_y_sources = unique_refs([
        source.function_ref(cpp, draw_y_func, "(TILESIZE_HEIGHT_PIXELS - bmpHeight) / 2"),
        source.function_ref(cpp, draw_y_func, "return mapCamera->getWindowYPositionWithOffset"),
        source.ref("src/map/cMapCamera.h", "return std::round(factorZoomLevel((absoluteYPosition - m_viewportStartY) + offset) + m_heightOfTopBar);"),
    ])
    visual_rectangle_sources = unique_refs([
        source.function_ref(cpp, visual_rectangle_func, "mapCamera->factorZoomLevel(getBmpWidth())"),
        source.function_ref(cpp, visual_rectangle_func, "originalWidth * visualScale"),
        source.function_ref(cpp, visual_rectangle_func, "draw_x() - (visualWidth - originalWidth) / 2"),
    ])
    visual_rectangle_y_sources = unique_refs([
        source.function_ref(cpp, visual_rectangle_func, "mapCamera->factorZoomLevel(getBmpHeight())"),
        source.function_ref(cpp, visual_rectangle_func, "originalHeight * visualScale"),
        source.function_ref(cpp, visual_rectangle_func, "draw_y() - (visualHeight - originalHeight) / 2"),
    ])
    world_scale_sources = unique_refs([
        source.ref("src/cGame.h", "return isHdGraphicsActive()"),
        source.ref("src/cGame.h", "static_cast<float>(m_effectiveWorldScalePercent) / 100.0F"),
        source.ref("src/cGame.h", ": 1.0F;"),
    ])
    unit_scale_sources = unique_refs([
        source.function_ref(cpp, visual_rectangle_func, "game.getWorldScaleFactor()"),
        source.function_ref("src/utils/WorldObjectScale.hpp", "inline float unitWorldScaleFactor(", "return worldScaleFactor;"),
    ])

    shadow_trans_path = "src/include/d2tmc.h"
    shadow_trans_match = re.search(
        r"constexpr int ShadowTrans\s*=\s*(\d+)\s*;",
        source.text(shadow_trans_path),
    )
    if shadow_trans_match is None:
        raise ValueError("ShadowTrans numeric definition was not found")
    shadow_trans = int(shadow_trans_match.group(1))
    shadow_trans_ref = source.ref(shadow_trans_path, "constexpr int ShadowTrans")

    carryall_offset, carryall_ref = parse_carryall_offset(source)
    carryall_rule = {
        "value": {"unit_type": "CARRYALL", "visual_y_offset_px": carryall_offset},
        "sources": [carryall_ref],
    }
    body_top_refs = [body_index_ref, head_index_ref]

    graphics_path = "src/utils/Graphics.cpp"
    graphics_text = "\n".join(source.search_lines(graphics_path))
    allowlist = sorted(set(re.findall(r'baseName\s*==\s*"(BUILD_[A-Z0-9_]+)"', graphics_text)))
    mask_refs = [
        source.ref("src/player/cPlayer.cpp", "m_hdTextureReferences = gfxdata->getDensity() > 1;"),
        source.ref("src/player/cPlayer.cpp", "gfxdata->getHouseTexture("),
        source.ref("src/player/cPlayer.cpp", "createTextureFromIndexedSurfaceWithPalette("),
        source.ref("src/player/cPlayer.cpp", "return m_hdTextureReferences"),
        source.ref(graphics_path, "const bool neutralHdStructure ="),
        source.ref(graphics_path, 'baseName.starts_with("BUILD_")'),
        source.ref(graphics_path, '"HV_" + houseCode'),
        source.ref(graphics_path, '"HOUSEVARIANT_" + houseName'),
        source.ref(graphics_path, 'dataPack->getIndexFromName("HM_" + selectedName)'),
        source.ref(graphics_path, 'dataPack->getIndexFromName("HOUSEMASK_" + selectedName)'),
        source.ref(graphics_path, 'dataPack->getIndexFromName("HM_" + baseName)'),
        source.ref(graphics_path, 'dataPack->getIndexFromName("HOUSEMASK_" + baseName)'),
        source.ref(graphics_path, "int selectedIndex = neutralHdStructure || compactVariantName.empty()"),
        source.ref(graphics_path, "if (!neutralHdStructure &&"),
        source.ref(graphics_path, "if (selectedIndex < 0) {"),
        source.ref(graphics_path, "const std::string selectedName = dataPack->getNameFromIndex(selectedIndex);"),
        source.ref(graphics_path, "if (!neutralHdStructure || hasEmbeddedHouseDetails) {"),
        source.ref(graphics_path, "if (maskIndex < 0 && selectedIndex != baseIndex) {"),
        source.ref(graphics_path, "if (mask && mask->w == prepared->w && mask->h == prepared->h)"),
        source.ref(graphics_path, "const float strength ="),
        source.ref(graphics_path, "if (strength >= 0.99F && a != 0) {"),
        source.ref(graphics_path, "(0.299F * r + 0.587F * g + 0.114F * b) / 128.0F;"),
        source.ref(graphics_path, "const float averageMaskedLuminance = maskedLuminancePixels > 0"),
        source.ref(graphics_path, "FactionTintReferenceLuminance;"),
        source.ref(graphics_path, "static_cast<float>(ma) / 255.0F"),
        source.ref(graphics_path, "static_cast<float>(std::max({mr, mg, mb})) / 255.0F"),
        source.ref(graphics_path, "if (strength <= 0.0F || a == 0) {"),
        source.ref(graphics_path, "const float luminance ="),
        source.ref(graphics_path, "const auto tint ="),
        source.ref(graphics_path, "original * (1.0F - strength) +"),
        source.ref(graphics_path, "tint(b, houseColor.b),"),
        source.ref("src/utils/FactionTint.hpp", "constexpr float FactionTintReferenceLuminance = 166.0F / 255.0F;"),
        source.ref("src/utils/FactionTint.hpp", "const float correction = FactionTintReferenceLuminance /"),
        source.ref("src/utils/FactionTint.hpp", "std::max(0.01F, averageLuminance)"),
        source.ref("src/utils/FactionTint.hpp", "target * pixelLuminance * correction,"),
        source.ref("src/utils/cIniGameRessouces.cpp", "gfxdata->getTexture(UNIT_CARRYALL_SHADOW)"),
        source.function_ref(
            "src/player/cPlayer.cpp",
            "Texture *cPlayer::getUnitShadowBitmap(int index)",
            "if (sUnitInfo[index].shadow)",
        ),
        source.ref("src/player/cPlayer.cpp", "bmp_unit[i] = createHouseTexture(unitType.bmp);"),
        source.ref("src/player/cPlayer.cpp", "bmp_unit_top[i] = createHouseTexture(unitType.top);"),
        source.ref("src/utils/cIniGameRessouces.cpp", "gfxdata->getTexture(BUILD_WINDTRAP_SHADOW)"),
    ] + [
        source.ref(graphics_path, f'baseName == "{name}"')
        for name in allowlist
    ]

    return {
        "draw_x": {
            "value": {
                "input": "pos_x()",
                "expression": draw_x_expr,
                "camera_transform": "round(factorZoomLevel((pos_x() - m_viewportStartX) + bmpOffset))",
                "tile_width_px": tile["width"],
            },
            "sources": draw_x_sources,
        },
        "draw_y": {
            "value": {
                "input": "pos_y()",
                "expression": draw_y_expr,
                "camera_transform": "round(factorZoomLevel((pos_y() - m_viewportStartY) + bmpOffset) + m_heightOfTopBar)",
                "tile_height_px": tile["height"],
            },
            "sources": draw_y_sources,
        },
        "visual_rectangle": {
            "value": "originalWidth = lround(factorZoomLevel(getBmpWidth())); visualWidth = lround(originalWidth * visualScale); x = draw_x() - (visualWidth - originalWidth) / 2. draw_x() обозначает левый край исходного кадра; с целочисленным округлением центр остаётся у draw_x() + originalWidth / 2.",
            "sources": visual_rectangle_sources,
        },
        "visual_rectangle_y": {
            "value": "originalHeight = lround(factorZoomLevel(getBmpHeight())); visualHeight = lround(originalHeight * visualScale); y = draw_y() - (visualHeight - originalHeight) / 2. draw_y() обозначает верхний край исходного кадра; с целочисленным округлением центр остаётся у draw_y() + originalHeight / 2.",
            "sources": visual_rectangle_y_sources,
        },
        "world_scale_configuration": {
            "value": "При активной HD-графике getWorldScaleFactor возвращает m_effectiveWorldScalePercent / 100; иначе возвращает 1.0F.",
            "sources": world_scale_sources,
        },
        "unit_world_scale_factor": {
            "value": "getVisualRectangle передаёт game.getWorldScaleFactor() в unitWorldScaleFactor; helper возвращает worldScaleFactor без изменения.",
            "sources": unit_scale_sources,
        },
        "source_rectangle": {
            "value": {
                "body_shadow_start_x": "bmp_body * bmp_width",
                "body_shadow_start_y": "bmp_height * iFrame",
                "top_start_x": "bmp_head * bmp_width",
                "top_start_y": "bmp_height * iFrame",
                "remainder_px": "Прямоугольник чтения имеет размер bmp_width × bmp_height; неполные полосы справа и снизу из remainder_px движок не читает.",
            },
            "sources": unique_refs([
                source.function_ref(cpp, draw_func, "cRectangle src = {start_x, start_y, bmp_width, bmp_height};"),
                start_x_body, start_y, start_x_top,
                body_index_ref, head_index_ref,
            ]),
        },
        "draw_order": {
            "value": {
                "order": ["shadow", "body", "top"],
                "destination": "Тень, корпус и верх используют один visual rectangle; в ветви CARRYALL к y тени добавляется считанное смещение.",
            },
            "sources": unique_refs([shadow_render, body_render, top_render]),
        },
        "draw_destination": {
            "value": {
                "visual_rectangle": "cUnit::draw берёт visual из getVisualRectangle().",
                "destination": "cRectangle dest = {visualX, visualY, roundedScaledWidth, roundedScaledHeight}; размер берётся из visual.getWidth() и visual.getHeight().",
            },
            "sources": unique_refs([
                source.function_ref(cpp, draw_func, "const cRectangle visual = getVisualRectangle();"),
                source.function_ref(cpp, draw_func, "cRectangle dest = {"),
                source.function_ref(cpp, draw_func, "roundedScaledWidth,"),
            ]),
        },
        "start_pixel_fields": {
            "value": "draw() формирует source rectangle через facing и iFrame; bmp_startpixel не читается.",
            "sources": unique_refs([
                start_x_body, start_y,
                source.ref("src/utils/cIniGameRessouces.cpp", "sUnitInfo[HARVESTER].bmp_startpixel = 24;"),
            ]),
        },
        "direction_columns": direction_rule,
        "facing_source": {
            "value": {"body": "iBodyFacing", "shadow": "iBodyFacing", "top": "iHeadFacing", "non_rendered": None},
            "sources": unique_refs(body_top_refs),
        },
        "hd4_density": {
            "value": {"density": density, "source_rect_scaled_by_density": True},
            "sources": density_rule["sources"],
        },
        "shadow_transparency": {
            "value": shadow_trans,
            "sources": unique_refs([shadow_trans_ref, shadow_render]),
        },
        "carryall_shadow_offset": carryall_rule,
        "tile_size": {"value": tile, "sources": unique_refs(tile_refs)},
        "hd_house_masks": {
            "value": {
                "neutral_hd_structure": "При density > 1 имя BUILD_* считается нейтральной HD-структурой.",
                "texture_path": "m_hdTextureReferences устанавливается условием gfxdata->getDensity() > 1 (density > 1): при его истинности вызывается getHouseTexture, иначе — createTextureFromIndexedSurfaceWithPalette.",
                "embedded_house_detail_allowlist": allowlist,
                "mask_lookup_order": [
                    "HM_<selectedName>", "HOUSEMASK_<selectedName>",
                    "HM_<baseName>", "HOUSEMASK_<baseName>",
                ],
                "mask_size_guard": "Если маска существует, она применяется только при совпадении mask->w == prepared->w и mask->h == prepared->h; при несовпадении размеров вся маска молча пропускается.",
                "mask_name_selection": "Для нейтральных зданий HD BUILD_* без встроенных деталей цвета Дома поиск маски выключен. Иначе selectedName берётся из доступного HV_<code>_<base>, затем HOUSEVARIANT_<house>_<base>, а если варианта нет — baseName. HM_<selectedName>/HOUSEMASK_<selectedName> ищется первым; HM_<baseName>/HOUSEMASK_<baseName> проверяется только если selectedIndex != baseIndex, то есть вариант выбран.",
                "excluded_shadows": "UNIT_*_SHADOW и BUILD_*_SHADOW загружаются через getTexture и не проходят через getHouseTexture.",
                "strength": "(mask alpha / 255) * (max(mask RGB) / 255)",
                "average_luminance_pixels": "Непрозрачные пиксели с strength >= 0.99F; luminance = (0.299*r + 0.587*g + 0.114*b) / 128.",
                "pixel_luminance": "(0.299*r + 0.587*g + 0.114*b) / 128",
                "average_luminance_fallback": "FactionTintReferenceLuminance, если подходящих пикселей маски нет.",
                "channel_correction": "FactionTintReferenceLuminance / max(0.01, averageLuminance)",
                "colored_channel": "round(clamp(target * pixelLuminance * correction, 0, 255))",
                "output_channel": "clamp(original * (1-strength) + colored * strength, 0, 255)",
                "skip_pixel": "Пропуск, если strength <= 0.0F или альфа исходного пикселя равна 0.",
                "output_alpha": "Сохраняется исходная альфа пикселя.",
            },
            "sources": unique_refs(mask_refs),
        },
    }


def _role_for_resource(resource: str, records: list[dict[str, Any]], is_mask: bool) -> str:
    fields = {
        field
        for record in records
        for field, assigned in record["resources"].items()
        if assigned == resource
    }
    if is_mask:
        return "mask_top" if fields == {"top"} else "mask_body"
    if "shadow" in fields:
        return "shadow"
    if "top" in fields:
        return "top"
    return "body"


def build_entries(
    source: SourceIndex,
    classic_pack: list,
    hd4_pack: list,
    image_cache: dict[int, Any],
    records: dict[str, dict[str, Any]],
    type_ids: dict[str, int],
    density: int,
    density_rule: dict[str, Any],
    direction_columns: list[dict[str, Any]],
    direction_rule: dict[str, Any],
    converter: dict[str, Any],
    row_usage: dict[str, tuple[str, list[dict[str, str]]]],
    sega_map: dict[str, tuple[str, list[dict[str, str]]]],
    tile: dict[str, int],
    tile_refs: list[dict[str, str]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    by_resource = build_unit_resource_index(records)
    sites_by_resource = parse_draw_sites(source, records, converter)
    draw_rules = parse_draw_geometry(
        source, density, density_rule, tile, tile_refs,
        direction_rule,
    )
    hd4_unit_entries = [
        entry for entry in hd4_pack
        if entry.name.startswith(("UNIT_", "HM_UNIT_"))
    ]
    names = {entry.name for entry in hd4_unit_entries}
    entries: list[dict[str, Any]] = []
    exceptions: list[dict[str, Any]] = []
    entry_by_name: dict[str, dict[str, Any]] = {}

    for pack_entry in hd4_unit_entries:
        hd4_size = image_size(pack_entry, image_cache)
        classic_size = (
            image_size(classic_pack[pack_entry.index], image_cache)
            if pack_entry.index < len(classic_pack)
            else None
        )
        base_name = pack_entry.name.removeprefix("HM_")
        mapped_records = by_resource.get(base_name, [])
        if not mapped_records:
            raise ValueError(f"no unit frame dimensions for atlas {pack_entry.name}")
        sizes = {
            (record["sizes"].get("bmp_width"), record["sizes"].get("bmp_height"))
            for record in mapped_records
        }
        sizes.discard((None, None))
        if len(sizes) != 1:
            raise ValueError(f"ambiguous frame dimensions for atlas {pack_entry.name}: {sizes}")
        width, height = next(iter(sizes))
        frame_classic = [width, height]
        frame_hd4 = [width * density, height * density]
        if hd4_size is None:
            columns = rows = None
            remainder = None
        else:
            columns, remainder_x = divmod(hd4_size[0], frame_hd4[0])
            rows, remainder_y = divmod(hd4_size[1], frame_hd4[1])
            remainder = [remainder_x, remainder_y]
        unit_types = sorted(
            {record["type"] for record in mapped_records},
            key=lambda name: type_ids.get(name, 999),
        )
        is_mask = pack_entry.name.startswith("HM_UNIT_")
        role = _role_for_resource(base_name, mapped_records, is_mask)
        if is_mask:
            painted_entry = base_name
            facing_source = None
            sites = []
        elif role == "top":
            painted_entry = None
            facing_source = "iHeadFacing"
            sites = sites_by_resource.get(pack_entry.name, [])
        elif role == "shadow":
            painted_entry = None
            facing_source = "iBodyFacing"
            sites = sites_by_resource.get(pack_entry.name, [])
        else:
            painted_entry = None
            facing_source = None if "SANDWORM" in unit_types else "iBodyFacing"
            sites = sites_by_resource.get(pack_entry.name, [])

        if is_mask:
            mask_refs = [source.ref("src/utils/Graphics.cpp", 'dataPack->getIndexFromName("HM_" + selectedName)')]
        else:
            mask_refs = []

        if columns is None:
            meanings: list[dict[str, Any]] = []
        elif "SANDWORM" in unit_types:
            meanings = [
                {"column": column, "direction": None, "yaw_deg": None, "meaning": "cUnit::draw не выбирает столбцы UNIT_SANDWORM для червя."}
                for column in range(columns)
            ]
        else:
            meanings = []
            for column in range(columns):
                if column < len(direction_columns):
                    meanings.append(dict(direction_columns[column]))
                else:
                    meanings.append({
                        "column": column,
                        "direction": None,
                        "yaw_deg": None,
                        "meaning": "В исходнике нет направления для этого столбца.",
                    })

        unit_rows = [row_usage[unit_type] for unit_type in unit_types]
        row_value = " ".join(sorted({item[0] for item in unit_rows}))
        row_refs = [ref for _, refs in unit_rows for ref in refs]
        type_refs = [source.ref("src/include/definitions.h", f"#define {unit_type}") for unit_type in unit_types]
        assignment_refs = [
            ref
            for record in mapped_records
            for ref in record["source_refs"].values()
        ]
        site_refs = [site["source"] for site in sites]
        draw_site_entries = [
            {
                "source": site["source"]["ref"],
                "identifier": site["source"]["identifier"],
                "column": site["column"],
                "row": site["row"],
            }
            for site in sites
        ]
        directional_refs = []
        if facing_source:
            directional_refs.append(
                source.function_ref(
                    "src/gameobjects/units/cUnit.cpp",
                    "void cUnit::draw()",
                    f"convertAngleToDrawIndex({facing_source})",
                )
            )
        if pack_entry.name.startswith("UNIT_"):
            mask_name = f"HM_{pack_entry.name}" if f"HM_{pack_entry.name}" in names else None
        else:
            mask_name = None

        if is_mask or role == "shadow":
            sega_reference = None
            sega_refs = []
        else:
            mapped_sega = sega_map.get(pack_entry.name)
            if mapped_sega is None:
                raise ValueError(f"{pack_entry.name}: no Sega AssetSpec mapping for atlas entry")
            sega_reference, sega_refs = mapped_sega

        pack_ref = (
            source.ref("src/utils/Graphics.cpp", 'dataPack->getIndexFromName("HM_" + selectedName)')
            if is_mask
            else source.ref("src/data/gfxdata.h", pack_entry.name)
        )
        entry_sources = unique_refs(
            [pack_ref]
            + assignment_refs + type_refs + row_refs + site_refs + directional_refs
            + direction_rule["sources"] + density_rule["sources"] + mask_refs + sega_refs
            + draw_rules["draw_x"]["sources"] + draw_rules["draw_y"]["sources"]
        )
        record = {
            "index": pack_entry.index,
            "name": pack_entry.name,
            "role": role,
            "unit_types": unit_types,
            "classic_size": classic_size,
            "hd4_size": hd4_size,
            "frame_classic": frame_classic,
            "frame_hd4": frame_hd4,
            "columns": columns,
            "rows": rows,
            "remainder_px": remainder,
            "row_meaning": {"value": row_value, "sources": unique_refs(row_refs)},
            "column_meaning": meanings,
            "facing_source": facing_source,
            "draw_sites": draw_site_entries,
            "house_mask": mask_name,
            "painted_entry": painted_entry,
            "sega_reference": sega_reference,
            "sources": entry_sources,
        }
        entries.append(record)
        entry_by_name[record["name"]] = record

        expected_size = [value * density for value in classic_size] if classic_size else None
        reasons = []
        if expected_size is not None and hd4_size != expected_size:
            reasons.append("HD4-размер не равен classic-размеру, умноженному на 4.")
        if remainder and any(remainder):
            reasons.append("HD4-размер не делится на целое число кадров.")
        if reasons:
            exceptions.append({
                "index": pack_entry.index,
                "name": pack_entry.name,
                "reasons": reasons,
                "classic_size": classic_size,
                "expected_hd4_size": expected_size,
                "hd4_size": hd4_size,
                "frame_hd4": frame_hd4,
                "columns": columns,
                "rows": rows,
                "remainder_px": remainder,
                "sources": entry_sources,
            })

    bodies_by_unit_types: dict[tuple[str, ...], list[dict[str, Any]]] = {}
    for entry in entries:
        if entry["role"] == "body":
            unit_types_key = tuple(entry["unit_types"])
            bodies_by_unit_types.setdefault(unit_types_key, []).append(entry)

    for entry in entries:
        if entry["role"] != "shadow":
            continue
        unit_types_key = tuple(entry["unit_types"])
        body_matches = bodies_by_unit_types.get(unit_types_key, [])
        body_names = [body["name"] for body in body_matches]
        if not body_matches:
            raise ValueError(
                f"{entry['name']}: no body entry matches unit_types {unit_types_key}"
            )
        if len(body_matches) > 1:
            raise ValueError(
                f"{entry['name']}: multiple body entries match unit_types {unit_types_key}: {body_names}"
            )
        body = body_matches[0]
        entry["sega_reference"] = body["sega_reference"]
        entry["sources"] = unique_refs(entry["sources"] + body["sources"])

    for unit_types_key, bodies in bodies_by_unit_types.items():
        if len(bodies) > 1:
            body_names = [body["name"] for body in bodies]
            raise ValueError(
                f"multiple body entries match unit_types {unit_types_key}: {body_names}"
            )

    for entry in entries:
        if not entry["name"].startswith("HM_UNIT_"):
            continue
        painted = entry_by_name.get(entry["painted_entry"])
        if painted is None:
            raise ValueError(f"{entry['name']}: painted entry {entry['painted_entry']!r} was not found")
        entry["facing_source"] = painted["facing_source"]
        entry["draw_sites"] = painted["draw_sites"]
        entry["sega_reference"] = painted["sega_reference"]
        entry["sources"] = unique_refs(entry["sources"] + painted["sources"])
    return entries, exceptions, draw_rules


def parse_structure_specs(
    source: SourceIndex,
    tile: dict[str, int],
    tile_refs: list[dict[str, str]],
) -> list[dict[str, Any]]:
    init_path = "src/utils/cIniGameRessouces.cpp"
    init_text = source.text(init_path)
    default_width_match = re.search(r"structureInfo\.bmp_width\s*=\s*([^;]+);", init_text)
    default_height_match = re.search(r"structureInfo\.bmp_height\s*=\s*([^;]+);", init_text)
    if default_width_match is None or default_height_match is None:
        raise ValueError("structureInfo default dimensions not found")
    default_width = parse_integer_expression(default_width_match.group(1))
    default_height = parse_integer_expression(default_height_match.group(1))
    bodies = {
        match.group(1): match.group(2)
        for match in re.finditer(
            r"sStructureInfo\[(\w+)\]\.bmp\s*=\s*gfxdata->getSurface\((BUILD_\w+)\);",
            init_text,
        )
    }
    shadows = {
        match.group(1): match.group(2)
        for match in re.finditer(
            r"sStructureInfo\[(\w+)\]\.shadow\s*=\s*gfxdata->getTexture\((BUILD_\w+_SHADOW)\);",
            init_text,
        )
    }
    widths = {
        match.group(1): parse_integer_expression(match.group(2))
        for match in re.finditer(r"sStructureInfo\[(\w+)\]\.bmp_width\s*=\s*([^;]+);", init_text)
    }
    heights = {
        match.group(1): parse_integer_expression(match.group(2))
        for match in re.finditer(r"sStructureInfo\[(\w+)\]\.bmp_height\s*=\s*([^;]+);", init_text)
    }
    gfx_path = "src/data/gfxdata.h"
    resource_ids = {
        match.group(1): int(match.group(2))
        for match in re.finditer(
            r"^#define\s+(BUILD_\w+)\s+(\d+)\s+/\*\s*BMP\s*\*/",
            source.text(gfx_path),
            re.MULTILINE,
        )
    }
    specs: list[dict[str, Any]] = []
    for structure_type, body_name in bodies.items():
        shadow_name = shadows.get(structure_type)
        if shadow_name is None:
            continue
        width = widths.get(structure_type, default_width)
        height = heights.get(structure_type, default_height)
        if body_name not in resource_ids or shadow_name not in resource_ids:
            raise ValueError(f"missing gfxdata ID for {structure_type}")
        width_anchor = (
            f"sStructureInfo[{structure_type}].bmp_width ="
            if structure_type in widths
            else "structureInfo.bmp_width ="
        )
        height_anchor = (
            f"sStructureInfo[{structure_type}].bmp_height ="
            if structure_type in heights
            else "structureInfo.bmp_height ="
        )
        specs.append({
            "structure_type": structure_type,
            "body_name": body_name,
            "shadow_name": shadow_name,
            "shadow_id": resource_ids[shadow_name],
            "frame_width": width,
            "frame_height": height,
            "runtime": True,
            "sources": [
                source.ref(init_path, f"sStructureInfo[{structure_type}].bmp = gfxdata->getSurface({body_name});"),
                source.ref(init_path, f"sStructureInfo[{structure_type}].shadow = gfxdata->getTexture({shadow_name});"),
                source.ref(gfx_path, f"#define {body_name}"),
                source.ref(gfx_path, f"#define {shadow_name}"),
                source.ref(init_path, width_anchor),
                source.ref(init_path, height_anchor),
            ],
        })

    prebuild_path = "src/drawers/cStructureDrawer.cpp"
    prebuild_text = source.text(prebuild_path)
    prebuilds = re.finditer(
        r"if\s*\(width\s*==\s*(\d+)\s*&&\s*height\s*==\s*(\d+)\)\s*\{\s*return\s+(BUILD_PRE_\w+);",
        prebuild_text,
    )
    for match in prebuilds:
        width_cells, height_cells = int(match.group(1)), int(match.group(2))
        body_name = match.group(3)
        shadow_name = f"{body_name}_SHADOW"
        if shadow_name not in resource_ids or body_name not in resource_ids:
            raise ValueError(f"missing gfxdata ID for {shadow_name}")
        width = width_cells * tile["width"]
        height = height_cells * tile["height"]
        specs.append({
            "structure_type": body_name.removeprefix("BUILD_"),
            "body_name": body_name,
            "shadow_name": shadow_name,
            "shadow_id": resource_ids[shadow_name],
            "frame_width": width,
            "frame_height": height,
            "runtime": False,
            "sources": [
                source.ref(prebuild_path, f"if (width == {width_cells} && height == {height_cells})"),
                source.ref(prebuild_path, f"return {body_name};"),
                source.ref(gfx_path, f"#define {body_name}"),
                source.ref(gfx_path, f"#define {shadow_name}"),
                *tile_refs,
                source.ref(prebuild_path, "renderDrawer->renderStrechFullSprite(gfxdata->getTexture(iDrawPreBuild), dest);"),
            ],
        })
    return specs


def structure_shadow_offset(source: SourceIndex) -> tuple[list[int] | None, list[dict[str, str]]]:
    path = "src/gameobjects/structures/cAbstractStructure.cpp"
    function = "void cAbstractStructure::drawWithShadow()"
    lines = source.function_lines(path, function)
    expected = {
        "cRectangle src =  {0, iSourceY, pixelWidth, pixelHeight};",
        "renderDrawer->renderStrechSprite(shadow, src, visual, ShadowTrans);",
        "renderDrawer->renderStrechSprite(bitmapToDraw, src, visual);",
    }
    present = {anchor for anchor in expected if any(anchor in line for _, line in lines)}
    if present != expected:
        return None, []
    return [0, 0], [
        source.function_ref(path, function, anchor)
        for anchor in sorted(expected)
    ]


def _centroid(mask: np.ndarray) -> list[float] | None:
    ys, xs = np.nonzero(mask)
    if len(xs) == 0:
        return None
    return [float(xs.mean()), float(ys.mean())]


def build_light(
    source: SourceIndex,
    hd_entries: list,
    image_cache: dict[int, Any],
    density: int,
    tile: dict[str, int],
    tile_refs: list[dict[str, str]],
) -> dict[str, Any]:
    entry_by_name = {entry.name: entry for entry in hd_entries}
    specs = parse_structure_specs(source, tile, tile_refs)
    offset, offset_refs = structure_shadow_offset(source)
    records: list[dict[str, Any]] = []
    excluded: list[dict[str, Any]] = []
    used_shadows: set[str] = set()
    threshold = 16
    for spec in specs:
        body_entry = entry_by_name.get(spec["body_name"])
        shadow_entry = entry_by_name.get(spec["shadow_name"])
        used_shadows.add(spec["shadow_name"])
        sources = list(spec["sources"])
        if not spec["runtime"]:
            sources += [
                source.function_ref(
                    "src/drawers/cStructureDrawer.cpp",
                    "void cStructureDrawer::drawStructurePrebuildAnimation(cAbstractStructure *structure)",
                    "renderDrawer->renderStrechFullSprite(gfxdata->getTexture(iDrawPreBuild), dest);",
                )
            ]
        else:
            sources += offset_refs
        if body_entry is None or shadow_entry is None:
            missing = "корпус" if body_entry is None else "тень"
            excluded.append({
                "structure_type": spec["structure_type"],
                "body_name": spec["body_name"],
                "shadow_name": spec["shadow_name"],
                "reason": f"В HD4 паке отсутствует парная запись {missing}.",
                "sources": unique_refs(sources),
            })
            continue
        body_image = image_for(body_entry, image_cache)
        shadow_image = image_for(shadow_entry, image_cache)
        if body_image is None or shadow_image is None:
            excluded.append({
                "structure_type": spec["structure_type"],
                "body_name": spec["body_name"],
                "shadow_name": spec["shadow_name"],
                "reason": "Парное изображение корпуса или тени не декодируется.",
                "sources": unique_refs(sources),
            })
            continue
        if spec["runtime"] and offset is None:
            excluded.append({
                "structure_type": spec["structure_type"],
                "body_name": spec["body_name"],
                "shadow_name": spec["shadow_name"],
                "reason": "Смещение тени в runtime-коде не удалось вычислить.",
                "sources": unique_refs(sources),
            })
            continue

        frame_width = spec["frame_width"] * density
        frame_height = spec["frame_height"] * density
        body_frame = body_image.convert("RGBA").crop((0, 0, frame_width, frame_height))
        shadow_frame = shadow_image.convert("RGBA").crop((0, 0, frame_width, frame_height))
        body_mask = np.asarray(body_frame.getchannel("A")) > threshold
        shadow_mask = np.asarray(shadow_frame.getchannel("A")) > threshold
        body_centroid = _centroid(body_mask)
        exposed_shadow = shadow_mask & ~body_mask
        shadow_centroid = _centroid(exposed_shadow)
        if body_centroid is None:
            reason = f"Кадр 0 корпуса пуст при alpha > {threshold}."
        elif not shadow_mask.any():
            reason = f"Кадр 0 тени пуст при alpha > {threshold}."
        elif shadow_centroid is None:
            reason = "У пикселей тени вне корпуса нет центроида."
        else:
            reason = None
        measurement_sources = unique_refs(sources + [
            source.ref("src/gameobjects/structures/cAbstractStructure.cpp", "int iSourceY = pixelHeight * iFrame;"),
            source.ref("src/gameobjects/structures/cAbstractStructure.cpp", "cRectangle src =  {0, iSourceY, pixelWidth, pixelHeight};"),
            source.ref("src/drawers/SDLDrawer.cpp", "srcRect.x *= src->density;"),
            source.ref("src/drawers/SDLDrawer.cpp", "srcRect.h *= src->density;"),
        ])
        if reason is not None:
            excluded.append({
                "structure_type": spec["structure_type"],
                "body_name": spec["body_name"],
                "shadow_name": spec["shadow_name"],
                "reason": reason,
                "body_pixels": int(body_mask.sum()),
                "shadow_pixels": int(shadow_mask.sum()),
                "shadow_only_pixels": int(exposed_shadow.sum()),
                "sources": measurement_sources,
            })
            continue
        dx = shadow_centroid[0] - body_centroid[0]
        dy = shadow_centroid[1] - body_centroid[1]
        length = float(math.hypot(dx, dy))
        angle = float(math.degrees(math.atan2(-dy, dx))) if length else None
        record = {
            "structure_type": spec["structure_type"],
            "body_name": spec["body_name"],
            "shadow_name": spec["shadow_name"],
            "shadow_id": spec["shadow_id"],
            "frame_index": 0,
            "frame_size_hd4_px": [frame_width, frame_height],
            "shadow_runtime_rendered": spec["runtime"],
            "alpha_threshold_exclusive": threshold,
            "body_pixels": int(body_mask.sum()),
            "shadow_pixels": int(shadow_mask.sum()),
            "shadow_only_pixels": int(exposed_shadow.sum()),
            "body_centroid_hd4_px": body_centroid,
            "shadow_only_centroid_hd4_px": shadow_centroid,
            "delta_shadow_minus_body_hd4_px": [float(dx), float(dy)],
            "angle_degrees": angle,
            "length_px": length,
            "runtime_offset_hd4_px": offset if spec["runtime"] else None,
            "outlier": False,
            "sources": measurement_sources,
        }
        records.append(record)
        if not spec["runtime"]:
            excluded.append({
                "structure_type": spec["structure_type"],
                "body_name": spec["body_name"],
                "shadow_name": spec["shadow_name"],
                "reason": "PRE_* тень присутствует в паке, но prebuild-код рисует только BUILD_PRE_* тело.",
                "sources": measurement_sources,
            })

    for entry in hd_entries:
        if entry.name.startswith("BUILD_") and entry.name.endswith("_SHADOW") and entry.name not in used_shadows:
            excluded.append({
                "structure_type": entry.name.removeprefix("BUILD_").removesuffix("_SHADOW"),
                "shadow_name": entry.name,
                "reason": "В исходниках нет парной конфигурации BUILD_* тела и тени.",
                "sources": [source.ref("src/data/gfxdata.h", entry.name)],
            })

    runtime_records = [
        item for item in records
        if item["shadow_runtime_rendered"]
    ]
    runtime_angle_records = [item for item in runtime_records if item["angle_degrees"] is not None]
    runtime_angles = [item["angle_degrees"] for item in runtime_angle_records]
    median_angle = min(
        enumerate(runtime_angles),
        key=lambda candidate: (
            sum(
                abs((candidate[1] - angle + 180.0) % 360.0 - 180.0)
                for angle in runtime_angles
            ),
            candidate[0],
        ),
    )[1] if runtime_angles else None
    median_length = statistics.median(item["length_px"] for item in runtime_records) if runtime_records else None
    for item in records:
        if median_angle is not None and item["angle_degrees"] is not None:
            difference = abs((item["angle_degrees"] - median_angle + 180.0) % 360.0 - 180.0)
            item["outlier"] = difference > 45.0

    measurement_refs = unique_refs([
        ref for item in records for ref in item.get("sources", [])
    ])
    return {
        "buildings": records,
        "excluded": excluded,
        "median_angle_degrees": median_angle,
        "median_length_px": median_length,
        "measurement": {
            "frame": "Кадр 0; размеры из cIniGameRessouces.cpp, умноженные на density.",
            "opaque_pixel": f"alpha > {threshold}",
            "shadow_pixels": "маска тени без пикселей корпуса",
            "vector": "centroid(exposed shadow) - centroid(body)",
            "angle": "degrees(atan2(-dy, dx)); 0 вправо, 90 вверх",
            "length": "hypot(dx, dy) в пикселях HD4",
            "median_population": "Для угла и длины используются только записи с shadow_runtime_rendered=true.",
            "median_angle": "Круговая медиана — наблюдаемый runtime-угол с минимальной суммой abs(((a - b + 180) % 360) - 180) по всем runtime-углам; при равенстве сумм выбирается угол, который раньше стоит в исходном списке.",
            "median_length": "Обычная медиана длины — середина отсортированного списка runtime-длин; при чётном числе значений берётся среднее двух центральных.",
            "outlier": "Выброс: круговая разница угла с круговой медианой runtime-записей превышает 45°.",
        },
        "sources": measurement_refs,
    }


def markdown_document(contract: dict[str, Any]) -> str:
    def scalar(value: Any) -> str:
        if value is None:
            return "—"
        if isinstance(value, bool):
            return "да" if value else "нет"
        if isinstance(value, float):
            return f"{value:.1f}"
        if isinstance(value, int):
            return str(value)
        if isinstance(value, str):
            return value.replace("|", "&#124;").replace("\r\n", "<br>").replace("\n", "<br>")
        return str(value)

    def compact(value: Any) -> str:
        if isinstance(value, dict):
            parts = [
                f"{scalar(key)}: {compact(child)}"
                for key, child in value.items()
                if key != "sources"
            ]
            return "; ".join(parts) if parts else "—"
        if isinstance(value, (list, tuple)):
            return ", ".join(compact(item) for item in value) if value else "—"
        return scalar(value)

    def dimensions(value: Any) -> str:
        if not isinstance(value, (list, tuple)):
            return compact(value)
        return " × ".join(scalar(part) for part in value)

    def remainder(value: Any) -> str:
        if not isinstance(value, (list, tuple)) or len(value) != 2:
            return "—"
        parts = [
            f"{axis}: {scalar(amount)}"
            for axis, amount in zip(("Ш", "В"), value)
            if amount != 0
        ]
        return "; ".join(parts) if parts else "—"

    def source_links(sources: list[dict[str, str]]) -> str:
        links = []
        seen = set()
        for source in sources or []:
            reference = source.get("ref")
            if not reference or reference in seen:
                continue
            seen.add(reference)
            source_path, separator, line_number = reference.rpartition(":")
            if not separator or not line_number.isdigit():
                continue
            links.append(f"[{reference}](../../{source_path}#L{line_number})")
            if len(links) == 3:
                break
        return ", ".join(links) if links else "—"

    lines = [
        "# Контракт атласов юнитов",
        "",
        "## Атласы юнитов",
        "",
        "| Индекс | Имя | Роль | Типы | Атлас HD4 (Ш×В) | Кадр HD4 (Ш×В) | Столбцы × строки | Остаток (px) | Маска | Лист Sega |",
        "| ---: | --- | --- | --- | ---: | ---: | ---: | --- | --- | --- |",
    ]
    for entry in contract["entries"]:
        reference = entry.get("sega_reference")
        sega_basename = reference.rsplit("/", 1)[-1] if reference else None
        unit_types = ", ".join(entry.get("unit_types", [])) or "—"
        grid = f"{scalar(entry.get('columns'))} × {scalar(entry.get('rows'))}"
        lines.append(
            "| {index} | `{name}` | {role} | {types} | {atlas} | {frame} | {grid} | {remainder} | {mask} | {sega} |".format(
                index=scalar(entry.get("index")),
                name=scalar(entry.get("name")),
                role=scalar(entry.get("role")),
                types=scalar(unit_types),
                atlas=dimensions(entry.get("hd4_size")),
                frame=dimensions(entry.get("frame_hd4")),
                grid=grid,
                remainder=remainder(entry.get("remainder_px")),
                mask=scalar(entry.get("house_mask")),
                sega=scalar(sega_basename),
            )
        )

    lines.extend([
        "", "## Правила отрисовки", "",
        "| Правило | Значение | Источники |", "| --- | --- | --- |",
    ])
    for rule_name, rule in contract["draw_rules"].items():
        value = rule.get("value", rule) if isinstance(rule, dict) else rule
        sources = rule.get("sources", []) if isinstance(rule, dict) else []
        lines.append(f"| `{scalar(rule_name)}` | {compact(value)} | {source_links(sources)} |")

    light = contract["light"]
    lines.extend([
        "", "## Свет по теням зданий", "",
        f"Медианный угол: {scalar(light.get('median_angle_degrees'))}°; медианная длина: {scalar(light.get('median_length_px'))} px.",
        "", "| Здание | Угол | Длина | Рисует движок | Выброс |", "| --- | ---: | ---: | --- | --- |",
    ])
    for building in light.get("buildings", []):
        names = [building.get("structure_type"), building.get("body_name"), building.get("shadow_name")]
        name = " / ".join(scalar(item) for item in names if item)
        angle = building.get("angle_degrees")
        length = building.get("length_px")
        angle_text = f"{scalar(angle)}°" if angle is not None else "—"
        length_text = f"{scalar(length)} px" if length is not None else "—"
        lines.append(
            f"| `{name}` | {angle_text} | {length_text} | {scalar(building.get('shadow_runtime_rendered'))} | {scalar(building.get('outlier'))} |"
        )
    excluded = light.get("excluded", [])
    lines.extend(["", "### Исключённые измерения", ""])
    if excluded:
        lines.extend(["| Ресурс | Причина |", "| --- | --- |"])
        for item in excluded:
            name = item.get("structure_type") or item.get("shadow_name") or "—"
            lines.append(f"| `{scalar(name)}` | {compact(item.get('reason'))} |")
    else:
        lines.append("Исключённых измерений нет.")

    document = "\n".join(lines) + "\n"
    size_bytes = len(document.encode("utf-8"))
    if size_bytes > 40000:
        raise ValueError(f"UNIT_CONTRACT.md is {size_bytes} bytes; limit is 40000")
    return document


def generate(pack_dir: Path, output_dir: Path) -> dict[str, Any]:
    source = SourceIndex(ROOT)
    classic_pack = read_pack(pack_dir / "sdl_data.dat")
    hd4_pack = read_pack(pack_dir / "sdl_data_hd4.dat")
    image_cache: dict[int, Any] = {}
    records = parse_unit_records(source)
    type_ids = parse_type_ids(source)
    density, density_rule = parse_density(source)
    tile, tile_refs = parse_tile_dimensions(source)
    direction_columns, direction_rule, converter = parse_angle_mapping(source)
    manifest = load_sega_manifest(source)
    infantry_assignments = parse_infantry_assignments(source)
    row_usage = {
        unit_type: unit_row_usage(source, unit_type, infantry_assignments)
        for unit_type in records
    }
    sega_map = sega_mapping(source, manifest, records)
    entries, exceptions, draw_rules = build_entries(
        source,
        classic_pack,
        hd4_pack,
        image_cache,
        records,
        type_ids,
        density,
        density_rule,
        direction_columns,
        direction_rule,
        converter,
        row_usage,
        sega_map,
        tile,
        tile_refs,
    )
    light = build_light(source, hd4_pack, image_cache, density, tile, tile_refs)
    contract = {
        "pack_names": {
            "classic": "sdl_data.dat",
            "hd4": "sdl_data_hd4.dat",
            "hd4_density": density,
        },
        "entries": entries,
        "size_exceptions": exceptions,
        "draw_rules": draw_rules,
        "light": light,
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    json_data = json.dumps(contract, ensure_ascii=False, indent=2) + "\n"
    (output_dir / "unit_contract.json").write_text(json_data, encoding="utf-8", newline="\n")
    (output_dir / "UNIT_CONTRACT.md").write_text(markdown_document(contract), encoding="utf-8", newline="\n")
    return contract


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--pack-dir",
        type=Path,
        default=Path(os.environ["D2TM_PACK_DIR"]) if os.environ.get("D2TM_PACK_DIR") else None,
        help="каталог с sdl_data.dat и sdl_data_hd4.dat; можно задать D2TM_PACK_DIR",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=ROOT / "docs/units",
        help="каталог для unit_contract.json и UNIT_CONTRACT.md",
    )
    args = parser.parse_args(argv)
    if args.pack_dir is None:
        parser.error("укажите --pack-dir или задайте D2TM_PACK_DIR")
    contract = generate(args.pack_dir, args.output_dir)
    print(json.dumps({
        "entries": len(contract["entries"]),
        "size_exceptions": len(contract["size_exceptions"]),
        "light_buildings": len(contract["light"]["buildings"]),
        "light_runtime": sum(item["shadow_runtime_rendered"] for item in contract["light"]["buildings"]),
        "light_excluded": len(contract["light"]["excluded"]),
        "median_angle_degrees": contract["light"]["median_angle_degrees"],
        "median_length_px": contract["light"]["median_length_px"],
        "output_dir": str(args.output_dir),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


