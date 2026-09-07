# Git Mental Model

English | [中文](../git-mental-model.md)

This page is the entry point to the Git Mental Model series. The four-area model is useful for quick operational decisions. The deeper series explains why Git behaves this way through snapshots, objects, refs, and history transformations.

Start with [why learn Git in the AI era](why-learn-git_en.md), then open the [interactive reading](https://xirong.github.io/my-git/interactive/git-mental-model/?lang=en). The [complete path](git-learning-path_en.md) keeps the articles, interactives, and temporary-repository labs for all ten topics in one sequence. The [knowledge map](knowledge-map_en.md) explains when this conceptual route should lead to a change or collaboration decision.

## Flagship series

1. [Snapshots and State: HEAD, Index, and Working Tree](git-mental-model-01-snapshots_en.md) · [Interactive](../../interactive/git-mental-model/snapshots-and-state.html?lang=en) · [Lab](../../labs/git-mental-model/01-snapshots-and-state/README.md)
2. [The Object Graph: Blobs, Trees, and Commits](git-mental-model-02-object-graph_en.md) · [Interactive](../../interactive/git-mental-model/object-graph.html?lang=en) · [Lab](../../labs/git-mental-model/02-object-graph/README.md)
3. [The Index Is the Next Commit Draft](git-mental-model-03-index_en.md) · [Interactive](../../interactive/git-mental-model/index-as-draft.html?lang=en) · [Lab](../../labs/git-mental-model/03-index/README.md)
4. [References, HEAD, and Identity](git-mental-model-04-refs_en.md) · [Interactive](../../interactive/git-mental-model/refs-and-head.html?lang=en) · [Lab](../../labs/git-mental-model/04-refs/README.md)
5. [Reachability, Reflog, and Recovery](git-mental-model-05-recovery_en.md) · [Interactive](../../interactive/git-mental-model/reachability-and-recovery.html?lang=en) · [Lab](../../labs/git-mental-model/05-recovery/README.md)
6. [Merge Starts with a Common Ancestor](git-mental-model-06-merge_en.md) · [Interactive](../../interactive/git-mental-model/three-way-merge.html?lang=en) · [Lab](../../labs/git-mental-model/06-merge/README.md)
7. [Rebase Replays Changes onto New History](git-mental-model-07-rebase_en.md) · [Interactive](../../interactive/git-mental-model/rebase-and-replay.html?lang=en) · [Lab](../../labs/git-mental-model/07-rebase/README.md)
8. [A Remote Is Another Repository; `origin/main` Is a Local Record](git-mental-model-08-remote_en.md) · [Interactive](../../interactive/git-mental-model/remote-and-fetch.html?lang=en) · [Lab](../../labs/git-mental-model/08-remote/README.md)
9. [Worktrees Share Objects and Isolate Checkout State](git-mental-model-09-worktree_en.md) · [Interactive](../../interactive/git-mental-model/worktree-and-isolation.html?lang=en) · [Lab](../../labs/git-mental-model/09-worktree/README.md)
10. [Logical Snapshots and Physical Storage Are Separate Layers](git-mental-model-10-storage_en.md) · [Interactive](../../interactive/git-mental-model/storage-and-maintenance.html?lang=en) · [Lab](../../labs/git-mental-model/10-storage/README.md)

The first chapter uses three versions of one file to show what `git add` and `git commit` actually record. It includes an [interactive demo](../../interactive/git-mental-model/snapshots-and-state.html) and a [runnable lab](../../labs/git-mental-model/01-snapshots-and-state/README.md).

The second chapter follows a commit into the object database, separates the responsibilities of blobs, trees, and commits, and includes an [object-graph interactive](../../interactive/git-mental-model/object-graph.html) and a [runnable lab](../../labs/git-mental-model/02-object-graph/README.md).

The third chapter goes deeper into the index through partial staging, `git diff --cached`, safe unstaging, and conflict stages 1, 2, and 3. It includes an [index-draft interactive](../../interactive/git-mental-model/index-as-draft.html) and a [runnable lab](../../labs/git-mental-model/03-index/README.md).

## Four-area quick model

To understand Git, first understand the four areas:

```text
working tree -> index -> local repository -> remote repository
```

## Working tree

The files you are currently editing.

Check:

```bash
git status
```

## Index

Also known as the staging area, it represents what the next commit will contain.

```bash
git add <file>
git diff --cached
```

## Local repository

The local commit history.

```bash
git log --oneline
```

## Remote repository

The remote repository, such as `origin` on GitHub.

```bash
git fetch
git pull --rebase
git push
```

## Key idea

This is an operational overview. It does not mean a file can belong to only one area or that every operation moves it away. The working tree, index, and HEAD can represent different versions simultaneously. A remote is another repository with its own objects and references.

Compare versions and references before deciding what an operation will change. A branch points to a commit; a commit refers to a snapshot. A branch is not another directory.

## Common Command Relationships

| Command | Primary Impact |
| --- | --- |
| `git add` | Working tree -> Index |
| `git commit` | Index -> Local repository |
| `git restore` | Discard or restore working tree content |
| `git restore --staged` | Restore the index from `HEAD` by default; keep the working tree unchanged |
| `git push` | Local repository -> Remote repository |
| `git fetch` | Remote repository -> Local remote reference |
| `git pull` | fetch + merge or fetch + rebase |

## Why This Model is Important

Many Git accidents stem from not clearly determining which area the current change is in.

For example:

- Preserve working edits before recovery; restoring working files may discard edits and is not a generic save operation.
- To unstage only, `git restore --staged` updates the index while preserving the working tree.
- Before rewriting commits, establish references, sharing, and recovery options. Different reset modes have different effects on working files.
- For shared history, usually append a revert commit. Database and external effects need separate treatment.

Judging the area first and then choosing the command is the primary principle of Git troubleshooting.

## Extended Reading

- [Pro Git: Git Basics](https://git-scm.com/book/en/v2/Git-Basics-Getting-a-Git-Repository)
- [git status Official Documentation](https://git-scm.com/docs/git-status)
- [git restore Official Documentation](https://git-scm.com/docs/git-restore)
- [Recommended Reading Index](../../09-resources/09-resources_en/recommended-reading_en.md)
