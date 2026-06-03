# 大厂工程实践决策图谱

这个页面把公开案例转成团队选型时可用的判断。

## 先按问题找案例

| 团队问题 | 可参考案例 | 对应主题文章 |
| --- | --- | --- |
| PR 太大，Review 成本高 | [Google Code Review](google-code-review.md)、[Meta Sapling](meta-sapling-stacked-commits.md) | [Pull Request 最佳实践](../03-team-collaboration/pull-request-best-practices.md)、[Stacked PR](../05-ai-native-development/stacked-pr-for-ai-generated-changes.md) |
| AI 生成大 diff，需要拆小 | [Google Code Review](google-code-review.md)、[Meta Sapling](meta-sapling-stacked-commits.md) | [AI Commit Splitting](../05-ai-native-development/ai-commit-splitting.md)、[AI 变更审查实战样例](../05-ai-native-development/ai-change-review-example.md) |
| PR 很多，主分支容易被组合变更破坏 | [Shopify Merge Queue](shopify-merge-queue.md)、[Merge Queue 合并队列实践](merge-queue-practices.md) | [Merge Queue](../04-github-engineering/merge-queue.md) |
| 固定发布窗口、release 分支、hotfix 回补 | [Microsoft Release Flow](microsoft-release-flow.md)、[腾讯 Gitflow](tencent-gitflow.md) | [Release Management](../04-github-engineering/release-management.md)、[Gitflow](../03-team-collaboration/gitflow.md) |
| 高频部署，需要把风险拆到日常发布中 | [Slack Deploys](slack-deploys.md)、[Netflix Spinnaker](netflix-spinnaker-release.md) | [Release Management](../04-github-engineering/release-management.md) |
| 仓库很大，clone、checkout、status 很慢 | [Microsoft Scalar](microsoft-scalar-large-repo.md)、[Uber GitFarm](uber-gitfarm.md) | [Large Repository Git Practices](../07-large-repo/large-repo-git-practices.md) |
| 主干开发支撑大规模协作 | [Google 主干开发](google-trunk-based-development.md)、[GitHub Flow 企业化实践](github-flow-enterprise.md) | [Trunk-Based Development](../03-team-collaboration/trunk-based-development.md)、[GitHub Flow](../03-team-collaboration/github-flow.md) |
| 多 feature 并行，需要灵活组合上线范围 | [阿里巴巴 AoneFlow](alibaba-aoneflow.md) | [Team Git Workflow Guide](../03-team-collaboration/team-git-workflow-guide.md)、[Gitflow](../03-team-collaboration/gitflow.md) |

## 四个核心判断

### 1. Google 小 CL 对 AI 大 diff 的启发

Google Code Review 强调小变更、清晰意图和长期代码健康。

AI 编程场景里，真正值得借鉴的是拆分原则：

- 测试、行为变化、重构、文档分开
- 每个变更都能讲清目标
- reviewer 能在有限时间内判断风险
- 大功能可以按连续小变更推进

对应阅读：

- [AI Commit Splitting](../05-ai-native-development/ai-commit-splitting.md)
- [AI 变更审查实战样例](../05-ai-native-development/ai-change-review-example.md)
- [Pull Request 最佳实践](../03-team-collaboration/pull-request-best-practices.md)

### 2. Shopify Merge Queue 对高并发 PR 团队的启发

当 PR 数量很大时，单个 PR 自己通过 CI 还不够。真正危险的是多个 PR 连续合入后的组合结果。

Shopify 的经验提醒我们，Merge Queue 的价值在于：

- 验证即将进入主分支的组合结果
- 减少 main 被合坏的概率
- 让失败原因、队列状态、重试路径对开发者可见
- 把 flaky tests 和慢 CI 暴露出来

对应阅读：

- [Merge Queue](../04-github-engineering/merge-queue.md)
- [企业 GitHub 协作配置栈](../04-github-engineering/enterprise-github-workflow-stack.md)

### 3. Microsoft Release Flow 对业务团队发布节奏的启发

很多业务团队并不能做到每个合入都立刻生产发布。此时 release 分支仍然有价值。

Microsoft Release Flow 的启发是：

- 主干负责日常开发
- release 分支负责发布窗口
- release 分支只接收稳定性修复
- 修复后必须同步回主干
- 发布记录要能追溯到 commit、tag、release note

对应阅读：

- [Release Management](../04-github-engineering/release-management.md)
- [Team Git Workflow Guide](../03-team-collaboration/team-git-workflow-guide.md)

### 4. Meta Sapling 对 stacked PR 的启发

大功能、大仓库、AI 大 diff 都会遇到同一个问题：单个变更太大后，人类很难稳定 Review。

Meta Sapling 的启发是：

- 用提交栈表达连续小变更
- 每一层都要能单独解释
- 下游变更依赖上游变更
- 工具要帮助开发者理解依赖关系和历史

对应阅读：

- [Stacked PR for AI-Generated Changes](../05-ai-native-development/stacked-pr-for-ai-generated-changes.md)
- [AI Commit Splitting](../05-ai-native-development/ai-commit-splitting.md)
- [Large Repository Git Practices](../07-large-repo/large-repo-git-practices.md)

## 迁移建议

不要照搬任何一家公司的完整流程。

更稳的做法是先回答：

1. 团队现在最痛的是 Review、发布、主分支稳定、大仓库性能，还是 AI 变更风险
2. 团队是否有足够快的 CI
3. 主分支是否要求随时可发布
4. 是否有固定发布窗口
5. 是否有明确 owner 和回滚路径

答案越清楚，越容易从这些案例里拿到可落地的做法。
