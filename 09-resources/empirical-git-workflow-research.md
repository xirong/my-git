# Git 工作流经验研究笔记

原文链接：

- [Do Small Code Changes Merge Faster? A Multi-Language Empirical Investigation](https://arxiv.org/abs/2203.05045)
- [The Impact of a Continuous Integration Service on the Delivery Time of Merged Pull Requests](https://arxiv.org/abs/2305.16365)

## 1. 小 PR 一定合并更快吗

不应这样写。

公开研究显示，变更大小和合并耗时之间没有稳定的简单关系。

这不代表小 PR 没价值。它真正稳定的价值在于：

- 更容易理解
- 更容易 Review
- 更容易定位问题
- 更容易回滚
- 更适合堆叠审查
- 更适合 AI 生成代码后的人工拆分

所以手册里推荐小 PR，理由应放在可审查性和可回滚性上，不要机械承诺吞吐速度一定提升。

## 2. CI 一定让交付更快吗

也不应这样写。

CI 的价值不只体现在交付时间上，更重要的是：

- 提升合入决策质量
- 提高作者和 reviewer 对变更的信心
- 提前发现编译、测试、格式和安全问题
- 让主分支稳定性有自动化基础

CI 变慢或不稳定时，甚至会拖慢团队节奏。

## 3. 写作时应该怎么表达

建议这样写：

- 小 PR 提升可理解性、可审查性和可回滚性
- CI 提升合入决策质量和开发者信心
- Merge Queue 保护主分支组合结果
- CODEOWNERS 让真正理解代码的人参与 Review
- Rulesets 把组织级规则固化到平台

避免这样写：

- 小 PR 一定更快合并
- 上 CI 就一定更快发布
- 分支越少团队越高效
- 工具开得越多治理越成熟

## 4. 对 AI 编程的启发

AI 生成代码后，小 PR 和小 commit 更重要，但理由仍然是可审查、可验证、可回滚。

不要把 AI 生成速度当成合入速度。合入速度取决于：

- diff 是否可理解
- 测试是否可信
- CI 是否稳定
- owner 是否能快速判断风险
- 回滚是否简单
