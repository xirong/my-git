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
  lab_dir=$(mktemp -d /tmp/my-git-recovery.XXXXXX)
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
git_lab config gc.reflogExpire never
git_lab config gc.reflogExpireUnreachable never

printf 'reachability-recovery\n' > "$lab_dir/.git/my-git-lab"

printf 'state=baseline\n' > "$lab_dir/ledger.txt"
git_lab add ledger.txt
GIT_AUTHOR_DATE='2026-01-01T00:00:00Z' \
GIT_COMMITTER_DATE='2026-01-01T00:00:00Z' \
  git_lab commit -q -m "baseline"
baseline_oid=$(git_lab rev-parse HEAD)

printf 'state=valuable\n' > "$lab_dir/ledger.txt"
git_lab add ledger.txt
GIT_AUTHOR_DATE='2026-01-01T00:01:00Z' \
GIT_COMMITTER_DATE='2026-01-01T00:01:00Z' \
  git_lab commit -q -m "keep recoverable commit"
recoverable_oid=$(git_lab rev-parse HEAD)

git_lab reset --hard HEAD~1 >/dev/null
git_lab update-ref -d ORIG_HEAD

git_lab switch -q -c discard-after-expiry
printf 'state=expires\n' > "$lab_dir/expiring.txt"
git_lab add expiring.txt
GIT_AUTHOR_DATE='2026-01-01T00:02:00Z' \
GIT_COMMITTER_DATE='2026-01-01T00:02:00Z' \
  git_lab commit -q -m "discard after expiry"
expired_oid=$(git_lab rev-parse HEAD)
git_lab switch -q main
git_lab branch -D discard-after-expiry >/dev/null

printf '%s\n' \
  "baseline_oid=$baseline_oid" \
  "recoverable_oid=$recoverable_oid" \
  "expired_oid=$expired_oid" > "$lab_dir/.git/my-git-recovery-state"

printf '%s\n' "$lab_dir"
