# Git Mental Model 02: The Object Graph

English | [中文](../git-mental-model-02-object-graph.md) | [Interactive demo](../../interactive/git-mental-model/object-graph.html) | [Runnable lab](../../labs/git-mental-model/02-object-graph/README.md)

When an AI agent says, “I committed two files,” Git did not actually save a commit containing two file copies. It saved a set of objects connected by object IDs: file content goes into blobs, directory structure goes into trees, and the commit points to the project’s root tree.

Once you understand the object graph, you can answer three questions directly: which object stores the content, which object records the filename, and which project snapshot a commit references.

## The short version

```text
commit C
└── tree T0                         project root
    ├── blob B1  app.txt            file content
    └── tree T1  docs               subdirectory
        └── blob B2  note.txt       file content
```

- A blob stores file content, without a filename or directory path.
- A tree stores one directory level. Each entry includes a mode, name, and object ID; `git ls-tree` also resolves and displays the object type.
- A commit points to a root tree and records metadata such as parent commits, author, committer, and message.
- An object ID is calculated from the object’s type, length, and content. Blobs with identical content receive the same object ID.
- How branches and `HEAD` point to commits belongs to the later chapter on refs. This chapter looks inside the commit first.

The statement from Chapter 1 that “a commit records a project snapshot” is implemented as a tree-and-blob object graph with a commit as its entry point.

## What each object owns

| Object | Primary content | What it does not own |
| --- | --- | --- |
| blob | A sequence of file-content bytes | Filename, path, commit time |
| tree | Names, modes, and object IDs for one directory level | Commit message, parent relationship |
| commit | Root tree, parent commits, author, committer, message | File content directly |

If `app.txt` and `copy.txt` have identical content, two entries in the same tree can use different names while pointing to one blob. Names belong to tree entries; content belongs to blobs.

## Why an object ID changes

For a blob, the logical input Git hashes can be represented as:

```text
blob <content-byte-count>\0<file-content>
```

Changing one content byte changes that logical input and therefore its object ID. A tree records child object IDs, so changing a child produces a new tree. A commit records the root tree ID, so a new snapshot produces a new commit object.

Repositories can use different object formats, and their object ID lengths can differ. Scripts and tools should read complete IDs instead of treating an abbreviated example length as a fixed rule.

## Interactive demo

[Open the Object Graph interactive](../../interactive/git-mental-model/object-graph.html). Step through writing blobs, staging paths, generating trees, and creating a commit to see each object appear and connect.

Start a static server from the repository root:

```bash
python3 -m http.server 8000
```

Then visit:

```text
http://localhost:8000/interactive/git-mental-model/object-graph.html
```

When finished, press `Ctrl-C` in the terminal running the server.

## Run the experiment in a temporary repository

The following experiment creates a new temporary repository. It does not modify the current project.

### 1. Create a snapshot with a subdirectory

```bash
lab_dir=$(mktemp -d "${TMPDIR:-/tmp}/my-git-object-graph.XXXXXX")
git -c init.defaultBranch=main init -q "$lab_dir"
cd "$lab_dir"
git config user.name "My Git Lab"
git config user.email "lab@example.com"

mkdir docs
printf 'hello object graph\n' > app.txt
printf 'trees name objects\n' > docs/note.txt
git add app.txt docs/note.txt
git commit -q -m "build object graph"
```

The working tree, index, and `HEAD` now agree. The next steps leave the file-oriented view and inspect the objects directly.

### 2. Locate the commit, trees, and blobs

```bash
commit_oid=$(git rev-parse HEAD)
root_tree_oid=$(git rev-parse 'HEAD^{tree}')
docs_tree_oid=$(git rev-parse 'HEAD:docs')
app_blob_oid=$(git rev-parse 'HEAD:app.txt')
note_blob_oid=$(git rev-parse 'HEAD:docs/note.txt')

git cat-file -t "$commit_oid"
git cat-file -t "$root_tree_oid"
git cat-file -t "$docs_tree_oid"
git cat-file -t "$app_blob_oid"
git cat-file -t "$note_blob_oid"
```

Expected output:

```text
commit
tree
tree
blob
blob
```

`git rev-parse HEAD:path` resolves a path through the object graph rooted at `HEAD` and returns the object ID at the end of that path.

### 3. See which root tree the commit references

```bash
git cat-file -p "$commit_oid"
```

The output begins with fields equivalent to:

```text
tree <root-tree-id>
author My Git Lab <lab@example.com> <timestamp> +0000
committer My Git Lab <lab@example.com> <timestamp> +0000

build object graph
```

The first object ID matches `$root_tree_oid`. The initial commit has no `parent` line; later commits record one or more parent objects.

### 4. Expand both tree levels

```bash
git ls-tree "$root_tree_oid"
git ls-tree "$docs_tree_oid"
```

The normalized structure is:

```text
100644 blob <app-blob-id>    app.txt
040000 tree <docs-tree-id>   docs
100644 blob <note-blob-id>   note.txt
```

The root tree records the names `app.txt` and `docs`. The `docs` entry points to another tree, which records `note.txt`.

### 5. Read blob content

```bash
git cat-file -p "$app_blob_oid"
git cat-file -p "$note_blob_oid"
```

Expected output, in order:

```text
hello object graph
trees name objects
```

Neither `app.txt` nor `docs/note.txt` appears in that output. The path comes from the trees above each blob.

### 6. Prove that identical content reuses one blob ID

```bash
same_content_oid=$(printf 'hello object graph\n' | git hash-object --stdin)
printf '%s\n' "$app_blob_oid"
printf '%s\n' "$same_content_oid"
test "$app_blob_oid" = "$same_content_oid" && echo "same content -> same blob"
```

Expected final line:

```text
same content -> same blob
```

`git hash-object` calculates an object ID by default. Add `-w` to write the object into the object database.

## A path-to-content inspection route

When you inspect `docs/note.txt` in `HEAD`, Git can resolve it in this order:

```text
HEAD
  -> commit
  -> root tree
  -> tree entry "docs"
  -> nested tree
  -> tree entry "note.txt"
  -> blob
  -> file content
```

Useful inspection commands:

```bash
git cat-file -t HEAD
git cat-file -p HEAD
git ls-tree HEAD
git ls-tree HEAD:docs
git show HEAD:docs/note.txt
```

These commands only read objects. They do not move a branch, change the index, or overwrite the working tree.

## Recovery: file content was overwritten

Suppose committed `app.txt` is overwritten with incorrect content:

```bash
printf 'broken content\n' > app.txt
git status --short
git diff -- app.txt
```

First verify the object type and content saved by `HEAD`:

```bash
app_blob_oid=$(git rev-parse 'HEAD:app.txt')
git cat-file -t "$app_blob_oid"
git cat-file -p "$app_blob_oid"
```

You should see `blob` and the original content, `hello object graph`. After confirming that the incorrect working-tree content can be discarded, restore it:

```bash
git restore --source=HEAD --worktree -- app.txt
git status --short
```

The final command should produce no output. Recovery works because the commit can still reach the original blob through its trees. Content that never entered Git’s object database or another backup cannot be recovered through this graph.

## Common misconceptions

### “A blob is a file”

A blob is file content. Multiple filenames, trees, and commits can reuse one blob.

### “A commit contains every file”

A commit records the root tree’s object ID. File content lives in blobs reachable from that tree.

### “The filename participates in the blob ID”

The filename lives in a tree entry. Renaming a path without changing its content can preserve the blob ID while changing the tree ID.

### “An object ID is a random number”

An object ID comes from the object’s type, length, and content. The same logical object gets the same ID; changed content gets another ID.

### “`git hash-object` always stores an object”

It only calculates the ID by default. Use `-w`, or workflows such as `git add` and `git commit`, to write the relevant objects into the object database.

## Why this matters for AI agents

| Fact to verify | Inspection |
| --- | --- |
| Whether the claimed path entered the commit | `git ls-tree -r --name-only HEAD -- <path>` |
| Which snapshot the commit references | `git rev-parse 'HEAD^{tree}'` |
| Which object a path resolves to | `git rev-parse 'HEAD:<path>'`, then `git cat-file -t` |
| Whether committed content matches the claim | `git show HEAD:<path>` |
| Whether two paths reuse the same content object | Compare the results of two `git rev-parse 'HEAD:<path>'` calls |
| Whether modes such as the executable bit are correct | `git ls-tree HEAD -- <path>` |

Practical rules:

- When an agent reports that a file was committed, also verify that the path exists in the commit tree.
- Identical content does not imply identical paths or modes; review the tree entries too.
- Do not hard-code abbreviated object IDs in long-lived scripts. Read the complete ID for machine processing.
- Use `cat-file` and `ls-tree` for read-only evidence before choosing recovery or history-changing commands.
- Repeated content can reuse objects, but repository size also depends on packfiles, compression, and reachability. The performance chapter will cover those mechanics.

## Check yourself

<details>
<summary>Which object stores the filename <code>app.txt</code>?</summary>

A tree entry stores the filename. The blob stores only its content.

</details>

<details>
<summary>If <code>app.txt</code> is renamed to <code>main.txt</code> without a content change, which objects change?</summary>

The blob can stay the same. The tree containing the name changes, so a commit referencing the new root tree also changes.

</details>

<details>
<summary>Why does changing one deeply nested file change the root tree ID?</summary>

The file produces a new blob, and its tree must record that new ID. The change propagates through each parent tree until Git produces a new root tree.

</details>

## Further reading

- [Previous chapter: Snapshots and State](git-mental-model-01-snapshots_en.md)
- [Pro Git: Git Internals, Git Objects](https://git-scm.com/book/en/v2/Git-Internals-Git-Objects)
- [Official `git cat-file` documentation](https://git-scm.com/docs/git-cat-file)
- [Official `git hash-object` documentation](https://git-scm.com/docs/git-hash-object)
- [Official `git ls-tree` documentation](https://git-scm.com/docs/git-ls-tree)
- [Official `git rev-parse` documentation](https://git-scm.com/docs/git-rev-parse)
- [Git Mental Model overview](git-mental-model_en.md)
