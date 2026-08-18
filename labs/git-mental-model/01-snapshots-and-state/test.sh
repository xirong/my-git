#!/usr/bin/env bash
set -euo pipefail

script_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)
lab_dir=$(bash "$script_dir/setup.sh")

cleanup() {
  if [[ -d "$lab_dir" ]]; then
    bash "$script_dir/cleanup.sh" "$lab_dir" >/dev/null
  fi
}
trap cleanup EXIT

bash "$script_dir/verify.sh" "$lab_dir"
