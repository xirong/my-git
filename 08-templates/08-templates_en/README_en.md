# Template Library

English | [中文](../README.md)

This directory provides templates that can be copied into your team's repository. The goal of these templates is to reduce communication costs and provide a fixed information structure for PRs, Reviews, releases, hotfixes, and AI code reviews.

## Recommended Combinations

| Team Stage | Suggested to Start With |
| --- | --- |
| Personal Projects | [Commit Message Convention](commit-message-convention_en.md), [Branch Naming Convention](branch-naming-convention_en.md) |
| Small Teams | [Pull Request Template](pull-request-template_en.md), [Code Review Checklist](code-review-checklist_en.md) |
| Growing Teams | PR Template, Review Checklist, Issue Template, Release Note |
| Teams with Production Release Pressure | [Hotfix Process](hotfix-process_en.md), [Release Note Template](release-note-template_en.md) |
| AI Programming Teams | [AI Code Review Checklist](ai-code-review-checklist_en.md), PR Template, Commit Message Convention |

## Template List

- [Pull Request Template](pull-request-template_en.md)
- [Code Review Checklist](code-review-checklist_en.md)
- [AI Code Review Checklist](ai-code-review-checklist_en.md)
- [Commit Message Convention](commit-message-convention_en.md)
- [Branch Naming Convention](branch-naming-convention_en.md)
- [Release Note Template](release-note-template_en.md)
- [Hotfix Process](hotfix-process_en.md)
- [Issue Template Bug](issue-template-bug_en.md)
- [Issue Template Feature](issue-template-feature_en.md)

## How to Use

You can copy the templates to the `.github/` directory of your team's repository:

```text
.github/
  PULL_REQUEST_TEMPLATE.md
  ISSUE_TEMPLATE/
    bug_report.md
    feature_request.md
```

If the team already has templates, only add the missing fields rather than replacing all processes at once.

## Recommendations for AI Programming Teams

At a minimum, add the following to your PR template:

- AI tool name
- Task boundaries set by humans for the AI
- Files and diffs actually reviewed by humans
- Verification commands and results
- Rollback plan

## Related Content

- [AI Native Development](../../05-ai-native-development/05-ai-native-development_en/README_en.md)
- [GitHub Engineering Governance](../../04-github-engineering/04-github-engineering_en/README_en.md)
- [Team Collaboration](../../03-team-collaboration/03-team-collaboration_en/README_en.md)
