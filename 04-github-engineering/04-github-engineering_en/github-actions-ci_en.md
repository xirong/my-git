# GitHub Actions CI

English | [中文](../github-actions-ci.md)

CI is the baseline quality gate in the GitHub collaboration workflow.

It cannot guarantee that the code is absolutely correct, but it prevents obvious compilation failures, test failures, formatting errors, and basic security issues from entering the main branch directly.

The value of CI is not just about "shipping faster", but more importantly making merge decisions more reliable and giving reviewers and authors more confidence in the quality of changes. For related research, see [Empirical Git Workflow Research Notes](../../09-resources/09-resources_en/empirical-git-workflow-research_en.md).

## Minimal CI

A formal team should at least have:

- lint
- test
- build

Example:

```yaml
name: ci

on:
  pull_request:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npm test
      - run: npm run build
```

Commands vary by language, but the principle is consistent: the most critical paths must be automatically verified before a PR is merged.

## Recommended Practices

- Keep job names stable for easy referencing in branch protection
- Fail fast to avoid obvious errors wasting queue time
- Cache dependencies to reduce CI time
- Trigger heavy tasks by paths for large repositories
- Run necessary checks on both the main branch and PRs
- Manage flaky tests as soon as possible; do not let the team get used to ignoring red lights

## Integration with Branch Protection

In GitHub branch protection, CI jobs can be configured as required status checks.

This prevents PRs from merging into the main branch if they fail CI.

## Multi-Repository Teams

Multi-repository teams should not copy and paste a workflow into every repository.

Extract common checks into reusable workflows, and then have business repositories call them by version. This standardizes job names, permissions, cache strategies, and basic checks, making it easier to promote alongside organizational-level rules.

See [Reusable Workflows](reusable-workflows_en.md) for details.

## AI Programming Scenarios

After AI generates code, CI is the baseline quality assurance.

At a minimum, check:

- Whether compilation passes
- Whether unit tests pass
- Whether linting passes
- Whether dependency lockfiles meet expectations
- Whether generated files conform to repository standards

## Further Reading

- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [Enterprise GitHub Workflow Stack](enterprise-github-workflow-stack_en.md)
- [Reusable Workflows](reusable-workflows_en.md)
- [Empirical Git Workflow Research Notes](../../09-resources/09-resources_en/empirical-git-workflow-research_en.md)
- [GitHub protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
- [GitHub Engineering Governance](github-engineering-governance_en.md)
- [Recommended Reading Index](../../09-resources/09-resources_en/recommended-reading_en.md)
