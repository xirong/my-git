# Rulesets

GitHub Rulesets 用于统一控制分支、tag 和 push 行为。

它比单个分支保护规则更适合组织级、仓库级的统一治理。

## 适合场景

- 多个分支需要统一规则
- 组织内多个仓库需要统一规范
- 需要规则启用、暂停、审计
- 需要限制特定路径、文件大小或提交元数据
- 希望把分支规则和 tag 规则集中管理

## 可以控制什么

常见规则包括：

- 限制创建、更新、删除分支
- 要求 PR 才能合入
- 要求状态检查通过
- 要求线性历史
- 限制 force push
- 保护 tag
- 对特定路径设置规则

不同规则能力会随 GitHub 版本和仓库类型变化，实际以官方文档和设置页为准。

## 和 Branch Protection 的关系

Rulesets 和 Branch Protection 可以同时存在。

GitHub 官方文档说明，多个 rulesets 命中同一目标时会聚合规则。

对新团队来说，建议先用 Branch Protection 起步。仓库多、规则复杂后，再逐步切到 Rulesets。

## 推荐落地顺序

1. 先保护 `main`
2. 再保护 `release/*`
3. 再抽象成 ruleset
4. 再推广到组织内多个仓库
5. 定期审计规则是否仍然有效

## 延伸阅读

- [GitHub Docs: About rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets)
- [GitHub Docs: Creating rulesets for a repository](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/creating-rulesets-for-a-repository)
- [Branch Protection](branch-protection.md)
- [推荐阅读索引](../09-resources/recommended-reading.md)
