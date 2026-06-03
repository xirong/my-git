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

```bash
git switch -c feat/my-task
git switch main
git branch
```

## Undo

```bash
git restore <file>
git restore --staged <file>
git revert <commit-sha>
```

## Recommended Practice Sequence

1. Use `git status` to understand the current state.
2. Use `git add` and `git commit` to complete one local commit.
3. Use `git switch -c` to create a task branch.
4. Use `git diff` to check changes before committing.
5. Use `git push` to push the branch and create a PR.
6. Use `git restore` to undo local changes.

## Don't Rush to Use High-Risk Commands

Use with caution during the novice stage:

```bash
git reset --hard
git push --force
git clean -fd
```

These commands may directly discard local changes or rewrite remote history.

If you just want to undo ordinary workspace changes, prioritize learning [Undo Anything](../../06-troubleshooting/06-troubleshooting_en/undo-anything_en.md).

## Extended Reading

- [Git Official Documentation](https://git-scm.com/docs)
- [Git Cheat Sheet](https://git-scm.com/cheat-sheet.pdf)
- [Pro Git: Git Basics](https://git-scm.com/book/en/v2/Git-Basics-Getting-a-Git-Repository)
- [Recommended Reading Index](../../09-resources/09-resources_en/recommended-reading_en.md)
