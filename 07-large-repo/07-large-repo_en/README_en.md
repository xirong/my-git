# Large Repository Practices

English | [中文](../README.md)

This directory is intended for teams dealing with monorepos, repositories with massive histories, large binary files, mixed multi-service repositories, and high CI clone costs.

## Identify Where the Slowness Originates First

| Symptom | Recommended Reading |
| --- | --- |
| Unsure how to optimize overall | [Large Repository Git Practices](large-repo-git-practices_en.md) |
| Clone is too slow, only need partial history | [Shallow Clone](shallow-clone_en.md) |
| History and blob objects are too large | [Partial Clone](partial-clone_en.md) |
| Only care about specific directories | [Sparse Checkout](sparse-checkout_en.md) |
| Large files must be checked into the repository | [Git LFS](git-lfs_en.md) |
| Parallel development across multiple branches | [Worktree](../../02-daily-workflow/02-daily-workflow_en/worktree_en.md) |
| Repository operations are getting progressively slower | [Repo Maintenance](repo-maintenance_en.md) |

## Architectural Trade-offs

- [Submodule vs Subtree](submodule-vs-subtree_en.md)

When dealing with shared code, cross-repository dependencies, and component reuse, do not merely consider whether a Git command is viable. Also evaluate team collaboration costs, release cadences, permission boundaries, and disaster recovery methods.

## Implementation Sequence

1. First, identify whether the bottleneck is in clone, checkout, status, fetch, CI, or IDE indexing.
2. Then, choose from shallow clone, partial clone, sparse checkout, LFS, or repo maintenance.
3. Optimize for CI and developers' local machines separately.
4. Establish repository rules for large files and generated files.
5. Configure CODEOWNERS and review rules for critical paths.

## Related Content

- [GitHub Engineering Governance](../../04-github-engineering/04-github-engineering_en/README_en.md)
- [Engineering Practice Cases from Top Tech Companies](../../10-company-practices/10-company-practices_en/README_en.md)
- [Microsoft Scalar and Large Repository Git Practices](../../10-company-practices/10-company-practices_en/microsoft-scalar-large-repo_en.md)
- [Uber GitFarm and Git Service Practices](../../10-company-practices/10-company-practices_en/uber-gitfarm_en.md)
