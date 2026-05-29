# 日常 Git 命令

这不是完整命令手册，只保留日常开发最常用的一条路径。

目标是让你能稳定完成：

```text
拉最新代码 -> 创建分支 -> 修改 -> 检查 diff -> 提交 -> 推送 -> 开 PR
```

## 开始一个任务

```bash
git switch main
git pull --rebase
git switch -c feat/my-task
```

如果你的团队主分支叫 `master` 或 `develop`，按团队实际分支替换。

## 查看当前状态

```bash
git status
git diff
git diff --stat
```

提交前一定要看 diff。

尤其是 AI 辅助开发时，先确认有没有无关文件、格式化噪音、临时日志、secret、构建产物。

## 暂存和提交

推荐用 `git add -p` 分块暂存：

```bash
git add -p
git commit -m "feat(scope): describe change"
```

如果这次改动很小，也可以直接：

```bash
git add <file>
git commit -m "fix(scope): describe bug fix"
```

## 同步主分支

```bash
git fetch origin
git rebase origin/main
```

如果你不确定是否应该 rebase，先看 [Rebase vs Merge](rebase-vs-merge.md)。

## 推送分支

```bash
git push -u origin feat/my-task
```

然后在 GitHub / GitLab 上创建 PR。

## 临时切换任务

```bash
git stash push -u -m "wip: current task"
git switch main
git switch -c hotfix/urgent-fix
```

恢复：

```bash
git switch feat/my-task
git stash apply
```

## 出问题先别慌

先保存现场：

```bash
git status
git log --oneline --decorate -10
git reflog -10
```

再按 [Git 高频事故处理手册](../06-troubleshooting/git-troubleshooting-playbook.md) 选择恢复方式。

## 延伸阅读

- [Git 官方文档](https://git-scm.com/docs)
- [Git Cheat Sheet](https://git-scm.com/cheat-sheet.pdf)
- [Atlassian Git tutorials](https://www.atlassian.com/git)
- [原有命令手册（归档）](../09-resources/legacy/useful-git-command.md)
