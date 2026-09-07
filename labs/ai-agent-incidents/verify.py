#!/usr/bin/env python3
"""Run disposable Git experiments for the Agent incident-recovery article."""
from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


MARKER_NAME = ".ai-agent-incidents-lab-marker"
MARKER_VALUE = "ai-agent-incidents-v1\n"
PREFIX = "my-git-ai-agent-incidents-"
REPOSITORY_ROOT = Path(__file__).resolve().parents[2]


def git_env() -> dict[str, str]:
    """Run Git without the caller's hooks, identity, or repository overrides."""
    env = os.environ.copy()
    for key in list(env):
        if key in {
            "GIT_DIR",
            "GIT_WORK_TREE",
            "GIT_INDEX_FILE",
            "GIT_OBJECT_DIRECTORY",
            "GIT_ALTERNATE_OBJECT_DIRECTORIES",
            "GIT_CEILING_DIRECTORIES",
            "GIT_TEMPLATE_DIR",
            "GIT_HOOKS_PATH",
        } or key.startswith("GIT_CONFIG_"):
            env.pop(key, None)
    env.update(
        {
            "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_CONFIG_GLOBAL": os.devnull,
            "GIT_TERMINAL_PROMPT": "0",
            "GIT_PAGER": "cat",
            "LC_ALL": "C",
            "PYTHONDONTWRITEBYTECODE": "1",
        }
    )
    return env


def run_git(
    directory: Path, *arguments: str, check: bool = True
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        ["git", "-C", str(directory), *arguments],
        env=git_env(),
        text=True,
        stdin=subprocess.DEVNULL,
        capture_output=True,
    )
    if check and result.returncode:
        raise RuntimeError(
            f"git {' '.join(arguments)} failed ({result.returncode})\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )
    return result


def git_output(directory: Path, *arguments: str) -> str:
    return run_git(directory, *arguments).stdout.strip()


def write(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def configure(repository: Path, hooks_dir: Path) -> None:
    hooks_dir.mkdir(parents=True, exist_ok=True)
    for key, value in (
        ("user.name", "AI Agent Incident Lab"),
        ("user.email", "lab@example.invalid"),
        ("commit.gpgsign", "false"),
        ("tag.gpgsign", "false"),
        ("core.hooksPath", str(hooks_dir)),
        ("core.autocrlf", "false"),
        ("gc.auto", "0"),
        ("maintenance.auto", "false"),
    ):
        run_git(repository, "config", key, value)


def init_repository(root: Path, name: str) -> Path:
    repository = root / name
    run_git(root, "init", "-q", "-b", "main", str(repository))
    configure(repository, root / f"{name}-hooks")
    return repository


def commit(repository: Path, message: str, *paths: str) -> str:
    run_git(repository, "add", "--", *paths)
    run_git(repository, "commit", "-q", "-m", message)
    return git_output(repository, "rev-parse", "HEAD")


def create_root() -> Path:
    root = Path(tempfile.mkdtemp(prefix=PREFIX)).resolve()
    if root in {Path("/"), Path.home().resolve(), REPOSITORY_ROOT.resolve()}:
        raise ValueError(f"refusing protected lab root: {root}")
    write(root / MARKER_NAME, MARKER_VALUE)
    return root


def require_root(value: str) -> Path:
    root = Path(value).resolve()
    if root in {Path("/"), Path.home().resolve(), REPOSITORY_ROOT.resolve()}:
        raise ValueError(f"refusing protected cleanup root: {root}")
    if not root.name.startswith(PREFIX):
        raise ValueError(f"not an incident-lab directory: {root}")
    marker = root / MARKER_NAME
    if marker.read_text(encoding="utf-8") != MARKER_VALUE:
        raise ValueError(f"incident-lab marker is missing or invalid: {root}")
    return root


def check_unshared_range(root: Path) -> dict[str, str]:
    repository = init_repository(root, "unshared")
    write(repository / "app.txt", "mode=base\n")
    base = commit(repository, "baseline", "app.txt")
    write(repository / "agent-a.txt", "agent change A\n")
    agent_first = commit(repository, "agent: first local change", "agent-a.txt")
    write(repository / "app.txt", "mode=agent\n")
    agent_last = commit(repository, "agent: second local change", "app.txt")

    if git_output(repository, "status", "--short"):
        raise AssertionError("unshared setup is unexpectedly dirty")
    if git_output(repository, "log", "--format=%s", f"{base}..HEAD").splitlines() != [
        "agent: second local change",
        "agent: first local change",
    ]:
        raise AssertionError("unshared range contains an unexpected commit")

    run_git(repository, "branch", "recovery/before-agent-reset", "HEAD")
    recovery = git_output(repository, "rev-parse", "recovery/before-agent-reset")
    run_git(repository, "reset", "--hard", base)
    if git_output(repository, "rev-parse", "HEAD") != base:
        raise AssertionError("unshared reset did not return to the verified base")
    if git_output(repository, "rev-parse", "recovery/before-agent-reset") != recovery:
        raise AssertionError("unshared recovery ref moved unexpectedly")
    if (repository / "agent-a.txt").exists():
        raise AssertionError("unshared reset retained an agent-only file")
    if (repository / "app.txt").read_text(encoding="utf-8") != "mode=base\n":
        raise AssertionError("unshared reset did not restore the base content")
    if git_output(repository, "status", "--short"):
        raise AssertionError("unshared reset left the repository dirty")
    return {
        "base": base,
        "agent_first": agent_first,
        "agent_last": agent_last,
        "recovery_ref": recovery,
        "final_head": git_output(repository, "rev-parse", "HEAD"),
    }


def check_shared_reverts(root: Path) -> dict[str, str]:
    remote = root / "shared-remote.git"
    run_git(root, "init", "--bare", "-q", str(remote))
    repository = init_repository(root, "shared-producer")
    run_git(repository, "remote", "add", "origin", str(remote))
    write(repository / "setting.txt", "mode=base\n")
    base = commit(repository, "baseline", "setting.txt")
    run_git(repository, "push", "-q", "-u", "origin", "main")

    write(repository / "agent-a.txt", "agent-only file\n")
    agent_first = commit(repository, "agent: add generated file", "agent-a.txt")
    write(repository / "human-note.txt", "human contribution\n")
    human = commit(repository, "human: retain this note", "human-note.txt")
    write(repository / "setting.txt", "mode=agent\n")
    agent_last = commit(repository, "agent: change setting", "setting.txt")
    run_git(repository, "push", "-q", "origin", "main")

    run_git(repository, "revert", "--no-edit", agent_last, agent_first)
    final_head = git_output(repository, "rev-parse", "HEAD")
    run_git(repository, "push", "-q", "origin", "main")
    if (repository / "agent-a.txt").exists():
        raise AssertionError("shared revert retained an agent-only file")
    if (repository / "setting.txt").read_text(encoding="utf-8") != "mode=base\n":
        raise AssertionError("shared revert did not restore the agent setting")
    if (repository / "human-note.txt").read_text(encoding="utf-8") != "human contribution\n":
        raise AssertionError("shared revert removed the intervening human contribution")
    if git_output(repository, "status", "--short"):
        raise AssertionError("shared revert left the repository dirty")
    remote_head = subprocess.run(
        ["git", "--git-dir", str(remote), "rev-parse", "refs/heads/main"],
        env=git_env(),
        text=True,
        stdin=subprocess.DEVNULL,
        capture_output=True,
        check=False,
    )
    if remote_head.returncode or remote_head.stdout.strip() != final_head:
        raise AssertionError("local bare remote did not receive the revert result")
    return {
        "base": base,
        "agent_first": agent_first,
        "human": human,
        "agent_last": agent_last,
        "final_head": final_head,
        "remote_head": remote_head.stdout.strip(),
    }


def check_revert_abort(root: Path) -> dict[str, str]:
    repository = init_repository(root, "revert-conflict")
    write(repository / "config.txt", "mode=base\n")
    commit(repository, "baseline", "config.txt")
    write(repository / "config.txt", "mode=agent\n")
    agent = commit(repository, "agent: change config", "config.txt")
    write(repository / "config.txt", "mode=human\n")
    before_revert = commit(repository, "human: follow-up config", "config.txt")

    conflicted = run_git(repository, "revert", "--no-edit", agent, check=False)
    if conflicted.returncode == 0:
        raise AssertionError("revert unexpectedly completed without the intended conflict")
    if "UU config.txt" not in git_output(repository, "status", "--short"):
        raise AssertionError("revert conflict did not leave the expected unmerged path")
    if "<<<<<<<" not in (repository / "config.txt").read_text(encoding="utf-8"):
        raise AssertionError("revert conflict did not leave conflict markers for inspection")
    run_git(repository, "revert", "--abort")
    if git_output(repository, "rev-parse", "HEAD") != before_revert:
        raise AssertionError("revert abort did not return to the pre-revert HEAD")
    if (repository / "config.txt").read_text(encoding="utf-8") != "mode=human\n":
        raise AssertionError("revert abort did not restore the pre-revert file")
    if git_output(repository, "status", "--short"):
        raise AssertionError("revert abort left the repository dirty")
    return {
        "agent": agent,
        "before_revert": before_revert,
        "conflict_returncode": str(conflicted.returncode),
        "final_head": git_output(repository, "rev-parse", "HEAD"),
    }


def check_worktree_protection(root: Path) -> dict[str, str]:
    repository = init_repository(root, "worktree-primary")
    write(repository / "tracked.txt", "base\n")
    commit(repository, "baseline", "tracked.txt")

    dirty = root / "dirty-worktree"
    run_git(repository, "worktree", "add", "-q", "--detach", str(dirty), "HEAD")
    write(dirty / "tracked.txt", "unsaved agent edit\n")
    removal = run_git(repository, "worktree", "remove", str(dirty), check=False)
    if removal.returncode == 0:
        raise AssertionError("ordinary worktree removal accepted dirty content")
    if not dirty.is_dir() or (dirty / "tracked.txt").read_text(encoding="utf-8") != "unsaved agent edit\n":
        raise AssertionError("failed ordinary removal did not preserve the dirty worktree")
    if "M tracked.txt" not in git_output(dirty, "status", "--short"):
        raise AssertionError("dirty worktree state was not preserved after rejected removal")

    locked = root / "locked-worktree"
    run_git(repository, "worktree", "add", "-q", "--detach", str(locked), "HEAD")
    run_git(repository, "worktree", "lock", "--reason", "incident evidence pending", str(locked))
    before_missing = git_output(repository, "worktree", "list", "--porcelain")
    if str(locked) not in before_missing or "locked incident evidence pending" not in before_missing:
        raise AssertionError("worktree lock was not recorded")

    # This is a marked temporary lab directory only. It simulates a removable
    # worktree becoming unavailable so that prune behavior can be observed.
    shutil.rmtree(locked)
    run_git(repository, "worktree", "prune", "--verbose")
    after_locked_prune = git_output(repository, "worktree", "list", "--porcelain")
    if str(locked) not in after_locked_prune or "locked incident evidence pending" not in after_locked_prune:
        raise AssertionError("prune discarded the locked stale worktree record")

    run_git(repository, "worktree", "unlock", str(locked))
    run_git(repository, "worktree", "prune", "--verbose")
    after_unlock_prune = git_output(repository, "worktree", "list", "--porcelain")
    if str(locked) in after_unlock_prune:
        raise AssertionError("unlocked stale worktree record remained after prune")
    return {
        "dirty_remove_returncode": str(removal.returncode),
        "dirty_worktree": str(dirty),
        "locked_worktree": str(locked),
        "record_retained_while_locked": "true",
        "record_removed_after_unlock": "true",
    }


def execute(root: Path) -> dict[str, object]:
    evidence = {
        "unshared_reset": check_unshared_range(root),
        "shared_revert": check_shared_reverts(root),
        "revert_abort": check_revert_abort(root),
        "worktree_protection": check_worktree_protection(root),
    }
    write(root / "evidence.json", json.dumps(evidence, indent=2, sort_keys=True) + "\n")
    return evidence


def cleanup(value: str) -> None:
    root = require_root(value)
    shutil.rmtree(root)
    print(f"removed lab root: {root}")


def main(arguments: list[str]) -> int:
    try:
        if arguments[1:] and arguments[1] == "--cleanup" and len(arguments) == 3:
            cleanup(arguments[2])
            return 0
        if arguments[1:] and arguments[1] == "--keep" and len(arguments) == 2:
            keep = True
        elif len(arguments) == 1:
            keep = False
        else:
            raise ValueError("usage: verify.py [--keep] | verify.py --cleanup <lab-root>")

        root = create_root()
        try:
            execute(root)
            print("ok: an unshared agent-only range moved locally after a recovery ref was retained")
            print("ok: verified shared agent commits were reverted while the human commit remained")
            print("ok: a conflicting revert aborted back to the pre-revert HEAD, content, and clean state")
            print("ok: ordinary worktree removal rejected dirty content and a lock retained stale metadata through prune")
            if keep:
                print(f"kept lab root: {root}")
            return 0
        finally:
            if not keep and root.exists():
                cleanup(str(root))
    except (AssertionError, OSError, RuntimeError, ValueError, json.JSONDecodeError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
