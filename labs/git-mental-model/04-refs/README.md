# Refs and HEAD Lab / 引用与 HEAD 实验

[中文文章](../../../01-getting-started/git-mental-model-04-refs.md) | [English article](../../../01-getting-started/01-getting-started_en/git-mental-model-04-refs_en.md)

## 中文

这个实验创建一个临时 Git 仓库，并建立下面这组真实引用：

~~~text
HEAD -> refs/heads/main -> main commit
refs/heads/agent/draft -> agent commit
refs/tags/v1-light -> baseline commit
refs/tags/v1-annotated -> tag object -> baseline commit
~~~

运行：

~~~bash
lab_path=$(bash setup.sh)
bash verify.sh "$lab_path"
bash cleanup.sh "$lab_path"
~~~

<code>setup.sh</code> 的标准输出只有临时仓库路径。它禁用系统和全局 Git 配置，为这个仓库设置本地身份、关闭提交和标签签名，并把 hooks 路径设为空目录。这样可以避开个人签名设置和全局 hooks 对实验的影响。

先在执行 <code>verify.sh</code> 前检查中间状态：

~~~bash
git -C "$lab_path" log --oneline --decorate --all --graph
git -C "$lab_path" symbolic-ref --short HEAD
git -C "$lab_path" cat-file -t v1-light
git -C "$lab_path" cat-file -t v1-annotated
~~~

预期语义：

~~~text
HEAD attached to main
v1-light is a commit
v1-annotated is a tag object
~~~

要亲自观察 detached HEAD，可以只在这个临时库中执行：

~~~bash
git -C "$lab_path" switch --detach v1-annotated
git -C "$lab_path" symbolic-ref -q HEAD || printf 'HEAD is detached\n'
printf 'keep this detached commit\n' > "$lab_path/detached.txt"
git -C "$lab_path" add detached.txt
git -C "$lab_path" commit -m "detached experiment"
git -C "$lab_path" branch keep-detached HEAD
git -C "$lab_path" switch main
~~~

新 commit 在 detached 状态下不会移动 <code>main</code> 或 <code>agent/draft</code>。<code>keep-detached</code> 给该 commit 加上一个可见引用，再切回 <code>main</code>。

<code>verify.sh</code> 用真实对象 ID、引用解析和对象类型断言当前状态；任何断言不成立都会以非零状态退出。它不只打印固定结果。<code>cleanup.sh</code> 只删除带有本实验标记的目录，并拒绝仓库根目录、用户主目录和根目录。

完整自测：

~~~bash
bash test.sh
~~~

## English

This lab creates a temporary Git repository with these real references:

~~~text
HEAD -> refs/heads/main -> main commit
refs/heads/agent/draft -> agent commit
refs/tags/v1-light -> baseline commit
refs/tags/v1-annotated -> tag object -> baseline commit
~~~

Run:

~~~bash
lab_path=$(bash setup.sh)
bash verify.sh "$lab_path"
bash cleanup.sh "$lab_path"
~~~

<code>setup.sh</code> prints only the temporary-repository path. It disables system and global Git configuration, sets a local identity, disables commit and tag signing, and points hooks to an empty directory. Personal signing settings and global hooks therefore do not affect the lab.

Inspect the intermediate state before running <code>verify.sh</code>:

~~~bash
git -C "$lab_path" log --oneline --decorate --all --graph
git -C "$lab_path" symbolic-ref --short HEAD
git -C "$lab_path" cat-file -t v1-light
git -C "$lab_path" cat-file -t v1-annotated
~~~

Expected meaning:

~~~text
HEAD attached to main
v1-light is a commit
v1-annotated is a tag object
~~~

To observe a detached HEAD yourself, run these commands only in this temporary repository:

~~~bash
git -C "$lab_path" switch --detach v1-annotated
git -C "$lab_path" symbolic-ref -q HEAD || printf 'HEAD is detached\n'
printf 'keep this detached commit\n' > "$lab_path/detached.txt"
git -C "$lab_path" add detached.txt
git -C "$lab_path" commit -m "detached experiment"
git -C "$lab_path" branch keep-detached HEAD
git -C "$lab_path" switch main
~~~

A commit made while detached moves neither <code>main</code> nor <code>agent/draft</code>. <code>keep-detached</code> gives that commit a visible reference before returning to <code>main</code>.

<code>verify.sh</code> asserts the actual object IDs, reference resolution, and object types. Any failed assertion exits nonzero; the script does not merely print a fixed result. <code>cleanup.sh</code> removes only a directory marked for this lab and refuses the repository root, the user home directory, and the filesystem root.

Run the full self-test:

~~~bash
bash test.sh
~~~
