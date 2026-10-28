import json
import math
import os
from pathlib import Path
import re
import statistics
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[3]
PACK_DIR = os.environ.get("D2TM_PACK_DIR")
TOOLS_DIR = ROOT / "tools"
sys.path.insert(0, str(TOOLS_DIR))
BACKTICK = chr(96)
RAW_CPP_STRING_RE = re.compile(r'(?:u8|u|U|L)?R"([^ ()\\\t\r\n]{0,16})\(')


def _is_integer(value):
    return isinstance(value, int) and not isinstance(value, bool)


def _strip_cpp_comments(source):
    output = []
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
            output.append(char)
            index += 1
            state = "string"
            continue

        output.append(char)
        index += 1

    return "".join(output)


def _walk_source_references(value, location="$"):
    if isinstance(value, dict):
        if "ref" in value:
            yield value["ref"], value.get("identifier"), f"{location}.ref"
        if "source" in value:
            yield value["source"], value.get("identifier"), f"{location}.source"
        for key, child in value.items():
            yield from _walk_source_references(child, f"{location}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from _walk_source_references(child, f"{location}[{index}]")


def _count_source_fields(value):
    count = 0
    if isinstance(value, dict):
        if "sources" in value:
            assert isinstance(value["sources"], list), "sources must be a list"
            assert value["sources"], "sources must not be empty"
            count += 1
        for child in value.values():
            count += _count_source_fields(child)
    elif isinstance(value, list):
        for child in value:
            count += _count_source_fields(child)
    return count


def _section_lines(markdown, heading, level):
    lines = markdown.splitlines()
    start = next(
        (index for index, line in enumerate(lines) if line.strip() == heading),
        None,
    )
    assert start is not None, f"missing Markdown section: {heading}"
    end = len(lines)
    for index in range(start + 1, len(lines)):
        line = lines[index]
        if line.startswith("#"):
            heading_level = len(line) - len(line.lstrip("#"))
            if heading_level <= level:
                end = index
                break
    return lines[start + 1:end]


def _markdown_table_data_rows(lines):
    rows = []
    for line in lines:
        stripped = line.strip()
        if not (stripped.startswith("|") and stripped.endswith("|")):
            continue
        cells = [cell.strip() for cell in stripped[1:-1].split("|")]
        if all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells):
            continue
        rows.append(cells)
    return rows[1:] if rows else []


def check_grid_and_size_exceptions(contract, markdown):
    entries = contract["entries"]
    required_fields = {
        "index",
        "name",
        "role",
        "unit_types",
        "hd4_size",
        "classic_size",
        "frame_classic",
        "frame_hd4",
        "columns",
        "rows",
        "remainder_px",
        "row_meaning",
        "column_meaning",
        "facing_source",
        "draw_sites",
        "painted_entry",
        "house_mask",
        "sega_reference",
        "sources",
    }
    roles = {"body", "top", "shadow", "mask_body", "mask_top"}
    expected_exception_indices = set()

    for entry in entries:
        name = entry.get("name")
        assert required_fields.issubset(entry), f"{name}: missing contract fields"
        assert entry["role"] in roles, f"{name}: unsupported role"
        assert isinstance(entry["unit_types"], list) and entry["unit_types"], (
            f"{name}: unit_types is empty"
        )
        assert entry["row_meaning"], f"{name}: row_meaning is empty"
        assert isinstance(entry["column_meaning"], list) and entry["column_meaning"], (
            f"{name}: column_meaning is empty"
        )

        frame_classic = entry["frame_classic"]
        frame_hd4 = entry["frame_hd4"]
        hd4_size = entry["hd4_size"]
        assert isinstance(frame_classic, list) and len(frame_classic) == 2, (
            f"{name}: frame_classic must have two dimensions"
        )
        assert all(_is_integer(value) and value > 0 for value in frame_classic), (
            f"{name}: frame_classic dimensions must be positive integers"
        )
        assert frame_hd4 == [dimension * 4 for dimension in frame_classic], (
            f"{name}: frame_hd4 must be four times frame_classic"
        )
        assert isinstance(hd4_size, list) and len(hd4_size) == 2, (
            f"{name}: hd4_size must have two dimensions"
        )
        assert all(_is_integer(value) and value > 0 for value in hd4_size), (
            f"{name}: hd4_size dimensions must be positive integers"
        )
        assert all(_is_integer(value) and value > 0 for value in frame_hd4), (
            f"{name}: frame_hd4 dimensions must be positive integers"
        )

        classic_size = entry["classic_size"]
        assert classic_size is None or (
            isinstance(classic_size, list)
            and len(classic_size) == 2
            and all(_is_integer(value) and value > 0 for value in classic_size)
        ), f"{name}: classic_size must be null or two positive integers"

        columns = entry["columns"]
        rows = entry["rows"]
        remainder = entry["remainder_px"]
        assert _is_integer(columns) and columns > 0, f"{name}: columns must be positive"
        assert _is_integer(rows) and rows > 0, f"{name}: rows must be positive"
        assert isinstance(remainder, list) and len(remainder) == 2, (
            f"{name}: remainder_px must have two dimensions"
        )
        assert all(
            _is_integer(value) and 0 <= value < frame_hd4[axis]
            for axis, value in enumerate(remainder)
        ), f"{name}: remainder_px must be an integer frame remainder"
        assert columns == hd4_size[0] // frame_hd4[0], (
            f"{name}: columns are not the complete frame count"
        )
        assert rows == hd4_size[1] // frame_hd4[1], (
            f"{name}: rows are not the complete frame count"
        )
        assert [
            columns * frame_hd4[0] + remainder[0],
            rows * frame_hd4[1] + remainder[1],
        ] == hd4_size, f"{name}: frame grid and remainder do not recover hd4_size"

        scale_mismatch = classic_size is not None and hd4_size != [
            dimension * 4 for dimension in classic_size
        ]
        if scale_mismatch or any(remainder):
            expected_exception_indices.add(entry["index"])

    exceptions = contract["size_exceptions"]
    exception_indices = [exception["index"] for exception in exceptions]
    assert len(exception_indices) == len(set(exception_indices)), (
        "size_exceptions contains duplicate indexes"
    )
    assert set(exception_indices) == expected_exception_indices, (
        "size_exceptions does not match scale differences and nonzero remainders"
    )
    for entry in entries:
        if any(entry["remainder_px"]):
            assert entry["index"] in set(exception_indices), (
                f"{entry['name']}: nonzero remainder is missing from size_exceptions"
            )

    by_name = {entry["name"]: entry for entry in entries}
    fixed_sizes = {
        "UNIT_SIEGEBASE": {
            "hd4_size": [1152, 152],
            "frame_hd4": [144, 144],
            "remainder_px": [0, 8],
            "columns": 8,
        },
        "UNIT_DEVASTATOR": {
            "hd4_size": [1216, 192],
            "frame_hd4": [152, 184],
            "remainder_px": [0, 8],
            "columns": 8,
        },
    }
    for name, expected in fixed_sizes.items():
        assert name in by_name, f"missing required atlas: {name}"
        for field, value in expected.items():
            assert by_name[name][field] == value, f"{name}: unexpected {field}"

    carryall_shadow = by_name["UNIT_CARRYALL_SHADOW"]
    assert carryall_shadow["classic_size"] is not None
    assert carryall_shadow["hd4_size"] != [
        dimension * 4 for dimension in carryall_shadow["classic_size"]
    ]
    carryall_exception = next(
        (
            exception
            for exception in exceptions
            if exception["index"] == carryall_shadow["index"]
        ),
        None,
    )
    assert carryall_exception is not None, (
        "UNIT_CARRYALL_SHADOW: classic×4 mismatch is absent from size_exceptions"
    )
    for key in ("classic_size", "expected_hd4_size", "reasons"):
        assert key in carryall_exception, (
            f"UNIT_CARRYALL_SHADOW: exception lacks {key}"
        )
    assert any(
        "classic" in reason.lower() and "4" in reason
        for reason in carryall_exception["reasons"]
    ), "UNIT_CARRYALL_SHADOW: exception does not explain the classic×4 mismatch"


def check_house_masks(contract, markdown):
    entries = contract["entries"]
    by_name = {entry["name"]: entry for entry in entries}
    assert len(by_name) == len(entries), "entry names must be unique"

    for entry in entries:
        name = entry["name"]
        if name.startswith("HM_UNIT_"):
            painted_name = name[len("HM_"):]
            assert entry["painted_entry"] == painted_name, (
                f"{name}: painted_entry must name {painted_name}"
            )
            assert painted_name in by_name, f"{name}: painted atlas is missing"
            painted = by_name[painted_name]
            assert entry["hd4_size"] == painted["hd4_size"], (
                f"{name}: size differs from {painted_name}"
            )
            assert painted["house_mask"] == name, (
                f"{painted_name}: house_mask does not name {name}"
            )

        mask_name = entry["house_mask"]
        if mask_name is not None:
            assert mask_name in by_name, f"{name}: house mask is missing"
            assert entry["hd4_size"] == by_name[mask_name]["hd4_size"], (
                f"{name}: size differs from {mask_name}"
            )

    mask_rules = contract["draw_rules"]["hd_house_masks"]
    value = mask_rules["value"]
    required_fields = {
        "neutral_hd_structure",
        "embedded_house_detail_allowlist",
        "mask_lookup_order",
        "mask_size_guard",
        "mask_name_selection",
        "excluded_shadows",
        "strength",
        "average_luminance_pixels",
        "pixel_luminance",
        "average_luminance_fallback",
        "channel_correction",
        "colored_channel",
        "output_channel",
        "skip_pixel",
        "output_alpha",
        "texture_path",
    }
    assert required_fields.issubset(value), (
        f"missing mask rule fields: {sorted(required_fields - value.keys())}"
    )
    expected_lookup = [
        "HM_<selectedName>",
        "HOUSEMASK_<selectedName>",
        "HM_<baseName>",
        "HOUSEMASK_<baseName>",
    ]
    assert value["mask_lookup_order"] == expected_lookup, (
        "mask_lookup_order does not include both selected and base names"
    )
    assert value["embedded_house_detail_allowlist"], (
        "embedded house detail allowlist is empty"
    )
    assert all(
        fragment in value["mask_size_guard"]
        for fragment in ("mask->w == prepared->w", "mask->h == prepared->h")
    ), "mask_size_guard omits a dimension comparison"
    assert all(
        fragment in value["mask_name_selection"]
        for fragment in ("HV_", "HOUSEVARIANT_")
    ), "mask_name_selection omits an HD house variant format"
    assert all(
        fragment in value["excluded_shadows"]
        for fragment in ("UNIT_*_SHADOW", "getTexture")
    ), "excluded_shadows does not identify unit shadow loading"
    assert "density > 1" in value["neutral_hd_structure"]
    assert "BUILD_*" in value["neutral_hd_structure"]

    texture_path = value["texture_path"]
    assert isinstance(texture_path, str), "texture_path must be text"
    for condition in (
        "m_hdTextureReferences",
        "density > 1",
        "getHouseTexture",
        "createTextureFromIndexedSurfaceWithPalette",
    ):
        assert condition in texture_path, (
            f"texture_path omits the {condition} condition"
        )

    graphics_source = (ROOT / "src/utils/Graphics.cpp").read_text(encoding="utf-8")
    for name in value["embedded_house_detail_allowlist"]:
        assert name in graphics_source, (
            f"embedded house detail is absent from Graphics.cpp: {name}"
        )

    source_links = mask_rules["sources"]
    identifiers = {item["identifier"] for item in source_links}
    source_requirements = {
        "HM lookup": 'getIndexFromName("HM_" + selectedName)',
        "pixel skip": "strength <= 0.0F",
        "luminance calculation": "averageMaskedLuminance",
        "mask size guard": "if (mask && mask->w == prepared->w && mask->h == prepared->h)",
        "compact variant": '"HV_" + houseCode',
        "legacy variant": '"HOUSEVARIANT_" + houseName',
        "unit shadow loading": "getTexture(UNIT_CARRYALL_SHADOW)",
        "unit shadow access": "sUnitInfo[index].shadow",
    }
    for description, identifier in source_requirements.items():
        assert any(identifier in source_identifier for source_identifier in identifiers), (
            f"mask rules have no source link for {description}"
        )

    texture_path_sources = [
        item
        for item in source_links
        if item["ref"].startswith("src/player/cPlayer.cpp:")
    ]
    assert texture_path_sources, "texture_path has no cPlayer.cpp source links"
    for identifier in (
        "m_hdTextureReferences =",
        "getDensity() > 1",
        "return m_hdTextureReferences",
        "getHouseTexture(",
        "createTextureFromIndexedSurfaceWithPalette(",
    ):
        assert any(identifier in item["identifier"] for item in texture_path_sources), (
            f"texture_path source links omit {identifier}"
        )


def check_source_references(contract, markdown):
    entries = contract["entries"]
    for index, entry in enumerate(entries):
        assert entry["sources"], f"entries[{index}] has no sources"
    assert _count_source_fields(entries) > 0, "entries have no sources"
    assert _count_source_fields(contract["draw_rules"]) > 0, (
        "draw_rules has no sources"
    )
    assert _count_source_fields(contract["light"]) > 0, "light has no sources"

    root = ROOT.resolve()
    source_lines_by_path = {}
    for reference, identifier, label in _walk_source_references(contract):
        assert isinstance(reference, str) and reference, (
            f"invalid source reference at {label}: {reference}"
        )
        assert isinstance(identifier, str) and identifier.strip(), (
            f"empty source identifier at {label}: {reference}"
        )
        source_path, separator, line_number = reference.rpartition(":")
        assert separator and line_number.isdigit(), (
            f"invalid source line reference at {label}: {reference}"
        )
        source_file = (ROOT / source_path).resolve()
        assert source_file.is_relative_to(root), (
            f"source reference escapes the repository: {reference}"
        )
        assert source_file.is_file(), f"source file is missing: {reference}"
        relative_path = source_file.relative_to(root)
        if relative_path not in source_lines_by_path:
            source_text = source_file.read_text(encoding="utf-8")
            source_lines_by_path[relative_path] = _strip_cpp_comments(
                source_text
            ).splitlines()
        lines = source_lines_by_path[relative_path]
        line_index = int(line_number) - 1
        assert line_index >= 0, f"source line must be positive: {reference}"
        assert line_index < len(lines), f"source line does not exist: {reference}"
        assert identifier in lines[line_index], (
            f"identifier is absent from executable source at {reference}: {identifier}"
        )

    facing_values = set()
    by_name = {entry["name"]: entry for entry in entries}
    harvester_sites = None
    for entry in entries:
        name = entry["name"]
        assert "facing_source" in entry, f"{name}: facing_source is missing"
        facing_source = entry["facing_source"]
        assert facing_source in {"iBodyFacing", "iHeadFacing", None}, (
            f"{name}: facing_source has an unsupported value"
        )
        facing_values.add(facing_source)
        if facing_source is not None:
            source_text = json.dumps(entry["sources"], ensure_ascii=False)
            assert facing_source in source_text, (
                f"{name}: facing_source has no matching source link"
            )

        draw_sites = entry.get("draw_sites")
        assert isinstance(draw_sites, list), f"{name}: draw_sites must be a list"
        for site in draw_sites:
            assert isinstance(site, dict), f"{name}: draw site must be an object"
            assert isinstance(site.get("source"), str) and site["source"], (
                f"{name}: draw site lacks a source link"
            )
            assert isinstance(site.get("identifier"), str) and site["identifier"], (
                f"{name}: draw site lacks a source identifier"
            )
            assert isinstance(site.get("column"), (int, str)) and not isinstance(
                site.get("column"), bool
            ), f"{name}: draw site column must be a number or text"
            assert isinstance(site.get("row"), (int, str)) and not isinstance(
                site.get("row"), bool
            ), f"{name}: draw site row must be a number or text"

        if name == "UNIT_HARVESTER":
            harvester_sites = draw_sites
        elif name == "UNIT_SANDWORM":
            continue
        elif name.startswith("HM_UNIT_"):
            painted_name = entry.get("painted_entry")
            painted = by_name.get(painted_name) if isinstance(painted_name, str) else None
            assert draw_sites or (painted is not None and painted.get("draw_sites")), (
                f"{name}: no draw sites to inherit from its painted atlas"
            )
        else:
            assert draw_sites, f"{name}: draw_sites is empty"

    assert "iBodyFacing" in facing_values, "no entry identifies iBodyFacing"
    assert "iHeadFacing" in facing_values, "no entry identifies iHeadFacing"
    assert harvester_sites is not None, "UNIT_HARVESTER has no draw_sites"
    assert any(
        "src/drawers/cStructureDrawer.cpp" in site["source"]
        and site["column"] == 6
        and site["row"] == 0
        and "getUnitBitmap(HARVESTER)" in site["identifier"]
        for site in harvester_sites
    ), "UNIT_HARVESTER lacks the refinery-pad draw site at column 6, row 0"


def check_direction_columns(contract, markdown):
    expected_directions = ["E", "NE", "N", "NW", "W", "SW", "S", "SE"]
    expected_yaws = [45 * index for index in range(len(expected_directions))]
    direction_columns = contract["draw_rules"]["direction_columns"]["value"]
    assert isinstance(direction_columns, list), (
        "draw_rules.direction_columns must be an ordered list"
    )
    assert [item.get("direction") for item in direction_columns] == expected_directions, (
        "draw_rules.direction_columns direction order is incorrect"
    )
    assert [item.get("yaw_deg") for item in direction_columns] == expected_yaws, (
        "draw_rules.direction_columns yaw order is incorrect"
    )
    assert [item.get("column") for item in direction_columns] == list(range(8)), (
        "draw_rules.direction_columns indexes are incorrect"
    )

    facing_values = set()
    for entry in contract["entries"]:
        name = entry["name"]
        meanings = entry["column_meaning"]
        columns = entry["columns"]
        assert isinstance(meanings, list), f"{name}: column_meaning must be a list"
        assert len(meanings) == columns, (
            f"{name}: column_meaning length differs from columns"
        )
        assert [meaning.get("column") for meaning in meanings] == list(
            range(columns)
        ), f"{name}: column indexes do not match list positions"

        facing_source = entry["facing_source"]
        assert facing_source in {"iBodyFacing", "iHeadFacing", None}, (
            f"{name}: facing_source has an unsupported value"
        )
        facing_values.add(facing_source)
        if facing_source is not None:
            assert columns == len(expected_directions), (
                f"{name}: directional atlas must have eight columns"
            )
            assert all(
                meaning.get("direction") is not None
                and meaning.get("yaw_deg") is not None
                for meaning in meanings
            ), f"{name}: every directional column needs a direction and yaw"
            assert [meaning["direction"] for meaning in meanings] == expected_directions, (
                f"{name}: direction order is incorrect"
            )
            assert [meaning["yaw_deg"] for meaning in meanings] == expected_yaws, (
                f"{name}: yaw order is incorrect"
            )
        else:
            for index, meaning in enumerate(meanings):
                assert meaning.get("direction") is None, (
                    f"{name} column {index}: non-direction has a direction"
                )
                assert meaning.get("yaw_deg") is None, (
                    f"{name} column {index}: non-direction has a yaw"
                )
                text = meaning.get("meaning")
                assert isinstance(text, str) and text.strip(), (
                    f"{name} column {index}: non-direction needs a meaning"
                )

    assert "iBodyFacing" in facing_values, "no entry identifies iBodyFacing"
    assert "iHeadFacing" in facing_values, "no entry identifies iHeadFacing"


def check_sega_references(contract, markdown):
    reference_root = ROOT / (
        "resources/hd/source_references/battle_for_arrakis_complete"
    )
    manifest = json.loads((reference_root / "manifest.json").read_text(encoding="utf-8"))
    manifest_files = {item["file"] for item in manifest["files"]}
    for item in manifest["files"]:
        assert (reference_root / item["file"]).is_file(), (
            f"manifest file is missing: {item['file']}"
        )

    entries = contract["entries"]
    by_name = {entry["name"]: entry for entry in entries}
    for entry in entries:
        name = entry["name"]
        reference = entry["sega_reference"]
        assert isinstance(reference, str) and reference, (
            f"{name}: sega_reference must not be null"
        )
        path = (ROOT / reference).resolve()
        assert path.is_relative_to(ROOT.resolve()), (
            f"{name}: Sega reference escapes the repository"
        )
        assert path.is_file(), f"{name}: Sega reference file is missing: {reference}"
        assert path.name in manifest_files, (
            f"{name}: Sega reference is absent from manifest.files: {reference}"
        )

    expected_references = {
        "UNIT_LAUNCHER": "550380_missile_tank_deviator.png",
        "UNIT_LAUNCHER_SHADOW": "550380_missile_tank_deviator.png",
        "HM_UNIT_LAUNCHER": "550380_missile_tank_deviator.png",
        "UNIT_FRIGATE": "550136_starport_ship.png",
        "UNIT_FRIGATE_SHADOW": "550136_starport_ship.png",
        "UNIT_SABOTEUR": "169099_soldier_infantry.png",
        "HM_UNIT_SABOTEUR": "169099_soldier_infantry.png",
        "UNIT_SINGLEFREMEN": "169099_soldier_infantry.png",
        "HM_UNIT_SINGLEFREMEN": "169099_soldier_infantry.png",
        "UNIT_TRIPLEFREMEN": "169099_soldier_infantry.png",
        "HM_UNIT_TRIPLEFREMEN": "169099_soldier_infantry.png",
        "UNIT_SONICTANK": "550030_siege_tank.png",
        "UNIT_SONICTANK_SHADOW": "550030_siege_tank.png",
        "HM_UNIT_SONICTANK": "550030_siege_tank.png",
        "UNIT_SIEGEBASE": "550030_siege_tank.png",
        "UNIT_SIEGEBASE_SHADOW": "550030_siege_tank.png",
        "UNIT_SIEGETOP": "550030_siege_tank.png",
        "HM_UNIT_SIEGEBASE": "550030_siege_tank.png",
        "HM_UNIT_SIEGETOP": "550030_siege_tank.png",
        "UNIT_DEVASTATOR": "550032_devastator.png",
        "UNIT_DEVASTATOR_SHADOW": "550032_devastator.png",
        "HM_UNIT_DEVASTATOR": "550032_devastator.png",
    }
    for name, filename in expected_references.items():
        assert name in by_name, f"missing Sega-mapped entry: {name}"
        assert Path(by_name[name]["sega_reference"]).name == filename, (
            f"{name}: expected Sega reference {filename}"
        )


def check_markdown_contract(contract, markdown):
    assert isinstance(markdown, str) and markdown, "Markdown contract is empty"
    assert len(markdown.encode("utf-8")) <= 40000, (
        "Markdown contract exceeds 40000 bytes"
    )

    entries = contract["entries"]
    unit_rows = _markdown_table_data_rows(
        _section_lines(markdown, "## Атласы юнитов", 2)
    )
    assert len(unit_rows) == len(entries), (
        "unit Markdown rows must match the number of contract entries"
    )
    markdown_names = []
    for row in unit_rows:
        assert len(row) >= 2, "unit Markdown row is missing its name"
        assert row[1].startswith(BACKTICK) and row[1].endswith(BACKTICK), (
            "unit Markdown name must be enclosed in backticks"
        )
        markdown_names.append(row[1][1:-1])
    expected_names = [entry["name"] for entry in entries]
    assert markdown_names == expected_names, (
        "unit Markdown must contain exactly one row for every entry name in order"
    )
    assert len(set(markdown_names)) == len(markdown_names), (
        "unit Markdown contains duplicate entry rows"
    )

    rule_rows = _markdown_table_data_rows(
        _section_lines(markdown, "## Правила отрисовки", 2)
    )
    rule_names = []
    for row in rule_rows:
        assert row, "draw rule Markdown row is empty"
        assert row[0].startswith(BACKTICK) and row[0].endswith(BACKTICK), (
            "draw rule Markdown key must be enclosed in backticks"
        )
        rule_names.append(row[0][1:-1])
    expected_rule_names = list(contract["draw_rules"])
    assert len(rule_rows) == len(expected_rule_names), (
        "draw rule Markdown rows must match the number of contract rules"
    )
    assert rule_names == expected_rule_names, (
        "draw rule Markdown must contain every contract key exactly once"
    )

    light = contract["light"]
    light_section = _section_lines(markdown, "## Свет по теням зданий", 2)
    excluded_heading = "### Исключённые измерения"
    excluded_index = next(
        (
            index
            for index, line in enumerate(light_section)
            if line.strip() == excluded_heading
        ),
        None,
    )
    assert excluded_index is not None, "light excluded measurements need a separate section"
    building_rows = _markdown_table_data_rows(light_section[:excluded_index])
    excluded_rows = _markdown_table_data_rows(light_section[excluded_index + 1:])
    assert len(building_rows) == len(light["buildings"]), (
        "light Markdown building rows must match light.buildings"
    )
    assert len(excluded_rows) == len(light["excluded"]), (
        "excluded light Markdown rows must match light.excluded"
    )

    buildings = light["buildings"]
    runtime = [
        building
        for building in buildings
        if building["shadow_runtime_rendered"]
    ]
    assert runtime, "light has no runtime-rendered buildings"
    assert all(
        not building["structure_type"].startswith("PRE_")
        for building in runtime
    ), "prebuild shadows are included among runtime buildings"

    excluded = light.get("excluded")
    assert isinstance(excluded, list), "light.excluded must be a list"
    excluded_names = {item.get("structure_type") for item in excluded}
    assert {"PRE_1X1", "PRE_2X2", "PRE_3X2", "PRE_3X3"}.issubset(
        excluded_names
    ), "light.excluded must list all four non-runtime prebuild shadows"
    for item in excluded:
        assert item.get("reason", "").strip(), (
            f"{item.get('structure_type')}: excluded light item lacks a reason"
        )

    required_fields = {"angle_degrees", "length_px", "outlier"}
    missing = [
        building["structure_type"]
        for building in buildings
        if not required_fields.issubset(building)
    ]
    assert not missing, (
        f"buildings lack angle_degrees, length_px, or outlier: {missing}"
    )
    for building in buildings:
        assert isinstance(building["angle_degrees"], (int, float)) and not isinstance(
            building["angle_degrees"], bool
        ), f"{building['structure_type']}: angle_degrees must be numeric"
        assert isinstance(building["length_px"], (int, float)) and not isinstance(
            building["length_px"], bool
        ), f"{building['structure_type']}: length_px must be numeric"
        assert isinstance(building["outlier"], bool), (
            f"{building['structure_type']}: outlier must be boolean"
        )

    def circular_delta(first, second):
        return abs((first - second + 180) % 360 - 180)

    runtime_angles = [building["angle_degrees"] for building in runtime]
    expected_median_angle = min(
        enumerate(runtime),
        key=lambda item: (
            sum(
                circular_delta(item[1]["angle_degrees"], angle)
                for angle in runtime_angles
            ),
            item[0],
        ),
    )[1]["angle_degrees"]
    assert abs(light["median_angle_degrees"] - expected_median_angle) <= 1e-9, (
        "median_angle_degrees is not the circular L1 median of runtime buildings"
    )
    expected_median_length = statistics.median(
        building["length_px"] for building in runtime
    )
    assert abs(light.get("median_length_px", float("inf")) - expected_median_length) <= 1e-9, (
        "median_length_px is not the median of runtime buildings"
    )

    outlier_names = set()
    for building in buildings:
        delta = circular_delta(
            building["angle_degrees"],
            light["median_angle_degrees"],
        )
        assert building["outlier"] == (delta > 45), (
            f"{building['structure_type']}: outlier flag disagrees with circular angle delta"
        )
        if building["outlier"]:
            outlier_names.add(building["structure_type"])
    assert {"REPAIR", "WOR", "STARPORT"}.issubset(outlier_names), (
        "runtime angle outliers are not identified"
    )


@unittest.skipUnless(PACK_DIR, "D2TM_PACK_DIR is not set")
class UnitContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from hd_assets import decode_image, read_pack

        cls.decode_image = staticmethod(decode_image)
        cls.pack_dir = Path(PACK_DIR)
        cls.hd4_pack = read_pack(cls.pack_dir / "sdl_data_hd4.dat")
        cls.classic_pack = read_pack(cls.pack_dir / "sdl_data.dat")
        cls.contract_path = ROOT / "docs/units/unit_contract.json"
        cls.markdown_path = ROOT / "docs/units/UNIT_CONTRACT.md"
        cls.script_path = ROOT / "tools/units3d/unit_contract.py"

    @property
    def contract(self):
        return json.loads(self.contract_path.read_text(encoding="utf-8"))

    @property
    def markdown(self):
        return self.markdown_path.read_text(encoding="utf-8")

    def test_generated_files_match_committed_files(self):
        with tempfile.TemporaryDirectory() as temporary:
            output_dir = Path(temporary)
            result = subprocess.run(
                [
                    sys.executable,
                    str(self.script_path),
                    "--pack-dir",
                    str(self.pack_dir),
                    "--output-dir",
                    str(output_dir),
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(
                result.returncode,
                0,
                msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
            )
            self.assertEqual(
                (output_dir / "unit_contract.json").read_bytes(),
                self.contract_path.read_bytes(),
            )
            self.assertEqual(
                (output_dir / "UNIT_CONTRACT.md").read_bytes(),
                self.markdown_path.read_bytes(),
            )

    def test_inventory_and_sizes_match_packs(self):
        hd4_units = [
            entry
            for entry in self.hd4_pack
            if entry.name.startswith(("UNIT_", "HM_UNIT_"))
        ]
        contract_entries = self.contract["entries"]
        contract_by_index = {entry["index"]: entry for entry in contract_entries}

        self.assertEqual(
            [(entry["index"], entry["name"]) for entry in contract_entries],
            [(entry.index, entry.name) for entry in hd4_units],
        )

        for hd4_entry in hd4_units:
            with self.subTest(index=hd4_entry.index, name=hd4_entry.name):
                record = contract_by_index[hd4_entry.index]
                self.assertEqual(record["name"], hd4_entry.name)
                hd4_image = self.decode_image(hd4_entry.payload)
                self.assertIsNotNone(hd4_image, "HD4 entry is not a decodable image")
                self.assertEqual(record["hd4_size"], list(hd4_image.size))

                if hd4_entry.index < len(self.classic_pack):
                    classic_image = self.decode_image(
                        self.classic_pack[hd4_entry.index].payload
                    )
                    classic_size = (
                        list(classic_image.size) if classic_image is not None else None
                    )
                else:
                    classic_size = None
                self.assertEqual(record["classic_size"], classic_size)

    def test_grid_and_size_exception_contract(self):
        check_grid_and_size_exceptions(self.contract, self.markdown)

    def test_house_masks_and_rules_match_painted_entries(self):
        check_house_masks(self.contract, self.markdown)

    def test_all_source_references_resolve_to_executable_lines(self):
        check_source_references(self.contract, self.markdown)

    def test_direction_columns_match_engine_order_and_yaw(self):
        check_direction_columns(self.contract, self.markdown)

    def test_sega_references_are_manifest_files(self):
        check_sega_references(self.contract, self.markdown)

    def test_markdown_sections_and_light_contract(self):
        check_markdown_contract(self.contract, self.markdown)


if __name__ == "__main__":
    unittest.main()
