# Git Mental Model 03: The Index Is the Next Commit Draft

English | [中文](../git-mental-model-03-index.md) | [Interactive demo](../../interactive/git-mental-model/index-as-draft.html) | [Runnable lab](../../labs/git-mental-model/03-index/README.md)

When an AI agent changes ten files but says, "I will commit only two," the working tree is not enough evidence. The text explanation is not enough either. The index decides what the next commit will contain.

The index is also called the staging area. Calling it "the next commit draft" is useful, but one lower-level fact matters: it is usually stored in the binary `.git/index` file. A normal entry records a path, mode, blob object ID, stage number, and filesystem metadata used for performance. File content lives in blobs in the object database; the index references that content by object ID.

This chapter answers three questions:

1. What does `git add` actually change?
2. How can one file contain staged and unstaged changes at the same time?
3. Why does the index contain stages 1, 2, and 3 during a conflict?

## The short version

```text
HEAD                    Index                         Working Tree
previous commit         next commit draft             current disk files

app.txt v1  --add -p--> app.txt v2  --edit again-->   app.txt v3
```

- `git add <path>` writes the selected current content as a blob and updates the index entry.
- `git commit` writes trees from stage-0 index entries, then creates a commit.
- `git diff --cached` compares `HEAD` with the index. It is the closest answer to "what will the next commit change?"
- `git diff` compares the index with the working tree and shows changes still outside the draft.
- In `git status --short`, the first column describes the index relative to `HEAD`; the second describes the working tree relative to the index.
- A conflicted path temporarily has no normal stage-0 entry. The index keeps the merge base, ours, and theirs as candidates for resolution.

A change visible in the working tree may therefore be absent from the next commit. Content already deleted or rewritten in the working tree may also remain in the index as a different version.

## What an index entry records

Run:

```bash
git ls-files --stage
```

The normal output shape is:

```text
<mode> <object-id> <stage>\t<path>
```

For example:

```text
100644 42c4cc2... 0	app.txt
```

This means:

- `100644`: a regular non-executable file mode.
- `42c4cc2...`: the blob object ID referenced by the index.
- `0`: a normal entry uses stage 0.
- `app.txt`: the path relative to the repository root.

The index also contains a stat cache and other performance fields. For deciding what the next commit contains, the important fields are the path, mode, object ID, and stage.

## `git add` updates one path snapshot

Suppose `app.txt` in `HEAD` contains:

```text
owner=team
deploy=off
```

Change `owner` to `agent`, then run:

```bash
git add app.txt
```

Git writes or reuses a blob for the current content and points the index entry for `app.txt` to it. If you then change `deploy` to `on`, the index is not updated automatically.

Three content versions can now coexist:

```text
HEAD          owner=team   deploy=off
Index         owner=agent  deploy=off
Working Tree  owner=agent  deploy=on
```

Inspect the two different comparisons:

```bash
git diff --cached -- app.txt
git diff -- app.txt
```

The first command shows only the `owner` change. The second shows only the `deploy` change.

## Partial staging: split one file into two review scopes

`git add -p` presents each diff hunk and lets you choose which hunks enter the index:

```bash
git add -p app.txt
```

Common answers:

- `y`: stage this hunk.
- `n`: skip this hunk.
- `s`: try to split this hunk further.
- `e`: edit the patch manually, for users who can validate patch semantics precisely.
- `q`: quit without processing later hunks.

After partial staging, `git status --short` may show:

```text
MM app.txt
```

The first `M` means the index differs from `HEAD`. The second means the working tree still differs from the index. Git is not counting one edit twice; each comparison boundary found its own difference.

Before committing, inspect at least:

```bash
git diff --cached
git status --short
```

If one behavior spans several hunks, splitting them may create a commit that does not build or is behaviorally incomplete. Partial staging should improve commit clarity without breaking change atomicity.

## Conflict stages: three candidate versions in the index

Normal paths use stage 0. During a content conflict, one path can have up to three higher-stage entries:

```text
stage 1  merge base, the common ancestor
stage 2  ours, the current branch version
stage 3  theirs, the merged branch version
```

Inspect them with:

```bash
git ls-files --unmerged
git show :1:conflict.txt
git show :2:conflict.txt
git show :3:conflict.txt
```

Example output:

```text
100644 8227059... 1	conflict.txt
100644 c3efd06... 2	conflict.txt
100644 d17b9a9... 3	conflict.txt
```

Resolve the conflict in the working tree, then run:

```bash
git add conflict.txt
```

Git removes stages 1, 2, and 3 and creates a stage-0 entry for the resolution. Here, `git add` communicates two facts: accept the current file content and mark this path resolved.

The ours/theirs description above applies to a regular merge. A rebase changes the replay perspective, so confirm the active operation before using `--ours` or `--theirs`.

## Interactive demo

[Open the Index Is the Next Commit Draft interactive](../../interactive/git-mental-model/index-as-draft.html). The page drives every command, `git status --short` result, index entry, and commit preview from one state model.

Start a static server from the repository root:

```bash
python3 -m http.server 8000
```

Then visit:

```text
http://localhost:8000/interactive/git-mental-model/index-as-draft.html
```

When finished, press `Ctrl-C` in the terminal running the server.

## Run the experiment in a temporary repository

The lab creates an isolated temporary repository and does not modify this project:

```bash
cd labs/git-mental-model/03-index
lab_path=$(bash setup.sh)
bash verify.sh "$lab_path"
bash cleanup.sh "$lab_path"
```

Run the complete self-test with:

```bash
bash labs/git-mental-model/03-index/test.sh
```

The final repository preserves three states that can be inspected together:

```text
MM app.txt
UU conflict.txt
 M settings.ini
```

- The first hunk in `app.txt` is in the index; the second remains only in the working tree.
- `conflict.txt` has stages 1, 2, and 3 in the index.
- `settings.ini` is changed only in the working tree and is outside the next commit draft.

See [expected.txt](../../labs/git-mental-model/03-index/expected.txt) for the full expected state.

## Recovery: an agent staged an unrelated file

Suppose an agent ran `git add -A` and staged the local configuration in `settings.ini`.

Inspect the draft first:

```bash
git status --short
git diff --cached -- settings.ini
```

After confirming that the path should not be committed, restore only the index:

```bash
git restore --staged -- settings.ini
git status --short
```

By default, `git restore --staged` restores the index from `HEAD` while keeping the working-tree edit. It fits the "unstage but keep my local work" case.

Do not use this just to unstage a path:

```bash
git reset --hard
```

`reset --hard` also overwrites the working tree and can destroy uncommitted content. When only the draft needs adjustment, use `git restore --staged` with an explicit path.

## Common misconceptions

### "The index is only a list of filenames to commit"

An index entry also records a mode, object ID, and stage. It identifies the specific content version prepared for each path.

### "After `git add`, later edits automatically enter the commit"

Each `git add` updates only the selected content at that moment. Later edits remain in the working tree until staged again.

### "`git commit -a` equals `git add -A && git commit`"

`git commit -a` automatically stages changes and deletions to tracked files, but it does not include new untracked files. It also reduces the opportunity to inspect the index separately before committing.

### "Conflict markers exist only in the working-tree file"

The working tree displays conflict markers while the index stores candidate blobs in stages 1, 2, and 3. `git add` restores stage 0 after resolution.

### "Unstaging deletes my edit"

`git restore --staged -- <path>` changes only the index. The working tree stays unchanged unless `--worktree` is also specified.

## Why this matters for AI agents

An agent may edit many files and may run an overly broad `git add -A`. Inspect the real index when accepting an agent-authored commit:

```bash
git status --short
git diff --cached --stat
git diff --cached
git ls-files --unmerged
```

Recommended acceptance checks:

1. `git diff --cached` contains only paths and hunks required by the task.
2. `git ls-files --unmerged` produces no output.
3. Remaining working-tree edits have a known owner and are not mistaken for committed work.
4. A partially staged commit can still be built, tested, or explained independently.
5. The agent's claimed commit scope matches the actual index.

For an AI agent, the index is the smallest commit-permission boundary. Inspecting it is more reliable than asking the agent what it plans to commit.

## Further reading

- [Git index format](https://git-scm.com/docs/index-format)
- [git ls-files](https://git-scm.com/docs/git-ls-files)
- [git add](https://git-scm.com/docs/git-add)
- [git restore](https://git-scm.com/docs/git-restore)
- [Previous chapter: The Object Graph](git-mental-model-02-object-graph_en.md)
