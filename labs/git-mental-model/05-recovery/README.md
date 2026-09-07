# Reachability and Recovery Lab / 可达性与恢复实验

[中文文章](../../../01-getting-started/git-mental-model-05-recovery.md) | [English article](../../../01-getting-started/01-getting-started_en/git-mental-model-05-recovery_en.md)

## 中文

这个实验只在新建的临时 Git 仓库中执行一次 <code>reset --hard</code>、reflog 过期和 <code>gc --prune=now</code>。初始状态包含两个没有 branch 名的 commit：

~~~text
main -> baseline

recoverable commit
  no ref reaches it
  still listed by HEAD reflog

expired commit
  no ref reaches it
  still listed by HEAD reflog
~~~

运行：

~~~bash
lab_path=$(bash setup.sh)

# 先观察还受 reflog 保护的状态
git -C "$lab_path" reflog show --oneline HEAD
git -C "$lab_path" fsck --no-reflogs --unreachable

# verify.sh 会恢复第一个 commit，并故意过期和清理第二个 commit
bash verify.sh "$lab_path"
bash cleanup.sh "$lab_path"
~~~

<code>setup.sh</code> 的标准输出只有临时仓库路径。它禁用系统和全局 Git 配置，为仓库设置本地身份、关闭提交和标签签名，并把 hooks 路径设为空目录。<code>reset --hard</code>、<code>reflog expire</code> 和 <code>gc --prune=now</code> 全部只作用于这个带实验标记的临时库。

<code>verify.sh</code> 会先用对象 ID、refs、HEAD reflog 和 <code>git fsck --no-reflogs --unreachable</code> 检查两个 commit 仍在对象库中且没有 ref 能到达它们。随后它创建 <code>recovered</code> branch 找回第一个 commit。最后它显式过期所有 reflog，并运行 <code>git gc --prune=now</code>，断言第二个 commit 已经无法用 <code>git cat-file</code> 解析。任何断言失败都会以非零状态退出。

运行完整自测：

~~~bash
bash test.sh
~~~

<code>verify.sh</code> 会不可逆地销毁第二个临时 commit。若要重新查看受 reflog 保护的中间状态，请重新运行 <code>setup.sh</code> 创建新实验库。

<code>cleanup.sh</code> 只删除带有本实验标记的目录，并拒绝仓库根目录、用户主目录和根目录。

## English

This lab performs one <code>reset --hard</code>, reflog expiration, and <code>gc --prune=now</code> only inside a newly created temporary Git repository. Its initial state has two commits without a branch name:

~~~text
main -> baseline

recoverable commit
  no ref reaches it
  still listed by HEAD reflog

expired commit
  no ref reaches it
  still listed by HEAD reflog
~~~

Run:

~~~bash
lab_path=$(bash setup.sh)

# Inspect the state that is still protected by reflog first.
git -C "$lab_path" reflog show --oneline HEAD
git -C "$lab_path" fsck --no-reflogs --unreachable

# verify.sh recovers the first commit and intentionally expires and prunes the second.
bash verify.sh "$lab_path"
bash cleanup.sh "$lab_path"
~~~

<code>setup.sh</code> prints only the temporary-repository path. It disables system and global Git configuration, sets a local identity, disables commit and tag signing, and points hooks to an empty directory. <code>reset --hard</code>, <code>reflog expire</code>, and <code>gc --prune=now</code> all operate only on this marked temporary repository.

<code>verify.sh</code> first asserts through object IDs, refs, the HEAD reflog, and <code>git fsck --no-reflogs --unreachable</code> that both commits still exist in the object database with no ref reaching them. It then creates a <code>recovered</code> branch for the first commit. Finally it explicitly expires every reflog and runs <code>git gc --prune=now</code>, asserting that the second commit no longer resolves through <code>git cat-file</code>. Any failed assertion exits nonzero.

Run the full self-test:

~~~bash
bash test.sh
~~~

<code>verify.sh</code> irreversibly destroys the second temporary commit. To inspect the reflog-protected intermediate state again, run <code>setup.sh</code> to create a new lab repository.

<code>cleanup.sh</code> removes only a directory marked for this lab and refuses the repository root, the user home directory, and the filesystem root.
