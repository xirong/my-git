# Git 心智模型 10：逻辑快照与物理存储是两层问题

[English](01-getting-started_en/git-mental-model-10-storage_en.md) | [交互演示](../interactive/git-mental-model/storage-and-maintenance.html) | [可运行实验](../labs/git-mental-model/10-storage/README.md)

某个仓库有很多提交、很多相近文件，`.git/objects` 占用空间变大时，容易把“每次 commit 都复制一份项目”当成解释。Git 的逻辑模型是提交、tree 和 blob 组成的快照图；物理层可以把对象保留为 loose object，或重排进 pack file，并用 delta 压缩相近对象。物理布局可以变化，同一个提交可见的内容不应变化。

本章讨论如何观察这两个层面，`repack`、`gc`、`prune` 分别负责什么，以及为什么 commit-graph 是加速元数据，不是业务快照的一部分。

## 场景：历史增长后，能否“清理 Git”

团队看到对象目录增长，想运行维护命令。先把问题分成四个层次：

```text
逻辑内容：git show <commit> 展示的提交、tree、blob 内容
可达性：哪些对象仍能从 branch、tag、reflog 等引用路径找到
物理布局：loose object、pack、delta、pack index 如何存放对象
辅助元数据：commit-graph 如何帮助遍历提交历史
```

如果 `main` 仍指向提交 C，正常的 repack 或 commit-graph 写入不应改变 `git show C` 的输出。删除一个分支引用后，该分支独有的对象是否会被清掉还受其他引用、reflog、过期策略和维护时间影响。把“分支已删”直接推导为“对象立刻消失”会遗漏恢复窗口。

## 概念：快照的逻辑含义不取决于 pack 布局

commit 指向 root tree，tree 指向路径和 blob 或子 tree，blob 保存文件内容。对象 ID 由对象类型与内容决定，Git 可以复用相同内容的对象。多个 commit 经常共享未变化文件的 blob 和 tree。

物理层开始时，许多对象可能各自保存在 `.git/objects/` 的 loose 文件中。`git repack` 可以把对象写入一个或多个 `.pack` 文件，并用 `.idx` 提供索引。相近对象可以用 delta 表示“相对另一对象的差异”。读出对象时 Git 会还原出相同的逻辑对象内容。

因此下列两句话同时成立：

```text
一个 commit 语义上是一次完整快照。
Git 在磁盘上可以共享对象，并压缩相近对象。
```

不能用“快照”推导“每次提交复制整棵工作目录”，也不能用 pack 中有 delta 推导“历史内容不完整”。

## 观察物理结构，不把观察写成性能结论

先看当前对象统计和 pack 目录：

```bash
git count-objects -vH
git rev-parse --git-path objects/pack
git verify-pack -v .git/objects/pack/*.idx
```

`count-objects` 的计数和字节数会随 Git 版本、对象哈希格式、压缩参数、文件内容、已执行的自动维护和机器环境变化。`verify-pack` 可以显示本次 pack 的对象与 delta 链信息。它们适合定位和比较同一受控实验，不能单独证明“仓库性能好”或定义所有项目都应达到的固定阈值。

对可丢弃副本或已完成备份且没有并发 Git 写入的维护窗口，常见命令是：

```bash
git status --short
git repack -ad
git commit-graph write --reachable
git commit-graph verify
git gc --no-prune
```

`repack -a` 把可达对象考虑进新的 pack，`-d` 会删除被新 pack 替代的 pack，并清理由 pack 覆盖的冗余 loose object。`gc` 编排多项仓库维护；`--no-prune` 明确保留 loose object 的删除动作，适合作为本章实验中较窄的观察步骤。生产或协作仓库的维护窗口需要结合仓库规模、磁盘空间、当前 Git 进程和团队发布流程评估。

## `gc`、`prune` 与可达性的安全边界

`git gc` 是面向日常维护的上层入口，会处理多种 housekeeping 任务。默认 prune 过期策略不会立即删除所有不可达对象，给 reflog 和误操作恢复留出时间。

`git prune` 是更低层的命令。官方手册建议大多数场景使用 `git gc`，因为它会连同其他维护任务一起处理 pruning。`git prune --expire=now` 会立即处理符合条件的 loose object；在另一个 Git 进程正写入同一仓库时，这会提高损坏风险。

执行破坏性维护前至少确认：

1. 目标是精确的本地仓库或可删除的副本，路径与当前目录一致。
2. 当前工作区、需要保留的分支和 tag 已检查，必要对象已有可恢复来源。
3. 没有 clone、fetch、repack、GC、IDE 后台 Git 或其他进程同时写对象库。
4. 命令、过期参数和预期删除范围已记录，优先先用 `git prune -n` 观察候选项。

不要把实验中的 `git prune --expire=now` 复制到协作仓库。它在本章实验里只删除脚本刚写入、没有任何引用指向的一个 blob，且实验根目录可整体移除。

## commit-graph：遍历加速的辅助文件

commit-graph 是序列化的提交图文件。`git commit-graph write --reachable` 从可达 refs 出发生成图，`git commit-graph verify` 会将其内容与对象库交叉验证。它可以帮助 Git 更快地做某些提交图遍历；开启 changed-paths 相关数据时，还能帮助按路径查询历史。

它不改变 commit、tree、blob、branch 语义，也不代替 pack、reflog 或备份。看到 commit-graph 文件存在，只能确认辅助结构已写入；性能差异必须在固定工作负载、机器、Git 版本和配置下实际测量。

## 在临时仓库运行实验

实验创建 14 个相近的逻辑快照，并在独立临时仓库中执行物理维护：

```bash
cd labs/git-mental-model/10-storage
lab_path=$(bash setup.sh)
bash verify.sh "$lab_path"
sed -n '1,200p' "$lab_path/observations.txt"
diff -u "$lab_path/show-before.txt" "$lab_path/show-after.txt"
sed -n '1,120p' "$lab_path/count-before.txt"
sed -n '1,120p' "$lab_path/count-after.txt"
bash cleanup.sh "$lab_path"
```

`verify.sh` 断言真实 Git 行为：

- 同一个 stable commit 的 `git show` 输出在 repack、commit-graph write、`gc --no-prune` 和实验 orphan 的 prune 前后完全一致。
- pack、pack index 存在，`git verify-pack` 报告至少一个 delta 对象。
- commit-graph 文件存在且 `git commit-graph verify` 成功。
- `git prune --expire=now` 只删除脚本专门创建的不可达 blob，保留的提交仍可 show。

实验关闭全局 Git 配置、签名和调用方 hooks。它记录 `count-objects` 的实际输出，却不把字节数、对象数或运行时间写成性能结论。`cleanup.sh` 只删除有本实验标记且结构完整的临时根目录。

完整自测：

```bash
bash labs/git-mental-model/10-storage/test.sh
```

## 预测题：哪种改变会影响逻辑内容？

先选择一个仍被 `main` 引用的提交 C：

| 操作 | `git show C` | 对象物理结构 | 可达性 |
| --- | --- | --- | --- |
| `git repack -ad` | 保持一致 | pack 与 delta 可能改变 | C 仍由 `main` 可达 |
| 写入、验证 commit-graph | 保持一致 | 新增或更新辅助文件 | C 仍可达 |
| `git gc --no-prune` | 保持一致 | 多项维护可能运行 | C 仍可达 |
| 删除唯一引用并等待对应过期条件 | C 可能失去可达路径 | 取决于后续维护 | 受 reflog、时间和配置影响 |

改变条件是 C 是否还有可达引用路径，以及维护命令是否到了允许删除的过期时间。不要预测固定 pack 大小、delta 数量或耗时；这些值依赖实际对象集合和 Git 的压缩选择。

## Agent 迁移题：维护操作的可审核记录

自动化涉及对象维护时，交接记录至少应包含：

```text
repository path and HEAD: <path> / <oid>
worktree and refs checked: clean state, branches, tags, reflog consideration
concurrent Git activity checked: <processes or scheduling boundary>
command and expiry parameters: <exact command>
logical invariant: git show <stable-commit> before/after comparison
physical observations: pack/index/commit-graph existence and count-objects output
deletion evidence: exact disposable object or dry-run candidate
```

这份记录让维护动作保持可追溯：逻辑内容是否保留、哪些物理结构变化、哪些删除仍有恢复边界。Agent 不应把“GC 成功返回”扩展成“仓库性能已提升”或“所有历史都安全”。

## 延伸阅读

- [git-gc 官方手册](https://git-scm.com/docs/git-gc)
- [git-repack 官方手册](https://git-scm.com/docs/git-repack)
- [git-prune 官方手册](https://git-scm.com/docs/git-prune)
- [git-commit-graph 官方手册](https://git-scm.com/docs/git-commit-graph)
- [实验说明](../labs/git-mental-model/10-storage/README.md)
