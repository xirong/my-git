# Meta Sapling and Stacked Commits Practice

English | [中文](../meta-sapling-stacked-commits.md)

Original links:

- [Sapling: Source control that’s user-friendly and scalable](https://engineering.fb.com/2022/11/15/open-source/sapling-source-control-scalable/)
- [Scaling Mercurial at Facebook](https://engineering.fb.com/2014/01/07/core-infra/scaling-mercurial-at-facebook/)

## 1. The Core Problem Meta Faces

In Meta's public materials, Sapling targets massive monorepo scenarios.

The difficulty of such scenarios is not just the sheer number of files, commits, and branches, but also includes:

- Developers struggle to understand the relationships of their own commits
- Large features need to be broken down into multiple continuous small changes
- History amendment and rebase costs are high
- Code review requires understanding a set of related changes
- Basic operations like clone, status, and pull can become slow

The value of Sapling lies in addressing scalability and workflow expression simultaneously.

## 2. What Problem Do Stacked Commits Solve

Stacked commits are ideal for breaking a large feature into multiple small steps that can be reviewed individually:

```text
commit A: add data model
commit B: add service logic
commit C: add API
commit D: add tests and docs
```

Each commit can be reviewed separately, yet they maintain dependency relationships.

This provides specific inspiration for AI coding: AI easily generates large diffs all at once, and humans need to break them back down into an ordered, explainable, and reversible set of small changes.

## 3. Inspiration from Smartlog

Sapling's smartlog emphasizes letting developers intuitively see the location of their local commits, remote mainline, and related branches.

Even if Git users do not use Sapling, they can borrow this idea:

- Use clear branch names to express tasks
- Use small commits to express steps
- Use PR descriptions to explain commit relationships
- Use `git log --graph --oneline --decorate` to assist in understanding history
- Write out the split sequence for complex changes

## 4. Inspiration for Large Repository Performance

Meta's early Scaling Mercurial articles emphasized capabilities like Watchman and remote file log to reduce the costs of status, clone, pull, and rebase.

For Git teams, the corresponding approaches are:

- partial clone
- sparse checkout
- fsmonitor
- commit-graph
- background maintenance
- Pruning by path for IDEs and build systems

## 5. What Typical Teams Can Adopt

Typical teams do not necessarily need Sapling, but they can adopt these practices:

- Break large features into stacked small changes
- Every PR has explicit dependencies and merge order
- Split commits first for AI-generated large diffs
- Large repository optimization should focus on daily developer command experience
- Tools should help developers understand history, not just add commands

## 6. Key Takeaways

Stacked commits, worktrees, multi-Agent parallelism, and PR review can be chained into an AI-era workflow:

```text
AI generates solution
-> Human splits into commit stack
-> Each commit reviewed individually
-> CI validates in stack order
-> Mainline remains clean upon merge
```
