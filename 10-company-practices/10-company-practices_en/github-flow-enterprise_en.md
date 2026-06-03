# GitHub Flow Enterprise Practice

English | [中文](../github-flow-enterprise.md)

Original links:

- [GitHub Flow](https://docs.github.com/en/get-started/using-github/github-flow)
- [About protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
- [About rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets)
- [About code owners](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)
- [Managing a merge queue](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue)

## 1. The Basic Form of GitHub Flow

The basic path of GitHub Flow is very simple:

```text
main -> branch -> pull request -> review -> merge -> deploy
```

Its value lies in its low learning curve, making it naturally suited for PRs, review, status checks, and continuous deployment.

However, enterprise teams cannot stop at just "creating branches, submitting PRs, and merging."

## 2. What it Looks Like After Enterprise Adoption

GitHub Flow in enterprise teams usually adds these capabilities:

| Capability | Problem Solved |
| --- | --- |
| Protected branches | Protects `main`, preventing direct push, force push, and unchecked merges |
| CODEOWNERS | Automatically finds owners for review based on file paths |
| Rulesets | Unifies rules at the repository or organization level |
| Required status checks | CI, lint, and security checks must pass |
| Merge Queue | Validates the combined results after PRs are queued |
| Actions | Automates build, testing, and release |
| Security features | Shifts left to discover secrets, dependencies, and code security issues |

At this point, GitHub Flow has upgraded from a lightweight process to a platform-based collaboration pipeline.

## 3. Relationship with Trunk-Based Development

GitHub Flow acts more like a workflow expression on a platform.

Trunk-Based Development acts more like an engineering principle at the organizational level.

When GitHub Flow meets these conditions, it is very close to trunk-based:

- Short branch lifecycle
- PRs are sufficiently small
- Main branch is continuously deployable
- Required CI is stable
- Feature flags manage unfinished features
- Merge Queue protects merge order
- Revert prioritized when problems occur

## 4. When to Adopt

Suitable for:

- Web / SaaS services
- Documentation sites and platform configuration repositories
- Internal tool repositories
- Business services with relatively high release frequencies
- Small to medium-sized teams with existing basic CI

Requires strengthening before use:

- Teams with very high PR throughput, requiring Merge Queue
- Multiple teams sharing a repository, requiring CODEOWNERS
- Multi-repository organizations, requiring Rulesets and reusable workflows
- Repositories with high security requirements, requiring code scanning, secret scanning, and Dependabot

## 5. Common Misconceptions

### Treating GitHub Flow as a rule-less process

GitHub Flow itself is very lightweight, and rules need to be supplemented by GitHub platform capabilities.

### Lack of a release closed-loop after merging

GitHub Flow emphasizes that the main branch is deployable, but enterprise teams also need to ensure tags, release notes, deployments, verifications, and rollbacks are traceable.

### Failing to handle large PRs

GitHub Flow relies on reviewers being able to quickly understand the diff. Large features should be broken down into stacked PRs or multiple small PRs.

## 6. Key Takeaways

When writing about GitHub Flow, do not just write "the process is simple."

A more valuable approach is to place it within the enterprise configuration stack:

```text
short branch
-> PR
-> CODEOWNERS
-> CI
-> security checks
-> Merge Queue
-> protected main
-> release
```
