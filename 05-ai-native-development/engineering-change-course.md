# 一次工程变更，从任务契约走到恢复

[English](05-ai-native-development_en/engineering-change-course_en.md) | [本地实验](../labs/ai-change-control/README.md)

一个 Agent 把 `SERVICE_TIMEOUT` 的空值修成默认 `30`，看起来是很小的修改。工程上需要回答的却是一串问题：任务到底允许改变什么？脏工作区里通过的测试，验证的是哪个版本？审查者同意的是哪一组 diff？集成后的代码、制品和运行结果怎样对应？如果要恢复，哪些影响还留在 Git 之外？

本课用 [Agent 变更控制实验](../labs/ai-change-control/README.md) 的同一个临时仓库贯穿这些决定。实验脚本会真实执行 Git、Python 单元测试、`git archive`、SHA-256 计算和 `127.0.0.1` HTTP 请求；它不连接真实 CI、GitHub、生产环境或外部服务。下文的「实验已验证」只指这个本地临时环境，不能推到线上结果。

这篇文章负责连续案例和每个交接处的接受条件。[接受 Agent 变更：从意图到证据](ai-change-control-loop.md) 深入记录证据时需要哪些字段和边界；[AI Native Git 工作流](ai-native-git-workflow.md) 提供日常检查、分支和 worktree 的操作速查。三篇文章互相连接，但不重复三份相同流程。

## 课程地图：每一段要交出什么

```text
任务契约
  -> 既有编辑与隔离
  -> Index 中的候选 diff
  -> 审查和候选 SHA
  -> CI / 集成结果
  -> 制品与本地运行身份
  -> 代码恢复与业务补偿
```

| 环节 | 此刻的决定 | 可接受的证据 | 需要拒绝或重新判断的情况 |
| --- | --- | --- | --- |
| 任务契约 | 空值是否默认 `30`，哪些行为保持 | 明确的输入、输出、保留项和验证方式 | 范围含糊，或默认值、错误语义、调用方影响没有写出 |
| 隔离 | 现有编辑是否属于本任务 | `status`、基线 SHA、路径归属 | 共享目录有未知编辑，仍准备切换、清理或部分提交 |
| 候选 commit | 哪些路径构成待审版本 | Index、提交 diff、候选 SHA | 测试通过只发生在脏工作区，或无关笔记被混入 |
| 审查与 CI | 谁接受哪一个版本，检查跑在哪个 SHA | 审查结论、命令、结果、被测 SHA | 用原分支测试替代已经不同的集成结果 |
| 制品与运行 | 运行的字节是否来自被接受版本 | 制品 SHA-256、清单、构建信息、运行响应 | 哈希被当成签名、可信构建或生产发布证明 |
| 恢复 | 哪些代码和外部效果要分别处理 | `revert` 后的代码验证、事件与补偿记录 | 把 Git 回退当成数据、消息或外部调用已自动撤销 |

## 先写任务契约：给小修复一个可判断的边界

实验的基线服务在 `SERVICE_TIMEOUT` 缺失或为空时抛出 `SERVICE_TIMEOUT must be set`。本次目标是让缺失值和空字符串返回 `30`。显式正整数仍按原值使用；非整数和非正数的错误规则仍保留。这些保留项使「测试通过」有具体含义，避免默认值修复顺手扩大成错误处理、接口或重试策略重写。

任务契约可以写成下面这样。尖括号表示实际项目需要填写的事实，不能用示意 SHA 替代真实值。

```text
目标：SERVICE_TIMEOUT 缺失或为空时使用 30。
保持：显式正整数照常使用；非法值仍失败；不改变接口、事件格式和重试策略。
范围：app.py 与 tests/test_timeout.py；notes/agent-scratch.md 不属于本任务。
验收：目标测试在候选 commit 的干净 worktree 通过；运行响应报告该候选 SHA。
恢复：若默认值行为有问题，恢复代码并评估已写出的事件或其他外部效果。
```

此刻要决定的是「行为边界」，还不是选命令。若业务要求空字符串与缺失值不同，或者线上配置、调用方兼容性会改变默认值的语义，应先补充契约和相关事实，再让 Agent 改代码。源码中的默认值只能说明代码可见的行为；最终环境变量、配置中心或部署参数仍需要在目标环境核实。

## 开始时保留现场，再决定隔离方式

实验每次都会创建带标记的临时根目录和其中的 `agent-worktree`。它先提交基线，然后让 Agent 同时改三处：

- `app.py` 含空值默认 `30` 的实现；
- `tests/test_timeout.py` 含目标测试；
- `notes/agent-scratch.md` 含无关本地笔记。

笔记的所有者是人，且不属于 timeout 修复。这个细节模拟真实共享工作区：`git status` 只说明路径改变，不能说明谁拥有它或它是否可以丢弃。

在真实仓库先做只读观察：

```bash
git status --short
git branch --show-current
git rev-parse HEAD
git worktree list
```

状态有未知 staged、unstaged 或 untracked 内容时，接受条件是先记录归属并转到单独的干净 worktree。不要用 `switch`、`restore`、`clean` 或广泛的 `reset` 腾出空间。已确认当前目录干净且团队规则允许时，才可以在这里建立任务分支；并行任务则应各有目录和 Index。具体的日常操作前提见 [AI Native Git 工作流](ai-native-git-workflow.md) 和 [给 AI Agent 使用的 Worktree](worktree-for-ai-agents.md)。

## Index 让候选版本可见：先经历一次会失败的接受尝试

实验先在脏工作区运行目标测试。此时工作区已有修复后的 `app.py`，所以测试退出码为 `0`。随后它只把 `tests/test_timeout.py` 放入 Index 并提交，得到坏候选 commit；修复后的 `app.py` 和无关笔记仍留在工作区。

这时必须拒绝「本地已通过，所以测试 commit 可以接受」的结论。候选 commit 的干净 worktree 只含新增测试和旧版应用，空值仍会报错。脚本实际断言该测试退出码为 `1`，并包含：

```text
empty timeout must default to 30; got SERVICE_TIMEOUT must be set
```

这个负例说明两个比较对象不同：`git diff` 观察 Working Tree 相对 Index 的内容，`git diff --cached` 观察 Index 相对 `HEAD` 的内容。测试进程读取当前文件系统，不会自动只读取已暂存内容。审查前至少检查：

```bash
git diff --stat
git diff
git diff --cached
git status --short
```

实验随后只提交 `app.py` 的修复，候选 commit 才同时含目标测试和实现；`notes/agent-scratch.md` 仍是未提交编辑。新建的干净 worktree 在实际候选 SHA 上通过测试。可接受的结论是「这条命令在这一个候选 SHA 的干净目录通过」，不能扩大为「整个工作区」或「已经集成」。

如果同一文件混有两种意图，路径级提交也不足以分开它们。应先进入干净的任务 worktree，再用交互式暂存组织 hunk；如果路径本身还有他人已有内容，停下来澄清归属。深入的 Index 心智模型见 [Index：下一次提交的草稿](../01-getting-started/git-mental-model-03-index.md)，拆分策略见 [AI Commit 拆分](ai-commit-splitting.md)。

## 审查候选：接受行为，不只接受绿色输出

候选 SHA 已明确后，审查者要回到任务契约检查 diff。这个案例至少要问：

- 缺失值与空字符串是否都返回 `30`；显式 `15` 是否仍返回 `15`；
- 非整数和非正数是否仍按契约失败；
- 默认值是否会被目标环境的配置覆盖；
- commit 是否只包含测试和应用修复，无关笔记是否仍在工作区；
- 测试是否能在修复前失败、修复后通过，以及失败原因是否就是预期边界。

审查者可以接受「候选实现符合契约，且证据绑定到该 SHA」，也可以因遗漏保留项、范围混入或未覆盖的配置来源拒绝。AI 的风险扫描可以帮助定位文件和反例，但它不替人确认业务语义。GitHub 的 Pull Request review 支持评论、批准和要求修改；实际仓库是否要求批准、由谁批准，取决于其规则与权限，[GitHub 官方说明](https://docs.github.com/en/pull-requests/reference/pull-request-reviews) 可作平台事实参考。

把结论连同版本写下来：

```text
候选：<本次运行产生的 candidate SHA>
检查：<命令>，退出码 <实际结果>
已覆盖：空值默认、显式值、候选范围
未覆盖：<真实配置来源、并发调用、其他依赖>
审查决定：接受 / 拒绝，原因 <具体行为或 diff>
```

证据字段的完整格式和「未覆盖」怎样写，继续阅读 [接受 Agent 变更：从意图到证据](ai-change-control-loop.md)。

## CI 与集成：候选 SHA 不是永远等于合入结果

本地干净 worktree 的测试证明的是候选 commit。合入可能产生不同的提交 SHA：merge commit、squash merge、rebase merge 都可能改变最终历史；目标分支在审查期间前进也会改变待集成的组合。只有快进合入且最终 `HEAD` 就是被测候选 SHA 时，候选测试才能直接对应该代码版本。

因此需要按条件作决定：

1. 集成结果 SHA 与已测候选 SHA 相同：保留候选测试证据，并记录实际合入 SHA、审查决定和环境。
2. 集成结果产生新 SHA，或目标分支在检查后已有新提交：原分支测试不能直接代表组合结果。对这个集成结果重新运行必要检查，并把输出绑定到新 SHA。
3. CI 提供的是 PR 合并结果或合并队列结果：接受该结果时记录触发事件、实际 ref 和 SHA，不能只贴 Agent 分支 SHA。

GitHub Actions 的对象需要特别标明：对未合入的 `pull_request`，默认 `GITHUB_REF` 是 PR merge ref，`GITHUB_SHA` 是该 merge ref 的最后一个 merge commit；要取得 Agent 分支最后一个 commit，使用 `github.event.pull_request.head.sha`。`merge_group` 又有自己的 SHA 和 ref。使用合并队列且把 Actions 检查设为必需时，工作流需要监听 `merge_group`，否则该检查不会在队列中报告。相关事件与 SHA 语义见 [GitHub Actions 官方文档](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows)。本文只要求在证据中区分这些对象，具体工作流配置归 [面向 AI 生成改动的 CI](ci-for-ai-generated-changes.md)。

受保护分支可以配置合入前的审查和状态检查；严格状态检查要求分支与 base 保持最新，合并队列会在最新目标分支及队列中的变更组合上运行必要检查。具体能力和仓库配置以 [GitHub protected branches 官方文档](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches) 为准。实验没有创建 PR，也没有运行 CI，所以不能把本地退出码写成 GitHub 检查通过。

本课只建立「哪个证据属于哪个版本」的判断链；后台或远程 Agent 的版本、环境与回收证据见 [后台 Agent 工作流](background-agent-workflow.md)。

## 制品发布前：把 commit、字节和运行身份连起来

实验从已通过的候选 commit 使用 `git archive` 取出源码，并打包 tar.gz 制品。它生成制品外部的 JSON 清单，记录：

- 候选 commit SHA；
- 完整 tar.gz 的 SHA-256；
- 提取后 `app.py` 的 SHA-256；
- 源码版本和写入制品的构建信息。

脚本还断言制品中的笔记仍是基线提交版本，未提交的 `notes/agent-scratch.md` 没有混入。接着它复制并篡改制品副本，在解包和服务启动前用 SHA-256 预检拒绝，错误包含 `artifact checksum mismatch`。这证明预检能够发现「这份副本的字节与此清单记录不一致」。

原制品通过预检后，脚本再次比较清单、Git 中该 commit 的 `app.py` 和制品内构建信息，才以空的 `SERVICE_TIMEOUT` 在系统分配端口启动服务。`/health` 的真实 HTTP 响应同时报告：默认超时 `30`、版本、候选 commit 和事件计数。这给出一条本地证据链：被测 SHA → 制品记录 → 运行响应。

哈希的能力要按对象区分。制品 SHA-256 检查整份制品字节是否匹配可信的清单记录；源码 SHA-256 检查清单中记录的 `app.py` 字节是否被替换。两者都不说明谁生成或签署了清单，不能证明构建机可信、依赖来源安全、制品已部署，更不能证明生产业务正确。生产发布仍需要真实的构建来源、权限、部署记录和目标环境验证。

## 在本地保留证据：先写判断，再解释错误答案

以下命令只运行这个仓库提供的临时实验，不会提交、切换或清理宿主仓库。先运行一次保留模式，复制最后一行 `kept lab root:` 后的实际路径；不要把示意路径或示意 SHA 当成结果。

```bash
python3 labs/ai-change-control/lab.py --keep

# 把上一条命令最后一行打印的真实路径填入这里
lab_path=/printed/lab/root

python3 -m json.tool "$lab_path/evidence/exercise-evidence.json"
git -C "$lab_path/agent-worktree" log --oneline --decorate --all --graph
git -C "$lab_path/agent-worktree" status --short
cat "$lab_path/external-state/events.jsonl"
```

在查看输出前，写下下面三项判断和理由：

1. 「测试 commit 已含新测试」能否推出候选已经修复？
2. 「清单中的 SHA-256 匹配」能否推出制品由可信系统构建并已安全发布？
3. 两个 `git revert` 后，事件文件是否应自动回到零条？

运行后，前两项的否定答案分别来自状态隔离和证据范围：测试 commit 缺少工作区中的应用修复；可重算哈希只比较字节与记录。第三项的否定答案来自状态归属：两个 HTTP 请求已经把临时事件写到 Git 外部。脚本会验证回退代码以显式 `15` 通过、回退制品响应的事件计数为 `2`，并在事件文件保留修复版本和回退版本的记录。

确认所需证据后，只清理脚本刚打印的带标记临时根：

```bash
python3 labs/ai-change-control/lab.py --cleanup "$lab_path"
```

该脚本会拒绝未标记目录、仓库根目录、用户主目录、文件系统根目录和临时目录之外的路径。若变量不是脚本输出的路径，停止，不要执行清理命令。

## 集成后仍要验证，事故时分别恢复代码和业务

在实验里，候选制品运行后写入第一条事件。随后脚本连续创建两个 `git revert` commit，恢复基线应用和测试，再构建并运行回退制品。回退代码能接受显式 `SERVICE_TIMEOUT=15`，但事件文件仍有两条记录：第一条来自修复版本，第二条来自回退版本。

这一步的接受条件分成两类：代码层面，回退 SHA 的干净 worktree 测试和回退制品响应都符合旧规则；业务层面，团队已经判断外部事件是否需要停止、去重、补偿或通知。若事件代表订单、扣款、消息投递或第三方调用，`git revert` 只生成反向代码提交，不能代替这些处置。不要为了恢复共享分支而改写他人已经依赖的历史。

本地实验只把事件写进临时 JSONL 文件，不能证明某个真实事故已被处理。真实场景的分级、沟通、补偿和证据留存，见后续专题 [AI Agent 事故恢复](../06-troubleshooting/ai-agent-incident-recovery.md)。

## 完成这课后，换一个仓库也能判断

面对另一个 Agent 的改动，不需要复制本课的文件名、语言或工具。你应该能回答：

- 任务允许改什么，哪些行为必须保持；
- 哪些编辑已有所有者，候选 diff 在 Index 和 commit 中到底包含什么；
- 哪个 SHA 运行了什么命令，集成 SHA 是否还是同一个版本；
- 制品和运行响应怎样回到这个 SHA，哈希还缺少什么信任前提；
- 代码恢复后，哪些数据或外部效果仍要由业务流程处理。

这条判断链把 Git 原理放进一段可重复的工程叙事。命令细节回到 [AI Native Git 工作流](ai-native-git-workflow.md)，证据合同回到 [接受 Agent 变更：从意图到证据](ai-change-control-loop.md)，然后再按项目风险选择 CI、后台 Agent 和事故恢复专题。
