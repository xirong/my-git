# Git 2.45 到 2.54 版本演进笔记

原文链接：

- [Highlights from Git 2.45](https://github.blog/open-source/git/highlights-from-git-2-45/)
- [Highlights from Git 2.46](https://github.blog/open-source/git/highlights-from-git-2-46/)
- [Highlights from Git 2.47](https://github.blog/open-source/git/highlights-from-git-2-47/)
- [Highlights from Git 2.48](https://github.blog/open-source/git/highlights-from-git-2-48/)
- [Highlights from Git 2.49](https://github.blog/open-source/git/highlights-from-git-2-49/)
- [Highlights from Git 2.50](https://github.blog/open-source/git/highlights-from-git-2-50/)
- [Highlights from Git 2.51](https://github.blog/open-source/git/highlights-from-git-2-51/)
- [Highlights from Git 2.52](https://github.blog/open-source/git/highlights-from-git-2-52/)
- [Highlights from Git 2.54](https://github.blog/open-source/git/highlights-from-git-2-54/)
- [Git BreakingChanges](https://git-scm.com/docs/BreakingChanges/2.51.0)
- [Git reftable documentation](https://git-scm.com/docs/reftable)
- [GitLab: What's new in Git 2.54.0](https://about.gitlab.com/blog/whats-new-in-git-2-54-0/)

## 1. 为什么团队要关注 Git 新版本

普通开发者日常用到的 Git 命令变化不大，但大仓库、CI、历史改写、引用存储、安全和性能相关能力一直在演进。

团队负责人关注 Git 新版本，主要看这些方向：

- 大仓库性能
- sparse checkout 和 partial clone 体验
- hooks 和统一检查
- reftable 等底层存储演进
- SHA-256 迁移准备
- 历史改写和自动化脚本能力

## 2. 对工程团队最有价值的变化

### reftable

reftable 是 Git 引用存储的新后端方向，用于改善大量 refs 场景下的性能和一致性。

当前建议：

- 先在非关键仓库试点
- 不要直接全组织默认切换
- 关注 Git 3.0 相关 BreakingChanges
- 迁移前确认托管平台、CI 镜像、开发者本机 Git 版本都支持

### partial clone 与 sparse checkout 继续成熟

大仓库团队应持续关注：

- `git clone --filter=blob:none`
- `git sparse-checkout`
- sparse 工作区里的交互式 add
- CI 中不同 clone 策略的取舍

这些能力直接关系到 monorepo 和大仓库体验。

### config-based hooks

Git 2.54 引入 config-based hooks 方向，降低了多仓库共享 hooks 的成本。

它对团队的潜在价值：

- 统一 pre-commit 检查
- 统一 secret scan
- 统一 commit message 检查
- 按用户、系统或仓库配置不同 hooks

落地前要注意：

- 老版本 Git 是否支持
- 本地 hooks 和 CI 检查要保持一致
- hooks 只能做提前提醒，不能代替 CI 和服务端规则

### `git history`

Git 2.54 的 `git history reword` 和 `git history split` 处于实验性阶段。

它适合简化部分历史改写任务，比如改旧 commit message 或拆分 commit。

团队使用建议：

- 只用于本地未公开历史
- 公共分支历史仍要谨慎
- 写入故障手册时标注 Git 版本要求
- 现阶段仍保留 `git rebase -i` 作为通用方案

## 3. 升级策略

### 个人开发环境

可以较快升级，但要确认 IDE、GUI Git 客户端、pre-commit 工具兼容。

### CI 镜像

CI 镜像里的 Git 版本更关键。

如果文档推荐了 partial clone、sparse checkout、config hooks，就要在 CI 镜像中确认 Git 版本支持。

### 企业统一推广

推荐顺序：

1. 先在文档里标注命令版本要求
2. 非关键仓库试点
3. CI 镜像升级
4. 开发者工具链提示升级
5. 再推广到大仓库或核心仓库

## 4. 本仓库后续写作注意

当文章使用新能力时，要写清：

- 最低 Git 版本
- 是否实验性
- 是否影响公共历史
- 是否要求托管平台支持
- 是否适合 CI 或本地开发者长期使用

例如 `git history` 这类新命令，不要直接替代所有 `rebase -i` 教程。

