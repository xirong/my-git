# Snapshots and State Lab / 快照与状态实验

[中文文章](../../../01-getting-started/git-mental-model-01-snapshots.md) | [English article](../../../01-getting-started/01-getting-started_en/git-mental-model-01-snapshots_en.md) | [Interactive demo](../../../interactive/git-mental-model/snapshots-and-state.html)

## 中文

这个实验创建一个临时 Git 仓库，并让 `app.txt` 同时处于以下状态：

```text
HEAD=version=1    Index=version=2    Working Tree=version=3
```

运行：

```bash
lab_path=$(bash setup.sh)
bash verify.sh "$lab_path"
bash cleanup.sh "$lab_path"
```

`setup.sh` 的标准输出只有临时仓库路径，便于在脚本中安全引用。`verify.sh` 会检查三个版本和 `MM app.txt` 状态。`cleanup.sh` 只接受带有本实验标记的仓库路径。

也可以一次运行完整自测：

```bash
bash test.sh
```

## English

This lab creates a temporary Git repository in which `app.txt` has three simultaneous states:

```text
HEAD=version=1    Index=version=2    Working Tree=version=3
```

Run:

```bash
lab_path=$(bash setup.sh)
bash verify.sh "$lab_path"
bash cleanup.sh "$lab_path"
```

The only standard output from `setup.sh` is the temporary repository path, so scripts can capture it safely. `verify.sh` checks all three versions and the `MM app.txt` state. `cleanup.sh` accepts only a repository marked as belonging to this lab.

Run the full self-test with:

```bash
bash test.sh
```
