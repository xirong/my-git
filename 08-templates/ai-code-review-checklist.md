# AI 生成代码 Review 清单

## Diff 质量

- [ ] The change is small enough to review
- [ ] Unrelated changes are split out
- [ ] Generated code is not blindly accepted
- [ ] Formatting noise is removed

## 行为变化

- [ ] Existing behavior is preserved unless intentionally changed
- [ ] Public API changes are documented
- [ ] Edge cases are considered
- [ ] Error handling is explicit

## 测试

- [ ] Tests cover the changed behavior
- [ ] Tests are not superficial
- [ ] Tests fail before the fix and pass after the fix when applicable
- [ ] Manual verification is documented when automated tests are unavailable

## 安全

- [ ] No secrets are committed
- [ ] No unsafe input handling is introduced
- [ ] No new dependency risk is introduced
- [ ] Sensitive logs are not added

## 可维护性

- [ ] The code follows existing style
- [ ] Naming is clear
- [ ] No unnecessary abstraction is introduced
- [ ] Generated comments are useful and accurate

## 最终决定

- [ ] Human reviewer understands and accepts the change
