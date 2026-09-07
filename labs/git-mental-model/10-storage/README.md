# Object Storage Lab / 对象存储实验

[中文文章](../../../01-getting-started/git-mental-model-10-storage.md) | [English article](../../../01-getting-started/01-getting-started_en/git-mental-model-10-storage_en.md)

## 中文

实验在一个新建临时仓库中创建 14 个相近的逻辑快照。它关闭全局 Git 配置、签名和调用方 hooks，不触碰当前项目。

```bash
lab_path=$(bash setup.sh)
bash verify.sh "$lab_path"
sed -n '1,200p' "$lab_path/observations.txt"
diff -u "$lab_path/show-before.txt" "$lab_path/show-after.txt"
sed -n '1,120p' "$lab_path/count-before.txt"
sed -n '1,120p' "$lab_path/count-after.txt"
bash cleanup.sh "$lab_path"
```

实验对同一个 commit 在 `repack`、`commit-graph write`、`gc --no-prune` 和已知孤立 blob 的 `prune --expire=now` 前后执行真实 `git show`，并断言输出完全一致。它还断言 pack/index 文件存在、`git verify-pack` 报告了 delta 对象、commit-graph 可验证，以及孤立 blob 已被 prune 删除。

`count-objects` 的输出只记录此机器和此数据集的物理观察。它不构成固定字节数、对象数量或性能结论。`prune --expire=now` 只在这个可删除的实验仓库中执行；不要把它照搬到正在协作、可能仍需恢复对象的仓库。

`cleanup.sh` 只删除带本实验标记且结构完整的临时根目录。保留现场时跳过 cleanup。

一次运行完整自测：

```bash
bash test.sh
```

## English

The lab creates 14 similar logical snapshots in a new temporary repository. It disables global Git configuration, signing, and caller hooks, and it does not touch this project.

```bash
lab_path=$(bash setup.sh)
bash verify.sh "$lab_path"
sed -n '1,200p' "$lab_path/observations.txt"
diff -u "$lab_path/show-before.txt" "$lab_path/show-after.txt"
sed -n '1,120p' "$lab_path/count-before.txt"
sed -n '1,120p' "$lab_path/count-after.txt"
bash cleanup.sh "$lab_path"
```

For the same commit, the lab runs real `git show` before and after `repack`, `commit-graph write`, `gc --no-prune`, and `prune --expire=now` of a known orphan blob, then asserts byte-for-byte identical output. It also asserts pack/index structure, delta objects reported by `git verify-pack`, a verifiable commit-graph, and removal of the known orphan.

`count-objects` records only a physical observation for this machine and dataset. It is not a fixed byte, object-count, or performance conclusion. `prune --expire=now` runs only in this disposable repository; do not copy it to a collaborative repository that may still need object recovery.

`cleanup.sh` deletes only a marked, structurally complete temporary root. Skip cleanup while inspecting the evidence.

Run the complete self-test:

```bash
bash test.sh
```
