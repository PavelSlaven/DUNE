Port step P15 (`codex-direct/P15/TASK-P15.md`): regular catch-up with upstream.

- New tool `tools/upstream/upstream_sync_report.py`: `--base <last merged upstream SHA> --target <new upstream SHA> --port <port tip> --out <dir> [--repo <path>]` writes `report.md` and `report.json` with the upstream commits, changed files, files changed on both sides and the conflicts of a trial `git merge-tree`. It does not touch the working tree, the index or the object store (the trial merge writes into a temporary object directory inside `--out`).
- `docs/UPSTREAM_SYNC.md`: when to update and the steps from the report to the merge, with the three things that broke most often in P14a.
- Tests: `tools/upstream/tests/test_upstream_sync_report.py`, 6 cases on a temporary repository.

Checks on servak: 6 new tests and the whole `tools/upstream/tests` suite (49) OK; a trial run on the real revisions of step P14a (base `d06f2fcd`, target `d7869e710`, port `0683500a`) reports 48 commits and 27 conflicts with the same paths as the trial merge used for P14a; an unknown revision exits with code 2.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
