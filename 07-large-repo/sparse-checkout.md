# Sparse Checkout

Sparse checkout 用于让工作区只保留部分目录。

它适合 monorepo 或大仓库：仓库里有很多项目，但你当前只需要少数目录。

## 示例

初始化 cone mode：

```bash
git sparse-checkout init --cone
```

只 checkout 指定目录：

```bash
git sparse-checkout set services/order services/payment
```

查看当前规则：

```bash
git sparse-checkout list
```

恢复完整工作区：

```bash
git sparse-checkout disable
```

## 适合场景

- monorepo 很大
- 当前任务只涉及少数目录
- CI 只需要部分路径
- 本地磁盘和 checkout 时间需要优化

## 和 partial clone 搭配

Sparse checkout 控制工作区有哪些路径。

Partial clone 控制对象下载策略。

组合使用：

```bash
git clone --filter=blob:none --sparse <url>
cd repo
git sparse-checkout set services/order
```

## 注意事项

- 构建脚本可能隐式依赖其他目录
- IDE 索引可能只看到 sparse 范围内文件
- 团队要明确哪些目录可以独立工作

## 延伸阅读

- [Git sparse checkout 官方文档](https://git-scm.com/docs/sparse-checkout)
- [Partial Clone](partial-clone.md)
- [Large Repository Git Practices](large-repo-git-practices.md)
- [推荐阅读索引](../09-resources/recommended-reading.md)
