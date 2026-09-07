# AI Native Development

English | [中文](../README.md)

This directory discusses Git workflows in the age of AI programming: AI can generate code faster, and humans need to use Git to organize changes into reviewable, verifiable, and rollback-ready engineering units.

It belongs to the “complete an engineering change” layer of the [knowledge map](../../01-getting-started/01-getting-started_en/knowledge-map_en.md). First distinguish the working tree, index, and committed revision; when you need to choose a team collaboration model, continue to [Team Collaboration](../../03-team-collaboration/03-team-collaboration_en/README_en.md).

## What to Read First

Start with the [engineering change course](engineering-change-course_en.md). Connect the task contract, commit scope, CI, runtime evidence, and recovery; then use [Accept an Agent Change](ai-change-control-loop_en.md) for evidence fields and boundaries.

The companion [local artifact-and-service exercise](../../labs/ai-change-control/README.md) builds an artifact in a temporary Git repository and starts a minimal HTTP service only on loopback to check a runtime result. It does not contact real CI, a hosting platform, production, or an external service. The [command-safety regression](../../labs/git-command-safety/README.md) covers only the four documented command patterns; remote authorization, branch protection, hooks, and team rules still need checks in the actual repository.

| Problem you want to solve | Recommended Reading |
| --- | --- |
| Establishing a Git workflow for AI programming | [AI Native Git Workflow](ai-native-git-workflow_en.md) |
| Taking a small repair from task contract through recovery | [Engineering Change Course](engineering-change-course_en.md) |
| Don't know how to review code after AI modifications | [AI Change Review Practice Example](ai-change-review-example_en.md) |
| Making CI name the actual candidate or integration revision | [CI for AI-Generated Changes](ci-for-ai-generated-changes_en.md) |
| Systematically reviewing AI-generated code | [How to Review AI-Generated Code](ai-generated-code-review_en.md) |
| AI modified too many files at once | [AI Commit Splitting](ai-commit-splitting_en.md) |
| Large diffs need to be split into multiple PRs | [Stacked PR for AI-Generated Changes](stacked-pr-for-ai-generated-changes_en.md) |
| Parallel development with multiple agents | [Multi-Agent Branch Strategy](multi-agent-branch-strategy_en.md) |
| Reclaiming a background agent result | [Background Agent Tasks](background-agent-workflow_en.md) |

## Tool Practices

- [Codex / Claude Code Git Practices](codex-claude-code-git-practices_en.md)
- [Git Integration Practices for AI Coding Tools](ai-coding-tools-git-integration_en.md)
- [Worktree for AI Agents](worktree-for-ai-agents_en.md)
- [AI Reviewer and Human Reviewer](ai-reviewer-and-human-reviewer_en.md)

Tools change, but underlying principles remain stable: isolate tasks, review diffs, split commits, retain validation, and let humans be responsible for the final merge.

## Recommended Combinations

| Scenario | Recommended Combination |
| --- | --- |
| Single small fix | AI Workflow + AI Review |
| Large feature | AI Workflow + Commit Splitting + Stacked PR |
| Multi-agent parallel work | Worktree + Multi-Agent Branch Strategy |
| Team adoption of AI Review | AI Generated Code Review + AI Reviewer and Human Reviewer |
| Background agent work | Background Agent Tasks + CI for AI-Generated Changes + AI Agent Incident Recovery |

## Related Content

- [Team Collaboration](../../03-team-collaboration/03-team-collaboration_en/README_en.md)
- [GitHub Engineering Governance](../../04-github-engineering/04-github-engineering_en/README_en.md)
- [AI Agent Incident Recovery](../../06-troubleshooting/06-troubleshooting_en/ai-agent-incident-recovery_en.md)
- [AI Code Review Checklist](../../08-templates/08-templates_en/ai-code-review-checklist_en.md)
