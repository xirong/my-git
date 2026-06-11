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

## 5. 用原生 git 操作一个栈

创建一个两层的栈：

```bash
git switch -c pr-1 main
# 提交 pr-1 的内容
git switch -c pr-2 pr-1
# 提交 pr-2 的内容

gh pr create --base main --head pr-1
gh pr create --base pr-1 --head pr-2
```

下游 PR 的 base 指向上游分支，reviewer 在 `pr-2` 里只会看到 `pr-2` 自己的改动。

上游改动后更新下游：

```bash
git switch pr-2
git rebase pr-1
git push --force-with-lease origin pr-2
```

栈比较深时，在栈顶一次更新整串（Git 2.38+）：

```bash
git switch pr-3
git rebase main --update-refs
git push --force-with-lease origin pr-1 pr-2 pr-3
```

`--update-refs` 会在 rebase 的同时移动栈里其他分支的指针，省去逐层手工 rebase。

`pr-1` 合入主线后，把已合入的提交从 `pr-2` 的历史里去掉：

```bash
git switch pr-2
git rebase --onto main pr-1
git push --force-with-lease origin pr-2
```

GitHub 会在 base 分支删除后自动把下游 PR 的 base 改回 `main`，rebase 仍然要自己完成。

风险提示：force push 只用于自己的栈分支，必须带 `--force-with-lease`，主分支永远禁止 force push。

## 6. 栈管理工具

栈深超过两三层，或者团队多人都在用栈时，建议引入工具代替手工 rebase。以 Graphite CLI 为例：

```bash
gt create -am "add tests"    # 在当前分支之上创建新的栈分支
gt modify -a                 # 修改当前分支，自动 restack 上层分支
gt submit --stack            # 整串推送并创建或更新 PR
gt sync                      # 拉取主线、清理已合并分支、restack
```

Sapling 的 ReviewStack 提供类似的栈式 Review 视图。

建议先用原生命令理解栈的原理，再决定要不要为工具调整团队工作流。

## 7. 和 commit 拆分的关系

commit 拆分适合一个 PR 内部保持历史清楚。

Stacked PR 适合把一个大功能拆成多个 Review 单元。

可以组合使用：

```text
stacked PR
  -> each PR has small logical commits
```

Meta Sapling 的公开实践说明，提交栈适合表达一组连续小变更。AI 生成大 diff 后，可以借鉴这个思路，把“大块结果”改造成“可审查的变更序列”。更多案例对照见 [大厂工程实践决策图谱](../10-company-practices/company-practices-decision-map.md)。

## 8. 适合什么场景

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

## 延伸阅读

- [git rebase 官方文档](https://git-scm.com/docs/git-rebase)
- [Graphite CLI Command Cheatsheet](https://graphite.dev/docs/cheatsheet)
- [Meta Sapling 与堆叠提交实践](../10-company-practices/meta-sapling-stacked-commits.md)
- [Google Code Review 实践](../10-company-practices/google-code-review.md)
- [大厂工程实践决策图谱](../10-company-practices/company-practices-decision-map.md)
