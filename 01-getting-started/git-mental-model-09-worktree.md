# Git 心智模型 09：Worktree 共享对象，隔离检出状态

[English](01-getting-started_en/git-mental-model-09-worktree_en.md) | [交互演示](../interactive/git-mental-model/worktree-and-isolation.html) | [可运行实验](../labs/git-mental-model/09-worktree/README.md)

一个仓库里既要修 `main` 的紧急问题，又要让 Agent 在 feature 分支做较长的改动时，反复 switch、stash 和 restore 会把上下文混在一起。`git worktree` 提供多个工作目录，让每个目录检出自己的分支，同时复用同一个 Git 对象库。

它解决的是 Git 检出状态的并行，不是进程、端口、数据库、仓库外缓存或环境变量的隔离。多个 worktree 能减少分支切换带来的文件覆盖，仍需要协调外部共享资源和最终集成。

## 场景：主线修复与 feature 并行

假设主工作树在 `main`，需要新增一个目录给 `feature/parallel`：

```text
common Git directory
  objects/                 commit、tree、blob 的共享对象库
  refs/heads/main          共享的普通分支引用
  refs/heads/feature/...   共享的普通分支引用

primary worktree
  HEAD -> main
  Index: primary 的下一次 commit 草稿
  Working Tree: primary 的磁盘文件

feature worktree
  HEAD -> feature/parallel
  Index: feature 的下一次 commit 草稿
  Working Tree: feature 的磁盘文件
```

`feature` 提交后，`primary` 可以直接读取这个提交对象并合入分支。合入 `main` 不会把 `feature` 工作树的 HEAD 自动切到 `main`。两处看到同一套对象和普通分支引用，却保留自己的 HEAD、Index 和已检出文件。

## 概念：共享什么，分开什么

`git worktree add <path> <commit-ish>` 创建 linked worktree。官方手册明确指出，它与当前仓库共享除每个 worktree 文件以外的内容，`HEAD`、`index` 就是典型的独立文件。

共享范围包括对象库和大多数普通 refs。一个 worktree 创建或推进 `feature/parallel` 后，另一个 worktree 可以用该分支名解析同一个提交。每个 worktree 的 HEAD 指向自己正在检出的分支，Index 也独立，所以可以同时各自暂存不同的文件。

Git 对某些每工作树的伪引用有特殊处理，`HEAD` 是最常见的一项。日常并行开发时，用下面的边界判断即可：

```text
同一对象库和普通分支引用：可以看到彼此已提交的 Git 对象
不同 HEAD、Index、Working Tree：可以独立检出、编辑、暂存
仓库外资源：Git 不负责锁定或隔离
```

## 创建、观察与移除 worktree

从 `main` 目录创建一个新分支和新目录：

```bash
git worktree add -b feature/agent-docs ../project-feature main
git worktree list --porcelain
```

分别检查两个位置：

```bash
git status --short
git -C ../project-feature status --short
git rev-parse --git-common-dir
git -C ../project-feature rev-parse --git-common-dir
git rev-parse --git-path HEAD
git -C ../project-feature rev-parse --git-path HEAD
git rev-parse --git-path index
git -C ../project-feature rev-parse --git-path index
```

预期是两个 `--git-common-dir` 归到同一处，HEAD 和 index 路径不同。只在 `main` 目录执行 `git add main-note.txt` 时，feature 的 `git diff --cached --name-only` 不应出现这个文件；反过来也成立。

完成 feature 后，在主工作树按团队的集成方式操作：

```bash
git status --short
git merge --no-ff feature/agent-docs
git status --short
git -C ../project-feature status --short
```

需要移除工作树时，先确认里面没有待保留文件：

```bash
git -C ../project-feature status --short
git worktree remove ../project-feature
git worktree list
```

正常使用 `git worktree remove`，它会检查不安全的删除情况。目录被手工移除后，才用 `git worktree prune` 清理陈旧管理记录。可移动磁盘或网络位置的工作树可先 `git worktree lock`，避免暂时不可见时被误判为陈旧。

## 同一分支的检出限制

如果 `main` 已由 `primary` 检出，下面的命令默认失败：

```bash
git worktree add ../another-main main
```

Git 的限制避免两个目录同时以同一个普通分支作为 HEAD，使一个位置提交或 reset 后，另一个位置对分支尖端的理解失去明确边界。不同分支可以并行：

```bash
git worktree add -b feature/review ../project-review main
```

`--force` 能绕开某些 worktree 保护。只有理解已有检出、协作约定和恢复路径时才考虑它；日常 Agent 并行任务应为每个工作树分配独立分支，或使用 detached HEAD 做纯检查。

## 外部共享资源仍需协调

Worktree 只管理各自目录内的 Git 检出状态。下面这些资源会跨 worktree 共享或竞争：

- 同一开发服务器端口。
- 仓库外的数据库、消息队列和测试账号。
- 位于仓库外的缓存、临时目录和日志路径。
- 被多个 worktree 指向的本地 `.env`、证书或生成目录。

例如两个 Agent 都启动 `localhost:3000`，第二个进程会因端口被占用而失败；Git 的 worktree 机制不会报告原因。给每个任务分配端口、临时目录和测试数据命名空间，再把实际映射写进交接记录。

## 在临时仓库运行实验

实验创建自己的 `primary` 和 `feature` 工作树，全部提交都在临时根目录内：

```bash
cd labs/git-mental-model/09-worktree
lab_path=$(bash setup.sh)
bash verify.sh "$lab_path"
sed -n '1,240p' "$lab_path/observations.txt"
sed -n '1,120p' "$lab_path/same-branch-results.txt"
bash cleanup.sh "$lab_path"
```

`verify.sh` 对真实 Git 状态做以下断言：

- primary 与 feature 的对象目录归到同一个 common Git directory，HEAD 和 Index 路径不同。
- `main-note.txt` 与 `feature-note.txt` 在提交前只出现在各自 Index。
- Git 拒绝第二个 `main` 检出，接受 `feature/parallel` 的检出。
- primary 合入 feature 后，primary 能看到 feature 文件，feature 的 HEAD 仍在自己的提交。
- 根目录中的 `external-resource.txt` 可由两处上下文写入，Git 没有为它提供隔离。

实验关闭全局 Git 配置、签名和调用方 hooks。`cleanup.sh` 只删除带本实验标记且结构完整的临时根目录。

完整自测：

```bash
bash labs/git-mental-model/09-worktree/test.sh
```

## 预测题：分支相同还是不同，Index 会怎样？

先在 `primary/main` 和 `feature/parallel` 分别暂存一个文件：

| 操作 | primary 的 Index | feature 的 Index | 预期 |
| --- | --- | --- | --- |
| primary 暂存 `main-note.txt` | 有 `main-note.txt` | 无 | 两份草稿独立 |
| feature 暂存 `feature-note.txt` | 无 `feature-note.txt` | 有 | 两份草稿独立 |
| 再为已检出的 `main` 创建 worktree | 不适用 | 不适用 | Git 拒绝 |
| 为 `feature/review` 创建 worktree | 原有内容保持 | 原有内容保持 | Git 允许 |

改变条件是目标分支是否已经被另一个 worktree 检出。若任务只需在同一提交上运行只读检查，可考虑 detached HEAD；若需要提交，给每个 Agent 独立分支并明确谁负责最终合入。

## Agent 迁移题：并行任务的交接清单

每个 Agent 的记录至少包含：

```text
worktree path: <absolute path>
branch and HEAD: <branch or detached> -> <oid>
Index state: clean | staged paths listed separately
working-tree state: clean | changed paths listed separately
integration owner and target branch: <person/agent> -> <branch>
external allocation: ports, temp directory, test-data namespace
```

这些字段让接手者可以区分“提交已共享，文件仍在另一个工作树”“本地草稿尚未提交”和“外部资源冲突”。`git worktree list --porcelain` 可作为路径、分支和 lock 状态的机器可读快照。

## 延伸阅读

- [git-worktree 官方手册](https://git-scm.com/docs/git-worktree)
- [gitrepository-layout 官方手册](https://git-scm.com/docs/gitrepository-layout)
- [gitrevisions 官方手册](https://git-scm.com/docs/gitrevisions)
- [实验说明](../labs/git-mental-model/09-worktree/README.md)
