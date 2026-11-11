import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path


def load(path):
    records = [json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()]
    return records[0], records[1:]


def line_covered(line, texts):
    name, text = line
    if name and text:
        name_rows = {t["y"] for t in texts if t["s"] == name}
        return any(t["s"] == text and t["y"] in name_rows for t in texts)
    wanted = name or text
    return any(t["s"] == wanted for t in texts)


def check_credits(logs_root):
    by_combo = defaultdict(list)
    for path in sorted(Path(logs_root).rglob("credits-*.geometry.jsonl")):
        header, records = load(path)
        combo = f"{header['resolution']}/{header['language']}/{header['graphics']}"
        by_combo[combo].append(records)
    problems = []
    for combo, logs in sorted(by_combo.items()):
        expected = [(r["name"], r["s"]) for r in logs[0] if r["k"] == "credit"]
        if not expected:
            problems.append((combo, "no expected credit lines in the log"))
            continue
        texts_per_log = [[r for r in records if r["k"] == "text"] for records in logs]
        for line in expected:
            if not any(line_covered(line, texts) for texts in texts_per_log):
                problems.append((combo, f"line not fully visible in any credits scene: {line[0]} | {line[1]}"))
    return len(by_combo), problems


def main(argv=None):
    parser = argparse.ArgumentParser(description="Check that every credits line is fully visible in some credits scene.")
    parser.add_argument("logs_root")
    args = parser.parse_args(argv)
    combos, problems = check_credits(args.logs_root)
    for combo, message in problems:
        print(f"{combo}: {message}")
    print(f"credits coverage: {'OK' if not problems and combos else 'FAIL'}; combos: {combos}; problems: {len(problems)}")
    return 0 if combos and not problems else 1


if __name__ == "__main__":
    sys.exit(main())
