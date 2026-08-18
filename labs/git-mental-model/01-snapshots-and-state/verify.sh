#!/usr/bin/env bash
set -euo pipefail

if (( $# != 1 )); then
  echo "usage: $0 <lab-repository>" >&2
  exit 2
fi

lab_dir=$1
if [[ ! -f "$lab_dir/.git/my-git-lab" ]] || [[ "$(<"$lab_dir/.git/my-git-lab")" != "snapshots-and-state" ]]; then
  echo "not a snapshots-and-state lab repository: $lab_dir" >&2
  exit 1
fi

head_value=$(git -C "$lab_dir" show HEAD:app.txt)
index_value=$(git -C "$lab_dir" show :app.txt)
working_value=$(<"$lab_dir/app.txt")
status_value=$(git -C "$lab_dir" status --short --untracked-files=no -- app.txt)

[[ "$head_value" == "version=1" ]] || { echo "HEAD mismatch: $head_value" >&2; exit 1; }
[[ "$index_value" == "version=2" ]] || { echo "index mismatch: $index_value" >&2; exit 1; }
[[ "$working_value" == "version=3" ]] || { echo "working tree mismatch: $working_value" >&2; exit 1; }
[[ "$status_value" == "MM app.txt" ]] || { echo "status mismatch: $status_value" >&2; exit 1; }

printf 'ok: HEAD=version=1, Index=version=2, Working Tree=version=3, Status=MM app.txt\n'
