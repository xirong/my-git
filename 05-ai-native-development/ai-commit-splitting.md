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

## 延伸阅读

- [git add 官方文档](https://git-scm.com/docs/git-add)
- [git reset 官方文档](https://git-scm.com/docs/git-reset)
- [AI Native Git Workflow](ai-native-git-workflow.md)
- [Commit Message](../02-daily-workflow/commit-message.md)
