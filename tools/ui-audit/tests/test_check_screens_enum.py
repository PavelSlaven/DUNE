import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import check_screens  # noqa: E402

ENUM_HEADER = """\
#pragma once

enum class eGameState : char {
    INITIALIZE = 0,        // initialize game
    OVER,                  // GAME OVER
    MENU,
    COUNT
};

const char *gameStateToString(eGameState state);
"""


class EnumStates(unittest.TestCase):
    def test_enumerators_get_the_old_constant_names(self):
        self.assertEqual(check_screens.code_enum_states(ENUM_HEADER),
                         ["GAME_INITIALIZE", "GAME_OVER", "GAME_MENU", "GAME_MAX_STATES"])

    def test_text_without_the_enum_gives_no_states(self):
        self.assertEqual(check_screens.code_enum_states("enum class Other { A, B };\n"), [])

    def test_collect_code_names_reads_the_enum(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            sources = {
                "src/include/eGameState.h": ENUM_HEADER,
                "src/gamestates/cA.h": "class cA {\n",
                "src/gameobjects/mentat/M.h": "class M : public X {\n",
                "src/save/SaveSlotsDialog.hpp": "class SaveSlotsDialog {\n",
            }
            for name, text in sources.items():
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(text, encoding="utf-8")
            self.assertEqual(check_screens.collect_code_names(root),
                             ["GAME_INITIALIZE", "GAME_OVER", "GAME_MENU", "GAME_MAX_STATES", "M", "cA", "SaveSlotsDialog"])


if __name__ == "__main__":
    unittest.main()
