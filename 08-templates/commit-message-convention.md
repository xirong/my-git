# Commit Message Convention

## 格式

```text
<type>(<scope>): <subject>
```

## 类型

- `feat`: new feature
- `fix`: bug fix
- `docs`: documentation
- `style`: formatting only
- `refactor`: code change without behavior change
- `test`: add or update tests
- `chore`: tooling or maintenance
- `perf`: performance improvement
- `ci`: CI/CD change

## 示例

```text
feat(auth): add GitHub OAuth login
fix(api): handle empty response correctly
docs(git): add troubleshooting guide
refactor(order): simplify pricing calculation
test(auth): cover expired token case
```

## 规则

- subject 使用祈使句或清晰动作描述
- 一个 commit 只表达一个意图
- 不使用 `update`、`misc`、`wip` 这类模糊标题作为最终提交

## AI 协作与 `Co-authored-by`

团队需要记录 AI 工具参与时，在 commit 正文后保留一个空行，再添加团队认可的署名 trailer：

```text
Co-authored-by: <name or approved tool identity> <email>
```

GitHub 支持用一个或多个 `Co-authored-by` trailer 记录共同作者，格式与邮箱要求见 [GitHub Docs：创建多作者 commit](https://docs.github.com/en/pull-requests/how-tos/commit-changes/creating-a-commit-with-multiple-authors)。

- 工具或模型、参与范围和受影响文件写在 PR 的 AI 协作记录中；不要用 trailer 猜测这些细节。
- `Co-authored-by` 用于记录提交中的署名或工具参与来源，不代表有人已经审查所有文件，也不证明变更正确。
- 不要虚构真实人的姓名或邮箱，也不要承诺 GitHub 会将工具身份识别为账号或共同作者。
- 人工审查的实际文件和审查重点，单独填写在 PR 的人工审查部分；尚未审查时明确标出。
