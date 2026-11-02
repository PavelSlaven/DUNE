import argparse
import sys
from itertools import permutations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_geometry

UNIT_PREFIX = "units-label-"
HARVESTER_SCENE = UNIT_PREFIX + "harvester"
UNIT_KINDS = ("health", "group", "experience")


def at_top(o, v):
    return o["y"] - v["y"] <= o["h"]


def at_right(o, v):
    return (v["x"] + v["w"]) - (o["x"] + o["w"]) <= o["w"]


def at_bottom(o, v):
    return (v["y"] + v["h"]) - (o["y"] + o["h"]) <= o["h"]


STRUCTURE_EDGES = {"structure-label-top": ("top", at_top), "structure-label-right": ("right", at_right)}


def objects_of(records, kinds):
    objects = {}
    for record in records:
        if record.get("k") == "label" and record["kind"] in kinds:
            entry = objects.setdefault(record["obj"], {"owner": record["owner"], "kinds": set(), "groups": []})
            entry["kinds"].add(record["kind"])
            if record["kind"] == "group":
                entry["groups"].append(record)
    return objects


def edges_reason(objects, viewport, roles):
    owners = [entry["owner"] for entry in objects.values()]
    for order in permutations(owners, len(roles)):
        if all(role(owner, viewport) for role, owner in zip(roles, order)):
            return None
    return "edge: the copies are not at the top, right and bottom edges of the map"


def text_inside_group(records, objects):
    for record in records:
        if record.get("k") != "text":
            continue
        for entry in objects.values():
            for group in entry["groups"]:
                if check_geometry.intersects(record, group):
                    return f"text {record['s']!r} lies inside a group label"
    return None


def check_units(header, records):
    objects = objects_of(records, UNIT_KINDS + ("spice",))
    if len(objects) != 3:
        return f"object count {len(objects)}, expected 3"
    wanted = set(UNIT_KINDS)
    if header["scene"] == HARVESTER_SCENE:
        wanted.add("spice")
    for number, entry in sorted(objects.items()):
        for kind in sorted(wanted - entry["kinds"]):
            return f"object {number} has no {kind} label"
    viewport = header.get("map_viewport")
    if not viewport:
        return "no map_viewport in the header"
    return (edges_reason(objects, viewport, (at_top, at_right, at_bottom))
            or text_inside_group(records, objects))


def check_structures(header, records):
    objects = objects_of(records, ("structure-health",))
    if len(objects) != 1:
        return f"object count {len(objects)}, expected 1"
    viewport = header.get("map_viewport")
    if not viewport:
        return "no map_viewport in the header"
    name, role = STRUCTURE_EDGES[header["scene"]]
    owner = next(iter(objects.values()))["owner"]
    if not role(owner, viewport):
        return f"edge: the building is not at the {name} edge of the map"
    return None


def check_scene(header, records):
    scene = header["scene"]
    if scene.startswith(UNIT_PREFIX):
        result = check_units(header, records)
    elif scene in STRUCTURE_EDGES:
        result = check_structures(header, records)
    else:
        return None
    return result or "OK"


def format_line(header, result):
    return f"{header['scene']}; {check_geometry.combo_of(header)}; {result}"


def check_file(path):
    header, records = check_geometry.load_log(path)
    result = check_scene(header, records)
    return None if result is None else format_line(header, result)


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("logs", nargs="+")
    parser.add_argument("--out")
    args = parser.parse_args(argv)
    lines = []
    for root in args.logs:
        for path in sorted(Path(root).rglob("*.geometry.jsonl")):
            line = check_file(path)
            if line is not None:
                lines.append(line)
    for line in lines:
        print(line)
    if args.out:
        Path(args.out).write_text("\n".join(lines) + "\n", encoding="utf-8")
    failed = [line for line in lines if not line.endswith("; OK")]
    print(f"scenes checked: {len(lines)}; failed: {len(failed)}")
    return 1 if failed or not lines else 0


if __name__ == "__main__":
    sys.exit(main())
