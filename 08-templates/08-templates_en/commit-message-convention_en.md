# Commit Message Convention

English | [中文](../commit-message-convention.md)

## Format

```text
<type>(<scope>): <subject>
```

## Types

- `feat`: new feature
- `fix`: bug fix
- `docs`: documentation
- `style`: formatting only
- `refactor`: code change without behavior change
- `test`: add or update tests
- `chore`: tooling or maintenance
- `perf`: performance improvement
- `ci`: CI/CD change

## Examples

```text
feat(auth): add GitHub OAuth login
fix(api): handle empty response correctly
docs(git): add troubleshooting guide
refactor(order): simplify pricing calculation
test(auth): cover expired token case
```

## Rules

- The subject should use the imperative mood or a clear action description
- A single commit should express only one intent
- Do not use vague titles like `update`, `misc`, or `wip` for final commits
