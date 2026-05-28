# Code Review 最佳实践

Code Review 的核心目标是确认变更意图、行为边界、风险和长期维护成本。

好的 Review 会找 bug，也会帮助团队保持共同的工程判断。

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

## Review 标准

Google 公开 Code Review 文档强调，代码审查的目标是让代码库长期健康持续变好。

这带来一个很实用的判断：如果一个 PR 明确改善了系统，且没有引入明显风险，reviewer 应该倾向于放行，不要因为非关键细节无限拖延。

团队可以把评论分成三类：

- 阻塞问题：正确性、安全、兼容性、明显维护风险
- 建议问题：命名、局部结构、可读性提升
- 可选问题：风格偏好、轻微优化、非当前 PR 必需内容

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

## 大型项目治理启发

Kubernetes 的 OWNERS 模型把 Review 拆成 reviewer 和 approver 两层，前者关注代码质量，后者关注整体接受标准、兼容性和长期影响。

企业团队可以借鉴这个分层：普通 reviewer 负责发现具体问题，code owner 或模块负责人负责最终批准。

## 模板

见 [Code Review Checklist](../08-templates/code-review-checklist.md)。

## 延伸阅读

- [GitHub Docs: About pull request reviews](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/about-pull-request-reviews)
- [Atlassian: Pull requests and code review](https://www.atlassian.com/git/tutorials/making-a-pull-request)
- [Google Engineering Practices: Code Review](https://google.github.io/eng-practices/review/)
- [Google Code Review 实践](../10-company-practices/google-code-review.md)
- [开源项目 Git 治理实践](../09-resources/open-source-governance-practices.md)
- [Gerrit 代码评审治理参考](../09-resources/gerrit-code-review-governance.md)
- [推荐阅读索引](../09-resources/recommended-reading.md)
