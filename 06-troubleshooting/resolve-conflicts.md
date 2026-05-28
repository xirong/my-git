# Resolve Conflicts

冲突处理的关键是先理解双方意图，再决定保留哪一侧或如何合并。

不要看到冲突标记就机械选择 `ours` 或 `theirs`。

## 冲突长什么样

```text
  <<<<<<< HEAD
当前分支内容
  =======
被合入分支内容
  >>>>>>> feature/login
```

你需要把这段内容整理成最终想保留的样子，并删除冲突标记。

## merge 过程中的冲突

查看状态：

```bash
git status
git diff
```

解决文件后：

```bash
git add <resolved-files>
git merge --continue
```

如果处理乱了：

```bash
git merge --abort
```

## rebase 过程中的冲突

查看状态：

```bash
git status
git diff
```

解决文件后：

```bash
git add <resolved-files>
git rebase --continue
```

如果处理乱了：

```bash
git rebase --abort
```

## 处理建议

- 先看冲突文件所属业务
- 找出两边各自想解决什么问题
- 必要时查看提交历史
- 解决后跑最小相关测试
- 不确定时找对应 owner 一起看

查看冲突来源：

```bash
git log --oneline --left-right --merge
```

## AI 编程场景

AI 处理冲突时容易只做文本拼接。

建议让 AI 解释两边语义，再由人类确认最终结果。

## 延伸阅读

- [GitHub Docs: Resolving a merge conflict using the command line](https://docs.github.com/en/get-started/using-git/resolving-merge-conflicts-after-a-git-rebase)
- [Atlassian: Merge conflicts](https://www.atlassian.com/git/tutorials/using-branches/merge-conflicts)
- [Git 高频事故处理手册](git-troubleshooting-playbook.md)
