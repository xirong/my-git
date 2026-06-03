# Codex / Claude Code Git Practices

English | [中文](../codex-claude-code-git-practices.md)

AI programming tools like Codex and Claude Code accelerate code changes — and make Git workspaces far easier to get into a mess.

This article focuses on a single question: when working with AI programming tools, how do you keep Git history clean, reviewable, and rollback-safe?

## Core Principles

### 1. One Branch per Task

Do not let AI explore directly on the main branch. Start from a dedicated branch instead:

```bash
git switch main
git pull --rebase
git switch -c ai/refactor-order-validator
```

Before merging, rename the branch to a standard naming convention:

```text
fix/order-timeout-validation
feat/github-governance-guide
```

### 2. Use Worktree for Multi-Agent Parallelism

The OpenAI Codex page describes the Codex app as built for multi-agent workflows, with native support for worktrees and cloud environments.

The Claude Code docs explicitly recommend using Git worktrees to isolate parallel sessions and prevent them from interfering with each other.

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

Exact commands may vary by version — check your local installation and the official docs.

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

## Codex Usage Tips

- Give Codex a well-scoped task boundary.
- Ask it to list changed files, how to validate, and any risks.
- Don't let it opportunistically refactor unrelated modules.
- Use worktrees or isolated environments when running tasks in parallel.
- Review the diff and test results yourself before merging.
- For remote tasks, keep the PR, logs, validation commands, and human sign-off on record.

Prompt example:

```text
Fix only the order timeout validation issue.
Do not modify interface signatures or format unrelated files.
When done, list changed files, behavioral changes, validation commands, and risks.
```

## Claude Code Usage Tips

The Claude Code docs cover parallel sessions with worktrees and also describe using Claude as a CLI tool inside validation pipelines.

Tips:

- Pin each Claude Code session to a dedicated worktree.
- Use `.claude/` or project docs to capture team conventions.
- Never share a workspace across different tasks.
- Keep branch and directory names descriptive for long-running tasks.
- Remove worktrees when a task is done.
- Handle `.env` files and local config with care — don't let sensitive values leak into temporary workspaces.

Cleanup:

```bash
git worktree list
git worktree remove ../repo-task-a
```

## Other AI Tools

Each tool has a different Git integration focus:

| Tool | Git Workflow Focus |
| --- | --- |
| Codex | Sandbox, remote environment, GitHub collaboration, task logs |
| Claude Code | Worktree isolation, parallel sessions, subagent workspaces |
| GitHub Copilot Cloud Agent | Asynchronous process from Issue to branch, commit, and PR |
| Aider | Automatic commits, `/diff`, `/undo`, local git-first workflow |
| Cursor | Multi-agent parallelism, aggregated diffs, manual commit splitting |

For a full breakdown, see [Git Integration Practices for AI Coding Tools](ai-coding-tools-git-integration_en.md).

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
