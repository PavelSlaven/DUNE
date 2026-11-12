import argparse
import json
import re
import sys
from pathlib import Path

STATE_DEFINE = re.compile(r"(?m)^inline constexpr int\s+(GAME_\w+)\s*=\s*-?\d+;")
CLASS_DEFINITION = re.compile(r"(?m)^[ \t]*class\s+(\w+)[^;{]*\{")
CLASS_DIRECTORIES = ("src/gamestates", "src/gameobjects/mentat")
CLASS_FILES = ("src/save/SaveSlotsDialog.hpp",)


def code_states(text):
    return STATE_DEFINE.findall(text)


def code_classes(sources):
    names = set()
    for text in sources:
        names.update(CLASS_DEFINITION.findall(text))
    return sorted(names)


def load_exclusions(text):
    exclusions = {}
    problems = []
    for number, line in enumerate(text.splitlines(), 1):
        if not line.strip() or line.startswith("#") or line.startswith("name\t"):
            continue
        name, _, reason = line.partition("\t")
        name, reason = name.strip(), reason.strip()
        if not reason:
            problems.append(f"exclusions line {number}: {name} has no reason")
        else:
            exclusions[name] = reason
    return exclusions, problems


def check_screens(scenes, code_names, exclusions):
    covered = set()
    for scene in scenes:
        for field in ("state", "screen"):
            if scene.get(field):
                covered.add(scene[field])
    problems = []
    for name in code_names:
        if name not in covered and name not in exclusions:
            problems.append(f"no scene and no exclusion for {name}")
    for name in sorted(exclusions):
        if name not in code_names:
            problems.append(f"exclusion {name} is not a name in the code")
        elif not exclusions[name]:
            problems.append(f"exclusion {name} has no reason")
    return problems


def collect_code_names(root):
    root = Path(root)
    states = code_states((root / "src/include/eGameState.h").read_text(encoding="utf-8", errors="replace"))
    sources = []
    for directory in CLASS_DIRECTORIES:
        for path in sorted((root / directory).glob("*.h")) + sorted((root / directory).glob("*.hpp")):
            sources.append(path.read_text(encoding="utf-8", errors="replace"))
    dialog = root / CLASS_FILES[0]
    dialog_classes = [name for name in code_classes([dialog.read_text(encoding="utf-8", errors="replace")])
                      if name == "SaveSlotsDialog"]
    return states + code_classes(sources) + dialog_classes


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", required=True)
    parser.add_argument("--root", required=True)
    parser.add_argument("--exclusions", required=True)
    args = parser.parse_args(argv)
    scenes = json.loads(Path(args.catalog).read_text(encoding="utf-8"))["scenes"]
    exclusions, problems = load_exclusions(Path(args.exclusions).read_text(encoding="utf-8"))
    problems += check_screens(scenes, collect_code_names(args.root), exclusions)
    for problem in problems:
        print(problem)
    print(f"screens: {'OK' if not problems else 'FAIL'}; problems: {len(problems)}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
