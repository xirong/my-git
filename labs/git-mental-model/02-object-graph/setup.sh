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
  lab_dir=$(mktemp -d "${TMPDIR:-/tmp}/my-git-object-graph.XXXXXX")
fi

lab_dir=$(cd "$lab_dir" && pwd -P)

git -c init.defaultBranch=main init -q "$lab_dir"
git -C "$lab_dir" config user.name "My Git Lab"
git -C "$lab_dir" config user.email "lab@example.com"
printf 'object-graph\n' > "$lab_dir/.git/my-git-lab"

mkdir "$lab_dir/docs"
printf 'hello object graph\n' > "$lab_dir/app.txt"
printf 'trees name objects\n' > "$lab_dir/docs/note.txt"
git -C "$lab_dir" add app.txt docs/note.txt
GIT_AUTHOR_DATE='2026-01-01T00:00:00Z' \
GIT_COMMITTER_DATE='2026-01-01T00:00:00Z' \
  git -C "$lab_dir" commit -q -m "build object graph"

printf '%s\n' "$lab_dir"
