#!/usr/bin/env python3
"""Regression checks for the Git command patterns in the old documentation."""
from __future__ import annotations

import os
from pathlib import Path
import subprocess
import tempfile


def git_env() -> dict[str, str]:
    """Avoid the host's aliases, config, signing, and hooks during the lab."""
    env = os.environ.copy()
    for key in list(env):
        if key.startswith("GIT_"):
            env.pop(key)
    env.update(
        {
            "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_CONFIG_GLOBAL": os.devnull,
            "GIT_TERMINAL_PROMPT": "0",
            "GIT_PAGER": "cat",
            "GIT_EDITOR": "true",
            "LC_ALL": "C",
        }
    )
    return env


def run_git(
    repo: Path,
    *args: str,
    check: bool = True,
    input_text: str | None = None,
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        ["git", *args],
        cwd=repo,
        env=git_env(),
        text=True,
        input=input_text,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if check and result.returncode != 0:
        raise AssertionError(
            f"git {' '.join(args)} failed with {result.returncode}\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )
    return result


def output(repo: Path, *args: str) -> str:
    return run_git(repo, *args).stdout.strip()


def write(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def make_repo(root: Path, name: str, branch: str = "master") -> Path:
    repo = root / name
    repo.mkdir()
    run_git(repo, "init", "-q", "-b", branch)
    (repo / ".safe-hooks").mkdir()
    run_git(repo, "config", "user.name", "Safety Lab")
    run_git(repo, "config", "user.email", "safety-lab@example.invalid")
    run_git(repo, "config", "commit.gpgsign", "false")
    run_git(repo, "config", "core.hooksPath", str(repo / ".safe-hooks"))
    return repo


def commit_all(repo: Path, message: str) -> None:
    run_git(repo, "add", "--all")
    run_git(repo, "commit", "-q", "-m", message)


def snapshot(repo: Path, paths: list[str]) -> dict[str, object]:
    return {
        "branch": output(repo, "branch", "--show-current"),
        "head": output(repo, "rev-parse", "HEAD"),
        "index_tree": output(repo, "write-tree"),
        "status": output(repo, "status", "--porcelain"),
        "files": {path: (repo / path).read_bytes() for path in paths},
    }


def assert_contains(text: str, fragment: str, message: str) -> None:
    if fragment not in text:
        raise AssertionError(f"{message}: expected {fragment!r} in:\n{text}")


def test_dirty_precondition_stops_without_mutating(root: Path) -> None:
    repo = make_repo(root, "dirty-precondition")
    write(repo / "user-staged.txt", "base staged\n")
    write(repo / "user-unstaged.txt", "base unstaged\n")
    commit_all(repo, "base")

    write(repo / "user-staged.txt", "user staged edit\n")
    run_git(repo, "add", "user-staged.txt")
    write(repo / "user-unstaged.txt", "user unstaged edit\n")
    write(repo / "user-untracked.txt", "user untracked edit\n")
    before = snapshot(
        repo,
        ["user-staged.txt", "user-unstaged.txt", "user-untracked.txt"],
    )

    # Exact documented precondition: inspect and stop while any output exists.
    stopped = bool(output(repo, "status", "--porcelain"))
    if not stopped:
        raise AssertionError("the deliberately dirty worktree did not trigger the stop condition")

    after = snapshot(
        repo,
        ["user-staged.txt", "user-unstaged.txt", "user-untracked.txt"],
    )
    if after != before:
        raise AssertionError("the dirty-worktree stop condition changed repository state")
    assert_contains(str(after["status"]), "M  user-staged.txt", "staged edit was not preserved")
    assert_contains(str(after["status"]), " M user-unstaged.txt", "unstaged edit was not preserved")
    assert_contains(str(after["status"]), "?? user-untracked.txt", "untracked edit was not preserved")
    print("ok: dirty precondition stops before rewrite or cleanup and preserves branch, Index, Working Tree, and untracked content")


def test_path_only_commit_preserves_unrelated_work(root: Path) -> None:
    repo = make_repo(root, "path-only-commit")
    write(repo / "agent.txt", "base agent\n")
    write(repo / "user-staged.txt", "base staged\n")
    write(repo / "user-unstaged.txt", "base unstaged\n")
    commit_all(repo, "base")

    write(repo / "user-staged.txt", "user staged edit\n")
    run_git(repo, "add", "user-staged.txt")
    write(repo / "user-unstaged.txt", "user unstaged edit\n")
    write(repo / "user-untracked.txt", "user untracked edit\n")
    write(repo / "agent.txt", "agent-owned complete path\n")
    before_branch = output(repo, "branch", "--show-current")
    staged_before = output(repo, "show", ":user-staged.txt")
    unstaged_before = (repo / "user-unstaged.txt").read_text(encoding="utf-8")
    untracked_before = (repo / "user-untracked.txt").read_text(encoding="utf-8")

    # Exact documented path-only commit flow. The target path is tracked and wholly owned.
    run_git(repo, "commit", "--only", "-m", "commit agent path only", "--", "agent.txt")

    if output(repo, "branch", "--show-current") != before_branch:
        raise AssertionError("path-only commit changed branch name")
    if output(repo, "show", "HEAD:agent.txt") != "agent-owned complete path":
        raise AssertionError("path-only commit did not record the named agent path")
    if output(repo, "show", "HEAD:user-staged.txt") != "base staged":
        raise AssertionError("path-only commit incorrectly included unrelated staged content")
    if output(repo, "show", ":user-staged.txt") != staged_before:
        raise AssertionError("path-only commit changed unrelated staged content")
    if (repo / "user-unstaged.txt").read_text(encoding="utf-8") != unstaged_before:
        raise AssertionError("path-only commit changed unrelated unstaged content")
    if (repo / "user-untracked.txt").read_text(encoding="utf-8") != untracked_before:
        raise AssertionError("path-only commit changed unrelated untracked content")
    status = output(repo, "status", "--porcelain")
    assert_contains(status, "M  user-staged.txt", "unrelated staged state was not preserved")
    assert_contains(status, " M user-unstaged.txt", "unrelated unstaged state was not preserved")
    assert_contains(status, "?? user-untracked.txt", "unrelated untracked state was not preserved")
    print("ok: git commit --only records a wholly owned task path and preserves unrelated staged, unstaged, and untracked work")


def prepare_large_commit(repo: Path) -> tuple[str, str]:
    base = "".join(f"line {number:02d}=base\n" for number in range(1, 22))
    changed = base.replace("line 02=base", "line 02=selected").replace(
        "line 19=base", "line 19=left-unselected"
    )
    write(repo / "story.txt", base)
    commit_all(repo, "base")
    write(repo / "story.txt", changed)
    run_git(repo, "add", "story.txt")
    run_git(repo, "commit", "-q", "-m", "large change")
    return base, changed


def test_soft_reset_counterexample_and_corrected_flow(root: Path) -> None:
    counterexample = make_repo(root, "soft-reset-counterexample")
    _, changed = prepare_large_commit(counterexample)
    run_git(counterexample, "reset", "--soft", "HEAD~1")
    index_before_add_p = output(counterexample, "write-tree")

    # `add -p` compares Index with Working Tree. After --soft they are already equal,
    # so it has no hunk to remove from the Index.
    run_git(counterexample, "add", "-p", "--", "story.txt", input_text="n\nn\n")
    if output(counterexample, "write-tree") != index_before_add_p:
        raise AssertionError("direct add -p unexpectedly changed the soft-reset Index")
    cached = output(counterexample, "diff", "--cached", "--", "story.txt")
    assert_contains(cached, "line 02=selected", "counterexample did not retain first staged hunk")
    assert_contains(cached, "line 19=left-unselected", "counterexample did not retain second staged hunk")
    if output(counterexample, "diff", "--", "story.txt"):
        raise AssertionError("soft reset should leave this large commit identical in Index and Working Tree")
    run_git(counterexample, "commit", "-q", "-m", "incorrect split")
    counterexample_commit = output(counterexample, "show", "HEAD:story.txt")
    if counterexample_commit != changed.strip():
        raise AssertionError("counterexample commit did not contain every originally staged hunk")

    corrected = make_repo(root, "soft-reset-corrected")
    prepare_large_commit(corrected)
    run_git(corrected, "reset", "--soft", "HEAD~1")
    run_git(corrected, "reset")
    if output(corrected, "diff", "--cached", "--", "story.txt"):
        raise AssertionError("mixed reset did not clear the Index before partial staging")
    unstaged = output(corrected, "diff", "--", "story.txt")
    assert_contains(unstaged, "line 02=selected", "corrected flow lost first working-tree hunk")
    assert_contains(unstaged, "line 19=left-unselected", "corrected flow lost second working-tree hunk")

    run_git(corrected, "add", "-p", "--", "story.txt", input_text="y\nn\n")
    selected = output(corrected, "diff", "--cached", "--", "story.txt")
    remaining = output(corrected, "diff", "--", "story.txt")
    assert_contains(selected, "line 02=selected", "selected hunk was not staged")
    if "line 19=left-unselected" in selected:
        raise AssertionError("unselected hunk remained staged in corrected flow")
    assert_contains(remaining, "line 19=left-unselected", "unselected hunk did not remain in Working Tree")
    if "line 02=selected" in remaining:
        raise AssertionError("selected hunk remained unstaged in corrected flow")
    run_git(corrected, "commit", "-q", "-m", "selected hunk only")
    committed = output(corrected, "show", "HEAD:story.txt")
    assert_contains(committed, "line 02=selected", "corrected commit omitted selected hunk")
    if "line 19=left-unselected" in committed:
        raise AssertionError("corrected commit included the unselected hunk")
    assert_contains(
        output(corrected, "diff", "--", "story.txt"),
        "line 19=left-unselected",
        "unselected hunk was not left for the next commit",
    )
    print("ok: soft reset followed directly by add -p keeps all hunks staged; reset then add -p commits only the selected hunk")


def test_non_main_integration_branch(root: Path) -> None:
    repo = make_repo(root, "non-main-branch", branch="master")
    write(repo / "base.txt", "base\n")
    commit_all(repo, "base")
    before = snapshot(repo, ["base.txt"])

    wrong_branch = run_git(repo, "switch", "main", check=False)
    if wrong_branch.returncode == 0:
        raise AssertionError("git switch main unexpectedly succeeded in a master-only repository")
    if snapshot(repo, ["base.txt"]) != before:
        raise AssertionError("failed git switch main changed state in a master-only repository")

    # Exact documented substitution for <integration-branch>.
    run_git(repo, "switch", "master")
    run_git(repo, "switch", "-c", "feat/uses-actual-base")
    if output(repo, "branch", "--show-current") != "feat/uses-actual-base":
        raise AssertionError("actual integration branch did not create the feature branch")
    if output(repo, "rev-parse", "HEAD") != str(before["head"]):
        raise AssertionError("feature branch did not start from the actual integration branch")
    print("ok: a master integration branch rejects the hard-coded main command and works through <integration-branch>")


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="my-git-command-safety-") as temporary_root:
        root = Path(temporary_root)
        test_dirty_precondition_stops_without_mutating(root)
        test_path_only_commit_preserves_unrelated_work(root)
        test_soft_reset_counterexample_and_corrected_flow(root)
        test_non_main_integration_branch(root)


if __name__ == "__main__":
    main()
