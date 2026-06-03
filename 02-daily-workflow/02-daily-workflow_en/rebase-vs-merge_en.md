# Rebase vs Merge

English | [中文](../rebase-vs-merge.md)

Both `merge` and `rebase` can combine two histories together, but they express different collaborative semantics.

Simply put:

- `merge` preserves the branch merge history
- `rebase` moves the commits of the current branch onto a new base

## Scenarios Suitable for merge

### 1. Merging Public Branches

When the history on a public branch has already been seen or built upon by others, prioritize using merge or revert to avoid casually rewriting history.

### 2. Wanting to Preserve Branch Context

If a feature branch represents a complete set of work, a merge commit can preserve the context of this integration.

### 3. Team Requires Clear Auditing

Some teams want to see from the history "when which branch was merged in"; in this case, merge is more appropriate.

## Scenarios Suitable for rebase

### 1. Cleaning Up Unpushed Local Commits

When local commits have not yet been pushed, you can use interactive rebase to clean up commits:

```bash
git rebase -i HEAD~3
```

Common operations:

- Modifying commit messages
- Squashing fragmented commits
- Adjusting commit order
- Deleting useless commits

### 2. Keeping a Feature Branch Up to Date with the Main Branch

```bash
git fetch origin
git rebase origin/main
```

This allows your branch history to be placed right after the latest main branch.

### 3. Keeping PR History More Linear

Some teams prefer a linear history and will require feature branches to be rebased onto the latest position of the main branch before merging.

## High-Risk Areas

Avoid rebasing public branches that have already been built upon by others.

GitHub documentation also warns that rebase rewrites commit history. Rebasing commits that have already been pushed to the repository will cause trouble for other collaborators.

## Recommended Rules

| Scenario | Recommendation |
| --- | --- |
| Cleanup of unpushed local commits | rebase |
| Syncing feature branch with main branch | rebase or merge, depending on team convention |
| Merging PRs into the main branch | merge, squash, or rebase merge, depending on repository strategy |
| Fixing errors in public history | revert |
| Someone has already built upon your branch | Avoid rebase |

## Common Commands

```bash
git merge feature/login
git rebase origin/main
git rebase -i HEAD~3
git rebase --abort
git rebase --continue
```

## Further Reading

- [GitHub Docs: About Git rebase](https://docs.github.com/en/get-started/using-git/about-git-rebase)
- [Pro Git: Rebasing](https://git-scm.com/book/en/v2/Git-Branching-Rebasing)
- [Atlassian: Merging vs Rebasing](https://www.atlassian.com/git/tutorials/merging-vs-rebasing)
- [Recommended Reading Index](../../09-resources/09-resources_en/recommended-reading_en.md)
