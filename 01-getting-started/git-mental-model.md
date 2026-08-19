# Git Mental Model

[English](01-getting-started_en/git-mental-model_en.md)

这篇是 Git 心智模型系列的总入口。四区域模型适合快速判断日常操作，更深入的系列会从快照、对象、引用和历史变化解释 Git 为什么这样工作。

## 旗舰系列

1. [快照与状态：HEAD、Index 与 Working Tree](git-mental-model-01-snapshots.md)
2. [对象图：blob、tree 与 commit](git-mental-model-02-object-graph.md)

第一章通过同一个文件的三个版本，演示 `git add` 和 `git commit` 实际记录什么，并提供[交互演示](../interactive/git-mental-model/snapshots-and-state.html)和[可运行实验](../labs/git-mental-model/01-snapshots-and-state/README.md)。

第二章沿 commit 进入对象库，拆解 blob、tree 与 commit 的责任边界，并提供[对象图交互演示](../interactive/git-mental-model/object-graph.html)和[可运行实验](../labs/git-mental-model/02-object-graph/README.md)。

## 四区域快速模型

理解 Git，先理解四个区域：

```text
working tree -> index -> local repository -> remote repository
```

## Working tree

你正在编辑的文件。

查看：

```bash
git status
```

## Index

也叫 staging area，表示下一次 commit 会包含什么。

```bash
git add <file>
git diff --cached
```

## Local repository

本地 commit 历史。

```bash
git log --oneline
```

## Remote repository

远端仓库，比如 GitHub 上的 `origin`。

```bash
git fetch
git pull --rebase
git push
```

## Key idea

Git 大多数命令都在移动这几个区域之间的内容。

先判断文件现在在哪个区域，再选择命令，误操作会少很多。

## 常见命令对应关系

| 命令 | 主要影响 |
| --- | --- |
| `git add` | 工作区 -> 暂存区 |
| `git commit` | 暂存区 -> 本地仓库 |
| `git restore` | 丢弃或恢复工作区内容 |
| `git restore --staged` | 默认用 `HEAD` 恢复 Index，Working Tree 保持不变 |
| `git push` | 本地仓库 -> 远端仓库 |
| `git fetch` | 远端仓库 -> 本地远端引用 |
| `git pull` | fetch + merge 或 fetch + rebase |

## 为什么这个模型重要

很多 Git 事故都来自没有判断清楚当前改动在哪个区域。

例如：

- 改动在工作区，应该用 `git restore` 或 `git stash`
- 改动已经暂存，应该先 `git restore --staged`
- commit 已经产生但没 push，可以用 `reset` 或 `commit --amend`
- commit 已经 push，通常优先用 `revert`

先判断区域，再选择命令，是 Git 排错的第一原则。

## 延伸阅读

- [Pro Git: Git Basics](https://git-scm.com/book/en/v2/Git-Basics-Getting-a-Git-Repository)
- [git status 官方文档](https://git-scm.com/docs/git-status)
- [git restore 官方文档](https://git-scm.com/docs/git-restore)
- [推荐阅读索引](../09-resources/recommended-reading.md)
