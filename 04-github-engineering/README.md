# GitHub 工程治理

这个目录面向技术负责人和团队维护者，目标是把 GitHub 从代码托管工具，配置成协作、Review、CI、发布、安全和审计的一部分。

## 先读什么

| 你要解决的问题 | 建议阅读 |
| --- | --- |
| 想建立仓库治理全景 | [GitHub Engineering Governance](github-engineering-governance.md) |
| 想一次看清企业协作配置组合 | [企业 GitHub 协作配置栈](enterprise-github-workflow-stack.md) |
| 想保护 main 或 release 分支 | [Branch Protection](branch-protection.md) |
| 多仓库想统一规则 | [Rulesets](rulesets.md) |
| 关键目录需要 owner Review | [CODEOWNERS](codeowners.md) |
| PR 多，主分支经常被合坏 | [Merge Queue](merge-queue.md) |

## CI 和发布

- [GitHub Actions CI](github-actions-ci.md)
- [Reusable Workflows](reusable-workflows.md)
- [Release Management](release-management.md)

多仓库团队优先看 Reusable Workflows，避免每个仓库复制一套 CI 后逐渐漂移。
有固定发布窗口、hotfix、release note 的团队，优先看 Release Management。

## 安全和配置

- [Security and Secret Scanning](security-and-secret-scanning.md)
- [GitOps and Config as Code](gitops-and-config-as-code.md)

如果团队已经把配置、基础设施、发布策略放进仓库，这两篇要一起看。

## 相关内容

- [团队协作](../03-team-collaboration/README.md)
- [模板库](../08-templates/README.md)
- [大厂工程实践案例](../10-company-practices/README.md)
