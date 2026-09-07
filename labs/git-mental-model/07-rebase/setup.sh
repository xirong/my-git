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
  lab_dir=$(mktemp -d "${TMPDIR:-/tmp}/my-git-rebase.XXXXXX")
fi

lab_dir=$(cd "$lab_dir" && pwd -P)

git -c init.defaultBranch=main init -q "$lab_dir"
mkdir -p "$lab_dir/.git/my-git-hooks"
git -C "$lab_dir" config user.name "My Git Lab"
git -C "$lab_dir" config user.email "lab@example.com"
git -C "$lab_dir" config commit.gpgSign false
git -C "$lab_dir" config tag.gpgSign false
git -C "$lab_dir" config core.hooksPath "$lab_dir/.git/my-git-hooks"
printf 'rebase\n' > "$lab_dir/.git/my-git-lab"

commit_at() {
  local timestamp=$1
  local message=$2
  GIT_AUTHOR_DATE="$timestamp" GIT_COMMITTER_DATE="$timestamp" \
    git -C "$lab_dir" commit -q -m "$message"
}

printf 'owner=base\n' > "$lab_dir/app.txt"
printf 'baseline note\n' > "$lab_dir/notes.txt"
git -C "$lab_dir" add app.txt notes.txt
commit_at '2026-01-01T00:00:00Z' 'baseline'
git -C "$lab_dir" branch replay-base HEAD
git -C "$lab_dir" branch conflict-base HEAD

# A successful replay gets a new parent and therefore a new commit object.
git -C "$lab_dir" switch -q -c replay-upstream replay-base
printf 'upstream context\n' > "$lab_dir/upstream.txt"
git -C "$lab_dir" add upstream.txt
commit_at '2026-01-01T00:01:00Z' 'upstream context'

git -C "$lab_dir" switch -q -c replay-topic replay-base
printf 'topic feature\n' > "$lab_dir/topic.txt"
git -C "$lab_dir" add topic.txt
commit_at '2026-01-01T00:02:00Z' 'topic feature'
git -C "$lab_dir" branch replay-topic-original replay-topic
git -C "$lab_dir" rebase replay-upstream >/dev/null 2>&1

# No commits are eligible here, so this invocation creates no replay commit.
git -C "$lab_dir" switch -q -c no-replay replay-upstream
git -C "$lab_dir" branch no-replay-before no-replay
git -C "$lab_dir" rebase replay-upstream >/dev/null 2>&1

# Rebase a two-commit topic. The first commit replays; the second conflicts.
git -C "$lab_dir" switch -q -c upstream conflict-base
printf 'owner=upstream\n' > "$lab_dir/app.txt"
git -C "$lab_dir" add app.txt
commit_at '2026-01-01T00:03:00Z' 'upstream edits owner'

git -C "$lab_dir" switch -q -c topic conflict-base
printf 'topic note\n' > "$lab_dir/topic-note.txt"
git -C "$lab_dir" add topic-note.txt
commit_at '2026-01-01T00:04:00Z' 'topic note'
printf 'owner=topic\n' > "$lab_dir/app.txt"
git -C "$lab_dir" add app.txt
commit_at '2026-01-01T00:05:00Z' 'topic edits owner'
git -C "$lab_dir" branch topic-original topic

if git -C "$lab_dir" rebase upstream >"$lab_dir/.git/rebase-output" 2>&1; then
  echo "expected app.txt to produce a rebase conflict" >&2
  exit 1
fi
git -C "$lab_dir" rev-parse -q --verify REBASE_HEAD >/dev/null

printf '%s\n' "$lab_dir"
