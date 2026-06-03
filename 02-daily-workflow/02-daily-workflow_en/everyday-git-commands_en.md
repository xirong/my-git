# Everyday Git Commands

English | [中文](../everyday-git-commands.md)

This is not a complete command manual; it only preserves the most commonly used path for daily development.

The goal is to enable you to reliably complete:

```text
Pull latest code -> Create branch -> Modify -> Check diff -> Commit -> Push -> Open PR
```

## Starting a Task

```bash
git switch main
git pull --rebase
git switch -c feat/my-task
```

If your team's main branch is named `master` or `develop`, replace it according to the actual branch used by your team.

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

```bash
git fetch origin
git rebase origin/main
```

If you are unsure whether you should rebase, read [Rebase vs Merge](rebase-vs-merge_en.md) first.

## Pushing the Branch

```bash
git push -u origin feat/my-task
```

Then create a PR on GitHub / GitLab.

## Temporarily Switching Tasks

```bash
git stash push -u -m "wip: current task"
git switch main
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
