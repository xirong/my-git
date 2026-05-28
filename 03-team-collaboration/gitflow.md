# Gitflow

Gitflow 是经典分支模型，适合有明确版本发布节奏的产品。

它把日常开发、发布准备、线上修复拆成不同分支角色，适合客户端、SDK、私有化交付等发版周期比较明确的场景。

## 分支

- `main`：生产版本历史
- `develop`：集成分支
- `feature/*`：功能开发
- `release/*`：发布准备
- `hotfix/*`：线上紧急修复

## 典型流程

```text
develop -> feature/* -> develop -> release/* -> main -> tag
                              \-> hotfix/* -> main -> develop
```

## 适合场景

- 需要维护多个版本
- 有固定发布窗口
- 客户端或 SDK 发版成本高
- 线上版本不能随时发布
- 发布前有明确测试和验收周期

## 不适合场景

- Web 服务高频发布
- 团队很小
- 主干可以随时部署
- CI/CD 成熟且发布风险可快速回滚

## 优点

- 分支职责清晰
- release 和 hotfix 有明确路径
- 适合版本化产品
- 容易和传统发布流程对齐

## 成本

- 分支多，流程复杂
- develop 和 main 可能长期分叉
- hotfix 后需要回合到多个分支
- 对高频发布团队可能拖慢节奏

## 判断建议

不要盲目照搬 Gitflow。

如果你的团队每天多次发布 Web 服务，GitHub Flow 或 Trunk-Based Development 往往更轻。

如果你的产品有明确版本线、发布窗口、客户侧升级周期，Gitflow 仍然有价值。

Atlassian 的 Gitflow 教程也把它放在特定发布型场景里理解：它适合版本列车、发布准备、热修复和审计较重的产品；在现代 CI/CD 和高频服务交付中，长期分支会增加偏离主线与集成冲突的成本。

## 企业实践参考

[腾讯云社区 Gitflow 分支规范实践](../10-company-practices/tencent-gitflow.md) 可以作为 Gitflow 风格团队规范的参考，尤其适合 release、hotfix、tag、回合路径都要写清楚的团队。

[阿里巴巴 AoneFlow 分支管理实践](../10-company-practices/alibaba-aoneflow.md) 则提供了另一种思路：保留 feature 和 release 的清晰边界，同时减少长期 `develop` 分支带来的复杂度。

## 延伸阅读

- [A successful Git branching model](https://nvie.com/posts/a-successful-git-branching-model/)
- [Atlassian: Gitflow Workflow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow)
- [腾讯云社区 Gitflow 分支规范实践](../10-company-practices/tencent-gitflow.md)
- [阿里巴巴 AoneFlow 分支管理实践](../10-company-practices/alibaba-aoneflow.md)
- [团队 Git 工作流指南](team-git-workflow-guide.md)
- [推荐阅读索引](../09-resources/recommended-reading.md)
