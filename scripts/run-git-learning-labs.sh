#!/usr/bin/env bash
set -euo pipefail

script_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)
repo_root=$(cd "$script_dir/.." && pwd -P)
cd "$repo_root"

mental_model_labs=(
  01-snapshots-and-state
  02-object-graph
  03-index
  04-refs
  05-recovery
  06-merge
  07-rebase
  08-remote
  09-worktree
  10-storage
)

for lab in "${mental_model_labs[@]}"; do
  printf '==> Git mental model lab: %s\n' "$lab"
  bash "labs/git-mental-model/$lab/test.sh"
done

printf '==> Git mental model reading experiments\n'
python3 labs/git-mental-model/reading-experiments/verify.py

printf '==> Git mental model displayed command regression\n'
node scripts/test-curriculum-commands.mjs

printf '==> AI change control lab\n'
bash labs/ai-change-control/test.sh

printf '==> AI agent incident recovery lab\n'
bash labs/ai-agent-incidents/test.sh

printf '==> Git command safety lab\n'
bash labs/git-command-safety/test.sh

printf 'ok: all Git learning labs passed\n'
