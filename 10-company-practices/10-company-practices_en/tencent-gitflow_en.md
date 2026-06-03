# Tencent Cloud Community Gitflow Branch Convention Practice

English | [中文](../tencent-gitflow.md)

Original links:

- [Git Branch Management and Workflow Conventions: Specific Conventions](https://cloud.tencent.com/developer/article/1110910)

## 1. What Problems Do Such Conventions Solve

The real problem for many teams is often unclear branch semantics:

- Is `master` really the production version?
- Does `develop` contain unreleased code?
- Can release branches continue to accept new features?
- Where should a hotfix be backported after it's resolved?
- When should feature branches be deleted?

The value of Gitflow lies in clarifying these roles. It is especially suitable for teams with explicit release cycles, fixed deployment windows, and longer testing periods.

## 2. Branch Roles

| Branch | Role |
| --- | --- |
| `master` / `main` | Stays strictly aligned with the live production version |
| `develop` | Daily development integration branch |
| `feature/*` | Feature development branches |
| `release/*` | Testing and release preparation for a specific version |
| `hotfix/*` | Emergency fixes for production issues |

The basic rule is: Do not modify the mainline and development integration branch directly; features, releases, and fixes are all handled through their respective branches.

## 3. Regular Development Process

```text
develop -> feature/x -> develop -> release/1.2.0 -> main -> tag
```

Operational meaning:

1. Create `feature/x` from `develop`
2. Merge back to `develop` once the feature is complete
3. When a batch of features is ready for QA, create `release/*` from `develop`
4. Issues found during the testing phase are fixed directly on `release/*`
5. After the release is complete, `release/*` is merged into `main` and tagged
6. Simultaneously, backport fixes from `release/*` into `develop`

## 4. Hotfix Process

Production issues take priority by creating a `hotfix/*` from the production baseline:

```text
main -> hotfix/1.2.1 -> main -> tag
                    \-> develop
```

Key points:

- Hotfixes only perform minimal repairs
- A tag must be created after the release
- Fixes must be backported to `develop`
- If an active release branch still exists, evaluate whether synchronization is also needed there

## 5. Common Special Cases

### `develop` already has unreleased code, but a small feature needs urgent release

In this case, do not branch directly off `develop`, as it might carry over content that shouldn't be released.

A safer approach is to create a branch from `main` or the production tag, release it like a hotfix or emergency release, and then synchronize the changes back to `develop`.

### Two features discover a hard dependency halfway through development

It is best to identify dependencies early during the requirements breakdown phase.

If they are already separated, the team needs to quickly decide whether to merge them into a single feature branch or establish a common base branch, avoiding long-term, mutual cherry-picking between the two branches.

### Boundaries of rebase

Rebase can be used for cleaning up commits locally.

Once a branch has been published to the shared repository—especially if others have already based continued development on it—do not arbitrarily rebase and force push.

## 6. When to Adopt

Suitable for:

- Client apps, SDKs, enterprise delivery products
- Needs dedicated release and testing cycles
- Needs to maintain multiple version lines
- Production hotfixes require explicit paths

Not suitable for:

- Web services deploying multiple times a day
- Very small teams with very lightweight releases
- Mature CI/CD where the mainline is deployable at any time

## 7. Key Takeaways

The focus of Gitflow is constraints:

- Which branches represent the production truth
- Which branches can accept new features
- Which branches can only fix bugs
- How changes are backported after a release
- How tags correspond to production versions

If a team adopts Gitflow, it is best to write these rules into the team conventions and use branch protection, PR templates, and CI checks to reduce human omissions.
