# Everyday Git Commands

English | [中文](../everyday-git-commands.md)

This is not a complete command manual; it only preserves the most commonly used path for daily development.

The goal is to enable you to reliably complete:

```text
Pull latest code -> Create branch -> Modify -> Check diff -> Commit -> Push -> Open PR
```

## Starting a Task

`<integration-branch>` is the integration branch selected by the repository and team, such as `main`, `master`, or `develop`. Before this flow, confirm that the workspace has no other pending edits. If `git status --porcelain` prints anything, preserve the state or move to a clean worktree; do not overwrite it with switching or synchronization commands.

```bash
git status --porcelain
git branch --show-current
git switch <integration-branch>
git pull --rebase origin <integration-branch>
git switch -c feat/my-task
```

## Checking Current Status

```bash
git status
git diff
git diff --stat
```

Always check the diff before committing.

Especially during AI-assisted development, first confirm there are no unrelated files, formatting noise, temporary logs, secrets, or build artifacts.

## Staging and Committing

Use `git add -p` to stage in chunks:

```bash
git add -p
git commit -m "feat(scope): describe change"
```

If the changes this time are very small, you can also directly:

```bash
git add <file>
git commit -m "fix(scope): describe bug fix"
```

## Syncing with the Main Branch

Before synchronizing a personal feature branch, confirm that the team permits rebasing, that collaborators have not based work on this branch, and that `git status --porcelain` prints nothing. Replace `origin/<integration-branch>` with the remote-tracking ref for the actual integration branch.

```bash
git status --porcelain
git fetch origin
git rebase origin/<integration-branch>
```

If you are unsure whether you should rebase, read [Rebase vs Merge](rebase-vs-merge_en.md) first.

## Pushing the Branch

```bash
git push -u origin feat/my-task
```

Then create a PR on GitHub / GitLab.

## Temporarily Switching Tasks

`git stash push -u` puts all currently tracked and untracked content into the stash. Use it only when all of that content belongs to you and you intend to restore it later. If edits have another owner or an uncertain source, stop in this worktree and use a separate worktree instead.

```bash
git stash push -u -m "wip: current task"
git switch <integration-branch>
git switch -c hotfix/urgent-fix
```

To restore:

```bash
git switch feat/my-task
git stash apply
```

## When Something Goes Wrong

Capture the current state first:

```bash
git status
git log --oneline --decorate -10
git reflog -10
```

Then follow the [Git Troubleshooting Playbook](../../06-troubleshooting/06-troubleshooting_en/git-troubleshooting-playbook_en.md) to select a recovery method.

## Further Reading

- [Git Official Documentation](https://git-scm.com/docs)
- [Git Cheat Sheet](https://git-scm.com/cheat-sheet.pdf)
- [Atlassian Git tutorials](https://www.atlassian.com/git)
- [Legacy Command Manual (Archived)](../../09-resources/legacy/useful-git-command.md)
