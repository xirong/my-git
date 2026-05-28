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

## 延伸阅读

- [GitHub Docs: Managing releases in a repository](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository)
- [Semantic Versioning](https://semver.org/)
- [GitHub 工程治理手册](github-engineering-governance.md)
- [推荐阅读索引](../09-resources/recommended-reading.md)
