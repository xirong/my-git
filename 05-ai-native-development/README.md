# AI Native Development

[English](05-ai-native-development_en/README_en.md) | 中文

这个目录讨论 AI 编程时代的 Git 工作流：AI 可以更快地产生代码，人类需要用 Git 把变更整理成可审查、可验证、可回滚的工程单元。

它属于[知识地图](../01-getting-started/knowledge-map.md)的“完成工程变更”层。前置是能区分工作区、Index 和已提交版本；需要选择团队协作模型时，继续阅读[团队协作](../03-team-collaboration/README.md)。

## 先读什么

第一次阅读，先走完[一次工程变更课程](engineering-change-course.md)：把任务契约、提交范围、CI、运行证据和恢复连起来；再用[接受 Agent 变更](ai-change-control-loop.md)核对证据字段与边界。

配套的[本地制品与服务实验](../labs/ai-change-control/README.md)在临时 Git 仓库中构建制品，并只在回环地址启动最小 HTTP 服务来核对运行结果。它不连接真实 CI、托管平台、生产环境或外部服务。旧命令示例的[安全回归](../labs/git-command-safety/README.md)只覆盖说明中列出的四种命令模式；远端授权、分支保护、hooks 和团队规则仍须在实际仓库核实。

| 你要解决的问题 | 建议阅读 |
| --- | --- |
| 想建立 AI 编程下的 Git 工作流 | [AI Native Git Workflow](ai-native-git-workflow.md) |
| 想把小修复从任务契约验收到恢复 | [一次工程变更课程](engineering-change-course.md) |
| AI 改完代码不知道怎么审 | [AI 变更审查实战样例](ai-change-review-example.md) |
| 想让 CI 指向实际候选或集成版本 | [AI 生成变更的 CI](ci-for-ai-generated-changes.md) |
| 想系统 Review AI 生成代码 | [How to Review AI-Generated Code](ai-generated-code-review.md) |
| AI 一次改太多文件 | [AI Commit Splitting](ai-commit-splitting.md) |
| 大 diff 需要拆成多个 PR | [Stacked PR for AI-Generated Changes](stacked-pr-for-ai-generated-changes.md) |
| 多个 Agent 并行开发 | [Multi-Agent Branch Strategy](multi-agent-branch-strategy.md) |
| 后台 Agent 返回结果需要接收 | [后台 Agent 任务](background-agent-workflow.md) |

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
| 后台 Agent 任务 | 后台 Agent 任务 + AI 生成变更的 CI + Agent 事故恢复 |

## 相关内容

- [团队协作](../03-team-collaboration/README.md)
- [GitHub 工程治理](../04-github-engineering/README.md)
- [Agent 事故恢复](../06-troubleshooting/ai-agent-incident-recovery.md)
- [AI 代码 Review 清单](../08-templates/ai-code-review-checklist.md)
