# Microsoft Scalar 与大仓库 Git 实践

原文链接：

- [The Story of Scalar](https://github.blog/open-source/git/the-story-of-scalar/)
- [Get up to speed with partial clone and shallow clone](https://github.blog/open-source/git/get-up-to-speed-with-partial-clone-and-shallow-clone/)
- [Git partial clone documentation](https://git-scm.com/docs/partial-clone)
- [Git sparse-checkout documentation](https://git-scm.com/docs/git-sparse-checkout)

说明：本文是面向本仓库读者的改写版，结合 GitHub Blog 与 Git 官方文档，整理为大仓库实践参考。

## 1. 大仓库的真实问题

仓库变大以后，开发者最先感受到的通常是：

- clone 太慢
- fetch 太慢
- checkout 太慢
- `git status` 太慢
- 工作区文件太多
- 历史对象和大文件拖慢本地操作

Microsoft Scalar 的故事说明，大仓库优化不能只靠“换一台更快的电脑”，需要组合使用 Git 的多项能力。

## 2. Scalar 的核心思路

Scalar 把多项适合大仓库的配置组合起来：

- partial clone，减少历史对象下载
- sparse checkout，只 checkout 当前需要的目录
- background maintenance，后台维护仓库性能
- 文件系统监控，减少状态扫描成本
- 针对大仓库的默认配置

对普通团队来说，重点是理解这些能力为什么要组合使用，不必一开始就要求所有人使用 Scalar。

## 3. Partial clone

Partial clone 适合减少初始 clone 和后续 fetch 下载的数据量。

常见方式：

```bash
git clone --filter=blob:none <url>
```

这类 blobless clone 会先下载 commit 和 tree，需要文件内容时再按需下载 blob。

适合：

- 开发者日常使用大仓库
- 历史里有大量文件内容
- 需要保留正常历史操作能力

注意：

- 首次访问某些历史文件内容时会触发额外下载
- 服务器需要支持 partial clone
- 需要团队文档说明哪些命令可能触发按需下载

## 4. Shallow clone

Shallow clone 只拉取部分提交历史：

```bash
git clone --depth 1 <url>
```

适合：

- 一次性 CI 构建
- 临时检查
- 不需要历史分析的自动化任务

不适合：

- 开发者长期工作区
- 需要 `git blame`、复杂 merge-base、历史追溯的场景
- 后续还要长期 fetch 的工作区

## 5. Sparse checkout

Sparse checkout 让工作区只保留部分目录：

```bash
git sparse-checkout init --cone
git sparse-checkout set service-a service-b
```

适合：

- Monorepo 中只负责某几个服务
- 构建系统能明确依赖哪些路径
- 工作区文件数量已经影响 IDE 和 Git 性能

Microsoft Scalar 的经验里，cone mode sparse checkout 是关键优化方向，因为按目录选择比任意 pattern 更容易获得稳定性能。

## 6. 大仓库团队的落地顺序

推荐顺序：

1. 先识别仓库慢在哪里，clone、fetch、status、checkout 分开看
2. CI 用 shallow clone 或 treeless/blobless clone 做针对性优化
3. 开发者工作区优先尝试 blobless partial clone
4. Monorepo 开启 sparse checkout，按团队或服务定义目录集合
5. 开启仓库维护能力，比如 `git maintenance`
6. 清理不该进入 Git 的大文件和生成产物

## 7. 对本仓库的启发

大仓库优化要避免单点思维：

- partial clone 解决对象下载
- sparse checkout 解决工作区规模
- maintenance 解决本地仓库维护
- LFS 解决大二进制文件
- CODEOWNERS 解决路径责任
- CI 缓存和构建系统解决构建成本

这些能力需要组合使用，才是真正可落地的大仓库实践。
