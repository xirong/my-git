#!/usr/bin/env bash
set -euo pipefail

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd -P)
expected_file="$script_dir/expected.txt"

cleanup_run() {
  local lab_path=$1
  if [[ -d "$lab_path" ]]; then
    python3 "$script_dir/verify.py" --cleanup "$lab_path" >/dev/null
  fi
}

verify_kept_run() {
  local output=$1
  local lab_path
  lab_path=$(sed -n 's/^kept lab root: //p' <<<"$output")

  [[ -n "$lab_path" ]] || {
    echo "verify.py --keep did not print a retained root" >&2
    exit 1
  }
  trap 'cleanup_run "$lab_path"' RETURN

  while IFS= read -r expected; do
    [[ -z "$expected" ]] && continue
    grep -Fqx -- "$expected" <<<"$output" || {
      echo "missing expected observation: $expected" >&2
      exit 1
    }
  done < "$expected_file"

  python3 - "$lab_path" <<'PY'
import json
import sys
from pathlib import Path

root = Path(sys.argv[1])
marker = root / ".ai-agent-incidents-lab-marker"
if marker.read_text(encoding="utf-8") != "ai-agent-incidents-v1\n":
    raise SystemExit("retained lab root has no expected marker")
evidence = json.loads((root / "evidence.json").read_text(encoding="utf-8"))
if evidence["unshared_reset"]["final_head"] != evidence["unshared_reset"]["base"]:
    raise SystemExit("unshared reset did not finish at the recorded base")
if evidence["shared_revert"]["final_head"] != evidence["shared_revert"]["remote_head"]:
    raise SystemExit("local bare remote does not have the shared revert result")
if evidence["revert_abort"]["before_revert"] != evidence["revert_abort"]["final_head"]:
    raise SystemExit("revert abort did not return to the recorded pre-revert head")
if evidence["worktree_protection"]["record_retained_while_locked"] != "true":
    raise SystemExit("locked worktree record was not retained")
if evidence["worktree_protection"]["record_removed_after_unlock"] != "true":
    raise SystemExit("unlocked worktree record was not pruned")
PY

  cleanup_run "$lab_path"
  trap - RETURN
  [[ ! -e "$lab_path" ]] || {
    echo "marked lab root remains after cleanup: $lab_path" >&2
    exit 1
  }
}

for attempt in 1 2; do
  output=$(PYTHONDONTWRITEBYTECODE=1 python3 "$script_dir/verify.py" --keep)
  printf '%s\n' "$output"
  verify_kept_run "$output"
done

unmarked_root=$(mktemp -d "${TMPDIR:-/tmp}/my-git-ai-agent-incidents-unmarked.XXXXXX")
cleanup_unmarked_root() {
  if [[ -n "$unmarked_root" && -d "$unmarked_root" ]]; then
    rmdir "$unmarked_root"
  fi
}
trap cleanup_unmarked_root EXIT

if python3 "$script_dir/verify.py" --cleanup "$unmarked_root" >/dev/null 2>&1; then
  echo "cleanup accepted an unmarked temporary directory" >&2
  exit 1
fi
[[ -d "$unmarked_root" ]] || {
  echo "cleanup removed an unmarked temporary directory" >&2
  exit 1
}
rmdir "$unmarked_root"
unmarked_root=

printf 'ok: retained runs passed and unmarked cleanup was rejected\n'
