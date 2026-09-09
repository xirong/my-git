# Changelog

[English](00-meta_en/changelog_en.md) | 中文

## v2.2.0：课程、修复与 AI 协作实践

[中文发布说明](release-notes-v2.2.0.md) | [English release notes](00-meta_en/release-notes-v2.2.0_en.md)

以下内容定义 v2.2.0 的发布范围。文档准备日期为 2026-09-09；版本状态见 [GitHub Releases](https://github.com/xirong/my-git/releases)。

### 已合并的课程与修复

- [PR #67](https://github.com/xirong/my-git/pull/67) 完成十个主题的双语原理文章、交互与隔离实验，并加入[知识地图](../01-getting-started/knowledge-map.md)、[工程变更课程](../05-ai-native-development/engineering-change-course.md)、CI、后台任务、事故恢复和工程案例材料。
- [PR #68](https://github.com/xirong/my-git/pull/68) 修复恢复路径缺少创建引用、存储路径缺少输出快照的展示命令，加入直接执行四条页面命令路径的回归，并准备真实读者验收任务。
- PR #68 的合并版本 `42ae30897b09a1b9f8bb147298b0d75204448ddf` 已构建到 Pages；2026-09-08 核实线上交互脚本与修复版一致。这只说明该合并版本的部署；v2.2.0 的版本状态见 [GitHub Releases](https://github.com/xirong/my-git/releases)。

### v2.2.0 治理与协作材料

- [PR 模板](../08-templates/pull-request-template.md)和仓库实际模板记录 AI 参与、任务边界、人工核验文件与验证缺口；[提交规范](../08-templates/commit-message-convention.md)解释参与溯源与审核证据的区别。
- [Agent 治理](../04-github-engineering/ai-agent-governance.md)补充不可信任务内容、提交给 Agent 的数据，以及 Agent 指令和权限配置自身变更的三个场景；安全与 CODEOWNERS 文章提供对应入口。
- [AI 协作度量](../05-ai-native-development/ai-collaboration-metrics.md)给出统计口径、观察窗口、数据来源和可复算的模拟示例，区分等待、实际审查投入与合并前后返工；不以 AI 代码占比或 PR 数量单独判断成效。
- 中英文导航、[路线图](roadmap.md)和发布说明同步更新，历史评估原件 `2.x-ai-native-待办.md` 保持不变。

### 验收与采用边界

文档交付检查包括本地链接、禁用文本、差异检查、中英文内容核对、度量示例复算和新增平台描述的官方来源核对。检查命令见仓库 [AGENTS.md](../AGENTS.md)。这组文档检查不等于已经在团队平台配置中实施了治理规则，也不证明 Agent 提升了真实团队效率。

真实读者试读仍待参与者执行；任务与记录口径见[路线图](roadmap.md)。v2.2.0 不引入度量采集服务或看板，也不改历史版本的发布说明。

## v2.1.0

- 新增 AI Agent 治理指南。
- 新增 AGENTS.md 模板。
- 新增本仓库的 AGENTS.md 与 AI 辅助贡献规则。
- 为多 Agent 分支策略与 stacked PR 指南补充可执行流程。
- 新增 [v2.1.0 发布说明](release-notes-v2.1.0.md)。

## 早期结构记录

下面保留此前标为 Unreleased 的早期记录，避免将已建立的结构重复列成本轮新增内容；各正式版本的范围以对应发布说明为准。

- 将项目定位更新为面向现代工程团队和 AI 编程工作流的 Git / GitHub 实战手册。
- 建立第一版 v2.0 内容结构。
- 新增 AI Native 开发指南。
- 新增团队协作与 GitHub 工程治理指南。
- 新增故障处理手册。
- 新增 PR、代码审查、提交、发布、hotfix、分支和 AI 审查模板。
- 新增公司实践和参考索引。
- 新增旧内容迁移清单。
- 起草 v2.0.0 发布说明。
