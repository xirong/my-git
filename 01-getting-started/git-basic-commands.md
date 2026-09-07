# Git Basic Commands

## Create or clone

```bash
git init
git clone <url>
```

## Check status

```bash
git status
git log --oneline --decorate
```

## Stage and commit

```bash
git add <file>
git commit -m "docs: add git basics"
```

## Sync

```bash
git fetch
git pull --rebase
git push
```

## Branch

`<integration-branch>` 是团队实际使用的集成分支名，常见值有 `main`、`master` 和 `develop`。先按仓库规则确认名称，再切换；不要把 `main` 当作固定默认值。

```bash
git switch -c feat/my-task
git branch --show-current
git switch <integration-branch>
git branch
```

## Undo

`git restore` 会覆盖指定路径的 Working Tree。执行前先确认该路径归属自己，且当前版本允许丢弃：

```bash
git status --porcelain
git diff -- <owned-path>
git restore --worktree -- <owned-path>
```

只想取消暂存、并保留该路径的 Working Tree 编辑时：

```bash
git restore --staged -- <owned-path>
```

已提交的改动需要新增反向 commit 时：

```bash
git revert <commit-sha>
```

`git restore --staged` 只调整 Index，Working Tree 的编辑会保留；`git revert` 为已提交的改动新增一个反向 commit。

## 建议练习顺序

1. 用 `git status` 看懂当前状态
2. 用 `git add` 和 `git commit` 完成一次本地提交
3. 用 `git switch -c` 创建任务分支
4. 用 `git diff` 检查提交前改动
5. 用 `git push` 推送分支并创建 PR
6. 用 `git restore` 撤销本地改动

## 高风险命令先别急着用

先检查是否存在需要保留的 staged、unstaged 或 untracked 内容，并只预览未跟踪文件：

```bash
git status --porcelain
git diff
git diff --cached
git clean -nd
```

`git status --porcelain` 有输出时，停止，不执行 `git reset --hard` 或 `git clean`。`git clean -nd` 只列出候选路径，不能证明它们可以删除。

确认本地编辑的归属和处置授权、验证 reset 的目标提交，并确认远端权限、分支规则和协作者影响后，才由 owner 决定是否使用 `git reset --hard`、`git clean -fd` 或 `git push --force`。它们分别可能丢弃已跟踪编辑、删除未跟踪路径和改写远端历史。

如果只是想撤销普通工作区改动，优先学习 [Undo Anything](../06-troubleshooting/undo-anything.md)。

## 延伸阅读

- [Git 官方文档](https://git-scm.com/docs)
- [Git Cheat Sheet](https://git-scm.com/cheat-sheet.pdf)
- [Pro Git: Git Basics](https://git-scm.com/book/en/v2/Git-Basics-Getting-a-Git-Repository)
- [推荐阅读索引](../09-resources/recommended-reading.md)
