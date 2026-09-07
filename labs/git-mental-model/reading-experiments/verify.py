#!/usr/bin/env python3
"""Verify the article's three models with real Git in disposable repositories."""
import os
from pathlib import Path
import subprocess
import tempfile


def git(repo, *args, input=None):
    result = subprocess.run(
        ["git", "-C", str(repo), *args], input=input, text=True,
        capture_output=True, check=True,
        env={**os.environ, "LC_ALL": "C", "GIT_CONFIG_NOSYSTEM": "1",
             "GIT_CONFIG_GLOBAL": os.devnull, "GIT_TERMINAL_PROMPT": "0"},
    )
    return result.stdout.rstrip("\n")


def init(root, name):
    repo = root / name
    repo.mkdir()
    git(repo, "init", "-q", "-b", "main")
    git(repo, "config", "user.name", "Git Learning Lab")
    git(repo, "config", "user.email", "lab@example.invalid")
    git(repo, "config", "commit.gpgsign", "false")
    return repo


def commit(repo, message):
    git(repo, "commit", "-q", "-m", message)


def file_versions(repo, name):
    return [git(repo, "show", f"HEAD:{name}"), git(repo, "show", f":{name}"),
            (repo / name).read_text().rstrip("\n")]


def snapshots(root):
    repo = init(root, "snapshots")
    path = repo / "app.txt"
    path.write_text("version=1\n")
    git(repo, "add", "app.txt")
    commit(repo, "initial snapshot")
    assert file_versions(repo, "app.txt") == ["version=1"] * 3
    path.write_text("version=2\n")
    assert file_versions(repo, "app.txt") == ["version=1", "version=1", "version=2"]
    assert git(repo, "status", "--short") == " M app.txt"
    git(repo, "add", "app.txt")
    assert file_versions(repo, "app.txt") == ["version=1", "version=2", "version=2"]
    path.write_text("version=3\n")
    assert file_versions(repo, "app.txt") == ["version=1", "version=2", "version=3"]
    assert git(repo, "status", "--short") == "MM app.txt"
    commit(repo, "record version 2")
    assert file_versions(repo, "app.txt") == ["version=2", "version=2", "version=3"]
    assert git(repo, "status", "--short") == " M app.txt"
    print("PASS snapshots: all five HEAD / index / working-tree states")


def objects(root):
    repo = init(root, "objects")
    git(repo, "commit", "-q", "--allow-empty", "-m", "parent C1")
    parent = git(repo, "rev-parse", "HEAD")
    (repo / "docs").mkdir()
    for name in ("guide.txt", "copy.txt"):
        (repo / "docs" / name).write_text("hello\n")
    git(repo, "add", "docs")
    commit(repo, "snapshot C2")
    current = git(repo, "rev-parse", "main")
    tree = git(repo, "rev-parse", "main^{tree}")
    subtree = git(repo, "rev-parse", "main:docs")
    blob = git(repo, "rev-parse", "main:docs/guide.txt")
    assert git(repo, "cat-file", "-p", "main").startswith(f"tree {tree}\nparent {parent}\n")
    assert git(repo, "ls-tree", "main") == f"040000 tree {subtree}\tdocs"
    assert git(repo, "ls-tree", "main:docs") == (
        f"100644 blob {blob}\tcopy.txt\n100644 blob {blob}\tguide.txt")
    for name in ("guide.txt", "copy.txt"):
        assert git(repo, "show", f"main:docs/{name}") == "hello"
    assert len({current, tree, subtree, blob}) == 4
    print("PASS objects: commit -> root tree -> docs tree -> shared blob; parent retained")


def draft(root):
    repo = init(root, "draft")
    path = repo / "app.conf"
    # Nine unchanged lines ensure separate hunks with the default diff context.
    middle = "".join(f"setting{i}=unchanged\n" for i in range(1, 10))
    original = f"timeout=10\n{middle}debug=false"
    selected = f"timeout=30\n{middle}debug=false"
    both = f"timeout=30\n{middle}debug=true"
    path.write_text(original + "\n")
    git(repo, "add", "app.conf")
    commit(repo, "initial settings")
    path.write_text(both + "\n")
    assert file_versions(repo, "app.conf") == [original, original, both]
    git(repo, "add", "-p", "--", "app.conf", input="y\nn\n")
    assert file_versions(repo, "app.conf") == [original, selected, both]
    git(repo, "add", "--", "app.conf")
    assert file_versions(repo, "app.conf") == [original, both, both]
    git(repo, "restore", "--staged", "-p", "--", "app.conf", input="n\ny\n")
    assert file_versions(repo, "app.conf") == [original, selected, both]
    commit(repo, "fix: adjust timeout")
    assert file_versions(repo, "app.conf") == [selected, selected, both]
    assert git(repo, "status", "--short") == " M app.conf"
    assert "+debug=true" not in git(repo, "show", "--format=", "HEAD")
    print("PASS draft: real add -p / restore --staged -p; only timeout committed")


if __name__ == "__main__":
    with tempfile.TemporaryDirectory(prefix="my-git-reading-") as directory:
        root = Path(directory)
        snapshots(root)
        objects(root)
        draft(root)
