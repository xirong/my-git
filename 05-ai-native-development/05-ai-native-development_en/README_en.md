# AI Native Development

English | [中文](../README.md)

This directory discusses Git workflows in the age of AI programming: AI can generate code faster, and humans need to use Git to organize changes into reviewable, verifiable, and rollback-ready engineering units.

## What to Read First

| Problem you want to solve | Recommended Reading |
| --- | --- |
| Establishing a Git workflow for AI programming | [AI Native Git Workflow](ai-native-git-workflow_en.md) |
| Don't know how to review code after AI modifications | [AI Change Review Practice Example](ai-change-review-example_en.md) |
| Systematically reviewing AI-generated code | [How to Review AI-Generated Code](ai-generated-code-review_en.md) |
| AI modified too many files at once | [AI Commit Splitting](ai-commit-splitting_en.md) |
| Large diffs need to be split into multiple PRs | [Stacked PR for AI-Generated Changes](stacked-pr-for-ai-generated-changes_en.md) |
| Parallel development with multiple agents | [Multi-Agent Branch Strategy](multi-agent-branch-strategy_en.md) |

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

## Related Content

- [Team Collaboration](../../03-team-collaboration/03-team-collaboration_en/README_en.md)
- [GitHub Engineering Governance](../../04-github-engineering/04-github-engineering_en/README_en.md)
- [AI Code Review Checklist](../../08-templates/08-templates_en/ai-code-review-checklist_en.md)
