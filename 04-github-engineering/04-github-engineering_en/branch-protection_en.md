# Branch Protection

English | [中文](../branch-protection.md)

Branch protection is used to safeguard critical branches, preventing unreviewed, unverified, or high-risk operations from entering the mainline directly.

For team repositories, branches like `main`, `master`, and `release/*` should be managed as public assets.

## Recommended Configuration

- Require a pull request before merging
- Require approvals
- Require status checks before merging
- Require conversation resolution before merging
- Require linear history when your team wants easier revert
- Block force pushes on main branches
- Block branch deletion on main branches

## Branches Recommended for Protection

- `main`
- `master`
- `develop`
- `release/*`
- `hotfix/*`

## Minimal Configuration

Small teams can start by enabling:

1. Require pull request before merging
2. Require status checks before merging
3. Block force pushes
4. Block deletions

This helps prevent the most common accidents first:

- Pushing directly to the main branch
- Merging despite red CI (failed checks)
- Overwriting remote history via force push
- Accidental deletion of critical branches

## Configuration for Growing Teams

As the team grows, also enable:

- Require approvals
- Dismiss stale pull request approvals when new commits are pushed
- Require review from Code Owners
- Require conversation resolution before merging

These rules link review, CODEOWNERS, and CI into a complete merge workflow.

## Common Pitfalls

### 1. Only protecting main

If the team uses `release/*` or `hotfix/*`, these branches should also be protected.

### 2. Adding rules but ignoring CI stability

Required checks must be stable. Flaky tests will cause the team to start bypassing rules.

### 3. Administrators bypassing rules long-term

Administrator bypasses should only be used in extremely rare emergency scenarios, and records should be kept.

## Further Reading

- [GitHub Docs: Protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
- [GitHub Docs: Required status checks](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches#require-status-checks-before-merging)
- [CODEOWNERS](codeowners_en.md)
- [GitHub Engineering Governance](github-engineering-governance_en.md)
