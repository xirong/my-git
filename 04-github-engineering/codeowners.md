# CODEOWNERS

CODEOWNERS 用于声明哪些路径由哪些人或团队负责 Review。

当 PR 修改了某些路径，GitHub 可以自动请求对应 owner Review。配合分支保护后，还可以要求对应 owner 批准后才能合入。

## 文件放在哪里

GitHub 支持把 `CODEOWNERS` 放在这些位置：

```text
.github/CODEOWNERS
CODEOWNERS
docs/CODEOWNERS
```

一般建议放在 `.github/CODEOWNERS`，和仓库协作模板放在一起。

## 示例

```text
# 默认 owner
* @team-platform

# 平台工程
/.github/ @team-platform
/scripts/ @team-platform

# 业务模块
/billing/ @team-billing
/auth/ @team-security
/docs/ @team-docs
```

## 推荐规则

- 先覆盖关键目录
- owner 要有真实响应能力
- 不要把所有路径都指给一个人
- 团队 owner 比个人 owner 更稳定
- 定期清理离职或职责变化的 owner
- 配合分支保护要求 code owner review

## 借鉴 Kubernetes OWNERS

Kubernetes 的 OWNERS 文件把 reviewer 和 approver 拆开：

- reviewer 关注代码质量、正确性、风格和局部实现
- approver 关注兼容性、API、依赖关系和整体接受标准

GitHub CODEOWNERS 没有内置这两层语义，但企业团队可以在流程上模拟：

- CODEOWNERS 指向模块负责人团队
- 普通 reviewer 先做代码层 Review
- owner 最后确认边界、风险和长期维护成本

## 常见问题

### 1. owner 没有写权限

GitHub 要求被列为 code owner 的用户或团队具备仓库写权限，否则不会按预期工作。

### 2. 团队不可见

如果使用团队作为 owner，团队可见性和权限也要正确配置。

### 3. 规则过细

规则过细会让 PR 被太多人卡住，建议先覆盖关键目录，再逐步扩展。

## 延伸阅读

- [GitHub Docs: About code owners](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)
- [GitHub Docs: About pull request reviews](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/about-pull-request-reviews)
- [开源项目 Git 治理实践](../09-resources/open-source-governance-practices.md)
- [GitHub 工程治理手册](github-engineering-governance.md)
- [推荐阅读索引](../09-resources/recommended-reading.md)
