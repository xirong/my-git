#!/usr/bin/env bash
set -euo pipefail

if (( $# != 1 )); then
  echo "usage: $0 <lab-repository>" >&2
  exit 2
fi

lab_dir=$1
if [[ ! -f "$lab_dir/.git/my-git-lab" ]] || [[ "$(<"$lab_dir/.git/my-git-lab")" != "reachability-recovery" ]]; then
  echo "not a reachability-recovery lab repository: $lab_dir" >&2
  exit 1
fi

git_lab() {
  env GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null git -C "$lab_dir" "$@"
}

state_file="$lab_dir/.git/my-git-recovery-state"
baseline_oid=$(sed -n 's/^baseline_oid=//p' "$state_file")
recoverable_oid=$(sed -n 's/^recoverable_oid=//p' "$state_file")
expired_oid=$(sed -n 's/^expired_oid=//p' "$state_file")

[[ -n "$baseline_oid" && -n "$recoverable_oid" && -n "$expired_oid" ]] || {
  echo "lab state is incomplete" >&2
  exit 1
}
[[ "$(git_lab symbolic-ref --short HEAD)" == "main" ]] || {
  echo "HEAD is not attached to main" >&2
  exit 1
}
[[ "$(git_lab rev-parse HEAD)" == "$baseline_oid" ]] || {
  echo "main did not reset to the baseline commit" >&2
  exit 1
}
if git_lab rev-parse -q --verify ORIG_HEAD >/dev/null; then
  echo "ORIG_HEAD still provides a direct reference in this lab" >&2
  exit 1
fi

head_reflog=$(git_lab reflog show --format='%H' HEAD)
for oid in "$recoverable_oid" "$expired_oid"; do
  git_lab cat-file -e "$oid^{commit}"
  if [[ -n "$(git_lab for-each-ref --format='%(refname)' --contains "$oid")" ]]; then
    echo "unexpected reference still reaches $oid" >&2
    exit 1
  fi
  if ! grep -Fqx "$oid" <<<"$head_reflog"; then
    echo "HEAD reflog does not retain $oid" >&2
    exit 1
  fi
done

unreachable_before=$(git_lab fsck --no-reflogs --unreachable --no-progress)
grep -Fq "unreachable commit $recoverable_oid" <<<"$unreachable_before" || {
  echo "recoverable commit is not reported unreachable without reflogs" >&2
  exit 1
}
grep -Fq "unreachable commit $expired_oid" <<<"$unreachable_before" || {
  echo "expired commit is not reported unreachable without reflogs" >&2
  exit 1
}

git_lab branch recovered "$recoverable_oid"
[[ "$(git_lab rev-parse refs/heads/recovered)" == "$recoverable_oid" ]] || {
  echo "recovered branch does not point to the recoverable commit" >&2
  exit 1
}
git_lab cat-file -e "$recoverable_oid^{commit}"

git_lab reflog expire --expire=now --expire-unreachable=now --all
git_lab gc --prune=now --quiet

git_lab cat-file -e "$recoverable_oid^{commit}"
if git_lab cat-file -e "$expired_oid^{commit}" 2>/dev/null; then
  echo "expired commit still exists after reflog expiration and immediate prune" >&2
  exit 1
fi

status_value=$(git_lab status --short)
[[ -z "$status_value" ]] || {
  echo "lab repository is not clean: $status_value" >&2
  exit 1
}

printf 'ok: reset moved main to %.12s while reflog retained %.12s\n' "$baseline_oid" "$recoverable_oid"
printf 'ok: recovered branch now names %.12s\n' "$recoverable_oid"
printf 'ok: after explicit reflog expiry and gc --prune=now, %.12s no longer resolves\n' "$expired_oid"
