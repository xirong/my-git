# Rebase vs Merge

`merge` 和 `rebase` 都能把两条历史合到一起，但它们表达的协作语义不一样。

简单说：

- `merge` 保留分支合并历史
- `rebase` 把当前分支的提交移动到新的基底上

## 适合使用 merge 的场景

### 1. 合并公共分支

公共分支上的历史已经被别人看到或基于开发时，优先使用 merge 或 revert，避免随意重写历史。

### 2. 希望保留分支上下文

如果一个 feature 分支代表一组完整工作，merge commit 可以保留这次合入的上下文。

### 3. 团队要求审计清晰

一些团队希望从历史上看到“什么时候把哪条分支合进来”，这时 merge 更合适。

## 适合使用 rebase 的场景

### 1. 整理本地未 push 的提交

本地还没 push 时，可以用交互式 rebase 整理 commit：

```bash
git rebase -i HEAD~3
```

常见操作：

- 修改 commit message
- 合并零散 commit
- 调整提交顺序
- 删除无用 commit

### 2. 让 feature 分支跟上主分支

```bash
git fetch origin
git rebase origin/main
```

这样可以让你的分支历史排在最新主分支之后。

### 3. 保持 PR 历史更线性

部分团队喜欢线性历史，会要求 feature 分支合入前 rebase 到主分支最新位置。

## 高风险点

不要随意 rebase 已经被别人基于开发的公共分支。

GitHub 文档也提醒，rebase 会改写提交历史，已经 push 到仓库的 commit 再 rebase，会给其他协作者带来麻烦。

## 推荐规则

| 场景 | 推荐 |
| --- | --- |
| 本地未 push 的整理 | rebase |
| feature 分支同步主分支 | rebase 或 merge，按团队约定 |
| 主分支合并 PR | merge、squash、rebase merge，按仓库策略 |
| 公共历史出错 | revert |
| 已经有人基于你的分支开发 | 避免 rebase |

## 常用命令

```bash
git merge feature/login
git rebase origin/main
git rebase -i HEAD~3
git rebase --abort
git rebase --continue
```

## 延伸阅读

- [GitHub Docs: About Git rebase](https://docs.github.com/en/get-started/using-git/about-git-rebase)
- [Pro Git: Rebasing](https://git-scm.com/book/en/v2/Git-Branching-Rebasing)
- [Atlassian: Merging vs Rebasing](https://www.atlassian.com/git/tutorials/merging-vs-rebasing)
- [推荐阅读索引](../09-resources/recommended-reading.md)
