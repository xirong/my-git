# AI Agent 治理

当 AI agent 开始创建分支、提交代码、发起 PR，仓库里就多了一类新的参与者。治理对象从人扩展到 agent，原有的分支保护、Review 规则、CI 策略需要重新检查一遍。

这篇回答五个问题：

1. agent 用什么身份提交代码
2. agent 的权限怎么收紧
3. agent 发起的 PR 谁来批准
4. agent 怎么触发 CI，secrets 怎么隔离
5. 出了问题怎么追溯到具体的 agent 会话

## Agent 的三种身份形态

### 1. 人类账号在本地运行工具

Claude Code、Codex CLI、Aider 在开发者本机运行，提交以开发者本人身份出现。

治理重点：

- 提交信息里标注工具参与，推荐 `Co-authored-by` trailer
- 开发者对自己账号推出去的所有代码负全责
- 团队规则写进 AGENTS.md，让每个人的 agent 都遵守同一套边界

```text
fix(order): handle empty timeout config

Co-authored-by: Claude <noreply@anthropic.com>
```

### 2. 平台托管 agent

GitHub Copilot cloud agent、Codex cloud 这类 agent 运行在平台沙箱里，以独立的 bot 身份提交。

以 Copilot cloud agent 为例，GitHub 内置了这些限制（来源见文末官方文档）：

- 只有对仓库有 write 权限的人能触发 agent，无权限用户的评论不会传给 agent
- agent 只能 push 到自己的 `copilot/` 分支，同样受分支保护和必需检查约束
- agent 发起的 PR 是 draft，agent 自己不能标记 ready、不能 approve、不能 merge
- 发起任务的人不能批准这个 PR，Required approvals 的控制不会被绕过
- 默认情况下，有 write 权限的人点击 Approve and run workflows 之后，Actions 才会运行

治理重点：先确认这些默认限制没有被放宽，再决定哪些仓库开放给托管 agent。

### 3. 自建自动化里的 agent

团队在 GitHub Actions 或内部平台里自己跑 agent，身份通常是 GitHub App 或 machine user。

治理重点：

- 优先用 GitHub App，权限可以精确到仓库和能力，避免个人 PAT
- 一个用途一个身份，方便审计和回收
- token 用 fine-grained 类型，只授需要的仓库

## 权限设计

核心原则：agent 拿到的权限按它要完成的任务给，按最小集合给。

- 写权限只开到专属分支前缀。用 Rulesets 的分支命名限制，约定 agent 只能推 `ai/**` 或 `copilot/**`
- 不给 agent 任何 bypass。Rulesets 的 bypass 名单里不应该出现 agent 身份
- 不给 agent 管理员权限，不让 agent 修改仓库设置、webhook、Actions 配置
- 高风险目录用 CODEOWNERS 兜底，owner 必须是人

## PR 审批规则

- agent 发起的 PR 必须有人类 approve，开启 Require approvals
- 发起任务的人和批准的人分开。托管 agent 平台一般内置了这条，自建 agent 要靠流程约定补上
- 高风险路径开启 Require review from Code Owners
- AI review 工具的结论只作为参考输入，批准动作必须由人完成

## CI 触发与 secrets 隔离

agent 提交的代码进入 CI 运行时，等于这段代码拿到了 CI 环境的执行权。三个控制点：

- 保持先人工批准、再跑 workflow 的默认行为，公开仓库尤其要保持
- 部署类 secrets 放进 environment，配置 required reviewers，agent 的分支拿不到
- 慎用 `pull_request_target`，它会让外部分支的代码在带 secrets 的上下文里运行

托管 agent 的运行环境默认有防火墙限制出网，放宽前先确认要访问的域名清单。

## 可追溯性

出问题时要能回答：这段代码来自谁的 agent、哪次会话、谁发起的。

- 提交署名要能区分人和 agent。托管 agent 的提交由 bot 署名、发起人作为 co-author，提交带签名
- 本地工具的提交统一加 `Co-authored-by` trailer
- commit message 里保留任务或会话链接
- 平台的 session log 和 audit log 保留备查

## 最小落地配置

小团队第一步只需要四件事：

1. 约定 agent 分支前缀，写进 AGENTS.md 和分支命名规范
2. 主分支开启 Require a pull request before merging 和 Require approvals
3. 约定提交 trailer 标注 AI 参与
4. 部署 secrets 移入 environment

成长期团队再补：

- 用 Rulesets 统一多仓库的 agent 分支规则
- CODEOWNERS 覆盖高风险目录
- 自建 agent 换成 GitHub App 身份
- 定期审计 agent 身份的权限和活跃度

## 常见误区

### 1. 给 agent 和人一样的权限

agent 不需要 admin，不需要 bypass，不需要访问所有仓库。权限给大了，审计时分不清是人还是 agent 在操作。

### 2. 所有 agent 共用一个 token

共享 token 意味着无法追责、无法单独回收。一个用途一个身份。

### 3. 把 AI review 当成人工批准

AI review 可以先扫一遍，但 Required approvals 必须由人完成。

### 4. agent 分支没有命名约定

没有统一前缀，审计、清理、Rulesets 限制都做不了。

## 延伸阅读

- [GitHub Docs: Risks and mitigations for Copilot cloud agent](https://docs.github.com/en/copilot/concepts/agents/cloud-agent/risks-and-mitigations)
- [Rulesets](rulesets.md)
- [Branch Protection](branch-protection.md)
- [CODEOWNERS](codeowners.md)
- [AGENTS.md 模板](../08-templates/agents-md-template.md)
- [AI Reviewer 与 Human Reviewer](../05-ai-native-development/ai-reviewer-and-human-reviewer.md)
