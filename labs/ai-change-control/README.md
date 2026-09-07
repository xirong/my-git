# Agent Change Control Lab / Agent 变更控制实验

[中文文章](../../05-ai-native-development/ai-change-control-loop.md) | [English article](../../05-ai-native-development/05-ai-native-development_en/ai-change-control-loop_en.md)

## 中文

这个实验用一个临时 Git 仓库和一个最小 HTTP 服务，走完一次 Agent 改动的验收链：

~~~text
意图 -> 范围 -> 候选 commit -> 干净检出测试 -> 制品 -> 本地运行结果 -> 代码恢复
~~~

它只需要 Python 3 和 Git。所有仓库、制品、运行目录和事件记录都在脚本新建的临时根目录中；宿主仓库不会被提交、切分支或清理。

### 运行

在仓库根目录执行：

~~~bash
python3 labs/ai-change-control/lab.py
~~~

脚本每次创建一个独立的实验根，并完成这些可观察动作：

1. 基线服务要求显式的 <code>SERVICE_TIMEOUT</code>。基线测试保留该旧契约的缺失、空值、非整数和非正数边界；Agent 同时修改应用、添加目标测试，并改动一份与任务无关的笔记。
2. 此时在脏工作区跑测试会通过。脚本只提交新测试，随后在该 commit 的干净 worktree 跑同一测试，并断言它以退出码 <code>1</code> 和指定错误消息失败。
3. 脚本只提交应用修复，并保留无关笔记为未提交编辑。新测试要求缺失或空值都默认到 <code>30</code>，显式正数保持原值，非整数和非正数仍报原来的错误。它在新建的干净 worktree 测试候选 commit，记录实际 SHA。
4. 脚本通过 <code>git archive</code> 从该 commit 构建 tar.gz 制品，生成制品外部的 JSON 清单，记录候选 commit SHA、制品 SHA-256、源码 SHA-256 和版本。它会断言制品中的笔记仍是提交版本，无关工作区编辑没有被打进制品。
5. 脚本先复制制品并篡改副本，复用启动前的 SHA-256 校验入口，断言副本以明确的 checksum mismatch 被拒绝且服务没有启动。它随后重新解包原始制品，重算制品 SHA-256，再核对清单、Git 源码和内置构建信息。
6. 原始制品通过校验后，脚本在 <code>127.0.0.1</code> 的系统分配端口启动其中的服务，并用真实 HTTP 请求验证默认超时值、版本、候选 SHA 和事件计数。
7. 脚本用两个 <code>git revert</code> commit 恢复代码，再构建和运行回退制品。先前 HTTP 请求写入的临时事件文件仍有两条记录，展示 Git 回退不会自动撤销外部状态。

每次输出中的 SHA-256、commit SHA 和端口都由本次运行产生。稳定的是输出标签和检查关系；示例格式见 [expected.txt](expected.txt)。

### 保留并检查一次运行

默认成功后会清理临时根。加 <code>--keep</code> 可保留成功结果：

~~~bash
python3 labs/ai-change-control/lab.py --keep
~~~

复制末行的路径到 <code>lab_path</code>，再检查真实中间证据：

~~~bash
lab_path=/printed/lab/root
python3 -m json.tool "$lab_path/evidence/exercise-evidence.json"
git -C "$lab_path/agent-worktree" log --oneline --decorate --all --graph
git -C "$lab_path/agent-worktree" status --short
cat "$lab_path/external-state/events.jsonl"
~~~

清理只接受脚本创建、名字匹配且根目录含正确标记文件的实验路径：

~~~bash
python3 labs/ai-change-control/lab.py --cleanup "$lab_path"
~~~

脚本不会删除仓库根目录、用户主目录、文件系统根目录、未标记目录，或临时目录之外的路径。

### 预测题

1. Agent 已在工作区修改 <code>app.py</code>，但只暂存了新增测试。测试为何在当前目录通过，而候选 commit 的干净 worktree 会失败？
2. 回退制品恢复了旧版超时规则后，为什么事件文件仍包含修复版本的那条记录？
3. 被篡改的制品为何在服务启动前就被拒绝？清单中的制品 SHA-256 与源码 SHA-256 分别能检查什么？它们为什么仍不能代替签名、可信构建系统或生产发布证据？

先写下判断，再运行实验，把它与 <code>exercise-evidence.json</code> 对照。

### 自测与边界

~~~bash
bash labs/ai-change-control/test.sh
~~~

自测会连续运行两次、验证每次保留结果的清单和事件证据、执行受控清理，并确认未标记路径被拒绝清理。

这是本地发布环境演练：HTTP 服务仅监听回环地址，事件文件是临时文件，清单是可重算的完整性记录。它没有连接真实 CI、托管平台、生产环境或外部服务；JSON 清单也不构成签名或供应链证明。

## English

This lab uses a temporary Git repository and a minimal HTTP service to exercise one Agent-change acceptance chain:

~~~text
intent -> scope -> candidate commit -> clean-checkout test -> artifact -> local runtime result -> code recovery
~~~

It needs only Python 3 and Git. The script creates all repositories, artifacts, runtime directories, and event records below its own temporary root. It does not commit, switch branches, or clean the host repository.

### Run it

From the repository root:

~~~bash
python3 labs/ai-change-control/lab.py
~~~

Each run creates an isolated lab root and performs these observable actions:

1. The baseline service requires an explicit <code>SERVICE_TIMEOUT</code>. Its tests retain the old-contract boundaries for missing, empty, non-integer, and non-positive values. The Agent changes the application, adds the target test, and edits an unrelated note.
2. The test passes in that dirty working tree. The script commits only the new test, then runs the same test in a clean worktree for that commit and asserts exit code <code>1</code> with the required failure message.
3. The script commits only the application repair and keeps the unrelated note as an uncommitted edit. The new tests require missing and empty values to default to <code>30</code>, preserve explicit positive values, and retain the prior errors for non-integer and non-positive values. It tests the candidate commit in a fresh clean worktree and records the actual SHA.
4. The script builds a tar.gz artifact from that commit with <code>git archive</code>. An external JSON manifest records the candidate commit SHA, artifact SHA-256, source SHA-256, and version. The lab asserts that the note in the artifact is the committed version and excludes the unrelated working-tree edit.
5. The script copies and tampers with the artifact, reuses the SHA-256 startup-preflight check, and asserts that the copy is rejected with an explicit checksum mismatch before any service starts. It then extracts the original artifact, recomputes its SHA-256, and checks the manifest, Git source, and embedded build metadata.
6. After the original artifact passes verification, the script starts its service on a system-assigned <code>127.0.0.1</code> port and uses a real HTTP request to check the default timeout, version, candidate SHA, and event count.
7. The script creates two <code>git revert</code> commits to recover the code, then builds and runs a rollback artifact. The temporary event file retains two records, showing that a Git revert does not automatically undo external state.

SHA-256 values, commit SHAs, and ports are measured anew on every run. The labels and assertions stay stable; see [expected.txt](expected.txt) for the output shape.

### Keep and inspect one run

A successful default run removes its temporary root. Use <code>--keep</code> to retain one:

~~~bash
python3 labs/ai-change-control/lab.py --keep
~~~

Copy the final path into <code>lab_path</code>, then inspect real intermediate evidence:

~~~bash
lab_path=/printed/lab/root
python3 -m json.tool "$lab_path/evidence/exercise-evidence.json"
git -C "$lab_path/agent-worktree" log --oneline --decorate --all --graph
git -C "$lab_path/agent-worktree" status --short
cat "$lab_path/external-state/events.jsonl"
~~~

Cleanup accepts only an experiment path created by the script whose name and root marker both match:

~~~bash
python3 labs/ai-change-control/lab.py --cleanup "$lab_path"
~~~

The script refuses the repository root, home directory, filesystem root, unmarked directories, and paths outside the temporary directory.

### Prediction questions

1. The Agent changed <code>app.py</code> in its working tree but staged only the new test. Why does the test pass there while the clean worktree for the candidate commit fails?
2. After the rollback artifact restores the earlier timeout rule, why does the event file still include the record from the repaired version?
3. Why is the tampered artifact rejected before a service starts? What can the artifact SHA-256 and source SHA-256 each check, and why can neither replace a signature, trusted build system, or production-release evidence?

Write down your prediction before running the lab, then compare it with <code>exercise-evidence.json</code>.

### Self-test and boundary

~~~bash
bash labs/ai-change-control/test.sh
~~~

The self-test runs the lab twice, verifies each retained run's manifest and event evidence, performs controlled cleanup, and checks that cleanup rejects an unmarked path.

This is a local release-environment exercise. The HTTP service listens only on loopback, and its event file is temporary. The manifest is a recomputable integrity record. The lab does not contact a real CI system, hosting platform, production environment, or external service, and its JSON manifest is not a signature or supply-chain proof.
