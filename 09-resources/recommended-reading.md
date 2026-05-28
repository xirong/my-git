# 推荐阅读

这个页面用于沉淀后续写作时参考过的官方文档、经典文章和知名资料。

原则：

- 优先官方文档和一手来源
- 再选择业界长期引用的经典资料
- 中文文章可以补充，但不要替代官方口径
- 新文章写完后，把参考资料挂到文末，方便读者继续深挖

## Git 基础与心智模型

| 资料 | 适合补充到哪里 | 说明 |
| --- | --- | --- |
| [Pro Git](https://git-scm.com/book/en/v2) | `01-getting-started/`、`02-daily-workflow/` | Git 官方站点推荐的系统学习资料 |
| [Git 官方文档](https://git-scm.com/docs) | 所有命令类文章 | 命令行为以官方文档为准 |
| [Git Cheat Sheet](https://git-scm.com/cheat-sheet.pdf) | `01-getting-started/git-basic-commands.md` | 适合做命令速查 |
| [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) | `02-daily-workflow/commit-message.md` | commit message 规范的常用参考 |
| [How to Write a Git Commit Message](https://cbea.ms/git-commit/) | `02-daily-workflow/commit-message.md` | 经典 commit message 写作文章 |

## 团队工作流

| 资料 | 适合补充到哪里 | 说明 |
| --- | --- | --- |
| [Atlassian Git tutorials](https://www.atlassian.com/git) | `03-team-collaboration/` | 覆盖集中式、Feature Branch、Gitflow、Forking、Pull Request 等工作流 |
| [GitHub Flow](https://docs.github.com/en/get-started/using-github/github-flow) | `03-team-collaboration/github-flow.md` | GitHub 官方轻量分支工作流 |
| [GitHub Flow 企业化实践](../10-company-practices/github-flow-enterprise.md) | `03-team-collaboration/github-flow.md`、`04-github-engineering/enterprise-github-workflow-stack.md` | GitHub Flow 如何配合平台治理能力升级为企业协作链路 |
| [GitLab Flow](../03-team-collaboration/gitlab-flow.md) | `03-team-collaboration/team-git-workflow-guide.md` | 适合需要 production / stable 分支的团队 |
| [Trunk Based Development](https://trunkbaseddevelopment.com) | `03-team-collaboration/trunk-based-development.md` | 主干开发、短分支、feature flag 的经典资料 |
| [Feature Flags](https://trunkbaseddevelopment.com/feature-flags/) | `03-team-collaboration/trunk-based-development.md` | 主干开发中隔离未完成能力的关键实践 |
| [A successful Git branching model](https://nvie.com/posts/a-successful-git-branching-model/) | `03-team-collaboration/gitflow.md` | Gitflow 的经典原文 |
| [Google Engineering Practices: Code Review](https://google.github.io/eng-practices/review/) | `03-team-collaboration/code-review-best-practices.md` | Google 公开的代码审查实践 |
| [Google Code Review 实践](../10-company-practices/google-code-review.md) | `03-team-collaboration/code-review-best-practices.md` | Review 标准、长期 code health、评论分级 |
| [阿里巴巴 AoneFlow 分支管理实践](../10-company-practices/alibaba-aoneflow.md) | `03-team-collaboration/team-git-workflow-guide.md`、`03-team-collaboration/gitflow.md` | 多 feature 并行、按发布范围组合 release 分支 |
| [腾讯云社区 Gitflow 分支规范实践](../10-company-practices/tencent-gitflow.md) | `03-team-collaboration/gitflow.md` | Gitflow 风格团队规范参考 |
| [字节跳动 Git 工作流与研发设施实践](../10-company-practices/bytedance-git-workflow.md) | `03-team-collaboration/team-git-workflow-guide.md`、`04-github-engineering/` | 大规模研发设施如何承接 Git 工作流 |
| [Google 主干开发与版本控制实践](../10-company-practices/google-trunk-based-development.md) | `03-team-collaboration/trunk-based-development.md` | 主干开发、大规模协作、小变更与快速 CI |
| [Microsoft Release Flow](../10-company-practices/microsoft-release-flow.md) | `03-team-collaboration/team-git-workflow-guide.md`、`04-github-engineering/release-management.md` | 主干开发配合 release 分支的团队实践 |

## GitHub 工程治理

| 资料 | 适合补充到哪里 | 说明 |
| --- | --- | --- |
| [Protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches) | `04-github-engineering/branch-protection.md` | 分支保护、必需检查、Review、Merge Queue |
| [Rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets) | `04-github-engineering/rulesets.md` | 仓库和组织级规则治理 |
| [Issue and pull request templates](https://docs.github.com/communities/using-templates-to-encourage-useful-issues-and-pull-requests/about-issue-and-pull-request-templates) | `.github/`、`08-templates/` | 标准化社区贡献信息 |
| [Pull request reviews](https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/about-pull-request-reviews) | `03-team-collaboration/code-review-best-practices.md` | PR Review、CODEOWNERS 自动请求 Review |
| [Secret scanning](https://docs.github.com/github/administering-a-repository/about-secret-scanning) | `04-github-engineering/security-and-secret-scanning.md` | 凭证扫描和泄露告警 |
| [Push protection](https://docs.github.com/code-security/secret-scanning/protecting-pushes-with-secret-scanning) | `04-github-engineering/security-and-secret-scanning.md` | 在 push 阶段拦截 secret |
| [GitHub Actions Docs](https://docs.github.com/en/actions) | `04-github-engineering/github-actions-ci.md` | GitHub Actions 官方文档 |
| [Reusable workflows](https://docs.github.com/en/actions/how-tos/reuse-automations/reuse-workflows) | `04-github-engineering/reusable-workflows.md` | 多仓库复用 CI 模板 |
| [Gerrit Access Controls](https://gerrit-review.googlesource.com/Documentation/access-control.html) | `09-resources/gerrit-code-review-governance.md` | Gerrit 权限、label、Submit 模型 |
| [Managing releases in a repository](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository) | `04-github-engineering/release-management.md` | GitHub Release 官方文档 |
| [Semantic Versioning](https://semver.org/) | `04-github-engineering/release-management.md` | 语义化版本规范 |
| [Merge Queue 合并队列实践](../10-company-practices/merge-queue-practices.md) | `04-github-engineering/merge-queue.md` | PR 高并发团队如何保护主分支稳定 |
| [Shopify Merge Queue 实践](../10-company-practices/shopify-merge-queue.md) | `04-github-engineering/merge-queue.md` | 大规模团队使用合并队列保护主分支的经验 |
| [企业 GitHub 协作配置栈](../04-github-engineering/enterprise-github-workflow-stack.md) | `04-github-engineering/` | GitHub Flow、CODEOWNERS、Rulesets、Actions、安全扫描、Merge Queue 的组合方案 |
| [GitOps and Config as Code](../04-github-engineering/gitops-and-config-as-code.md) | `04-github-engineering/github-engineering-governance.md` | 配置、基础设施和发布策略如何进入 PR、Review、CI 链路 |
| [Slack Deploys 实践](../10-company-practices/slack-deploys.md) | `04-github-engineering/release-management.md` | 高频部署团队如何降低日常发布风险 |

## 工程经验研究

| 资料 | 适合补充到哪里 | 说明 |
| --- | --- | --- |
| [Do Small Code Changes Merge Faster?](https://arxiv.org/abs/2203.05045) | `03-team-collaboration/pull-request-best-practices.md` | 小变更和合并耗时关系的经验研究 |
| [The Impact of a Continuous Integration Service on the Delivery Time of Merged Pull Requests](https://arxiv.org/abs/2305.16365) | `04-github-engineering/github-actions-ci.md` | CI 对合并决策、交付时间和开发者信心的研究 |
| [Git 工作流经验研究笔记](empirical-git-workflow-research.md) | `03-team-collaboration/`、`04-github-engineering/` | 把研究结论转成写作边界 |

## AI 编程与代码审查

| 资料 | 适合补充到哪里 | 说明 |
| --- | --- | --- |
| [Responsible use of GitHub Copilot code review](https://docs.github.com/en/copilot/responsible-use/code-review) | `05-ai-native-development/ai-generated-code-review.md` | GitHub 对 AI Review 能力边界的官方说明 |
| [Review AI-generated code](https://docs.github.com/en/enterprise-cloud@latest/copilot/tutorials/review-ai-generated-code) | `05-ai-native-development/ai-generated-code-review.md` | 面向 AI 生成代码审查流程的官方教程 |
| [OpenAI Codex](https://openai.com/codex/) | `05-ai-native-development/codex-claude-code-git-practices.md` | Codex 官方产品页，包含 multi-agent workflows 和 worktrees 说明 |
| [OpenAI Codex Web](https://developers.openai.com/codex/cloud) | `05-ai-native-development/ai-coding-tools-git-integration.md` | Codex Web、GitHub 集成和远程任务入口 |
| [OpenAI Codex Sandboxing](https://developers.openai.com/codex/concepts/sandboxing) | `05-ai-native-development/ai-coding-tools-git-integration.md` | Codex sandbox 与权限模型 |
| [Claude Code Worktrees](https://code.claude.com/docs/en/worktrees) | `05-ai-native-development/codex-claude-code-git-practices.md` | Claude Code 官方 worktree 并行会话说明 |
| [Claude Code Common Workflows](https://code.claude.com/docs/en/common-workflows) | `05-ai-native-development/codex-claude-code-git-practices.md` | Claude Code 官方常见工作流 |
| [GitHub Copilot Cloud Agent](https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-cloud-agent) | `05-ai-native-development/ai-coding-tools-git-integration.md` | Issue 到 PR 的异步 Agent 工作流 |
| [Aider Git Integration](https://aider.chat/docs/git.html) | `05-ai-native-development/ai-coding-tools-git-integration.md` | git-first 本地 AI 结对实践 |
| [Cursor 2.0 and Composer](https://cursor.com/blog/2-0) | `05-ai-native-development/ai-coding-tools-git-integration.md` | 多 Agent、Composer 和聚合 diff 入口 |
| [AI 变更审查实战样例](../05-ai-native-development/ai-change-review-example.md) | `05-ai-native-development/ai-native-git-workflow.md`、`05-ai-native-development/ai-generated-code-review.md` | AI diff 审查、清理、拆 commit、写 PR 的完整示例 |
| [Stacked PR for AI-Generated Changes](../05-ai-native-development/stacked-pr-for-ai-generated-changes.md) | `05-ai-native-development/ai-native-git-workflow.md`、`05-ai-native-development/ai-commit-splitting.md` | AI 大 diff 如何拆成可审查的小 PR |

## 开源项目治理

| 资料 | 适合补充到哪里 | 说明 |
| --- | --- | --- |
| [Kubernetes OWNERS Files](https://www.kubernetes.dev/docs/guide/owners/) | `04-github-engineering/codeowners.md`、`03-team-collaboration/code-review-best-practices.md` | OWNERS、reviewer / approver 两阶段评审 |
| [Kubernetes Pull Request Process](https://www.kubernetes.dev/docs/guide/pull-requests/) | `03-team-collaboration/pull-request-best-practices.md` | PR 流程、自动化检查和维护者协作 |
| [Linux Kernel Pull Requests](https://docs.kernel.org/maintainer/pull-requests.html) | `09-resources/open-source-governance-practices.md` | 维护者树状模型和 pull request 规范 |
| [Go Contribution Guide](https://go.dev/doc/contribute) | `09-resources/open-source-governance-practices.md` | Gerrit、Review 权限和贡献流程 |
| [Rust RFCs](https://github.com/rust-lang/rfcs) | `09-resources/open-source-governance-practices.md` | 重大变更 RFC 模型 |

## 故障处理与恢复

| 资料 | 适合补充到哪里 | 说明 |
| --- | --- | --- |
| [Git Flight Rules](https://github.com/k88hudson/git-flight-rules) | `06-troubleshooting/` | Git 高频事故处理清单 |
| [git reflog](https://git-scm.com/docs/git-reflog.html) | `06-troubleshooting/recover-lost-commit.md` | 恢复丢失 commit 的核心命令 |
| [git restore](https://git-scm.com/docs/git-restore.html) | `06-troubleshooting/undo-anything.md` | 撤销工作区和暂存区改动 |
| [How to undo almost anything with Git](https://github.blog/open-source/git/how-to-undo-almost-anything-with-git/) | `06-troubleshooting/undo-anything.md` | GitHub 经典撤销指南 |
| [Removing sensitive data from a repository](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository) | `06-troubleshooting/remove-secret-from-history.md` | GitHub 官方敏感数据清理说明 |
| [git filter-repo](https://github.com/newren/git-filter-repo) | `06-troubleshooting/remove-secret-from-history.md` | 清理 Git 历史的常用工具 |

## 大仓库与 Monorepo

| 资料 | 适合补充到哪里 | 说明 |
| --- | --- | --- |
| [Partial clone](https://git-scm.com/docs/partial-clone.html) | `07-large-repo/partial-clone.md` | 减少对象下载 |
| [Sparse checkout](https://git-scm.com/docs/sparse-checkout) | `07-large-repo/sparse-checkout.md` | 只保留部分工作区路径 |
| [git worktree](https://git-scm.com/docs/git-worktree) | `02-daily-workflow/worktree.md`、`05-ai-native-development/worktree-for-ai-agents.md` | 多分支并行工作区 |
| [Git LFS](https://git-lfs.com) | `07-large-repo/git-lfs.md` | Git 大文件管理工具 |
| [Pro Git: Submodules](https://git-scm.com/book/en/v2/Git-Tools-Submodules) | `07-large-repo/submodule-vs-subtree.md` | submodule 系统说明 |
| [git maintenance](https://git-scm.com/docs/git-maintenance) | `07-large-repo/repo-maintenance.md` | 仓库维护命令 |
| [Microsoft Scalar 与大仓库 Git 实践](../10-company-practices/microsoft-scalar-large-repo.md) | `07-large-repo/large-repo-git-practices.md` | partial clone、sparse checkout、maintenance 的组合实践 |
| [Meta Sapling 与堆叠提交实践](../10-company-practices/meta-sapling-stacked-commits.md) | `03-team-collaboration/pull-request-best-practices.md`、`07-large-repo/` | 堆叠提交和超大仓库开发体验 |
| [Uber GitFarm 与 Git 服务化实践](../10-company-practices/uber-gitfarm.md) | `07-large-repo/large-repo-git-practices.md` | Git 作为大规模 monorepo 基础设施服务 |
| [Git 版本演进笔记](git-version-upgrade-notes.md) | `07-large-repo/large-repo-git-practices.md`、`09-resources/` | Git 2.45 到 2.54 中值得工程团队关注的能力 |
