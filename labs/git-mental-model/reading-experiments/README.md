# Article experiments / 阅读页实验

[交互阅读页 / Interactive article](../../../interactive/git-mental-model/index.html)

## 中文

这里验证新版阅读页中的三个小模型，文件名和内容与图中一致。原有三个深入实验保留各自的数据集。

从仓库根目录执行：

```bash
python3 labs/git-mental-model/reading-experiments/verify.py
```

脚本只在新建的临时目录中创建 Git 仓库并提交，退出时自动清理这些实验目录，不修改当前仓库或全局 Git 配置。需要 Python 3 和支持 `git init -b`、`git restore` 的 Git。

阅读 [verify.py](verify.py) 中的 `snapshots`、`objects`、`draft` 函数，可以看到各实验的完整初始化和按顺序执行的 Git 命令。断言比较真实 Git 输出，没有用浏览器中的状态数组代替 Git。

- 快照：逐步比较 HEAD、Index、工作区，并检查 ` M` 与 `MM` 状态。
- 对象：创建父提交和含两个同内容文件的提交，核对 tree 条目、共享 blob 与文件内容。C1、C2、T1、T2、B1 只用于图示，不是假定的真实哈希。
- 部分暂存：`app.conf` 的两处改动之间有九行未修改配置，保证默认 diff 上下文下是两个 hunk。`git add -p` 依次回答 `y`、`n`；`git restore --staged -p` 依次回答 `n`、`y`。不要把这组回答直接用于其他文件，先读清实际展示的补丁。

浏览器展开的命令是相关步骤的摘录，省略号表示中间未修改行。完整初始化以此脚本为准。三个 PASS 说明模型对应的 Git 行为已验证，不代表浏览器视觉或性能也已通过。

## English

These checks reproduce the three small models in the redesigned reading page, using the same filenames and content. The three existing in-depth labs keep their own datasets.

From the repository root, run:

```bash
python3 labs/git-mental-model/reading-experiments/verify.py
```

The script creates and commits only inside newly allocated temporary repositories. It removes those temporary directories on exit and does not change the current repository or global Git configuration. It requires Python 3 and Git with `git init -b` and `git restore` support.

The `snapshots`, `objects`, and `draft` functions in [verify.py](verify.py) contain the complete setup and ordered Git commands. Assertions compare real Git output, not the browser's state arrays.

- Snapshots: compare HEAD, the index, and the working tree at each step, including ` M` and `MM` status.
- Objects: create a parent and a commit containing two identical files; check tree entries, shared blob identity, and content. C1, C2, T1, T2, and B1 are diagram labels, not assumed real hashes.
- Partial staging: nine unchanged settings separate the two edits in `app.conf`, producing two hunks with default diff context. Answer `y`, `n` to `git add -p`, then `n`, `y` to `git restore --staged -p`. Do not reuse those answers for arbitrary files; read the actual patch first.

The browser shows excerpts from each step; ellipses represent unchanged middle lines. This script supplies the complete setup. Three PASS messages verify the Git behavior behind the models, not browser visuals or performance.
