# Large Repository Git Practices

大仓库的核心问题通常不在某条 Git 命令，而在历史太大、文件太多、依赖太重、协作边界不清。

## 1. Clone 策略

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

## 2. 工作策略

- 用 `worktree` 并行处理多个分支
- 用 CODEOWNERS 表达路径责任
- PR 按路径聚焦，避免跨域大改
- 生成文件、日志、dump 不进仓库

## 3. 大文件

大文件优先使用 Git LFS。

不要把以下内容直接提交进 Git：

- 日志
- 数据库 dump
- 构建产物
- 临时压缩包
- 大二进制中间文件

## 4. 仓库维护

```bash
git maintenance start
git gc
git commit-graph write --reachable
```

具体命令是否适合，要结合团队环境和 Git 版本确认。

## 5. 企业实践参考

[Microsoft Scalar 与大仓库 Git 实践](../09-resources/company-practices/microsoft-scalar-large-repo.md) 的启发是，大仓库优化通常要组合使用 partial clone、sparse checkout、后台维护、文件系统监控和构建系统能力。

不要只优化 clone。开发者日常更常遇到的是 `status`、`fetch`、`checkout`、IDE 索引和构建速度问题。

Git 新版本也在持续补强大仓库体验，尤其是 reftable、partial clone、sparse checkout、config-based hooks 等方向，见 [Git 版本演进笔记](../09-resources/git-version-upgrade-notes.md)。

## 延伸阅读

- [Git partial clone](https://git-scm.com/docs/partial-clone.html)
- [Git sparse checkout](https://git-scm.com/docs/sparse-checkout)
- [git worktree](https://git-scm.com/docs/git-worktree)
- [Git LFS](https://git-lfs.com)
- [Microsoft Scalar 与大仓库 Git 实践](../09-resources/company-practices/microsoft-scalar-large-repo.md)
- [Git 版本演进笔记](../09-resources/git-version-upgrade-notes.md)
- [推荐阅读索引](../09-resources/recommended-reading.md)
