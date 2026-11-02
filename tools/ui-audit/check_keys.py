import argparse
import csv
import sys
from collections import Counter
from pathlib import Path

STATE_SEPARATOR = " | "
BINDING_PREFIX = "m_commandBindings."
REBINDING_WORDS = "переназначение без проверки занятости"


def load_tsv(path):
    with open(path, encoding="utf-8", newline="") as handle:
        lines = [line for line in handle.read().splitlines() if line.strip() and not line.startswith("#")]
    reader = csv.DictReader(lines, delimiter="\t")
    return [{key: (value or "") for key, value in row.items() if key} for row in reader]


def normalize(key):
    for prefix in ("SDLK_", "SDL_SCANCODE_"):
        if key.startswith(prefix):
            return key[len(prefix):].upper()
    return key.upper()


def is_binding_marker(row):
    return row["key"].startswith(BINDING_PREFIX)


def states_of(row):
    return [state.strip() for state in row["state"].split(STATE_SEPARATOR) if state.strip() and state.strip() != "-"]


def is_handled(row):
    return row.get("action", "-") != "-" and not is_binding_marker(row)


def conflicts(rows):
    groups = {}
    for row in rows:
        if not is_handled(row):
            continue
        for state in states_of(row):
            groups.setdefault((state, normalize(row["key"]), row.get("mods", "")), []).append(row)
    flags = []
    for (state, key, mods), members in sorted(groups.items()):
        actions = sorted({member["action"] for member in members})
        if len(actions) > 1:
            places = sorted({f"{member['file']}:{member['line']}" for member in members})
            flags.append({"rule": 10, "state": state, "key": key, "mods": mods,
                          "actions": actions, "places": places})
    return flags


def rebindable_from_rows(rows):
    commands = {}
    for row in rows:
        if is_binding_marker(row):
            command = row["key"][len(BINDING_PREFIX):]
            commands.setdefault(command, [])
            for state in states_of(row):
                if state not in commands[command]:
                    commands[command].append(state)
    return [{"command": command, "states": states} for command, states in sorted(commands.items())]


def rebinding_flags(rows, rebindable, check_place):
    if check_place is not None:
        return []
    flags = []
    for entry in rebindable:
        command = entry["command"]
        for state in entry["states"]:
            keys = set()
            for row in rows:
                if is_handled(row) and state in states_of(row) and row["action"] != command:
                    keys.add(normalize(row["key"]))
            flags.append({"rule": 10, "command": command, "state": state, "keys": sorted(keys)})
    return flags


def format_flag(flag):
    if "command" in flag:
        return (f"rule 10: state={flag['state']}; command={flag['command']}; {REBINDING_WORDS}; "
                f"keys already used in this state: {', '.join(flag['keys']) or '-'}")
    mods = f"+{flag['mods']}" if flag["mods"] else ""
    return (f"rule 10: state={flag['state']}; key={flag['key']}{mods}; "
            f"actions: {' / '.join(flag['actions'])}; places: {', '.join(flag['places'])}")


def freshness(raw_rows, table_rows):
    def triples(rows):
        return Counter((row["file"], row["function"], row["key"]) for row in rows)

    raw_count, table_count = triples(raw_rows), triples(table_rows)
    problems = []
    for triple, count in sorted((raw_count - table_count).items()):
        problems.append(f"no annotation in keys.tsv: {triple[0]} {triple[1]} {triple[2]} (x{count})")
    for triple, count in sorted((table_count - raw_count).items()):
        problems.append(f"no such key use in the code: {triple[0]} {triple[1]} {triple[2]} (x{count})")
    return problems


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--keys", required=True)
    parser.add_argument("--raw", required=True)
    parser.add_argument("--binding-check")
    parser.add_argument("--out")
    args = parser.parse_args(argv)
    table = load_tsv(args.keys)
    problems = freshness(load_tsv(args.raw), table)
    flags = conflicts(table) + rebinding_flags(table, rebindable_from_rows(table), args.binding_check)
    lines = [format_flag(flag) for flag in flags]
    for problem in problems:
        print(problem)
    for line in lines:
        print(line)
    if args.out:
        Path(args.out).write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
    print(f"keys: freshness {'OK' if not problems else 'FAIL'}; rule 10 flags: {len(lines)}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
