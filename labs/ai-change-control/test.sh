#!/usr/bin/env bash
set -euo pipefail

script_dir=$(cd "$(dirname "$0")" && pwd -P)

cleanup_run() {
  local lab_path=$1
  if [[ -d "$lab_path" ]]; then
    python3 "$script_dir/lab.py" --cleanup "$lab_path" >/dev/null
  fi
}

verify_kept_run() {
  local output=$1
  local lab_path
  lab_path=$(sed -n 's/^kept lab root: //p' <<<"$output")

  [[ -n "$lab_path" ]] || {
    echo "lab.py --keep did not print a retained root" >&2
    exit 1
  }

  trap 'cleanup_run "$lab_path"' RETURN

  python3 - "$lab_path" <<'PY'
import hashlib
import json
import sys
from pathlib import Path

root = Path(sys.argv[1])
marker = root / ".ai-change-control-lab-marker"
if marker.read_text(encoding="utf-8") != "ai-change-control-lab-v1\n":
    raise SystemExit("retained root has no expected marker")

evidence = json.loads(
    (root / "evidence" / "exercise-evidence.json").read_text(encoding="utf-8")
)
candidate = evidence["candidate"]
rollback = evidence["rollback"]

if candidate["clean_test_exit_code"] != 0:
    raise SystemExit("candidate clean-worktree test did not pass")
if evidence["bad_candidate"]["clean_test_exit_code"] != 1:
    raise SystemExit("bad candidate did not have the expected failing exit code")
if (
    evidence["bad_candidate"]["clean_test_required_message"]
    not in evidence["bad_candidate"]["clean_test_stderr"]
):
    raise SystemExit("bad candidate did not fail with the required message")
if candidate["http_response"]["timeout"] != 30:
    raise SystemExit("candidate artifact did not use the default timeout")
if rollback["http_response"]["timeout"] != 15:
    raise SystemExit("rollback artifact did not accept the explicit timeout")
if evidence["external_state"]["event_count_after_rollback"] != 2:
    raise SystemExit("rollback unexpectedly changed external event count")
if not isinstance(candidate["http_port"], int) or candidate["http_port"] <= 0:
    raise SystemExit("candidate did not use a system-assigned port")

artifact = Path(candidate["artifact"]["artifact_path"])
manifest = json.loads(
    Path(candidate["artifact"]["manifest_path"]).read_text(encoding="utf-8")
)
digest = hashlib.sha256(artifact.read_bytes()).hexdigest()
if digest != manifest["artifact_sha256"]:
    raise SystemExit("candidate artifact hash does not match manifest")
if manifest["candidate_commit"] != candidate["commit_sha"]:
    raise SystemExit("candidate manifest does not match candidate commit")
if "artifact checksum mismatch" not in evidence["tampered_artifact"]["rejection"]:
    raise SystemExit("tampered artifact was not rejected for checksum mismatch")
if evidence["tampered_artifact"]["external_event_count_before_start"] != 0:
    raise SystemExit("tampered artifact created external state before startup")
PY

  cleanup_run "$lab_path"
  trap - RETURN
  [[ ! -e "$lab_path" ]] || {
    echo "marked lab root still exists after cleanup: $lab_path" >&2
    exit 1
  }
}

for attempt in 1 2; do
  output=$(python3 "$script_dir/lab.py" --keep)
  printf '%s\n' "$output"
  verify_kept_run "$output"
done

unmarked_root=$(python3 - <<'PY'
import tempfile

print(tempfile.mkdtemp(prefix="ai-change-control-unmarked-"))
PY
)

cleanup_unmarked_root() {
  if [[ -n "$unmarked_root" && -d "$unmarked_root" ]]; then
    rmdir "$unmarked_root"
  fi
}
trap cleanup_unmarked_root EXIT

if python3 "$script_dir/lab.py" --cleanup "$unmarked_root" >/dev/null 2>&1; then
  echo "cleanup accepted an unmarked temporary root" >&2
  exit 1
fi
[[ -d "$unmarked_root" ]] || {
  echo "unmarked temporary root was removed" >&2
  exit 1
}
rmdir "$unmarked_root"
unmarked_root=

printf 'ok: repeated retained runs passed and unmarked cleanup was rejected\n'
