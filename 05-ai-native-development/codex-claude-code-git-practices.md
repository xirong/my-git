# Codex / Claude Code Git 实践

[English](05-ai-native-development_en/codex-claude-code-git-practices_en.md) | 中文

Codex、Claude Code 这类 AI 编程工具会让代码修改速度变快，也会让 Git 工作区更容易变乱。

这篇只讨论一个问题：使用 AI 编程工具时，如何让 Git 历史仍然清楚、可审查、可回滚。工具能力、官方来源和版本差异由[AI 编程工具的 Git 集成实践](ai-coding-tools-git-integration.md)集中维护；这里保留跨工具都适用的 Git 实践与流程。

## 核心原则

### 1. 每个任务一个分支

不要让 AI 直接在主分支上探索。

`<integration-branch>` 是仓库实际使用的集成分支，例如 `main`、`master` 或 `develop`。先让 `git status --porcelain` 没有输出；有其他 owner 的编辑时，保留现场并使用独立 worktree。

推荐：

```bash
git status --porcelain
git switch <integration-branch>
git pull --rebase origin <integration-branch>
git switch -c ai/refactor-order-validator
```

如果最终要合入，可以整理成正常业务分支名：

```text
fix/order-timeout-validation
feat/github-governance-guide
```

### 2. 多 Agent 并行用 worktree

工具能否创建或管理 worktree，要以[工具事实速查](ai-coding-tools-git-integration.md)中的官方来源和本机版本为准。本节只处理 Git 层面的要求：并行任务不能共享同一个工作目录。

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

工具启动命令会随版本变化；确认方式见[工具事实速查](ai-coding-tools-git-integration.md)。

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

部分暂存前先确认这是干净或隔离的任务工作区，`git diff --cached` 里没有其他任务的内容。发现其他 owner 的 staged、unstaged 或 untracked 编辑时，停止在这里拆分，不要用 reset 或清理命令腾位置。

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
重点检查行为范围、测试有效性、安全风险、无关改动。
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

## 工具无关的执行约定

- 任务说明要写清目标、范围、验收方式和风险，避免无关重构混入。
- 每个并行任务绑定独立分支或 worktree，完成后用清楚的分支和目录名保留上下文。
- 合入前由人检查 diff、测试结果和回滚路径；远程任务额外保留 PR、日志、验证命令和人工复核记录。
- `.env`、本地配置和密钥文件不应默认复制到临时工作区。
- 任务完成后确认 worktree 状态，再清理已经不需要的目录：

```bash
git worktree list
git worktree remove ../repo-task-a
```

各工具的当前能力和 Git 集成差异见[AI 编程工具的 Git 集成实践](ai-coding-tools-git-integration.md)。

## 常见反模式

### 1. 同一个目录里跑多个 AI 工具

风险：互相覆盖文件，分支状态混乱。

建议：一个任务一个 worktree。

### 2. AI 改完直接 commit

风险：无关文件、调试代码、配置变更混入。

建议：先 `git diff --stat`，再 `git add -p`。

### 3. 让 AI 自行决定合入

风险：工具缺少团队发布、回滚、责任边界上下文。

建议：AI 可以给建议，合入决定由人负责。

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
