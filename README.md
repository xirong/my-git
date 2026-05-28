# My Git Handbook

面向现代工程团队与 AI 编程时代的 Git / GitHub 实战手册。

## 为什么维护这个仓库

这个仓库最早是 Git 学习资料合集，帮助很多中文开发者入门 Git。

但今天继续只做“资料导航”，价值已经不够了。Git 的核心问题，已经从“命令怎么用”扩展到这些更真实的问题：

1. 个人开发者如何理解 Git 的心智模型
2. 日常开发中如何处理冲突、回滚、误提交
3. 团队如何选择合适的分支和 PR 工作流
4. 技术负责人如何用 GitHub 建立工程协作规范
5. AI 编程时代，如何审查、拆分、验证和回滚 AI 生成的代码变更

所以 v2.0 会把这个仓库升级为：

> 一个面向现代工程团队与 AI 编程时代的 Git / GitHub 实战手册。

## 适合谁

- Git 新手，希望建立正确心智模型
- 普通开发者，经常需要处理冲突、回滚、误提交
- 高级开发者，关心 PR、Review、CI、发布协作
- 技术负责人，需要设计团队 Git 工作流和 GitHub 治理规范
- AI 编程用户，需要控制 Codex、Claude Code、Cursor、Cline 等工具带来的代码变更风险

## 学习路径

### 新手路径

1. [为什么使用 Git](why-git.md)
2. [Git 心智模型](01-getting-started/git-mental-model.md)
3. [Git 基础命令](01-getting-started/git-basic-commands.md)
4. [日常 Git 命令](02-daily-workflow/everyday-git-commands.md)

### 日常开发路径

1. [分支与合并](02-daily-workflow/branch-and-merge.md)
2. [Rebase 与 Merge](02-daily-workflow/rebase-vs-merge.md)
3. [Stash](02-daily-workflow/stash.md)
4. [Worktree](02-daily-workflow/worktree.md)

### 团队协作路径

1. [团队 Git 工作流指南](03-team-collaboration/team-git-workflow-guide.md)
2. [Pull Request 最佳实践](03-team-collaboration/pull-request-best-practices.md)
3. [Code Review 最佳实践](03-team-collaboration/code-review-best-practices.md)
4. [经典 Git 工作流教程](git-workflow-tutorial.md)

### GitHub 工程治理路径

1. [GitHub 工程治理手册](04-github-engineering/github-engineering-governance.md)
2. [分支保护](04-github-engineering/branch-protection.md)
3. [Rulesets](04-github-engineering/rulesets.md)
4. [发布管理](04-github-engineering/release-management.md)

### AI Native 开发路径

1. [AI Native Git Workflow](05-ai-native-development/ai-native-git-workflow.md)
2. [AI 生成代码 Review](05-ai-native-development/ai-generated-code-review.md)
3. [Codex / Claude Code Git 实践](05-ai-native-development/codex-claude-code-git-practices.md)
4. [AI 编程工具的 Git 集成实践](05-ai-native-development/ai-coding-tools-git-integration.md)
5. [Worktree for AI Agents](05-ai-native-development/worktree-for-ai-agents.md)
6. [AI Reviewer 与 Human Reviewer](05-ai-native-development/ai-reviewer-and-human-reviewer.md)

### 故障处理路径

1. [Git 高频事故处理手册](06-troubleshooting/git-troubleshooting-playbook.md)
2. [Undo Anything](06-troubleshooting/undo-anything.md)
3. [Recover Lost Commit](06-troubleshooting/recover-lost-commit.md)
4. [Remove Secret from History](06-troubleshooting/remove-secret-from-history.md)

## 第一阶段最值得读

- [AI Native Git Workflow](05-ai-native-development/ai-native-git-workflow.md)
- [Codex / Claude Code Git 实践](05-ai-native-development/codex-claude-code-git-practices.md)
- [AI 编程工具的 Git 集成实践](05-ai-native-development/ai-coding-tools-git-integration.md)
- [Git 高频事故处理手册](06-troubleshooting/git-troubleshooting-playbook.md)
- [团队 Git 工作流指南](03-team-collaboration/team-git-workflow-guide.md)
- [GitHub 工程治理手册](04-github-engineering/github-engineering-governance.md)
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

## v2.0 维护计划

详细计划见 [roadmap](00-meta/roadmap.md)。

已有内容会逐步纳入新的学习路径，资料索引见 [resources](09-resources/resources-index.md)。

## Contributing

欢迎贡献真实问题、团队实践、事故恢复经验、AI 编程工作流和可复用模板。

新内容请遵循 [Content Style Guide](00-meta/content-style-guide.md)。
