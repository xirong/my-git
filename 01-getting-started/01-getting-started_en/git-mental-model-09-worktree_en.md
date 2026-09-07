# Git Mental Model 09: Worktrees Share Objects and Isolate Checkout State

English | [中文](../git-mental-model-09-worktree.md) | [Interactive demo](../../interactive/git-mental-model/worktree-and-isolation.html?lang=en) | [Runnable lab](../../labs/git-mental-model/09-worktree/README.md)

When one repository needs an urgent `main` fix while an agent makes a longer feature change, repeated switch, stash, and restore operations mix contexts. `git worktree` provides multiple working directories, each checking out its own branch while reusing one Git object store.

It solves parallel Git checkout state. It does not isolate processes, ports, databases, out-of-repository caches, or environment variables. Multiple worktrees reduce branch-switching file overwrite risk, yet external shared resources and final integration still need coordination.

## Scenario: mainline work and a feature run in parallel

Suppose the primary worktree is on `main` and a new directory is needed for `feature/parallel`:

```text
common Git directory
  objects/                 shared commit, tree, and blob object store
  refs/heads/main          shared ordinary branch ref
  refs/heads/feature/...   shared ordinary branch ref

primary worktree
  HEAD -> main
  Index: primary's next-commit draft
  Working Tree: primary's disk files

feature worktree
  HEAD -> feature/parallel
  Index: feature's next-commit draft
  Working Tree: feature's disk files
```

After feature commits, primary can read that commit object directly and merge its branch. Merging `main` does not automatically switch the feature worktree’s HEAD to `main`. Both locations see the same objects and ordinary branch refs while retaining their own HEAD, index, and checked-out files.

## Concepts: what is shared and what is separate

`git worktree add <path> <commit-ish>` creates a linked worktree. The official manual says that it shares everything with the current repository except per-worktree files, with `HEAD` and `index` as typical independent files.

The shared scope includes the object store and most ordinary refs. When one worktree creates or advances `feature/parallel`, another can resolve that branch name to the same commit. Each worktree’s HEAD points to its own checked-out branch and each index is separate, so they can stage different files at the same time.

Git gives some per-worktree pseudo-refs special treatment; `HEAD` is the familiar example. For routine parallel development, use these boundaries:

```text
same object store and ordinary branch refs: each worktree can see the other’s committed Git objects
different HEAD, index, and working tree: each can check out, edit, and stage independently
resources outside the repository: Git neither locks nor isolates them
```

## Create, inspect, and remove a worktree

From the `main` directory, create a new branch and directory:

```bash
git worktree add -b feature/agent-docs ../project-feature main
git worktree list --porcelain
```

Inspect both locations:

```bash
git status --short
git -C ../project-feature status --short
git rev-parse --git-common-dir
git -C ../project-feature rev-parse --git-common-dir
git rev-parse --git-path HEAD
git -C ../project-feature rev-parse --git-path HEAD
git rev-parse --git-path index
git -C ../project-feature rev-parse --git-path index
```

The expected result is that both `--git-common-dir` values lead to the same location while HEAD and index paths differ. If only the `main` directory runs `git add main-note.txt`, feature’s `git diff --cached --name-only` should not show that file, and the converse also holds.

After feature is ready, integrate from the primary worktree according to the team’s agreement:

```bash
git status --short
git merge --no-ff feature/agent-docs
git status --short
git -C ../project-feature status --short
```

To remove a worktree, first confirm that it contains no work you need to retain:

```bash
git -C ../project-feature status --short
git worktree remove ../project-feature
git worktree list
```

Use `git worktree remove` in ordinary cases; it checks unsafe removal conditions. If a directory was manually removed, use `git worktree prune` to clean stale administrative records. For a worktree on a removable drive or network share, use `git worktree lock` first so a temporarily unavailable path is not mistaken for stale.

## The same-branch checkout limit

If `primary` already checks out `main`, this command fails by default:

```bash
git worktree add ../another-main main
```

The limit avoids two directories using the same ordinary branch as HEAD, where a commit or reset in one location makes the other location’s understanding of the branch tip ambiguous. Different branches can run in parallel:

```bash
git worktree add -b feature/review ../project-review main
```

`--force` can bypass some worktree protections. Consider it only when the existing checkout, collaboration agreement, and recovery path are understood. Routine agent parallelism should assign a distinct branch per worktree, or use a detached HEAD for inspection only.

## External shared resources still require coordination

Worktrees manage Git checkout state only inside their directories. These resources can be shared or contested across worktrees:

- The same development-server port.
- Databases, message queues, and test accounts outside the repository.
- Caches, temporary directories, and log paths outside the repository.
- Local `.env` files, certificates, or generated directories referenced by multiple worktrees.

For example, if two agents start `localhost:3000`, the second process can fail because the port is occupied; Git’s worktree machinery does not report that cause. Allocate a port, temporary directory, and test-data namespace per task, then put the actual mapping in the handoff record.

## Run the temporary-repository lab

The lab creates its own `primary` and `feature` worktrees, and every commit stays below its temporary root:

```bash
cd labs/git-mental-model/09-worktree
lab_path=$(bash setup.sh)
bash verify.sh "$lab_path"
sed -n '1,240p' "$lab_path/observations.txt"
sed -n '1,120p' "$lab_path/same-branch-results.txt"
bash cleanup.sh "$lab_path"
```

`verify.sh` asserts real Git state:

- Primary and feature object directories resolve to one common Git directory while HEAD and index paths differ.
- Before commits, `main-note.txt` and `feature-note.txt` appear only in their own indexes.
- Git rejects a second `main` checkout and accepts a `feature/parallel` checkout.
- After primary merges feature, primary sees the feature file and feature’s HEAD remains at its own commit.
- `external-resource.txt` in the root can be written from both contexts, with no Git-provided isolation.

The lab disables global Git configuration, signing, and caller hooks. `cleanup.sh` deletes only a marked, structurally complete temporary root.

Run the complete self-test:

```bash
bash labs/git-mental-model/09-worktree/test.sh
```

## Prediction: how do branch identity and indexes change the result?

First stage one file in `primary/main` and one in `feature/parallel`:

| Operation | Primary index | Feature index | Expected result |
| --- | --- | --- | --- |
| Primary stages `main-note.txt` | has `main-note.txt` | does not | two independent drafts |
| Feature stages `feature-note.txt` | lacks `feature-note.txt` | has it | two independent drafts |
| Create another worktree for checked-out `main` | not applicable | not applicable | Git rejects it |
| Create a worktree for `feature/review` | existing content remains | existing content remains | Git allows it |

The changed condition is whether the target branch is already checked out by another worktree. If a task needs read-only inspection at the same commit, consider a detached HEAD. If it needs commits, give each agent a distinct branch and name the owner of final integration.

## Agent migration exercise: a handoff checklist for parallel tasks

Each agent should record at least:

```text
worktree path: <absolute path>
branch and HEAD: <branch or detached> -> <oid>
Index state: clean | staged paths listed separately
working-tree state: clean | changed paths listed separately
integration owner and target branch: <person/agent> -> <branch>
external allocation: ports, temp directory, test-data namespace
```

These fields let the next person distinguish “the commit is shared but the file remains in another worktree,” “a local draft is not committed,” and “an external resource conflict exists.” `git worktree list --porcelain` can provide a machine-readable snapshot of paths, branches, and lock state.

## Further reading

- [Official git-worktree documentation](https://git-scm.com/docs/git-worktree)
- [Official gitrepository-layout documentation](https://git-scm.com/docs/gitrepository-layout)
- [Official gitrevisions documentation](https://git-scm.com/docs/gitrevisions)
- [Lab instructions](../../labs/git-mental-model/09-worktree/README.md)
