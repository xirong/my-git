#!/usr/bin/env bash
set -euo pipefail

export GIT_CONFIG_NOSYSTEM=1
export GIT_CONFIG_GLOBAL=/dev/null
export GIT_TERMINAL_PROMPT=0

if (( $# != 1 )); then
  echo "usage: $0 <lab-repository>" >&2
  exit 2
fi

lab_dir=$1
if [[ ! -f "$lab_dir/.git/my-git-lab" ]] || [[ "$(<"$lab_dir/.git/my-git-lab")" != "merge" ]]; then
  echo "not a merge lab repository: $lab_dir" >&2
  exit 1
fi

actual_status=$(git -C "$lab_dir" status --short)
[[ "$actual_status" == "UU conflict.txt" ]] || {
  printf 'unexpected status:\n%s\n' "$actual_status" >&2
  exit 1
}
[[ "$(git -C "$lab_dir" branch --show-current)" == "main" ]] || {
  echo "main is not checked out during the conflict" >&2
  exit 1
}

conflict_base=$(git -C "$lab_dir" merge-base main conflict-topic)
[[ "$conflict_base" == "$(git -C "$lab_dir" rev-parse conflict-base)" ]] || {
  echo "unexpected common ancestor for the conflict" >&2
  exit 1
}
merge_head=$(git -C "$lab_dir" rev-parse --verify MERGE_HEAD)
[[ "$merge_head" == "$(git -C "$lab_dir" rev-parse conflict-topic)" ]] || {
  echo "MERGE_HEAD does not name conflict-topic" >&2
  exit 1
}

stage_entries=$(git -C "$lab_dir" ls-files --unmerged -- conflict.txt)
[[ "$(awk 'END { print NR }' <<<"$stage_entries")" == "3" ]] || {
  echo "conflict stages are missing" >&2
  exit 1
}
stage_numbers=$(awk '{ printf "%s%s", separator, $3; separator = " " } END { print "" }' <<<"$stage_entries")
[[ "$stage_numbers" == "1 2 3" ]] || {
  echo "conflict stages are not 1, 2, 3" >&2
  exit 1
}
[[ "$(git -C "$lab_dir" show ':1:conflict.txt')" == "owner=base" ]] || { echo "stage 1 mismatch" >&2; exit 1; }
[[ "$(git -C "$lab_dir" show ':2:conflict.txt')" == "owner=main" ]] || { echo "stage 2 mismatch" >&2; exit 1; }
[[ "$(git -C "$lab_dir" show ':3:conflict.txt')" == "owner=topic" ]] || { echo "stage 3 mismatch" >&2; exit 1; }

fast_forward_oid=$(git -C "$lab_dir" rev-parse fast-forward)
[[ "$(git -C "$lab_dir" rev-parse ff-target)" == "$fast_forward_oid" ]] || {
  echo "fast-forward did not move ff-target to fast-forward" >&2
  exit 1
}
[[ "$(git -C "$lab_dir" rev-list --parents -n 1 ff-target | awk '{ print NF - 1 }')" == "1" ]] || {
  echo "fast-forward unexpectedly created a merge commit" >&2
  exit 1
}
git -C "$lab_dir" merge-base --is-ancestor merge-base-point ff-target

[[ "$(git -C "$lab_dir" merge-base merge-main merge-topic)" == "$(git -C "$lab_dir" rev-parse merge-base-point)" ]] || {
  echo "unexpected common ancestor for the true merge" >&2
  exit 1
}
[[ "$(git -C "$lab_dir" rev-list --parents -n 1 merge-result | awk '{ print NF - 1 }')" == "2" ]] || {
  echo "merge-result does not have two parents" >&2
  exit 1
}
[[ "$(git -C "$lab_dir" merge-base semantic-server semantic-client)" == "$(git -C "$lab_dir" rev-parse semantic-base)" ]] || {
  echo "unexpected common ancestor for the semantic merge" >&2
  exit 1
}
[[ "$(git -C "$lab_dir" rev-list --parents -n 1 semantic-result | awk '{ print NF - 1 }')" == "2" ]] || {
  echo "semantic-result does not have two parents" >&2
  exit 1
}

behavior_dir=$(mktemp -d "${TMPDIR:-/tmp}/my-git-merge-behavior.XXXXXX")
cleanup_behavior_dir() {
  rm -rf -- "$behavior_dir"
}
trap cleanup_behavior_dir EXIT

for path in server.py client.py behavior_check.py; do
  git -C "$lab_dir" show "semantic-result:$path" > "$behavior_dir/$path"
done

set +e
(cd "$behavior_dir" && PYTHONDONTWRITEBYTECODE=1 python3 behavior_check.py) >"$behavior_dir/behavior-output" 2>&1
behavior_status=$?
set -e
if (( behavior_status == 0 )); then
  echo "expected the clean semantic merge to fail its behavior check" >&2
  exit 1
fi
grep -Fxq 'semantic check failed: expected https://service:8443, got http://service:8443' "$behavior_dir/behavior-output" || {
  cat "$behavior_dir/behavior-output" >&2
  exit 1
}

printf 'state: ff-target -> %.12s (one parent; fast-forward created no merge commit)\n' "$fast_forward_oid"
printf 'state: merge-result has two parents\n'
printf 'state: semantic-result has two parents and behavior_check.py exited %s\n' "$behavior_status"
printf 'state: conflict merge-base=%.12s MERGE_HEAD=%.12s\n' "$conflict_base" "$merge_head"
printf 'state: git status --short\n%s\n' "$actual_status"
printf 'state: git ls-files --unmerged -- conflict.txt\n%s\n' "$stage_entries"
printf 'ok: stage 1=base, stage 2=main, stage 3=topic\n'
printf 'ok: clean text merge did not establish behavioral compatibility\n'
