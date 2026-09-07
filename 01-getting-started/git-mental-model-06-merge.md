# Git 心智模型 06：Merge 先找共同祖先，再合并两条历史

[English](01-getting-started_en/git-mental-model-06-merge_en.md) | [交互演示](../interactive/git-mental-model/three-way-merge.html) | [可运行实验](../labs/git-mental-model/06-merge/README.md)

两个人都从同一份代码开始工作，为什么 Git 需要共同祖先，且一次合并有时只移动分支指针、有时会创建一个新 commit？只比较两个分支最新文件不够。Git 还要知道两边从哪份快照开始分叉，才能判断每一边相对那份快照做了什么。

本章解决五个问题：

1. 共同祖先如何定义三方合并的比较边界。
2. 普通 merge 中 `base`、`ours`、`theirs` 分别是哪份内容。
3. 快进和 merge commit 为什么具有不同历史形状。
4. 内容冲突与语义冲突分别遗漏了什么判断。
5. 冲突发生时，Index 的 stage 1、2、3 怎样帮助你做有依据的选择。

## 先看因果关系

设 `B` 是当前分支与待合并分支的共同祖先：

```text
          F1---F2  feature
         /
...---B---M1---M2  main (HEAD)
```

普通三方合并比较的是三份快照：

```text
base   = B   分叉前双方都承认的版本
ours   = M2  当前 HEAD 的版本
theirs = F2  被合入分支的版本
```

Git 根据 `base -> ours` 和 `base -> theirs` 两份变化尝试构造结果。共同祖先通常可由下面的命令直接读取：

```bash
git merge-base main feature
```

两个提交可以有多个同样好的共同祖先，例如交叉合并形成的图。此时 `git merge-base --all` 会列出全部候选；没有 `--all` 时，不应把输出的单个 ID 当成唯一候选。日常两分支合并一般只需要确认它确实是两边都可达的祖先。

## 普通 merge 里的 base、ours 与 theirs

发生内容冲突时，Git 不会把候选内容只留在冲突标记里。Index 会暂时保存三种版本：

| Index stage | 内容来源 | 在上图中的含义 |
| --- | --- | --- |
| 1 | merge base | `B` |
| 2 | 当前 `HEAD` | `ours`，即 `M2` |
| 3 | `MERGE_HEAD` | `theirs`，即 `F2` |

在一次尚未完成的普通 merge 中检查它们：

```bash
git status --short
git merge-base HEAD MERGE_HEAD
git ls-files --unmerged
git show :1:conflict.txt
git show :2:conflict.txt
git show :3:conflict.txt
```

输出中的 `:1:`、`:2:`、`:3:` 是从 Index 读取对象，和 Working Tree 的冲突标记是两层互补的证据。编辑 Working Tree 后执行：

```bash
git add conflict.txt
git merge --continue
```

`git add` 用解决后的内容替换三个高 stage 条目，建立 stage 0 条目。只有所有冲突路径回到 stage 0，merge 才能继续生成结果 commit。

第 03 章已经说明 Index 是下一次 commit 的草稿。这里可以看到它在冲突期间还有第二个作用：保存三方合并的候选输入。[回看 Index 章节](git-mental-model-03-index.md)。

## 快进与 merge commit：改变的是引用，还是对象图

### 快进

如果当前分支是待合并分支的祖先：

```text
main:    B
feature: B---F1---F2
```

执行默认 merge 时，Git 可以让 `main` 直接指向既有的 `F2`：

```bash
git switch main
git merge --ff-only feature
```

```text
main, feature: B---F1---F2
```

这个结果没有新 commit。`--ff-only` 要求必须快进，遇到已分叉历史会以非零状态退出，适合把预期历史形状写进脚本。默认 `--ff` 在可快进时使用快进；`--no-ff` 即使能够快进也会创建 merge commit。

### 已分叉历史的 merge commit

如果双方从共同祖先后都产生了提交：

```text
          F1---F2  feature
         /         \
...---B---M1---M2---R  main
```

`R` 是新的 merge commit，拥有两个 parent：当前分支原来的 `M2` 和被合入分支的 `F2`。这个对象把两条历史连接起来，同时记录合并结果的快照。

```bash
git switch main
git merge feature
git show --no-patch --format=raw HEAD
```

如果要在创建 merge commit 前检查结果，用：

```bash
git merge --no-ff --no-commit feature
git diff --cached
git status --short
```

快进没有 merge commit，所以 `--no-commit` 单独使用无法让 Git 停在快进前；`--no-ff --no-commit` 才会建立可审查的停点。完成检查后执行 `git commit`，放弃本次合并可执行 `git merge --abort`。

开始前先让 Index 与 `HEAD` 对齐，并保存尚未提交的工作。Git 官方文档明确提示：合并从有复杂未提交改动的工作区开始，`git merge --abort` 在某些情况下无法完整重建原状。

## 内容冲突和语义冲突分别说明什么

内容冲突表示 Git 无法机械地选出同一块文本的结果。它通常发生在双方都改了相同行或重叠 hunk。冲突标记要求人决定最终内容，解决后还要测试。

语义冲突可以没有冲突标记。两边修改了不同文件或不同代码区域，Git 成功合并文本，但组合后的接口、配置、权限或行为已经不满足约定。一次干净 merge 只证明 Git 构造出了文件快照，不能证明这个快照可以构建、通过测试或符合产品规则。

本章实验给出一个可重复的反例：

```text
semantic-server  将服务端协议和端口改为 https / 8443
semantic-client  将客户端地址改为 http://service:8443
semantic-result  两个不同文件的变更被干净合并
```

实验从 `semantic-result` 的真实 Git tree 取出文件，再运行标准库 Python 检查。它预期 `https://service:8443`，实际得到 `http://service:8443`，进程以退出码 `1` 结束。这是一个真正失败的行为检查，不是用文字假设出来的冲突。

## 运行真实实验

实验创建独立临时仓库，禁用系统和全局 Git 配置，设置临时身份、关闭签名并隔离 hooks。它不会修改当前项目：

```bash
cd labs/git-mental-model/06-merge
lab_path=$(bash setup.sh)
bash verify.sh "$lab_path"
```

`verify.sh` 的核心断言包括：

```text
ff-target       与 fast-forward 指向同一 commit，且该 commit 只有一个 parent
merge-result    有两个 parent
semantic-result 有两个 parent，行为检查退出码为 1
main            处于 UU conflict.txt；Index 中有 stage 1、2、3
```

保留实验现场时，可以按下面的顺序观察：

```bash
cd "$lab_path"
git log --graph --oneline --all --decorate
git show --no-patch --format=raw merge-result
git status --short
git merge-base HEAD MERGE_HEAD
git ls-files --unmerged -- conflict.txt
git show :1:conflict.txt
git show :2:conflict.txt
git show :3:conflict.txt
```

完成后仅清理带有本实验标记的临时仓库：

```bash
bash cleanup.sh "$lab_path"
```

一次运行创建、断言和清理：

```bash
bash test.sh
```

完整预期见 [expected.txt](../labs/git-mental-model/06-merge/expected.txt)。

## 改变条件预测题

当前图是：

```text
main:    B
feature: B---F1---F2
```

1. `git merge --ff-only feature` 后，`main` 指向哪里？会有几个 parent？
2. 同一位置改为 `git merge --no-ff feature`，对象图多了什么？
3. 如果 `main` 先新增 `M1`，再执行 `git merge --ff-only feature`，退出码和历史会怎样？

答案：

1. `main` 指向已有的 `F2`；`F2` 本身保持原有的一个 parent。
2. Git 创建一个新的 merge commit，它的两个 parent 是 `B` 与 `F2`。
3. `--ff-only` 以非零状态退出，因为 `main` 和 `feature` 已分叉；换成普通 merge 会尝试创建一个两 parent 的结果 commit。

## Agent 判断题

Agent 报告“merge 成功，没有冲突，可以直接放行”。以下哪组证据足够支撑放行判断？

```text
A. 只看 git status 没有 UU
B. 只看 merge commit 已出现
C. 检查共同祖先和结果 diff，确认 Index 没有未合并条目，再运行受影响的构建、测试和接口契约检查
```

选择 C。A 只排除了未解决的文本冲突，B 只说明对象图已经连接。行为正确性还依赖实际受影响路径的验证。若 Agent 无法说明它改动了哪些契约，先缩小 diff 和测试范围，再决定是否放行。

## 常见误解

### “共同祖先就是两条分支名称相同的起点”

共同祖先由 commit parent 关系决定，不由分支名称或创建日期决定。`git merge-base` 从对象图中计算可达关系。

### “快进也创建了一个 merge commit”

快进只让当前引用指向已有 commit。用 `git rev-list --parents -n 1 HEAD` 可以看到目标 commit 的 parent 数没有因为快进增加。

### “没有冲突标记就代表行为正确”

冲突标记回答的是文本如何拼接。构建、测试、迁移校验、接口契约和人工业务判断负责验证拼接后的含义。

### “ours 总是我想保留的业务版本”

在普通 merge 里，ours 是当前 `HEAD`，theirs 是 `MERGE_HEAD`。这是操作上下文的名称，不是业务优先级。使用 `--ours`、`--theirs` 前先读取当前操作和三个 stage 的实际内容。

## 延伸阅读

- [`git merge` 官方文档](https://git-scm.com/docs/git-merge)
- [`git merge-base` 官方文档](https://git-scm.com/docs/git-merge-base)
- [`git ls-files` 官方文档](https://git-scm.com/docs/git-ls-files)
- [第 03 章：Index 是下一次 commit 的草稿](git-mental-model-03-index.md)
