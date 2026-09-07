#!/usr/bin/env python3
"""Create and verify a disposable Git worktree lab."""
from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


MARKER_NAME = ".my-git-worktree-lab"
MARKER_VALUE = "git-mental-model-09-worktree-v1\n"
PROJECT_ROOT = Path(__file__).resolve().parents[3]


def git_env() -> dict[str, str]:
    env = os.environ.copy()
    for key in list(env):
        if key in {
            "GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_OBJECT_DIRECTORY",
            "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_CEILING_DIRECTORIES",
            "GIT_TEMPLATE_DIR", "GIT_HOOKS_PATH",
        } or key.startswith("GIT_CONFIG_"):
            env.pop(key, None)
    env.update({
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_CONFIG_GLOBAL": os.devnull,
        "GIT_TERMINAL_PROMPT": "0",
        "GIT_PAGER": "cat",
        "LC_ALL": "C",
    })
    return env


def git(*args: str, cwd: Path | None = None, check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        ["git", *args], cwd=cwd, env=git_env(), text=True,
        stdin=subprocess.DEVNULL, capture_output=True,
    )
    if check and result.returncode:
        raise RuntimeError(
            f"git {' '.join(args)} failed ({result.returncode})\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )
    return result


def text(*args: str, cwd: Path | None = None) -> str:
    return git(*args, cwd=cwd).stdout.rstrip("\n")


def git_path(repo: Path, name: str) -> Path:
    path = Path(text("rev-parse", "--git-path", name, cwd=repo))
    return (repo / path).resolve() if not path.is_absolute() else path.resolve()


def configure(repo: Path, hooks_dir: Path) -> None:
    git("config", "user.name", "Git Mental Model Lab", cwd=repo)
    git("config", "user.email", "lab@example.invalid", cwd=repo)
    git("config", "commit.gpgsign", "false", cwd=repo)
    git("config", "core.hooksPath", str(hooks_dir), cwd=repo)
    git("config", "gc.auto", "0", cwd=repo)
    git("config", "maintenance.auto", "false", cwd=repo)


def commit(repo: Path, message: str) -> str:
    git("commit", "-q", "-m", message, cwd=repo)
    return text("rev-parse", "HEAD", cwd=repo)


def create_root(requested: str | None) -> Path:
    if requested:
        root = Path(requested).expanduser()
        if root.exists() and not root.is_dir():
            raise ValueError(f"target exists and is not a directory: {root}")
        root.mkdir(parents=True, exist_ok=True)
        if any(root.iterdir()):
            raise ValueError(f"target directory must be empty: {root}")
    else:
        root = Path(tempfile.mkdtemp(prefix="my-git-worktree-"))
    root = root.resolve()
    if root in {Path("/"), Path.home().resolve(), PROJECT_ROOT.resolve()}:
        raise ValueError(f"refusing protected lab directory: {root}")
    (root / MARKER_NAME).write_text(MARKER_VALUE, encoding="utf-8")
    return root


def require_root(requested: str) -> Path:
    root = Path(requested).expanduser().resolve()
    if root in {Path("/"), Path.home().resolve(), PROJECT_ROOT.resolve()}:
        raise ValueError(f"refusing protected lab directory: {root}")
    marker = root / MARKER_NAME
    if marker.read_text(encoding="utf-8") != MARKER_VALUE:
        raise ValueError(f"not a worktree lab directory: {root}")
    return root


def setup(requested: str | None) -> None:
    root = create_root(requested)
    primary = root / "primary"
    feature = root / "feature"
    disabled_hooks = root / "disabled-hooks"
    disabled_hooks.mkdir()
    git("init", "-q", "-b", "main", str(primary))
    configure(primary, disabled_hooks)
    (primary / "app.txt").write_text("base=1\n", encoding="utf-8")
    git("add", "app.txt", cwd=primary)
    base = commit(primary, "baseline")

    git("worktree", "add", "-q", "-b", "feature/parallel", str(feature), "main", cwd=primary)
    if text("branch", "--show-current", cwd=feature) != "feature/parallel":
        raise AssertionError("different-branch worktree was not created")
    main_common = git_path(primary, "objects").parent
    feature_common = git_path(feature, "objects").parent
    if main_common != feature_common:
        raise AssertionError("worktrees do not share a common Git directory")
    primary_index = git_path(primary, "index")
    feature_index = git_path(feature, "index")
    if primary_index == feature_index:
        raise AssertionError("worktrees unexpectedly share one Index path")

    (primary / "main-note.txt").write_text("owner=main\n", encoding="utf-8")
    git("add", "main-note.txt", cwd=primary)
    (feature / "feature-note.txt").write_text("owner=feature\n", encoding="utf-8")
    git("add", "feature-note.txt", cwd=feature)
    primary_staged = text("diff", "--cached", "--name-only", cwd=primary)
    feature_staged = text("diff", "--cached", "--name-only", cwd=feature)
    if primary_staged != "main-note.txt" or feature_staged != "feature-note.txt":
        raise AssertionError(f"independent Index check failed: {primary_staged!r}, {feature_staged!r}")

    external = root / "external-resource.txt"
    external.write_text("writer=main\n", encoding="utf-8")
    with external.open("a", encoding="utf-8") as handle:
        handle.write("writer=feature\n")
    if external.read_text(encoding="utf-8") != "writer=main\nwriter=feature\n":
        raise AssertionError("external shared resource observation failed")

    feature_commit = commit(feature, "feature contribution")
    main_commit = commit(primary, "main contribution")
    if text("rev-parse", "feature/parallel", cwd=primary) != feature_commit:
        raise AssertionError("shared branch ref is unavailable from the primary worktree")
    git("cat-file", "-e", f"{feature_commit}^{{commit}}", cwd=primary)
    git("merge", "--no-ff", "-m", "integrate feature worktree", "feature/parallel", cwd=primary)
    merge_commit = text("rev-parse", "HEAD", cwd=primary)
    if text("rev-parse", "HEAD", cwd=feature) != feature_commit:
        raise AssertionError("integrating main moved the feature worktree HEAD")
    git("cat-file", "-e", f"{merge_commit}^{{commit}}", cwd=feature)
    if (feature / "main-note.txt").exists():
        raise AssertionError("feature worktree unexpectedly changed after main integration")
    if not (primary / "feature-note.txt").is_file():
        raise AssertionError("integrated feature file is absent from main worktree")

    same_main = root / "same-main"
    same_branch = git("worktree", "add", str(same_main), "main", cwd=primary, check=False)
    if same_branch.returncode == 0:
        raise AssertionError("same branch was checked out in a second worktree")
    if not any(message in same_branch.stderr for message in ("already checked out", "already used by worktree")):
        raise AssertionError(f"same-branch rejection message missing: {same_branch.stderr}")
    if same_main.exists():
        raise AssertionError("failed same-branch add created a worktree directory")

    state = {
        "base": base,
        "feature_commit": feature_commit,
        "main_commit": main_commit,
        "merge_commit": merge_commit,
        "primary_index": str(primary_index),
        "feature_index": str(feature_index),
        "common_dir": str(main_common),
        "same_branch_returncode": same_branch.returncode,
    }
    (root / "state.json").write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    (root / "same-branch-results.txt").write_text(same_branch.stderr, encoding="utf-8")
    (root / "observations.txt").write_text(
        "different branch worktree\n"
        f"  primary branch: main\n"
        "  feature branch: feature/parallel\n"
        f"  shared common Git directory: {main_common}\n"
        f"  primary Index path: {primary_index}\n"
        f"  feature Index path: {feature_index}\n"
        "  staged only in primary: main-note.txt\n"
        "  staged only in feature: feature-note.txt\n\n"
        "integration\n"
        f"  main merge commit: {merge_commit}\n"
        f"  feature tip remains: {feature_commit}\n"
        "  primary can read the feature commit; feature can read the merge commit\n\n"
        "same branch attempt\n"
        "  a second checkout of main was rejected by Git\n\n"
        "external resource\n"
        "  external-resource.txt is outside both worktrees and was written by both contexts\n",
        encoding="utf-8",
    )
    print(root)


def verify(requested: str) -> None:
    root = require_root(requested)
    state = json.loads((root / "state.json").read_text(encoding="utf-8"))
    primary = root / "primary"
    feature = root / "feature"
    checks = [
        (text("branch", "--show-current", cwd=primary) == "main", "primary no longer checks out main"),
        (text("branch", "--show-current", cwd=feature) == "feature/parallel", "feature worktree branch changed"),
        (text("rev-parse", "HEAD", cwd=primary) == state["merge_commit"], "merge commit changed"),
        (text("rev-parse", "HEAD", cwd=feature) == state["feature_commit"], "feature tip changed"),
        (text("rev-parse", "feature/parallel", cwd=primary) == state["feature_commit"], "shared ref missing in primary"),
        (git("merge-base", "--is-ancestor", state["feature_commit"], state["merge_commit"], cwd=primary, check=False).returncode == 0, "feature is not integrated into main"),
        (git_path(primary, "index") != git_path(feature, "index"), "Index paths became shared"),
        (str(git_path(primary, "objects").parent) == state["common_dir"], "primary common directory changed"),
        (str(git_path(feature, "objects").parent) == state["common_dir"], "feature common directory changed"),
        (text("status", "--short", cwd=primary) == "", "primary has unexpected changes"),
        (text("status", "--short", cwd=feature) == "", "feature has unexpected changes"),
        ((primary / "main-note.txt").read_text(encoding="utf-8") == "owner=main\n", "main file mismatch"),
        ((primary / "feature-note.txt").read_text(encoding="utf-8") == "owner=feature\n", "integrated feature file mismatch"),
        (not (feature / "main-note.txt").exists(), "feature worktree leaked main file"),
        ((root / "external-resource.txt").read_text(encoding="utf-8") == "writer=main\nwriter=feature\n", "external resource observation changed"),
        (state["same_branch_returncode"] != 0, "same branch add unexpectedly succeeded"),
        (any(message in (root / "same-branch-results.txt").read_text(encoding="utf-8") for message in ("already checked out", "already used by worktree")), "same branch rejection evidence missing"),
    ]
    failures = [message for passed, message in checks if not passed]
    if failures:
        raise AssertionError("; ".join(failures))
    print("ok: main and feature worktrees share objects and branch refs while using distinct HEAD/Index/working-tree state")
    print("ok: staged paths remained isolated until each worktree committed its own change")
    print("ok: Git rejected a second checkout of main and allowed the different feature branch")
    print("ok: integration made the feature commit visible from main without moving feature HEAD")
    print("ok: the external file was outside Git worktree isolation")


def cleanup(requested: str) -> None:
    root = require_root(requested)
    if not (root / "primary" / ".git").exists() or not (root / "feature" / ".git").exists():
        raise ValueError(f"worktree lab structure is incomplete: {root}")
    shutil.rmtree(root)
    print(f"removed lab directory: {root}")


def main(argv: list[str]) -> int:
    try:
        if argv[1:] and argv[1] == "setup" and len(argv) in {2, 3}:
            setup(argv[2] if len(argv) == 3 else None)
        elif len(argv) == 3 and argv[1] == "verify":
            verify(argv[2])
        elif len(argv) == 3 and argv[1] == "cleanup":
            cleanup(argv[2])
        else:
            raise ValueError("usage: lab.py setup [target-directory] | verify <lab-directory> | cleanup <lab-directory>")
    except (AssertionError, OSError, RuntimeError, ValueError, json.JSONDecodeError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
