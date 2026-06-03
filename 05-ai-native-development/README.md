# AI Native Development

[English](05-ai-native-development_en/README_en.md) | 中文

这个目录讨论 AI 编程时代的 Git 工作流：AI 可以更快地产生代码，人类需要用 Git 把变更整理成可审查、可验证、可回滚的工程单元。

## 先读什么

| 你要解决的问题 | 建议阅读 |
| --- | --- |
| 想建立 AI 编程下的 Git 工作流 | [AI Native Git Workflow](ai-native-git-workflow.md) |
| AI 改完代码不知道怎么审 | [AI 变更审查实战样例](ai-change-review-example.md) |
| 想系统 Review AI 生成代码 | [How to Review AI-Generated Code](ai-generated-code-review.md) |
| AI 一次改太多文件 | [AI Commit Splitting](ai-commit-splitting.md) |
| 大 diff 需要拆成多个 PR | [Stacked PR for AI-Generated Changes](stacked-pr-for-ai-generated-changes.md) |
| 多个 Agent 并行开发 | [Multi-Agent Branch Strategy](multi-agent-branch-strategy.md) |

## 工具实践

- [Codex / Claude Code Git 实践](codex-claude-code-git-practices.md)
- [AI 编程工具的 Git 集成实践](ai-coding-tools-git-integration.md)
- [Worktree for AI Agents](worktree-for-ai-agents.md)
- [AI Reviewer 与 Human Reviewer](ai-reviewer-and-human-reviewer.md)

工具会变化，但底层原则稳定：隔离任务、审查 diff、拆分提交、保留验证、让人类负责最终合入。

## 推荐组合

| 场景 | 推荐组合 |
| --- | --- |
| 单个小修复 | AI Workflow + AI Review |
| 大功能 | AI Workflow + Commit Splitting + Stacked PR |
| 多 Agent 并行 | Worktree + Multi-Agent Branch Strategy |
| 团队接入 AI Review | AI Generated Code Review + AI Reviewer 与 Human Reviewer |

## 相关内容

- [团队协作](../03-team-collaboration/README.md)
- [GitHub 工程治理](../04-github-engineering/README.md)
- [AI 代码 Review 清单](../08-templates/ai-code-review-checklist.md)
