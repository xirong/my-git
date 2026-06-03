# Release Management

English | [中文](../release-management.md)

Release management must ensure that versions are trackable, changes are explainable, and issues can be rolled back.

Git itself records version history, while GitHub Release, tags, changelogs, and CI/CD turn this history into deliverable version assets.

## Recommended Artifacts

- tag
- release note
- changelog
- rollback plan
- migration note
- verification note

## Release Process

```text
merge -> tag -> release notes -> deploy -> verify -> announce
```

## Tag Conventions

Semantic versioning is recommended:

```text
v2.0.0
v2.0.1
v2.1.0
```

Common meanings:

- major: Incompatible changes
- minor: Backwards-compatible new features
- patch: Backwards-compatible fixes

## What Should Be in a Release Note

Include at least:

- Key changes
- Bug fixes
- Breaking changes
- Upgrade instructions
- Rollback procedures
- Contributors

See [Release Note Template](../../08-templates/08-templates_en/release-note-template_en.md) for a template.

## Hotfix Releases

Hotfixes only address emergency issues in the production environment.

Principles:

- Small diff
- Do not mix in refactoring
- Clear verification
- Rollback plan in place
- Backport to the trunk after release

For the process, see [Hotfix Process](../../08-templates/08-templates_en/hotfix-process_en.md).

## Release Pipeline

Public practices like Netflix Spinnaker remind us that for many teams, the real risk is concentrated in the release process, of which the branching model is only a part.

Once a team has PRs, CI, and branch protection, the next things to add are:

- Linking releases to commits or tags
- Release records include release notes
- Clear checkpoints before production release
- Manual approval points for high-risk releases
- Trackable verification results post-release
- Clear rollback paths

See [Netflix Spinnaker and Release Pipeline Practices](../../10-company-practices/10-company-practices_en/netflix-spinnaker-release_en.md) for details.

## Release Flow and Daily Deployment

The Microsoft Release Flow experience is suited for teams with fixed sprints and fixed release windows:

- Daily development enters the trunk
- Cut a release branch from the trunk before release
- The release branch only accepts stability fixes
- Sync back to the trunk after fixes are completed
- Trace release versions using tags and release notes

Slack's publicly shared deployment practices place more emphasis on "continuous small-batch releases": breaking down risks into daily deployments through automated checks, deployment queues, observability, and rollback paths.

These two types of practices differ in direction, but their common ground is clear: release management cannot solely rely on branch naming; it must string together verifications, approval points, release records, monitoring, and rollback paths.

If the team has fixed release windows, Microsoft Release Flow can be prioritized as a reference. If the team deploys frequently, Slack Deploys and Netflix Spinnaker can be prioritized. For more case comparisons, see [Big Tech Engineering Practice Decision Map](../../10-company-practices/10-company-practices_en/company-practices-decision-map_en.md).

## Further Reading

- [GitHub Docs: Managing releases in a repository](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository)
- [Semantic Versioning](https://semver.org/)
- [Netflix Spinnaker and Release Pipeline Practices](../../10-company-practices/10-company-practices_en/netflix-spinnaker-release_en.md)
- [Microsoft Release Flow](../../10-company-practices/10-company-practices_en/microsoft-release-flow_en.md)
- [Slack Deploys Practices](../../10-company-practices/10-company-practices_en/slack-deploys_en.md)
- [Big Tech Engineering Practice Decision Map](../../10-company-practices/10-company-practices_en/company-practices-decision-map_en.md)
- [GitHub Engineering Governance](github-engineering-governance_en.md)
- [Recommended Reading Index](../../09-resources/09-resources_en/recommended-reading_en.md)
