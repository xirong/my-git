# Recover Force Push

English | [中文](../recover-force-push.md)

After a force push overwrites a remote branch, first retrieve the correct commit.

If someone still retains the old branch locally, it can usually be recovered.

## Preserve the Current State

First notify the team to pause pushing to the related branch.

Then check locally:

```bash
git reflog
git log --oneline --decorate -20
```

You can also ask colleagues to check locally:

```bash
git reflog
git log --oneline --decorate -20
```

## Find the Correct Commit

After confirming the good sha, first create a backup branch:

```bash
git branch backup-good-main <good-sha>
```

Check the content:

```bash
git show --stat <good-sha>
git diff <bad-sha>..<good-sha>
```

## Restore Remote Branch

```bash
git push origin <good-sha>:main
```

If the main branch is protected, it requires administrator handling.

## Follow-up Remediation

- Check if anyone continued developing based on the wrong history
- Notify everyone to resynchronize
- Enable branch protection for the main branch
- Restrict force push permissions
- Conduct a post-mortem on why it happened

## Further Reading

- [git reflog Official Documentation](https://git-scm.com/docs/git-reflog.html)
- [GitHub protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
- [Git Troubleshooting Playbook](git-troubleshooting-playbook_en.md)
