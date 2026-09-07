# Agent 事故恢复实验

本实验把 [Agent 事故恢复](../../06-troubleshooting/ai-agent-incident-recovery.md) 的几个高风险判断放进独立、带标记的临时目录。它执行真实 Git commit、`reset --hard`、`revert`、worktree 和一次推送到本地 bare remote；不会读取或修改当前仓库的历史、远端、工作区或凭据。

## 覆盖的判断

1. 未共享且仅含 Agent commits 的本地分支，先创建恢复分支，再用精确基线执行 `reset --hard`。
2. 已推送到实验 bare remote 的两条 Agent commits，按已确认 SHA 从新到旧 `revert`；夹在中间的人工 commit 保留。
3. `revert` 遇到同一文件的后续人工修改时产生冲突；`git revert --abort` 回到冲突前的 HEAD、文件内容和干净状态。
4. 普通 `git worktree remove` 拒绝脏 worktree；lock 使临时缺失目录的管理记录留过一次 `prune`，解锁后才清理该记录。

实验不包含真实 secret，也不模拟 GitHub secret scanning、GitHub Actions、分支保护、外部备份或生产数据补偿。它只验证本地 Git 的命令语义和文中列出的负例边界。

## 运行

从仓库根目录执行：

```bash
python3 labs/ai-agent-incidents/verify.py
bash labs/ai-agent-incidents/test.sh
```

`test.sh` 连续运行两次保留模式，读取 [expected.txt](expected.txt) 中的断言结果，检查保留目录的 marker 和证据文件，随后调用受 marker 限制的 cleanup。它还验证 cleanup 会拒绝一个无 marker 的空临时目录。

## 保留一次现场复查

```bash
lab_path=$(python3 labs/ai-agent-incidents/verify.py --keep)
sed -n '1,260p' "$lab_path/evidence.json"
python3 labs/ai-agent-incidents/verify.py --cleanup "$lab_path"
```

只有目录名带本实验前缀并含有预期 marker 时，`--cleanup` 才会删除目录。`--keep` 有助于人工查看 commit 图、revert 结果和 worktree 元数据；完成后应执行给出的 cleanup 命令。
