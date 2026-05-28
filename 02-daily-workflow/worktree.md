# Worktree

`git worktree` 允许同一个仓库同时 checkout 多个分支到不同目录。

它适合需要并行处理多个任务的人，尤其适合 hotfix、长期分支维护和 AI Agent 并行开发。

## 适合场景

- 需要同时处理多个分支
- 临时修 hotfix
- 不想频繁 stash
- 多个 AI Agent 并行处理任务
- 一个分支跑测试，另一个分支继续开发

## 基础命令

创建新的 worktree：

```bash
git worktree add ../project-hotfix -b hotfix/urgent-fix
```

查看 worktree：

```bash
git worktree list
```

删除 worktree：

```bash
git worktree remove ../project-hotfix
```

清理无效记录：

```bash
git worktree prune
```

## 和 stash 的区别

`stash` 适合临时保存当前未完成改动。

`worktree` 适合同时保留多个完整工作区。

如果你一天内频繁在多个分支切换，worktree 通常比 stash 更清楚。

## AI 编程场景

多个 AI Agent 不建议写同一个工作区。

推荐：

```bash
git worktree add ../repo-agent-a -b ai/task-a
git worktree add ../repo-agent-b -b ai/task-b
```

每个 Agent 一个分支，一个目录，最后由人类整理和合入。

## 延伸阅读

- [git worktree 官方文档](https://git-scm.com/docs/git-worktree)
- [Worktree for AI Agents](../05-ai-native-development/worktree-for-ai-agents.md)
- [AI Native Git Workflow](../05-ai-native-development/ai-native-git-workflow.md)
- [推荐阅读索引](../09-resources/recommended-reading.md)
