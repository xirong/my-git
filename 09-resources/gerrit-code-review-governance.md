# Gerrit 代码评审治理参考

原文链接：

- [Gerrit Code Review: Access Controls](https://gerrit-review.googlesource.com/Documentation/access-control.html)
- [Go Contribution Guide](https://go.dev/doc/contribute)

## 1. 为什么需要 Gerrit 对照

GitHub 的优势是平台体验和生态整合。

Gerrit 的优势是评审和权限语义更细，适合强流程、强权限、强审查的团队。

对企业团队来说，比较二者是为了理解不同工具背后的治理模型，避免简单选边站。

## 2. Gerrit 的典型特点

| 能力 | 含义 |
| --- | --- |
| 组级权限 | 权限通常授予组，避免散落到个人 |
| Code-Review label | 评审意见可以分级，比如 -2 到 +2 |
| Submit 权限 | Review 通过和最终提交可以分离 |
| Service Users | 自动化系统使用专门身份 |
| Project ACL | 项目、分支、引用可以有细粒度权限 |

这套模型更像评审中枢，适合需要明确授权和审查等级的组织。

## 3. 和 GitHub 的差异

GitHub 更自然的路径是：

```text
branch -> pull request -> review -> status checks -> merge
```

Gerrit 更强调：

```text
change -> labels -> votes -> submit requirements -> submit
```

GitHub 适合统一开发平台，Gerrit 适合把 Review 作为强约束流程。

## 4. 企业团队可以借鉴什么

即使不用 Gerrit，也可以借鉴这些思想：

- Review 结果分级，不是所有评论都同等重要
- 最终合入权限和普通 Review 权限分开
- 自动化账号使用专门身份
- 高风险分支和目录使用更细权限
- 审查记录要能解释“谁批准了什么”

## 5. 对 GitHub 团队的迁移启发

如果团队使用 GitHub，可以用这些能力模拟一部分 Gerrit 治理：

- CODEOWNERS 表达路径责任
- Branch Protection 要求 owner Review
- Rulesets 统一组织级规则
- Required status checks 固定自动化检查
- Environment protection rules 控制部署审批
- Merge Queue 验证合入组合结果

## 6. 适合放在哪些文章里

这个对照适合补充到：

- GitHub 工程治理
- Code Review 最佳实践
- CODEOWNERS
- Rulesets
- 企业协作配置栈
