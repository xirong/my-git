# AI 变更审查实战样例

这篇用一个模拟场景说明：AI 改完代码后，人类如何用 Git 把变更重新整理成可审查、可验证、可回滚的工程单元。

## 场景

你让 AI 修复一个问题：

```text
订单超时配置为空时，系统应该使用默认超时时间，不能直接抛异常。
```

AI 完成后，工作区变成这样：

```bash
git status --short
```

```text
 M src/order/timeout.ts
 M src/order/validator.ts
 M src/order/index.ts
 M test/order/timeout.test.ts
 M package-lock.json
 M README.md
?? debug-output.log
```

这时不要直接 `git add .`。

## 第一步：先看变更规模

```bash
git diff --stat
```

重点看三件事：

1. 文件数量是否超出任务范围
2. 是否有生成文件、日志、锁文件
3. 是否混入文档、格式化、依赖升级

这个例子里，任务是修复订单超时配置，但出现了：

- `src/order/index.ts`
- `package-lock.json`
- `README.md`
- `debug-output.log`

这些都需要先确认是否相关。

## 第二步：确认归属，不凭“无关”清理

状态列表能说明路径变了，不能说明谁拥有它。这个场景里的 `package-lock.json`、`README.md` 和 `debug-output.log` 可能来自 AI，也可能是用户或另一个 Agent 正在保留的编辑、排障证据或待提交工作。

先记录 staged 和 unstaged 的范围：

```bash
git status --short
git diff --cached --name-only
git diff --name-only
```

把每个路径标成“本任务完整路径”“其他 owner 的编辑”或“尚未确认”。尚未确认和其他 owner 的路径保持不动。当前 commit 不需要它们时，后面的路径限定提交会把它们留在原处。

丢弃内容需要路径归属、期望基线和 owner 授权同时成立。例如，只有 owner 明确确认 `debug-output.log` 是可丢弃的 AI 临时文件时，才可执行：

```bash
rm -- debug-output.log
```

只有 owner 确认两个已跟踪路径都完全由 AI 产生，并确认它们应恢复为 `HEAD` 时，才可执行：

```bash
git restore --source=HEAD --staged --worktree -- package-lock.json README.md
```

后一条命令会同时覆盖指定路径的 Index 和 Working Tree。指定路径里只要混有用户 hunk、已有 staged 内容或不确定来源，就停止，不执行 restore、`git clean` 或广泛的 reset。

## 第三步：按意图拆 diff

先看测试：

```bash
git diff -- test/order/timeout.test.ts
```

假设人工复核确认测试文件是本任务的完整已跟踪路径，且该路径没有已有 staged hunk，可以只提交这个路径的 Working Tree 版本：

```bash
git diff -- test/order/timeout.test.ts
git diff --cached -- test/order/timeout.test.ts
git commit --only -m "test(order): cover empty timeout config" -- test/order/timeout.test.ts
```

再看实现：

```bash
git diff -- src/order/timeout.ts src/order/validator.ts
```

确认实现只改了默认值处理，没有顺手改错误码、接口签名、日志格式。

两个实现路径也必须都是本任务的完整已跟踪路径，且它们的 `git diff --cached` 没有已有 hunk：

```bash
git diff -- src/order/timeout.ts src/order/validator.ts
git diff --cached -- src/order/timeout.ts src/order/validator.ts
git commit --only -m "fix(order): fallback to default timeout config" -- src/order/timeout.ts src/order/validator.ts
```

`git commit --only` 读取指定路径的整个 Working Tree 版本，并保留其他路径的 staged、unstaged 和 untracked 内容。它不适合“同一个文件只提交已暂存 hunk”的场景，也不会替你区分该路径里的不同意图。遇到这种文件，先转到干净或隔离的 task worktree，再用 `git add -p` 和普通 `git commit`。可运行的 [Git 命令安全回归](../labs/git-command-safety/README.md) 覆盖了这两条边界。

这样最后形成两个 commit：

```text
test(order): cover empty timeout config
fix(order): fallback to default timeout config
```

## 第四步：让 AI 做一轮风险扫描

可以把当前 diff 或 commit 范围交给 AI 审查：

```text
请审查当前分支相对团队约定的集成分支的变更。
只列具体风险，不做泛泛总结。
重点检查：
1. 行为边界是否被扩大
2. 错误处理是否变弱
3. 默认值是否影响兼容性
4. 测试是否覆盖真实业务场景
5. 是否有无关变更混入
```

如果 AI 输出的问题没有文件路径、没有具体风险、只有“看起来不错”，这轮 Review 价值很低，需要继续追问。

## 第五步：人工复核重点

人类 reviewer 至少要确认：

- 空配置、空字符串、非法数字分别怎么处理
- 默认值来自哪里
- 线上配置是否可能覆盖代码默认值
- 错误码和日志是否变化
- 调用方是否依赖原来的异常行为
- 测试是否能在修复前失败、修复后通过

涉及线上配置时，静态代码只能说明默认行为。最终线上值仍要结合配置中心、环境变量或部署参数确认。

## 第六步：运行验证

只跑和本次变更最相关的验证：

```bash
npm test -- test/order/timeout.test.ts
```

如果项目有 lint 或类型检查，也补上：

```bash
npm run lint
npm run typecheck
```

PR 里要写清实际执行过的命令和结果。

## 第七步：写 PR

推荐 PR 描述：

```md
## What changed

- Add test coverage for empty timeout config
- Fallback to default timeout config when config is empty

## Why

Empty timeout config should not break order validation.

## How tested

- npm test -- test/order/timeout.test.ts
- npm run lint

## Risk

Low. The change only affects empty timeout config fallback.

## Rollback plan

Revert this PR.
```

## 第八步：如果 diff 仍然太大

如果 AI 一次改了跨层能力，比如 model、service、API、UI、文档都变了，单个 PR 仍然很难审。

这时可以拆成 stacked PR：

```text
PR 1: add tests for timeout fallback
PR 2: implement timeout fallback
PR 3: update API response note
PR 4: update docs
```

详细见 [Stacked PR for AI-Generated Changes](stacked-pr-for-ai-generated-changes.md)。

## 常见错误

### 直接提交 AI 的全部输出

风险：无关文件、调试日志、依赖变化会混入。

建议：永远先看 `git diff --stat`。

### 只看测试通过

风险：AI 可能写出只验证当前实现的测试。

建议：确认测试是否覆盖业务边界，并尽量确认修复前会失败。

### 把重构和行为修复放在一起

风险：reviewer 无法判断风险来自哪里。

建议：先修行为，再单独做重构。

## 延伸阅读

- [AI Native Git Workflow](ai-native-git-workflow.md)
- [How to Review AI-Generated Code](ai-generated-code-review.md)
- [AI Commit Splitting](ai-commit-splitting.md)
- [Stacked PR for AI-Generated Changes](stacked-pr-for-ai-generated-changes.md)
- [AI Code Review Checklist](../08-templates/ai-code-review-checklist.md)
