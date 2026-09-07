#!/usr/bin/env python3
"""Create and verify a disposable, local-only Git remote lab."""
from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


MARKER_NAME = ".my-git-remote-lab"
MARKER_VALUE = "git-mental-model-08-remote-v1\n"
PROJECT_ROOT = Path(__file__).resolve().parents[3]


def git_env(extra: dict[str, str] | None = None) -> dict[str, str]:
    """Keep the lab independent from caller Git config, hooks, and prompts."""
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
    if extra:
        env.update(extra)
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
        root = Path(tempfile.mkdtemp(prefix="my-git-remote-"))
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
        raise ValueError(f"not a remote lab directory: {root}")
    return root


def setup(requested: str | None) -> None:
    root = create_root(requested)
    disabled_hooks = root / "disabled-hooks"
    disabled_hooks.mkdir()
    origin = root / "origin.git"
    seed = root / "seed"
    reader = root / "reader"
    writer = root / "writer"
    git("init", "-q", "--bare", str(origin))
    git("init", "-q", "-b", "main", str(seed))
    configure(seed, disabled_hooks)

    (seed / "story.txt").write_text("version=1\n", encoding="utf-8")
    git("add", "story.txt", cwd=seed)
    base = commit(seed, "baseline A")
    origin_url = origin.as_uri()
    git("remote", "add", "origin", origin_url, cwd=seed)
    git("push", "-q", "-u", "origin", "main", cwd=seed)
    git("--git-dir", str(origin), "symbolic-ref", "HEAD", "refs/heads/main")

    hook = origin / "hooks" / "pre-receive"
    hook.write_text(
        "#!/usr/bin/env bash\n"
        "set -eu\n"
        "while read -r old new ref; do\n"
        "  if [ \"$ref\" = \"refs/heads/protected\" ]; then\n"
        "    echo \"policy: protected branch rejects direct pushes\" >&2\n"
        "    exit 1\n"
        "  fi\n"
        "done\n",
        encoding="utf-8",
    )
    hook.chmod(0o755)

    git("clone", "-q", origin_url, str(reader))
    git("clone", "-q", origin_url, str(writer))
    configure(reader, disabled_hooks)
    configure(writer, disabled_hooks)
    if text("rev-parse", "main", cwd=reader) != base:
        raise AssertionError("reader did not start at baseline A")
    if text("rev-parse", "origin/main", cwd=reader) != base:
        raise AssertionError("reader origin/main did not start at baseline A")

    (writer / "story.txt").write_text("version=2\n", encoding="utf-8")
    git("add", "story.txt", cwd=writer)
    fetched = commit(writer, "writer publishes B")
    git("push", "-q", "origin", "main", cwd=writer)

    git("fetch", "-q", "origin", cwd=reader)
    fetch_only = {
        "head": text("rev-parse", "HEAD", cwd=reader),
        "main": text("rev-parse", "main", cwd=reader),
        "origin_main": text("rev-parse", "origin/main", cwd=reader),
        "working_tree": (reader / "story.txt").read_text(encoding="utf-8"),
        "index": text("show", ":story.txt", cwd=reader) + "\n",
    }
    if fetch_only != {
        "head": base,
        "main": base,
        "origin_main": fetched,
        "working_tree": "version=1\n",
        "index": "version=1\n",
    }:
        raise AssertionError(f"fetch-only state mismatch: {fetch_only}")

    git("merge", "--ff-only", "origin/main", cwd=reader)
    integrated = {
        "head": text("rev-parse", "HEAD", cwd=reader),
        "main": text("rev-parse", "main", cwd=reader),
        "origin_main": text("rev-parse", "origin/main", cwd=reader),
        "working_tree": (reader / "story.txt").read_text(encoding="utf-8"),
        "index": text("show", ":story.txt", cwd=reader) + "\n",
    }
    if integrated != {
        "head": fetched,
        "main": fetched,
        "origin_main": fetched,
        "working_tree": "version=2\n",
        "index": "version=2\n",
    }:
        raise AssertionError(f"fast-forward integration mismatch: {integrated}")

    (reader / "story.txt").write_text("version=3\n", encoding="utf-8")
    git("add", "story.txt", cwd=reader)
    reader_tip = commit(reader, "reader prepares C")
    (writer / "story.txt").write_text("version=4\n", encoding="utf-8")
    git("add", "story.txt", cwd=writer)
    origin_tip = commit(writer, "writer publishes D")
    git("push", "-q", "origin", "main", cwd=writer)

    rejected_push = git("push", "origin", "main", cwd=reader, check=False)
    if rejected_push.returncode == 0:
        raise AssertionError("expected a non-fast-forward push rejection")
    if text("--git-dir", str(origin), "rev-parse", "refs/heads/main") != origin_tip:
        raise AssertionError("rejected push changed the local bare origin")
    if git("merge-base", "--is-ancestor", reader_tip, origin_tip, cwd=reader, check=False).returncode == 0:
        raise AssertionError("reader tip unexpectedly became an ancestor of origin")

    policy_push = git("push", "origin", "main:protected", cwd=reader, check=False)
    if policy_push.returncode == 0:
        raise AssertionError("expected the protected-branch hook to reject the push")
    if "policy: protected branch rejects direct pushes" not in policy_push.stderr:
        raise AssertionError(f"policy rejection message missing: {policy_push.stderr}")
    if git("--git-dir", str(origin), "show-ref", "--verify", "--quiet", "refs/heads/protected", check=False).returncode == 0:
        raise AssertionError("protected branch was created despite the policy rejection")

    state = {
        "base": base,
        "fetched": fetched,
        "reader_tip": reader_tip,
        "origin_tip": origin_tip,
        "non_fast_forward_returncode": rejected_push.returncode,
        "policy_returncode": policy_push.returncode,
    }
    (root / "state.json").write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    (root / "push-results.txt").write_text(
        "non-fast-forward push stderr:\n"
        f"{rejected_push.stderr}\n"
        "protected-branch policy stderr:\n"
        f"{policy_push.stderr}",
        encoding="utf-8",
    )
    (root / "observations.txt").write_text(
        "fetch-only observation\n"
        f"  reader HEAD/main: {base}\n"
        f"  reader origin/main: {fetched}\n"
        "  reader Index and Working Tree story.txt: version=1\n\n"
        "after explicit merge --ff-only origin/main\n"
        f"  reader HEAD/main/origin/main: {fetched}\n"
        "  reader Index and Working Tree story.txt: version=2\n\n"
        "after independent commits\n"
        f"  reader main: {reader_tip}\n"
        f"  bare origin main: {origin_tip}\n"
        "  direct push from reader: rejected because its tip cannot fast-forward origin\n"
        "  protected branch push: rejected by this lab's server-side policy hook\n",
        encoding="utf-8",
    )
    print(root)


def verify(requested: str) -> None:
    root = require_root(requested)
    state = json.loads((root / "state.json").read_text(encoding="utf-8"))
    origin = root / "origin.git"
    reader = root / "reader"
    writer = root / "writer"
    base, fetched = state["base"], state["fetched"]
    reader_tip, origin_tip = state["reader_tip"], state["origin_tip"]
    checks = [
        (text("rev-parse", "main", cwd=reader) == reader_tip, "reader main tip changed"),
        (text("rev-parse", "origin/main", cwd=reader) == fetched, "reader origin/main changed"),
        (text("rev-parse", "main", cwd=writer) == origin_tip, "writer main tip changed"),
        (text("--git-dir", str(origin), "rev-parse", "refs/heads/main") == origin_tip, "bare origin main mismatch"),
        ((reader / "story.txt").read_text(encoding="utf-8") == "version=3\n", "reader worktree mismatch"),
        (text("show", ":story.txt", cwd=reader) == "version=3", "reader index mismatch"),
        (git("merge-base", "--is-ancestor", base, fetched, cwd=reader, check=False).returncode == 0, "B lost A as ancestor"),
        (git("merge-base", "--is-ancestor", fetched, reader_tip, cwd=reader, check=False).returncode == 0, "C lost B as ancestor"),
        (git("merge-base", "--is-ancestor", fetched, origin_tip, cwd=writer, check=False).returncode == 0, "D lost B as ancestor"),
        (state["non_fast_forward_returncode"] != 0, "non-fast-forward push unexpectedly succeeded"),
        (state["policy_returncode"] != 0, "policy push unexpectedly succeeded"),
        ("policy: protected branch rejects direct pushes" in (root / "push-results.txt").read_text(encoding="utf-8"), "policy output missing"),
        (git("--git-dir", str(origin), "show-ref", "--verify", "--quiet", "refs/heads/protected", check=False).returncode != 0, "protected ref exists"),
    ]
    failures = [message for passed, message in checks if not passed]
    if failures:
        raise AssertionError("; ".join(failures))
    print("ok: fetch updated origin/main from A to B while reader main and files stayed at A")
    print("ok: explicit merge --ff-only moved reader HEAD, Index, and Working Tree to B")
    print("ok: two diverged local histories caused a real push rejection against the disposable bare origin")
    print("ok: the local bare origin policy hook rejected a protected-branch update")


def cleanup(requested: str) -> None:
    root = require_root(requested)
    if not (root / "origin.git" / "HEAD").is_file() or not (root / "reader" / ".git").exists():
        raise ValueError(f"remote lab structure is incomplete: {root}")
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
