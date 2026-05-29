# 为什么使用 Git

Git 解决的核心问题，是多人协作时如何记录变化、交换变化、审查变化和恢复变化。

如果只把 Git 当成“上传代码的命令”，会很容易在冲突、回滚、分支协作、线上事故时手忙脚乱。真正理解 Git，要把它看成一套工程协作系统。

## Git 帮你解决什么

### 1. 记录变化

每个 commit 都是一份可追踪的工程记录。

好的 commit 能回答：

- 为什么改
- 改了什么
- 谁改的
- 什么时候改的
- 出问题时如何定位

### 2. 隔离工作

分支让不同任务互不影响。

你可以同时处理：

- 一个新功能
- 一个线上 hotfix
- 一次重构实验
- 一个 AI Agent 生成的候选方案

只要分支边界清楚，团队协作就不会因为一个人的本地改动阻塞所有人。

### 3. 支持审查

Git 和 GitHub / GitLab 结合后，Pull Request 会变成团队审查入口。

团队可以在合入前检查：

- diff 是否聚焦
- 行为变化是否清楚
- 测试是否足够
- 风险是否可接受
- 回滚方式是否明确

### 4. 快速恢复

Git 不只负责保存代码，也负责事故恢复。

常见场景包括：

- 提交到了错误分支
- reset 错了
- rebase 冲突处理乱了
- merge 了错误分支
- commit 丢了
- secret 提交进历史

这些问题的处理方式，见 [Git 高频事故处理手册](../06-troubleshooting/git-troubleshooting-playbook.md)。

## Git 在 AI 编程时代为什么更重要

AI 让代码生成速度变快，但也让变更规模更大、边界更容易变模糊。

Git 的新价值，是把 AI 生成的大块改动切回人类可以理解、可以审查、可以回滚的工程单元。

如果你正在使用 Codex、Claude Code、Cursor、Cline 或其他 AI 编程工具，建议优先阅读 [AI Native Git Workflow](../05-ai-native-development/ai-native-git-workflow.md)。

## 学习建议

先掌握这条主线：

```text
工作区 -> 暂存区 -> 本地仓库 -> 远端仓库
```

再掌握三类能力：

1. 日常提交和同步
2. 分支协作和 PR Review
3. 故障恢复和风险控制

原有文章见归档目录 [why-git.md](../09-resources/legacy/why-git.md)。

## 延伸阅读

- [Pro Git](https://git-scm.com/book/en/v2)
- [Git 官方文档](https://git-scm.com/docs)
- [Atlassian Git tutorials](https://www.atlassian.com/git)
- [推荐阅读索引](../09-resources/recommended-reading.md)
