import argparse
import re
import sys
from pathlib import Path

KEY_TOKEN = re.compile(r"SDLK_\w+|SDL_SCANCODE_\w+|eKeyAction::\w+")
SOURCE_SUFFIXES = (".cpp", ".h", ".hpp", ".c", ".cc")
EXCLUDED_FILES = ("src/controls/cKeyBindings.cpp",)


def strip_comments(text):
    out = []
    i, n = 0, len(text)
    while i < n:
        c = text[i]
        two = text[i:i + 2]
        if two == "//":
            while i < n and text[i] != "\n":
                i += 1
        elif two == "/*":
            end = text.find("*/", i + 2)
            end = n if end < 0 else end + 2
            out.append("\n" * text.count("\n", i, end))
            i = end
        elif c in "\"'":
            j = i + 1
            while j < n and text[j] != c and text[j] != "\n":
                j += 2 if text[j] == "\\" else 1
            out.append(text[i:j + 1])
            i = j + 1
        else:
            out.append(c)
            i += 1
    return "".join(out)


def definition_name(line):
    if not line or line[0] in " \t#}/{)" or line.rstrip().endswith(";"):
        return None
    head = line.split("(", 1)
    if len(head) < 2:
        return None
    parts = re.split(r"[\s*&]+", head[0].strip())
    name = parts[-1] if parts else ""
    return name if re.fullmatch(r"[~\w:<>]+", name) else None


def extract(text, file):
    rows = []
    function = "-"
    for number, line in enumerate(strip_comments(text).split("\n"), 1):
        if line.startswith("}"):
            function = "-"
        else:
            name = definition_name(line)
            if name:
                function = name
        for token in KEY_TOKEN.findall(line):
            rows.append({"file": file, "function": function, "key": token, "line": number})
    return rows


def to_tsv(rows):
    lines = ["file\tfunction\tkey\tline"]
    lines += [f"{r['file']}\t{r['function']}\t{r['key']}\t{r['line']}" for r in rows]
    return "\n".join(lines) + "\n"


def extract_tree(root):
    root = Path(root)
    rows = []
    for path in sorted((root / "src").rglob("*")):
        if path.suffix in SOURCE_SUFFIXES and path.is_file():
            relative = path.relative_to(root).as_posix()
            if relative in EXCLUDED_FILES:
                continue
            rows += extract(path.read_text(encoding="utf-8", errors="replace"), relative)
    return rows


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args(argv)
    rows = extract_tree(args.root)
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "w", encoding="utf-8", newline="") as handle:
        handle.write(to_tsv(rows))
    print(f"keys-raw rows: {len(rows)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
