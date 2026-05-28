# Security and Secret Scanning

安全治理至少要覆盖凭证、依赖和代码扫描。

对普通团队来说，最容易出大事故的是把 token、密码、私钥、内部地址或生产配置提交进仓库。

## 推荐检查

- Secret scanning
- Push protection
- Dependabot alerts
- Code scanning
- Dependency review

这些能力适合作为 PR 和 push 阶段的安全检查点，和分支保护、Rulesets、CI 组合使用，见 [企业 GitHub 协作配置栈](enterprise-github-workflow-stack.md)。

## Secret scanning 做什么

GitHub secret scanning 会扫描仓库中的凭证泄露风险，并在发现可疑 secret 时生成告警。

GitHub 文档说明，secret scanning 会扫描仓库所有分支的 Git 历史。

具体可用范围会随仓库类型、组织计划和 GitHub 安全能力变化，实际以仓库设置页和官方文档为准。

## Push protection 做什么

Push protection 会在开发者 push 时识别可能的 secret，并阻止它进入远端仓库。

这比事后发现更有价值，因为它能把风险拦在进入历史之前。

## 如果 secret 已经提交

第一步永远是废弃并轮换 secret。

不要以为删除文件或 revert commit 就安全了。Git 历史、fork、缓存、日志里都可能已经留下痕迹。

建议流程：

1. 立即废弃 secret
2. 轮换新 secret
3. 确认访问日志和影响范围
4. 清理 Git 历史
5. 通知相关 owner
6. 补充提交前扫描

详细处理见 [Remove Secret from History](../06-troubleshooting/remove-secret-from-history.md)。

## 团队规则

- 禁止把 `.env`、私钥、token 提交到仓库
- 给本地开发提供 `.env.example`
- CI/CD 使用平台 secret 管理
- PR 模板加入 secret 自查项
- 关键仓库开启 secret scanning 和 push protection

## Dependabot 和 Code Scanning

Dependabot 适合把依赖升级和 GitHub Actions 版本升级变成可 Review 的 PR。

Code scanning 适合把静态安全问题前移到 PR 或主分支检查中，并通过告警把问题分配给 owner。

这两类能力要和 CODEOWNERS、必需检查、处理时限配合，否则只是增加告警数量。

## 延伸阅读

- [GitHub Docs: About secret scanning](https://docs.github.com/en/code-security/concepts/secret-security/about-secret-scanning)
- [GitHub Docs: Enabling secret scanning features](https://docs.github.com/en/code-security/secret-scanning/enabling-secret-scanning-features)
- [GitHub security features](https://docs.github.com/en/code-security/getting-started/github-security-features)
- [企业 GitHub 协作配置栈](enterprise-github-workflow-stack.md)
- [Remove Secret from History](../06-troubleshooting/remove-secret-from-history.md)
