# AI 生成变更的 CI：让检查指向实际候选版本

[English](05-ai-native-development_en/ci-for-ai-generated-changes_en.md) | 中文 | [Agent 事故恢复](../06-troubleshooting/ai-agent-incident-recovery.md)

AI 会降低生成代码的成本，也会让一次 PR 更容易同时带入行为、依赖、配置和工作流变化。CI 的任务是把这些风险拆成可执行检查，并让每条结果明确回答：检查了哪一个 SHA、使用什么环境、还没有证明什么。

本文只说明怎样设计检查，不启用本仓库的 GitHub Actions、secret scanning、dependency review 或分支规则。GitHub 能力和计划前提已于 **2026-09-07** 按官方文档核实；仓库的实际计划、Actions 设置、规则集、required checks 和运行记录仍需在目标仓库确认。

## 先定义一条可复查的证据链

一条最小链路是：

```text
任务意图 → 候选 SHA → 干净检出 → 变更类型检查 → 项目测试 → 集成 SHA 检查 → 合入决定
```

每一段回答不同问题：

| 风险 | 可执行检查 | 应保留的证据 |
| --- | --- | --- |
| 工作区测试读到了未提交修复 | 在干净环境检出候选 SHA，再运行测试 | 候选 SHA、实际 `git rev-parse HEAD`、测试输出 |
| AI 扩大了行为范围 | 根据改动路径选择单元、契约、集成或迁移测试 | 路径、测试场景、通过和未覆盖项 |
| `.env`、token 或私钥混入 | 平台 secret scanning、经审查的组织扫描策略与人工复核 | 扫描能力是否可用、告警处理记录；不记录秘密正文 |
| manifest 或 lockfile 改动被忽略 | 依赖 diff、许可证与漏洞审查、项目构建测试 | 直接和间接依赖变化、批准理由、构建结果 |
| PR 通过后与最新目标分支组合失败 | 对 PR 合并结果或 merge queue 的集成 SHA 重新运行必要检查 | 集成 SHA、触发事件、检查名称和结果 |
| 不可信 PR 取得凭据或写权限 | 最小 token 权限、无 secret 的 untrusted-code job、隔离特权任务 | workflow 权限、触发条件、是否执行 fork head |

从 [一次 Agent 变更，如何从意图走到验收](ai-change-control-loop.md) 开始，可以先在本地把“测试结果属于哪个 commit”说清；CI 将同一判断搬到可重复的干净环境。[AI 变更审查实战样例](ai-change-review-example.md) 负责审 diff 和业务边界，两者互补。

## 候选 SHA 与干净检出

GitHub 的 `pull_request` 事件默认把 `GITHUB_SHA` 指向 PR merge branch 的最后一个 merge commit；需要只检查 PR head 时，官方建议使用 `github.event.pull_request.head.sha`。因此要先决定检查对象：

- **候选检查**：检出 `github.event.pull_request.head.sha`，回答 Agent 提交本身是否通过。
- **集成检查**：使用 PR merge ref 或 merge queue 的 SHA，回答它与最新目标分支组合后是否通过。

不要把两种结果混称为“PR 已测试”。下面是教学用的最小 workflow 骨架。`<official-full-commit-SHA>` 和项目测试步骤必须在启用前替换：到 action 的官方仓库选择稳定 release，核实该 release 对应的完整 commit SHA、仓库 owner 和变更说明，再将完整 SHA 写入 `uses`。完整 SHA 是 GitHub 官方安全文档所述的不可变 action 引用方式。

```yaml
name: AI change evidence

on:
  pull_request:
    types: [opened, synchronize, reopened]
  merge_group:
    types: [checks_requested]

permissions:
  contents: read

jobs:
  agent-candidate:
    if: github.event_name == 'pull_request'
    name: ai-change-candidate
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@<official-full-commit-SHA>
        with:
          ref: ${{ github.event.pull_request.head.sha }}
          fetch-depth: 1
          persist-credentials: false
      - name: Record candidate SHA
        env:
          EXPECTED_SHA: ${{ github.event.pull_request.head.sha }}
        run: |
          actual_sha=$(git rev-parse HEAD)
          test "$actual_sha" = "$EXPECTED_SHA"
          printf 'candidate SHA: %s\n' "$actual_sha"
      - name: Replace with the project's focused tests before enabling
        run: |
          echo 'Replace this failing placeholder with the project test command.'
          echo 'Example selection: a changed API needs contract and negative-path tests.'
          exit 1

  integration:
    name: ai-change-integration
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@<official-full-commit-SHA>
        with:
          fetch-depth: 1
          persist-credentials: false
      - name: Record tested integration SHA
        run: git rev-parse HEAD
      - name: Replace with integration tests before enabling
        run: |
          echo 'Replace this failing placeholder with an integration-appropriate command.'
          exit 1
```

这个骨架故意用失败占位步骤，避免未替换项目测试时得到伪绿色结果。`pull_request` job 检出 head SHA；`integration` job 在 PR 上使用默认 merge ref，在 merge queue 上使用 `merge_group` 的 SHA。GitHub 官方文档说明，使用 merge queue 的 required Actions checks 必须显式监听 `merge_group`，否则入队后不会报告该 check。

示例里的 `permissions: contents: read` 是 YAML 显式设定的低权限，不是对所有仓库的默认权限描述。GitHub 允许企业、组织和仓库设置 workflow token 的默认权限，也允许 workflow 或 job 用 `permissions` 进一步收紧或按需增加权限；本例不引用 `secrets`，也不配置特权环境。

这是配置解析层面的示例，未在真实 GitHub Actions 运行。可本地执行的 Git 边界由 [Agent 变更控制实验](../labs/ai-change-control/README.md) 和本文关联的事故恢复实验验证；Actions 触发、平台扫描和 required rule 的真实结果需要目标仓库的运行记录。

## 根据变更选择业务测试

通用的 `npm test` 或 `mvn test` 不能自动覆盖 Agent 改动触及的业务契约。根据 diff 中的路径、调用方和数据边界选择测试，再在 PR 中记录理由：

| 变更类别 | 至少补充的检查 | 不能由绿灯推出的结论 |
| --- | --- | --- |
| API、错误码、序列化 | 契约测试、旧客户端或负例 | 所有调用方都已适配 |
| 权限、身份、租户范围 | 拒绝路径、越权边界、审计字段 | 线上权限配置已正确 |
| 数据库或迁移 | 空库升级、回滚可行性、关键查询 | 生产数据修复已经完成 |
| 重试、队列、异步任务 | 幂等、重复投递、超时和失败路径 | 外部系统没有副作用 |
| 配置、默认值、feature flag | 默认值、覆盖来源、关闭路径 | 每个环境已使用同一最终配置 |
| 依赖或 lockfile | 构建、受影响测试、依赖审查 | 新库的运行时许可和风险已被接受 |

“项目测试入口”应是实际仓库已有命令，例如精确的模块测试、契约测试或迁移演练；不要把教程中的命令原样填入生产 workflow。测试退出码只证明覆盖的场景，未覆盖项仍要写进审查材料。

## 敏感信息和依赖：使用能力前先确认可用范围

GitHub secret scanning 会扫描仓库所有分支的 Git 历史中已知的硬编码凭据类型，并在发现泄露时创建告警。按 [GitHub Secret scanning 官方说明](https://docs.github.com/en/code-security/concepts/secret-security/secret-scanning)，公开仓库可免费自动使用；组织拥有的私有和内部仓库需要 GitHub Team 或 GitHub Enterprise Cloud 上启用 GitHub Secret Protection；用户拥有的仓库还有不同限制。secret scanning 缺少告警不能证明仓库不存在秘密，也不替代凭据失效和轮换。

组织自定义模式可以覆盖特定的私钥、连接串或 API key 形式。规则应由安全 owner 基于真实凭据格式、误报处理和日志暴露风险维护。不要把教学用的正则表达式当成生产 secret scanner，也不要把真实 secret 放进 CI 测试样本。

Dependency review 展示 PR 中 manifest 与 lockfile 的直接和间接依赖变化、漏洞、许可证、依赖者和发布时间。按 [GitHub Dependency review 官方说明](https://docs.github.com/en/code-security/concepts/supply-chain-security/dependency-review)，该功能面向公开 GitHub.com 仓库，以及启用 GitHub Code Security 的 GitHub Team 组织仓库；dependency review action 可用于公共仓库，以及启用了 GitHub Code Security 或 GitHub Advanced Security 的私有仓库。启用前还要确认 dependency graph、支持的生态和组织许可；本教程不假定每个计划都能使用这些能力。

## Required checks 的名字、来源与合并队列

把一个 CI job 设为 required 前，先确定它在 GitHub UI 的实际 check 名称、来源 App、触发事件和适用分支。保护分支要求的 check 可来自 checks 或 commit statuses；同名 job 出现在多个 workflow 时会造成歧义，官方文档提示这可能阻塞 PR。为每个 required job 使用稳定、唯一的 `name`，例如上例的 `ai-change-candidate` 和 `ai-change-integration`，再在分支保护或 ruleset 中按目标仓库的实际名称配置。

本仓库现有 [Docs Check workflow](../.github/workflows/docs-check.yml) 的 job ID 是 `docs-check`。该文件是否已经成为 required check、GitHub UI 显示的完整名称，以及是否适用于所有目标分支，都需要从当前 PR 与仓库设置核实；本文不改变它。

合并队列会将 PR 和最新目标分支及队列中的前序变更组合成新的 merge group。GitHub 为 `merge_group` 提供独立 SHA，必须在这个 SHA 上重新跑 required checks；PR head 的绿灯不能替代这次结果。

## 不可信 PR 的权限与 secret 隔离

把 fork 或来源不明的 PR head 当作不可信代码。为它运行的 job 使用最小 `GITHUB_TOKEN` 权限，避免注入 deployment、云、包仓库或其他长效 secrets。上面的 `contents: read` 与 `persist-credentials: false` 是该示例强制的源码读取边界，具体项目可以有不同权限需求，但应逐项写入 workflow 并接受审查。

需要分开看平台、仓库设置和示例本身。GitHub 当前文档说明，fork 触发的 `pull_request` 默认不向 runner 传递普通 secrets，且在未允许发送 write token 时会将 write 权限调整为只读。企业、组织或仓库可以设置默认 workflow 权限；私有仓库的 fork 策略还可允许 write token、secrets 与 variables、以及人工批准。目标仓库应在 Actions 设置中核实这些选项。这个示例不依赖上述默认限制：它明确将 `GITHUB_TOKEN` 设为 `contents: read`，没有引用 secrets，也不把 head 代码放进特权 job。即使这些限制都成立，不可信脚本仍能读取 job 可见的文件、缓存和环境，并影响同一 job 的输出。

`pull_request_target` 在默认分支上下文运行，可用于受限的标签或评论操作。这类仅处理 metadata 的 job 可以只授予完成标签或评论所需的写权限；该 job 不得检出或执行不可信 PR head。GitHub 明确警告，特权触发器结合不可信检出会带来缓存投毒、秘密泄露或写权限扩大风险。执行不可信代码的 job 与标签/评论等特权 metadata 处理必须隔离；发布、签名和部署也只在受信任的集成 SHA 或经人工批准的隔离流程中执行。self-hosted runner 还需要独立评估宿主机、网络和残留数据。

## 官方依据与下一步

- [GitHub Actions secure use reference](https://docs.github.com/en/actions/reference/security/secure-use)：最小权限、完整 SHA 固定 action、`pull_request_target` 与不可信检出的风险。
- [Events that trigger workflows](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows)：PR head SHA、merge ref 与 `merge_group` 触发条件。
- [Secret scanning](https://docs.github.com/en/code-security/concepts/secret-security/secret-scanning)：扫描范围与公开、组织私有、用户拥有仓库的可用条件。
- [Dependency review](https://docs.github.com/en/code-security/concepts/supply-chain-security/dependency-review)：依赖差异、action 和计划前提。
- [About protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)：required checks、名称歧义与 merge queue 的行为。
- [Workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax)：`permissions` 的计算顺序与 fork PR 的 write-token 例外。
- [Managing GitHub Actions settings for a repository](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository)：私有仓库 fork 的 write token、secret 和审批设置。

下一步可按仓库的实际测试入口、GitHub 计划和分支规则，把上表中的检查映射为稳定 job 名和明确的候选/集成 SHA。事故需要回退时，使用 [Agent 事故恢复](../06-troubleshooting/ai-agent-incident-recovery.md)；课程入口由 [工程变更课程入口](engineering-change-course.md) 统一组织。
