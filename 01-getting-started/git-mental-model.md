# Git Mental Model

[English](01-getting-started_en/git-mental-model_en.md)

这篇是 Git 心智模型系列的总入口。四区域模型适合快速判断日常操作，更深入的系列会从快照、对象、引用和历史变化解释 Git 为什么这样工作。

先了解[为什么在 AI 时代学 Git](why-learn-git.md)，再打开[交互学习](https://xirong.github.io/my-git/interactive/git-mental-model/)。[完整学习路径](git-learning-path.md)把十个递进主题的文章、交互和临时仓库实验放在同一顺序中。[知识地图](knowledge-map.md)说明这条原理路径在什么情况下进入一次变更或协作决策。

## 旗舰系列

1. [快照与状态：HEAD、Index 与 Working Tree](git-mental-model-01-snapshots.md) · [交互](../interactive/git-mental-model/snapshots-and-state.html) · [实验](../labs/git-mental-model/01-snapshots-and-state/README.md)
2. [对象图：blob、tree 与 commit](git-mental-model-02-object-graph.md) · [交互](../interactive/git-mental-model/object-graph.html) · [实验](../labs/git-mental-model/02-object-graph/README.md)
3. [Index 是下一次 commit 的草稿](git-mental-model-03-index.md) · [交互](../interactive/git-mental-model/index-as-draft.html) · [实验](../labs/git-mental-model/03-index/README.md)
4. [引用、HEAD 与身份](git-mental-model-04-refs.md) · [交互](../interactive/git-mental-model/refs-and-head.html) · [实验](../labs/git-mental-model/04-refs/README.md)
5. [可达性、reflog 与恢复](git-mental-model-05-recovery.md) · [交互](../interactive/git-mental-model/reachability-and-recovery.html) · [实验](../labs/git-mental-model/05-recovery/README.md)
6. [Merge 先找共同祖先，再合并两条历史](git-mental-model-06-merge.md) · [交互](../interactive/git-mental-model/three-way-merge.html) · [实验](../labs/git-mental-model/06-merge/README.md)
7. [Rebase 重放变化，分支引用指向新历史](git-mental-model-07-rebase.md) · [交互](../interactive/git-mental-model/rebase-and-replay.html) · [实验](../labs/git-mental-model/07-rebase/README.md)
8. [远端是另一仓库，origin/main 是本地记录](git-mental-model-08-remote.md) · [交互](../interactive/git-mental-model/remote-and-fetch.html) · [实验](../labs/git-mental-model/08-remote/README.md)
9. [Worktree 共享对象，隔离检出状态](git-mental-model-09-worktree.md) · [交互](../interactive/git-mental-model/worktree-and-isolation.html) · [实验](../labs/git-mental-model/09-worktree/README.md)
10. [逻辑快照与物理存储是两层问题](git-mental-model-10-storage.md) · [交互](../interactive/git-mental-model/storage-and-maintenance.html) · [实验](../labs/git-mental-model/10-storage/README.md)

第一章通过同一个文件的三个版本，演示 `git add` 和 `git commit` 实际记录什么，并提供[交互演示](../interactive/git-mental-model/snapshots-and-state.html)和[可运行实验](../labs/git-mental-model/01-snapshots-and-state/README.md)。

第二章沿 commit 进入对象库，拆解 blob、tree 与 commit 的责任边界，并提供[对象图交互演示](../interactive/git-mental-model/object-graph.html)和[可运行实验](../labs/git-mental-model/02-object-graph/README.md)。

第三章深入 Index，演示部分暂存、`git diff --cached`、安全取消暂存与冲突 stage 1、2、3，并提供[Index 草稿交互演示](../interactive/git-mental-model/index-as-draft.html)和[可运行实验](../labs/git-mental-model/03-index/README.md)。

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

这张图是操作概览，不表示文件只能处于一个区域，也不表示每次操作都把文件搬走。工作区、Index 和 HEAD 可以同时表示不同版本；远端也是一个仓库，拥有自己的对象和引用。

先比较版本和引用，再判断操作会改变什么。分支是指向 commit 的引用，commit 关联快照；不要把分支理解成另一份目录。

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

- 要保留工作区改动，先保存现场；`restore` 工作文件可能丢弃编辑，不能当作通用保存操作。
- 只想取消暂存，`git restore --staged` 更新 Index，保留工作区。
- 要修改已有提交，先确认引用、共享情况和备份；`reset` 的不同模式对工作区影响不同。
- 已共享历史通常通过 `revert` 追加撤销提交；数据库和外部副作用还需要另行处理。

先判断区域，再选择命令，是 Git 排错的第一原则。

## 延伸阅读

- [Pro Git: Git Basics](https://git-scm.com/book/en/v2/Git-Basics-Getting-a-Git-Repository)
- [git status 官方文档](https://git-scm.com/docs/git-status)
- [git restore 官方文档](https://git-scm.com/docs/git-restore)
- [推荐阅读索引](../09-resources/recommended-reading.md)
