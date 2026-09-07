# Pull Rebase

`git pull --rebase` 用于拉取远端更新，并把本地提交重新放到远端最新提交之后。

它常用于个人 feature 分支，目标是减少无意义 merge commit，让历史更线性。

## 普通 pull 做了什么

`git pull` 大致等价于：

```bash
git fetch
git merge
```

如果你的本地分支和远端分支都产生了新提交，普通 pull 可能会产生一个 merge commit。

## pull --rebase 做了什么

`<integration-branch>` 表示团队实际的集成分支，可能是 `main`、`master` 或 `develop`。

```bash
git pull --rebase origin <integration-branch>
```

大致等价于：

```bash
git fetch origin
git rebase origin/<integration-branch>
```

它会先拿到远端更新，再把你的本地提交放到远端最新提交之后。

## 适合场景

- 个人 feature 分支
- 本地提交还没 push
- 团队偏好线性历史
- 希望同步主分支时减少 merge commit

## 不适合场景

- 当前分支是多人共享分支
- 本地提交已经被别人基于开发
- 你不了解 rebase 的影响
- 当前分支冲突复杂，缺少备份

## 推荐流程

先让 `git status --porcelain` 没有输出。已有编辑只有在全部属于自己并明确准备 stash 后恢复时才可放进 stash；其他 owner 的编辑或来源不清的未跟踪文件要留在原处，改用干净 worktree。

```bash
git status --porcelain
git pull --rebase origin <integration-branch>
```

如果冲突处理乱了：

```bash
git rebase --abort
```

## 延伸阅读

- [GitHub Docs: About Git rebase](https://docs.github.com/en/get-started/using-git/about-git-rebase)
- [git pull 官方文档](https://git-scm.com/docs/git-pull)
- [git rebase 官方文档](https://git-scm.com/docs/git-rebase)
- [Rebase vs Merge](rebase-vs-merge.md)
