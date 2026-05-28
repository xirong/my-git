# Shallow Clone

Shallow clone 只拉取部分历史。

它适合 CI、临时检查、快速下载仓库，不适合需要完整历史分析的场景。

## 基础用法

只拉最近一次提交：

```bash
git clone --depth 1 <url>
```

只拉某个分支的浅历史：

```bash
git clone --depth 1 --branch main <url>
```

## 适合场景

- CI 只需要当前版本源码
- 临时查看项目
- 构建镜像时降低拉取时间
- 仓库历史很大，但当前任务不需要历史

## 不适合场景

- 需要 `git blame`
- 需要 `git bisect`
- 需要生成完整 changelog
- 需要分析历史提交
- 需要切换很多历史分支或 tag

## 转成完整仓库

如果后续需要完整历史：

```bash
git fetch --unshallow
```

## 和 partial clone 的区别

Shallow clone 减少历史深度。

Partial clone 减少对象下载。

两者解决的问题不同，可以结合使用，但要确认你的 Git 版本和托管平台支持情况。

## 延伸阅读

- [git clone 官方文档](https://git-scm.com/docs/git-clone)
- [Partial Clone](partial-clone.md)
- [Large Repository Git Practices](large-repo-git-practices.md)
- [推荐阅读索引](../09-resources/recommended-reading.md)
