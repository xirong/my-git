# 知识地图：从理解设计到管理协作

[English](01-getting-started_en/knowledge-map_en.md) | 中文

这张地图用于选择阅读路径和下一步决策，不替代命令手册，也不重复十个 Git 原理主题的课程顺序。先判断自己处在哪一层，再进入对应文章。

## 三层路径

| 层次 | 需要的前置理解 | 这层负责回答的问题 | 从哪里开始 | 下一步要作出的判断 |
| --- | --- | --- | --- | --- |
| 理解设计 | 愿意在临时仓库中观察一次编辑、暂存和提交 | Git 到底记录了什么，历史怎样形成，什么状态可恢复 | [为什么在 AI 时代学习 Git](why-learn-git.md) → [Git 心智模型](git-mental-model.md) → [十个主题学习路径](git-learning-path.md) | 能否说清一次变更在 Working Tree、Index、HEAD 和远端各自的状态？能，进入工程变更；不能，回到对应实验。 |
| 完成工程变更 | 能区分工作区、Index 与已提交版本，并会在发现已有编辑时保留现场 | 怎样把一个明确任务变成范围清楚、证据对应、可以恢复的变更 | [一次工程变更课程](../05-ai-native-development/engineering-change-course.md) → [接受 Agent 变更](../05-ai-native-development/ai-change-control-loop.md) → [AI 生成变更的 CI](../05-ai-native-development/ci-for-ai-generated-changes.md) | 这次变更能否独立审查，测试和 CI 是否对应候选或集成提交，出错时代码与外部副作用各如何处理？ |
| 管理协作 | 每个变更已能说明任务边界、验证证据和恢复范围 | 团队该选什么协作模型，哪些规则可以落实，案例能否迁移 | [团队 Git 工作流指南](../03-team-collaboration/team-git-workflow-guide.md) → [GitHub 工程治理](../04-github-engineering/github-engineering-governance.md) → [模板库](../08-templates/README.md) → [工程实践决策图谱](../10-company-practices/company-practices-decision-map.md) | 分支寿命、审批责任、必需检查、发布与恢复由谁定义，规则怎样在仓库和平台中执行？ |

Git 的概念学习、一次变更的验收和团队规则彼此相连，但不能互相替代。通过十章实验不等于某次业务变更已经验证；本地测试通过也不等于团队的权限、发布和外部状态已经确认。

## 关键文章各自负责什么

| 文章或入口 | 负责的问题 | 读完后去哪里 |
| --- | --- | --- |
| [为什么在 AI 时代学习 Git](why-learn-git.md) | 人为什么仍要理解 Git，以及人和工具各自承担什么判断 | 进入[Git 心智模型](git-mental-model.md)，建立状态、对象和引用的因果解释。 |
| [Git 心智模型](git-mental-model.md) | 用四区域快速模型进入十个主题，解释 Git 的底层关系 | 按[学习路径](git-learning-path.md)预测、观察并重现具体行为。 |
| [Git 学习路径](git-learning-path.md) | 十个原理主题的文章、交互和实验顺序 | 在能预测行为后，带着一个真实小任务进入工程变更路径。 |
| [一次工程变更课程](../05-ai-native-development/engineering-change-course.md) | 用一个任务契约贯穿隔离、候选提交、审查、CI、制品、运行和恢复 | 再读[接受 Agent 变更](../05-ai-native-development/ai-change-control-loop.md)补足证据字段，或按风险进入 CI、后台任务和事故恢复。 |
| [接受 Agent 变更](../05-ai-native-development/ai-change-control-loop.md) | 把意图、候选提交、测试、制品和运行证据连成一次可检查的练习 | 用[AI 变更审查样例](../05-ai-native-development/ai-change-review-example.md)练习针对 diff 作出接受或退回决定。 |
| [AI 生成变更的 CI](../05-ai-native-development/ci-for-ai-generated-changes.md) | 把检查绑定到候选或集成版本，并按变更类型选择业务测试 | 核对实际仓库的工作流、权限、secrets 和必需检查，再作合入决定。 |
| [后台 Agent 任务](../05-ai-native-development/background-agent-workflow.md) | 任务从发出到回收需要哪些版本、范围、权限和证据 | 接收人核对 candidate SHA 后作接受、返工、拒绝或过期决定；案例迁移时阅读[两个 AI Agent 工程案例](../10-company-practices/ai-native-engineering-cases.md)。 |
| [AI 编程工具的 Git 集成实践](../05-ai-native-development/ai-coding-tools-git-integration.md) | 记录工具能力、官方来源和需要随产品更新复核的接入差异 | 确定工具形态后，按[Codex / Claude Code Git 实践](../05-ai-native-development/codex-claude-code-git-practices.md)执行稳定的 Git 习惯。 |
| [Codex / Claude Code Git 实践](../05-ai-native-development/codex-claude-code-git-practices.md) | 用分支或 worktree 隔离任务，审查 diff，组织提交并保留人工合入责任 | 需要多人协作时，进入[团队工作流](../03-team-collaboration/team-git-workflow-guide.md)和[GitHub 工程治理](../04-github-engineering/github-engineering-governance.md)。 |
| [团队 Git 工作流指南](../03-team-collaboration/team-git-workflow-guide.md) | 按团队约束选择分支和集成模型 | 将决定落实到[GitHub 工程治理](../04-github-engineering/github-engineering-governance.md)与可复制的[模板](../08-templates/README.md)。 |
| [Agent 事故恢复](../06-troubleshooting/ai-agent-incident-recovery.md) | Agent 误改、遗留 worktree、错误 commit 或泄露凭据时先保全什么现场 | 按共享状态处理代码恢复与业务补偿，再回到工程变更路径补足范围、审查和验证。 |

## 按眼前问题选择

| 你现在需要决定什么 | 先读 | 接着检查 |
| --- | --- | --- |
| 一条命令会改动哪份状态 | [Git 心智模型](git-mental-model.md) | 用学习路径中的临时仓库实验复现。 |
| Agent 说“完成了”，我该接受吗 | [一次工程变更课程](../05-ai-native-development/engineering-change-course.md) | 提交范围、验证版本、制品和运行证据是否能对应。 |
| 后台任务返回得很晚或重复运行，怎样接收 | [后台 Agent 任务](../05-ai-native-development/background-agent-workflow.md) | 任务 ID、base、candidate、目标 ref、证据和接受责任是否一致。 |
| 多个任务同时改仓库，怎么避免互相覆盖 | [Codex / Claude Code Git 实践](../05-ai-native-development/codex-claude-code-git-practices.md) | worktree 或分支是否隔离，谁负责集成和清理。 |
| Agent 误改、删除或留下未知 worktree，先做什么 | [Agent 事故恢复](../06-troubleshooting/ai-agent-incident-recovery.md) | 现场、提交范围、共享状态和 Git 外部影响是否已经分开记录。 |
| 团队该使用 GitHub Flow、Gitflow 还是主干开发 | [团队 Git 工作流指南](../03-team-collaboration/team-git-workflow-guide.md) | 发布节奏、集成频率、CI 能力和回滚成本。 |
| 引入 Agent 后，审查与返工是否改善 | [AI 协作度量](../05-ai-native-development/ai-collaboration-metrics.md) | 等待与实际投入、合并前后返工、观察窗口和任务差异是否分开统计。 |
| 一项公开案例能否照搬 | [两个 AI Agent 工程案例](../10-company-practices/ai-native-engineering-cases.md) | 来源是作者自报还是独立证据，你的团队约束是否与案例前提一致。 |

命令、事故案例和模板都是执行辅助。需要它们时从本页进入相应层次，再回到这张地图作下一项决策。
