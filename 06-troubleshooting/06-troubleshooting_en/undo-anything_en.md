# Undo Anything

English | [中文](../undo-anything.md)

Before undoing in Git, first determine the state of the changes.

Only three questions matter:

1. Have the changes been committed?
2. Has the commit been pushed?
3. Has anyone continued development based on it?

## Local Uncommitted Changes

Discard working tree changes of a file:

```bash
git restore <file>
```

Unstage:

```bash
git restore --staged <file>
```

Discard working tree changes of all tracked files:

```bash
git restore .
```

Check before executing:

```bash
git status
git diff
```

## Committed but Not Pushed

Amend the last commit:

```bash
git commit --amend
```

Undo the last commit, but keep changes in the staging area:

```bash
git reset --soft HEAD~1
```

Undo the last commit, and keep changes in the working tree:

```bash
git reset HEAD~1
```

## Pushed Public Commits

For public commits, prioritize using:

```bash
git revert <commit-sha>
```

This will add a reverse commit, keeping history clear without breaking collaborators' local branches.

## High-Risk Commands

```bash
git reset --hard
git push --force
git clean -fd
```

Before executing these commands, confirm there are no changes you need to preserve.

Create a backup branch first:

```bash
git branch backup-before-undo
```

## Further Reading

- [GitHub Blog: How to undo almost anything with Git](https://github.blog/open-source/git/how-to-undo-almost-anything-with-git/)
- [git restore Official Documentation](https://git-scm.com/docs/git-restore)
- [git revert Official Documentation](https://git-scm.com/docs/git-revert)
- [Git Troubleshooting Playbook](git-troubleshooting-playbook_en.md)
