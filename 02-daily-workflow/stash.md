# Stash

`git stash` 用于临时保存未提交改动。

它适合处理“我手上有未完成代码，但现在必须切分支、拉代码、修 hotfix”的场景。

## 适合场景

- 当前改动还没准备好 commit
- 临时要切到另一个分支
- pull / rebase 前想先保存现场
- 想快速做一个本地检查点

## 基础用法

保存当前改动，包括未跟踪文件：

```bash
git stash push -u -m "wip: describe current work"
```

查看 stash 列表：

```bash
git stash list
```

应用某个 stash，但保留 stash 记录：

```bash
git stash apply stash@{0}
```

应用并删除 stash：

```bash
git stash pop
```

删除某个 stash：

```bash
git stash drop stash@{0}
```

## apply 和 pop 怎么选

重要改动优先用 `apply`。

`pop` 会在应用成功后删除 stash，如果应用过程中出现冲突，处理起来更容易慌。

稳妥流程：

```bash
git stash apply stash@{0}
git status
git diff
git stash drop stash@{0}
```

## 常见误区

### 1. 把 stash 当长期存储

stash 适合临时保存，不适合长期保存重要工作。

重要工作应该尽快 commit 到明确分支。

### 2. 忘记保存未跟踪文件

默认 `git stash` 不一定保存未跟踪文件，建议使用：

```bash
git stash push -u
```

### 3. stash 太多不清理

stash 多了之后很难知道每个保存点是什么。

建议每次加 `-m` 说明用途。

## 延伸阅读

- [git stash 官方文档](https://git-scm.com/docs/git-stash)
- [Pro Git: Stashing and Cleaning](https://git-scm.com/book/en/v2/Git-Tools-Stashing-and-Cleaning)
- [Atlassian: git stash](https://www.atlassian.com/git/tutorials/saving-changes/git-stash)
- [推荐阅读索引](../09-resources/recommended-reading.md)
