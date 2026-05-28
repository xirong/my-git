# Branch Protection

分支保护用于保护关键分支，避免未经审查、未经验证或高风险操作直接进入主线。

对团队仓库来说，`main`、`master`、`release/*` 这类分支应该被当成公共资产管理。

## 推荐配置

- Require a pull request before merging
- Require approvals
- Require status checks before merging
- Require conversation resolution before merging
- Require linear history when your team wants easier revert
- Block force pushes on main branches
- Block branch deletion on main branches

## 建议保护的分支

- `main`
- `master`
- `develop`
- `release/*`
- `hotfix/*`

## 最小配置

小团队可以先启用：

1. Require pull request before merging
2. Require status checks before merging
3. Block force pushes
4. Block deletions

这样能先防住最常见的事故：

- 直接 push 主分支
- CI 红了仍然合入
- force push 覆盖远端历史
- 误删关键分支

## 成长期团队配置

团队变大后，建议继续启用：

- Require approvals
- Dismiss stale pull request approvals when new commits are pushed
- Require review from Code Owners
- Require conversation resolution before merging

这些规则可以把 Review、CODEOWNERS、CI 串成一个完整合入流程。

## 常见误区

### 1. 只保护 main

如果团队使用 `release/*`、`hotfix/*`，这些分支也应该保护。

### 2. 只加规则，不管 CI 稳定性

必需检查必须稳定。flaky test 会让团队开始绕过规则。

### 3. 管理员长期绕过规则

管理员绕过应该只用于极少数紧急场景，并留下记录。

## 延伸阅读

- [GitHub Docs: Protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
- [GitHub Docs: Required status checks](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches#require-status-checks-before-merging)
- [CODEOWNERS](codeowners.md)
- [GitHub 工程治理手册](github-engineering-governance.md)
