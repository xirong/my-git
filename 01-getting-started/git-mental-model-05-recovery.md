# Git 心智模型 05：可达性、reflog 与恢复

[English](01-getting-started_en/git-mental-model-05-recovery_en.md) | [交互演示](../interactive/git-mental-model/reachability-and-recovery.html) | [可运行实验](../labs/git-mental-model/05-recovery/README.md)

在执行 <code>reset --hard</code>、rebase、amend、删除 branch 或强制更新远端之前，先判断恢复线索是否存在。Git 的恢复能力来自对象、引用和本地 reflog，不来自“刚刚执行过命令”这一事实。

本章先建立恢复能力，再解释危险重写操作。这样可以把“分支名消失”和“对象已经不可恢复”分开判断。

## 先看结论

~~~text
refs/heads/main -> C1
refs/heads/recovered -> C2

HEAD reflog earlier value -> C3

no ref, no reflog, object pruned -> cannot resolve C4
~~~

- 可达性描述从一组起点沿 commit、tree 和 blob 连接能否找到对象。常见起点是 branch、tag 和其他 refs。
- 删除 branch 名或把 branch reset 到旧 commit，只会移除或移动引用。旧 commit 常常仍在对象库中，并可能暂时由 reflog 指向。
- reflog 记录本地仓库里 branch 及其他引用的 tip 更新，HEAD reflog 还记录切换分支。它不随 push 作为远端备份传播。
- reflog 有保留期限。当前官方默认值是可达条目 90 天、从当前分支 tip 不可达的条目 30 天，配置和显式 expire 命令可以改变这些期限。
- 对象失去 ref 和 reflog 保护后，GC 可以清理它。对象已经清理后，Git 无法从其对象库恢复它。
- 从未经过 <code>git add</code> 或 <code>git commit</code> 记录的编辑，没有可供 Git 对象恢复的内容；需要依赖编辑器、文件系统或其他备份。

官方文档说明，reflog 是本地仓库中引用 tip 更新的记录，<code>HEAD@{2}</code> 等写法可以引用过去的 HEAD 值。[git-reflog](https://git-scm.com/docs/git-reflog)

## 从“有名字”到“无保护”的对象状态

实验使用以下对象关系：

~~~text
main -> C1 baseline

C2 keep recoverable commit
  main reset away from C2
  no ref reaches it
  HEAD reflog still names C2

C3 discard after expiry
  temporary branch deleted
  no ref reaches it
  HEAD reflog still names C3
~~~

运行 <code>git branch recovered C2</code> 后：

~~~text
refs/heads/recovered -> C2
~~~

<code>C2</code> 又有直接引用，GC 会把它视为受保护对象。对 <code>C3</code> 显式过期 reflog，再运行立即 prune 后：

~~~text
no ref -> no reflog -> object pruned
~~~

此时对象 ID 可能已经无法通过 <code>git cat-file</code> 解析。这个过程说明恢复有时间和保留条件，不能当作永久备份策略。

## 可达性取决于使用的起点

<code>git log main</code> 从 <code>main</code> 出发遍历其祖先。若 <code>main</code> 已从 <code>C2</code> reset 回 <code>C1</code>，<code>C2</code> 不再位于 <code>main</code> 的历史中。

但这不代表 <code>C2</code> 已从仓库磁盘消失。<code>git fsck</code> 默认把 index、<code>refs</code> 和 reflog 都作为可达性追踪的起点；加 <code>--no-reflogs</code> 可以检查一个只由 reflog 线索保留的旧对象是否会成为不可达对象。[git-fsck](https://git-scm.com/docs/git-fsck)

~~~bash
git fsck --no-reflogs --unreachable
~~~

预期会包含类似输出：

~~~text
unreachable commit <old-commit-id>
~~~

这是一项检查结果，不是保证对象还能恢复多久。对象是否仍在对象库、reflog 是否尚未过期，以及 GC 是否已清理，都会改变结论。

## reflog 是本地恢复线索，有期限

先查看本地 HEAD 移动记录：

~~~bash
git reflog show --oneline HEAD
git reflog show --oneline main
~~~

可以看到 commit、reset、checkout 等操作留下的记录。<code>HEAD@{1}</code> 表示当前 HEAD 的上一个 reflog 值；<code>main@{1}</code> 表示 main 的上一个值。<code>gitrevisions</code> 规定这些形式查询的是本地 ref 在过去某个时间或序号的位置。[gitrevisions](https://git-scm.com/docs/gitrevisions)

默认保留时间来自配置项：

~~~bash
git config --get gc.reflogExpire
git config --get gc.reflogExpireUnreachable
~~~

没有本地覆盖时，Git 当前文档给出的默认值是 <code>gc.reflogExpire=90 days</code>，<code>gc.reflogExpireUnreachable=30 days</code>。前者用于一般条目，后者会更早清理从当前 branch tip 不可达的条目。仓库配置、组织模板、手动 expire 和维护任务都能改变实际保留结果。[git-reflog 的 expire 选项](https://git-scm.com/docs/git-reflog)

因此，reflog 适合作为短期事故恢复线索，不应替代远端仓库、bundle、备份或正式发布制品。不同 clone 各自拥有 reflog；在 A 仓库看到的 <code>HEAD@{1}</code> 不会自动出现在 B 仓库。

## 危险操作前先建立恢复点

在本地重写前执行以下检查：

~~~bash
git status --short
git branch safety/before-rewrite HEAD
git show --no-patch --oneline safety/before-rewrite
git reflog show -n 5 HEAD
~~~

这段命令有三个作用：

1. <code>git status --short</code> 先暴露未提交状态。要保留的编辑需要先选择合适的保存方式。
2. <code>safety/before-rewrite</code> 给当前 commit 一个显式引用，避免只依赖 reflog。
3. <code>git reflog</code> 记录当前可用的本地恢复线索，便于操作后核对。

若历史已经推送，或其他人可能基于它开发，还需检查远端、协作者和发布影响。共享历史的撤销常常适合新增一个 <code>git revert</code> commit。Git 对数据库写入、部署、消息和其他外部副作用没有自动恢复能力。

<code>git reset</code> 的 commit 形式会改变 HEAD 所指向的 commit，并在操作前把当前 branch tip 放入 <code>ORIG_HEAD</code>；<code>--hard</code> 还会覆盖工作树和 Index。官方文档明确说明它可能覆盖未跟踪文件。[git-reset](https://git-scm.com/docs/git-reset)

## 在临时仓库运行实验

实验脚本新建一个带标记的临时库，设置本地身份，关闭签名和 hooks。<code>setup.sh</code> 在该临时库中生成 <code>C2</code>，执行一次 <code>reset --hard</code>，移除 <code>ORIG_HEAD</code>，再生成并删除承载 <code>C3</code> 的临时 branch。宿主仓库不会被这些动作修改。

### 1. 建立临时库，先看仍受 reflog 保护的状态

从仓库根目录执行：

~~~bash
lab_path=$(bash labs/git-mental-model/05-recovery/setup.sh)
git -C "$lab_path" show-ref --heads
git -C "$lab_path" reflog show --oneline HEAD
git -C "$lab_path" fsck --no-reflogs --unreachable
~~~

预期语义：

~~~text
main points to the baseline commit
HEAD reflog contains "keep recoverable commit"
HEAD reflog contains "discard after expiry"
fsck without reflogs reports both commits as unreachable
~~~

对象 ID 和 reflog 序号会变化。先把带有 <code>keep recoverable commit</code> 的对象 ID 记作 <code>&lt;recoverable-id&gt;</code>，不要凭格式猜测它。

### 2. 用 reflog 中的对象 ID 新建恢复 branch

~~~bash
git -C "$lab_path" branch recovered <recoverable-id>
git -C "$lab_path" show --no-patch --oneline recovered
git -C "$lab_path" rev-parse refs/heads/recovered
~~~

预期：

~~~text
keep recoverable commit
<recoverable-id>
~~~

此时恢复动作只是创建一条 branch 引用，commit 内容没有被改写。接下来可以审查差异、选择 merge、rebase 或让该 branch 保持为恢复点。

### 3. 验证脚本执行两种结局

步骤 2 已向临时库写入 <code>recovered</code>。验证脚本需要从“没有 ref 能到达两个 commit”的初始状态开始，因此先删除这一个实验库，再创建新的实验库：

~~~bash
bash labs/git-mental-model/05-recovery/cleanup.sh "$lab_path"
lab_path=$(bash labs/git-mental-model/05-recovery/setup.sh)
~~~

然后运行：

~~~bash
bash labs/git-mental-model/05-recovery/verify.sh "$lab_path"
~~~

预期结构：

~~~text
ok: reset moved main to <baseline-id> while reflog retained <recoverable-id>
ok: recovered branch now names <recoverable-id>
ok: after explicit reflog expiry and gc --prune=now, <expired-id> no longer resolves
~~~

脚本在第一项断言中确认没有 ref 能到达 <code>C2</code> 和 <code>C3</code>，它们仍存在于 HEAD reflog，且 <code>git fsck --no-reflogs --unreachable</code> 报告它们。第二项创建 <code>recovered</code>。第三项故意让 <code>C3</code> 失去 reflog 保护并立即清理。

### 4. 在实验库中观察过期与清理的风险

验证脚本的最后一个断言使用下面两条命令删除恢复线索并立即清理无保护对象。只可用于由本章 <code>setup.sh</code> 刚创建的 <code>$lab_path</code>，不要复制到活跃仓库、共享仓库或另有 Git 进程写入的仓库。若要手动重现整个过程，请重新运行 <code>setup.sh</code>，先检查 reflog，再运行这些命令：

~~~bash
git -C "$lab_path" reflog expire --expire=now --expire-unreachable=now --all
git -C "$lab_path" gc --prune=now
~~~

Git 文档说明 <code>gc --prune=now</code> 会清理所有年龄的无用 loose object，且与并发写入同一仓库会增加损坏风险。普通 <code>git gc</code> 的 prune 默认阈值是两周前，实际值可由 <code>gc.pruneExpire</code> 覆盖。[git-gc](https://git-scm.com/docs/git-gc)

### 5. 清理临时库

~~~bash
bash labs/git-mental-model/05-recovery/cleanup.sh "$lab_path"
~~~

清理脚本会检查本实验标记，并拒绝删除仓库根目录、用户主目录和根目录。

## 安全边界

### “没有分支名”需要继续取证

先依次检查：

~~~bash
git show-ref --heads --tags
git reflog show --oneline HEAD
git fsck --no-reflogs --unreachable
git cat-file -t <candidate-object-id>
~~~

这些命令分别回答：有没有显式引用、HEAD 是否记录过该对象、去掉 reflog 作为起点后它是否不可达、对象是否仍可读取。只有这些证据都不存在或对象已被清理时，才能说 Git 对象库中没有该恢复线索。

### “我没有改文件”不能证明工作树安全

<code>reset --hard</code> 可能覆盖工作树、Index 和未跟踪文件。执行前先检查 <code>git status --short</code> 和实际文件内容。若工作中含有从未经过 <code>git add</code> 或 <code>git commit</code> 记录的编辑，Git 对象库没有相应恢复依据；应暂停危险操作并转向编辑器历史、文件系统快照或其他备份。

### reflog 不承担跨机器和长期保存

reflog 属于本地仓库，条目也会过期。重要恢复点应保留明确的 branch 或 tag，并按照团队策略推送、备份或制作可验证的发布制品。

## 常见误解

### “删除 branch 会立刻删除 commit”

删除 branch 先移除一个引用。只要对象仍被其他 refs、reflog 或其他保留机制引用，并且尚未被清理，仍可能找到它。

### “reflog 是永久历史”

它是本地、可过期的引用更新记录。默认期限也可以被配置和命令改变。

### “只要知道对象 ID，就一定能恢复”

对象 ID 只能在对象仍存在时解析。没有 refs、reflog 或其他保留，GC 可能已经清理对象。

### “Git 能恢复所有未提交编辑”

Git 只能基于它实际记录过的对象和引用工作。从未经过 <code>git add</code> 或 <code>git commit</code> 记录的编辑，需要从 Git 之外寻找恢复来源。

### “git fsck 输出 unreachable 就等于对象损坏”

unreachable 说明相对于本次检查使用的起点找不到该对象。对象仍可能完整存在于对象库，并能通过新的 branch 恢复。

## Agent 场景迁移题

Agent 在本地生成了一个可审查 commit，随后执行 <code>git reset --hard HEAD~1</code>。它说“提交丢了”，没有推送，也没有说明工作树里是否有其他编辑。

先完成以下判断，再决定恢复方式：

1. 运行 <code>git status --short</code>，确认是否还有未提交编辑需要保护。
2. 运行 <code>git reflog show --oneline HEAD</code>，找到 reset 前的对象 ID。
3. 运行 <code>git cat-file -t &lt;id&gt;</code> 和 <code>git show --stat &lt;id&gt;</code>，确认对象类型和内容。
4. 创建 <code>git branch recovery/agent-reset &lt;id&gt;</code>，让恢复对象重新获得显式引用。
5. 核对该 branch 是否需要推送、合并、保留为审查点，或改用共享历史适用的撤销策略。

如果 Agent 的关键编辑从未经过 <code>git add</code> 或 <code>git commit</code> 记录，reflog 和对象图不能恢复它。此时应明确缺少 Git 证据，并检查授权范围内的编辑器历史或备份。

## 延伸阅读

- [git-reflog](https://git-scm.com/docs/git-reflog)
- [git-fsck](https://git-scm.com/docs/git-fsck)
- [git-gc](https://git-scm.com/docs/git-gc)
- [git-reset](https://git-scm.com/docs/git-reset)
- [gitrevisions](https://git-scm.com/docs/gitrevisions)
- [上一章：引用、HEAD 与身份](git-mental-model-04-refs.md)
