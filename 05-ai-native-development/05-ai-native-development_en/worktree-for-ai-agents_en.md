# Worktree for AI Agents

English | [中文](../worktree-for-ai-agents.md)

`git worktree` is suitable for isolating multiple AI tasks into different directories, reducing cross-contamination of workspaces.

## Suitable Scenarios

- Multiple agents exploring different solutions in parallel.
- One task for development, another for review.
- Need to maintain running environments for multiple branches simultaneously.
- Don't want to repeatedly stash and switch branches.

## Basic Commands

```bash
git worktree add ../project-task-a -b ai/task-a
git worktree add ../project-task-b -b ai/task-b
git worktree list
git worktree remove ../project-task-a
```

## Recommended Rules

- One worktree serves only one task.
- Branch names clearly state the AI task intent.
- Delete worktrees promptly after tasks are finished.
- Return to the main workspace for final checks before merging.
- Do not copy `.env`, keys, or production configurations to AI worktrees by default.
- If a tool automatically creates worktrees, add the corresponding directories to `.gitignore`.

## Claude Code Scenarios

Claude Code officially supports creating isolated sessions via `--worktree`:

```bash
claude --worktree feature-auth
claude --worktree bugfix-payment-timeout
```

These types of automatic worktrees are suitable for parallel exploration, but you should still return to the Git perspective to check before merging:

```bash
git worktree list
git status
git diff --stat
```

## Extended Reading

- [git worktree](https://git-scm.com/docs/git-worktree)
- [Claude Code Worktrees](https://code.claude.com/docs/en/worktrees)
- [Git Integration Practices for AI Coding Tools](ai-coding-tools-git-integration_en.md)
