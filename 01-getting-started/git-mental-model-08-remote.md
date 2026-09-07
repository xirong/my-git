# Git 心智模型 08：远端是另一个仓库，`origin/main` 是本地记录

[English](01-getting-started_en/git-mental-model-08-remote_en.md) | [交互演示](../interactive/git-mental-model/remote-and-fetch.html) | [可运行实验](../labs/git-mental-model/08-remote/README.md)

当 Agent 报告“我已经看到远端最新 `main`”时，审查者需要追问两件事：它看的是远端服务此刻的分支，还是本地上次 fetch 留下的 `origin/main`？它有没有把这份记录合入本地工作目录？这两个问题决定了下一步是只读检查、整合变更，还是处理协作冲突。

本章用 `reader`、`writer` 和一个临时 bare `origin.git` 说明：普通 `git fetch origin` 更新远端跟踪引用，不会自动改写当前分支、Index 或 Working Tree；显式 fast-forward 整合才会把文件带到工作目录；push 还会经过服务端的认证、授权、分支策略和快进规则。

## 场景：远端有人先推了一次提交

初始时，`reader` 的本地 `main` 与本地记录 `origin/main` 都在提交 A：

```text
reader
  HEAD -> main -> A
  origin/main -> A
  Index / Working Tree: story.txt = version=1

writer pushes B to the bare origin
```

`reader` 执行普通 fetch 后：

```text
reader
  HEAD -> main -> A
  origin/main -> B
  Index / Working Tree: story.txt = version=1
```

`B` 的对象已下载到本地，`origin/main` 也指向 B。`main` 仍在 A，所以文件没有变化。接着明确执行：

```bash
git merge --ff-only origin/main
```

状态才变为：

```text
reader
  HEAD -> main -> B
  origin/main -> B
  Index / Working Tree: story.txt = version=2
```

## 概念：远端名、远端分支与远端跟踪引用

`origin` 是本地配置里一个远端仓库的名字，常见于 clone 后的默认配置。它指向 URL，不等于某个分支。

`main` 是当前仓库中的本地分支引用，通常位于 `refs/heads/main`。`origin/main` 是本地的远端跟踪引用，通常位于 `refs/remotes/origin/main`。它记录的是最近一次成功 fetch 后，本地看到的远端 `main` 提示位置。

因此可以同时存在：

```text
main          A   本地工作基线
origin/main   B   最近 fetch 到的远端提示
HEAD          main
```

远端服务的真实分支可能在下一秒继续前进。没有新的网络查询时，`origin/main` 只能证明本地已记录的观察结果，不能证明服务端仍停在同一个提交。

普通 `git fetch origin` 下载需要的对象并更新配置的远端跟踪引用。它还会更新 `FETCH_HEAD`，并可能触发自动维护。它不会执行 merge、rebase、switch 或 checkout，因此不会把 B 的文件内容写入当前 Working Tree。带自定义 refspec 的底层用法有不同目标；本章讨论 clone 后最常见的 `git fetch origin`。

## 先观察，再决定是否整合

先确认自己站在哪个引用上：

```bash
git status --short
git branch -vv
git log --oneline --decorate --graph --all -n 12
git rev-parse main origin/main
```

只想获取远端信息时：

```bash
git fetch origin
git log --left-right --graph --oneline main...origin/main
git diff --stat main..origin/main
```

预期结果是 `origin/main` 可能移动，当前 `main` 和已检出文件不变。`main...origin/main` 让左右两侧各自独有的提交显式出现，适合判断落后、领先或分叉。

确认远端提示是本地分支的后代，并希望把它带入工作目录时：

```bash
git merge --ff-only origin/main
git status --short
git rev-parse HEAD main origin/main
```

`--ff-only` 把“只能直进”写进命令。若两边已分叉，命令失败并保持现状，让人选择 merge、rebase 或其他团队约定的整合方式。`git pull` 把 fetch 和后续整合放进一个命令，具体使用 merge 还是 rebase 受参数和配置影响；需要展示状态变化时，分开写更容易审核。

## push：本地声明要更新远端，远端负责接受或拒绝

```bash
git push origin main
```

这个命令要求把本地 `main` 推到名为 `origin` 的远端 `main`。Git 会发送远端尚缺少的对象，并尝试更新目标引用。能否完成取决于多层条件：

1. 传输是否能连接，凭据是否通过认证。
2. 服务端是否授权该身份写入目标仓库和分支。
3. 服务端的保护规则或 hook 是否接受这次更新。
4. 目标分支是否能从旧尖端 fast-forward 到本地提交。

非快进拒绝的图形是：

```text
          C  reader local main
         /
        B
         \
          D  origin main after writer push
```

远端 `D` 不是本地 `C` 的祖先。本地直接把远端从 D 改到 C 会丢失 D 那条路径，所以默认 push 拒绝。安全恢复顺序是：

```bash
git fetch origin
git log --left-right --graph --oneline main...origin/main
# 按团队约定 merge 或 rebase，并处理冲突
# 运行该仓库要求的检查
git push origin main
```

`git push --force` 可以改写已经发布的历史，可能使其他人的提交失去分支引用。共享分支只在团队明确允许、确认影响范围并完成对应检查后才讨论 `--force-with-lease` 等选项；它不是非快进拒绝的默认修复手段。

本地 bare 仓库可以复现 Git 的图关系和服务端 hook 拒绝，却无法替代 GitHub、GitLab 等平台的真实账号认证与分支保护配置。实验中的 `protected` hook 仅展示“服务端可拒绝客户端请求”这个边界。

## 在临时仓库运行实验

实验创建自己的临时根目录、bare origin 和两个 clone。所有 push 只发往该临时 bare 路径：

```bash
cd labs/git-mental-model/08-remote
lab_path=$(bash setup.sh)
bash verify.sh "$lab_path"
sed -n '1,240p' "$lab_path/observations.txt"
sed -n '1,240p' "$lab_path/push-results.txt"
bash cleanup.sh "$lab_path"
```

`verify.sh` 使用真实 Git 输出断言：

- fetch-only 时，`reader` 的 `origin/main` 从 A 到 B，`reader/main`、Index 和 Working Tree 仍在 A。
- `merge --ff-only origin/main` 后，`reader` 的 HEAD、`main`、Index 和 Working Tree 都到 B。
- `reader` 产生 C、`writer` 把 D 推到临时 bare origin 后，`reader` 的直接 push 失败。
- 临时 bare origin 的 hook 拒绝 `protected` 分支更新。

实验关闭全局 Git 配置、签名和调用方 hooks。`cleanup.sh` 只接受有本实验标记且结构完整的临时根目录。想继续查看状态时先不要执行 cleanup。

完整自测：

```bash
bash labs/git-mental-model/08-remote/test.sh
```

## 预测题：改变的是 fetch 还是整合？

`writer` 已将 B 推到远端，`reader` 初始仍在 A。先写下预测，再运行实验：

| 操作 | `reader/main` | `reader/origin/main` | `story.txt` |
| --- | --- | --- | --- |
| `git fetch origin` | A | B | `version=1` |
| 随后 `git merge --ff-only origin/main` | B | B | `version=2` |

改变条件是第二行多了明确的整合命令。若 fetch 后远端提示与本地分叉，`--ff-only` 会停止并保留现状。此时应先展示两侧提交和团队整合约定，不能猜测该 merge、rebase 还是放弃本地提交。

## Agent 迁移题：把“最新”变成可审计的状态声明

Agent 的交接记录至少应包含：

```text
fetch time: 2026-... with remote origin
local branch and HEAD: main -> <oid>
remote-tracking ref after fetch: origin/main -> <oid>
working-tree change performed: none | merge --ff-only origin/main | other approved integration
push result: not attempted | accepted | rejected, with reason
```

这份记录把“看见远端”“更新本地文件”和“得到远端写入权限”拆成可验证事实。自动化只做 fetch 时，报告应写成“已更新本地 `origin/main`”，不要写成“本地已同步”或“已获得 push 权限”。

## 延伸阅读

- [git-fetch 官方手册](https://git-scm.com/docs/git-fetch)
- [git-push 官方手册](https://git-scm.com/docs/git-push)
- [git-remote 官方手册](https://git-scm.com/docs/git-remote)
- [实验说明](../labs/git-mental-model/08-remote/README.md)
