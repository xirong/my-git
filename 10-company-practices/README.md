# 大厂工程实践索引

这个目录收录公开资料中的 Git、分支管理、代码评审、CI、Monorepo 和工程治理实践。

这里不追求罗列资料，重点是把公开案例里的工程判断讲清楚：什么问题、什么做法、适合什么团队、迁移时要注意什么。

## 已整理案例

| 案例 | 适合阅读场景 |
| --- | --- |
| [阿里巴巴 AoneFlow 分支管理实践](alibaba-aoneflow.md) | 多 feature 并行、按环境组织 release 分支、需要灵活调整上线范围 |
| [腾讯 Gitflow 分支规范实践](tencent-gitflow.md) | 客户端、SDK、企业交付产品，需要稳定的 release / hotfix 流程 |
| [字节跳动 Git 工作流与研发设施实践](bytedance-git-workflow.md) | 大规模研发组织，需要把 Git 流程、权限、CI、发布平台串起来 |
| [GitHub Flow 企业化实践](github-flow-enterprise.md) | GitHub Flow 如何配合分支保护、CODEOWNERS、Rulesets、Merge Queue 变成企业协作链路 |
| [Google 主干开发与版本控制实践](google-trunk-based-development.md) | 想理解主干开发为什么能支撑大规模协作 |
| [Google Code Review 实践](google-code-review.md) | 想建立团队 Review 标准，避免 PR 被低价值评论拖慢 |
| [Microsoft Scalar 与大仓库 Git 实践](microsoft-scalar-large-repo.md) | 大仓库 clone、status、checkout、历史对象下载太慢 |
| [Meta Sapling 与堆叠提交实践](meta-sapling-stacked-commits.md) | 大功能拆成提交栈、AI 大 diff 拆分、超大仓库开发体验 |
| [Uber GitFarm 与 Git 服务化实践](uber-gitfarm.md) | Monorepo 自动化系统频繁 clone / checkout 成为基础设施瓶颈 |
| [Netflix Spinnaker 与发布流水线实践](netflix-spinnaker-release.md) | 分支模型之外，如何把发布过程做成可追踪、可审批、可回滚的流水线 |
| [Merge Queue 合并队列实践](merge-queue-practices.md) | PR 多、主分支繁忙、单个 PR CI 通过但组合合入风险高 |
| [Microsoft Release Flow](microsoft-release-flow.md) | 主干开发配合 release 分支，适合有固定发布窗口的产品团队 |
| [Shopify Merge Queue 实践](shopify-merge-queue.md) | 大规模团队如何用合并队列保护主分支稳定 |
| [Slack Deploys 实践](slack-deploys.md) | 高频部署团队如何用小批量、自动化检查和快速回滚降低发布风险 |
