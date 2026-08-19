#!/usr/bin/env bash
set -euo pipefail

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
  lab_dir=$(mktemp -d "${TMPDIR:-/tmp}/my-git-index-draft.XXXXXX")
fi

lab_dir=$(cd "$lab_dir" && pwd -P)

git -c init.defaultBranch=main init -q "$lab_dir"
git -C "$lab_dir" config user.name "My Git Lab"
git -C "$lab_dir" config user.email "lab@example.com"
printf 'index-draft\n' > "$lab_dir/.git/my-git-lab"

printf '%s\n' \
  'title=Index Lab' \
  'owner=team' \
  'status=draft' \
  'scope=docs' \
  'review=required' \
  'tests=enabled' \
  'release=manual' \
  'notes=clean' \
  'agent=idle' \
  'limit=one' \
  'backup=on' \
  'format=text' \
  'sync=off' \
  'deploy=off' \
  'footer=end' > "$lab_dir/app.txt"
printf 'mode=safe\n' > "$lab_dir/settings.ini"
printf 'owner=base\n' > "$lab_dir/conflict.txt"

git -C "$lab_dir" add app.txt settings.ini conflict.txt
GIT_AUTHOR_DATE='2026-01-01T00:00:00Z' \
GIT_COMMITTER_DATE='2026-01-01T00:00:00Z' \
  git -C "$lab_dir" commit -q -m "baseline"

git -C "$lab_dir" switch -q -c agent-change
printf 'owner=agent\n' > "$lab_dir/conflict.txt"
git -C "$lab_dir" add conflict.txt
GIT_AUTHOR_DATE='2026-01-01T00:01:00Z' \
GIT_COMMITTER_DATE='2026-01-01T00:01:00Z' \
  git -C "$lab_dir" commit -q -m "agent edits owner"

git -C "$lab_dir" switch -q main
printf 'owner=human\n' > "$lab_dir/conflict.txt"
git -C "$lab_dir" add conflict.txt
GIT_AUTHOR_DATE='2026-01-01T00:02:00Z' \
GIT_COMMITTER_DATE='2026-01-01T00:02:00Z' \
  git -C "$lab_dir" commit -q -m "human edits owner"

if git -C "$lab_dir" merge agent-change >/dev/null 2>&1; then
  echo "expected conflict.txt to conflict" >&2
  exit 1
fi
git -C "$lab_dir" rev-parse -q --verify MERGE_HEAD >/dev/null

printf '%s\n' \
  'title=Index Lab' \
  'owner=agent' \
  'status=draft' \
  'scope=docs' \
  'review=required' \
  'tests=enabled' \
  'release=manual' \
  'notes=clean' \
  'agent=idle' \
  'limit=one' \
  'backup=on' \
  'format=text' \
  'sync=off' \
  'deploy=on' \
  'footer=end' > "$lab_dir/app.txt"

printf 'y\nn\n' | git -C "$lab_dir" add -p app.txt >/dev/null
printf 'mode=fast\n' > "$lab_dir/settings.ini"

printf '%s\n' "$lab_dir"
