# AGENTS.md 模板

AGENTS.md 是给 AI coding agent 看的项目说明文件，一个开放格式，Codex、GitHub Copilot cloud agent、Devin、Cursor、Aider、Gemini CLI 等工具都会读取。README 写给人看，AGENTS.md 写给 agent 看：环境怎么搭、改完跑什么验证、哪些地方不能动。

Claude Code 读取的是 CLAUDE.md，内容结构相同，两份可以互相引用，避免维护两套规则。

## 放置位置

- 仓库根目录放一份
- monorepo 可以在子项目目录再放一份，agent 一般优先读取离改动文件最近的那份

## 模板

```markdown
# AGENTS.md

## 项目概览

一句话说清这个仓库做什么、技术栈、服务边界。

## 环境准备

- 安装依赖: `pnpm install`
- 启动本地服务: `pnpm dev`

## 改动后必须验证

- 单元测试: `pnpm test`
- 类型检查: `pnpm typecheck`
- 代码检查: `pnpm lint`

任何改动至少跑一次相关模块的测试，改公共模块时跑全量。

## 代码风格

- TypeScript strict 模式
- 与所在文件保持一致的命名和注释密度
- 引入新依赖前，先确认仓库里是否已有同类依赖

## 仓库结构

- `src/api/`: 对外接口层
- `src/service/`: 业务逻辑
- `src/infra/`: 数据访问与外部依赖

## 边界约定

禁止以下操作:

- 修改 `.github/workflows/` 下的 CI 配置
- 修改数据库 migration 历史文件
- 删除或改写已有测试断言来让测试通过
- force push 到任何共享分支
- 把 `.env`、密钥、token 写进任何文件

## 提交与 PR 约定

- 分支命名: `ai/task-<topic>`
- commit 格式: `<type>(<scope>): <subject>`
- AI 参与的提交加 trailer: `Co-authored-by: <tool> <email>`
- PR 描述写明: 任务边界、人工检查过的文件、验证命令和结果
```

## 写作建议

- 写可执行命令，少写散文。agent 对“请保持代码整洁”无能为力，对 `pnpm lint` 能直接执行
- 约束写成允许和禁止两张清单，越具体越有效
- 验证命令和 CI 保持一致，agent 在本地跑的就是 CI 要跑的
- 定期修剪。过时的指令会持续误导 agent，比没有指令更糟
- 篇幅控制在一两屏内，agent 每次会话都要读它，太长会稀释关键约束

## 和各工具配置文件的对应

| 工具 | 读取文件 |
| --- | --- |
| Codex、Devin、Cursor、Aider、Gemini CLI 等 | `AGENTS.md` |
| Claude Code | `CLAUDE.md`，可在其中引用 AGENTS.md |
| GitHub Copilot | `AGENTS.md`，也支持 `.github/copilot-instructions.md` |

工具支持范围以 [agents.md](https://agents.md) 官方列表为准。

## 延伸阅读

- [agents.md 官方说明](https://agents.md)
- [本仓库的 AGENTS.md 实例](../AGENTS.md)
- [Codex / Claude Code Git 实践](../05-ai-native-development/codex-claude-code-git-practices.md)
- [AI Agent 治理](../04-github-engineering/ai-agent-governance.md)
