# 故障处理

[English](06-troubleshooting_en/README_en.md) | 中文

这个目录用于处理 Git 高频事故。先判断状态，再选择恢复方案，不要一上来复制危险命令。

## 先回答三个问题

1. 代码是否已经提交
2. commit 是否已经 push
3. 是否已经有人基于这些 commit 继续开发

这三个答案决定了能不能改写历史、应该用 revert 还是 reset、是否需要先和团队确认。

## 按状态选方案

| 当前状态 | 推荐入口 |
| --- | --- |
| 代码还没提交 | [Undo Anything](undo-anything.md) |
| 已提交，还没 push | [Git 高频事故处理手册](git-troubleshooting-playbook.md) |
| 已 push | [Git 高频事故处理手册](git-troubleshooting-playbook.md)、[Revert Merge Commit](revert-merge-commit.md) |
| 已被别人基于它开发 | [Git 高频事故处理手册](git-troubleshooting-playbook.md) |
| secret 已经提交 | [Remove Secret from History](remove-secret-from-history.md) |
| force push 覆盖远端 | [Recover Force Push](recover-force-push.md) |

## 急救入口

| 我现在遇到的问题 | 建议阅读 |
| --- | --- |
| 不确定该怎么救 | [Git 高频事故处理手册](git-troubleshooting-playbook.md) |
| commit 提交到了错误分支 | [Committed to Wrong Branch](committed-to-wrong-branch.md) |
| 想撤销某个操作 | [Undo Anything](undo-anything.md) |
| commit 找不到了 | [Recover Lost Commit](recover-lost-commit.md) |
| force push 覆盖了远端 | [Recover Force Push](recover-force-push.md) |
| merge 后发现合错了 | [Revert Merge Commit](revert-merge-commit.md) |
| 冲突处理乱了 | [Resolve Conflicts](resolve-conflicts.md) |
| secret 提交进历史 | [Remove Secret from History](remove-secret-from-history.md) |

## 处理原则

- 不确定时，先 `git status`、`git log --oneline -10`、`git reflog -10`
- 公共分支优先用 `revert`
- 本地未 push 的错误更容易整理
- 涉及 secret 时，先废弃和轮换密钥，再清理历史
- 涉及协作者时，先确认有没有人基于旧提交继续开发

## 相关内容

- [日常 Git 命令](../02-daily-workflow/everyday-git-commands.md)
- [AI 变更审查实战样例](../05-ai-native-development/ai-change-review-example.md)
- [Hotfix Process](../08-templates/hotfix-process.md)
