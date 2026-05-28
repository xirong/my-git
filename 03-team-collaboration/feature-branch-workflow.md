# Feature Branch Workflow

Feature Branch Workflow 是多数团队最容易落地的协作方式。

它的核心是：每个需求或修复在独立分支开发，完成后通过 PR 合入主分支。

## 流程

```text
main -> feature branch -> pull request -> review -> CI -> merge
```

## 适合场景

- 多人并行开发
- 中大型业务系统
- 需要 Review 和 CI 的团队
- 团队还没准备好全面主干开发
- 需求通常可以拆成独立任务

## 分支建议

```text
feat/user-login
fix/payment-timeout
docs/git-workflow-guide
refactor/order-validator
```

分支名要表达任务意图，不要使用 `test`、`tmp`、`new` 这类名字。

## PR 建议

- 一个 PR 只解决一个问题
- 行为变化和重构尽量拆开
- PR 描述写清验证方式
- 有风险的改动写清回滚方案
- 合入后及时删除分支

## 注意事项

### 1. 分支不要长期存在

分支存在越久，和主分支偏离越大，合并冲突越难处理。

### 2. 定期同步主分支

```bash
git fetch origin
git rebase origin/main
```

是否使用 rebase 要按团队约定。

### 3. 避免大 PR

如果 PR 已经很难 Review，先拆。

## 延伸阅读

- [Atlassian: Feature Branch Workflow](https://www.atlassian.com/continuous-delivery/principles/workflows-with-feature-branching-and-gitflow)
- [Pull Request 最佳实践](pull-request-best-practices.md)
- [Code Review 最佳实践](code-review-best-practices.md)
- [推荐阅读索引](../09-resources/recommended-reading.md)
