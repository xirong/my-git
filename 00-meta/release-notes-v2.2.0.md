# v2.2.0：Git 学习、命令修复与 AI 协作实践

中文 | [English](00-meta_en/release-notes-v2.2.0_en.md) | [更新记录](changelog.md)

本文定义已获授权的 v2.2.0 发布范围。文档准备日期为 2026-09-09；版本状态见 [GitHub Releases](https://github.com/xirong/my-git/releases)。

## Highlights

- [PR #67](https://github.com/xirong/my-git/pull/67) 完成十个主题的双语 Git 心智模型文章、交互与可删除实验仓库，并补入知识地图、工程变更课程、AI 生成变更的 CI、后台 Agent 任务、Agent 事故恢复和工程案例。
- [PR #68](https://github.com/xirong/my-git/pull/68) 修复恢复路径缺少创建引用、存储路径缺少输出快照的展示命令；新增回归会执行四条页面命令路径，并分别核对对象状态和快照内容。
- 更新 [PR 模板](../08-templates/pull-request-template.md)、仓库实际模板和[提交规范](../08-templates/commit-message-convention.md)，记录 AI 参与、任务边界、人工核验文件、验证缺口与提交溯源。
- 更新 [Agent 治理](../04-github-engineering/ai-agent-governance.md)，覆盖不可信任务内容、提交给 Agent 的数据，以及会改变 Agent 行为的指令和权限配置；安全与 CODEOWNERS 文章提供对应入口。
- 新增 [AI 协作度量](../05-ai-native-development/ai-collaboration-metrics.md)，说明统计口径、观察窗口、数据来源和可复算的模拟示例，区分等待、实际审查投入与合并前后返工。
- 同步中英文导航、路线图、更新记录和本发布说明。

## 为什么纳入 v2.2.0

v2.1.0 建立了 Agent 治理和协作约定。v2.2.0 将这些约定连接到可操作的学习材料、命令回归、可填写的协作模板和可复算的度量示例，帮助团队分别判断课程理解、变更证据与协作结果。

## 验收与证据边界

- 文档检查覆盖 `python3 scripts/check-docs.py`、`python3 scripts/check-links.py --no-external` 和 `git diff --check`。
- PR #67 和 PR #68 已合并；2026-09-08 已核实 PR #68 合并版本 `42ae30897b09a1b9f8bb147298b0d75204448ddf` 的 Pages 构建与线上交互脚本一致。该事实只覆盖该合并版本。
- 真实读者试读仍待执行，任务与记录口径见[路线图](roadmap.md)。自动文档检查、命令回归和 Agent 模拟读者不能证明读者掌握课程，也不能证明团队效率提升。
- 本版本不引入度量采集服务或看板。团队是否采用治理规则、平台实际配置和真实协作效果需要各团队单独取得证据。
