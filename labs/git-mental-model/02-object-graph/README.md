# Object Graph Lab / 对象图实验

[中文文章](../../../01-getting-started/git-mental-model-02-object-graph.md) | [English article](../../../01-getting-started/01-getting-started_en/git-mental-model-02-object-graph_en.md) | [Interactive demo](../../../interactive/git-mental-model/object-graph.html)

## 中文

这个实验创建一个临时 Git 仓库，并验证以下真实对象关系：

```text
commit
└── root tree
    ├── app.txt -> blob
    └── docs -> tree
        └── note.txt -> blob
```

运行：

```bash
lab_path=$(bash setup.sh)
bash verify.sh "$lab_path"
bash cleanup.sh "$lab_path"
```

`setup.sh` 的标准输出只有临时仓库路径。`verify.sh` 会检查每个对象的类型、tree 条目、blob 内容、commit 到根 tree 的连接，以及相同内容是否得到相同 blob ID。`cleanup.sh` 只接受带有本实验标记的仓库路径。

一次运行完整自测：

```bash
bash test.sh
```

## English

This lab creates a temporary Git repository and verifies this real object relationship:

```text
commit
└── root tree
    ├── app.txt -> blob
    └── docs -> tree
        └── note.txt -> blob
```

Run:

```bash
lab_path=$(bash setup.sh)
bash verify.sh "$lab_path"
bash cleanup.sh "$lab_path"
```

The only standard output from `setup.sh` is the temporary repository path. `verify.sh` checks every object type, the tree entries, blob content, the commit-to-root-tree edge, and whether identical content receives the same blob ID. `cleanup.sh` accepts only a repository marked as belonging to this lab.

Run the full self-test with:

```bash
bash test.sh
```
