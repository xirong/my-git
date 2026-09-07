# Agent 事故恢复：先保全现场，再按证据处理

[English](06-troubleshooting_en/ai-agent-incident-recovery_en.md) | 中文 | [可运行实验](../labs/ai-agent-incidents/README.md)

Agent 可能在几分钟内改动许多文件、创建多个 commit，或退出时留下 worktree。恢复的第一目标是保住还能判断的证据：谁在什么位置改了什么、Git 是否已经记录内容、是否有协作者基于它继续工作。

本文处理四类事故：误删或误改、成组 commit 的撤销、Agent 退出后的 worktree，以及提交中的 `.env` 或凭据。它补充 [Git 高频事故处理手册](git-troubleshooting-playbook.md)、[Recover Lost Commit](recover-lost-commit.md) 和 [Remove Secret from History](remove-secret-from-history.md)，不重复 Git 对象、reflog 与 worktree 的完整原理。

## 事故刚发生：停止写入，分开记录四个位置

先停止会继续修改该目录的 Agent、终端命令、格式化器和生成器。不要先执行 `restore`、`clean`、`reset`、`stash` 或删除 worktree。随后在事故工作目录执行只读检查：

```bash
git status --short
git diff --name-status
git diff --cached --name-status
git ls-files --others --exclude-standard
git rev-parse --verify HEAD
git log --oneline --decorate -10
git reflog -20
```

这些输出分别帮助确认：

| 位置 | 应记录的内容 | 先别做什么 |
| --- | --- | --- |
| `HEAD` | 已提交的基线和分支指向 | 不凭记忆选 `HEAD~1` |
| Index | 已暂存、尚未提交的草稿 | 不直接取消全部暂存 |
| Working Tree | 已跟踪文件中尚未暂存的编辑 | 不对整棵目录执行 `restore` |
| untracked | Git 尚未跟踪的文件 | 不用 `clean` 批量删除 |

把命令输出、当前路径、Agent 任务标识和已知 owner 记入事故记录。文件内容还存在时，先按团队规则复制到仓库外、受保护的位置，或让 owner 在原地确认；复制动作本身也要避免覆盖已有证据。

`reflog` 记录的是引用移动等 Git 事件，可帮助找回曾经可解析的 commit。**从未保存为 Git 对象的编辑，reflog 无法恢复。** 例如 Agent 删除了只在 Working Tree 中存在、未暂存且未进入其他备份的文件，应优先查看编辑器本地历史、文件系统备份或 Agent 的可审计输出。不要把 `reflog` 有内容误读成所有未提交文本都有恢复点。

## 一组 Agent commits 要撤销：先证明范围，再选择公共或本地流程

先确定每个待处理 commit 是否确实由该 Agent 产生、它们的顺序、基线以及是否混有其他人的贡献。`<agent-base>` 和 `<agent-tip>` 必须从刚刚检查的历史中替换：

```bash
git log --oneline --decorate <agent-base>..<agent-tip>
git diff --name-status <agent-base>..<agent-tip>
git merge-base --is-ancestor <agent-base> <agent-tip>
git branch --contains <agent-tip>
git branch -r --contains <agent-tip>
```

这些命令首先提供本地 Git 证据。`git branch -r --contains` 只检查本机已有的 remote-tracking refs；空结果可能来自缓存过期、尚未 fetch、远端分支删除或改名，不能证明 commit 从未 push，也不能证明没有协作者基于它工作。判断“尚未共享”前，先确认权威 remote，按授权在合适的时间 fetch 该 remote 的 refs，并结合 PR、任务记录和协作者记录。这个文档不会自动对真实 remote 执行 fetch。

`<agent-base>..HEAD` 只有在这个区间的每个 commit 都已核实属于同一事故时才可使用。区间夹杂人工修复、其他 Agent 工作或合并 commit 时，改用已确认的 commit SHA 列表；不要为了省事把整个区间一起回退。

### 尚未共享：保留恢复指针后只移动自有分支

以下步骤只适用于干净的、Agent 独占的本地分支：待撤销 commits 从该分支的基线一直到尖端连续排列，并且已通过确认的 remote refs、PR/任务记录和协作者记录证实未共享。仅凭 `git branch -r --contains` 的空结果不满足这个条件。无法确认未共享时，按已共享处理，创建精确的 `revert` commit，不进入 `reset --hard` 流程。满足条件后，先创建恢复指针，再移动本地分支：

```bash
git status --short
git log --oneline <agent-base>..HEAD
git branch recovery/before-agent-reset HEAD
git reset --hard <agent-base>
```

`reset --hard` 会让 Index 和 Working Tree 与 `<agent-base>` 一致。因此状态里有待保留的 staged、unstaged 或 untracked 内容时，停止在命令前，保留现场或在独立 worktree 处理。`recovery/before-agent-reset` 只提供本地恢复锚点，尚未成为远端备份。

### 已共享：创建反向 commit，保留公共历史

已 push、已进 PR、已被别人 fetch 或可能作为后续工作的基线时，优先在约定分支创建 `revert` commit。按新到旧的顺序明确列出已核实的 Agent commits：

```bash
git status --short
git revert --no-edit <agent-last-sha> <agent-middle-sha> <agent-first-sha>
git log --oneline -6
git diff <agent-first-sha>^..HEAD
```

这会生成新的反向提交，已有协作者仍可沿同一历史同步。推送、PR、分支保护规则和发布处置由相应 owner 按团队权限执行。本地 `revert` 成功只证明反向补丁生成；还需要运行受影响业务的测试，并评估数据库、队列、外部调用或已发布制品是否要另行补偿。

`revert` 发生冲突表示 Git 无法机械决定怎样同时保留后续编辑和撤销目标。先查看冲突范围；决定尚未完成时，用下面的命令回到开始 revert 前的状态：

```bash
git status
git diff
git revert --abort
```

需要继续时，先由负责业务语义的 owner 明确保留哪些后续修改，再解决冲突、测试并记录实际结果。不要把冲突标记删除后直接提交，也不要用 `--no-commit` 把来源不明的额外改动混入反向提交。

## Agent 退出后遗留 worktree：先确认进程与现场

Agent 会话结束不代表该目录已经没有写入者。先保留目录，再向任务运行器、终端 owner 或已知进程记录确认是否还有 Agent、测试、编辑器 Git 操作或生成器活动。对每个 worktree 记录状态：

```bash
git worktree list --porcelain
git -C <worktree-path> status --short
git -C <worktree-path> diff --name-status
git -C <worktree-path> diff --cached --name-status
git -C <worktree-path> ls-files --others --exclude-standard
```

`git worktree list` 能列出 Git 已知的 worktree，不能证明其中没有仍在写文件的进程。发现未知编辑或进程时，保留目录、分支名和上述输出，交由对应 owner 处理。

### lock、prune 与 remove 的边界

| 命令或状态 | 用途 | 事故中的判断 |
| --- | --- | --- |
| `git worktree lock <path>` | 标记该 worktree 的管理记录，避免暂时不可见的目录被 `prune` 当成陈旧记录清理 | 需要等待 owner、可移动磁盘暂时离线时可用；记录原因和责任人 |
| `git worktree unlock <path>` | 解除上述保护 | 只在已确认目录和编辑无需继续保留后执行 |
| `git worktree prune` | 清理已不存在目录的陈旧管理记录 | 它不检查丢失目录里原有未提交编辑是否曾被保留；先完成现场确认 |
| `git worktree remove <path>` | 移除 linked worktree 目录和关联记录 | 只用于已确认干净且不再需要的目录；普通模式会做安全检查 |

不要手工删除 `.git/worktrees/.../locked`，也不要用 `git worktree remove --force` 绕过未提交编辑或锁的保护。前者会让管理记录与真实目录脱节；后者可能让待保留编辑失去原始位置。目录被手工移动或确实删除后，只有确认其分支、未提交内容和 owner 都不再需要，才执行 `git worktree prune`。

更多关于共享对象、独立 HEAD 与 Index 的事实见 [Worktree for AI Agents](../05-ai-native-development/worktree-for-ai-agents.md) 和 [Git 心智模型 09：Worktree](../01-getting-started/git-mental-model-09-worktree.md)。

## `.env` 或 secret 已进 commit：先让凭据失效

凭据进入 commit、PR、日志或制品时，优先顺序如下：

1. 通过凭据发行方禁用、撤销或轮换该凭据，并确认新凭据未沿用旧权限。
2. 限制继续传播：停止使用泄露凭据的自动化，记录已知 commit、远端、分支、tag、PR、制品和日志位置。
3. 通知安全与仓库 owner，按影响范围查看访问记录、fork、缓存和下游系统。
4. 再按已授权范围处理 Git 历史和平台扫描结果。

`git revert` 只能让新的分支尖端不再包含该文本。历史重写也不能收回已经被 clone、转存、缓存、日志记录或截屏的秘密。详细的远端范围确认、`git filter-repo` 与协作者同步见 [Remove Secret from History](remove-secret-from-history.md)；仓库内预防措施见 [Security and Secret Scanning](../04-github-engineering/security-and-secret-scanning.md)。

不要在事故记录、终端输出或截图中再次粘贴完整凭据。可以记录凭据类型、发行方、失效时间、关联的 commit SHA 和处理 owner，使后续复查有证据又不扩大泄露范围。

## 可运行实验与下一步

[Agent 事故恢复实验](../labs/ai-agent-incidents/README.md) 在带标记的临时目录中执行真实 Git 操作，覆盖：

- 自有且未共享的一组 commits 在恢复分支保留后被本地回退；
- 推送到实验本地 bare remote 的两条 Agent commits 被按已核实 SHA 反向提交，夹在中间的人工 commit 保留；
- `git revert` 冲突后执行 `git revert --abort`，回到冲突前的提交与文件内容；
- 脏 worktree 被普通 `remove` 拒绝，lock 保护的陈旧记录不会被 `prune` 清掉，解锁后才可清理记录。

实验不接触本仓库的 Git 历史，不演练真实 secret，也不证明 GitHub 平台、外部备份或生产数据已经恢复。需要把 Agent 变更的候选 SHA、业务测试和合并结果连到 CI 时，继续阅读 [AI 生成变更的 CI](../05-ai-native-development/ci-for-ai-generated-changes.md)。

## 延伸阅读

- [Git 高频事故处理手册](git-troubleshooting-playbook.md)
- [Recover Lost Commit](recover-lost-commit.md)
- [Undo Anything](undo-anything.md)
- [Remove Secret from History](remove-secret-from-history.md)
- [AI 变更审查实战样例](../05-ai-native-development/ai-change-review-example.md)
- [工程变更课程入口](../05-ai-native-development/engineering-change-course.md)
- [git worktree 官方文档](https://git-scm.com/docs/git-worktree)
- [git revert 官方文档](https://git-scm.com/docs/git-revert)
