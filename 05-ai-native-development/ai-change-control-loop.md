# 一次 Agent 变更，如何从意图走到验收

[English](05-ai-native-development_en/ai-change-control-loop_en.md) | 中文

场景：让 Agent 修复一个超时问题。它交付了代码、测试和“已完成”的说明。你需要决定是否接受这次改动，以及出现问题时能恢复什么。

本文负责把意图、范围、候选 SHA 和验收证据写成可审核的合同。要沿同一个 `SERVICE_TIMEOUT` 实验案例连续学习隔离、Index、审查、集成 SHA、制品和恢复，请先读[一次工程变更，从任务契约走到恢复](engineering-change-course.md)。日常命令速查归[AI Native Git 工作流](ai-native-git-workflow.md)。

把验收连成一条可追踪的链：**任务意图 → 变更范围 → 提交版本 → 验证证据 → 合入决定 → 发布结果。** 任意相邻环节对不上，都可能让“测试通过”失去意义。

## 1. 先定义你愿意接受的行为

任务至少说清：现有错误、期望结果、不能改变的行为，以及如何验证。对于超时修复，明确是否允许调整默认值、错误码和重试策略。任务规模很小时可以只写几句话。

让 Agent 同时说明它使用的基线提交和修改路径。基线帮助区分任务产生的变化与原来就存在的变化。

## 2. 确认现场与隔离范围

先读状态，避免把别人的编辑当成 Agent 的结果：

```bash
git status --short
git branch --show-current
git rev-parse HEAD
git worktree list
```

这些命令只读。记录已有改动及其归属。分支隔离历史线，worktree 隔离工作目录和各自的 Index；同一个工作目录里切换分支，不能替代并行隔离。具体步骤见 [Worktree for AI Agents](worktree-for-ai-agents.md)。

## 3. 用 Index 定义本次接受的改动

```bash
git diff --stat
git diff
git diff --cached
```

普通 diff 比较工作区与 Index，cached diff 比较 Index 与 HEAD，两者都要结合未跟踪文件检查。确认范围后，按具体路径暂存；一个文件混有多个意图时，使用部分暂存。提交动作按仓库权限约定执行。

**不要仅因无关文件碍眼就清理它。** 先确认归属，只提交任务相关部分。入门见 [Index 草稿](../01-getting-started/git-mental-model-03-index.md)，操作见 [AI Commit Splitting](ai-commit-splitting.md)。

## 4. 把验证绑定到实际版本

工作区测试可能读到未暂存内容。只有“运行了测试”还不足以证明待提交草稿正确。获得提交权限后，记录提交 ID，并尽量在该提交的干净检出中执行项目规定的验证；依赖、环境和测试数据也应能够说明。

```bash
git rev-parse HEAD
git status --short
git show --stat --oneline HEAD
```

这三个命令用于核对版本与现场，本身不是业务测试。若验证期间修改了源码、测试或配置，已有证据需要重新判断是否仍适用。合并结果也可能与分支版本不同，应验证实际将发布的版本。

对于没有测试体系的项目，记录可重复的手工步骤、实际结果和未覆盖项，不能写成“全面验证”。

## 4.1 可运行练习：让证据指向同一个候选版本

[Agent 变更控制实验](../labs/ai-change-control/README.md) 用临时 Git 仓库、最小 Python 服务、真实测试、制品和回环 HTTP 请求，把本节的判断串起来。它不触碰当前仓库的提交或工作区。

从仓库根目录运行：

~~~bash
python3 labs/ai-change-control/lab.py
bash labs/ai-change-control/test.sh
~~~

实验故意先构造一个负例：应用修复仍留在脏工作区，只有新测试进入候选 commit。当前目录测试通过，干净 worktree 的同一测试以退出码 <code>1</code> 和明确的超时错误失败。修正后，实验记录干净 worktree 实际执行的候选 SHA，再用 <code>git archive</code> 从该 commit 构建制品。

制品清单存放在制品外部，记录 commit SHA、制品 SHA-256、源码 SHA-256 和版本。实验会先复制并篡改制品，复用启动前的 SHA-256 校验入口，断言它以 checksum mismatch 被拒绝。原始制品随后重算 SHA-256，再核对清单、Git 源码和制品内的构建信息。HTTP 响应还会回传候选 SHA 和版本，作为运行结果与制品对应关系的辅助证据。

最后的 <code>git revert</code> 恢复代码，并不会自动删除服务先前写入的临时事件。这个边界说明代码恢复、制品切换和外部状态补偿需要分别处理。实验仅在 <code>127.0.0.1</code> 的临时目录运行，不代表真实 CI、生产发布、签名或供应链证明。

## 5. 给审查者一份可作决定的材料

下面是模板，尖括号字段必须替换为实际值：

```text
意图：<要解决的问题与不允许变化的行为>
基线 / 候选提交：<base SHA> / <head SHA>
范围：<相关路径与主要行为差异>
证据：<测试命令、结果、执行版本、必要环境>
未覆盖：<还不知道什么>
恢复：<代码恢复方式；数据或外部副作用如何处理>
责任：<按团队约定负责合入与发布的人或规则>
```

PR 是讨论和审查变更的入口，不能把标题、作者身份或绿色状态当作业务正确性的证明。见 [GitHub Pull requests](https://docs.github.com/en/pull-requests/reference/pull-requests) 与 [AI Reviewer 与 Human Reviewer](ai-reviewer-and-human-reviewer.md)。

## 6. 合入、发布、恢复分别验收

合入决定接受代码历史，发布把某个制品交给运行环境，业务验证证明目标行为是否成立。三者需要对应版本，也需要不同证据。

例如新超时策略触发了重复订单：revert 可以构造撤销代码的提交，但已经产生的订单需要业务补偿。先理解影响，再按已有事故流程处理。不要在共享分支上用历史重写代替团队恢复流程。

继续阅读 [Undo Anything](../06-troubleshooting/undo-anything.md) 和 [发布管理](../04-github-engineering/release-management.md)。

## 学会的标志

换一个 Agent 或一个代码库，你仍能找出：

- 哪些改动属于本次意图；
- 哪个版本经过何种验证；
- 谁按什么证据接受了变化；
- 哪些效果可以通过代码恢复，哪些不行。

这就是把 Git 原理转化为 AI 时代工程判断的一次完整练习。
