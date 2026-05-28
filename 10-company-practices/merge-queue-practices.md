# Merge Queue 合并队列实践

原文链接：

- [GitHub Docs: Managing a merge queue](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue)
- [GitHub Docs: merge_group event](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#merge_group)
- [Buildkite: Using GitHub Merge Queue in pipelines](https://buildkite.com/resources/blog/using-github-mergequeue-in-pipelines/)
- [Mergify: The origin story of merge queues](https://mergify.com/blog/the-origin-story-of-merge-queues/)

## 1. Merge Queue 解决什么问题

高并发 PR 团队会遇到一个经典问题：

```text
main: A
PR 1: A + B，CI 通过
PR 2: A + C，CI 通过
```

两个 PR 单独看都没问题，但 PR 1 合入后，PR 2 实际合入的是：

```text
A + B + C
```

这个组合结果没有被验证过，主分支就可能被破坏。

Merge Queue 的价值是，在真正合入前先构造接近合入后的组合结果，对它执行必需检查。

## 2. 适合什么团队

适合：

- PR 合入频率高
- 主分支必须稳定
- 必需检查已经比较完整
- CI 资源足够
- 团队愿意接受排队合入

不适合：

- PR 很少
- CI 经常失败或很慢
- 检查项命名不稳定
- 没有主分支保护
- 紧急修复流程还没定义

## 3. 启用前的准备

### 稳定的必需检查

Merge Queue 依赖 required status checks。

如果检查项经常改名，或者不同 PR 上检查项不一致，队列会变得很难维护。

### CI 支持 `merge_group`

GitHub merge queue 会触发 `merge_group` 事件。

如果团队使用 GitHub Actions，要确保关键工作流响应这个事件：

```yaml
on:
  pull_request:
  merge_group:
```

如果使用外部 CI，也要确认它能识别 merge queue 创建的临时引用或对应事件。

### 明确紧急通道

Merge Queue 会增加合入等待时间。

团队要提前定义 hotfix 怎么处理，哪些人可以临时绕过队列，以及绕过后如何补验证。

## 4. 落地步骤

推荐顺序：

1. 先启用分支保护
2. 配置必需检查
3. 统一 CI 检查名称
4. 在 Actions 或外部 CI 中支持 `merge_group`
5. 小范围启用 Merge Queue
6. 观察队列时长、失败率、CI 消耗
7. 再扩展到主仓库或关键分支

## 5. 常见失败模式

### CI 太慢导致队列堆积

Merge Queue 会把“合入前组合验证”显性化。

如果 CI 本来就慢，队列会让这个问题更明显，需要先优化测试分层和并发能力。

### flaky tests 让队列反复失败

不稳定测试会让队列吞吐下降。

启用前最好先治理 flaky tests，至少要能标记、隔离和重跑。

### 队列规则没人理解

开发者需要知道：

- PR 什么时候进入队列
- 进入队列后还能不能继续 push
- 队列失败后谁处理
- 检查失败是自己 PR 问题还是组合问题

这些规则应写进团队 PR 指南。

## 6. 对本仓库的启发

Merge Queue 不是高级团队才需要的“复杂功能”。

当 PR 数量增长到一定程度，它解决的是主分支稳定性的基本问题。

但启用顺序很关键，先有稳定 CI 和分支保护，再谈合并队列。

