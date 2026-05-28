# Google Code Review 实践

原文链接：

- [Google Engineering Practices](https://google.github.io/eng-practices/)
- [Google Code Review Introduction](https://google.github.io/eng-practices/review/)
- [The Standard of Code Review](https://google.github.io/eng-practices/review/reviewer/standard.html)

## 1. 最核心的判断

Google Code Review 文档最值得借鉴的地方，是它把代码审查的目标放在长期 code health 上。

这意味着 reviewer 的重点不是把每个 PR 打磨到完美，重点是判断这次变更是否让系统整体变得更好。

企业团队很容易把 Review 做成挑刺流程，最后所有人都慢下来。Google 这套文档提醒我们，Review 需要同时平衡两件事：

- 代码库长期健康
- 开发者可以持续推进工作

## 2. Reviewer 应该看什么

可以拆成这几类：

| 维度 | 关注点 |
| --- | --- |
| 设计 | 方案是否适合当前系统 |
| 正确性 | 是否真的解决问题，是否引入新 bug |
| 复杂度 | 是否过度设计，是否让维护成本上升 |
| 测试 | 是否覆盖关键行为和边界 |
| 命名 | 是否清楚表达意图 |
| 风格 | 是否符合团队已有规范 |
| 文档 | 对外行为或复杂逻辑是否说明清楚 |

## 3. 不要追求“完美 PR”

Review 的目标不是让代码毫无瑕疵。

如果一个变更整体上改善了系统，并且没有明显降低可维护性，reviewer 应该倾向于放行，同时把非关键建议标成可选改进。

团队可以采用这个规则：

- 阻塞问题：正确性、安全、兼容性、明显维护风险
- 建议问题：命名、局部结构、可读性提升
- 可选问题：风格偏好、轻微优化、非当前 PR 必需内容

这样可以避免 reviewer 把所有评论都变成必须修改。

## 4. 对 AI 生成代码更重要

AI 生成代码看起来常常很完整，但 Review 时仍要回到 code health：

- 有没有引入不必要抽象
- 有没有绕开现有设计
- 有没有让错误处理变弱
- 有没有改出“看起来更通用，实际上更难维护”的代码
- 有没有只补表面测试

AI 代码 Review 要看语法是否合理，更要看长期维护成本是否可接受。

## 5. 企业团队可落地规则

1. Review 评论分级，标清阻塞和建议
2. reviewer 优先看设计、正确性、测试、安全
3. 风格问题尽量交给自动化工具
4. 对非关键建议使用 `nit` 或类似标记
5. 长时间争议要升级到 owner 或技术负责人，不要让 PR 卡死
6. Review 结束时要明确是否可以合入

## 6. 对本仓库的启发

Code Review 是团队工程判断的载体。

好的 Review 既要守住底线，也要让有价值的改动尽快进入主线。
