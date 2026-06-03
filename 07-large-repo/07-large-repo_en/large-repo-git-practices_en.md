# Large Repository Git Practices

English | [中文](../large-repo-git-practices.md)

The core issues with large repositories usually do not lie in a specific Git command, but rather in massive histories, excessive files, heavy dependencies, and unclear collaboration boundaries.

## 1. Identify Where the Slowness Originates First

Before optimizing a large repository, break down the problem:

| Symptom | Common Causes | Look Into First |
| --- | --- | --- |
| `git clone` is slow | History and blob objects are too large | partial clone, shallow clone |
| `git checkout` is slow | Too many files in the working directory | sparse checkout, path splitting |
| `git status` is slow | Too many files, too many untracked files | `.gitignore`, fsmonitor, repository maintenance |
| CI code pulling is slow | Each job repeatedly clones the complete repository | shallow clone, partial clone, caching |
| IDE indexing is slow | Checked out irrelevant directories | sparse checkout, open projects by service |
| PR review is slow | Large cross-directory, cross-owner changes | CODEOWNERS, splitting PRs, path responsibilities |

Identify the bottleneck first, then choose a solution. Do not have every team immediately pursue monorepo tool platform adoption.

## 2. Clone Strategies

### Shallow clone

Only pull partial history:

```bash
git clone --depth 1 <url>
```

Suitable for CI and temporary checks; not suitable for scenarios requiring complete historical analysis.

### Partial clone

Reduce object downloads:

```bash
git clone --filter=blob:none <url>
```

See official documentation on [partial clone](https://git-scm.com/docs/partial-clone.html).

### Sparse checkout

Only checkout specific directories:

```bash
git sparse-checkout init --cone
git sparse-checkout set service-a service-b
```

See official documentation on [sparse checkout](https://git-scm.com/docs/sparse-checkout).

## 3. Strategy Selection

| Scenario | Recommended Approach | Considerations |
| --- | --- | --- |
| CI only needs to run a single build | shallow clone | Not suitable for version calculations relying on complete history |
| Developers are only responsible for a few directories | sparse checkout | Directory boundaries must be stable |
| Both repository history and blob objects are very large | partial clone | Need to verify server-side and toolchain support |
| Parallel development across multiple branches | worktree | Each worktree must have a clear branch name |
| Large binary files must be checked into the repository | Git LFS | Requires accompanying permission, storage, and cleanup strategies |
| Multiple teams share one repository | CODEOWNERS | Owner rules should not be so granular that no one can approve |

## 4. Workflow Strategies

- Use `worktree` to handle multiple branches in parallel
- Use CODEOWNERS to express path responsibilities
- Focus PRs by path, avoiding large cross-domain changes
- Generated files, logs, and dumps should not enter the repository

## 5. Large Files

For large files, prioritize using Git LFS.

Do not commit the following contents directly into Git:

- Logs
- Database dumps
- Build artifacts
- Temporary archives
- Large binary intermediate files

## 6. Repository Maintenance

```bash
git maintenance start
git gc
git commit-graph write --reachable
```

Whether specific commands are appropriate needs to be verified against the team's environment and Git version.

## 7. Enterprise Practice References

The inspiration from [Microsoft Scalar and Large Repository Git Practices](../../10-company-practices/10-company-practices_en/microsoft-scalar-large-repo_en.md) is that optimizing large repositories usually requires a combination of partial clone, sparse checkout, background maintenance, file system monitoring, and build system capabilities.

Do not only optimize clone. Developers more commonly encounter issues with `status`, `fetch`, `checkout`, IDE indexing, and build speeds in their daily work.

Newer Git versions are also continuously improving the large repository experience, especially in areas like reftable, partial clone, sparse checkout, and config-based hooks, see [Git Version Upgrade Notes](../../09-resources/09-resources_en/git-version-upgrade-notes_en.md).

[Uber GitFarm and Git Service Practices](../../10-company-practices/10-company-practices_en/uber-gitfarm_en.md) further reminds us that when a monorepo grows to a certain scale, Git costs will spread from developers' local machines to automated systems like CI, builds, releases, and static analysis. At this point, optimization goals include personal clone speeds as well as the costs of repeated clones and checkouts by automated systems.

## Further Reading

- [Git partial clone](https://git-scm.com/docs/partial-clone.html)
- [Git sparse checkout](https://git-scm.com/docs/sparse-checkout)
- [git worktree](https://git-scm.com/docs/git-worktree)
- [Git LFS](https://git-lfs.com)
- [Microsoft Scalar and Large Repository Git Practices](../../10-company-practices/10-company-practices_en/microsoft-scalar-large-repo_en.md)
- [Meta Sapling and Stacked Commits Practices](../../10-company-practices/10-company-practices_en/meta-sapling-stacked-commits_en.md)
- [Uber GitFarm and Git Service Practices](../../10-company-practices/10-company-practices_en/uber-gitfarm_en.md)
- [Git Version Upgrade Notes](../../09-resources/09-resources_en/git-version-upgrade-notes_en.md)
- [Recommended Reading Index](../../09-resources/09-resources_en/recommended-reading_en.md)
