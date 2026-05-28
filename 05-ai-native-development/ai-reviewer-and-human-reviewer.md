# AI Reviewer and Human Reviewer

AI Reviewer 适合发现重复问题、检查遗漏、生成 Review 清单。

Human Reviewer 负责判断意图、边界、长期维护成本和是否可以合入。

## AI Reviewer 适合检查

- diff 是否过大
- 是否有无关改动
- 是否有明显 bug
- 是否有测试缺口
- 是否有安全风险
- 是否有风格不一致

## Human Reviewer 负责判断

- 这个需求是否应该这样实现
- 语义边界是否正确
- 抽象是否值得引入
- 风险是否可接受
- 是否允许合入

## 可复用 Prompt

```text
请作为 AI reviewer 审查当前 git diff。
只列出具体风险，按严重程度排序。
每条包含文件位置、问题、建议。
不要输出泛泛的赞美或总结。
```

## 协作原则

AI Reviewer 可以提高检查覆盖面，但不能替代人类 owner 判断。

推荐流程：

1. 作者先自审 diff
2. AI Reviewer 做第一轮风险扫描
3. 作者处理明确问题
4. Human Reviewer 做最终判断
5. CI 和必要手工验证通过后再合入

## 延伸阅读

- [Responsible use of GitHub Copilot code review](https://docs.github.com/en/copilot/responsible-use/code-review)
- [AI 生成代码 Review](ai-generated-code-review.md)
- [AI Code Review Checklist](../08-templates/ai-code-review-checklist.md)
- [推荐阅读索引](../09-resources/recommended-reading.md)
