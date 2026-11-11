import argparse
import re
import sys
from pathlib import Path

HIT = re.compile(r"\b(isWithin\w*|isOver\w*|isMouseOver\w*|isPointWithin\w*|isInside\w*|containsPoint\w*|pointInRect\w*)\s*\(")
FUNCTION = re.compile(r"^[A-Za-z_][\w:<>,\s\*&~]*?\b([A-Za-z_~]\w*::[~\w]+)\s*\(")
DIRECTORIES = ("src/gui", "src/drawers", "src/gamestates", "src/managers", "src/sidebar", "src/gameobjects/mentat",
               "src/controls", "src/debug")
RECORDS = ("uiaudit::recordClick", "uiaudit::recordCanvasClick")


def enclosing_functions(lines):
    current = None
    for number, line in enumerate(lines, 1):
        match = FUNCTION.match(line)
        if match and not line.rstrip().endswith(";"):
            current = match.group(1)
        yield number, current


def scan_text(text):
    lines = text.splitlines()
    owners = dict(enclosing_functions(lines))
    record_lines = [number for number, line in enumerate(lines, 1) if any(record in line for record in RECORDS)]
    recorded = {owners[number] for number in record_lines}
    rows = []
    for number, line in enumerate(lines, 1):
        if HIT.search(line) and not line.lstrip().startswith("//"):
            function = owners.get(number)
            rows.append((number, function or "-", "yes" if function in recorded else "no", line.strip()[:110]))
    return rows, len(record_lines)


def scan(root):
    root = Path(root)
    result = []
    for directory in DIRECTORIES:
        for path in sorted((root / directory).rglob("*.cpp")):
            rows, records = scan_text(path.read_text(encoding="utf-8", errors="replace"))
            relative = str(path.relative_to(root)).replace("\\", "/")
            for number, function, recorded, code in rows:
                result.append((relative, number, function, recorded, records, code))
    return result


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    args = parser.parse_args(argv)
    print("file\tline\tfunction\trecorded_in_function\trecords_in_file\tcode")
    for row in scan(args.root):
        print("\t".join(str(item) for item in row))
    return 0


if __name__ == "__main__":
    sys.exit(main())
