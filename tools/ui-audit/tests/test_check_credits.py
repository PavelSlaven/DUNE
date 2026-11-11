import json
import tempfile
import unittest
from pathlib import Path

import check_credits


def write_log(root, scene, notes, texts, resolution="1024x768"):
    directory = Path(root) / "logs" / resolution / "en" / "hd"
    directory.mkdir(parents=True, exist_ok=True)
    header = {"k": "header", "scene": scene, "resolution": resolution, "language": "en", "graphics": "hd",
              "canvas": {"w": 800, "h": 600}, "game_screen": False, "version": "v"}
    records = [header]
    records += [{"k": "credit", "name": n, "s": t} for n, t in notes]
    records += [{"k": "text", "s": s, "x": 0, "y": y, "w": 10, "h": 10, "box": None} for s, y in texts]
    (directory / f"{scene}.geometry.jsonl").write_text("\n".join(json.dumps(r) for r in records) + "\n",
                                                       encoding="utf-8")


class CheckCreditsTests(unittest.TestCase):
    def test_all_lines_covered_across_scenes(self):
        notes = [("", "Title"), ("Paul", "Developer"), ("Fedaygin", "")]
        with tempfile.TemporaryDirectory() as root:
            write_log(root, "credits-1", notes, [("Title", 10), ("Paul", 50), ("Developer", 50)])
            write_log(root, "credits-2", notes, [("Fedaygin", 20)])
            combos, problems = check_credits.check_credits(root)
        self.assertEqual((1, []), (combos, problems))

    def test_missing_line_is_reported(self):
        notes = [("", "Title"), ("Fedaygin", "")]
        with tempfile.TemporaryDirectory() as root:
            write_log(root, "credits-1", notes, [("Title", 10)])
            combos, problems = check_credits.check_credits(root)
        self.assertEqual(1, len(problems))
        self.assertIn("Fedaygin", problems[0][1])

    def test_name_and_text_must_share_a_row(self):
        notes = [("Paul", "Developer")]
        with tempfile.TemporaryDirectory() as root:
            write_log(root, "credits-1", notes, [("Paul", 50), ("Developer", 90)])
            _, problems = check_credits.check_credits(root)
        self.assertEqual(1, len(problems))

    def test_log_without_notes_is_a_problem(self):
        with tempfile.TemporaryDirectory() as root:
            write_log(root, "credits-1", [], [("Title", 10)])
            _, problems = check_credits.check_credits(root)
        self.assertEqual(1, len(problems))


if __name__ == "__main__":
    unittest.main()
