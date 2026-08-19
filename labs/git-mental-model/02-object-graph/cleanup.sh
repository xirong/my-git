#!/usr/bin/env bash
set -euo pipefail

if (( $# != 1 )); then
  echo "usage: $0 <lab-repository>" >&2
  exit 2
fi

requested=$1
if [[ ! -d "$requested" ]]; then
  echo "lab repository does not exist: $requested" >&2
  exit 1
fi

lab_dir=$(cd "$requested" && pwd -P)
script_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)
project_root=$(cd "$script_dir/../../.." && pwd -P)

if [[ "$lab_dir" == "/" || "$lab_dir" == "$HOME" || "$lab_dir" == "$project_root" ]]; then
  echo "refusing to remove protected directory: $lab_dir" >&2
  exit 1
fi

if [[ ! -f "$lab_dir/.git/my-git-lab" ]] || [[ "$(<"$lab_dir/.git/my-git-lab")" != "object-graph" ]]; then
  echo "refusing to remove an unmarked directory: $lab_dir" >&2
  exit 1
fi

rm -rf -- "$lab_dir"
printf 'removed lab repository: %s\n' "$lab_dir"
