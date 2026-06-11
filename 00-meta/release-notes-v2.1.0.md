# v2.1.0: AI Agent 治理与协作约定

这个版本把 AI agent 当作仓库里的正式参与者来覆盖：怎么治理它们，怎么给它们写约定。

## Highlights

- 新增 [AI Agent 治理指南](https://github.com/xirong/my-git/blob/v2.1.0/04-github-engineering/ai-agent-governance.md)，覆盖 agent 的三种身份形态、权限收紧、PR 审批规则、CI 触发与 secrets 隔离、可追溯性，托管 agent 的内置限制以 GitHub 官方文档为依据
- 新增 [AGENTS.md 模板](https://github.com/xirong/my-git/blob/v2.1.0/08-templates/agents-md-template.md)，可直接复制到团队仓库，含环境命令、验证要求、边界禁令、提交约定，并附各工具配置文件对照表
- 本仓库开始遵循自己倡导的约定：根目录新增 [AGENTS.md](https://github.com/xirong/my-git/blob/v2.1.0/AGENTS.md)，贡献指南补充 AI 辅助贡献规则，文档检查覆盖 AGENTS.md
- [Multi-Agent Branch Strategy](https://github.com/xirong/my-git/blob/v2.1.0/05-ai-native-development/multi-agent-branch-strategy.md) 补齐可执行流程：对比实验分支、整合胜出方案、同文件冲突处理、清理落选分支
- [Stacked PR for AI-Generated Changes](https://github.com/xirong/my-git/blob/v2.1.0/05-ai-native-development/stacked-pr-for-ai-generated-changes.md) 补齐原生 git 栈操作（`--update-refs`、`rebase --onto`、`--force-with-lease`）和 Graphite CLI 核心命令
- 以上内容均为中英双语成对维护

## 为什么发这个版本

v2.0 确立了面向 AI 编程时代的方向，但 agent 治理和协作约定还是空白。

AI agent 已经在创建分支、发起 PR、触发 CI，v2.1.0 把它们从"diff 生成器"升级为"被治理的参与者"：管理者有了治理配置清单，团队有了可复制的 AGENTS.md 模板，开发者有了多 Agent 并行和栈式 PR 的实操命令。

## Validation

- `python3 scripts/check-docs.py`
- `python3 scripts/check-links.py --no-external`
- `git diff --check`
