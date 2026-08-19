#!/usr/bin/env bash
set -euo pipefail

if (( $# != 1 )); then
  echo "usage: $0 <lab-repository>" >&2
  exit 2
fi

lab_dir=$1
if [[ ! -f "$lab_dir/.git/my-git-lab" ]] || [[ "$(<"$lab_dir/.git/my-git-lab")" != "object-graph" ]]; then
  echo "not an object-graph lab repository: $lab_dir" >&2
  exit 1
fi

commit_oid=$(git -C "$lab_dir" rev-parse --verify 'HEAD^{commit}')
root_tree_oid=$(git -C "$lab_dir" rev-parse 'HEAD^{tree}')
docs_tree_oid=$(git -C "$lab_dir" rev-parse 'HEAD:docs')
app_blob_oid=$(git -C "$lab_dir" rev-parse 'HEAD:app.txt')
note_blob_oid=$(git -C "$lab_dir" rev-parse 'HEAD:docs/note.txt')

[[ "$(git -C "$lab_dir" cat-file -t "$commit_oid")" == "commit" ]] || { echo "HEAD is not a commit" >&2; exit 1; }
[[ "$(git -C "$lab_dir" cat-file -t "$root_tree_oid")" == "tree" ]] || { echo "root object is not a tree" >&2; exit 1; }
[[ "$(git -C "$lab_dir" cat-file -t "$docs_tree_oid")" == "tree" ]] || { echo "docs object is not a tree" >&2; exit 1; }
[[ "$(git -C "$lab_dir" cat-file -t "$app_blob_oid")" == "blob" ]] || { echo "app object is not a blob" >&2; exit 1; }
[[ "$(git -C "$lab_dir" cat-file -t "$note_blob_oid")" == "blob" ]] || { echo "note object is not a blob" >&2; exit 1; }

commit_tree_oid=$(git -C "$lab_dir" cat-file -p "$commit_oid" | sed -n 's/^tree //p' | head -n 1)
[[ "$commit_tree_oid" == "$root_tree_oid" ]] || { echo "commit points to the wrong root tree" >&2; exit 1; }

app_entry=$(git -C "$lab_dir" ls-tree "$root_tree_oid" -- app.txt)
docs_entry=$(git -C "$lab_dir" ls-tree "$root_tree_oid" -- docs)
note_entry=$(git -C "$lab_dir" ls-tree "$docs_tree_oid" -- note.txt)
[[ "$app_entry" == $'100644 blob '"$app_blob_oid"$'\tapp.txt' ]] || { echo "app.txt tree entry mismatch" >&2; exit 1; }
[[ "$docs_entry" == $'040000 tree '"$docs_tree_oid"$'\tdocs' ]] || { echo "docs tree entry mismatch" >&2; exit 1; }
[[ "$note_entry" == $'100644 blob '"$note_blob_oid"$'\tnote.txt' ]] || { echo "note.txt tree entry mismatch" >&2; exit 1; }

[[ "$(git -C "$lab_dir" cat-file -p "$app_blob_oid")" == "hello object graph" ]] || { echo "app blob content mismatch" >&2; exit 1; }
[[ "$(git -C "$lab_dir" cat-file -p "$note_blob_oid")" == "trees name objects" ]] || { echo "note blob content mismatch" >&2; exit 1; }

same_content_oid=$(printf 'hello object graph\n' | git -C "$lab_dir" hash-object --stdin)
[[ "$same_content_oid" == "$app_blob_oid" ]] || { echo "identical content produced another blob ID" >&2; exit 1; }

status_value=$(git -C "$lab_dir" status --short)
[[ -z "$status_value" ]] || { echo "lab repository is not clean: $status_value" >&2; exit 1; }

printf 'ok: commit %.12s -> tree %.12s\n' "$commit_oid" "$root_tree_oid"
printf 'ok: app.txt -> blob %.12s; docs/note.txt -> blob %.12s\n' "$app_blob_oid" "$note_blob_oid"
printf 'ok: same content -> same blob\n'
