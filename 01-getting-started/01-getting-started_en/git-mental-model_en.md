# Git Mental Model

English | [中文](../git-mental-model.md)

This page is the entry point to the Git Mental Model series. The four-area model is useful for quick operational decisions. The deeper series explains why Git behaves this way through snapshots, objects, refs, and history transformations.

## Flagship series

1. [Snapshots and State: HEAD, Index, and Working Tree](git-mental-model-01-snapshots_en.md)
2. [The Object Graph: Blobs, Trees, and Commits](git-mental-model-02-object-graph_en.md)

The first chapter uses three versions of one file to show what `git add` and `git commit` actually record. It includes an [interactive demo](../../interactive/git-mental-model/snapshots-and-state.html) and a [runnable lab](../../labs/git-mental-model/01-snapshots-and-state/README.md).

The second chapter follows a commit into the object database, separates the responsibilities of blobs, trees, and commits, and includes an [object-graph interactive](../../interactive/git-mental-model/object-graph.html) and a [runnable lab](../../labs/git-mental-model/02-object-graph/README.md).

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

Most Git commands are about moving content between these areas.

Determine which area the file is in first before choosing a command, and errors will be significantly reduced.

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

- If the change is in the working tree, use `git restore` or `git stash`.
- If the change is already staged, use `git restore --staged` first.
- If the commit has been generated but not pushed, you can use `reset` or `commit --amend`.
- If the commit has been pushed, usually prioritize using `revert`.

Judging the area first and then choosing the command is the primary principle of Git troubleshooting.

## Extended Reading

- [Pro Git: Git Basics](https://git-scm.com/book/en/v2/Git-Basics-Getting-a-Git-Repository)
- [git status Official Documentation](https://git-scm.com/docs/git-status)
- [git restore Official Documentation](https://git-scm.com/docs/git-restore)
- [Recommended Reading Index](../../09-resources/09-resources_en/recommended-reading_en.md)
