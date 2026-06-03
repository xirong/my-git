# GitLab Flow

English | [中文](../gitlab-flow.md)

Original links:

- [What is GitLab Flow?](https://about.gitlab.com/topics/version-control/what-is-gitlab-flow/)
- [GitLab Flow](https://docs.gitlab.com/topics/gitlab_flow/)

GitLab Flow sits between GitHub Flow and Gitflow.

It retains the lightweight collaboration style of feature branches and merge requests while introducing concepts like production branches and stable branches, making it suitable for teams needing environment, production, or stable release branches.

## What Problems Does It Solve?

GitHub Flow is very lightweight and suited for teams whose main branch is always deployable.

Gitflow has comprehensive branch roles but is too heavy for many Web / SaaS teams.

GitLab Flow fits the middle ground:

- Daily development still uses feature branches
- Review via merge requests prior to merging
- Production deployments can be bound to the production branch
- Multi-version delivery can utilize stable branches
- Issues, MRs, environments, and release records can be linked together

## Common Forms

### Production branch

```text
feature/* -> main -> production
```

`main` receives daily integrations, while `production` represents the state already deployed to production.

Suitable for:

- Production release frequency is lower than merge frequency
- Needing clear distinction between "merged" and "live"
- Release processes requiring additional validation

### Stable branch

```text
main -> stable/1.0
main -> stable/1.1
```

Stable branches represent version lines requiring long-term maintenance.

Suitable for:

- Clients
- SDKs
- Enterprise delivery products
- Private deployments

## Differences from Other Models

| Model | Core Features |
| --- | --- |
| GitHub Flow | Lightest, centers around default branch and PRs |
| GitLab Flow | Adds production / stable branches on top of lightweight MR flows |
| Gitflow | Most comprehensive branch roles, heaviest process |
| Trunk-Based Development | Emphasizes frequent mainline integration, short branches, and rapid validation |

## Which Teams Is It Suitable For?

Suitable for:

- Differing release and merge frequencies
- Needing a production branch to represent live reality
- Multi-environment deployments
- Multiple stable version lines
- Teams that find full Gitflow too heavy

Not suitable for:

- Small teams doing rapid releases
- Main branch already deployable at any time
- Teams lacking clear need for environment branches

## Implementation Advice

1. Clarify the semantics of `main` and `production` first
2. All changes still go through MRs / PRs
3. The production branch only receives validated changes
4. Stable branches only receive hotfixes for their respective versions
5. Use tags and release notes to document versions post-release
6. Hotfixes must be synced back to the mainline to avoid losing fixes

## Extended Reading

- [GitLab Flow](https://docs.gitlab.com/topics/gitlab_flow/)
- [Team Git Workflow Guide](team-git-workflow-guide_en.md)
- [Release Management](../../04-github-engineering/04-github-engineering_en/release-management_en.md)
