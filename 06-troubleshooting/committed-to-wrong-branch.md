# Committed to Wrong Branch

提交到了错误分支，先判断是否已经 push。

还没 push 时很好处理。已经 push 后，要优先避免破坏公共历史。

## 先检查

```bash
git status
git branch --show-current
git log --oneline --decorate -5
```

## 还没 push

假设你在 `main` 上误提交了最后一个 commit，本来应该在 `feat/right-branch`。

```bash
git branch feat/right-branch
git reset --hard HEAD~1
git switch feat/right-branch
```

这会把当前 commit 保留到新分支，再让原分支回到提交前。

## 已经 push

如果已经 push 到公共分支，优先用 revert 修正原分支：

```bash
git revert <commit-sha>
```

再把正确 commit cherry-pick 到目标分支：

```bash
git switch feat/right-branch
git cherry-pick <commit-sha>
```

## 如果多个 commit 都错了

可以创建目标分支后，批量 cherry-pick：

```bash
git switch -c feat/right-branch
git cherry-pick <oldest-sha>^..<newest-sha>
```

执行前先确认 commit 范围。

## 避免再次发生

- 每次 commit 前看 `git branch --show-current`
- shell prompt 显示当前分支
- 主分支开启保护
- 重要仓库禁止直接 push 主分支

## 延伸阅读

- [Git Flight Rules](https://github.com/k88hudson/git-flight-rules)
- [git cherry-pick 官方文档](https://git-scm.com/docs/git-cherry-pick)
- [Undo Anything](undo-anything.md)
- [Git 高频事故处理手册](git-troubleshooting-playbook.md)
