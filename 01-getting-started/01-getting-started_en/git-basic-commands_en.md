# Git Basic Commands

English | [中文](../git-basic-commands.md)

## Create or clone

```bash
git init
git clone <url>
```

## Check status

```bash
git status
git log --oneline --decorate
```

## Stage and commit

```bash
git add <file>
git commit -m "docs: add git basics"
```

## Sync

```bash
git fetch
git pull --rebase
git push
```

## Branch

`<integration-branch>` is the team's actual integration branch name. Common values include `main`, `master`, and `develop`. Confirm it from repository rules before switching; do not treat `main` as a fixed default.

```bash
git switch -c feat/my-task
git branch --show-current
git switch <integration-branch>
git branch
```

## Undo

`git restore` overwrites the Working Tree for the named path. Before running it, confirm that the path belongs to you and that its current version may be discarded:

```bash
git status --porcelain
git diff -- <owned-path>
git restore --worktree -- <owned-path>
```

To unstage the named path while keeping its Working Tree edit:

```bash
git restore --staged -- <owned-path>
```

To make a reverse commit for an already committed change:

```bash
git revert <commit-sha>
```

`git restore --staged` adjusts only the Index and keeps the Working Tree edit; `git revert` creates a reverse commit for an already committed change.

## Recommended Practice Sequence

1. Use `git status` to understand the current state.
2. Use `git add` and `git commit` to complete one local commit.
3. Use `git switch -c` to create a task branch.
4. Use `git diff` to check changes before committing.
5. Use `git push` to push the branch and create a PR.
6. Use `git restore` to undo local changes.

## Don't Rush to Use High-Risk Commands

First check for staged, unstaged, or untracked content that must be retained, and only preview untracked files:

```bash
git status --porcelain
git diff
git diff --cached
git clean -nd
```

If `git status --porcelain` prints anything, stop and do not run `git reset --hard` or `git clean`. `git clean -nd` only lists candidate paths; it does not establish that they may be deleted.

After confirming ownership and authorization to dispose of local edits, verifying the reset target, and confirming remote permission, branch rules, and collaborator impact, the owner can decide whether to use `git reset --hard`, `git clean -fd`, or `git push --force`. They can respectively discard tracked edits, delete untracked paths, and rewrite remote history.

If you just want to undo ordinary workspace changes, prioritize learning [Undo Anything](../../06-troubleshooting/06-troubleshooting_en/undo-anything_en.md).

## Extended Reading

- [Git Official Documentation](https://git-scm.com/docs)
- [Git Cheat Sheet](https://git-scm.com/cheat-sheet.pdf)
- [Pro Git: Git Basics](https://git-scm.com/book/en/v2/Git-Basics-Getting-a-Git-Repository)
- [Recommended Reading Index](../../09-resources/09-resources_en/recommended-reading_en.md)
