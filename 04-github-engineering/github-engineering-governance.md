# GitHub Engineering Governance

GitHub 对现代工程团队来说，不只是代码托管平台，也是协作、审查、发布、安全和治理的一部分。

## 1. 仓库治理清单

- Branch protection
- Required status checks
- Required review
- CODEOWNERS
- Rulesets
- Merge queue
- Secret scanning
- Dependabot
- Code scanning
- PR template
- Issue template
- Release process

## 2. 成熟度模型

| 成熟度 | 应该具备 |
| --- | --- |
| L1 个人项目 | README、LICENSE、基础目录说明 |
| L2 小团队 | PR、基础 CI、分支保护 |
| L3 成长期团队 | CODEOWNERS、Issue / PR 模板、发布流程 |
| L4 中大型团队 | Rulesets、Merge Queue、安全扫描 |
| L5 平台化团队 | 统一仓库规范、自动化检查、指标看板 |

## 3. 正式团队的最小配置

### Main branch protection

建议：

- 禁止直接推主分支
- Require pull request before merging
- Require status checks before merging
- Require conversation resolution before merging
- 禁止删除主分支
- 禁止普通成员强推主分支

GitHub 官方文档见 [protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)。

### Pull request template

PR 模板至少要求填写：

- What changed
- Why
- How tested
- Risk
- Rollback plan

模板见 [Pull Request Template](../08-templates/pull-request-template.md)。

### Basic CI

至少包含：

- lint
- unit test
- build

团队越大，CI 越要快。慢 CI 会让开发者绕过规则。

多仓库团队建议用 [Reusable Workflows](reusable-workflows.md) 统一 CI 模板，避免每个仓库复制一份配置后逐渐漂移。

## 4. 成长期团队推荐配置

### CODEOWNERS

关键目录配置 owner：

```text
/billing/ @team-billing
/auth/ @team-security
/.github/ @team-platform
```

Kubernetes 的 OWNERS 模型提供了更完整的治理样板：reviewer 负责代码质量，approver 负责整体接受标准。GitHub CODEOWNERS 可以作为企业团队的轻量版本，见 [开源项目 Git 治理实践](../09-resources/open-source-governance-practices.md)。

### Rulesets

Rulesets 可以对分支、tag 和 push 行为设置规则。

GitHub 文档说明，多个 rulesets 可以同时作用，且更严格的规则会生效，见 [about rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets)。

### 安全检查

建议开启：

- Secret scanning
- Dependabot alerts
- Code scanning

安全能力的可用范围会随 GitHub 计划和仓库类型变化，实际以官方文档和仓库设置页为准。

## 5. 大团队进阶配置

### Merge Queue

PR 数量高、主分支繁忙时，可以启用 Merge Queue。

它适合解决“每个 PR 单独 CI 通过，但排队合并后主分支被组合变更破坏”的问题。

GitHub 分支保护文档中说明，merge queue 可以配合 required checks 使用，见 [protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)。

### 仓库规则基线

大组织建议建立统一基线：

- 默认分支命名
- PR 模板
- Issue 模板
- CI 必需项
- Secret scanning
- 依赖扫描
- Release note 格式
- CODEOWNERS 规则

## 6. 常见错误

### 只有规则，没有速度

治理不是让所有人慢下来。

规则越多，自动化越要强，CI 越要快，模板越要清楚。

### 只保护 main，不管 release

如果团队有 `release/*` 或 `hotfix/*` 分支，也要配置保护规则。

### CODEOWNERS 过细

过细会导致 PR 长时间没人批。

建议从关键目录开始，再逐步细化。

### 安全扫描开启后没人处理

扫描只是发现问题，团队还需要 owner、SLA 和升级路径。

## 延伸阅读

- [GitHub protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
- [GitHub rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets)
- [Reusable Workflows](reusable-workflows.md)
- [开源项目 Git 治理实践](../09-resources/open-source-governance-practices.md)
- [GitHub code scanning merge protection](https://docs.github.com/en/code-security/concepts/code-scanning/merge-protection)
- [Issue and pull request templates](https://docs.github.com/communities/using-templates-to-encourage-useful-issues-and-pull-requests/about-issue-and-pull-request-templates)
- [GitHub secret scanning](https://docs.github.com/github/administering-a-repository/about-secret-scanning)
- [推荐阅读索引](../09-resources/recommended-reading.md)
