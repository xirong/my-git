# Meta Sapling 与堆叠提交实践

原文链接：

- [Sapling: Source control that’s user-friendly and scalable](https://engineering.fb.com/2022/11/15/open-source/sapling-source-control-scalable/)
- [Scaling Mercurial at Facebook](https://engineering.fb.com/2014/01/07/core-infra/scaling-mercurial-at-facebook/)

## 1. Meta 面对的核心问题

Meta 公开资料里，Sapling 面向的是超大 monorepo 场景。

这类场景的难点不仅是文件多、提交多、分支多，还包括：

- 开发者很难理解自己所在的提交关系
- 大功能需要拆成多个连续小变更
- 历史修正和 rebase 成本高
- 代码评审需要理解一组相关变更
- clone、status、pull 等基础操作可能变慢

Sapling 的价值在于把可扩展性和工作流表达能力一起处理。

## 2. 堆叠提交解决什么问题

堆叠提交适合把一个大功能拆成多个可以单独 Review 的小步骤：

```text
commit A: add data model
commit B: add service logic
commit C: add API
commit D: add tests and docs
```

每个提交都可以被单独审查，但它们又保持依赖关系。

这对 AI 编程特别有启发：AI 很容易一次生成大 diff，人类需要把它拆回一组有顺序、可解释、可回滚的小变更。

## 3. Smartlog 带来的启发

Sapling 的 smartlog 强调让开发者直观看到自己本地提交、远端主线和相关分支的位置。

Git 用户虽然未必使用 Sapling，也可以借鉴这个思想：

- 用清楚的分支名表达任务
- 用小 commit 表达步骤
- 用 PR 描述说明提交关系
- 用 `git log --graph --oneline --decorate` 辅助理解历史
- 对复杂变更写出拆分顺序

## 4. 大仓库性能启发

Meta 早期 Scaling Mercurial 文章强调 Watchman、remote file log 等能力，用来减少 status、clone、pull、rebase 的成本。

对 Git 团队来说，对应的思路是：

- partial clone
- sparse checkout
- fsmonitor
- commit-graph
- background maintenance
- IDE 和构建系统按路径裁剪

## 5. 适合普通团队借鉴什么

普通团队不一定需要 Sapling，但可以借鉴这些做法：

- 大功能拆成堆叠小变更
- 每个 PR 有明确依赖和合入顺序
- AI 生成的大 diff 先拆 commit
- 大仓库优化要关注开发者日常命令体验
- 工具要帮开发者理解历史，不能只增加命令

## 6. 对本仓库的启发

堆叠提交、worktree、多 Agent 并行和 PR Review 可以连成一套 AI 时代工作流：

```text
AI 生成方案
-> 人类拆成提交栈
-> 每个提交单独 Review
-> CI 按栈顺序验证
-> 合入时保持主线清晰
```
