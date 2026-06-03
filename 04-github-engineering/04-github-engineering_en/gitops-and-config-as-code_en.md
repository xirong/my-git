# GitOps and Config as Code

English | [中文](../gitops-and-config-as-code.md)

Original Links:

- [Airbnb: Safeguarding Dynamic Configuration Changes at Scale](https://airbnb.tech/infrastructure/safeguarding-dynamic-configuration-changes-at-scale/)
- [Spotify Fleet Management Part 2: The Path to Declarative Infrastructure](https://engineering.atspotify.com/2023/05/fleet-management-at-spotify-part-2-the-path-to-declarative-infrastructure)
- [Spotify Fleet Management Part 3: Fleet-wide Refactoring](https://engineering.atspotify.com/2023/05/fleet-management-at-spotify-part-3-fleet-wide-refactoring)

The boundaries of Git have expanded from code to configurations, infrastructure, release, and organizational processes.

For engineering teams, Git not only stores source code but also records the change history of configurations, infrastructure, and release strategies.

## 1. Why Configurations Should Enter Git

If configuration changes only exist in an admin backend, these problems easily arise:

- Unclear who made the change
- Unclear why it was changed
- Unclear if the change was Reviewed
- Unclear how to roll back if issues occur
- Unclear which services are affected

After incorporating configurations into the Git workflow, existing capabilities can be reused:

- PR
- Review
- CODEOWNERS
- CI validation
- Release records
- rollback
- Change auditing

## 2. Inspiration from Airbnb Sitar

Configuration management practices like Airbnb Sitar show that dynamic configurations also require engineering governance.

Key point: After configuration files enter the repository, configuration changes must also go through:

```text
PR -> validation -> review -> staged rollout -> monitoring -> rollback
```

This is very similar to code releases.

## 3. Inspiration from Spotify Declarative Infrastructure

Spotify manages infrastructure configurations alongside source code, gaining peer review and audit trails through a GitOps workflow.

Its key points:

- Infrastructure configurations enter the repository
- Changes pass through PR review
- CI performs a dry run or lightweight validation
- Runtime status can be queried by the platform
- A break-glass mechanism is retained for emergencies

## 4. Automated Changes Should Also Go Through PRs

Cases like Spotify fleet-wide refactoring remind us that automated refactoring cannot bypass collaboration workflows.

Large-scale automated changes should:

- Automatically create PRs
- Pass checks
- Merge with rate limits
- Merge during working hours
- Leave audit records
- Be able to stop quickly if issues arise

This also has direct implications for the AI era. AI-generated changes, batch changes from local scripts, and automatic platform remediations should all return to PRs, Reviews, CI, and release records.

## 5. Implementation Recommendations for Teams

1. Incorporate high-risk configurations into Git management first
2. Enable CODEOWNERS in the configuration repository
3. Configuration changes must go through PRs
4. CI validates formats, semantics, and risks
5. Release systems should track configuration versions
6. Retain emergency change paths, but ensure there are audit records

## 6. Suitable Scenarios

Suitable for:

- Feature toggles
- Dynamic configurations
- Infrastructure configurations
- Kubernetes manifest
- Permissions configuration
- Release strategies

Unsuitable for:

- High-frequency real-time operational data
- Temporary states that must take effect in milliseconds
- Sensitive values that cannot be exposed to the repository permissions system
