# Feature Branch Workflow

English | [中文](../feature-branch-workflow.md)

Feature Branch Workflow is the most straightforward collaboration model for most teams to adopt.

Its core principle is: develop every feature or fix in an independent branch, and merge it into the main branch via a PR when complete.

## Process

```text
main -> feature branch -> pull request -> review -> CI -> merge
```

## Suitable Scenarios

- Parallel development with multiple people
- Medium to large business systems
- Teams requiring review and CI
- Teams not yet ready for full Trunk-Based Development
- Requirements can generally be broken down into independent tasks

## Branch Recommendations

```text
feat/user-login
fix/payment-timeout
docs/git-workflow-guide
refactor/order-validator
```

Branch names should express the intent of the task; avoid names like `test`, `tmp`, or `new`.

## PR Recommendations

- One PR solves only one problem
- Separate behavioral changes and refactoring as much as possible
- PR descriptions should clearly state validation methods
- Risky changes should clearly outline fallback plans
- Delete branches promptly after merging

## Things to Note

### 1. Branches should not be long-lived

The longer a branch exists, the more it diverges from the main branch, making merge conflicts harder to resolve.

### 2. Sync with the main branch regularly

```bash
git fetch origin
git rebase origin/main
```

Whether to use rebase depends on team conventions.

### 3. Avoid large PRs

If a PR is already hard to review, break it down first.

## Extended Reading

- [Atlassian: Feature Branch Workflow](https://www.atlassian.com/continuous-delivery/principles/workflows-with-feature-branching-and-gitflow)
- [Pull Request Best Practices](pull-request-best-practices_en.md)
- [Code Review Best Practices](code-review-best-practices_en.md)
- [Recommended Reading Index](../../09-resources/09-resources_en/recommended-reading_en.md)
