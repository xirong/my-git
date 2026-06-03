# Merge Queue Practice

English | [中文](../merge-queue-practices.md)

Original links:

- [GitHub Docs: Managing a merge queue](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue)
- [GitHub Docs: merge_group event](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#merge_group)
- [Buildkite: Using GitHub Merge Queue in pipelines](https://buildkite.com/resources/blog/using-github-mergequeue-in-pipelines/)
- [Mergify: The origin story of merge queues](https://mergify.com/blog/the-origin-story-of-merge-queues/)

## 1. What Problem Does Merge Queue Solve

Teams with high-concurrency PRs encounter a classic problem:

```text
main: A
PR 1: A + B, CI passes
PR 2: A + C, CI passes
```

Both PRs look fine individually, but after PR 1 is merged, what PR 2 actually merges into is:

```text
A + B + C
```

This combined result has not been validated, and the main branch could be broken.

The value of Merge Queue is that before actually merging, it constructs a combined result close to what it will be post-merge, and executes required checks on it.

## 2. When to Adopt

Suitable for:

- High PR merge frequency
- Main branch must be stable
- Required checks are already relatively complete
- Sufficient CI resources
- Team is willing to accept queued merging

Not suitable for:

- Few PRs
- CI fails frequently or is very slow
- Unstable check item naming
- No main branch protection
- Emergency hotfix process is not defined

## 3. Preparation Before Enabling

### Stable Required Checks

Merge Queue relies on required status checks.

If check items frequently change names, or check items are inconsistent across different PRs, the queue will become very difficult to maintain.

### CI Supports `merge_group`

GitHub merge queue triggers the `merge_group` event.

If the team uses GitHub Actions, ensure critical workflows respond to this event:

```yaml
on:
  pull_request:
  merge_group:
```

If using external CI, also confirm that it can recognize the temporary refs or corresponding events created by the merge queue.

### Clear Emergency Channels

Merge Queue will increase merge wait times.

The team needs to define in advance how hotfixes are handled, who can temporarily bypass the queue, and how to backfill validation after bypassing.

## 4. Adoption Steps

Recommended sequence:

1. Enable branch protection first
2. Configure required checks
3. Unify CI check names
4. Support `merge_group` in Actions or external CI
5. Enable Merge Queue on a small scale
6. Observe queue duration, failure rates, and CI consumption
7. Expand to the main repository or critical branches

## 5. Common Failure Modes

### CI is too slow causing queue buildup

Merge Queue makes "pre-merge combination validation" explicit.

If CI is inherently slow, the queue will make this problem more obvious. Test layering and concurrency capabilities must be optimized first.

### Flaky tests cause repeated queue failures

Unstable tests will cause queue throughput to drop.

Address flaky tests before enabling it, or at least be able to mark, isolate, and re-run them.

### Nobody understands the queue rules

Developers need to know:

- When a PR enters the queue
- Whether they can still push after entering the queue
- Who handles queue failures
- Whether a check failure is a problem with their own PR or a combination issue

These rules should be written into the team's PR guidelines.

## 6. Key Takeaways

Merge Queue is not a "complex feature" only needed by advanced teams.

When the number of PRs grows to a certain point, it solves the fundamental problem of main branch stability.

However, the sequence of enabling it is critical; stable CI and branch protection must come first before discussing merge queues.
