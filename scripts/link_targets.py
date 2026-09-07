"""Normalize documentation link targets before checking local paths."""
from __future__ import annotations

import urllib.parse
from pathlib import Path


REPO_PAGES_HOST = "xirong.github.io"
REPO_PAGES_PREFIX = "/my-git/"


def normalize_target(raw: str) -> str:
    """Trim a Markdown target and remove optional angle-bracket delimiters."""
    target = raw.strip()
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1].strip()
    return target


def local_path_from_target(target: str) -> str:
    """Return a decoded local pathname, excluding a URL query and fragment.

    Decode only after URL parsing so `%23` continues to represent a literal
    hash character in a filename instead of becoming a fragment delimiter.
    """
    return urllib.parse.unquote(urllib.parse.urlsplit(target).path)


def repo_pages_path(target: str, repo_root: Path) -> Path | None:
    """Map this repository's GitHub Pages URL to a local source path.

    The returned path may not exist so callers can report a broken Pages URL.
    Jekyll-style ``.html`` output is mapped to a same-name Markdown source when
    that source exists. Query strings and fragments never affect the path.
    """
    parsed = urllib.parse.urlsplit(target)
    if (
        parsed.scheme not in {"http", "https"}
        or (parsed.hostname or "").lower() != REPO_PAGES_HOST
        or not parsed.path.startswith(REPO_PAGES_PREFIX)
    ):
        return None

    relative_path = urllib.parse.unquote(parsed.path[len(REPO_PAGES_PREFIX):])
    candidate = (repo_root / relative_path).resolve()
    try:
        candidate.relative_to(repo_root.resolve())
    except ValueError:
        return None

    if candidate.is_dir():
        candidate = candidate / "index.html"
    if candidate.exists():
        return candidate

    if candidate.suffix == ".html":
        markdown_source = candidate.with_suffix(".md")
        if markdown_source.exists():
            return markdown_source
    return candidate
