# Release Management

发布管理要保证版本可追踪、变更可解释、问题可回滚。

Git 本身负责记录版本历史，GitHub Release、tag、changelog、CI/CD 则把这些历史变成可交付的版本资产。

## 推荐产物

- tag
- release note
- changelog
- rollback plan
- migration note
- verification note

## 发布流程

```text
merge -> tag -> release notes -> deploy -> verify -> announce
```

## Tag 规范

推荐使用语义化版本：

```text
v2.0.0
v2.0.1
v2.1.0
```

常见含义：

- major：不兼容变化
- minor：向后兼容的新能力
- patch：向后兼容的修复

## Release note 应该写什么

至少包含：

- 重点变化
- Bug 修复
- 破坏性变化
- 升级说明
- 回滚方式
- 贡献者

模板见 [Release Note Template](../08-templates/release-note-template.md)。

## Hotfix 发布

hotfix 只处理生产环境紧急问题。

原则：

- diff 小
- 不混入重构
- 有明确验证
- 有回滚方案
- 发布后回合到主干

流程见 [Hotfix Process](../08-templates/hotfix-process.md)。

## 发布流水线

Netflix Spinnaker 这类公开实践提醒我们，很多团队真正的风险集中在发布过程，分支模型只是其中一部分。

当团队已经有 PR、CI 和分支保护后，下一步要补的是：

- 发布关联 commit 或 tag
- 发布记录包含 release note
- 生产发布前有明确检查点
- 高风险发布有人工审批点
- 发布后验证结果可追踪
- 回滚路径明确

详细见 [Netflix Spinnaker 与发布流水线实践](../10-company-practices/netflix-spinnaker-release.md)。

## Release Flow 和日常部署

Microsoft Release Flow 的经验适合有固定 sprint、固定发布窗口的团队：

- 日常开发进入主干
- 发布前从主干切 release 分支
- release 分支只接收稳定性修复
- 修复完成后同步回主干
- 发布版本用 tag 和 release note 留痕

Slack 公开分享的部署实践更强调“持续小批量发布”：通过自动化检查、发布队列、可观测性和回滚路径，把风险拆散到日常部署中处理。

这两类实践方向不同，但共同点很清楚：发布管理不能只依赖分支命名，要把验证、审批点、发布记录、监控和回滚路径串起来。

## 延伸阅读

- [GitHub Docs: Managing releases in a repository](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository)
- [Semantic Versioning](https://semver.org/)
- [Netflix Spinnaker 与发布流水线实践](../10-company-practices/netflix-spinnaker-release.md)
- [Microsoft Release Flow](../10-company-practices/microsoft-release-flow.md)
- [Slack Deploys 实践](../10-company-practices/slack-deploys.md)
- [GitHub 工程治理手册](github-engineering-governance.md)
- [推荐阅读索引](../09-resources/recommended-reading.md)
