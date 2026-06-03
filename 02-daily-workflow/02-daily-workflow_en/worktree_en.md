# Worktree

English | [中文](../worktree.md)

`git worktree` allows the same repository to check out multiple branches into different directories simultaneously.

Best for people who need to process multiple tasks in parallel, especially for hotfixes, long-term branch maintenance, and parallel development by AI Agents.

## Suitable Scenarios

- Need to handle multiple branches simultaneously
- Handling an urgent hotfix
- Do not want to stash frequently
- Multiple AI Agents processing tasks in parallel
- Running tests on one branch while continuing development on another

## Basic Commands

Create a new worktree:

```bash
git worktree add ../project-hotfix -b hotfix/urgent-fix
```

View worktrees:

```bash
git worktree list
```

Remove a worktree:

```bash
git worktree remove ../project-hotfix
```

Clean up invalid records:

```bash
git worktree prune
```

## Difference from stash

`stash` is suitable for temporarily saving current unfinished changes.

`worktree` is suitable for keeping multiple complete workspaces simultaneously.

If you frequently switch between multiple branches within a day, worktree is usually clearer than stash.

## AI Programming Scenarios

Avoid having multiple AI Agents write to the same workspace.

Recommended:

```bash
git worktree add ../repo-agent-a -b ai/task-a
git worktree add ../repo-agent-b -b ai/task-b
```

One branch and one directory per Agent, eventually consolidated and merged by humans.

## Further Reading

- [git worktree official documentation](https://git-scm.com/docs/git-worktree)
- [Worktree for AI Agents](../../05-ai-native-development/05-ai-native-development_en/worktree-for-ai-agents_en.md)
- [AI Native Git Workflow](../../05-ai-native-development/05-ai-native-development_en/ai-native-git-workflow_en.md)
- [Recommended Reading Index](../../09-resources/09-resources_en/recommended-reading_en.md)
