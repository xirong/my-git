# Microsoft Release Flow

English | [中文](../microsoft-release-flow.md)

Original links:

- [Release Flow: How We Do Branching on the VSTS Team](https://devblogs.microsoft.com/devops/release-flow-how-we-do-branching-on-the-vsts-team/)

Microsoft Release Flow is a great reference for mid-to-large business teams.

It adopts a trunk-based integration approach, but does not deploy `master` directly to production continuously. The team creates a release branch from `master` per sprint, and production hotfixes are merged into `master` first, then cherry-picked to the current release branch.

## Core Process

```text
feature branch -> PR -> master
master -> releases/M130 -> production
hotfix -> master -> cherry-pick -> releases/M130
```

This model separates two goals:

- `master` maintains fast integration
- production release branch maintains release stability

## Why Not Use Complex Long-Term Branches

Microsoft's article mentions that complex, multi-layered branch structures easily mirror organizational structures, with code integrating upwards to the trunk, then syncing back from the trunk to various branches, eventually forming sustained merge pressure.

The trade-off made by Release Flow is:

- Daily development should enter the trunk as much as possible
- Release rhythm is handled by release branches
- Production hotfixes still originate from the trunk
- Release branches serve the current release and do not accumulate complex history over the long term

## Hotfix Rules

The most valuable takeaway from Release Flow is "master first."

Production fixes are first merged into `master`, then cherry-picked to the current release branch.

This avoids a common incident: fixing an issue in production, but the trunk doesn't have the fix, and the next release brings the issue back.

Only when the fix is no longer applicable on the trunk should one consider fixing it directly on the release branch.

## When to Adopt

Suitable for:

- Mid-to-large Web / SaaS teams
- Trunk requires fast integration
- Production releases are driven by sprints or windows
- Hotfixes need to reach production quickly
- Teams with stable PR, review, and CI processes

Not suitable for:

- Small teams deploying multiple times a day directly
- Need to maintain multiple customer versions long-term
- No clear release rhythm

## Key Takeaways

Release Flow illustrates a very practical combination:

```text
trunk-based integration + release branch deployment + master-first hotfix
```

It is lighter than a full Gitflow, yet more suitable for mid-to-large service teams than pure GitHub Flow.
