# Stacked PR for AI-Generated Changes

原文链接：

- [Google Small CLs](https://google.github.io/eng-practices/review/developer/small-cls.html)
- [GitHub Stacked PRs](https://github.github.com/gh-stack/)
- [GitHub Stacked PRs Overview](https://github.github.com/gh-stack/introduction/overview/)
- [Sapling ReviewStack](https://sapling-scm.com/docs/addons/reviewstack/)
- [Graphite: Stacked Diffs](https://graphite.com/guides/stacked-diffs)

AI 很容易一次生成一个看起来完整、实际很难审查的大 PR。

Stacked PR 的价值在于把一个大变更拆成一组有依赖关系的小 PR，让每一步都能被理解、验证和回滚。

## 1. 什么是 Stacked PR

普通 PR：

```text
main <- big-pr
```

Stacked PR：

```text
main <- pr-1 <- pr-2 <- pr-3
```

`pr-1` 先合入主线，`pr-2` 基于 `pr-1`，`pr-3` 基于 `pr-2`。

每个 PR 都解决一个更小的问题。

## 2. 为什么适合 AI 生成代码

AI 生成代码常见问题：

- 一次改太多文件
- 行为变化、重构、测试、文档混在一起
- reviewer 需要重建意图
- 回滚时很难只撤掉风险部分

Stacked PR 可以把它拆成：

```text
PR 1: add tests
PR 2: change implementation
PR 3: remove old helper
PR 4: update docs
```

这样 reviewer 可以逐步理解意图，CI 也能按层验证。

## 3. 拆分方式

### 按层拆

```text
data model -> service -> API -> UI
```

适合架构分层清楚的功能。

### 按行为拆

```text
support feature A -> support feature B -> enable flag
```

适合多个子能力。

### 按风险拆

```text
test only -> refactor no behavior change -> behavior change -> cleanup
```

适合 AI 重构或事故修复。

## 4. 操作规则

- 每个 PR 都要能单独解释
- 每个 PR 都要写清依赖关系
- 上游 PR 改动后，下游 PR 要及时 rebase
- 不要把生成文件和行为变化混在一个 PR
- 合入顺序要明确
- 回滚时优先从栈顶向下处理

## 5. 和 commit 拆分的关系

commit 拆分适合一个 PR 内部保持历史清楚。

Stacked PR 适合把一个大功能拆成多个 Review 单元。

可以组合使用：

```text
stacked PR
  -> each PR has small logical commits
```

## 6. 适合什么场景

适合：

- AI 一次生成大 diff
- 大功能逐步落地
- 跨层改动
- 重构后接行为变化
- 需要多个 owner Review 的变更

不适合：

- 很小的 bugfix
- 没有依赖关系的多个独立任务
- 团队还没有稳定 PR Review 习惯
