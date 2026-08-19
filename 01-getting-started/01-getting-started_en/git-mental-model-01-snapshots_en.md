# Git Mental Model 01: Snapshots and State

English | [中文](../git-mental-model-01-snapshots.md) | [Interactive demo](../../interactive/git-mental-model/snapshots-and-state.html) | [Runnable lab](../../labs/git-mental-model/01-snapshots-and-state/README.md)

When an AI agent says that a change is complete, you still need to ask one question: is the change only in the working tree, staged in the index, or already recorded in a commit?

These three locations can hold three versions of the same file at the same time. This model explains exactly what `git add`, `git commit`, `git diff`, and `git restore` affect.

## The model in one view

```text
HEAD snapshot         Index snapshot        Working Tree
current commit        next commit draft     files on disk
version=1             version=2             version=3
```

- `HEAD` points to the currently checked-out commit, which records a project snapshot.
- The index, also called the staging area, holds the snapshot proposed for the next commit.
- The working tree is the current state of files on disk.
- An untracked file belongs to neither the index nor a commit until it is added.

`git commit` takes its input from the index. Unstaged working-tree content does not enter that commit.

## Git records snapshots and presents differences

In the user-facing logical model, each commit records a snapshot of the project. `git diff` computes the difference between two states and shows what changed between them.

Git may use delta compression inside packfiles to save storage. That implementation detail does not change the snapshot model represented by a commit.

The three common comparisons are:

```text
HEAD -------- git diff --cached --------> Index
Index ----------- git diff -------------> Working Tree
HEAD ------------ git diff HEAD --------> Working Tree
```

| Command | Compared states | Main question |
| --- | --- | --- |
| `git diff` | Index and working tree | What has not been staged yet? |
| `git diff --cached` | HEAD and index | What will the next commit record? |
| `git diff HEAD` | HEAD and working tree | What is the total tracked change from the current commit? |

## Interactive demo

[Open the Snapshots and State interactive](../../interactive/git-mental-model/snapshots-and-state.html). Step through edit, stage, edit again, and commit to see how `app.txt` changes across all three locations.

To view it through a local static server, run this command from the repository root:

```bash
python3 -m http.server 8000
```

Then visit:

```text
http://localhost:8000/interactive/git-mental-model/snapshots-and-state.html
```

Press `Ctrl-C` in the server terminal when you are finished.

## Run the experiment in a temporary repository

This experiment creates a new temporary repository and does not modify the current project.

### Create the first snapshot

```bash
lab_dir=$(mktemp -d "${TMPDIR:-/tmp}/my-git-snapshots.XXXXXX")
git -c init.defaultBranch=main init -q "$lab_dir"
cd "$lab_dir"
git config user.name "My Git Lab"
git config user.email "lab@example.com"

printf 'version=1\n' > app.txt
git add app.txt
git commit -q -m "record version 1"
git status --short
```

Expected output: no output, because HEAD, the index, and the working tree match.

### Change only the working tree

```bash
printf 'version=2\n' > app.txt
git status --short
```

Expected output:

```text
 M app.txt
```

The first column represents the index and the second represents the working tree. The blank first column and `M` in the second mean that only the working tree has changed.

```text
HEAD=version=1    Index=version=1    Working Tree=version=2
```

### Put version=2 in the index

```bash
git add app.txt
git status --short
```

Expected output:

```text
M  app.txt
```

The `M` moves to the first column. The index differs from HEAD, while the working tree matches the index.

```text
HEAD=version=1    Index=version=2    Working Tree=version=2
```

### Edit again after staging

```bash
printf 'version=3\n' > app.txt
git status --short
```

Expected output:

```text
MM app.txt
```

The file now has three simultaneous versions. Read each location directly:

```bash
git show HEAD:app.txt
git show :app.txt
cat app.txt
```

The expected outputs, in order, are:

```text
version=1
version=2
version=3
```

The `:app.txt` syntax reads `app.txt` from the index.

### Commit the index snapshot

```bash
git commit -m "record version 2"
git status --short
```

The object ID in the commit output varies by environment. Its normalized form is:

```text
[main <object-id>] record version 2
 1 file changed, 1 insertion(+), 1 deletion(-)
```

The following `git status --short` still shows:

```text
 M app.txt
```

Final state:

```text
HEAD=version=2    Index=version=2    Working Tree=version=3
```

The commit recorded version=2 from the index. Version=3 remains as an uncommitted working-tree edit.

## A misleading inspection path

After staging, this command may produce no output:

```bash
git diff
```

That result only means that the working tree matches the index. It does not prove that the repository has no changes. Continue with:

```bash
git diff --cached
git status --short
```

When an agent or a person reports that there is no diff, the report should identify which comparison was run.

## Recovery case: deleting a tracked working-tree file

If tracked `app.txt` was deleted only from the working tree, inspect the state first:

```bash
git status --short
git diff -- app.txt
```

After confirming that the deletion can be discarded, restore the file from HEAD:

```bash
git restore --source=HEAD --worktree -- app.txt
git status --short
```

`git restore` overwrites the working-tree state for the selected path. Confirm that the current edit is disposable before running it.

Git cannot recover an untracked file that was never added, committed, or saved by another tool. Understanding that boundary matters more than memorizing a recovery command.

## Common misconceptions

### "A commit records every modified file on disk"

A commit records the index. Unstaged working-tree content remains on disk.

### "No output from `git diff` means there are no changes"

By default, `git diff` compares the index with the working tree. Use `git diff --cached` to inspect staged changes.

### "Git only stores each change as a delta"

Git presents commits as snapshots. A diff is a comparison result, while packfiles may use delta compression internally.

### "Any file inside a Git repository can be recovered"

Recovery requires content recorded in Git objects, the index, a stash, or another backup. Git has no recovery source for untracked content that was never saved.

## Why this matters for AI agents

After completing a task, an agent should distinguish these forms of evidence:

| Fact to confirm | Inspection |
| --- | --- |
| Unstaged working-tree changes | `git diff` |
| Snapshot proposed by the index | `git diff --cached` |
| All tracked changes from HEAD | `git diff HEAD` |
| Untracked, staged, or mixed states | `git status --short` |
| Content of the latest commit | `git show --stat --oneline HEAD` |

Practical rules:

- Do not report generated files as committed changes.
- Do not treat an empty `git diff` as a substitute for `git diff --cached` and `git status`.
- Inspect paths before staging and avoid an unnecessarily broad `git add -A`.
- Without commit authorization, verify and report state without creating a commit.
- Before recovery, determine whether the content ever entered the index, a commit, a stash, or another backup.

## Check your understanding

<details>
<summary>Why can <code>git status --short</code> show <code>MM app.txt</code>?</summary>

The index differs from HEAD, and the working tree also differs from the index.

</details>

<details>
<summary>Which version is committed from the <code>MM app.txt</code> state?</summary>

Git commits the index version. In this experiment, that is version=2.

</details>

<details>
<summary>Can reflog recover a deleted untracked file that was never staged?</summary>

No. Reflog records ref updates and has no recorded content for a file that never entered Git.

</details>

## Further reading

- [Next chapter: The Object Graph](git-mental-model-02-object-graph_en.md)
- [Pro Git: What is Git?](https://git-scm.com/book/en/v2/Getting-Started-What-is-Git%3F)
- [Git User Manual: history and snapshots](https://git-scm.com/docs/user-manual)
- [`git diff` documentation](https://git-scm.com/docs/git-diff)
- [`git status` documentation](https://git-scm.com/docs/git-status)
- [`git commit` documentation](https://git-scm.com/docs/git-commit)
- [`git restore` documentation](https://git-scm.com/docs/git-restore)
- [Git Mental Model overview](git-mental-model_en.md)
