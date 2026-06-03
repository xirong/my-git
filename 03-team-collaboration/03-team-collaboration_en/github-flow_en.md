# GitHub Flow

English | [中文](../github-flow.md)

GitHub Flow is a lightweight branching workflow, suitable for small teams and Web services with a stable main branch, frequent releases, and complete CI.

Its core philosophy is: the main branch remains deployable, and all changes are merged via short-lived branches and PRs.

In enterprise teams, GitHub Flow shouldn't be limited to just a lightweight process. By pairing it with branch protection, CODEOWNERS, Rulesets, Merge Queue, Actions, and security scanning, it can evolve into a complete GitHub collaboration configuration stack.

## Process

```text
main -> branch -> pull request -> review -> CI -> merge -> deploy
```

## Suitable Scenarios

- Web services
- Small or medium-sized teams
- High release frequency
- Well-established automated testing and CI
- Fast rollback when issues occur

## Basic Rules

- `main` always remains deployable
- Create a short-lived branch for every change
- Merge every branch via PR
- Complete at least review and CI before merging
- Deploy as soon as possible after merging
- Prioritize reverting when issues occur

## Branch Lifecycle

GitHub Flow discourages long-lived feature branches.

If a feature takes a long time to develop, break it down:

- Merge preparatory refactoring with no behavioral changes first
- Then merge backend capabilities
- Then merge frontend entry points
- Control unfinished capabilities using feature flags

## Common Misconceptions

### 1. `main` is unprotected

If everyone can push directly to `main`, GitHub Flow will quickly devolve into chaotic centralized committing.

Minimum requirements:

- Require pull request
- Required status checks
- Required review

### 2. PRs are too large

GitHub Flow relies on fast reviews.

When PRs are too large, reviews become a mere formality.

### 3. Lack of deployment and rollback mechanisms

GitHub Flow is suited for high-frequency releases, provided deployments and rollbacks are reliable enough.

## Enterprise Configuration

Recommended minimum configuration:

- Enable branch protection for `main`
- All changes go through PRs
- CODEOWNERS covers critical directories
- CI configured as required status checks
- Shift security scanning left to the PR or push phase
- Enable Merge Queue after reaching high PR concurrency
- Track tags, releases, and deployment status after merging

## Extended Reading

- [GitHub Docs: GitHub Flow](https://docs.github.com/en/get-started/using-github/github-flow)
- [Enterprise GitHub Flow Practices](../../10-company-practices/10-company-practices_en/github-flow-enterprise_en.md)
- [Enterprise GitHub Collaboration Stack](../../04-github-engineering/04-github-engineering_en/enterprise-github-workflow-stack_en.md)
- [GitHub protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
- [Pull Request Best Practices](pull-request-best-practices_en.md)
- [Recommended Reading Index](../../09-resources/09-resources_en/recommended-reading_en.md)
