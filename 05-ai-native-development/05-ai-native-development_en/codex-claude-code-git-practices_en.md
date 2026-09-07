# Codex / Claude Code Git Practices

English | [中文](../codex-claude-code-git-practices.md)

AI programming tools like Codex and Claude Code accelerate code changes and can make Git workspaces far easier to get into a mess.

This article focuses on a single question: when working with AI programming tools, how do you keep Git history clean, reviewable, and rollback-safe? [Git Integration Practices for AI Coding Tools](ai-coding-tools-git-integration_en.md) maintains tool capabilities, official sources, and version differences; this page keeps the Git practices and workflow that apply across tools.

## Core Principles

### 1. One Branch per Task

Do not let AI explore directly on the main branch. Start from a dedicated branch instead:

`<integration-branch>` is the repository's actual integration branch, such as `main`, `master`, or `develop`. First require `git status --porcelain` to print nothing; if there are edits owned by someone else, preserve the state and use a separate worktree.

```bash
git status --porcelain
git switch <integration-branch>
git pull --rebase origin <integration-branch>
git switch -c ai/refactor-order-validator
```

Before merging, rename the branch to a standard naming convention:

```text
fix/order-timeout-validation
feat/github-governance-guide
```

### 2. Use Worktree for Multi-Agent Parallelism

Whether a tool can create or manage a worktree depends on its documented capability and installed version; check the [tool fact lookup](ai-coding-tools-git-integration_en.md). This section owns the Git requirement: parallel tasks must not share one working directory.

Create worktrees manually:

```bash
git worktree add ../repo-task-a -b ai/task-a
git worktree add ../repo-task-b -b ai/task-b
```

Then start the appropriate tool in each directory:

```bash
cd ../repo-task-a
codex

cd ../repo-task-b
claude
```

Tool startup commands vary by version; use the [tool fact lookup](ai-coding-tools-git-integration_en.md) to confirm them.

### 3. Always Review the Diff After AI Changes

Start with:

```bash
git status
git diff --stat
git diff
```

Check for:

- Unrelated files touched by the AI
- Formatting-only noise
- Temporary debug logs
- Secrets or internal configuration values
- Lock file and dependency changes
- Behavioral changes to public APIs

### 4. Split Commits for Large Diffs

AI frequently modifies many files at once. Don't merge that as a single jumbled commit.

Before partial staging, confirm this is a clean or isolated task worktree and that `git diff --cached` has no content from another task. If staged, unstaged, or untracked edits have another owner, stop splitting here rather than using reset or cleanup commands to make room.

Split by concern, for example:

```text
test(order): cover timeout validation
fix(order): reject expired timeout config
docs(order): explain timeout behavior
```

Commands:

```bash
git add -p
git commit -m "test(order): cover timeout validation"
git add -p
git commit -m "fix(order): reject expired timeout config"
```

### 5. Use AI Review as a First Pass, Not a Final Gate

AI can help you do an initial risk scan:

```text
Please review the current git diff.
Output only specific risks, sorted by severity.
Focus checks on behavioral boundaries, test validity, security risks, and irrelevant changes.
```

Merging is still a human responsibility.

## Recommended Workflow

```text
Create branch
-> AI makes changes
-> Human reviews diff
-> Split into commits
-> Run tests
-> AI does first-pass review
-> Human review
-> Open PR
-> Merge after CI passes
```

## Tool-Independent Execution Conventions

- State the goal, scope, acceptance method, and risk in the task so unrelated refactors do not enter the change.
- Bind every parallel task to a separate branch or worktree, and use clear branch and directory names to retain context.
- Before merging, a person checks the diff, test results, and rollback path. For remote tasks, also retain the PR, logs, validation commands, and human sign-off.
- Do not copy `.env`, local configuration, or secret files into temporary workspaces by default.
- When a task is done, check worktree state and then remove directories that are no longer needed:

```bash
git worktree list
git worktree remove ../repo-task-a
```

See [Git Integration Practices for AI Coding Tools](ai-coding-tools-git-integration_en.md) for current tool capabilities and Git integration differences.

## Common Anti-Patterns

### 1. Running Multiple AI Tools in the Same Directory

Risk: Tools overwrite each other's files and leave branch state in chaos.

Fix: One worktree per task.

### 2. Committing Immediately After AI Changes

Risk: Unrelated files, debug code, and config changes get bundled into the commit.

Fix: Run `git diff --stat` first, then stage selectively with `git add -p`.

### 3. Letting AI Decide When to Merge

Risk: AI tools have no visibility into team release schedules, rollback plans, or ownership boundaries.

Fix: AI can recommend; humans make the call on merging.

## Further Reading

- [OpenAI Codex](https://openai.com/codex/)
- [OpenAI Codex Web](https://developers.openai.com/codex/cloud)
- [OpenAI Codex Sandboxing](https://developers.openai.com/codex/concepts/sandboxing)
- [Claude Code: Run parallel sessions with worktrees](https://code.claude.com/docs/en/worktrees)
- [Claude Code: Common workflows](https://code.claude.com/docs/en/common-workflows)
- [Git Integration Practices for AI Coding Tools](ai-coding-tools-git-integration_en.md)
- [git worktree official documentation](https://git-scm.com/docs/git-worktree)
- [AI Native Git Workflow](ai-native-git-workflow_en.md)
- [Worktree for AI Agents](worktree-for-ai-agents_en.md)
