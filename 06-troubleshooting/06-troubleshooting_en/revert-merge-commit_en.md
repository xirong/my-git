# Revert Merge Commit

English | [中文](../revert-merge-commit.md)

When reverting a merge commit, you need to specify the mainline parent.

For normal commits, you can directly:

```bash
git revert <commit-sha>
```

But a merge commit has two or more parent commits, and Git needs to know which side you want to keep as the mainline.

## Check Merge Commit First

```bash
git show --summary <merge-commit-sha>
git log --oneline --graph --decorate -20
```

Confirm which branch this merge commit was merged from.

## Common Usage

```bash
git revert -m 1 <merge-commit-sha>
```

`-m 1` usually indicates keeping the target branch perspective, undoing the changes brought by the merged branch.

## Why -m is Needed

A merge commit has multiple parents.

For example:

```text
parent 1: Position of main before merge
parent 2: Position of feature branch
```

`-m 1` means taking parent 1 as the mainline, reverting the changes brought by the other branch.

## Risks

After reverting a merge commit, if you want to merge the same branch again in the future, Git may consider part of the changes already handled.

A safer approach is:

- Confirm this is just to roll back a production risk
- Create a new branch for subsequent redevelopment
- Cherry-pick commits to keep if necessary

## Further Reading

- [git revert Official Documentation](https://git-scm.com/docs/git-revert)
- [GitHub Blog: How to undo almost anything with Git](https://github.blog/open-source/git/how-to-undo-almost-anything-with-git/)
- [Git Troubleshooting Playbook](git-troubleshooting-playbook_en.md)
