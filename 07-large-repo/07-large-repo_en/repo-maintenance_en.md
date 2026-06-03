# Repo Maintenance

English | [中文](../repo-maintenance.md)

Large repositories require periodic maintenance.

Repository maintenance is not just about running `git gc`; it also includes managing file boundaries, history volume, branch cleanup, dependency governance, and document timeliness.

## Checklist

- [ ] Are there any large files mistakenly committed?
- [ ] Are there any generated files checked into the repository?
- [ ] Are there any long-standing unused branches?
- [ ] Are there any broken submodules?
- [ ] Are there any outdated documents and links?
- [ ] Are there any leaked secrets?
- [ ] Are there any long-unmaintained CI jobs?

## Local Object Inspection

```bash
git count-objects -vH
```

This command displays object counts and sizes, useful for determining if the repository needs cleanup.

## Local Maintenance Commands

```bash
git gc
git maintenance start
git commit-graph write --reachable
```

Whether these commands are appropriate needs to be verified against the team's environment, Git version, and repository scale.

## Branch Cleanup

View merged branches:

```bash
git branch --merged
```

Delete local branch:

```bash
git branch -d feature/old-task
```

Prune deleted remote branch references:

```bash
git fetch --prune
```

## Large File Governance

Periodic checks:

- Are there files exceeding the team's threshold?
- Are there logs, dumps, zips, or build artifacts?
- Should they be migrated to Git LFS?
- Is history cleanup necessary?

## Document Maintenance

This repository itself also needs maintenance:

- Are old links broken?
- Is older advice outdated?
- Is there more authoritative official documentation available?
- Is the document content consistent with current Git/GitHub behaviors?

## Further Reading

- [git maintenance official documentation](https://git-scm.com/docs/git-maintenance)
- [git gc official documentation](https://git-scm.com/docs/git-gc)
- [git commit-graph official documentation](https://git-scm.com/docs/git-commit-graph)
- [Large Repository Git Practices](large-repo-git-practices_en.md)
