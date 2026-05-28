# AI Commit Splitting

AI 一次改很多文件时，提交前先拆 commit。

## 判断维度

- 行为修复
- 测试补充
- 文档更新
- 重构清理
- 依赖变更
- 配置变更

## 命令

```bash
git diff --stat
git add -p
git commit -m "test(module): cover edge case"
git add -p
git commit -m "fix(module): handle edge case"
```

已经提交成一个大 commit，但还没 push：

```bash
git reset --soft HEAD~1
git add -p
```

已 push 后谨慎重写历史，先确认有没有人基于这个分支继续开发。

## 拆分建议

优先拆成这些类型：

- 测试提交
- 行为修复
- 文档说明
- 局部重构
- 配置调整
- 依赖变化

不要把“修 bug + 大重构 + 格式化 + 依赖升级”放在同一个 commit。

## 借鉴堆叠提交

Meta Sapling 的公开实践把 stack of commits 作为重要工作流，适合把大功能拆成多个连续的小变更。

AI 生成大 diff 后，也可以按这个思路整理：

```text
commit 1: add failing test
commit 2: change implementation
commit 3: update docs
commit 4: remove obsolete helper
```

每个 commit 都要能单独解释，且顺序清楚。

当一个大 diff 超过单个 PR 的 Review 承载能力时，可以继续拆成 stacked PR。commit 拆分解决 PR 内部历史清楚的问题，stacked PR 解决多人 Review 和分层合入的问题。

## 延伸阅读

- [git add 官方文档](https://git-scm.com/docs/git-add)
- [git reset 官方文档](https://git-scm.com/docs/git-reset)
- [AI Native Git Workflow](ai-native-git-workflow.md)
- [AI 变更审查实战样例](ai-change-review-example.md)
- [Commit Message](../02-daily-workflow/commit-message.md)
- [Meta Sapling 与堆叠提交实践](../10-company-practices/meta-sapling-stacked-commits.md)
- [Stacked PR for AI-Generated Changes](stacked-pr-for-ai-generated-changes.md)
