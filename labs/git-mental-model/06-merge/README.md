# Merge Common-Ancestor Lab / Merge 共同祖先实验

[中文文章](../../../01-getting-started/git-mental-model-06-merge.md) | [English article](../../../01-getting-started/01-getting-started_en/git-mental-model-06-merge_en.md)

## 中文

这个实验使用真实 Git 对象和引用，保留三个合并结果及一个正在进行的内容冲突：

```text
ff-target        快进到 fast-forward，没有新的 merge commit
merge-result     两条已分叉历史合并，commit 有两个 parent
semantic-result  文本合并成功，行为检查退出码为 1
main             与 conflict-topic 冲突，Index 保存 stage 1、2、3
```

运行：

```bash
lab_path=$(bash setup.sh)
bash verify.sh "$lab_path"
bash cleanup.sh "$lab_path"
```

`setup.sh` 的标准输出只有临时仓库路径。它禁用系统和全局 Git 配置，在仓库内设置身份、关闭签名，并把 hooks 路径指向空目录。`verify.sh` 会断言快进分支仍只有一个 parent、普通 merge 和语义 merge 都有两个 parent、冲突路径保存 base/ours/theirs 三个 Index 条目。它还从 `semantic-result` 读取真实 Git 内容并运行 `behavior_check.py`，确认退出码非零。

查看正在进行的冲突：

```bash
cd "$lab_path"
git status --short
git merge-base HEAD MERGE_HEAD
git ls-files --unmerged -- conflict.txt
git show :1:conflict.txt
git show :2:conflict.txt
git show :3:conflict.txt
```

预期 `conflict.txt` 有三条 Index 记录：stage 1 为 `owner=base`，stage 2 为 `owner=main`，stage 3 为 `owner=topic`。解决时编辑文件，再执行 `git add conflict.txt` 和 `git merge --continue`。若选择放弃本次合并，先确认没有需要保留的未提交改动，再执行 `git merge --abort`。

一次运行完整自测：

```bash
bash test.sh
```

## English

This lab uses real Git objects and refs. It preserves three merge outcomes and one in-progress content conflict:

```text
ff-target        fast-forwards to fast-forward, with no new merge commit
merge-result     merges two divergent histories; the commit has two parents
semantic-result  text merge succeeds; the behavior check exits with status 1
main             conflicts with conflict-topic; the index stores stages 1, 2, and 3
```

Run:

```bash
lab_path=$(bash setup.sh)
bash verify.sh "$lab_path"
bash cleanup.sh "$lab_path"
```

The only standard output from `setup.sh` is the temporary repository path. It disables system and global Git configuration, sets an in-repository identity, turns off signing, and routes hooks to an empty directory. `verify.sh` asserts that the fast-forward branch still has one parent, that the regular and semantic merges have two parents, and that the conflicted path has base/ours/theirs index entries. It also reads the actual Git content from `semantic-result`, runs `behavior_check.py`, and asserts a non-zero exit status.

Inspect the in-progress conflict:

```bash
cd "$lab_path"
git status --short
git merge-base HEAD MERGE_HEAD
git ls-files --unmerged -- conflict.txt
git show :1:conflict.txt
git show :2:conflict.txt
git show :3:conflict.txt
```

`conflict.txt` should have three index entries: stage 1 is `owner=base`, stage 2 is `owner=main`, and stage 3 is `owner=topic`. To resolve it, edit the file, then run `git add conflict.txt` and `git merge --continue`. To abandon this merge, first make sure no uncommitted work needs to be retained, then run `git merge --abort`.

Run the complete self-test with:

```bash
bash test.sh
```
