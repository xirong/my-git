# 后台 Agent 任务：从发出到回收

[English](05-ai-native-development_en/background-agent-workflow_en.md) | 中文

后台 Agent 可以在提问者离开后继续执行。它给出“完成”消息时，工程团队仍要回答：它改的是哪一个仓库和基线？候选版本是什么？证据覆盖了什么？谁有权接受它？这篇把后台任务当作一次可回收的工程交接，而非一条完成通知。

它适用于任何异步执行的编码 Agent。本文的流程是平台中立的；文末 GitHub Copilot cloud agent 仅作一个已核实的具体映射。本文没有实际启动云端 Agent，也不把示例当作云端运行记录。

本文提出的最小任务契约、attempt、过期状态、现场保留和接受决定，是本手册建议团队自行采用的交接规则。Agent 平台未必原生保存这些字段、阻止重复执行，或在到期时自动回收结果。团队需要在任务系统、PR 模板、编排配置或人工流程中落实它们；GitHub 段只说明本次查到的 GitHub 原生行为，不把这些规则表述为平台自动保证。

## 问题：完成状态没有说明可否接受

“Agent 已完成”只表示该次执行到达了某个结束状态。它不能证明候选改动仍以正确基线为前提，不能证明测试跑在候选版本，也不能证明改动符合业务意图。后台任务需要完整经过：

```text
发出任务 -> 执行与留痕 -> 回收结果 -> 人工决定
                                      -> 接受
                                      -> 拒绝
                                      -> 返工
                                      -> 过期
```

接受的是一组有边界的变更和证据。拒绝、返工、过期同样是正常结果，并为下一次尝试保留可核对的现场。

## 1. 发出前写最小任务契约

任务 ID 是整个交接的关联键。不要只用自然语言标题关联任务、分支、日志和 PR；重试或相似需求很容易混淆。下表字段足以让接收人判断该回收哪一份结果。

| 字段 | 要写清的内容 |
| --- | --- |
| 任务 ID | 唯一 ID、尝试次数、幂等键；重复发出时保留同一父任务并增加 attempt |
| 仓库与目标 | 规范仓库标识、目标分支或集成 ref、任务目录 |
| 已确认基线与候选 | 发出时的 `base SHA`；回收时必须补充 `candidate SHA` 或明确说明未产生提交 |
| 允许范围 | 可改路径、允许动作、明确保留的文件和行为 |
| 预期行为 | 输入、输出、错误语义、兼容性，以及不能变化的约束 |
| 验证 | 必跑命令、手工步骤、所需数据或环境，以及证据应绑定的 SHA |
| 权限 | 读取、写入、网络、密钥、PR、CI 与发布的最小允许范围 |
| 负责人 | 发出人、接收人、集成人；谁有权终止、接受、返工或过期 |
| 预算和时限 | 令牌、并发、费用或运行时限；到期后的保存与处理规则 |

一个小修复也可以用简短契约表达。下面的 `orders-api`、`main` 和 `8d21...` 都是虚构示意：实际任务必须填写真实仓库、真实集成 ref 和完整 SHA。

```text
任务：AGT-184，attempt 1
仓库 / 目标：orders-api，main
基线：8d21...；候选：待回收
允许：src/timeout/**、tests/timeout/**；不改部署配置和依赖清单
行为：空 timeout 返回 30；非法值仍报原有错误
验证：在 candidate SHA 的干净目录运行 npm test -- timeout
权限：只写任务分支；不能合并、发布或访问生产数据
接收人：值班工程师；45 分钟后过期并保存现场
```

示意 SHA 无法让人辨认后来移动过的基线。

## 2. 执行期间记录可回收的事实

执行平台至少应把任务 ID 关联到仓库、开始 ref、运行环境、工具权限、每一次 attempt、分支或 worktree、日志位置和结束原因。由 Agent 报告的“测试通过”还要附上命令、退出码、执行时间、工作目录和被测 SHA。

Agent 需要继续做事时，追加指令也应进入同一任务记录，并注明它是当前 attempt 的输入。若重新开一个 session，增加 attempt 号并重新确认基线，避免两次运行把彼此的改动认作自己的结果。

对于长任务，设置一个可观察的心跳和到期时间。心跳消失、预算用尽或基础环境失效时，状态应成为 `expired` 或 `failed`，不可伪装成空结果。迟到的提交仍可作为新 attempt 的输入，不能自动覆盖已被人接受的集成状态。

## 3. 回收时先核对版本、范围与证据

接收人按照同一顺序处理结果，能减少“先看绿色输出，后发现版本不对”的返工。

1. 核对任务 ID、仓库、目标 ref、基线 SHA、候选 SHA 和 attempt。
2. 比较目标 ref 现在的 SHA 与发出时记录的 base。不同代表集成基线已移动，候选需要按新组合重新判断。
3. 在 `base..candidate` 范围查看路径和 diff，确认没有越过允许范围。
4. 检查候选提交是否完整。工作区中的未提交编辑、未跟踪文件和未交付的 patch 只能作为现场，不能当作候选提交。
5. 核对每条验证证据执行的命令、结果、环境和 SHA；证据缺失时把任务退回返工或拒绝。
6. 用任务契约中的预期行为审查 diff，再由有权限的接收人作出接受、拒绝、返工或过期决定。

下面的命令只读，不会连接 remote。它们用于检查已有的 base 和 candidate：

```bash
git rev-parse <integration-ref>
git merge-base --is-ancestor <base-sha> <candidate-sha>
git diff --name-status <base-sha>..<candidate-sha>
git diff --check <base-sha>..<candidate-sha>
git show --stat --oneline <candidate-sha>
```

`merge-base --is-ancestor` 只说明候选继承了记录的基线；它不能证明目标 ref 尚未前进，也不能取代 diff 和测试。若集成 ref 已前进，复现验证时应针对准备接受的组合，而非继续引用旧 candidate 的绿色输出。

## 4. 常见异常如何回收

| 观察到的情况 | 接收动作 | 不要做什么 |
| --- | --- | --- |
| base 已变化 | 记录新 ref SHA；让 Agent 或接收人基于新组合更新候选并重新验证 | 把旧 base 的测试结果写成已集成的证据 |
| 编辑未提交 | 保存状态、diff、未跟踪路径和归属；要求提交为候选，或由负责人决定是否丢弃 | 用 `clean`、`restore` 或宽泛 `reset` 清除未知编辑 |
| 错误分支或目标 | 比较 candidate 的父链、PR 目标和允许路径；返工时明确正确 base/ref | 仅因 commit 信息看起来合理就接受 |
| 没有可复查的证据 | 标记缺少的命令、输出、版本或环境；要求补跑或拒绝 | 用“Agent 说通过”代替实际证据 |
| 同一任务重复运行 | 以任务 ID、attempt、仓库、base 和目标路径去重；保留一个主动 attempt，其他结果只作候选输入 | 让多个运行向同一分支无序写入 |
| 超时或失败 | 标记 `expired`/`failed`；保存最后的 SHA、状态、日志和未提交差异，再释放平台占用 | 把超时任务标成成功，或在未保存现场时删除其隔离目录 |

失败现场的价值在于可追溯。保存最少的任务契约、分支或 candidate SHA、`git status --porcelain`、路径列表、diff 摘要、验证输出、环境标识和终止原因。若日志含密钥、用户数据或内部地址，按团队数据规则脱敏后再分享。

清理应发生在决定之后：先写下保留位置和负责人，再只处理已证明由该任务独占的 worktree、临时目录或分支。含未知编辑的目录保持原状并升级给其所有者。候选提交即使被拒绝，也应在审计保留期内能够定位；安全删除的具体期限由团队的存储与合规规则决定。

## 5. 平台中立的交接与回收示例

发出方可以把以下记录放进 issue、任务系统或 PR 描述；尖括号内容必须被实际值替换。

```text
任务 ID：AGT-184 / attempt 2
仓库与目标：orders-api / main
发出基线：<base SHA>
候选：<candidate SHA>；分支：agent/AGT-184
允许范围：src/timeout/**、tests/timeout/**
行为：空 timeout 返回 30；非法输入仍保留原错误
证据：npm test -- timeout，退出码 <n>，在 <candidate SHA>、<环境> 执行
未覆盖：<真实配置来源、并发调用或其他边界>
权限与时限：只写任务分支；不得合并/发布；到 <时间> 过期
建议：接受 / 返工，原因 <与契约对应的事实>
```

回收人不要只回复“收到”。一个可执行的决定应该像这样：

```text
决定：返工
依据：main 已从 <base SHA> 前进到 <new SHA>；测试只记录了旧 candidate。
下一步：以 <new SHA> 为基线生成新 candidate，并在干净目录重跑指定测试。
保留：attempt 2 的分支、diff 摘要和测试日志，保存至 <位置>。
负责人：<姓名或角色>；截止：<时间>。
```

## 6. 可运行的本地版本核对

以下示例只在 `/tmp` 创建一个带 `background-agent-demo.` 前缀的临时 Git 仓库。它模拟 Agent 提交候选后 `main` 前进，并在独立 worktree 检查候选文件；不访问 remote、不创建 PR、不触发付费服务。运行前仍应读懂每一行，尤其不要把示例路径替换成真实工作目录。

```bash
set -euo pipefail
demo_dir=$(mktemp -d /tmp/background-agent-demo.XXXXXX)
case "$demo_dir" in /tmp/background-agent-demo.*) ;; *) exit 1 ;; esac

git init -q -b main "$demo_dir"
git -C "$demo_dir" config user.name "Background Agent Demo"
git -C "$demo_dir" config user.email "background-agent-demo@example.invalid"
printf 'timeout=10\n' > "$demo_dir/config.txt"
git -C "$demo_dir" add config.txt
git -C "$demo_dir" commit -qm "base timeout"
base_sha=$(git -C "$demo_dir" rev-parse main)

git -C "$demo_dir" switch -q -c agent/AGT-42 "$base_sha"
printf 'timeout=30\n' > "$demo_dir/config.txt"
git -C "$demo_dir" add config.txt
git -C "$demo_dir" commit -qm "agent timeout change"
candidate_sha=$(git -C "$demo_dir" rev-parse HEAD)

git -C "$demo_dir" switch -q main
printf 'release_note=keep\n' > "$demo_dir/release.txt"
git -C "$demo_dir" add release.txt
git -C "$demo_dir" commit -qm "integration moved"
integration_sha=$(git -C "$demo_dir" rev-parse main)

test "$base_sha" != "$integration_sha"  # 检出 base 已移动
git -C "$demo_dir" merge-base --is-ancestor "$base_sha" "$candidate_sha"
git -C "$demo_dir" diff --check "$base_sha".."$candidate_sha"
git -C "$demo_dir" worktree add --detach "$demo_dir/verify" "$candidate_sha"
test "$(sed -n '1p' "$demo_dir/verify/config.txt")" = 'timeout=30'
git -C "$demo_dir" worktree remove --force "$demo_dir/verify"
```

最后一条 `worktree remove` 的目标是前面刚创建且名称固定的 `verify` 目录。临时根目录的处置应在确认运行结果已记录后，按操作系统的可恢复删除方式处理。真实仓库的 worktree、分支或未知目录不适用这个示例。

## 7. GitHub Copilot cloud agent 的具体映射

截至 2026-09-07，GitHub 官方文档描述的 cloud agent 可作为上述协议的一个具体实现。该映射只覆盖 GitHub 当前公开能力，功能处于预览或仓库设置不同都会改变实际行为。

GitHub 的 Issue、session、分支和 PR 可以承载任务记录，却不会因本文的模板自动获得任务 ID、允许路径、预算、过期结论或接受决定。将这些团队字段写入 Issue、PR、外部任务系统或自动化配置后，仍由团队自己的规则和有权限的人执行回收。

| 回收环节 | GitHub 官方文档已说明的映射 | 团队仍需保留的判断 |
| --- | --- | --- |
| 任务发出 | 有仓库写权限的人可给 Issue 分配 Copilot；该流程会启动任务、创建 PR，并在完成时请求 review | Issue 要写清契约，特别是 base、范围、测试与负责人 |
| Agent 身份与执行 | API 文档将可分配身份列为 `copilot-swe-agent`；cloud agent 在 GitHub Actions 支持的临时开发环境中工作 | 记录实际 Issue、session、分支、PR 和候选 SHA，方便以后审计 |
| 结果与验证 | Agent 可在环境中执行测试和 linter；GitHub 还可配置内建代码质量、安全检查与第二次 Copilot review | 这些工具和 Agent 报告只是证据输入；接收人仍核对行为、范围、执行 SHA 和未覆盖项 |
| 工作流触发 | 默认情况下，Agent 向 PR 推送后 GitHub Actions 工作流不会自动运行；PR 的合并框可由人点击批准运行。管理员可改为自动运行 | 检查执行的工作流、权限和 secrets，再决定是否批准；任何绿色结果都要写回其对应 SHA |
| 接受 | Agent 完成后会请求 reviewer；PR 的人工审查、分支规则和合并授权仍按该仓库配置 | 有合并权限的人依据任务契约作接受或返工决定，不能把自动结束状态当作合入授权 |

GitHub 还说明，修改 cloud agent 的验证工具与自动 Actions 设置需要仓库管理员权限。将 Actions 改成免人工批准可能让未经审查的代码取得仓库写权限或访问 Actions secrets，文档对这一点有明确警告。先在低风险仓库和最小权限设置中验证团队规则，再扩大自动化范围。

来源均在本次写作时只读核实： [Using Copilot cloud agent on GitHub](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent/use-cloud-agent-on-github)、[Configuring settings for GitHub Copilot cloud agent](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent/configuring-agent-settings)、[Using Copilot cloud agent via the API](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent/use-cloud-agent-via-the-api) 和 [Assigning issues and pull requests](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/assigning-issues-and-pull-requests-to-other-github-users)。本文没有替团队核实某个仓库是否已启用该功能、其付费计划、权限、分支规则、工作流或 secrets。

## 继续阅读

- [一次 Agent 变更，如何从意图走到验收](ai-change-control-loop.md)
- [AI 生成变更的 CI：把检查绑定到候选版本](ci-for-ai-generated-changes.md)
- [AI Agent 事故恢复：先保留现场，再决定代码处理](../06-troubleshooting/ai-agent-incident-recovery.md)
- [两个 AI Agent 工程案例：把公开报告转成团队决策](../10-company-practices/ai-native-engineering-cases.md)
