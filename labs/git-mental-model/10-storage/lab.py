#!/usr/bin/env python3
"""Create and verify a disposable Git object-storage lab."""
from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


MARKER_NAME = ".my-git-storage-lab"
MARKER_VALUE = "git-mental-model-10-storage-v1\n"
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


def git(
    *args: str,
    cwd: Path | None = None,
    check: bool = True,
    input_text: str | None = None,
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        ["git", *args], cwd=cwd, env=git_env(), text=True,
        input=input_text, capture_output=True,
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


def count_objects(repo: Path) -> str:
    return text("count-objects", "-v", cwd=repo)


def delta_count(repo: Path) -> int:
    pack_dir = git_path(repo, "objects/pack")
    indexes = sorted(pack_dir.glob("*.idx"))
    if not indexes:
        raise AssertionError("repack created no pack index")
    count = 0
    for index in indexes:
        output = text("verify-pack", "-v", str(index), cwd=repo)
        for line in output.splitlines():
            fields = line.split()
            if len(fields) >= 7 and fields[1] in {"blob", "tree", "commit", "tag"}:
                count += 1
    return count


def create_root(requested: str | None) -> Path:
    if requested:
        root = Path(requested).expanduser()
        if root.exists() and not root.is_dir():
            raise ValueError(f"target exists and is not a directory: {root}")
        root.mkdir(parents=True, exist_ok=True)
        if any(root.iterdir()):
            raise ValueError(f"target directory must be empty: {root}")
    else:
        root = Path(tempfile.mkdtemp(prefix="my-git-storage-"))
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
        raise ValueError(f"not a storage lab directory: {root}")
    return root


def setup(requested: str | None) -> None:
    root = create_root(requested)
    repo = root / "repository"
    disabled_hooks = root / "disabled-hooks"
    disabled_hooks.mkdir()
    git("init", "-q", "-b", "main", str(repo))
    configure(repo, disabled_hooks)

    lines = [f"line-{number:04d}=stable-content-for-delta-compression\n" for number in range(1800)]
    ledger = repo / "ledger.txt"
    for revision in range(1, 15):
        lines[revision * 97] = f"line-{revision * 97:04d}=revision-{revision:02d}-changed-content\n"
        ledger.write_text("".join(lines), encoding="utf-8")
        git("add", "ledger.txt", cwd=repo)
        commit(repo, f"record logical snapshot {revision}")

    stable_commit = text("rev-parse", "HEAD", cwd=repo)
    before_show = text("show", "--format=fuller", "--no-ext-diff", stable_commit, cwd=repo)
    before_counts = count_objects(repo)
    (root / "show-before.txt").write_text(before_show + "\n", encoding="utf-8")
    (root / "count-before.txt").write_text(before_counts + "\n", encoding="utf-8")

    git("repack", "-adf", "--window=250", "--depth=50", cwd=repo)
    pack_dir = git_path(repo, "objects/pack")
    packs = sorted(pack_dir.glob("*.pack"))
    indexes = sorted(pack_dir.glob("*.idx"))
    if not packs or not indexes:
        raise AssertionError("git repack did not leave a pack and index")
    deltas = delta_count(repo)
    if deltas == 0:
        raise AssertionError("the deliberately similar revisions produced no packed delta objects")

    git("commit-graph", "write", "--reachable", cwd=repo)
    git("commit-graph", "verify", cwd=repo)
    commit_graph = git_path(repo, "objects/info/commit-graph")
    if not commit_graph.is_file():
        raise AssertionError("commit-graph write produced no commit-graph file")

    git("gc", "--no-prune", cwd=repo)
    after_show = text("show", "--format=fuller", "--no-ext-diff", stable_commit, cwd=repo)
    if after_show != before_show:
        raise AssertionError("repack, commit-graph, or gc changed git show for the same commit")
    after_counts = count_objects(repo)
    (root / "show-after.txt").write_text(after_show + "\n", encoding="utf-8")
    (root / "count-after.txt").write_text(after_counts + "\n", encoding="utf-8")

    orphan = git(
        "hash-object", "-w", "--stdin", cwd=repo,
        input_text="unreachable object created only for this disposable lab\n",
    ).stdout.strip()
    git("cat-file", "-e", f"{orphan}^{{blob}}", cwd=repo)
    git("prune", "--expire=now", cwd=repo)
    if git("cat-file", "-e", f"{orphan}^{{blob}}", cwd=repo, check=False).returncode == 0:
        raise AssertionError("prune did not remove the known unreachable loose blob")
    if text("show", "--format=fuller", "--no-ext-diff", stable_commit, cwd=repo) != before_show:
        raise AssertionError("pruning the disposable orphan changed the retained commit")

    state = {
        "stable_commit": stable_commit,
        "orphan": orphan,
        "delta_objects_after_repack": deltas,
        "commit_graph": str(commit_graph),
    }
    (root / "state.json").write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    (root / "observations.txt").write_text(
        f"stable commit: {stable_commit}\n"
        "git show before and after repack, commit-graph write, gc, and disposable prune: identical\n"
        f"pack files after repack: {len(packs)}\n"
        f"pack index files after repack: {len(indexes)}\n"
        f"delta objects reported by git verify-pack after repack: {deltas}\n"
        f"commit-graph file: {commit_graph}\n"
        f"known unreachable blob pruned with --expire=now: {orphan}\n"
        "count-objects output is recorded in count-before.txt and count-after.txt; it is an observation, not a performance benchmark.\n",
        encoding="utf-8",
    )
    print(root)


def verify(requested: str) -> None:
    root = require_root(requested)
    state = json.loads((root / "state.json").read_text(encoding="utf-8"))
    repo = root / "repository"
    stable = state["stable_commit"]
    current_show = text("show", "--format=fuller", "--no-ext-diff", stable, cwd=repo)
    before_show = (root / "show-before.txt").read_text(encoding="utf-8").rstrip("\n")
    after_show = (root / "show-after.txt").read_text(encoding="utf-8").rstrip("\n")
    pack_dir = git_path(repo, "objects/pack")
    packs = sorted(pack_dir.glob("*.pack"))
    indexes = sorted(pack_dir.glob("*.idx"))
    checks = [
        (current_show == before_show == after_show, "git show changed across physical maintenance"),
        (bool(packs) and bool(indexes), "no pack structure remains"),
        (delta_count(repo) > 0, "no delta object remains in current packs"),
        (Path(state["commit_graph"]).is_file(), "commit-graph file is absent"),
        (git("commit-graph", "verify", cwd=repo, check=False).returncode == 0, "commit-graph verify failed"),
        (git("cat-file", "-e", f"{state['orphan']}^{{blob}}", cwd=repo, check=False).returncode != 0, "known orphan remains after prune"),
        (text("status", "--short", cwd=repo) == "", "repository has unexpected working-tree changes"),
    ]
    failures = [message for passed, message in checks if not passed]
    if failures:
        raise AssertionError("; ".join(failures))
    print("ok: the same git show output survived repack, commit-graph creation, gc, and pruning a known orphan")
    print("ok: repack produced real pack/index structure and at least one delta object")
    print("ok: commit-graph exists and verifies as auxiliary graph-walk metadata")
    print("ok: prune --expire=now removed only the deliberately unreachable disposable blob")


def cleanup(requested: str) -> None:
    root = require_root(requested)
    if not (root / "repository" / ".git").is_dir() or not (root / "state.json").is_file():
        raise ValueError(f"storage lab structure is incomplete: {root}")
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
