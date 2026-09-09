# My Git Handbook

[English](README_en.md) | 中文

面向 AI Native 软件工程的 Git 变更控制手册：理解原理，验证改动，管理协作。

## AI 会操作，人为什么还要学？

AI 可以代劳命令，理解决定我们能看见哪些选择、提出什么问题，以及凭什么接受结果。脑中没有一个概念，遇到问题时就很难想到用它。

我维护这个仓库，是希望把 Git 中值得传承的设计讲清楚：快照如何记录状态，对象如何复用内容，引用如何组织历史，以及协作如何处理分歧。让这些思想成为人的判断依据，让 AI 帮助我们实验、执行和验证。

**学习的重心，从熟练执行，走向理解、判断与验证。** 操作仍然值得练习，尤其是读懂关键命令和识别风险；实践是检验理解的方式。

[读完整理念](01-getting-started/why-learn-git.md) · [直接打开交互学习](https://xirong.github.io/my-git/interactive/git-mental-model/)

## 从理解设计到管理协作

先用[知识地图](01-getting-started/knowledge-map.md)确认自己正在解决的是原理、一次工程变更还是团队协作，再进入下面的文章。

| 你想获得什么 | 从这里开始 | 学会后能判断什么 |
| --- | --- | --- |
| 理解设计 | [交互学习](https://xirong.github.io/my-git/interactive/git-mental-model/) → [完整学习路径](01-getting-started/git-learning-path.md) | 改动存在哪里，历史如何形成，恢复依赖什么 |
| 完成工程变更 | [一次变更的完整验收](05-ai-native-development/ai-change-control-loop.md) → [AI 变更审查样例](05-ai-native-development/ai-change-review-example.md) | 范围、提交版本和测试证据是否对应 |
| 管理协作 | [团队 Git 工作流指南](03-team-collaboration/team-git-workflow-guide.md) → [GitHub 工程治理](04-github-engineering/github-engineering-governance.md) | 如何隔离、审查、授权、发布与恢复 |

Git 提供版本与历史的基础。测试、审查、权限、制品和发布系统一起，才能形成完整的变更控制。这里既讲工具的能力，也讲它的边界。

## 适合谁

- Git 新手，希望建立正确心智模型
- 普通开发者，经常需要处理冲突、回滚、误提交
- 高级开发者，关心 PR、Review、CI、发布协作
- 技术负责人，需要设计团队 Git 工作流和 GitHub 治理规范
- AI 编程用户，需要控制 Codex、Claude Code、Cursor、Cline 等工具带来的代码变更风险

## 目录导航

| 目录 | 主要内容 |
| --- | --- |
| [01-getting-started](01-getting-started/) | Git 入门、心智模型，以及[知识地图](01-getting-started/knowledge-map.md) |
| [02-daily-workflow](02-daily-workflow/) | 日常命令、分支合并、rebase、stash、worktree |
| [03-team-collaboration](03-team-collaboration/README.md) | 团队工作流、PR、Code Review、协作模型选型 |
| [04-github-engineering](04-github-engineering/README.md) | 分支保护、Rulesets、CODEOWNERS、CI、发布、安全 |
| [05-ai-native-development](05-ai-native-development/README.md) | AI 编程下的 diff 审查、commit 拆分、worktree、多 Agent |
| [06-troubleshooting](06-troubleshooting/README.md) | Git 误操作恢复、冲突处理、secret 清理、force push 恢复 |
| [07-large-repo](07-large-repo/README.md) | 大仓库、monorepo、partial clone、sparse checkout、Git LFS |
| [08-templates](08-templates/README.md) | PR、Issue、Review、Hotfix、Release、AI Review 模板 |
| [10-company-practices](10-company-practices/README.md) | 大厂工程实践案例和决策图谱 |

## 在线交互学习

通过动画、文章和临时仓库实验理解 Git 的快照、对象图、引用、历史变化、远端、worktree 与存储。十个主题按同一顺序安排，01 至 03 对应既有交互，04 至 10 对应新增交互；材料与脚本可检查，读者理解仍需要用预测、重现和迁移来验证。

[打开 Git 心智模型交互实验](https://xirong.github.io/my-git/interactive/git-mental-model/)

[查看十个主题的文章、交互与实验导航](01-getting-started/git-learning-path.md)

## 学习路径

### 新手路径

1. [为什么在 AI 时代学习 Git](01-getting-started/why-learn-git.md)
2. [Git 心智模型](01-getting-started/git-mental-model.md)
3. [十个主题的课程导航](01-getting-started/git-learning-path.md)：每个主题都连接文章、交互和临时仓库实验。
4. [Git 基础命令](01-getting-started/git-basic-commands.md)
5. [日常 Git 命令](02-daily-workflow/everyday-git-commands.md)

### 日常开发路径

1. [分支与合并](02-daily-workflow/branch-and-merge.md)
2. [Rebase 与 Merge](02-daily-workflow/rebase-vs-merge.md)
3. [Stash](02-daily-workflow/stash.md)
4. [Worktree](02-daily-workflow/worktree.md)

### 团队协作路径

1. [团队 Git 工作流指南](03-team-collaboration/team-git-workflow-guide.md)
2. [GitLab Flow](03-team-collaboration/gitlab-flow.md)
3. [Pull Request 最佳实践](03-team-collaboration/pull-request-best-practices.md)
4. [Code Review 最佳实践](03-team-collaboration/code-review-best-practices.md)
5. [GitHub Flow](03-team-collaboration/github-flow.md)
6. [Trunk-Based Development](03-team-collaboration/trunk-based-development.md)
7. [Gitflow](03-team-collaboration/gitflow.md)

### GitHub 工程治理路径

1. [GitHub 工程治理手册](04-github-engineering/github-engineering-governance.md)
2. [企业 GitHub 协作配置栈](04-github-engineering/enterprise-github-workflow-stack.md)
3. [分支保护](04-github-engineering/branch-protection.md)
4. [Rulesets](04-github-engineering/rulesets.md)
5. [Merge Queue](04-github-engineering/merge-queue.md)
6. [GitOps and Config as Code](04-github-engineering/gitops-and-config-as-code.md)
7. [发布管理](04-github-engineering/release-management.md)
8. [AI Agent 治理](04-github-engineering/ai-agent-governance.md)

### AI Native 开发路径

1. [一次工程变更课程](05-ai-native-development/engineering-change-course.md)
2. [接受 Agent 变更](05-ai-native-development/ai-change-control-loop.md)
3. [AI 生成变更的 CI](05-ai-native-development/ci-for-ai-generated-changes.md)
4. [后台 Agent 任务](05-ai-native-development/background-agent-workflow.md)
5. [AI Native Git Workflow](05-ai-native-development/ai-native-git-workflow.md)
6. [AI 生成代码 Review](05-ai-native-development/ai-generated-code-review.md)
7. [Codex / Claude Code Git 实践](05-ai-native-development/codex-claude-code-git-practices.md)
8. [AI 编程工具的 Git 集成实践](05-ai-native-development/ai-coding-tools-git-integration.md)
9. [Worktree for AI Agents](05-ai-native-development/worktree-for-ai-agents.md)
10. [Stacked PR for AI-Generated Changes](05-ai-native-development/stacked-pr-for-ai-generated-changes.md)
11. [AI Reviewer 与 Human Reviewer](05-ai-native-development/ai-reviewer-and-human-reviewer.md)
12. [AI 协作度量](05-ai-native-development/ai-collaboration-metrics.md)

### 故障处理路径

1. [Git 高频事故处理手册](06-troubleshooting/git-troubleshooting-playbook.md)
2. [Agent 事故恢复](06-troubleshooting/ai-agent-incident-recovery.md)
3. [Undo Anything](06-troubleshooting/undo-anything.md)
4. [Recover Lost Commit](06-troubleshooting/recover-lost-commit.md)
5. [Remove Secret from History](06-troubleshooting/remove-secret-from-history.md)

## 按问题找答案

| 我现在遇到的问题 | 建议先看 |
| --- | --- |
| 刚把 commit 提交到了错误分支 | [Committed to Wrong Branch](06-troubleshooting/committed-to-wrong-branch.md) |
| reset、rebase、force push 后不知道怎么恢复 | [Git 高频事故处理手册](06-troubleshooting/git-troubleshooting-playbook.md) |
| 团队不知道该选 GitHub Flow、Gitflow 还是 Trunk-Based Development | [团队 Git 工作流指南](03-team-collaboration/team-git-workflow-guide.md) |
| PR 太大，Review 很慢 | [Pull Request 最佳实践](03-team-collaboration/pull-request-best-practices.md) |
| AI 一次改了很多文件，不知道怎么审 | [AI 变更审查实战样例](05-ai-native-development/ai-change-review-example.md) |
| AI 生成的大 diff 需要拆 commit 或拆 PR | [AI Commit Splitting](05-ai-native-development/ai-commit-splitting.md)、[Stacked PR for AI-Generated Changes](05-ai-native-development/stacked-pr-for-ai-generated-changes.md) |
| 想保护 main 分支 | [Branch Protection](04-github-engineering/branch-protection.md) |
| AI agent 开始直接提交代码、发 PR，不知道怎么管 | [AI Agent 治理](04-github-engineering/ai-agent-governance.md) |
| 想给团队仓库写一份 agent 协作约定 | [AGENTS.md 模板](08-templates/agents-md-template.md) |
| PR 很多，主分支经常被合坏 | [Merge Queue](04-github-engineering/merge-queue.md) |
| 大仓库 clone、status、checkout 很慢 | [Large Repository Git Practices](07-large-repo/large-repo-git-practices.md) |
| 想直接复制团队模板 | [Templates](08-templates/) |

## 第一阶段最值得读

- [AI Native Git Workflow](05-ai-native-development/ai-native-git-workflow.md)
- [Codex / Claude Code Git 实践](05-ai-native-development/codex-claude-code-git-practices.md)
- [AI 编程工具的 Git 集成实践](05-ai-native-development/ai-coding-tools-git-integration.md)
- [AI 变更审查实战样例](05-ai-native-development/ai-change-review-example.md)
- [Stacked PR for AI-Generated Changes](05-ai-native-development/stacked-pr-for-ai-generated-changes.md)
- [Git 高频事故处理手册](06-troubleshooting/git-troubleshooting-playbook.md)
- [团队 Git 工作流指南](03-team-collaboration/team-git-workflow-guide.md)
- [GitHub 工程治理手册](04-github-engineering/github-engineering-governance.md)
- [企业工程实践案例库](10-company-practices/README.md)
- [大厂工程实践决策图谱](10-company-practices/company-practices-decision-map.md)
- [AI 代码 Review 清单](08-templates/ai-code-review-checklist.md)

## 推荐资料来源

新内容会优先参考官方文档和业界常用资料：

- [Pro Git](https://git-scm.com/book/en/v2)
- [Git 官方文档](https://git-scm.com/docs)
- [GitHub Docs](https://docs.github.com)
- [Atlassian Git tutorials](https://www.atlassian.com/git)
- [Trunk Based Development](https://trunkbaseddevelopment.com)
- [Git Flight Rules](https://github.com/k88hudson/git-flight-rules)

更完整的资料索引见 [推荐阅读](09-resources/recommended-reading.md)。

## 版本与维护计划

详细计划见 [roadmap](00-meta/roadmap.md)。

课程、修复和协作材料已整理为 [v2.2.0 发布说明](00-meta/release-notes-v2.2.0.md)与 [Changelog](00-meta/changelog.md)。发布文档准备日期为 2026-09-09；版本状态见 [GitHub Releases](https://github.com/xirong/my-git/releases)。

已有内容会逐步纳入新的学习路径，迁移清单见 [legacy content migration](00-meta/legacy-content-migration.md)，资料索引见 [resources](09-resources/resources-index.md)。

## 项目治理

- [License](LICENSE)
- [Contributing](CONTRIBUTING.md)
- [Roadmap](ROADMAP.md)
- [Maintainers](MAINTAINERS.md)
- [Agent 协作约定](AGENTS.md)

本仓库原创内容采用 MIT License。第三方资料、历史电子书、外部文章、链接资源和引用内容仍遵循其原始许可证和版权声明。

## Contributing

欢迎贡献真实问题、团队实践、事故恢复经验、AI 编程工作流和可复用模板。

新内容请遵循 [Content Style Guide](00-meta/content-style-guide.md)。
