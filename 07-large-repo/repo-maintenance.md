# Repo Maintenance

大仓库需要定期维护。

仓库维护不是只跑 `git gc`，还包括文件边界、历史体积、分支清理、依赖治理和文档时效性。

## 检查项

- 是否有大文件误提交
- 是否有生成文件进仓库
- 是否有长期无用分支
- 是否有失效 submodule
- 是否有过期文档和链接
- 是否有泄露 secret
- 是否有长期无人维护的 CI job

## 本地对象检查

```bash
git count-objects -vH
```

这个命令能看到对象数量和体积，用于判断仓库是否需要清理。

## 本地维护命令

```bash
git gc
git maintenance start
git commit-graph write --reachable
```

这些命令是否适合，要结合团队环境、Git 版本、仓库规模确认。

## 分支清理

查看已合并分支：

```bash
git branch --merged
```

删除本地分支：

```bash
git branch -d feature/old-task
```

清理远端已删除分支引用：

```bash
git fetch --prune
```

## 大文件治理

定期检查：

- 是否有超过团队阈值的文件
- 是否有日志、dump、zip、构建产物
- 是否应该迁移到 Git LFS
- 是否需要清理历史

## 文档维护

这个仓库本身也需要维护：

- 老链接是否失效
- 旧建议是否过时
- 是否有更权威的官方文档
- 文档内容是否和当前 Git/GitHub 行为一致

## 延伸阅读

- [git maintenance 官方文档](https://git-scm.com/docs/git-maintenance)
- [git gc 官方文档](https://git-scm.com/docs/git-gc)
- [git commit-graph 官方文档](https://git-scm.com/docs/git-commit-graph)
- [Large Repository Git Practices](large-repo-git-practices.md)
