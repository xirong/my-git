# Committed to Wrong Branch

English | [中文](../committed-to-wrong-branch.md)

When committing to the wrong branch, first determine if it has been pushed.

It is easy to handle when not yet pushed. Once pushed, prioritize avoiding disruption to the public history.

## Check First

```bash
git status
git branch --show-current
git log --oneline --decorate -5
```

## Not Yet Pushed

Assume you accidentally committed the last commit to `main`, but it should have been in `feat/right-branch`.

```bash
git branch feat/right-branch
git reset --hard HEAD~1
git switch feat/right-branch
```

This preserves the current commit in a new branch and reverts the original branch to its pre-commit state.

## Already Pushed

If already pushed to a public branch, prioritize using revert to correct the original branch:

```bash
git revert <commit-sha>
```

Then cherry-pick the correct commit to the target branch:

```bash
git switch feat/right-branch
git cherry-pick <commit-sha>
```

## If Multiple Commits are Wrong

You can batch cherry-pick after creating the target branch:

```bash
git switch -c feat/right-branch
git cherry-pick <oldest-sha>^..<newest-sha>
```

Verify the commit range before executing.

## Prevention

- Check `git branch --show-current` before each commit
- Display the current branch in the shell prompt
- Enable branch protection for main branches
- Prohibit direct pushes to main branches in critical repositories

## Further Reading

- [Git Flight Rules](https://github.com/k88hudson/git-flight-rules)
- [git cherry-pick Official Documentation](https://git-scm.com/docs/git-cherry-pick)
- [Undo Anything](undo-anything_en.md)
- [Git Troubleshooting Playbook](git-troubleshooting-playbook_en.md)
