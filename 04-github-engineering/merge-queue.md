# Merge Queue

Merge Queue 适合 PR 合入频繁、主分支繁忙的团队。

它解决的问题是：每个 PR 单独看都通过 CI，但多个 PR 连续合入后，组合结果可能破坏主分支。

## 问题

假设两个 PR 都基于同一个 `main`：

```text
main: A
PR 1: A + B
PR 2: A + C
```

PR 1 和 PR 2 单独跑 CI 都通过。

但 PR 1 先合入后，PR 2 实际要合入的是：

```text
A + B + C
```

这个组合结果没有被验证过，就可能把主分支弄坏。

## 适合场景

- 每天有大量 PR 合入主分支
- 主分支必须保持稳定
- CI 足够自动化
- 团队能接受排队合入
- 仓库已经启用 required status checks

## 不适合场景

- PR 很少
- CI 很慢且资源不足
- 团队还没有稳定的基础检查
- 主分支不要求随时可发布

## 使用前提

启用 Merge Queue 前，先确认：

- CI 能处理 merge queue 相关事件
- required checks 名称稳定
- 团队知道 PR 进入队列后的行为
- 紧急 hotfix 有明确处理路径

## 落地要点

如果使用 GitHub Actions，关键工作流要响应 `merge_group` 事件：

```yaml
on:
  pull_request:
  merge_group:
```

Merge Queue 适合在分支保护和必需检查稳定之后启用。CI 如果很慢，或者 flaky tests 很多，队列会把这些问题放大。

Shopify 的公开实践很有参考价值：当团队规模变大后，单个 PR 通过 CI 已经不够，还要验证排队后的组合结果，并且要把队列状态、失败原因、重试路径展示给开发者。Merge Queue 的核心价值，是把合入主分支前的组合风险提前暴露出来。

## 延伸阅读

- [Merge Queue 合并队列实践](../10-company-practices/merge-queue-practices.md)
- [Shopify Merge Queue 实践](../10-company-practices/shopify-merge-queue.md)
- [企业 GitHub 协作配置栈](enterprise-github-workflow-stack.md)
- [GitHub protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
- [GitHub Docs: Managing a merge queue](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue)
- [GitHub Docs: merge_group event](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#merge_group)
- [GitHub 工程治理手册](github-engineering-governance.md)
- [推荐阅读索引](../09-resources/recommended-reading.md)
