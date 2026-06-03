# AI-Generated Code Review Checklist

English | [中文](../ai-code-review-checklist.md)

## Diff Quality

- [ ] The change is small enough to review
- [ ] Unrelated changes are split out
- [ ] Generated code is not blindly accepted
- [ ] Formatting noise is removed

## Behavior Changes

- [ ] Existing behavior is preserved unless intentionally changed
- [ ] Public API changes are documented
- [ ] Edge cases are considered
- [ ] Error handling is explicit

## Tests

- [ ] Tests cover the changed behavior
- [ ] Tests are not superficial
- [ ] Tests fail before the fix and pass after the fix when applicable
- [ ] Manual verification is documented when automated tests are unavailable

## Security

- [ ] No secrets are committed
- [ ] No unsafe input handling is introduced
- [ ] No new dependency risk is introduced
- [ ] Sensitive logs are not added

## Maintainability

- [ ] The code follows existing style
- [ ] Naming is clear
- [ ] No unnecessary abstraction is introduced
- [ ] Generated comments are useful and accurate

## Final Decision

- [ ] Human reviewer understands and accepts the change
