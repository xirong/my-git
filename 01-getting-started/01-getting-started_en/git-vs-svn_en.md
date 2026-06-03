# Git vs SVN

English | [中文](../git-vs-svn.md)

Many people naturally understand Git in an SVN way when they first encounter it.

This leads to a problem: you can complete commits and updates with Git, but it's hard to leverage Git's true value in local commits, branching, merging, and PR collaboration.

## Core Differences

| Topic | SVN | Git |
| --- | --- | --- |
| Repository Model | Central repository mainly | Everyone has a complete local repository |
| Commit Location | Usually committed directly to the central repository | Committed to the local repository first |
| Branching Cost | Relatively high | Very low, used daily |
| Offline Work | Weak capability | Can fully commit, view history, and switch branches |
| Collaboration Style | Tends to be centralized | Tends to be distributed |
| Review Method | Often relies on post-commit checks | Often through pre-merge review via PRs |

## Common Pitfalls When Migrating from SVN to Git

### 1. Only committing once at the very end

In the SVN era, many people were used to "committing only after finishing".

Git recommends committing in logical batches, where each commit expresses a clear intent.

### 2. Fearing branch creation

Git branches are very lightweight; daily tasks should prioritize isolation using branches.

Recommendation:

```bash
git switch -c feat/my-task
```

### 3. Treating pull as mindless synchronization

`git pull` actually consists of fetch and merge; improper use can generate many meaningless merge commits.

On personal feature branches, consider:

```bash
git pull --rebase
```

But avoid rebasing public branches that others have based their work on.

### 4. Ignoring PR review

Git's value lies not only in local commands but also in pre-merge review.

Teams should try to merge into the main branch via PRs as much as possible, avoiding everyone directly pushing to the main branch.

## When You Might Still Encounter SVN

- Legacy systems still using SVN
- Some documentation or artifact repositories still retain SVN
- The transition phase when a company migrates from SVN to Git

If you want to migrate, first unify the team's branching strategy, commit conventions, and main branch protection rules before migrating the tools.

## Extended Reading

- [Pro Git: Distributed Git](https://git-scm.com/book/en/v2/Distributed-Git-Distributed-Workflows)
- [Atlassian: Migrating from SVN to Git](https://www.atlassian.com/git/tutorials/migrating-overview)
- [Git Workflow Tutorial (Legacy)](../../09-resources/legacy/git-workflow-tutorial.md)
- [Recommended Reading Index](../../09-resources/09-resources_en/recommended-reading_en.md)
