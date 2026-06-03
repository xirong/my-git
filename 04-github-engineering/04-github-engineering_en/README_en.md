# GitHub Engineering Governance

English | [中文](../README.md)

This directory is intended for tech leads and team maintainers. Its goal is to configure GitHub from just a code hosting tool into a core part of collaboration, review, CI, release, security, and auditing.

## What to Read First

| Problem to Solve | Recommended Reading |
| --- | --- |
| Want to establish a complete view of repository governance | [GitHub Engineering Governance](github-engineering-governance_en.md) |
| Want to see the enterprise collaboration configuration stack at once | [Enterprise GitHub Workflow Stack](enterprise-github-workflow-stack_en.md) |
| Want to protect main or release branches | [Branch Protection](branch-protection_en.md) |
| Want to unify rules across multiple repositories | [Rulesets](rulesets_en.md) |
| Key directories require owner review | [CODEOWNERS](codeowners_en.md) |
| Too many PRs, main branch breaks frequently on merge | [Merge Queue](merge-queue_en.md) |

## CI and Release

- [GitHub Actions CI](github-actions-ci_en.md)
- [Reusable Workflows](reusable-workflows_en.md)
- [Release Management](release-management_en.md)

Teams with multiple repositories should prioritize Reusable Workflows to avoid configuration drift caused by copying CI setups per repository.
Teams with fixed release windows, hotfixes, and release notes should prioritize Release Management.

## Security and Configuration

- [Security and Secret Scanning](security-and-secret-scanning_en.md)
- [GitOps and Config as Code](gitops-and-config-as-code_en.md)

If the team has already placed configurations, infrastructure, and release strategies into the repository, these two articles should be read together.

## Related Content

- [Team Collaboration](../../03-team-collaboration/03-team-collaboration_en/README_en.md)
- [Template Library](../../08-templates/08-templates_en/README_en.md)
- [Big Tech Engineering Practice Cases](../../10-company-practices/10-company-practices_en/README_en.md)
