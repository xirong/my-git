# Enterprise GitHub Workflow Stack

English | [中文](../enterprise-github-workflow-stack.md)

Original Links:

- [GitHub Flow](https://docs.github.com/en/get-started/using-github/github-flow)
- [About protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
- [About rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets)
- [About code owners](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)
- [Managing a merge queue](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue)
- [Understanding GitHub Actions](https://docs.github.com/en/actions/about-github-actions/understanding-github-actions)
- [About code scanning](https://docs.github.com/en/code-security/concepts/code-scanning/about-code-scanning)
- [About Dependabot version updates](https://docs.github.com/en/code-security/dependabot/dependabot-version-updates/about-dependabot-version-updates)
- [About secret scanning](https://docs.github.com/en/code-security/secret-scanning/introduction/about-secret-scanning)
- [Gerrit Code Review: Access Controls](https://gerrit-review.googlesource.com/Documentation/access-control.html)

## 1. Default Configuration Stack

The GitHub collaboration configuration of a mature team can be built along this pipeline:

```text
Issue / ADR / Ticket
-> short-lived branch
-> draft PR
-> CODEOWNERS routing
-> CI
-> security checks
-> required review
-> merge queue
-> protected main
-> tag / release
-> deploy
```

This configuration fits GitHub Flow and can also support trunk-based style team collaboration.

## 2. Six Types of Checkpoints

### Branch Checkpoints

Goal: Avoid developing directly on the main branch.

Recommendations:

- All changes go through short-lived branches
- Branch names are linked to requirements, Issues, or tasks
- Direct pushes to the main branch by regular members are prohibited

### Review Checkpoints

Goal: Involve those who understand the corresponding code in the review.

Recommendations:

- Configure CODEOWNERS
- PR templates require filling out risks and validations
- High-risk directories require owner approval
- AI Review is only used as an auxiliary scan

### Policy Checkpoints

Goal: Solidify team rules into the platform.

Recommendations:

- Protected branches protect `main`
- Rulesets unify organizational-level rules
- Deleting and force pushing critical branches are prohibited
- Required checks names must remain stable

Branch Protection is more suitable for starting with single repositories and a few critical branches. Rulesets are better suited for organizational levels, multi-repositories, rule superposition, and audit visibility.

### Security Checkpoints

Goal: Shift left common security issues to the PR and push stages.

Recommendations:

- Secret scanning
- Push protection
- Dependabot
- Code scanning
- Dependency review

Dependabot can turn dependency and GitHub Actions version upgrades into PRs. Code scanning is responsible for finding code security issues, and Secret scanning is responsible for detecting credential leak risks. These three types of checks should be tied to the PR workflow, rather than just acting as post-facto scans.

### Integration Checkpoints

Goal: Verify the combined result of the main branch before merging.

Recommendations:

- Required CI checks
- Merge Queue
- `merge_group` events trigger CI
- Address flaky tests

### Release Checkpoints

Goal: Ensure deployed versions are trackable, explainable, and can be rolled back.

Recommendations:

- tag
- GitHub Release
- release note
- rollback plan
- deploy verification

## 3. The Relationship Between GitHub Flow and Trunk-Based Development

GitHub Flow is a lightweight collaboration path on the GitHub platform. Its core is short branches, PRs, Reviews, and merging into the default branch.

Trunk-Based Development is a stronger organizational principle that emphasizes high-frequency integration around the trunk, extremely short branch lifecycles, and keeping the trunk continuously releasable.

When a team adds the following to GitHub Flow:

- Required CI
- CODEOWNERS
- Rulesets
- Merge Queue
- feature flag
- release from main

It comes very close to the enterprise implementation form of trunk-based development.

## 4. Rollout Sequence

Do not turn on all capabilities at once.

Recommended sequence:

1. PR templates
2. Basic CI
3. Branch protection
4. CODEOWNERS
5. Rulesets
6. Secret scanning and Dependabot
7. Code scanning
8. Merge Queue
9. Release notes and deployment records

## 5. Differences from Gerrit

GitHub acts more like a unified development platform. Its strengths are the integration of PRs, Actions, security scanning, Issues, Releases, and Rulesets.

Gerrit is more of a review hub. Its strengths lie in group-level permissions, label voting, Submit permissions, and finer-grained review semantics.

If the team needs an exceptionally strong Review permission model, refer to [Gerrit Code Review Governance Reference](../../09-resources/09-resources_en/gerrit-code-review-governance_en.md). If the team wants to build a unified collaboration platform around the GitHub ecosystem, prioritize GitHub's native capability combinations.

## 6. Common Pitfalls

### Only protecting main

If the team has `release/*`, `hotfix/*`, or production tags, rules should be designed for them as well.

### Adding rules but ignoring speed

The slower the CI, the more inclined developers are to bypass rules.

### Treating security scans as the end result

Scanning merely uncovers issues; it also requires owners, processing SLAs, and escalation paths.

### Merge Queue enabled but CI unchanged

When using GitHub Actions, critical workflows must respond to `merge_group`:

```yaml
on:
  pull_request:
  merge_group:
```

## 7. Implications for This Repository

GitHub engineering governance should not be written as a tool checklist.

It is better written as a collaboration pipeline from proposing a change to completing a release, so readers understand which risk point each tool addresses.
