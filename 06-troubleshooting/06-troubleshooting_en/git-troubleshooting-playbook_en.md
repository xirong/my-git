# Git Troubleshooting Playbook

English | [中文](../git-troubleshooting-playbook.md)

Before attempting recovery, first answer three questions:

1. Has the code been committed?
2. Has the commit been pushed?
3. Has anyone continued development based on these commits?

Different answers require completely different handling methods.

## First Aid Decision Tree

| Current State | What to Do First | Recommended Handling | What to Avoid |
| --- | --- | --- | --- |
| Code not yet committed | `git status`, and if necessary `git stash push -u` | Use `git restore`, `git stash`, or manually move files to preserve the current state | Direct `git reset --hard` |
| Committed, not yet pushed | `git log --oneline -5`, `git reflog -10` | Can use `reset`, `commit --amend`, `rebase -i` to clean up local history | Cleaning up without leaving a backup branch |
| Pushed, but no one is developing based on it | First confirm remote branch and team status | Prioritize `git revert`; if history must be rewritten, communicate first then `push --force-with-lease` | Direct `push --force` |
| Pushed, and someone is developing based on it | First notify collaborators, confirm scope of impact | Use a new commit to fix, prioritize `revert` for public branches | Rewriting public history |
| Secret has been committed | Immediately revoke and rotate secret | Then clean up Git history and platform cache | Ending with just a revert |
| Force push overwrote remote | Find someone who still has the correct commits or local reflog | Restore remote branch with correct commit | Continuing to stack commits on the wrong branch |

If you are unsure which category you belong to, execute only read-only commands first:

```bash
git status
git log --oneline --decorate -10
git reflog -10
git branch -vv
```

Do not rush to execute commands that alter the working tree or history.

## Preserve the Current State Before Fixing

Capture the current state first:

```bash
git status
git log --oneline --decorate -10
git reflog -10
```

If the working tree still has uncommitted code, confirm that all of it belongs to you and that you intend to restore it later before temporarily saving it:

```bash
git stash push -u -m "backup-before-recovery"
```

If status includes edits owned by someone else or untracked files with an uncertain source, stop in this worktree, preserve the state, or use a separate worktree.

## Scenario 1: Committed to the wrong branch

### Phenomenon

You made a commit on a branch named `main` that originally belonged in a feature branch. `main` is an example; use the wrong branch name established by the checks.

### Check First

```bash
git status --porcelain
git log --oneline -5
```

### Safe Handling: Not yet pushed

This flow applies only when the last commit has not been pushed, no collaborator depends on it, and `git status --porcelain` prints nothing. If there is staged, unstaged, or untracked content, stop before reset and preserve the state.

```bash
git branch feat/right-branch
git reset --hard HEAD~1
git switch feat/right-branch
```

This will preserve the current commit in a new branch and revert the original branch to its pre-commit state.

### If already pushed

If already pushed, prioritize creating a new PR to fix it; do not directly rewrite public branch history.

You can:

```bash
git switch -c feat/right-branch <commit-sha>
git push -u origin feat/right-branch
```

Then undo it on the original branch using revert:

```bash
git revert <commit-sha>
```

## Scenario 2: Reset to the wrong position

### Check First

```bash
git reflog
```

### Recovery Method

After finding the position before the reset, first confirm a clean workspace and preserve the current position, then recover:

```bash
git status --porcelain
git branch backup-before-recover HEAD
git reset --hard HEAD@{1}
```

Stop when `git status --porcelain` prints anything. `HEAD@{1}` must come from the reflog entry just inspected; do not guess by position.

## Scenario 3: Lost a commit

### Check First

```bash
git reflog
```

### Recovery Method

```bash
git branch recovered-work <commit-sha>
git switch recovered-work
```

As long as the commit is still in the reflog, it can usually be recovered.

## Scenario 4: Incorrect code already pushed

### If no one has continued developing based on it

You can amend the history after confirming with the team:

```bash
git revert <commit-sha>
```

Prioritize using revert because it does not rewrite public history.

### If the commit includes a secret

Do not just revert.

First revoke and rotate keys, then clean up history, see [Remove Secret from History](remove-secret-from-history_en.md).

## Scenario 5: Force push overwrote remote branch

### Check First

```bash
git reflog
git log --oneline --decorate -10
```

`<integration-branch>` is the actual integration branch that was overwritten, such as `main`, `master`, or `develop`. Have colleagues who still retain the old commits execute:

```bash
git log --oneline origin/<integration-branch> -10
git reflog -10
```

### Restore Remote Branch

After finding the correct commit, confirming remote permissions and branch rules, and obtaining authorization from the relevant owner:

```bash
git push origin <good-sha>:<integration-branch>
```

If the branch is protected, it requires handling by an administrator or platform owner.

## Scenario 6: Merged the wrong branch

### If a merge commit has already been generated

```bash
git log --oneline --merges -10
git revert -m 1 <merge-commit-sha>
```

`-m 1` indicates keeping the perspective of the first parent branch, undoing the changes brought by the merged branch.

### Avoid

Do not carelessly run `reset --hard` on a main branch that has already been pushed and is being used by others.

## Scenario 7: Committed a secret

### First Action

Immediately revoke and rotate the secret.

Git history cleanup cannot make an already leaked token secure again.

### Then Clean Up History

Use `git filter-repo` or a secure processing flow provided by the platform.

See [Remove Secret from History](remove-secret-from-history_en.md).

## Scenario 8: Rebase process gets messy

### Still in rebase, abort first

```bash
git rebase --abort
```

### Continue after resolving conflicts

```bash
git status
git add <files>
git rebase --continue
```

### Recover to before rebase

```bash
git reflog
git status --porcelain
git branch backup-before-rebase-recover HEAD
git reset --hard <before-rebase-sha>
```

This also requires `git status --porcelain` to print nothing, and `<before-rebase-sha>` must come from an inspected reflog entry rather than a guessed commit.

## Scenario 9: Reverting a public commit

For public commits, prioritize using:

```bash
git revert <commit-sha>
```

This adds a reverse commit, keeping history clear and collaborators safe.

## Scenario 10: Cleaning up local changes

### First identify what will be deleted

```bash
git status --porcelain
git clean -nd
```

`git clean -nd` only lists candidates; it does not prove that they may be deleted.

### Delete untracked files

After confirming that a path is an untracked file the owner authorizes discarding, name that path precisely:

```bash
git clean -f -- <owned-untracked-path>
```

### Discard tracked file changes

After confirming path ownership, the expected baseline, and authorization:

```bash
git restore --worktree -- <owned-tracked-path>
```

### High-risk operation

First run:

```bash
git status --porcelain
```

If `git status --porcelain` prints anything, stop. Only when the worktree is clean, `<verified-ref>` has been verified, and local history may be rewritten, preserve the current position and run reset:

```bash
git branch backup-before-hard-reset HEAD
git reset --hard <verified-ref>
```

If there is staged, unstaged, or untracked content that must be retained, stop rather than run a broad restore, clean, or reset.

## Quick Decision Table

| State | Priority Plan |
| --- | --- |
| Not committed | `git stash` or `git restore` |
| Committed, not pushed | `reset`, `commit --amend`, interactive rebase |
| Pushed, no one developing based on it | Can rewrite history after negotiation |
| Pushed, someone developing based on it | Prioritize `git revert` |
| Committed a secret | First rotate keys, then clean up history |

## Further Reading

- [Undo Anything](undo-anything_en.md)
- [Recover Lost Commit](recover-lost-commit_en.md)
- [Remove Secret from History](remove-secret-from-history_en.md)
- [Git Flight Rules](https://github.com/k88hudson/git-flight-rules)
- [git reflog](https://git-scm.com/docs/git-reflog.html)
- [git restore](https://git-scm.com/docs/git-restore.html)
- [Recommended Reading Index](../../09-resources/09-resources_en/recommended-reading_en.md)
