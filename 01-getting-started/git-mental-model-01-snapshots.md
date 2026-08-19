# Git 心智模型 01：快照与状态

[English](01-getting-started_en/git-mental-model-01-snapshots_en.md) | [交互演示](../interactive/git-mental-model/snapshots-and-state.html) | [可运行实验](../labs/git-mental-model/01-snapshots-and-state/README.md)

当 AI Agent 回复“已经改完”，你还需要确认一件事：这些改动位于 Working Tree、Index，还是已经进入 commit？

这三个位置可以同时保存同一个文件的三个版本。理解这一点，就能准确判断 `git add`、`git commit`、`git diff` 和 `git restore` 会影响什么。

## 先看结论

```text
HEAD snapshot         Index snapshot        Working Tree
current commit        next commit draft     files on disk
version=1             version=2             version=3
```

- `HEAD` 指向当前检出的 commit，该 commit 记录一个项目快照。
- Index 也叫 staging area，保存下一次 commit 准备记录的快照。
- Working Tree 是磁盘上正在编辑的文件状态。
- 未跟踪文件在执行 `git add` 前，不属于 Index 或任何 commit。

`git commit` 的输入来自 Index。Working Tree 中尚未暂存的内容不会进入这次 commit。

## Git 保存快照，也展示差异

从使用者的逻辑模型看，每个 commit 记录项目在某个时刻的快照。`git diff` 根据两个状态计算差异，让你看到快照之间发生了什么。

Git 的底层存储可能在 packfile 中使用 delta compression 节省空间，但这种存储优化不会改变 commit 表达项目快照的心智模型。

三个常用比较方向：

```text
HEAD -------- git diff --cached --------> Index
Index ----------- git diff -------------> Working Tree
HEAD ------------ git diff HEAD --------> Working Tree
```

| 命令 | 比较的状态 | 主要回答 |
| --- | --- | --- |
| `git diff` | Index 与 Working Tree | 还有哪些改动没有暂存 |
| `git diff --cached` | HEAD 与 Index | 下一次 commit 会记录什么 |
| `git diff HEAD` | HEAD 与 Working Tree | 当前文件相对 commit 总共改了什么 |

## 交互演示

[打开“快照与状态”交互演示](../interactive/git-mental-model/snapshots-and-state.html)，依次执行“编辑、暂存、再次编辑、提交”，观察三个位置中 `app.txt` 的版本变化。

直接在本地浏览器查看时，可以从仓库根目录启动静态服务器：

```bash
python3 -m http.server 8000
```

然后访问：

```text
http://localhost:8000/interactive/git-mental-model/snapshots-and-state.html
```

查看完成后，在运行服务器的终端按 `Ctrl-C` 退出。

## 在临时仓库运行实验

下面的实验不会修改当前项目。它会创建一个新的临时仓库。

### 1. 创建第一个快照

```bash
lab_dir=$(mktemp -d "${TMPDIR:-/tmp}/my-git-snapshots.XXXXXX")
git -c init.defaultBranch=main init -q "$lab_dir"
cd "$lab_dir"
git config user.name "My Git Lab"
git config user.email "lab@example.com"

printf 'version=1\n' > app.txt
git add app.txt
git commit -q -m "record version 1"
git status --short
```

预期输出：没有输出，表示 HEAD、Index 和 Working Tree 内容一致。

### 2. 只修改 Working Tree

```bash
printf 'version=2\n' > app.txt
git status --short
```

预期输出：

```text
 M app.txt
```

左侧第一列表示 Index，右侧第二列表示 Working Tree。这里第一列为空、第二列是 `M`，说明改动只存在于 Working Tree。

此时：

```text
HEAD=version=1    Index=version=1    Working Tree=version=2
```

### 3. 把 version=2 放入 Index

```bash
git add app.txt
git status --short
```

预期输出：

```text
M  app.txt
```

`M` 移到第一列，表示 Index 相对 HEAD 已经改变，Working Tree 与 Index 一致。

```text
HEAD=version=1    Index=version=2    Working Tree=version=2
```

### 4. 暂存后再次编辑

```bash
printf 'version=3\n' > app.txt
git status --short
```

预期输出：

```text
MM app.txt
```

现在同一个文件同时有三个版本。直接读取三个位置：

```bash
git show HEAD:app.txt
git show :app.txt
cat app.txt
```

预期输出依次是：

```text
version=1
version=2
version=3
```

其中 `:app.txt` 表示读取 Index 中的 `app.txt`。

### 5. 提交 Index 中的快照

```bash
git commit -m "record version 2"
git status --short
```

commit 输出中的对象 ID 会因环境而变化，可以把它规范化理解为：

```text
[main <object-id>] record version 2
 1 file changed, 1 insertion(+), 1 deletion(-)
```

随后 `git status --short` 仍会显示：

```text
 M app.txt
```

最终状态：

```text
HEAD=version=2    Index=version=2    Working Tree=version=3
```

这证明 commit 记录了 Index 中的 version=2。稍后写入 Working Tree 的 version=3 仍然没有提交。

## 一条容易误判的检查路径

暂存以后执行：

```bash
git diff
```

可能没有任何输出。这只能说明 Working Tree 与 Index 一致，不能证明仓库没有改动。继续检查：

```bash
git diff --cached
git status --short
```

因此，Agent 或人类在汇报“没有 diff”时，还应明确执行的是哪一种 diff。

## 故障恢复：误删 Working Tree 文件

如果 `app.txt` 已经被 Git 跟踪，并且只在 Working Tree 中误删，先检查：

```bash
git status --short
git diff -- app.txt
```

确认需要丢弃这次删除后，从 HEAD 恢复：

```bash
git restore --source=HEAD --worktree -- app.txt
git status --short
```

`git restore` 会覆盖 Working Tree 中对应路径的状态。执行前必须确认当前改动确实可以丢弃。

Git 无法恢复从未被 `git add`、commit 或其他工具保存过的未跟踪文件。这个边界比恢复命令本身更重要。

## 常见误解

### “commit 会记录磁盘上的全部修改”

commit 记录 Index。未暂存的 Working Tree 内容仍留在磁盘上。

### “`git diff` 没输出就代表没有改动”

`git diff` 默认只比较 Index 与 Working Tree。已暂存改动要用 `git diff --cached` 检查。

### “Git 只保存每次修改的增量”

Git 对外呈现 commit 快照。差异是比较结果，底层 packfile 可以使用增量压缩。

### “只要文件在 Git 仓库目录里就能恢复”

只有进入 Git 对象、Index、stash 或其他备份的内容才有恢复依据。未跟踪且从未保存的内容不在 Git 的恢复范围内。

## 对 AI Agent 的意义

Agent 完成任务后，至少应区分以下证据：

| 要确认的事实 | 检查方式 |
| --- | --- |
| Working Tree 有哪些未暂存改动 | `git diff` |
| Index 准备提交什么 | `git diff --cached` |
| 当前相对 HEAD 的全部已跟踪改动 | `git diff HEAD` |
| 是否存在未跟踪、暂存或混合状态 | `git status --short` |
| 最近一次 commit 实际记录了什么 | `git show --stat --oneline HEAD` |

实践规则：

- 不把“文件已生成”写成“变更已提交”。
- 不因为 `git diff` 为空就跳过 `git diff --cached` 和 `git status`。
- 暂存前逐路径检查，避免直接使用范围过大的 `git add -A`。
- 未获得提交授权时，可以验证和汇报状态，不擅自创建 commit。
- 恢复前先区分内容是否进入过 Index、commit、stash 或其他备份。

## 自测

<details>
<summary>为什么 `git status --short` 会出现 <code>MM app.txt</code>？</summary>

Index 中的版本相对 HEAD 已修改，同时 Working Tree 中的版本相对 Index 也已修改。

</details>

<details>
<summary>在 <code>MM app.txt</code> 状态执行 commit，会提交哪个版本？</summary>

提交 Index 中的版本。实验中是 version=2。

</details>

<details>
<summary>删除一个从未暂存过的未跟踪文件，reflog 能找回来吗？</summary>

不能。reflog 记录引用更新，无法为从未进入 Git 的文件内容提供恢复依据。

</details>

## 延伸阅读

- [下一章：对象图](git-mental-model-02-object-graph.md)
- [Pro Git：Git 是什么](https://git-scm.com/book/zh/v2/%E8%B5%B7%E6%AD%A5-Git-%E6%98%AF%E4%BB%80%E4%B9%88%EF%BC%9F)
- [Git User Manual：理解历史与快照](https://git-scm.com/docs/user-manual)
- [`git diff` 官方文档](https://git-scm.com/docs/git-diff)
- [`git status` 官方文档](https://git-scm.com/docs/git-status)
- [`git commit` 官方文档](https://git-scm.com/docs/git-commit)
- [`git restore` 官方文档](https://git-scm.com/docs/git-restore)
- [Git 心智模型总览](git-mental-model.md)
