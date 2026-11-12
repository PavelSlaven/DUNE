from __future__ import annotations

import argparse
import json
import os
import sys
import subprocess
import tempfile
from pathlib import Path


class UnknownRevision(Exception):
    pass


class InvalidBase(Exception):
    pass


class GitCommandError(Exception):
    pass


def run_git(
    repo: str | Path, *args: str, env: dict[str, str] | None = None
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        check=False,
        capture_output=True,
        text=True,
        cwd=repo,
        env=env,
    )


def git_output(repo: str | Path, *args: str) -> str:
    result = run_git(repo, *args)
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip()
        raise GitCommandError(detail or f"git {' '.join(args)} failed")
    return result.stdout


def resolve_revision(repo: str | Path, revision: str) -> str:
    result = run_git(repo, "rev-parse", "--verify", "-q", f"{revision}^{{commit}}")
    if result.returncode != 0:
        raise UnknownRevision(revision)
    return result.stdout.strip()


def parse_conflicts(text: str) -> list[tuple[str, str]]:
    conflicts = []
    for line in text.splitlines():
        if not line.startswith("CONFLICT ("):
            continue
        header, separator, detail = line[len("CONFLICT ("):].partition("): ")
        if not separator:
            continue
        path = detail
        content_prefix = "Merge conflict in "
        if path.startswith(content_prefix):
            path = path[len(content_prefix):]
        conflicts.append((header, path))
    return conflicts


def parse_upstream_files(text: str) -> list[dict[str, str]]:
    files = []
    for line in text.splitlines():
        fields = line.split("\t")
        if len(fields) < 2:
            continue
        status = fields[0]
        path = fields[-1] if status.startswith("R") else fields[1]
        files.append({"status": status, "path": path})
    return files


def run_merge_tree(
    repo: str | Path,
    port: str,
    target: str,
    temporary_parent: str | Path | None,
) -> subprocess.CompletedProcess[str]:
    args = (
        "merge-tree",
        "--write-tree",
        "--name-only",
        "--messages",
        port,
        target,
    )
    if temporary_parent is None:
        return run_git(repo, *args)

    parent = Path(temporary_parent).resolve()
    parent.mkdir(parents=True, exist_ok=True)
    object_path = Path(
        git_output(repo, "rev-parse", "--git-path", "objects").strip()
    )
    if not object_path.is_absolute():
        object_path = Path(repo) / object_path
    with tempfile.TemporaryDirectory(prefix=".merge-tree-", dir=parent) as object_dir:
        env = os.environ.copy()
        env["GIT_OBJECT_DIRECTORY"] = str(Path(object_dir).resolve())
        env["GIT_ALTERNATE_OBJECT_DIRECTORIES"] = str(object_path.resolve())
        return run_git(repo, *args, env=env)


def build_report(
    repo: str | Path,
    base: str,
    target: str,
    port: str,
    temporary_parent: str | Path | None = None,
) -> dict:
    base_sha = resolve_revision(repo, base)
    target_sha = resolve_revision(repo, target)
    port_sha = resolve_revision(repo, port)

    ancestor = run_git(repo, "merge-base", "--is-ancestor", base_sha, target_sha)
    if ancestor.returncode != 0:
        raise InvalidBase()

    commit_text = git_output(
        repo,
        "log",
        "--format=%h%x09%s",
        "--no-merges",
        f"{base_sha}..{target_sha}",
    )
    commits = []
    for line in commit_text.splitlines():
        sha, separator, subject = line.partition("\t")
        if separator:
            commits.append({"sha": sha, "subject": subject})

    upstream_files = parse_upstream_files(
        git_output(repo, "diff", "--name-status", base_sha, target_sha)
    )
    port_base = git_output(repo, "merge-base", port_sha, target_sha).strip()
    port_files = set(
        git_output(repo, "diff", "--name-only", port_base, port_sha).splitlines()
    )
    both_changed = sorted(
        {entry["path"] for entry in upstream_files}.intersection(port_files)
    )

    merge = run_merge_tree(
        repo, port_sha, target_sha, temporary_parent
    )
    conflicts = [
        {"kind": kind, "path": path}
        for kind, path in parse_conflicts(merge.stdout + merge.stderr)
    ]

    return {
        "base": base_sha,
        "target": target_sha,
        "port": port_sha,
        "port_base": port_base,
        "commits": commits,
        "upstream_files": upstream_files,
        "both_changed": both_changed,
        "merge_exit": merge.returncode,
        "conflicts": conflicts,
        "counts": {
            "commits": len(commits),
            "upstream_files": len(upstream_files),
            "both_changed": len(both_changed),
            "conflicts": len(conflicts),
        },
    }


def render_markdown(report: dict) -> str:
    lines = [
        "# Отчёт об обновлении с апстрима",
        f"- База: {report['base']}",
        f"- Цель: {report['target']}",
        f"- Порт: {report['port']}",
        "",
        f"## Коммиты апстрима ({report['counts']['commits']})",
    ]
    lines.extend(
        f"- {commit['sha']} {commit['subject']}" for commit in report["commits"]
    )
    lines.extend(["", f"## Файлы апстрима ({report['counts']['upstream_files']})"])
    lines.extend(
        f"- {entry['status']} {entry['path']}"
        for entry in report["upstream_files"]
    )
    lines.extend(
        [
            "",
            "## Пробное слияние",
            f"Код merge-tree: {report['merge_exit']}",
            f"Конфликтов: {report['counts']['conflicts']}",
        ]
    )
    lines.extend(
        f"- {conflict['kind']}: {conflict['path']}"
        for conflict in report["conflicts"]
    )
    lines.extend(
        [
            "",
            "## Файлы, которые меняли обе стороны "
            f"({report['counts']['both_changed']})",
        ]
    )
    lines.extend(f"- {path}" for path in report["both_changed"])
    return "\n".join(lines) + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", required=True)
    parser.add_argument("--target", required=True)
    parser.add_argument("--port", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--repo", default=".")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        report = build_report(
            args.repo, args.base, args.target, args.port, temporary_parent=args.out
        )
    except UnknownRevision as error:
        print(f"unknown revision: {error}", file=sys.stderr)
        return 2
    except InvalidBase:
        print("base is not an ancestor of target", file=sys.stderr)
        return 2
    except (GitCommandError, OSError) as error:
        print(f"cannot create upstream sync report: {error}", file=sys.stderr)
        return 1

    out = Path(args.out)
    try:
        out.mkdir(parents=True, exist_ok=True)
        (out / "report.json").write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )
        (out / "report.md").write_text(
            render_markdown(report), encoding="utf-8", newline="\n"
        )
    except OSError as error:
        print(f"cannot write upstream sync report: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
