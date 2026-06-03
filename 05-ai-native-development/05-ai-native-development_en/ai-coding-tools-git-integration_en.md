# Git Integration Practices for AI Coding Tools

English | [中文](../ai-coding-tools-git-integration.md)

Original links:

- [OpenAI Codex Web](https://developers.openai.com/codex/cloud)
- [OpenAI Codex Sandboxing](https://developers.openai.com/codex/concepts/sandboxing)
- [OpenAI Codex Changelog](https://developers.openai.com/codex/changelog)
- [Claude Code Worktrees](https://code.claude.com/docs/en/worktrees)
- [Claude Code Common Workflows](https://code.claude.com/docs/en/common-workflows)
- [GitHub Copilot Cloud Agent](https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-cloud-agent)
- [GitHub Copilot Sessions](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent/start-copilot-sessions)
- [Aider Git Integration](https://aider.chat/docs/git.html)
- [Cursor 2.0 and Composer](https://cursor.com/blog/2-0)

## 1. Common Trends

AI coding tools are shifting from "completing code in the editor" to "completing tasks around the Git workspace."

Their common direction is clear:

- Tasks are triggered from Issues, Prompts, PR comments, or local commands.
- Modifications occur in isolated branches, worktrees, sandboxes, or remote environments.
- Output is presented as diffs, commits, PRs, logs, and validation results.
- Merging still requires human review, CI, and repository rules.

This indicates that Git remains the collaboration boundary in AI programming.

## 2. Codex: Remote Environments, Sandboxes, PR Collaboration

The core feature of Codex is executing tasks in isolated environments and feeding results back to GitHub or local workflows.

Recommended team usage:

- Give Codex a clear task; avoid letting it freely explore the entire repository.
- Require it to output changed files, validation commands, and risks.
- Use PRs or diffs as entry points for human review.
- Maintain a default tight grip on permissions, networking, and command execution.
- Split large tasks into multiple small tasks for parallel execution.

The value of the Codex sandbox lies in limiting the execution scope. The ability for AI to run commands is a source of efficiency but also a source of risk; teams must include permissions, network access, sensitive files, and external writes in their rules.

Recommended PR description addition:

```text
AI tool:
Codex

Human intent:
Fix timeout validation for expired config.

Human checked:
- git diff --stat
- changed files
- test result
- rollback path
```

## 3. Claude Code: Worktree Isolation for Parallel Sessions

Official Claude Code documentation explicitly recommends using worktrees as a way to isolate parallel sessions.

It solves the problem of multiple AI sessions overwriting each other in the same repository.

Recommended practice:

```bash
claude --worktree feature-auth
claude --worktree bugfix-payment-timeout
```

Or create manually:

```bash
git worktree add ../repo-feature-auth -b ai/feature-auth
cd ../repo-feature-auth
claude
```

Note:

- Add `.claude/worktrees/` to `.gitignore`.
- Do not copy `.env`, local configurations, or secret files to worktrees by default.
- Check `git status` after each worktree is finished.
- Reorganize branches to follow team naming conventions before merging.
- Clean up useless worktrees to avoid too much leftover local context.

## 4. GitHub Copilot Cloud Agent: From Issue to PR

The typical path for GitHub Copilot Cloud Agent is triggering a task from an Issue or GitHub entry point; the Agent analyzes requirements, modifies code, commits to a branch, and creates a PR.

Suitable for:

- Small fixes
- Documentation additions
- Test completion
- Low-risk refactoring
- Issues with clear acceptance criteria

Not suitable for:

- Large features with unclear requirement boundaries
- Problems requiring production data for judgment
- High-risk changes involving security, permissions, billing, or payments
- Architectural adjustments requiring cross-team approval

Teams should write Issues more like task orders:

```text
Goal:

Scope:

Out of scope:

Acceptance criteria:

Tests to run:

Risk:
```

## 5. Aider: Git-First Local Pair Programming

Aider's characteristic is its deep use of Git: it can automatically commit AI modifications, and you can also use `/diff`, `/undo`, `/commit`, and `/git` to manage changes.

Best for local developers who want to pair program quickly, but teams should pay close attention to automatic commit strategies.

Suggestions:

- Ensure the workspace is clean before starting.
- Do not mix uncommitted human changes with AI modifications.
- Letting Aider commit automatically can improve the convenience of rolling back, but commits should still be manually organized before merging.
- For repositories requiring pre-commit hooks, clarify whether to enable `--git-commit-verify`.

Recommended workflow:

```bash
git status
git switch -c ai/aider-small-fix
aider
git log --oneline -5
git diff main...HEAD
git rebase -i main
```

## 6. Cursor: Multi-Agent and Aggregated Diffs

The official Cursor 2.0 release emphasizes Composer, multi-agent parallelism, and a more centralized diff review experience.

This tool form's requirements for Git workflows are:

- Multi-agent tasks must have clear boundaries.
- Each agent's output must be individually reviewable.
- Aggregated diffs can only serve as an entry point and cannot replace file-level review.
- Final commits should be split by logic to avoid committing directly based on tool execution results.

Suitable for using Cursor in:

- Exploring multiple solutions
- Local transformations of UI or frontend
- Documentation and test additions
- Small-scale refactoring

## 7. Unified Team Rules

Regardless of the AI tool used, teams should unify these rules:

| Rule | Recommended Practice |
| --- | --- |
| Task Boundary | Process only one clear goal at a time |
| Isolation Method | Branches, worktrees, sandboxes, or remote environments |
| Diff review | Humans first check `git diff --stat` and key files |
| Commit Splitting | Split by tests, implementation, documentation, and configuration |
| Validation Results | PR must clearly state commands and results |
| Merge Responsibility | Human reviewer assumes final judgment |
| Rollback Path | Each PR must explain how to undo it |

## 8. Recommended Minimum Workflow

```text
Issue / prompt
-> isolated branch or worktree
-> AI edits
-> human checks diff
-> split commits
-> run tests
-> AI review as assistant
-> human review
-> PR
-> CI
-> merge
```

The stronger the AI tools, the clearer the Git workflow must be.
