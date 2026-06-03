# 模板库

[English](08-templates_en/README_en.md) | 中文

这个目录提供可以复制到团队仓库里的模板。模板的目标是降低沟通成本，让 PR、Review、发布、hotfix、AI 代码审查都有固定信息结构。

## 推荐组合

| 团队阶段 | 建议先用 |
| --- | --- |
| 个人项目 | [Commit Message Convention](commit-message-convention.md)、[Branch Naming Convention](branch-naming-convention.md) |
| 小团队 | [Pull Request Template](pull-request-template.md)、[Code Review Checklist](code-review-checklist.md) |
| 成长期团队 | PR 模板、Review 清单、Issue 模板、Release Note |
| 有生产发布压力的团队 | [Hotfix Process](hotfix-process.md)、[Release Note Template](release-note-template.md) |
| AI 编程团队 | [AI Code Review Checklist](ai-code-review-checklist.md)、PR 模板、commit message 规范 |

## 模板列表

- [Pull Request Template](pull-request-template.md)
- [Code Review Checklist](code-review-checklist.md)
- [AI Code Review Checklist](ai-code-review-checklist.md)
- [Commit Message Convention](commit-message-convention.md)
- [Branch Naming Convention](branch-naming-convention.md)
- [Release Note Template](release-note-template.md)
- [Hotfix Process](hotfix-process.md)
- [Issue Template Bug](issue-template-bug.md)
- [Issue Template Feature](issue-template-feature.md)

## 如何使用

可以把模板复制到团队仓库的 `.github/` 目录中：

```text
.github/
  PULL_REQUEST_TEMPLATE.md
  ISSUE_TEMPLATE/
    bug_report.md
    feature_request.md
```

如果团队已经有模板，建议只补缺失字段，不要一次替换所有流程。

## AI 编程团队建议

PR 模板里至少补充：

- AI 工具名称
- 人类给 AI 的任务边界
- 人类实际检查过的文件和 diff
- 验证命令和结果
- 回滚方案

## 相关内容

- [AI Native Development](../05-ai-native-development/README.md)
- [GitHub 工程治理](../04-github-engineering/README.md)
- [团队协作](../03-team-collaboration/README.md)
