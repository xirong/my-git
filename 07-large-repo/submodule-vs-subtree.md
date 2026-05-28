# Submodule vs Subtree

共享代码常见方案有 submodule 和 subtree。

两者都能把外部仓库内容纳入当前项目，但使用体验和维护成本差异很大。

## Submodule

Submodule 让当前仓库记录另一个仓库的特定 commit。

适合：

- 需要精确引用外部仓库版本
- 外部仓库有独立生命周期
- 当前项目不想直接复制外部代码

常用命令：

```bash
git submodule add <url> path/to/module
git submodule update --init --recursive
```

缺点：

- 新成员容易忘记初始化
- 分支切换后 submodule 状态容易混乱
- PR Review 时要同时看父仓库和子仓库
- CI 需要正确拉取 submodule

## Subtree

Subtree 把外部仓库内容合入当前仓库的子目录。

适合：

- 希望使用者无感知
- 外部代码更新频率不高
- 当前仓库希望直接包含完整代码

常见特点：

- clone 后直接有代码
- 不需要额外初始化
- 同步上下游时流程更重
- 历史可能变复杂

## 怎么选

| 场景 | 建议 |
| --- | --- |
| 第三方库独立维护 | submodule |
| 团队内部共享代码但使用者要简单 | subtree |
| 频繁共同演进的核心代码 | 考虑 monorepo 或包管理 |
| 只是复用少量代码 | 重新评估是否该抽库 |

## 工程建议

不要为了“复用”过早引入 submodule。

很多团队的 submodule 问题，本质上是代码边界没有设计清楚。

如果共享代码需要频繁和主仓库一起改，monorepo、包管理或直接合并模块，可能比 submodule 更稳。

## 延伸阅读

- [Pro Git: Submodules](https://git-scm.com/book/en/v2/Git-Tools-Submodules)
- [git submodule 官方文档](https://git-scm.com/docs/git-submodule)
- [Atlassian: Git subtree](https://www.atlassian.com/git/tutorials/git-subtree)
- [Large Repository Git Practices](large-repo-git-practices.md)
