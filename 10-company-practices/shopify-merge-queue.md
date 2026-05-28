# Shopify Merge Queue 实践

原文链接：

- [Successfully Merging the Work of 1000+ Developers](https://shopify.engineering/successfully-merging-work-1000-developers)
- [Introducing the Merge Queue](https://shopify.engineering/introducing-the-merge-queue)

Shopify 的 Merge Queue 实践很适合解释大团队为什么不能靠人工点 merge。

公开文章里，Shopify 提到他们在单体代码库上采用 trunk-based workflow，每天大量变更进入 `master`。随着团队规模上升，直接合并会带来软冲突、部署积压、事故期间继续合入等问题。

## 三条安全规则

Shopify 总结过三条关键规则：

- `master` 必须保持绿色
- `master` 不能离生产太远
- 紧急修复必须足够快

这三条非常适合普通团队借鉴。

主分支绿色，意味着开发者可以随时基于它工作。

主分支接近生产，意味着发布风险和回滚复杂度更低。

紧急修复足够快，意味着事故期间不会被长队列拖住。

## Merge Queue 解决的问题

### 组合验证

单个 PR CI 通过，不代表多个 PR 连续合入后仍然通过。

Merge Queue 会把队列里的变更放到接近未来主分支的上下文中验证。

### 队列可控

事故期间可以锁队列，阻止普通变更继续进入主分支，把通道留给紧急修复。

### 审计清楚

紧急绕过、队列失败、PR 被移出队列，都应该留下记录。

## 对 GitHub 团队的启发

GitHub 原生 Merge Queue 已经提供通用能力，但 Shopify 的经验仍然有借鉴价值：

- 必须先治理 CI 稳定性
- 必须支持 `merge_group` 或等价事件
- 需要定义紧急通道
- flaky tests 会直接影响队列吞吐
- 队列批量大小要在吞吐和风险之间取平衡

## 适合什么团队

适合：

- 单仓库 PR 吞吐高
- 主分支必须随时可发布
- 多个团队同时向主分支合入
- CI 比较稳定
- 事故期间需要冻结普通合入

不适合：

- PR 很少
- CI 很慢
- flaky tests 很多
- 团队还没启用分支保护
