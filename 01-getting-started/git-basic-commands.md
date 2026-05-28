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

```bash
git switch -c feat/my-task
git switch main
git branch
```

## Undo

```bash
git restore <file>
git restore --staged <file>
git revert <commit-sha>
```

## 建议练习顺序

1. 用 `git status` 看懂当前状态
2. 用 `git add` 和 `git commit` 完成一次本地提交
3. 用 `git switch -c` 创建任务分支
4. 用 `git diff` 检查提交前改动
5. 用 `git push` 推送分支并创建 PR
6. 用 `git restore` 撤销本地改动

## 高风险命令先别急着用

新手阶段谨慎使用：

```bash
git reset --hard
git push --force
git clean -fd
```

这些命令可能直接丢弃本地改动或改写远端历史。

如果只是想撤销普通工作区改动，优先学习 [Undo Anything](../06-troubleshooting/undo-anything.md)。

## 延伸阅读

- [Git 官方文档](https://git-scm.com/docs)
- [Git Cheat Sheet](https://git-scm.com/cheat-sheet.pdf)
- [Pro Git: Git Basics](https://git-scm.com/book/en/v2/Git-Basics-Getting-a-Git-Repository)
- [推荐阅读索引](../09-resources/recommended-reading.md)
