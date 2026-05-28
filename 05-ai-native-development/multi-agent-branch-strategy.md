# Multi-Agent Branch Strategy

多 Agent 并行开发时，核心是隔离任务、明确归属、最后由人类做整合。

## 分支命名

```text
ai/task-parser-refactor
ai/task-api-test
ai/review-parser-refactor
```

## 推荐流程

1. 每个 Agent 一个分支
2. 每个分支一个明确任务
3. 每个分支独立提交和验证
4. 人类选择需要保留的方案
5. 合并前重新整理 commit

## 避免

- 多个 Agent 写同一个工作区
- 多个 Agent 同时改同一组文件
- 让 Agent 自行合并公共分支
- 没看 diff 就接受结果

## 推荐命名

```text
ai/experiment-parser-a
ai/experiment-parser-b
ai/review-parser-a
```

实验分支合入前，建议整理成正常业务分支：

```text
feat/parser-error-handling
fix/parser-empty-input
```

## 延伸阅读

- [git worktree](https://git-scm.com/docs/git-worktree)
- [Worktree for AI Agents](worktree-for-ai-agents.md)
- [AI Native Git Workflow](ai-native-git-workflow.md)
- [推荐阅读索引](../09-resources/recommended-reading.md)
