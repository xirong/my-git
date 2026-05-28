# Team Git Workflow Guide

没有万能的 Git 工作流。

工作流本质上是在速度、安全、发布频率、团队规模、产品复杂度之间做取舍。

## 1. 选择矩阵

| 团队 / 产品 | 推荐工作流 | 适合原因 |
| --- | --- | --- |
| 小团队 Web 产品 | GitHub Flow | 分支短、合入快、发布频繁 |
| 高频后端服务 | Trunk-Based Development | 主干稳定、CI 反馈快、回滚清晰 |
| 中大型业务团队 | Feature Branch + Protected Main | 兼顾并行开发和主分支稳定 |
| 开源项目 | Fork + Pull Request | 降低外部贡献者写权限风险 |
| 多版本交付产品 | Release Branch | 需要维护多个发布版本 |
| 多环境 SaaS / 企业内部平台 | GitLab Flow | 合入频率和上线频率不同，需要 production / stable 分支 |
| 移动端 / 客户端 | Release Branch + Hotfix | 发版周期长，线上版本分散 |
| 老系统维护 | Conservative Branch Strategy | 变更少、风险高，优先稳定 |

## 2. GitHub Flow

### 适合

- 小团队
- Web 服务
- 高频发布
- CI 完整
- 回滚成本可控

### 流程

```text
main -> feature branch -> pull request -> review -> CI -> merge -> deploy
```

### 团队规则

- `main` 始终可部署
- 所有变更通过 PR
- PR 尽量小
- 合入前必须通过 CI
- 出问题优先 revert

## 3. Trunk-Based Development

### 适合

- 自动化测试成熟
- 主干发布频繁
- 团队有较强工程纪律
- 使用 feature flag 控制未完成能力

### 流程

```text
short-lived branch -> main -> CI -> deploy
```

### 风险

- CI 不稳定时会拖垮团队节奏
- 缺少 feature flag 时，未完成能力容易暴露
- 大团队需要更强的代码所有权和 Review 规则

## 3.1 GitHub Flow 和 Trunk-Based Development 的关系

GitHub Flow 更像 GitHub 平台上的轻量实现路径：短分支、PR、Review、合入默认分支。

Trunk-Based Development 更像组织原则：分支生命周期极短，团队围绕主干持续集成，主干保持可发布。

当 GitHub Flow 加上必需 CI、CODEOWNERS、Rulesets、Merge Queue、feature flag 和 release from main，它就已经很接近 trunk-based 的企业实现形态。

## 4. Feature Branch + Protected Main

这是多数中大型业务团队的现实选择。

### 推荐规则

- `main` 或 `master` 受保护
- 所有变更必须走 PR
- 必需状态检查通过后才允许合入
- 至少 1 名 reviewer 批准
- 关键目录配置 CODEOWNERS
- 禁止普通成员强推主分支

GitHub 分支保护可要求 Review、状态检查、线性历史、合并队列等能力，官方说明见 [protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)。

## 5. Gitflow

Gitflow 适合版本发布节奏明确的产品，比如客户端、SDK、企业交付产品。

### 适合

- 需要长期维护多个版本
- 有明确 release / hotfix 分支
- 发布窗口固定
- 线上版本不能随时部署

### 避免

- 高频 Web 服务
- 小团队快速迭代
- CI/CD 成熟且主干可以随时发布的系统

Gitflow 的分支模型有历史价值，但照搬到所有团队会制造额外复杂度。

## 6. GitLab Flow

GitLab Flow 适合发布频率和合入频率不完全一致的团队。

它保留 feature branch 和 merge request 的轻量协作方式，同时用 `production`、`stable/*` 这类分支表达线上状态和稳定版本线。

### 适合

- Web / SaaS 团队需要区分“已合入”和“已上线”
- 企业内部平台有多环境发布流程
- SDK、客户端、私有化产品需要稳定版本分支
- 团队觉得 GitHub Flow 太轻，Gitflow 太重

详细见 [GitLab Flow](gitlab-flow.md)。

## 7. Fork + Pull Request

### 适合

- 开源项目
- 外部贡献者很多
- 不希望给所有贡献者写权限

### 流程

```text
fork -> branch -> commit -> pull request -> maintainer review -> merge
```

### 维护者要做

- 提供清晰贡献指南
- 提供 Issue / PR 模板
- 标记适合新手的任务
- 用 CI 降低 Review 成本

## 8. Release Branch

### 适合

- 移动端
- 客户端
- SDK
- 私有化部署产品
- 多版本并行维护产品

### 基本流程

```text
main -> release/1.8 -> bugfix -> tag -> hotfix -> back merge
```

### 关键规则

- release 分支只接收稳定性修复
- 新功能继续进主干
- hotfix 后必须回合到主干
- 每个发布版本打 tag

Microsoft Release Flow 提供了一个更偏实战的组合：主干承接日常开发，按 sprint 或发布窗口创建 release 分支，修复完成后同步回主干。详细见 [Microsoft Release Flow](../10-company-practices/microsoft-release-flow.md)。

## 9. 常见反模式

### 长期存在的大 feature 分支

问题：合并风险越来越大，主干反馈失效。

建议：拆小任务，尽早合入，未完成能力用 feature flag 控制。

### 所有人直接推主分支

问题：主分支随时可能坏，责任边界不清。

建议：主分支保护，PR 审查，CI 必需通过。

### PR 太大

问题：Review 变成形式。

建议：一个 PR 只解决一个问题，重构和行为变化分开。

### 迷信某一种模型

问题：团队真实约束被忽略。

建议：按发布频率、团队规模、风险等级选择工作流。

## 10. 企业实践参考

| 实践 | 可借鉴点 |
| --- | --- |
| [阿里巴巴 AoneFlow](../10-company-practices/alibaba-aoneflow.md) | 用 release 分支表达发布范围，支持 feature 灵活组合和撤下 |
| [腾讯 Gitflow 分支规范](../10-company-practices/tencent-gitflow.md) | 适合固定版本发布、release 测试、hotfix 回合的团队 |
| [字节跳动 Git 工作流](../10-company-practices/bytedance-git-workflow.md) | 把分支、权限、Review、CI、发布放进统一研发设施 |
| [Google 主干开发](../10-company-practices/google-trunk-based-development.md) | 用短分支、快 CI、小变更支撑大规模协作 |
| [Microsoft Release Flow](../10-company-practices/microsoft-release-flow.md) | 主干开发配合 release 分支，适合有固定发布窗口的产品团队 |
| [Meta Sapling](../10-company-practices/meta-sapling-stacked-commits.md) | 用堆叠提交表达大功能的连续小变更 |

这些案例不要直接照搬，先看自己的发布频率、团队规模、测试能力和线上回滚能力。

## 11. 迁移策略

从旧流程迁移到新流程，不要一次改完所有规则。

推荐顺序：

1. 先要求所有变更走 PR
2. 再启用基础 CI
3. 再启用分支保护
4. 再引入 Review 要求
5. 再配置 CODEOWNERS
6. PR 量大后再考虑 merge queue

## 延伸阅读

- [Atlassian Git tutorials](https://www.atlassian.com/git)
- [GitHub Flow](https://docs.github.com/en/get-started/using-github/github-flow)
- [GitLab Flow](gitlab-flow.md)
- [Trunk Based Development](https://trunkbaseddevelopment.com)
- [Feature Flags](https://trunkbaseddevelopment.com/feature-flags/)
- [大厂工程实践索引](../10-company-practices/README.md)
- [企业 GitHub 协作配置栈](../04-github-engineering/enterprise-github-workflow-stack.md)
- [GitHub protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
- [GitHub rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets)
- [推荐阅读索引](../09-resources/recommended-reading.md)
