# Revert Merge Commit

撤销 merge commit 时，需要指定 mainline parent。

普通 commit 可以直接：

```bash
git revert <commit-sha>
```

但 merge commit 有两个或多个父提交，Git 需要知道你要保留哪一侧作为主线。

## 先检查 merge commit

```bash
git show --summary <merge-commit-sha>
git log --oneline --graph --decorate -20
```

确认这个 merge commit 是从哪个分支合入的。

## 常见用法

```bash
git revert -m 1 <merge-commit-sha>
```

`-m 1` 通常表示保留目标分支视角，撤销被合入分支带来的变化。

## 为什么需要 -m

merge commit 有多个 parent。

例如：

```text
parent 1: main 合并前的位置
parent 2: feature 分支的位置
```

`-m 1` 表示以 parent 1 为主线，撤销另一个分支带来的变化。

## 风险

撤销 merge commit 后，如果未来还想重新合入同一个分支，Git 可能认为部分变更已经处理过。

更稳妥的做法是：

- 确认这次只是回滚线上风险
- 后续重新开发时新开分支
- 必要时 cherry-pick 需要保留的 commit

## 延伸阅读

- [git revert 官方文档](https://git-scm.com/docs/git-revert)
- [GitHub Blog: How to undo almost anything with Git](https://github.blog/open-source/git/how-to-undo-almost-anything-with-git/)
- [Git 高频事故处理手册](git-troubleshooting-playbook.md)
