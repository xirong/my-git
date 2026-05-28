# AI Native Git Workflow

AI 让写代码变便宜，但让验证代码变贵。

Git 在 AI 编程时代的新价值，是把 AI 生成的大块变化重新切回人类可以理解、可以审查、可以回滚的工程单元。

## 1. 新风险

AI 改代码通常有几个特点：

- diff 变大，文件数量变多
- 代码看起来合理，但行为边界可能被悄悄改掉
- 测试可能只是覆盖了表面路径
- 抽象和命名可能脱离原项目习惯
- 依赖、配置、生成文件容易被顺手带进去
- 多个 Agent 并行时，分支和工作区容易互相污染

所以 AI 编程后的 Git 工作流，重点是让变更重新变小、变清楚、可验证，不能只追求更快提交。

不同 AI 工具的 Git 集成方式不同，但目标一致：把 AI 修改限制在可审查、可回滚的工程单元里。Codex 更强调远程环境和 sandbox，Claude Code 强调 worktree 隔离，Copilot Cloud Agent 更贴近 Issue 到 PR，Aider 则把本地 Git 提交和撤销作为核心体验。详细对比见 [AI 编程工具的 Git 集成实践](ai-coding-tools-git-integration.md)。

## 2. 核心原则

### 小提交

一个 commit 只表达一个完整意图。

如果 AI 一次改了 20 个文件，先审 diff，再拆成多个 commit。

### 隔离分支

每个任务一个分支。

AI 探索性改动不要直接落在 `main`、`master`、`develop` 或长期维护分支上。

### 可审查 diff

提交前先看：

```bash
git status
git diff
git diff --stat
```

如果你无法在几分钟内讲清这次 diff 为什么存在，就先不要提交。

### 可复现验证

每次 AI 改动都要留下验证方式：

- 单元测试
- 集成测试
- 编译
- 静态检查
- 本地手工回归
- 线上前置验证说明

### 人类负责合入

AI 可以生成代码、解释 diff、做第一轮 Review，但最终合入决定必须由人类负责。

### 快速回滚

每个 PR 都要能回答：

- 出问题怎么回滚
- 是否可用 `git revert`
- 是否涉及数据库、配置、消息、外部依赖
- 回滚后是否需要补偿数据

## 3. 推荐工作流

### 第 1 步：创建隔离分支

```bash
git switch main
git pull --rebase
git switch -c feat/ai-assisted-short-task
```

### 第 2 步：复杂任务使用 worktree

适合并行让多个 AI 工具处理不同任务：

```bash
git worktree add ../my-project-task-a -b feat/task-a
git worktree add ../my-project-task-b -b feat/task-b
```

官方文档见 [git worktree](https://git-scm.com/docs/git-worktree)。

### 第 3 步：让 AI 修改代码

给 AI 的任务要足够具体：

```text
只修改订单校验逻辑，不调整接口签名，不改动无关格式化。
完成后列出改动文件、行为变化、验证方式和潜在风险。
```

### 第 4 步：先审 diff，再提交

```bash
git status
git diff --stat
git diff
```

重点看：

- 是否有无关文件
- 是否有格式化噪音
- 是否有配置、锁文件、生成文件变更
- 是否有 public API 行为变化
- 是否改了测试但没改实现，或改了实现但没改测试

### 第 5 步：拆 commit

用交互式暂存拆分变更：

```bash
git add -p
git commit -m "fix(auth): handle expired token"
```

如果已经提交成一个大 commit，可以用：

```bash
git reset --soft HEAD~1
git add -p
```

注意：只在本地未 push 的 commit 上这样做。

如果 AI 生成的是一个跨层大功能，可以考虑拆成一组有依赖关系的小 PR，让测试、实现、清理、文档分层进入 Review。详细见 [Stacked PR for AI-Generated Changes](stacked-pr-for-ai-generated-changes.md)。

### 第 6 步：运行验证

根据项目类型选择最小必要验证：

```bash
npm test
mvn test
go test ./...
pytest
```

没有测试时，也要写清本地验证路径。

### 第 7 步：让 AI 做第一轮 Review

可以让 AI 按固定清单检查：

```text
请基于当前 git diff 做 Review。
重点检查：行为边界、错误处理、兼容性、测试有效性、安全风险、无关改动。
不要泛泛总结，只列出具体风险和文件位置。
```

### 第 8 步：创建 PR

PR 描述至少包含：

- What changed
- Why
- How tested
- Risk
- Rollback plan

可以直接使用 [PR Template](../08-templates/pull-request-template.md)。

### 第 9 步：CI 通过后再合入

AI 代码尤其要依赖 CI 做最低质量验收。

如果团队使用 GitHub，建议配合分支保护、必需状态检查、Review 要求，见 [GitHub branch protection docs](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)。

## 4. Commit 策略

### 推荐拆法

```text
docs: explain the behavior
test: cover the failing case
fix: change the implementation
refactor: simplify local helper
```

### 不推荐

```text
fix all ai changes
update files
misc
wip
```

### 判断标准

一个 commit 应该能独立回答：

- 为什么改
- 改了什么行为
- 怎么验证
- 出问题怎么回退

## 5. 分支策略

### 单任务

```text
feat/short-description
fix/bug-description
docs/topic-name
```

### AI 探索

```text
ai/experiment-short-description
```

### 多 Agent 并行

```text
ai/task-a
ai/task-b
ai/review-task-a
```

多 Agent 最好配合 `git worktree`，避免多个工具在同一个工作区抢文件。

## 6. Human Review Checklist

- [ ] diff 足够小，可以被认真审完
- [ ] 没有无关格式化和生成文件
- [ ] 行为变化写清楚了
- [ ] public API、配置、数据结构变化被标注
- [ ] 测试覆盖了真实变更
- [ ] 验证命令可复现
- [ ] 回滚方式清楚
- [ ] 人类 reviewer 理解并接受这次变化

完整模板见 [AI Code Review Checklist](../08-templates/ai-code-review-checklist.md)。

跨层或跨 owner 的大变更，优先拆成 stacked PR，避免一个 PR 同时承担需求解释、代码理解、测试验证和风险判断。

## 7. 常见反模式

### 一次让 AI 改完整个模块

风险：diff 太大，Review 失效。

建议：先让 AI 输出计划，再按小任务逐步改。

### AI 改完直接 commit

风险：无关文件、调试代码、配置改动混入。

建议：永远先 `git diff`。

### 让 AI 同时修 bug、重构、补测试、改文档

风险：行为变化和结构变化混在一起。

建议：拆成多个 commit 或多个 PR。

### 用 force push 覆盖协作者分支

风险：别人基于旧提交做的工作丢失。

建议：公共分支优先用新 commit 修正，确实需要重写历史时先确认协作者状态。

## 8. 示例流程

```bash
git switch main
git pull --rebase
git switch -c fix/order-timeout-validation

# AI modifies files

git status
git diff --stat
git diff

git add -p
git commit -m "test(order): cover timeout validation"

git add -p
git commit -m "fix(order): reject expired timeout config"

mvn test -pl order-service -Dtest=OrderTimeoutValidatorTest

git push -u origin fix/order-timeout-validation
```

PR 中写清：

```text
What changed:
Add validation for expired timeout config.

How tested:
mvn test -pl order-service -Dtest=OrderTimeoutValidatorTest

Risk:
Low. Only affects invalid timeout config path.

Rollback:
Revert this PR.
```

## 延伸阅读

- [git worktree](https://git-scm.com/docs/git-worktree)
- [AI 变更审查实战样例](ai-change-review-example.md)
- [AI 编程工具的 Git 集成实践](ai-coding-tools-git-integration.md)
- [GitHub protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
- [GitHub rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets)
- [Responsible use of GitHub Copilot code review](https://docs.github.com/en/copilot/responsible-use/code-review)
- [推荐阅读索引](../09-resources/recommended-reading.md)
