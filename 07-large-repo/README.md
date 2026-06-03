# 大仓库实践

这个目录面向 monorepo、大历史仓库、大二进制文件、多服务混合仓库和 CI clone 成本很高的团队。

## 先判断慢在哪里

| 症状 | 建议阅读 |
| --- | --- |
| 不知道整体该怎么优化 | [Large Repository Git Practices](large-repo-git-practices.md) |
| clone 太慢，只需要部分历史 | [Shallow Clone](shallow-clone.md) |
| 历史和 blob 太大 | [Partial Clone](partial-clone.md) |
| 只关心部分目录 | [Sparse Checkout](sparse-checkout.md) |
| 大文件必须进仓库 | [Git LFS](git-lfs.md) |
| 多分支并行开发 | [Worktree](../02-daily-workflow/worktree.md) |
| 仓库运行越来越慢 | [Repo Maintenance](repo-maintenance.md) |

## 架构取舍

- [Submodule vs Subtree](submodule-vs-subtree.md)

共享代码、跨仓依赖、组件复用时，不要只看 Git 命令是否可行，还要看团队协作成本、发布节奏、权限边界和故障恢复方式。

## 落地顺序

1. 先定位慢在 clone、checkout、status、fetch、CI 还是 IDE 索引
2. 再选择 shallow clone、partial clone、sparse checkout、LFS 或 repo maintenance
3. 对 CI 和开发者本机分别优化
4. 对大文件和生成文件建立仓库规则
5. 对关键路径配置 CODEOWNERS 和 Review 规则

## 相关内容

- [GitHub 工程治理](../04-github-engineering/README.md)
- [大厂工程实践案例](../10-company-practices/README.md)
- [Microsoft Scalar 与大仓库 Git 实践](../10-company-practices/microsoft-scalar-large-repo.md)
- [Uber GitFarm 与 Git 服务化实践](../10-company-practices/uber-gitfarm.md)
