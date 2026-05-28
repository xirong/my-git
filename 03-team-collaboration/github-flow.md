# GitHub Flow

GitHub Flow 是一种轻量分支工作流，适合主分支稳定、发布频繁、CI 完整的小团队和 Web 服务。

它的核心思路是：主分支保持可发布，所有变更通过短分支和 PR 合入。

## 流程

```text
main -> branch -> pull request -> review -> CI -> merge -> deploy
```

## 适合场景

- Web 服务
- 小团队或中等规模团队
- 发布频率高
- 自动化测试和 CI 较完善
- 出问题可以快速回滚

## 基本规则

- `main` 始终保持可发布
- 每个变更创建短分支
- 每个分支通过 PR 合入
- 合入前至少完成 Review 和 CI
- 合入后尽快部署
- 出问题优先 revert

## 分支生命周期

GitHub Flow 不鼓励长期存在的 feature 分支。

如果一个功能需要开发很久，建议拆小：

- 先合入无行为变化的准备性重构
- 再合入后端能力
- 再合入前端入口
- 未完成能力用 feature flag 控制

## 常见误区

### 1. main 没有保护

如果所有人都能直接 push 到 `main`，GitHub Flow 很快会变成混乱的集中式提交。

至少需要：

- Require pull request
- Required status checks
- Required review

### 2. PR 太大

GitHub Flow 依赖快速 Review。

PR 太大时，Review 会流于形式。

### 3. 没有发布和回滚机制

GitHub Flow 适合高频发布，但前提是发布和回滚足够稳。

## 延伸阅读

- [GitHub Docs: GitHub Flow](https://docs.github.com/en/get-started/using-github/github-flow)
- [GitHub protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
- [Pull Request 最佳实践](pull-request-best-practices.md)
- [推荐阅读索引](../09-resources/recommended-reading.md)
