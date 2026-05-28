# Codex / Claude Code Git 实践

Codex、Claude Code 这类 AI 编程工具会让代码修改速度变快，也会让 Git 工作区更容易变乱。

这篇只讨论一个问题：使用 AI 编程工具时，如何让 Git 历史仍然清楚、可审查、可回滚。

## 核心原则

### 1. 每个任务一个分支

不要让 AI 直接在主分支上探索。

推荐：

```bash
git switch main
git pull --rebase
git switch -c ai/refactor-order-validator
```

如果最终要合入，可以整理成正常业务分支名：

```text
fix/order-timeout-validation
feat/github-governance-guide
```

### 2. 多 Agent 并行用 worktree

OpenAI Codex 官方页面提到 Codex app 面向 multi-agent workflows，并支持 built-in worktrees 和 cloud environments。

Claude Code 官方文档也明确建议用 Git worktrees 隔离并行 Claude Code sessions，避免不同会话互相影响。

本地手工创建：

```bash
git worktree add ../repo-task-a -b ai/task-a
git worktree add ../repo-task-b -b ai/task-b
```

每个目录单独启动对应工具：

```bash
cd ../repo-task-a
codex

cd ../repo-task-b
claude
```

工具命令会随版本变化，实际以你本机安装和官方文档为准。

### 3. AI 改完先审 diff

永远先看：

```bash
git status
git diff --stat
git diff
```

重点检查：

- 有没有无关文件
- 有没有格式化噪音
- 有没有临时日志
- 有没有 secret 或内部配置
- 有没有锁文件和依赖变化
- 有没有 public API 行为变化

### 4. 大 diff 先拆 commit

AI 一次改很多文件很常见，但人类不应该按大杂烩合入。

推荐拆成：

```text
test(order): cover timeout validation
fix(order): reject expired timeout config
docs(order): explain timeout behavior
```

命令：

```bash
git add -p
git commit -m "test(order): cover timeout validation"
git add -p
git commit -m "fix(order): reject expired timeout config"
```

### 5. AI Review 只能做辅助

AI 可以帮你做第一轮风险扫描：

```text
请审查当前 git diff。
只输出具体风险，按严重程度排序。
重点检查行为边界、测试有效性、安全风险、无关改动。
```

最终合入仍然由人类负责。

## 推荐工作流

```text
创建分支
-> 让 AI 修改
-> 人类审 diff
-> 拆 commit
-> 跑测试
-> AI 做第一轮 Review
-> 人类 Review
-> 开 PR
-> CI 通过后合入
```

## Codex 使用建议

- 给 Codex 明确任务边界
- 要求它列出改动文件、验证方式、风险
- 不让它顺手重构无关模块
- 多任务并行时使用 worktree 或独立环境
- 合入前人工检查 diff 和测试结果
- 对远程任务保留 PR、日志、验证命令和人类复核记录

提示词示例：

```text
只修复订单超时校验问题。
不要修改接口签名，不要格式化无关文件。
完成后列出改动文件、行为变化、验证命令和风险。
```

## Claude Code 使用建议

Claude Code 官方文档提供了 worktree 并行会话说明，也提到可以把 Claude 作为命令行式工具接入验证流程。

建议：

- 每个 Claude Code session 绑定一个 worktree
- 用 `.claude/` 或项目文档沉淀团队约定
- 不同任务不要共享同一个工作区
- 长任务保留清楚的分支名和目录名
- 清理完成后的 worktree
- 对需要复制的 `.env`、本地配置保持谨慎，避免把敏感信息带进临时工作区

清理：

```bash
git worktree list
git worktree remove ../repo-task-a
```

## 其他 AI 工具

不同工具的 Git 集成重点不同：

| 工具 | Git 工作流关注点 |
| --- | --- |
| Codex | sandbox、远程环境、GitHub 协作、任务日志 |
| Claude Code | worktree 隔离、并行 session、subagent 工作区 |
| GitHub Copilot Cloud Agent | Issue 到分支、提交、PR 的异步流程 |
| Aider | 自动提交、`/diff`、`/undo`、本地 git-first 工作流 |
| Cursor | 多 Agent 并行、聚合 diff、人工拆分提交 |

详细整理见 [AI 编程工具的 Git 集成实践](ai-coding-tools-git-integration.md)。

## 常见反模式

### 1. 同一个目录里跑多个 AI 工具

风险：互相覆盖文件，分支状态混乱。

建议：一个任务一个 worktree。

### 2. AI 改完直接 commit

风险：无关文件、调试代码、配置变更混入。

建议：先 `git diff --stat`，再 `git add -p`。

### 3. 让 AI 自行决定合入

风险：工具缺少团队发布、回滚、责任边界上下文。

建议：AI 可以建议，人类负责合入。

## 延伸阅读

- [OpenAI Codex](https://openai.com/codex/)
- [OpenAI Codex Web](https://developers.openai.com/codex/cloud)
- [OpenAI Codex Sandboxing](https://developers.openai.com/codex/concepts/sandboxing)
- [Claude Code: Run parallel sessions with worktrees](https://code.claude.com/docs/en/worktrees)
- [Claude Code: Common workflows](https://code.claude.com/docs/en/common-workflows)
- [AI 编程工具的 Git 集成实践](ai-coding-tools-git-integration.md)
- [git worktree 官方文档](https://git-scm.com/docs/git-worktree)
- [AI Native Git Workflow](ai-native-git-workflow.md)
- [Worktree for AI Agents](worktree-for-ai-agents.md)
