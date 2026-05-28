# Recover Lost Commit

丢 commit 时，先看 reflog。

很多“丢了”的 commit 其实还在本地，只是当前分支指针不再指向它。

## 先保存现场

```bash
git status
git log --oneline --decorate -10
git reflog -20
```

如果工作区还有未提交改动：

```bash
git stash push -u -m "backup before recover lost commit"
```

## 用 reflog 找 commit

```bash
git reflog
```

找到目标 commit 后，不要急着 reset，先创建恢复分支：

```bash
git branch recovered-work <commit-sha>
git switch recovered-work
```

这样可以先检查内容：

```bash
git show --stat
git diff main...HEAD
```

## 常见可恢复场景

- reset 错了
- rebase 后提交不见了
- amend 覆盖了上一个 commit
- 切分支后找不到刚才的提交
- 删除了本地分支

## 什么时候可能恢复不了

- reflog 已经过期
- 本地对象已经被清理
- 从来没有 commit，只是工作区文件被删除
- 只存在于别人机器上，自己本地没有对象

如果从来没有 commit，Git 通常救不了，需要看编辑器、本地备份、IDE local history。

## 延伸阅读

- [git reflog 官方文档](https://git-scm.com/docs/git-reflog.html)
- [Atlassian: git reflog](https://www.atlassian.com/git/tutorials/rewriting-history/git-reflog)
- [Git Flight Rules](https://github.com/k88hudson/git-flight-rules)
- [Git 高频事故处理手册](git-troubleshooting-playbook.md)
