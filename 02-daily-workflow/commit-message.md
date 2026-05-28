# Commit Message

好的 commit message 让未来的人知道这次变更为什么存在。

它不只是写给现在的 reviewer，也是写给未来排查问题、回滚代码、生成 changelog 的自己和队友。

## 推荐格式

```text
<type>(<scope>): <subject>
```

示例：

```text
feat(auth): add GitHub OAuth login
fix(api): handle empty response
docs(git): add troubleshooting guide
refactor(order): simplify pricing calculation
```

这个格式来自 [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/)，它已经被很多开源项目和自动化发布工具采用。

## 常见 type

| type | 含义 |
| --- | --- |
| `feat` | 新功能 |
| `fix` | Bug 修复 |
| `docs` | 文档 |
| `style` | 纯格式调整 |
| `refactor` | 不改变行为的重构 |
| `test` | 测试 |
| `chore` | 工具、依赖、维护 |
| `perf` | 性能优化 |
| `ci` | CI/CD |

## 好标题的标准

好的标题应该：

- 能看出改动意图
- 范围足够具体
- 不依赖上下文也能理解
- 避免 `update`、`misc`、`wip` 这类无意义表达

不推荐：

```text
update
fix bug
misc changes
wip
```

推荐：

```text
fix(order): reject expired timeout config
docs(ai): add git workflow for coding agents
test(auth): cover expired token case
```

## AI 编程时怎么写 commit

AI 一次改很多文件时，不要直接提交成一个大 commit。

推荐按意图拆分：

```text
test(order): cover timeout validation
fix(order): reject expired timeout config
docs(order): explain timeout behavior
```

拆分方式见 [AI Commit Splitting](../05-ai-native-development/ai-commit-splitting.md)。

## 模板

见 [Commit Message Convention](../08-templates/commit-message-convention.md)。

## 延伸阅读

- [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/)
- [How to Write a Git Commit Message](https://cbea.ms/git-commit/)
- [git commit 官方文档](https://git-scm.com/docs/git-commit)
- [推荐阅读索引](../09-resources/recommended-reading.md)
