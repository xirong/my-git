#!/usr/bin/env bash
set -euo pipefail

if (( $# != 1 )); then
  echo "usage: $0 <lab-repository>" >&2
  exit 2
fi

lab_dir=$1
if [[ ! -f "$lab_dir/.git/my-git-lab" ]] || [[ "$(<"$lab_dir/.git/my-git-lab")" != "refs-head" ]]; then
  echo "not a refs-head lab repository: $lab_dir" >&2
  exit 1
fi

git_lab() {
  env GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null git -C "$lab_dir" "$@"
}

state_file="$lab_dir/.git/my-git-refs-state"
base_oid=$(sed -n 's/^base_oid=//p' "$state_file")
agent_oid=$(sed -n 's/^agent_oid=//p' "$state_file")
main_oid=$(sed -n 's/^main_oid=//p' "$state_file")

[[ -n "$base_oid" && -n "$agent_oid" && -n "$main_oid" ]] || {
  echo "lab state is incomplete" >&2
  exit 1
}

[[ "$(git_lab symbolic-ref --short HEAD)" == "main" ]] || {
  echo "HEAD is not attached to main" >&2
  exit 1
}
[[ "$(<"$lab_dir/.git/HEAD")" == "ref: refs/heads/main" ]] || {
  echo "HEAD file is not a symbolic reference to main" >&2
  exit 1
}
[[ "$(git_lab rev-parse HEAD)" == "$main_oid" ]] || {
  echo "HEAD does not resolve to the recorded main commit" >&2
  exit 1
}
[[ "$(git_lab rev-parse refs/heads/main)" == "$main_oid" ]] || {
  echo "main reference does not resolve to the recorded main commit" >&2
  exit 1
}
[[ "$(git_lab rev-parse refs/heads/agent/draft)" == "$agent_oid" ]] || {
  echo "agent/draft reference does not resolve to the recorded agent commit" >&2
  exit 1
}
[[ "$base_oid" != "$main_oid" ]] || {
  echo "main did not move away from the baseline commit" >&2
  exit 1
}
git_lab cat-file -e "$base_oid^{commit}"
git_lab cat-file -e "$agent_oid^{commit}"
git_lab cat-file -e "$main_oid^{commit}"

[[ "$(git_lab cat-file -t v1-light)" == "commit" ]] || {
  echo "v1-light is not a lightweight tag directly naming a commit" >&2
  exit 1
}
[[ "$(git_lab rev-parse v1-light)" == "$base_oid" ]] || {
  echo "v1-light does not resolve to the baseline commit" >&2
  exit 1
}
[[ "$(git_lab cat-file -t v1-annotated)" == "tag" ]] || {
  echo "v1-annotated is not an annotated tag object" >&2
  exit 1
}
[[ "$(git_lab rev-parse 'v1-annotated^{}')" == "$base_oid" ]] || {
  echo "v1-annotated does not peel to the baseline commit" >&2
  exit 1
}
tag_body=$(git_lab cat-file -p v1-annotated)
grep -Fqx "object $base_oid" <<<"$tag_body" || {
  echo "annotated tag does not name the baseline object" >&2
  exit 1
}
grep -Fqx 'type commit' <<<"$tag_body" || {
  echo "annotated tag does not record a commit target" >&2
  exit 1
}

status_value=$(git_lab status --short)
[[ -z "$status_value" ]] || {
  echo "lab repository is not clean: $status_value" >&2
  exit 1
}

printf 'ok: HEAD -> refs/heads/main -> %.12s\n' "$main_oid"
printf 'ok: refs/heads/agent/draft -> %.12s\n' "$agent_oid"
printf 'ok: refs/tags/v1-light -> %.12s\n' "$base_oid"
printf 'ok: refs/tags/v1-annotated -> tag -> %.12s\n' "$base_oid"
