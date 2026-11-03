import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import check_keys  # noqa: E402


def row(state, key, action, mods="", file="src/a.cpp", function="A::f", line="1"):
    return {"file": file, "function": function, "key": key, "mods": mods, "line": line,
            "state": state, "action": action}


def raw(file, function, key, line="1"):
    return {"file": file, "function": function, "key": key, "line": line}


class KeyConflicts(unittest.TestCase):
    def test_one_key_two_actions_in_one_state_is_flagged(self):
        flags = check_keys.conflicts([row("menu", "ESCAPE", "back"), row("menu", "ESCAPE", "quit")])
        self.assertEqual(len(flags), 1)
        self.assertEqual(flags[0]["rule"], 10)
        self.assertEqual(flags[0]["state"], "menu")
        self.assertEqual(flags[0]["key"], "ESCAPE")
        self.assertEqual(flags[0]["actions"], ["back", "quit"])

    def test_same_key_in_different_states_is_honest(self):
        rows = [row("menu", "ESCAPE", "back"), row("game", "ESCAPE", "pause")]
        self.assertEqual(check_keys.conflicts(rows), [])

    def test_same_action_twice_is_honest(self):
        rows = [row("menu", "RETURN", "ok", file="a.cpp"), row("menu", "RETURN", "ok", file="b.cpp")]
        self.assertEqual(check_keys.conflicts(rows), [])

    def test_different_modifiers_are_different_keys(self):
        rows = [row("game", "D", "deploy", mods=""), row("game", "D", "scroll", mods="CTRL")]
        self.assertEqual(check_keys.conflicts(rows), [])

    def test_deploy_and_unload_selected_together_on_one_key_is_flagged(self):
        state = "game: selection deploy+unload"
        flags = check_keys.conflicts([row(state, "D", "deploy"), row(state, "D", "unload")])
        self.assertEqual(len(flags), 1)
        self.assertEqual(flags[0]["actions"], ["deploy", "unload"])

    def test_deploy_and_unload_selected_apart_is_honest(self):
        rows = [row("game: selection deploy", "D", "deploy"), row("game: selection unload", "D", "unload")]
        self.assertEqual(check_keys.conflicts(rows), [])

    def test_row_without_key_handling_is_not_a_conflict(self):
        self.assertEqual(check_keys.conflicts([row("game", "D", "deploy"), row("game", "D", "-")]), [])

    def test_three_actions_on_one_key_are_one_flag(self):
        rows = [row("game", "D", "a"), row("game", "D", "b"), row("game", "D", "c")]
        flags = check_keys.conflicts(rows)
        self.assertEqual(len(flags), 1)
        self.assertEqual(flags[0]["actions"], ["a", "b", "c"])

    def test_flag_line_names_state_key_and_actions(self):
        flag = check_keys.conflicts([row("menu", "ESCAPE", "back"), row("menu", "ESCAPE", "quit")])[0]
        line = check_keys.format_flag(flag)
        self.assertNotIn("\n", line)
        for part in ("rule 10", "menu", "ESCAPE", "back", "quit"):
            self.assertIn(part, line)


class KeyRebinding(unittest.TestCase):
    ROWS = [
        row("game", "W", "scroll-up"),
        row("game", "S", "scroll-down"),
        row("game", "A", "scroll-left"),
        row("game: selection combat", "SPACE", "stop"),
        row("game: selection combat", "R", "repair"),
    ]
    REBINDABLE = [
        {"command": "attack", "states": ["game", "game: selection combat"]},
        {"command": "repair", "states": ["game: selection combat"]},
    ]

    def test_one_flag_per_command_and_state_pair(self):
        flags = check_keys.rebinding_flags(self.ROWS, self.REBINDABLE, None)
        self.assertEqual(len(flags), 3)
        self.assertEqual({(f["command"], f["state"]) for f in flags}, {
            ("attack", "game"), ("attack", "game: selection combat"), ("repair", "game: selection combat"),
        })
        self.assertTrue(all(flag["rule"] == 10 for flag in flags))

    def test_flag_lists_occupied_keys_of_the_state_once(self):
        flags = check_keys.rebinding_flags(self.ROWS, self.REBINDABLE, None)
        game = next(f for f in flags if f["command"] == "attack" and f["state"] == "game")
        self.assertEqual(game["keys"], ["A", "S", "W"])

    def test_own_key_is_not_listed_as_occupied(self):
        flags = check_keys.rebinding_flags(self.ROWS, self.REBINDABLE, None)
        repair = next(f for f in flags if f["command"] == "repair")
        self.assertEqual(repair["keys"], ["SPACE"])

    def test_row_without_key_handling_is_not_listed_as_occupied(self):
        rows = self.ROWS + [row("game: selection combat", "T", "-")]
        flags = check_keys.rebinding_flags(rows, self.REBINDABLE, None)
        repair = next(f for f in flags if f["command"] == "repair")
        self.assertEqual(repair["keys"], ["SPACE"])

    def test_state_without_other_keys_still_gives_a_flag(self):
        flags = check_keys.rebinding_flags([], [{"command": "attack", "states": ["game"]}], None)
        self.assertEqual(len(flags), 1)
        self.assertEqual(flags[0]["keys"], [])

    def test_flag_line_has_state_command_words_and_keys(self):
        flag = check_keys.rebinding_flags(self.ROWS, self.REBINDABLE, None)[0]
        line = check_keys.format_flag(flag)
        self.assertNotIn("\n", line)
        self.assertIn("переназначение без проверки занятости", line)
        self.assertIn(flag["command"], line)
        self.assertIn(flag["state"], line)
        for key in flag["keys"]:
            self.assertIn(key, line)

    def test_existing_check_removes_the_flags(self):
        place = "src/gamestates/cOptionsState.cpp:1544"
        self.assertEqual(check_keys.rebinding_flags(self.ROWS, self.REBINDABLE, place), [])


class KeyTableFreshness(unittest.TestCase):
    def test_equal_tables_are_fresh(self):
        raw_rows = [raw("a.cpp", "A::f", "K_A"), raw("b.cpp", "B::g", "K_B")]
        table = [row("s", "K_B", "x", file="b.cpp", function="B::g"), row("s", "K_A", "y", file="a.cpp", function="A::f")]
        self.assertEqual(check_keys.freshness(raw_rows, table), [])

    def test_line_number_is_not_compared(self):
        raw_rows = [raw("a.cpp", "A::f", "K_A", line="10")]
        table = [row("s", "K_A", "y", file="a.cpp", function="A::f", line="99")]
        self.assertEqual(check_keys.freshness(raw_rows, table), [])

    def test_missing_row_in_the_table_is_a_problem(self):
        raw_rows = [raw("a.cpp", "A::f", "K_A"), raw("a.cpp", "A::f", "K_B")]
        table = [row("s", "K_A", "y", file="a.cpp", function="A::f")]
        problems = check_keys.freshness(raw_rows, table)
        self.assertEqual(len(problems), 1)
        self.assertIn("K_B", problems[0])

    def test_extra_row_in_the_table_is_a_problem(self):
        raw_rows = [raw("a.cpp", "A::f", "K_A")]
        table = [row("s", "K_A", "y", file="a.cpp", function="A::f"), row("s", "K_Z", "z", file="a.cpp", function="A::f")]
        problems = check_keys.freshness(raw_rows, table)
        self.assertEqual(len(problems), 1)
        self.assertIn("K_Z", problems[0])

    def test_two_checks_of_one_key_in_one_function_are_two_rows(self):
        raw_rows = [raw("a.cpp", "A::f", "K_A", "10"), raw("a.cpp", "A::f", "K_A", "20")]
        one_row = [row("s", "K_A", "y", file="a.cpp", function="A::f")]
        self.assertEqual(len(check_keys.freshness(raw_rows, one_row)), 1)
        two_rows = one_row + [row("s", "K_A", "y", file="a.cpp", function="A::f", line="20")]
        self.assertEqual(check_keys.freshness(raw_rows, two_rows), [])

    def test_same_key_in_another_function_is_a_different_row(self):
        raw_rows = [raw("a.cpp", "A::f", "K_A")]
        table = [row("s", "K_A", "y", file="a.cpp", function="A::g")]
        self.assertEqual(len(check_keys.freshness(raw_rows, table)), 2)


class TsvLoading(unittest.TestCase):
    def test_rows_are_read_by_the_header(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "keys.tsv"
            path.write_text("file\tfunction\tkey\tline\nsrc/a.cpp\tA::f\tSDLK_A\t12\n", encoding="utf-8")
            rows = check_keys.load_tsv(path)
        self.assertEqual(rows, [{"file": "src/a.cpp", "function": "A::f", "key": "SDLK_A", "line": "12"}])


if __name__ == "__main__":
    unittest.main()
