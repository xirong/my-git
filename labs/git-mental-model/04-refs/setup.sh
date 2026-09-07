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
  lab_dir=$(mktemp -d /tmp/my-git-refs.XXXXXX)
fi

lab_dir=$(cd "$lab_dir" && pwd -P)

env GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null \
  git -c init.defaultBranch=main init -q "$lab_dir"

git_lab() {
  env GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null git -C "$lab_dir" "$@"
}

mkdir -p "$lab_dir/.git/lab-hooks"
git_lab config user.name "My Git Lab"
git_lab config user.email "lab@example.com"
git_lab config commit.gpgSign false
git_lab config tag.gpgSign false
git_lab config core.hooksPath "$lab_dir/.git/lab-hooks"
git_lab config gc.auto 0

printf 'refs-head\n' > "$lab_dir/.git/my-git-lab"

printf '%s\n' \
  'release=base' \
  'owner=team' > "$lab_dir/service.txt"
git_lab add service.txt
GIT_AUTHOR_DATE='2026-01-01T00:00:00Z' \
GIT_COMMITTER_DATE='2026-01-01T00:00:00Z' \
  git_lab commit -q -m "baseline"
base_oid=$(git_lab rev-parse HEAD)

GIT_COMMITTER_DATE='2026-01-01T00:00:10Z' \
  git_lab tag v1-light "$base_oid"
GIT_COMMITTER_DATE='2026-01-01T00:00:20Z' \
  git_lab tag -a v1-annotated -m "Annotated release at baseline" "$base_oid"

git_lab switch -q -c agent/draft "$base_oid"
printf 'proposal=retry\n' > "$lab_dir/agent.txt"
git_lab add agent.txt
GIT_AUTHOR_DATE='2026-01-01T00:01:00Z' \
GIT_COMMITTER_DATE='2026-01-01T00:01:00Z' \
  git_lab commit -q -m "agent draft"
agent_oid=$(git_lab rev-parse HEAD)

git_lab switch -q main
printf '%s\n' \
  'release=main-1' \
  'owner=team' > "$lab_dir/service.txt"
git_lab add service.txt
GIT_AUTHOR_DATE='2026-01-01T00:02:00Z' \
GIT_COMMITTER_DATE='2026-01-01T00:02:00Z' \
  git_lab commit -q -m "main release"
main_oid=$(git_lab rev-parse HEAD)

printf '%s\n' \
  "base_oid=$base_oid" \
  "agent_oid=$agent_oid" \
  "main_oid=$main_oid" > "$lab_dir/.git/my-git-refs-state"

printf '%s\n' "$lab_dir"
