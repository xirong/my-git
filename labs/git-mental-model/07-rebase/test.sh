#!/usr/bin/env bash
set -euo pipefail

export GIT_CONFIG_NOSYSTEM=1
export GIT_CONFIG_GLOBAL=/dev/null
export GIT_TERMINAL_PROMPT=0

script_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)
lab_dir=$(bash "$script_dir/setup.sh")

cleanup() {
  if [[ -d "$lab_dir" ]]; then
    bash "$script_dir/cleanup.sh" "$lab_dir" >/dev/null
  fi
}
trap cleanup EXIT

bash "$script_dir/verify.sh" "$lab_dir"

topic_before_abort=$(git -C "$lab_dir" rev-parse topic)
[[ "$topic_before_abort" == "$(git -C "$lab_dir" rev-parse topic-original)" ]] || {
  echo "topic ref changed before abort" >&2
  exit 1
}
git -C "$lab_dir" rebase --abort
[[ "$(git -C "$lab_dir" branch --show-current)" == "topic" ]] || {
  echo "rebase --abort did not return to topic" >&2
  exit 1
}
[[ "$(git -C "$lab_dir" rev-parse topic)" == "$topic_before_abort" ]] || {
  echo "rebase --abort did not restore the topic ref" >&2
  exit 1
}
[[ -z "$(git -C "$lab_dir" status --short)" ]] || {
  echo "rebase --abort did not restore a clean working tree" >&2
  exit 1
}
if git -C "$lab_dir" rev-parse -q --verify REBASE_HEAD >/dev/null; then
  echo "REBASE_HEAD remains after rebase --abort" >&2
  exit 1
fi
[[ "$(git -C "$lab_dir" show topic:app.txt)" == "owner=topic" ]] || {
  echo "topic content was not restored by rebase --abort" >&2
  exit 1
}

printf 'ok: rebase --abort restored topic=%.12s and a clean working tree\n' "$topic_before_abort"
