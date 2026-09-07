# Rebase Replay Lab / Rebase 重放实验

[中文文章](../../../01-getting-started/git-mental-model-07-rebase.md) | [English article](../../../01-getting-started/01-getting-started_en/git-mental-model-07-rebase_en.md)

## 中文

这个实验用真实 Git 结果保留三种 rebase 情况：

```text
replay-topic            已成功重放，指向新 commit
replay-topic-original   显式保留旧 commit，旧对象仍可读取
no-replay               没有待重放 commit，引用不变
topic                   rebase 到 upstream 时在第二个 commit 发生内容冲突
```

运行：

```bash
lab_path=$(bash setup.sh)
bash verify.sh "$lab_path"
bash cleanup.sh "$lab_path"
```

`setup.sh` 的标准输出只有临时仓库路径。它禁用系统和全局 Git 配置，在仓库内设置身份、关闭签名，并把 hooks 路径指向空目录。`verify.sh` 会断言成功重放的旧、新 commit ID 不同，旧 commit 的 parent 是 `replay-base`，新 commit 的 parent 是 `replay-upstream`，并确认 `replay-topic-original` 让旧对象保持可达。它还验证 `no-replay` 没有创建新 commit。

实验最终停在真实 rebase 冲突中。观察状态：

```bash
cd "$lab_path"
git status --short
git rebase --show-current-patch
git ls-files --unmerged -- app.txt
git show :1:app.txt
git show :2:app.txt
git show :3:app.txt
```

预期 `app.txt` 的 stage 1 是 `owner=base`，stage 2 是 `owner=upstream`，stage 3 是 `owner=topic`。在 rebase 的冲突语境里，stage 2 的 ours 是已经以 `upstream` 为基础的重放结果，stage 3 的 theirs 是当前正被重放的 topic commit；它和普通 merge 的分支视角不同。

解决后执行 `git add app.txt` 与 `git rebase --continue`。若要放弃本次 rebase，开始前和中途都应避免混入未提交工作；在这个干净实验里，`git rebase --abort` 会让 `topic` 回到 `topic-original`。`test.sh` 会实际执行这一 abort 并断言引用、Working Tree 和 `REBASE_HEAD` 的结果。

一次运行完整自测：

```bash
bash test.sh
```

## English

This lab preserves three real Git rebase cases:

```text
replay-topic            successfully replayed and points to a new commit
replay-topic-original   explicitly retains the old commit, which remains readable
no-replay               has no commits to replay, so its ref is unchanged
topic                   conflicts on its second commit while rebasing onto upstream
```

Run:

```bash
lab_path=$(bash setup.sh)
bash verify.sh "$lab_path"
bash cleanup.sh "$lab_path"
```

The only standard output from `setup.sh` is the temporary repository path. It disables system and global Git configuration, sets an in-repository identity, turns off signing, and routes hooks to an empty directory. `verify.sh` asserts that the old and new IDs for a successful replay differ, the old commit's parent is `replay-base`, the new commit's parent is `replay-upstream`, and `replay-topic-original` keeps the old object reachable. It also verifies that `no-replay` created no new commit.

The lab stops in a real rebase conflict. Inspect the state:

```bash
cd "$lab_path"
git status --short
git rebase --show-current-patch
git ls-files --unmerged -- app.txt
git show :1:app.txt
git show :2:app.txt
git show :3:app.txt
```

For `app.txt`, stage 1 is expected to be `owner=base`, stage 2 `owner=upstream`, and stage 3 `owner=topic`. In a rebase conflict, stage-2 ours is the replay result built on `upstream`; stage-3 theirs is the topic commit currently being replayed. That view differs from a regular merge.

After resolving, run `git add app.txt` and `git rebase --continue`. To abandon the rebase, avoid mixing uncommitted work into it before or during the operation; in this clean lab, `git rebase --abort` returns `topic` to `topic-original`. `test.sh` actually runs that abort and asserts the ref, working tree, and `REBASE_HEAD` outcome.

Run the complete self-test with:

```bash
bash test.sh
```
