# Merge Queue

English | [中文](../merge-queue.md)

Merge Queue is suitable for teams with frequent PR merges and a busy main branch.

The problem it solves is: each PR passes CI individually, but when multiple PRs are merged sequentially, the combined result might break the main branch.

## The Problem

Suppose two PRs are both based on the same `main`:

```text
main: A
PR 1: A + B
PR 2: A + C
```

Both PR 1 and PR 2 pass CI when run individually.

But after PR 1 is merged first, what PR 2 actually needs to merge into is:

```text
A + B + C
```

This combined result has not been verified, and it could break the main branch.

## Suitable Scenarios

- A large number of PRs are merged into the main branch every day
- The main branch must remain stable
- CI is fully automated
- The team can accept queuing for merges
- The repository has already enabled required status checks

## Unsuitable Scenarios

- Very few PRs
- CI is very slow and lacks resources
- The team does not yet have stable basic checks
- The main branch is not required to be deployable at any time

## Prerequisites for Use

Before enabling Merge Queue, confirm that:

- CI can handle merge queue-related events
- Required checks names are stable
- The team understands the behavior once a PR enters the queue
- Emergency hotfixes have a clear processing path

## Implementation Key Points

If using GitHub Actions, critical workflows must respond to the `merge_group` event:

```yaml
on:
  pull_request:
  merge_group:
```

Merge Queue is best enabled after branch protection and required checks are stable. If CI is slow or there are many flaky tests, the queue will amplify these issues.

Shopify's public practices are a useful reference: as team size grows, passing CI for a single PR is no longer enough; the combined result after queuing must also be verified, and the queue status, failure reasons, and retry paths must be presented to developers. The core value of Merge Queue is exposing the combined risk before merging into the main branch.

If the team doesn't yet have stable CI, required checks, branch protection, and hotfix paths, fill in the basic capabilities first before enabling Merge Queue. For more case comparisons, see [Big Tech Engineering Practice Decision Map](../../10-company-practices/10-company-practices_en/company-practices-decision-map_en.md).

## Further Reading

- [Merge Queue Practices](../../10-company-practices/10-company-practices_en/merge-queue-practices_en.md)
- [Shopify Merge Queue Practices](../../10-company-practices/10-company-practices_en/shopify-merge-queue_en.md)
- [Big Tech Engineering Practice Decision Map](../../10-company-practices/10-company-practices_en/company-practices-decision-map_en.md)
- [Enterprise GitHub Workflow Stack](enterprise-github-workflow-stack_en.md)
- [GitHub protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
- [GitHub Docs: Managing a merge queue](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue)
- [GitHub Docs: merge_group event](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#merge_group)
- [GitHub Engineering Governance](github-engineering-governance_en.md)
- [Recommended Reading Index](../../09-resources/09-resources_en/recommended-reading_en.md)
