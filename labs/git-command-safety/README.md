# Git command safety regression

This self-contained regression uses only Python 3's standard library and Git. It creates disposable repositories in a Python-managed temporary directory, disables global/system Git configuration, signing, and hooks, then removes the temporary directory automatically.

Run it from the repository root:

```bash
bash labs/git-command-safety/test.sh
```

It verifies the exact command patterns documented in the paired articles.

| Scenario | Documented command pattern | Assertion |
| --- | --- | --- |
| A workspace already has staged, unstaged, and untracked work | `git status --porcelain`; any output stops the rewrite or cleanup flow | The branch name, `HEAD`, Index tree, tracked file contents, untracked file, and status remain unchanged. |
| A task owns complete tracked paths while unrelated work is already staged | `git commit --only -m "..." -- <agent-owned-paths>` | The commit contains only the named task path; unrelated staged, unstaged, and untracked content remains in place. |
| A local unpushed large commit must be split | `git reset --soft HEAD~1`, then `git reset`, then `git add -p` | The counterexample proves that `add -p` immediately after a soft reset leaves every hunk staged. The corrected flow commits only the selected hunk. |
| The integration branch is `master` | `git switch <integration-branch>` | `git switch main` fails without changing state; substituting `master` succeeds. |

The test only establishes local Git behavior in the temporary repositories. Remote authorization, protected-branch policies, hooks, and team workflow rules still require the actual repository's checks.

## 中文说明

这是一个只用 Python 3 标准库和 Git 的自包含回归实验。它在 Python 管理的临时目录创建仓库，隔离系统和全局 Git 配置、签名与 hooks，结束时自动移除临时目录。

从仓库根目录执行：

```bash
bash labs/git-command-safety/test.sh
```

实验对应中英文文章中的命令流程：工作区已有 staged、unstaged、untracked 内容时，`git status --porcelain` 有输出就停止重写或清理流程，并断言分支、`HEAD`、Index、文件内容和状态均未改变；完整任务路径用 `git commit --only -m "..." -- <agent-owned-paths>` 提交时，保留其他已有编辑；soft reset 后先执行 `git reset` 再 `git add -p`，才能只提交选中的 hunk；把占位符替换成实际集成分支 `master` 时，流程不依赖 `main`。

实验只证明临时本地仓库中的 Git 行为。实际仓库的远端授权、受保护分支、hooks 和团队规则仍需要单独确认。
