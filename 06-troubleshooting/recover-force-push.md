# Recover Force Push

force push 覆盖远端分支后，先找回正确 commit。

如果有人本地还保留旧分支，通常可以恢复。

## 先冻结现场

先通知团队暂停向相关分支 push。

然后在本地检查：

```bash
git reflog
git log --oneline --decorate -20
```

也可以让同事在本地找：

```bash
git reflog
git log --oneline --decorate -20
```

## 找到正确 commit

确认 good sha 后，先建备份分支：

```bash
git branch backup-good-main <good-sha>
```

检查内容：

```bash
git show --stat <good-sha>
git diff <bad-sha>..<good-sha>
```

## 恢复远端分支

```bash
git push origin <good-sha>:main
```

如果主分支受保护，需要管理员处理。

## 后续补救

- 检查是否有人基于错误历史继续开发
- 通知所有人重新同步
- 给主分支开启分支保护
- 限制 force push 权限
- 复盘为什么会发生

## 延伸阅读

- [git reflog 官方文档](https://git-scm.com/docs/git-reflog.html)
- [GitHub protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
- [Git 高频事故处理手册](git-troubleshooting-playbook.md)
