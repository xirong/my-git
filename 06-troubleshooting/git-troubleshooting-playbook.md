# Git Troubleshooting Playbook

动手恢复前，先回答三个问题：

1. 代码是否已经提交
2. commit 是否已经 push
3. 是否已经有人基于这些 commit 继续开发

不同答案，处理方式完全不同。

## 修复前先保留现场

先保存现场：

```bash
git status
git log --oneline --decorate -10
git reflog -10
```

如果工作区还有未提交代码，先临时保存：

```bash
git stash push -u -m "backup-before-recovery"
```

## 场景 1：commit 提交到了错误分支

### 现象

你在 `main` 上提交了本来应该在 feature 分支里的 commit。

### 先检查

```bash
git status
git log --oneline -5
```

### 安全处理：还没 push

```bash
git branch feat/right-branch
git reset --hard HEAD~1
git switch feat/right-branch
```

这会把当前 commit 保留到新分支，并让原分支回到提交前。

### 如果已经 push

如果已经 push，优先新建 PR 修正，不要直接重写公共分支历史。

可以：

```bash
git switch -c feat/right-branch <commit-sha>
git push -u origin feat/right-branch
```

然后在原分支上用 revert 撤销：

```bash
git revert <commit-sha>
```

## 场景 2：reset 到了错误位置

### 先检查

```bash
git reflog
```

### 恢复方式

找到 reset 前的位置：

```bash
git reset --hard HEAD@{1}
```

如果不确定，先创建备份分支：

```bash
git branch backup-before-recover HEAD@{1}
```

## 场景 3：commit 丢了

### 先检查

```bash
git reflog
```

### 恢复方式

```bash
git branch recovered-work <commit-sha>
git switch recovered-work
```

只要 commit 还在 reflog 里，通常可以救回来。

## 场景 4：错误代码已经 push

### 如果还没人基于它继续开发

可以和团队确认后修正历史：

```bash
git revert <commit-sha>
```

优先用 revert，因为它不会改写公共历史。

### If the commit includes secret

不要只 revert。

先废弃并轮换密钥，再清理历史，见 [Remove Secret from History](remove-secret-from-history.md)。

## 场景 5：force push 覆盖了远端分支

### 先检查

```bash
git reflog
git log --oneline --decorate -10
```

让仍保留旧提交的同事执行：

```bash
git log --oneline origin/main -10
git reflog -10
```

### 恢复远端分支

找到正确 commit 后：

```bash
git push origin <good-sha>:main
```

如果分支受保护，需要管理员或平台 owner 处理。

## 场景 6：合并了错误分支

### 如果已经产生 merge commit

```bash
git log --oneline --merges -10
git revert -m 1 <merge-commit-sha>
```

`-m 1` 表示保留第一父分支的视角，撤销被合入分支带来的变化。

### 避免

不要对已经 push 且被别人使用的主分支随意 `reset --hard`。

## 场景 7：提交了 secret

### 第一动作

立即废弃并轮换 secret。

Git 历史清理不能让已经泄露的 token 重新安全。

### 然后清理历史

推荐使用 `git filter-repo` 或平台提供的安全处理流程。

见 [Remove Secret from History](remove-secret-from-history.md)。

## 场景 8：rebase 处理乱了

### 还在 rebase 中，先中止

```bash
git rebase --abort
```

### 冲突解决后继续

```bash
git status
git add <files>
git rebase --continue
```

### 恢复到 rebase 前

```bash
git reflog
git reset --hard <before-rebase-sha>
```

## 场景 9：撤销公共 commit

公共 commit 优先用：

```bash
git revert <commit-sha>
```

这样会新增一个反向 commit，历史清楚，协作者也安全。

## 场景 10：清理本地改动

### 先看会删除什么

```bash
git status
git clean -nd
```

### 删除未跟踪文件

```bash
git clean -fd
```

### 丢弃已跟踪文件改动

```bash
git restore <file>
```

### 高风险操作

```bash
git reset --hard
```

执行前确认没有需要保留的本地改动。

## 快速判断表

| 状态 | 优先方案 |
| --- | --- |
| 未提交 | `git stash` 或 `git restore` |
| 已提交未 push | `reset`、`commit --amend`、交互式 rebase |
| 已 push 无人基于它开发 | 可以协商后重写历史 |
| 已 push 且别人基于它开发 | 优先 `git revert` |
| 提交了 secret | 先轮换密钥，再清理历史 |

## 延伸阅读

- [Undo Anything](undo-anything.md)
- [Recover Lost Commit](recover-lost-commit.md)
- [Remove Secret from History](remove-secret-from-history.md)
- [Git Flight Rules](https://github.com/k88hudson/git-flight-rules)
- [git reflog](https://git-scm.com/docs/git-reflog.html)
- [git restore](https://git-scm.com/docs/git-restore.html)
- [推荐阅读索引](../09-resources/recommended-reading.md)
