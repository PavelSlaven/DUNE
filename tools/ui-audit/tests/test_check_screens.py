import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import check_screens  # noqa: E402

DEFINITIONS = """\
inline constexpr int GAME_INITIALIZE = 0;
inline constexpr int GAME_MENU = 1;
inline constexpr int GAME_PLAYING = 2; // the game screen
inline constexpr int GAME_MAX_STATES = 3;
inline constexpr int SOMETHING_ELSE = 9;
"""

SOURCE_A = """\
class cOptionsState : public cGameState {
public:
    void draw();
};

class cForward;
enum class Mode { A, B };
"""

SOURCE_B = """\
  class cCreditsState : public cGameState
  {
  };
struct NotAClass {};
"""


class CodeNames(unittest.TestCase):
    def test_game_state_constants_are_read_from_inline_definitions(self):
        self.assertEqual(check_screens.code_states(DEFINITIONS),
                         ["GAME_INITIALIZE", "GAME_MENU", "GAME_PLAYING", "GAME_MAX_STATES"])

    def test_classes_are_read_without_forward_declarations_and_enums(self):
        self.assertEqual(check_screens.code_classes([SOURCE_A, SOURCE_B]), ["cCreditsState", "cOptionsState"])


class Exclusions(unittest.TestCase):
    def test_exclusions_are_read_with_reasons(self):
        exclusions, problems = check_screens.load_exclusions(
            "name\treason\n# note\nGAME_INITIALIZE\tне экран\n\ncGameState\tне экран\n")
        self.assertEqual(exclusions, {"GAME_INITIALIZE": "не экран", "cGameState": "не экран"})
        self.assertEqual(problems, [])

    def test_exclusion_without_a_reason_is_a_problem(self):
        exclusions, problems = check_screens.load_exclusions("GAME_OVER\t\nGAME_INTRO\n")
        self.assertEqual(exclusions, {})
        self.assertEqual(len(problems), 2)
        self.assertIn("GAME_OVER", problems[0])
        self.assertIn("GAME_INTRO", problems[1])


class Coverage(unittest.TestCase):
    CODE = ["GAME_MENU", "GAME_PLAYING", "cOptionsState", "GAME_INITIALIZE"]

    def test_every_name_covered_by_a_scene_or_an_exclusion_is_complete(self):
        scenes = [{"id": "menu", "state": "GAME_MENU"}, {"id": "game", "screen": "GAME_PLAYING"},
                  {"id": "options", "screen": "cOptionsState"}, {"id": "other"}]
        problems = check_screens.check_screens(scenes, self.CODE, {"GAME_INITIALIZE": "не экран"})
        self.assertEqual(problems, [])

    def test_code_name_without_a_scene_is_a_problem(self):
        scenes = [{"id": "menu", "state": "GAME_MENU"}]
        problems = check_screens.check_screens(scenes, self.CODE, {"GAME_INITIALIZE": "не экран"})
        self.assertEqual(len(problems), 2)
        self.assertTrue(any("GAME_PLAYING" in p for p in problems))
        self.assertTrue(any("cOptionsState" in p for p in problems))

    def test_exclusion_of_a_name_the_code_does_not_have_is_a_problem(self):
        scenes = [{"id": "menu", "state": "GAME_MENU"}, {"id": "g", "state": "GAME_PLAYING"},
                  {"id": "o", "state": "cOptionsState"}]
        exclusions = {"GAME_INITIALIZE": "не экран", "GAME_REMOVED": "не экран"}
        problems = check_screens.check_screens(scenes, self.CODE, exclusions)
        self.assertEqual(len(problems), 1)
        self.assertIn("GAME_REMOVED", problems[0])

    def test_exclusion_with_an_empty_reason_is_a_problem(self):
        scenes = [{"id": "menu", "state": "GAME_MENU"}, {"id": "g", "state": "GAME_PLAYING"},
                  {"id": "o", "state": "cOptionsState"}]
        problems = check_screens.check_screens(scenes, self.CODE, {"GAME_INITIALIZE": ""})
        self.assertEqual(len(problems), 1)
        self.assertIn("GAME_INITIALIZE", problems[0])

    def test_scene_naming_an_unknown_state_is_not_a_problem(self):
        scenes = [{"id": "menu", "state": "GAME_MENU"}, {"id": "g", "state": "GAME_PLAYING"},
                  {"id": "o", "state": "cOptionsState"}, {"id": "x", "state": "GAME_UNKNOWN"}]
        self.assertEqual(check_screens.check_screens(scenes, self.CODE, {"GAME_INITIALIZE": "не экран"}), [])


if __name__ == "__main__":
    unittest.main()
