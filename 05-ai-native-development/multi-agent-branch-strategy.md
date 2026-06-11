# Multi-Agent Branch Strategy

多 Agent 并行开发时，核心是隔离任务、明确归属、最后由人类做整合。

## 分支命名

```text
ai/task-parser-refactor      # 单一明确任务
ai/experiment-parser-a       # 同一问题的方案 A
ai/experiment-parser-b       # 同一问题的方案 B
ai/review-parser-refactor    # 给 Review 用的整理分支
```

实验分支合入前，整理成正常业务分支：

```text
feat/parser-error-handling
fix/parser-empty-input
```

## 推荐流程

1. 每个 Agent 一个分支，配合 worktree 一个分支一个目录
2. 每个分支一个明确任务，边界按目录或模块切分
3. 每个分支独立提交和验证
4. 人类对比结果，选择保留的方案
5. 合并前整理 commit，实验分支重命名为业务分支

## 对比多个实验分支

两个 Agent 各自做了一版方案，先分别看每个分支相对主线改了什么：

```bash
git log --oneline main..ai/experiment-parser-a
git diff main...ai/experiment-parser-a    # 三个点：只看分支自己的改动
git diff main...ai/experiment-parser-b
```

再直接对比两个方案：

```bash
git diff ai/experiment-parser-a..ai/experiment-parser-b
git range-diff main ai/experiment-parser-a ai/experiment-parser-b
```

`git range-diff` 按 commit 对齐两个分支，适合两个方案结构接近时逐个提交看差异。

对比不能只看 diff。两个分支用同样的命令各跑一遍测试，把结果记进任务说明或 PR 描述，作为选型依据。

## 整合胜出方案

方案 A 整体胜出时，把它整理成业务分支：

```bash
git switch -c feat/parser-error-handling ai/experiment-parser-a
git rebase main
```

只需要方案 B 里的局部成果时，按 commit 捡：

```bash
git cherry-pick <commit-sha>
```

或者按文件捡：

```bash
git restore --source ai/experiment-parser-b -- src/parser/recover.ts
git add src/parser/recover.ts
git commit
```

## 两个 Agent 改了同一个文件

预防优先：切分任务时就避免两个 Agent 的范围重叠，路由表、依赖清单、公共配置这类文件尽量只让一个任务碰。

真撞上时按顺序处理：

1. 先合入其中一个分支
2. 另一个分支 rebase 到最新主线：`git rebase main`
3. 冲突由人决策。可以让 Agent 解释两边各自的意图，最终采用哪边由人决定
4. 解完冲突重新跑该分支的验证，再进 Review

## 清理落选分支

```bash
# 需要保留现场时，先打归档 tag
git tag archive/ai-experiment-parser-b ai/experiment-parser-b

# 删除本地分支和对应 worktree
git branch -D ai/experiment-parser-b
git worktree remove ../wt-parser-b

# 推送过远端的话，同时删除远端分支
git push origin --delete ai/experiment-parser-b
```

落选分支对应的 draft PR 关闭时写明落选原因，下次做同类任务时有据可查。

## 避免

- 多个 Agent 写同一个工作区
- 多个 Agent 同时改同一组文件
- 让 Agent 自行合并公共分支
- 没看 diff 就接受结果
- 实验分支长期不清理，仓库里堆满 `ai/` 死分支

## 延伸阅读

- [git worktree](https://git-scm.com/docs/git-worktree)
- [git range-diff](https://git-scm.com/docs/git-range-diff)
- [Worktree for AI Agents](worktree-for-ai-agents.md)
- [AI Native Git Workflow](ai-native-git-workflow.md)
- [AI Agent 治理](../04-github-engineering/ai-agent-governance.md)
- [推荐阅读索引](../09-resources/recommended-reading.md)
