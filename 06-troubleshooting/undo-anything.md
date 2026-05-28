# Undo Anything

Git 撤销前先判断变更状态。

最关键的问题只有三个：

1. 改动是否已经 commit
2. commit 是否已经 push
3. 是否已经有人基于它继续开发

## 本地未提交改动

丢弃某个文件的工作区改动：

```bash
git restore <file>
```

取消暂存：

```bash
git restore --staged <file>
```

丢弃所有已跟踪文件的工作区改动：

```bash
git restore .
```

执行前先看：

```bash
git status
git diff
```

## 已提交但未 push

修改最后一个 commit：

```bash
git commit --amend
```

撤回最后一个 commit，但保留改动在暂存区：

```bash
git reset --soft HEAD~1
```

撤回最后一个 commit，并保留改动在工作区：

```bash
git reset HEAD~1
```

## 已 push 的公共 commit

公共 commit 优先用：

```bash
git revert <commit-sha>
```

这样会新增一个反向 commit，历史清楚，也不会破坏协作者本地分支。

## 高风险命令

```bash
git reset --hard
git push --force
git clean -fd
```

这些命令执行前，先确认没有要保留的改动。

建议先建备份分支：

```bash
git branch backup-before-undo
```

## 延伸阅读

- [GitHub Blog: How to undo almost anything with Git](https://github.blog/open-source/git/how-to-undo-almost-anything-with-git/)
- [git restore 官方文档](https://git-scm.com/docs/git-restore)
- [git revert 官方文档](https://git-scm.com/docs/git-revert)
- [Git 高频事故处理手册](git-troubleshooting-playbook.md)
