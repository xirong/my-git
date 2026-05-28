# Worktree for AI Agents

`git worktree` 适合把多个 AI 任务隔离到不同目录中，减少工作区互相污染。

## 适合场景

- 多个 Agent 并行探索不同方案
- 一个任务开发，一个任务 Review
- 需要同时保留多个分支的运行环境
- 不想反复 stash 和切分支

## 基础命令

```bash
git worktree add ../project-task-a -b ai/task-a
git worktree add ../project-task-b -b ai/task-b
git worktree list
git worktree remove ../project-task-a
```

## 推荐规则

- 一个 worktree 只服务一个任务
- 分支名写清 AI 任务意图
- 任务结束后及时删除 worktree
- 合入前统一回到主工作区做最终检查
- 不默认复制 `.env`、密钥、生产配置到 AI worktree
- 如果工具自动创建 worktree，要把对应目录加入 `.gitignore`

## Claude Code 场景

Claude Code 官方支持通过 `--worktree` 创建隔离会话：

```bash
claude --worktree feature-auth
claude --worktree bugfix-payment-timeout
```

这类自动 worktree 适合并行探索，但合入前仍要回到 Git 视角检查：

```bash
git worktree list
git status
git diff --stat
```

## 延伸阅读

- [git worktree](https://git-scm.com/docs/git-worktree)
- [Claude Code Worktrees](https://code.claude.com/docs/en/worktrees)
- [AI 编程工具的 Git 集成实践](ai-coding-tools-git-integration.md)
