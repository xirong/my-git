# Git 心智模型 02：对象图

[English](01-getting-started_en/git-mental-model-02-object-graph_en.md) | [交互演示](../interactive/git-mental-model/object-graph.html) | [可运行实验](../labs/git-mental-model/02-object-graph/README.md)

当 AI Agent 说“已经提交两个文件”，Git 实际保存的并不是一个装着文件副本的 commit。它保存一组通过对象 ID 连接起来的对象：文件内容进入 blob，目录结构进入 tree，commit 再指向项目的根 tree。

理解对象图以后，你可以直接回答三个问题：内容保存在哪个对象里，文件名由谁记录，一个 commit 究竟引用了哪份项目快照。

## 先看结论

```text
commit C
└── tree T0                         项目根目录
    ├── blob B1  app.txt            文件内容
    └── tree T1  docs               子目录
        └── blob B2  note.txt       文件内容
```

- blob 保存文件内容，不保存文件名和目录路径。
- tree 保存一层目录的条目，每个条目包含模式、名称和对象 ID；`git ls-tree` 还会解析并显示对象类型。
- commit 指向一个根 tree，并记录父 commit、作者、提交者和提交说明等元数据。
- 对象 ID 由对象的类型、长度和内容共同计算。内容相同的 blob 会得到相同的对象 ID。
- 分支和 `HEAD` 如何指向 commit，属于后续 refs 章节；本章先看 commit 内部的对象连接。

第一章所说的“commit 保存项目快照”，在底层就是一棵由 tree 和 blob 组成、由 commit 作为入口的对象图。

## 三种对象各自负责什么

| 对象 | 主要内容 | 不负责什么 |
| --- | --- | --- |
| blob | 一段文件内容 | 文件名、路径、提交时间 |
| tree | 一层目录中的名称、模式和对象 ID | 提交说明、父子提交关系 |
| commit | 根 tree、父 commit、作者、提交者、说明 | 直接保存文件内容 |

假设 `app.txt` 和 `copy.txt` 内容完全相同，它们可以在同一个 tree 中以两个名称指向同一个 blob。文件名属于 tree 条目，内容属于 blob。

## 对象 ID 为什么会变化

以 blob 为例，Git 计算对象 ID 时使用的逻辑输入可以表示为：

```text
blob <内容字节数>\0<文件内容>
```

文件内容只改一个字节，逻辑输入就会改变，对象 ID 也随之改变。tree 中记录了子对象 ID，因此子文件改变会产生新的 tree；commit 又记录根 tree ID，因此新的快照会产生新的 commit 对象。

不同仓库可能使用不同对象格式，对象 ID 的长度也可能不同。脚本和工具应该读取完整 ID，不要把示例中的缩写长度写成固定规则。

## 交互演示

[打开“对象图”交互演示](../interactive/git-mental-model/object-graph.html)，依次执行写入 blob、暂存文件、生成 tree 和创建 commit，观察对象如何出现并连接。

从仓库根目录启动静态服务器：

```bash
python3 -m http.server 8000
```

然后访问：

```text
http://localhost:8000/interactive/git-mental-model/object-graph.html
```

查看完成后，在运行服务器的终端按 `Ctrl-C` 退出。

## 在临时仓库运行实验

下面的实验会创建一个新的临时仓库，不修改当前项目。

### 1. 创建包含子目录的快照

```bash
lab_dir=$(mktemp -d "${TMPDIR:-/tmp}/my-git-object-graph.XXXXXX")
git -c init.defaultBranch=main init -q "$lab_dir"
cd "$lab_dir"
git config user.name "My Git Lab"
git config user.email "lab@example.com"

mkdir docs
printf 'hello object graph\n' > app.txt
printf 'trees name objects\n' > docs/note.txt
git add app.txt docs/note.txt
git commit -q -m "build object graph"
```

此时 Working Tree、Index 和 `HEAD` 一致。接下来绕过文件视角，直接读取对象。

### 2. 找到 commit、tree 和 blob

```bash
commit_oid=$(git rev-parse HEAD)
root_tree_oid=$(git rev-parse 'HEAD^{tree}')
docs_tree_oid=$(git rev-parse 'HEAD:docs')
app_blob_oid=$(git rev-parse 'HEAD:app.txt')
note_blob_oid=$(git rev-parse 'HEAD:docs/note.txt')

git cat-file -t "$commit_oid"
git cat-file -t "$root_tree_oid"
git cat-file -t "$docs_tree_oid"
git cat-file -t "$app_blob_oid"
git cat-file -t "$note_blob_oid"
```

预期输出：

```text
commit
tree
tree
blob
blob
```

`git rev-parse HEAD:path` 会沿 `HEAD` 对应的对象图解析路径，并返回路径末端的对象 ID。

### 3. 查看 commit 指向哪个根 tree

```bash
git cat-file -p "$commit_oid"
```

输出开头会包含：

```text
tree <root-tree-id>
author My Git Lab <lab@example.com> <timestamp> +0000
committer My Git Lab <lab@example.com> <timestamp> +0000

build object graph
```

第一行的对象 ID 应与 `$root_tree_oid` 一致。第一个 commit 没有 `parent` 行；后续 commit 会记录一个或多个父对象。

### 4. 展开两层 tree

```bash
git ls-tree "$root_tree_oid"
git ls-tree "$docs_tree_oid"
```

规范化后的结构是：

```text
100644 blob <app-blob-id>    app.txt
040000 tree <docs-tree-id>   docs
100644 blob <note-blob-id>   note.txt
```

根 tree 记录 `app.txt` 和 `docs` 两个名称。`docs` 条目指向另一个 tree，第二个 tree 再记录 `note.txt`。

### 5. 读取 blob 内容

```bash
git cat-file -p "$app_blob_oid"
git cat-file -p "$note_blob_oid"
```

预期输出依次是：

```text
hello object graph
trees name objects
```

输出中看不到 `app.txt` 或 `docs/note.txt`。路径信息来自上层 tree。

### 6. 证明相同内容复用同一个 blob ID

```bash
same_content_oid=$(printf 'hello object graph\n' | git hash-object --stdin)
printf '%s\n' "$app_blob_oid"
printf '%s\n' "$same_content_oid"
test "$app_blob_oid" = "$same_content_oid" && echo "same content -> same blob"
```

预期最后一行是：

```text
same content -> same blob
```

`git hash-object` 默认只计算对象 ID；加 `-w` 才会把对象写入对象库。

## 一条从路径走到内容的检查路径

当你检查 `HEAD` 中的 `docs/note.txt`，Git 可以按以下顺序解析：

```text
HEAD
  -> commit
  -> root tree
  -> tree entry "docs"
  -> nested tree
  -> tree entry "note.txt"
  -> blob
  -> file content
```

常用检查命令：

```bash
git cat-file -t HEAD
git cat-file -p HEAD
git ls-tree HEAD
git ls-tree HEAD:docs
git show HEAD:docs/note.txt
```

这些命令只读取对象，不会移动分支、修改 Index 或覆盖 Working Tree。

## 故障恢复：文件内容被意外覆盖

假设已提交的 `app.txt` 被错误内容覆盖：

```bash
printf 'broken content\n' > app.txt
git status --short
git diff -- app.txt
```

先确认 `HEAD` 中保存的对象类型和内容：

```bash
app_blob_oid=$(git rev-parse 'HEAD:app.txt')
git cat-file -t "$app_blob_oid"
git cat-file -p "$app_blob_oid"
```

预期看到 `blob` 和原始内容 `hello object graph`。确认 Working Tree 的错误内容可以丢弃后再恢复：

```bash
git restore --source=HEAD --worktree -- app.txt
git status --short
```

最后一条命令应没有输出。恢复有效，是因为 commit 仍能沿 tree 找到原始 blob。没有进入 Git 对象库或其他备份的内容，无法通过这条对象图恢复。

## 常见误解

### “blob 就是一个文件”

blob 是文件内容。一个 blob 可以被多个文件名、多个 tree 或多个 commit 复用。

### “commit 里面保存全部文件”

commit 记录根 tree 的对象 ID。文件内容位于根 tree 可以到达的 blob 中。

### “文件名参与 blob 的对象 ID 计算”

文件名记录在 tree 条目中。只改文件名且内容不变时，blob ID 可以保持不变，tree ID 会改变。

### “对象 ID 是随机编号”

对象 ID 来自对象的类型、长度和内容。相同逻辑对象会得到相同 ID，内容变化会得到另一个 ID。

### “`git hash-object` 一定会保存对象”

默认只计算 ID。只有使用 `-w` 或通过 `git add`、`git commit` 等流程，相关对象才会写入对象库。

## 对 AI Agent 的意义

| 要确认的事实 | 检查方式 |
| --- | --- |
| Agent 声称的路径是否进入 commit | `git ls-tree -r --name-only HEAD -- <path>` |
| commit 实际指向哪个快照 | `git rev-parse 'HEAD^{tree}'` |
| 某路径对应什么对象 | `git rev-parse 'HEAD:<path>'`、`git cat-file -t` |
| 已提交内容是否符合预期 | `git show HEAD:<path>` |
| 两个路径是否复用相同内容对象 | 比较两个 `git rev-parse 'HEAD:<path>'` 的结果 |
| 可执行位等模式是否正确 | `git ls-tree HEAD -- <path>` |

实践规则：

- Agent 汇报“文件已经提交”时，要同时验证路径存在于 commit 的 tree 中。
- 内容相同不代表路径和模式相同，Review 时还要检查 tree 条目。
- 不把对象 ID 缩写写入长期脚本；需要机器处理时读取完整 ID。
- 使用 `cat-file` 和 `ls-tree` 做只读取证，再决定是否执行恢复或历史修改命令。
- 大量重复内容可能复用对象，但仓库体积还受 packfile、压缩和可达性影响，相关原理将在性能章节展开。

## 自测

<details>
<summary>文件名 <code>app.txt</code> 保存在哪种对象中？</summary>

保存在 tree 条目中。blob 只保存文件内容。

</details>

<details>
<summary>只把 <code>app.txt</code> 重命名为 <code>main.txt</code>，内容不变，哪些对象会变化？</summary>

blob 可以保持不变；包含该名称的 tree 会变化，因此引用新根 tree 的 commit 也会变化。

</details>

<details>
<summary>为什么修改深层目录中的一个文件会改变根 tree ID？</summary>

文件产生新 blob，包含它的 tree 需要记录新 ID；变化沿父 tree 逐层向上传递，最终产生新的根 tree。

</details>

## 延伸阅读

- [上一章：快照与状态](git-mental-model-01-snapshots.md)
- [Pro Git：Git 内部原理与 Git 对象](https://git-scm.com/book/zh/v2/Git-%E5%86%85%E9%83%A8%E5%8E%9F%E7%90%86-Git-%E5%AF%B9%E8%B1%A1)
- [`git cat-file` 官方文档](https://git-scm.com/docs/git-cat-file)
- [`git hash-object` 官方文档](https://git-scm.com/docs/git-hash-object)
- [`git ls-tree` 官方文档](https://git-scm.com/docs/git-ls-tree)
- [`git rev-parse` 官方文档](https://git-scm.com/docs/git-rev-parse)
- [Git 心智模型总览](git-mental-model.md)
