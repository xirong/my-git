# Git 学习路径

Git 不适合靠背命令学习。

更有效的方式，是按真实工作场景建立能力。

## 第一阶段：建立心智模型

先理解四个区域：

```text
工作区 -> 暂存区 -> 本地仓库 -> 远端仓库
```

建议阅读：

1. [Git 心智模型](git-mental-model.md)
2. [Git 基础命令](git-basic-commands.md)
3. [为什么使用 Git](why-git.md)

掌握目标：

- 看懂 `git status`
- 知道 `git add` 和 `git commit` 的关系
- 知道本地 commit 和远端 push 的区别

## 第二阶段：日常开发

建议阅读：

1. [日常 Git 命令](../02-daily-workflow/everyday-git-commands.md)
2. [分支与合并](../02-daily-workflow/branch-and-merge.md)
3. [Rebase 与 Merge](../02-daily-workflow/rebase-vs-merge.md)
4. [Stash](../02-daily-workflow/stash.md)

掌握目标：

- 每个任务创建分支
- 提交前会看 diff
- 知道什么时候用 stash
- 知道本地 rebase 和公共历史的风险

## 第三阶段：团队协作

建议阅读：

1. [团队 Git 工作流指南](../03-team-collaboration/team-git-workflow-guide.md)
2. [Pull Request 最佳实践](../03-team-collaboration/pull-request-best-practices.md)
3. [Code Review 最佳实践](../03-team-collaboration/code-review-best-practices.md)

掌握目标：

- 会写可 Review 的 PR
- 会拆小 commit 和小 PR
- 理解不同团队为什么选择不同工作流

## 第四阶段：故障恢复

建议阅读：

1. [Git 高频事故处理手册](../06-troubleshooting/git-troubleshooting-playbook.md)
2. [Undo Anything](../06-troubleshooting/undo-anything.md)
3. [Recover Lost Commit](../06-troubleshooting/recover-lost-commit.md)

掌握目标：

- 知道 reflog 能救什么
- 公共 commit 优先 revert
- 高风险命令执行前先保存现场

## 第五阶段：AI 编程时代的 Git

建议阅读：

1. [AI Native Git Workflow](../05-ai-native-development/ai-native-git-workflow.md)
2. [AI 生成代码 Review](../05-ai-native-development/ai-generated-code-review.md)
3. [Worktree for AI Agents](../05-ai-native-development/worktree-for-ai-agents.md)

掌握目标：

- AI 改完先审 diff
- 大 diff 先拆 commit
- 多 Agent 并行用分支和 worktree 隔离

## 延伸阅读

- [Pro Git](https://git-scm.com/book/en/v2)
- [Git Cheat Sheet](https://git-scm.com/cheat-sheet.pdf)
- [Atlassian Git tutorials](https://www.atlassian.com/git)
- [推荐阅读索引](../09-resources/recommended-reading.md)
