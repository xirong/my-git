# Git 学习路径：从理解到判断

[English](01-getting-started_en/git-learning-path_en.md) | 中文

先读[为什么在 AI 时代学习 Git](why-learn-git.md)，再沿“理解设计 → 验证判断 → 管理变更”前进。命令可以随用随查；每一段都要能解释行为，并预测条件改变后的结果。

本页只编排十个 Git 原理主题的学习顺序。需要在原理学习、一次工程变更和团队协作之间选择路径时，使用[知识地图](knowledge-map.md)。

## 第一部分：理解 Git 的设计

下面是十个主题的统一顺序。每个主题都有中英文文章、一个交互页和一个可运行的临时仓库实验；从 01 到 03 是既有交互主题，04 到 10 是本轮补入的七个主题。材料和脚本可供检查，读者是否掌握仍需要预测、重现和迁移的实际证据。

| 顺序 | 要回答的问题 | 文章、交互与实验 | 判断练习 |
| --- | --- | --- | --- |
| 01 快照与状态 | 编辑、暂存、提交分别记录什么？ | [文章](git-mental-model-01-snapshots.md) · [交互](../interactive/git-mental-model/snapshots-and-state.html) · [实验](../labs/git-mental-model/01-snapshots-and-state/README.md) | add 后再次编辑，commit 记录哪个版本？ |
| 02 对象图 | commit、tree、blob 各负责什么？ | [文章](git-mental-model-02-object-graph.md) · [交互](../interactive/git-mental-model/object-graph.html) · [实验](../labs/git-mental-model/02-object-graph/README.md) | 为什么两个路径可以指向同一个 blob？ |
| 03 Index | 下一次提交的草稿是什么？ | [文章](git-mental-model-03-index.md) · [交互](../interactive/git-mental-model/index-as-draft.html) · [实验](../labs/git-mental-model/03-index/README.md) | 如何提交一个文件中的部分修改？ |
| 04 引用与 HEAD | branch、tag、HEAD、detached HEAD 如何关联？ | [文章](git-mental-model-04-refs.md) · [交互](../interactive/git-mental-model/refs-and-head.html) · [实验](../labs/git-mental-model/04-refs/README.md) | 分支名移动时，原 commit 会改变吗？ |
| 05 可达性与恢复 | 没有名字的提交还能找回吗？ | [文章](git-mental-model-05-recovery.md) · [交互](../interactive/git-mental-model/reachability-and-recovery.html) · [实验](../labs/git-mental-model/05-recovery/README.md) | reflog 为什么不能当永久备份？ |
| 06 合并与共同祖先 | Git 如何理解两条历史的分歧？ | [文章](git-mental-model-06-merge.md) · [交互](../interactive/git-mental-model/three-way-merge.html) · [实验](../labs/git-mental-model/06-merge/README.md) | 没有文本冲突，行为就一定兼容吗？ |
| 07 重放与历史重写 | rebase 为何产生新的 commit？ | [文章](git-mental-model-07-rebase.md) · [交互](../interactive/git-mental-model/rebase-and-replay.html) · [实验](../labs/git-mental-model/07-rebase/README.md) | 为什么共享历史上的重写需要协调？ |
| 08 远端与同步 | origin/main 和远端 main 有何区别？ | [文章](git-mental-model-08-remote.md) · [交互](../interactive/git-mental-model/remote-and-fetch.html) · [实验](../labs/git-mental-model/08-remote/README.md) | fetch 后，本地工作文件一定变了吗？ |
| 09 worktree 与并行 | 哪些状态共享，哪些状态隔离？ | [文章](git-mental-model-09-worktree.md) · [交互](../interactive/git-mental-model/worktree-and-isolation.html) · [实验](../labs/git-mental-model/09-worktree/README.md) | 两个 Agent 各有分支，为何还可能互相干扰？ |
| 10 存储与维护 | 逻辑快照怎样存得下、查得快？ | [文章](git-mental-model-10-storage.md) · [交互](../interactive/git-mental-model/storage-and-maintenance.html) · [实验](../labs/git-mental-model/10-storage/README.md) | 对象图的连线等同于磁盘上的布局吗？ |

维护者可运行 `bash scripts/run-git-learning-labs.sh` 回归十个实验、三项既有阅读实验、一次本地 Agent 变更验收实验和一次命令安全回归。它只验证脚本描述的临时本地场景，不能测量读者学习效果，也不能证明生产环境状态。

每章按这个顺序练习：先猜结果，操控动画，读完整文章，在临时仓库重现，再改变一个条件重试。恢复能力安排在历史重写前，避免先学危险操作再补救。

## 第二部分：把原理用于一次真实变更

从[一次工程变更课程](../05-ai-native-development/engineering-change-course.md)开始，用一个小修复贯穿任务契约、候选提交、CI、运行证据和恢复：

1. 写清期望行为和不允许改动的范围。
2. 识别已有编辑，安排分支与工作目录。
3. 用 Index 选择要接受的变化，检查 diff。
4. 记录并验证具体提交，核对测试覆盖。
5. 形成审查决定，确认实际发布版本。
6. 解释代码恢复与业务补偿的边界。

继续阅读：[接受 Agent 变更](../05-ai-native-development/ai-change-control-loop.md)、[AI 生成变更的 CI](../05-ai-native-development/ci-for-ai-generated-changes.md)、[AI 变更审查样例](../05-ai-native-development/ai-change-review-example.md)、[AI Commit Splitting](../05-ai-native-development/ai-commit-splitting.md)、[Agent 事故恢复](../06-troubleshooting/ai-agent-incident-recovery.md)。

可用这个问题自查：当 Agent 说“完成了”，能否指出提交范围、验证证据，以及尚未验证的部分？

## 第三部分：把个人判断变成团队机制

按约束选方案，不必把所有工作流同时引入团队：

| 约束 | 继续阅读 | 需要作出的判断 |
| --- | --- | --- |
| 团队需要统一协作方式 | [团队工作流](../03-team-collaboration/team-git-workflow-guide.md) | 集成频率、分支寿命、责任如何分配？ |
| 后台或并行 Agent 带来集成压力 | [后台 Agent 任务](../05-ai-native-development/background-agent-workflow.md) → [多 Agent 分支策略](../05-ai-native-development/multi-agent-branch-strategy.md) | 每个结果怎样回收，隔离后的成果怎样比较、验证和整合？ |
| 改动之间有依赖 | [Stacked PR](../05-ai-native-development/stacked-pr-for-ai-generated-changes.md) | 下层变化后，上层证据是否需要更新？ |
| 接受变更需要规则 | [GitHub 工程治理](../04-github-engineering/github-engineering-governance.md) | 哪些权限、检查和审批能真正执行？ |
| 发布有外部副作用 | [发布管理](../04-github-engineering/release-management.md) | 提交、制品、环境和业务结果如何对应？ |

最后再读[两个 AI Agent 工程案例](../10-company-practices/ai-native-engineering-cases.md)和[企业工程案例](../10-company-practices/README.md)，比较来源、约束与取舍。公开报告提供经验，团队仍要用自己的仓库和验证结果判断适用性。

## 按需使用的参考资料

- [Git 基础命令](git-basic-commands.md)：遇到操作时查阅。
- [故障处理手册](../06-troubleshooting/git-troubleshooting-playbook.md)：先判断现场与风险。
- [模板](../08-templates/README.md)：理解目的之后再复制。
- [内容建设路线图](../00-meta/roadmap.md)：查看尚未补齐的课程与验收标准。
