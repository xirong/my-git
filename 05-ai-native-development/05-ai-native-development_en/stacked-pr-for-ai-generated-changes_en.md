# Stacked PR for AI-Generated Changes

English | [中文](../stacked-pr-for-ai-generated-changes.md)

Original links:

- [Google Small CLs](https://google.github.io/eng-practices/review/developer/small-cls.html)
- [GitHub Stacked PRs](https://github.github.com/gh-stack/)
- [GitHub Stacked PRs Overview](https://github.github.com/gh-stack/introduction/overview/)
- [Sapling ReviewStack](https://sapling-scm.com/docs/addons/reviewstack/)
- [Graphite: Stacked Diffs](https://graphite.com/guides/stacked-diffs)

AI easily generates a large PR that looks complete but is actually hard to review.

The value of Stacked PRs lies in splitting a large change into a set of PRs with dependencies, allowing each step to be understood, verified, and rolled back.

## 1. What is a Stacked PR

Ordinary PR:

```text
main <- big-pr
```

Stacked PR:

```text
main <- pr-1 <- pr-2 <- pr-3
```

`pr-1` is merged into the main line first, `pr-2` is based on `pr-1`, and `pr-3` is based on `pr-2`.

Each PR solves a smaller problem.

## 2. Why it is Suitable for AI-Generated Code

Common problems with AI-generated code:

- Too many files modified at once.
- Behavioral changes, refactoring, tests, and documentation are mixed together.
- Reviewers need to reconstruct intent.
- It is hard to roll back only the risky parts.

Stacked PRs can split it into:

```text
PR 1: add tests
PR 2: change implementation
PR 3: remove old helper
PR 4: update docs
```

This way, reviewers can gradually understand intent, and CI can verify layer by layer.

## 3. Ways to Split

### Split by Layer

```text
data model -> service -> API -> UI
```

Suitable for features with clear architectural layering.

### Split by Behavior

```text
support feature A -> support feature B -> enable flag
```

Suitable for multiple sub-capabilities.

### Split by Risk

```text
test only -> refactor no behavior change -> behavior change -> cleanup
```

Suitable for AI refactoring or incident fixes.

## 4. Operational Rules

- Each PR must be independently explainable.
- Each PR must clearly state its dependencies.
- Downstream PRs must be rebased promptly after upstream PR changes.
- Do not mix generated files and behavioral changes in one PR.
- Merge order must be clear.
- Rollback prioritized from top of the stack downwards.

## 5. Relationship with Commit Splitting

Commit splitting is suitable for keeping history clear within a PR.

Stacked PRs are suitable for splitting a large feature into multiple review units.

They can be used in combination:

```text
stacked PR
  -> each PR has small logical commits
```

Meta Sapling's public practice indicates that commit stacks are suitable for expressing a set of continuous small changes. After AI generates a large diff, you can borrow this idea to transform "large chunks of results" into "reviewable sequences of changes." For more case comparisons, see [Enterprise Git Workflow Stack Decision Map](../../10-company-practices/10-company-practices_en/company-practices-decision-map_en.md).

## 6. Suitable Scenarios

Suitable for:

- AI generating a large diff at once.
- Large features landing incrementally.
- Cross-layer changes.
- Behavioral changes following refactoring.
- Changes requiring review from multiple owners.

Not suitable for:

- Very small bugfixes.
- Multiple independent tasks without dependencies.
- Teams that do not yet have stable PR Review habits.

## Extended Reading

- [Meta Sapling and Stacked Commits Practice](../../10-company-practices/10-company-practices_en/meta-sapling-stacked-commits_en.md)
- [Google Code Review Practice](../../10-company-practices/10-company-practices_en/google-code-review_en.md)
- [Enterprise Git Workflow Stack Decision Map](../../10-company-practices/10-company-practices_en/company-practices-decision-map_en.md)
