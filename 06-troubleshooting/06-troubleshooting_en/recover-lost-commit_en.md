# Recover Lost Commit

English | [中文](../recover-lost-commit.md)

When you lose a commit, check reflog first.

Many "lost" commits are actually still local, just that the current branch pointer no longer points to them.

## Capture the Current State

```bash
git status
git log --oneline --decorate -10
git reflog -20
```

If there are still uncommitted changes in the working tree:

```bash
git stash push -u -m "backup before recover lost commit"
```

## Find Commit Using Reflog

```bash
git reflog
```

After finding the target commit, do not rush to reset; first create a recovery branch:

```bash
git branch recovered-work <commit-sha>
git switch recovered-work
```

This allows you to check the content first:

```bash
git show --stat
git diff main...HEAD
```

## Common Recoverable Scenarios

- Reset incorrectly
- Commits disappeared after rebase
- Amend overwrote the previous commit
- Cannot find recent commits after switching branches
- Deleted a local branch

## When Recovery Might Be Impossible

- Reflog has expired
- Local objects have been garbage collected
- Never committed, just working tree files were deleted
- Only exists on someone else's machine, no local object

If it was never committed, Git usually cannot save it; you need to look at editor history, local backups, or IDE local history.

## Further Reading

- [git reflog Official Documentation](https://git-scm.com/docs/git-reflog.html)
- [Atlassian: git reflog](https://www.atlassian.com/git/tutorials/rewriting-history/git-reflog)
- [Git Flight Rules](https://github.com/k88hudson/git-flight-rules)
- [Git Troubleshooting Playbook](git-troubleshooting-playbook_en.md)
