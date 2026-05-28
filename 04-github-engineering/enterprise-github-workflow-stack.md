# 企业 GitHub 协作配置栈

原文链接：

- [GitHub Flow](https://docs.github.com/en/get-started/using-github/github-flow)
- [About protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
- [About rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets)
- [About code owners](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)
- [Managing a merge queue](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue)
- [Understanding GitHub Actions](https://docs.github.com/en/actions/about-github-actions/understanding-github-actions)
- [About code scanning](https://docs.github.com/en/code-security/concepts/code-scanning/about-code-scanning)
- [About Dependabot version updates](https://docs.github.com/en/code-security/dependabot/dependabot-version-updates/about-dependabot-version-updates)
- [About secret scanning](https://docs.github.com/en/code-security/secret-scanning/introduction/about-secret-scanning)
- [Gerrit Code Review: Access Controls](https://gerrit-review.googlesource.com/Documentation/access-control.html)

## 1. 默认配置栈

一个成熟团队的 GitHub 协作配置，可以按这条链路建设：

```text
Issue / ADR / Ticket
-> short-lived branch
-> draft PR
-> CODEOWNERS routing
-> CI
-> security checks
-> required review
-> merge queue
-> protected main
-> tag / release
-> deploy
```

这套配置适合 GitHub Flow，也能承载 trunk-based 风格的团队协作。

## 2. 六类检查点

### 分支检查点

目标：避免直接在主分支上开发。

建议：

- 所有变更走短生命周期分支
- 分支名关联需求、Issue 或任务
- 主分支禁止普通成员直接 push

### 评审检查点

目标：让懂对应代码的人参与 Review。

建议：

- 配置 CODEOWNERS
- PR 模板要求填写风险和验证
- 高风险目录要求 owner 批准
- AI Review 只能作为辅助扫描

### 策略检查点

目标：把团队规则固化到平台。

建议：

- Protected branches 保护 `main`
- Rulesets 统一组织级规则
- 关键分支禁止删除和强推
- 必需检查名称保持稳定

Branch Protection 更适合单仓库、少量关键分支起步。Rulesets 更适合组织级、多仓库、规则叠加和审计可见性。

### 安全检查点

目标：把常见安全问题前移到 PR 和 push 阶段。

建议：

- Secret scanning
- Push protection
- Dependabot
- Code scanning
- Dependency review

Dependabot 可以把依赖和 GitHub Actions 版本升级变成 PR，Code scanning 负责发现代码安全问题，Secret scanning 负责发现凭证泄露风险。这三类检查适合和 PR 流程绑定，不能只做事后扫描。

### 集成检查点

目标：合入前验证主分支组合结果。

建议：

- 必需 CI 检查
- Merge Queue
- `merge_group` 事件触发 CI
- flaky tests 治理

### 发布检查点

目标：让上线版本可追踪、可解释、可回滚。

建议：

- tag
- GitHub Release
- release note
- rollback plan
- deploy verification

## 3. GitHub Flow 与主干开发的关系

GitHub Flow 是 GitHub 平台上的轻量协作路径，核心是短分支、PR、Review、合入默认分支。

Trunk-Based Development 是更强的组织原则，强调围绕主干高频集成，分支生命周期极短，主干持续可发布。

当一个团队在 GitHub Flow 上加上：

- 必需 CI
- CODEOWNERS
- Rulesets
- Merge Queue
- feature flag
- release from main

它就已经很接近 trunk-based 的企业实现形态。

## 4. 推广顺序

不要一次性把所有能力打开。

推荐顺序：

1. PR 模板
2. 基础 CI
3. 分支保护
4. CODEOWNERS
5. Rulesets
6. Secret scanning 和 Dependabot
7. Code scanning
8. Merge Queue
9. Release note 和发布记录

## 5. 和 Gerrit 的差异

GitHub 更像统一开发平台，优势是 PR、Actions、安全扫描、Issue、Release、Rulesets 一体化。

Gerrit 更像评审中枢，优势是组级权限、label 投票、Submit 权限和更细的评审语义。

如果团队需要特别强的 Review 权限模型，可以参考 [Gerrit 代码评审治理参考](../09-resources/gerrit-code-review-governance.md)。如果团队希望围绕 GitHub 生态建设统一协作平台，则优先用 GitHub 原生能力组合。

## 6. 常见误区

### 只保护 main

如果团队有 `release/*`、`hotfix/*` 或生产 tag，也要设计规则。

### 只加规则，不提速度

CI 越慢，开发者越倾向绕过规则。

### 把安全扫描当结果

扫描只是发现问题，还需要 owner、处理时限和升级路径。

### Merge Queue 开了但 CI 没改

使用 GitHub Actions 时，关键 workflow 要响应 `merge_group`：

```yaml
on:
  pull_request:
  merge_group:
```

## 7. 对本仓库的启发

GitHub 工程治理不要写成工具清单。

更适合写成从变更提出到发布完成的协作链路，让读者知道每个工具解决哪个风险点。
