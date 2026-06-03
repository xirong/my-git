# Multi-Agent Branch Strategy

English | [中文](../multi-agent-branch-strategy.md)

When developing with multiple agents in parallel, the core is isolating tasks, clarifying ownership, and finally having humans perform integration.

## Branch Naming

```text
ai/task-parser-refactor
ai/task-api-test
ai/review-parser-refactor
```

## Recommended Process

1. One branch per agent.
2. One clear task per branch.
3. Independent commits and validation for each branch.
4. Human selects which solutions to retain.
5. Organize commits before merging.

## Avoid

- Multiple agents writing to the same workspace.
- Multiple agents modifying the same set of files simultaneously.
- Letting agents merge public branches themselves.
- Accepting results without looking at the diff.

## Recommended Naming

```text
ai/experiment-parser-a
ai/experiment-parser-b
ai/review-parser-a
```

Before merging experimental branches, it is suggested to reorganize them into normal business branches:

```text
feat/parser-error-handling
fix/parser-empty-input
```

## Extended Reading

- [git worktree](https://git-scm.com/docs/git-worktree)
- [Worktree for AI Agents](worktree-for-ai-agents_en.md)
- [AI Native Git Workflow](ai-native-git-workflow_en.md)
- [Recommended Reading Index](../../09-resources/09-resources_en/recommended-reading_en.md)
