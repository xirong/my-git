# 日常 Git 命令

这不是完整命令手册，只保留日常开发最常用的一条路径。

目标是让你能稳定完成：

```text
拉最新代码 -> 创建分支 -> 修改 -> 检查 diff -> 提交 -> 推送 -> 开 PR
```

## 开始一个任务

`<integration-branch>` 是仓库和团队确定的集成分支，例如 `main`、`master` 或 `develop`。下面流程开始前，先确认工作区没有其他待处理编辑；`git status --porcelain` 有输出时，保留现场，或转到干净 worktree，不能用切换或同步命令覆盖它。

```bash
git status --porcelain
git branch --show-current
git switch <integration-branch>
git pull --rebase origin <integration-branch>
git switch -c feat/my-task
```

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

在自己的 feature 分支上同步前，确认团队允许 rebase、分支未被协作者基于开发，并让 `git status --porcelain` 保持无输出。`origin/<integration-branch>` 必须替换为实际集成分支的远端跟踪引用。

```bash
git status --porcelain
git fetch origin
git rebase origin/<integration-branch>
```

如果你不确定是否应该 rebase，先看 [Rebase vs Merge](rebase-vs-merge.md)。

## 推送分支

```bash
git push -u origin feat/my-task
```

然后在 GitHub / GitLab 上创建 PR。

## 临时切换任务

`git stash push -u` 会把当前已跟踪和未跟踪内容都放进 stash。只在所有这些内容都属于自己、并且准备稍后恢复时使用；出现其他 owner 的编辑或来源不清的文件时，停止在这个工作区操作，改用独立 worktree。

```bash
git stash push -u -m "wip: current task"
git switch <integration-branch>
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
