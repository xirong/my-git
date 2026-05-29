# Git vs SVN

很多人第一次接触 Git 时，会自然地用 SVN 的方式理解它。

这会带来一个问题：你能用 Git 完成提交和更新，但很难发挥 Git 在本地提交、分支、合并、PR 协作上的真正价值。

## 核心差异

| Topic | SVN | Git |
| --- | --- | --- |
| 仓库模型 | 中心仓库为主 | 每个人都有完整本地仓库 |
| 提交位置 | 通常直接提交到中心仓库 | 先提交到本地仓库 |
| 分支成本 | 相对高 | 很低，日常使用 |
| 离线工作 | 能力较弱 | 可以完整提交、查看历史、切分支 |
| 协作方式 | 偏集中 | 偏分布式 |
| 审查方式 | 常依赖提交后检查 | 常通过 PR 合入前审查 |

## 从 SVN 迁到 Git 时最容易踩的坑

### 1. 只在最后一次性 commit

SVN 时代很多人习惯“写完再提交”。

Git 更推荐按逻辑分批提交，每个 commit 都表达一个清楚意图。

### 2. 害怕创建分支

Git 分支非常轻量，日常任务应该优先用分支隔离。

推荐：

```bash
git switch -c feat/my-task
```

### 3. 把 pull 当成无脑同步

`git pull` 实际上包含 fetch 和 merge，使用不当会产生很多无意义 merge commit。

个人 feature 分支上，可以考虑：

```bash
git pull --rebase
```

但不要随意 rebase 已经被别人基于开发的公共分支。

### 4. 忽略 PR Review

Git 的价值不只在本地命令，也在合入前审查。

团队应该尽量通过 PR 合入主分支，而不是人人直接 push 主分支。

## 什么时候还会遇到 SVN

- 老系统仍在使用 SVN
- 部分文档或制品仓库还保留 SVN
- 公司从 SVN 迁 Git 的过渡阶段

如果要迁移，建议先统一团队分支策略、提交规范和主分支保护规则，再迁移工具。

## 延伸阅读

- [Pro Git: Distributed Git](https://git-scm.com/book/en/v2/Distributed-Git-Distributed-Workflows)
- [Atlassian: Migrating from SVN to Git](https://www.atlassian.com/git/tutorials/migrating-overview)
- [Git Workflow Tutorial（归档）](../09-resources/legacy/git-workflow-tutorial.md)
- [推荐阅读索引](../09-resources/recommended-reading.md)
