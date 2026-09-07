# Worktree Lab / Worktree 实验

[中文文章](../../../01-getting-started/git-mental-model-09-worktree.md) | [English article](../../../01-getting-started/01-getting-started_en/git-mental-model-09-worktree_en.md)

## 中文

实验在一个新建临时根目录中创建 `primary` 主工作树和 `feature` linked worktree。它关闭全局 Git 配置、签名和调用方 hooks，所有提交只存在于临时仓库。

```bash
lab_path=$(bash setup.sh)
bash verify.sh "$lab_path"
sed -n '1,240p' "$lab_path/observations.txt"
sed -n '1,120p' "$lab_path/same-branch-results.txt"
bash cleanup.sh "$lab_path"
```

实验实际断言以下状态：两个工作树共享 common Git directory 中的对象和分支引用；`HEAD`、Index 路径和 Working Tree 彼此不同；`main-note.txt` 与 `feature-note.txt` 在提交前各自只出现在自己的 Index；Git 拒绝把已在 `primary` 检出的 `main` 再检出到 `same-main`，但允许不同的 `feature/parallel` 分支；主工作树合入 feature 后，feature 工作树仍停在自己的分支。

`external-resource.txt` 位于两个工作树之外，实验从两个上下文写入它。这只证明 Git 不管理仓库外的文件，不能用于推断真实并发时的写入顺序。

`cleanup.sh` 只删除带本实验标记并且结构完整的临时根目录。保留现场时跳过 cleanup。

一次运行完整自测：

```bash
bash test.sh
```

## English

The lab creates a temporary root with a primary worktree and a linked `feature` worktree. It disables global Git configuration, signing, and caller hooks. Every commit remains in the temporary repository.

```bash
lab_path=$(bash setup.sh)
bash verify.sh "$lab_path"
sed -n '1,240p' "$lab_path/observations.txt"
sed -n '1,120p' "$lab_path/same-branch-results.txt"
bash cleanup.sh "$lab_path"
```

The lab asserts that the worktrees share objects and branch refs in the common Git directory while keeping distinct `HEAD`, index paths, and working trees. Before committing, `main-note.txt` appears only in the primary index and `feature-note.txt` only in the feature index. Git rejects a second checkout of `main`, already checked out by `primary`, while allowing the distinct `feature/parallel` branch. After the primary worktree merges feature, the feature worktree remains on its own branch.

`external-resource.txt` sits outside both worktrees and is written from both contexts. This proves that Git does not manage files outside the worktrees; it does not predict write order during real concurrent activity.

`cleanup.sh` deletes only a marked, structurally complete temporary root. Skip cleanup while inspecting the scene.

Run the complete self-test:

```bash
bash test.sh
```
