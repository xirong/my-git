# Commit Message

English | [中文](../commit-message.md)

A good commit message lets people in the future know why this change exists.

It is not just written for the current reviewer, but also for yourself and your teammates in the future when troubleshooting, reverting code, or generating changelogs.

## Recommended Format

```text
<type>(<scope>): <subject>
```

Examples:

```text
feat(auth): add GitHub OAuth login
fix(api): handle empty response
docs(git): add troubleshooting guide
refactor(order): simplify pricing calculation
```

This format comes from [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/), which has been adopted by many open-source projects and automated release tools.

## Common Types

| type | Meaning |
| --- | --- |
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation |
| `style` | Purely formatting adjustments |
| `refactor` | Refactoring that does not change behavior |
| `test` | Tests |
| `chore` | Tooling, dependencies, maintenance |
| `perf` | Performance optimization |
| `ci` | CI/CD |

## Standards for a Good Subject

A good subject should:

- Reveal the intent of the change
- Be specific enough in scope
- Be understandable without context
- Avoid meaningless expressions like `update`, `misc`, `wip`

Not recommended:

```text
update
fix bug
misc changes
wip
```

Recommended:

```text
fix(order): reject expired timeout config
docs(ai): add git workflow for coding agents
test(auth): cover expired token case
```

## How to Write Commits During AI Programming

When AI modifies many files at once, do not commit them all as one large commit directly.

Split them by intent:

```text
test(order): cover timeout validation
fix(order): reject expired timeout config
docs(order): explain timeout behavior
```

For splitting methods, see [AI Commit Splitting](../../05-ai-native-development/05-ai-native-development_en/ai-commit-splitting_en.md).

## Templates

See [Commit Message Convention](../../08-templates/08-templates_en/commit-message-convention_en.md).

## Further Reading

- [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/)
- [How to Write a Git Commit Message](https://cbea.ms/git-commit/)
- [git commit official documentation](https://git-scm.com/docs/git-commit)
- [Recommended Reading Index](../../09-resources/09-resources_en/recommended-reading_en.md)
