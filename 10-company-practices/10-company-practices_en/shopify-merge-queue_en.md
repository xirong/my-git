# Shopify Merge Queue Practice

English | [中文](../shopify-merge-queue.md)

Original links:

- [Successfully Merging the Work of 1000+ Developers](https://shopify.engineering/successfully-merging-work-1000-developers)
- [Introducing the Merge Queue](https://shopify.engineering/introducing-the-merge-queue)

Shopify's Merge Queue practice is highly suitable for explaining why large teams cannot rely on manual merge clicks.

In their public articles, Shopify mentions using a trunk-based workflow on a monolithic codebase, with massive amounts of changes entering `master` daily. As team size increases, direct merging leads to soft conflicts, deployment backlogs, and continued merges during incidents.

## Three Safety Rules

Shopify has summarized three key rules:

- `master` must remain green
- `master` cannot drift too far from production
- Emergency fixes must be fast enough

These three rules are highly adaptable for typical teams.

A green main branch means developers can base their work on it at any time.

A main branch close to production means lower release risks and lower rollback complexity.

Fast emergency fixes mean you won't be delayed by a long queue during incidents.

## Problems Solved by Merge Queue

### Combination Validation

A single PR passing CI does not guarantee that consecutive merges of multiple PRs will still pass.

Merge Queue places the changes in the queue into a context close to the future main branch for validation.

### Controllable Queues

During incidents, the queue can be locked to prevent normal changes from continuing to enter the main branch, leaving the channel open for emergency fixes.

### Clear Auditing

Emergency bypasses, queue failures, and PRs removed from the queue should all leave records.

## Inspiration for GitHub Teams

GitHub native Merge Queue already provides generic capabilities, but Shopify's experience still holds valuable lessons:

- CI stability must be governed first
- Must support `merge_group` or equivalent events
- Emergency channels need to be defined
- Flaky tests will directly impact queue throughput
- Queue batch size must strike a balance between throughput and risk

## When to Adopt

Suitable for:

- High single-repository PR throughput
- Main branch must be deployable at any time
- Multiple teams merging into the main branch simultaneously
- Relatively stable CI
- Need to freeze normal merges during incidents

Not suitable for:

- Few PRs
- Very slow CI
- Many flaky tests
- Teams that have not yet enabled branch protection
