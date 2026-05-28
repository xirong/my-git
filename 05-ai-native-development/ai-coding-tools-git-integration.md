# AI 编程工具的 Git 集成实践

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

## 1. 共同趋势

AI 编程工具正在从“编辑器里补代码”变成“围绕 Git 工作区完成任务”。

它们的共同方向很清楚：

- 任务从 Issue、Prompt、PR 评论或本地命令触发
- 修改发生在隔离分支、worktree、sandbox 或远程环境中
- 输出以 diff、commit、PR、日志和验证结果呈现
- 合入前仍要经过人类 Review、CI 和仓库规则

这说明 Git 在 AI 编程里仍然是协作边界。

## 2. Codex：远程环境、sandbox、PR 协作

Codex 的核心特点是把任务放到隔离环境里执行，再把结果反馈到 GitHub 或本地工作流。

适合的团队用法：

- 给 Codex 一个明确任务，避免让它自由探索整个仓库
- 要求它输出改动文件、验证命令和风险
- 用 PR 或 diff 作为人类审查入口
- 对权限、网络、命令执行保持默认收紧
- 大任务拆成多个小任务并行执行

Codex sandbox 的价值在于限制执行范围。AI 能跑命令是效率来源，也是风险来源，团队要把权限、网络访问、敏感文件、外部写入都纳入规则。

推荐 PR 描述补充：

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

## 3. Claude Code：worktree 隔离并行会话

Claude Code 官方文档明确把 worktree 用作并行会话隔离方式。

它解决的是同一个仓库里多个 AI 会话互相覆盖的问题。

推荐做法：

```bash
claude --worktree feature-auth
claude --worktree bugfix-payment-timeout
```

或手工创建：

```bash
git worktree add ../repo-feature-auth -b ai/feature-auth
cd ../repo-feature-auth
claude
```

需要注意：

- 把 `.claude/worktrees/` 加入 `.gitignore`
- `.env`、本地配置、密钥文件不要默认复制到 worktree
- 每个 worktree 完成后检查 `git status`
- 合入前把分支整理成团队正常命名
- 清理无用 worktree，避免本地残留太多上下文

## 4. GitHub Copilot Cloud Agent：Issue 到 PR

GitHub Copilot Cloud Agent 的典型路径是从 Issue 或 GitHub 入口触发任务，Agent 分析需求、修改代码、提交到分支，并创建 PR。

适合：

- 小型修复
- 文档补充
- 测试补齐
- 低风险重构
- 有清晰验收条件的 Issue

不适合：

- 需求边界不清的大功能
- 需要线上数据判断的问题
- 牵涉安全、权限、计费、支付的高风险改动
- 需要跨团队拍板的架构调整

团队应该把 Issue 写得更像任务单：

```text
Goal:

Scope:

Out of scope:

Acceptance criteria:

Tests to run:

Risk:
```

## 5. Aider：git-first 本地结对

Aider 的特点是深度使用 Git：可以自动提交 AI 修改，也可以用 `/diff`、`/undo`、`/commit`、`/git` 管理变更。

它适合本地开发者快速结对，但团队要特别注意自动提交策略。

建议：

- 开始前先保证工作区干净
- 不要把人类未提交改动和 AI 修改混在一起
- 让 Aider 自动提交可以提高回退便利性，但合入前仍要人工整理 commit
- 对需要 pre-commit hook 的仓库，明确是否启用 `--git-commit-verify`

推荐流程：

```bash
git status
git switch -c ai/aider-small-fix
aider
git log --oneline -5
git diff main...HEAD
git rebase -i main
```

## 6. Cursor：多 Agent 与聚合 diff

Cursor 2.0 的官方发布强调 Composer、多 Agent 并行和更集中的 diff 审查体验。

这种工具形态对 Git 工作流的要求是：

- 多 Agent 任务必须有清晰边界
- 每个 Agent 的输出要能单独审查
- 聚合 diff 只能作为入口，不能代替文件级 Review
- 最终提交要按逻辑拆分，避免按工具运行结果直接提交

适合把 Cursor 用在：

- 多方案探索
- UI 或前端局部改造
- 文档和测试补充
- 小范围重构

## 7. 团队统一规则

不管使用哪种 AI 工具，团队都应该统一这些规则：

| 规则 | 推荐做法 |
| --- | --- |
| 任务边界 | 每次只处理一个明确目标 |
| 隔离方式 | 分支、worktree、sandbox 或远程环境 |
| diff 审查 | 人类先看 `git diff --stat` 和关键文件 |
| commit 拆分 | 按测试、实现、文档、配置拆开 |
| 验证结果 | PR 必须写清命令和结果 |
| 合入责任 | 人类 reviewer 承担最终判断 |
| 回滚路径 | 每个 PR 都要能说明如何撤销 |

## 8. 推荐最小流程

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

AI 工具越强，Git 工作流越要清楚。
