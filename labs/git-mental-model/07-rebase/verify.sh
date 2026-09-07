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
if [[ ! -f "$lab_dir/.git/my-git-lab" ]] || [[ "$(<"$lab_dir/.git/my-git-lab")" != "rebase" ]]; then
  echo "not a rebase lab repository: $lab_dir" >&2
  exit 1
fi

replay_old=$(git -C "$lab_dir" rev-parse replay-topic-original)
replay_new=$(git -C "$lab_dir" rev-parse replay-topic)
[[ "$replay_old" != "$replay_new" ]] || {
  echo "successful replay did not create a new commit object" >&2
  exit 1
}
[[ "$(git -C "$lab_dir" rev-parse "$replay_old^")" == "$(git -C "$lab_dir" rev-parse replay-base)" ]] || {
  echo "old replay commit has the wrong parent" >&2
  exit 1
}
[[ "$(git -C "$lab_dir" rev-parse "$replay_new^")" == "$(git -C "$lab_dir" rev-parse replay-upstream)" ]] || {
  echo "new replay commit has the wrong parent" >&2
  exit 1
}
git -C "$lab_dir" cat-file -e "$replay_old^{commit}"
[[ "$(git -C "$lab_dir" show "$replay_old:topic.txt")" == "topic feature" ]] || { echo "old topic content mismatch" >&2; exit 1; }
[[ "$(git -C "$lab_dir" show "$replay_new:topic.txt")" == "topic feature" ]] || { echo "new topic content mismatch" >&2; exit 1; }

[[ "$(git -C "$lab_dir" rev-parse no-replay)" == "$(git -C "$lab_dir" rev-parse no-replay-before)" ]] || {
  echo "no-replay unexpectedly changed the branch ref" >&2
  exit 1
}
[[ "$(git -C "$lab_dir" rev-parse no-replay)" == "$(git -C "$lab_dir" rev-parse replay-upstream)" ]] || {
  echo "no-replay does not point at its upstream" >&2
  exit 1
}

actual_status=$(git -C "$lab_dir" status --short)
[[ "$actual_status" == "UU app.txt" ]] || {
  printf 'unexpected status:\n%s\n' "$actual_status" >&2
  exit 1
}
[[ "$(git -C "$lab_dir" rev-parse topic)" == "$(git -C "$lab_dir" rev-parse topic-original)" ]] || {
  echo "topic ref moved before the rebase completed" >&2
  exit 1
}
rebase_head=$(git -C "$lab_dir" rev-parse --verify REBASE_HEAD)
[[ "$rebase_head" == "$(git -C "$lab_dir" rev-parse topic-original)" ]] || {
  echo "REBASE_HEAD does not name the commit being replayed" >&2
  exit 1
}

old_topic_note=$(git -C "$lab_dir" rev-parse topic-original~1)
new_topic_note=$(git -C "$lab_dir" rev-parse HEAD)
[[ "$old_topic_note" != "$new_topic_note" ]] || {
  echo "the first topic commit was not replayed" >&2
  exit 1
}
[[ "$(git -C "$lab_dir" rev-parse "$new_topic_note^")" == "$(git -C "$lab_dir" rev-parse upstream)" ]] || {
  echo "the replayed topic note does not sit on upstream" >&2
  exit 1
}
[[ "$(git -C "$lab_dir" show "$old_topic_note:topic-note.txt")" == "topic note" ]] || { echo "old topic note content mismatch" >&2; exit 1; }
[[ "$(git -C "$lab_dir" show "$new_topic_note:topic-note.txt")" == "topic note" ]] || { echo "new topic note content mismatch" >&2; exit 1; }

current_patch=$(git -C "$lab_dir" rebase --show-current-patch)
grep -Fq '+owner=topic' <<<"$current_patch" || {
  echo "current rebase patch does not contain the topic owner change" >&2
  exit 1
}
stage_entries=$(git -C "$lab_dir" ls-files --unmerged -- app.txt)
[[ "$(awk 'END { print NR }' <<<"$stage_entries")" == "3" ]] || {
  echo "conflict stages are missing" >&2
  exit 1
}
stage_numbers=$(awk '{ printf "%s%s", separator, $3; separator = " " } END { print "" }' <<<"$stage_entries")
[[ "$stage_numbers" == "1 2 3" ]] || {
  echo "conflict stages are not 1, 2, 3" >&2
  exit 1
}
[[ "$(git -C "$lab_dir" show ':1:app.txt')" == "owner=base" ]] || { echo "stage 1 mismatch" >&2; exit 1; }
[[ "$(git -C "$lab_dir" show ':2:app.txt')" == "owner=upstream" ]] || { echo "stage 2 mismatch" >&2; exit 1; }
[[ "$(git -C "$lab_dir" show ':3:app.txt')" == "owner=topic" ]] || { echo "stage 3 mismatch" >&2; exit 1; }

printf 'state: replay-topic-original=%.12s -> replay-topic=%.12s\n' "$replay_old" "$replay_new"
printf 'state: old replay parent=replay-base; new replay parent=replay-upstream\n'
printf 'state: no-replay stayed at replay-upstream and created no new commit\n'
printf 'state: first topic commit replayed to %.12s; REBASE_HEAD=%.12s\n' "$new_topic_note" "$rebase_head"
printf 'state: git status --short\n%s\n' "$actual_status"
printf 'state: git ls-files --unmerged -- app.txt\n%s\n' "$stage_entries"
printf 'ok: rebase conflict stage 1=base, stage 2=upstream, stage 3=topic\n'
