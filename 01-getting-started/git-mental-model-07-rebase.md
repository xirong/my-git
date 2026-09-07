# Git 心智模型 07：Rebase 重放变化，分支引用指向新历史

[English](01-getting-started_en/git-mental-model-07-rebase_en.md) | [交互演示](../interactive/git-mental-model/rebase-and-replay.html) | [可运行实验](../labs/git-mental-model/07-rebase/README.md)

上游分支前进后，为什么 `git rebase` 常让代码改动看起来相同，commit ID 却变了？原因在于 rebase 不会把旧 commit 移到新位置。它选择需要保留的变化，再以新的 parent 关系创建重放 commit，最后更新分支引用。

本章解决五个问题：

1. rebase 怎样从旧分叉点挑选变化并逐个重放。
2. 什么条件下会创建新 commit，什么条件下不会。
3. 旧对象、备份引用、reflog 与新分支 tip 的关系。
4. 冲突时如何确认正在重放哪一份变化，以及为什么 rebase 中 ours/theirs 的视角与普通 merge 不同。
5. 已共享分支改写历史前应如何协调与验证。

## 先看因果关系

开始时，`topic` 和 `main` 从 `B` 分叉：

```text
          T1---T2  topic
         /
...---B---U1---U2  main
```

在 `topic` 上执行：

```bash
git rebase main
```

Git 会找出 `topic` 相对 `main` 需要保留的提交，临时以 `main` 为起点，按顺序应用这些变化，然后把 `topic` 更新到结果 tip：

```text
...---B---U1---U2  main
                 \
                  T1'---T2'  topic

          T1---T2  旧对象仍可由备份引用或 reflog 找到
```

`T1'` 与 `T1` 可以有相同的文件级变化，但 parent 已从 `B` 变成 `U2`。commit 对象记录 tree、parent、作者和提交者等数据；Git 创建新对象时，它的对象 ID 随对象内容而变化。rebase 改写的是分支引用所指向的历史，不会原地改写旧 commit 对象。

官方文档将这个过程概括为：列出当前分支上相对上游没有等价项的提交，检出上游，再按顺序重放，最后更新分支引用。

## 什么时候会有新 commit

“执行 rebase 一定会改变所有 commit ID”不准确。应先判断 Git 是否真正创建了重放 commit：

| 条件 | 结果 |
| --- | --- |
| 当前分支有相对新上游仍需保留的、非等价提交，并且 Git 成功重放它 | Git 创建新的重放 commit；新 parent 关系使其成为新对象 |
| 当前分支已经位于上游，或没有提交需要重放 | 不创建重放 commit，引用可以保持不变 |
| 上游已经包含一个可识别为等价的干净 cherry-pick | 默认 rebase 会跳过该提交；`--reapply-cherry-picks` 等选项会改变这个处理 |
| 交互式 rebase 删除、合并、修改或重排提交 | 结果取决于 todo 列表；保留下来的重放变化会形成新的对象，删除项不会出现在结果历史 |

对象 ID 变化来自实际创建的新对象，不是 `rebase` 命令名称本身。写自动化断言时，应比较 parent、tree、提交范围和引用，而非假设每次调用都必定改写每个 ID。

## 旧对象和引用：先保留可读的对照点

分支名称是可移动的引用。为了让旧历史在操作后仍有一个稳定名称，先建立显式备份引用：

```bash
git switch topic
git branch backup/topic-before-rebase topic
git rebase origin/main
```

重放成功后，可以同时检查旧、新历史：

```bash
git log --graph --oneline --decorate --all
git show backup/topic-before-rebase
git show topic
git reflog show topic
```

`backup/topic-before-rebase` 让旧 tip 持续可达，适合审查和恢复。reflog 通常也会记录引用移动，但它会受过期和仓库维护策略影响；需要可靠对照时，显式备份引用更清楚。

## 真实实验：一个新对象、一次无重放和一个冲突

实验创建独立临时仓库，禁用系统和全局 Git 配置，设置临时身份、关闭签名并隔离 hooks。它不会修改当前项目：

```bash
cd labs/git-mental-model/07-rebase
lab_path=$(bash setup.sh)
bash verify.sh "$lab_path"
```

实验同时保留三种实际结果：

```text
replay-topic            成功重放后指向新 commit
replay-topic-original   显式引用旧 commit，旧对象仍可读取
no-replay               已在上游 tip，没有待重放提交
topic                   正在 rebase 到 upstream，第二个提交产生内容冲突
```

`verify.sh` 会断言：

```text
replay-topic-original 的 parent 是 replay-base
replay-topic 的 parent 是 replay-upstream
两个 commit ID 不同，topic.txt 内容相同
no-replay 与 no-replay-before、replay-upstream 指向同一 commit
topic 冲突时 Working Tree 为 UU app.txt，Index 有 stage 1、2、3
```

这同时给出两个边界：成功重放实际创建新对象；没有待重放提交的一次 rebase 没有创建新对象。

保留实验现场时：

```bash
cd "$lab_path"
git log --graph --oneline --all --decorate
git show --no-patch --format=raw replay-topic-original
git show --no-patch --format=raw replay-topic
git status --short
git rebase --show-current-patch
git ls-files --unmerged -- app.txt
```

清理仅接受带有本实验标记的临时仓库：

```bash
bash cleanup.sh "$lab_path"
```

一次运行创建、断言、abort 验证和清理：

```bash
bash test.sh
```

完整预期见 [expected.txt](../labs/git-mental-model/07-rebase/expected.txt)。

## rebase 冲突：先读正在重放的变化

本章实验的 topic 有两个提交。第一个 `topic-note.txt` 已成功重放到 `upstream` 之上；第二个把 `app.txt` 改为 `owner=topic` 的提交与上游的 `owner=upstream` 冲突。此时执行：

```bash
git status --short
git rebase --show-current-patch
git ls-files --unmerged -- app.txt
git show :1:app.txt
git show :2:app.txt
git show :3:app.txt
```

本实验的输出含义：

| Index stage | 内容 | rebase 冲突里的解释 |
| --- | --- | --- |
| 1 | `owner=base` | 三方合并的共同祖先 |
| 2 | `owner=upstream` | ours，已经以 `upstream` 为基础的重放结果 |
| 3 | `owner=topic` | theirs，当前正被重放的旧 topic 提交 |

普通 merge 中，stage 2 通常是当前分支 `HEAD`，stage 3 是 `MERGE_HEAD`。rebase 的执行动作是把工作分支提交应用到上游之上，因此这里的 ours 是已重放序列与上游的组合，theirs 是正在应用的工作分支提交。使用 `git checkout --ours` 或 `git checkout --theirs` 前先读 stage 内容，不能只依赖词面印象。

解决流程：

```bash
# 编辑 app.txt，选择符合实际契约的结果
git add app.txt
git rebase --continue
```

`git add` 让冲突路径回到 stage 0；`git rebase --continue` 再尝试后续重放。若某个提交的变化确认不需要，应先理解跳过会从最终历史移除这份变化，再使用 `git rebase --skip`。

## 内部状态只用于观察，不作为跨版本脚本契约

Git 的 rebase 后端可能在 Git 目录中使用 `rebase-merge` 或 `rebase-apply` 记录临时状态。需要教学观察时，可以让 Git 计算其路径：

```bash
for backend in rebase-merge rebase-apply; do
  state_dir=$(git rev-parse --git-path "$backend")
  test -d "$state_dir" && printf 'active backend state: %s\n' "$state_dir"
done
```

后端、版本和选项会影响实际目录。稳定的检查入口是 `git status --short`、`git rebase --show-current-patch`、`git ls-files --unmerged` 与 Index stage 内容；本章实验不会把固定内部目录作为断言条件。

## abort 的安全边界

在开始 rebase 前先检查并保存工作现场：

```bash
git status --short
git branch backup/topic-before-rebase topic
git rebase origin/main
```

若在这个干净前提下决定放弃：

```bash
git rebase --abort
```

`test.sh` 实际执行了这条命令，并确认 `topic` 回到 `topic-original`、Working Tree 恢复干净、`REBASE_HEAD` 消失。这个结果覆盖本实验开始时工作区干净的范围。把额外未提交修改混入 rebase 前或冲突解决过程中，会扩大恢复难度；先保存这些修改，再选择 abort 或继续。

## 已共享历史：协调优先于命令

本地私有 topic 可以由作者自行重放。分支一旦已 push，或已经有人基于旧 commit 开发，改写会改变其他人的共同祖先和后续操作路径。先确认共享状态和项目规则，再执行历史改写。

一个常见的受控流程是：

```bash
git fetch origin
git switch topic
git status --short
git branch backup/topic-before-rebase topic
git rebase origin/main
# 运行本项目受影响的构建、测试和审查
git push --force-with-lease origin topic
```

`--force-with-lease` 会要求远端引用仍是本地预期的值，远端已被其他提交推进时会失败。它减少误覆盖风险，不能替代协作通知、评审和行为验证。后台自动 fetch 也会影响没有显式期望值的 lease 判断，所以关键共享分支应遵守团队明确的远端更新流程。

| 分支状态 | 优先判断 |
| --- | --- |
| 只在本地，作者独自使用 | 可在备份引用后 rebase，并验证结果 |
| 已 push，但没有其他人基于旧 tip 开发 | 先告知相关人，重放后使用项目允许的受控推送方式 |
| 已有人基于旧 tip 开发或分支承担发布职责 | 协调共同的迁移方案；merge、追加 revert 或新分支常比直接改写更容易恢复 |

## 改变条件预测题

给定：

```text
          T1  topic
         /
...---B---U1  main
```

1. `git rebase main` 成功应用 `T1` 后，为什么结果 commit 不等于 `T1`？
2. 如果 `topic` 已经等于 `main`，再执行同一条命令，会不会必定生成新 commit？
3. 如果上游已有与 `T1` 等价的干净 cherry-pick，默认 rebase 可能怎样处理？

答案：

1. 新结果以 `U1` 为 parent，Git 创建了另一个 commit 对象。
2. 不会。没有需要重放的提交时，Git 可以保持引用不变。
3. Git 可以识别该变化已在上游，并在默认处理下跳过它；需要保留这种重放行为时，要显式选择相应选项并检查结果历史。

## Agent 判断题

Agent 准备对已经 push 的 `topic` 执行 rebase，并说“代码 diff 很小，直接 `git push --force` 就行”。哪一组行动符合可审核的协作流程？

```text
A. 直接 force push，只要本地测试通过即可
B. 先确认是否有人基于旧 tip 开发，建立备份引用，rebase 后运行受影响验证，并按项目规则使用 force-with-lease 或协调迁移
C. 只检查 commit ID 是否变化
```

选择 B。代码 diff 的大小不能说明引用改写对协作者的影响。备份引用支持审查与恢复，受影响的验证检查重放后的行为，远端 lease 只负责一部分并发保护。

## 常见误解

### “rebase 修改了旧 commit”

旧 commit 对象保持不变。rebase 在需要重放时创建新对象，并把分支引用更新到新 tip。

### “每次 rebase 都会修改所有 commit ID”

只有实际创建的重放 commit 才有新 ID。没有待重放提交，或提交被识别为已在上游时，结果历史可能没有对应的新对象。

### “rebase 里的 ours 与普通 merge 含义相同”

rebase 把工作分支变化应用到上游之上，stage 2 表示以新上游为基础的已重放结果，stage 3 表示正在应用的工作分支提交。先读取实际内容再选择解决策略。

### “abort 可以无条件保留我所有临时修改”

`git rebase --abort` 的恢复效果依赖开始前和过程中工作区的状态。干净开始、明确保存额外修改，再执行 abort，恢复边界才清楚。

## 延伸阅读

- [`git rebase` 官方文档](https://git-scm.com/docs/git-rebase)
- [`git push` 官方文档：force-with-lease](https://git-scm.com/docs/git-push)
- [`git merge-base` 官方文档](https://git-scm.com/docs/git-merge-base)
- [第 06 章：Merge 先找共同祖先](git-mental-model-06-merge.md)
