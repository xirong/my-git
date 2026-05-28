# GitLab Flow

原文链接：

- [What is GitLab Flow?](https://about.gitlab.com/topics/version-control/what-is-gitlab-flow/)
- [GitLab Flow](https://docs.gitlab.com/topics/gitlab_flow/)

GitLab Flow 介于 GitHub Flow 和 Gitflow 之间。

它保留 feature branch 和 merge request 的轻量协作方式，同时引入 production branch、stable branch 等概念，适合需要环境分支、生产分支或版本稳定分支的团队。

## 解决什么问题

GitHub Flow 很轻，适合主分支随时可发布的团队。

Gitflow 分支角色完整，但对很多 Web / SaaS 团队太重。

GitLab Flow 适合中间地带：

- 日常开发仍然走 feature branch
- 合入前通过 merge request Review
- 生产部署可以绑定 production branch
- 多版本交付可以使用 stable branch
- Issue、MR、环境和发布记录可以串起来

## 常见形态

### Production branch

```text
feature/* -> main -> production
```

`main` 接收日常集成，`production` 表示已经发布到生产的状态。

适合：

- 生产发布频率低于合入频率
- 需要明确区分“已合入”和“已上线”
- 发布过程需要额外验证

### Stable branch

```text
main -> stable/1.0
main -> stable/1.1
```

stable 分支表示需要长期维护的版本线。

适合：

- 客户端
- SDK
- 企业交付产品
- 私有化部署

## 和其他模型的区别

| 模型 | 核心特点 |
| --- | --- |
| GitHub Flow | 最轻，围绕默认分支和 PR |
| GitLab Flow | 在轻量 MR 流程上补 production / stable 分支 |
| Gitflow | 分支角色最完整，流程也最重 |
| Trunk-Based Development | 强调围绕主干高频集成，短分支和快速验证 |

## 适合什么团队

适合：

- 发布频率和合入频率不同
- 需要生产分支表达线上事实
- 有多环境部署
- 有多个稳定版本线
- 不想采用完整 Gitflow

不适合：

- 小团队快速发布
- 主分支已经可以随时部署
- 团队没有明确环境分支需求

## 落地建议

1. 先明确 `main` 和 `production` 的语义
2. 所有变更仍然通过 MR / PR
3. production 分支只接收经过验证的变更
4. stable 分支只接收对应版本修复
5. 发布后用 tag 和 release note 记录版本
6. hotfix 必须同步回主线，避免修复丢失

## 延伸阅读

- [GitLab Flow](https://docs.gitlab.com/topics/gitlab_flow/)
- [团队 Git 工作流指南](team-git-workflow-guide.md)
- [Release Management](../04-github-engineering/release-management.md)
