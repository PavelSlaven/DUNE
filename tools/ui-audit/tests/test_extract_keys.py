import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import extract_keys  # noqa: E402

SOURCE = """\
static const int kDefault = SDLK_F1;

void cMainMenuState::onKeyDown(const cKeyboardEvent &event) {
    if (event.hasKey(SDL_SCANCODE_ESCAPE)) {
        quit();
    }
    // SDL_SCANCODE_Q is only a comment
    if (event.hasKey(SDL_SCANCODE_M) || event.hasKey(SDL_SCANCODE_MUTE)) { // SDLK_SPACE
        mute();
    }
    int x = 0; /* SDLK_TAB */
}

int helper(int value) {
    return value == SDLK_RETURN;
}

int afterwards = SDLK_DELETE;
"""


class ExtractKeys(unittest.TestCase):
    def rows(self, text=SOURCE):
        return extract_keys.extract(text, "src/a.cpp")

    def test_one_row_per_key_token_in_order(self):
        keys = [r["key"] for r in self.rows()]
        self.assertEqual(keys, ["SDLK_F1", "SDL_SCANCODE_ESCAPE", "SDL_SCANCODE_M", "SDL_SCANCODE_MUTE",
                                "SDLK_RETURN", "SDLK_DELETE"])

    def test_row_has_file_function_key_and_line(self):
        escape = next(r for r in self.rows() if r["key"] == "SDL_SCANCODE_ESCAPE")
        self.assertEqual(escape, {"file": "src/a.cpp", "function": "cMainMenuState::onKeyDown",
                                  "key": "SDL_SCANCODE_ESCAPE", "line": 4})

    def test_function_is_the_last_column_zero_definition_above(self):
        by_key = {r["key"]: r["function"] for r in self.rows()}
        self.assertEqual(by_key["SDL_SCANCODE_M"], "cMainMenuState::onKeyDown")
        self.assertEqual(by_key["SDLK_RETURN"], "helper")

    def test_use_outside_any_function_has_a_dash(self):
        by_key = {r["key"]: r["function"] for r in self.rows()}
        self.assertEqual(by_key["SDLK_F1"], "-")
        self.assertEqual(by_key["SDLK_DELETE"], "-")

    def test_comments_are_ignored(self):
        keys = [r["key"] for r in self.rows()]
        for ignored in ("SDL_SCANCODE_Q", "SDLK_SPACE", "SDLK_TAB"):
            self.assertNotIn(ignored, keys)

    def test_two_uses_of_one_key_in_one_function_are_two_rows(self):
        text = "void A::f() {\n    if (k == SDLK_A) {}\n    if (k == SDLK_A) {}\n}\n"
        rows = extract_keys.extract(text, "a.cpp")
        self.assertEqual([r["line"] for r in rows], [2, 3])

    def test_text_without_keys_gives_no_rows(self):
        self.assertEqual(extract_keys.extract("int main() { return 0; }\n", "a.cpp"), [])

    def test_tsv_has_a_header_and_tab_separated_rows(self):
        tsv = extract_keys.to_tsv(self.rows()[:1])
        self.assertEqual(tsv.splitlines(), ["file\tfunction\tkey\tline", "src/a.cpp\t-\tSDLK_F1\t1"])

    def test_action_token_is_a_row(self):
        text = "void A::f(const cKeyboardEvent &event) {\n    if (event.isAction(eKeyAction::QUICK_SAVE)) {}\n}\n"
        rows = extract_keys.extract(text, "a.cpp")
        self.assertEqual([(r["function"], r["key"], r["line"]) for r in rows], [("A::f", "eKeyAction::QUICK_SAVE", 2)])

    def test_the_defaults_table_file_gives_no_rows(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "src" / "controls"
            source.mkdir(parents=True)
            (source / "cKeyBindings.cpp").write_text(
                "void f() { bind(eKeyAction::SCREENSHOT, {SDL_SCANCODE_F11}); }\n", encoding="utf-8")
            (source / "other.cpp").write_text("void g() { return SDLK_A; }\n", encoding="utf-8")
            rows = extract_keys.extract_tree(directory)
        self.assertEqual([row["file"] for row in rows], ["src/controls/other.cpp"])


if __name__ == "__main__":
    unittest.main()
