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

`git add -p` 适合干净或隔离的任务工作区。先检查 Index 和 Working Tree；发现其他任务的 staged、unstaged 或 untracked 内容时，停止在这个工作区拆分，不要靠 reset 或清理命令把它们移走。

```bash
git status --porcelain
git diff --stat
git diff --cached
git add -p
git commit -m "test(module): cover edge case"
git add -p
git commit -m "fix(module): handle edge case"
```

已经提交成一个大 commit，但还没 push，且该分支没有协作者使用时：

```bash
git status --porcelain
git log --oneline --decorate -2
git reset --soft HEAD~1
git reset
git diff
git add -p
git diff --cached
```

`reset --soft` 后，原 commit 的所有 hunk 都已经在 Index。直接 `git add -p` 不会取消其中未选择的 hunk。无参数 `git reset` 先把 Index 恢复为当前 `HEAD`，Working Tree 保留全部修改，随后部分暂存才会决定下一次 commit 的内容。

上面两个流程中，`git status --porcelain` 的预期都是没有输出。只要有输出，就保留当前现场并在干净 task worktree 中继续。已 push 后谨慎重写历史，先确认有没有人基于这个分支继续开发。可运行的状态断言见 [Git 命令安全回归](../labs/git-command-safety/README.md)。

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

Google 小 CL 和 Meta Sapling 的共同启发是：先让变更变小，再让 Review 变准。AI 改代码时，拆分的核心价值是把风险切回可判断范围。案例对照见 [大厂工程实践决策图谱](../10-company-practices/company-practices-decision-map.md)。

## 延伸阅读

- [git add 官方文档](https://git-scm.com/docs/git-add)
- [git reset 官方文档](https://git-scm.com/docs/git-reset)
- [AI Native Git Workflow](ai-native-git-workflow.md)
- [AI 变更审查实战样例](ai-change-review-example.md)
- [Commit Message](../02-daily-workflow/commit-message.md)
- [Meta Sapling 与堆叠提交实践](../10-company-practices/meta-sapling-stacked-commits.md)
- [Stacked PR for AI-Generated Changes](stacked-pr-for-ai-generated-changes.md)
- [大厂工程实践决策图谱](../10-company-practices/company-practices-decision-map.md)
