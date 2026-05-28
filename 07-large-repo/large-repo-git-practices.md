# Large Repository Git Practices

大仓库的核心问题通常不在某条 Git 命令，而在历史太大、文件太多、依赖太重、协作边界不清。

## 1. 先判断慢在哪里

大仓库优化前，先把问题拆开：

| 症状 | 常见原因 | 优先看 |
| --- | --- | --- |
| `git clone` 很慢 | 历史和 blob 太大 | partial clone、shallow clone |
| `git checkout` 很慢 | 工作区文件太多 | sparse checkout、路径拆分 |
| `git status` 很慢 | 文件数量太多、未跟踪文件太多 | `.gitignore`、fsmonitor、仓库维护 |
| CI 拉代码很慢 | 每个 job 重复 clone 完整仓库 | shallow clone、partial clone、缓存 |
| IDE 索引很慢 | checkout 了无关目录 | sparse checkout、按服务打开工程 |
| PR Review 很慢 | 跨目录、跨 owner 大改 | CODEOWNERS、拆 PR、路径责任 |

先定位瓶颈，再选方案。不要所有团队一上来就追求 monorepo 工具平台化。

## 2. Clone 策略

### Shallow clone

只拉部分历史：

```bash
git clone --depth 1 <url>
```

适合 CI、临时检查，不适合需要完整历史分析的场景。

### Partial clone

减少对象下载：

```bash
git clone --filter=blob:none <url>
```

官方文档见 [partial clone](https://git-scm.com/docs/partial-clone.html)。

### Sparse checkout

只 checkout 部分目录：

```bash
git sparse-checkout init --cone
git sparse-checkout set service-a service-b
```

官方文档见 [sparse checkout](https://git-scm.com/docs/sparse-checkout)。

## 3. 策略选择

| 场景 | 推荐做法 | 注意事项 |
| --- | --- | --- |
| CI 只需要跑一次构建 | shallow clone | 不适合依赖完整历史的版本计算 |
| 开发者只负责少数目录 | sparse checkout | 目录边界要稳定 |
| 仓库历史和 blob 都很大 | partial clone | 需要确认服务端和工具链支持情况 |
| 多分支并行开发 | worktree | 每个 worktree 都要有清楚的分支名 |
| 大二进制文件必须进仓库 | Git LFS | 需要配套权限、存储和清理策略 |
| 多团队共享一个仓库 | CODEOWNERS | owner 规则不要细到没人能批 |

## 4. 工作策略

- 用 `worktree` 并行处理多个分支
- 用 CODEOWNERS 表达路径责任
- PR 按路径聚焦，避免跨域大改
- 生成文件、日志、dump 不进仓库

## 5. 大文件

大文件优先使用 Git LFS。

不要把以下内容直接提交进 Git：

- 日志
- 数据库 dump
- 构建产物
- 临时压缩包
- 大二进制中间文件

## 6. 仓库维护

```bash
git maintenance start
git gc
git commit-graph write --reachable
```

具体命令是否适合，要结合团队环境和 Git 版本确认。

## 7. 企业实践参考

[Microsoft Scalar 与大仓库 Git 实践](../10-company-practices/microsoft-scalar-large-repo.md) 的启发是，大仓库优化通常要组合使用 partial clone、sparse checkout、后台维护、文件系统监控和构建系统能力。

不要只优化 clone。开发者日常更常遇到的是 `status`、`fetch`、`checkout`、IDE 索引和构建速度问题。

Git 新版本也在持续补强大仓库体验，尤其是 reftable、partial clone、sparse checkout、config-based hooks 等方向，见 [Git 版本演进笔记](../09-resources/git-version-upgrade-notes.md)。

[Uber GitFarm 与 Git 服务化实践](../10-company-practices/uber-gitfarm.md) 进一步提醒我们，当 monorepo 大到一定程度，Git 成本会从开发者本机扩散到 CI、构建、发布、静态分析等自动化系统。此时优化目标包含个人 clone 速度，也包含自动化系统重复 clone 和 checkout 的成本。

## 延伸阅读

- [Git partial clone](https://git-scm.com/docs/partial-clone.html)
- [Git sparse checkout](https://git-scm.com/docs/sparse-checkout)
- [git worktree](https://git-scm.com/docs/git-worktree)
- [Git LFS](https://git-lfs.com)
- [Microsoft Scalar 与大仓库 Git 实践](../10-company-practices/microsoft-scalar-large-repo.md)
- [Meta Sapling 与堆叠提交实践](../10-company-practices/meta-sapling-stacked-commits.md)
- [Uber GitFarm 与 Git 服务化实践](../10-company-practices/uber-gitfarm.md)
- [Git 版本演进笔记](../09-resources/git-version-upgrade-notes.md)
- [推荐阅读索引](../09-resources/recommended-reading.md)
