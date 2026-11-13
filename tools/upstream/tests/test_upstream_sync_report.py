import contextlib
import io
import subprocess
import tempfile
import unittest
from pathlib import Path

from tools.upstream import upstream_sync_report


def git(repo, *args):
    result = subprocess.run(
        [
            "git",
            "-c",
            "user.name=Test User",
            "-c",
            "user.email=test@example.com",
            *args,
        ],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


class UpstreamSyncReportTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.repo = self.root / "repo"
        self.repo.mkdir()
        git(self.repo, "init", "-q", "-b", "main")

        (self.repo / "a.txt").write_text("1\n", encoding="utf-8")
        (self.repo / "b.txt").write_text("1\n", encoding="utf-8")
        (self.repo / "c.txt").write_text("1\n", encoding="utf-8")
        git(self.repo, "add", "a.txt", "b.txt", "c.txt")
        git(self.repo, "commit", "-qm", "base")
        self.base = git(self.repo, "rev-parse", "HEAD")

        git(self.repo, "switch", "-c", "up")
        (self.repo / "a.txt").write_text("up\n", encoding="utf-8")
        git(self.repo, "add", "a.txt")
        git(self.repo, "commit", "-qm", "up a")
        (self.repo / "c.txt").write_text("2\n", encoding="utf-8")
        git(self.repo, "add", "c.txt")
        git(self.repo, "commit", "-qm", "up c")
        (self.repo / "d.txt").write_text("1\n", encoding="utf-8")
        git(self.repo, "add", "d.txt")
        git(self.repo, "commit", "-qm", "up d")

        git(self.repo, "switch", "-c", "port", self.base)
        (self.repo / "a.txt").write_text("port\n", encoding="utf-8")
        git(self.repo, "add", "a.txt")
        git(self.repo, "commit", "-qm", "port a")
        (self.repo / "b.txt").write_text("2\n", encoding="utf-8")
        git(self.repo, "add", "b.txt")
        git(self.repo, "commit", "-qm", "port b")
        self.head = git(self.repo, "rev-parse", "HEAD")

    def test_parse_conflicts_reads_content_lines(self):
        text = (
            "CONFLICT (content): Merge conflict in x/y.cpp\n"
            "Auto-merging z.cpp\n"
        )
        self.assertEqual(
            upstream_sync_report.parse_conflicts(text),
            [("content", "x/y.cpp")],
        )

    def test_parse_conflicts_keeps_other_kinds(self):
        text = "CONFLICT (modify/delete): q.txt deleted in up and modified in port.\n"
        self.assertEqual(
            upstream_sync_report.parse_conflicts(text),
            [("modify/delete", "q.txt deleted in up and modified in port.")],
        )

    def test_report_counts(self):
        report = upstream_sync_report.build_report(
            self.repo, "main", "up", "port"
        )
        self.assertEqual(
            report["counts"],
            {
                "commits": 3,
                "upstream_files": 3,
                "both_changed": 1,
                "conflicts": 1,
            },
        )
        self.assertEqual(report["both_changed"], ["a.txt"])
        self.assertEqual(
            report["conflicts"], [{"kind": "content", "path": "a.txt"}]
        )
        self.assertEqual(report["merge_exit"], 1)

    def test_markdown_sections_in_order(self):
        report = upstream_sync_report.build_report(
            self.repo, "main", "up", "port"
        )
        markdown = upstream_sync_report.render_markdown(report)
        headers = [
            "## Коммиты апстрима (3)",
            "## Файлы апстрима (3)",
            "## Пробное слияние",
            "## Файлы, которые меняли обе стороны (1)",
        ]
        positions = [markdown.index(header) for header in headers]
        self.assertEqual(positions, sorted(positions))
        self.assertIn("Конфликтов: 1", markdown)
        self.assertIn("- content: a.txt", markdown)

    def test_main_writes_files_and_leaves_tree(self):
        head_before = git(self.repo, "rev-parse", "HEAD")
        out = self.root / "out"
        result = upstream_sync_report.main(
            [
                "--repo",
                str(self.repo),
                "--base",
                self.base,
                "--target",
                "up",
                "--port",
                "port",
                "--out",
                str(out),
            ]
        )
        self.assertEqual(result, 0)
        self.assertTrue((out / "report.json").is_file())
        self.assertTrue((out / "report.md").is_file())
        self.assertEqual(git(self.repo, "status", "--porcelain"), "")
        self.assertEqual(git(self.repo, "rev-parse", "HEAD"), head_before)

    def test_main_rejects_unknown_revision(self):
        out = self.root / "missing-out"
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            result = upstream_sync_report.main(
                [
                    "--repo",
                    str(self.repo),
                    "--base",
                    self.base,
                    "--target",
                    "nosuchref",
                    "--port",
                    "port",
                    "--out",
                    str(out),
                ]
            )
        self.assertEqual(result, 2)
        self.assertFalse(out.exists())
        self.assertIn("unknown revision: nosuchref", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
