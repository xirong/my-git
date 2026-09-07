# Undo Anything

Git 撤销前先判断变更状态。

最关键的问题只有三个：

1. 改动是否已经 commit
2. commit 是否已经 push
3. 是否已经有人基于它继续开发

## 本地未提交改动

丢弃一个已经确认归属、允许丢弃的已跟踪路径的工作区改动：

```bash
git restore --worktree -- <owned-path>
```

取消暂存：

```bash
git restore --staged -- <owned-path>
```

只有所有已跟踪编辑都属于自己、已经逐项检查且 owner 授权全部丢弃时，才可扩大到整个工作区：

```bash
git restore --worktree -- .
```

执行前先看：

```bash
git status --porcelain
git diff -- <owned-path>
git diff --cached -- <owned-path>
```

状态里出现来源不清、其他 owner 或需要保留的 staged、unstaged、untracked 内容时，停止，不执行 restore、clean 或 reset。

## 已提交但未 push

以下 reset 只处理自己尚未 push、没有协作者依赖的最后一个 commit。先确认 `git status --porcelain` 没有输出；已有 staged 内容会和 `reset --soft` 留下的内容混在同一个 Index，应该先保留现场或使用干净 worktree。

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

这些命令分别会重写本地状态、远端历史或删除未跟踪文件。先用明确路径和只读检查确认归属，再由 owner 决定是否丢弃。

先执行：

```bash
git status --porcelain
```

`git status --porcelain` 有输出时停止，保留现场。只有工作区干净、`<verified-ref>` 已核实且本地历史确实允许重写时，才先建备份分支再执行 reset：

```bash
git branch backup-before-undo HEAD
git reset --hard <verified-ref>
```

单独预览未跟踪候选路径：

```bash
git clean -nd
```

`git clean -nd` 只列出候选文件。只有 owner 确认某个未跟踪路径可丢弃时，才对该路径执行 `git clean -f -- <owned-untracked-path>`；不要把预览直接扩大成 `git clean -fd`。`git push --force` 是另一类远端操作，还需要远端权限、分支规则和协作者确认。

## 延伸阅读

- [GitHub Blog: How to undo almost anything with Git](https://github.blog/open-source/git/how-to-undo-almost-anything-with-git/)
- [git restore 官方文档](https://git-scm.com/docs/git-restore)
- [git revert 官方文档](https://git-scm.com/docs/git-revert)
- [Git 高频事故处理手册](git-troubleshooting-playbook.md)
