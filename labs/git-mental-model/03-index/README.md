# Index Draft Lab / Index 草稿实验

[中文文章](../../../01-getting-started/git-mental-model-03-index.md) | [English article](../../../01-getting-started/01-getting-started_en/git-mental-model-03-index_en.md) | [Interactive demo](../../../interactive/git-mental-model/index-as-draft.html)

## 中文

这个实验创建一个临时 Git 仓库，并同时保留三类 Index 状态：

```text
MM app.txt       一个 hunk 已暂存，另一个 hunk 仍在 Working Tree
UU conflict.txt  Index 保存 stage 1、2、3
 M settings.ini  修改只在 Working Tree
```

运行：

```bash
lab_path=$(bash setup.sh)
bash verify.sh "$lab_path"
bash cleanup.sh "$lab_path"
```

`setup.sh` 的标准输出只有临时仓库路径。`verify.sh` 会检查 `HEAD`、Index 和 Working Tree 中的 `app.txt` 内容，确认 `git diff --cached` 只包含选中的 hunk，并验证冲突 stages 的 base、ours、theirs 内容。`cleanup.sh` 只接受带有本实验标记的仓库路径。

一次运行完整自测：

```bash
bash test.sh
```
## English

This lab creates a temporary Git repository and preserves three index states at once:

```text
MM app.txt       one hunk staged, another hunk still in the working tree
UU conflict.txt  stages 1, 2, and 3 stored in the index
 M settings.ini  change present only in the working tree
```

Run:

```bash
lab_path=$(bash setup.sh)
bash verify.sh "$lab_path"
bash cleanup.sh "$lab_path"
```

The only standard output from `setup.sh` is the temporary repository path. `verify.sh` checks the `app.txt` content in `HEAD`, the index, and the working tree; confirms that `git diff --cached` contains only the selected hunk; and verifies the base, ours, and theirs content in the conflict stages. `cleanup.sh` accepts only a repository marked as belonging to this lab.

Run the full self-test with:

```bash
bash test.sh
```
