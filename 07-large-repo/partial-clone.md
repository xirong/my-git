# Partial Clone

Partial clone 用于减少 clone 时下载的 Git 对象。

大仓库中，历史和对象体积可能很大。Partial clone 可以让 Git 先拿必要元数据，blob 等对象按需下载。

## 示例

```bash
git clone --filter=blob:none <url>
```

常见含义：

- `--filter=blob:none`：先不下载文件内容对象，后续按需获取
- `--filter=tree:0`：进一步减少 tree 对象下载，适合更极端的大仓库场景

具体支持情况要看 Git 版本和远端服务能力。

## 适合场景

- 仓库历史很大
- 当前任务只需要部分文件
- CI 希望减少网络下载
- monorepo 初次 clone 太慢

## 注意事项

- 首次访问缺失对象时仍然会触发下载
- 某些老工具可能不理解 partial clone
- 和 sparse checkout 搭配效果更明显

## 推荐组合

```bash
git clone --filter=blob:none --sparse <url>
cd repo
git sparse-checkout set services/order
```

## 延伸阅读

- [Git partial clone 官方文档](https://git-scm.com/docs/partial-clone.html)
- [git clone 官方文档](https://git-scm.com/docs/git-clone)
- [Sparse Checkout](sparse-checkout.md)
- [Large Repository Git Practices](large-repo-git-practices.md)
