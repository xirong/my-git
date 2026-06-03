# Team Git Workflow Guide

English | [中文](../team-git-workflow-guide.md)

No Git workflow is universally correct.

Every workflow is a trade-off among speed, safety, release frequency, team size, and product complexity.

## 1. Selection Matrix

| Team / Product | Recommended Workflow | Rationale |
| --- | --- | --- |
| Small team web products | GitHub Flow | Short branches, fast merges, frequent releases |
| High-frequency backend services | Trunk-Based Development | Stable trunk, fast CI feedback, clean rollbacks |
| Medium-to-large business teams | Feature Branch + Protected Main | Balances parallel development with main branch stability |
| Open-source projects | Fork + Pull Request | Reduces write-access risk from external contributors |
| Multi-version delivery products | Release Branch | Must maintain multiple live versions simultaneously |
| Multi-environment SaaS / internal enterprise platforms | GitLab Flow | Merge and deploy frequencies differ; needs `production` / `stable` branches |
| Mobile / desktop clients | Release Branch + Hotfix | Long release cycles, fragmented live versions |
| Legacy system maintenance | Conservative Branch Strategy | Infrequent changes, high risk, stability first |

## 2. GitHub Flow

### Suitable For

- Small teams
- Web services
- Frequent releases
- Comprehensive CI
- Manageable rollback costs

### Process

```text
main -> feature branch -> pull request -> review -> CI -> merge -> deploy
```

### Team Rules

- `main` is always deployable
- All changes go through PRs
- PRs should be as small as possible
- Must pass CI before merging
- Prioritize reverting when issues occur

## 3. Trunk-Based Development

### Suitable For

- Mature automated testing
- Frequent trunk deployments
- Strong engineering discipline across the team
- Feature flags to gate unfinished work

### Process

```text
short-lived branch -> main -> CI -> deploy
```

### Risks

- Flaky CI slows the whole team
- Without feature flags, incomplete features leak into production
- Large teams need tighter code ownership and review standards

## 3.1 GitHub Flow vs. Trunk-Based Development

GitHub Flow is a lightweight process built around GitHub's platform: short branches, PRs, reviews, and merging into the default branch.

Trunk-Based Development is an organizational principle: branch lifetimes are measured in hours, the team integrates continuously against the trunk, and the trunk stays deployable at all times.

Add required CI, CODEOWNERS, Rulesets, Merge Queue, feature flags, and release-from-main to a GitHub Flow setup, and you arrive at the enterprise implementation of trunk-based development.

## 4. Feature Branch + Protected Main

This is the practical default for most medium-to-large business teams.

### Recommended Rules

- Protect `main` or `master`
- All changes go through PRs
- Required status checks must pass before merging
- At least one reviewer approval required
- Configure CODEOWNERS for critical directories
- Block force-pushes to the main branch for regular members

GitHub branch protection rules can enforce reviews, status checks, linear history, merge queues, and more. See [protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches) in the GitHub docs.

## 5. Gitflow

Gitflow works well for products with a defined release cadence: desktop clients, SDKs, and enterprise delivery products.

### Suitable For

- Long-term maintenance of multiple versions
- Explicit release and hotfix branches
- Fixed release windows
- Live versions that cannot be deployed on demand

### Avoid For

- High-frequency web services
- Small teams iterating quickly
- Systems with mature CI/CD where the trunk ships anytime

Gitflow's branch model has historical value, but applying it across every team adds complexity without proportional benefit.

## 6. GitLab Flow

GitLab Flow fits teams where merge frequency and release frequency do not align.

It keeps the lightweight collaboration of feature branches and merge requests, and adds `production` and `stable/*` branches to represent live state and stable version lines.

### Suitable For

- Web / SaaS teams that need to distinguish "merged" from "live"
- Internal enterprise platforms with multi-environment release pipelines
- SDKs, clients, and private-deployment products that need stable version branches
- Teams that find GitHub Flow too minimal and Gitflow too heavy

See [GitLab Flow](gitlab-flow_en.md) for details.

## 7. Fork + Pull Request

### Suitable For

- Open-source projects
- Many external contributors
- Repositories where granting write access to all contributors is impractical

### Process

```text
fork -> branch -> commit -> pull request -> maintainer review -> merge
```

### Maintainer Responsibilities

- Publish clear contribution guidelines
- Provide Issue and PR templates
- Label beginner-friendly tasks
- Use CI to reduce the review burden

## 8. Release Branch

### Suitable For

- Mobile
- Clients
- SDKs
- Private deployment products
- Products maintaining multiple parallel versions

### Basic Process

```text
main -> release/1.8 -> bugfix -> tag -> hotfix -> back merge
```

### Key Rules

- Release branches accept stability fixes only
- New features go into the trunk
- Hotfixes must be backported to the trunk
- Tag every published release

Microsoft Release Flow offers a proven combination of both approaches: the trunk carries day-to-day development, release branches are cut per sprint or release window, and fixes flow back to the trunk. See [Microsoft Release Flow](../../10-company-practices/10-company-practices_en/microsoft-release-flow_en.md) for details.

## 9. Common Anti-Patterns

### Long-Lived Feature Branches

Problem: Merge risk compounds over time, and trunk feedback stops being useful.

Recommendation: Break work into smaller tasks, merge early, and hide unfinished work behind feature flags.

### Direct Pushes to Main

Problem: The main branch can break at any time, and accountability is unclear.

Recommendation: Enable branch protection, require PR reviews, and make CI mandatory.

### Oversized PRs

Problem: Reviews become a rubber stamp.

Recommendation: One PR, one problem. Keep refactoring and behavioral changes in separate PRs.

### Treating One Workflow as Universal

Problem: The team's actual constraints get ignored.

Recommendation: Match the workflow to your release cadence, team size, and risk tolerance.

## 10. Enterprise Practice References

| Practice | Key Takeaways |
| --- | --- |
| [Alibaba AoneFlow](../../10-company-practices/10-company-practices_en/alibaba-aoneflow_en.md) | Release branches define the release scope, enabling flexible feature inclusion and removal |
| [Tencent Gitflow Branching Practice](../../10-company-practices/10-company-practices_en/tencent-gitflow_en.md) | Well-suited for fixed-version release cycles with dedicated release testing and hotfix backporting |
| [ByteDance Git Workflow](../../10-company-practices/10-company-practices_en/bytedance-git-workflow_en.md) | Unifies branches, permissions, reviews, CI, and releases into a single engineering platform |
| [Google Trunk-Based Development](../../10-company-practices/10-company-practices_en/google-trunk-based-development_en.md) | Short branches, fast CI, and small commits power collaboration at massive scale |
| [Microsoft Release Flow](../../10-company-practices/10-company-practices_en/microsoft-release-flow_en.md) | Trunk-based development paired with release branches, designed for teams with fixed release windows |
| [Meta Sapling](../../10-company-practices/10-company-practices_en/meta-sapling-stacked-commits_en.md) | Stacked commits express large features as a chain of small, reviewable changes |

Before borrowing from any of these, assess your own release frequency, team size, testing maturity, and ability to roll back in production.

## 11. Migration Strategy

Moving from an old process to a new one works best as a sequence of small, deliberate steps — not a big-bang switchover.

Recommended sequence:

1. Require all changes to go through PRs.
2. Enable basic CI.
3. Enable branch protection.
4. Introduce review requirements.
5. Configure CODEOWNERS.
6. Add merge queues once PR volume makes it worthwhile.

## Extended Reading

- [Atlassian Git tutorials](https://www.atlassian.com/git)
- [GitHub Flow](https://docs.github.com/en/get-started/using-github/github-flow)
- [GitLab Flow](gitlab-flow_en.md)
- [Trunk Based Development](https://trunkbaseddevelopment.com)
- [Feature Flags](https://trunkbaseddevelopment.com/feature-flags/)
- [Tech Giant Engineering Practice Index](../../10-company-practices/10-company-practices_en/README_en.md)
- [Enterprise GitHub Collaboration Stack](../../04-github-engineering/04-github-engineering_en/enterprise-github-workflow-stack_en.md)
- [GitHub protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
- [GitHub rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets)
- [Recommended Reading Index](../../09-resources/09-resources_en/recommended-reading_en.md)
