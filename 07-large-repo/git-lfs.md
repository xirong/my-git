# Git LFS

Git LFS 用于管理大文件。

Git 本身适合管理文本和小文件。大二进制文件如果频繁进普通 Git 历史，会让仓库越来越慢，也会让 clone、fetch、diff 成本变高。

## 适合场景

- 图片
- 音视频
- 设计资源
- 模型文件
- 必须跟随版本的大二进制文件

## 不适合提交进 Git 的内容

- 日志
- 临时文件
- 构建产物
- 数据库 dump
- 本地缓存
- 可重新生成的中间文件

这些内容优先放对象存储、制品库或 CI 缓存。

## 基础用法

安装后启用：

```bash
git lfs install
```

跟踪某类文件：

```bash
git lfs track "*.psd"
git add .gitattributes
git add design.psd
git commit -m "chore(lfs): track design assets"
```

## 团队规则

- 先定义哪些文件必须走 LFS
- `.gitattributes` 进仓库
- 不把生成产物放进 LFS
- CI 环境确认已安装 Git LFS
- 定期检查是否有大文件误提交到普通 Git 历史

## 已经误提交大文件怎么办

需要清理历史，通常使用 `git filter-repo` 或 BFG Repo-Cleaner。

清理历史会影响协作者，必须提前通知团队。

## 延伸阅读

- [Git LFS 官方站点](https://git-lfs.com)
- [GitHub Docs: About Git Large File Storage](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-git-large-file-storage)
- [Large Repository Git Practices](large-repo-git-practices.md)
- [推荐阅读索引](../09-resources/recommended-reading.md)
