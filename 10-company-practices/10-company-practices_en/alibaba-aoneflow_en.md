# Alibaba AoneFlow Branch Management Practice

English | [中文](../alibaba-aoneflow.md)

Original links:

- [How Do We Manage Code Branches at Alibaba?](https://www.alibabacloud.com/blog/how-do-we-manage-code-branches-at-alibaba_593834)
- [Evolved Branch Management with AoneFlow](https://www.alibabacloud.com/blog/evolved-branch-management-with-aoneflow_594903)

## 1. What Problem Does AoneFlow Solve

Traditional Gitflow has clear branch roles, but it involves many branches and a heavy process. After long-term use, it is easy to have multiple divergences across `develop`, `release`, and `main`, leading to high backporting costs.

Trunk-Based Development is lightweight enough, but it requires relatively mature CI, test coverage, feature flags, and team discipline. For teams with multiple features running in parallel and frequently adjusting release scopes, adopting trunk-based development directly can be stressful.

AoneFlow aims to address this middle ground:

- Multiple features being developed in parallel
- Each release requires a specific combination of features
- A feature could be delayed, dropped, or replaced at any time
- `release/*` branches need to align with testing, staging, and production environments
- The team wants to reduce the branch complexity of Gitflow

## 2. Core Branch Model

AoneFlow primarily maintains three types of branches:

| Branch | Role |
| --- | --- |
| `master` / `main` | The mainline of released code, using tags to mark production versions |
| `feature/*` | A feature branch corresponding to each requirement or task |
| `release/*` | A feature combination branch intended for a specific environment or a specific release |

Its key aspect is that `release/*` can be created from the mainline, and then a group of feature branches are merged into it according to the release plan, without needing to depend on `develop` for long-term evolution.

```text
main
  \-> feature/a
  \-> feature/b
  \-> feature/c

main -> release/test  <- merge feature/a + feature/b
main -> release/prod  <- merge feature/a
```

The advantage of this approach is that the release branch expresses "which features are to be released this time," rather than just "what code is currently on the integration branch."

## 3. Three Key Rules

### Rule 1: Create a feature branch from the mainline before development

For every task, first create a `feature/*` branch from the mainline. Developers should not modify the mainline directly.

This naturally makes each requirement an optional, removable, and reviewable unit.

### Rule 2: Generate release branches by combining features

When testing or releasing is needed, create a `release/*` branch from the mainline, and then merge the features to be released this time one by one.

If a feature is temporarily pulled from the release, the release branch can be regenerated, merging only the remaining features, reducing the risks of manual rollbacks and cherry-picking code.

### Rule 3: Merge back to the mainline and clean up branches after release

When a specific release branch has completed its production deployment, merge it into the mainline, create a tag, and delete the released feature branches.

In this way, the mainline still represents the fact of what has been released, and the tag represents a traceable production version.

## 4. Practices Worth Adopting

### Using release branches to represent environments

You can bind `release/test`, `release/staging`, and `release/prod` to deployment environments, making the source of code for each environment clear and traceable.

This is suitable for the common scenario in business systems: "test a batch, stage a batch, release a batch to production."

### Using platforms to track the relationship between features and releases

The complexity of AoneFlow lies not in Git commands, but in "which features were merged into which release branch."

If relying on human memory, mistakes are easy to make. The team needs to at least use Issues, PRs, project management platforms, or release tickets to record these relationships.

### Keeping builds reproducible

The original text specifically emphasizes that production branches must not rely on snapshot packages that only exist locally or in temporary environments.

This is critical because release branches are often reconstructed. If dependencies are not reproducible, the reconstructed package might be inconsistent with the previous one.

## 5. When to Adopt

Suitable for:

- Multiple features in parallel
- Release scope changes frequently
- Multiple environments like testing, staging, and production
- Need to combine features for release on demand
- Do not want to maintain a long-term `develop` branch

Not suitable for:

- Small teams with high-frequency Web services
- Weak CI and few tests
- No release platform or release ticket records
- The team cannot maintain the mapping between features and releases

## 6. Key Takeaways

AoneFlow's reminder to teams is:

- Branch strategy should serve the release strategy
- Release branches should ideally express a clear release scope
- Features should remain optional, removable, and reviewable
- Branch relationships require tools or processes to track
- Return to the mainline as source of truth promptly after release completion

If a team is at a stage where Gitflow feels too heavy and trunk-based development feels too aggressive, they can refer to AoneFlow to create a lightweight version.
