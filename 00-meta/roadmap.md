# Roadmap

v2.0 的目标是补齐现代工程团队在 Git / GitHub 协作、AI 编程、事故处理和工程治理上的实战内容。

## v2.2.0：理解、实验、变更控制与 AI 协作实践

仓库用[理念文章](../01-getting-started/why-learn-git.md)说明维护动机，并用[学习路径](../01-getting-started/git-learning-path.md)连接十个主题的中英文文章、交互和临时仓库实验。现有目录继续作为资料索引，读者不必按文件夹编号学习。v2.2.0 的范围见[发布说明](release-notes-v2.2.0.md)，文档准备日期为 2026-09-09；版本状态见 [GitHub Releases](https://github.com/xirong/my-git/releases)。

### 已合并材料

- [x] 新增[知识地图](../01-getting-started/knowledge-map.md)，按“理解设计 → 完成工程变更 → 管理协作”说明前置知识、问题入口和下一项判断。
- [x] 明确[工具集成实践](../05-ai-native-development/ai-coding-tools-git-integration.md)负责工具事实与来源，[Codex / Claude Code Git 实践](../05-ai-native-development/codex-claude-code-git-practices.md)负责跨工具的稳定 Git 流程。
- [x] 新增[工程变更课程](../05-ai-native-development/engineering-change-course.md)、[AI 生成变更的 CI](../05-ai-native-development/ci-for-ai-generated-changes.md)、[后台 Agent 任务](../05-ai-native-development/background-agent-workflow.md)和[Agent 事故恢复](../06-troubleshooting/ai-agent-incident-recovery.md)，分别连接验收链、检查版本、异步交接和事故现场。
- [x] 新增[两个 AI Agent 工程案例](../10-company-practices/ai-native-engineering-cases.md)，将第一手公开报告与团队本地试点判断分开。

上述材料已通过 [PR #67](https://github.com/xirong/my-git/pull/67) 合并；展示命令修复与回归通过 [PR #68](https://github.com/xirong/my-git/pull/68) 合并，两次 PR 的文档与链接 CI 均通过。2026-09-08 核实，GitHub Pages 构建版本为 `42ae30897b09a1b9f8bb147298b0d75204448ddf`，线上交互脚本与修复版一致。这个结果只覆盖该合并版本，也不证明真实读者掌握了课程。

### 收尾与后续待办

- [x] 修复恢复分支缺少创建引用、存储分支缺少输出快照的问题；`node scripts/test-curriculum-commands.mjs` 直接执行四条展示命令路径，并独立核对对象状态和快照内容。对旧源的定向检查可捕获缺少引用与快照的原错误。
- [x] 通过 PR #68 合并修复，并核对 Pages 实际部署版本。
- [ ] 完成一次真实读者试读，按下面的任务记录结果。
- [x] 整理 [v2.2.0 发布说明](release-notes-v2.2.0.md)与双语 Changelog，明确课程、修复、治理模板和度量文章的发布范围。

### v2.2.0 内容补齐

这些条目用于验收 v2.2.0 文档范围，合并与部署状态需要单独核对。

- [x] [PR 模板](../08-templates/pull-request-template.md)、仓库实际模板和[提交规范](../08-templates/commit-message-convention.md)提供 AI 参与、任务边界、真实人工核验、验证缺口与溯源写法。
- [x] [Agent 治理](../04-github-engineering/ai-agent-governance.md)补齐不可信输入、提交给 Agent 的数据、Agent 规则自身变更三个场景，并从安全与 CODEOWNERS 文章交叉引用。
- [x] [AI 协作度量](../05-ai-native-development/ai-collaboration-metrics.md)给出定义、分母、观察窗口、数据来源和可复算的模拟示例，区分等待、实际投入及合并前后返工。
- [x] [双语 Changelog](changelog.md)和[发布说明](release-notes-v2.2.0.md)整理 PR #67 / #68 的已合并记录、治理模板与度量文章，并链接 GitHub Releases 查看版本状态。

历史评估中的 Agent 治理、AGENTS.md 模板、仓库自身约定、多 Agent 与 stacked PR 操作、事故恢复、CI、后台任务、工程案例和工具文章职责已覆盖。原始评估保留不变，新的工作以这里的具体缺口为准。

### 真实读者验收任务

邀请一位未参与编写的工程师，从[知识地图](../01-getting-started/knowledge-map.md)进入课程。主持人先不解释答案，只记录读者的预测、实际操作、提示次数和卡住位置；所有 Git 操作仅在课程创建的可删除实验仓库中执行。

1. 在恢复章节中，先预测 C2 与 C3 在 reflog 过期和清理后的结果，再执行实验，用引用和对象检查解释差异。
2. 在存储章节中，执行维护前后内容比较，说明“内容不变”可以证明什么，以及为什么不能据此断言性能提升。
3. 迁移到一个 Agent 场景：Agent 修改了已提交文件、未暂存文件和外部数据库。分别说明需要保存哪些证据、Git 能恢复什么、哪些状态需另行处理。
4. 从文章进入交互和实验，再切换语言，记录失效链接、术语障碍和需要额外帮助的位置。

每项记录“独立完成 / 提示后完成 / 未完成”，附预测与实际结果的差异；单次试读只说明该参与者在该版本上的表现。尚未安排参与者，不能把自动测试或 Agent 模拟读者计为试读通过。

### 材料和证据边界

| 代码与材料可见 | 覆盖范围 | 仍需单独取得的证据 |
| --- | --- | --- |
| 01 至 10 的十篇中英文原理文章、十个实验和十个交互入口按同一顺序链接 | 快照、对象、Index、引用、恢复、合并、rebase、远端、worktree 与存储 | 读者实际能否预测、重现和迁移，还没有行为数据 |
| 交互入口保留 01 至 03 的三个既有主题，并补入 04 至 10 的七个主题 | 每个主题可从文章跳转交互和实验；上述合并版本的部署已核实 | 全路径浏览器行为、后续修复部署与真实读者体验需要分别验证 |
| [工程变更课程](../05-ai-native-development/engineering-change-course.md)与[完整验收链](../05-ai-native-development/ai-change-control-loop.md)配有本地制品与 HTTP 服务实验 | 任务意图、候选 commit、干净检出测试、制品、回环地址运行结果和代码恢复可在临时根目录中观察 | 它不连接真实 CI、托管平台、生产环境或外部服务，也不构成供应链证明 |
| [命令安全回归](../labs/git-command-safety/README.md)复核四种已列出的旧命令模式 | 脏工作区停手、完整路径提交、soft reset 后再部分暂存、集成分支占位符 | 未列出的历史示例、远端授权、分支保护、hooks 和团队规则不在这组回归范围内 |
| `bash scripts/run-git-learning-labs.sh` 串行运行十个课程实验、三个阅读实验和三项 Agent/命令回归入口 | 可重复检查脚本描述的本地 Git 场景，包括 Agent 事故恢复实验 | 运行通过不能代替读者学习效果、性能基准或生产状态证据 |

### 课程顺序与验证

1. **01 至 03：快照、对象、Index。** 先观察一次编辑怎样分别出现在 HEAD、Index 和 Working Tree，再进入对象图和提交草稿。
2. **04 至 05：引用与恢复。** branch、tag、HEAD 之后是可达性、reflog 与 GC 的恢复期限。
3. **06 至 09：历史与协作。** 三方合并、rebase 重放、远端跟踪引用和 worktree 依次解释分歧、整合与隔离。
4. **10：存储与维护。** 在对象模型之后区分逻辑快照、pack、GC 和 commit-graph，实验只观察受控临时仓库，性能结论仍需要单独测量。
5. **Agent 变更验收。** 用本地制品与服务实验连接提交、测试和运行证据，并保留 Git 无法自动恢复外部状态的边界。

### 每章的教学合同

一条因果问题、一幅稳定画布、一个可改变的条件、一份临时仓库实验、一组预期输出、一种误解和恢复边界，以及一个 Agent 场景的判断题。动画只有在能解释变化时才运动；时间、计数和哈希必须注明真实或示意。

学习验收包含三件事：能预测、能重现、能迁移。读者看完觉得“炫酷”是体验反馈，不能单独证明掌握。

### 仍需维护的边界

- Git 不保存所有工程状态：忽略文件、secrets、LFS 对象、子模块、数据库、依赖来源和环境需要分别处理。
- 内容哈希、身份签名、CI 结果、业务正确性是不同证据，避免混为可信度评分。
- 多 Agent 的瓶颈可能在集成与审查容量，不能只增加并行数。
- 图解的简化条件、键盘操作、减少动态效果和无 JavaScript 阅读，需要持续维护。
- 工具接入说明单独维护日期与来源，稳定原理不依赖某个产品的按钮位置。

## v2.0 目标

v2.0 先做一件事：建立清晰的内容结构，并完成第一批能直接使用的核心文章和模板。

## 第一阶段：30 天版本

### Week 1：定位升级

- [x] 更新 README
- [x] 新增主入口说明
- [x] 建立新目录结构
- [x] 新增内容风格规范
- [x] 新增 GitHub Issue / PR 模板
- [x] 梳理旧文件迁移清单

### Week 2：AI 差异化

- [x] 新增 `ai-native-git-workflow.md`
- [x] 新增 `ai-generated-code-review.md`
- [x] 新增 `codex-claude-code-git-practices.md`
- [x] 新增 AI 代码 Review 模板
- [x] 新增 `worktree-for-ai-agents.md`
- [x] 新增 `ai-commit-splitting.md`
- [x] 新增 `multi-agent-branch-strategy.md`

### Week 3：团队工程实践

- [x] 新增 `team-git-workflow-guide.md`
- [x] 新增 `github-engineering-governance.md`
- [x] 新增 PR 和 Review 模板
- [x] 新增 `branch-protection.md` 完整版
- [x] 新增 `release-management.md`
- [x] 新增 `codeowners.md`

### Week 4：事故手册和发布

- [x] 新增 `git-troubleshooting-playbook.md`
- [x] 新增 `undo-anything.md`
- [x] 新增 `recover-lost-commit.md`
- [x] 新增 `remove-secret-from-history.md`
- [x] 全仓库链接校验
- [x] `v2.0.0` release notes 文件已纳入仓库

## v2.1.0：Agent 治理与协作约定

v2.1.0 把 AI agent 当作仓库里的正式参与者来覆盖，补齐治理和约定层。

- [x] 新增 `ai-agent-governance.md`，覆盖 bot 身份、权限、PR 审批、CI 触发、secrets 隔离
- [x] 新增 AGENTS.md 模板，供团队仓库直接复制
- [x] 本仓库落地自己的 AGENTS.md，贡献指南补充 AI 贡献规则
- [x] `multi-agent-branch-strategy.md` 补齐对比、整合、清理的可执行流程
- [x] `stacked-pr-for-ai-generated-changes.md` 补齐原生 git 命令和栈管理工具

## 内容原则

1. 少堆链接，多讲判断
2. 少列命令，多讲场景
3. 少追求大而全，多给可执行路径
4. 每篇文章都要能回答“什么情况该用，什么情况别用”

## v2.0 Release 叙事

AI 编程正在改变软件开发方式，Git 的价值也随之变化。

v2.0 会围绕团队协作、GitHub 工程治理、AI 代码审查、事故恢复和大仓库实践，系统补齐 Git / GitHub 实战内容。

## 近期优化清单

- [x] README 增加按问题找答案
- [x] 新增 AI 变更审查实战样例
- [x] 新增旧内容迁移清单
- [x] 补齐 `07-large-repo/` 的实战决策表
- [x] 核对 `v2.0.0` release notes 文件已存在
