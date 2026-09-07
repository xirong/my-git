# Git 心智模型 04：引用、HEAD 与身份

[English](01-getting-started_en/git-mental-model-04-refs_en.md) | [交互演示](../interactive/git-mental-model/refs-and-head.html) | [可运行实验](../labs/git-mental-model/04-refs/README.md)

当 Agent 说“我已经切到另一个分支”或“我给这个版本打了标签”，真正需要确认的是：哪个引用现在指向哪个 commit，HEAD 是附着在分支上，还是直接指向一个 commit。

这决定了下一次 commit 会移动哪条引用，也决定了某个提交会不会因为离开 detached HEAD 而难以再次找到。

## 先看结论

~~~text
HEAD -> refs/heads/main -> C3
refs/heads/agent/draft -> C2
refs/tags/v1-light -> C1
refs/tags/v1-annotated -> T1(tag object) -> C1
~~~

- branch 是位于 <code>refs/heads/</code> 的可移动引用，通常指向一个 commit。
- tag 是位于 <code>refs/tags/</code> 的引用。轻量标签直接指向对象；附注标签先指向 tag object，再由该对象指向目标对象。
- HEAD 在附着状态保存类似 <code>ref: refs/heads/main</code> 的符号引用。提交时，Git 创建一个新 commit，并前移 <code>main</code>。
- detached HEAD 直接记录一个 commit ID。提交时，HEAD 前移到新 commit，已有 branch 不会随之移动。
- 移动引用不会修改旧 commit 的内容。branch 和 HEAD 等带有 reflog 的本地更新还会留下恢复线索；旧对象能否长期保留，取决于后续是否仍可达、是否有 reflog 保护，以及 GC 策略。

<code>gitrevisions</code> 把 branch 名、tag 名和完整对象 ID 都作为 revision 的写法；<code>HEAD</code> 表示当前工作树所基于的 commit。[官方 revision 文档](https://git-scm.com/docs/gitrevisions)

## 场景：同一项目看起来有三条历史

临时仓库中有三个 commit：

~~~text
C1 baseline
├── C2 agent draft       refs/heads/agent/draft
└── C3 main release      HEAD -> refs/heads/main

v1-light     -> C1
v1-annotated -> tag object -> C1
~~~

<code>C1</code>、<code>C2</code>、<code>C3</code> 都是对象。<code>main</code>、<code>agent/draft</code>、<code>v1-light</code> 和 <code>v1-annotated</code> 是给对象取名的引用。一个对象可以被多个引用命名；移动其中一个名字不会让其他名字或旧对象变成另一个内容。

这解释了分支切换的关键区别：切换分支会让 HEAD 改为附着到另一个 branch；创建分支只是新增一个指向现有 commit 的名字；在某分支创建 commit 时，只有该分支的引用会前移。

## branch、tag 和 HEAD 各自表达什么

| 名称 | 常见位置 | 指向什么 | 创建新 commit 时会怎样 |
| --- | --- | --- | --- |
| branch | <code>refs/heads/</code> | 通常是 commit | 当前附着分支前移 |
| lightweight tag | <code>refs/tags/</code> | 直接是目标对象，常见为 commit | 保持原值 |
| annotated tag | <code>refs/tags/</code> | tag object，该对象再指向目标 | 保持原值 |
| attached HEAD | <code>.git/HEAD</code> | 某条 branch 的符号引用 | 跟随该 branch |
| detached HEAD | <code>.git/HEAD</code> | 直接是 commit ID | HEAD 前移，branch 不动 |

<code>git symbolic-ref HEAD</code> 可以读取 HEAD 所指向的 branch。官方文档说明，符号引用是以 <code>ref: refs/</code> 开头的普通文件；当 HEAD 已 detached，带 <code>-q</code> 的读取命令会非零退出。[git-symbolic-ref](https://git-scm.com/docs/git-symbolic-ref)

## 附着和 detached：下一次 commit 移动谁

在附着状态：

~~~text
HEAD -> main -> C3
git commit
HEAD -> main -> C4
~~~

在 detached 状态：

~~~text
HEAD -> C1
git commit
HEAD -> C4
main -> C3
agent/draft -> C2
~~~

两种状态都可以创建 commit。风险在于 detached commit 没有 branch 名自动承接。继续切换或做其他引用更新后，它可能只剩下 HEAD reflog 的短期线索。

需要保留 detached 工作时，在离开前创建一个 branch：

~~~bash
git branch agent/experiment HEAD
git switch main
~~~

这两个命令不复制项目文件，也不复制 commit 对象。它们新增一个引用，再切回主线。

## 标签类型改变了对象图

Git 官方文档规定：未使用 <code>-a</code>、<code>-s</code> 或 <code>-u</code> 时，<code>git tag</code> 创建直接指向目标对象的 lightweight tag；使用这些选项会创建 tag object。附注标签包含 tagger、日期、消息和可选签名，轻量标签只是对象的名称。[git-tag](https://git-scm.com/docs/git-tag)

用对象类型检查区别：

~~~bash
git cat-file -t v1-light
git cat-file -t v1-annotated
git rev-parse 'v1-annotated^{}'
~~~

预期：

~~~text
commit
tag
<baseline-commit-id>
~~~

最后一条中的 <code>^{}</code> 会解开 tag object，得到它最终指向的非 tag 对象。发布版本通常需要附注标签，因为它带有可审查的元数据；临时定位或本地试验常用 lightweight tag。团队还需单独约定标签是否可以移动、是否必须签名和如何发布。

## 在临时仓库运行实验

实验数据和本章图一致：<code>service.txt</code> 的 baseline 是 <code>release=base</code>，<code>agent/draft</code> 新增 <code>agent.txt</code>，<code>main</code> 把 <code>service.txt</code> 更新为 <code>release=main-1</code>。

### 1. 建立隔离仓库并验证初始状态

从仓库根目录运行：

~~~bash
lab_path=$(bash labs/git-mental-model/04-refs/setup.sh)
bash labs/git-mental-model/04-refs/verify.sh "$lab_path"
~~~

预期输出中的对象 ID 会因 Git 版本和对象格式不同而变化，结构固定：

~~~text
ok: HEAD -> refs/heads/main -> <main-id>
ok: refs/heads/agent/draft -> <agent-id>
ok: refs/tags/v1-light -> <baseline-id>
ok: refs/tags/v1-annotated -> tag -> <baseline-id>
~~~

<code>setup.sh</code> 只输出临时目录路径，并禁用系统和全局 Git 配置、提交签名、标签签名和 hooks 对本实验的干扰。

### 2. 从名字读到对象

~~~bash
git -C "$lab_path" for-each-ref \
  --format='%(refname:short) %(objecttype) %(objectname)' \
  refs/heads refs/tags
git -C "$lab_path" symbolic-ref --short HEAD
git -C "$lab_path" rev-parse HEAD
git -C "$lab_path" rev-parse refs/heads/main
~~~

预期语义：

~~~text
agent/draft points at a commit
main points at a different commit
v1-light has object type commit
v1-annotated has object type tag
HEAD is attached to main
HEAD and refs/heads/main resolve to the same commit ID
~~~

比较 <code>main</code> 与 <code>agent/draft</code> 的 ID，可以看到两条 branch 同时存在。查看它们指向的文件：

~~~bash
git -C "$lab_path" show refs/heads/main:service.txt
git -C "$lab_path" show refs/heads/agent/draft:service.txt
git -C "$lab_path" show refs/heads/agent/draft:agent.txt
~~~

预期先看到 <code>release=main-1</code>，再看到 <code>release=base</code> 和 <code>proposal=retry</code>。

### 3. 进入 detached HEAD 并把新 commit 命名

以下操作只适用于刚创建的实验目录。它会创建一个新的临时 commit：

~~~bash
git -C "$lab_path" switch --detach v1-annotated
git -C "$lab_path" symbolic-ref -q HEAD || printf 'HEAD is detached\n'
printf 'keep this detached commit\n' > "$lab_path/detached.txt"
git -C "$lab_path" add detached.txt
git -C "$lab_path" commit -m "detached experiment"
git -C "$lab_path" branch keep-detached HEAD
git -C "$lab_path" switch main
~~~

预期关键输出：

~~~text
HEAD is detached
~~~

随后 <code>keep-detached</code> 指向刚创建的 commit，<code>main</code> 仍指向步骤 1 的 main commit。删除 <code>keep-detached</code> 前，应先判断该 commit 是否还需要保留或分享。

### 4. 清理临时仓库

~~~bash
bash labs/git-mental-model/04-refs/cleanup.sh "$lab_path"
~~~

清理脚本要求目录内存在本实验专用标记，拒绝删除仓库根目录、用户主目录和根目录。

## 安全边界

### 改分支前先确认对象、引用和共享范围

重写本地历史、移动分支或强制移动标签前，先保存当前引用：

~~~bash
git status --short
git branch safety/before-rewrite HEAD
git show --no-patch --oneline safety/before-rewrite
git reflog show -n 5 HEAD
~~~

这会新增一个本地 branch，给当前 commit 一个明确名字。它不处理未提交编辑，也不代替远端备份。已经推送且有他人基于其开发的历史，需要先确认协作影响；多数共享撤销场景应评估 <code>git revert</code>。

<code>git tag -f</code> 会移动既有标签名。若该标签代表已发布版本、构建输入或签名声明，移动它会改变下游解析到的对象。先建立新的标签命名或获得团队确认。

### detached 状态下先命名，再离开

若实验、bisect 或查看旧版本时要提交，先运行：

~~~bash
git branch agent/experiment HEAD
~~~

这个 branch 是恢复线索。它仍在本地，尚未推送就不构成远端备份。

## 常见误解

### “分支是一份独立目录”

分支是一个引用。切换分支会让 HEAD 和工作树对齐到另一个 commit 的快照，branch 本身不保存一套独立文件副本。

### “切换 branch 会改写旧 commit”

切换和前移 branch 改变引用目标。新内容由新 commit 表达，旧 commit 仍保留原有对象 ID 和内容。

### “tag 永远不能移动”

Git 可以强制更新 tag 引用。发布流程通常把已发布标签视为稳定标识，是否允许移动属于团队发布约定。

### “HEAD 就是当前分支名”

HEAD 在附着状态通过符号引用间接指向 branch；detached 时直接记录 commit ID。先检查 HEAD 的解析方式，才能判断下一次 commit 移动哪条引用。

### “detached HEAD 不能提交”

它可以提交。问题在于新 commit 没有 branch 自动承接，离开前应创建 branch。

## Agent 场景迁移题

Agent 为了验证旧版本运行了：

~~~bash
git switch --detach <old-commit>
git commit -am "try a compatibility fix"
~~~

它随后报告“修改已提交”。验收时应回答两个问题：

1. 新 commit 移动了哪条 branch？
2. 如果需要保留该试验，哪条引用能稳定地命名它？

答案：此时 HEAD 直接指向新 commit，没有常规 branch 前移。先用 <code>git log -1 --decorate HEAD</code>、<code>git symbolic-ref -q HEAD</code> 和 <code>git show-ref --heads</code> 检查状态，再执行 <code>git branch agent/compatibility-test HEAD</code>。最后检查新 branch 指向的对象 ID，并明确该 branch 是否需要推送或建立其他备份。

## 延伸阅读

- [gitrevisions](https://git-scm.com/docs/gitrevisions)
- [git-symbolic-ref](https://git-scm.com/docs/git-symbolic-ref)
- [git-tag](https://git-scm.com/docs/git-tag)
- [下一章：可达性、reflog 与恢复](git-mental-model-05-recovery.md)
- [上一章：Index 是下一次 commit 的草稿](git-mental-model-03-index.md)
