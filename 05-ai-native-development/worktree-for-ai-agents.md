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

## 延伸阅读

- [git worktree](https://git-scm.com/docs/git-worktree)
