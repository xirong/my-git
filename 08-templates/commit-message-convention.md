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
