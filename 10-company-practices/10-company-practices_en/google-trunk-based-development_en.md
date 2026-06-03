# Google Trunk-Based Development and Version Control Practice

English | [中文](../google-trunk-based-development.md)

Original links:

- [Software Engineering at Google: Version Control and Branch Management](https://abseil.io/resources/swe-book/html/ch16.html)
- [Trunk Based Development](https://trunkbaseddevelopment.com/)

## 1. Key Judgments from Google's Practice

The focus of trunk-based development is to have the team continuously integrate around a single main line of code, minimizing long-term branches.

The underlying judgment is: the longer a branch exists, the greater the integration risk, the later the feedback, and the harder it is to handle conflicts and semantic divergences.

The core reason large-scale teams adopt trunk-based development is that it exposes complexity early into daily integration, testing, and reviews.

## 2. Prerequisites for Trunk-Based Development

| Prerequisite | Description |
| --- | --- |
| Fast CI | Rapid feedback is required before and after changes are merged |
| Small Changes | Every commit and PR must be small enough to facilitate review and rollback |
| Code Ownership | Critical paths need responsible people for review |
| Automated Testing | Trunk stability relies on reliable test signals |
| Feature Flags | Unfinished capabilities must not be exposed directly to users |
| Fast Rollback | Must be able to quickly undo changes when the trunk encounters issues |

Without these prerequisites, trunk-based development becomes "everyone just dumping code straight into the main branch."

## 3. Branch Strategy

Trunk-based development does not mean having absolutely no branches.

A more realistic approach is:

- Short-lived branches can be created for each task
- Branches exist only for a few hours to a few days
- Initiate PR or change review as early as possible
- Isolate unfinished capabilities using feature flags
- Continue to rely on CI and monitoring for validation after merging into the trunk

```text
short-lived branch -> review -> main -> CI -> release
```

## 4. Why it is Suitable for Large-Scale Collaboration

### Integration risks surface earlier

Long-term branches delay risks until the day of merging.

Trunk-based development breaks risks into small pieces, handling them in daily commits and checks.

### Production truth is closer to the mainline

The closer the mainline is to production, the easier it is to locate problems.

When production versions can be traced back to clear commits or tags on the mainline, both rollbacks and auditing become easier.

### Platforms can optimize around the mainline

CI, code search, dependency analysis, code ownership, and release systems can all build unified models around the mainline.

Multiple long-term branches would cause the complexity of these capabilities to increase rapidly.

## 5. How Typical Teams Can Adopt It

Do not strive for "pure trunk-based development" right from the start.

A more stable sequence is:

1. Shorten the lifecycle of feature branches
2. Require PRs to be sufficiently small
3. Establish required CI checks
4. Configure owners for core directories
5. Introduce feature flags
6. Establish a revert-first habit for incident handling
7. Then progressively reduce long-term branches

## 6. When to Adopt

Suitable for:

- Web services
- Backend services
- Platform engineering
- Teams with mature automated testing
- Products with high release frequencies and manageable rollback costs

Not suitable for:

- Strong version delivery on clients
- Private deployments
- Unstable CI
- Lack of feature flags
- Teams accustomed to large-batch merging

## 7. Key Takeaways

Trunk-based development is not a lightweight process slogan; it is the result of a set of engineering capabilities.

If a team wants to use it, they must simultaneously build:

- Small PRs
- Fast CI
- Stable tests
- Code ownership
- Feature flags
- Fast rollback

These capabilities are more important than "whether to keep only one main branch."
