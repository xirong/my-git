# Pull Request Best Practices

PR 的目标是让一次变更可以被理解、审查、验证和回滚。

## 推荐规则

- 一个 PR 只解决一个问题
- 标题写清行为变化
- 描述里写清 why、how tested、risk、rollback
- 不混入格式化噪音
- 重构和行为变化分开
- 合入前通过 CI
- 出问题优先 revert

## PR 大小

如果 reviewer 无法在合理时间内审完，PR 就太大了。

可以拆成：

- 准备性重构
- 行为变更
- 测试补充
- 文档更新
- 配置变更

小 PR 的价值主要在于更容易理解、更容易回滚、更适合堆叠审查，不要机械承诺“小 PR 一定合并更快”。

有研究发现，变更大小和合并耗时之间并没有稳定相关性。团队仍然应该鼓励小 PR，但理由要放在可审查性、可验证性和可回滚性上，见 [Git 工作流经验研究笔记](../09-resources/empirical-git-workflow-research.md)。

## 堆叠 PR

当一个功能天然较大，可以拆成一组有依赖关系的小 PR：

```text
PR 1: data model
PR 2: service logic
PR 3: API
PR 4: tests and docs
```

这种方式适合大功能、AI 生成大 diff、跨模块重构。

注意事项：

- 每个 PR 要能单独解释
- PR 描述写清依赖关系
- 合入顺序要明确
- 后续 PR 要随着前序变更及时 rebase

## 模板

直接使用 [Pull Request Template](../08-templates/pull-request-template.md)。

## 一个好的 PR 应该包含什么

- 清楚的标题
- 简短的背景说明
- 聚焦的 diff
- 可复现的验证方式
- 风险说明
- 回滚方案
- 必要截图或日志

## AI 编程场景

AI 生成代码后，PR 描述不能只写“AI generated”。

至少要写清：

- 人类希望它解决什么问题
- AI 实际改了哪些文件
- 哪些 diff 已经人工检查
- 跑过哪些验证
- 还有哪些风险需要 reviewer 重点看

## 延伸阅读

- [GitHub Docs: About pull requests](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests)
- [GitHub Docs: About pull request reviews](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/about-pull-request-reviews)
- [Atlassian: Making a Pull Request](https://www.atlassian.com/git/tutorials/making-a-pull-request)
- [Meta Sapling 与堆叠提交实践](../10-company-practices/meta-sapling-stacked-commits.md)
- [Git 工作流经验研究笔记](../09-resources/empirical-git-workflow-research.md)
- [推荐阅读索引](../09-resources/recommended-reading.md)
