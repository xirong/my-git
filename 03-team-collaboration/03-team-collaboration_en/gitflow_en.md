# Gitflow

English | [中文](../gitflow.md)

Gitflow is a classic branching model suitable for products with a clear version release cadence.

It divides daily development, release preparation, and live hotfixes into different branch roles. It is ideal for scenarios with distinct release cycles, such as clients, SDKs, and private deployments.

## Branches

- `main`: Production version history
- `develop`: Integration branch
- `feature/*`: Feature development
- `release/*`: Release preparation
- `hotfix/*`: Live urgent hotfixes

## Typical Process

```text
develop -> feature/* -> develop -> release/* -> main -> tag
                              \-> hotfix/* -> main -> develop
```

## Suitable Scenarios

- Need to maintain multiple versions
- Have fixed release windows
- High release costs for clients or SDKs
- Live versions cannot be released at any time
- Explicit testing and acceptance cycles before release

## Unsuitable Scenarios

- High-frequency Web service releases
- Very small teams
- Trunk can be deployed at any time
- Mature CI/CD where release risks can be quickly rolled back

## Advantages

- Clear branch responsibilities
- Explicit paths for release and hotfix
- Suitable for versioned products
- Easy to align with traditional release processes

## Costs

- Many branches, complex processes
- `develop` and `main` may diverge for long periods
- Hotfixes require backporting to multiple branches
- May slow down the pace for high-frequency release teams

## Decision Recommendations

Do not blindly copy Gitflow.

If your team releases Web services multiple times a day, GitHub Flow or Trunk-Based Development is often lighter.

If your product has clear version lines, release windows, and customer-side upgrade cycles, Gitflow still holds value.

Atlassian's Gitflow tutorial also frames it within specific release-oriented scenarios: it is suitable for release trains, release prep, hotfixes, and heavily audited products. In modern CI/CD and high-frequency service delivery, long-lived branches increase the cost of diverging from the mainline and causing integration conflicts.

## Enterprise Practice References

[Tencent Cloud Gitflow Branching Practice](../../10-company-practices/10-company-practices_en/tencent-gitflow_en.md) can serve as a reference for Gitflow-style team guidelines, especially suitable for teams needing well-defined paths for releases, hotfixes, tags, and backporting.

[Alibaba AoneFlow Branching Practice](../../10-company-practices/10-company-practices_en/alibaba-aoneflow_en.md) provides an alternative perspective: retaining the clear boundary between feature and release while reducing the complexity introduced by a long-lived `develop` branch.

## Extended Reading

- [A successful Git branching model](https://nvie.com/posts/a-successful-git-branching-model/)
- [Atlassian: Gitflow Workflow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow)
- [Tencent Cloud Gitflow Branching Practice](../../10-company-practices/10-company-practices_en/tencent-gitflow_en.md)
- [Alibaba AoneFlow Branching Practice](../../10-company-practices/10-company-practices_en/alibaba-aoneflow_en.md)
- [Team Git Workflow Guide](team-git-workflow-guide_en.md)
- [Recommended Reading Index](../../09-resources/09-resources_en/recommended-reading_en.md)
