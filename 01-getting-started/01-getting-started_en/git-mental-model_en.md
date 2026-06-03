# Git Mental Model

English | [中文](../git-mental-model.md)

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
| `git restore --staged` | Index -> Working tree |
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
