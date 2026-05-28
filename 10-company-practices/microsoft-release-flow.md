# Microsoft Release Flow

原文链接：

- [Release Flow: How We Do Branching on the VSTS Team](https://devblogs.microsoft.com/devops/release-flow-how-we-do-branching-on-the-vsts-team/)

Microsoft Release Flow 很适合中大型业务团队参考。

它采用 trunk-based 的主干集成方式，但不会把 `master` 直接持续部署到生产。团队按 sprint 从 `master` 创建 release branch，生产 hotfix 先合入 `master`，再 cherry-pick 到当前 release branch。

## 核心流程

```text
feature branch -> PR -> master
master -> releases/M130 -> production
hotfix -> master -> cherry-pick -> releases/M130
```

这个模型把两个目标分开：

- `master` 保持快速集成
- production release branch 保持发布稳定

## 为什么不用复杂长期分支

Microsoft 文章里提到，复杂的多层分支结构容易复制组织结构，代码一路向主干集成，再从主干反向同步到各分支，最后形成持续合并压力。

Release Flow 的取舍是：

- 日常开发尽量进入主干
- 发布节奏由 release branch 承接
- 生产 hotfix 仍以主干为源头
- release 分支服务当前发布，不长期堆积复杂历史

## Hotfix 规则

Release Flow 最值得借鉴的是 master first。

生产修复先合入 `master`，再 cherry-pick 到当前 release branch。

这样可以避免一个常见事故：线上修了问题，但主干没有这个修复，下一次发布又把问题带回来。

只有当修复在主干上已经不适用时，才考虑直接修 release branch。

## 适合什么团队

适合：

- 中大型 Web / SaaS 团队
- 主干需要快速集成
- 生产发布按 sprint 或窗口推进
- hotfix 要快速进入生产
- 团队有稳定的 PR、Review、CI 流程

不适合：

- 小团队每天多次直接发布
- 需要长期维护多个客户版本
- 没有清晰发布节奏

## 对本手册的启发

Release Flow 说明了一个很实用的组合：

```text
trunk-based integration + release branch deployment + master-first hotfix
```

它比完整 Gitflow 轻，又比纯 GitHub Flow 更适合中大型服务团队。
