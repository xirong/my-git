#!/usr/bin/env python3
from __future__ import annotations

import re
import subprocess
import sys
import urllib.parse
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]

DOC_ROOTS = [
    "README.md",
    "README.zh-CN.md",
    ".github",
    "00-meta",
    "01-getting-started",
    "02-daily-workflow",
    "03-team-collaboration",
    "04-github-engineering",
    "05-ai-native-development",
    "06-troubleshooting",
    "07-large-repo",
    "08-templates",
    "09-resources",
    "10-company-practices",
]

SKIP_PARTS = {
    ".git",
    "09-resources/legacy",
}

FORBIDDEN_LITERAL = [
    "——",
    "门禁",
    "重启",
    "重新维护",
    "断更",
    "中断",
    "Reboot",
    "reboot",
    "当前阶段",
    "先写中文",
    "后面补英文",
    "英文版",
    "翻译成英文",
    "而不是",
]

FORBIDDEN_REGEX = [
    re.compile(r"不是.{0,40}而是"),
    re.compile(r"不在于.{0,40}而在"),
]

FORBIDDEN_TRACKED_EXTENSIONS = {
    ".pdf",
    ".doc",
    ".docx",
    ".ppt",
    ".pptx",
    ".key",
}

FORBIDDEN_TRACKED_NAMES = {
    ".DS_Store",
}

ALLOWED_TRACKED_ARTIFACTS = {
    "command-handbook/git-cheat-sheet.pdf",
    "ebooks/Git Community Book.pdf",
    "ebooks/Git Magic.pdf",
    "ebooks/git-internals.pdf",
    "ebooks/progit_v2.1.37.pdf",
}


def rel(path: Path) -> str:
    return str(path.relative_to(REPO_ROOT))


def is_skipped(path: Path) -> bool:
    rel_path = rel(path)
    return any(rel_path == part or rel_path.startswith(part + "/") for part in SKIP_PARTS)


def markdown_files() -> list[Path]:
    files: list[Path] = []
    for item in DOC_ROOTS:
        path = REPO_ROOT / item
        if not path.exists():
            continue
        if path.is_file() and path.suffix == ".md" and not is_skipped(path):
            files.append(path)
        elif path.is_dir():
            files.extend(
                p for p in path.rglob("*.md")
                if p.is_file() and not is_skipped(p)
            )
    return sorted(set(files))


def check_local_links(files: list[Path]) -> list[str]:
    pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    errors: list[str] = []

    for path in files:
        text = path.read_text(encoding="utf-8")
        for match in pattern.finditer(text):
            raw = match.group(1).strip()
            if not raw or raw.startswith(("#", "http://", "https://", "mailto:")):
                continue

            target = raw.split("#", 1)[0]
            target = urllib.parse.unquote(target)
            if target.startswith("<") and target.endswith(">"):
                target = target[1:-1]

            resolved = (path.parent / target).resolve()
            if not resolved.exists():
                line = text[:match.start()].count("\n") + 1
                errors.append(f"{rel(path)}:{line}: broken local link: {raw}")

    return errors


def check_forbidden_text(files: list[Path]) -> list[str]:
    errors: list[str] = []

    for path in files:
        for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            for token in FORBIDDEN_LITERAL:
                if token in line:
                    errors.append(f"{rel(path)}:{line_no}: forbidden text: {token}")
            for pattern in FORBIDDEN_REGEX:
                if pattern.search(line):
                    errors.append(f"{rel(path)}:{line_no}: forbidden pattern: {pattern.pattern}")

    return errors


def tracked_files() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=REPO_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    return [REPO_ROOT / line for line in result.stdout.splitlines() if line]


def check_tracked_files(files: list[Path]) -> list[str]:
    errors: list[str] = []
    for path in files:
        rel_path = rel(path)
        if path.name in FORBIDDEN_TRACKED_NAMES:
            errors.append(f"{rel_path}: forbidden tracked file name")
        if path.suffix.lower() in FORBIDDEN_TRACKED_EXTENSIONS and rel_path not in ALLOWED_TRACKED_ARTIFACTS:
            errors.append(f"{rel_path}: forbidden tracked document artifact")
    return errors


def main() -> int:
    files = markdown_files()
    checks = {
        "local links": check_local_links(files),
        "forbidden text": check_forbidden_text(files),
        "tracked files": check_tracked_files(tracked_files()),
    }

    failed = False
    for name, errors in checks.items():
        if not errors:
            print(f"ok: {name}")
            continue
        failed = True
        print(f"failed: {name}")
        for error in errors:
            print(f"  {error}")

    if failed:
        return 1

    print(f"checked {len(files)} markdown files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
