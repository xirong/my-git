# Git 心智模型 03：Index 是下一次 commit 的草稿

[English](01-getting-started_en/git-mental-model-03-index_en.md) | [交互演示](../interactive/git-mental-model/index-as-draft.html) | [可运行实验](../labs/git-mental-model/03-index/README.md)

当 AI Agent 修改了十个文件，却说“我只会提交其中两个”时，不能只看 Working Tree，也不能只相信文字说明。真正决定下一次 commit 内容的是 Index。

Index 也叫 staging area。把它理解成“下一次 commit 的草稿”很实用，但还要补上一层底层事实：它通常存放在 `.git/index` 这个二进制文件中，普通条目记录路径、模式、blob 对象 ID、stage 号和用于性能优化的文件系统元数据。文件内容位于对象库中的 blob，Index 通过对象 ID 引用这些内容。

本章解决三个问题：

1. `git add` 到底改变了什么。
2. 同一个文件为什么可以同时有 staged 和 unstaged 改动。
3. 合并冲突时，Index 为什么会出现 stage 1、2、3。

## 先看结论

```text
HEAD                    Index                         Working Tree
上一次 commit           下一次 commit 的草稿          当前磁盘文件

app.txt v1  --add -p--> app.txt v2  --继续编辑-->      app.txt v3
```

- `git add <path>` 把该路径当前选中的内容写成 blob，并更新 Index 条目。
- `git commit` 根据 Index 的 stage 0 条目生成 tree，再创建 commit。
- `git diff --cached` 比较 `HEAD` 与 Index，最接近“下一次 commit 会改变什么”。
- `git diff` 比较 Index 与 Working Tree，显示尚未进入草稿的修改。
- `git status --short` 第一列描述 Index 相对 `HEAD` 的变化，第二列描述 Working Tree 相对 Index 的变化。
- 冲突路径暂时没有正常的 stage 0 条目，会保留共同祖先、ours、theirs 三个版本供你解决。

因此，Working Tree 里看得到的修改，不一定会进入下一次 commit；Working Tree 里已经删除或改写的内容，也可能仍以另一个版本存在于 Index。

## Index 条目记录什么

运行：

```bash
git ls-files --stage
```

普通输出格式是：

```text
<mode> <object-id> <stage>\t<path>
```

例如：

```text
100644 42c4cc2... 0	app.txt
```

这表示：

- `100644`：普通非可执行文件的模式。
- `42c4cc2...`：Index 引用的 blob 对象 ID。
- `0`：正常条目使用 stage 0。
- `app.txt`：相对仓库根目录的路径。

Index 还包含 stat cache 等性能字段。日常判断下一次 commit 内容时，最重要的是路径、模式、对象 ID 和 stage。

## `git add` 更新的是一份路径快照

假设 `app.txt` 在 `HEAD` 中是：

```text
owner=team
deploy=off
```

把 `owner` 改成 `agent` 后执行：

```bash
git add app.txt
```

Git 会为当前内容写入或复用 blob，并让 Index 的 `app.txt` 指向这个 blob。之后继续把 `deploy` 改成 `on`，不会自动再次更新 Index。

此时可能同时存在三份内容：

```text
HEAD          owner=team   deploy=off
Index         owner=agent  deploy=off
Working Tree  owner=agent  deploy=on
```

查看两段不同的差异：

```bash
git diff --cached -- app.txt
git diff -- app.txt
```

第一条只显示 `owner` 的变化，第二条只显示 `deploy` 的变化。

## 部分暂存：一个文件拆成两个审查范围

`git add -p` 会逐个展示 diff hunk，并让你选择哪些 hunk 进入 Index：

```bash
git add -p app.txt
```

常用回答：

- `y`：暂存当前 hunk。
- `n`：跳过当前 hunk。
- `s`：尝试把当前 hunk 继续拆分。
- `e`：手工编辑补丁，适合能准确判断补丁语义的用户。
- `q`：退出，后续 hunk 不再处理。

部分暂存后，`git status --short` 可能显示：

```text
MM app.txt
```

第一个 `M` 表示 Index 相对 `HEAD` 已修改，第二个 `M` 表示 Working Tree 相对 Index 还有修改。这里包含两个比较边界，各自发现了一份差异。

提交前至少检查：

```bash
git diff --cached
git status --short
```

如果业务逻辑跨越多个 hunk，拆开提交可能造成某个 commit 无法构建或行为不完整。部分暂存服务于清晰提交，不能破坏变更的原子性。

## 冲突 stages：Index 暂存三个候选版本

普通路径在 Index 中使用 stage 0。发生内容冲突时，一个路径会出现最多三个高 stage 条目：

```text
stage 1  merge base，共同祖先版本
stage 2  ours，当前分支版本
stage 3  theirs，被合入分支版本
```

检查命令：

```bash
git ls-files --unmerged
git show :1:conflict.txt
git show :2:conflict.txt
git show :3:conflict.txt
```

示意输出：

```text
100644 8227059... 1	conflict.txt
100644 c3efd06... 2	conflict.txt
100644 d17b9a9... 3	conflict.txt
```

解决 Working Tree 中的冲突并执行：

```bash
git add conflict.txt
```

Git 会移除 stage 1、2、3，为解决结果建立新的 stage 0 条目。这里的 `git add` 同时表达两个事实：接受当前文件内容，并把该路径标记为已解决。

上面的 ours/theirs 解释适用于普通 merge。rebase 会改变变更重放的视角，使用 `--ours` 或 `--theirs` 前要重新确认当前操作语义。

## 交互演示

[打开“Index 是下一次 commit 的草稿”交互演示](../interactive/git-mental-model/index-as-draft.html)。页面把每一步命令、`git status --short`、Index 条目和提交预览绑定到同一份状态数据。

从仓库根目录启动静态服务器：

```bash
python3 -m http.server 8000
```

然后访问：

```text
http://localhost:8000/interactive/git-mental-model/index-as-draft.html
```

查看完成后，在运行服务器的终端按 `Ctrl-C` 退出。

## 在临时仓库运行实验

实验会创建一个独立临时仓库，不修改当前项目：

```bash
cd labs/git-mental-model/03-index
lab_path=$(bash setup.sh)
bash verify.sh "$lab_path"
bash cleanup.sh "$lab_path"
```

一次运行完整自测：

```bash
bash labs/git-mental-model/03-index/test.sh
```

实验最终保留三个可同时检查的状态：

```text
MM app.txt
UU conflict.txt
 M settings.ini
```

- `app.txt` 的第一个 hunk 已进入 Index，第二个 hunk 只在 Working Tree。
- `conflict.txt` 在 Index 中保存 stage 1、2、3。
- `settings.ini` 只在 Working Tree 改动，不属于下一次 commit 草稿。

完整预期说明见 [expected.txt](../labs/git-mental-model/03-index/expected.txt)。

## 故障恢复：Agent 暂存了无关文件

假设 Agent 执行了 `git add -A`，把本地配置 `settings.ini` 一起放进 Index。

先检查草稿：

```bash
git status --short
git diff --cached -- settings.ini
```

确认该路径不应提交后，只恢复 Index：

```bash
git restore --staged -- settings.ini
git status --short
```

`git restore --staged` 默认用 `HEAD` 中的版本恢复 Index，Working Tree 的修改保持不变。这很适合“取消暂存但保留本地编辑”的场景。

不要为了取消暂存直接使用：

```bash
git reset --hard
```

`reset --hard` 还会覆盖 Working Tree，可能丢失尚未提交的内容。只需要调整草稿时，应使用带明确路径的 `git restore --staged`。

## 常见误解

### “Index 只是待提交文件名列表”

Index 条目还记录模式、对象 ID 和 stage。它描述的是每个路径准备提交的具体内容版本。

### “`git add` 以后，文件后续修改也会自动进入提交”

每次 `git add` 只更新当时选中的内容。后续编辑仍在 Working Tree，需要再次暂存。

### “`git commit -a` 等价于 `git add -A && git commit`”

`git commit -a` 会自动暂存已跟踪文件的修改和删除，但不会包含新的未跟踪文件。它也减少了提交前单独审查 Index 的机会。

### “冲突标记只存在于 Working Tree 文件里”

Working Tree 展示冲突标记，Index 同时保存 stage 1、2、3 的候选 blob。解决后 `git add` 才会恢复 stage 0。

### “取消暂存会删除我的修改”

`git restore --staged -- <path>` 只修改 Index。没有同时指定 `--worktree` 时，Working Tree 保持不变。

## 在 AI Agent 场景中的意义

Agent 可能修改许多文件，也可能运行范围过大的 `git add -A`。验收 Agent 提交时，应该检查真实 Index：

```bash
git status --short
git diff --cached --stat
git diff --cached
git ls-files --unmerged
```

推荐放行规则：

1. `git diff --cached` 只包含当前任务需要的路径和 hunk。
2. `git ls-files --unmerged` 没有输出。
3. Working Tree 中保留的改动已经明确归属，不会被误认为已提交。
4. 部分暂存后的提交仍能独立构建、测试或解释。
5. Agent 声明的提交范围与 Index 的真实内容一致。

对 AI Agent 来说，Index 是提交权限的最小边界。检查它，比询问 Agent “你准备提交什么”更可靠。

## 延伸阅读

- [Git index format](https://git-scm.com/docs/index-format)
- [git ls-files](https://git-scm.com/docs/git-ls-files)
- [git add](https://git-scm.com/docs/git-add)
- [git restore](https://git-scm.com/docs/git-restore)
- [上一章：对象图](git-mental-model-02-object-graph.md)
