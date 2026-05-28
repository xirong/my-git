# Code Review 最佳实践

Code Review 的核心目标是确认变更意图、行为边界、风险和长期维护成本。

好的 Review 不只是找 bug，也是在帮助团队保持共同的工程判断。

## Review 顺序

建议按这个顺序看：

1. PR 目标是否清楚
2. diff 范围是否聚焦
3. 行为变化是否符合预期
4. 测试和验证是否可信
5. 错误处理和边界条件是否完整
6. 命名、结构和现有风格是否一致
7. 安全风险和回滚路径是否清楚

## Reviewer 应该问什么

- 这次改动解决的问题清楚吗
- 有没有无关改动
- 影响范围是否被说明
- 测试是否覆盖真实行为
- 命名和结构是否符合现有项目
- 出问题是否容易回滚

## Author 应该做什么

- 开 PR 前先自审 diff
- 主动说明风险和验证方式
- 对复杂设计补充上下文
- 收到 Review 后按问题逐条回应
- 不把未解释的大改动直接丢给 reviewer

## AI 生成代码怎么 Review

AI 代码尤其要注意：

- diff 是否过大
- 有没有悄悄改变行为边界
- 测试是否只是表面覆盖
- 是否引入不必要抽象
- 是否混入无关格式化和生成文件

详细见 [AI 生成代码 Review](../05-ai-native-development/ai-generated-code-review.md)。

## 模板

见 [Code Review Checklist](../08-templates/code-review-checklist.md)。

## 延伸阅读

- [GitHub Docs: About pull request reviews](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/about-pull-request-reviews)
- [Atlassian: Pull requests and code review](https://www.atlassian.com/git/tutorials/making-a-pull-request)
- [Google Engineering Practices: Code Review](https://google.github.io/eng-practices/review/)
- [推荐阅读索引](../09-resources/recommended-reading.md)
