# How to Review AI-Generated Code

AI 生成代码的危险点，是它经常在“看起来合理”的状态下改变边界、语义、依赖和长期维护成本。

Review AI 代码时，先审意图，再审 diff，再审验证。

## 1. Review 顺序

### 先理解意图

先问：

- 这次要解决什么问题
- 成功标准是什么
- 哪些行为不应该变化
- 影响范围有哪些

没有明确意图的 AI diff，先不要进入代码细节。

### 再看 diff 大小

```bash
git diff --stat
```

如果文件数量太多，先拆：

- 行为修复
- 测试补充
- 重构清理
- 文档说明
- 依赖或配置调整

### 再看行为变化

重点检查：

- public API
- 错误码
- 配置默认值
- 数据库读写
- 并发和重试
- 权限和安全
- 兼容性

### 最后看测试

AI 写的测试容易只验证“它刚写出来的实现”，不验证真实业务边界。

好的测试应该能回答：

- 修复前会失败吗
- 覆盖了异常路径吗
- 覆盖了边界条件吗
- 是否只是在 mock 里自证正确

## 2. 高风险信号

- 大量无关格式化
- 一次改多个业务问题
- 新增抽象但只有一个调用点
- 改配置却没有说明运行时影响
- 修改锁文件但没有说明依赖变化
- 新测试没有断言核心行为
- 删除异常处理或吞掉错误
- 修改 public API 没有兼容说明
- 出现硬编码 token、key、账号、内部地址

## 3. Review 清单

- [ ] 我能用一句话说清这次变更的目标
- [ ] diff 可以在合理时间内审完
- [ ] 无关改动已拆出去
- [ ] 行为变化被明确标注
- [ ] 错误处理没有变弱
- [ ] 测试能证明真实行为
- [ ] 没有新增敏感信息
- [ ] 没有引入不必要依赖
- [ ] 回滚路径清楚

## 4. Prompt 示例

### 让 AI 做风险 Review

```text
请审查当前 git diff。
只输出具体风险，不做泛泛总结。
重点检查：行为边界、兼容性、错误处理、测试有效性、安全风险、无关变更。
每个问题给出文件路径、风险说明、建议修改方式。
```

### 让 AI 拆 commit

```text
请基于当前 git diff，建议如何拆成多个逻辑 commit。
每个 commit 给出标题、包含文件、拆分理由。
不要修改文件。
```

### 让 AI 生成 PR 描述

```text
请基于当前 git diff 生成 PR 描述。
包含 What changed、Why、How tested、Risk、Rollback plan。
对无法从代码确认的内容标注“需要人工补充”。
```

## 5. 人类承担最终责任

AI 可以帮助你更快发现问题，但它不能替你承担合入责任。

最终 reviewer 至少要确认：

- 自己理解这次变更
- 验证结果可信
- 风险和回滚方案可接受
- 合入后出现问题能定位责任边界

## 6. AI Review 工具怎么用

AI Review 工具适合做第一轮扫描，尤其是发现明显 bug、测试缺口、安全风险、无关改动和可维护性问题。

团队使用时要保留三条边界：

1. AI Review 结果不能直接等同于 owner 批准
2. 高风险目录仍要走人类 owner Review
3. AI Review 的误报和漏报要定期复盘

建议把 AI Review 结果放进 PR 流程，但不要让它替代人类合入判断。

## 延伸阅读

- [AI Code Review Checklist](../08-templates/ai-code-review-checklist.md)
- [AI 变更审查实战样例](ai-change-review-example.md)
- [Pull Request Template](../08-templates/pull-request-template.md)
- [Responsible use of GitHub Copilot code review](https://docs.github.com/en/copilot/responsible-use/code-review)
- [Review AI-generated code](https://docs.github.com/en/enterprise-cloud@latest/copilot/tutorials/review-ai-generated-code)
- [AI 编程工具的 Git 集成实践](ai-coding-tools-git-integration.md)
- [推荐阅读索引](../09-resources/recommended-reading.md)
