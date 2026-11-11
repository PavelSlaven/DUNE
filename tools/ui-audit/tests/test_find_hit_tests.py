import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import find_hit_tests  # noqa: E402

SOURCE = """\
void cFirstState::draw() const
{
    if (uiaudit::isEnabled()) {
        uiaudit::recordClick("first", 0, 0, 1, 1);
    }
}

void cFirstState::onMouseLeftButtonClicked(const s_MouseEvent &event)
{
    if (mouse->isOverRectangle(&rect)) {
        fire();
    }
}

void cSecondState::onNotifyMouseEvent(const s_MouseEvent &event)
{
    // isOverRectangle in a comment is ignored
    if (isWithinRect(event.coords)) {
        fire();
    }
}
"""


class ScanTextTest(unittest.TestCase):
    def test_hit_test_in_function_without_record_is_marked_no(self):
        rows, _ = find_hit_tests.scan_text(SOURCE)
        by_function = {function: recorded for _, function, recorded, _ in rows}
        self.assertEqual(by_function["cFirstState::onMouseLeftButtonClicked"], "no")
        self.assertEqual(by_function["cSecondState::onNotifyMouseEvent"], "no")

    def test_hit_test_in_function_with_record_is_marked_yes(self):
        text = SOURCE.replace("void cFirstState::draw() const\n{\n", "void cFirstState::draw() const\n{\n    if (isOverRect(a)) {}\n")
        rows, _ = find_hit_tests.scan_text(text)
        by_function = {function: recorded for _, function, recorded, _ in rows}
        self.assertEqual(by_function["cFirstState::draw"], "yes")

    def test_comment_lines_are_ignored(self):
        rows, _ = find_hit_tests.scan_text(SOURCE)
        self.assertEqual(len(rows), 2)

    def test_record_count_counts_both_kinds(self):
        text = SOURCE + 'void cThird::draw() const\n{\n    uiaudit::recordCanvasClick("c");\n}\n'
        _, records = find_hit_tests.scan_text(text)
        self.assertEqual(records, 2)


class ScanTreeTest(unittest.TestCase):
    def test_only_listed_directories_are_scanned(self):
        with tempfile.TemporaryDirectory() as root:
            for directory in ("src/gui", "src/other"):
                path = Path(root) / directory
                path.mkdir(parents=True)
                (path / "a.cpp").write_text(SOURCE, encoding="utf-8")
            rows = find_hit_tests.scan(root)
        self.assertEqual({row[0] for row in rows}, {"src/gui/a.cpp"})


if __name__ == "__main__":
    unittest.main()
