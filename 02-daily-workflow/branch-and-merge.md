# 分支与合并

分支用于隔离任务，合并用于把验证后的变更带回主线。

好的分支习惯能降低冲突、减少无关改动，也能让 PR 更容易 Review。

## 什么时候创建分支

建议每个独立任务创建一个分支：

- 新功能
- Bug 修复
- 文档更新
- 重构
- 实验性方案
- AI Agent 生成代码的候选方案

创建分支：

```bash
git switch -c feat/my-task
```

切回主分支：

```bash
git switch main
```

## 分支命名建议

```text
feat/github-governance-guide
fix/recover-lost-commit-example
docs/ai-native-git-workflow
hotfix/remove-broken-link
ai/review-large-repo-guide
```

更多模板见 [Branch Naming Convention](../08-templates/branch-naming-convention.md)。

## 合并前检查

合并前先看：

```bash
git status
git diff --stat main...HEAD
git log --oneline main..HEAD
```

确认：

- 分支只包含当前任务
- commit 标题能看懂
- 没有无关格式化
- 没有 secret、临时文件、构建产物
- 验证已经完成

## 合并方式

### merge commit

保留分支合入历史，适合需要审计合并上下文的团队。

```bash
git switch main
git merge --no-ff feat/my-task
```

### squash merge

把 PR 里的多个 commit 压成一个 commit，适合保持主分支历史简洁。

### rebase merge

把 PR 中的 commit 重新放到目标分支之后，适合追求线性历史的团队。

合并策略要按团队约定统一，不要每个人按个人喜好选择。

## 推荐团队规则

- 个人分支可以频繁提交
- 主分支只接受经过 Review 和 CI 的变更
- 合并前确认分支是最新的
- 大改动拆成多个小 PR
- 出问题优先 revert

## 延伸阅读

- [git branch 官方文档](https://git-scm.com/docs/git-branch)
- [git merge 官方文档](https://git-scm.com/docs/git-merge)
- [Atlassian: Git Branch](https://www.atlassian.com/git/tutorials/using-branches)
- [团队 Git 工作流指南](../03-team-collaboration/team-git-workflow-guide.md)
