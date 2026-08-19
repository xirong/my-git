#!/usr/bin/env bash
set -euo pipefail

if (( $# != 1 )); then
  echo "usage: $0 <lab-repository>" >&2
  exit 2
fi

lab_dir=$1
if [[ ! -f "$lab_dir/.git/my-git-lab" ]] || [[ "$(<"$lab_dir/.git/my-git-lab")" != "index-draft" ]]; then
  echo "not an index-draft lab repository: $lab_dir" >&2
  exit 1
fi

expected_status=$'MM app.txt\nUU conflict.txt\n M settings.ini'
actual_status=$(git -C "$lab_dir" status --short)
[[ "$actual_status" == "$expected_status" ]] || {
  printf 'unexpected status:\n%s\n' "$actual_status" >&2
  exit 1
}

app_stage=$(git -C "$lab_dir" ls-files --stage -- app.txt | awk '{print $3}')
settings_stage=$(git -C "$lab_dir" ls-files --stage -- settings.ini | awk '{print $3}')
[[ "$app_stage" == "0" ]] || { echo "app.txt is not at stage 0" >&2; exit 1; }
[[ "$settings_stage" == "0" ]] || { echo "settings.ini is not at stage 0" >&2; exit 1; }

app_index_oid=$(git -C "$lab_dir" ls-files --stage -- app.txt | awk '{print $2}')
settings_index_oid=$(git -C "$lab_dir" ls-files --stage -- settings.ini | awk '{print $2}')
app_index_content=$(git -C "$lab_dir" cat-file -p "$app_index_oid")
settings_index_content=$(git -C "$lab_dir" cat-file -p "$settings_index_oid")
app_head_content=$(git -C "$lab_dir" show HEAD:app.txt)

grep -qx 'owner=team' <<<"$app_head_content" || { echo "HEAD app owner mismatch" >&2; exit 1; }
grep -qx 'deploy=off' <<<"$app_head_content" || { echo "HEAD app deploy mismatch" >&2; exit 1; }
grep -qx 'owner=agent' <<<"$app_index_content" || { echo "index app owner mismatch" >&2; exit 1; }
grep -qx 'deploy=off' <<<"$app_index_content" || { echo "index app deploy mismatch" >&2; exit 1; }
grep -qx 'owner=agent' "$lab_dir/app.txt" || { echo "working-tree app owner mismatch" >&2; exit 1; }
grep -qx 'deploy=on' "$lab_dir/app.txt" || { echo "working-tree app deploy mismatch" >&2; exit 1; }
[[ "$settings_index_content" == "mode=safe" ]] || { echo "index settings mismatch" >&2; exit 1; }
[[ "$(<"$lab_dir/settings.ini")" == "mode=fast" ]] || { echo "working-tree settings mismatch" >&2; exit 1; }

cached_diff=$(git -C "$lab_dir" diff --cached -- app.txt)
working_diff=$(git -C "$lab_dir" diff -- app.txt)
grep -q '^-owner=team' <<<"$cached_diff" || { echo "selected owner hunk missing from cached diff" >&2; exit 1; }
grep -q '^+owner=agent' <<<"$cached_diff" || { echo "selected owner hunk missing from cached diff" >&2; exit 1; }
if grep -q 'deploy=' <<<"$cached_diff"; then
  echo "unstaged deploy hunk leaked into cached diff" >&2
  exit 1
fi
grep -q '^-deploy=off' <<<"$working_diff" || { echo "deploy hunk missing from working diff" >&2; exit 1; }
grep -q '^+deploy=on' <<<"$working_diff" || { echo "deploy hunk missing from working diff" >&2; exit 1; }
if grep -q 'owner=' <<<"$working_diff"; then
  echo "staged owner hunk leaked into working diff" >&2
  exit 1
fi

conflict_entries=$(git -C "$lab_dir" ls-files --stage -- conflict.txt)
[[ "$(wc -l <<<"$conflict_entries" | tr -d ' ')" == "3" ]] || { echo "conflict stages missing" >&2; exit 1; }
[[ "$(awk 'NR == 1 {print $3}' <<<"$conflict_entries")" == "1" ]] || { echo "stage 1 missing" >&2; exit 1; }
[[ "$(awk 'NR == 2 {print $3}' <<<"$conflict_entries")" == "2" ]] || { echo "stage 2 missing" >&2; exit 1; }
[[ "$(awk 'NR == 3 {print $3}' <<<"$conflict_entries")" == "3" ]] || { echo "stage 3 missing" >&2; exit 1; }

[[ "$(git -C "$lab_dir" show ':1:conflict.txt')" == "owner=base" ]] || { echo "stage 1 content mismatch" >&2; exit 1; }
[[ "$(git -C "$lab_dir" show ':2:conflict.txt')" == "owner=human" ]] || { echo "stage 2 content mismatch" >&2; exit 1; }
[[ "$(git -C "$lab_dir" show ':3:conflict.txt')" == "owner=agent" ]] || { echo "stage 3 content mismatch" >&2; exit 1; }

printf 'ok: app.txt HEAD owner=team -> Index owner=agent -> Working Tree deploy=on\n'
printf 'ok: git diff --cached contains only the selected owner hunk\n'
printf 'ok: conflict.txt stages 1=base, 2=human, 3=agent\n'
printf 'ok: settings.ini remains outside the next commit draft\n'
