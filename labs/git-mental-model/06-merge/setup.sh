#!/usr/bin/env bash
set -euo pipefail

# Keep the lab independent from the reader's global Git settings, signing, and hooks.
export GIT_CONFIG_NOSYSTEM=1
export GIT_CONFIG_GLOBAL=/dev/null
export GIT_EDITOR=true
export GIT_TERMINAL_PROMPT=0

if (( $# > 1 )); then
  echo "usage: $0 [target-directory]" >&2
  exit 2
fi

if (( $# == 1 )); then
  lab_dir=$1
  if [[ -e "$lab_dir" && ! -d "$lab_dir" ]]; then
    echo "target exists and is not a directory: $lab_dir" >&2
    exit 1
  fi
  mkdir -p "$lab_dir"
  if [[ -n "$(find "$lab_dir" -mindepth 1 -maxdepth 1 -print -quit)" ]]; then
    echo "target directory must be empty: $lab_dir" >&2
    exit 1
  fi
else
  lab_dir=$(mktemp -d "${TMPDIR:-/tmp}/my-git-merge.XXXXXX")
fi

lab_dir=$(cd "$lab_dir" && pwd -P)

git -c init.defaultBranch=main init -q "$lab_dir"
mkdir -p "$lab_dir/.git/my-git-hooks"
git -C "$lab_dir" config user.name "My Git Lab"
git -C "$lab_dir" config user.email "lab@example.com"
git -C "$lab_dir" config commit.gpgSign false
git -C "$lab_dir" config tag.gpgSign false
git -C "$lab_dir" config core.hooksPath "$lab_dir/.git/my-git-hooks"
printf 'merge\n' > "$lab_dir/.git/my-git-lab"

commit_at() {
  local timestamp=$1
  local message=$2
  GIT_AUTHOR_DATE="$timestamp" GIT_COMMITTER_DATE="$timestamp" \
    git -C "$lab_dir" commit -q -m "$message"
}

printf 'owner=base\n' > "$lab_dir/conflict.txt"
printf '%s\n' \
  'PROTOCOL = "http"' \
  'PORT = 8080' > "$lab_dir/server.py"
printf '%s\n' \
  'def endpoint():' \
  '    return "http://service:8080"' > "$lab_dir/client.py"
printf '%s\n' \
  'from client import endpoint' \
  'from server import PORT, PROTOCOL' \
  '' \
  'actual = endpoint()' \
  'expected = f"{PROTOCOL}://service:{PORT}"' \
  'if actual != expected:' \
  '    print(f"semantic check failed: expected {expected}, got {actual}")' \
  '    raise SystemExit(1)' \
  'print(f"semantic check passed: {actual}")' > "$lab_dir/behavior_check.py"

git -C "$lab_dir" add conflict.txt server.py client.py behavior_check.py
commit_at '2026-01-01T00:00:00Z' 'baseline'
git -C "$lab_dir" branch merge-base-point HEAD
git -C "$lab_dir" branch semantic-base HEAD
git -C "$lab_dir" branch conflict-base HEAD

# A fast-forward only moves ff-target to the existing fast-forward commit.
git -C "$lab_dir" switch -q -c fast-forward merge-base-point
printf 'fast-forward branch work\n' > "$lab_dir/fast-forward.txt"
git -C "$lab_dir" add fast-forward.txt
commit_at '2026-01-01T00:01:00Z' 'fast-forward work'
git -C "$lab_dir" switch -q -c ff-target merge-base-point
git -C "$lab_dir" merge --ff-only --no-edit fast-forward >/dev/null

# These two branches diverged, so their clean merge has two parents.
git -C "$lab_dir" switch -q -c merge-main merge-base-point
printf 'main side work\n' > "$lab_dir/main-only.txt"
git -C "$lab_dir" add main-only.txt
commit_at '2026-01-01T00:02:00Z' 'main side work'

git -C "$lab_dir" switch -q -c merge-topic merge-base-point
printf 'topic side work\n' > "$lab_dir/topic-only.txt"
git -C "$lab_dir" add topic-only.txt
commit_at '2026-01-01T00:03:00Z' 'topic side work'

git -C "$lab_dir" switch -q -c merge-result merge-main
git -C "$lab_dir" merge --no-edit merge-topic >/dev/null

# This merge changes different files, so it is textually clean. Its real behavior
# check still fails because the client and server no longer agree on the protocol.
git -C "$lab_dir" switch -q -c semantic-server semantic-base
printf '%s\n' \
  'PROTOCOL = "https"' \
  'PORT = 8443' > "$lab_dir/server.py"
git -C "$lab_dir" add server.py
commit_at '2026-01-01T00:04:00Z' 'server uses TLS port'

git -C "$lab_dir" switch -q -c semantic-client semantic-base
printf '%s\n' \
  'def endpoint():' \
  '    return "http://service:8443"' > "$lab_dir/client.py"
git -C "$lab_dir" add client.py
commit_at '2026-01-01T00:05:00Z' 'client keeps plaintext proxy route'

git -C "$lab_dir" switch -q -c semantic-result semantic-server
git -C "$lab_dir" merge --no-edit semantic-client >/dev/null

# Leave the main worktree in a real three-way content conflict for inspection.
git -C "$lab_dir" switch -q -c conflict-topic conflict-base
printf 'owner=topic\n' > "$lab_dir/conflict.txt"
git -C "$lab_dir" add conflict.txt
commit_at '2026-01-01T00:06:00Z' 'topic edits owner'

git -C "$lab_dir" switch -q main
printf 'owner=main\n' > "$lab_dir/conflict.txt"
git -C "$lab_dir" add conflict.txt
commit_at '2026-01-01T00:07:00Z' 'main edits owner'

if git -C "$lab_dir" merge --no-edit conflict-topic >"$lab_dir/.git/merge-conflict-output" 2>&1; then
  echo "expected conflict.txt to produce a merge conflict" >&2
  exit 1
fi
git -C "$lab_dir" rev-parse -q --verify MERGE_HEAD >/dev/null

printf '%s\n' "$lab_dir"
