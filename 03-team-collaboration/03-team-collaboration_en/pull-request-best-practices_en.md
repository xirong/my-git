# Pull Request Best Practices

English | [中文](../pull-request-best-practices.md)

The goal of a PR is to make a change understandable, reviewable, testable, and reversible.

## Recommended Rules

- One PR solves only one problem
- Titles should clearly state behavioral changes
- Descriptions should clearly outline the why, how tested, risks, and rollback plans
- Do not mix in formatting noise
- Separate refactoring from behavioral changes
- Pass CI before merging
- Prioritize reverting when issues occur

## PR Size

If a reviewer cannot review it within a reasonable time, the PR is too large.

It can be split into:

- Preparatory refactoring
- Behavioral changes
- Supplemental testing
- Documentation updates
- Configuration changes

The value of a small PR lies mainly in being easier to understand, roll back, and stack for review; avoid making blanket claims that "small PRs always merge faster."

Research has found no stable correlation between change size and merge time. Teams should still encourage small PRs, but the reasoning should focus on reviewability, verifiability, and reversibility; see [Empirical Git Workflow Research Notes](../../09-resources/09-resources_en/empirical-git-workflow-research_en.md).

Public practices like Google Code Review and Meta Sapling point to the same conclusion: the core value of small changes is lowering comprehension barriers and risk-isolation costs. When AI generates large diffs, they should also be broken down into smaller, human-reviewable units first; see [Tech Giant Engineering Practice Decision Map](../../10-company-practices/10-company-practices_en/company-practices-decision-map_en.md).

## Stacked PRs

When a feature is inherently large, it can be broken down into a series of dependent small PRs:

```text
PR 1: data model
PR 2: service logic
PR 3: API
PR 4: tests and docs
```

This approach is suitable for large features, AI-generated large diffs, and cross-module refactoring.

Things to Note:

- Each PR must be explainable on its own
- PR descriptions must clarify dependencies
- Merge order must be explicit
- Subsequent PRs must promptly rebase following preceding changes

## Templates

Use the [Pull Request Template](../../08-templates/08-templates_en/pull-request-template_en.md) directly.

## What Should a Good PR Include?

- A clear title
- A brief background explanation
- A focused diff
- Reproducible validation methods
- Risk explanations
- Rollback plans
- Necessary screenshots or logs

## AI Programming Scenarios

After AI generates code, the PR description should not merely say "AI generated."

At a minimum, clarify:

- The problem the human intended to solve
- The files the AI actually modified
- Which diffs have been manually reviewed
- What validation has been run
- What remaining risks reviewers should focus on

## Extended Reading

- [GitHub Docs: About pull requests](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests)
- [GitHub Docs: About pull request reviews](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/about-pull-request-reviews)
- [Atlassian: Making a Pull Request](https://www.atlassian.com/git/tutorials/making-a-pull-request)
- [Meta Sapling and Stacked Commits Practices](../../10-company-practices/10-company-practices_en/meta-sapling-stacked-commits_en.md)
- [Tech Giant Engineering Practice Decision Map](../../10-company-practices/10-company-practices_en/company-practices-decision-map_en.md)
- [Empirical Git Workflow Research Notes](../../09-resources/09-resources_en/empirical-git-workflow-research_en.md)
- [Recommended Reading Index](../../09-resources/09-resources_en/recommended-reading_en.md)
