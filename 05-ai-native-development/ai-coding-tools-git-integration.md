# AI 编程工具的 Git 集成实践

[English](05-ai-native-development_en/ai-coding-tools-git-integration_en.md) | 中文

原文链接：

- [OpenAI Codex Web](https://developers.openai.com/codex/cloud)
- [OpenAI Codex Sandboxing](https://developers.openai.com/codex/concepts/sandboxing)
- [OpenAI Codex Changelog](https://developers.openai.com/codex/changelog)
- [Claude Code Worktrees](https://code.claude.com/docs/en/worktrees)
- [Claude Code Common Workflows](https://code.claude.com/docs/en/common-workflows)
- [GitHub Copilot Cloud Agent](https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-cloud-agent)
- [GitHub Copilot Sessions](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent/start-copilot-sessions)
- [Aider Git Integration](https://aider.chat/docs/git.html)
- [Cursor 2.0 and Composer](https://cursor.com/blog/2-0)

## 本文负责什么

本文是工具事实的速查入口：各工具与 Git 的接入形态、官方来源，以及需要随产品版本重新核对的差异都放在这里。采用某项能力前，打开对应原文确认适用版本、权限与产品边界。

分支隔离、diff 审查、提交组织、验证和人工合入责任是跨工具的稳定实践，见[Codex / Claude Code Git 实践](codex-claude-code-git-practices.md)。

## 1. 怎样使用这份工具事实

这些工具都可能接触仓库或 GitHub，但触发入口、执行环境、网络与写入权限、提交和 PR 行为会随产品、套餐、组织配置与版本变化。本页不把某个工具的界面或默认值写成团队流程。先从对应官方链接确认本次实际可用的能力，再进入[Codex / Claude Code Git 实践](codex-claude-code-git-practices.md)采用跨工具的隔离、审查和人工接收规则。

## 2. Codex：cloud、sandbox 与版本变化

OpenAI 将 Codex cloud、sandboxing 和变更记录分别维护在上方三份官方资料中。采用时确认任务实际运行在本地还是 cloud，所选 sandbox 的命令、网络和文件访问范围，以及仓库连接和 PR 回传是否已经在本次账户与组织配置中启用。页面中的功能名称和可用范围以对应版本的官方文档与 changelog 为准。

## 3. Claude Code：worktree 形态

Claude Code 的官方 worktree 文档将并行会话与 Git worktree 联系起来；常见工作流文档补充其命令和会话行为。启用前按对应版本核对 worktree 的创建位置、分支命名和本地配置处理方式。worktree 是否继承敏感文件、该目录是否可安全清理，以及怎样接收其中的改动，仍按仓库规则和[实践页](codex-claude-code-git-practices.md)判断。

## 4. GitHub Copilot Cloud Agent：云端任务和会话

GitHub 的 cloud-agent 与 session 文档说明其 GitHub 内的任务入口和会话概念。实际能否从某个 Issue 或入口发起、会产生什么分支或 PR、哪些 Actions 会运行，以及哪些令牌和 secrets 可见，取决于当前 GitHub 计划、仓库设置、工作流和权限。任务契约、候选 SHA 与接收决定由[后台 Agent 任务](background-agent-workflow.md)统一说明。

## 5. Aider：Git 集成本地会话

Aider 的 Git 集成文档记录其 Git 相关命令与自动提交能力。使用自动提交、`/undo`、`/diff` 或 commit verification 前，应以当前 Aider 版本文档确认开关、hook 行为和实际改动范围。提交是否属于任务、是否可以重写历史以及哪些验证必须保留，见[实践页](codex-claude-code-git-practices.md)。

## 6. Cursor：Composer 与多 Agent 发布信息

Cursor 2.0 的发布资料介绍 Composer、多 Agent 并行和集中 diff 审查体验。该发布页说明的是该版本的产品形态，不保证其他版本、套餐或组织配置也有相同行为。并行任务的边界、候选接收和审查容量，由[后台 Agent 任务](background-agent-workflow.md)与[多 Agent 分支策略](multi-agent-branch-strategy.md)处理。

## 7. 从工具事实进入工程实践

确认工具事实后，再根据眼前的工程问题选择一份稳定规则：

- [Codex / Claude Code Git 实践](codex-claude-code-git-practices.md)：隔离、检查已有编辑、审查 diff、组织提交和人工合入前提。
- [一次工程变更课程](engineering-change-course.md)：把任务契约、候选版本、运行证据和恢复串成连续案例。
- [AI 生成变更的 CI](ci-for-ai-generated-changes.md)：将检查绑定到候选或集成 SHA，并核对工作流权限和 secrets。
- [后台 Agent 任务](background-agent-workflow.md)：记录异步任务的 base、candidate、attempt、权限和接收决定。
