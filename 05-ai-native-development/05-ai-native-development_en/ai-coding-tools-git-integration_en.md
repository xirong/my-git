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

## Scope

This page is the fact lookup for tool integrations: Git-facing shapes, official sources, and differences that need rechecking as product versions change. Before adopting a capability, open its source and confirm the relevant version, permissions, and product boundary.

Branch isolation, diff review, commit organization, validation, and human merge responsibility are stable practices across tools; see [Codex / Claude Code Git Practices](codex-claude-code-git-practices_en.md).

## 1. How to use these tool facts

Each tool may touch a repository or GitHub, but its entry point, execution environment, network and write permissions, and commit or PR behavior can vary by product, plan, organization settings, and version. This page does not turn one tool's UI or defaults into a team workflow. Confirm the capability available in the relevant official source, then use [Codex / Claude Code Git Practices](codex-claude-code-git-practices_en.md) for tool-independent isolation, review, and human acceptance rules.

## 2. Codex: cloud, sandboxing, and version changes

OpenAI maintains separate official material for Codex cloud, sandboxing, and the changelog above. Before adoption, confirm whether a task actually runs locally or in cloud, the selected sandbox's command, network, and file-access scope, and whether repository connection and PR return are enabled for the account and organization in question. Feature names and availability follow the official documentation and changelog for the relevant version.

## 3. Claude Code: the worktree form

Claude Code's official worktree documentation connects parallel sessions with Git worktrees; its common-workflows documentation adds command and session behavior. Before enabling it, check the worktree location, branch naming, and local-configuration handling for the relevant version. Whether a worktree inherits sensitive files, can be safely cleaned, or contains an acceptable change remains a repository decision under the [practices page](codex-claude-code-git-practices_en.md).

## 4. GitHub Copilot Cloud Agent: cloud tasks and sessions

GitHub's cloud-agent and session documentation define its GitHub task entry points and session concepts. Whether a task can start from a particular Issue or entry point, which branch or PR it creates, which Actions run, and which tokens and secrets are visible depends on the current GitHub plan, repository settings, workflows, and permissions. [Background Agent Tasks](background-agent-workflow_en.md) owns the task contract, candidate SHA, and receiving decision.

## 5. Aider: Git-integrated local sessions

Aider's Git-integration documentation records its Git-facing commands and automatic-commit capability. Before using automatic commits, `/undo`, `/diff`, or commit verification, confirm the setting, hook behavior, and changed-path scope in the current Aider documentation. Whether a commit belongs to the task, whether history may be rewritten, and which validation must be retained belong to the [practices page](codex-claude-code-git-practices_en.md).

## 6. Cursor: Composer and multi-agent release information

Cursor's 2.0 release material introduces Composer, multi-agent parallelism, and concentrated diff review. That release page describes one product version; it does not establish matching behavior for other versions, plans, or organization settings. [Background Agent Tasks](background-agent-workflow_en.md) and [Multi-Agent Branch Strategy](multi-agent-branch-strategy_en.md) cover boundaries, candidate reclaim, and review capacity for concurrent work.

## 7. From tool facts to engineering practices

After confirming a tool fact, choose the stable rule for the engineering problem in front of you:

- [Codex / Claude Code Git Practices](codex-claude-code-git-practices_en.md): isolation, existing-edit checks, diff review, commit organization, and the human acceptance preconditions.
- [Engineering Change Course](engineering-change-course_en.md): a continuous case for task contract, candidate revision, runtime evidence, and recovery.
- [CI for AI-Generated Changes](ci-for-ai-generated-changes_en.md): bind checks to a candidate or integration SHA and inspect workflow permissions and secrets.
- [Background Agent Tasks](background-agent-workflow_en.md): record base, candidate, attempt, permission, and receiving decision for asynchronous work.
